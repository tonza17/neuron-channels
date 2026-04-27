---
spec_version: "2"
library_id: "minimal_dsgc_spatial_gaba"
documented_by_task: "t0053_minimal_dsgc_spatial_gaba"
date_documented: "2026-04-25"
---
# Minimal DSGC with Spatial Centripetal-Gating GABA

## Metadata

* **Name**: Minimal DSGC with Spatial Centripetal-Gating GABA
* **Version**: 0.1.0
* **Task**: `t0053_minimal_dsgc_spatial_gaba`
* **Dependencies**: neuron, numpy, matplotlib, pandas, tqdm
* **Modules**: `code/constants.py`, `code/paths.py`, `code/swc_io.py`, `code/neuron_bootstrap.py`,
  `code/cell.py`, `code/placement.py`, `code/synapses.py`, `code/trial.py`,
  `code/run_tuning_curve.py`, `code/render_figures.py`, `code/compute_metrics.py`,
  `code/metrics_extra.py`

## Overview

This library implements a minimal compartmental direction-selective ganglion cell (DSGC) on the
project's calibrated dendritic morphology, where direction selectivity arises from a per-synapse
spatial firing rule rather than the scalar gabaMOD scaling used in the t0052 sibling task. Each
inhibitory synapse fires only when the moving stimulus has a centripetal component relative to that
synapse's centrifugal axis, defined as `theta_centrifugal_i = atan2(y_i - y_soma, x_i - x_soma)`.
When fired, the I synapse delivers the full 2 nS GABA amplitude with no scalar scaling; when silent,
its NetCon weight is set to zero.

The library mirrors t0052's structure module-for-module (14 of 15 modules are direct copies, adapted
only for import paths and the new sentinel env-var). The two scientifically meaningful extensions
are: (1) `synapses.py` exposes `i_synapse_fires` and a `ScheduleResult` dataclass that carries the
per-pair `i_fired_mask`; (2) `cell.py` exposes `CellHandles.soma_origin_um` so the spatial driver
can compute centrifugal directions. `compute_metrics.py` replaces t0052's hard IPSP-conductance gate
with a soft per-direction active-fraction sanity check (mean across 12 directions expected in
`[0.4, 0.6]`), and `render_figures.py` adds a new `render_active_fraction_polar` function that
produces a closed-polygon polar plot of the active fraction vs direction. Because placement uses the
same fixed seed (0) as t0052, downstream tasks can perform trial-for-trial mechanism comparisons
between the two models on identical synapse positions.

## API Reference

### Cell builder (`code/cell.py`)

```python
from tasks.t0053_minimal_dsgc_spatial_gaba.code.cell import (
    CellHandles,
    build_dsgc_from_swc,
    summarize_cell,
)

cell: CellHandles = build_dsgc_from_swc(swc_path=Path("calibrated.swc"))
# cell.soma                  -> h.Section ("soma" with hh)
# cell.axon_initial_segment  -> h.Section ("axon_initial_segment" with boosted hh)
# cell.dendrites             -> list[h.Section]
# cell.dendrite_xyz_um       -> list[(x, y, z, length_um)]
# cell.soma_origin_um        -> (x, y, z) of the first SWC soma row
```

### Synapse placement (`code/placement.py`)

```python
from tasks.t0053_minimal_dsgc_spatial_gaba.code.placement import (
    Location,
    sample_dendritic_locations,
    save_placement_json,
)

locations: list[Location] = sample_dendritic_locations(cell=cell, n_pairs=100, seed=0)
save_placement_json(locations=locations, out_path=Path("placement_seed0.json"))
```

### Spatial-gating drivers (`code/synapses.py`)

