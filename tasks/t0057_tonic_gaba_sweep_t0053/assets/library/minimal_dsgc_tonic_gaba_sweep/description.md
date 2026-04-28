---
spec_version: "2"
library_id: "minimal_dsgc_tonic_gaba_sweep"
documented_by_task: "t0057_tonic_gaba_sweep_t0053"
date_documented: "2026-04-28"
---
# Minimal DSGC with Tonic GABA Sweep

## Metadata

* **Name**: Minimal DSGC with Tonic GABA Sweep
* **Version**: 0.1.0
* **Task**: `t0057_tonic_gaba_sweep_t0053`
* **Dependencies**: neuron, numpy, matplotlib, pandas, tqdm
* **Modules**: `code/constants.py`, `code/paths.py`, `code/swc_io.py`, `code/neuron_bootstrap.py`,
  `code/cell.py`, `code/placement.py`, `code/synapses.py`, `code/trial.py`,
  `code/run_tuning_curve.py`, `code/render_figures.py`, `code/compute_metrics.py`,
  `code/metrics_extra.py`, `code/mod/GabaTonic.mod`

## Overview

This library implements a minimal compartmental direction-selective ganglion cell (DSGC) on the
project's t0009-calibrated dendritic morphology, with the same per-synapse spatial
centripetal-gating predicate as t0053 but a fundamentally different inhibition mechanism. The GABA
branch's per-event `Exp2Syn` + `NetStim` + `NetCon` triplet is replaced by a single `gaba_tonic`
POINT_PROCESS instance per pair (defined in `code/mod/GabaTonic.mod`), which delivers a sustained
conductance over a configurable `(t_on, t_off)` window per synapse with an optional 1 ms cosine ramp
at each window edge. The amplitude of the tonic conductance is exposed as the public constant
`GABA_BASE_NS_VALUES`, allowing the sweep harness to vary peak conductance from 0.25 to 2.0 nS in
five steps without re-importing.

The library mirrors `minimal_dsgc_spatial_gaba` (from t0053) module-for-module: `cell.py`,
`swc_io.py`, `placement.py`, `metrics_extra.py`, the spatial-gating predicate `i_synapse_fires`, and
the test files are bit-identical apart from import-path rewrites. The two scientifically meaningful
changes are (1) `synapses.py` replaces the GABA branch with the new tonic POINT_PROCESS (no NetStim,
no NetCon for GABA; conductance is set by direct attribute write), and (2) `run_tuning_curve.py`
adds an outer `GABA_BASE_NS_VALUES` loop over the existing `(angle, trial, mode)` triple loop,
threading `gaba_base_ns` through `_run_sweep_for_mode` and `run_one_trial` and adding it as a
leading column to every per-mode CSV. The MOD compilation pipeline (`run_nrnivmodl.cmd` shim +
`ensure_gaba_tonic_compiled` bootstrap) is borrowed verbatim from the t0055 NMDA_MgBlock pattern.

## API Reference

### Public sweep constants (`code/constants.py`)

```python
from tasks.t0057_tonic_gaba_sweep_t0053.code.constants import (
    GABA_BASE_NS_VALUES,
    T_ON_MS,
    T_OFF_MS,
    GABA_RAMP_MS,
)
# GABA_BASE_NS_VALUES = (0.25, 0.5, 1.0, 1.5, 2.0)  # nS
# T_ON_MS = 100.0; T_OFF_MS = 1400.0; GABA_RAMP_MS = 1.0
```

`GABA_BASE_NS_VALUES` is the public sweep parameter consumed by `run_tuning_curve.run_full_sweep`.
Downstream callers can override it by importing the module, rebinding the constant, and re-running
the sweep harness.

### Custom MOD POINT_PROCESS (`code/mod/GabaTonic.mod`)

```text
NEURON {
    POINT_PROCESS gaba_tonic
    RANGE g, e, t_on, t_off, ramp_ms, i
    NONSPECIFIC_CURRENT i
}
```

After `ensure_gaba_tonic_compiled()` is called, the mechanism becomes available as `h.gaba_tonic`.
RANGE attributes are set by direct attribute write: `g` in microsiemens, `e` in mV, `t_on` / `t_off`
/ `ramp_ms` in ms. The conductance envelope is `g * envelope(t)` where envelope is 0 outside
`[t_on, t_off]`, a 1 ms cosine ramp at each window edge, and 1 in the middle.

### Cell builder (`code/cell.py`)

```python
from tasks.t0057_tonic_gaba_sweep_t0053.code.cell import (
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
from tasks.t0057_tonic_gaba_sweep_t0053.code.placement import (
    Location,
    sample_dendritic_locations,
    save_placement_json,
)

locations: list[Location] = sample_dendritic_locations(cell=cell, n_pairs=100, seed=0)
save_placement_json(locations=locations, out_path=Path("placement_seed0.json"))
```

### Tonic-gating drivers (`code/synapses.py`)

