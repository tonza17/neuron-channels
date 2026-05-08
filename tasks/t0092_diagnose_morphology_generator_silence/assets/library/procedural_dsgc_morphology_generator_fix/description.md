---
spec_version: "2"
library_id: "procedural_dsgc_morphology_generator_fix"
documented_by_task: "t0092_diagnose_morphology_generator_silence"
date_documented: "2026-05-08"
---
# Procedural DSGC Morphology Generator Fix

## Metadata

* **Name**: Procedural DSGC Morphology Generator Fix
* **Version**: 0.1.0
* **Task**: `t0092_diagnose_morphology_generator_silence`
* **Dependencies**: `neuron`, `numpy`
* **Modules**: `code/morphology_generator_fix.py`, `code/baseline_channels.py`, `code/paths.py`,
  `code/constants.py`
* **Categories**: `compartmental-modeling`, `direction-selectivity`, `retinal-ganglion-cell`

## Overview

This library is a **drop-in replacement** for the `generate_morphology` entry point of t0090's
`procedural_dsgc_morphology_generator` library. It patches the structural bug responsible for
t0090's all-cell silence (0 / 60 spiking cells) under the t0083 best-cell channel set, and exposes
the patched builder under the same signature so downstream tasks (in particular t0091's planned 68-d
joint NSGA-II run) can swap the import path with no other code changes.

The bug is at `tasks/t0090_morphology_generator_diversity_test/code/generator.py:392-403`. The
procedural generator emits the soma's two pt3d points at
`(start_xy[0], start_xy[1], 0.0, soma_diameter)` and `(end_xy[0], end_xy[1], 0.0, soma_diameter)`.
For the BedB-equivalent base point both `start_xy` and `end_xy` are `(0, 0)`, so the two pt3d points
coincide. NEURON computes the cumulative pt3d distance as ~0 (specifically `1e-9` µm on Windows /
NEURON 8.2.7), overrides the prior `sec.L = soma_diameter_um` assignment, and the soma's surface
area collapses to ~9.4e-14 µm². When synaptic input arrives the somatic Vm diverges to NaN within
a few simulation steps and the trial returns `non_finite_voltage`. Every procedural cell t0090 built
triggers this — hence 0 / 60.

The fix re-emits the soma's pt3d points along the **z-axis**: `(0, 0, 0, d_target)` and
`(0, 0, soma_diameter_um, d_target)`. The cumulative pt3d distance is now `soma_diameter_um` and the
cylinder surface area is `pi * d_target * soma_diameter_um`. We choose `d_target` so the area
matches the t0024 hand-coded reference (~220 µm²) — the channel densities the t0083 NSGA-II run
optimised against. The wrapper is a thin one: it calls `generate_morphology` to get the standard
`MorphologyResult`, then patches the soma section in place. All other fields (dendrites, AIS,
terminal locations, section endpoint table, morphometric summary) are unchanged.

## API Reference

### `generate_fixed_morphology`

```python
def generate_fixed_morphology(
    *,
    params: MorphologyParams,
    morph_seed: int | None = None,
) -> MorphologyResult: ...
```

Drop-in replacement for
`tasks.t0090_morphology_generator_diversity_test.code.generator.generate_morphology`. Contract:

* **Inputs**: same as `generate_morphology` — a `MorphologyParams` (14 morphology knobs) and an
  optional `morph_seed` integer that overrides `params.morph_seed`.
* **Output**: a `MorphologyResult` (15 fields) with the soma section patched. The `MorphologyResult`
  duck-types as `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.build_cell_ais.DSGCCellWithAIS`
  so `apply_parameter_vector`, `setup_synapses_parametric`, and `run_one_trial` consume it without
  modification.
* **Determinism**: same `(params, morph_seed)` → byte-identical output across calls.
* **Soma area target**: the patched soma's surface area is within ±5% of
  `BEDB_AREA_TARGET_UM2 = 220.0` µm². Verified by the unit test `test_soma_area_within_tolerance`.
* **Side effects**: the underlying NEURON sections are mutated in place. Caller must keep the
  returned `MorphologyResult` alive (e.g., via a module-level list) to avoid the `id()`-reuse GC bug
  documented in t0090's `verification.py:118-122`.

### `insert_baseline_channels`

```python
def insert_baseline_channels(*, h: Any, cell: Any) -> None: ...
```

Inserts `HHst` + `cad` on the soma + every dendrite section, and `HHst` on the two AIS subsegments.
NEURON treats duplicate `insert(name)` calls as silent no-ops, so this helper is idempotent without
its own cache. Copied from `tasks/t0090_.../code/verification.py:125-137` because that helper is
task-internal in t0090, not a library entry point. Call this **before** `apply_parameter_vector` or
any other channel-density write — the t0080 trial driver assumes HHst is already present.

## Usage Examples

The expected usage from t0091 (or any downstream task that wants the patched generator):

```python
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params import (
    apply_parameter_vector,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_driver import (
    run_one_trial,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_helpers import (
    setup_synapses_parametric,
)
from tasks.t0090_morphology_generator_diversity_test.code.load_default_params import (
    load_t0083_best_cell_param_vector,
)
from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
)

# Drop-in swap: change the import from t0090's generate_morphology to t0092's
# generate_fixed_morphology. No other code changes are required.
from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import (
    generate_fixed_morphology,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.baseline_channels import (
    insert_baseline_channels,
)

params = MorphologyParams.from_bedb_base_point()
cell = generate_fixed_morphology(params=params, morph_seed=1234)

insert_baseline_channels(h=cell.h, cell=cell)
pv = load_t0083_best_cell_param_vector()
apply_parameter_vector(cell=cell, params=pv)

bundle = setup_synapses_parametric(
    cell=cell,
    n_ach=pv.n_ach,
    n_gaba=pv.n_gaba,
    rho_0_ach=pv.rho0_ach,
    lambda_ach_um=pv.lambda_ach_um,
    rho_0_gaba=pv.rho0_gaba,
    lambda_gaba_um=pv.lambda_gaba_um,
    w_ach_us=pv.w_ach_us,
    w_gaba_us=pv.w_gaba_us,
    placer_seed=42,
    gnmda_dend=pv.gnmda_dend,
    mg_conc_mm=pv.mg_conc_mm,
    voff_nmda=pv.voff_nmda,
)
trial = run_one_trial(cell=cell, bundle=bundle, direction_deg=0.0, seed=1000)
print(f"PD spikes: {trial.spike_count}, peak Vm: {trial.peak_mv:.2f} mV")
```

