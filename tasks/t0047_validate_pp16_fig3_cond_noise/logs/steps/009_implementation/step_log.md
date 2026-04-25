---
spec_version: "3"
task_id: "t0047_validate_pp16_fig3_cond_noise"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-24T22:40:46Z"
completed_at: "2026-04-25T00:36:30Z"
---
## Summary

Implemented all 13 plan steps end-to-end across the 5 milestones (scaffolding, recorder wrapper,
drivers, metrics, charts + answer asset). Created 8 Python modules under `code/` (paths, constants,
dsi, scoring, run_with_conductances, run_fig3_validation, run_noise_extension, compute_metrics,
render_figures) that import t0046's library subtree without copying. Ran the 56-trial gNMDA sweep,
the 6-cell PSP-trace pass, and the 96-trial noise extension sweep on local CPU (NEURON 8.2.7);
produced all 7 required reproduction PNGs, the explicit-multi-variant metrics.json with 19 variants,
and the `polegpolsky-2016-fig3-conductances-validation` answer asset with details.json +
short_answer.md + full_answer.md. The headline finding is that per-synapse-class summed peak
conductances at the code-pinned b2gnmda = 0.5 nS are 6-9x the paper's Fig 3A-E targets and that DSI
vs gNMDA peaks at 0.19 near b2gnmda = 0.5 nS and decays to 0.018 by 3.0 nS (paper claims a flat
~0.30 plateau).

## Actions Taken

1. Created `code/__init__.py` (already existed empty), `code/paths.py` (TASK_ROOT-anchored Path
   constants), `code/constants.py` (sweep grids, paper Fig 3 targets, NoiseCondition enum, CSV
   column names), `code/dsi.py` (compute_dsi_pd_nd helper copied from t0046's compute_metrics.py
   lines 100-124), and `code/scoring.py` (compute_roc_auc_pd_vs_baseline copied from t0046 lines
   142-158).
2. Built `code/run_with_conductances.py` with the recording wrapper: ConductanceRecorders dataclass
   carrying one Vector per synapse for `_ref_gAMPA`, `_ref_gNMDA` (BIPsyn), `_ref_g` (SACexc and
   SACinhib), plus a soma voltage recorder for offline current computation. Added a smoke-test
   `__main__` that runs one trial and prints all 12 peak fields. Smoke test passed: peak NMDA summed
   = 69.4 nS, peak GABA summed = 100.3 nS at default b2gnmda = 0.5 nS, all four channels non-zero.
3. Built `code/run_fig3_validation.py` (gNMDA sweep + PSP-trace pass) and
   `code/run_noise_extension.py` (Fig 6/7 noise sweep). Both expose a `--limit N` validation gate
   for early failure detection. Validation gate at b2gnmda = 0.0 PD showed peak_g_nmda = 0 (correct
   when NMDA is off) and PSP = 13 mV (consistent with AMPA-only drive). Validation gate for the
   noise sweep showed peak_psp_mv = 22-25 mV at CONTROL/PD/no-noise, consistent with t0046's prior
   measurement of 23 mV.
4. Ran the full 56-trial gNMDA sweep (b2gnmda in {0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0} x PD/ND x 4
   trials) and the 6-cell PSP-trace pass (b2gnmda in {0.0, 0.5, 2.5} x PD/ND). Wrote
   `results/data/gnmda_sweep_trials.csv` (56 rows) and `results/data/psp_traces_fig3f_top.csv`
   (24006 rows = 6 cells x 4001 samples).
5. Ran the full 96-trial noise extension sweep (3 conditions x 4 flickerVAR x 2 dirs x 4 trials).
   AP5 = control exptype with b2gnmda_override = 0; 0Mg = ExperimentType.ZERO_MG. Wrote
   `results/data/noise_extension_trials.csv` (96 rows).
6. Created `code/compute_metrics.py` to derive `results/data/conductance_comparison_table.csv` (42
   rows = 3 channels x 2 dirs x 7 gNMDA values, with paper-target comparison and +/- 25% verdict),
   `results/data/dsi_by_gnmda.json`, `results/data/dsi_auc_by_condition_noise.json`, and
   `results/metrics.json` in the explicit multi-variant format with 19 variants (7 gNMDA + 12 noise
   cells), each carrying the registered metric `direction_selectivity_index`.
7. Built `code/render_figures.py` and rendered the 7 required PNGs to `results/images/`:
   `fig3a_nmda_conductance_pd_vs_nd.png`, `fig3b_ampa_conductance_pd_vs_nd.png`,
   `fig3c_gaba_conductance_pd_vs_nd.png`, `fig3f_top_psp_traces.png`,
   `fig3f_bottom_dsi_vs_gnmda.png`, `fig6_dsi_vs_noise_per_condition.png`,
   `fig7_auc_vs_noise_per_condition.png`. All PNGs >= 42 KB.
