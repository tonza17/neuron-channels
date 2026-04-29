---
spec_version: "2"
library_id: "minimal_dsgc_bar_locked_gaba_ampa_sweep"
documented_by_task: "t0059_bar_locked_gaba_ampa_sweep_t0057"
date_documented: "2026-04-29"
---
# Minimal DSGC with Bar-Arrival-Locked Tonic GABA + AMPA Sweep

## Metadata

* **Name**: Minimal DSGC with Bar-Arrival-Locked Tonic GABA + AMPA Sweep
* **Version**: 0.1.0
* **Task**: `t0059_bar_locked_gaba_ampa_sweep_t0057`
* **Dependencies**: neuron, numpy, matplotlib, pandas, tqdm
* **Modules**: `code/constants.py`, `code/paths.py`, `code/swc_io.py`, `code/cell.py`,
  `code/placement.py`, `code/synapses.py`, `code/trial.py`, `code/run_tuning_curve.py`,
  `code/compute_metrics.py`, `code/render_figures.py`, `code/metrics_extra.py`,
  `code/neuron_bootstrap.py`, `code/mod/GabaTonic.mod`

## Overview

This library forks `minimal_dsgc_tonic_gaba_sweep` (from task `t0057_tonic_gaba_sweep_t0053`) and
applies three bundled changes on the same calibrated DSGC morphology that t0052 / t0053 / t0057 have
used:

1. **Per-synapse bar-arrival-locked GABA window.** The global tonic window
   `(t_on, t_off) = (100, 1400)` ms in t0057 is replaced by a per-synapse window
   `t_on_i = (x_i cos theta + y_i sin theta) / v + 100 ms`, `t_off_i = t_on_i + WINDOW_MS` (ms),
   gated by the same centripetal-gating predicate from t0053. The `gaba_tonic.mod` POINT_PROCESS is
   **unchanged** — only the Python caller writes different attribute values per pair per trial.

2. **EPSP_PASSIVE / IPSP_PASSIVE measurement protocol fix (S-0055-01).** The legacy `AMPA_ONLY` /
   `GABA_ONLY` modes are replaced by `EPSP_PASSIVE` / `IPSP_PASSIVE`. Both passive modes save and
   zero the HH `gnabar` / `gkbar` conductances on the soma and axon initial segment (dendrites have
   no HH mechanism), then run the trial, and restore via try/finally. This guarantees the soma trace
   is the pure synaptic envelope (no spikes), which downstream metrics need for the EPSP-decay
   quantity to be well-defined.

3. **5x5 (gAMPA, GABA_BASE_NS) sweep.** The previously hard-coded `AMPA_PEAK_NS = 0.5 nS` is
   replaced by a public `AMPA_PEAK_NS_VALUES = (0.5, 1.0, 2.0, 3.0, 4.0)` constant; the GABA sweep
   values are also rebound to `(0.1, 0.2, 0.5, 1.0, 2.0)`. Total trial budget: 5 x 5 x 12 x 10 x 3 =
   9,000 trials.

The trial length is also standardised at `TSTOP_MS = 1400.0` ms (was 1500 ms in t0057), per the
S-0055-01 protocol specification.

## API Reference

### `code/constants.py`

```python
TSTOP_MS: float = 1400.0
WINDOW_MS: float = 200.0
AMPA_PEAK_NS_VALUES: tuple[float, ...] = (0.5, 1.0, 2.0, 3.0, 4.0)
GABA_BASE_NS_VALUES: tuple[float, ...] = (0.1, 0.2, 0.5, 1.0, 2.0)

class TrialMode(StrEnum):
    FULL = "full"
    EPSP_PASSIVE = "epsp_passive"
    IPSP_PASSIVE = "ipsp_passive"
```

### `code/synapses.py`

```python
def i_synapse_fires(*, theta_stim_deg: float, theta_centrifugal_deg: float) -> bool:
    """cos(radians(theta_stim - theta_centrifugal)) < 0 (strict; perpendicular silent)."""

def build_ei_pairs(
    *,
    h: Any,
    locations: list[Location],
    sections: list[Any],
    soma_origin_um: tuple[float, float, float],
) -> list[EiPair]:
    """One AMPA Exp2Syn + one h.gaba_tonic per Location."""

def schedule_ei_onsets(
    *,
    pairs: list[EiPair],
    angle_deg: float,
    velocity_um_per_ms: float,
    gampa_ns: float,
    gaba_base_ns: float,
) -> ScheduleResult:
    """Set AMPA NetStim.start, AMPA NetCon.weight[0] = gampa_ns * 1e-3, and per-pair tonic GABA
    (g, t_on, t_off) where t_on_i is the bar-arrival time and t_off_i = t_on_i + WINDOW_MS."""
```

