---
spec_version: "1"
task_id: "t0047_validate_pp16_fig3_cond_noise"
research_stage: "code"
tasks_reviewed: 9
tasks_cited: 8
libraries_found: 7
libraries_relevant: 3
date_completed: "2026-04-24"
status: "complete"
---
# Research Code: t0047 Validate Poleg-Polsky 2016 Fig 3A-F Conductances and Noise Sweep

## Task Objective

This task wraps t0046's existing `modeldb_189347_dsgc_exact` library to record per-synapse NMDA,
AMPA, and GABA peak conductances (nS) and currents (nA) per direction (PD vs ND) for a gNMDA sweep
that reproduces Poleg-Polsky 2016 Figure 3A-E and Figure 3F bottom (DSI vs gNMDA), then extends
t0046's noise sweep to `flickerVAR in {0.0, 0.1, 0.3, 0.5}` for control / AP5 / 0Mg conditions to
fill the high-noise gap in t0046's Figures 6-8 reproduction. The task does not modify the model; it
only records additional state from the deposited control to enable a simulation-vs-simulation
comparison against the paper's figures. The deliverable is one answer asset
(`polegpolsky-2016-fig3-conductances-validation`) plus seven reproduction PNGs.

## Library Landscape

The library aggregator (`aggregate_libraries.py`) is not present in this worktree's
`arf/scripts/ aggregators/` (only
categories/costs/machines/metric_results/metrics/suggestions/task_types/tasks aggregators are
present in the current branch). I therefore enumerated libraries by walking every
`tasks/*/assets/library/` subfolder containing a `details.json` and reading those files directly.
The `details.json` files were authored under `meta/asset_types/library/specification.md` and carry
the canonical metadata. No correction overlays affect any of the libraries below (verified against
`tasks/*/corrections/*.md`; nothing references the relevant library IDs).

Seven library assets were found:

* `modeldb_189347_dsgc` (created by `[t0008]`) — initial port of the ModelDB 189347 HOC/MOD
  sources. Superseded by t0046's exact reproduction; not used by this task.
* `modeldb_189347_dsgc_gabamod` (created by `[t0020]`) — gabaMOD-swap variant of the t0008 port.
  Superseded by t0046; not used by this task.
* `modeldb_189347_dsgc_dendritic` (created by `[t0022]`) — channel-modification testbed; not
  relevant for a validation-only task.
* `modeldb_189347_dsgc_exact` (created by `[t0046]`) — **PRIMARY DEPENDENCY**. The exact
  reproduction this task wraps. Sources at
  `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/` and
  driver code at `tasks/t0046_reproduce_poleg_polsky_2016_exact/code/`. Library declares
  `entry_points` for `build_dsgc`, `run_one_trial`, `ensure_neuron_importable`, and three scripts
  (`run_all_figures`, `compute_metrics`, `render_figures`). Per the task plan, this task imports
  `run_one_trial` directly via the cross-task package path
  `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun import run_one_trial`,
  which is allowed because the entire `code/` subtree is the implementation of this registered
  library.
* `de_rosenroll_2026_dsgc` (created by `[t0024]`) — independent DSGC model; not used by this
  validation task.
* `tuning_curve_viz` (created by `[t0011]`) — **RELEVANT (limited)**. Importable as
  `from tasks.t0011_response_visualization_library.code.tuning_curve_viz.<module> import ...`.
  Provides `plot_cartesian_tuning_curve`, `plot_polar_tuning_curve`, `plot_multi_model_overlay`,
  `plot_angle_raster_psth`. All four entry points operate on a 12-angle tuning-curve CSV schema;
  this task records only PD + ND (2 directions), so the library cannot directly plot Fig 3A-E
  per-direction conductance bar charts or Fig 3F top PSP traces. The Okabe-Ito palette
  (`MODEL_COLORS` in `tuning_curve_viz/constants.py`) and bootstrap CI helpers
  (`stats.bootstrap_ci`) are still reusable in raw matplotlib code we write for the bar charts and
  trace overlays.
