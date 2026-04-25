---
spec_version: "2"
task_id: "t0049_seclamp_cond_remeasure"
date_completed: "2026-04-24"
status: "complete"
---
# Plan: Re-measure Fig 3A-E Conductances Under Somatic SEClamp on the Deposited DSGC

## Objective

Re-measure per-channel synaptic conductance (NMDA, AMPA, GABA) on the deposited Poleg-Polsky 2016
DSGC under a somatic single-electrode voltage clamp (NEURON `SEClamp`) at -65 mV, then compare the
re-measured values to (a) the paper's Fig 3A-E targets and (b) t0047's per-synapse-direct
conductances. The goal is to adjudicate whether the t0047 amplitude mismatch (per-synapse-summed
conductances 6-9x over the paper's Fig 3A-E values) is a measurement-modality artefact (paper
reports somatic-clamp values, t0047 measured per-synapse `_ref_g`) or a real parameter discrepancy
in the deposited model. Done means: 32 simulated trials are complete; per-channel somatic-equivalent
conductance is reported with mean and SD; comparison table covers paper vs SEClamp this task vs
t0047 per-synapse-summed vs t0047 per-synapse-mean across NMDA/AMPA/GABA at PD and ND; verdict on
H0/H1/H2 is rendered per channel x direction; one answer asset and two PNG charts are committed.

## Task Requirement Checklist

The operative request from `task.json` and `task_description.md`:

> **Name**: Re-measure Fig 3A-E conductances under somatic SEClamp on the deposited DSGC
>
> **Short description**: Add a SEClamp at soma of deposited DSGC and re-measure per-channel synaptic
> conductance under voltage clamp; compare to t0047 per-synapse direct and paper Fig 3A-E.
>
> Long-description (excerpts from `task_description.md`):
>
> * Add a NEURON SEClamp at the soma of the deposited DSGC, voltage-clamp it at -65 mV, and record
>   the total synaptic current per channel as the wave stimulus sweeps. The current divided by the
>   driving force `(V_clamp - E_rev)` gives the somatic-voltage-clamp-equivalent conductance per
>   channel.
> * Re-use the existing `modeldb_189347_dsgc_exact` library produced by t0046. No code copy or fork.
> * SEClamp parameters: `dur1 = h.tstop`, `amp1 = -65 mV`, `rs = 0.001 MOhm`. Record `clamp._ref_i`
>   sub-sampled at dt = 0.25 ms.
> * Run four channel-isolation trial types per direction: full circuit (all synapses on), AMPA-only
>   (`b2gnmda = 0`, `gabaMOD = 0`), NMDA-only (`b2gampa = 0`, `gabaMOD = 0`), GABA-only
>   (`b2gnmda = 0`, `b2gampa = 0`).
> * Run at the single condition gNMDA = 0.5 nS, exptype = 1 (control), 4 trials per direction per
>   channel-isolation. Total = 2 directions x 4 channel-isolations x 4 trials = 32 trials.
> * Compute `g_soma_eq = mean_peak_i_channel / (V_clamp - E_rev)` with `V_clamp = -65 mV`,
>   `E_rev_NMDA = E_rev_AMPA = 0 mV`, `E_rev_GABA = -60 mV` (driving forces -65, -65, -5 mV).
> * Compare per-channel SEClamp conductance to t0047's per-synapse-summed conductance and to paper
>   Fig 3A-E targets. Verdict on H0 / H1 / H2.
> * Produce one answer asset `seclamp-conductance-remeasurement-fig3` and two PNGs:
>   `seclamp_conductance_pd_vs_nd.png` and `seclamp_vs_per_syn_direct_modality_comparison.png`.
> * H1: SEClamp values within +/- 25% of paper. H2: closer than t0047 but outside +/- 25%. H0:
>   essentially equal to t0047's per-synapse-summed values.

The concrete requirements decomposed:

* **REQ-1**: Insert a NEURON `SEClamp` at `h.RGC.soma(0.5)` with `dur1 = h.tstop`, `amp1 = -65.0`,
  `rs = 0.001`, AFTER `placeBIP()` so it does not interfere with synapse placement. Record
  `clamp._ref_i` via `h.Vector().record(clamp._ref_i, DT_RECORD_MS=0.25 ms)`. Also record
  `h.RGC.soma(0.5)._ref_v` to verify the clamp holds within +/- 0.5 mV of -65 mV. Satisfied by: Step
  4 (`code/run_seclamp.py` SEClamp insertion path). Evidence: clamp soma-voltage trace SD < 0.5 mV
  asserted at runtime, recorded in implementation logs.

* **REQ-2**: Implement four channel-isolation trial types per direction by writing HOC globals AFTER
  `simplerun()` returns (full / AMPA-only / NMDA-only / GABA-only with the override pairs in the
  task description), then re-`update()`, re-`placeBIP()`, attach the SEClamp, and
  `finitialize(V_INIT_MV) -> continuerun(TSTOP_MS)`. Satisfied by: Step 4 (`code/run_seclamp.py`
  channel-isolation override branch). Evidence: per-trial CSV rows tagged with
  `channel_on in {all, ampa_only, nmda_only, gaba_only}`.

* **REQ-3**: Run the full sweep: 2 directions (PD, ND) x 4 channel-isolations x 4 trials at gNMDA =
  0.5 nS, exptype = CONTROL = 1. Total 32 trials. Record per-trial peak SEClamp current, baseline
  mean, and the soma-voltage clamp-quality SD. Write to a per-trial CSV. Satisfied by: Step 5
  (`code/run_seclamp_sweep.py`). Evidence: `results/data/seclamp_trials.csv` with 32 rows.

* **REQ-4**: Compute per-channel somatic-equivalent conductance using
  `g_soma_eq_nS = abs(i_peak_pA) / abs(V_CLAMP_MV - E_REV_MV)` with explicit per-channel reversal
  potentials (NMDA 0 mV, AMPA 0 mV, GABA -60 mV; clamp -65 mV; driving forces -65, -65, -5 mV). Sign
  convention: SEClamp `_ref_i` is current INTO clamp from cell; inward synaptic current at -65 mV
  clamp is sourced by clamp (negative `_ref_i`); we use `abs()` so `g` is positive. Satisfied by:
  Step 6 (`code/compute_metrics.py`). Evidence: per-channel `g_*_ns` columns in the aggregated CSV
  and the per-channel x per-direction values in `metrics.json` variants.