### `code/trial.py`

```python
@dataclass(frozen=True, slots=True)
class HhConductanceSnapshot:
    soma_gnabar: list[float]
    soma_gkbar: list[float]
    ais_gnabar: list[float]
    ais_gkbar: list[float]


def _save_and_zero_hh(*, cell: CellHandles) -> HhConductanceSnapshot:
    """Save HH conductances on every soma + AIS segment, then zero them."""

def _restore_hh(*, cell: CellHandles, snapshot: HhConductanceSnapshot) -> None:
    """Restore HH conductances; always called from try/finally."""

def run_one_trial(
    *,
    h: Any,
    cell: CellHandles,
    pairs: list[EiPair],
    mode: TrialMode,
    angle_deg: float,
    trial_seed: int,
    gampa_ns: float,
    gaba_base_ns: float,
) -> TrialResult:
    """One trial; for passive modes, HH is saved-and-zeroed inside a try/finally."""
```

### `code/run_tuning_curve.py`

```python
def setup_sweep_artifacts() -> SweepArtifacts:
    """Bootstrap NEURON, build cell, place synapses, build EI pairs."""

def run_dry_run_validation(
    *,
    artifacts: SweepArtifacts,
    gampa_ns: float = 1.0,
    gaba_base_ns: float = 0.5,
) -> None:
    """1 angle x 2 trials x 3 modes dry-run gate at the centre grid cell."""

def run_full_sweep(*, voltage_sample_stride: int = 8) -> None:
    """Full 9000-trial sweep across the 5x5 (gampa, gaba) grid."""
```

### `code/compute_metrics.py` and `code/render_figures.py`

Each is invokable as a module
(`uv run python -u -m tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.compute_metrics`) after the
sweep produces the per-mode CSVs. `compute_metrics` writes `results/metrics.json` (75 variants) and
`results/derived_quantities.json`; `render_figures` writes 1225 per-cell PNGs plus the 6 cross-grid
heatmaps and the regime-boundary contour overlay.

## Usage Examples

End-to-end sweep:

```python
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.run_tuning_curve import run_full_sweep

run_full_sweep()
# Outputs:
#   results/tuning_curve_full.csv (300 rows)
#   results/tuning_curve_epsp_passive.csv (300 rows)
#   results/tuning_curve_ipsp_passive.csv (300 rows)
#   results/spike_times_*.csv, results/voltage_traces_*.csv
#   results/active_fraction_per_direction.csv (12 rows)
#   results/placement_seed0.json, results/wallclock.json
```

Single trial at a single grid cell:

```python
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.constants import TrialMode
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.run_tuning_curve import (
    setup_sweep_artifacts,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.trial import run_one_trial

artifacts = setup_sweep_artifacts()
from neuron import h
result = run_one_trial(
    h=h,
    cell=artifacts.cell,
    pairs=artifacts.pairs,
    mode=TrialMode.FULL,
    angle_deg=180.0,
    trial_seed=1,
    gampa_ns=2.0,
    gaba_base_ns=0.5,
)
print(result.firing_rate_hz, result.i_active_fraction)
```

Just the dry-run gate from the CLI:

```bash
uv run python -u -m tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.run_tuning_curve --dry-run
```

## Dependencies

* **neuron** — compartmental simulation kernel; the C runtime is loaded via the `neuron_bootstrap`
  helpers and the custom POINT_PROCESS is compiled by `nrnivmodl`.
* **numpy** — array math; required by `placement.py` (length-weighted sampling) and `trial.py`
  (V(t) traces).
* **matplotlib** — figure rendering; `Agg` backend used in batch mode.
* **pandas** — CSV I/O and pivot operations in `compute_metrics.py` and `render_figures.py`.
* **tqdm** — progress bars during the 9000-trial sweep.

The library also imports two registered cross-task libraries (`tuning_curve_loss` from t0012 and
`tuning_curve_viz` from t0011); these are listed as task dependencies in `task.json` rather than
under `dependencies` here because they are intra-repo and resolve via the `tasks.tNNNN_*.code.*`
import path.

