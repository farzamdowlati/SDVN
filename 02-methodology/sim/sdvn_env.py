"""SDVN control-plane load-balancing environment (tier 1: abstract discrete tick).

Implements the frozen spec in 02-methodology/env-spec-2026-09-19.md:
K controllers, R RSUs (data-plane switches) partitioned across controllers,
V vehicles moving on a ring road, nearest-RSU association with hysteresis,
handover registration bursts, Poisson control-plane demand, M/M/1-style
controller queues, and a switch-migration actuator with cost + cooldown.

Deterministic: every run is reproducible from Config.seed.

Usage:
    cfg = Config(vehicles=300, ticks=1800)
    env = SDVNEnv(cfg)
    obs = env.reset()
    for _ in range(cfg.ticks):
        obs, r, done, info = env.step(0)
    print(env.metrics())
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, field, asdict
from typing import Any

import numpy as np


@dataclass
class Config:
    # topology
    K: int = 3                 # controllers
    R: int = 15                # RSUs / switches
    vehicles: int = 300
    road_len: float = 3000.0   # metres, circular road
    # mobility
    speed_mean: float = 13.0   # m/s (~47 km/h)
    speed_sd: float = 5.0
    hysteresis: float = 0.10   # re-associate only if >10% closer
    # demand
    per_vehicle_rate: float = 0.20   # control msgs / vehicle / tick (Poisson mean)
    handover_burst: float = 3.0      # extra msgs per handover event
    hotspot_rsus: int = 4            # how many RSUs sit in the demand hotspot
    hotspot_mult: float = 3.0        # their demand multiplier (spatial imbalance)
    # controllers  (mu is derived from density unless mu_override is set)
    mu_override: float = 0.0   # 0 -> compute mu from target_util
    target_util: float = 0.80  # reference controller utilisation at mean demand
    capacity_mult: float = 2.0 # overload threshold = capacity_mult * mu
    queue_cap_mult: float = 4.0 # hard queue cap = queue_cap_mult * mu; overflow counts as packet loss
    mu: float = 45.0           # service rate (msgs/tick) - set in reset()
    capacity: float = 120.0    # queue length that counts as "overloaded" - set in reset()
    # actuator
    mig_cost_msg: float = 4.0
    mig_cost_sync: float = 0.06   # per unit of in-flight state transferred
    cooldown: int = 30         # ticks before the same switch may move again
    s_cand: int = 3           # most-loaded switches exposed as action candidates
    # reward
    w_jain: float = 1.0
    w_cost: float = 0.05
    w_overload: float = 0.5
    w_remig: float = 0.5
    # observation
    window: int = 8            # ticks stacked per feature
    telemetry_dropout: float = 0.0   # p(drop) for neighbour telemetry blocks
    # run
    ticks: int = 3600
    seed: int = 0

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=1)


@dataclass
class StepInfo:
    overload_events: int = 0
    overload_onset: list[int] = field(default_factory=list)
    migrations: int = 0
    migration_cost: float = 0.0
    remigrations: int = 0


class SDVNEnv:
    """Discrete-tick SDVN control-plane load-balancing environment."""

    #: per-controller observation block layout (documented for the agent)
    OBS_FIELDS = ["queue", "arrival_ewma", "service_rate", "overload_flag",
                  "vehicles_in_zone", "handover_in_rate", "ticks_since_migration"]

    def __init__(self, cfg: Config | None = None):
        self.cfg = cfg or Config()
        c = self.cfg
        if c.R % c.K:
            raise ValueError("R must be divisible by K")
        self.rng = np.random.default_rng(c.seed)
        self.rsu_pos = np.linspace(0, c.road_len, c.R, endpoint=False)
        self.rsu_ctrl = np.repeat(np.arange(c.K), c.R // c.K)      # controller of each RSU
        # spatial demand heterogeneity: a contiguous hotspot block (city-centre RSUs)
        w = np.ones(c.R)
        h = min(c.hotspot_rsus, c.R)
        start = max(0, c.R // 2 - h // 2)
        w[start:start + h] = c.hotspot_mult
        self.rsu_weight = w
        self.reset()

    # ---------------------------------------------------------------- mechanics
    def reset(self) -> dict[str, Any]:
        c = self.cfg
        self.t = 0
        # service rate sized from mean demand so utilisation = target_util at the
        # reference (uniform) vehicle distribution; mobility/hotspots create the imbalance
        mean_demand = c.vehicles * c.per_vehicle_rate * float(self.rsu_weight.mean())
        c.mu = c.mu_override if c.mu_override > 0 else mean_demand / (c.target_util * c.K)
        c.capacity = c.capacity_mult * c.mu
        self.veh_pos = self.rng.uniform(0, c.road_len, c.vehicles)
        self.veh_speed = np.clip(self.rng.normal(c.speed_mean, c.speed_sd, c.vehicles), 1.0, None)
        self.assoc = self._nearest_rsu(self.veh_pos)
        self.queue = np.zeros(c.K)
        self.arrival_ewma = np.zeros(c.K)
        self.zone_veh = np.zeros(c.R, dtype=int)
        self.handover_in = np.zeros(c.K)          # handovers into each controller this tick
        self.handover_rate = np.zeros(c.K)        # ewma
        self.since_mig = np.full(c.R, 10 ** 6, dtype=float)   # ticks since each RSU moved
        self.last_mig_tick = np.full(c.R, -10 ** 6, dtype=float)  # for re-migration detection
        self._last_remig = False
        self.last_ctrl = self.rsu_ctrl.copy()     # current owner of each RSU
        self.overload_prev = np.zeros(c.K, dtype=bool)
        self.drops = 0.0
        self.arrivals_total = 0.0
        self.served_total = 0.0
        self.overload_ticks = 0
        self.latencies: list[float] = []
        self.jain_hist: list[float] = []
        self.cost_hist: list[float] = []
        self.history: list[np.ndarray] = []       # per-tick per-controller feature rows
        self.overload_onset: list[int] = []
        self.migrations = 0
        self.migration_cost = 0.0
        self.remigrations = 0
        self.trace: list[int] = []
        return self._obs()

    def _nearest_rsu(self, pos: np.ndarray) -> np.ndarray:
        d = np.abs(pos[:, None] - self.rsu_pos[None, :])
        d = np.minimum(d, self.cfg.road_len - d)          # circular distance
        return np.argmin(d, axis=1)

    def _dist_to(self, idx: int, pos: np.ndarray) -> np.ndarray:
        d = np.abs(pos - self.rsu_pos[idx])
        return np.minimum(d, self.cfg.road_len - d)

    def _mobility(self) -> None:
        c = self.cfg
        self.veh_pos = (self.veh_pos + self.veh_speed) % c.road_len
        target = self._nearest_rsu(self.veh_pos)
        # hysteresis: keep the old RSU unless the new one is clearly closer
        moved = target != self.assoc
        if moved.any():
            cur_d = self._dist_to_many(self.assoc[moved], self.veh_pos[moved])
            new_d = self._dist_to_many(target[moved], self.veh_pos[moved])
            keep = new_d > (1.0 - c.hysteresis) * cur_d
            target[moved] = np.where(keep, self.assoc[moved], target[moved])
        self.handover_in = np.zeros(c.K)
        changed = target != self.assoc
        if changed.any():
            new_ctrl = self.rsu_ctrl[target[changed]]
            np.add.at(self.handover_in, new_ctrl, 1)
        self.assoc = target

    def _dist_to_many(self, idx: np.ndarray, pos: np.ndarray) -> np.ndarray:
        d = np.abs(pos - self.rsu_pos[idx])
        return np.minimum(d, self.cfg.road_len - d)

    def _demand(self) -> np.ndarray:
        c = self.cfg
        self.zone_veh = np.bincount(self.assoc, minlength=c.R)
        lam_rsu = self.zone_veh * c.per_vehicle_rate * self.rsu_weight
        # handover registration bursts land on the receiving controller
        burst = self.handover_in.astype(float) * c.handover_burst
        owner = self.last_ctrl                                  # RSU -> controller now
        lam_ctrl = np.bincount(owner, weights=lam_rsu, minlength=c.K) + burst
        self.handover_rate = 0.7 * self.handover_rate + 0.3 * self.handover_in
        return lam_ctrl

    def _serve_and_queue(self, lam: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        c = self.cfg
        arrivals = self.rng.poisson(np.maximum(lam, 0.0))
        self.queue += arrivals
        qmax = c.queue_cap_mult * c.mu
        overflow = np.maximum(self.queue - qmax, 0.0)     # dropped: finite control-plane queue
        self.drops += float(overflow.sum())
        self.served_total += float(np.minimum(self.queue, c.mu).sum())
        self.arrivals_total += float(arrivals.sum())
        self.queue = np.minimum(self.queue, qmax)
        served = np.minimum(self.queue, c.mu)
        self.queue -= served
        lat = self.queue / c.mu                      # normalised waiting time
        self.latencies.extend(lat.tolist())
        return arrivals, lat

    def _jain(self, x: np.ndarray) -> float:
        x = np.asarray(x, dtype=float)
        s = x.sum()
        if s <= 0:
            return 1.0
        return float(x.sum() ** 2 / (len(x) * (x ** 2).sum()))

    # ------------------------------------------------------------------ actuator
    def legal_actions(self) -> list[tuple[int, int]]:
        """[(switch, target_controller)] for the s_cand most-loaded switches."""
        c = self.cfg
        loads = np.array([self._rsu_load_est(r) for r in range(c.R)])
        cand = np.argsort(-loads)[: c.s_cand]
        acts = []
        for s in cand:
            if self.since_mig[s] < c.cooldown:
                continue
            for j in range(c.K):
                if j != self.last_ctrl[s]:
                    acts.append((int(s), int(j)))
        return acts

    def _rsu_load_est(self, r: int) -> float:
        return float(self.zone_veh[r] * self.cfg.per_vehicle_rate * self.rsu_weight[r])

    def _apply_migration(self, switch: int, target: int) -> float:
        c = self.cfg
        src = int(self.last_ctrl[switch])
        if self.since_mig[switch] < c.cooldown:
            return 0.0                                     # illegal -> no-op
        state = float(self.zone_veh[switch] * c.per_vehicle_rate * self.rsu_weight[switch])
        cost = c.mig_cost_msg + c.mig_cost_sync * state
        remig = (self.t - self.last_mig_tick[switch]) < 2 * c.cooldown
        self.last_ctrl[switch] = target
        self.since_mig[switch] = 0
        self.last_mig_tick[switch] = self.t
        self.migrations += 1
        self.migration_cost += cost
        self.remigrations += int(remig)
        self._last_remig = bool(remig)
        return cost

    # ------------------------------------------------------------------- RL API
    def obs_dim(self) -> int:
        return self.cfg.K * len(self.OBS_FIELDS) + self.cfg.K      # + telemetry mask

    def action_dim(self) -> int:
        return 1 + self.cfg.s_cand * (self.cfg.K - 1)

    def _features(self) -> np.ndarray:
        """[K, F] instantaneous per-controller features."""
        c = self.cfg
        feats = np.zeros((c.K, len(self.OBS_FIELDS)))
        feats[:, 0] = self.queue
        feats[:, 1] = self.arrival_ewma
        feats[:, 2] = np.minimum(c.mu, self.queue + self.arrival_ewma)
        feats[:, 3] = (self.queue > c.capacity).astype(float)
        zone_by_ctrl = np.bincount(self.last_ctrl, weights=self.zone_veh, minlength=c.K)
        feats[:, 4] = zone_by_ctrl
        feats[:, 5] = self.handover_rate
        feats[:, 6] = [np.min(self.since_mig[self.last_ctrl == k]) if (self.last_ctrl == k).any() else 10 ** 6
                       for k in range(c.K)]
        return feats

    def _obs(self) -> dict[str, Any]:
        c = self.cfg
        row = self._features()
        self.history.append(row)
        self.history = self.history[-c.window:]
        win = np.zeros((c.window, c.K, len(self.OBS_FIELDS)))
        win[-len(self.history):] = np.stack(self.history)
        mask = np.ones(c.K)
        if c.telemetry_dropout > 0:
            mask = (self.rng.random(c.K) > c.telemetry_dropout).astype(float)
            mask[0] = 1.0                                   # self-telemetry never drops
        obs = win * mask[None, :, None]
        return {"window": obs.astype(np.float32),          # [window, K, F]
                "mask": mask.astype(np.float32),           # [K]
                "flat": np.concatenate([obs.reshape(-1), mask]).astype(np.float32),
                "legal": self.legal_actions()}

    def step(self, action: int):
        c = self.cfg
        cost = 0.0
        legal = self.legal_actions()
        if action > 0:
            idx = action - 1
            if idx < len(legal):
                s, j = legal[idx]
                cost = self._apply_migration(s, j)
                self.trace.append(action)
        self.since_mig += 1

        self._mobility()
        lam = self._demand()
        arrivals, lat = self._serve_and_queue(lam)
        self.arrival_ewma = 0.7 * self.arrival_ewma + 0.3 * arrivals

        overload = self.queue > c.capacity
        self.overload_ticks += int(overload.sum())
        newly = overload & ~self.overload_prev
        for k in np.flatnonzero(newly):
            self.overload_onset.append(self.t)
        self.overload_prev = overload

        jain = self._jain(self.queue + 1e-9)
        self.jain_hist.append(jain)
        self.cost_hist.append(cost)
        rew = -(c.w_jain * (1.0 - jain)
                + c.w_cost * cost
                + c.w_overload * float(overload.sum())
                + c.w_remig * (1.0 if self._last_remig else 0.0))
        self._last_remig = False
        self.t += 1
        done = self.t >= c.ticks
        info = {"t": self.t, "queue": self.queue.copy(), "jain": jain, "cost": cost,
                "overload": overload.sum(), "legal": len(legal), "reward": rew}
        return self._obs(), float(rew), done, info

    # ------------------------------------------------------------------ reporting
    def metrics(self) -> dict[str, float]:
        lat = np.array(self.latencies) if self.latencies else np.zeros(1)
        jain = np.array(self.jain_hist) if self.jain_hist else np.zeros(1)
        return {
            "jain_mean": float(jain.mean()),
            "jain_p05": float(np.percentile(jain, 5)),
            "p95_latency": float(np.percentile(lat, 95)),
            "overload_events": float(len(self.overload_onset)),
            "overload_ticks": float(self.overload_ticks),
            "migrations": float(self.migrations),
            "migration_cost": float(self.migration_cost),
            "remigrations": float(self.remigrations),
            "handover_total": float(self.handover_rate.sum()),
            "packet_loss_rate": float(self.drops / max(self.arrivals_total, 1.0)),
            "drops": float(self.drops),
        }
