---
spec_version: "3"
task_id: "t0048_voff_nmda1_dsi_test"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-25T08:43:57Z"
completed_at: "2026-04-25T09:09:05Z"
---
## Summary

Implemented the Voff_bipNMDA = 1 (voltage-independent NMDA) DSI sweep for the t0046+t0047 stack:
copied t0047's recorder and DSI helpers into this task with attribution, ran the 56-trial gNMDA
sweep at exptype = ZERO_MG, computed DSI per gNMDA, classified the H0 / H1 / H2 verdict (range and
slope tests), rendered the DSI overlay and conductance comparison PNGs, and produced the
`dsi-flatness-test-voltage-independent-nmda` answer asset. The headline finding is H2:
voltage-independent NMDA flattens the curve roughly 2.6x but never reaches the paper's claimed 0.30
line, sitting at 0.04-0.10 across the entire range.

## Actions Taken

1. **Verified worktree state and dependencies.** Confirmed that t0007, t0046, and t0047 are all
   status `completed` via `aggregate_tasks --status completed --format ids`. Verified the t0047
   baseline CSV `gnmda_sweep_trials.csv` exists and has 57 lines (header + 56 trials) at the
   expected absolute path. Ran a one-off `_smoke_imports.py` confirming `ExperimentType.ZERO_MG = 2`
   and `CONTROL = 1` from t0046's library; deleted the file after the check passed.
2. **Created the scaffold.** Wrote `code/paths.py` (anchored to
   `Path(__file__). resolve().parent.parent`, with the t0047 baseline CSV path included) and
   `code/constants.py` (sweep grid, recorder timing, reversal potentials with the
   `assert E_SACINHIB_MV_OVERRIDE == _T0046_E_SACINHIB_MV` self-check, paper Fig 3F target, the new
   H1 range / slope thresholds and the t0047 H2 reference).
3. **Copied t0047's recorder and DSI helpers with attribution.** Wrote
   `code/run_with_conductances.py` (re-targeted constants import to `tasks.t0048...`, deleted the
   smoke-test block) and `code/dsi.py` (no adaptation). Both files carry leading attribution
   docstrings naming t0047 as the source and explaining that t0047 is not a registered library asset
   so its code must be COPIED rather than imported.
