---
spec_version: "3"
task_id: "t0049_seclamp_cond_remeasure"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-25T09:59:02Z"
completed_at: "2026-04-25T10:18:41Z"
---
## Summary

Implemented the SEClamp channel-isolation conductance re-measurement on the deposited Poleg-Polsky
2016 DSGC. Wrote 6 Python modules under `code/`, ran a 32-trial sweep (~7.9 minutes wall-clock),
generated per-trial and per-channel comparison CSVs, rendered two PNG charts, populated a multi-
variant `metrics.json` (9 variants), and produced one answer asset
(`seclamp-conductance-remeasurement-fig3`). All ruff / mypy / verificators that exist in this branch
pass with zero errors.

Headline results at gNMDA = 0.5 nS, V_clamp = -65 mV (mean +/- SD, n = 4 trials per cell):

* NMDA PD = 13.89 +/- 0.38 nS (paper 7.0; t0047 summed 69.55) — H2
* NMDA ND = 13.71 +/- 0.19 nS (paper 5.0; t0047 summed 33.98) — H2
* AMPA PD = 5.93 +/- 0.27 nS (paper 3.5; t0047 summed 10.92) — H2
* AMPA ND = 5.79 +/- 0.19 nS (paper 3.5; t0047 summed 10.77) — H2
* GABA PD = 47.47 +/- 1.98 nS (paper 12.5; t0047 summed 106.13) — H2
* GABA ND = 48.04 +/- 1.76 nS (paper 30.0; t0047 summed 215.57) — H2

Verdict: All 6 cells are H2. SEClamp values lie between the paper targets and t0047 per-synapse-
direct values but match neither within tolerance. Modality is necessary but not sufficient to
explain the t0047 amplitude mismatch with the paper. The deposited model also fails to reproduce the
paper's GABA PD/ND asymmetry under SEClamp (DSI = -0.006 vs paper ~ -0.41).

## Actions Taken

1. Created `code/paths.py` with all task-local Path constants; auto-creates output dirs.
2. Created `code/constants.py` with SEClamp parameters, reversal potentials, paper targets, t0047
   baselines, channel-isolation enum, sweep grid, and a runtime assertion that re-affirms
   `E_GABA_MV` against t0046's `E_SACINHIB_MV`.
3. Copied `code/dsi.py` verbatim from t0047 (with attribution) — t0047 is not a registered library
   so the cross-task copy rule applies.
4. Created `code/run_seclamp.py` — the SEClamp simulation wrapper. Imports `_ensure_cell` from
   t0046 directly (registered library). Inserts SEClamp at `h.RGC.soma(0.5)` after channel-isolation
   overrides + re-`update()` + re-`placeBIP()`. Runs `finitialize` + `continuerun`. Asserts
   clamp_v_sd_mv < 0.5 mV and BIP positions return to baseline.
5. Created `code/run_seclamp_sweep.py` — the 32-trial sweep driver with a 2-trial validation gate.
   Wrote `results/data/seclamp_trials.csv` (32 rows). Sweep wall-clock: 471.7 s (~7.9 min) plus ~60
   s cell build.
6. Validation gate output: peak_i_pa = -524 to -533 pA, clamp_v_sd_mv = 1.6e-4 mV. PASSED.
7. Created `code/compute_metrics.py` — aggregates per-trial currents into per-channel mean +/- SD
   conductance, applies H0/H1/H2 verdict logic, writes `seclamp_comparison_table.csv` (6 rows) and
   `results/metrics.json` (9 variants: 6 channel x direction with empty metrics + 3 DSI roll-ups).
8. **Bug found and fixed**: initial `compute_metrics.py` divided by 1000 in the conductance
   conversion, giving values ~1000x too small (~0.014 nS for NMDA). Root cause: I conflated "convert
   nA to pA" with the unit identity `g[nS] = i[pA] / V[mV]`. NEURON's SEClamp `_ref_i` is in nA; we
   already multiply by 1000 to get pA in `run_seclamp.py`; in `compute_metrics.py` we only need
   `g[nS] = pA / mV`. Fixed; re-ran metrics; values now in the plausible band.
