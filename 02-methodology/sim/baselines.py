"""Baselines B0-B3 for the SDVN tick environment (spec: 02-methodology/env-spec-2026-09-19.md).

Every baseline is a pure function of the environment's *reachable* state, so the
same policy object can be ported to the Mininet-WiFi + Ryu vignette (tier 2).

    B0  static:      never migrate (lower bound)
    B1  greedy:      at every slot, move the most-loaded switch off the most-loaded
                     controller when that strictly lowers the load spread (cost-blind)
    B2  threshold:   migrate only when a controller's queue exceeds `cap` and the
                     least-loaded neighbour has headroom; respects the cooldown
                     (reactive family: EASM / Marwein-class)
    B3  random:      uniform random legal migration (sanity control)

B4 (memoryless DQN), B5 (recurrent DQN) and B6 (Marwein-style hierarchical) are
not in this file: B4/B5 need the agent module, B6 is an analytical re-implementation.
"""
from __future__ import annotations

import numpy as np

from sdvn_env import SDVNEnv


def b0_static(env: SDVNEnv, obs) -> int:
    return 0


def b1_greedy(env: SDVNEnv, obs) -> int:
    """Least-loaded-first, cost-blind: migrate whenever it improves the spread."""
    load = env.queue + env.arrival_ewma
    if load.max() - load.min() < 1e-9:
        return 0
    best, best_gain = 0, 0.0
    for i, (s, j) in enumerate(obs["legal"], start=1):
        before = load.max() - load.min()
        trial = load.copy()
        moved = env.zone_veh[s] * env.cfg.per_vehicle_rate
        trial[env.last_ctrl[s]] -= moved
        trial[j] += moved
        gain = before - (trial.max() - trial.min())
        if gain > best_gain:
            best, best_gain = i, gain
    return best


def b2_threshold(env: SDVNEnv, obs, headroom: float = 0.5) -> int:
    """Reactive threshold migration with cooldown (classical LB family)."""
    c = env.cfg
    load = env.queue
    hot = np.flatnonzero(load > c.capacity)
    if hot.size == 0:
        return 0
    i = int(hot[np.argmax(load[hot])])
    cool = np.flatnonzero(load < headroom * c.capacity)
    if cool.size == 0:
        return 0
    j_target = int(cool[np.argmin(load[cool])])
    best = 0
    for idx, (s, j) in enumerate(obs["legal"], start=1):
        if env.last_ctrl[s] == i and j == j_target:
            best = idx
            break
    return best


def b3_random(env: SDVNEnv, obs) -> int:
    if not obs["legal"]:
        return 0
    return int(env.rng.integers(1, len(obs["legal"]) + 1))


BASELINES = {"B0_static": b0_static, "B1_greedy": b1_greedy,
             "B2_threshold": b2_threshold, "B3_random": b3_random}