```python
from tasks.t0057_tonic_gaba_sweep_t0053.code.synapses import (
    EiPair,
    ScheduleResult,
    build_ei_pairs,
    i_synapse_fires,
    schedule_ei_onsets,
)

pairs: list[EiPair] = build_ei_pairs(
    h=h,
    locations=locations,
    sections=cell.dendrites,
    soma_origin_um=cell.soma_origin_um,
)
result: ScheduleResult = schedule_ei_onsets(
    pairs=pairs,
    angle_deg=210.0,
    velocity_um_per_ms=1.0,
    gaba_base_ns=1.0,
)
```

### Trial runner (`code/trial.py`)

```python
from tasks.t0057_tonic_gaba_sweep_t0053.code.trial import (
    TrialResult,
    run_one_trial,
)

result: TrialResult = run_one_trial(
    h=h,
    cell=cell,
    pairs=pairs,
    mode=TrialMode.FULL,
    angle_deg=210.0,
    trial_seed=1234,
    gaba_base_ns=1.0,
)
```

### Sweep harness (`code/run_tuning_curve.py`)

```python
from tasks.t0057_tonic_gaba_sweep_t0053.code.run_tuning_curve import run_full_sweep

run_full_sweep()  # 1,800 trials; ~25-30 min wall-clock on local CPU under CVODE
```

### Metrics + figures

```python
from tasks.t0057_tonic_gaba_sweep_t0053.code.compute_metrics import main as compute_metrics_main
from tasks.t0057_tonic_gaba_sweep_t0053.code.render_figures import main as render_figures_main

compute_metrics_main()  # writes metrics.json (15 variants) + derived_quantities.json
render_figures_main()   # writes per-(gaba, direction) PNGs + 6 cross-conductance summaries
```

## Usage Examples

```python
from neuron import h
from pathlib import Path

from tasks.t0057_tonic_gaba_sweep_t0053.code.constants import (
    GABA_BASE_NS_VALUES,
    TrialMode,
)
from tasks.t0057_tonic_gaba_sweep_t0053.code.cell import build_dsgc_from_swc
from tasks.t0057_tonic_gaba_sweep_t0053.code.neuron_bootstrap import (
    enable_cvode,
    ensure_gaba_tonic_compiled,
    ensure_neuron_importable,
    load_stdrun,
)
from tasks.t0057_tonic_gaba_sweep_t0053.code.placement import sample_dendritic_locations
from tasks.t0057_tonic_gaba_sweep_t0053.code.synapses import build_ei_pairs
from tasks.t0057_tonic_gaba_sweep_t0053.code.trial import run_one_trial


def run_one_off_trial() -> None:
    """Single trial at theta=210, gaba=1.0 nS, FULL mode."""
    ensure_neuron_importable()
    load_stdrun()
    ensure_gaba_tonic_compiled()
    enable_cvode()

    cell = build_dsgc_from_swc(swc_path=Path("calibrated.swc"))
    locations = sample_dendritic_locations(cell=cell, n_pairs=100, seed=0)
    pairs = build_ei_pairs(
        h=h,
        locations=locations,
        sections=cell.dendrites,
        soma_origin_um=cell.soma_origin_um,
    )
    result = run_one_trial(
        h=h,
        cell=cell,
        pairs=pairs,
        mode=TrialMode.FULL,
        angle_deg=210.0,
        trial_seed=1,
        gaba_base_ns=1.0,
    )
    print(
        f"firing_rate={result.firing_rate_hz:.2f} Hz, "
        f"i_active_fraction={result.i_active_fraction:.3f}",
    )


for gaba_value in GABA_BASE_NS_VALUES:
    print(f"sweep value: {gaba_value:.2f} nS")
```

## Dependencies

* **`neuron`** — single-cell compartmental simulator that provides `h.Section`, `h.Exp2Syn`,
  `h.NetStim`, `h.NetCon`, `h.cvode`, the standard run machinery (`stdrun.hoc`), and the dynamic
  MOD-loading entry point `h.nrn_load_dll`. NEURON is loaded via the `neuron_bootstrap` module's
  Windows-aware initialisation (`NEURONHOME` env var + `os.add_dll_directory`).
* **`numpy`** — array ops for placement sampling, vector-sum DSI, and voltage-trace pivots.
* **`matplotlib`** — figure rendering (per-(gaba, direction) line plots, polar plots, and the 6
  cross-conductance summary PNGs).
* **`pandas`** — CSV I/O and pivot operations in `compute_metrics` and `render_figures`.
* **`tqdm`** — progress bars for the sweep harness.

The library also depends on two registered libraries from prior tasks:
[`tuning_curve_loss`](../../../t0012_tuning_curve_scoring_loss_library/assets/library/tuning_curve_loss/details.json)
(from t0012, used for `compute_dsi`, `compute_hwhm_deg`, etc.), and
[`tuning_curve_viz`](../../../t0011_response_visualization_library/assets/library/tuning_curve_viz/details.json)
(from t0011, used for `plot_polar_tuning_curve`, `plot_cartesian_tuning_curve`,
`plot_angle_raster_psth`).

## Testing

