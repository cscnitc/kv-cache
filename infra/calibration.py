"""Sanity check: cache-hit and cache-miss TTFTs should be clearly separate."""
import csv
import json
import os
import random
import statistics as st
import time

import config
import harness

def random_prompt():
    # Random from token 0 (caching matches from the start), same length every time.
    return [random.randint(1000, 100_000) for _ in range(config.PROMPT_TOKENS)]


def main():
    hit_prompt = random_prompt()

    for _ in range(config.WARMUP):          # discarded
        harness.measure_ttft(random_prompt())
    harness.measure_ttft(hit_prompt)        # puts hit prompt in the cache, discarded

    rows = []
    for i in range(config.N_MEASUREMENTS):
        order = ["hit", "miss"]
        random.shuffle(order)               # interleave so drift/noise affects both equally
        for kind in order:
            prompt = hit_prompt if kind == "hit" else random_prompt()
            rows.append({"trial": i, "kind": kind, "ttft_ms": harness.measure_ttft(prompt) * 1000})
            time.sleep(0.1)

    hit = [r["ttft_ms"] for r in rows if r["kind"] == "hit"]
    miss = [r["ttft_ms"] for r in rows if r["kind"] == "miss"]
    summary = {
        k: {"mean": st.mean(v), "median": st.median(v), "std": st.stdev(v), "min": min(v), "max": max(v)}
        for k, v in (("hit", hit), ("miss", miss))
    }
    summary["separated"] = max(hit) < min(miss)  # no overlap at all

    os.makedirs(config.EVAL_DIR, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    with open(f"{config.EVAL_DIR}/samples_{stamp}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["trial", "kind", "ttft_ms"])
        w.writeheader()
        w.writerows(rows)
    with open(f"{config.EVAL_DIR}/summary_{stamp}.json", "w") as f:
        json.dump(summary, f, indent=2)

    for k in ("hit", "miss"):
        s = summary[k]
        print(f"{k:5s} median {s['median']:7.1f} ms  mean {s['mean']:7.1f}  std {s['std']:6.1f}  "
              f"range [{s['min']:.1f}, {s['max']:.1f}]")
    print("SEPARATED" if summary["separated"] else "OVERLAP: distributions are not clearly separate")


if __name__ == "__main__":
    main()
