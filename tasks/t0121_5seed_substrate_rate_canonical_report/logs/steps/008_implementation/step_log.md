---
spec_version: "3"
task_id: "t0121_5seed_substrate_rate_canonical_report"
step_number: 8
step_name: "implementation"
status: "completed"
started_at: "2026-05-24T01:47:20Z"
completed_at: "2026-05-24T02:00:00Z"
---
# Step 8: Implementation

## Summary

Spawned an `/implementation` subagent that ran the full 13-step plan end-to-end. All 16 REQs done;
per-seed canonical numbers reproduce exactly (3.2318% / 0.3472% / 0.0000% / 8.1317% / 1.1932%);
5-seed mean = 2.58% +/- SE 1.50% matching the anchor; bootstrap CI (B=10000, seed=42) = (0.38%,
5.53%); 3 of 5 seeds above Hay envelope. 11 Python files, 5 CSVs, 1 parquet (675 rows), 3 PNGs, and
1 answer asset produced. ruff, mypy, and answer asset verifier all clean.

## Actions Taken

1. Spawned a subagent to execute the `/implementation` skill against task t0121.
2. The subagent wrote 11 Python files under `code/`: `paths.py`, `constants.py`, `seed_metadata.py`,
   `loaders.py`, `per_seed.py`, `stats.py`, `csv_writers.py`, `charts.py`, `answer_asset.py`,
   `main.py`, `__init__.py`.
3. Loaded 5 source-task evaluation JSONs (with prefix-suffix path resolution per t0117 pattern) and
   reproduced all per-seed canonical numbers via asserts.
4. Wrote 5 CSVs (per-seed table, convention drift, substrate stats with both CIs, convergence
   overview, literature comparison) and 1 parquet (pooled LEGIT joint-pass cells, 675 rows).
5. Rendered 3 PNGs (per-seed acceptance bar with literature reference lines, 5-seed HV trajectory
   with pool-restart annotations and Mohacsi convergence band, DSI-vs-PD scatter with threshold
   lines).
6. Wrote 1 answer asset at `assets/answer/substrate-rate-5seed-canonical/` with confidence "medium"
   and 3 paper IDs + 8 task IDs.
7. Ran `ruff check`, `ruff format`, `mypy -p tasks.t0121_*.code`, local answer-asset verifier -- all
   PASSED.

## Outputs

* 11 Python source files in `code/`
* 5 CSV files in `results/data/`
* `results/data/pooled_legit_jointpass_cells.parquet` (675 rows, exact match to 121+7+0+484+63)
* 3 PNGs in `results/images/`
* 1 answer asset at `assets/answer/substrate-rate-5seed-canonical/`
* `tasks/t0121_5seed_substrate_rate_canonical_report/logs/steps/008_implementation/step_log.md`

## Key Numbers

* Per-seed LEGIT acceptance: 44=**3.2318%**, 77=**0.3472%**, 2247=**0.0000%**, 7755=**8.1317%**,
  9354=**1.1932%**.
* 5-seed mean = **2.58%**, SD = **3.35%**, SE = **1.50%**.
* Normal-approx 95% CI = (-0.35%, +5.51%); bootstrap 95% CI (B=10000, seed=42) = (+0.38%, +5.53%) --
  bootstrap excludes 0% while normal-approx straddles it.
* 3 of 5 seeds above Hay 2011 envelope (0.40%).

## Convention drift surfaced

* Seed 7755: legacy silence-guard-included headline 12.95% vs canonical LEGIT 8.13% (delta -4.82%).
* Seed 44: 3.63% legacy vs 3.23% canonical (delta -0.40%).
* Seed 2247: 0.15% legacy vs 0.00% canonical (delta -0.15%).
* Seeds 77 and 9354 unchanged (legacy already LEGIT or LEGIT-by-coincidence).

## Requirement Completion Checklist

All 16 plan REQ-* items marked `done` (see subagent's checklist in return summary).

## Issues

No issues encountered. Minor cosmetic deviation: normal-approx CI is (-0.35, +5.51) vs plan
narrative (-0.36, +5.52) due to z=1.96 rounding -- substantive numbers identical.
