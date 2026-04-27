---
spec_version: "2"
library_id: "minimal_dsgc_scalar_gaba"
documented_by_task: "t0052_minimal_dsgc_scalar_gaba"
date_documented: "2026-04-25"
---

# Minimal DSGC with Scalar gabaMOD

## Metadata

* **Name**: Minimal DSGC with Scalar gabaMOD
* **Version**: 0.1.0
* **Task**: `t0052_minimal_dsgc_scalar_gaba`
* **Dependencies**: neuron, numpy, matplotlib, pandas, tqdm
* **Modules**: `code/constants.py`, `code/paths.py`, `code/swc_io.py`,
  `code/neuron_bootstrap.py`, `code/cell.py`, `code/placement.py`, `code/synapses.py`,
  `code/trial.py`, `code/run_tuning_curve.py`, `code/render_figures.py`,
  `code/compute_metrics.py`, `code/metrics_extra.py`

## Overview

This library implements a minimal compartmental direction-selective ganglion cell (DSGC) using
only NEURON built-in mechanisms — `hh`, `pas`, and `Exp2Syn` — and the project's calibrated
baseline morphology from t0009. There is no MOD compilation: the library runs against the stock
NEURON 8.2.7 install on Windows via the same sentinel-guarded `os.execv` re-exec bootstrap used
by t0046. Unlike the deposited Poleg-Polsky 2016 codebase and the t0022 channel-testbed lineage,
the cell here is built from scratch in pure Python so every parameter is auditable.

Direction-dependent inhibition is implemented as a scalar `gabaMOD(theta)` multiplier applied to
every IPSC: `gabaMOD(0 deg) = 0.33` (preferred direction, weak inhibition) and
`gabaMOD(180 deg) = 0.99` (null direction, strong inhibition). The 100 dendritic locations are
sampled by length-weighted uniform sampling with `numpy.random.default_rng(0)` so the placement
is reproducible. Each location hosts one co-located E + I pair driven by single-event `NetStim`
sources; the bar-leading-edge crossing time at the synapse position is the per-trial start time.

The library exposes three trial modes — FULL (E+I), AMPA_ONLY (zeroed GABA NetCons), and
GABA_ONLY (zeroed AMPA NetCons) — so the per-direction aggregate EPSP and aggregate IPSP can be
measured independently of the FULL spiking response. A dry-run validation gate (one angle, two
trials per mode) runs automatically before the full 12 angles x 10 trials x 3 modes = 360-trial
sweep, and aborts the run if AMPA-only at the preferred direction fails to produce spikes.

## API Reference

### `code/cell.py`

```python
@dataclass(frozen=True, slots=True)
class CellHandles:
    soma: Any
    axon_initial_segment: Any
    dendrites: list[Any]
    dendrite_xyz_um: list[tuple[float, float, float, float]]


def build_dsgc_from_swc(*, swc_path: Path) -> CellHandles: ...
def summarize_cell(*, cell: CellHandles) -> CellBuildSummary: ...
```

`build_dsgc_from_swc` parses the calibrated SWC, collapses the 19 soma rows into a single soma
Section (length = sum of segment-to-segment Euclidean distances; diameter = 2 x mean radius),
builds one `h.Section(name=f"dend[{i}]")` per non-soma compartment, attaches a synthetic
`axon_initial_segment` (length 30 um, diameter 2 um, boosted HH gNa = 1.2 S/cm^2, gK =
0.04 S/cm^2, gl_hh = 0.008 S/cm^2, el_hh = -65 mV), inserts `hh` only on soma + AIS, and inserts
`pas` (with `g_pas = 1/Rm`, `e_pas = -65 mV`) on every dendrite. Returns the cell handles plus
per-compartment (x, y, z, length_um) coordinates used for placement.

### `code/placement.py`

```python
@dataclass(frozen=True, slots=True)
class Location:
    section_index: int
    section_x: float
    x_um: float
    y_um: float
    z_um: float


def sample_dendritic_locations(*, cell: CellHandles, n_pairs: int, seed: int) -> list[Location]:
    ...
def save_placement_json(*, locations: list[Location], out_path: Path) -> None: ...
```

`sample_dendritic_locations` builds a cumulative-length array over the dendrite list, samples
`n_pairs` uniform draws in `[0, total_length]` with `numpy.random.default_rng(seed)`, and
resolves each draw to `(section_index, section_x in [0, 1], x_um, y_um, z_um)`.

### `code/synapses.py`

```python
def gaba_mod(*, theta_deg: float, theta_pd_deg: float = 0.0) -> float: ...

def build_ei_pairs(
    *,
    h: Any,
    locations: list[Location],
    sections: list[Any],
) -> list[EiPair]: ...

def schedule_ei_onsets(
    *,
    pairs: list[EiPair],
    angle_deg: float,
    velocity_um_per_ms: float,
    gaba_mod_theta: float,
) -> list[float]: ...
```