* `tuning_curve_loss` (created by `[t0012]`) — **RELEVANT (limited)**. Importable as
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.metrics import compute_dsi`.
  The `compute_dsi` function requires a `TuningCurve` over 12 angles (`compute_peak_hz` =
  `np.max(rates)`, `compute_null_hz` = rate at index +n/2 from peak). For PD/ND pair input the
  standard `(PD - ND) / (PD + ND)` formula is reproduced one-line in
  `t0046/code/compute_metrics.py:_dsi`; we copy that helper rather than reuse `compute_dsi` because
  constructing a 12-row TuningCurve from a 2-row pair just to call the library is wasteful and
  brittle.

## Key Findings

### Synapse list pattern in the t0046 library is HOC-objref arrays accessed via h.RGC

`build_cell.py` (lines 124-140) and the underlying HOC in
`assets/library/modeldb_189347_dsgc_exact/sources/RGCmodel.hoc` (lines 11, 13, 11835-11848) show
that synapses are stored as **HOC objref arrays** declared on the `RGC` template:

```hoc
public soma,dend,dends,somas,all,ON,OFF,SACinhibsyn,numsyn,BIPsyn,SACexcsyn,countON
objref SACinhibsyn[2],BIPsyn[2],SACexcsyn[2]
...
objref SACinhibsyn[numsyn],SACexcsyn[numsyn],BIPsyn[numsyn]
for ... {
    SACinhibsyn[countn] = new SACinhib(.5)
    SACexcsyn[countn]   = new SACexc(.5)
    BIPsyn[countn]      = new bipNMDA(.5)
}
```

There is **no separate `bipampa` array** — the bipolar AMPA + NMDA synapse is a single dual-
component POINT_PROCESS named `bipNMDA` (the t0046 task description's enumeration of "bipampa,
bipNMDA, SACinhib, SACexc lists" conflated component names with object names). The three synapse
arrays of interest are therefore `BIPsyn[]` (bipNMDA, dual AMPA+NMDA), `SACexcsyn[]` (SACexc,
AMPA-like), and `SACinhibsyn[]` (SACinhib, GABA-A). All three are POINT_PROCESS instances created at
`RGCmodel.hoc:11842-11848`. Iterate from Python via
`for idx in range(int(h.RGC.numsyn)): syn = h.RGC.BIPsyn[idx]` (this exact iteration pattern is
already used in `t0046/code/build_cell.py:read_synapse_coords`).

The synapse objects are created **once** during `init_sim()` (which is called from `build_dsgc()` in
`t0046/code/build_cell.py:100`) and survive every `simplerun()` invocation thereafter. `simplerun()`
calls `placeBIP()` which only re-randomizes `Vinf` playback vectors and `locx`- based start times,
**not** the synapse objects' identities. This means we can attach `Vector.record(syn._ref_g)` once
per (cell, synapse) at process startup and reuse the recorders across all trials [t0046].

### Per-synapse `_ref_g` exposure: every MOD declares `g` as a RANGE variable

I read each of the three relevant MOD files in
`tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/sources/`:

* **`bipolarNMDA.mod`** (POINT_PROCESS `bipNMDA`, lines 12-20): RANGE block declares `g` and
  separately `gAMPA`, `gNMDA`. The BREAKPOINT (line 113) computes `g = gNMDA + gAMPA`. Reversal
  potential PARAMETER `e = 0 (mV)` (line 49). Both AMPA and NMDA share the same reversal (e = 0 mV)
  per the MOD. This is not a hard blocker: we can record `_ref_g` (total) and also `_ref_gAMPA` and
  `_ref_gNMDA` separately, which is exactly what Fig 3A (NMDA) vs Fig 3B (AMPA) wants.

* **`SAC2RGCexc.mod`** (POINT_PROCESS `SACexc`, lines 11-17): RANGE declares `g`, `i`. Reversal
  PARAMETER `e = 0 (mV)` (line 32). BREAKPOINT (line 62) sets `i = (1e-3)*g * (v - e)`. Single
  conductance variable; record `syn._ref_g`.

* **`SAC2RGCinhib.mod`** (POINT_PROCESS `SACinhib`, lines 11-17): RANGE declares `g`, `i`. Reversal
  PARAMETER `e = -65 (mV)` (line 32). NOTE: t0046's `constants.py` records `E_SACINHIB_MV = -60.0`
  because `main.hoc` overrides the MOD default (-65) at module load (`main.hoc` line ~96 per t0046's
  audit). Record `syn._ref_g`; for current computation we use `e_sacinhib = -60` (the main.hoc
  override) per t0046's audit row.

**No hard blocker**: every relevant conductance is exposed as a RANGE variable accessible via
`_ref_<name>` from Python. The only subtlety is that `bipNMDA`'s `g` is the AMPA+NMDA sum; for the
Fig 3A (NMDA) and Fig 3B (AMPA) separate panels we record `_ref_gAMPA` and `_ref_gNMDA` individually
[t0046].

### Reversal potentials per channel for current = g * (V - E_rev)

Pulled from each MOD's PARAMETER block and t0046's `constants.py` audit (which records the
`main.hoc` override where present):

| Channel | MOD default | main.hoc override | Use |
| --- | --- | --- | --- |
| `bipNMDA.e` (AMPA + NMDA, shared) | 0 mV | none | 0 mV |
| `SACexc.e` (AMPA-like) | 0 mV | none | 0 mV |
| `SACinhib.e` (GABA-A) | -65 mV | -60 mV | **-60 mV** (`E_SACINHIB_MV` in t0046 constants) |

The 1e-3 unit conversion in each MOD's BREAKPOINT (`i = (1e-3) * g * (v - e)`) reflects that `g` is
in nS and `v - e` is in mV, giving `i` in nA. We replicate this exact formula offline against the
recorded `g(t)` and `v(t)` traces (no separate `_ref_i` recorder needed; this saves ~8.5 MB per
trial of recording memory). [t0046]

### t0046 `run_one_trial` signature and the right place to attach Vector.record calls

`tasks/t0046_reproduce_poleg_polsky_2016_exact/code/run_simplerun.py:81-188` defines:

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
) -> TrialResult:
```

