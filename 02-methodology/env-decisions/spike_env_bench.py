"""Spike: pure-Python discrete-tick SDVN control-plane environment.

Purpose: MEASURE whether a lightweight kinematics+arrival model can run RL
training loops at speeds Mininet emulation cannot. Not the thesis
implementation — a throwaway benchmark (per 02-methodology decision doc).

Model per tick (dt = 1 s):
  - N vehicles: pos (x,y), velocity, simple straight-corridor kinematics
    with per-vehicle speed noise (random-walk around cruise).
  - R RSUs at fixed (x,y). Association = nearest RSU with 10% hysteresis
    (handover damping). Handover = control-plane churn event.
  - C controllers partitioning RSUs; switch(=RSU)-to-controller fixed.
  - packet-in arrivals per RSU: Poisson(lambda0 * local_density) per tick
    + handover events -> registration requests.
  - Controller load = served queue: M/M/1-ish exponential service, drain
    min(load, capacity) per tick; load>cap -> overload event.
"""
import numpy as np
import time

rng = np.random.default_rng(42)

def run(n_vehicles=300, n_rsus=15, n_controllers=3, ticks=20000, dt=1.0):
    L = 5000.0  # 5 km corridor
    rsu_x = np.linspace(100, L - 100, n_rsus)
    rsu_ctrl = (np.arange(n_rsus) * n_controllers) // n_rsus  # partition
    x = rng.uniform(0, L, n_vehicles)
    v = rng.normal(14, 3, n_vehicles)            # ~50 km/h
    assoc = np.argmin(np.abs(x[:, None] - rsu_x[None, :]), axis=1)
    ctrl_load = np.zeros(n_controllers)
    overload_events = 0
    handovers = 0
    cap = 400.0  # req capacity per tick per controller (tuned)
    lambda0 = 0.6  # base flow arrival intensity per vehicle-ish

    for t in range(ticks):
        # kinematics (wrap)
        v = np.clip(v + rng.normal(0, 0.5, n_vehicles), 5, 30)
        x = (x + v * dt) % L
        # association with hysteresis: switch only if new best is 10% closer
        d = np.abs(x[:, None] - rsu_x[None, :])
        best = np.argmin(d, axis=1)
        cur = d[np.arange(n_vehicles), assoc]
        sw = best != assoc
        swap = sw & (d[np.arange(n_vehicles), best] < 0.9 * cur)
        newly = np.where(swap)[0]
        handovers += len(newly)
        assoc[newly] = best[newly]
        # arrivals per RSU: Poisson(lambda0 * density) + handover churn
        dens = np.bincount(assoc, minlength=n_rsus)
        hv = np.bincount(assoc[newly], minlength=n_rsus) if len(newly) else np.zeros(n_rsus, int)
        lam = lambda0 * dens + 2.0 * hv
        arrivals = rng.poisson(lam)
        # queue per controller: arrivals minus service
        a_c = np.bincount(rsu_ctrl, weights=arrivals, minlength=n_controllers)
        ctrl_load = np.maximum(0.0, ctrl_load + a_c - np.minimum(ctrl_load + a_c, cap))
        overload_events += int((ctrl_load >= cap).sum())
    return handovers, overload_events, ctrl_load

# --- measure throughput -------------------------------------------------
# warm up
run(n_vehicles=50, ticks=200)

for n in (100, 300, 1000):
    t0 = time.perf_counter()
    hv, ov, ld = run(n_vehicles=n, ticks=10000)
    dt_wall = time.perf_counter() - t0
    tps = 10000 / dt_wall
    print(f"N={n:5d} vehicles: 10k ticks in {dt_wall:6.2f}s  => {tps:8.0f} ticks/s "
          f"(1 sim-hour = {3600/tps:6.2f} wall-sec) | handovers={hv} overload-events={ov}")
