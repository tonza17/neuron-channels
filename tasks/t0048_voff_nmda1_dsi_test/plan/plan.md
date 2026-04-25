---
spec_version: "2"
task_id: "t0048_voff_nmda1_dsi_test"
date_completed: "2026-04-25"
status: "complete"
---
# Plan: Test Voff_bipNMDA=1 (Voltage-Independent NMDA) on DSI vs gNMDA Flatness

## Objective

Re-run t0047's exact 7-point gNMDA sweep `b2gnmda in {0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0}` nS at
`exptype = ExperimentType.ZERO_MG` (`= 2`, which sets `Voff_bipNMDA = 1`, voltage-independent NMDA;
the deposited "0 Mg2+" condition in ModelDB 189347) instead of `exptype = ExperimentType.CONTROL`
(`= 1`, `Voff_bipNMDA = 0`, voltage-dependent NMDA with Mg block) used by t0047. Use 4 trials per
direction per gNMDA value (56 trials total). Compute DSI per gNMDA value, overlay on t0047's
`Voff = 0` baseline plus the paper's flat ~0.30 reference line, and produce one answer asset
`dsi-flatness-test-voltage-independent-nmda` containing the DSI table, the H0/H1/H2 verdict with
numerical evidence, and the per-synapse conductance comparison at gNMDA = 0.5 nS. Done means: the
56-trial CSV exists in `results/data/`; the DSI overlay PNG and conductance comparison PNG exist in
`results/images/`; `results/metrics.json` uses the explicit multi-variant format with seven variants
(one per gNMDA value); the answer asset validates against `meta/asset_types/answer/specification.md`
v2; the H0 / H1 / H2 verdict is stated with two numerical tests (max-min DSI range across the 7 grid
points and linear regression slope of DSI vs `b2gnmda_ns`). The task does NOT modify the model —
no HOC, MOD, or t0046 code is changed; only `exptype = 1` is swapped for `exptype = 2` in the trial
runner call.

## Task Requirement Checklist

Operative task request quoted verbatim from `task.json` and `task_description.md`:

```text
Test Voff_bipNMDA=1 (voltage-independent NMDA) on DSI vs gNMDA flatness.

Re-run t0046's gNMDA sweep at exptype=2 (Voff_bipNMDA=1, voltage-independent NMDA) to test if NMDA
voltage-dependence causes the DSI-vs-gNMDA collapse t0047 documented.

Re-use the existing modeldb_189347_dsgc_exact library produced by t0046. No code copy or fork.
Re-use t0047's code/run_with_conductances.py recorder pattern.
Add a thin Python driver code/run_voff1_sweep.py that calls run_one_trial(exptype=2, ...) for the
same b2gnmda in {0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0} nS grid, 4 trials per direction per value
(matching t0047's protocol exactly).
Record per-synapse NMDA / AMPA / GABA conductances for cross-comparison with t0047's
Voff_bipNMDA = 0 data.
Compute DSI per gNMDA value via the same inlined _dsi(*, pd_values, nd_values) helper pattern
from t0047.
Plot DSI vs gNMDA for Voff_bipNMDA = 1 overlaid on t0047's Voff_bipNMDA = 0 curve plus the
paper's flat ~0.30 line, on a single panel.
Report per-direction PSP amplitudes at gNMDA = 0.5, 1.5, 2.5 nS to characterize how
voltage-independence affects the absolute amplitudes.

Pass criterion: per-grid-point DSI within +/- 0.05 of constant determines H1; clearly flatter than
t0047 but still trending = H2; same shape as t0047 = H0.
```

Concrete requirements extracted from the quoted task text and from `task_description.md`:

* **REQ-1** — Re-use the `modeldb_189347_dsgc_exact` library from t0046 unchanged. Cross-task
  imports via the registered library entry points:
  `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun import run_one_trial, TrialResult`,
  `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.constants import ExperimentType, Direction, B2GNMDA_CODE, V_INIT_MV, TSTOP_MS, DT_MS, E_SACINHIB_MV`,
  `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.neuron_bootstrap import ensure_neuron_importable`.
  NO modification to t0046. Satisfied by Steps 4, 6, 7, 8.
* **REQ-2** — Centralise paths in `code/paths.py` and constants in `code/constants.py` per the
  project Python style guide. Constants must include the gNMDA sweep grid
  `B2GNMDA_GRID_NS = (0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0)`, trial count `TRIALS_PER_CELL = 4`,
  recording sub-sample interval `DT_RECORD_MS = 0.25`, paper-target `DSI_PAPER_FIG3F_TARGET = 0.30`
  and tolerance band `DSI_FIG3F_TOLERANCE = 0.05`, the H1 max-min range threshold
  `DSI_RANGE_FLAT_THRESHOLD = 0.10`, the H1 slope threshold `DSI_SLOPE_FLAT_THRESHOLD = 0.02`,
  reversal potentials `E_BIPNMDA_MV = 0.0`, `E_SACEXC_MV = 0.0`, `E_SACINHIB_MV_OVERRIDE = -60.0`
  (with the `assert E_SACINHIB_MV_OVERRIDE == _T0046_E_SACINHIB_MV` self-check), direction labels
  `DIRECTION_PD_LABEL = "PD"` / `DIRECTION_ND_LABEL = "ND"`, and all 17 `COL_*` strings matching
  t0047's CSV schema. Satisfied by Steps 4, 5.
