---
spec_version: "2"
task_id: "t0057_tonic_gaba_sweep_t0053"
date_completed: "2026-04-28"
status: "complete"
---
# Plan: Tonic GABA + Amplitude Sweep on t0053 Spatial DSGC

## Objective

Replace t0053's per-event `Exp2Syn` GABA point process with a new `gaba_tonic.mod` POINT_PROCESS
that delivers a sustained conductance over a configurable `(t_on, t_off)` window per synapse, then
sweep `GABA_BASE_NS in {0.25, 0.5, 1.0, 1.5, 2.0}` nS while preserving t0053's morphology, synapse
placement (seed 0), AMPA path, spatial centripetal-gating predicate, and 12-direction stimulus
protocol bit-for-bit. "Done" means: a registered library asset `minimal_dsgc_tonic_gaba_sweep`
exists; for each of the 5 conductance values per-direction
soma-V/EPSP/IPSP/PSTH/activation/active-fraction figures and a polar tuning curve are produced; six
cross-conductance summary plots (DSI primary, DSI vector-sum, peak Hz, null Hz, HWHM, RMSE vs
`GABA_BASE_NS`) are produced; a 15-variant `metrics.json` (5 conductances x 3 modes) is written; the
IPSP-sustained-window regression test passes (`v(1300 ms) >= 0.5 * v(200 ms)` relative to V_rest at
the most-active direction); and `verify_plan.py`, `verify_research_code.py`,
`verify_task_metrics.py`, and the library asset verificator all pass with 0 errors.

## Task Requirement Checklist

The operative task text from `task_description.md` is:

> Build a new GABA mechanism (`gaba_tonic.mod`) that delivers a sustained conductance over a
> configurable `(t_on, t_off)` window per synapse, integrate it into the t0053 minimal DSGC code as
> a drop-in replacement for the current Exp2Syn GABA mechanism, sweep per-synapse peak conductance
> across five values, and report the directional response.

> Sweep: `GABA_BASE_NS in {0.25, 0.5, 1.0, 1.5, 2.0}` nS — five conductance values. Total: 12
> directions x 10 trials x 3 modes (FULL / AMPA_ONLY / GABA_ONLY) x 5 conductances = 1800 trials.

> Library Asset: produce one library asset `minimal_dsgc_tonic_gaba_sweep`. The library should
> expose `GABA_BASE_NS` as a public parameter so the sweep harness can vary it without re-importing.

The full task description is at `tasks/t0057_tonic_gaba_sweep_t0053/task_description.md`.

| ID | Requirement | Satisfying step(s) | Evidence of completion |
| --- | --- | --- | --- |
| REQ-1 | Build `gaba_tonic.mod` POINT_PROCESS with parameters `(g, e, t_on, t_off)`, sustained `g` between `t_on` and `t_off`, zero outside, reversal `e = -75 mV`, optional 1-2 ms cosine ramp at edges. | Step 5 | `code/mod/gaba_tonic.mod` exists; `code/mod/nrnmech.dll` builds; `print(h.gaba_tonic)` succeeds. |
| REQ-2 | Compile and load the new MOD via a `code/run_nrnivmodl.cmd` shim and `ensure_gaba_tonic_compiled()` bootstrap (mirror of [t0055]). | Step 6 | `nrnmech.dll` regenerated on demand; `hasattr(h, "gaba_tonic")` is True after bootstrap. |
| REQ-3 | Drop-in replacement: each E/I pair gets one `gaba_tonic` instance instead of `Exp2Syn` + NetStim + NetCon plumbing. | Steps 7, 8 | `synapses.py` has no `gaba_netstim` / `gaba_netcon` references; per-pair `gaba_syn = h.gaba_tonic(seg)` constructed once per pair. |
| REQ-4 | Spatial centripetal-gating predicate from t0053 preserved bit-for-bit (`cos(radians(theta_stim - theta_centrifugal_synapse)) < 0`); fired synapses get `g = GABA_BASE_NS`, `t_on = 100 ms`, `t_off = 1400 ms`; silent synapses get `g = 0`. | Steps 7, 8 | `i_synapse_fires` predicate identical to t0053's `synapses.py` lines 76-91; `test_spatial_gating.py` passes. |
| REQ-5 | Same fixed placement seed (0) as t0052 / t0053; bit-identical `placement_seed0.json`. | Step 4 | `test_placement_seed0_match.py` passes against t0053's reference `placement_seed0.json` (POSITION_TOLERANCE = 1e-9). |
| REQ-6 | AMPA mechanism unchanged from t0053 (Exp2Syn rise=0.5 ms, decay=2.5 ms, e=0 mV, peak 0.5 nS). | Step 7 | AMPA construction in `synapses.py` matches t0053 verbatim; AMPA_ONLY peak Hz = 0.667 across all 12 directions in metrics. |
| REQ-7 | Sweep `GABA_BASE_NS in {0.25, 0.5, 1.0, 1.5, 2.0}` nS x 12 directions x 10 trials x 3 modes (FULL, AMPA_ONLY, GABA_ONLY) = 1800 trials. | Steps 9, 11 | Per-mode tuning-curve CSVs contain 5 (`gaba_base_ns`) x 12 (`angle_deg`) = 60 rows per mode; spike CSVs contain 1800 unique trial rows. |
| REQ-8 | Library asset `minimal_dsgc_tonic_gaba_sweep` registered per `meta/asset_types/library/specification.md` with `GABA_BASE_NS` exposed as a public parameter. | Step 14 | `assets/library/minimal_dsgc_tonic_gaba_sweep/details.json` exists; `description.md` documents the public API including `GABA_BASE_NS`; library verificator passes with 0 errors. |
| REQ-9 | For each conductance: 12 PNGs of soma V(t), 12 PNGs of aggregate EPSP, 12 PNGs of aggregate IPSP, 12 PNGs of firing-rate PSTH, 12 PNGs of per-synapse activation-time histogram, and a polar tuning curve. | Step 13 | `results/images/` contains the 5 x (12 + 12 + 12 + 12 + 12 + 1) = 305 per-conductance PNGs; counts asserted in the dry-run gate. |
| REQ-10 | Polar plot of "fraction of I synapses active vs direction" carried over from t0053. | Step 13 | `results/images/active_fraction_polar.png` exists; values match t0053's 0.34-0.66 modulation since spatial gating rule is unchanged. |
| REQ-11 | Cross-conductance summary plots: DSI (primary), DSI (vector-sum), peak Hz, null Hz, HWHM, RMSE vs t0004 target — all vs `GABA_BASE_NS`. | Step 13 | 6 cross-conductance summary PNGs saved in `results/images/`. |
| REQ-12 | Per-conductance `metrics.json` entries with primary DSI, vector-sum DSI, preferred direction, peak Hz, null Hz, HWHM, RMSE vs t0004. | Step 12 | `results/metrics.json` contains 15 variants (5 conductances x 3 modes) with `dimensions = {"mode": ..., "gaba_base_ns": ...}` and the full metric set. |
| REQ-13 | IPSP-sustained-window regression: at the most-active direction, IPSP voltage at `t = 1300 ms` is at least 50% of IPSP voltage at `t = 200 ms` (relative to V_rest). | Step 11, dry-run gate | `code/test_gaba_tonic_envelope.py` asserts the ratio for each of the 5 conductances; included in the dry-run gate. |
| REQ-14 | AMPA_ONLY 0.667 Hz uniform peak rate regression (no-regression sentinel for the unchanged AMPA path). | Step 12, dry-run gate | `compute_metrics.py` asserts `peak_hz_ampa_only == 0.6667` for every conductance. |
| REQ-15 | Tonic mechanism uses `(t_on, t_off) = (100 ms, 1400 ms)` per active synapse — fully covering the stimulus presentation interval minus the BASE_OFFSET buffer. | Steps 5, 8 | `gaba_tonic.mod` defaults / `synapses.py` writes use `T_ON_MS = 100.0`, `T_OFF_MS = 1400.0` from `constants.py`. |
| REQ-16 | Direct head-to-head against t0053: at the swept value matching t0053's 2 nS, report whether the tonic mechanism produces non-zero firing and what DSI it yields. | Step 12 | `metrics.json` variant `gaba_2.00_full` records peak Hz, null Hz, primary DSI; documented in implementation log. |
| REQ-17 | Cross-conductance peak Hz vs t0004 target — does any single `GABA_BASE_NS` land within an order of magnitude of the t0004 target peak (32 Hz)? | Step 12 | `derived_quantities.json` contains `peak_hz_vs_gaba` array; comparison annotated in the cross-conductance peak-Hz figure. |

