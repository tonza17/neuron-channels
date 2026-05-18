# t0110 — Plan

## Objective

Re-run the t0108 varimax FA pipeline at relaxed thresholds (DSI > 0.2 AND PD > 3) on 247 unique
t0106 cells and compare DSI/PD factor correlations against t0108 strict (DSI > 0.5 AND PD > 10)
to test the truncated-cohort hypothesis.

## Approach

Single Python module (`code/factor_analysis_relaxed.py`) that:

1. Loads t0106 evaluations from main repo.
2. Applies DSI > 0.2 AND PD > 3.
3. Dedupes by 68-d vector at 6 decimals.
4. Runs sklearn FactorAnalysis + manual Kaiser varimax (same routine as t0108 imported by path).
5. Computes Pearson r between factor scores and DSI / PD-rate.
6. Renders a comparison chart against t0108 (left: t0108 strict; right: t0110 relaxed) with the
   same y-axis scale.

## Cost Estimation

| Item | Estimate |
| --- | --- |
| Local compute (FA on 247 x 68) | < 1 minute |
| API costs | $0 |
| **Predicted spend** | **$0** |
| **Hard cap** | **$0** |

## Step by Step

1. Load + filter + dedupe t0106 cells at the relaxed threshold.
2. Run varimax FA; compute Pearson correlations with DSI / PD.
3. Render side-by-side comparison chart against t0108.
4. Write 1 answer asset + results documents.

## Remote Machines

None.

## Assets Needed

* `tasks/t0106_long_pdnd_nsga2_300gen/results/data/all_evaluations_seed44.json.gz`.
* `tasks/t0108_t0106_cluster_factor_dsi05_pd10/results/data/factor_analysis.json` (for comparison).

## Expected Assets

* 1 answer asset: `t0106-pd-correlation-sign-flip-relaxed-cohort` (does the all-negative PD
  column persist?).

## Time Estimation

* Implementation: 20-30 min.
* Reporting: 20-30 min.
* **Total**: ~1 hour wall clock.

## Risks & Fallbacks

* **Risk**: Kaiser cap reduces to fewer factors at N=247 (more cells → potentially fewer
  eigenvalues > 1). **Fallback**: report the natural factor count without forcing parity with
  t0108's 10 factors.
* **Risk**: factor identities differ between t0108 and t0110 (factor numbering is
  rotation-dependent). **Fallback**: compare by *loadings overlap* not by factor index; the
  question is whether *any* factor in the relaxed cohort has positive r(PD).

## Verification Criteria

* `verify_task_complete t0110_relaxed_cohort_factor_analysis` passes with 0 errors.
* The single answer asset validates.
* Comparison chart is embedded in `results_detailed.md`.

## REQ Checklist

* **REQ-1**: Load + filter + dedupe at DSI > 0.2 AND PD > 3; record N_raw, N_passing, N_unique.
* **REQ-2**: Same varimax FA pipeline as t0108; record factor count and eigenvalue spectrum.
* **REQ-3**: Pearson r between each factor and DSI / PD; report sign counts.
* **REQ-4**: Side-by-side comparison chart (t0108 vs t0110) with matching y-axis.
* **REQ-5**: One answer asset with the question + answer + evidence.
