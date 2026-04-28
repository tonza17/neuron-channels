---
spec_version: "2"
library_id: "minimal_dsgc_ampa_nmda_scalar_gaba"
documented_by_task: "t0054_minimal_dsgc_ampa_nmda_scalar_gaba"
date_documented: "2026-04-25"
---
# Minimal DSGC AMPA + NMDA Scalar gabaMOD

## Metadata

* **Name**: Minimal DSGC AMPA + NMDA Scalar gabaMOD
* **Version**: 0.1.0
* **Task**: `t0054_minimal_dsgc_ampa_nmda_scalar_gaba`
* **Dependencies**: neuron, numpy, matplotlib, pandas, tqdm
* **Modules**: `code/constants.py`, `code/paths.py`, `code/swc_io.py`, `code/neuron_bootstrap.py`,
  `code/cell.py`, `code/placement.py`, `code/synapses.py`, `code/trial.py`,
  `code/run_tuning_curve.py`, `code/render_figures.py`, `code/compute_metrics.py`,
  `code/metrics_extra.py`

## Overview

This library extends the t0052 minimal DSGC with a co-located voltage-independent NMDA `Exp2Syn`
(`tau1 = 5 ms`, `tau2 = 80 ms`, `e = 0 mV`) at every E synapse. The peak NMDA conductance `gNMDA` is
swept over `{0.0, 0.25, 0.5, 1.0}` nS in an outer loop wrapping the existing 12-direction ×
10-trial × 3-mode sweep, producing 1,440 trials in total. The trial mode set is renamed: t0052's
`AMPA_ONLY` is replaced by `E_ONLY` (AMPA + NMDA active, GABA zeroed); `GABA_ONLY` zeros both AMPA
and NMDA NetCons; `FULL` keeps everything active.

Direction-dependent inhibition uses the same scalar `gaba_mod(theta)` formula as t0052 (`0.33` at
preferred direction, `0.99` at null direction), so at `gNMDA = 0` the FULL-mode firing rates are
bit-identical to t0052's `tuning_curve_full.csv`. The library enforces this as a hard regression
gate inside `compute_metrics.py`. Placement is bit-identical to t0052/t0053 by reusing the same
length-weighted draw with `numpy.random.default_rng(0)`; a dedicated `test_placement_seed0_match.py`
asserts pair-by-pair equality within `1e-9`.

The library is designed to characterise three quantities as a function of `gNMDA`: (1) the EPSP
decay-to-1/e time at the preferred direction (E_ONLY trace), (2) the FULL-mode peak firing rate, and
(3) the FULL-mode primary and vector-sum DSI. Sweep-summary plots (`epsp_decay_vs_gnmda.png`,
`peak_hz_vs_gnmda.png`, `dsi_vs_gnmda.png`) directly answer these questions.

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

`build_dsgc_from_swc` parses the calibrated SWC, collapses the 19 soma rows into one soma section,
builds one `dend[i]` per non-soma compartment, and attaches a synthetic AIS with boosted HH
densities (`gnabar = 1.2`, `gkbar = 0.04`, `gl = 0.008`, `el_hh = -65 mV`). All dendrites are
passive with `Rm = 5999 Ω·cm²`, `Ra = 100 Ω·cm`, `cm = 1.0 µF/cm²`.

### `code/synapses.py`

```python
@dataclass(frozen=True, slots=True)
class EiPair:
    pair_index: int
    section_index: int
    section_x: float
    x_um: float
    y_um: float
    ampa_syn: Any
    nmda_syn: Any
    gaba_syn: Any
    ampa_netstim: Any
    gaba_netstim: Any
    ampa_netcon: Any
    nmda_netcon: Any
    gaba_netcon: Any


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
    gnmda_ns: float,
) -> list[float]: ...
```

`build_ei_pairs` constructs three `Exp2Syn` mechanisms (AMPA, NMDA, GABA) per location on the same
`seg`. AMPA and NMDA share a single `NetStim` driven by two separate `NetCon` instances — there is
NO second NetStim — so AMPA and NMDA fire at byte-identical times. `schedule_ei_onsets` writes
per-trial weights: AMPA at `AMPA_PEAK_NS × 1e-3` µS, NMDA at `gnmda_ns × 1e-3` µS (so
`gnmda_ns = 0` yields a wired-but-inert mechanism), and GABA at
`GABA_BASE_NS × gaba_mod(theta) × 1e-3` µS.

### `code/trial.py`

```python
class TrialMode(StrEnum):
    FULL = "full"
    E_ONLY = "e_only"
    GABA_ONLY = "gaba_only"


@dataclass(frozen=True, slots=True)
class TrialResult:
    mode: TrialMode
    angle_deg: float
    trial_seed: int
    gnmda_ns: float
    t_ms: np.ndarray
    v_soma_mv: np.ndarray
    spike_times_ms: list[float]
    synapse_onset_times_ms: list[float]
    firing_rate_hz: float
    gaba_mod_theta: float


def run_one_trial(
    *,
    h: Any,
    cell: CellHandles,
    pairs: list[EiPair],
    mode: TrialMode,
    angle_deg: float,
    trial_seed: int,
    gnmda_ns: float,
) -> TrialResult: ...
```