* **REQ-3** — Copy `tasks/t0047_validate_pp16_fig3_cond_noise/code/run_with_conductances.py`
  verbatim (with leading attribution comment naming t0047 as the source and stating the t0048 use
  case `Voff_bipNMDA = 1`) into `tasks/t0048_voff_nmda1_dsi_test/code/run_with_conductances.py`.
  t0047 is NOT a registered library asset (it only produced an answer asset), so per the project's
  cross-task code-reuse rule, only library-registered code may be cross-imported and t0047's
  recorder must be COPIED. Re-target the smoke-test's `from tasks.t0047...` self-import to
  `from tasks.t0048_voff_nmda1_dsi_test.code.constants import ...` (or delete the smoke-test block).
  Public surface preserved: `build_cell_and_attach_recorders`, `attach_conductance_recorders`,
  `run_one_trial_with_conductances`, dataclasses `ConductanceRecorders` and
  `TrialResultWithConductances`. Satisfied by Step 6.
* **REQ-4** — Copy `tasks/t0047_validate_pp16_fig3_cond_noise/code/dsi.py` verbatim (with leading
  attribution comment naming t0047 as the source) into
  `tasks/t0048_voff_nmda1_dsi_test/code/dsi.py`. The function signature
  `compute_dsi_pd_nd(*, pd_values: list[float], nd_values: list[float]) -> float | None` is exactly
  what t0048 needs — no adaptation. Satisfied by Step 6.
* **REQ-5** — Implement `code/run_voff1_sweep.py` as a thin driver that builds the cell and
  recorders ONCE via `build_cell_and_attach_recorders()`, then iterates the triple loop
  `for gi, b2gnmda in enumerate(B2GNMDA_GRID_NS)` x
  `for di, (direction, dir_label) in enumerate(((Direction.PREFERRED, "PD"), (Direction.NULL, "ND")))`
  x `for trial in range(TRIALS_PER_CELL)`. Each iteration calls
  `run_one_trial_with_conductances(recorders=recorders, exptype=ExperimentType.ZERO_MG, direction=direction, trial_seed=_trial_seed_for(gnmda_idx=gi, dir_idx=di, trial=trial), flicker_var=0.0, stim_noise_var=0.0, b2gnmda_override=float(b2gnmda))`
  and writes one CSV row per trial to `results/data/gnmda_sweep_trials_voff1.csv` with the same
  17-column schema as t0047's CSV. The trial-seed helper
  `_trial_seed_for(*, gnmda_idx, dir_idx, trial) -> int = 1000 * gnmda_idx + 100 * dir_idx + trial`
  is COPIED from `tasks/t0047_validate_pp16_fig3_cond_noise/code/run_fig3_validation.py:84-85` so PD
  trial 0 at gNMDA = 0.5 (gnmda_idx = 1) gets seed `1100` for both `Voff = 0` (t0047) and `Voff = 1`
  (t0048) — identical noise realizations isolate the Voff effect. Satisfied by Steps 7, 8.
* **REQ-6** — Run the full 56-trial sweep (7 gNMDA x 2 directions x 4 trials) at
  `exptype = ExperimentType.ZERO_MG`. Total wall-clock estimate: ~5 sec/trial x 56 trials = ~5
  minutes, matching t0047's measured wall-clock. Satisfied by Step 8.
* **REQ-7** — Compute DSI per gNMDA value from the freshly written `gnmda_sweep_trials_voff1.csv`
  using
  `compute_dsi_pd_nd(pd_values=<peak_psp_mv for PD trials>, nd_values=<peak_psp_mv for ND trials>)`.
  Persist as JSON `results/data/dsi_by_gnmda_voff1.json` (one entry per gNMDA value, matching
  t0047's `dsi_by_gnmda.json` schema). Satisfied by Step 9.
* **REQ-8** — Read t0047's baseline data from
  `tasks/t0047_validate_pp16_fig3_cond_noise/results/data/gnmda_sweep_trials.csv` (the canonical
  Voff = 0 baseline; verified read-only with no correction overlays affecting it) via absolute path
  constant in `code/paths.py`. Apply the same `compute_dsi_pd_nd` helper to compute Voff = 0 DSI per
  gNMDA. Persist as JSON `results/data/dsi_by_gnmda_voff0_from_t0047.json` for transparency.
  Satisfied by Steps 9, 10.
* **REQ-9** — Render `results/images/dsi_vs_gnmda_voff0_vs_voff1.png` (single panel, x = gNMDA in
  nS, y = DSI, two curves: Voff = 0 from t0047 in one colour and Voff = 1 from this task in another
  colour, with a horizontal
  `axhline(DSI_PAPER_FIG3F_TARGET, color="grey", linestyle="--", label="paper claim 0.30")`). Use
  raw matplotlib only (the t0011 visualisation library is for 12-angle tuning curves and does not
  fit the 2-direction PD/ND data shape). Satisfied by Step 10.
* **REQ-10** — Render `results/images/conductance_comparison_voff0_vs_voff1_at_gnmda_0p5.png` (bar
  chart, x = three synapse classes `NMDA / AMPA / GABA`, two grouped bars per class: t0047 Voff = 0
  mean of `peak_g_nmda_summed_ns` / `peak_g_ampa_summed_ns` / `peak_g_sacinhib_summed_ns` at
  `b2gnmda_ns == 0.5`, and the corresponding t0048 Voff = 1 means from this task's CSV at the same
  gNMDA value). Both curves include separate PD vs ND bars (so 12 bars total per panel: 3 channels x
  2 directions x 2 conditions). Satisfied by Step 10.
* **REQ-11** — Report per-direction peak PSP amplitudes at gNMDA = 0.5, 1.5, 2.5 nS in the answer
  asset's `full_answer.md` to characterize how voltage-independence affects absolute amplitudes (per
  `task_description.md` In-Scope item 7). Satisfied by Steps 9, 11.