8. Created the answer asset
   `tasks/t0047_validate_pp16_fig3_cond_noise/assets/answer/polegpolsky-2016-fig3-conductances-validation/`
   with details.json (spec_version "2"), short_answer.md (2-3 paragraphs with headline verdict), and
   full_answer.md (per-synapse comparison table, PSP-trace overlay table, DSI-vs-gNMDA table, two
   noise-sweep tables, 15-entry discrepancy catalogue extending t0046's 12 entries with 3 new
   entries, one-paragraph synthesis).
9. Ran `uv run flowmark --inplace --nobackup` on both answer documents, then
   `uv run ruff check --fix . && uv run ruff format . && uv run mypy .` from the repo root: all
   checks pass (258 source files clean).
10. Ran `verify_plan.py` (PASSED, 0 errors), `verify_task_metrics.py` (PASSED, 0 errors after fixing
    the variant_id format from `flickerVAR` to `flicker` so the variant_id slug regex accepts only
    lowercase letters / digits / dots / hyphens / underscores per TM-E003).

## Outputs

* `tasks/t0047_validate_pp16_fig3_cond_noise/code/` — 9 modules (paths, constants, dsi, scoring,
  run_with_conductances, run_fig3_validation, run_noise_extension, compute_metrics, render_figures,
  plus `__init__.py`)
* `tasks/t0047_validate_pp16_fig3_cond_noise/results/data/gnmda_sweep_trials.csv` (56 rows)
* `tasks/t0047_validate_pp16_fig3_cond_noise/results/data/noise_extension_trials.csv` (96 rows)
* `tasks/t0047_validate_pp16_fig3_cond_noise/results/data/psp_traces_fig3f_top.csv` (24006 rows)
* `tasks/t0047_validate_pp16_fig3_cond_noise/results/data/conductance_comparison_table.csv` (42
  rows)
* `tasks/t0047_validate_pp16_fig3_cond_noise/results/data/dsi_by_gnmda.json`
* `tasks/t0047_validate_pp16_fig3_cond_noise/results/data/dsi_auc_by_condition_noise.json`
* `tasks/t0047_validate_pp16_fig3_cond_noise/results/metrics.json` (19 variants, explicit format)
* `tasks/t0047_validate_pp16_fig3_cond_noise/results/images/` — 7 PNGs
* `tasks/t0047_validate_pp16_fig3_cond_noise/assets/answer/polegpolsky-2016-fig3-conductances-validation/`
  (details.json, short_answer.md, full_answer.md)

## Issues

* **ROC AUC saturated at 1.0 across every (condition, noise) cell**. The t0046 helper uses
  pre-stimulus baseline mean as the negative-class distribution; at the model's PSP amplitudes
  (peaks 18-25 mV above v_init; baselines 5-6 mV above v_init), every PD-peak vs baseline pair is
  correctly ordered, so AUC is 1.0 in every cell. Documented as discrepancy entry 15 in the answer
  asset's full_answer.md. Future task should re-implement AUC with no-stimulus negatives.
* **Variant ID format**. The plan specified `control_flickerVAR_0p0` style IDs but the
  `verify_task_metrics.py` regex (TM-E003) rejects uppercase letters; renamed to
  `control_flicker_0p0`, `ap5_flicker_0p0`, `zero_mg_flicker_0p0` style. metrics.json now passes
  verification.