* **REQ-5**: Aggregate per-trial conductances to mean +/- SD per channel (NMDA, AMPA, GABA) per
  direction (PD, ND) and write `results/metrics.json` in the explicit multi-variant format with one
  variant per channel x direction = 6 variants minimum. Each variant carries a
  `direction_selectivity_index` metric (SEClamp conductance DSI per channel) computed from the per-
  channel summed currents. Satisfied by: Step 6 (`code/compute_metrics.py`). Evidence:
  `results/metrics.json` validates with `verify_task_metrics.py`.

* **REQ-6**: Compute and report the per-channel comparison table containing four columns: (a) paper
  Fig 3A-E target (NMDA PD/ND ~7/~5 nS, AMPA PD/ND ~3.5/~3.5 nS, GABA PD/ND ~12.5/~30 nS); (b) this
  task's SEClamp summed conductance; (c) t0047's per-synapse-summed conductance from t0047's
  `results_summary.md`; (d) t0047's per-synapse-mean (= summed / 282) for completeness. Satisfied
  by: Step 6 plus Step 8 (answer-asset writing). Evidence:
  `results/data/seclamp_comparison_table.csv` and the table inside
  `assets/answer/... /full_answer.md`.

* **REQ-7**: Render two PNG charts in `results/images/` per the task description:
  * `seclamp_conductance_pd_vs_nd.png` — bar chart, 3 channels x 2 directions, paper target +
    SEClamp this task side-by-side per channel x direction.
  * `seclamp_vs_per_syn_direct_modality_comparison.png` — bar chart comparing the two modalities
    (per-synapse-direct from t0047 vs SEClamp this task) at gNMDA = 0.5. Satisfied by: Step 7
    (`code/render_figures.py`). Evidence: both PNG files exist and are embedded in
    `results/results_detailed.md` (orchestrator step) and the answer asset.

* **REQ-8**: Render the H0 / H1 / H2 verdict per channel x direction (6 cells). H1 if all 6 cells
  fall within +/- 25% of paper. H2 if some but not all. H0 if SEClamp values are within +/- 10% of
  t0047 per-synapse-summed (modality irrelevant). The verdict is computed in Step 6 and rendered in
  the answer asset. Satisfied by: Step 6 (verdict logic) and Step 8 (answer-asset rendering).
  Evidence: verdict column in `seclamp_comparison_table.csv` and the verdict block in
  `assets/answer/seclamp-conductance-remeasurement-fig3/full_answer.md`.

* **REQ-9**: Produce one answer asset `assets/answer/seclamp-conductance-remeasurement-fig3/` per
  `meta/asset_types/answer/ specification.md` v2 with `details.json`, `short_answer.md`,
  `full_answer.md`. The `full_answer.md` must contain: question framing, per-channel comparison
  table (paper vs SEClamp this task vs per-syn-summed t0047 vs per-syn-mean t0047), H0/H1/H2
  verdict, SEClamp methodology notes (clamp parameters, channel-isolation protocol, sign
  convention), synthesis paragraph. Satisfied by: Step 8 (answer-asset writing). Evidence:
  `verify_answer_asset` passes; folder structure matches v2 spec.

* **REQ-10**: Re-use the `modeldb_189347_dsgc_exact` library by direct cross-task import (no code
  copy or fork of t0046 simulation code). Use the override-and-rerun pattern from
  `tasks/t0046_reproduce_poleg_polsky_2016_exact/code/run_simplerun.py:135-151` as the canonical
  template for the channel-isolation re-run. Satisfied by: Step 4 (`code/run_seclamp.py` imports
  from `tasks.t0046_..._exact.code.*`). Evidence: top of `code/run_seclamp.py` imports
  `_ensure_cell`, `Direction`, `ExperimentType`, `V_INIT_MV`, `TSTOP_MS`, `B2GNMDA_CODE`,
  `E_SACINHIB_MV` directly; no copy of the simulation driver lives in this task folder.

* **REQ-11**: Centralise paths in `code/paths.py` and constants in `code/constants.py` per project
  Python style guide. Add a runtime assertion that re-affirms `E_SACINHIB_MV` against t0046's
  constant (style-guide pattern from t0047). Satisfied by: Step 1 (paths) and Step 2 (constants).
  Evidence: both files exist and import-time assertion passes.

* **REQ-12**: Ensure verificators pass. `verify_task_file.py`, `verify_plan.py`,
  `verify_answer_asset.py`, `verify_task_metrics.py`, `verify_task_results.py` must all return zero
  errors at task completion. Verification is the responsibility of the orchestrator's reporting step
  but the implementation must produce artefacts that satisfy all verificators. Satisfied by: Steps
  1-8 collectively producing standards-compliant outputs. Evidence: orchestrator reporting log
  records zero errors.

## Approach

The technical approach follows directly from the research-code findings
(`research/research_code. md`) and t0046's library design.

**Key research findings embedded here**:

* **The cell build is cached and the wall-clock bottleneck**: `_ensure_cell()` in
  `tasks.t0046_..._exact.code.run_simplerun` uses a module-global `_CELL_STATE` dict, so the DSGC is
  built exactly once per Python process (30-60 s) and trials are 5-10 s thereafter. This means the
  SEClamp object is inserted **once after the first build** and persists across all 32 trials;
  recorder vectors are reset between trials via `vec.resize(0)`.

* **`simplerun()` rebinds globals every call** (lines 100-138 of `run_simplerun.py`). It writes
  `b2gnmda = 0.5 * nmdaOn` and `achMOD = 0.33` unconditionally, clobbering any pre-call Python
  override. The only correct way to apply non-canonical conductance values is the override-and-rerun
  pattern (lines 135-151): after `simplerun()` returns, write the desired global values, call
  `h("update()")` and `h("placeBIP()")`, attach fresh recorder vectors, `h.finitialize(V_INIT_MV)`,
  `h.continuerun(TSTOP_MS)`. The SEClamp insertion path uses the same pattern; the SEClamp object is
  attached between `placeBIP()` and `finitialize`.

* **bipolarNMDA dual-component synapse independence**: The deposited `bipolarNMDA.mod` exposes
  separate `gAMPA` and `gNMDA` state variables driven by the same vesicle release. Setting
  `b2gampa = 0` zeroes only the AMPA per-vesicle conductance while NMDA continues to release (and
  vice versa). t0047 confirmed this independence by recording `_ref_gAMPA` and `_ref_gNMDA`
  independently. The `gabaMOD` global multiplies the SAC inhibitory stimulus amplitude in
  `mulnoise.fill(VampT*gabaMOD,...)`, so `gabaMOD = 0` zeroes the inhibitory wave drive at the
  presynaptic level (no GABA release). These three knobs (`b2gampa`, `b2gnmda`, `gabaMOD`) are
  sufficient and independent for the four channel-isolation trial types.

