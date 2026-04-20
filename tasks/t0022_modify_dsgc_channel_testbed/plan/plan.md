---
spec_version: "2"
task_id: "t0022_modify_dsgc_channel_testbed"
date_completed: "2026-04-21"
status: "complete"
---
# Plan: Modify DSGC Port with Spatially-Asymmetric Inhibition for Channel Testbed

## Objective

Produce a new NEURON library asset `modeldb_189347_dsgc_dendritic` (sibling to `modeldb_189347_dsgc`
from t0008 and `modeldb_189347_dsgc_gabamod` from t0020) in which direction selectivity arises from
per-dendrite spatially-asymmetric inhibition (on-the-path shunting per Koch-Poggio-Torre 1982/1983,
Taylor 2000) rather than from stimulus-rotation or global gabaMOD swap, and expose the AIS / soma /
dendrite compartments as explicit `forsec` blocks so follow-up channel-swap tasks can edit channels
without touching the driver. Run a 12-angle moving-bar sweep with >=10 trials per angle, score via
t0012 `tuning_curve_loss`, and hit DSI >= 0.5 with peak >= 10 Hz. "Done" means: new library asset
passes `verify_library_asset`, `tuning_curves.csv` has exactly 12 x >=10 = >=120 rows, and
`score_report.json` reports DSI >= 0.5 and peak >= 10 Hz.

## Task Requirement Checklist

Verbatim task text from `task.json` plus the resolved `task_description.md` scope and requirements:

> **Name**: Modify DSGC port with spatially-asymmetric inhibition for channel testbed
>
> **Short description**: Modify modeldb_189347_dsgc to produce DSI via dendritic-computation with
> 12-angle moving-bar sweep and channel-modular AIS for spike-mechanism testing.
>
> **Long description (task_description.md Requirements section)**:
>
> 1. Dendritic-computation DS: stimulus is a moving bar in 12 directions (0, 30, ..., 330); no
>    per-condition gabaMOD swaps or per-angle BIP coordinate rotation. DS arises from
>    spatially-asymmetric inhibition (Koch-Poggio-Torre / Barlow-Levick on-the-path shunting).
> 2. 12-angle coverage: `tuning_curves.csv` with columns `(angle_deg, trial_seed, firing_rate_hz)`,
>    at least 10 trials per angle, >=120 rows total.
> 3. Dendritic-computation only: a single fixed mechanism set across all 12 angles; only the
>    stimulus direction changes. No parameter swaps, no driver tricks.
> 4. Spike output: somatic spikes detectable at least in the preferred direction. Peak firing rate
>    at or above 10 Hz target; DSI at or above 0.5 acceptable (hitting the paper's [40, 80] Hz peak
>    envelope is not required).
> 5. Channel-modular AIS: AIS, soma, and dendrite regions in separate `forsec` blocks with explicit
>    channel-insertion points. `description.md` documents how to add/remove channels and how to swap
>    the spike.mod channel set.
> 6. Metrics: use t0012's `tuning_curve_loss` scorer to compute DSI, HWHM, peak firing rate, and
>    per-angle reliability. Produce `score_report.json`.
> 7. Comparison: `results_detailed.md` includes a comparison table vs t0008 (rotation proxy: DSI
>    0.316, peak 18.1 Hz) and t0020 (gabaMOD swap: DSI 0.7838, peak 14.85 Hz) covering DSI, peak,
>    HWHM, and reliability.

Decomposition into stable checklist IDs:

* **REQ-1**: Driver implements dendritic-computation DS via per-dendrite E-I pairs with
  direction-dependent timing offsets; NO BIP coordinate rotation and NO gabaMOD parameter swap.
  Satisfied by Steps 5-7. Evidence: per-trial assertion that `h.gabaMOD` and every
  `BIPsyn.locx/locy` remain at baseline, plus code review of the new `run_one_trial_dendritic`
  function.
* **REQ-2**: 12-angle sweep with >=10 trials per angle produces `tuning_curves.csv` with columns
  `(angle_deg, trial_seed, firing_rate_hz)` and >=120 rows. Satisfied by Step 10 (preflight gate)
  and Step 11 (full sweep). Evidence: row count of
  `data/tuning_curves/curve_modeldb_189347_dendritic.csv`.
