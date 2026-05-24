---
spec_version: "1"
task_id: "t0121_5seed_substrate_rate_canonical_report"
date_completed: "2026-05-24"
status: "complete"
---
# Results Summary: Canonical 5-seed Substrate-Rate Report

## Summary

Consolidated the S-0112-01 5-seed substrate-rate batch (t0106 seed 44, t0112 seed 77, t0113 seed
2247, t0114 seed 7755, t0115 seed 9354) into one canonical report with harmonised LEGIT-only
conventions, both normal-approx and bootstrap 95% CIs, and a literature comparison table against Hay
2011 / Druckmann 2007 / Mohacsi 2024. The bootstrap CI (B=10000, seed=42) excludes 0% (lower bound
+0.38%), strengthening the case that the substrate is more populated than Hay's 0.40% envelope upper
bound, even though the normal-approx CI still brackets 0.

## Metrics

* **Per-seed LEGIT acceptance**: t0106/44 = **3.2318%** (121/3744), t0112/77 = **0.3472%** (7/2016),
  t0113/2247 = **0.0000%** (0/1344), t0114/7755 = **8.1317%** (484/5952), t0115/9354 = **1.1932%**
  (63/5280).
* **5-seed mean**: **2.58%** (sample SD = 3.35%, sample SE = 1.50%).
* **Normal-approx 95% CI**: **(-0.35%, +5.51%)** -- straddles 0%.
* **Bootstrap 95% CI** (B=10000, seed=42): **(+0.38%, +5.53%)** -- excludes 0%; strengthens the
  point estimate.
* **n_seeds above Hay 2011 envelope (0.40%)**: **3** of 5 (seeds 44, 7755, 9354 each independently
  beat the envelope by 8x / 20x / 3x respectively).
* **Convention drift**: seed 7755 silence-guard-included legacy headline 12.95% -> canonical LEGIT
  8.13% (delta -4.82%); seed 44 3.63% -> 3.23% (delta -0.40%); seed 2247 0.15% -> 0.00% (delta
  -0.15%).
* **Pooled cells**: 675 LEGIT joint-pass cells (121 + 7 + 0 + 484 + 63) collected into one parquet
  for downstream analysis.

## Verification

* `verify_research_code` -- PASSED (0 errors, 0 warnings).
* `verify_plan` -- PASSED (0 errors, 0 warnings).
* Local-fallback answer-asset verifier (`meta.asset_types.answer.verificator`) -- PASSED (0 errors,
  0 warnings).
* `ruff check`, `ruff format`, `mypy -p tasks.t0121_5seed_substrate_rate_canonical_report.code` --
  all PASSED on 11 Python files.
* Per-seed counts cross-checked via assert: 121 + 7 + 0 + 484 + 63 = 675 (pooled parquet row count
  matches).
