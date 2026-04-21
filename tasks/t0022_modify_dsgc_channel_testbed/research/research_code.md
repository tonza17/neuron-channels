---
spec_version: "1"
task_id: "t0022_modify_dsgc_channel_testbed"
research_stage: "code"
tasks_reviewed: 13
tasks_cited: 12
libraries_found: 4
libraries_relevant: 4
date_completed: "2026-04-21"
status: "complete"
---
# Research Code: Modify DSGC Port for Dendritic-Computation DS with Channel-Modular AIS

## Task Objective

Produce a new NEURON library asset `modeldb_189347_dsgc_dendritic` that replaces the stimulus-
rotation driver of [t0008] and the gabaMOD parameter-swap driver of [t0020] with a per-dendrite E-I
scheduler: direction sets timing offsets per excitation-inhibition pair (shunting on-the-path
inhibition) while stimulus position is a single moving-bar sweep, not a rotation of BIP coordinates.
The asset must expose channel-modular `forsec` partitioning so AIS channels (Nav1.1 proximal, Nav1.6
\+ Kv1.2 distal) and soma/dendrite channels can be added, removed, or replaced without editing the
driver, emit a 12-angle tuning CSV with >=10 trials per angle, and score via the t0012 library with
DSI >=0.5 and peak >=10 Hz acceptance gates. Research here documents everything the implementation
subagent needs to avoid reinventing the cell-build, scoring, or CSV-plumbing code already produced
in prior tasks.

## Library Landscape

Four project libraries were discovered by inspecting `tasks/*/assets/library/*/details.json`
directly (the `aggregate_libraries` script is absent from this worktree's `arf/scripts/aggregators/`
tree; the same data was read from each `details.json` to preserve auditability). All four are
`spec_version "2"` and all four are relevant to t0022.

* `modeldb_189347_dsgc` v0.1.0 (created by [t0008]) — the verbatim Poleg-Polsky & Diamond 2016
  HOC/MOD port with a Python driver that rotates BIP synapse coordinates per angle. **Relevant**:
  the HOC sources (`RGCmodel.hoc`, `dsgc_model.hoc`, MOD files), the `build_dsgc()` entry point, the
  `apply_params()` parameterisation, and the synapse-coordinate snapshot / restore helpers are the
  exact pieces t0022 must import. Path:
  `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/`. No corrections overlay.

* `tuning_curve_loss` v0.1.0 (created by [t0012]) — pure-Python + NumPy + pandas scorer that loads
  a canonical `(angle_deg, trial_seed, firing_rate_hz)` CSV, computes DSI / peak / null / HWHM /
  split-half reliability, and gates against the literature envelope. **Relevant**: t0022 Requirement
  6 names this library explicitly. Path:
  `tasks/t0012_tuning_curve_scoring_loss_library/assets/library/tuning_curve_loss/`.

* `tuning_curve_viz` v0.1.0 (created by [t0011]) — matplotlib Cartesian / polar / overlay / raster
  rendering library that consumes the same canonical CSV schema. **Relevant for results rendering**:
  the comparison chart required in t0022 `results_detailed.md` (t0022 vs t0008 vs t0020) can be
  produced with `plot_multi_model_overlay(...)`. Path:
  `tasks/t0011_response_visualization_library/assets/library/tuning_curve_viz/`.

* `modeldb_189347_dsgc_gabamod` v0.1.0 (created by [t0020]) — sibling driver that reuses t0008's
  `build_dsgc()` and `apply_params()` but overrides `h.gabaMOD` between PD (0.33) and ND (0.99)
  instead of rotating synapse coordinates. **Relevant as a code-style template**: t0020 shows the
  exact pattern t0022 must follow — fork t0008's driver, keep the cell build, replace the
  per-trial direction-control mechanism, and keep the canonical CSV schema. Path:
  `tasks/t0020_port_modeldb_189347_gabamod/assets/library/modeldb_189347_dsgc_gabamod/`.

No libraries produced by [t0015]-[t0019] (those tasks produced answer assets, not libraries), and
none were corrected by downstream tasks.

## Key Findings

### Driver architecture is a thin Python shell around verbatim HOC

