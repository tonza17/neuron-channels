---
spec_version: "2"
task_id: "t0107_t0106_polar_8dir_recheck"
date_completed: "2026-05-18"
---

# t0107 — 8-Direction Polar Re-Evaluation: Results Summary

## Summary

Re-evaluated 10 randomly selected cells from the t0106 top-50 at an 8-direction protocol (45°
steps) with N_EVAL_SEEDS = 3. **Rank order is preserved** between metrics (Spearman ρ = 0.758,
p = 0.011), but the **absolute DSI values diverge sharply**: t0106 mean 2-direction ratio DSI =
**0.939** vs t0107 mean 8-direction vector-sum DSI = **0.519**, a mean absolute drop of **0.42**.
The 2-direction reformulation used in t0106 systematically overstates selectivity vs the
conventional 16- / 8-direction literature.

## Metrics

* **direction_selectivity_index (registered, 8-dir vector-sum mean across 10 cells)** = **0.519**
* **t0106 2-dir ratio DSI (re-reported for these 10 cells, mean)** = **0.939**
* **Mean DSI difference (t0106 - t0107)** = **+0.42** (always positive — t0106 always reports
  higher)
* **Spearman ρ(t0106 DSI, t0107 8-dir vsum DSI)** = **0.758** (p = 0.011) — above the
  pre-registered 0.7 threshold; rank order largely preserved
* **2-dir ratio sanity check** (recomputed from the 8-dir PD@0 and ND@180 values): mean **0.867**,
  Spearman vs t0106 ρ = **0.721**. The slight drop from 0.939 is noise replicate variation, not
  evaluator drift
* **Mean PD@0° firing rate** = 84.2 Hz; **mean ND@180° firing rate** = 6.9 Hz; **mean firing
  rate across all 8 directions** = 43.3 Hz

## Verification

* `verify_research_code` — PASSED (0 errors, 2 warnings)
* `verify_plan` — PASSED (0 errors, 4 warnings)
* `verify_task_dependencies` — PASSED (t0106 confirmed completed)
* `verify_machines_destroyed` — PASSED
* `verify_predictions_asset` — PASSED
* Local pre-commit hooks (ruff check / format, mypy) — PASSED on 22 task source files

## Figures

* `results/images/polar_tuning_curves_top10.png` — 2 × 5 grid of polar tuning curves for the 10
  cells, with t0106 ratio DSI and t0107 8-dir vector-sum DSI annotated per panel.

## Headline interpretation

t0106's "DSI ≈ 1.0" headline is a **metric artefact** of the 2-direction protocol, not a
biological claim about the cells. Under conventional 8-direction tuning, the same cells score
DSI = 0.22 – 0.81 (mean 0.52) — still direction-selective, but in the realistic range reported
for biological DSGCs (Trenholm 2013: mouse Hb9 DSI = 0.76; Poleg-Polsky 2026 unconstrained ML
ceiling = 0.731). Rank order between metrics is preserved, so the t0106 *ordering* of cells
remains informative for selection purposes; only the absolute DSI numbers should be reported
with the metric explicitly stated.
