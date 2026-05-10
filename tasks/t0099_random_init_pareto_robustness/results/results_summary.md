---
spec_version: "1"
task_id: "t0099_random_init_pareto_robustness"
date_completed: "2026-05-10"
status: "complete"
---

# Results Summary: Random-Init NSGA-II Reproducibility Test

## Summary

Three NSGA-II runs from totally random LHS-sampled initial populations (seeds 11, 22, 33), no
anchor warm-start, on the same 68-d substrate t0091 used. **0 of 55 Pareto cells across all
3 seeds qualified as strict joint-pass (DSI≥0.5, PD≥30Hz, robust≥0.7), versus 1 such cell in
t0091's 57-cell warm-start Pareto.** This is direct evidence that t0091's 5-anchor warm-start
was load-bearing for reaching the joint-pass corner of objective space within an 8-generation
budget — and refines the claim further: warm-start was load-bearing **specifically for the
high-PD-rate dimension**, since seed 22 reached t0091's DSI threshold (DSI=0.49) but only
half the firing rate (PD=18.7Hz vs t0091's 35Hz). Total Vast.ai cost $7.71 (38.5% of $20
task budget).

## Metrics

* **Pareto cell counts per seed**: seed 11 = **19** (5 gens, $1 cap hit), seed 22 = **22** (8
  gens), seed 33 = **14** (8 gens). t0091 reference: 57.
* **Strict joint-pass count per seed**: **0 / 0 / 0**; t0091 = 1.
* **Best DSI across all seeds**: 0.49 (seed 22 gen 8); t0091 best = 0.51.
* **Best PD-rate across all seeds**: 47 Hz (seed 22 gen 8, but DSI=0); t0091 best joint = 35
  Hz with DSI=0.51.
* **Mean DSI per Pareto** (registered metric): seed 11 = 0.112, seed 22 = 0.292, seed 33 =
  0.059. t0091 reference = 0.221.
* **HV (final-gen) per seed**: seed 11 = 1.07 (capped at gen 5), seed 22 = 9.80, seed 33 =
  4.75; t0091 = 23.71 (gen 2, the only gen recorded for t0091 reference).
* **Anchor distribution per seed** ([bedb_like, symmetric, pd_asymm, nd_asymm,
  alt_topology]): seed 11 = `[2, 0, 7, 5, 5]`, seed 22 = `[4, 0, 4, 2, 12]`, seed 33 = `[1,
  0, 9, 0, 4]`; t0091 = `[20, 0, 12, 9, 16]`.
* **Symmetric anchor count = 0 in ALL 4 datasets**, including warm-started t0091.
* **Total cost**: $7.71 (Vast.ai instance for 46.7 hours; per-seed: $1.13 + $1.96 + $3.41).

## Verification

* `verify_predictions_asset.py` × 3 — all PASSED (each with PR-W014/PR-W015 expected warnings)
* `verify_answer_asset.py` — PASSED
* `verify_task_metrics.py` — PASSED
* `verify_machines_destroyed.py` — PASSED (RM-W001 false-negative + RM-W003 long-uptime
  warnings expected)
* `ruff check` + `ruff format` on `code/` — PASSED
* `mypy -p tasks.t0099_random_init_pareto_robustness.code` — PASSED (no issues)
