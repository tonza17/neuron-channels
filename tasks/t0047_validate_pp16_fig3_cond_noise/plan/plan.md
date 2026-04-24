---
spec_version: "2"
task_id: "t0047_validate_pp16_fig3_cond_noise"
date_completed: "2026-04-24"
status: "complete"
---
# Plan: Validate Poleg-Polsky 2016 Fig 3A-F Conductances and Extend Noise Sweep

## Objective

Wrap the existing `modeldb_189347_dsgc_exact` library produced by t0046 with a thin Python recording
layer that captures per-synapse NMDA, AMPA, and GABA conductance and current traces (PD vs ND) for a
gNMDA sweep `b2gnmda in {0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0}` nS, reproducing Poleg-Polsky and
Diamond 2016 (Neuron, DOI `10.1016/j.neuron.2016.02.013`) Figure 3A-E (per-synapse conductance
balance) and Figure 3F (PSP traces and DSI-vs-gNMDA flatness). Extend t0046's truncated noise sweep
to `flickerVAR in {0.0, 0.1, 0.3, 0.5}` for `exptype in {control, AP5, 0Mg}` (4 trials per direction
per cell), reproducing Figures 6-7 (DSI vs noise SD; subthreshold ROC AUC vs noise SD). Publish a
single answer asset `polegpolsky-2016-fig3-conductances-validation` containing the per-synapse
conductance comparison table (paper vs ours, +/-25% verdict per channel per direction), the
DSI-vs-gNMDA chart and table (paper claim ~0.3 vs ours), the noise-sweep tables (DSI vs flickerVAR
per condition; AUC vs flickerVAR per condition), the discrepancy catalogue extended from t0046's 12
entries, and a one-paragraph synthesis. Done means: seven reproduction PNGs exist under
`results/images/`; the answer asset validates against `meta/asset_types/answer/specification.md` v2;
`results/metrics.json` uses the explicit multi-variant format with one variant per gNMDA value and
one variant per (condition, noise) cell; the per-figure pass criterion in the Pass Criterion is met
or documented with numerical gap. The task does NOT modify the model — no HOC, MOD, or t0046 code
is changed. The task does NOT re-fork t0046's library; the entire `tasks/t0046_.../code/` subtree is
imported via the project's standard cross-task package path because that subtree is the registered
implementation of `modeldb_189347_dsgc_exact`.

## Task Requirement Checklist

Operative task request quoted verbatim from `task.json` and `task_description.md`:

> Validate Poleg-Polsky 2016 Fig 3A-F conductances and extend noise sweep. Re-run t0046 library to
> record per-synapse NMDA/AMPA/GABA conductances per direction (Fig 3A-E targets) and extend noise
> sweep to flickerVAR in {0.0, 0.1, 0.3, 0.5} for control / AP5 / 0 Mg. Re-use the existing
> modeldb_189347_dsgc_exact library produced by t0046. No code copy or fork. Add a thin Python
> wrapper code/run_with_conductances.py that drives simplerun() and records soma voltage,
> per-synapse-class summed conductance over the trial (NMDA, AMPA, GABA), peak in nS over the trial
> window separately for PD vs ND, per-synapse-class summed current (i = g * (V - E_rev)) peak in nA
> for diagnostic. Run the gNMDA sweep at b2gnmda in {0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0} nS, 4 trials
> per direction per value, recording all of the above. Reproduces Fig 3A-E (per-synapse balance) and
> Fig 3F bottom (DSI vs gNMDA). Reproduce Fig 3F top: simulated PSP traces PD vs ND at gNMDA = 0.0,
> 0.5, 2.5 nS. Extend the noise sweep to flickerVAR in {0.0, 0.1, 0.3, 0.5} for exptype in {control,
> AP5, 0Mg}. AP5 is modelled as b2gnmda = 0 per t0046's convention. 4 trials per direction per
> (condition, noise) cell. Compare every recorded conductance against the paper's Fig 3A-E values:
> NMDAR PD ~7 nS / ND ~5 nS; AMPAR PD ~3.5 nS / ND ~3.5 nS; GABA PD ~12-13 nS / ND ~30 nS. Catalogue
> any conductance-balance discrepancies and the simulated DSI-vs-gNMDA mismatch.

Concrete requirements extracted from the quoted task text and from `task_description.md`:

* **REQ-1** — Re-use the `modeldb_189347_dsgc_exact` library from t0046 unchanged. NO code copy or
  fork; cross-task imports via
  `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.* import ...` for `run_one_trial`,
  `build_dsgc`, `read_synapse_coords`, `assert_bip_positions_baseline`, `ensure_neuron_importable`,
  `DT_MS`, `TSTOP_MS`, `V_INIT_MV`, `E_SACINHIB_MV`, `ExperimentType`, `Direction`. Satisfied by
  Steps 2, 3, 5, 6.
* **REQ-2** — Centralise paths in `code/paths.py` and constants in `code/constants.py` per the
  project Python style guide. Constants must include the gNMDA sweep grid
  `B2GNMDA_GRID_NS = (0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0)`, the noise grid
  `FLICKER_VAR_GRID = (0.0, 0.1, 0.3, 0.5)`, the condition list
  `NOISE_CONDITIONS = (control, AP5, 0Mg)`, recording sub-sample interval `DT_RECORD_MS = 0.25`,
  trial count `TRIALS_PER_CELL = 4`, paper Fig 3 targets `NMDA_PD_TARGET_NS = 7.0`,
  `NMDA_ND_TARGET_NS = 5.0`, `AMPA_PD_TARGET_NS = 3.5`, `AMPA_ND_TARGET_NS = 3.5`,
  `GABA_PD_TARGET_NS = 12.5`, `GABA_ND_TARGET_NS = 30.0`, `CONDUCTANCE_TOLERANCE_FRAC = 0.25`,
  `DSI_PAPER_FIG3F_TARGET = 0.30`, `DSI_FIG3F_TOLERANCE = 0.05`, plus reversal potentials
  `E_BIPNMDA_MV = 0.0`, `E_SACEXC_MV = 0.0`, `E_SACINHIB_MV_OVERRIDE = -60.0` (the `main.hoc`
  override of MOD default `-65`, sourced from t0046's `constants.py`). Satisfied by Steps 3, 4.
* **REQ-3** — Implement `code/run_with_conductances.py` with two public functions:
  `attach_conductance_recorders(*, h: Any, dt_record_ms: float = 0.25) -> ConductanceRecorders` and
  `run_one_trial_with_conductances(*, ...same kwargs as t0046's run_one_trial...) -> TrialResultWithConductances`.
  The wrapper attaches FOUR `Vector.record(syn._ref_*, dt_record_ms)` vectors per synapse:
  `BIPsyn[i]._ref_gAMPA`, `BIPsyn[i]._ref_gNMDA`, `SACexcsyn[i]._ref_g`, `SACinhibsyn[i]._ref_g`, by
  iterating `for idx in range(int(h.RGC.numsyn)): syn = h.RGC.BIPsyn[idx]` etc. Recorders are
  attached ONCE after `_ensure_cell()` returns and re-used across all trials (verified safe in
  research_code.md: `placeBIP()` only re-binds `Vinf` Vectors; synapse POINT_PROCESS objects persist
  for process life). After each trial, the wrapper extracts per-class summed peak conductance (nS)
  and computes per-class summed peak current offline as `i = g * (v - E_rev)` using the soma voltage
  trace from `run_one_trial` (no second `_ref_i` recorder needed; saves ~8.5 MB / trial of NEURON
  memory). Satisfied by Step 5.
* **REQ-4** — Reproduce Figure 3A-E per-synapse conductance balance: for every gNMDA value in
  `B2GNMDA_GRID_NS`, run 4 trials per direction (PD, ND), record per-synapse-class summed peak
  conductance (NMDA, AMPA, GABA) and per-synapse-class summed peak current (nA). Report both
  per-synapse-mean and summed-across-synapses values in the answer asset's table because the paper's
  plotting convention (per-synapse vs summed) is ambiguous from Fig 3 captions. Verdict per
  (channel, direction, gNMDA) is "within +/-25%" or "outside +/-25%" of the paper target. Satisfied
  by Steps 6, 8, 12.
* **REQ-5** — Reproduce Figure 3F top: render PSP traces (mV vs ms) for PD vs ND at gNMDA =
  `{0.0, 0.5, 2.5}` nS as the 6-panel figure `fig3f_top_psp_traces.png`. PSP peak amplitude must be
  within +/-20% of t0046's previously recorded values at the same `b2gnmda` (sanity check that the
  recording wrapper has not changed `simplerun()` semantics). Satisfied by Steps 7, 12.