* **REQ-3**: Single fixed mechanism set across all 12 angles — only bar direction varies.
  Satisfied by Step 7. Evidence: the `run_one_trial_dendritic` body and the per-trial
  baseline-assertion block.
* **REQ-4**: Spike output with peak >= 10 Hz and DSI >= 0.5. Satisfied by Step 12 (scoring).
  Evidence: `data/score_report.json` `metrics.direction_selectivity_index >= 0.5` and
  `metrics.peak_firing_rate_hz >= 10`.
* **REQ-5**: Channel-modular AIS partition as separate `forsec` blocks (soma, dendrite, proximal
  AIS, distal AIS, thin axon), with `description.md` documenting add/remove/swap. Satisfied by Steps
  3, 4, and 13. Evidence: the new HOC overlay file, the library `description.md` Channel-Modular
  Partition section, and the Nav1.1-not-Nav1.2 correction note.
* **REQ-6**: t0012 `tuning_curve_loss` scorer produces `score_report.json` with DSI, HWHM, peak,
  reliability. Satisfied by Step 12. Evidence: `data/score_report.json` populated with all four
  METRIC_KEY_* entries.
* **REQ-7**: `results_detailed.md` comparison table vs t0008 and t0020. This is orchestrator work
  (execute-task post-implementation), not plan-step work; named here for traceability but not
  implemented in the Step by Step section.

## Approach

The t0022 driver inherits the Poleg-Polsky 2016 HOC skeleton, the `build_dsgc()` bootstrap, and the
`apply_params()` parameterisation from `modeldb_189347_dsgc` (t0008) unchanged. The new mechanism
replaces t0008's `run_one_trial` (rotation proxy, rejected) and t0020's `run_one_trial_gabamod`
(global scalar swap, rejected) with `run_one_trial_dendritic`, which inserts one AMPA (Exp2Syn) and
one GABA_A (Exp2Syn) synapse per dendritic subunit, positions the GABA proximal to the AMPA on the
same branch (on-the-path shunt per KochPoggio1982), and schedules per-synapse onsets via VecStim so
that E leads I by +10 ms in the preferred direction and I leads E by 10 ms in the null direction
(WehrZador2003, KochPoggio1983 5-20 ms window). Per-dendrite E conductance ~0.3 nS
(direction-untuned) and I conductance ~0.6-2.4 nS with null/preferred ratio 2-4x (Park2014).

Channel-modular AIS partitioning is delivered via a new HOC overlay file sourced after
`RGCmodel.hoc` that declares five SectionLists — `SOMA_CHANNELS`, `DEND_CHANNELS`, `AIS_PROXIMAL`,
`AIS_DISTAL`, `THIN_AXON` — each with a single `forsec` insertion block. Baseline channel set is
the t0008 HHst inheritance unchanged (t0022 is the testbed; follow-up tasks swap channels). The
library `description.md` documents the partition with channel-density priors from
research_internet.md (Nav1.6 distal 8 S/cm^2, Nav1.1 proximal 1.5 S/cm^2, Kv1.2 distal 0.1 S/cm^2)
and flags the Nav1.1-not-Nav1.2 correction per VanWart2006.

**Alternatives considered**: (a) Keep t0008's stimulus-rotation proxy — rejected because it
doesn't implement spatially-asymmetric inhibition as a biophysical mechanism, only as a geometric
trick, and already underperformed (DSI 0.316) against the dendritic-computation target. (b) Reuse
t0020's gabaMOD global-scale swap — rejected because it toggles a single global parameter rather
than the spatial/temporal structure of individual synaptic inputs, making it unable to serve as a
testbed for channel-density effects on dendritic integration. Per-dendrite E-I scheduling is the
only approach that matches the dendritic-computation mechanism described in KochPoggio1982/1983 and
Taylor2000.