`schedule_ei_onsets` computes the bar-leading-edge crossing time at each synapse,
`t_bar = (x*cos(theta) + y*sin(theta)) / velocity + base_offset`, sets each NetStim's `start`,
and writes the per-trial AMPA / GABA NetCon weights (`AMPA_PEAK_NS * 1e-3` and
`GABA_BASE_NS * gaba_mod_theta * 1e-3` in microsiemens).

### `code/trial.py`

```python
class TrialMode(StrEnum):
    FULL = "full"
    AMPA_ONLY = "ampa_only"
    GABA_ONLY = "gaba_only"


def run_one_trial(
    *,
    h: Any,
    cell: CellHandles,
    pairs: list[EiPair],
    mode: TrialMode,
    angle_deg: float,
    trial_seed: int,
) -> TrialResult: ...
```

### `code/run_tuning_curve.py`

```python
def setup_sweep_artifacts() -> SweepArtifacts: ...
def run_dry_run_validation(*, artifacts: SweepArtifacts) -> None: ...
def run_full_sweep(*, voltage_sample_stride: int = 8) -> None: ...
```

The full sweep emits seven CSV outputs: per-mode tuning curves
`(angle_deg, trial_seed, firing_rate_hz)`, per-mode spike times
`(angle_deg, trial_index, spike_time_s)`, per-mode voltage traces
`(angle_deg, trial_seed, sample_idx, t_ms, voltage_mv)`, and a single mode-independent
activation-time CSV `(angle_deg, synapse_index, onset_time_ms)`.

### `code/compute_metrics.py` and `code/metrics_extra.py`

`compute_metrics.main()` is the orchestrator script. It loads the three per-mode tuning curves,
calls the t0012 `tuning_curve_loss` library for `compute_dsi`, `compute_hwhm_deg`,
`compute_reliability`, the t0052 `metrics_extra` library for `compute_vector_sum_dsi` and
`compute_preferred_direction_deg`, and computes the per-direction aggregate EPSP / IPSP peak
somatic deflections from the long-form voltage CSVs. **Hard-fails** with `AssertionError` if the
IPSP gNULL/gPD ratio falls outside `[2.7, 3.3]`; otherwise writes `metrics.json` (explicit
multi-variant format, three variants `full`, `ampa_only`, `gaba_only`) and
`derived_quantities.json` (peak Hz, null Hz, vector-sum DSI, preferred direction, IPSP ratio,
per-direction EPSP / IPSP peaks).

### `code/render_figures.py`

Per-direction figure renderers: `render_soma_voltage_per_direction`, `render_aggregate_epsp`,
`render_aggregate_ipsp`, `render_psth`, `render_activation_histogram`, plus the polar and
Cartesian tuning curves via the t0011 `tuning_curve_viz` library.

## Usage Examples

End-to-end sweep:

```python
from tasks.t0052_minimal_dsgc_scalar_gaba.code.run_tuning_curve import run_full_sweep

# Setup, dry-run gate, full 360 trials, write all CSVs.
run_full_sweep()
```

Build a single trial outside the sweep harness:

```python
from tasks.t0052_minimal_dsgc_scalar_gaba.code.cell import build_dsgc_from_swc
from tasks.t0052_minimal_dsgc_scalar_gaba.code.constants import TrialMode
from tasks.t0052_minimal_dsgc_scalar_gaba.code.neuron_bootstrap import (
    enable_cvode,
    ensure_neuron_importable,
    load_stdrun,
)
from tasks.t0052_minimal_dsgc_scalar_gaba.code.paths import MORPHOLOGY_SWC_PATH
from tasks.t0052_minimal_dsgc_scalar_gaba.code.placement import sample_dendritic_locations
from tasks.t0052_minimal_dsgc_scalar_gaba.code.synapses import build_ei_pairs
from tasks.t0052_minimal_dsgc_scalar_gaba.code.trial import run_one_trial

ensure_neuron_importable()
load_stdrun()
enable_cvode()
from neuron import h

cell = build_dsgc_from_swc(swc_path=MORPHOLOGY_SWC_PATH)
locations = sample_dendritic_locations(cell=cell, n_pairs=100, seed=0)
pairs = build_ei_pairs(h=h, locations=locations, sections=cell.dendrites)
result = run_one_trial(
    h=h,
    cell=cell,
    pairs=pairs,
    mode=TrialMode.FULL,
    angle_deg=0.0,
    trial_seed=1,
)
print(f"firing_rate_hz = {result.firing_rate_hz}")
print(f"n_spikes = {len(result.spike_times_ms)}")
print(f"v_soma_max = {result.v_soma_mv.max():.2f} mV")
```

Compute the gabaMOD scalar at any direction:

```python
from tasks.t0052_minimal_dsgc_scalar_gaba.code.synapses import gaba_mod

print(gaba_mod(theta_deg=0))    # 0.33
print(gaba_mod(theta_deg=90))   # 0.66
print(gaba_mod(theta_deg=180))  # 0.99
```

## Dependencies