* **REQ-6** — Reproduce Figure 3F bottom: compute and plot DSI vs gNMDA (PD-vs-ND DSI, copy
  t0046's 8-line `_dsi(*, pd_values, nd_values) -> float | None` helper into `code/dsi.py` as
  `compute_dsi_pd_nd`). Output `fig3f_bottom_dsi_vs_gnmda.png` and the DSI table. Pass criterion:
  every gNMDA value's DSI within +/-0.05 of 0.30, i.e. DSI in `[0.25, 0.35]`. If the criterion
  fails, the divergence is catalogued explicitly (consistent with t0046's preliminary finding that
  DSI vs gNMDA is non-flat: 0.124 -> 0.204 -> 0.049 -> 0.026 across gNMDA = 0.0 / 0.5 / 1.5 / 2.5
  nS). Satisfied by Steps 6, 8, 12.
* **REQ-7** — Extend the noise sweep: for each `(condition, flickerVAR)` cell with
  `condition in {control, AP5, 0Mg}` and `flickerVAR in {0.0, 0.1, 0.3, 0.5}`, run 4 trials per
  direction (PD, ND) and record peak PSP, baseline mean, and per-synapse-class peak conductance. AP5
  is modelled as `b2gnmda_override = 0.0` (t0046's convention; documented in t0046's
  `compute_metrics.py`). Control and 0Mg use t0046's existing `ExperimentType` enum (`exptype = 1`
  and `exptype = 2`). The `flicker_var` argument is forwarded to `run_one_trial(flicker_var=...)`
  which already exposes it. Satisfied by Steps 9, 12.
* **REQ-8** — Reproduce Figures 6-7: compute per-condition DSI vs flickerVAR (Fig 6) and one-sided
  ROC AUC of PD-trial peaks vs trial baselines (Fig 7), per condition per noise level. Copy t0046's
  ~20-line `_roc_auc_pd_vs_baseline(*, pd_values, baselines)` helper into `code/scoring.py` as
  `compute_roc_auc_pd_vs_baseline`. Output `fig6_dsi_vs_noise_per_condition.png` and
  `fig7_auc_vs_noise_per_condition.png`. Qualitative pass criterion: DSI declines monotonically and
  AUC declines monotonically as noise increases, per condition. Satisfied by Steps 9, 12.
* **REQ-9** — Render the seven required reproduction PNGs to `results/images/`:
  `fig3a_nmda_conductance_pd_vs_nd.png`, `fig3b_ampa_conductance_pd_vs_nd.png`,
  `fig3c_gaba_conductance_pd_vs_nd.png`, `fig3f_top_psp_traces.png`,
  `fig3f_bottom_dsi_vs_gnmda.png`, `fig6_dsi_vs_noise_per_condition.png`,
  `fig7_auc_vs_noise_per_condition.png`. Use raw matplotlib (the t0011 `tuning_curve_viz` API is for
  12-angle curves only); import the Okabe-Ito `MODEL_COLORS` palette from
  `tasks.t0011_response_visualization_library.code.tuning_curve_viz.constants` for visual
  consistency. Satisfied by Step 12.
* **REQ-10** — Produce the answer asset
  `tasks/t0047_validate_pp16_fig3_cond_noise/assets/answer/polegpolsky-2016-fig3-conductances-validation/`
  per `meta/asset_types/answer/specification.md` v2: `details.json`, `short_answer.md`,
  `full_answer.md`. The `details.json` must declare `spec_version: "2"`, `short_answer_path`,
  `full_answer_path`, the question framing string, source-list (cite t0046's library asset, the
  Poleg-Polsky 2016 paper asset `10.1016_j.neuron.2016.02.013`, and t0046's audit answer asset
  `poleg-polsky-2016-reproduction-audit`). The `full_answer.md` must contain: question framing,
  per-synapse conductance table (NMDA / AMPA / GABA, PD vs ND, paper target vs ours, verdict),
  PSP-trace overlay table (Fig 3F top, gNMDA = 0.0, 0.5, 2.5 nS), DSI-vs-gNMDA table and chart, two
  noise-sweep tables (DSI and AUC vs flickerVAR per condition), updated discrepancy catalogue
  building on t0046's 12 entries with new rows for any per-synapse mismatch outside +/-25%, and a
  one-paragraph synthesis. Satisfied by Step 13.
* **REQ-11** — Catalogue conductance-balance discrepancies and the DSI-vs-gNMDA mismatch
  numerically; carry forward t0046's 12 catalogue rows verbatim and append new rows. Reference
  t0046's audit row 35 (`Voff_bipNMDA = 0` in the deposited control) as the candidate root cause if
  the per-synapse balance matches but DSI-vs-gNMDA still mismatches. Satisfied by Step 13.
* **REQ-12** — Local CPU only; no Vast.ai; no remote machines. Total trial budget approximately
  152: `7 gNMDA values * 2 directions * 4 trials = 56` for the gNMDA sweep plus
  `3 conditions * 4 noise levels * 2 directions * 4 trials = 96` for the noise extension. Satisfied
  by Steps 6, 9 and the Time Estimation section.