## Approach

The chosen approach copies t0053's twelve-module code package verbatim and surgically replaces only
the GABA mechanism. The research-code summary (research/research_code.md) identifies the swap
surface as five touchpoints: `code/synapses.py` GABA construction (t0053 lines 121-124, 132-136,
142-144, 184-229), `code/trial.py` mode toggling (lines 47-64, 119-127), `code/run_tuning_curve.py`
outer sweep loop, `code/compute_metrics.py` multi-variant emission, and `code/render_figures.py`
per-conductance + cross-conductance figures. Bit-identical files copied unchanged (apart from
import-prefix rewrites): `cell.py`, `swc_io.py`, `placement.py`, `metrics_extra.py`,
`test_spatial_gating.py`, `test_quiescent_rest.py`, `test_placement_seed0_match.py`.

The new GABA delivery uses a custom NEURON `.mod` POINT_PROCESS rather than NetStim/NetCon event
plumbing because (a) tonic delivery cannot be expressed as a single instantaneous event with Exp2Syn
kinetics — the conductance envelope must be a function of `t`, not of post-event time, and (b) the
only existing repo precedent for shipping a custom MOD ([t0055]'s `NMDA_MgBlock.mod`) demonstrated
this pattern works on Windows with a `run_nrnivmodl.cmd` shim and `ensure_<mech>_compiled()`
bootstrap. Conductance is set by direct attribute write (`pair.gaba_syn.g = gaba_base_ns * 1e-3`)
and `(t_on, t_off)` is set per synapse before each trial. The optional 1-2 ms cosine ramp at window
edges (preferred per task description) is implemented as a piecewise function inside `BREAKPOINT` to
avoid stiff-step integrator artefacts.

The outer-loop sweep pattern is borrowed verbatim from [t0055]'s `run_tuning_curve.py` lines
269-298: a `GABA_BASE_NS_VALUES = (0.25, 0.5, 1.0, 1.5, 2.0)` constant, a per-trial `gaba_base_ns`
parameter threaded through `_run_sweep_for_mode` and `run_one_trial`, and a `gaba_base_ns` column
added to every per-mode CSV header. CVODE (`atol = 1e-3`, from [t0055]'s `enable_cvode`) is
mandatory: it drops per-trial wall-clock from ~75 s (fixed-step) to ~3-8 s, which is the only way
1800 trials fit in the ~25-30 min wall-clock budget on local CPU.

**Recommended task type(s)**: `build-model` and `experiment-run` (already declared in `task.json`'s
`task_types` field). The `build-model` Planning Guidelines steered (a) the explicit hyperparameter
logging requirement (per-conductance, per-mode, seed, dt), (b) the explicit metrics variants format
(15 variants in `metrics.json`), and (c) the model asset (here a library asset embedding the
simulation code). The `experiment-run` Planning Guidelines steered (a) the hypothesis-style framing
(does any conductance produce non-zero FULL-mode tuning?), (b) the per-condition metrics breakdown,
(c) the saved-predictions equivalent (per-trial spike CSVs and per-direction voltage traces are the
diagnostic raw data), and (d) the explicit baseline comparisons (t0004 target peak 32 Hz; AMPA_ONLY
0.667 Hz regression invariant from t0052/t0053).

**Alternatives considered**:

* **Modify t0053 to use a longer Exp2Syn `tau2`.** Rejected because raising `tau2` from 20 ms to
  ~500 ms still gives an exponential decay envelope rather than a true sustained conductance, and
  multiple per-event firings would still be needed to fill 1300 ms — i.e., the mechanism would
  still couple amplitude to event-decay-tau interactions, defeating the purpose of decoupling
  amplitude from timing.
* **Use multiple per-synapse spike events spaced through the stimulus window.** Rejected because it
  adds an extra spacing hyperparameter, increases NetStim/NetCon overhead, and produces a ripple
  envelope rather than a clean tonic plateau — harder to interpret in the IPSP voltage trace and
  harder to compare to canonical SAC->DSGC IPSC profiles.
* **Implement a single-instance global GABA conductance in `cell.py` rather than per-synapse.**
  Rejected because spatial centripetal gating is fundamentally per-synapse — the active-vs-silent
  split is determined by each synapse's centrifugal angle relative to the stimulus direction, so a
  global conductance loses the spatial modulation.

## Cost Estimation

* External API costs: **$0.00** (no LLM calls, no third-party APIs).
* Remote compute: **$0.00** (local CPU only; CVODE keeps the 1800-trial sweep within ~25-30 min
  wall-clock on the user's machine).
* Storage: **$0.00** (all artefacts written under the task folder; per-mode CSVs use stride-8
  voltage downsampling per [t0055] guidance to keep disk usage reasonable).
* Total estimated cost: **$0.00** vs. project budget of $1.00 (`project/budget.json`).

## Step by Step

### Milestone 1: Bootstrap MOD compilation pipeline

1. **Create `code/paths.py` and `code/constants.py`.** Copy
   `tasks/t0053_minimal_dsgc_spatial_gaba/code/paths.py` and
   `tasks/t0053_minimal_dsgc_spatial_gaba/code/constants.py` to
   `tasks/t0057_tonic_gaba_sweep_t0053/code/paths.py` and `code/constants.py`. Rewrite the import
   prefix `tasks.t0053_minimal_dsgc_spatial_gaba` to `tasks.t0057_tonic_gaba_sweep_t0053`. In
   `paths.py` add `MOD_DIR = CODE_DIR / "mod"`,
   `RUN_NRNIVMODL_CMD = CODE_DIR / "run_nrnivmodl.cmd"`, `NRNMECH_DLL = MOD_DIR / "nrnmech.dll"`
   (mirror lines 38-41 of `tasks/t0055_nmda_mg_block_dsi_recovery/code/paths.py`). Add
   `T0053_PLACEMENT_JSON` pointing at
   `tasks/t0053_minimal_dsgc_spatial_gaba/results/placement_seed0.json` for the bit-identity test.
   In `constants.py` add `GABA_BASE_NS_VALUES = (0.25, 0.5, 1.0, 1.5, 2.0)`, `T_ON_MS = 100.0`,
   `T_OFF_MS = 1400.0`, and a `GABA_RAMP_MS = 1.0` constant for the optional cosine ramp width.
   Satisfies REQ-1, REQ-15.

2. **Create the Windows `nrnivmodl` shim.** Copy
   `tasks/t0055_nmda_mg_block_dsi_recovery/code/run_nrnivmodl.cmd` (12 lines) verbatim to
   `tasks/t0057_tonic_gaba_sweep_t0053/code/run_nrnivmodl.cmd`. The script `pushd`s into `code/mod/`
   and calls `C:\Users\md1avn\nrn-8.2.7\bin\nrnivmodl.bat .` to produce `code/mod/nrnmech.dll`. The
   script is task-agnostic so no edits are needed beyond placement. Satisfies REQ-2.

3. **Write the new `gaba_tonic.mod` POINT_PROCESS.** Create
   `tasks/t0057_tonic_gaba_sweep_t0053/code/mod/gaba_tonic.mod` (~50-80 lines). Reference style:
   `tasks/t0055_nmda_mg_block_dsi_recovery/code/mod/NMDA_MgBlock.mod` lines 55-120. Body skeleton:

   ```text
   NEURON {
     POINT_PROCESS gaba_tonic
     RANGE g, e, t_on, t_off, i, ramp_ms
     NONSPECIFIC_CURRENT i
   }
   PARAMETER {
     g = 0       (uS)    : tonic peak conductance, set per trial
     e = -75    (mV)
     t_on = 0   (ms)
     t_off = 0  (ms)
     ramp_ms = 1 (ms)
   }
   ASSIGNED { v (mV)   i (nA) }
   BREAKPOINT {
     i = g_envelope(t) * g * (v - e)
   }
   FUNCTION g_envelope(tloc) {
     LOCAL d_on, d_off
     if (tloc < t_on || tloc > t_off) {
       g_envelope = 0
     } else {
       d_on  = tloc - t_on
       d_off = t_off - tloc
       if (d_on  < ramp_ms) { g_envelope = 0.5 * (1 - cos(3.14159265358979 * d_on  / ramp_ms)) }
       else if (d_off < ramp_ms) { g_envelope = 0.5 * (1 - cos(3.14159265358979 * d_off / ramp_ms)) }
       else { g_envelope = 1 }
     }
   }
   ```

   No `NET_RECEIVE` block needed — conductance is set by direct attribute write at trial-setup
   time. Smoke-test by running `code/run_nrnivmodl.cmd` and confirming `code/mod/nrnmech.dll` exists
   with non-zero size. Satisfies REQ-1, REQ-15.

### Milestone 2: Port t0053 code skeleton

4. **Copy invariant modules from t0053 (bit-identical apart from import prefix rewrite).** Copy the
   following files from `tasks/t0053_minimal_dsgc_spatial_gaba/code/` to
   `tasks/t0057_tonic_gaba_sweep_t0053/code/`:

   * `cell.py` (~226 lines) — builds the calibrated DSGC from the t0009 SWC.
   * `swc_io.py` — SWC parser (imported by `cell.py`).
   * `placement.py` (~88 lines) — length-weighted random placement of 100 dendritic locations with
     seed=0; saves `placement_seed0.json`.
   * `metrics_extra.py` (~44 lines) — `compute_vector_sum_dsi`, `compute_preferred_direction_deg`.
   * `test_spatial_gating.py` (~67 lines) — 4 unit tests for the centripetal predicate.
   * `test_quiescent_rest.py` — V_rest = -65 mV +/- 0.5 mV gate.
   * `test_placement_seed0_match.py` (~74 lines) — bit-identity check vs t0053
     `placement_seed0.json`. Update the reference path constant to point at `T0053_PLACEMENT_JSON`
     from `paths.py`. Preserve `POSITION_TOLERANCE = 1e-9`.

   For every copied file, rewrite import prefix `tasks.t0053_minimal_dsgc_spatial_gaba` to
   `tasks.t0057_tonic_gaba_sweep_t0053`. No logic changes. Satisfies REQ-4 (preserves
   `i_synapse_fires` test infrastructure), REQ-5, REQ-6 (cell + placement contracts unchanged).

5. **Port `code/neuron_bootstrap.py` with the new `ensure_gaba_tonic_compiled()` hook.** Copy
   `tasks/t0055_nmda_mg_block_dsi_recovery/code/neuron_bootstrap.py` (~146 lines). Rename
   `ensure_nmda_mg_block_compiled` to `ensure_gaba_tonic_compiled`. Change all `NMDA_MgBlock`
   references to `gaba_tonic`. Rename the `_T0055_NEURONHOME_BOOTSTRAPPED` sentinel constant to
   `_T0057_NEURONHOME_BOOTSTRAPPED`. Rebind `RUN_NRNIVMODL_CMD` and `NRNMECH_DLL` paths to those
   declared in `tasks.t0057_tonic_gaba_sweep_t0053.code.paths`. The function rebuilds
   `code/mod/nrnmech.dll` via `subprocess.run([str(RUN_NRNIVMODL_CMD)], check=True)` if missing,
   then calls `h.nrn_load_dll(str(NRNMECH_DLL))` and asserts `hasattr(h, "gaba_tonic")`. Keep the
   `enable_cvode(atol=1e-3)` helper and the `_T0057_NEURONHOME_BOOTSTRAPPED` Windows env bootstrap.
   Satisfies REQ-2.

### Milestone 3: GABA-mechanism swap

6. **Adapt `code/synapses.py` for direct `gaba_tonic` attribute writes.** Copy
   `tasks/t0053_minimal_dsgc_spatial_gaba/code/synapses.py` (~229 lines). Keep these unchanged
   (apart from import prefix rewrite):

   * `EiPair` dataclass field set, minus `gaba_netstim` and `gaba_netcon` fields (drop both).
   * `i_synapse_fires` predicate (lines 76-91) — bit-identical centripetal-gating function.
   * `theta_centrifugal_rad` precomputation (lines 146-149) — per-pair angle from soma origin.
   * `_onset_time_ms` helper for E synapses.
   * AMPA construction: `ampa_syn = h.Exp2Syn(seg)` with `tau1 = 0.5 ms`, `tau2 = 2.5 ms`,
     `e = 0 mV`; `ampa_netstim = h.NetStim(); ampa_netstim.number = 1; ampa_netstim.noise = 0`;
     `ampa_netcon = h.NetCon(ampa_netstim, ampa_syn, 0, 0, 0.5e-3)` (peak 0.5 nS).

   Replace the GABA branch:

   * **Old**:
     `gaba_syn = h.Exp2Syn(seg); gaba_syn.tau1 = 1.0; gaba_syn.tau2 = 20.0; gaba_syn.e = -75; gaba_netstim = h.NetStim(); ...; gaba_netcon = h.NetCon(gaba_netstim, gaba_syn, 0, 0, 0)`
     (lines 121-124, 132-136, 142-144).
   * **New**:
     `gaba_syn = h.gaba_tonic(seg); gaba_syn.e = -75.0; gaba_syn.g = 0.0; gaba_syn.t_on = 0.0; gaba_syn.t_off = 0.0; gaba_syn.ramp_ms = GABA_RAMP_MS`.
     No NetStim, no NetCon for the GABA branch.

   Replace `schedule_ei_onsets` (lines 184-229): accept `gaba_base_ns: float` parameter. For each
   pair compute `fired = i_synapse_fires(theta_stim_rad, pair.theta_centrifugal_rad)`. For E
   synapses keep the existing onset write (`pair.gaba_netstim.start = onset_ms` is the AMPA netstim,
   not GABA — verify in the t0053 source whether the variable name is `ampa_netstim`). For I
   synapses:

   * If `fired`: `pair.gaba_syn.g = gaba_base_ns * 1e-3`, `pair.gaba_syn.t_on = T_ON_MS`,
     `pair.gaba_syn.t_off = T_OFF_MS`.
   * Else: `pair.gaba_syn.g = 0.0`, `pair.gaba_syn.t_on = 0.0`, `pair.gaba_syn.t_off = 0.0`.

   Also append `i_active_fraction = sum(fired) / len(pairs)` to the returned scheduler result for
   downstream `active_fraction_per_direction.csv` emission. Satisfies REQ-3, REQ-4, REQ-15.

7. **Adapt `code/trial.py` for tonic mode toggling.** Copy
   `tasks/t0053_minimal_dsgc_spatial_gaba/code/trial.py` (~140 lines). Rewrite `_apply_mode_weights`
   (lines 47-64):

   * **AMPA_ONLY**: zero GABA via `pair.gaba_syn.g = 0.0` (instead of
     `pair.gaba_netcon.weight[0] = 0.0`); leave AMPA NetCon weight at 0.5 nS.
   * **GABA_ONLY**: zero AMPA NetCon weight as before; leave GABA `g` at the gated value set by
     `schedule_ei_onsets`.
   * **FULL**: leave both at scheduled values.

   Rewrite the post-trial defensive-restore block (lines 119-127): after each trial restore AMPA
   NetCon weights from saved dict and reset `pair.gaba_syn.g`, `pair.gaba_syn.t_on`,
   `pair.gaba_syn.t_off` to 0.0 (so the next trial's `schedule_ei_onsets` writes from a clean
   state).

   Add `gaba_base_ns: float` parameter to `run_one_trial`. Add `gaba_base_ns` field to `TrialResult`
   dataclass for downstream CSV emission. Satisfies REQ-3, REQ-7.

### Milestone 4: Sweep harness and per-conductance metrics

8. **Adapt `code/run_tuning_curve.py` for the outer conductance loop.** Copy
   `tasks/t0053_minimal_dsgc_spatial_gaba/code/run_tuning_curve.py` (~459 lines). Major changes:

   * Import `GABA_BASE_NS_VALUES`, `T_ON_MS`, `T_OFF_MS` from
     `tasks.t0057_tonic_gaba_sweep_t0053.code.constants`.
   * In `setup_sweep_artifacts()` call `ensure_gaba_tonic_compiled()` AFTER `load_stdrun()` and
     BEFORE any `h.gaba_tonic(seg)` construction (mirror lines 128-131 of [t0055]'s
     `run_tuning_curve.py`).
   * Add `gaba_base_ns` outer loop wrapping the existing `(angle, trial, mode)` triple loop. Mirror
     lines 285-294 of [t0055]'s `run_tuning_curve.py`.
   * Thread `gaba_base_ns` into `_run_sweep_for_mode` and `run_one_trial`.
   * Add `gaba_base_ns` as the leading column to every per-mode CSV header
     (`tuning_curve_<mode>.csv`, `spike_times_<mode>.csv`, `voltage_traces_<mode>.csv`,
     `activation_times.csv`). Mirror lines 165-178 of [t0055]'s `run_tuning_curve.py`.
   * Also keep `active_fraction_per_direction.csv` (12 rows; values are conductance-independent
     because the spatial gating rule is unchanged, so write it once not 5 times).
   * Use stride-8 voltage downsampling for `voltage_traces_<mode>.csv` to keep disk size reasonable
     per [t0055] guidance.

   Satisfies REQ-7, REQ-9, REQ-10.

9. **Validation gate: dry-run with one conductance and one direction.** Before launching the full
   1800-trial sweep, run `run_tuning_curve.py --dry-run` (or equivalent flag) which executes a
   single conductance pass at `gaba_base_ns = 1.0`, `theta = 0`, 2 trials, all 3 modes. The trivial
   baseline values are: AMPA_ONLY peak Hz = 0.667 (the t0052/t0053 unchanged-AMPA-path invariant);
   FULL spike count <= AMPA_ONLY spike count (because GABA inhibits, never excites);
   `i_active_fraction` at theta=0 is in `[0.30, 0.70]` (from t0053's spatial-gating polar). The
   dry-run gate also runs the new IPSP-sustained-window check at `theta = 210 deg`,
   `mode = GABA_ONLY`, `gaba_base_ns = 1.0`: assert
   `abs(v_at_1300_ms - V_INIT_MV) >= 0.5 * abs(v_at_200_ms - V_INIT_MV)`. Failure condition: if
   `peak_hz_ampa_only != 0.6667 +/- 1e-3`, or `i_active_fraction not in [0.30, 0.70]`, or the
   IPSP-sustained-window assertion fails, STOP and inspect 5 individual trials per failing mode
   (read raw spike CSV, raw voltage CSV) — do not proceed to the full 1800-trial sweep until the
   gate passes. This validation gate is mandatory because the full sweep is ~25-30 min wall-clock
   and a broken integration would waste that whole window. Satisfies REQ-13, REQ-14.

10. **Run the full 1800-trial sweep.** Execute
    `uv run python -m arf.scripts.utils.run_with_logs --task-id t0057_tonic_gaba_sweep_t0053 -- uv run python -u -m tasks.t0057_tonic_gaba_sweep_t0053.code.run_tuning_curve`.
    Expected wall-clock: ~25-30 min on local CPU (per t0052/t0053 reference: 19m 13s and 17m 11s for
    360 trials each; t0057 has 1800 trials = 5x but uses the same per-trial CVODE budget). Outputs:
    `results/tuning_curve_full.csv`, `results/tuning_curve_ampa_only.csv`,
    `results/tuning_curve_gaba_only.csv`, `results/spike_times_*.csv`,
    `results/voltage_traces_*.csv`, `results/activation_times.csv`,
    `results/active_fraction_per_direction.csv`, `results/placement_seed0.json`. Satisfies REQ-7.

11. **Add IPSP-sustained-window regression test.** Create
    `tasks/t0057_tonic_gaba_sweep_t0053/code/test_gaba_tonic_envelope.py`. The test loads
    `results/voltage_traces_gaba_only.csv`, pivots by `(gaba_base_ns, angle_deg, sample_idx)` to
    `mean_v_mv`, and for the most-active direction (`theta = 210 deg` from t0053's spatial-gating
    polar) asserts for each of the 5 conductance values
    `abs(v_at_1300_ms - V_INIT_MV) >= 0.5 * abs(v_at_200_ms - V_INIT_MV)`. Pivot template:
    `_voltage_pivot_per_angle` at lines 72-97 of t0053's `render_figures.py`. Run with
    `uv run pytest tasks/t0057_tonic_gaba_sweep_t0053/code/test_gaba_tonic_envelope.py -v`.
    Satisfies REQ-13.

12. **Adapt `code/compute_metrics.py` for the 15-variant `metrics.json`.** Copy
    `tasks/t0053_minimal_dsgc_spatial_gaba/code/compute_metrics.py` (~298 lines). Pivot all loaders
    by `gaba_base_ns` first, then by `mode`. For each `(gaba_base_ns, mode)` pair compute
    `direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
    `tuning_curve_rmse` (vs t0004 target curve), `peak_hz`, `null_hz`, `vector_sum_dsi`, and
    `preferred_direction_deg`. Emit 5 x 3 = 15 variants in `results/metrics.json` with explicit
    multi-variant schema:

    ```json
    {
      "variants": [
        {
          "variant_id": "gaba_0.25_full",
          "dimensions": {"mode": "full", "gaba_base_ns": 0.25},
          "metrics": {"direction_selectivity_index": ..., "tuning_curve_hwhm_deg": ..., ...}
        },
        ...
      ]
    }
    ```

    Use the exact format defined in `arf/specifications/metrics_specification.md`. Also write
    `results/derived_quantities.json` with cross-conductance summary arrays (`peak_hz_vs_gaba`,
    `dsi_primary_vs_gaba`, `dsi_vector_sum_vs_gaba`, `null_hz_vs_gaba`, `hwhm_vs_gaba`,
    `rmse_vs_gaba`) plus per-direction EPSP / IPSP envelopes. Add the `peak_hz_ampa_only == 0.6667`
    sentinel assertion (REQ-14 regression). Use libraries from
    `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss`:
    `compute_dsi(curve=...)`, `compute_hwhm_deg(curve=...)`, `compute_peak_hz(curve=...)`,
    `compute_null_hz(curve=...)`, `compute_reliability(curve=...)`,
    `load_tuning_curve(csv_path=...)`. Use `compute_vector_sum_dsi` and
    `compute_preferred_direction_deg` from local
    `tasks.t0057_tonic_gaba_sweep_t0053.code.metrics_extra`. The four registered metrics
    (`direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
    `tuning_curve_rmse`) all apply: each is computed once per variant. Satisfies REQ-12, REQ-14,
    REQ-16, REQ-17.

13. **Adapt `code/render_figures.py` for per-conductance and cross-conductance plots.** Copy
    `tasks/t0053_minimal_dsgc_spatial_gaba/code/render_figures.py` (~324 lines). Each per-direction
    figure family becomes a per-(conductance, direction) family: the inner loop over 12 angles is
    wrapped by an outer loop over `GABA_BASE_NS_VALUES`. Output PNG names encode both, e.g.
    `soma_v_gaba_0.50_theta_180.png`. Six figure families per conductance: soma V(t), aggregate
    EPSP, aggregate IPSP (the new headline observable), firing-rate PSTH, per-synapse
    activation-time histogram, and the polar tuning curve (1 polar per conductance). For tuning
    curves use
    `tasks.t0011_response_visualization_library.code.tuning_curve_viz.plot_polar_tuning_curve( curve_csv=..., out_png=..., target_csv=...)`
    and `plot_cartesian_tuning_curve(curve_csv=..., out_png=..., target_csv=...)`.

    Add a new figure family: 6 cross-conductance summary PNGs (DSI primary, DSI vector-sum, peak Hz,
    null Hz, HWHM, RMSE — each as scalar vs `GABA_BASE_NS`). Use `matplotlib.pyplot` directly or
    `plot_multi_model_overlay` from
    `tasks.t0011_response_visualization_library.code.tuning_curve_viz` with one curve per
    conductance for the optional cross-conductance polar overlay. Keep `active_fraction_polar.png`
    from t0053 (single PNG, conductance-independent). Total expected PNG count: 5 conductances x (12
    \+ 12 + 12 + 12 + 12 + 1) + 6 summary + 1 active-fraction polar = 305 + 6 + 1 = 312 PNGs.
    Satisfies REQ-9, REQ-10, REQ-11.

### Milestone 5: Library asset

14. **Create the `minimal_dsgc_tonic_gaba_sweep` library asset.** Create
    `tasks/t0057_tonic_gaba_sweep_t0053/assets/library/minimal_dsgc_tonic_gaba_sweep/details.json`
    per `meta/asset_types/library/specification.md`. Required fields: `spec_version: "2"`,
    `library_id: "minimal_dsgc_tonic_gaba_sweep"`, `name`, `version: "0.1.0"`, `short_description`,
    `description_path: "description.md"`,
    `module_paths: ["code/cell.py", "code/swc_io.py", "code/placement.py", "code/synapses.py", "code/trial.py", "code/run_tuning_curve.py", "code/compute_metrics.py", "code/render_figures.py", "code/metrics_extra.py", "code/neuron_bootstrap.py", "code/paths.py", "code/constants.py", "code/mod/gaba_tonic.mod"]`,
    `entry_points` listing `run_tuning_curve` (script), `gaba_tonic` (POINT_PROCESS class via
    `code/mod/gaba_tonic.mod`), `schedule_ei_onsets` (function), `run_one_trial` (function), and the
    public `GABA_BASE_NS_VALUES` constant (function-kind entry pointing at `constants.py`),
    `dependencies: ["neuron", "numpy", "matplotlib"]`,
    `test_paths: ["code/test_spatial_gating.py", "code/test_quiescent_rest.py", "code/test_placement_seed0_match.py", "code/test_gaba_tonic_envelope.py"]`,
    `categories: ["library", "dsgc", "simulation", "neuron-mod"]` (use existing slugs from
    `meta/categories/`; if `neuron-mod` is missing, omit it),
    `created_by_task: "t0057_tonic_gaba_sweep_t0053"`, `date_created: "2026-04-28"`. Then write
    `description.md` with YAML frontmatter (`spec_version: "2"`, `library_id`, `documented_by_task`,
    `date_documented`) and the seven mandatory sections (`## Metadata`, `## Overview`,
    `## API Reference`, `## Usage Examples`, `## Dependencies`, `## Testing`, `## Main Ideas`,
    `## Summary`). The `## API Reference` section must explicitly document `GABA_BASE_NS_VALUES` as
    a public parameter the sweep harness can vary (REQ-8). Run
    `uv run python -m arf.scripts.verificators.verify_assets t0057_tonic_gaba_sweep_t0053` to
    confirm the library asset passes with 0 errors. Satisfies REQ-8.

## Remote Machines

None required. Local CPU only. CVODE (`atol = 1e-3`) keeps per-trial wall-clock at ~3-8 s, making
the 1800-trial sweep tractable in ~25-30 min on the user's local machine. No GPU is needed —
single-cell compartmental simulation on the t0009-calibrated 141009_Pair1DSGC morphology fits
comfortably in CPU and RAM budget.

## Assets Needed

* **From [t0009_calibrate_dendritic_diameters]**: the calibrated SWC morphology referenced via
  `tasks.t0057_tonic_gaba_sweep_t0053.code.paths` constant pointing at the t0009 SWC file (same
  reference as t0053's `cell.py`).
* **From [t0011_response_visualization_library]**: registered library `tuning_curve_viz`, imported
  as
  `from tasks.t0011_response_visualization_library.code.tuning_curve_viz import ( plot_polar_tuning_curve, plot_cartesian_tuning_curve, plot_angle_raster_psth, plot_multi_model_overlay)`.
* **From [t0012_tuning_curve_scoring_loss_library]**: registered library `tuning_curve_loss`,
  imported as
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import ( TuningCurve, load_tuning_curve, compute_dsi, compute_hwhm_deg, compute_peak_hz, compute_null_hz, compute_reliability)`.
* **From [t0053_minimal_dsgc_spatial_gaba]**: 12 source files copied verbatim into the t0057 `code/`
  directory (per CLAUDE.md rule 3, only registered libraries cross task boundaries via import;
  non-library code must be copied). Also the reference
  `tasks/t0053_minimal_dsgc_spatial_gaba/results/placement_seed0.json` is read by
  `test_placement_seed0_match.py` for the bit-identity check.
* **From [t0055_nmda_mg_block_dsi_recovery]**: `code/run_nrnivmodl.cmd` (12 lines) copied verbatim,
  and `code/neuron_bootstrap.py` (~146 lines) copied with `NMDA_MgBlock` -> `gaba_tonic`
  substitutions.
* **From [t0004_target_tuning_curve]** (indirect via [t0012] / [t0053]): the t0004 target tuning
  curve CSV used as the RMSE reference. Path resolved via `paths.py` (same constant as t0053).

No external download or paid API calls required.

## Expected Assets

* **library: `minimal_dsgc_tonic_gaba_sweep`** — one library asset at
  `tasks/t0057_tonic_gaba_sweep_t0053/assets/library/minimal_dsgc_tonic_gaba_sweep/`. Contains
  `details.json`, `description.md`. Public API surface includes `GABA_BASE_NS_VALUES` constant,
  `gaba_tonic` POINT_PROCESS, `schedule_ei_onsets(*, theta_stim_rad, gaba_base_ns, pairs, ...)`,
  `run_one_trial(*, ..., gaba_base_ns)`, and `run_tuning_curve` script entry point. Component
  structure mirrors `minimal_dsgc_spatial_gaba` (from [t0053]) except the inhibition driver uses the
  new `gaba_tonic` mechanism. Matches `task.json` `expected_assets: {"library": 1}`.

## Time Estimation

* Research: complete (research_code.md done 2026-04-28).
* Implementation (Milestones 1-2, MOD bootstrap + code skeleton port): ~60-90 min.
* Implementation (Milestones 3-4, GABA-mechanism swap + sweep harness + metrics): ~90-120 min.
* Validation (dry-run gate per step 9): ~5 min wall-clock; debugging if gate fails: ~30-60 min worst
  case.
* Full sweep (1800 trials): ~25-30 min wall-clock on local CPU.
* Plotting + library asset creation (Milestone 5): ~30-45 min.
* Verification (verify_plan.py, verify_research_code.py, verify_task_metrics.py, library asset
  verificator): ~5 min.
* Total: ~3.5-5.5 hours including buffer.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| `nrnivmodl` fails on Windows due to missing toolchain or path issue | Medium | Blocking for entire task — without `gaba_tonic.mod` compiled, no simulation can run | Run `code/run_nrnivmodl.cmd` standalone first; verify `code/mod/nrnmech.dll` exists with non-zero size before integrating; if it fails, inspect `nrnivmodl` stderr in detail and fall back to manual invocation of `nrnivmodl.bat`; if still blocked, create an `intervention/missing_neuron_toolchain.md` per the framework intervention mechanism |
| `gaba_tonic.mod` cosine-ramp `BREAKPOINT` introduces integrator instability or NaN currents | Low | Critical — would invalidate every trial and silently produce zero spikes | Smoke-test with a single isolated `h.gaba_tonic` instance and `print(seg.gaba_tonic.i)` over 100 ms before integrating into the full network; if NaN, fall back to piecewise-constant envelope (drop the cosine ramp) — this is the simpler default per the task description's "piecewise constant is acceptable" clause |
| All 5 conductance values produce 0 Hz FULL-mode tuning curves | Medium | Reduces task value but does not invalidate the task — would still produce a publishable null result | The task description explicitly anticipates this scenario by sweeping a 8x range (0.25 to 2.0 nS); document the negative result in `results_detailed.md` and propose extending the sweep to lower values (0.05, 0.1 nS) via a new suggestion |
| All 5 conductance values produce single-spike-degenerate tuning curves (DSI = 1.0 trivially) | Low | Reduces task value but still produces a published curve | Same fallback: report the result, suggest a finer-grained sweep at lower conductances (per task description "Out of Scope" — deferred to a future brainstorm); the dry-run gate (step 9) would catch this early |
| Bit-identical placement seed test fails (test_placement_seed0_match.py) due to numpy version drift | Low | Blocking — invalidates the bit-identity claim against t0052/t0053 | Lock numpy version in `pyproject.toml` matching t0053; if drift detected, inspect each pair's coordinates side-by-side; fall back to relaxing `POSITION_TOLERANCE` to 1e-6 (still semantically meaningful but document the relaxation in the test) |
| 1800-trial sweep exceeds 30 min wall-clock budget significantly (e.g., > 1 hour) | Medium | Delays task delivery but does not invalidate it | Per [t0055] guidance, CVODE `atol = 1e-3` is mandatory; if still too slow, stride-down voltage CSV resolution further (stride-16 instead of stride-8); if still too slow, drop the GABA_ONLY mode for non-headline conductances (keep only at 1.0 nS) |
| IPSP-sustained-window regression fails (v(1300)/v(200) ratio < 0.5) | Medium | Critical — would mean the new mechanism is silently degrading back to event-like behaviour | Inspect raw `voltage_traces_gaba_only.csv` at the failing direction; verify `g_envelope(t)` returns 1.0 in the middle of the window via a print probe; if the window write order is wrong (e.g., `g` set after `t_on` in the wrong sequence), fix the attribute write order in `schedule_ei_onsets`; this gate is the headline t0057 quality criterion |
| AMPA_ONLY peak Hz drifts from 0.667 (REQ-14 regression sentinel fails) | Low | Critical — invalidates the unchanged-AMPA-path invariant | Diff `synapses.py` AMPA branch against t0053 verbatim; verify NetCon weight is 0.5e-3 microsiemens; verify `ampa_netstim.start = onset_ms` is unchanged; if still failing, run a single AMPA_ONLY trial with the t0053 binary versus the t0057 binary back-to-back at theta=0 and bisect |

## Verification Criteria

* **Plan structure**: Run
  `uv run python -m arf.scripts.verificators.verify_plan t0057_tonic_gaba_sweep_t0053`. Expected
  output: 0 errors. (PL-W warnings are acceptable but should be reviewed.)
* **Research-code structure**: Run
  `uv run python -m arf.scripts.verificators.verify_research_code t0057_tonic_gaba_sweep_t0053`.
  Expected output: 0 errors.
* **Library asset**: Run
  `uv run python -m arf.scripts.verificators.verify_assets t0057_tonic_gaba_sweep_t0053`. Expected
  output: 0 errors against `meta/asset_types/library/specification.md`.
* **Task metrics**: Run
  `uv run python -m arf.scripts.verificators.verify_task_metrics t0057_tonic_gaba_sweep_t0053`.
  Expected output: 0 errors; `results/metrics.json` contains 15 variants
  (`gaba_{0.25,0.5,1.0,1.5,2.0}_{full,ampa_only,gaba_only}`) with all four registered metrics
  (`direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
  `tuning_curve_rmse`) populated per variant.
* **Spatial-gating regression**: Run
  `uv run pytest tasks/t0057_tonic_gaba_sweep_t0053/code/test_spatial_gating.py -v`. Expected
  output: 4 passed, 0 failed.
* **Quiescent-rest regression**: Run
  `uv run pytest tasks/t0057_tonic_gaba_sweep_t0053/code/test_quiescent_rest.py -v`. Expected
  output: 1 passed, 0 failed (V_rest = -65 mV +/- 0.5 mV).
* **Placement-seed bit-identity**: Run
  `uv run pytest tasks/t0057_tonic_gaba_sweep_t0053/code/test_placement_seed0_match.py -v`. Expected
  output: 1 passed; all 100 pairs match t0053 `placement_seed0.json` to `POSITION_TOLERANCE = 1e-9`.
  Confirms REQ-5.
* **IPSP-sustained-window regression**: Run
  `uv run pytest tasks/t0057_tonic_gaba_sweep_t0053/code/test_gaba_tonic_envelope.py -v`. Expected
  output: 5 passed (one per conductance value); for each, IPSP voltage at t=1300 ms is at least 50%
  of IPSP voltage at t=200 ms relative to V_rest at theta=210 deg. Confirms REQ-13.
* **AMPA_ONLY no-regression sentinel**: Inspect `results/metrics.json` and confirm every variant
  with `mode = "ampa_only"` has `peak_hz` of approximately 0.6667 Hz (within 1e-3 tolerance) across
  all 5 conductance values. Confirms REQ-14.
* **PNG count**: List `results/images/` and confirm at least 312 PNG files present (5 conductances x
  61 per-conductance PNGs + 6 cross-conductance summary + 1 active-fraction polar). Confirms REQ-9,
  REQ-10, REQ-11.
* **MOD compilation artifact**: Confirm `code/mod/nrnmech.dll` exists with non-zero size after the
  bootstrap; confirm
  `python -c "from neuron import h; h.nrn_load_dll('code/mod/nrnmech.dll'); print(hasattr(h, 'gaba_tonic'))"`
  prints `True`. Confirms REQ-1, REQ-2.
* **Requirement coverage**: Cross-check each `REQ-*` row in `## Task Requirement Checklist` against
  the produced outputs (15-variant `metrics.json`, 312 PNGs, library asset, regression tests). Each
  REQ must have at least one observable artefact in the task folder.