Both [t0008] and [t0020] use the same pattern: Python loads `nrnmech.dll`, sources `RGCmodel.hoc`
(11 861 lines, verbatim Poleg-Polsky) and `dsgc_model.hoc` (330 lines, GUI-free derivative), then
drives a per-trial loop. The cell itself — morphology, `HHst` insertion, `bipNMDA`/`SACinhib`/
`SACexc` point processes, `placeBIP()` procedure — lives entirely in HOC. This means t0022 must
extend, not replace, the HOC layer: the channel-modular `forsec` blocks required by Requirement 5
belong in a new HOC file sourced after `RGCmodel.hoc`, not in Python. The existing `RGCmodel.hoc`
already has four `forsec` blocks (at lines 11 800, 11 813, 11 820, 11 832) that iterate over `all`,
`dends`, and `ON` SectionLists — the same pattern will be extended for AIS/soma/dend channel sets.

### DSI mechanism differs radically between t0008 and t0020 — t0022 is a third path

[t0008] achieves DSI 0.316 (peak 18.1 Hz) by rotating **only** `BIPsyn.locx/locy` while keeping
`SACinhibsyn` and `SACexcsyn` coordinates fixed; this breaks the bundled BIP/SAC spatial symmetry
and biases arrival times. The rotation is explicitly commented (`build_cell.py:218-239`) as a proxy,
not the paper's mechanism. [t0020] achieves DSI 0.7838 (peak 14.85 Hz) by overriding the single
global `h.gabaMOD` scalar between PD (0.33) and ND (0.99) — the paper's native protocol — with a
per-trial `_assert_bip_positions_baseline()` guard (`run_gabamod_sweep.py:109-127`) that fires if
any BIP coordinate drifts from baseline, preventing the rotation logic from silently re-engaging.
t0022 must do **neither**: no rotation, no gabaMOD swap. Instead it schedules inhibitory arrival
time per-dendrite so that null-direction bars see inhibition before excitation (shunting veto) while
preferred-direction bars see excitation first. The asymmetry lives in per- synapse `starttime`
offsets derived from the cell's native geometry plus a direction-dependent delay term, and is
applied once per angle rather than by editing a global scalar.

### Canonical CSV schema is shared and must not change

[t0004] defines and [t0012] consumes a single tuning-curve CSV schema:
`(angle_deg, trial_seed, firing_rate_hz)`. [t0008] emits it at
`data/tuning_curves/curve_modeldb_189347.csv` with 240 rows (12 * 20); [t0011]'s viz and [t0012]'s
scorer both load exactly this format via `load_tuning_curve(...)` in `tuning_curve_loss/loader.py`.
[t0020] deviated to a 2-condition `(condition, trial_seed, firing_rate_hz)` schema because gabaMOD
PD/ND has no natural angle axis, and consequently had to re-implement DSI locally and bypass the
12-angle t0012 scorer path. **t0022 reverts to the 12-angle canonical schema** so
`tuning_curve_loss.score(simulated_curve_csv=...)` works unchanged.

### Scoring glue is a 101-line script with four metric keys