## Testing

Run all five regression tests:

```bash
uv run pytest tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/code/test_*.py -v
```

What each test covers:

* **`test_quiescent_rest.py`** — passive 200 ms run with no synapses; soma rests at
  `V_INIT_MV = -65 mV +/- 0.5 mV`.
* **`test_spatial_gating.py`** — 4 unit tests of the centripetal-gating predicate.
* **`test_placement_seed0_match.py`** — bit-identity vs t0057's seed-0 placement
  (`POSITION_TOLERANCE = 1e-9`).
* **`test_bar_locked_ipsp_envelope.py`** — bar-arrival-locked IPSP centre-of-mass shift between
  `theta = 0` and `theta = 90` exceeds the predicted lower bound (REQ-13).
* **`test_hh_save_and_zero.py`** — runs one EPSP_PASSIVE trial then one FULL reference trial; the
  FULL trace must match the stored reference at `atol = 1e-6` mV (REQ-14). On first run, the test
  writes the reference and skips comparison.

## Main Ideas

* **Bar-locked windows are a one-line change at the synapse layer.** The `gaba_tonic.mod`
  POINT_PROCESS already exposes per-instance `t_on` / `t_off` RANGE attributes; the t0057 -> t0059
  surgical edit is replacing two constant writes in `schedule_ei_onsets` with
  `(onset_ms, onset_ms + WINDOW_MS)`. This is the cleanest possible direction-dependent IPSP timing
  within the same simulation substrate.
* **HH save-and-zero is per-segment and try/finally-wrapped.** NEURON's `seg.hh.gnabar` is
  segment-scoped, so the snapshot iterates `for seg in section`. Dendrites have no HH mechanism and
  must NOT be touched. The try/finally guarantees HH is restored even if the integrator raises
  mid-trial — without this, a single bad trial would silently disable HH for the rest of the
  9000-trial sweep.
* **CVODE is mandatory for the 9000-trial sweep.** With `cvode.atol = 1e-3`, per-trial wall-clock
  drops from ~75 s (fixed-step at dt = 0.025 ms) to ~3-8 s. Without CVODE, the sweep would take ~7.8
  days; with CVODE, ~8.75 h on local CPU.
* **Placement seed 0 is bit-identical to t0052 / t0053 / t0057.** This is the project's invariant
  for cross-task comparability — the `test_placement_seed0_match.py` test guards it at
  floating-point precision (1e-9 tolerance).
* **No correction overlays are needed.** Both DOI- and downstream-task-corrections paths in the
  parent are already in their canonical state; t0059 forks the substrate, not the metadata.

## Summary

`minimal_dsgc_bar_locked_gaba_ampa_sweep` is a forked, surgically-edited version of t0057's
minimal-DSGC tonic-GABA library. The fork replaces t0057's global GABA window with a per-synapse
bar-arrival-locked window, swaps the legacy `AMPA_ONLY` / `GABA_ONLY` measurement modes for an
HH-save-and-zero `EPSP_PASSIVE` / `IPSP_PASSIVE` pair, and exposes `gAMPA` as a public per-synapse
parameter so the simulation can sweep a 5x5 (gAMPA, GABA_BASE_NS) grid in one go. The library is the
substrate for the t0059 task's experiment-run: 9000 trials produce a 75-variant `metrics.json` and a
1233-PNG figure set, with the headline question being whether any operating point on the (gAMPA,
GABA_BASE_NS) plane produces direction-selective multi-spike firing.

The library inherits t0057's MOD compilation pipeline (`run_nrnivmodl.cmd` + `GabaTonic.mod`)
unchanged — the headline change is in Python (where it belongs), not in NEURON's C kernel. This
keeps the integration surface narrow and the cross-task bit-identity guarantees (placement seed,
AMPA path, HH parameters) intact.

Downstream tasks consuming this library can either run the full sweep, sweep a sub-grid by
restricting `AMPA_PEAK_NS_VALUES` and `GABA_BASE_NS_VALUES`, or call `run_one_trial` directly for
one-off perturbation experiments. The HH save-and-zero is exposed via `_save_and_zero_hh` /
`_restore_hh` so derived libraries that wrap their own simulation harnesses can opt into the
S-0055-01 protocol fix without re-implementing it.