Returns a `TrialResult` (frozen dataclass) with `peak_psp_mv`, `baseline_mean_mv`, `spike_times_ms`.
The function uses module-level `_CELL_STATE: dict[str, Any]` to cache the built cell across trials;
`_ensure_cell()` builds the cell once via `build_dsgc()` then snapshots synapse coords once. After
each `simplerun()` it asserts BIP positions are still at baseline.

For our wrapper, the crucial observation is: **the synapse POINT_PROCESS objects are created inside
`build_dsgc()` (in HOC's `init_sim()` proc) and persist for the life of the process**. Therefore we
attach `_ref_g` recorders **once after `_ensure_cell()` returns**, before the first
`run_one_trial()` call. The recorders survive all subsequent `placeBIP()` and `run()` cycles because
`placeBIP()` only re-binds `Vinf` playback vectors, not the synapse objects.

We do not need to modify `run_simplerun.py`. We expose two helpers in our wrapper:
`attach_conductance_recorders(*, h) -> ConductanceRecorders` (call once at process start) and
`run_one_trial_with_conductances(*, ...same args as run_one_trial...) -> TrialResultWithConductances`
(calls `run_one_trial`, then reads the recorder vectors after the NEURON `run()` completes inside
`simplerun()` and computes per-class peak conductance and peak current). [t0046]

### NEURON Vector recording at sub-sampled intervals to manage memory

t0046's `run_simplerun.py:114-117` records the soma trace at the **simulation dt** (no second arg to
`Vector.record`):

```python
v_rec: Any = h.Vector()
v_rec.record(h.RGC.soma(0.5)._ref_v)
t_rec: Any = h.Vector()
t_rec.record(h._ref_t)
```

NEURON's `Vector.record(ref, dt_ms)` with an explicit `dt_ms` second argument records at the
specified interval (linear-interpolated to that grid). At `tstop = 1000 ms` and `dt = 0.1 ms`,
recording every dt gives 10001 samples per vector. With ~282 synapses x 3 channels (gAMPA, gNMDA,
gSACexc, gSACinhib — actually 4 record vectors per synapse if we keep gAMPA/gNMDA separate, which
we should for Fig 3A vs 3B) + 1 soma = ~1129 vectors per trial. At 10001 samples each that is ~10.1M
floats = ~81 MB per trial of NEURON-side memory.

Sub-sampling at `dt_record = 0.5 ms` reduces to ~16 MB per trial. The memory cost is per-trial
(vectors are re-emptied or re-created each trial); peak during simulation is what matters. The task
plan estimates ~152 trials but vectors are reset each trial (we extract peak and discard the trace).
Sub-sampling at 0.5 ms is sufficient for peak detection because synaptic conductance time constants
are tens of ms (`tauAMPA = 2 ms` is the only sub-ms-relevant constant; AMPA peaks may be slightly
underestimated at 0.5 ms sampling — to be safe we sub- sample at `dt_record = 0.25 ms`, ~32 MB per
trial, half the AMPA tau). The pattern is: `v.record(syn._ref_g, 0.25)`. [t0046, t0008]