```python
from tasks.t0053_minimal_dsgc_spatial_gaba.code.synapses import (
    EiPair,
    ScheduleResult,
    build_ei_pairs,
    i_synapse_fires,
    schedule_ei_onsets,
)

# Boolean predicate; cos(radians(theta_stim - theta_centrifugal)) < 0
fires: bool = i_synapse_fires(theta_stim_deg=180.0, theta_centrifugal_deg=0.0)  # True

pairs: list[EiPair] = build_ei_pairs(
    h=h,
    locations=locations,
    sections=cell.dendrites,
    soma_origin_um=cell.soma_origin_um,
)

schedule: ScheduleResult = schedule_ei_onsets(
    pairs=pairs,
    angle_deg=180.0,
    velocity_um_per_ms=1.0,
)
# schedule.onset_times_ms: list[float] (one per pair)
# schedule.i_fired_mask:  list[bool]  (True iff that pair's GABA fires)
```

### Trial runner (`code/trial.py`)

```python
from tasks.t0053_minimal_dsgc_spatial_gaba.code.trial import TrialResult, run_one_trial
from tasks.t0053_minimal_dsgc_spatial_gaba.code.constants import TrialMode

result: TrialResult = run_one_trial(
    h=h,
    cell=cell,
    pairs=pairs,
    mode=TrialMode.FULL,
    angle_deg=0.0,
    trial_seed=1,
)
# result.spike_times_ms, result.firing_rate_hz
# result.i_fired_mask, result.i_active_fraction (in [0, 1])
```

### Sweep harness (`code/run_tuning_curve.py`)

```python
from tasks.t0053_minimal_dsgc_spatial_gaba.code.run_tuning_curve import run_full_sweep

run_full_sweep()
# Writes results/tuning_curve_{full,ampa_only,gaba_only}.csv (120 rows each),
# results/spike_times_*.csv, results/voltage_traces_*.csv,
# results/activation_times.csv (1,200 rows with is_fired),
# results/active_fraction_per_direction.csv (12 rows).
```

### Metrics and figures

```python
from tasks.t0053_minimal_dsgc_spatial_gaba.code.metrics_extra import (
    compute_preferred_direction_deg,
    compute_vector_sum_dsi,
)
from tasks.t0053_minimal_dsgc_spatial_gaba.code.render_figures import (
    render_active_fraction_polar,
)

render_active_fraction_polar(
    active_fraction_csv=Path("active_fraction_per_direction.csv"),
    out_dir=Path("results/images"),
)
```

## Usage Examples

End-to-end pipeline from SWC to figures and metrics:

```python
from pathlib import Path

from tasks.t0053_minimal_dsgc_spatial_gaba.code.compute_metrics import main as compute_main
from tasks.t0053_minimal_dsgc_spatial_gaba.code.render_figures import main as render_main
from tasks.t0053_minimal_dsgc_spatial_gaba.code.run_tuning_curve import run_full_sweep

# 1. Run the 360-trial sweep (12 directions x 10 trials x 3 modes).
run_full_sweep()

# 2. Compute the multi-variant metrics.json + derived_quantities.json.
compute_main()

# 3. Render all per-direction figures + the active-fraction polar plot.
render_main()
```

Inspect spatial gating directly:

```python
import numpy as np
from tasks.t0053_minimal_dsgc_spatial_gaba.code.synapses import i_synapse_fires

# Uniform-random centrifugal angles -> ~50% fire at any given stimulus direction.
rng = np.random.default_rng(seed=42)
n: int = 1000
fired: int = sum(
    1 for theta in rng.uniform(0.0, 360.0, n)
    if i_synapse_fires(theta_stim_deg=0.0, theta_centrifugal_deg=float(theta))
)
print(f"active fraction = {fired / n:.3f}")  # ~0.48-0.52
```

## Dependencies

* `neuron` — NEURON 8.2.7 simulator (Windows install at `C:\Users\md1avn\nrn-8.2.7`); imported via
  `code/neuron_bootstrap.py` which sets `NEURONHOME` and DLL paths.