```bash
uv run pytest tasks/t0057_tonic_gaba_sweep_t0053/code/test_spatial_gating.py -v
uv run pytest tasks/t0057_tonic_gaba_sweep_t0053/code/test_quiescent_rest.py -v
uv run pytest tasks/t0057_tonic_gaba_sweep_t0053/code/test_placement_seed0_match.py -v
uv run pytest tasks/t0057_tonic_gaba_sweep_t0053/code/test_gaba_tonic_envelope.py -v
```

Tests cover:

* `test_spatial_gating.py`: 4 tests of the centripetal-gating predicate
  (`cos(radians(theta_stim - theta_centrifugal)) < 0`), including a 1000-sample uniform-random
  active-fraction-near-half check.
* `test_quiescent_rest.py`: 200 ms passive run with no synapses; asserts V_rest = -65 mV +/- 0.5 mV.
* `test_placement_seed0_match.py`: bit-identity check vs the reference t0053 placement
  (`POSITION_TOLERANCE = 1e-9`).
* `test_gaba_tonic_envelope.py`: IPSP-sustained-window regression (REQ-13). For each of the 5
  conductance values, asserts that at the most-active direction (theta = 210 deg),
  `|v(1300 ms) - V_init| >= 0.5 * |v(200 ms) - V_init|`. This gate ensures the new tonic mechanism
  actually sustains inhibition through the stimulus window rather than collapsing early like the
  t0053 Exp2Syn-event mechanism did.

## Main Ideas

* **Conductance amplitude is decoupled from event-decay-tau interactions.** With t0053's `Exp2Syn`
  GABA, the tau2 = 20 ms decay meant the conductance envelope was effectively a 100-200 ms pulse,
  and amplitude affected both peak shunt and total inhibition area inseparably. The new `gaba_tonic`
  mechanism delivers a flat conductance over `(t_on, t_off) = (100 ms, 1400 ms)`, so the sweep over
  `GABA_BASE_NS_VALUES` produces a clean amplitude-vs-suppression curve.
* **Spatial gating predicate is preserved bit-for-bit from t0053.** The
  `cos(radians(theta_stim - theta_centrifugal)) < 0` rule is in `i_synapse_fires` unchanged; the
  `theta_centrifugal_rad = atan2(y - y_soma, x - x_soma)` precomputation in `build_ei_pairs` is
  unchanged; the `placement_seed0.json` matches t0053 at floating-point precision.
* **AMPA path is bit-identical to t0053.** The Exp2Syn rise = 0.5 ms, decay = 2.5 ms, e = 0 mV, peak
  0.5 nS configuration with NetStim + NetCon plumbing is reused verbatim. This is the AMPA_ONLY
  0.667 Hz uniform peak-rate regression sentinel (REQ-14).
* **Custom MOD compilation is automated on Windows.** The `run_nrnivmodl.cmd` shim wraps NEURON's
  `nrnivmodl.bat` for the MinGW toolchain; `ensure_gaba_tonic_compiled` rebuilds the DLL on demand
  and registers it via `h.nrn_load_dll`. This is the t0055 pattern reused.
* **CVODE is mandatory for the 1800-trial sweep budget.** With `atol = 1e-3`, per-trial wall-clock
  drops from ~75 s (fixed-step) to ~3-8 s — the only way the 5 GABA x 12 angles x 10 trials x 3
  modes sweep fits in the ~25-30 min budget on local CPU.

## Summary

The `minimal_dsgc_tonic_gaba_sweep` library extends the t0053 minimal DSGC with a custom tonic GABA
POINT_PROCESS that decouples conductance amplitude from event-decay-tau interactions. The library
exposes `GABA_BASE_NS_VALUES` as a public sweep parameter and writes 15-variant `metrics.json` (5
conductances x 3 modes) plus 312 PNG figures to `tasks/t0057_tonic_gaba_sweep_t0053/results/`. The
new `gaba_tonic.mod` POINT_PROCESS replaces t0053's per-event Exp2Syn + NetStim + NetCon triplet
with direct attribute writes (`g`, `t_on`, `t_off`), and the 1 ms cosine ramp at each window edge
avoids stiff-step integrator artefacts under CVODE.

The library is consumed primarily by `run_tuning_curve.run_full_sweep` (the sweep harness) and the
two analysis scripts (`compute_metrics.main` and `render_figures.main`). Downstream tasks that want
to vary the conductance sweep values can import `GABA_BASE_NS_VALUES` directly. The MOD compilation
pipeline (`ensure_gaba_tonic_compiled`) is reusable as a template for any future custom
POINT_PROCESS shipped with a task; the four test modules cover the spatial-gating predicate, the
quiescent rest gate, the bit-identity placement check, and the headline IPSP-sustained-window
regression.

Known limitations: (a) the MOD compilation requires the NEURON Windows MinGW toolchain at
`C:\Users\md1avn\nrn-8.2.7\bin\nrnivmodl.bat` — Linux/macOS callers need to adapt the shim; (b)
the cosine ramp width is hardcoded to 1 ms via `GABA_RAMP_MS` in `constants.py`; setting
`ramp_ms = 0` on a `gaba_tonic` instance falls back to a piecewise-constant envelope. The library
does not currently support multiple concurrent tonic windows per synapse — only one active window
per pair is honoured.
