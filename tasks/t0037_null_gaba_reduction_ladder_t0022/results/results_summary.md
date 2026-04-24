---
spec_version: "2"
task_id: "t0037_null_gaba_reduction_ladder_t0022"
date_completed: "2026-04-24"
status: "complete"
---
# Results Summary: Null-GABA Reduction Ladder on t0022 DSGC

## Summary

Swept `GABA_CONDUCTANCE_NULL_NS` across 5 levels {4, 2, 1, 0.5, 0} nS at baseline diameter on t0022
(600 trials). **S-0036-01 rescue hypothesis CONFIRMED**: null firing unpinned at every tested level
(6-15 Hz vs t0036's 0 Hz at 6 nS baseline). The **operational sweet spot is 4 nS**: DSI=0.429, peak
15 Hz, null 6 Hz, preferred direction ~40° — biologically realistic DSGC regime. At ≤ 2 nS the cell
fires everywhere and preferred direction randomises. The follow-up recommendation is to **rerun
t0030's 7-diameter sweep at GABA=4 nS** to measure the Schachter2010 vs passive-filtering slope.

## Metrics

* **GABA unpinning threshold**: **≤ 4.0 nS** (highest tested level with null firing already
  unpinned). t0036's 6 nS was just above this threshold.
* **Null firing rate by GABA**: **15, 14, 15, 14, 6 Hz** at {0, 0.5, 1, 2, 4} nS — all ≥ critical
  0.1 Hz unpinning threshold.
* **Primary DSI by GABA**: **0.167, 0.200, 0.157, 0.243, 0.429** — DSI peaks at 4 nS and collapses
  below 2 nS as preferred direction randomises.
* **Preferred-direction angle stability**: stable at 40.8° only at 4 nS; drifts to 187-278° at lower
  GABA levels (directional tuning lost).
* **Vector-sum DSI**: **0.058, 0.069, 0.099, 0.093, 0.259** — tracks primary DSI, peaks at 4 nS.
* **Classification**: `unpinned` label emitted; threshold=0.0 nS auto-reported (but operational
  sweet spot is 4 nS per DSI / preferred-direction stability).
* **Total trials executed**: **600** (5 GABA levels × 12 directions × 10 trials).
* **Sweep wall time**: approximately **20 minutes** on local Windows CPU.

## Verification

* `verify_task_file.py` — target 0 errors.
* `verify_task_dependencies.py` — PASSED (t0022 + t0036 completed).
* `verify_research_code.py` — PASSED.
* `verify_plan.py` — PASSED.
* `verify_task_results.py` — PASSED.
* `verify_task_folder.py` — target 0 errors.
* `verify_logs.py` — target 0 errors.
* `ruff check --fix`, `ruff format`, `mypy -p tasks.t0037_null_gaba_reduction_ladder_t0022.code` —
  all clean (11 files).
* Pre-condition gate: **PASSED** (null_hz ≥ 0.1 at every level; peak_hz ≥ 10 at the highest tested
  level; no AssertionError during 600 trials).