9. Created `code/render_figures.py` — produced both PNGs in `results/images/`.
10. Created the answer asset folder `assets/answer/seclamp-conductance-remeasurement-fig3/` with
    `details.json`, `short_answer.md`, `full_answer.md` per
    `meta/asset_types/answer/specification.md` v2.
11. Ran `flowmark`, `ruff check --fix`, `ruff format`, `mypy` — all PASSED.
12. Ran `verify_task_metrics`, `verify_task_folder`, `verify_task_file`, `verify_plan` — all
    PASSED with at most 1 informational warning (`FD-W002 logs/searches/ is empty`).

## Outputs

* `tasks/t0049_seclamp_cond_remeasure/code/paths.py`
* `tasks/t0049_seclamp_cond_remeasure/code/constants.py`
* `tasks/t0049_seclamp_cond_remeasure/code/dsi.py`
* `tasks/t0049_seclamp_cond_remeasure/code/run_seclamp.py`
* `tasks/t0049_seclamp_cond_remeasure/code/run_seclamp_sweep.py`
* `tasks/t0049_seclamp_cond_remeasure/code/compute_metrics.py`
* `tasks/t0049_seclamp_cond_remeasure/code/render_figures.py`
* `tasks/t0049_seclamp_cond_remeasure/results/data/seclamp_trials.csv` (32 rows)
* `tasks/t0049_seclamp_cond_remeasure/results/data/seclamp_comparison_table.csv` (6 rows)
* `tasks/t0049_seclamp_cond_remeasure/results/metrics.json` (9 variants)
* `tasks/t0049_seclamp_cond_remeasure/results/images/seclamp_conductance_pd_vs_nd.png`
* `tasks/t0049_seclamp_cond_remeasure/results/images/seclamp_vs_per_syn_direct_modality_comparison.png`
* `tasks/t0049_seclamp_cond_remeasure/assets/answer/seclamp-conductance-remeasurement-fig3/details.json`
* `tasks/t0049_seclamp_cond_remeasure/assets/answer/seclamp-conductance-remeasurement-fig3/short_answer.md`
* `tasks/t0049_seclamp_cond_remeasure/assets/answer/seclamp-conductance-remeasurement-fig3/full_answer.md`

## Issues

* Unit conversion bug in `compute_metrics.py` (caught during inspection of small initial values;
  values were 1000x too small at first run). Fixed by removing the spurious `/ 1000.0` factor; the
  inline comment now documents the NEURON unit identity `g[nS] = i[pA] / V[mV]`. The validation
  gate's plausible-conductance band assertion was tightened post-fix and is now consistent.
* `verify_answer_asset` does not exist as a standalone module in this branch; the answer-asset
  structure was instead validated by manual inspection against
  `meta/asset_types/answer/ specification.md` v2 and by the task-folder verificator. The
  orchestrator's reporting step will re-run any branch-specific answer verificator if added later.

## Requirement Completion Checklist

* **REQ-1** — `done`. SEClamp inserted at `h.RGC.soma(0.5)` with `dur1 = TSTOP_MS`,
  `amp1 = -65 mV`, `rs = 0.001 MOhm`. `_ref_i` recorded at `DT_RECORD_MS = 0.25 ms`. Soma voltage
  recorded; runtime assertion `clamp_v_sd_mv < 0.5 mV` PASSED on every trial (max observed ~ 2.9e-4
  mV, three orders of magnitude below tolerance). Evidence: `code/run_seclamp.py:115-145` and
  `results/data/seclamp_trials.csv` `clamp_v_sd_mv` column.

* **REQ-2** — `done`. Channel-isolation overrides applied AFTER `simplerun()` returns: AMPA-only
  (`b2gnmda=0`, `gabaMOD=0`), NMDA-only (`b2gampa=0`, `gabaMOD=0`), GABA-only (`b2gnmda=0`,
  `b2gampa=0`), with re-`update()` + re-`placeBIP()` + SEClamp insertion + `finitialize` +
  `continuerun`. Evidence: `code/run_seclamp.py:_apply_channel_overrides` and `seclamp_trials.csv`
  `channel_on` column showing 4 trials per (direction, channel_on).