* **REQ-13** — Use absolute imports; wrap every CLI call in
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0047_validate_pp16_fig3_cond_noise -- <command>`
  per the project Python style guide. Satisfied by every Step that invokes a script.
* **REQ-14** — Write `results/metrics.json` in the explicit multi-variant format with one variant
  per gNMDA value (named e.g. `gnmda_0p5ns`) and one variant per (condition, noise) cell (named e.g.
  `control_flickerVAR_0p3`). Each variant records `direction_selectivity_index` (registered metric
  `direction_selectivity_index`). Per `arf/specifications/metrics_specification.md` v4. Satisfied by
  Step 11.

## Approach

The implementation re-uses t0046's `modeldb_189347_dsgc_exact` library exactly, importing the cell
builder, the trial driver, the synapse-coords reader, and the BIP-position guard via the project's
standard cross-task package path (allowed because the entire `tasks/t0046_.../code/` subtree is the
registered implementation of the library). On top of that, a thin recording wrapper
`code/run_with_conductances.py` attaches NEURON `Vector.record(syn._ref_*, dt_record_ms)` handles to
every synapse's conductance state variable once per process (after `_ensure_cell()` returns), then
delegates each trial to the unmodified `run_one_trial(...)` and reads the recorder vectors after
each `simplerun()` returns.

Per the research findings (`research/research_code.md`):

* **Synapse list pattern** — t0046's `RGCmodel.hoc` declares HOC objref arrays `BIPsyn[numsyn]`,
  `SACexcsyn[numsyn]`, `SACinhibsyn[numsyn]` (each of size `numsyn = 282` per the deposited code).
  Iterate from Python via `for idx in range(int(h.RGC.numsyn)): syn = h.RGC.BIPsyn[idx]` — the
  same pattern t0046's `read_synapse_coords` uses.
* **MOD `_ref_*` handles** — `bipNMDA.mod` declares both `_ref_gAMPA` and `_ref_gNMDA` separately
  (the BREAKPOINT computes `g = gNMDA + gAMPA`), so the dual-component bipolar synapse can be split
  into Fig 3A (NMDA) and Fig 3B (AMPA). `SACexc.mod` and `SACinhib.mod` each declare only `_ref_g`.
* **Sub-sample dt** — `Vector.record(ref, dt_ms)` with an explicit second argument records at a
  linear-interpolated grid. At `tstop = 1000 ms` and `dt = 0.1 ms`, recording every dt gives 10001
  samples per vector. With ~282 synapses x 4 channels = ~1128 vectors per trial, recording at the
  simulation dt would be ~81 MB / trial. Sub-sampling at `dt_record_ms = 0.25` (2.5x sub-sample;
  conservative for AMPA's 2 ms tau) reduces to ~32 MB / trial — safe for peak detection.
* **Reversal potentials for offline current** — `bipNMDA.e = 0` (shared by AMPA and NMDA),
  `SACexc.e = 0`, `SACinhib.e = -60` (the `main.hoc` override of MOD default `-65`, recorded in
  t0046's `constants.E_SACINHIB_MV`). Current is computed offline as
  `i_nA = (1e-3) * g_nS * (v_mV - e_mV)` — replicates each MOD's BREAKPOINT formula and saves the
  per-synapse `_ref_i` recorder vectors (~8.5 MB / trial saved).
* **DSI helper** — t0046's 8-line `_dsi(*, pd_values, nd_values) -> float | None` is copied into
  `code/dsi.py` as `compute_dsi_pd_nd`. The t0012 `compute_dsi` library function requires a 12-angle
  TuningCurve; constructing one from a 2-row PD/ND pair just to call the library is brittle (the
  library validates `len(angles_deg) == 12`).
* **ROC AUC helper** — t0046's ~20-line `_roc_auc_pd_vs_baseline(*, pd_values, baselines)` is
  copied into `code/scoring.py` as `compute_roc_auc_pd_vs_baseline` (private function, not exposed
  via any registered library).
* **Plot palette** — `MODEL_COLORS` (Okabe-Ito) is imported from
  `tasks.t0011_response_visualization_library.code.tuning_curve_viz.constants`. The four entry
  points in t0011's `tuning_curve_viz` package (`plot_cartesian_tuning_curve`, etc.) all assume a
  12-angle tuning curve and cannot directly draw Fig 3A-E (PD vs ND bars) or Fig 3F top (PSP vs
  time) — raw matplotlib is required for those.

**Alternatives considered**:

* *Add `_ref_i` recorders directly* (as a second `Vector.record(syn._ref_i)` per synapse). Rejected:
  doubles per-trial memory (~64 MB instead of ~32 MB) for no benefit because each MOD's BREAKPOINT
  computes `i = (1e-3) * g * (v - e)` and we already record `g(t)` and `v(t)`; multiplying offline
  is exact.
* *Modify t0046's `run_simplerun.py` in place* to attach the conductance recorders. Rejected: the
  cross-task code-reuse rule is "import via library" for registered libraries; modifying t0046's
  files would break the rule and t0046's task immutability. Wrapping is the cleaner pattern.
* *Run only the gNMDA sweep this task and defer the noise extension* to a separate task. Rejected:
  the task description groups them together because they share the same recording infrastructure and
  the same answer asset; splitting would duplicate ~80% of the wrapper code in another task.
* *Use t0012's `compute_dsi` and construct a 12-angle TuningCurve from PD + ND* (filling unobserved
  angles with NaN). Rejected: t0012's `_validate_angle_grid` rejects any input with
  `len(angles_deg) != 12`; the 8-line copy is faster, simpler, and matches t0046's convention.
* *Write `metrics.json` in legacy flat format* with one DSI-per-condition. Rejected: the task
  reports two-axis sweeps (gNMDA value × direction; condition × noise level × direction). Per the
  experiment-run task type's planning guidelines, multi-condition tasks must use the explicit
  variant format.

**Task type**: `experiment-run` (already declared in `task.json`). Per
`meta/task_types/experiment-run/instruction.md`: define the hypothesis (does the deposited control
reproduce Fig 3A-F per-synapse balance and Fig 3F flatness?), specify independent variables (gNMDA
value, condition, noise level, direction) and dependent variables (per-synapse peak conductance,
DSI, ROC AUC), use multi-variant `metrics.json`, render >= 2 charts (we render 7), reference at
least one prior published baseline (paper Fig 3A-E targets and t0046's audit conclusions), set and
log random seeds (we re-use t0046's `trial_seed` parameter exposed by `run_one_trial`).

The pre-mortem failure modes are listed in Risks & Fallbacks.

## Cost Estimation

Total cost: **$0.00 USD**. Project budget remaining is $1.00 (per `project/budget.json`); this task
spends $0 because:

* **API calls**: $0. No LLM calls; all analysis is local Python.
* **Remote compute**: $0. Local CPU only; no Vast.ai or other paid compute. The full ~152-trial
  sweep runs on a developer laptop in ~13 minutes wall-clock.
* **Storage / network**: $0. All inputs are cached locally from t0046; outputs are < 100 MB total
  (CSVs + 7 PNGs).
* **No paid services declared in `project/budget.json` `available_services`** (the field is `[]`).

## Step by Step

The Step by Step covers ONLY the implementation work — driver scaffolding through chart rendering
and the answer asset. Downstream artifacts beyond chart rendering and the answer asset are
orchestrator-managed steps in execute-task and are NOT included here.

### Milestone A — Scaffolding and constants (Steps 1-4)

Independently verifiable: scaffolding files exist, constants are imported by a smoke test.

1. **Verify dependency state.** Run
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0047_validate_pp16_fig3_cond_noise -- python -u -m arf.scripts.aggregators.aggregate_tasks --format ids --ids t0007_install_neuron_netpyne t0011_response_visualization_library t0012_tuning_curve_scoring_loss_library t0046_reproduce_poleg_polsky_2016_exact`.
   Expected output: all four task IDs listed (each is `completed` per the dependency-validation
   step). Confirm `tasks/t0046_.../code/sources/nrnmech.dll` exists (this is the compiled MOD
   library that `build_dsgc()` will load transparently); if it is absent, halt and create an
   intervention file (the task cannot proceed without t0046's compiled DLL). Satisfies REQ-1,
   REQ-12.

2. **Initialise the task `code/` package.** Create
   `tasks/t0047_validate_pp16_fig3_cond_noise/code/__init__.py` (empty file). This makes `code` a
   proper Python package importable as `tasks.t0047_validate_pp16_fig3_cond_noise.code.<module>`.
   Satisfies REQ-13.

3. **Centralise paths.** Create `tasks/t0047_validate_pp16_fig3_cond_noise/code/paths.py` defining:
   `TASK_ROOT: Path` (the task folder), `RESULTS_DIR: Path`, `RESULTS_DATA_DIR: Path`
   (`results/data/`), `RESULTS_IMAGES_DIR: Path` (`results/images/`), `ASSETS_ANSWER_DIR: Path`
   (`assets/answer/polegpolsky-2016-fig3-conductances-validation/`), `LOGS_DIR: Path`, plus per-CSV
   file constants `GNMDA_TRIALS_CSV: Path` (`results/data/gnmda_sweep_trials.csv`),
   `NOISE_TRIALS_CSV: Path` (`results/data/noise_extension_trials.csv`), `PSP_TRACES_CSV: Path`
   (`results/data/psp_traces_fig3f_top.csv`), `CONDUCTANCE_TABLE_CSV: Path`
   (`results/data/conductance_comparison_table.csv`). Use `pathlib.Path` and
   `Path(__file__).resolve().parent.parent` to anchor `TASK_ROOT`. Satisfies REQ-2.

4. **Centralise constants.** Create `tasks/t0047_validate_pp16_fig3_cond_noise/code/constants.py`
   with:
   * `B2GNMDA_GRID_NS: tuple[float, ...] = (0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0)`
   * `FLICKER_VAR_GRID: tuple[float, ...] = (0.0, 0.1, 0.3, 0.5)`
   * `TRIALS_PER_CELL: int = 4`
   * `DT_RECORD_MS: float = 0.25`
   * `E_BIPNMDA_MV: float = 0.0`
   * `E_SACEXC_MV: float = 0.0`
   * `E_SACINHIB_MV_OVERRIDE: float = -60.0` (re-affirms the value imported from
     `tasks.t0046_reproduce_poleg_polsky_2016_exact.code.constants.E_SACINHIB_MV`; do an `assert` at
     module load to confirm the two values agree)
   * Paper Fig 3 targets: `NMDA_PD_TARGET_NS = 7.0`, `NMDA_ND_TARGET_NS = 5.0`,
     `AMPA_PD_TARGET_NS = 3.5`, `AMPA_ND_TARGET_NS = 3.5`, `GABA_PD_TARGET_NS = 12.5`,
     `GABA_ND_TARGET_NS = 30.0`
   * Pass-criterion thresholds: `CONDUCTANCE_TOLERANCE_FRAC: float = 0.25`,
     `DSI_PAPER_FIG3F_TARGET: float = 0.30`, `DSI_FIG3F_TOLERANCE: float = 0.05`,
     `PSP_PEAK_TOLERANCE_FRAC: float = 0.20`
   * `PSP_TRACE_GNMDA_VALUES_NS: tuple[float, ...] = (0.0, 0.5, 2.5)` (Fig 3F top sub-grid)
   * Enums for noise conditions:
     `class NoiseCondition(Enum): CONTROL = "control"; AP5 = "AP5"; ZERO_MG = "0Mg"`
   * Per `arf/styleguide/python_styleguide.md`, every constant has an explicit type annotation.
     Satisfies REQ-2.

### Milestone B — Recording wrapper (Step 5)

Independently verifiable: smoke test (`run_one_trial_with_conductances` for one trial) prints
non-zero per-class peak g values.

5. **Implement the recording wrapper.** Create
   `tasks/t0047_validate_pp16_fig3_cond_noise/code/run_with_conductances.py`. Imports:
   ```python
   from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.neuron_bootstrap import (
       ensure_neuron_importable,
   )
   from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.build_cell import (
       build_dsgc,
       read_synapse_coords,
       assert_bip_positions_baseline,
   )
   from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun import (
       run_one_trial,
       TrialResult,
   )
   from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.constants import (
       DT_MS, TSTOP_MS, V_INIT_MV, E_SACINHIB_MV, ExperimentType, Direction,
   )
   from tasks.t0047_validate_pp16_fig3_cond_noise.code.constants import (
       DT_RECORD_MS, E_BIPNMDA_MV, E_SACEXC_MV, E_SACINHIB_MV_OVERRIDE,
   )
   ```
   Define two frozen-slots dataclasses:
   ```python
   @dataclass(frozen=True, slots=True)
   class ConductanceRecorders:
       g_ampa: list[Any]      # one Vector per synapse, BIPsyn[i]._ref_gAMPA
       g_nmda: list[Any]      # one Vector per synapse, BIPsyn[i]._ref_gNMDA
       g_sacexc: list[Any]    # one Vector per synapse, SACexcsyn[i]._ref_g
       g_sacinhib: list[Any]  # one Vector per synapse, SACinhibsyn[i]._ref_g
       t_rec: Any             # one Vector recording h._ref_t at dt_record_ms
       num_synapses: int

   @dataclass(frozen=True, slots=True)
   class TrialResultWithConductances:
       trial: TrialResult
       peak_g_nmda_summed_ns: float
       peak_g_ampa_summed_ns: float
       peak_g_sacexc_summed_ns: float
       peak_g_sacinhib_summed_ns: float
       peak_g_nmda_per_syn_mean_ns: float
       peak_g_ampa_per_syn_mean_ns: float
       peak_g_sacexc_per_syn_mean_ns: float
       peak_g_sacinhib_per_syn_mean_ns: float
       peak_i_nmda_summed_na: float
       peak_i_ampa_summed_na: float
       peak_i_sacexc_summed_na: float
       peak_i_sacinhib_summed_na: float
   ```
   Public functions:
   ```python
   def attach_conductance_recorders(
       *,
       h: Any,
       dt_record_ms: float = DT_RECORD_MS,
   ) -> ConductanceRecorders: ...

   def run_one_trial_with_conductances(
       *,
       recorders: ConductanceRecorders,
       exptype: ExperimentType,
       direction: Direction,
       trial_seed: int,
       flicker_var: float = 0.0,
       stim_noise_var: float = 0.0,
       b2gnmda_override: float | None = None,
       record_spikes: bool = False,
   ) -> TrialResultWithConductances: ...
   ```
   `attach_conductance_recorders` iterates `for idx in range(int(h.RGC.numsyn)):` and for each `idx`
   calls `vec = h.Vector(); vec.record(h.RGC.BIPsyn[idx]._ref_gAMPA, dt_record_ms)` etc., appending
   each `vec` to the corresponding `g_*` list in the dataclass. Also records `h._ref_t` at
   `dt_record_ms`. Returns a populated `ConductanceRecorders`. After every trial, the wrapper
   computes per-class **per-time-step** sum across all `numsyn` synapses, then peak across the trial
   window: `peak_g_class_summed_ns = max_t (sum_i g_class[i](t))`. Per-synapse-mean peak is
   `peak_g_class_summed_ns / numsyn`. For peak current, use the soma voltage trace from
   `TrialResult` (`run_one_trial` already records `v_rec` and `t_rec` at the simulation dt; we
   resample to the recording dt by linear interpolation, or sub-sample by index if `dt_record_ms`
   divides `DT_MS` evenly — at `0.25 / 0.1 = 2.5` it does NOT, so use `numpy.interp`). The peak
   current per class uses `e = E_BIPNMDA_MV` for AMPA and NMDA, `e = E_SACEXC_MV` for SACexc,
   `e = E_SACINHIB_MV_OVERRIDE` for SACinhib. The unit conversion is
   `i_nA = (1e-3) * g_nS_summed * (v_mV - e_mV)` per the MOD BREAKPOINT formula. After computing
   peaks, **reset all recorder vectors** (`vec.resize(0)`) so the next trial starts clean — peak
   memory stays bounded at one trial's worth.

   Smoke-test gate (validation gate before any sweep): include a `__main__` that runs ONE trial
   (`exptype=CONTROL, direction=PD, trial_seed=1`) and prints all twelve peak fields to stdout.
   Verify that `peak_g_nmda_summed_ns > 0`, `peak_g_ampa_summed_ns > 0`, and
   `peak_g_sacinhib_summed_ns > 0` (zero would indicate the `_ref_*` handle was not attached).
   **Failure condition**: if any of the three is zero, halt and inspect the relevant MOD file's
   RANGE block — do NOT proceed to the full sweep until non-zero peaks are confirmed for all four
   classes. Read the printed `peak_g_nmda_summed_ns` value and confirm it is in the order of ~282
   synapses * ~5 nS = ~1400 nS (any value < 100 nS or > 10000 nS suggests a unit error). Satisfies
   REQ-3.

### Milestone C — Drivers (Steps 6-9)

Independently verifiable: per-trial CSVs exist with the expected number of rows.

6. **Implement the gNMDA sweep driver.** Create
   `tasks/t0047_validate_pp16_fig3_cond_noise/code/run_fig3_validation.py`. Imports
   `attach_conductance_recorders`, `run_one_trial_with_conductances`, `TrialResultWithConductances`,
   the t0046 `build_dsgc`, `ensure_neuron_importable`, `ExperimentType`, `Direction`, and the local
   `B2GNMDA_GRID_NS`, `TRIALS_PER_CELL`, `GNMDA_TRIALS_CSV`. Steps in the script:
   1. `ensure_neuron_importable()` (idempotent re-exec sentinel).
   2. `import neuron; h = neuron.h; build_dsgc(); _ = read_synapse_coords(h=h)` (the read locks in
      the BIP-position baseline that subsequent `assert_bip_positions_baseline` calls compare
      against; this exact sequence is the one t0046 uses in `run_simplerun._ensure_cell`).
   3. `recorders = attach_conductance_recorders(h=h)`.
   4. For each `b2gnmda in B2GNMDA_GRID_NS`, for each `direction in (Direction.PD, Direction.ND)`,
      for `trial in range(TRIALS_PER_CELL)`:
      * Compute deterministic seed: `trial_seed = 1000 * <gnmda_index> + 100 * <dir_index> + trial`.
      * Call
        `result = run_one_trial_with_conductances(recorders=recorders, exptype=ExperimentType.CONTROL, direction=direction, trial_seed=trial_seed, b2gnmda_override=b2gnmda)`.
      * Write one row to `GNMDA_TRIALS_CSV` with columns: `b2gnmda_ns`, `direction`, `trial_seed`,
        `peak_psp_mv`, `baseline_mean_mv`, `peak_g_nmda_summed_ns`, `peak_g_ampa_summed_ns`,
        `peak_g_sacexc_summed_ns`, `peak_g_sacinhib_summed_ns`, `peak_g_nmda_per_syn_mean_ns`,
        `peak_g_ampa_per_syn_mean_ns`, `peak_g_sacexc_per_syn_mean_ns`,
        `peak_g_sacinhib_per_syn_mean_ns`, `peak_i_nmda_summed_na`, `peak_i_ampa_summed_na`,
        `peak_i_sacexc_summed_na`, `peak_i_sacinhib_summed_na`.
   5. Use `tqdm` for progress (56 trials). Run via
      `uv run python -m arf.scripts.utils.run_with_logs --task-id t0047_validate_pp16_fig3_cond_noise -- python -u -m tasks.t0047_validate_pp16_fig3_cond_noise.code.run_fig3_validation`.
      Validation gate: before launching the full 56-trial sweep, run with `--limit 4` (4 trials at
      the first gNMDA value, PD only) and verify all 4 rows appear in `GNMDA_TRIALS_CSV` with
      non-NaN per-synapse conductance peaks. Failure condition: if any `peak_g_*_summed_ns` is NaN
      or zero across all 4 trials, halt and re-inspect the wrapper smoke test from Step 5. Read all
      4 rows of the limited CSV and confirm individual values look plausible. Expected observable
      output: progress bar shows 56/56 trials; CSV has 56 rows. Confirm
      `assert_bip_positions_baseline(h=h, baseline=...)` is called inside `run_one_trial` after
      every trial (this is t0046's existing guard; we do not need to call it explicitly, but should
      observe no AssertionError in the log). Satisfies REQ-4, REQ-6, REQ-12, REQ-13.

7. **Add the PSP-trace recorder for Fig 3F top.** Extend `code/run_fig3_validation.py` with a second
   pass that re-runs the same trials at `b2gnmda in PSP_TRACE_GNMDA_VALUES_NS = (0.0, 0.5, 2.5)` and
   saves the full soma voltage trace (`v_rec`, `t_rec`) for one canonical trial per (gnmda,
   direction). Output: `PSP_TRACES_CSV` with columns `b2gnmda_ns`, `direction`, `t_ms`, `v_mv` (long
   format). The `run_one_trial` function already records `v_rec` and `t_rec` at the simulation dt;
   expose them via a small modification: instead of modifying `run_one_trial`, extend
   `run_one_trial_with_conductances` to optionally return the raw `v_rec` and `t_rec` lists (add an
   optional `return_traces: bool = False` kwarg; when True, the dataclass also returns
   `v_trace_mv: list[float] | None` and `t_trace_ms: list[float] | None` fields — note in
   `TrialResultWithConductances` these fields are `None` by default to keep the default-path memory
   low). Satisfies REQ-5.

8. **Compute the per-gNMDA aggregated table.** Create
   `tasks/t0047_validate_pp16_fig3_cond_noise/code/compute_metrics.py`. Inputs: `GNMDA_TRIALS_CSV`.
   Outputs: `CONDUCTANCE_TABLE_CSV` (one row per `(channel, direction, b2gnmda)` cell with
   `mean_summed_ns`, `std_summed_ns`, `paper_target_ns`, `verdict_within_25pct`) and a Python dict
   `dsi_by_gnmda: dict[float, float]` written to `results/data/dsi_by_gnmda.json`. Use the helpers
   from `code/dsi.py` (next step). Sub-step:
   * Copy t0046's `_dsi(*, pd_values, nd_values) -> float | None` and the 7-line
     `_mean(*, values) -> float | None` helpers from
     `tasks/t0046_reproduce_poleg_polsky_2016_exact/code/compute_metrics.py:117-124` and lines
     100-105 into `tasks/t0047_validate_pp16_fig3_cond_noise/code/dsi.py` as `compute_dsi_pd_nd` and
     `_mean`. Add a leading comment citing the source path and line numbers per
     `arf/styleguide/python_styleguide.md`. Total ~15 lines copied. For each `b2gnmda`, compute
     `dsi_by_gnmda[b2gnmda] = compute_dsi_pd_nd(pd_values=peak_psp_pd, nd_values=peak_psp_nd)`.
     Verdict per (channel, direction, gnmda) is
     `abs(observed_summed_ns - paper_target_ns) / paper_target_ns <= CONDUCTANCE_TOLERANCE_FRAC`.
     Run via the `run_with_logs` wrapper. Satisfies REQ-4, REQ-6.

9. **Implement the noise-extension driver.** Create
   `tasks/t0047_validate_pp16_fig3_cond_noise/code/run_noise_extension.py`. Same skeleton as Step 6,
   but the outer loop is over `(condition, flicker_var)` cells with
   `condition in {NoiseCondition.CONTROL, NoiseCondition.AP5, NoiseCondition.ZERO_MG}` and
   `flicker_var in FLICKER_VAR_GRID`. The exptype mapping is:
   * `CONTROL` -> `ExperimentType.CONTROL` (= 1), no `b2gnmda_override`.
   * `AP5` -> `ExperimentType.CONTROL` with `b2gnmda_override = 0.0` (per t0046's convention; AP5 is
     modelled by zeroing NMDA conductance, not by changing exptype).
   * `ZERO_MG` -> `ExperimentType.ZERO_MG` (= 2; the `Voff_bipNMDA = 1` setting in t0046's
     `simplerun()`), no `b2gnmda_override`. Per (condition, flicker_var), run 4 trials per
     direction. The recorder vectors are still attached but for Fig 6/7 we only need PSP peak and
     baseline (we still write the per-class peak conductances to the CSV for diagnostic
     completeness). Output: `NOISE_TRIALS_CSV` with columns `condition`, `flicker_var`, `direction`,
     `trial_seed`, `peak_psp_mv`, `baseline_mean_mv`, plus the four `peak_g_*_summed_ns` columns.
     Trial-seed formula:
     `trial_seed = 10000 + 1000 * <condition_index> + 100 * <noise_index> + 10 * <dir_index> + trial`.
     Validation gate: before the full 96-trial sweep, run with `--limit 4` (4 trials at
     `(CONTROL, flicker_var=0.0, PD)`) and verify `peak_psp_mv` is in the range t0046 observed for
     control / no-noise / PD (~20-30 mV at b2gnmda = 0.5; t0046's prior reproduction of this cell
     measured 23.25 mV PD PSP). Failure condition: if `peak_psp_mv < 5 mV` or `> 50 mV`, halt and
     inspect — the recording wrapper or the `flicker_var` plumbing may be broken. Read all 4 rows
     and confirm individual values are plausible. Satisfies REQ-7, REQ-12.

### Milestone D — Per-cell metrics (Step 10) and metrics.json (Step 11)

Independently verifiable: `metrics.json` exists and validates against the registered metrics.

10. **Compute per-(condition, noise) DSI and ROC AUC.** Extend `code/compute_metrics.py` (or add
    `code/scoring.py`) to consume `NOISE_TRIALS_CSV` and produce
    `dsi_by_condition_noise: dict[str, dict[float, float]]` and
    `auc_by_condition_noise: dict[str, dict[float, float]]`. Sub-step:
    * Copy t0046's `_roc_auc_pd_vs_baseline(*, pd_values, baselines) -> float | None` from
      `tasks/t0046_reproduce_poleg_polsky_2016_exact/code/compute_metrics.py:142-160` into
      `tasks/t0047_validate_pp16_fig3_cond_noise/code/scoring.py` as
      `compute_roc_auc_pd_vs_baseline`. Add the source citation comment. ~20 lines copied. DSI per
      cell: `compute_dsi_pd_nd(pd_values=psp_pd, nd_values=psp_nd)` using the cell's 4 PD and 4 ND
      `peak_psp_mv` values. AUC per cell:
      `compute_roc_auc_pd_vs_baseline(pd_values=psp_pd, baselines=baseline_mean_mv_all_8_trials_in_cell)`.
      Write both dicts to `results/data/dsi_auc_by_condition_noise.json`. Satisfies REQ-7, REQ-8.

11. **Write `results/metrics.json`** in the explicit multi-variant format per
    `arf/specifications/metrics_specification.md` v4. Variants:
    * Seven gNMDA-sweep variants named `gnmda_0p0ns`, `gnmda_0p5ns`, ..., `gnmda_3p0ns`. Each
      records `direction_selectivity_index` (registered metric, unit `ratio`) computed from PSP DSI
      at that gNMDA value.
    * Twelve noise-cell variants named `control_flickerVAR_0p0`, `control_flickerVAR_0p1`, ...,
      `0Mg_flickerVAR_0p5`. Each records `direction_selectivity_index` (PSP DSI at that condition ×
      noise cell). Note: the registered metric set in `meta/metrics/` does not include a "ROC AUC"
      metric, so AUC values are written to `results/data/dsi_auc_by_condition_noise.json` as
      task-specific operational data, NOT to `metrics.json` (per
      `arf/specifications/metrics_specification.md` v4 distinction between registered metrics and
      task-specific results data). The other three registered metrics (`tuning_curve_hwhm_deg`,
      `tuning_curve_reliability`, `tuning_curve_rmse`) are NOT applicable: this task records only PD
      and ND (2 directions), not a 12-angle tuning curve, so HWHM, reliability, and RMSE cannot be
      computed; this omission is deliberate and is noted explicitly in the metrics file's
      `description` field. Satisfies REQ-7, REQ-14.

### Milestone E — Charts and answer asset (Steps 12-13)

Independently verifiable: seven PNGs exist in `results/images/`; answer asset folder exists with the
three required files.

12. **Render the seven reproduction PNGs.** Create
    `tasks/t0047_validate_pp16_fig3_cond_noise/code/render_figures.py`. Imports include
    `from tasks.t0011_response_visualization_library.code.tuning_curve_viz.constants import MODEL_COLORS`.
    Use `matplotlib.use("Agg")` for headless rendering. Read CSVs from `RESULTS_DATA_DIR` and write
    PNGs to `RESULTS_IMAGES_DIR` (created with `mkdir(parents=True, exist_ok=True)`). Required
    outputs:
    * `fig3a_nmda_conductance_pd_vs_nd.png` — grouped bar chart (x = gNMDA value, two bars per
      cell PD vs ND) of `peak_g_nmda_summed_ns` mean across trials, with error bars (std). Overlay
      paper targets (NMDA PD ~7 nS, ND ~5 nS) as horizontal dashed lines.
    * `fig3b_ampa_conductance_pd_vs_nd.png` — same chart for `peak_g_ampa_summed_ns`. Paper
      targets: PD ~3.5, ND ~3.5.
    * `fig3c_gaba_conductance_pd_vs_nd.png` — same chart for `peak_g_sacinhib_summed_ns`. Paper
      targets: PD ~12.5, ND ~30.
    * `fig3f_top_psp_traces.png` — 3-row × 2-column subplots (rows = b2gnmda values 0.0/0.5/2.5,
      columns = direction PD/ND); each subplot shows mV vs ms PSP traces (one canonical trial).
    * `fig3f_bottom_dsi_vs_gnmda.png` — line plot of DSI vs `b2gnmda_ns` (x-axis 0-3 nS),
      horizontal dashed line at `DSI_PAPER_FIG3F_TARGET = 0.30`, shaded band
      `[0.30 - DSI_FIG3F_TOLERANCE, 0.30 + DSI_FIG3F_TOLERANCE]`. Overlay t0046's previously
      observed values (0.124, 0.204, 0.049, 0.026) at gNMDA = (0.0, 0.5, 1.5, 2.5) as a comparison
      series.
    * `fig6_dsi_vs_noise_per_condition.png` — three lines (control / AP5 / 0Mg), x = flickerVAR
      (0.0, 0.1, 0.3, 0.5), y = DSI.
    * `fig7_auc_vs_noise_per_condition.png` — three lines (control / AP5 / 0Mg), x = flickerVAR
      (0.0, 0.1, 0.3, 0.5), y = ROC AUC. Each PNG must have axis labels with units, legend, and a
      title that names the figure (e.g. "Fig 3A: NMDA peak conductance, PD vs ND"). Use the
      `MODEL_COLORS` palette for series colours. Run via the `run_with_logs` wrapper. Expected
      observable output: 7 PNG files exist under `results/images/`, each non-empty (>= 10 KB).
      Satisfies REQ-5, REQ-6, REQ-8, REQ-9.

13. **Produce the answer asset.** Create
    `tasks/t0047_validate_pp16_fig3_cond_noise/assets/answer/polegpolsky-2016-fig3-conductances-validation/`
    with three files per `meta/asset_types/answer/specification.md` v2:
    * `details.json` — `spec_version: "2"`,
      `answer_id: "polegpolsky-2016-fig3-conductances-validation"`,
      `question: "Does the deposited ModelDB 189347 code reproduce Poleg-Polsky 2016's Fig 3A-F per-synapse conductance balance and DSI-vs-gNMDA flatness, and does the extended noise sweep match the paper's qualitative shape?"`,
      `short_answer_path: "short_answer.md"`, `full_answer_path: "full_answer.md"`,
      `produced_by_task: "t0047_validate_pp16_fig3_cond_noise"`, `date_produced: "2026-04-24"`,
      `sources: [...]` with three entries citing t0046's library asset, the Poleg-Polsky 2016 paper
      asset (DOI slug `10.1016_j.neuron.2016.02.013`), and t0046's audit answer asset
      `poleg-polsky-2016-reproduction-audit`.
    * `short_answer.md` — 2-3 paragraphs summarising the headline finding (within or outside the
      +/-25% conductance band; DSI flatness verdict; noise-sweep monotonicity verdict).
    * `full_answer.md` — Per the task description's Deliverables section, must contain (in this
      order): question framing; per-synapse conductance comparison table (NMDA / AMPA / GABA, PD vs
      ND, paper target nS, our observed nS, +/- diff %, verdict); PSP-trace overlay table (Fig 3F
      top, gNMDA = 0.0 / 0.5 / 2.5 nS, embed `fig3f_top_psp_traces.png`); DSI-vs-gNMDA table and
      chart (embed `fig3f_bottom_dsi_vs_gnmda.png`); two noise-sweep tables (DSI vs flickerVAR per
      condition; AUC vs flickerVAR per condition; embed `fig6_dsi_vs_noise_per_condition.png` and
      `fig7_auc_vs_noise_per_condition.png`); updated discrepancy catalogue (the 12 entries from
      t0046's published 12-entry discrepancy catalogue copied verbatim with attribution to t0046's
      audit answer asset, plus any new entries from per-synapse mismatch); one-paragraph synthesis
      tying the conductance-balance verdict to the DSI-vs-gNMDA outcome and naming the first-target
      modification for the next task. Validate the answer asset folder against the v2 spec by direct
      inspection (the project's current branch does not include `verify_answer_asset.py`; per
      t0046's prior practice, that asset type is validated by direct inspection against the v2
      spec). Satisfies REQ-9, REQ-10, REQ-11.

