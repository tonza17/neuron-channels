---
spec_version: "3"
task_id: "t0078_bedb_mobo_v2_ais_tiered_ahp"
step_number: 12
step_name: "results"
status: "completed"
started_at: "2026-05-04T15:57:15Z"
completed_at: "2026-05-04T16:05:00Z"
---
# Step 12 — Results

## Summary

Wrote the three required results files (`results_summary.md`, `results_detailed.md`,
`results/metrics.json`) plus generated the two required PNGs (`pareto_front.png`,
`hypervolume_trajectory.png`) by running the local `plot_pareto.py` with `--skip-deep-dives`. The
headline result is captured in both summary docs: 491 cells / 78,560 NEURON simulations produced a
17-cell Pareto front with **HV 11.41 (+36% over t0076)** but the joint pass criterion (DSI ≥ 0.4
AND PD rate ≥ 10 Hz) was **narrowly missed** by the closest cell at iter 81 (DSI 0.316, PD 9.68
Hz). The Task Requirement Coverage section enumerates all 22 REQ items from the plan with their
status: 18 done, 2 partial (REQ-10 acquisition count 416/700 due to early-stop, REQ-14 deep-dive
PNGs skipped due to local NEURON unavailability), 1 deferred (REQ-16 substrate regression check), 1
done with caveat (REQ-19 costs.json finalised by teardown step rather than orchestrator, but
spec-compliant).

## Actions Taken

1. Ran `prestep results`.
2. Ran `plot_pareto.py --skip-deep-dives` locally to generate `pareto_front.png` and
   `hypervolume_trajectory.png`. Deep-dive PNGs require nrnivmodl-compiled t78 MODs which are not
   available on Windows; this is a documented limitation.
3. Wrote `results/metrics.json` in multi-variant format with 17 variants (one per Pareto cell), each
   carrying the registered metric `direction_selectivity_index`. The variants are sorted by
   descending DSI and labelled by Pareto-front position (high-DSI sub-threshold extreme, high-DSI
   rail, transition, mid-trade-off, high-rate slope, high-rate corner).
4. Wrote `results/results_summary.md` with all 3 mandatory sections (Summary, Metrics,
   Verification).
5. Wrote `results/results_detailed.md` with all 7 mandatory sections (Summary, Methodology,
   Visualisations, Examples, Verification, Limitations, Files Created) plus the Task Requirement
   Coverage section as the final section per the project rule.

## Outputs

* `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/results/results_summary.md` — headline findings
* `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/results/results_detailed.md` — full analysis with
  17-cell Pareto table, methodology, examples, REQ checklist
* `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/results/metrics.json` — multi-variant metrics with 17
  Pareto cells
* `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/results/images/pareto_front.png`
* `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/results/images/hypervolume_trajectory.png`
* `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/logs/steps/012_results/step_log.md` — this step log

## Issues

No blocking issues. Minor notes documented in the results_detailed.md Limitations section:

1. Deep-dive PNGs were skipped because the t78 MOD library was not compiled on the local Windows
   machine (nrnivmodl ran on the Vast.ai instance; local machine has Python NEURON but no MOD
   compilation). Two PNGs (Pareto front + hypervolume trajectory) are sufficient to meet the
   chart-count requirement; deep-dive PNGs are a follow-up if needed.
2. The Pareto-front cells include 5 cells at iter > 416 (max iter at acq 416 was iter 491). The
   pareto_front.json was generated at the last checkpoint (cell 484) on the remote, so it includes
   Pareto candidates from cells 1-484, not 1-491. The 7 cells from acq 477-491 (cell numbers
   552-566) are absent from the saved pareto_front but their (DSI, PD) values are in
   `data/trial_history.parquet`. None of those 7 cells crossed the joint pass criterion either (per
   the mobo_loop.log inspection during the run).