* **REQ-3** — `done`. Full sweep: 2 directions x 4 channel-isolations x 4 trials = 32 trials at
  gNMDA = 0.5 nS, exptype = CONTROL. Evidence: `seclamp_trials.csv` has exactly 32 rows with 8
  groups of 4 (verified at end of sweep run).

* **REQ-4** — `done`. Per-channel conductance computed via
  `g_nS = abs(i_pA) / abs(V_clamp - E_rev)` with explicit per-channel reversal potentials (NMDA =
  AMPA = 0 mV, GABA = -60 mV). Evidence: `code/compute_metrics.py:_per_trial_conductances` and
  `seclamp_comparison_table.csv` `g_seclamp_mean_ns` column.

* **REQ-5** — `done`. `results/metrics.json` written in the explicit multi-variant format with 9
  variants: 6 channel x direction (empty `metrics` — conductance amplitudes are reported in the
  comparison CSV, not in the registered metric set) + 3 DSI roll-ups carrying the registered
  `direction_selectivity_index` metric. Evidence: `results/metrics.json` validates with
  `verify_task_metrics.py` (PASSED).

* **REQ-6** — `done`. Per-channel comparison table with all four reference columns (paper Fig 3A-E
  target, SEClamp this task, t0047 per-syn-summed, t0047 per-syn-mean) committed at
  `results/data/seclamp_comparison_table.csv` and reproduced in
  `assets/answer/seclamp-conductance-remeasurement-fig3/full_answer.md` "Per-channel comparison
  table" section.

* **REQ-7** — `done`. Both PNGs rendered: `results/images/seclamp_conductance_pd_vs_nd.png` (56
  KB) and `results/images/seclamp_vs_per_syn_direct_modality_comparison.png` (65 KB). Both embedded
  in the answer asset's `full_answer.md`.

* **REQ-8** — `done`. H0 / H1 / H2 verdict rendered for all 6 cells in
  `seclamp_comparison_table.csv` `verdict` column and discussed cell-by-cell in the answer asset.
  All 6 cells: H2.

* **REQ-9** — `done`. Answer asset `assets/answer/seclamp-conductance-remeasurement-fig3/` written
  per `meta/asset_types/answer/specification.md` v2 with `details.json`, `short_answer.md`,
  `full_answer.md`. The full answer contains all required sections (Question, Short Answer, Research
  Process, Evidence from Papers/Internet/Code, Synthesis, Limitations, Sources) plus the per-channel
  comparison table, the cell-by-cell verdict block, the SEClamp methodology notes, and the
  integrated synthesis paragraph identifying H2 (modality necessary but not sufficient).

* **REQ-10** — `done`. `code/run_seclamp.py` imports `_ensure_cell`, `Direction`,
  `ExperimentType`, `V_INIT_MV`, `TSTOP_MS`, `PSP_BASELINE_MS`, `reset_globals_to_canonical`,
  `assert_bip_positions_baseline`, `ensure_neuron_importable` directly from t0046's
  `modeldb_189347_dsgc_exact` library modules. The override-and-rerun pattern from t0046
  `run_simplerun.py:135-151` is re-implemented (not copied) inside `run_seclamp_trial` to interleave
  the SEClamp insertion. No copy of the simulation driver lives in this task folder.

* **REQ-11** — `done`. All paths centralised in `code/paths.py`; all constants in
  `code/constants.py`. Runtime assertion at module load: `assert E_GABA_MV == _T0046_E_SACINHIB_MV`
  PASSES.

* **REQ-12** — `done`. Verificators that exist in this branch all return zero errors:
  `verify_task_file` PASSED, `verify_plan` PASSED, `verify_task_metrics` PASSED,
  `verify_task_folder` PASSED (1 informational warning about empty `logs/searches/`).
  `verify_answer_asset` does not exist as a standalone module in this branch; the answer-asset
  structure was validated against `meta/asset_types/answer/specification.md` v2 by manual
  inspection. The orchestrator's reporting step will re-run any branch-specific verificator if added
  later. `verify_task_results` is not run by the implementation skill (the `results` step produces
  the additional files it requires).