4. **Implemented `code/run_voff1_sweep.py`.** Single-file driver that builds the cell and recorders
   once, runs a smoke test at `b2gnmda_override = 0.5` and `3.0` PD trials with assertions on
   `peak_psp_mv` finiteness and the +/- 50 mV sanity band, and then runs the 56-trial sweep with the
   trial-seed formula `1000 * gnmda_idx + 100 * dir_idx + trial` copied from t0047. Output goes to
   `results/data/gnmda_sweep_trials_voff1.csv` (17 columns matching t0047's schema). `--limit N`
   flag supports a small validation gate.
5. **Validation gate run.** Ran `--limit 4` first; it produced 4 rows in
   `gnmda_sweep_trials_voff1_limit.csv` with PD at 0.0 nS = 13.19 mV, ND at 0.0 nS = 10.74 mV, PD at
   0.5 nS = 22.46 mV, ND at 0.5 nS = 18.72 mV — all finite, all distinguishable, all within the
   +/- 50 mV sanity band. Compared to t0047's baseline (PD at 0.5 nS = 23.42 mV) — Voff = 1 is
   within 4% of Voff = 0 at gNMDA = 0.5 nS, well inside the +/- 50% gate from the plan.
6. **Full sweep.** Ran the full 56-trial sweep in the background. Wall-clock was 13 min 28 s (about
   14.4 s/trial), longer than the planned ~5 min/sweep estimate but still well within budget. Output
   at `results/data/gnmda_sweep_trials_voff1.csv` (56 rows + header).
7. **Implemented `code/compute_metrics.py`.** Reads both CSVs, computes DSI per gNMDA via the
   inlined `compute_dsi_pd_nd` helper, runs the two REQ-12 verdict tests (range and slope via
   `numpy.polyfit deg=1`), classifies the verdict label, and writes:
   * `results/data/dsi_by_gnmda_voff1.json`
   * `results/data/dsi_by_gnmda_voff0_from_t0047.json`
   * `results/data/verdict_voff1.json`
   * `results/metrics.json` (explicit multi-variant format, 7 variants `voff1_gnmda_0p0ns` through
     `voff1_gnmda_3p0ns`, each with the registered `direction_selectivity_index` metric).
8. **Implemented `code/render_figures.py`.** Wrote two PNGs to `results/images/`: the DSI overlay
   panel (Voff = 0 from t0047 + Voff = 1 from this task + paper claim line at 0.30 with a +/- 0.05
   band) and the per-class conductance comparison bar chart at gNMDA = 0.5 nS (3 channels x 2
   directions x 2 conditions = 12 grouped bars, color-coded by Voff and hatched by direction).
9. **Wrote the answer asset.** Created `assets/answer/dsi-flatness-test-voltage- independent-nmda/`
   with `details.json` (spec_version "2", `code-experiment` + `papers` answer methods, citing the
   Poleg-Polsky 2016 paper and t0046 + t0047), `short_answer.md` (Question / Answer / Sources,
   2-5-sentence H2 answer), and `full_answer.md` (all 9 mandatory sections including the DSI table,
   the verdict table with both numerical tests, the per-direction PSP table, the per-synapse
   conductance comparison table, both embedded PNGs, and a synthesis paragraph explaining the
   mechanism). Ran flowmark on both markdown files. Re-tightened the verdict-test row that flowmark
   mis-parsed as a table separator (replaced the `|slope|` notation with plain "abs slope" wording
   so the pipe characters no longer collide with table syntax).
10. **Quality checks.** Ran `uv run ruff check`, `uv run ruff format`,
    `uv run mypy -p tasks.t0048_voff_nmda1_dsi_test.code` — all pass with zero errors.

## Outputs

* `tasks/t0048_voff_nmda1_dsi_test/code/paths.py`
* `tasks/t0048_voff_nmda1_dsi_test/code/constants.py`
* `tasks/t0048_voff_nmda1_dsi_test/code/dsi.py`
* `tasks/t0048_voff_nmda1_dsi_test/code/run_with_conductances.py`
* `tasks/t0048_voff_nmda1_dsi_test/code/run_voff1_sweep.py`
* `tasks/t0048_voff_nmda1_dsi_test/code/compute_metrics.py`
* `tasks/t0048_voff_nmda1_dsi_test/code/render_figures.py`
* `tasks/t0048_voff_nmda1_dsi_test/results/data/gnmda_sweep_trials_voff1.csv` (56 rows, 17 columns)
* `tasks/t0048_voff_nmda1_dsi_test/results/data/gnmda_sweep_trials_voff1_limit.csv` (4 rows from the
  validation gate)
* `tasks/t0048_voff_nmda1_dsi_test/results/data/dsi_by_gnmda_voff1.json`
* `tasks/t0048_voff_nmda1_dsi_test/results/data/dsi_by_gnmda_voff0_from_t0047.json`
* `tasks/t0048_voff_nmda1_dsi_test/results/data/verdict_voff1.json`
* `tasks/t0048_voff_nmda1_dsi_test/results/metrics.json` (7 variants)
* `tasks/t0048_voff_nmda1_dsi_test/results/images/dsi_vs_gnmda_voff0_vs_voff1.png`
* `tasks/t0048_voff_nmda1_dsi_test/results/images/conductance_comparison_voff0_vs_voff1_at_gnmda_0p5.png`
* `tasks/t0048_voff_nmda1_dsi_test/assets/answer/dsi-flatness-test-voltage-independent-nmda/details.json`
* `tasks/t0048_voff_nmda1_dsi_test/assets/answer/dsi-flatness-test-voltage-independent-nmda/short_answer.md`
* `tasks/t0048_voff_nmda1_dsi_test/assets/answer/dsi-flatness-test-voltage-independent-nmda/full_answer.md`

## Issues

No blocking issues. Three minor findings worth recording:

1. **Headline result is H2, not the H1 hypothesis.** Voff_bipNMDA = 1 partially flattens the curve
   (range 0.174 -> 0.066, slope -0.058 -> -0.024 per nS) but does not reach the paper's claimed 0.30
   line — Voff = 1 DSI runs at 0.04-0.10 across the range. The mechanism is exactly the predicted
   one (NMDA PD/ND asymmetry collapses from 2.05 to 1.00 at gNMDA = 0.5), but the paper's flat 0.30
   plateau requires a co-tuning of AMPA / GABA balance that this single- variable swap does not
   provide. Recorded honestly in the answer asset.
2. **Sweep wall-clock was longer than planned.** 13 min 28 s vs the planned ~5 min, driven by a
   higher per-trial cost (~14 s vs ~5 s) at Voff = 1. Still well within the 1-2 hour task budget; no
   replanning needed.
3. **Flowmark interaction with verdict table.** The first version of the verdict row used `|slope|`
   notation, which flowmark parsed as a markdown table cell separator and split the row. Rewrote
   with plain "abs slope" wording. No data loss.

## Requirement Completion Checklist

* **REQ-1** — *done*. Re-used the `modeldb_189347_dsgc_exact` library from t0046 unchanged via the
  registered entry-point imports (`run_one_trial`, `ExperimentType`, `Direction`,
  `ensure_neuron_importable`). Evidence: `code/run_with_conductances.py:30-38`,
  `code/run_voff1_sweep.py:32-38`.
* **REQ-2** — *done*. Centralized paths in `code/paths.py` and constants in `code/constants.py`.
  The sweep grid, trial count, recorder timing, reversal potentials with the t0046 self-check,
  paper-target, the H1 range / slope thresholds, the t0047 H2 reference, all 17 `COL_*` strings, and
  the PD / ND direction labels are all declared. Evidence: `code/paths.py`, `code/constants.py`.
* **REQ-3** — *done*. Copied
  `tasks/t0047_validate_pp16_fig3_cond_noise/code/run_with_conductances.py` to
  `tasks/t0048_voff_nmda1_dsi_test/code/run_with_conductances.py` with the required attribution
  docstring; re-targeted the constants import to the local `tasks.t0048...` path; preserved every
  public function (`build_cell_and_attach_recorders`, `attach_conductance_recorders`,
  `run_one_trial_with_conductances`, `_peak_summed_g_ns`, `_peak_summed_i_na`, `_reset_recorders`)
  and both dataclasses (`ConductanceRecorders`, `TrialResultWithConductances`). Evidence:
  `code/run_with_conductances.py:1-13`.
* **REQ-4** — *done*. Copied `tasks/t0047_validate_pp16_fig3_cond_noise/code/dsi.py` to
  `tasks/t0048_voff_nmda1_dsi_test/code/dsi.py` with the attribution docstring; the
  `compute_dsi_pd_nd(*, pd_values, nd_values) -> float | None` signature is unchanged. Evidence:
  `code/dsi.py:1-12`.
* **REQ-5** — *done*. `code/run_voff1_sweep.py` builds the cell once via
  `build_cell_and_attach_recorders`, then runs the triple loop (gnmda x direction x trial) calling
  `run_one_trial_with_conductances(..., exptype=ExperimentType.ZERO_MG, direction=direction, trial_seed= _trial_seed_for(...), b2gnmda_override=float(b2gnmda_ns))`
  and writes the 17-column CSV. The seed formula `1000 * gnmda_idx + 100 * dir_idx + trial` is
  copied from t0047. Evidence: `code/run_voff1_sweep.py:179-237` (the sweep loop) and
  `code/run_voff1_sweep.py:102-107` (the seed helper).
* **REQ-6** — *done*. Ran the full 56-trial sweep at exptype = ZERO_MG. Wall-clock 13 min 28 s.
  Evidence: `results/data/gnmda_sweep_trials_voff1.csv` has 56 rows.
* **REQ-7** — *done*. Computed DSI per gNMDA from the CSV via `compute_dsi_pd_nd`. Persisted as
  `results/data/dsi_by_gnmda_voff1.json`. Evidence: file exists with 7 keys; values 0.103, 0.102,
  0.078, 0.057, 0.053, 0.044, 0.037.
* **REQ-8** — *done*. Read t0047's baseline CSV via the absolute-path constant
  `T0047_GNMDA_TRIALS_CSV`, applied the same `compute_dsi_pd_nd` helper, and persisted as
  `results/data/dsi_by_gnmda_voff0_from_t0047.json`. Evidence: file exists with the 7 t0047 DSI
  values matching t0047's own `dsi_by_gnmda.json` exactly.
* **REQ-9** — *done*. Rendered `results/images/dsi_vs_gnmda_voff0_vs_voff1.png` with both curves
  plus the horizontal paper-claim line at 0.30 and the +/- 0.05 band. Evidence: file size 56 KB.
* **REQ-10** — *done*. Rendered
  `results/images/conductance_comparison_voff0_vs_voff1_at_gnmda_0p5.png` with 3 channels x 2
  directions x 2 conditions = 12 grouped bars, hatched by direction and color-coded by Voff.
  Evidence: file size 53 KB.
* **REQ-11** — *done*. Per-direction peak PSP amplitudes at gNMDA = 0.5, 1.5, 2.5 nS reported in
  the answer asset's full_answer.md as a 3x4 table with means and standard deviations. Evidence:
  `assets/answer/dsi-flatness-test-voltage- independent-nmda/full_answer.md` "Per-direction PSP
  amplitude comparison" section.
* **REQ-12** — *done*. Both numerical tests computed: range = 0.066 (H1, <= 0.10 threshold) and
  slope = -0.024 per nS (H2, |slope| < |t0047's -0.058| but >= 0.02 H1 cutoff). Combined verdict H2.
  Persisted to `results/data/verdict_voff1.json` and reported in the answer asset.
* **REQ-13** — *done*. `results/metrics.json` uses the explicit multi-variant format with 7
  variants (`voff1_gnmda_0p0ns` through `voff1_gnmda_3p0ns`), each carrying the registered
  `direction_selectivity_index` metric. Evidence: `results/metrics.json` parses cleanly; 7
  variant_id strings present.
* **REQ-14** — *done*. Answer asset `dsi-flatness-test-voltage-independent-nmda` produced with all
  three required files. `full_answer.md` contains: question framing, the DSI table (Voff=0 vs Voff=1
  vs paper), the H0/H1/H2 verdict with both numerical tests, the per-synapse conductance comparison
  table at gNMDA=0.5, the per-direction PSP table at gNMDA=0.5/1.5/2.5, and a synthesis paragraph
  explaining the mechanistic interpretation and the deposited-control implications.
* **REQ-15** — *done*. Smoke test at gNMDA=0.5 (PD): peak_psp_mv = 22.46 mV (within +/- 50% of
  t0047's 23.42 mV) and per-class peak conductances all non-negative finite. Smoke test at gNMDA=3.0
  (PD) also passed, peak_psp_mv finite and inside the +/- 50 mV sanity band. Evidence:
  validation-gate run output and the `_smoke_test_one` assertions in
  `code/run_voff1_sweep.py:138-176`.
* **REQ-16** — *done*. Local CPU only, no Vast.ai, no remote machines. Every CLI call wrapped in
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0048_voff_nmda1_dsi_test -- <command>`.
  Absolute imports used throughout (no relative imports anywhere in the task code). Evidence: every
  `code/*.py` module imports via `from tasks.t0048_voff_nmda1_dsi_test.code.*`.
