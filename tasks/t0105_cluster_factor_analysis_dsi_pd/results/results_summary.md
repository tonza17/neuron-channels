# Results Summary: t0105 — Cluster + Factor Analysis of High-DSI/High-PD Cells

## Summary

t0105 pools 7,003 per-cell evaluations from four 68-d NSGA-II lineages (t0091, t0099, t0102, t0104),
applies a silence-artifact filter (73 cells excluded) plus the primary cohort filter
`DSI > 0.1 AND PD > 2 Hz` with dedupe by 68-d vector to land at **N=85 unique cells**, and runs
asymmetry classification, PCA on the 54-d electrophys submatrix, and varimax factor analysis on the
full 68-d matrix. PC1 separates the 20 symmetric and 65 asymmetric cells at **Mann-Whitney U=31.0,
p=1.48e-10**, top-loading Ca-activated K-channels (SK_TERMINAL, BK_TERMINAL, SK_SOMA, BK_MID) and
persistent Na (NAP_PRIMARY) — morphology class pre-selects a different electrophys regime. **No
factor** exceeds |r| > 0.3 on both DSI and PD, so the joint-DSI/PD corner has no single-axis driver
in the substrate.

## Metrics

* **Primary cohort N**: **85 unique cells** (t0091=26, t0099=20, t0102=19, t0104=20); strict cohort
  N=30
* **Silence-artifact exclusions**: **73 cells** (t0091=5, t0099=23, t0102=45, t0104=0) — t0104's
  S-0102-01 guard fully holds
* **Asymmetry class counts** (threshold 0.5): **20 symmetric, 65 asymmetric**; all 20 symmetric
  cells come from t0091
* **PCA variance explained**: PC1=**29.5 %**, PC2=8.4 %, PC3=6.1 %
* **PC1 Mann-Whitney U**: U=**31.00**, p=**1.48e-10**; PC2 p=0.78 (no separation on PC2)
* **Strict cohort PC1 separation**: U=10.00, p=**8.23e-5** (preserved at N=30)
* **Factor count (Kaiser, capped at 10)**: **10 factors**; 18 eigenvalues exceeded 1.0
* **Top DSI factor**: F1 r=**-0.322**, p=0.003; **Top PD factor**: F1 r=**-0.265**, p=0.014
* **Joint DSI-PD factors** (|r| > 0.3 on both): **0**
* **Bootstrap-stable factors** (200 resamples): F1, F2 only — F3 through F10 are unstable at N=85
* **Total task cost**: **$0.00** (pure local analysis, no remote machines)

## Verification

* `verify_task_results.py` — PASSED (see verificator log for codes)
* `verify_suggestions.py` — PASSED (0 errors)
* `verify_compare_literature.py` — PASSED (0 errors)
* `verify_task_metrics.py` — PASSED (multi-variant `primary_cohort` + `strict_cohort`)
* Answer asset `symmetric-vs-asymmetric-electrophys-cluster` — PASS
* Answer asset `dsi-pd-diversity-factor-decomposition` — PASS