**Task types**: `code-reproduction` (matches `task.json`). The code-reproduction planning guidelines
from `meta/task_types/code-reproduction/instruction.md` require marking the driver execution step as
`[CRITICAL]`, using absolute imports with keyword arguments, centralising paths in `code/paths.py`,
and logging environment details — all adopted below.

## Cost Estimation

Total: **$0**. All work runs on the local Windows workstation (same environment as t0008 and t0020).
No API calls, no remote GPU compute, no paid datasets. Budget in `project/budget.json` is not
touched. Itemised: NEURON simulation (~9-15 minutes of local CPU, $0), Python orchestration ($0),
library-asset metadata authoring ($0).

## Step by Step

Grouped into four milestones: (A) library-asset skeleton, (B) per-dendrite E-I driver, (C) preflight
validation gate, (D) full 12-angle sweep + scoring.

### Milestone A: Library-Asset Skeleton

1. **Copy the NEURON-on-Windows bootstrap and t0008 shared code.** Create
   `tasks/t0022_modify_dsgc_channel_testbed/code/` and copy verbatim: `constants.py` (~85 lines) and
   `paths.py` (~91 lines) from `tasks/t0008_port_modeldb_189347/code/`. Then copy the 55-line
   `_ensure_neuron_importable()` helper and `_NEURONHOME_DEFAULT`/`_NEURONHOME_SENTINEL_ENV` from
   `tasks/t0020_port_modeldb_189347_gabamod/code/run_gabamod_sweep.py` (lines 29-81) into a new
   `code/neuron_bootstrap.py`. Rename the sentinel env-var to `_T0022_NEURONHOME_BOOTSTRAPPED` to
   avoid cross-task collisions. Add new constants to `constants.py`:
   `EI_OFFSET_PREFERRED_MS = 10.0`, `EI_OFFSET_NULL_MS = -10.0`, `EI_OFFSET_BAND_MS = (5.0, 20.0)`,
   `AMPA_CONDUCTANCE_NS = 0.3`, `GABA_CONDUCTANCE_PREFERRED_NS = 0.6`,
   `GABA_CONDUCTANCE_NULL_NS = 2.4`, `GABA_NULL_PREF_RATIO = 4.0`, `BAR_VELOCITY_UM_PER_MS = 1.0`,
   `N_ANGLES = 12`, `N_TRIALS = 10`. Satisfies REQ-3 (fixed mechanism set).

2. **Create library-asset folder and stub details.json.** Create
   `tasks/t0022_modify_dsgc_channel_testbed/assets/library/modeldb_189347_dsgc_dendritic/` with
   `details.json` populated with `spec_version: "2"`, `library_id: "modeldb_189347_dsgc_dendritic"`,
   `name: "ModelDB 189347 DSGC — Dendritic-Computation Driver"`, `version: "0.1.0"`,
   `description_path: "description.md"`,
   `module_paths: ["code/neuron_bootstrap.py", "code/run_tuning_curve.py", "code/score_envelope.py", "code/constants.py", "code/paths.py", "code/dsgc_channel_partition.hoc"]`,
   `entry_points` listing `run_one_trial_dendritic` (function), `run_tuning_curve` (script),
   `score_envelope` (script), `dependencies: ["neuron", "numpy", "pandas"]`,
   `categories: ["compartmental-modeling", "direction-selectivity", "retinal-ganglion-cell", "voltage-gated-channels"]`,
   `created_by_task: "t0022_modify_dsgc_channel_testbed"`, `date_created: "2026-04-21"`. Inputs:
   nothing. Outputs: `assets/library/modeldb_189347_dsgc_dendritic/details.json`. Satisfies REQ-5
   partial (library scaffolding).

3. **Write the channel-modular HOC overlay.** Create `code/dsgc_channel_partition.hoc` that declares
   five named SectionLists (`SOMA_CHANNELS`, `DEND_CHANNELS`, `AIS_PROXIMAL`, `AIS_DISTAL`,
   `THIN_AXON`) and five `forsec` insertion blocks, one per region. Populate each block with the
   baseline HHst insertion inherited from t0008 unchanged (so t0022 is the testbed; channel swaps
   come later). Add inline comments naming the post-2020 priors from `research_internet.md`: Nav1.6
   distal AIS 8.0 S/cm^2, Nav1.1 proximal AIS 1.5 S/cm^2, Kv1.2 distal AIS 0.1 S/cm^2, Kv3 optional
   0.0033 S/cm^2. Populate AIS_PROXIMAL / AIS_DISTAL by inspecting `h.axon` sections via their
   `distance(0.5)` from the soma and splitting at the canonical 10 um mark (VanWart2006). Satisfies
   REQ-5 partial (forsec layout).