### Reusable t0008 / t0020 / t0022 / t0046 patterns referenced via the library or to copy

Per the cross-task code-reuse rule, we **import** from registered libraries and **copy** anything
else. Since t0046's entire `code/` subtree is the implementation of `modeldb_189347_dsgc_exact`, the
t0046 plan explicitly authorises direct cross-task imports such as
`from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun import run_one_trial`. This
includes `build_cell.py`, `constants.py`, `paths.py`, `neuron_bootstrap.py`, `run_simplerun.py`.
Every BIP-position-baseline guard, NEURONHOME bootstrap, and HOC-safe chdir is therefore reused via
import, not copy. The MOD compile recipe lives at `t0046/code/run_nrnivmodl.cmd` and produces
`t0046/code/sources/nrnmech.dll`; t0047 does **not** recompile MOD files because t0046's
`nrnmech.dll` is already loaded by `build_cell.py:load_neuron` [t0008, t0020, t0022, t0046].

### DSI helper for PD/ND-only data: copy 8-line `_dsi` from t0046, do not adapt t0012's library

`tasks/t0046_reproduce_poleg_polsky_2016_exact/code/compute_metrics.py:117-124` defines:

```python
def _dsi(*, pd_values: list[float], nd_values: list[float]) -> float | None:
    pd_mean: float | None = _mean(pd_values)
    nd_mean: float | None = _mean(nd_values)
    if pd_mean is None or nd_mean is None:
        return None
    if pd_mean + nd_mean == 0.0:
        return 0.0
    return float((pd_mean - nd_mean) / (pd_mean + nd_mean))
```

This is the PD-vs-ND DSI we need both for the conductance DSI (Fig 3A-E) and the PSP DSI (Fig 3F
bottom). t0012's library `compute_dsi` (`tuning_curve_loss/metrics.py:41-47`) requires a 12-angle
`TuningCurve` object and computes peak/null over the full grid; constructing a TuningCurve from two
angles (PD, ND) just to call the library would be brittle (`load_curve` would reject a 2-row CSV:
`_validate_angle_grid` requires `len(angles_deg) == N_ANGLES = 12`). Copy the 8-line `_dsi` helper
into our `code/`. [t0012, t0046]

### Visualisation: t0011 cannot draw Fig 3A-E or 3F top; use raw matplotlib + Okabe-Ito

The four entry points in `tuning_curve_viz` (`plot_cartesian_tuning_curve`,
`plot_polar_tuning_curve`, `plot_multi_model_overlay`, `plot_angle_raster_psth`) all assume a
12-angle tuning curve. Fig 3A-E is a per-direction (PD vs ND) bar chart per channel; Fig 3F top is
mV-vs-ms PSP traces. Neither maps to t0011's API. We write raw matplotlib code in
`code/render_fig3.py` and `code/render_noise_extension.py`, importing only the `MODEL_COLORS`
palette constant from `tuning_curve_viz.constants` (Okabe-Ito) for visual consistency with prior
tasks' figures. For the noise-sweep DSI/AUC vs flickerVAR plots, line plots over flickerVAR per
condition are also raw matplotlib because the x-axis is noise SD, not angle. [t0011]

### t0046 already provides PSP peak, baseline, and DSI machinery — reuse it

`run_simplerun.py:165-188` returns peak PSP, baseline mean, and (for spiking trials) AP times in a
`TrialResult` dataclass. Our wrapper extends this: a `TrialResultWithConductances` dataclass embeds
a `TrialResult` plus seven additional fields (peak_g_NMDA_nS, peak_g_AMPA_nS, peak_g_GABA_nS for the
bipNMDA gNMDA / bipNMDA gAMPA / SACinhib g sums; peak_g_SACexc_nS for the SAC excitatory cholinergic
synapse; and peak_i_nA per channel via offline `i = g * (v - E)` multiplication). [t0046]

### Discrepancy catalogue from t0046 lists 12 paper-vs-code rows; t0047 will append, not replace