* **REQ-12** — Compute the H0 / H1 / H2 verdict using two numerical tests: (a) **range test**:
  max-min DSI across the 7 grid points; H1 if range <= 0.10, H2 if range < t0047's range (= 0.192 -
  0.018 = 0.174), H0 otherwise. (b) **slope test**: linear regression of DSI vs `b2gnmda_ns`
  (numpy.polyfit deg=1); H1 if `|slope| < 0.02` per nS, H2 if `|slope|` < t0047's slope, H0
  otherwise. Both numbers MUST be recorded in the answer asset alongside the verdict. Satisfied by
  Steps 9, 11.
* **REQ-13** — Write `results/metrics.json` in the explicit multi-variant format with seven
  variants (one per gNMDA value, named `voff1_gnmda_0p0ns`, `voff1_gnmda_0p5ns`, ...,
  `voff1_gnmda_3p0ns`). Each variant records `direction_selectivity_index` (registered metric
  `direction_selectivity_index` per `meta/metrics/`). Per
  `arf/specifications/metrics_specification.md` v4 and
  `arf/specifications/task_results_specification.md` v8. Satisfied by Step 9.
* **REQ-14** — Produce the answer asset
  `tasks/t0048_voff_nmda1_dsi_test/assets/answer/dsi-flatness-test-voltage-independent-nmda/` per
  `meta/asset_types/answer/specification.md` v2: `details.json` (with `spec_version: "2"`,
  `short_answer_path`, `full_answer_path`, the question framing, source list citing
  `t0046_reproduce_poleg_polsky_2016_exact`, `t0047_validate_pp16_fig3_cond_noise`, and the
  Poleg-Polsky 2016 paper asset `10.1016_j.neuron.2016.02.013`), `short_answer.md` (Question /
  Answer / Sources), and `full_answer.md` (Question / Short Answer / Research Process / Evidence
  from Papers / Evidence from Internet Sources / Evidence from Code or Experiments / Synthesis /
  Limitations / Sources). The `full_answer.md` must contain: question framing, DSI-vs-gNMDA table
  (Voff = 0 vs Voff = 1 vs paper), H0 / H1 / H2 verdict with numerical evidence (range and slope
  tests), per-synapse conductance comparison table at gNMDA = 0.5, per-direction PSP amplitude table
  at gNMDA = 0.5 / 1.5 / 2.5 nS, and a synthesis paragraph explaining the mechanistic interpretation
  and what the result means for the deposited control choice (`exptype = 1` vs `exptype = 2`).
  Satisfied by Step 11.
* **REQ-15** — Smoke-test the recorder + sweep before running the full 56-trial sweep: invoke
  `run_one_trial_with_conductances(..., exptype=ExperimentType.ZERO_MG, direction=Direction.PREFERRED, trial_seed=1, b2gnmda_override=0.5)`
  and assert (a) `peak_psp_mv` is finite and within +/- 50% of t0047's PD peak at gNMDA = 0.5
  (sanity check that the swap to ZERO_MG did not break the pipeline); (b) per-class summed peak
  conductances are non-negative and finite. Repeat at `b2gnmda_override=3.0` to flag the task
  description's risk #1 (unphysical results at high gNMDA). Failure stops the sweep. Satisfied by
  Step 8.