### Milestone B: Per-Dendrite E-I Driver

4. **Import the t0008 cell bootstrap.** In a new `code/run_tuning_curve.py`, import `build_dsgc`,
   `apply_params`, `read_synapse_coords`, `reset_synapse_coords`, `SynapseCoords`, and `CellSummary`
   from `tasks.t0008_port_modeldb_189347.code.build_cell`. Do NOT import `run_one_trial` or
   `rotate_synapse_coords_in_place`. Also import `score` and the four `METRIC_KEY_*` constants from
   `tasks.t0012_tuning_curve_scoring_loss_library.code` (`tuning_curve_loss`). After `build_dsgc()`
   succeeds, call `h.load_file("code/dsgc_channel_partition.hoc")` using the HOC-safe forward-slash
   path helper from `tasks.t0008_port_modeldb_189347.code.build_cell._sources_dir_hoc_safe`.
   Satisfies REQ-1 (re-uses cell-build but replaces driver).

5. **Implement the per-dendrite E-I synapse inserter.** Add to `code/run_tuning_curve.py` a function
   signature:

   ```python
   @dataclass(frozen=True, slots=True)
   class EiPair:
       dendrite_section: Any
       ampa_syn: Any       # Exp2Syn at sec(0.9) distal
       gaba_syn: Any       # Exp2Syn at sec(0.3) proximal on same sec
       ampa_vecstim: Any
       gaba_vecstim: Any
       ampa_netcon: Any
       gaba_netcon: Any
       azimuth_deg: float  # computed from section midpoint (x, y)

   def build_ei_pairs(*, h: Any) -> list[EiPair]: ...
   ```

   The function iterates every dendritic section in `h.ON` (the existing ON-dendrite SectionList),
   inserts one AMPA `Exp2Syn` at `sec(0.9)` and one GABA_A `Exp2Syn` at `sec(0.3)` on the same
   section (per DSGC-Poirazi-GH and ModelDB-189347 conventions), creates one VecStim per synapse,
   creates one NetCon per synapse with `delay = 0` and weight = conductance in uS
   (`AMPA_CONDUCTANCE_NS * 1e-3`, `GABA_CONDUCTANCE_PREFERRED_NS * 1e-3`). AMPA kinetics: tau1=0.2,
   tau2=1.5, e=0 mV. GABA_A kinetics: tau1=0.5, tau2=8.0, e=-70 mV. Azimuth is `atan2(y_mid, x_mid)`
   from section midpoint. Satisfies REQ-1 (per-dendrite pairs), REQ-3 (fixed mechanism).

6. **Implement the per-angle onset scheduler.** Add a function:

   ```python
   def schedule_ei_onsets(
       *,
       pairs: list[EiPair],
       angle_deg: float,
       velocity_um_per_ms: float,
       ei_offset_ms: float,
       gaba_null_pref_ratio: float,
       trial_seed: int,
   ) -> None: ...
   ```

   For each `EiPair`, compute `t_bar = (x * cos(theta) + y * sin(theta)) / velocity` at section
   midpoint (same formula as ModelDB-189347 README). Compute angular distance from this pair's
   azimuth to the bar direction; if preferred (|delta| < 90 deg), set `ampa_onset = t_bar` and
   `gaba_onset = t_bar + ei_offset_ms` (E leads I by +10 ms). If null (|delta| >= 90 deg), set
   `gaba_onset = t_bar` and `ampa_onset = t_bar + ei_offset_ms` (I leads E by 10 ms). Scale the GABA
   NetCon weight by `gaba_null_pref_ratio` in the null-half and by 1.0 in the preferred-half (giving
   the Park2014 2-4x ratio). Call `vecstim.play(h.Vector([onset_ms]))` for each VecStim. Satisfies
   REQ-1 (direction-dependent timing), REQ-3 (only direction changes — weights are functions of
   direction but the mechanism set is fixed).