`tasks/t0046_reproduce_poleg_polsky_2016_exact/results/results_summary.md:9-29` documents 12
discrepancies including the 282-vs-177 synapse count, 0.5-vs-2.5 nS gNMDA pin, and the noise- driver
re-classification. The `Voff_bipNMDA = 0` (voltage-dependent NMDA in control) was flagged as a
finding worth catching in t0047 specifically; t0046's audit row 35 records the deposited code's
`Voff_bipNMDA = 0` setting in control. Our answer asset's discrepancy catalogue inherits and extends
t0046's, adding any new rows for per-synapse conductance mismatches against Fig 3A-E targets (NMDA
PD ~7 / ND ~5; AMPA PD ~3.5 / ND ~3.5; GABA PD ~12-13 / ND ~30 nS, all per the task description).
[t0046]

## Reusable Code and Assets

### `run_one_trial` and `_ensure_cell` from t0046 driver — **import via library**

* **Source**: `tasks/t0046_reproduce_poleg_polsky_2016_exact/code/run_simplerun.py:81-197`.
* **What it does**: builds the DSGC cell (cached) and runs one drifting-bar trial via
  `h.simplerun(exptype, direction)`, returning
  `TrialResult(peak_psp_mv, baseline_mean_mv, spike_times_ms, ...)`.
* **Reuse method**: **import via library**.
  `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun import run_one_trial, TrialResult`.
* **Function signature**: see Key Findings section "t0046 `run_one_trial` signature".
* **Adaptation needed**: none. We wrap it in
  `code/run_with_conductances.py:run_one_trial_with_conductances(...)` which calls it unmodified,
  then reads the persistent `_ref_g` recorder vectors.
* **Line count**: 197 lines source; 0 lines copied (import-only).

### `build_dsgc`, `_ensure_cell` access pattern, `read_synapse_coords` — **import via library**

* **Source**: `tasks/t0046_reproduce_poleg_polsky_2016_exact/code/build_cell.py:84-140`.
* **What it does**: NEURON bootstrap, HOC source loading, RGC template instantiation; provides
  `read_synapse_coords` to enumerate every BIPsyn / SACinhibsyn / SACexcsyn (locx, locy).
* **Reuse method**: **import via library**.
  `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.build_cell import build_dsgc, read_synapse_coords, assert_bip_positions_baseline`.
* **Function signatures**: `build_dsgc() -> Any (h)`,
  `read_synapse_coords(*, h: Any) -> list[SynapseCoords]`,
  `assert_bip_positions_baseline(*, h: Any, baseline: list[SynapseCoords]) -> None`.
* **Adaptation needed**: none.
* **Line count**: 174 lines source; 0 lines copied.

### `neuron_bootstrap.ensure_neuron_importable` — **import via library**

* **Source**: `tasks/t0046_reproduce_poleg_polsky_2016_exact/code/neuron_bootstrap.py:34-58`.
* **What it does**: Idempotent NEURONHOME / sys.path / DLL-dir bootstrap with re-exec sentinel.
* **Reuse method**: **import via library**.
  `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.neuron_bootstrap import ensure_neuron_importable`.
* **Adaptation needed**: none. The sentinel env var (`_T0046_NEURONHOME_BOOTSTRAPPED`) is
  t0046-namespaced; reusing it from t0047 is safe because the sentinel only prevents an infinite
  re-exec loop, not double-import.
* **Line count**: 58 lines source; 0 lines copied.

### Constants from t0046 (`DT_MS`, `TSTOP_MS`, `V_INIT_MV`, `E_SACINHIB_MV`, etc.) — **import via library**

* **Source**: `tasks/t0046_reproduce_poleg_polsky_2016_exact/code/constants.py`.
* **What it does**: Canonical numeric values from `main.hoc` plus enums (`ExperimentType`,
  `Direction`).
* **Reuse method**: **import via library**.
  `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.constants import DT_MS, TSTOP_MS, V_INIT_MV, E_SACINHIB_MV, ExperimentType, Direction`.
* **Adaptation needed**: none. We add t0047-specific constants (E_BIPNMDA_MV = 0.0, E_SACEXC_MV =
  0.0, the gNMDA sweep grid `(0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0)`, the noise grid
  `(0.0, 0.1, 0.3, 0.5)`, `DT_RECORD_MS = 0.25`) in our own `tasks/t0047.../code/constants.py`.