* **SEClamp insertion idiom**: `clamp = h.SEClamp(h.RGC.soma(0.5))`, `clamp.dur1 = h.tstop`,
  `clamp.amp1 = -65.0`, `clamp.rs = 0.001`. Record `clamp._ref_i` via `h.Vector().record(...)`.
  `h.RGC.soma(0.5)` is the same handle t0046 already uses on line 115 of `run_simplerun.py`; no
  additional HOC plumbing is required.

* **Per-channel conductance formula**: `g_nS(t) = abs(i_clamp_nA(t) * 1000) / abs(V_clamp - E_rev)`.
  Driving forces with `V_clamp = -65 mV`: NMDA (E_rev=0) -65 mV; AMPA (E_rev=0) -65 mV; GABA SAC
  inhibitory (E_rev=-60 from `dsgc_model_exact.hoc:80`) -5 mV. The GABA conversion factor is 13x
  larger than NMDA/AMPA — the wrapper must compute conductance with explicit per-channel reversal
  potentials, never a single shared constant. We record the soma voltage trace alongside the clamp
  current to assert the clamp holds within +/- 0.5 mV of -65 mV.

* **t0047 baseline values** (per-synapse-summed conductances at gNMDA = 0.5 nS, from
  `tasks/t0047_validate_pp16_fig3_cond_noise/results/results_summary.md` lines 15-22):

| Channel | PD (nS, summed) | ND (nS, summed) | Paper target PD / ND (nS) |
| --- | --- | --- | --- |
| NMDA | 69.55 +/- 5.86 | 33.98 +/- 1.83 | ~7.0 / ~5.0 |
| AMPA | 10.92 +/- 0.37 | 10.77 +/- 0.60 | ~3.5 / ~3.5 |
| GABA | 106.13 +/- 5.77 | 215.57 +/- 2.72 | ~12.5 / ~30.0 |

These values are hard-coded into `code/constants.py` so the comparison table renders without reading
t0047's results files at runtime.

**Cross-task imports (no copy of t0046 simulation code)**:

* `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun import _ensure_cell, get_dt_ms, get_tstop_ms`
* `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.constants import Direction, ExperimentType, V_INIT_MV, TSTOP_MS, DT_MS, B2GNMDA_CODE, E_SACINHIB_MV`
* `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.build_cell import reset_globals_to_canonical, assert_bip_positions_baseline`
* `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.neuron_bootstrap import ensure_neuron_importable`

**Code copied (with attribution)**:

* `code/dsi.py` — copied from `tasks/t0047_validate_pp16_fig3_cond_noise/code/dsi.py` (~30 lines).
  t0047 is **not** a registered library so the cross-task copy rule applies. The DSI helper is used
  to compute SEClamp conductance DSI per channel for the metrics file.
* The override-and-rerun pattern from `tasks/t0046_..._exact/code/run_simplerun.py:135-151` (~20
  lines) is the template for the channel-isolation re-run inside `code/run_seclamp.py`. It is
  re-implemented (not literally copied) because the SEClamp insertion is interleaved with the
  override block.
* The recorder-management pattern from `tasks/t0047_..._cond_noise/code/run_with_conductances.py`
  (~50 lines) is the template for `recorder.resize(0)` per-trial reset. Re-implemented for the
  SEClamp single-vector recorder.

**Alternatives considered**:

1. **Use `run_one_trial` directly with a SEClamp set up before the call**: rejected because
   `simplerun()` would internally trigger the synaptic placement, run the simulation, and return
   without giving us a hook to insert the SEClamp at the right point. The SEClamp must be active
   during the simulation; it cannot be retrofitted after the fact. The override-and-rerun pattern is
   the only way to interpose the SEClamp insertion between `placeBIP()` and `finitialize`.

2. **Simulate AMPA-only / NMDA-only / GABA-only by recording per-synapse currents and post-hoc
   summing** (the t0047 approach): rejected because that is exactly the modality this task is
   replacing. The point of this task is the somatic-clamp measurement, which is fundamentally
   different from per-synapse currents (cable attenuation collapses to a smaller value at the soma).

3. **Fork `bipolarNMDA.mod` to add per-component i-clamp recording**: rejected because the task
   description explicitly forbids modifying the deposited library; channel isolation via HOC global
   overrides is sufficient given the dual-component synapse design (verified in research- code
   finding above).

4. **Run only one trial per condition**: rejected because the `flickerVAR = 0` deterministic seed
   does not vary trial-to-trial, but `gabaMOD = 0` and `b2gampa = 0` overrides leave the trial
   determinism intact, so 4 trials per condition are conservative (likely zero variance, but
   confirms determinism). The 32-trial cost is ~5 minutes on local CPU which is negligible.

**Task type**: `experiment-run` (declared in `task.json`). The Planning Guidelines from
`meta/task_types/experiment-run/instruction.md` were consulted: hypothesis is explicit (H1/H2/H0);
independent variables (channel-isolation, direction, trial seed) are specified; dependent variable
(per-channel somatic-equivalent conductance) is specified; baselines (paper Fig 3A-E values, t0047
per-synapse-direct values) are specified; multi-variant `metrics.json` is required (6 variants
minimum: per channel x per direction). No fine-tuning or paid inference, so `efficiency_*` and
`cost_*` metrics do not apply.

**Random seeds**: deterministic per-trial seeds offset by 10000 from t0047 / t0048 to avoid
collisions. PD seeds: `[20000, 20001, 20002, 20003]` (full circuit), `[20100, 20101, 20102, 20103]`
(AMPA-only), `[20200, 20201, 20202, 20203]` (NMDA-only), `[20300, 20301, 20302, 20303]` (GABA-only).
ND uses `[21000+...]`, etc. Concretely:
`seed = 20000 + 1000*direction_idx + 100* channel_idx + trial_idx`.

## Cost Estimation

Total estimated cost: **$0.00 USD**.

Breakdown:

* **Local CPU compute**: $0.00. All simulations run on the developer's local Windows workstation
  using the NEURON 8.2.7 toolchain installed by t0007. No GPU, no remote machine.
* **Paid APIs**: $0.00. No LLM inference, no external service calls.
* **Storage / bandwidth**: $0.00. All inputs are repository-local; outputs are local files.

