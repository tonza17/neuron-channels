---
spec_version: "1"
task_id: "t0048_voff_nmda1_dsi_test"
research_stage: "code"
tasks_reviewed: 8
tasks_cited: 8
libraries_found: 7
libraries_relevant: 1
date_completed: "2026-04-25"
status: "complete"
---
# Research Code: t0048 Voff_bipNMDA=1 DSI vs gNMDA Flatness Test

## Task Objective

This task re-runs t0047's exact 7-point gNMDA sweep
(`b2gnmda in {0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0}` nS, 4 trials per direction per cell, 56 trials
total) but with `exptype = 2` (`Voff_bipNMDA = 1`, voltage-independent NMDA — the deposited "0
Mg2+" condition) instead of t0047's `exptype = 1` control. The goal is to test whether NMDA
voltage-dependence is the mechanistic source of the DSI-vs-gNMDA collapse documented in `[t0047]`'s
answer asset (DSI peaked at 0.19 at gNMDA = 0.5 nS and decayed to 0.018 at gNMDA = 3.0 nS instead of
the paper's claimed flat ~0.30). The deliverable is one answer asset
(`dsi-flatness-test-voltage-independent-nmda`) plus an overlay PNG of `Voff = 1` vs `Voff = 0` DSI
curves and a per-synapse conductance comparison bar chart at gNMDA = 0.5 nS. No model modification
— only an exptype choice swap.

## Library Landscape

The library aggregator (`aggregate_libraries.py`) is not present in this worktree's
`arf/scripts/aggregators/` directory (only `categories`, `costs`, `machines`, `metric_results`,
`metrics`, `suggestions`, `task_types`, and `tasks` aggregators exist on the current branch). I
therefore enumerated libraries by walking every `tasks/*/assets/library/*/details.json` file
directly. No correction overlays affect any of the libraries below (verified against
`tasks/*/corrections/*.md`; nothing references the relevant library IDs).

Seven library assets were found:

* `modeldb_189347_dsgc` (created by `[t0008]`) — initial port of ModelDB 189347. Superseded by
  `[t0046]`'s exact reproduction. Not used by this task.
* `modeldb_189347_dsgc_gabamod` (created by `[t0020]`) — gabaMOD-swap variant of the t0008 port.
  Superseded by `[t0046]`. Not used.
* `modeldb_189347_dsgc_dendritic` (created by `[t0022]`) — channel-modification testbed; not
  relevant for an exptype-choice sweep that mutates nothing in the model.
* `de_rosenroll_2026_dsgc` (created by `[t0024]`) — different DSGC implementation; out of scope
  for a t0046+t0047-only re-sweep.
* `tuning_curve_viz` (created by `[t0011]`) — Matplotlib visualizer keyed off
  12-angle-tuning-curve CSVs. Not relevant: this task plots two-condition (PD/ND) line overlays, not
  a polar / Cartesian tuning curve.
* `tuning_curve_loss` (created by `[t0012]`) — `compute_dsi(curve)` requires a 12-angle
  TuningCurve. Not relevant for the same reason `[t0047]` documented: we have only PD vs ND values,
  and constructing a 12-angle curve to satisfy the API would mask intent.
* `modeldb_189347_dsgc_exact` (created by `[t0046]`) — **PRIMARY DEPENDENCY**. The exact
  reproduction this task wraps. Sources at
  `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/` and
  driver code at `tasks/t0046_reproduce_poleg_polsky_2016_exact/code/`. Library `details.json`
  declares `entry_points` for `build_dsgc`, `run_one_trial`, `ensure_neuron_importable`, and three
  scripts (`run_all_figures`, `compute_metrics`, `render_figures`). Per the t0046 library contract
  (mirrored in `[t0047]`'s plan), this task imports `run_one_trial` directly via the cross-task
  package path `tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun.run_one_trial`.

## Key Findings

### simplerun(exptype, direction) globals at exptype=2

The HOC entry point for every t0046 / t0047 trial is `simplerun($1, $2)`, defined in two identical
copies: the deposited mirror at
`tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/sources/main.hoc:349-368`
and the verbatim re-write at
`tasks/t0046_reproduce_poleg_polsky_2016_exact/code/sources/dsgc_model_exact.hoc:316-334`. Both
copies set the same five condition globals on every call:

* `b2gampa = 0.25` (always)
* `b2gnmda = 0.5 * nmdaOn` (always; t0046's `run_one_trial` overrides this after the call —
  `run_simplerun.py:130-151`)
* `s2ggaba = 0.5` (always)
* `s2gach = 0.5` (always)
* `Voff_bipNMDA = ($1 == 2)` — **0 when exptype != 2, 1 when exptype == 2**
* `gabaMOD = 0.33 + 0.66 * $2` (PD = 0.33, ND = 0.99)
* `achMOD = 0.33` (re-asserted unconditionally; `if ($1 == 3) {achMOD += 0.66 * (1 - $2)}` for
  HIGH_CL only)
* `exptype = 2 - SpikesOn` (rebound from a different field; this is the HOC global named `exptype`,
  distinct from simplerun's `$1` arg — note this aliasing)

What `exptype = 2` does NOT modify versus `exptype = 1`: `b2gampa`, `b2gnmda`, `s2ggaba`, `s2gach`,
`gabaMOD`, `achMOD`, `Vset_bipNMDA` (stays at the canonical -43 from `dsgc_model_exact.hoc:89` /
`main.hoc:104` — **simplerun never rewrites Vset_bipNMDA**), or any channel / cable / morphology
parameter. Conclusion: switching from `ExperimentType.CONTROL` (=1) to `ExperimentType.ZERO_MG` (=2)
flips exactly one variable: `Voff_bipNMDA` from 0 to 1. This is the clean experimental swap the task
hypothesis requires `[t0046]`.

The HOC global `Vset_bipNMDA = -43` (set at module load, `dsgc_model_exact.hoc:89`) is therefore the
value used during `Voff = 1` trials.

### bipolarNMDA.mod BREAKPOINT semantics for Voff

The relevant MOD file is at
`tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/sources/bipolarNMDA.mod`.
Lines 53-54 declare the GLOBALs as PARAMETER defaults: `Voff = 0`
(`0 - voltage dependent 1 - voltage independent`) and `Vset = -60`. The BREAKPOINT block at line 108
implements the mode switch with one line:

```text
local_v = v * (1 - Voff) + Vset * Voff
gNMDA   = (A - B) / (1 + n * exp(-gama * local_v))
```

When `Voff = 0`: `local_v = v` (true membrane potential). Mg block is felt at the local dendrite
voltage. When `Voff = 1`: `local_v = Vset` (a fixed driving voltage), so the
`(1 + n * exp(-gama * local_v))` denominator becomes a constant. `gNMDA` becomes proportional only
to `(A - B)` (the unblocked open-channel kinetics), independent of postsynaptic voltage. The
numerical value at `Vset = -43`, `n = 0.3` (`[t0046]` constants line 65: main.hoc override beats MOD
default 0.25), `gama = 0.07` (constants line 66: main.hoc override beats MOD default 0.08) gives
`1 + 0.3 * exp(-0.07 * -43) = 1 + 0.3 * exp(3.01) = 1 + 6.07 = 7.07`. The voltage-dependent
denominator at `v = -65` is `1 + 0.3 * exp(0.07 * 65) = 1 + 28.7 = 29.7`, i.e. the Voff=1 setting
drives roughly **4.2x larger NMDA conductance** at hyperpolarized voltages than the deposited Voff=0
control [t0046]. This is the mechanism the H1/H2 verdict is testing: at high gNMDA values, Voff=0
has a runaway feedback (more NMDA -> more depolarization -> less Mg block -> more NMDA), and the ND
branch eventually saturates so PD/ND distinction collapses; Voff=1 removes that feedback by clamping
the Mg-block term to a voltage-independent constant.

### The cross-task Python API: run_one_trial and run_one_trial_with_conductances

t0046's Python API for one trial lives in
`tasks/t0046_reproduce_poleg_polsky_2016_exact/code/run_simplerun.py:81-188`. Signature
(keyword-only after the `*`):

```python
def run_one_trial(
    *,
    exptype: ExperimentType,
    direction: Direction,
    trial_seed: int,
    flicker_var: float = 0.0,
    stim_noise_var: float = 0.0,
    b2gnmda_override: float | None = None,
    record_spikes: bool = False,
) -> TrialResult: ...
```

`TrialResult` (frozen dataclass, lines 49-61) carries `peak_psp_mv`, `baseline_mean_mv`,
`b2gnmda_ns`, `flicker_var`, `stim_noise_var`, `spike_times_ms`, plus the (`exptype`, `direction`,
`trial_seed`) inputs. Critically, `run_one_trial` already calls `reset_globals_to_canonical(h=h)`
(line 94) before each trial and includes a post-call rerun loop (lines 130-151) that re-applies
`b2gnmda` if simplerun's unconditional rewrite (`b2gnmda = 0.5 * nmdaOn`) clobbered the override.
Setting `exptype = ExperimentType.ZERO_MG` (value `2`) on every call drives
`simplerun(2, direction)` and therefore `Voff_bipNMDA = 1` for the entire sweep `[t0046]`.

t0047's recorder wraps t0046's runner with per-synapse Vector.record handles. Public callables in
`tasks/t0047_validate_pp16_fig3_cond_noise/code/run_with_conductances.py`:

* `build_cell_and_attach_recorders(*, dt_record_ms=DT_RECORD_MS) -> ConductanceRecorders` (lines
  76-88) — idempotent; calls `_ensure_cell()` (imported from t0046) then
  `attach_conductance_recorders`.
* `attach_conductance_recorders(*, h, dt_record_ms=DT_RECORD_MS) -> ConductanceRecorders` (lines
  91-141) — attaches `Vector.record` to `bip._ref_gAMPA`, `bip._ref_gNMDA`, `sacexc._ref_g`,
  `sacinhib._ref_g` for every synapse plus soma `v` and `t`.
* `run_one_trial_with_conductances(*, recorders, exptype, direction, trial_seed, flicker_var=0, stim_noise_var=0, b2gnmda_override=None, record_spikes=False, return_traces=False) -> TrialResultWithConductances`
  (lines 188-267) — calls `run_one_trial` then computes per-class summed peak g (nS) and peak |i|
  (nA), and resets the recorder vectors at the end.

`TrialResultWithConductances` (frozen dataclass, lines 55-73) wraps the inner `TrialResult` and adds
twelve `peak_g_*` / `peak_i_*` fields plus optional `v_trace_mv` / `t_trace_ms`.

**Confirmed import path for t0048**:

```python
from tasks.t0047_validate_pp16_fig3_cond_noise.code.run_with_conductances import (
    ConductanceRecorders,
    TrialResultWithConductances,
    build_cell_and_attach_recorders,
    run_one_trial_with_conductances,
)
```

`[t0047]`'s own `run_fig3_validation.py` (lines 116-158) demonstrates the pattern: build recorders
once, then call `run_one_trial_with_conductances` in a triple loop over `(gnmda, direction, trial)`.
The same loop structure works for t0048 with one substitution: `exptype=ExperimentType.ZERO_MG`
instead of `exptype=ExperimentType.CONTROL`. The CROSS-TASK RULE (no library / no `assets/library/`
registration for t0047's recorder) requires copying, NOT importing — see Reusable Code section
below.

### DSI helper: signature and provenance

`tasks/t0047_validate_pp16_fig3_cond_noise/code/dsi.py:21-37` defines the canonical DSI helper:

```python
def compute_dsi_pd_nd(
    *,
    pd_values: list[float],
    nd_values: list[float],
) -> float | None: ...
```

Returns `(PD_mean - ND_mean) / (PD_mean + ND_mean)`, or `None` if either input list is empty, or
`0.0` if both means sum to zero. Sourced from
`tasks/t0046_reproduce_poleg_polsky_2016_exact/code/compute_metrics.py:117-124` (the `_dsi` helper,
~12 lines including its `_mean` companion). The file's docstring documents the design choice:
`[t0012]`'s `compute_dsi(curve)` requires a 12-angle TuningCurve, which we cannot construct
meaningfully from PD-vs-ND values alone, so the helper is inlined `[t0047]`. The task description
for t0048 explicitly directs the same inline-copy approach.

### t0047 baseline data schema for the overlay

`tasks/t0047_validate_pp16_fig3_cond_noise/results/data/gnmda_sweep_trials.csv` is the authoritative
`Voff = 0` baseline for the overlay chart `[t0047]`. It contains 56 rows (7 gNMDA values x 2
directions x 4 trials) with the following 17 columns (header verified at
`gnmda_sweep_trials.csv:1`):

`b2gnmda_ns, direction, trial_seed, peak_psp_mv, baseline_mean_mv, peak_g_nmda_summed_ns, peak_g_ampa_summed_ns, peak_g_sacexc_summed_ns, peak_g_sacinhib_summed_ns, peak_g_nmda_per_syn_mean_ns, peak_g_ampa_per_syn_mean_ns, peak_g_sacexc_per_syn_mean_ns, peak_g_sacinhib_per_syn_mean_ns, peak_i_nmda_summed_na, peak_i_ampa_summed_na, peak_i_sacexc_summed_na, peak_i_sacinhib_summed_na`.

`direction` is the string label `"PD"` or `"ND"` (constants `DIRECTION_PD_LABEL` /
`DIRECTION_ND_LABEL` in t0047 constants). To compute DSI per gNMDA from this CSV: read with
`pandas`, filter rows by `b2gnmda_ns`, split by `direction`, pass the seven `peak_psp_mv` values per
side into the inlined `compute_dsi_pd_nd` helper. The schema is sufficient — `peak_psp_mv` is the
canonical PSP amplitude. The same schema also supports the secondary per-synapse conductance
comparison: at `b2gnmda_ns == 0.5`, the `peak_g_nmda_summed_ns` / `peak_g_ampa_summed_ns` /
`peak_g_sacinhib_summed_ns` columns provide the t0047 (Voff=0) numbers to compare against this
task's Voff=1 outputs.

### Trial seed scheme

`[t0047]`'s `_trial_seed_for(*, gnmda_idx, dir_idx, trial)` at
`tasks/t0047_validate_pp16_fig3_cond_noise/code/run_fig3_validation.py:84-85` returns
`1000 * gnmda_idx + 100 * dir_idx + trial`. Reusing this identical formula for t0048 means the PD
trial 0 at gNMDA=0.5 nS (gnmda_idx=1) gets seed `1100` for both `Voff = 0` (t0047) and `Voff = 1`
(t0048). This puts the PD/ND comparisons on identical noise realizations, isolating the Voff effect.
The task plan should adopt this scheme verbatim.

### sweep grid and trials per cell

`tasks/t0047_validate_pp16_fig3_cond_noise/code/constants.py:19, 23` define
`B2GNMDA_GRID_NS = (0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0)` and `TRIALS_PER_CELL = 4`. t0048 should
reuse these exact values (re-declare in its own `constants.py` per the project's
no-cross-task-import-of-non-library-code rule).

### Paper-target overlay constant

`tasks/t0047_validate_pp16_fig3_cond_noise/code/constants.py:54` defines
`DSI_PAPER_FIG3F_TARGET = 0.30` and line 55 defines `DSI_FIG3F_TOLERANCE = 0.05`. The task
description's H1 verdict band ("within +/- 0.05 of some constant") matches this tolerance exactly.
t0048 should re-declare both constants in its own `constants.py` and reuse them when plotting the
horizontal reference line on the overlay PNG and when stating the H0/H1/H2 verdict.

## Reusable Code and Assets

### Imports via library

* `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun import run_one_trial, TrialResult`
  — **import via library** (`modeldb_189347_dsgc_exact`, registered entry point `run_one_trial`
  per `details.json:27-31`). Source:
  `tasks/t0046_reproduce_poleg_polsky_2016_exact/code/run_simplerun.py:81-188`. No adaptation
  needed; pass `exptype=ExperimentType.ZERO_MG` and `b2gnmda_override=<grid value>` per call.
* `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.constants import ExperimentType, Direction, B2GNMDA_CODE, V_INIT_MV, TSTOP_MS, DT_MS`
  — **import via library** (`modeldb_189347_dsgc_exact`, declared module `code/constants.py` per
  `details.json:9`). Source:
  `tasks/t0046_reproduce_poleg_polsky_2016_exact/code/constants.py:138-154` (enums) and lines 24-43
  (timing / conductance constants).
* `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.neuron_bootstrap import ensure_neuron_importable`
  — **import via library** (declared entry point per `details.json:33-37`). Required at the top of
  any script that calls `run_one_trial` because the NEURON import is Windows-fragile.

### Copy into task

* `tasks/t0047_validate_pp16_fig3_cond_noise/code/run_with_conductances.py` — **copy into task**
  as `tasks/t0048_voff_nmda1_dsi_test/code/run_with_conductances.py`. ~340 lines. t0047 is NOT
  registered as a library asset (the recorder is task-internal code; only
  `modeldb_189347_dsgc_exact` is library-registered). Adapt: keep the imports from t0046 unchanged;
  rewrite the `from tasks.t0047...` import in the file's `_smoke_test()` to read from the new t0048
  module path (the smoke-test is optional — t0048 may delete it). Keep every public function:
  `build_cell_and_attach_recorders`, `attach_conductance_recorders`,
  `run_one_trial_with_conductances`, `_peak_summed_g_ns`, `_peak_summed_i_na`, `_reset_recorders`,
  plus dataclasses `ConductanceRecorders` and `TrialResultWithConductances`.
* `tasks/t0047_validate_pp16_fig3_cond_noise/code/dsi.py:21-37` — **copy into task** as
  `tasks/t0048_voff_nmda1_dsi_test/code/dsi.py`. ~37 lines including module docstring. No
  adaptation; the function signature `compute_dsi_pd_nd(*, pd_values, nd_values) -> float | None` is
  exactly what t0048 needs.
* Trial-seed helper from
  `tasks/t0047_validate_pp16_fig3_cond_noise/code/run_fig3_validation.py:84-85` (the function
  `_trial_seed_for`) — **copy into task**, ~2 lines. Identical formula `1000 * gnmda_idx + 100
  * dir_idx + trial` ensures PD/ND noise realizations match t0047 by construction.
* CSV column / direction-label constants from
  `tasks/t0047_validate_pp16_fig3_cond_noise/code/constants.py:19-77` (the `B2GNMDA_GRID_NS`,
  `TRIALS_PER_CELL`, `DT_RECORD_MS`, `E_BIPNMDA_MV`, `E_SACEXC_MV`, `E_SACINHIB_MV_OVERRIDE`,
  `DSI_PAPER_FIG3F_TARGET = 0.30`, `DSI_FIG3F_TOLERANCE = 0.05`, `DIRECTION_PD_LABEL = "PD"`,
  `DIRECTION_ND_LABEL = "ND"`, plus all 17 `COL_*` strings) — **copy into task** as
  `tasks/t0048_voff_nmda1_dsi_test/code/constants.py`. ~80 lines. The same
  `assert E_SACINHIB_MV_OVERRIDE == _T0046_E_SACINHIB_MV` self-check should be preserved.
* The sweep loop pattern from
  `tasks/t0047_validate_pp16_fig3_cond_noise/code/run_fig3_validation.py:116-158` (function
  `_run_gnmda_sweep`) — **copy into task** as part of
  `tasks/t0048_voff_nmda1_dsi_test/code/run_voff1_sweep.py`. ~45 lines. Adapt: change
  `exptype=ExperimentType.CONTROL` to `exptype=ExperimentType.ZERO_MG` on the `runner(...)` call
  (line 143), change the output CSV path constant, change the progress-bar description string. Keep
  every other line.
* Per-trial CSV reader pattern: t0048 must read
  `tasks/t0047_validate_pp16_fig3_cond_noise/results/data/gnmda_sweep_trials.csv` with
  `pandas.read_csv` to compute the t0047 baseline DSI for the overlay. No code to copy — write ~10
  lines of pandas filter/groupby in t0048's `compute_metrics.py`.

### Datasets to read directly

* `tasks/t0047_validate_pp16_fig3_cond_noise/results/data/gnmda_sweep_trials.csv` — 56 rows, 17
  columns, the canonical Voff=0 baseline (see Key Findings for full schema). t0048 reads it via
  absolute path constant in its own `paths.py`. **No correction overlays applied** (verified
  `tasks/*/corrections/*.md` does not reference t0047 results). Read-only.
* `tasks/t0047_validate_pp16_fig3_cond_noise/results/data/dsi_by_gnmda.json` — already-computed
  DSI per gNMDA from `[t0047]`. Optional convenience: t0048 can either re-compute from the CSV
  (preferred for transparency) or read the JSON to avoid duplicating the computation.

## Lessons Learned

* `run_one_trial`'s post-call b2gnmda re-apply loop (`run_simplerun.py:130-151`) is essential:
  `simplerun()` unconditionally writes `b2gnmda = 0.5 * nmdaOn`, so without the explicit re-apply
  our 0.0 / 1.5 / 2.5 / 3.0 nS values would silently get clobbered to 0.5 nS. `[t0046]` encountered
  and fixed this; t0047 inherited the fix; t0048 inherits it again by importing `run_one_trial`. Do
  not bypass this wrapper.
* `[t0047]` learned the hard way that the Mg-block term in the deposited control **dominates the
  high-gNMDA DSI behavior** — DSI peaks at gNMDA = 0.5 nS (0.19) then decays to 0.018 at gNMDA =
  3.0 nS instead of staying near the paper's claimed 0.30. The t0048 hypothesis builds directly on
  this observation: if the Mg-block runaway is the cause, removing it (Voff = 1) should flatten the
  curve.
* `[t0046]`'s `_dsi(*, pd_values, nd_values)` helper (compute_metrics.py:117-124) was duplicated
  inline in `[t0047]`'s `dsi.py` for the same architectural reason: the registered
  `tuning_curve_loss` library `[t0012]` requires a 12-angle TuningCurve, but PD/ND data has only 2
  angles. Re-creating a 12-angle curve to satisfy the API would mask intent. Same decision applies
  to t0048.
* The `DT_RECORD_MS = 0.25` recorder dt in `[t0047]` was deliberately coarser than NEURON's
  `DT_MS = 0.1` simulation dt to keep memory bounded across 282 synapses x 4 channels x 4000 samples
  per trial x 56 trials. Reusing the same value in t0048 is required for memory budget and for
  cross-task comparability of recorded conductance traces.
* `[t0047]`'s recorder pattern uses NEURON `Vector.resize(0)` to flush data between trials rather
  than reattaching new vectors (`run_with_conductances.py:174-185`, `_reset_recorders`). This is the
  canonical NEURON idiom and avoids the "recorder attached after run started" assertion that
  `_peak_summed_g_ns` defends against (lines 152-155).
* The cell is built **once per process** (`run_simplerun.py:64-78`, `_CELL_STATE` cache). This
  matters because rebuilding the 350-section DSGC cell takes seconds; the t0048 sweep should run in
  a single Python process, not parallelized via `ProcessPoolExecutor` (NEURON state is
  process-global and not pickle-friendly).
* Wall-clock at `[t0047]` was about 5 sec/trial * 56 trials = ~5 min for the gNMDA sweep on CPU.
  t0048's sweep is identical cardinality, so the same budget applies.

## Recommendations for This Task

1. **Import** `run_one_trial`, `ExperimentType`, `Direction`, `ensure_neuron_importable`, and the
   relevant timing constants from t0046's `modeldb_189347_dsgc_exact` library. These are
   library-registered entry points (`assets/library/modeldb_189347_dsgc_exact/details.json`) and
   therefore the only legal cross-task imports for t0048.
2. **Copy** `tasks/t0047_validate_pp16_fig3_cond_noise/code/run_with_conductances.py` verbatim into
   `tasks/t0048_voff_nmda1_dsi_test/code/run_with_conductances.py` (with attribution comment naming
   t0047 as the source). Per the project's cross-task code-reuse rule, only library-registered
   assets may be cross-imported; t0047's recorder is task-internal code.
3. **Copy** `tasks/t0047_validate_pp16_fig3_cond_noise/code/dsi.py` verbatim (with attribution
   comment naming t0047 as the source) into `tasks/t0048_voff_nmda1_dsi_test/code/dsi.py`.
4. **Copy and adapt** `_run_gnmda_sweep` from
   `tasks/t0047_validate_pp16_fig3_cond_noise/code/run_fig3_validation.py:116-158` into
   `tasks/t0048_voff_nmda1_dsi_test/code/run_voff1_sweep.py`. The single substantive line change is
   `exptype=ExperimentType.CONTROL` -> `exptype=ExperimentType.ZERO_MG` at the `runner(...)` call.
   Reuse the same `_trial_seed_for` formula so PD/ND realizations match t0047 trial-by-trial.
5. **Reuse** the `B2GNMDA_GRID_NS`, `TRIALS_PER_CELL`, `DSI_PAPER_FIG3F_TARGET`,
   `DSI_FIG3F_TOLERANCE`, `DIRECTION_PD_LABEL`, `DIRECTION_ND_LABEL`, and all `COL_*` constants in
   t0048's `code/constants.py` by copying from t0047's `code/constants.py`. Re-declare the
   `assert E_SACINHIB_MV_OVERRIDE == _T0046_E_SACINHIB_MV` self-check.
6. **Read** `tasks/t0047_validate_pp16_fig3_cond_noise/results/data/gnmda_sweep_trials.csv` via
   absolute path constant to build the overlay chart's Voff=0 curve. Do not duplicate the data into
   t0048; reference it. Apply the same `compute_dsi_pd_nd` helper to compute Voff=0 DSI from this
   CSV and Voff=1 DSI from t0048's freshly written CSV.
7. **Drop** any plan to use `[t0011]`'s `tuning_curve_viz` or `[t0012]`'s `tuning_curve_loss` —
   the data shape (2 directions, 7 gNMDA values, 4 trials each) does not fit the 12-angle
   tuning-curve interface. Hand-write the overlay PNG with `matplotlib.pyplot` directly: x = gNMDA
   grid, y = DSI, two line series (Voff=0 from t0047, Voff=1 from this task) plus a horizontal
   `axhline(0.30, color="grey", linestyle="--", label="paper claim")`.
8. **Verify before sweep**: run a single-trial smoke test at exptype=ZERO_MG, gNMDA=0.5, PD,
   trial_seed=1 and confirm the soma trace is finite and `peak_psp_mv` is in the expected range for
   the 0Mg condition (consult t0046's Fig 5 reproduction in `[t0046]`'s results for sanity). The
   task description flags risk #1 ("unphysical results at high gNMDA"); the smoke test should also
   be repeated at gNMDA=3.0 nS.
9. **Verdict computation**: implement the H0/H1/H2 verdict with two numerical tests: (a) max-min DSI
   range across the 7 grid points (H1 if range <= 0.10, H2 if range < t0047's 0.17 range, H0
   otherwise); (b) linear regression slope of DSI vs `b2gnmda_ns` (H1 if `|slope| < 0.02`, H2 if
   slope < t0047's, H0 otherwise). Record both numbers in the answer asset.

## Task Index

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Initial port of ModelDB 189347 DSGC
* **Status**: completed
* **Relevance**: Original port library; superseded by `[t0046]` and not used directly. Listed for
  library-landscape completeness only.

### [t0011]

* **Task ID**: `t0011_response_visualization_library`
* **Name**: Tuning Curve Visualizer library
* **Status**: completed
* **Relevance**: Surveyed in Library Landscape; the visualizer's polar / Cartesian /
  multi-model-overlay APIs are tuned for 12-angle tuning curves and not applicable to the
  2-direction PD/ND data shape t0048 produces.

### [t0012]

* **Task ID**: `t0012_tuning_curve_scoring_loss_library`
* **Name**: Tuning curve scoring / loss library
* **Status**: completed
* **Relevance**: Provides `compute_dsi(curve)` for 12-angle TuningCurve objects. Documented in
  Lessons Learned as why t0048 inherits `[t0047]`'s decision to inline a 2-angle DSI helper rather
  than synthesize a 12-angle curve.

### [t0020]

* **Task ID**: `t0020_port_modeldb_189347_gabamod`
* **Name**: gabaMOD-swap variant of t0008 port
* **Status**: completed
* **Relevance**: Library-landscape completeness only; superseded by `[t0046]`.

### [t0022]

* **Task ID**: `t0022_modify_dsgc_channel_testbed`
* **Name**: Modify DSGC channel testbed
* **Status**: completed
* **Relevance**: Library-landscape completeness only — its `modeldb_189347_dsgc_dendritic` library
  is a channel-modification testbed and is not used by an exptype-choice sweep.

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC
* **Status**: completed
* **Relevance**: Library-landscape completeness only — its `de_rosenroll_2026_dsgc` library is a
  different DSGC implementation; t0048 stays on the t0046+t0047 stack.

### [t0046]

* **Task ID**: `t0046_reproduce_poleg_polsky_2016_exact`
* **Name**: Exact reproduction of Poleg-Polsky 2016 (ModelDB 189347) with audit
* **Status**: completed
* **Relevance**: **Primary upstream**. Provides the `modeldb_189347_dsgc_exact` library, the HOC
  `simplerun` proc that switches `Voff_bipNMDA` based on exptype, and the Python `run_one_trial`
  wrapper t0048 imports unchanged. Also confirms that exptype=2 is the deposited 0 Mg2+ condition
  and that no other globals beyond Voff are touched.

### [t0047]

* **Task ID**: `t0047_validate_pp16_fig3_cond_noise`
* **Name**: Validate Poleg-Polsky 2016 Fig 3A-F conductances and extend noise sweep
* **Status**: completed
* **Relevance**: **Primary upstream for the recorder pattern, the gNMDA grid, the trial protocol,
  the DSI helper, and the Voff=0 baseline data.** The DSI-vs-gNMDA collapse t0047 documented is
  exactly what t0048 tests the mechanistic explanation of. t0048 copies four files / fragments from
  t0047's code directory (recorder, DSI helper, sweep loop, constants) and reads its
  `gnmda_sweep_trials.csv` for the overlay chart.