* **Line count**: 174 lines source; 0 lines copied.

### `_dsi` PD-vs-ND helper — **copy into task** (8 lines)

* **Source**: `tasks/t0046_reproduce_poleg_polsky_2016_exact/code/compute_metrics.py:117-124`.
* **What it does**: `(PD_mean - ND_mean) / (PD_mean + ND_mean)` with None-safety and
  zero-denominator handling.
* **Reuse method**: **copy into task**. Library `compute_dsi` from t0012 requires a 12-angle
  TuningCurve and is not appropriate for 2-direction PD/ND aggregation.
* **Function signature**: `_dsi(*, pd_values: list[float], nd_values: list[float]) -> float | None`.
* **Adaptation needed**: rename to `compute_dsi_pd_nd` for clarity in our `code/dsi.py`.
* **Line count**: 8 lines (plus 7-line `_mean` helper at lines 100-105 — copy both, total ~15
  lines).

### Okabe-Ito palette constant — **import via library**

* **Source**: `tasks/t0011_response_visualization_library/code/tuning_curve_viz/constants.py`.
* **What it does**: `MODEL_COLORS: tuple[str, ...]` colour-blind-safe palette.
* **Reuse method**: **import via library**.
  `from tasks.t0011_response_visualization_library.code.tuning_curve_viz.constants import MODEL_COLORS`.
* **Adaptation needed**: none. Used by raw-matplotlib bar/line/trace plots.
* **Line count**: 1 line imported.

### MOD source files and `nrnmech.dll` — reuse in place via library asset

* **Source**:
  `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/ modeldb_189347_dsgc_exact/sources/`.
* **What it does**: Compiled NEURON mechanism DLL plus six HOC/MOD sources.
* **Reuse method**: **import via library** (effectively — t0046's `build_cell.load_neuron` loads
  `code/sources/nrnmech.dll` via `h.nrn_load_dll`; the library asset is a mirror of
  `code/sources/`). t0047 calls `build_dsgc()` which transparently loads the DLL. No copy or
  re-compile needed.
* **Adaptation needed**: none.

### t0046 `compute_metrics.py:_roc_auc_pd_vs_baseline` — **copy into task** (~20 lines)

* **Source**: `tasks/t0046_reproduce_poleg_polsky_2016_exact/code/compute_metrics.py:142-160`.
* **What it does**: One-sided ROC AUC of PD-trial peaks vs baselines; needed for the noise- sweep
  AUC vs flickerVAR comparison (Fig 7).
* **Reuse method**: **copy into task**. Function is private (`_` prefix) and not exposed via any
  registered library.
* **Function signature**:
  `_roc_auc_pd_vs_baseline(*, pd_values: list[float], baselines: list[float]) -> float | None`.
* **Adaptation needed**: rename to `compute_roc_auc_pd_vs_baseline` and put in `code/scoring.py`.
* **Line count**: ~20 lines.

## Lessons Learned

* **t0046's audit revealed `Voff_bipNMDA = 0` in control** — the deposited control models
  voltage-dependent NMDA with Mg block, while the paper claims biological DSGC NMDA is largely
  voltage-independent. t0046 catalogued this as a discrepancy to revisit; t0047 does not modify the
  model but the conductance recordings will let us see whether the NMDA gNMDA(t) trace shape (slow
  rise, voltage-block dependence) matches the paper's per-synapse claim or diverges in the way t0046
  hypothesised [t0046].

* **t0046's DSI vs gNMDA was non-flat** (0.124 -> 0.204 -> 0.049 -> 0.026 across gNMDA = 0.0, 0.5,
  1.5, 2.5 nS), diverging from the paper's claimed flat ~0.3 line. t0046's `compute_metrics` uses
  2-3 trials per direction; t0047 uses 4 trials per direction per gNMDA value (per task plan), which
  still falls short of the paper's 12-19 (S-0046-01). The gNMDA = 0.5 over-shoot (DSI = 0.204) and
  the 2.5 nS collapse (DSI = 0.026) suggest the synaptic-balance claim itself may be wrong —
  recording per-synapse conductances will let us substantiate this [t0046].