[t0008]'s `code/score_envelope.py` (101 lines) is the canonical scoring glue: it reads the CSV,
calls `tuning_curve_loss.score(simulated_curve_csv=TUNING_CURVE_MODELDB_CSV)`, dumps the full
`ScoreReport` to `data/score_report.json`, and writes the four registered metric keys
(`direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
`tuning_curve_rmse`) to `results/metrics.json`. The four keys come from
`tuning_curve_loss/__init__.py` as `METRIC_KEY_*` constants. This exact script can be copied into
t0022 with only the CSV filename changed. [t0020]'s `code/score_envelope.py` (208 lines) is a
diverged version that bakes in the PD/ND-only computation; it is **not** the template for t0022.

### AIS channel priors from [t0017] and [t0019] are order-of-magnitude constraints

[t0017] and [t0019] answer assets supply Nav1.6 at distal AIS, Nav1.2 (project description mentions
Nav1.1 but the AIS literature consistently reports Nav1.2 — the implementation subagent should
reconcile the terminology) at proximal AIS, Kv1.1/Kv1.2 co-localised with Nav1.6 at the distal AIS,
peak AIS Nav conductance density ~2500-5000 pS/um2 (~50x somatic), and Nav1.6 activation V_half
~10-15 mV more negative than Nav1.2. These map directly onto two `forsec AIS` sub-blocks (`proximal`
/ `distal`) with explicit `insert`/`gbar` lines; [t0019]'s answer also flags Fohlmeister-Miller 1997
as the canonical HH kinetic source for RGC Na/K. These priors are for later channel-testbed tasks
but must be settable via `forsec` hooks in t0022 today.

### Known NEURON-on-Windows quirks

[t0020]'s driver contains a 55-line `_ensure_neuron_importable()` helper
(`run_gabamod_sweep.py:29- 81`) that sets `NEURONHOME`, re-execs the process if the variable was
missing at C startup, inserts `<NEURONHOME>/lib/python` on `sys.path`, and calls
`os.add_dll_directory(...)` so `hoc.pyd` finds `libnrniv.dll`. [t0008]'s simpler `load_neuron()`
(`build_cell.py:96-117`) assumes `NEURONHOME` is already set. t0022 should adopt the t0020 bootstrap
— it is the robust form, proven across 40 trials. HOC path literals must use forward slashes on
Windows (`build_cell.py:120-126`); the `_sources_dir_hoc_safe()` helper implements that escape.

## Reusable Code and Assets

### Import via library: `modeldb_189347_dsgc` cell build and parameterisation

* **Source**: [t0008] `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/` and the
  accompanying driver modules in `tasks/t0008_port_modeldb_189347/code/`.
* **What it does**: Loads compiled `nrnmech.dll`, sources RGCmodel.hoc + dsgc_model.hoc, and returns
  a fully-initialised `h` with `h.RGC` (soma + 350 dend sections, 282 ON-dendrite triples of
  BIP/SACinhib/SACexc point processes, HHst inserted on soma).
* **Reuse method**: **import via library** (registered library, absolute import from
  `tasks.t0008_port_modeldb_189347.code.*`).
* **Function signatures to import**:
  * `def load_neuron() -> Any` (build_cell.py:96, idempotent DLL loader)
  * `def build_dsgc() -> Any` (build_cell.py:129, 47-line full cell bootstrap)
  * `def get_cell_summary(h: Any) -> CellSummary` (build_cell.py:178)
  * `def read_synapse_coords(h: Any) -> list[SynapseCoords]` (build_cell.py:192, 17 lines)
  * `def reset_synapse_coords(*, h: Any, baseline: list[SynapseCoords]) -> None` (build_cell.py:265,
    13 lines)
  * `def apply_params(h: Any, *, seed: int) -> None` (build_cell.py:280, 38 lines — sets
    conductances, stimulus geometry, HHst vshift, NMDA kinetics)
* **Adaptation needed**: none; import as-is. t0022 does **not** import `run_one_trial` or
  `rotate_synapse_coords_in_place` — both are rotation-proxy logic to avoid.
* **Line count to reuse via import**: ~180 lines of `build_cell.py` plus the full HOC skeleton (12
  587 HOC lines bundled in the library asset).

### Import via library: `tuning_curve_loss` scorer

* **Source**: [t0012]
  `tasks/t0012_tuning_curve_scoring_loss_library/assets/library/tuning_curve_loss/`.
* **What it does**: Loads a canonical tuning-curve CSV, computes DSI / peak / null / HWHM /
  split-half reliability, scores against the t0004 target, returns a frozen `ScoreReport` with
  per-metric residuals, envelope pass/fail flags, and an overall `loss_scalar`.
* **Reuse method**: **import via library**.
* **Key entry points**:
  * `def score(*, simulated_curve_csv: Path, ...) -> ScoreReport` (scoring.py, main entry)
  * `def compute_dsi(...) -> float`, `compute_peak_hz`, `compute_null_hz`, `compute_hwhm_deg`
    (metrics.py, 125 lines total)
  * `def compute_reliability(...) -> float | None` (split-half Pearson correlation)
  * Constants `METRIC_KEY_DSI`, `METRIC_KEY_HWHM`, `METRIC_KEY_RELIABILITY`, `METRIC_KEY_RMSE`
    (`__init__.py`, 88 lines)
* **Adaptation needed**: none. Works on any `(angle_deg, trial_seed, firing_rate_hz)` CSV; t0022
  must emit that schema verbatim to satisfy Requirement 2.

### Copy into task: 12-angle sweep driver skeleton (95 lines)

* **Source**: [t0008] `tasks/t0008_port_modeldb_189347/code/run_tuning_curve.py` (95 lines).
* **What it does**: Builds the cell once, loops over 12 angles x 20 trials, calls a per-trial
  function, and emits the canonical CSV.
* **Reuse method**: **copy into task** (non-library code). Per Key Rule 9 and the cross-task
  code-reuse rule, `code/` modules from other tasks cannot be imported; they must be copied.
* **Adaptation needed**: replace the call to
  `run_one_trial(h=h, angle_deg=..., seed=..., baseline_coords=...)` with a new t0022-local
  `run_one_trial_dendritic(h=h, angle_deg=..., seed=..., ei_schedule=...)` that (a) applies params
  via the imported `apply_params`, (b) sets per-dendrite inhibitory `starttime` offsets derived from
  angle + dendrite azimuth, (c) does NOT rotate BIP coordinates, (d) finitialize + continuerun +
  count threshold crossings.

### Copy into task: scoring-glue script (101 lines)

* **Source**: [t0008] `tasks/t0008_port_modeldb_189347/code/score_envelope.py` (101 lines).
* **What it does**: Loads the tuning curve, calls `tuning_curve_loss.score(...)`, writes
  `data/score_report.json` and `results/metrics.json` with the four registered metric keys.
* **Reuse method**: **copy into task**.
* **Adaptation needed**: change the CSV path constant to the t0022-local one; leave the rest
  unchanged so the four-metric-key `results/metrics.json` is produced automatically.

### Copy into task: NEURON-on-Windows bootstrap (55 lines)

* **Source**: [t0020] `tasks/t0020_port_modeldb_189347_gabamod/code/run_gabamod_sweep.py:29-81` —
  the `_ensure_neuron_importable()` helper and the `_NEURONHOME_DEFAULT` /
  `_NEURONHOME_SENTINEL_ENV` constants.
* **What it does**: Guarantees `NEURONHOME` is in the C environment (re-execing if needed), inserts
  `<NEURONHOME>/lib/python` on `sys.path`, and registers `<NEURONHOME>/bin` as a DLL search
  directory for `hoc.pyd`.
* **Reuse method**: **copy into task**.
* **Adaptation needed**: rename sentinel env-var to `_T0022_NEURONHOME_BOOTSTRAPPED` to avoid
  cross-task collisions if two drivers run back-to-back.

### Copy into task: `constants.py` + `paths.py` skeletons (~100 lines combined)

* **Source**: [t0008] `code/constants.py` (85 lines) and `code/paths.py` (91 lines).
* **What it does**: Centralises all HOC-value constants (`TSTOP_MS`, `DT_MS`, `CELSIUS_DEG_C`,
  `LIGHTSPEED_UM_PER_MS`, `V_INIT_MV`, `AP_THRESHOLD_MV`, `B2GAMPA_NS`, `B2GNMDA_NS`, `S2GGABA_NS`,
  `N_ANGLES=12`, `N_TRIALS=20`, etc.) and path constants (`LIBRARY_ASSET_DIR`,
  `MODELDB_SOURCES_DIR`, `TUNING_CURVES_DIR`, `SCORE_REPORT_JSON`, `METRICS_JSON`).
* **Reuse method**: **copy into task**. Copy verbatim, then add the per-dendrite E-I scheduler
  constants (null/preferred delay offsets, inhibition strength scalar, any new conductance knobs for
  the channel-modular AIS).

### Import via library (optional, for results rendering): `tuning_curve_viz`

* **Source**: [t0011] `tasks/t0011_response_visualization_library/assets/library/tuning_curve_viz/`.
* **What it does**: Renders polar / Cartesian / overlay / raster PNGs from the canonical CSV.
* **Reuse method**: **import via library**.
* **Adaptation needed**: none. The multi-model overlay is the simplest way to produce the comparison
  chart required in t0022 `results_detailed.md`.

### Reference: t0008's `description.md` AIS / channel commentary

* **Source**: [t0008]
  `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/ description.md`.
* **What it does**: Documents the bundled HHst insertion and morphology; a useful style template for
  the t0022 library `description.md`, which must explain how to add/remove channels in each
  compartment without touching the driver (Requirement 5).
* **Reuse method**: **copy into task** (as a style template only; the content must be rewritten for
  the new `forsec` layout).

## Lessons Learned

* **Rotation proxy does not reach envelope** ([t0008]): DSI 0.316 against the 0.70-0.85 target;
  rotating only BIP (not SAC) coordinates is biologically inauthentic and does not reproduce the
  paper's contrast. Do not repeat this for t0022.
* **gabaMOD swap reaches DSI envelope but not peak** ([t0020]): DSI 0.7838 (inside [0.70, 0.85]) but
  peak 14.85 Hz (below [40, 80]). The two ports confirm that the 14-18 Hz peak ceiling is a property
  of the bundled HHst channel parameters + the single-cell HHst-only AIS, not of the driver. **Do
  not chase the 40-80 Hz peak in t0022**: Requirement 4 explicitly sets a >=10 Hz acceptance, and
  the peak-gap investigation is out of scope. A follow-up channel-testbed task will attempt the peak
  by swapping in split Nav1.6/Nav1.2 + Kv1.2 AIS channels.
* **Per-trial assertions save debugging time** ([t0020]): `_assert_bip_positions_baseline()` fires
  on any silent re-engagement of rotation logic. t0022 should add an equivalent assertion that
  checks the global `h.gabaMOD` stays at its baseline (no stealth parameter swap) and that BIP
  coordinates remain at baseline (no stealth rotation) on every trial.
* **Shared parameterisation reduces drift** ([t0020] reused [t0008]'s `apply_params`): building the
  cell and parameterising it in a single place prevents per-task constant drift. t0022 must follow
  the same pattern rather than re-initialising the HOC globals in a task-local function.
* **HOC path escaping is a silent Windows failure mode** ([t0008]): backslashes in `h.chdir("...")`
  are parsed as HOC escape sequences; `_sources_dir_hoc_safe()` converts to forward slashes.
  Propagate this helper if any new HOC file has to be sourced from a task-local directory.
* **Reliability is trivially high because noise is synthetic** ([t0008]): reliability 0.991 with 20
  trials per angle, because the per-trial randomness is a seeded BIP jitter. t0022 should keep 10-20
  trials (Requirement 2) — there is no statistical reason to inflate trial counts.
* **Scoring identity test catches target drift** ([t0012]): `score(target, target).loss_scalar` is
  exactly 0.0. If t0022 ever modifies the target CSV or the scorer weights, that identity must hold
  or the pipeline is broken.

## Recommendations for This Task

1. **Import [t0008]'s library wholesale** — `build_dsgc`, `apply_params`, `read_synapse_coords`,
   `reset_synapse_coords`, and the `SynapseCoords` / `CellSummary` dataclasses. **Do not import**
   `run_one_trial` or `rotate_synapse_coords_in_place`.
2. **Copy the [t0020] NEURONHOME bootstrap verbatim** — it is already proven; rename the sentinel
   env-var to `_T0022_NEURONHOME_BOOTSTRAPPED`.
3. **Copy [t0008]'s `run_tuning_curve.py` skeleton** and replace the inner per-trial call with a new
   `run_one_trial_dendritic(...)` that sets per-dendrite inhibitory `starttime` offsets from the
   angle + dendrite azimuth instead of rotating BIP coordinates. Keep the canonical CSV schema
   `(angle_deg, trial_seed, firing_rate_hz)`.
4. **Copy [t0008]'s `score_envelope.py` verbatim** and only change the CSV path constant. The
   four-metric-key `results/metrics.json` emission is already correct.
5. **Source a new HOC file after `RGCmodel.hoc`** that adds three explicit SectionList-scoped
   `forsec` blocks — `AIS_PROXIMAL`, `AIS_DISTAL`, `SOMA_CHANNELS`, `DEND_CHANNELS` — so channel
   sets can be added/removed/replaced by editing the HOC, not the Python driver. Populate today with
   the [t0008] HHst baseline (unchanged) so t0022 remains a testbed, not a channel experiment; later
   tasks will swap in Nav1.6/Nav1.2/Kv1.2 per [t0017] and [t0019].
6. **Add a per-trial assertion** that both `h.gabaMOD == GABA_MOD` (0.33, baseline) and every
   `BIPsyn.locx/locy` equals its baseline. Mirrors [t0020]'s guard and enforces "only the direction
   changes" (Requirement 3).
7. **Produce the comparison table** required in `results_detailed.md` using the metric values
   aggregated here: t0008 DSI 0.316 / peak 18.1 Hz / HWHM 82.8 deg / reliability 0.991 vs t0020 DSI
   0.7838 / peak 14.85 Hz vs t0022 (new values). Use
   `tuning_curve_viz.plot_multi_model_ overlay(...)` to render a polar overlay of all three into
   `results/images/`.
8. **Target the >=10 Hz peak / >=0.5 DSI acceptance gate in Requirement 4** — do not chase the
   paper's 40-80 Hz envelope. The peak-gap is explicitly out of scope.

## Task Index

### [t0004]

* **Task ID**: `t0004_generate_target_tuning_curve`
* **Name**: Generate canonical target angle-to-AP-rate tuning curve
* **Status**: completed
* **Relevance**: Source of the canonical 12-angle target CSV schema and of the target curve that
  `tuning_curve_loss.score(...)` compares against. t0022's CSV must match this schema.

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 and similar DSGC compartmental models to NEURON
* **Status**: completed
* **Relevance**: Source of the `modeldb_189347_dsgc` library (HOC/MOD sources, cell build, param
  apply, synapse-coord snapshot/restore) and the script skeletons t0022 copies
  (`run_tuning_curve .py`, `score_envelope.py`). Rotation-proxy result DSI 0.316 / peak 18.1 Hz is
  the baseline comparison anchor.

### [t0009]

* **Task ID**: `t0009_calibrate_dendritic_diameters`
* **Name**: Calibrate dendritic diameters for dsgc-baseline-morphology
* **Status**: completed
* **Relevance**: Produced the calibrated DSGC SWC; t0008 documented (not swapped in) this
  morphology. t0022 also uses the bundled Poleg-Polsky morphology and only references the calibrated
  SWC for future channel-testbed tasks.

### [t0011]

* **Task ID**: `t0011_response_visualization_library`
* **Name**: Response-visualisation library (firing rate vs angle graphs)
* **Status**: completed
* **Relevance**: Source of the `tuning_curve_viz` library used to render the t0022 vs t0008 vs t0020
  comparison chart for `results_detailed.md`.

### [t0012]

* **Task ID**: `t0012_tuning_curve_scoring_loss_library`
* **Name**: Tuning-curve scoring loss library
* **Status**: completed
* **Relevance**: Source of the `tuning_curve_loss` library named in Requirement 6 (DSI, HWHM, peak,
  reliability, RMSE). t0022 imports `score(...)` and the four `METRIC_KEY_*` constants unchanged.

### [t0015]

* **Task ID**: `t0015_literature_survey_cable_theory`
* **Name**: Literature survey: cable theory and dendritic filtering
* **Status**: completed
* **Relevance**: Cable-theory priors constraining dendritic space constants and the region over
  which on-the-path inhibition can shunt excitation — informs the per-dendrite E-I scheduler
  geometry in t0022.

### [t0016]

* **Task ID**: `t0016_literature_survey_dendritic_computation`
* **Name**: Literature survey: dendritic computation beyond DSGCs
* **Status**: completed
* **Relevance**: Supplies the on-the-path shunting motif that motivates t0022's spatially-
  asymmetric inhibition mechanism; NMDA-on-branch supralinearity and asymmetric inhibition placement
  are the two transferable motifs.

### [t0017]

* **Task ID**: `t0017_literature_survey_patch_clamp`
* **Name**: Literature survey: patch-clamp recordings of RGCs and DSGCs
* **Status**: completed
* **Relevance**: AIS channel-density priors (Nav1.6 distal / Nav1.2 proximal, ~50x somatic density)
  for the channel-modular AIS layout in t0022 Requirement 5.

### [t0018]

* **Task ID**: `t0018_literature_survey_synaptic_integration`
* **Name**: Literature survey: synaptic integration in RGC-adjacent systems
* **Status**: completed
* **Relevance**: E-I temporal co-tuning and AMPA/NMDA/GABA kinetic priors for the per-dendrite E-I
  scheduler driver.

### [t0019]

* **Task ID**: `t0019_literature_survey_voltage_gated_channels`
* **Name**: Literature survey: voltage-gated channels in retinal ganglion cells
* **Status**: completed
* **Relevance**: Kv1/Kv3 AIS placement priors and Fohlmeister-Miller HH kinetics; the
  `forsec AIS_DISTAL` block in t0022's new HOC file must be able to carry these channels verbatim
  when later testbed tasks swap them in.

### [t0020]

* **Task ID**: `t0020_port_modeldb_189347_gabamod`
* **Name**: Port ModelDB 189347 DSGC under native gabaMOD parameter-swap protocol
* **Status**: completed
* **Relevance**: Sibling port and direct comparison anchor (DSI 0.7838 / peak 14.85 Hz). Source of
  the robust NEURON-on-Windows bootstrap and the per-trial baseline-coordinate assertion pattern
  t0022 reuses.

### [t0021]

* **Task ID**: `t0021_brainstorm_results_4`
* **Name**: Brainstorm Session 4: DSGC Model Channel Testbed
* **Status**: completed
* **Relevance**: Strategic brainstorm that produced t0022; sets the channel-testbed framing and the
  acceptance gates (DSI >=0.5, peak >=10 Hz) adopted in Requirement 4.