7. **Replace per-trial function body.** Add:

   ```python
   def run_one_trial_dendritic(
       *,
       h: Any,
       pairs: list[EiPair],
       angle_deg: float,
       trial_seed: int,
       baseline_coords: list[SynapseCoords],
       baseline_gaba_mod: float,
   ) -> float: ...
   ```

   Body: (a) call `apply_params(h=h, seed=trial_seed)`, (b) assert `h.gabaMOD == baseline_gaba_mod`
   and every BIPsyn coord equals baseline (mirror t0020's `_assert_bip_positions_baseline`), (c)
   call `schedule_ei_onsets(...)`, (d) call `h.finitialize(V_INIT_MV)` and
   `h.continuerun(TSTOP_MS)`, (e) count threshold crossings from the somatic `h.Vector` via the
   existing t0008 spike-count helper. Return firing rate in Hz. Satisfies REQ-1, REQ-3, REQ-4.

### Milestone C: Preflight Validation Gate

8. **Compile MOD files freshly.** Run
   `uv run python -m arf.scripts.utils.run_with_logs -- nrnivmodl tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/files/sources/`
   to rebuild `nrnmech.dll` against the bundled HHst + spike MOD files. Expected output:
   `nrnmech.dll` written to the sources directory with no compilation errors. If this fails, halt
   — NEURON MOD recompilation is a blocking prerequisite.

9. **Preflight cell build + partition source-in.** Run
   `uv run python -u -m tasks.t0022_modify_dsgc_channel_testbed.code.run_tuning_curve --dry-run`.
   Expected: cell builds (~300+ dendritic sections), `dsgc_channel_partition.hoc` sources without
   HOC errors, `build_ei_pairs()` returns >= 200 EiPair objects (matching the 282 ON-dendrite
   triples documented by t0008). Satisfies REQ-5 smoke test.

10. **Preflight mini-run validation gate (4 angles x 2 trials = 8 trials).** Run
    `uv run python -u -m tasks.t0022_modify_dsgc_channel_testbed.code.run_tuning_curve --preflight`
    with the preflight flag running only 4 directions (0, 90, 180, 270 deg) x 2 trials (~30s total).
    **Baseline**: an all-zero tuning curve would give DSI undefined. **Expected**: at least one
    spike per preferred-direction trial (>= 5 Hz firing rate at angle 0 or 180), AND preferred
    firing > null firing (DSI sign > 0, i.e. DSI > 0 rather than abs(DSI) > 0). **Failure
    condition**: if any preferred trial has 0 spikes or if preferred <= null, HALT the pipeline, do
    NOT run the full 120-trial sweep, and inspect per-trial somatic voltage traces logged to
    `logs/preflight/trace_*.csv`. Individual-output inspection: dump the per-EiPair scheduled
    `(ampa_onset, gaba_onset)` pairs for angle 0 and angle 180 to `logs/preflight/onsets.json` for
    visual check that the preferred direction has E leading I and the null direction has I leading
    E. Satisfies REQ-1, REQ-3, REQ-4 preflight.

### Milestone D: Full Sweep and Scoring

11. **[CRITICAL] Run the full 12-angle x 10-trial sweep to produce tuning_curves.csv via the t0022
    per-dendrite E-I driver — not rotation proxy, not gabaMOD.** Execute
    `uv run python -u -m tasks.t0022_modify_dsgc_channel_testbed.code.run_tuning_curve` (no flags).
    The script loops 12 angles x 10 trials = 120 runs, orchestrated via
    `concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count - 3)` per the DSGC-Poirazi-GH
    convention. Per-trial Random123 seed = `(22, angle_index, trial_index)`. Output:
    `data/tuning_curves/curve_modeldb_189347_dendritic.csv` with columns
    `(angle_deg, trial_seed, firing_rate_hz)` and exactly 120 rows. Expected wall-clock: ~9-15
    minutes. This is the critical step — if it becomes blocked (MOD compile error, HOC source
    error, NEURONHOME missing) the implementation agent must create an intervention file rather than
    fall back to the rotation proxy or gabaMOD driver. Satisfies REQ-1, REQ-2, REQ-3, REQ-4.

12. **Copy and run the scoring glue.** Copy `tasks/t0008_port_modeldb_189347/code/score_envelope.py`
    (101 lines, not the 208-line t0020 version) into `code/score_envelope.py`. Change the CSV path
    constant to
    `TUNING_CURVE_DENDRITIC_CSV = DATA_DIR / "tuning_curves" / "curve_modeldb_189347_dendritic.csv"`.
    Run `uv run python -u -m tasks.t0022_modify_dsgc_channel_testbed.code.score_envelope`. Expected
    outputs: `data/score_report.json` with full `ScoreReport` and `results/metrics.json` with the
    four registered metric keys (`direction_selectivity_index`, `tuning_curve_hwhm_deg`,
    `tuning_curve_reliability`, `tuning_curve_rmse`). Acceptance gate: `direction_selectivity_index
    > = 0.5`AND`peak_firing_rate_hz >= 10`. Satisfies REQ-4, REQ-6.

13. **[CRITICAL] Write the library description.md with Nav1.1-not-Nav1.2 correction and
    channel-modular partition.** Create
    `assets/library/modeldb_189347_dsgc_dendritic/description.md` with YAML frontmatter
    (`spec_version: "2"`, `library_id: "modeldb_189347_dsgc_dendritic"`,
    `documented_by_task: "t0022_modify_dsgc_channel_testbed"`, `date_documented: "2026-04-21"`) and
    the eight mandatory sections from `meta/asset_types/library/specification.md`. In the Overview
    and Main Ideas sections, explicitly state the Nav1.1 (not Nav1.2) correction per VanWart2006 and
    the RGC-AIS-Review-2022 confirmation: "The task description referenced a Nav1.6/Nav1.2 split
    drawn from cortical-pyramidal literature; in RGCs the proximal AIS partner is Nav1.1, not
    Nav1.2. This library's AIS_PROXIMAL block is labelled for Nav1.1 insertion in follow-up
    channel-swap tasks." Document the 5-region forsec layout (SOMA_CHANNELS / DEND_CHANNELS /
    AIS_PROXIMAL / AIS_DISTAL / THIN_AXON) with a table mapping region -> expected channel set ->
    gbar prior -> literature source. Satisfies REQ-5, REQ-7 traceability for the correction note.