* **HOC objref array iteration via Python is the standard pattern** in this project — t0046's
  `read_synapse_coords` (lines 124-140) iterates
  `for idx in range(int(h.RGC.numsyn)): syn = h.RGC.BIPsyn[idx]` and reads `syn.locx`. The same
  pattern works for `_ref_g`: `vec.record(h.RGC.BIPsyn[idx]._ref_g)` [t0046, t0008].

* **`placeBIP()` does not recreate synapse objects** — it only re-binds `Vinf` Vector.play vectors
  and re-randomises start times. The POINT_PROCESS instances created in `init_sim()` (called from
  `build_dsgc()`) persist for the life of the process. This is what makes our
  attach-once-record-many approach work [t0046].

* **NEURON `Vector.record(ref, dt_ms)` with a sub-sample dt is the standard memory-saver** for
  per-channel recording. t0046 records the soma at the simulation dt because it only has one vector;
  for ~1100 vectors (282 synapses x 4 channels) we must sub-sample. AMPA's 2-ms tau is the binding
  constraint; sub-sampling at 0.25 ms is conservative.

* **Cross-task imports work cleanly when the source is a registered library** — t0046's plan
  explicitly authorises `from tasks.t0046_.../code/run_simplerun import run_one_trial` because the
  entire `code/` subtree implements `modeldb_189347_dsgc_exact`. This avoids a 200-line copy of
  `run_simplerun.py` into t0047 [t0046].

* **t0008/t0020 had cross-task import rule violations** that t0046 fixed by copying `build_cell`
  patterns rather than importing them. t0047 inherits the cleaner approach: the registered- library
  source is imported directly, the per-task helpers (`_dsi`, `_roc_auc_pd_vs_baseline`) are copied
  [t0008, t0020, t0046].

## Recommendations for This Task

1. **Wrapper architecture**: implement `code/run_with_conductances.py` with two public functions:
   `attach_conductance_recorders(*, h: Any, dt_record_ms: float = 0.25) -> ConductanceRecorders`
   (called once at process start, attaches `_ref_g`, `_ref_gAMPA`, `_ref_gNMDA` per synapse) and
   `run_one_trial_with_conductances(*, ...same kwargs as run_one_trial...) -> TrialResultWithConductances`
   (calls `run_one_trial`, then reads recorder vectors and computes per-class peak g and per-class
   peak i = g * (v - E_rev) using the t0046 `E_SACINHIB_MV = -60` and `e = 0` for bipNMDA / SACexc).