* **Bootstrap re-exec scope**. The first smoke-test attempt was launched as `python -u -m ...`
  inside `run_with_logs` (no `uv run` wrapper) and failed with `ModuleNotFoundError: numpy` because
  the bootstrap re-exec used the system Python rather than the venv. Fix: every wrapped command uses
  `uv run python -u -m ...` (matching t0046's logged convention). Documented in this step log so
  future tasks avoid the same pitfall.
* No other issues encountered. All seven verification gates from `plan.md` pass: `verify_plan` (0
  errors), `verify_task_metrics` (0 errors), all 7 PNGs exist > 10 KB, CSV row counts match (gnmda
  56, noise 96, psp_cells 6), answer asset details.json declares spec_version "2" + both canonical
  paths, and t0046 code is import-only with no file-content overlap (only `paths.py`,
  `constants.py`, `__init__.py`, `compute_metrics.py`, `render_figures.py` share filenames; md5 sums
  of the two latter files differ).

## Requirement Completion Checklist

* **REQ-1** — done. t0046's library is imported via cross-task package paths in
  `code/run_with_conductances.py` (`run_one_trial`, `_ensure_cell`, `TrialResult`),
  `code/run_fig3_validation.py` and `code/run_noise_extension.py` (`Direction`, `ExperimentType`,
  `ensure_neuron_importable`), and `code/constants.py` (`E_SACINHIB_MV`). No t0046 file is copied;
  md5 verification confirms the two filename overlaps (compute_metrics.py, render_figures.py) are
  independent task-local implementations.
* **REQ-2** — done. `code/paths.py` and `code/constants.py` exist with all the constants
  enumerated in the plan plus an assert at constants.py module-load that
  `E_SACINHIB_MV_OVERRIDE == t0046's E_SACINHIB_MV` (confirms canonical-value drift surveillance).
* **REQ-3** — done. `code/run_with_conductances.py` defines `ConductanceRecorders`,
  `TrialResultWithConductances`, `attach_conductance_recorders`, `build_cell_and_attach_recorders`,
  and `run_one_trial_with_conductances`. Recorders are attached ONCE after the cell is built; the
  wrapper resets all recorder vectors via `vec.resize(0)` after every trial so peak memory stays
  bounded.
* **REQ-4** — done. `gnmda_sweep_trials.csv` has 56 rows = 7 b2gnmda x 2 dirs x 4 trials;
  `conductance_comparison_table.csv` has the per-(channel, direction, gnmda) summed-mean,
  per-syn-mean, paper-target, diff %, and +/- 25% verdict. Every cell verdict is OUTSIDE on summed
  scale and the per-syn-mean is well below paper target.
* **REQ-5** — done. `psp_traces_fig3f_top.csv` covers all 6 cells; `fig3f_top_psp_traces.png`
  rendered as a 3-row x 2-column subplot grid. PSP-trace peak amplitudes match the sweep means to
  within 1.6 mV (well inside the +/- 20% tolerance in the plan).
* **REQ-6** — done. `code/dsi.py` carries the copied `compute_dsi_pd_nd` helper with the source
  citation comment. DSI per gNMDA value is in `dsi_by_gnmda.json` and rendered to
  `fig3f_bottom_dsi_vs_gnmda.png`. None of the 7 gNMDA values yields a DSI within +/- 0.05 of 0.30;
  the divergence is documented numerically in the answer asset's full_answer.md (entry 14 of the
  discrepancy catalogue).
* **REQ-7** — done. `noise_extension_trials.csv` has 96 rows; AP5 was modelled as
  `b2gnmda_override = 0.0` and 0Mg as `ExperimentType.ZERO_MG` per the plan. Per-class conductance
  peaks are written to the CSV alongside peak PSP and baseline mean.
* **REQ-8** — done. `code/scoring.py` carries the copied `compute_roc_auc_pd_vs_baseline` helper
  with citation comment. Per-(condition, flickerVAR) DSI and AUC are in
  `dsi_auc_by_condition_noise.json` and rendered to `fig6_dsi_vs_noise_per_condition.png` and
  `fig7_auc_vs_noise_per_condition.png`. **Partial result**: DSI declines as flickerVAR rises in
  control (19% drop) and 0Mg (48% drop) and AP5 (50% drop), satisfying the qualitative pass
  criterion. AUC saturates at 1.0 in every cell (metric-implementation limitation, documented as new
  discrepancy entry 15).
* **REQ-9** — done. All 7 PNGs exist in `results/images/` with sizes 42-170 KB. The Okabe-Ito
  `MODEL_COLORS` palette is imported from t0011's `tuning_curve_viz.constants`.
* **REQ-10** — done. The answer asset folder contains the three required files; `details.json`
  declares spec_version "2", `short_answer_path`, `full_answer_path`, and three sources (paper
  `10.1016_j.neuron.2016.02.013`, task `t0046_reproduce_poleg_polsky_2016_exact`). `full_answer.md`
  contains the per-synapse conductance table, PSP-trace overlay, DSI-vs-gNMDA chart and table, two
  noise-sweep tables, the extended 15-entry discrepancy catalogue, and a one-paragraph synthesis.
* **REQ-11** — done. The discrepancy catalogue carries forward t0046's 12 entries verbatim with
  attribution and adds three new entries: the per-synapse-class conductance excess (entry 13), the
  DSI-vs-gNMDA non-flatness (entry 14), and the ROC AUC saturation (entry 15). t0046's audit row 35
  (`Voff_bipNMDA = 0`) is referenced as the candidate root cause for the conductance excess.
* **REQ-12** — done. Total trials run = 56 (gNMDA) + 96 (noise) = 152. All on local CPU; no remote
  machines. Wall-clock per trial averaged ~5 sec (gNMDA) and ~4 sec (noise); total simulation
  wall-clock ~13 min as the plan estimated.
* **REQ-13** — done. All Python modules use absolute imports anchored at the repo root. Every CLI
  invocation in this task is wrapped via
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0047_validate_pp16_fig3_cond_noise -- uv run python -u ...`
  per the t0046 logged convention.
* **REQ-14** — done. `results/metrics.json` uses the explicit multi-variant format with 19
  variants. Each variant carries the registered metric `direction_selectivity_index` (the only
  registered metric this task can compute from PD/ND data; HWHM, reliability, and RMSE require a
  12-angle tuning curve, which is out of scope per the plan and noted explicitly in discrepancy
  catalogue entry 12). `verify_task_metrics.py` PASSES with 0 errors.