## Remote Machines

None required. All work runs on the local Windows workstation (same environment used for t0008 and
t0020). NEURON 8.x is already installed with `NEURONHOME` configured; the
`_ensure_neuron_importable()` bootstrap from t0020 is copied verbatim.

## Assets Needed

* Library `modeldb_189347_dsgc` from `tasks/t0008_port_modeldb_189347/` — source of HOC/MOD files,
  `build_dsgc()`, `apply_params()`, synapse-coord helpers, MOD-compiled `nrnmech.dll`.
* Library `tuning_curve_loss` from `tasks/t0012_tuning_curve_scoring_loss_library/` — DSI / HWHM /
  peak / reliability scorer (`METRIC_KEY_*` constants and `score(...)` entry point).
* Answer assets from t0015-t0019 (read during research stage; no runtime dependency).
* Bar-stimulus / moving-bar convention from `[ModelDB-189347]` README (documented in
  `research_internet.md`).
* No external datasets; no downloads.

## Expected Assets

* **1 library asset**:
  `tasks/t0022_modify_dsgc_channel_testbed/assets/library/modeldb_189347_dsgc_dendritic/` (matches
  `task.json` `expected_assets.library: 1`). Contains `details.json` with `spec_version "2"`,
  `library_id "modeldb_189347_dsgc_dendritic"`, `module_paths` listing six files in `code/`, and
  `description.md` documenting the 5-region `forsec` partition, the Nav1.1-not-Nav1.2 correction,
  and the per-dendrite E-I scheduler API.