`E_ONLY` zeros only every GABA NetCon (AMPA and NMDA stay scheduled). `GABA_ONLY` zeros both AMPA
and NMDA. The post-trial weight-restore block defensively restores AMPA, NMDA, and GABA back to
their FULL-mode baselines so cross-mode state cannot leak.

### `code/run_tuning_curve.py`

```python
def setup_sweep_artifacts() -> SweepArtifacts: ...
def run_dry_run_validation(*, artifacts: SweepArtifacts, gnmda_ns: float = 0.0) -> None: ...
def run_full_sweep(*, voltage_sample_stride: int = 8) -> None: ...
```

The full sweep iterates the four `gNMDA` values in the outer loop. All four `gNMDA` rows are
appended to a single per-mode CSV (one CSV per mode); each ends up with 4 × 12 × 10 = 480 rows
including the new `gnmda_ns` column. Long-form voltage and spike CSVs likewise gain a `gnmda_ns`
column.

### `code/compute_metrics.py` and `code/metrics_extra.py`

`compute_metrics.main()` groups each per-mode CSV by `gnmda_ns` and writes 12 metrics variants (4
gNMDA × 3 modes) with `variant_id = f"gnmda_{gnmda:.2f}_{mode}"`. Hard-fails with `AssertionError`
if (a) the IPSP conductance ratio `gabaMOD(180)/gabaMOD(0)` is outside `[2.7, 3.3]`, or (b) any
`gnmda_ns = 0` FULL row differs from t0052's `tuning_curve_full.csv` by more than `1e-6` Hz.
`derived_quantities.json` carries per-variant peak Hz / null Hz / vector-sum DSI / preferred
direction / `active_fraction = 1.0`, and per-`gNMDA` `epsp_decay_to_1e_ms` from the E_ONLY trace at
the preferred direction.

### `code/render_figures.py`

Per-direction renderers (`render_soma_voltage_per_direction`, `render_aggregate_epsp`,
`render_aggregate_ipsp`, `render_psth`, `render_activation_histogram`) each loop over
`NMDA_PEAK_NS_VALUES`. Plus per-`gNMDA` polar and Cartesian tuning-curve overviews via the t0011
`tuning_curve_viz` library, and three sweep-summary line plots: `epsp_decay_vs_gnmda.png`,
`peak_hz_vs_gnmda.png`, `dsi_vs_gnmda.png`.

## Usage Examples

End-to-end sweep:

```python
from tasks.t0054_minimal_dsgc_ampa_nmda_scalar_gaba.code.run_tuning_curve import (
    run_full_sweep,
)

# Setup, dry-run gate, full 1,440 trials, write all CSVs.
run_full_sweep()
```

Single trial outside the sweep harness:

```python
from tasks.t0054_minimal_dsgc_ampa_nmda_scalar_gaba.code.cell import build_dsgc_from_swc
from tasks.t0054_minimal_dsgc_ampa_nmda_scalar_gaba.code.constants import TrialMode
from tasks.t0054_minimal_dsgc_ampa_nmda_scalar_gaba.code.neuron_bootstrap import (
    enable_cvode,
    ensure_neuron_importable,
    load_stdrun,
)
from tasks.t0054_minimal_dsgc_ampa_nmda_scalar_gaba.code.paths import MORPHOLOGY_SWC_PATH
from tasks.t0054_minimal_dsgc_ampa_nmda_scalar_gaba.code.placement import (
    sample_dendritic_locations,
)
from tasks.t0054_minimal_dsgc_ampa_nmda_scalar_gaba.code.synapses import build_ei_pairs
from tasks.t0054_minimal_dsgc_ampa_nmda_scalar_gaba.code.trial import run_one_trial

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
    gnmda_ns=0.5,
)
print(f"firing_rate_hz = {result.firing_rate_hz}")
print(f"n_spikes = {len(result.spike_times_ms)}")
print(f"v_soma_max = {result.v_soma_mv.max():.2f} mV")
```

Compute the gabaMOD scalar at any direction (unchanged from t0052):

```python
from tasks.t0054_minimal_dsgc_ampa_nmda_scalar_gaba.code.synapses import gaba_mod

print(gaba_mod(theta_deg=0))    # 0.33
print(gaba_mod(theta_deg=90))   # 0.66
print(gaba_mod(theta_deg=180))  # 0.99
```

## Dependencies

* `neuron` — NEURON 8.2.7, imported via the sentinel-guarded bootstrap in
  `code/neuron_bootstrap.py`. Required for `h.Section`, `h.Exp2Syn`, `h.NetStim`, `h.NetCon`,
  `h.finitialize`, `h.continuerun`, and the `hh` / `pas` mechanisms. Voltage-independent NMDA is
  implemented as a plain `Exp2Syn` so no MOD compilation is needed.