2. **Recording strategy**: attach FOUR vector recorders per synapse (`bipNMDA._ref_gAMPA`,
   `bipNMDA._ref_gNMDA`, `SACexc._ref_g`, `SACinhib._ref_g`) plus the soma `_ref_v` recorder
   (already done by `run_one_trial`). Sub-sample at `dt_record_ms = 0.25 ms` (40x reduction vs
   simulation dt = 0.0625 ms is wrong; here `DT_MS = 0.1 ms` per t0046 constants, so 0.25 ms is 2.5x
   sub-sample, still conservative for AMPA's 2-ms tau).

3. **Per-class summing**: at the wrapper return, sum per-class across all 282 synapses at every
   recorded time-step, then compute per-class peak. Report both per-synapse-mean peak g and summed
   peak g in the answer asset's table because the paper's plotting convention (per-synapse vs
   summed) is ambiguous from the figure caption.

4. **DSI helper**: copy t0046's 8-line `_dsi` into `code/dsi.py` as `compute_dsi_pd_nd`. Do NOT
   import t0012's `compute_dsi` (requires 12 angles).

5. **ROC AUC helper**: copy t0046's `_roc_auc_pd_vs_baseline` into `code/scoring.py` as
   `compute_roc_auc_pd_vs_baseline`. Apply per (condition, noise level) cell for the Fig 7
   reproduction.

6. **Visualisation**: write raw matplotlib in `code/render_fig3.py` and
   `code/render_noise_extension.py`. Import only `MODEL_COLORS` from `tuning_curve_viz. constants`
   for palette consistency. Save PNGs to `tasks/t0047.../results/images/` per the seven filenames
   listed in the task description.

7. **Path centralisation**: define all CSV / PNG / asset paths in `tasks/t0047.../code/paths.py`.
   Constants (gNMDA grid, noise grid, `DT_RECORD_MS`, `E_BIPNMDA_MV = 0.0`, `E_SACEXC_MV = 0.0`,
   `E_SACINHIB_MV = -60.0`) in `tasks/t0047.../code/constants.py`. Per the t0046 pattern.

8. **No MOD recompile**: `t0046/code/sources/nrnmech.dll` already has every MOD compiled; do not
   invoke `nrnivmodl`. `build_dsgc()` loads the DLL transparently.

9. **Trial budget**: the task plan estimates ~152 trials at ~5 sec each = ~13 min wall-clock. Memory
   per trial at 0.25 ms sub-sample is ~32 MB of NEURON-side recorder vectors; resetting recorders
   each trial keeps peak RAM bounded.

10. **Discrepancy catalogue carry-forward**: copy t0046's 12-row catalogue into the
    `polegpolsky-2016-fig3-conductances-validation` answer asset's `full_answer.md` and add new rows
    for any per-synapse conductance mismatch outside the +/-25% band. Cite t0046's audit row 35 for
    the `Voff_bipNMDA = 0` finding.

## Task Index

### [t0007]

* **Task ID**: `t0007_install_neuron_netpyne`
* **Name**: Install and validate NEURON 8.2.7 + NetPyNE 1.1.1 toolchain
* **Status**: completed
* **Relevance**: Validated the NEURON 8.2.7 install on Windows that t0046's `nrnmech.dll` and
  `neuron_bootstrap.ensure_neuron_importable` depend on. t0047 inherits the same toolchain via
  t0046's library import.

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: First port of ModelDB 189347 to NEURON 8.2.7 + NetPyNE
* **Status**: completed
* **Relevance**: Original source of the `BIPsyn / SACinhibsyn / SACexcsyn` HOC iteration pattern and
  the soma `_ref_v` recording approach that t0046 inherited and t0047 extends to per-synapse
  `_ref_g`.

### [t0011]

* **Task ID**: `t0011_response_visualization_library`
* **Name**: Tuning-curve visualisation library
* **Status**: completed
* **Relevance**: Provides the `MODEL_COLORS` Okabe-Ito palette and bootstrap CI helpers we reuse via
  library import. Its 12-angle plot APIs do not fit Fig 3A-E (PD vs ND bars) or Fig 3F top (PSP
  traces); raw matplotlib is required for those.

### [t0012]

* **Task ID**: `t0012_tuning_curve_scoring_loss_library`
* **Name**: Tuning-curve scoring / loss library
* **Status**: completed
* **Relevance**: Provides `compute_dsi` for 12-angle tuning curves. We do NOT use it because Fig 3
  records only PD/ND (2 directions); the 8-line PD-vs-ND DSI helper from t0046's
  `compute_metrics.py` is copied instead.

### [t0020]

* **Task ID**: `t0020_port_modeldb_189347_gabamod`
* **Name**: gabaMOD-swap port of ModelDB 189347
* **Status**: completed
* **Relevance**: Origin of the `assert_bip_positions_baseline` BIP-position guard pattern that t0046
  absorbed and t0047 inherits via library import. Confirms the iteration pattern works across
  multiple driver scripts.

### [t0022]

* **Task ID**: `t0022_modify_dsgc_channel_testbed`
* **Name**: DSGC channel-modification testbed
* **Status**: completed
* **Relevance**: Source of the NEURONHOME bootstrap pattern (re-exec sentinel) that t0046's
  `neuron_bootstrap.py` copied. t0047 imports t0046's bootstrap directly; no further copy needed.

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port of De Rosenroll 2026 DSGC model
* **Status**: completed
* **Relevance**: Independent DSGC implementation. Surveyed for completeness; not used by this
  validation task because t0047 explicitly targets ModelDB 189347 / Poleg-Polsky 2016 reproduction,
  not De Rosenroll 2026.

### [t0046]

* **Task ID**: `t0046_reproduce_poleg_polsky_2016_exact`
* **Name**: Exact reproduction of Poleg-Polsky 2016 (ModelDB 189347) with audit
* **Status**: completed
* **Relevance**: Direct dependency. Provides the `modeldb_189347_dsgc_exact` library this task
  wraps, the 12-row paper-vs-code discrepancy catalogue we extend, the `run_one_trial` and
  `build_dsgc` API we import unmodified, the constants module with `E_SACINHIB_MV`, the audit
  conclusion that DSI vs gNMDA is non-flat (motivating this task), and the audit observation that
  `Voff_bipNMDA = 0` in the deposited control.