Project budget: $1.00 USD total / $1.00 per-task default (`project/budget.json`). Spent so far:
$0.00. This task adds $0.00. Remaining budget after this task: $1.00 USD. No risk of budget overrun;
no cost cap is needed.

## Step by Step

### Milestone A: Scaffolding (Steps 1-3)

1. **[CRITICAL] Create `code/paths.py`** with the centralised path constants for this task. Anchor
   on `Path(__file__).resolve().parent.parent` (same pattern as t0047). Define: `TASK_ROOT`,
   `RESULTS_DIR`, `RESULTS_DATA_DIR`, `RESULTS_IMAGES_DIR`, `ASSETS_DIR`,
   `ASSETS_ANSWER_DIR = ASSETS_DIR / "answer" / "seclamp-conductance-remeasurement-fig3"`,
   `LOGS_DIR`, `SECLAMP_TRIALS_CSV = RESULTS_DATA_DIR / "seclamp_trials.csv"`,
   `SECLAMP_COMPARISON_CSV = RESULTS_DATA_DIR / "seclamp_comparison_table.csv"`,
   `METRICS_JSON = RESULTS_DIR / "metrics.json"`,
   `SECLAMP_PD_VS_ND_PNG = RESULTS_IMAGES_DIR / "seclamp_conductance_pd_vs_nd.png"`,
   `SECLAMP_MODALITY_PNG = RESULTS_IMAGES_DIR / "seclamp_vs_per_syn_direct_modality_comparison .png"`.
   Also create `RESULTS_DATA_DIR` and `RESULTS_IMAGES_DIR` at module-load time via
   `dir.mkdir(parents=True, exist_ok=True)` if they do not exist. Satisfies REQ-11.