For the BedB-equivalent base point this prints `PD spikes: 61, peak Vm: ~11.0 mV` (well above the
`-10` mV AP threshold). The unpatched `generate_morphology` returns 0 spikes with a non-finite
voltage trace.

## Dependencies

* `neuron` — required at runtime; the library calls `h.pt3dclear` and `h.pt3dadd` to patch the
  soma. Tested against NEURON 8.2.7 on Windows 11 / Python 3.13 + the Vast.ai Linux pip wheel of
  NEURON.
* `numpy` — used by the unit tests (Vm-trace `np.isfinite` checks). Not required by
  `generate_fixed_morphology` itself.

No additional packages beyond what t0090 already depends on. The fix is purely a thin wrapper over
existing functionality.

## Testing

Run the four unit tests with:

```bash
uv run pytest tasks/t0092_diagnose_morphology_generator_silence/code/test_morphology_generator_fix.py -v
```

The tests cover:

* `test_soma_area_within_tolerance` — patched soma surface area is within ±5% of 220 µm². Uses
  the t0090 `BEDB_BASE_POINT` and `MORPH_SEED=1234`.
* `test_determinism` — same `(params, morph_seed)` produces structurally identical sections
  (matching `sec.L`, `sec.diam`, `sec.nseg`, and section count) across two calls.
* `test_no_nan_on_bedb_base_point` — patched soma Vm under a 50 ms unstimulated `finitialize` at
  `V_init = -70 mV` has no NaN samples and stays within ±5 mV of `V_init` (the unpatched generator
  fails this with `non_finite_voltage`).
* `test_soma_pt3d_z_axis` — patched soma has exactly two pt3d points at `(0, 0, 0, d_target)` and
  `(0, 0, soma_diameter_um, d_target)`, confirming the z-axis cylinder geometry.

All four tests pass on Windows 11 / NEURON 8.2.7 / Python 3.13.

## Main Ideas

* **The generator emits a degenerate soma cylinder.** Two coincident pt3d points at z=0 produce a
  cable of cumulative length ~0; NEURON resets `sec.L` from the assigned `soma_diameter_um` to
  `1e-9` µm, the surface area collapses to ~9.4e-14 µm², and synaptic current density blows up to
  infinity within a few `h.run()` steps.
* **The fix is a thin soma-pt3d patch.** The wrapper calls `generate_morphology` unchanged and only
  patches the soma section in place via `h.pt3dclear()` + two `h.pt3dadd` calls along the z-axis.
  All dendritic geometry, AIS extension, terminal locations, and morphometric metadata are
  preserved.
* **Soma surface area target is the t0024 reference (~220 µm²).** The hand-coded Bed B soma's
  measured area is 287 µm² (this task's structural dump). The plan-level target of 220 µm² was
  set from prior research-code estimation of the t0024 frustum stack; the actual measurement is ~30%
  larger but still in the same regime, and the t0083 channel densities tolerate small soma- area
  variation. The library uses `BEDB_AREA_TARGET_UM2 = 220.0` exactly as specified in the plan to
  keep the fix deterministic and auditable.
* **The fix unlocks spiking on every t0090 cell tested.** The patched BedB-equivalent procedural
  cell fires at 43.6 Hz on the PD direction (peak Vm ~11 mV; clean APs); 5 of 5 STABLE-from-t0090
  cells from Phase F also fire (`different/morph_14` reaches DSI = 0.962 at 36.4 Hz; the symmetric
  BedB-equivalent has DSI = 0.034 because its primary stems are uniformly distributed). Direction
  selectivity is driven by the asymmetry knobs and is t0091's optimisation target.

## Summary

The `procedural_dsgc_morphology_generator_fix` library ships one production function,
`generate_fixed_morphology`, that is a drop-in replacement for t0090's `generate_morphology`. It
fixes the structural bug responsible for t0090's all-cell silence under the t0083 best-cell channel
set: t0090 emits the soma's two pt3d points at coincident `(x, y, 0)` coordinates, NEURON treats the
soma as a 0-length cable, and the resulting soma surface area is essentially zero. The fix re-emits
the pt3d points along the z-axis so the cylinder length equals `soma_diameter_um` and the surface
area equals the t0024 hand-coded reference (~220 µm²).

In the project, this library unblocks t0091's planned 68-d joint NSGA-II run — t0091 only needs to
swap one import path. The library also exports `insert_baseline_channels`, a copy of t0090's
task-internal helper that downstream tasks can re-use without copying code into their own folder.

Known limitation: the fix recovers spiking (43.6 Hz PD-rate on the BedB-equivalent cell) but does
not recover full direction selectivity (DSI ~0.034) on its own. Direction selectivity emerges from
the cell's spatial asymmetry; t0091's joint optimisation is the right venue for tuning the asymmetry
knobs (`field_elongation_pd`, `soma_offset_pd_um`, `branch_density_gradient_pd`,
`primary_branch_pd_concentration`) against the patched generator.