* `numpy` — array math, RNG, vector-sum DSI, tuning-curve aggregation.
* `matplotlib` — all figure rendering (`Agg` backend; no GUI).
* `pandas` — long-form CSV ingestion for the renderers and metrics.
* `tqdm` — sweep progress bar (~360 trials).

The libraries `tasks.t0011_response_visualization_library.code.tuning_curve_viz` and
`tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss` are imported as registered
library assets — not duplicated into this task's `code/`.

## Testing

Three pytest-style test files live under `code/`:

```bash
uv run python -u tasks/t0053_minimal_dsgc_spatial_gaba/code/test_quiescent_rest.py
uv run python -u tasks/t0053_minimal_dsgc_spatial_gaba/code/test_spatial_gating.py
uv run python -u tasks/t0053_minimal_dsgc_spatial_gaba/code/test_placement_seed0_match.py
```

`test_quiescent_rest.py` builds the cell, runs 200 ms with no synapses, and asserts V_rest is within
`+/- 0.5 mV` of -65 mV. `test_spatial_gating.py` checks the three diagnostic angles for
`i_synapse_fires` (PD-side silent, ND-side fires, perpendicular silent) plus a uniform-random
1,000-synapse fraction near 0.5. `test_placement_seed0_match.py` confirms the seed-0 placement JSON
is bit-identical to t0052's; if t0052's file is absent it is silently skipped.

## Main Ideas

* **Spatial-only directional asymmetry**: the GABA mechanism has no scalar amplitude knob. Direction
  selectivity emerges from which subset of I synapses fires, not from how strongly any individual
  synapse fires.
* **Soma-relative centrifugal axis**: each synapse's gating angle is its outward direction from the
  soma origin, computed once at pair construction. Trials only evaluate a cosine sign.
* **Identical placement to t0052**: seed-0 placement reproduces t0052's bit-for-bit, enabling
  trial-for-trial mechanism comparisons in downstream tasks.
* **Soft sanity bounds**: the cross-direction mean active fraction is expected near 0.5; the band
  `[0.4, 0.6]` is informational, not a hard gate. Deviations reflect dendritic-field asymmetry from
  the off-centre soma.
* **No MOD compilation**: every mechanism is a NEURON built-in (`hh`, `pas`, `Exp2Syn`, `NetStim`,
  `NetCon`); the spatial decision is made in Python at scheduling time.

## Summary

The `minimal_dsgc_spatial_gaba` library is the spatial-asymmetry sibling of t0052's
`minimal_dsgc_scalar_gaba`. Both libraries share an identical compartmental cell builder, identical
seed-0 synapse placement, identical Exp2Syn / NetStim / NetCon rigging, and an identical
12-direction by 10-trial by 3-mode (FULL / AMPA_ONLY / GABA_ONLY) sweep harness with the same CSV
schemas. The mechanistic difference lives entirely in `synapses.py`: t0052 modulates every I
synapse's amplitude by a scalar `gaba_mod(theta_stim)` ranging 0.33 -> 0.99 across directions; t0053
makes a per-synapse boolean firing decision based on whether the bar moves centripetally with
respect to that synapse's outward axis from the soma.

The library is consumed by this task's results / suggestions / compare-literature pipelines and is
intended to be the canonical reference implementation for the spatial-asymmetry mechanism in later
tasks. Downstream tasks that want to compare the two mechanisms head-to-head should import both
libraries (registered as cross-task library assets), run them on the shared seed-0 placement, and
use the `tuning_curve_loss` scoring library plus this library's `active_fraction_per_direction.csv`
for diagnostic interpretation.

Limitations: the spatial rule is binary (either full 2 nS or zero, with strict cosine inequality). A
continuous spatial weighting was rejected (the project specification requires the strict half-plane
gate). The model has no axonal channels beyond a synthetic AIS, no GABA-B / NMDA mechanisms, no
noise, and no plasticity. Wall-clock for the full 360-trial sweep is roughly 20 minutes on a modern
CPU thanks to the variable-step CVODE solver.