* `neuron` — NEURON 8.2.7, imported via the sentinel-guarded bootstrap in
  `code/neuron_bootstrap.py`. Required for `h.Section`, `h.Exp2Syn`, `h.NetStim`, `h.NetCon`,
  `h.finitialize`, `h.continuerun`, and the `hh` / `pas` mechanisms.
* `numpy` — used for length-weighted placement sampling, tuning-curve aggregation, and metric
  computation.
* `matplotlib` — figure rendering for soma V(t), EPSP, IPSP, PSTH, and activation histograms.
* `pandas` — long-form CSV manipulation for voltage traces, spikes, and activation times.
* `tqdm` — progress bars for the 360-trial sweep.

The library does NOT need to compile MOD files; only the NEURON-bundled `hh` and `pas`
mechanisms plus the built-in `Exp2Syn` point process are used.

## Testing

Two pytest-style test modules live in `code/`:

```bash
uv run python -m arf.scripts.utils.run_with_logs --task-id t0052_minimal_dsgc_scalar_gaba -- \
  uv run python -u tasks/t0052_minimal_dsgc_scalar_gaba/code/test_gaba_mod.py

uv run python -m arf.scripts.utils.run_with_logs --task-id t0052_minimal_dsgc_scalar_gaba -- \
  uv run python -u tasks/t0052_minimal_dsgc_scalar_gaba/code/test_quiescent_rest.py
```

`test_gaba_mod.py` checks the two endpoint values: `gaba_mod(0) == 0.33` and
`gaba_mod(180) == 0.99`. `test_quiescent_rest.py` is the **REQ-2 validation gate**: it builds
the cell with no synapses, runs `h.finitialize(-65); h.continuerun(200)`, and asserts that the
final soma voltage is within +/- 0.5 mV of -65 mV. Failure indicates a passive-parameter or
HH-density bug.

## Main Ideas

* **No MOD compilation.** The cell uses only NEURON built-in mechanisms. This eliminates the
  Windows `nrnivmodl` toolchain dependency carried by t0022 / t0046 and keeps the build pipeline
  pure Python.
* **Scalar gabaMOD vs spatial inhibition.** Direction-dependence comes from a single per-trial
  scalar `gabaMOD(theta)` applied uniformly to every IPSC. This is the structurally simplest
  form of de Rosenroll-style direction-selective inhibition; t0053 (the sibling task) implements
  the spatially asymmetric variant.
* **Position-gated event scheduler.** Every E and I synapse fires exactly one event per trial,
  triggered when the bar's leading edge crosses the synapse's (x, y) projected onto the bar's
  normal. There is no E-I offset, no PD/ND branching, and no `noise` on the NetStim — the trial
  is fully deterministic given the placement seed.
* **AIS spike-initiation zone.** With the spec's 100 synapses x 0.5 nS AMPA distributed over
  ~200 ms of bar passage, the somatic depolarisation never reaches the textbook HH threshold
  with default densities (peak v_soma ~ -21 mV). The synthetic AIS is therefore built with
  boosted HH `gnabar` (1.2 S/cm^2) and lower `gkbar` (0.04 S/cm^2), with `gl_hh` and `el_hh`
  tuned so the cell stays at V_rest = -65 +/- 0.5 mV with no input. This is the smallest tuning
  needed to satisfy both REQ-2 (rest gate) and the firing requirements of REQ-9 / REQ-14.
* **CVODE for wall-clock.** The cell has ~6,700 dendritic compartments. With fixed-step
  `dt = 0.025 ms` integration each 1.5 s trial takes ~75 s; with `cvode.active(True)` and
  `atol = 1e-3` it drops to ~3-4 s, bringing the full 360-trial sweep from ~7.5 hours to
  ~25 minutes.

## Summary

This library provides the minimum machinery needed to study how scalar direction-dependent
inhibition shapes a compartmental DSGC's tuning curve: one cell builder, one length-weighted
placement sampler, one position-gated AMPA + GABA driver pair, one trial runner with three
mode toggles, one 12-direction sweep harness with a built-in dry-run validation gate, and one
metrics computer with a hard IPSP-ratio sanity check. All numeric parameters live in
`code/constants.py`; all file paths live in `code/paths.py`. The cell uses only `hh`, `pas`, and
`Exp2Syn` so no MOD compilation is required.

The library is the implementation backbone of t0052. Its sweep CSVs feed the per-direction
figure renderers and the metrics computer; the FULL-mode tuning curve and IPSP ratio are
exported as project-registered metrics for cross-task comparison. The AMPA_ONLY and GABA_ONLY
voltage traces support the per-direction aggregate EPSP and IPSP figures called out in the task
specification.

Limitations: (1) The AIS HH densities are tuned by hand to satisfy REQ-2 and REQ-14
simultaneously; a future task could re-derive these from a Park 2014 firing-rate target. (2)
The placement is uniform across total dendritic length without distal bias; the project's
target tuning curve from t0004 (Park 2014) implies the real cell has more selective synapse
placement, so subsequent tasks may layer placement biases onto this same library. (3) CVODE is
required for an acceptable wall-clock; switching back to fixed-step integration is supported
but raises per-trial wall-clock by ~20x.