* **REQ-16** — Local CPU only; no Vast.ai; no remote machines. Use absolute imports throughout.
  Wrap every CLI call in
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0048_voff_nmda1_dsi_test -- <command>`
  per the project Python style guide. Satisfied by every Step that invokes a script.

## Approach

The implementation re-uses the entire t0046 + t0047 infrastructure:

* **Library imports from t0046** (registered library `modeldb_189347_dsgc_exact` per
  `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/details.json`):
  `run_one_trial`, `TrialResult`, `ExperimentType`, `Direction`, `ensure_neuron_importable`,
  `B2GNMDA_CODE`, `V_INIT_MV`, `TSTOP_MS`, `DT_MS`, `E_SACINHIB_MV`. These are library entry points
  and are imported via `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.* import ...`. No
  modification.
* **Files COPIED from t0047** (t0047 is NOT a library asset, only an answer asset):
  `tasks/t0047_validate_pp16_fig3_cond_noise/code/run_with_conductances.py` (~340 lines) and
  `tasks/t0047_validate_pp16_fig3_cond_noise/code/dsi.py` (~37 lines). Each copy carries an
  attribution comment at the top naming t0047 as the source plus the t0048 use case ("Voff_bipNMDA =
  1 sweep"). The `_trial_seed_for` formula `1000 * gnmda_idx + 100 * dir_idx + trial` is also copied
  so PD/ND noise realizations match t0047 trial-by-trial.
* **Single substantive code change** versus t0047's sweep loop: `exptype=ExperimentType.CONTROL` (=
  1\) becomes `exptype=ExperimentType.ZERO_MG` (= 2) at the `runner(...)` call. Per the deposited
  HOC code at
  `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/sources/main.hoc:349-368`,
  `simplerun($1, $2)` sets `Voff_bipNMDA = ($1 == 2)` and changes nothing else (`b2gampa`,
  `b2gnmda`, `s2ggaba`, `s2gach`, `gabaMOD`, `achMOD`, `Vset_bipNMDA`, channel / cable / morphology
  parameters all stay identical). This is the clean experimental swap the task hypothesis requires.

**Mechanistic prediction (per `research/research_code.md`)**: at `Vset_bipNMDA = -43`, `n = 0.3`,
`gama = 0.07` (the canonical main.hoc overrides), the Voff = 1 setting drives roughly 4.2x larger
NMDA conductance at hyperpolarized voltages than the deposited Voff = 0 control. At high gNMDA
values, Voff = 0 has a runaway feedback (more NMDA -> more depolarization -> less Mg block -> more
NMDA), and the ND branch eventually saturates so PD/ND distinction collapses. Voff = 1 removes that
feedback by clamping the Mg-block term to a voltage-independent constant. If this mechanistic story
is correct, the H1 verdict (flat DSI vs gNMDA) follows. The task plan does not pre-commit to a
verdict; the numerical tests in REQ-12 distinguish among H0 / H1 / H2.

**Recommended task type** (already declared in `task.json`): `experiment-run`. Per
`meta/task_types/experiment-run/instruction.md`, this task: (a) defines the hypothesis explicitly
(H0 / H1 / H2); (b) has one independent variable (`Voff_bipNMDA`, swept across one value `= 1`
versus t0047's `= 0` baseline) plus the secondary independent variable `b2gnmda` swept across 7
values; (c) reports per-variant `direction_selectivity_index` in the multi-variant `metrics.json`;
(d) uses fixed seeds (the `_trial_seed_for` formula); (e) compares against an explicit baseline
(t0047's `Voff = 0` curve and the paper's flat 0.30 claim); (f) inspects individual outputs (the
smoke-test in REQ-15 reads single-trial PSP and conductance values before the full sweep). The plan
satisfies every Implementation Guideline that applies; metrics guidelines
`efficiency_training_time_seconds`, `efficiency_inference_time_per_item_seconds`,
`efficiency_inference_cost_per_item_usd` do not apply because no model is trained and no billable
inference occurs (CPU-only NEURON simulation). The `predictions` asset and `model` asset guidelines
do not apply for the same reason.

**Alternatives considered**:

* *Cross-task IMPORT t0047's `run_with_conductances.py` and `dsi.py` instead of copying.* Rejected:
  the project's cross-task code-reuse rule (CLAUDE.md, Key Rule 9 / arf/README.md Subagent-Isolation
  principle) says only library-registered code may be cross-imported. t0047 produces only an answer
  asset, not a library asset, so its `code/` subtree is task-internal and must be copied with
  attribution. Importing would break the rule and risk silent breakage if t0047's code drifts.
* *Add a separate exptype to the t0046 library to express "Voff = 1 with Mg block disabled".*
  Rejected: this is a model modification, out of scope per `task_description.md`. The deposited
  `exptype = 2` already maps cleanly to `Voff_bipNMDA = 1` and is the canonical paper-aligned
  setting.
* *Run a finer gNMDA grid (e.g. 14 values) for sharper H1 / H2 discrimination.* Rejected: the task
  hypothesis requires a direct comparison to t0047's 7-point grid; using a different grid would
  force a separate baseline run and double the wall-clock budget. Future tasks may sweep a finer
  grid (already captured under suggestion S-0046-01 / S-0047-01 follow-ups).

## Cost Estimation

* **API costs**: $0.00. No LLM calls, no paid services.
* **Remote compute**: $0.00. Local CPU only; no Vast.ai or other cloud provider.
* **Project budget remaining**: $1.00 (per `project/budget.json`); $0.00 spent so far.
* **Task allocated budget**: $1.00 (per-task default limit per `project/budget.json`).
* **Estimated total task cost**: $0.00. The 56 NEURON trials run in ~5 minutes wall-clock on the
  developer's local CPU; no billable resources are consumed.

## Step by Step

### Milestone A: Scaffold task code (Steps 1-6)

1. **Verify worktree and dependency state.** Run
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0048_voff_nmda1_dsi_test -- uv run python -u -m arf.scripts.aggregators.aggregate_tasks --format json --detail full --ids t0007_install_neuron_netpyne t0046_reproduce_poleg_polsky_2016_exact t0047_validate_pp16_fig3_cond_noise`.
   Expected: every dependency is `status: completed`. If not, halt and create an intervention file.
   Satisfies REQ-1.