* `numpy` — used for length-weighted placement sampling, tuning-curve aggregation, and metric
  computation (including the gNMDA = 0 regression check).
* `matplotlib` — figure rendering for soma V(t), EPSP, IPSP, PSTH, activation histograms,
  per-gNMDA polar / Cartesian overviews, and the three sweep-summary line plots.
* `pandas` — long-form CSV manipulation for voltage traces, spikes, and activation times,
  including per-gNMDA slicing.
* `tqdm` — progress bars for the 1,440-trial sweep.

The library does NOT need to compile MOD files; only the NEURON-bundled `hh` and `pas` mechanisms
plus the built-in `Exp2Syn` point process are used.

## Testing

Three pytest-style test modules live in `code/`:

```bash
uv run python -m arf.scripts.utils.run_with_logs --task-id t0054_minimal_dsgc_ampa_nmda_scalar_gaba -- \
  uv run python -u tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/code/test_gaba_mod.py

uv run python -m arf.scripts.utils.run_with_logs --task-id t0054_minimal_dsgc_ampa_nmda_scalar_gaba -- \
  uv run python -u tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/code/test_quiescent_rest.py

uv run python -m arf.scripts.utils.run_with_logs --task-id t0054_minimal_dsgc_ampa_nmda_scalar_gaba -- \
  uv run python -u tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/code/test_placement_seed0_match.py
```

`test_gaba_mod.py` checks `gaba_mod(0) == 0.33` and `gaba_mod(180) == 0.99`.
`test_quiescent_rest.py` is the **REQ-2 / REQ-21 validation gate**: with no synapses, the soma must
rest at `-65 ± 0.5 mV` after a 200 ms `continuerun`. `test_placement_seed0_match.py` is the
**REQ-23 validation gate**: per-synapse coordinates in `placement_seed0.json` must match t0052's
within `1e-9`.

## Main Ideas

* **Voltage-independent NMDA via `Exp2Syn`.** The task spec is explicit that this is the minimal
  NMDA — no Mg block, no `n` exponent. We implement it as a plain `Exp2Syn` with `tau1 = 5 ms`,
  `tau2 = 80 ms`, `e = 0 mV` co-located with AMPA. Voltage-dependent NMDA with proper Mg block is
  deferred to a follow-up task.
* **Single shared NetStim per pair drives both AMPA and NMDA.** A second `NetCon` is wired to the
  same `NetStim`. This guarantees AMPA and NMDA fire at byte-identical times and removes one class
  of out-of-sync bugs.
* **Wired-but-inert NMDA at `gNMDA = 0`.** The NMDA `Exp2Syn` is always built; only the per-trial
  `nmda_netcon.weight[0]` is set to zero when `gnmda_ns = 0.0`. This is the cleanest way to satisfy
  the gNMDA = 0 regression gate (results bit-identical to t0052) without conditional construction.
* **All four gNMDA rows in a single per-mode CSV.** Each per-mode CSV gains a `gnmda_ns` column and
  ends up with 480 rows. Downstream analysis groups by `(gnmda_ns, mode)`.
* **Hard regression gate against t0052.** `compute_metrics.py` reloads
  `tasks/t0052_minimal_dsgc_scalar_gaba/results/tuning_curve_full.csv` and asserts every
  `gnmda_ns = 0` row matches within `1e-6` Hz. Failure halts metrics-writing and surfaces the
  offending rows.

## Summary

This library extends the t0052 minimal DSGC with co-located voltage-independent NMDA at every E
synapse and adds a `gNMDA` outer sweep. The cell builder, placement sampler, and gabaMOD scaling are
byte-identical to t0052, so at `gNMDA = 0` the entire FULL-mode tuning curve is guaranteed to
reproduce t0052 row-by-row within floating-point tolerance. Three sweep-summary plots — EPSP
decay-to-1/e vs `gNMDA`, peak Hz vs `gNMDA`, DSI vs `gNMDA` — directly answer the task's headline
questions.

The library is the implementation backbone of t0054. Its sweep CSVs feed the per-direction figure
renderers and the metrics computer; the FULL-mode tuning curve at every `gNMDA` is exported as a
registered metric variant for cross-task comparison. The same modules are importable in any
downstream task that needs an `Exp2Syn`-based AMPA + NMDA + gabaMOD model.

Limitations: (1) NMDA is voltage-independent — there is no Mg block, so the EPSP shape at high
`gNMDA` becomes driving-force-saturated rather than supralinearly amplified. (2) The AIS HH
densities inherited from t0052 produce single-spike trains at most directions even at `gNMDA = 1.0`
nS, so the primary-DSI metric remains in the trivial "1.0 = single-spike" regime in some variants;
vector-sum DSI is reported alongside as a more robust alternative. (3) Placement is uniform over
total dendritic length; spatial bias variants are deferred to follow-up tasks.
