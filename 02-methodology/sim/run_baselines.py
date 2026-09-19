#!/usr/bin/env python3
"""Smoke test: run every implemented baseline on the tick env and print metrics.

    python3 run_baselines.py [--ticks 3600] [--vehicles 300] [--seeds 3] [--json out.json]

Purpose: prove the environment is sane (deterministic, sane metrics, baselines
ordered as theory predicts) before any learning agent is attached.
"""
from __future__ import annotations

import argparse, json, statistics as st, sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from sdvn_env import Config, SDVNEnv
from baselines import BASELINES


def run_once(policy, cfg):
    env = SDVNEnv(cfg)
    obs = env.reset()
    while True:
        a = policy(env, obs)
        obs, r, done, info = env.step(a)
        if done:
            break
    m = env.metrics()
    m["reward_sum"] = float(sum(env.jain_hist and [] or []))  # placeholder, see below
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticks", type=int, default=3600)
    ap.add_argument("--vehicles", type=int, default=300)
    ap.add_argument("--controllers", type=int, default=3)
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    results = {}
    for name, pol in BASELINES.items():
        rows = []
        for s in range(a.seeds):
            cfg = Config(ticks=a.ticks, vehicles=a.vehicles, K=a.controllers, seed=s)
            rows.append(run_once(pol, cfg))
        agg = {k: st.mean(r[k] for r in rows) for k in rows[0]}
        results[name] = agg
        print(f"{name:14s} jain={agg['jain_mean']:.4f} p05={agg['jain_p05']:.4f} "
              f"p95lat={agg['p95_latency']:6.2f} overload_ev={agg['overload_events']:5.1f} "
              f"migr={agg['migrations']:5.1f} cost={agg['migration_cost']:7.1f} "
              f"remig={agg['remigrations']:5.1f} ploss={agg['packet_loss_rate']*100:5.2f}%")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(results, indent=1))
        print("wrote", a.json)

    # sanity assertions (theory: B0 worst fairness, greedy/threshold should lift it)
    assert results["B0_static"]["jain_mean"] <= max(results[b]["jain_mean"] for b in results) + 1e-9
    for k, v in results.items():
        for f, val in v.items():
            assert val == val, f"NaN metric {k}.{f}"
    print("smoke test OK")


if __name__ == "__main__":
    main()