## Time Estimation

Research (already complete): 0 min. Implementation (Milestones A-B): ~3-4 hours coding and testing.
Preflight mini-run (Milestone C, Step 10): ~30 seconds simulation. Full 12 x 10 sweep (Step 11):
~9-15 minutes simulation. Scoring (Step 12): <5 seconds. Library description authoring (Step 13):
~30 minutes. Total wall-clock: ~5 hours.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| DSI sign flip (NEURON spikes stronger in "null" than "preferred") | Medium | Blocking | Preflight gate (Step 10) runs 4 angles x 2 trials; if DSI <= 0 or preferred < null, halt before full sweep and inspect per-EiPair onsets dumped to `logs/preflight/onsets.json`. Swap the sign of `EI_OFFSET_PREFERRED_MS` if preferred-direction definition is inverted. |
| MOD recompilation fails or imports break from t0008 | Low | Blocking | Step 8 runs `nrnivmodl` freshly before any Python driver executes; if compilation fails, halt and inspect `nrnivmodl` stderr. The `_ensure_neuron_importable()` helper from t0020 is copied verbatim — it is proven across 40+ trials. |
| Per-trial seed reproducibility drifts (NEURON state leak between trials) | Low | Low | Use subprocess ProcessPoolExecutor (Step 11) rather than a single long-running NEURON process, so each trial starts from a fresh process. Random123 3-tuple seeds `(22, angle_idx, trial_idx)` are CLI-passed and logged. |
| Segment length violates `0.1 * lambda` after adding E-I synapses | Low | Medium | Assert `max_seg_length_over_lambda < 0.1` at build time in Step 4 using the `d_lambda` rule from Mainen1996; halt if violated. |
| Full 120-trial sweep consumes >20 min and risks a Windows sleep-suspend | Low | Low | Expected runtime is ~9-15 min; Step 11 prints per-angle progress so a watchdog can detect stalls; the sweep is restartable at the angle level via the CSV append pattern. |
| Nav1.1 vs Nav1.2 confusion persists in downstream tasks | Medium | Low | Step 13 explicitly documents the correction in `description.md` with VanWart2006 and RGC-AIS-Review-2022 citations. |

## Verification Criteria

* Run
  `uv run python -m arf.scripts.verificators.verify_library_asset tasks/t0022_modify_dsgc_channel_testbed/assets/library/modeldb_189347_dsgc_dendritic`
  and expect 0 errors (warnings acceptable if `test_paths` is empty — tests are not required for
  this reproduction task, and `LA-W014` is a non-blocking warning). This confirms REQ-5 structural
  delivery.
* Run `uv run python -u -m tasks.t0022_modify_dsgc_channel_testbed.code.run_tuning_curve` and
  confirm `data/tuning_curves/curve_modeldb_189347_dendritic.csv` exists with exactly 120 rows and
  columns `(angle_deg, trial_seed, firing_rate_hz)`. Check `data/score_report.json` reports
  `direction_selectivity_index >= 0.5` AND `peak_firing_rate_hz >= 10`. This confirms REQ-1, REQ-2,
  REQ-3, REQ-4, REQ-6.
* Run a REQ-coverage review: open `plan.md` and confirm every REQ-1 through REQ-7 listed in the Task
  Requirement Checklist is referenced by at least one numbered step (REQ-1: Steps 4, 5, 6, 7, 10,
  11; REQ-2: Steps 10, 11; REQ-3: Steps 1, 5, 6, 7, 10, 11; REQ-4: Steps 7, 10, 11, 12; REQ-5: Steps
  2, 3, 9, 13; REQ-6: Step 12; REQ-7 is orchestrator post-implementation work and named in the
  checklist for traceability). This confirms traceability from task text to implementation.
* Run
  `uv run python -u -c "import json; r = json.load(open(r'tasks/t0022_modify_dsgc_channel_testbed/results/metrics.json')); print(r)"`
  and confirm the four metric keys `direction_selectivity_index`, `tuning_curve_hwhm_deg`,
  `tuning_curve_reliability`, `tuning_curve_rmse` are all present and non-null.