(All downstream artifacts beyond chart rendering and the answer asset are orchestrator-managed in
execute-task and are NOT covered by this plan, per the planning skill's Forbidden list.)

## Remote Machines

None required. Per `task_description.md`: "Local CPU only. No Vast.ai." The full ~152-trial sweep
runs on the developer laptop at ~5 sec/trial = ~13 min wall-clock. Per-trial peak memory is ~32 MB
of NEURON recorder vectors plus the soma voltage trace; total Python process RSS < 1 GB. No GPU
required. The t0046 library's `nrnmech.dll` is already compiled and lives at
`tasks/t0046_reproduce_poleg_polsky_2016_exact/code/sources/nrnmech.dll`; `build_dsgc()` loads it
transparently via `h.nrn_load_dll`. No MOD recompilation is needed.

## Assets Needed

Input assets and external dependencies:

* **Library asset** `modeldb_189347_dsgc_exact` (registered library) — produced by t0046 at
  `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/`. The
  registered library's implementation lives at `tasks/t0046_.../code/` and is imported wholesale via
  the cross-task package path. Provides: `build_dsgc`, `read_synapse_coords`,
  `assert_bip_positions_baseline`, `run_one_trial`, `TrialResult`, `ensure_neuron_importable`,
  `DT_MS`, `TSTOP_MS`, `V_INIT_MV`, `E_SACINHIB_MV`, `ExperimentType`, `Direction`, plus the
  compiled `code/sources/nrnmech.dll` and the deposited `RGCmodel.hoc` morphology + MOD sources.
* **Library asset** `tuning_curve_viz` (registered library) — produced by t0011 at
  `tasks/t0011_response_visualization_library/code/tuning_curve_viz/`. Used only for the
  `MODEL_COLORS` Okabe-Ito palette constant.
* **Paper asset** `10.1016_j.neuron.2016.02.013` (Poleg-Polsky and Diamond 2016, Neuron) — the
  source of the Fig 3A-E targets and the Fig 3F flatness claim. Lives in t0046's task folder under
  `assets/paper/` and is referenced as a source in the answer asset's `details.json`.
* **Answer asset** `poleg-polsky-2016-reproduction-audit` — produced by t0046 at
  `tasks/t0046_.../assets/answer/`. Source of the 12-entry discrepancy catalogue this task extends.
* **NEURON 8.2.7 + NetPyNE 1.1.1 toolchain** — installed and validated by t0007. No re-install.
* **No external downloads** (no new datasets, no new papers).

## Expected Assets

Output assets (must match `task.json` `expected_assets: {"answer": 1}`):

* **Answer asset** (1) — `polegpolsky-2016-fig3-conductances-validation` at
  `tasks/t0047_validate_pp16_fig3_cond_noise/assets/answer/polegpolsky-2016-fig3-conductances-validation/`
  with `details.json` (v2), `short_answer.md`, and `full_answer.md` per
  `meta/asset_types/answer/specification.md` v2. Question: "Does the deposited ModelDB 189347 code
  reproduce Poleg-Polsky 2016's Fig 3A-F per-synapse conductance balance and DSI-vs-gNMDA flatness,
  and does the extended noise sweep match the paper's qualitative shape?". Sources cited:
  `modeldb_189347_dsgc_exact` (t0046 library), `10.1016_j.neuron.2016.02.013` (Poleg-Polsky 2016
  paper), `poleg-polsky-2016-reproduction-audit` (t0046 audit answer).

In addition (not asset-counted but required deliverables per `task_description.md`):

* Seven reproduction PNGs under `results/images/`: `fig3a_nmda_conductance_pd_vs_nd.png`,
  `fig3b_ampa_conductance_pd_vs_nd.png`, `fig3c_gaba_conductance_pd_vs_nd.png`,
  `fig3f_top_psp_traces.png`, `fig3f_bottom_dsi_vs_gnmda.png`,
  `fig6_dsi_vs_noise_per_condition.png`, `fig7_auc_vs_noise_per_condition.png`.
* Per-trial CSVs under `results/data/`: `gnmda_sweep_trials.csv`, `noise_extension_trials.csv`,
  `psp_traces_fig3f_top.csv`, `conductance_comparison_table.csv`, `dsi_by_gnmda.json`,
  `dsi_auc_by_condition_noise.json`.
* `results/metrics.json` in the explicit multi-variant format with 19 variants (7 gNMDA + 12 noise
  cells), each recording `direction_selectivity_index`.

## Time Estimation

* Research (already complete): research-code stage took ~12 min wall-clock (logged in
  `logs/steps/006_research-code/`).
* Planning (this stage): ~25 min wall-clock to write and verify `plan.md`.
* Implementation (Steps 1-13):
  * Milestone A (scaffolding) — ~10 min.
  * Milestone B (recorder wrapper + smoke test) — ~30 min including the validation-gate run.
  * Milestone C (gNMDA + noise drivers): ~13 min wall-clock for the ~152-trial sweep at ~5 sec /
    trial, plus ~15 min for the validation-gate `--limit 4` runs and ~20 min coding the drivers.
    Total ~48 min.
  * Milestone D (per-cell metrics + metrics.json) — ~20 min.
  * Milestone E (chart rendering + answer asset) — ~45 min including iterating on chart aesthetics
    and writing the full_answer.md tables and synthesis.
* Total implementation: ~2.5 hours wall-clock (consistent with the task description's "1-2 hours"
  estimate; the upper end allows for one unforeseen iteration on the wrapper smoke-test gate).

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| `bipNMDA._ref_gAMPA` or `_ref_gNMDA` not exposed as expected (e.g. RANGE block uses different name) | Low | Blocking — Fig 3A vs 3B split impossible | Inspect `bipolarNMDA.mod` RANGE block (research_code.md confirms `g`, `gAMPA`, `gNMDA` are all RANGE; this is a low-likelihood risk). Smoke test in Step 5 catches mismatch before any sweep. If the handle is genuinely missing, fall back to recording only `_ref_g` (total) and report the AMPA + NMDA combined value, document the limitation in the discrepancy catalogue. |
| Per-trial recorder memory exhaustion at `dt_record_ms = 0.25` (~32 MB / trial) | Low | Process OOM on long trials | Reset every recorder vector (`vec.resize(0)`) at the end of each trial in `run_one_trial_with_conductances`. Vectors persist as objects but their data is discarded. Peak RAM stays bounded at one trial's worth. If RSS still exceeds 4 GB, increase `dt_record_ms` to 0.5 (still > AMPA tau / 4) and re-run. |
| `placeBIP()` accidentally re-creates synapse POINT_PROCESS objects, invalidating the persistent `Vector.record` handles | Low | Silent zero / garbage values | Smoke test in Step 5 verifies non-zero peak conductances on trial 1. Add a second smoke test: run trials 1, 2, 5 in sequence and verify `peak_g_nmda_summed_ns` stays in the same order of magnitude across all three (a sudden drop to zero on trial 2 would indicate handle invalidation). The research_code.md analysis of `placeBIP()` confirms it only re-binds `Vinf` Vector.play vectors, not POINT_PROCESS instances; this is low-likelihood. |
| `assert_bip_positions_baseline` failure inside `run_one_trial` (BIP positions drifted during the sweep) | Low | Sweep halts mid-way | This is t0046's existing safety guard; it raises `AssertionError`. Catch the exception in `run_with_conductances`, log the trial that failed, write what was completed so far to the per-trial CSV, and exit with a clear error. The implementation can then be debugged and the partial CSV preserved. Idempotent re-run resumes from where the CSV left off if the script supports a `--resume-from-csv` flag (optional; not required for first pass). |
| gNMDA = 3.0 nS pushes the soma into AP territory even with TTX nominally on (`SpikesOn = 0`) | Medium | PSP peak unreliable at the highest gNMDA value | Re-confirm `SpikesOn = 0` in t0046's `simplerun()` invocation (it is set in `main.hoc` and not overridden by `run_one_trial`). Inspect `psp_traces_fig3f_top.csv` for the gNMDA = 2.5 PD trace before fitting — if any spikelets appear (peak > 50 mV with a fast deflection), document in the answer asset and exclude that trial from the DSI computation. The 3.0 nS pass is exploratory; the pass criterion only requires reporting the value, not a passing verdict. |
| Cross-task import of t0046's `code` subtree fails because t0046's worktree is in a different folder | Medium | Blocking — wrapper cannot import | The cross-task import works because `tasks/` is on `sys.path` from the repo root, and each task `code/` has `__init__.py`. The implementation agent must run scripts from the repo root via `uv run python -m tasks.t0047_.../code/...` (the `-m` form, not direct `python file.py`). Document this in the script header comments. If the import fails at runtime, the agent should `cd` to the repo root (the task worktree's repo root) and retry. |
| `flicker_var > 0` causes `placeBIP()` to take significantly longer (random noise generation) | Medium | 96-trial noise sweep takes > 13 min | Time the first 4-trial validation-gate run (Step 9). If per-trial wall-clock exceeds 10 sec, the full 96-trial sweep is bounded at ~16 min. Acceptable. If it exceeds 30 sec / trial, reduce `TRIALS_PER_CELL` to 3 for the noise sweep only and record the reduction in the answer asset's discrepancy catalogue. |
| Paper Fig 3A-E values are per-synapse rather than summed (caption ambiguous) | Medium | Verdict misclassified | Report BOTH per-synapse-mean (`peak_g_*_per_syn_mean_ns`) and summed (`peak_g_*_summed_ns`) in the answer asset's table. State both verdicts. Future task can resolve the ambiguity from supplementary materials (S-0046-05 manual fetch). |

## Verification Criteria

Concrete, testable checks that confirm the task is complete:

* **plan.md verificator passes**: Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0047_validate_pp16_fig3_cond_noise -- python -u -m arf.scripts.verificators.verify_plan t0047_validate_pp16_fig3_cond_noise`.
  Expected output: `0 errors`. Warnings about word counts may be acceptable but must each have a
  documented reason.
* **All seven required PNGs exist and are non-empty**: Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0047_validate_pp16_fig3_cond_noise -- python -c "from pathlib import Path; required = ['fig3a_nmda_conductance_pd_vs_nd.png', 'fig3b_ampa_conductance_pd_vs_nd.png', 'fig3c_gaba_conductance_pd_vs_nd.png', 'fig3f_top_psp_traces.png', 'fig3f_bottom_dsi_vs_gnmda.png', 'fig6_dsi_vs_noise_per_condition.png', 'fig7_auc_vs_noise_per_condition.png']; root = Path('tasks/t0047_validate_pp16_fig3_cond_noise/results/images'); [print(p, root.joinpath(p).exists(), root.joinpath(p).stat().st_size if root.joinpath(p).exists() else 0) for p in required]"`.
  Expected output: every line ends with `True <size_in_bytes>` and every size is `>= 10000`.
* **Per-trial CSVs exist with the expected row counts**: `gnmda_sweep_trials.csv` has 56 data rows
  (7 gNMDA × 2 directions × 4 trials); `noise_extension_trials.csv` has 96 data rows (3 conditions
  × 4 noise levels × 2 directions × 4 trials); `psp_traces_fig3f_top.csv` has 6 unique
  `(b2gnmda_ns, direction)` cells. Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0047_validate_pp16_fig3_cond_noise -- python -c "import pandas as pd; print('gnmda', len(pd.read_csv('tasks/t0047_validate_pp16_fig3_cond_noise/results/data/gnmda_sweep_trials.csv'))); print('noise', len(pd.read_csv('tasks/t0047_validate_pp16_fig3_cond_noise/results/data/noise_extension_trials.csv'))); df = pd.read_csv('tasks/t0047_validate_pp16_fig3_cond_noise/results/data/psp_traces_fig3f_top.csv'); print('psp_cells', df.groupby(['b2gnmda_ns','direction']).ngroups)"`.
  Expected output: `gnmda 56`, `noise 96`, `psp_cells 6`.
* **`results/metrics.json` validates**: Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0047_validate_pp16_fig3_cond_noise -- python -u -m arf.scripts.verificators.verify_task_metrics t0047_validate_pp16_fig3_cond_noise`.
  Expected output: `0 errors`. The file must use the explicit multi-variant format with 19 variants,
  each containing `direction_selectivity_index` (the only registered metric this task can compute
  from PD/ND data).
* **Answer asset folder exists with the three required files** and `details.json` declares
  `spec_version: "2"`, `short_answer_path`, `full_answer_path`. Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0047_validate_pp16_fig3_cond_noise -- python -c "import json; from pathlib import Path; root = Path('tasks/t0047_validate_pp16_fig3_cond_noise/assets/answer/polegpolsky-2016-fig3-conductances-validation'); details = json.loads((root / 'details.json').read_text(encoding='utf-8')); print(details['spec_version'], details['short_answer_path'], details['full_answer_path'], (root / 'short_answer.md').exists(), (root / 'full_answer.md').exists())"`.
  Expected output: `2 short_answer.md full_answer.md True True`.
* **REQ coverage check**: every `REQ-*` ID listed in `## Task Requirement Checklist` appears at
  least once in the `## Step by Step` section. Verified by
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0047_validate_pp16_fig3_cond_noise -- python -c "import re; from pathlib import Path; plan = Path('tasks/t0047_validate_pp16_fig3_cond_noise/plan/plan.md').read_text(encoding='utf-8'); reqs = set(re.findall(r'\bREQ-\d+\b', plan)); checklist_idx = plan.find('## Task Requirement Checklist'); steps_idx = plan.find('## Step by Step'); end_idx = plan.find('## Remote Machines'); declared = set(re.findall(r'\bREQ-\d+\b', plan[checklist_idx:steps_idx])); used = set(re.findall(r'\bREQ-\d+\b', plan[steps_idx:end_idx])); print('declared', sorted(declared)); print('used', sorted(used)); print('missing', sorted(declared - used))"`.
  Expected output: the `missing` set is empty.
* **t0046 code is import-only (no fork)**: confirm no file under
  `tasks/t0047_validate_pp16_fig3_cond_noise/code/` duplicates a t0046 file by file size or by
  content hash on a sampled file. Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0047_validate_pp16_fig3_cond_noise -- python -c "from pathlib import Path; t46 = Path('tasks/t0046_reproduce_poleg_polsky_2016_exact/code'); t47 = Path('tasks/t0047_validate_pp16_fig3_cond_noise/code'); shared = {p.name for p in t47.glob('*.py')} & {p.name for p in t46.glob('*.py')}; print('shared filenames (must be empty or only paths.py / constants.py / __init__.py):', sorted(shared))"`.
  Expected output: the only overlapping filenames are `paths.py`, `constants.py`, and `__init__.py`
  (each is allowed because we author our own version with task-specific paths and constants; the
  t0046 versions are imported as `tasks.t0046_....constants`).

## Alternative Approaches Considered

(Already covered inline in `## Approach`; reproduced here for reviewer convenience.)

* Add `_ref_i` recorders directly — rejected; doubles memory for no benefit, offline
  `i = g * (v - e)` is exact.
* Modify t0046's `run_simplerun.py` in place — rejected; violates the cross-task code-reuse rule
  for registered libraries.
* Defer the noise extension to a separate task — rejected; shares the same wrapper infrastructure
  and the same answer asset.
* Use t0012's `compute_dsi` with a 12-angle TuningCurve — rejected; library validates 12 angles,
  copying the 8-line PD/ND helper is simpler.
* Use the legacy flat `metrics.json` format — rejected; this is a multi-condition experiment, the
  experiment-run task type's planning guidelines mandate the explicit variant format.