2. **[CRITICAL] Create `code/constants.py`** with all task constants. Include:
   * Clamp params: `V_CLAMP_MV: float = -65.0`, `AMP1: float = -65.0`, `RS_MOHM: float = 0.001`,
     `DT_RECORD_MS: float = 0.25`.
   * Reversal potentials and runtime assertion against t0046's `E_SACINHIB_MV`:
     `E_NMDA_MV: float = 0.0`, `E_AMPA_MV: float = 0.0`, `E_GABA_MV: float = -60.0`. Assert
     `E_GABA_MV == _T0046_E_SACINHIB_MV` (import the t0046 value as `_T0046_E_SACINHIB_MV`).
   * Paper Fig 3A-E targets: `NMDA_PD_TARGET_NS = 7.0`, `NMDA_ND_TARGET_NS = 5.0`,
     `AMPA_PD_TARGET_NS = 3.5`, `AMPA_ND_TARGET_NS = 3.5`, `GABA_PD_TARGET_NS = 12.5`,
     `GABA_ND_TARGET_NS = 30.0`. Tolerances: `CONDUCTANCE_TOLERANCE_FRAC = 0.25`,
     `H0_TOLERANCE_FRAC = 0.10`.
   * t0047 per-synapse-summed baseline values (hard-coded from t0047's published summary):
     `T0047_NMDA_PD_NS = 69.55`, `T0047_NMDA_ND_NS = 33.98`, `T0047_AMPA_PD_NS = 10.92`,
     `T0047_AMPA_ND_NS = 10.77`, `T0047_GABA_PD_NS = 106.13`, `T0047_GABA_ND_NS = 215.57`. Number of
     synapses = 282 for the per-syn-mean derivation.
   * Channel isolation enum:
     ```python
     class ChannelIsolation(Enum):
         ALL = "all"
         AMPA_ONLY = "ampa_only"
         NMDA_ONLY = "nmda_only"
         GABA_ONLY = "gaba_only"
     ```
   * Trial seeds: `BASE_SEED = 20000`, `TRIALS_PER_CONDITION = 4`, `SEED_OFFSET_DIRECTION = 1000`,
     `SEED_OFFSET_CHANNEL = 100`. Also `B2GNMDA_NS = 0.5` (single-condition value).
   * CSV column-name constants and clamp-quality threshold:
     `CLAMP_VOLTAGE_TOLERANCE_MV: float = 0.5` (max SD allowed in soma trace during clamped run).
   * `METRIC_KEY_DSI = "direction_selectivity_index"` (registered metric). Satisfies REQ-11.

3. **Copy `code/dsi.py` from t0047 with attribution**. Copy
   `tasks/t0047_validate_pp16_fig3_cond_noise/code/dsi.py` verbatim into
   `tasks/t0049_seclamp_cond_remeasure/code/dsi.py`. Update the source-comment at the top to record
   the copy. The function `compute_dsi_pd_nd(*, pd_values, nd_values)` is the only API used here.
   Satisfies REQ-5 (DSI computation).

### Milestone B: SEClamp wrapper (Step 4)

4. **[CRITICAL] Create `code/run_seclamp.py`** — the SEClamp simulation wrapper. This module
   encapsulates the channel-isolation override + SEClamp insertion + simulation re-run.
   * **Imports**:
     `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun import _ensure_cell`,
     `from tasks.t0046_..._exact.code.constants import Direction, ExperimentType, V_INIT_MV, TSTOP_MS, B2GNMDA_CODE`,
     `from tasks.t0046_..._exact.code.build_cell import reset_globals_to_canonical, assert_bip_positions_baseline`,
     plus task-local
     `from tasks.t0049_seclamp_cond_remeasure.code.constants import ChannelIsolation, V_CLAMP_MV, RS_MOHM, DT_RECORD_MS, CLAMP_VOLTAGE_TOLERANCE_MV, B2GNMDA_NS`.
   * **Dataclass**: `@dataclass(frozen=True, slots=True) class SeclampTrialResult` with fields
     `direction: Direction`, `channel_on: ChannelIsolation`, `trial_seed: int`, `b2gnmda_ns: float`,
     `peak_i_pa: float`, `baseline_i_pa: float`, `peak_i_minus_baseline_pa: float`,
     `clamp_v_sd_mv: float` (clamp-quality assertion).
   * **Function
     `run_seclamp_trial(*, direction: Direction, channel_on: ChannelIsolation, trial_seed: int) -> SeclampTrialResult`**:
     1. Call `h, _ = _ensure_cell()` — builds the DSGC if not yet built. The cell handle is
        cached.
     2. `reset_globals_to_canonical(h=h)`. Set `h.flickerVAR = 0.0`, `h.stimnoiseVAR = 0.0`,
        `h.b2gnmda = B2GNMDA_NS`, `h.seed2 = int(trial_seed)`, `h.SpikesOn = 0`, `h.nmdaOn = 1`.
     3. Run the canonical full trial: `h.simplerun(int(ExperimentType.CONTROL), int(direction))`.
        This builds the synaptic input, propagates a wave, runs the simulation. We do this even when
        `channel_on != ALL` because `simplerun()` is the only way to trigger `placeBIP()` with the
        deposited stimulus generator.
     4. Apply channel-isolation overrides (no-op for `ALL`):
        * `AMPA_ONLY`: `h.b2gnmda = 0.0`; `h.gabaMOD = 0.0`.
        * `NMDA_ONLY`: `h.b2gampa = 0.0`; `h.gabaMOD = 0.0`.
        * `GABA_ONLY`: `h.b2gnmda = 0.0`; `h.b2gampa = 0.0`.
     5. Re-update and re-place: `h("update()")`, `h("placeBIP()")` per the t0046 override-and- rerun
        pattern (Lesson Learned 5 from research-code).
     6. Insert the SEClamp at the soma:
        ```python
        clamp = h.SEClamp(h.RGC.soma(0.5))
        clamp.dur1 = TSTOP_MS
        clamp.amp1 = V_CLAMP_MV  # -65.0
        clamp.rs = RS_MOHM  # 0.001
        ```
        Keep `clamp` alive for the duration of the call (Python reference required).
     7. Attach fresh recorder vectors:
        ```python
        i_rec = h.Vector(); i_rec.record(clamp._ref_i, DT_RECORD_MS)
        v_rec = h.Vector(); v_rec.record(h.RGC.soma(0.5)._ref_v, DT_RECORD_MS)
        t_rec = h.Vector(); t_rec.record(h._ref_t, DT_RECORD_MS)
        ```
     8. `h.finitialize(V_INIT_MV)`, `h.continuerun(TSTOP_MS)`.
     9. Convert `i_rec` (nA) to `i_arr_pa` (pA) by `i_arr * 1000.0`.
     10. Compute `baseline_i_pa = mean(i_arr_pa[t_arr < PSP_BASELINE_MS=100.0])`.
     11. Compute `peak_i_pa = max(abs(i_arr_pa - baseline_i_pa))` over the post-stimulus window.
         Sign convention: SEClamp `_ref_i` is current INTO clamp from cell; inward synaptic current
         at -65 mV clamp is sourced by the clamp (negative `_ref_i`); we use `abs()`.
     12. Compute clamp-quality: `clamp_v_sd_mv = std(v_arr_mv)`. Assert
         `clamp_v_sd_mv < CLAMP_VOLTAGE_TOLERANCE_MV` (0.5 mV) — fail loudly if the clamp is
         drifting. Print a warning + log to step log if exceeded.
     13. `assert_bip_positions_baseline(h=h, baseline=...)` — sanity check that synapse positions
         did not drift mid-sweep.
     14. Return `SeclampTrialResult(...)`.
   * **Note**: the SEClamp object is currently created fresh every trial; this is correct because
     the channel-isolation overrides demand a re-update + re-placeBIP, which means the existing
     clamp would also need re-attachment. Cell build and synapse positions are still cached across
     trials; only the clamp + recorders are recreated, which is cheap (~10 ms). Satisfies REQ-1,
     REQ-2, REQ-10.

### Milestone C: Sweep driver and metrics (Steps 5-6)

5. **[CRITICAL] Create `code/run_seclamp_sweep.py`** — the 32-trial sweep driver and per-trial CSV
   writer.
   * **Imports**:
     `from tasks.t0049_seclamp_cond_remeasure.code.run_seclamp import run_seclamp_trial, SeclampTrialResult`,
     `from tasks.t0049_..._cond_remeasure.code.constants import ChannelIsolation, BASE_SEED, TRIALS_PER_CONDITION, SEED_OFFSET_DIRECTION, SEED_OFFSET_CHANNEL, B2GNMDA_NS`,
     `from tasks.t0046_..._exact.code.constants import Direction`,
     `from tasks.t0049_..._cond_remeasure.code.paths import SECLAMP_TRIALS_CSV`.
   * **Sweep loop**: nested
     `for direction_idx, direction in enumerate([Direction.PD, Direction.ND])`,
     `for channel_idx, channel in enumerate([ChannelIsolation.ALL, ChannelIsolation.AMPA_ONLY, ChannelIsolation.NMDA_ONLY, ChannelIsolation.GABA_ONLY])`,
     `for trial_idx in range(TRIALS_PER_CONDITION)`. Compute `seed = BASE_SEED +
     SEED_OFFSET_DIRECTION * direction_idx + SEED_OFFSET_CHANNEL * channel_idx
     + trial_idx`. Call `run_seclamp_trial(...)` and append to a list.
   * **Validation gate (small initial sub-sweep)**: BEFORE the full 32-trial sweep, run only the
     first 2 trials (PD, full circuit, seeds 20000/20001) and confirm:
     * `peak_i_minus_baseline_pa > 0` (non-zero current — pipeline is alive).
     * `clamp_v_sd_mv < 0.5` (clamp holds — REQ-1).
     * Convert peak current to NMDA-channel conductance: `g = peak_i_pa / 65.0` (pA/mV = pA/mV; with
       1 mV-1 nS unit identity at 1 nA/mV, that is `g_nS = peak_i_pa / 65.0 / 1000`). Confirm the
       result is in the range [0.5, 200] nS — sanity check that the SEClamp current is in a
       plausible range (paper expects ~7 nS; t0047 saw ~70 nS; both are within this band). If
       `g_nS < 0.1` or `g_nS > 1000`: STOP and inspect individual outputs (read the full i_rec trace
       and verify the SEClamp is connected to the right segment). Do NOT proceed to the full sweep
       until the small validation passes.
   * **Output CSV**: write `SECLAMP_TRIALS_CSV` with columns: `direction`, `channel_on`,
     `trial_seed`, `b2gnmda_ns`, `peak_i_pa`, `baseline_i_pa`, `peak_i_minus_baseline_pa`,
     `clamp_v_sd_mv`. Use `pandas.DataFrame.to_csv(index=False)`.
   * **Expected wall-clock**: ~60 s cell build + 32 trials x 5 s = ~5 minutes total.
   * **Idempotence**: the sweep is fully deterministic (seeded). Re-running overwrites the CSV.
     Satisfies REQ-3.

6. **[CRITICAL] Create `code/compute_metrics.py`** — aggregate per-trial CSV into the comparison
   table and write `metrics.json`.
   * **Imports**: `import pandas as pd`,
     `from tasks.t0049_..._cond_remeasure.code.paths import SECLAMP_TRIALS_CSV, SECLAMP_COMPARISON_CSV, METRICS_JSON`,
     `from tasks.t0049_..._cond_remeasure.code.constants import V_CLAMP_MV, E_NMDA_MV, E_AMPA_MV, E_GABA_MV, NMDA_PD_TARGET_NS, ..., T0047_NMDA_PD_NS, ..., CONDUCTANCE_TOLERANCE_FRAC, H0_TOLERANCE_FRAC, METRIC_KEY_DSI, ChannelIsolation`,
     `from tasks.t0049_..._cond_remeasure.code.dsi import compute_dsi_pd_nd`.
   * **Channel -> reversal-potential mapping**:
     ```python
     channel_to_e_rev: dict[ChannelIsolation, float] = {
         ChannelIsolation.AMPA_ONLY: E_AMPA_MV,
         ChannelIsolation.NMDA_ONLY: E_NMDA_MV,
         ChannelIsolation.GABA_ONLY: E_GABA_MV,
     }
     ```
   * **Conductance derivation per trial**:
     `g_nS = peak_i_minus_baseline_pa / abs(V_CLAMP_MV - e_rev)`. For NMDA/AMPA the divisor is 65;
     for GABA it is 5.
   * **Aggregation**: group by `(direction, channel_on)`; compute `g_mean_ns`, `g_sd_ns`, `n` per
     group. Six groups (3 channels x 2 directions). Drop the `ALL`-channel rows from the comparison
     table — they are kept in the per-trial CSV for the optional cross-check (sum of per-channel
     should approximately equal `ALL`).
   * **Verdict per channel x direction**:
     * `paper_target = {NMDA_PD: 7.0, ...}[channel, direction]`.
     * `t0047_summed = {NMDA_PD: 69.55, ...}[channel, direction]`.
     * `delta_paper_frac = abs(g_mean - paper_target) / paper_target`.
     * `delta_t0047_frac = abs(g_mean - t0047_summed) / t0047_summed`.
     * `verdict = "H1" if delta_paper_frac <= 0.25 else ("H0" if delta_t0047_frac <= 0.10 else "H2")`.
   * **Comparison-table CSV**: write `SECLAMP_COMPARISON_CSV` with columns: `channel`, `direction`,
     `g_seclamp_mean_ns`, `g_seclamp_sd_ns`, `n`, `paper_target_ns`, `t0047_summed_ns`,
     `t0047_per_syn_mean_ns` (= summed / 282), `delta_paper_frac`, `delta_t0047_frac`, `verdict`.
   * **`metrics.json`**: write the explicit multi-variant format. Six variants, one per channel x
     direction, plus three roll-up DSI variants per channel:
     ```json
     {
       "variants": [
         {
           "variant_id": "nmda_pd",
           "label": "NMDA, preferred direction (SEClamp at -65 mV)",
           "dimensions": {
             "channel": "nmda", "direction": "PD",
             "v_clamp_mv": -65.0, "b2gnmda_ns": 0.5
           },
           "metrics": {}
         },
         ... (5 more for ampa_pd/nd, nmda_nd, gaba_pd/nd) ...
         {
           "variant_id": "nmda_dsi",
           "label": "NMDA conductance DSI (SEClamp)",
           "dimensions": {"channel": "nmda", "metric_kind": "conductance_dsi"},
           "metrics": {"direction_selectivity_index": <value>}
         },
         ... (2 more for ampa_dsi, gaba_dsi) ...
       ]
     }
     ```
     The 6 channel x direction variants carry empty `metrics: {}` because the conductance amplitude
     is not a registered metric (the registered `direction_selectivity_index` lives in the 3 DSI
     roll-up variants). Conductance values are reported in the per-channel comparison CSV
     `seclamp_comparison_table.csv` and surfaced into the answer asset. The DSI roll-ups use
     `compute_dsi_pd_nd(pd_values=[... trials], nd_values=[...trials])` per channel; this is the
     only registered metric this task measures (HWHM / RMSE / reliability do not apply because there
     is no tuning curve).
   * **Validation gate**: assert no NaNs in the comparison table; assert `n == 4` per group; assert
     at least one verdict is rendered for each of the 6 cells. Satisfies REQ-4, REQ-5, REQ-6, REQ-8.

### Milestone D: Figures and answer asset (Steps 7-8)

7. **Create `code/render_figures.py`** — generate the two PNG charts.
   * **Imports**: `import matplotlib.pyplot as plt`, `import pandas as pd`, `import numpy as np`,
     `from tasks.t0049_..._cond_remeasure.code.paths import SECLAMP_COMPARISON_CSV, SECLAMP_PD_VS_ND_PNG, SECLAMP_MODALITY_PNG`.
   * **Chart 1 `seclamp_conductance_pd_vs_nd.png`**: grouped bar chart, x-axis = 6 cells (NMDA_PD,
     NMDA_ND, AMPA_PD, AMPA_ND, GABA_PD, GABA_ND), two bars per cell (paper target vs SEClamp this
     task), y-axis = conductance (nS), error bars = SEClamp SD. Title = "Somatic SEClamp conductance
     vs Poleg-Polsky 2016 Fig 3A-E target (gNMDA = 0.5 nS)". Include legend, y-axis label, value
     annotations on each bar.
   * **Chart 2 `seclamp_vs_per_syn_direct_modality_comparison.png`**: grouped bar chart, same x-
     axis, three bars per cell (paper target, SEClamp this task, t0047 per-synapse-summed), y-axis =
     conductance (nS) on log scale (because the three modalities span ~2 orders of magnitude).
     Include legend, y-axis label "Conductance (nS, log scale)", value annotations.
   * Use `plt.savefig(path, dpi=150, bbox_inches="tight")` and `plt.close()`. Satisfies REQ-7.

8. **[CRITICAL] Create the answer asset
   `tasks/t0049_seclamp_cond_remeasure/assets/answer/seclamp-conductance-remeasurement-fig3/`** per
   `meta/asset_types/answer/specification.md` v2.
   * **`details.json`**:
     ```json
     {
       "spec_version": "2",
       "answer_id": "seclamp-conductance-remeasurement-fig3",
       "question": "Does measuring per-channel synaptic conductance under a somatic SEClamp on the deposited DSGC reproduce Poleg-Polsky 2016 Fig 3A-E values within +/- 25%, and resolve the t0047 amplitude mismatch as a measurement-modality artefact?",
       "short_title": "SEClamp re-measurement of Fig 3A-E conductances",
       "short_answer_path": "short_answer.md",
       "full_answer_path": "full_answer.md",
       "categories": [],
       "answer_methods": ["code-experiment"],
       "source_paper_ids": [],
       "source_urls": [],
       "source_task_ids": ["t0046_reproduce_poleg_polsky_2016_exact",
         "t0047_validate_pp16_fig3_cond_noise"],
       "confidence": "<high|medium|low based on verdict consistency>",
       "created_by_task": "t0049_seclamp_cond_remeasure",
       "date_created": "<YYYY-MM-DD>"
     }
     ```
     If no project category matches, use empty `categories: []`. Set `confidence` based on verdict
     consistency: `high` if all 6 cells render the same verdict (H0/H1/H2); `medium` if mixed; `low`
     if SEClamp values are inside the H2 band but with high SD.
   * **`short_answer.md`** (2-5 sentence answer): `## Question` (verbatim from `details.json`),
     `## Answer` (decisive: yes/no/insufficient + reasoning), `## Sources`. No inline citations in
     `## Answer`.
   * **`full_answer.md`** with these sections per spec v2: `## Question`, `## Short Answer`,
     `## Research Process`, `## Evidence from Papers` (state explicitly: not used),
     `## Evidence from Internet Sources` (state explicitly: not used),
     `## Evidence from Code or Experiments` (the SEClamp experiment + comparison-table walkthrough),
     `## Synthesis` (the integrated verdict), `## Limitations`, `## Sources`. The
     `## Evidence from Code or Experiments` section contains:
     * SEClamp methodology notes (clamp parameters, channel-isolation protocol, sign convention).
     * Per-channel comparison table (4 columns: paper, SEClamp this task, t0047 per-syn-summed,
       t0047 per-syn-mean) for all 6 channel x direction cells.
     * H0/H1/H2 verdict per cell with the supporting numbers.
     * Embedded charts:
       `![SEClamp vs paper](../../../results/images/seclamp_conductance_pd_vs_nd .png)` and
       `![SEClamp vs t0047 modality](../../../results/images/ seclamp_vs_per_syn_direct_modality_comparison.png)`.
   * The `## Synthesis` section is the headline 1-2 paragraph answer to whether modality alone
     explains the t0047 mismatch. Satisfies REQ-9.

(Subsequent stages — results writing, suggestions, compare-literature, cost tracking, machine
tracking, reporting — are orchestrator-managed and are NOT part of this plan.)

## Remote Machines

**None required**. The full 32-trial sweep takes ~5 minutes on the developer's local Windows
workstation using the NEURON 8.2.7 toolchain installed by t0007. No GPU is needed for SEClamp
simulation; NEURON is single-threaded and CPU-only for these compartmental simulations. Reference:
`arf/specifications/remote_machines_specification.md` for machine lifecycle (not invoked).

## Assets Needed

* **`modeldb_189347_dsgc_exact` library** (from
  `tasks/t0046_reproduce_poleg_polsky_2016_exact/ assets/library/modeldb_189347_dsgc_exact/`): the
  deposited DSGC sources, MOD files, and compiled DLL. Reused via direct cross-task import; no copy.
* **t0046 simulation driver**
  (`tasks/t0046_reproduce_poleg_polsky_2016_exact/code/run_simplerun. py` and `code/build_cell.py`
  and `code/constants.py`): imported directly by `code/run_seclamp.py`.
* **t0046 NEURON bootstrap**
  (`tasks/t0046_reproduce_poleg_polsky_2016_exact/code/ neuron_bootstrap.py`): imported to ensure
  NEURON DLL is loaded before any HOC call.
* **t0047 per-synapse-summed baseline values** (from
  `tasks/t0047_validate_pp16_fig3_cond_noise/ results/results_summary.md`): hard-coded into
  `code/constants.py` rather than imported, so the comparison table renders without runtime IO.
* **t0047 DSI helper** (`tasks/t0047_validate_pp16_fig3_cond_noise/code/dsi.py`): copied verbatim
  with attribution to `code/dsi.py`.
* **NEURON 8.2.7 environment** installed by t0007: the `neuron` Python module must be importable and
  the compiled MOD DLL must be loadable.

## Expected Assets

This task produces exactly one asset, matching `task.json` `expected_assets: {"answer": 1}`:

* **answer / `seclamp-conductance-remeasurement-fig3`** at
  `tasks/t0049_seclamp_cond_remeasure/assets/answer/seclamp-conductance-remeasurement-fig3/` per
  `meta/asset_types/answer/specification.md` v2. Contains `details.json`, `short_answer.md`,
  `full_answer.md`. The full answer carries: question framing, per-channel comparison table (paper
  vs SEClamp this task vs per-syn-summed t0047 vs per-syn-mean t0047), H0/H1/H2 verdict per cell,
  SEClamp methodology notes, synthesis paragraph identifying which interpretation (modality vs
  parameters) is supported.

In addition, the task produces these non-asset implementation artefacts under `results/` for the
orchestrator's `results` step to surface:

* `results/data/seclamp_trials.csv` — 32 rows, per-trial peak SEClamp current.
* `results/data/seclamp_comparison_table.csv` — 6 rows, per-channel x per-direction comparison.
* `results/images/seclamp_conductance_pd_vs_nd.png` — Chart 1.
* `results/images/seclamp_vs_per_syn_direct_modality_comparison.png` — Chart 2.
* `results/metrics.json` — explicit multi-variant format with 6 channel x direction variants
  (empty `metrics`) plus 3 DSI roll-up variants (one `direction_selectivity_index` each).

## Time Estimation

* **Research stage (already done)**: 0 hours (research-papers / research-internet skipped per
  step_tracker; research-code complete).
* **Planning stage (this document)**: ~30 minutes.
* **Implementation stage**:
  * Step 1 paths.py: 5 min.
  * Step 2 constants.py: 10 min.
  * Step 3 dsi.py copy: 2 min.
  * Step 4 run_seclamp.py: 30-45 min (most novel code).
  * Step 5 run_seclamp_sweep.py + validation gate + 32-trial run: 30 min coding + 5 min runtime =
    ~35 min.
  * Step 6 compute_metrics.py: 20 min.
  * Step 7 render_figures.py: 15 min.
  * Step 8 answer-asset writing: 30 min.
  * **Subtotal**: ~3 hours.
* **Quality + style + verificator iteration**: 30 min.
* **Total wall-clock**: ~4 hours including the 5 min sweep runtime. Within the task description's
  "1-2 hours" estimate at the lower end was optimistic; 4 hours is a realistic upper bound.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| SEClamp drift: clamp does not hold within +/- 0.5 mV of -65 mV due to high-current epochs (e.g., GABA at -5 mV driving force generates large clamp current) | Medium | Conductance values would be biased; verdict unreliable | Step 4 records soma voltage; runtime assertion `clamp_v_sd_mv < 0.5` mV. If breached, lower `rs` further (try 0.0001 MOhm) or use `dur1/amp1/dur2/amp2` two-stage clamp; document in implementation log. If unfixable, mark conductance values as "lower bound" in the answer asset and downgrade `confidence` to `low`. |
| Channel-isolation overrides leak (e.g., AMPA contribution remains under `b2gampa = 0` because of a hidden global) | Low | Per-channel currents would be cross-contaminated; H0/H1/H2 verdict would be wrong | Cross-check: sum of (AMPA-only + NMDA-only + GABA-only) currents should approximately equal the full-circuit current at each timepoint within ~10% tolerance. The `ALL` trial is included for this purpose. If sum disagrees by >20%, halt and inspect individual `_ref_gAMPA` / `_ref_gNMDA` / `_ref_g` traces to identify the leak. |
| t0046 cross-task import fails because of module-load side effects (NEURON DLL must be loaded once per process and certain HOC files must be sourced) | Low | Implementation cannot start | Mitigate via `from tasks.t0046_..._exact.code.neuron_bootstrap import ensure_neuron_importable; ensure_neuron_importable()` at the top of `code/run_seclamp.py`. If this fails, file an intervention noting the t0046 DLL is broken in this worktree. |
| `simplerun()` clobbers the SEClamp insertion (it is called BEFORE we attach SEClamp; the clamp is re-attached after the override-rerun) | Low | Wrong measurement (no clamp during the actual recorded run) | The plan attaches the SEClamp AFTER `simplerun()` returns and AFTER the override + `update()` + `placeBIP()`, just before `finitialize` + `continuerun`. Recorder vectors only record during the second (post-clamp) run. Verified by the clamp-quality assertion in Step 4. |
| `_ref_i` sign convention misinterpretation leads to negative conductances | Medium | Comparison table garbled | Use `abs(peak_i - baseline_i)` and `abs(V_clamp - E_rev)` so derived conductance is always positive. Document the sign convention explicitly in `code/run_seclamp.py` docstring and in the answer asset. |
| Cell build cache (`_CELL_STATE` in t0046) goes stale between channel-isolation overrides because `placeBIP()` re-shuffles synapse positions | Low | Spurious trial-to-trial variance | t0046 already asserts BIP positions return to baseline after each `simplerun()`. We re-call `assert_bip_positions_baseline` at the end of every trial. If it fails, force a fresh `_ensure_cell()` clear (`_CELL_STATE.clear()`) and rebuild. |
| Per-channel-summed vs full-circuit cross-check fails because of nonlinear channel interactions (e.g., NMDA voltage-dependence at -65 mV is small but nonzero) | Medium | The `ALL` reference is not exactly the linear sum; minor cross-talk is expected | Document the expected discrepancy in the answer asset. Use a 10-15% tolerance on the cross-check rather than strict equality. NMDA at -65 mV is ~10-20% of full conductance under standard Mg block, so the linearity assumption is approximate. |

## Verification Criteria

Six concrete checks. Every criterion specifies the exact command and the expected output.

* **Plan verificator (REQ-12)**: Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0049_seclamp_cond_remeasure -- uv run python -m arf.scripts.verificators.verify_plan t0049_seclamp_cond_remeasure`.
  Expected: zero errors. Warnings other than `PL-W003` (frontmatter) are acceptable but should be
  reviewed.

* **Per-trial CSV exists with 32 rows (REQ-3)**: After Step 5 completes, run
  `python -c "import pandas as pd; df = pd.read_csv('tasks/t0049_seclamp_cond_remeasure/results/ data/seclamp_trials.csv'); print(len(df), df.groupby(['direction','channel_on']).size())"`.
  Expected: `32` and 8 groups of 4 rows each (2 directions x 4 channel-isolations).

* **Comparison table covers all 6 cells (REQ-6)**: After Step 6, run
  `python -c "import pandas as pd; df = pd.read_csv('tasks/t0049_seclamp_cond_remeasure/results/ data/seclamp_comparison_table.csv'); print(len(df), set(df['channel'].unique()), set(df['direction'].unique()), set(df['verdict'].unique()))"`.
  Expected: 6 rows, channels = {`nmda`, `ampa`, `gaba`}, directions = {`PD`, `ND`}, verdicts subset
  of {`H0`, `H1`, `H2`}.

* **Metrics file uses explicit multi-variant format with at least 6 channel x direction variants
  (REQ-5)**: Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0049_seclamp_cond_remeasure -- uv run python -m arf.scripts.verificators.verify_task_metrics t0049_seclamp_cond_remeasure`.
  Expected: zero errors. Then
  `python -c "import json; m = json.load(open('tasks/ t0049_seclamp_cond_remeasure/results/metrics.json')); print(len(m['variants']))"`.
  Expected: 9 (6 channel x direction + 3 DSI roll-ups).

* **Both PNGs exist and are non-empty (REQ-7)**:
  `ls -la tasks/t0049_seclamp_cond_remeasure/ results/images/seclamp_conductance_pd_vs_nd.png tasks/t0049_seclamp_cond_remeasure/results/ images/seclamp_vs_per_syn_direct_modality_comparison.png`.
  Expected: both files exist and have size > 1 KB.

* **Answer asset structure passes verificator (REQ-9, REQ-12)**: Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0049_seclamp_cond_remeasure -- uv run python -m arf.scripts.verificators.verify_answer_asset t0049_seclamp_cond_remeasure`.
  Expected: zero errors. The asset folder must contain `details.json`, `short_answer.md`,
  `full_answer.md` per v2 spec; the `## Synthesis` paragraph must explicitly resolve modality vs
  parameters.

* **Requirement-coverage check (REQ-1 through REQ-12)**: After all steps, manually grep the
  `results/results_detailed.md` (orchestrator-written but seeded by these implementation artefacts)
  for each `REQ-N` ID. Each requirement must map to at least one evidence path (CSV, PNG, asset, or
  log). Command: `grep -c "REQ-" tasks/t0049_seclamp_cond_remeasure/results/ results_detailed.md`
  must return >= 12.