2. **Smoke test t0046 import path.** Create `code/_smoke_imports.py` that imports
   `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun import run_one_trial`,
   `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.constants import ExperimentType, Direction`,
   and
   `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.neuron_bootstrap import ensure_neuron_importable`.
   Run via
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0048_voff_nmda1_dsi_test -- uv run python -u tasks/t0048_voff_nmda1_dsi_test/code/_smoke_imports.py`.
   Expected: prints `IMPORTS OK exptype.ZERO_MG=2`. Delete the file after the smoke check is logged.
   Satisfies REQ-1.

3. **Verify cross-task data file is present.** Run
   `ls -l tasks/t0047_validate_pp16_fig3_cond_noise/results/data/gnmda_sweep_trials.csv`. Expected:
   file exists, size > 5 KB, 57 lines (1 header + 56 trial rows). If absent, halt and create an
   intervention file (the t0047 baseline is required for the overlay chart). Satisfies REQ-8.

4. **Create `code/paths.py`.** Define `TASK_ROOT = Path(__file__).resolve().parent.parent`,
   subdirectories `RESULTS_DIR`, `RESULTS_DATA_DIR`, `RESULTS_IMAGES_DIR`, `ASSETS_DIR`,
   `ASSETS_ANSWER_DIR = ASSETS_DIR / "answer" / "dsi-flatness-test-voltage-independent-nmda"`,
   `LOGS_DIR`, the t0047 baseline CSV path
   `T0047_GNMDA_TRIALS_CSV = TASK_ROOT.parent / "t0047_validate_pp16_fig3_cond_noise" / "results" / "data" / "gnmda_sweep_trials.csv"`,
   plus the per-output paths `GNMDA_TRIALS_VOFF1_CSV`, `DSI_BY_GNMDA_VOFF1_JSON`,
   `DSI_BY_GNMDA_VOFF0_FROM_T0047_JSON`, `METRICS_JSON`,
   `DSI_OVERLAY_PNG = RESULTS_IMAGES_DIR / "dsi_vs_gnmda_voff0_vs_voff1.png"`,
   `CONDUCTANCE_COMPARISON_PNG = RESULTS_IMAGES_DIR / "conductance_comparison_voff0_vs_voff1_at_gnmda_0p5.png"`.
   Satisfies REQ-2.

5. **Create `code/constants.py`.** Copy the relevant subset of t0047's `code/constants.py`
   (`B2GNMDA_GRID_NS`, `TRIALS_PER_CELL`, `DT_RECORD_MS`, `E_BIPNMDA_MV`, `E_SACEXC_MV`,
   `E_SACINHIB_MV_OVERRIDE`, the `assert E_SACINHIB_MV_OVERRIDE == _T0046_E_SACINHIB_MV` self-check,
   `DSI_PAPER_FIG3F_TARGET`, `DSI_FIG3F_TOLERANCE`, `DIRECTION_PD_LABEL`, `DIRECTION_ND_LABEL`,
   `METRIC_KEY_DSI`, all 17 `COL_*` strings) and add three new constants specific to t0048:
   `DSI_RANGE_FLAT_THRESHOLD: float = 0.10` (REQ-12 range test threshold),
   `DSI_SLOPE_FLAT_THRESHOLD: float = 0.02` (REQ-12 slope test threshold per nS), and
   `T0047_DSI_RANGE_REFERENCE: float = 0.174` (the empirical t0047 range = 0.192 - 0.018, used as
   the H2 reference). Add a leading attribution docstring naming t0047 as the source for the
   re-declared constants. Satisfies REQ-2.

6. **Copy `run_with_conductances.py` and `dsi.py` from t0047 with attribution.** Copy
   `tasks/t0047_validate_pp16_fig3_cond_noise/code/run_with_conductances.py` to
   `tasks/t0048_voff_nmda1_dsi_test/code/run_with_conductances.py` and
   `tasks/t0047_validate_pp16_fig3_cond_noise/code/dsi.py` to
   `tasks/t0048_voff_nmda1_dsi_test/code/dsi.py`. Prepend each file with a comment block:
   `"""COPIED from tasks/t0047_validate_pp16_fig3_cond_noise/code/<filename>.py per the project's cross-task code-reuse rule (t0047 is not a registered library asset). Use case: t0048's Voff_bipNMDA = 1 sweep. Original attribution preserved below."""`.
   Re-target imports inside the copied `run_with_conductances.py` from
   `tasks.t0047_validate_pp16_fig3_cond_noise.code.*` to `tasks.t0048_voff_nmda1_dsi_test.code.*`
   (only the constants module reference changes; t0046 imports stay the same). Optionally delete the
   smoke-test block at the bottom of `run_with_conductances.py` (it is invoked only manually). Run
   `uv run mypy tasks/t0048_voff_nmda1_dsi_test/code/run_with_conductances.py tasks/t0048_voff_nmda1_dsi_test/code/dsi.py`
   and confirm 0 errors before proceeding. Satisfies REQ-3, REQ-4.

### Milestone B: Implement the Voff = 1 sweep (Steps 7-8)

7. **Implement `code/run_voff1_sweep.py`.** Single-file driver. Copy and adapt the
   `_run_gnmda_sweep` function from
   `tasks/t0047_validate_pp16_fig3_cond_noise/code/run_fig3_validation.py:116-158` (~45 lines):
   change `exptype=ExperimentType.CONTROL` to `exptype=ExperimentType.ZERO_MG` at the `runner(...)`
   call (line 143 in t0047's source); change `out_csv_path` constant to t0048's
   `GNMDA_TRIALS_VOFF1_CSV`; change tqdm `desc` to `"gNMDA sweep (Voff=1)"`. Copy the
   `_trial_seed_for` and `_row_for` helpers verbatim. Imports: `run_one_trial_with_conductances` and
   `build_cell_and_attach_recorders` from this task's local `code/run_with_conductances.py`;
   `ExperimentType`, `Direction`, `ensure_neuron_importable` from t0046; `B2GNMDA_GRID_NS`,
   `TRIALS_PER_CELL`, all `COL_*` constants from this task's `code/constants.py`;
   `GNMDA_TRIALS_VOFF1_CSV`, `RESULTS_DATA_DIR` from this task's `code/paths.py`. The `main()`
   function calls `ensure_neuron_importable()` first, then
   `recorders = build_cell_and_attach_recorders()`, then runs the smoke test described in REQ-15
   (call
   `run_one_trial_with_conductances(recorders, exptype=ExperimentType.ZERO_MG, direction=Direction.PREFERRED, trial_seed=1, b2gnmda_override=0.5)`
   and assert `np.isfinite(result.trial.peak_psp_mv) and abs(result.trial.peak_psp_mv) < 100.0`;
   repeat at `b2gnmda_override=3.0`), then calls
   `_run_gnmda_sweep(recorders=recorders, runner=run_one_trial_with_conductances, grid=B2GNMDA_GRID_NS, trials_per_cell=TRIALS_PER_CELL, out_csv_path=GNMDA_TRIALS_VOFF1_CSV)`.
   Add an `argparse --limit N` option to support a small validation run. Satisfies REQ-5, REQ-15.

8. **Run the smoke test then the full sweep.** **[CRITICAL]** First validate:
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0048_voff_nmda1_dsi_test -- uv run python -u -m tasks.t0048_voff_nmda1_dsi_test.code.run_voff1_sweep --limit 4`.
   This runs only 4 trials (one PD + ND pair at gNMDA = 0.0 and 0.5). Inspect the resulting CSV
   manually: confirm 4 rows, 17 columns, finite `peak_psp_mv` values. **Validation gate**: t0047's
   PD `peak_psp_mv` at gNMDA = 0.5 is approximately 9-12 mV (per t0047's `gnmda_sweep_trials.csv`);
   the Voff = 1 PD value should be within +/- 50% of that. If the Voff = 1 PD value is below 4 mV or
   above 25 mV, STOP and inspect the recorder output before proceeding. After the small run passes,
   read 5 individual trial rows and verify they look reasonable. Then run the full sweep:
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0048_voff_nmda1_dsi_test -- uv run python -u -m tasks.t0048_voff_nmda1_dsi_test.code.run_voff1_sweep`.
   Expected: 56-row CSV at `results/data/gnmda_sweep_trials_voff1.csv`; ~5 minutes wall-clock; tqdm
   progress bar reaches 56 / 56. Satisfies REQ-5, REQ-6, REQ-15.

### Milestone C: Compute metrics and produce comparison artifacts (Steps 9-10)

9. **Implement `code/compute_metrics.py`.** Reads the freshly written `gnmda_sweep_trials_voff1.csv`
   plus t0047's baseline `gnmda_sweep_trials.csv` via `pandas.read_csv` with explicit dtypes. For
   each of the 7 gNMDA values, splits PD vs ND rows by `direction` column and calls
   `compute_dsi_pd_nd(pd_values=<list of peak_psp_mv for PD>, nd_values=<list of peak_psp_mv for ND>)`.
   Writes: (a) `results/data/dsi_by_gnmda_voff1.json` — `{"0.0": <dsi>, "0.5": <dsi>, ...}`; (b)
   `results/data/dsi_by_gnmda_voff0_from_t0047.json` — same shape from t0047's CSV; (c)
   `results/metrics.json` — explicit multi-variant format per
   `arf/specifications/metrics_specification.md` v4 and
   `arf/specifications/task_results_specification.md` v8. Seven variants named `voff1_gnmda_0p0ns`,
   `voff1_gnmda_0p5ns`, ..., `voff1_gnmda_3p0ns`, each with
   `metrics: {"direction_selectivity_index": <value>}` and a `description` like
   `"Voff_bipNMDA=1 (voltage-independent NMDA), b2gnmda=0.5 nS, 4 trials per direction"`. Also
   computes the H0 / H1 / H2 verdict tests (REQ-12): max-min DSI range across the 7 grid points, and
   `numpy.polyfit(b2gnmda_array, dsi_array, deg=1)` slope. Persists both numbers and the verdict
   label to `results/data/verdict_voff1.json` for downstream use by the answer asset writer.
   Satisfies REQ-7, REQ-8, REQ-12, REQ-13.

10. **Implement `code/render_figures.py`.** Reads `dsi_by_gnmda_voff1.json` and
    `dsi_by_gnmda_voff0_from_t0047.json`, plus the two CSVs (for the conductance comparison).
    Produces: (a) `results/images/dsi_vs_gnmda_voff0_vs_voff1.png` (REQ-9):
    `matplotlib.pyplot.figure(figsize=(7, 5))`,
    `plot(B2GNMDA_GRID_NS, voff0_dsi, marker="o", label="Voff=0 (t0047 baseline)")`,
    `plot(B2GNMDA_GRID_NS, voff1_dsi, marker="s", label="Voff=1 (this task)")`,
    `axhline(DSI_PAPER_FIG3F_TARGET, color="grey", linestyle="--", label="paper claim 0.30")`,
    `axhspan(DSI_PAPER_FIG3F_TARGET - DSI_FIG3F_TOLERANCE, DSI_PAPER_FIG3F_TARGET + DSI_FIG3F_TOLERANCE, color="grey", alpha=0.15, label="+/- 0.05 band")`,
    `xlabel("b2gnmda (nS)")`, `ylabel("DSI")`, `title("DSI vs gNMDA: Voff=0 vs Voff=1 vs paper")`,
    `legend()`, `grid(True, alpha=0.3)`, `savefig(DSI_OVERLAY_PNG, dpi=120)`. (b)
    `results/images/conductance_comparison_voff0_vs_voff1_at_gnmda_0p5.png` (REQ-10): bar chart with
    3 channels x 2 directions x 2 conditions = 12 grouped bars. Read both CSVs filtered to
    `b2gnmda_ns == 0.5`, group by `direction`, mean of `peak_g_nmda_summed_ns` /
    `peak_g_ampa_summed_ns` / `peak_g_sacinhib_summed_ns`; plot grouped bars with `plt.bar` and
    offsets. Use distinct colours for Voff = 0 vs Voff = 1, hatching for PD vs ND.
    `savefig(CONDUCTANCE_COMPARISON_PNG, dpi=120)`. Satisfies REQ-9, REQ-10.

### Milestone D: Write the answer asset (Step 11)

11. **Write the answer asset** at
    `tasks/t0048_voff_nmda1_dsi_test/assets/answer/dsi-flatness-test-voltage-independent-nmda/`.
    Three files: (a) `details.json` per `meta/asset_types/answer/specification.md` v2 with
    `spec_version: "2"`, `answer_id: "dsi-flatness-test-voltage-independent-nmda"`,
    `question: "Does setting Voff_bipNMDA = 1 (voltage-independent NMDA) reproduce the paper's claim that DSI vs gNMDA is approximately constant ~0.30 across 0-3 nS?"`,
    `short_title: "Voff_bipNMDA=1 DSI flatness test"`, `short_answer_path: "short_answer.md"`,
    `full_answer_path: "full_answer.md"`,
    `categories: ["direction-selectivity", "compartmental-modeling", "synaptic-integration"]`,
    `answer_methods: ["code-experiment", "papers"]`,
    `source_paper_ids: ["10.1016_j.neuron.2016.02.013"]`, `source_urls: []`,
    `source_task_ids: ["t0046_reproduce_poleg_polsky_2016_exact", "t0047_validate_pp16_fig3_cond_noise"]`,
    `confidence` chosen based on the verdict (`"high"` if the verdict is unambiguous, `"medium"` if
    the smoke-test flagged any anomaly), `created_by_task: "t0048_voff_nmda1_dsi_test"`,
    `date_created: "<today>"`. (b) `short_answer.md` per the spec: YAML frontmatter, `## Question`
    (verbatim), `## Answer` (2-5 sentences stating the H0 / H1 / H2 verdict directly with the
    headline numerical evidence), `## Sources` (bullet list of paper / tasks). NO inline citations
    in `## Answer`. (c) `full_answer.md` per the spec: YAML frontmatter (with matching
    `confidence`), `## Question` (verbatim), `## Short Answer` (2-5 sentences, citation-free),
    `## Research Process` (describes the swap from `exptype=1` to `exptype=2` and the trial-seed
    alignment with t0047), `## Evidence from Papers` (one-paragraph summary of Poleg-Polsky 2016's
    Fig 3F flat ~0.30 claim and the in-vivo voltage-independence text statement),
    `## Evidence from Internet Sources` (single sentence: "The `internet` method was not used; t0046
    \+ t0047 already exhausted the corpus."), `## Evidence from Code or Experiments` (the DSI table
    — Voff = 0 from t0047 vs Voff = 1 from this task vs paper, the per-direction PSP table at
    gNMDA = 0.5 / 1.5 / 2.5 nS, the per-synapse conductance comparison table at gNMDA = 0.5, and the
    two embedded figure references
    `![DSI overlay](../../../results/images/dsi_vs_gnmda_voff0_vs_voff1.png)` and
    `![Conductance comparison](../../../results/images/conductance_comparison_voff0_vs_voff1_at_gnmda_0p5.png)`),
    `## Synthesis` (mechanistic interpretation: does removing voltage-dependent NMDA flatten the
    curve?, what does this mean for the deposited control choice?), `## Limitations` (small N per
    condition (4 trials), single sweep dimension, no AP5 cross-control, no SEClamp re-measurement of
    conductances), `## Sources` (bullet list with reference link definitions). Satisfies REQ-11,
    REQ-14.

## Remote Machines

None required. The task runs the 56-trial NEURON sweep entirely on the developer's local CPU in ~5
minutes wall-clock. Per `task_description.md` Execution Guidance: "Local CPU only. No Vast.ai."
NEURON state is process-global and not pickle-friendly, so there would be no benefit from
process-pool parallelism even if a remote machine were used.

## Assets Needed

* **Library asset** `modeldb_189347_dsgc_exact` from
  `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/`
  (registered library; entry points listed in its `details.json`). Provides the cell builder, the
  `run_one_trial` driver, and the `ExperimentType` / `Direction` enums.
* **Answer asset** `polegpolsky-2016-fig3-conductances-validation` from
  `tasks/t0047_validate_pp16_fig3_cond_noise/assets/answer/` (read-only context for the task's
  hypothesis framing).
* **Per-trial CSV** `tasks/t0047_validate_pp16_fig3_cond_noise/results/data/gnmda_sweep_trials.csv`
  (the canonical Voff = 0 baseline for the overlay chart; 56 rows, 17 columns, no correction
  overlays applied).
* **Code files COPIED from t0047** (with attribution): `code/run_with_conductances.py` and
  `code/dsi.py`. See REQ-3, REQ-4.
* **Paper asset** `10.1016_j.neuron.2016.02.013` from
  `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/paper/10.1016_j.neuron.2016.02.013/` (cited
  in the answer asset's `## Evidence from Papers` section).

## Expected Assets

Match `task.json` `expected_assets: {"answer": 1}`:

* **answer asset** (`dsi-flatness-test-voltage-independent-nmda`) at
  `tasks/t0048_voff_nmda1_dsi_test/assets/answer/dsi-flatness-test-voltage-independent-nmda/`.
  Contents per `meta/asset_types/answer/specification.md` v2: `details.json`, `short_answer.md`,
  `full_answer.md`. The full answer contains the DSI table (Voff = 0 vs Voff = 1 vs paper), the H0 /
  H1 / H2 verdict with two numerical tests (range and slope), the per-synapse conductance comparison
  table at gNMDA = 0.5 nS, the per-direction PSP table at gNMDA = 0.5 / 1.5 / 2.5 nS, the two
  embedded PNGs, and a synthesis paragraph.

No dataset / library / model / paper / predictions assets are produced by this task.

## Time Estimation

* Research (already complete): n/a.
* Planning (this step): ~30 minutes.
* Implementation Milestone A (scaffold task code): ~25 minutes (mostly file copies plus 5-line
  modifications).
* Implementation Milestone B (sweep): ~5 minutes for the smoke test plus ~5 minutes for the full
  56-trial sweep, ~10 minutes total wall-clock plus ~10 minutes coding/debug headroom.
* Implementation Milestone C (metrics + figures): ~25 minutes (~10 min compute_metrics.py, ~15 min
  render_figures.py).
* Implementation Milestone D (answer asset writing): ~30 minutes.
* Reporting / verification (orchestrator-managed, post-plan): ~30 minutes.
* **Total wall-clock**: ~2 hours, matching the `task_description.md` estimate of 1-2 hours.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Voff = 1 produces unphysical PSP at high gNMDA (saturation / spurious spikes with TTX on) | Medium | Blocks DSI computation | REQ-15 smoke test runs at gNMDA = 0.5 and gNMDA = 3.0 before the full sweep. If `peak_psp_mv` is non-finite or > 25 mV, halt and inspect the soma trace; record the failure as the H2 evidence (Voff = 1 destabilizes the cell at high gNMDA). Confirmed `SpikesOn = 0` (TTX on) in the t0046 library. |
| t0047 baseline CSV missing or moved | Low | Cannot render overlay | Step 3 verifies file existence before any sweep starts. Fallback: read the cached `dsi_by_gnmda.json` from t0047 instead of recomputing from CSV (slightly less transparent but unblocks the chart). |
| `run_one_trial`'s `b2gnmda_override` re-apply loop fails silently and the sweep collapses to gNMDA = 0.5 across all 56 trials (the bug t0046 fixed) | Low | All 7 variants would have identical DSI | After the smoke test in Step 8, manually verify the first 14 trials of the CSV: PD trials at gNMDA = 0.0 should show much smaller peak_g_nmda_summed_ns than at gNMDA = 3.0. If all gNMDA values produce identical conductance, halt and inspect `run_simplerun.py:130-151` for regression. |
| Result is H0 (same shape as t0047) — voltage-dependence is NOT the cause | Medium | Disproves the working hypothesis | The H0 outcome is still informative and satisfies REQ-12. The answer asset's synthesis paragraph must honestly state "the candidate mechanism is rejected" and include suggestions for follow-up tasks (e.g., test gabaMOD = 0 to check whether it is the inhibition path that drives the collapse). |
| Cross-task copy of t0047's `run_with_conductances.py` re-imports a t0047-internal symbol that t0048 does not provide | Low | mypy fails at Step 6 | Step 6 mandates re-targeting t0047 imports to t0048 paths and running mypy before proceeding. If a non-trivial t0047 dependency surfaces, copy that helper module too with attribution. |
| Wall-clock blows past the 1-2 hour estimate due to NEURON build issues on Windows | Low | Schedule slip | Smoke test in Step 2 catches NEURON import failures early. The `ensure_neuron_importable` bootstrap is the same one t0046 + t0047 use successfully. |

## Verification Criteria

* **Plan verificator**:
  `uv run python -u -m arf.scripts.verificators.verify_plan t0048_voff_nmda1_dsi_test`. Expected: 0
  errors, 0 warnings.
* **Task file verificator**:
  `uv run python -u -m arf.scripts.verificators.verify_task_file t0048_voff_nmda1_dsi_test`.
  Expected: 0 errors.
* **Answer asset verificator** (or direct inspection against
  `meta/asset_types/answer/specification.md` v2):
  `uv run python -u -m arf.scripts.verificators.verify_answer_assets t0048_voff_nmda1_dsi_test` (or
  the closest available verificator). Expected: 0 errors for
  `assets/answer/dsi-flatness-test-voltage-independent-nmda/`.
* **Metrics verificator**:
  `uv run python -u -m arf.scripts.verificators.verify_task_metrics t0048_voff_nmda1_dsi_test`.
  Expected: 0 errors; `metrics.json` contains exactly 7 variants `voff1_gnmda_0p0ns` through
  `voff1_gnmda_3p0ns`, each with a single `direction_selectivity_index` value.
* **CSV row count check**:
  `uv run python -u -c "import csv; rows = list(csv.DictReader(open( 'tasks/t0048_voff_nmda1_dsi_test/results/data/gnmda_sweep_trials_voff1.csv'))); print(len(rows))"`.
  Expected output: `56`.
* **PNG existence check**:
  `ls -l tasks/t0048_voff_nmda1_dsi_test/results/images/dsi_vs_gnmda_voff0_vs_voff1.png tasks/t0048_voff_nmda1_dsi_test/results/images/conductance_comparison_voff0_vs_voff1_at_gnmda_0p5.png`.
  Expected: both files exist with size > 10 KB.
* **Style checks**:
  `uv run ruff check tasks/t0048_voff_nmda1_dsi_test/code/ && uv run ruff format --check tasks/t0048_voff_nmda1_dsi_test/code/ && uv run mypy tasks/t0048_voff_nmda1_dsi_test/code/`.
  Expected: 0 errors from each.
* **Requirement coverage check**: open `tasks/t0048_voff_nmda1_dsi_test/results/results_detailed.md`
  (written by orchestrator) and verify the `## Task Requirement Coverage` section addresses every
  REQ-1 through REQ-16 with an explicit answer. (This criterion is enforced by the orchestrator's
  reporting step but is included here for traceability.)
