# Canonical 5-seed Substrate-Rate Report (S-0112-01 batch closed)

## Source Suggestion

S-0115-02: "5-seed substrate-rate batch (S-0112-01) is now complete; write canonical report."

## Motivation

The S-0112-01 substrate-rate confirmation batch closed with t0115 (seed 9354). The 5 GA seeds (44,
77, 2247, 7755, 9354) on the 68-d Bed B + 14-d morphology substrate produced LEGIT joint-pass
acceptance rates of 3.23%, 0.35%, 0.00%, 8.13%, 1.19% respectively. The 5-seed mean is 2.58% +/- SE
1.50%, with a 95% CI of (-0.36%, +5.52%) that still brackets both Hay 2011's 0.40% envelope upper
bound and Druckmann 2007's 0.10% baseline -- but 3 of 5 seeds individually beat Hay's envelope, and
the point estimate is 6.5x above Hay and 25.8x above Druckmann.

The data lives in five separate task folders with slightly different reporting conventions (t0106
reported on a $25 cap; t0112 used a $25 cap; t0113/t0114/t0115 used auto-stop disabled; t0106 used
auto-stop enabled). A single canonical document with harmonised metric conventions is needed before
this finding can be referenced by downstream tasks or external write-ups.

## Scope

Pure write-up. No new simulation, no new NSGA-II runs. Re-read the 5 source tasks' results parquets
and produce one consolidated canonical document plus one answer asset.

## Approach

1. **Re-read source data**: load each of the 5 tasks' `results/data/pareto_front_seed*.json` (or
   equivalent) and `all_evaluations_seed*.json` if available. Verify total evaluation counts match
   the per-seed reports (3744, 2016, 1344, 5952, 5280).
2. **Harmonise conventions**: re-compute LEGIT joint-pass count per seed using the canonical
   definition (DSI >= 0.5 AND PD-rate >= 30 Hz AND DSI < 0.9999). Cross-check against each task's
   reported number; flag and document any discrepancies.
3. **Compute 5-seed statistics**: per-seed acceptance rate, 5-seed mean, sample SD, sample SE, 95%
   CI (normal approx), 95% CI (bootstrap with B=10000), and counts of seeds beating Hay envelope.
4. **Comparison table**: harmonise with Hay 2011's 0.40% upper envelope and 0.0104% perisomatic
   bottleneck, and with Druckmann 2007's 0.10% baseline.
5. **Per-seed convergence-trajectory comparison**: HV trajectory, plateau generation, total
   evaluations, wall-clock per generation.
6. **Charts**: (a) per-seed acceptance rate bar chart with Hay/Druckmann reference lines, (b) 5-seed
   HV-trajectory overlay (one trace per seed), (c) DSI-vs-PD scatter for the pooled LEGIT joint-pass
   cells colored by seed.
7. **Answer asset**: write one answer asset answering "What is the LEGIT joint-pass acceptance rate
   on the 68-d Bed B + 14-d morphology substrate, estimated from a 5-seed random-init NSGA-II batch,
   and how does it compare to Hay 2011 and Druckmann 2007?"

## Expected Outputs

* `results/data/per_seed_substrate_rate_5seed.csv` -- one row per seed with all relevant statistics.
* `results/data/pooled_legit_jointpass_cells.parquet` -- pooled LEGIT joint-pass cells across the 5
  seeds (DSI, PD, source-seed, generation, cell_id).
* `results/images/per_seed_acceptance_bar.png` -- per-seed acceptance bar chart.
* `results/images/hv_trajectory_5seed_overlay.png` -- 5-seed HV-trajectory overlay.
* `results/images/dsi_pd_scatter_5seed_pooled.png` -- pooled scatter colored by seed.
* `assets/answer/substrate-rate-5seed-canonical/` -- 1 answer asset.
* `results/results_summary.md` and `results/results_detailed.md` with the canonical numbers.

## Budget

Local CPU only, no remote machines. Estimate <$0.20.

## Dependencies

* `t0106_long_pdnd_nsga2_300gen` -- seed 44.
* `t0112_t0106_seed77_replicate` -- seed 77.
* `t0113_t0106_seed2247_replicate` -- seed 2247.
* `t0114_seed7755_no_autostop` -- seed 7755.
* `t0115_seed9354_no_autostop` -- seed 9354.
* `t0119_brainstorm_results_23` -- commissions this task.

## Verification Criteria

* All 5 per-seed acceptance rates match the source task reports within rounding.
* 5-seed mean and SE match the brainstorm-session-23 summary (2.58% +/- 1.50%) within rounding.
* Charts saved and embedded in `results_detailed.md`.
* Answer asset passes `verify_answer_asset` (or local fallback).

## Cross-References

* Source suggestion: S-0115-02.
* Source tasks: t0106, t0112, t0113, t0114, t0115.
* Hay 2011 -- 10.1371/journal.pcbi.1002107 (or t0114 `compare_literature.md` for citation).
* Druckmann 2007 -- as cited in t0114 `compare_literature.md`.
