---
spec_version: "2"
library_id: "de_rosenroll_2026_dsgc"
documented_by_task: "t0024_port_de_rosenroll_2026_dsgc"
date_documented: "2026-04-21"
---
# de Rosenroll 2026 DSGC

A port of the de Rosenroll, Sethuramanujam, Tukker & Awatramani (2026, *Cell Reports*)
direction-selective retinal ganglion cell (DSGC) model, DOI `10.1016/j.celrep.2025.116833`, into
this project. The source companion repository is
`https://github.com/geoffder/ds-circuit-ei-microarchitecture` at commit
`a23f642aa6557a23a51bf76f51e420e8149773fa` (MIT license), vendored under `sources/` here.

## Metadata

* **Name**: de Rosenroll 2026 DSGC
* **Version**: 0.1.0
* **Task**: `t0024_port_de_rosenroll_2026_dsgc`
* **Dependencies**: `neuron`, `numpy`, `pandas`
* **Modules**: `code/ar2_noise.py`, `code/build_cell.py`, `code/constants.py`, `code/paths.py`,
  `code/plot_tuning_curves.py`, `code/run_tuning_curve.py`, `code/score_envelope.py`
* **Vendored sources**: `sources/RGCmodelGD.hoc`, `sources/HHst_noiseless.mod`,
  `sources/cadecay.mod`, `sources/Exp2NMDA.mod`, `sources/nrnmech.dll`
* **Upstream commit**: `a23f642aa6557a23a51bf76f51e420e8149773fa`
* **Upstream license**: MIT (see `sources/LICENSE`)

## Overview

This library wraps the de Rosenroll et al. 2026 NEURON-based DSGC model behind a project-friendly
Python API and a moving-bar tuning-curve driver. The upstream code is a 2,500-line research codebase
that bundles the DSGC morphology (`RGCmodelGD.hoc`, 341 sections), three custom NEURON mechanisms
(`HHst_noiseless.mod`, `cadecay.mod`, `Exp2NMDA.mod`), and a Python driver (`ei_balance.py`,
`SacNetwork.py`) that simulates correlated SAC ACh/GABA co-release onto the DSGC's terminal
dendrites. The library vendors the HOC template and MOD mechanisms verbatim, compiles them into a
Windows `nrnmech.dll`, and provides a simplified Python re-implementation of the release-noise model
and moving-bar protocol that captures the paper's headline finding: that correlated ACh/GABA release
within each SAC terminal produces stronger direction selectivity than decorrelated release (the AMB
/ ambient-ACh control).

The simplified driver in this library replaces the upstream's full SAC varicosity network
(`bp_locs`, per-direction release probability matrix `probs`, per-synapse angle deltas `deltas`)
with a single global GABA release probability that varies sigmoidally with bar direction, plus an
AR(2) release-rate noise process whose ACh/GABA cross-channel correlation is the correlated /
uncorrelated knob. This is sufficient to reproduce the qualitative correlated-vs-uncorrelated DSI
contrast but does not aim to match the paper's absolute DSI magnitudes exactly.

## API Reference

### `code/ar2_noise.py`

```python
def generate_ar2_batch(
    *,
    n_samples: int,
    n_streams: int,
    phi: tuple[float, float],
    rho: float,
    seed: int,
    innov_scale: float = 1.0,
) -> np.ndarray
```

Vectorised AR(2) release-rate noise generator. Returns an array of shape `(n_streams, n_samples, 2)`
containing two correlated AR(2) processes per stream, with AR coefficients `phi` (default
`(0.9, -0.1)` per plan REQ-1) and Pearson cross-channel correlation `rho`. `rho = 0.6` reproduces
the paper's correlated condition; `rho = 0.0` is the AMB / decorrelated control. Backed by
`numpy.random.default_rng(seed)` for reproducibility.

```python
def generate_ar2_process(
    *,
    n_samples: int,
    phi: tuple[float, float],
    rho: float,
    seed: int,
    innov_scale: float = 1.0,
) -> np.ndarray
```

Single-stream wrapper that returns `generate_ar2_batch(..., n_streams=1)[0]` for callers that only
need one channel pair.

### `code/build_cell.py`

```python
def load_neuron() -> Any
```

Bootstraps NEURON 8.2.7: appends the local install's `cp313` bindings to `sys.path`, sets
`NEURONHOME`, imports `neuron.h`, loads the vendored `nrnmech.dll`, and explicitly sources
`stdrun.hoc` from the local install. Returns the `h` namespace.

```python
def build_dsgc_cell() -> DSGCCell
```

Loads `RGCmodelGD.hoc`, instantiates `h.DSGC(0, 0)`, walks the dendrite tree to partition sections
into primary / non-terminal / terminal, applies plan-pinned HHst Na/K densities and M-type-K
densities per compartment class (soma `gnabar=0.15`, primary `gnabar=0.20`, terminal `gnabar=0.03`,
all in S/cm^2), and returns a `DSGCCell` frozen dataclass.

```python
@dataclass(frozen=True, slots=True)
class DSGCCell:
    h: Any
    rgc: Any
    soma: Any
    all_dends: list[Any]
    primary_dends: list[Any]
    non_terminal_dends: list[Any]
    terminal_dends: list[Any]
    terminal_locs_xy: NDArray[np.float64]
    origin_xy: tuple[float, float]
```

### `code/run_tuning_curve.py` (script)

CLI:
`python -m tasks.t0024_port_de_rosenroll_2026_dsgc.code.run_tuning_curve --mode {preflight,full} [--limit-per-angle N]`.

Drives moving-bar sweeps over both 8-direction and 12-angle grids x {correlated, uncorrelated}
release conditions. Writes one CSV per condition to `data/` with columns
`(trial, direction_deg, spike_count, peak_mv)`. The `--mode preflight` flag runs only the
8-direction correlated sweep for sanity checking before the full ~30-50 minute run.

### `code/score_envelope.py` (script)

CLI: `python -m tasks.t0024_port_de_rosenroll_2026_dsgc.code.score_envelope`.

Reads the four sweep CSVs, converts them to the canonical t0012 schema
`(angle_deg, trial_seed, firing_rate_hz)`, scores the 12-angle correlated curve against the t0004
envelope via `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.score_curves`,
evaluates the REQ-5 port-fidelity gate, and writes `data/score_report.json` plus
`results/metrics.json`. On gate miss it also writes `intervention/port_fidelity_miss.md` as a
first-class finding (per plan step 13).

### `code/plot_tuning_curves.py` (script)

CLI: `python -m tasks.t0024_port_de_rosenroll_2026_dsgc.code.plot_tuning_curves`.

Renders polar and Cartesian PNGs for all four sweep CSVs into `results/images/` by delegating to
`tasks.t0011_response_visualization_library.code.tuning_curve_viz.{polar,cartesian}`.

## Usage Examples

### End-to-end: build the cell, run one trial, count spikes

```python
from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import build_dsgc_cell
from tasks.t0024_port_de_rosenroll_2026_dsgc.code.run_tuning_curve import (
    _setup_synapses,
    run_single_trial,
)

cell = build_dsgc_cell()
bundle = _setup_synapses(cell=cell, gaba_weight_scale=1.0)
result = run_single_trial(
    cell=cell,
    ncs_ach=bundle.ncs_ach,
    ncs_gaba=bundle.ncs_gaba,
    direction_deg=0.0,
    rho=0.6,
    seed=42,
)
print(f"spikes={result.spike_count}  peak={result.peak_mv:+.1f} mV")
```

### Standalone AR(2) noise generation

```python
from tasks.t0024_port_de_rosenroll_2026_dsgc.code.ar2_noise import generate_ar2_batch

trace = generate_ar2_batch(
    n_samples=1000,
    n_streams=177,
    phi=(0.9, -0.1),
    rho=0.6,
    seed=0,
)
# trace.shape == (177, 1000, 2)  # (synapses, time, channel)
```

### CLI: full sweep + scoring + plots

```bash
python -m tasks.t0024_port_de_rosenroll_2026_dsgc.code.run_tuning_curve --mode full
python -m tasks.t0024_port_de_rosenroll_2026_dsgc.code.score_envelope
python -m tasks.t0024_port_de_rosenroll_2026_dsgc.code.plot_tuning_curves
```

## Dependencies

* **`neuron`** — the NEURON 8.2.7 simulator. The Python bridge is loaded from the local install at
  `C:\Users\md1avn\nrn-8.2.7\` (path is hard-coded as `NEURONHOME_DEFAULT` in `constants.py`).
* **`numpy`** — array math throughout, including the vectorised AR(2) generator and Cholesky-style
  cross-channel correlation.
* **`pandas`** — CSV I/O for the tuning-curve outputs and the score-envelope conversion to
  canonical schema.

The library also imports two sibling task libraries: the t0012 `tuning_curve_loss` library
(`score_curves`, `load_tuning_curve`) for envelope scoring, and the t0011 `tuning_curve_viz` library
(`plot_polar_tuning_curve`, `plot_cartesian_tuning_curve`) for plotting. Both are loaded via the
project-standard absolute-import path; no PyPI publication is involved.

## Testing

No unit tests are currently shipped with this library. The validation strategy is two-tiered:

1. **Standalone self-test**: `python -m tasks.t0024_port_de_rosenroll_2026_dsgc.code.ar2_noise` runs
   an empirical-statistics sanity check on the AR(2) generator (verifies cross-channel rho matches
   the target to within 0.05 and lag-1 autocorrelation matches `phi_1 / (1 - phi_2)`).
2. **End-to-end port-fidelity gate**: the full pipeline is validated by running the four-condition
   sweep and checking that `score_envelope.py` reports `de_rosenroll_port_fidelity_gate_pass: true`
   in `results/metrics.json` (DSI corr in `[0.30, 0.50]`, uncorr in `[0.18, 0.35]`,
   correlated-to-uncorrelated drop >= 20%).

Adding pytest-based unit tests (e.g., for the `_gaba_prob_for_direction` sigmoid, the
`_bar_arrival_times` projection, and the `_count_spikes` threshold-crossing routine) is filed as a
follow-up suggestion.

## Main Ideas

* **Vendor the HOC + MOD verbatim**: the 341-section morphology and the three custom mechanisms
  (`HHst_noiseless`, `cadecay`, `Exp2NMDA`) are copied from the upstream repository unchanged so the
  biophysics can be audited against the published model.
* **Re-implement the Python driver in a simplified form**: rather than carrying 2,500 lines of
  upstream `SacNetwork`, the driver places one ACh + one GABA `Exp2Syn` per terminal and uses an
  AR(2)-modulated Poisson release process. The single direction-dependent GABA release probability
  carries the asymmetric-inhibition mechanism.
* **Expose the correlated-vs-uncorrelated knob explicitly**: the `rho` argument to
  `generate_ar2_batch` (and the `correlated` flag in `run_tuning_curve.py`) is the single switch
  between paper's correlated SAC release (`rho=0.6`) and the AMB / decorrelated control (`rho=0.0`,
  GABA weight x1.8 per plan REQ-5).
* **Score with the same loss library used for every other DSGC port in this project**: t0012's
  `tuning_curve_loss.score_curves` is the canonical scoring function, so this port's results land on
  the same DSI / HWHM / RMSE / reliability axes as t0008, t0020, t0022, t0023.
* **Document every simplification**: the deltas vs. upstream (no full SacNetwork, no NMDA, no plexus
  / ambient ACh, single global GABA sigmoid) are listed inline in `run_tuning_curve.py`'s module
  docstring and recorded in `intervention/port_fidelity_miss.md` if the gate misses.

## Summary

This library is the project's third NEURON-based DSGC port, alongside the Poleg-Polsky lineage
(t0008, t0020, t0022) and the Hanson port (t0023). It vendors the de Rosenroll 2026 morphology,
mechanisms, and compiled `nrnmech.dll`, and pairs them with a simplified Python driver that
implements the paper's headline correlated-vs-uncorrelated SAC release contrast via an AR(2)
release-rate noise process with configurable cross-channel correlation. The driver runs both the
paper's native 8-direction protocol and the project-standard 12-angle protocol under both correlated
(`rho=0.6`) and uncorrelated (`rho=0.0`) conditions, and the scoring layer evaluates both the t0004
envelope match and a port-fidelity gate against the paper's published DSI numbers.

The library is consumed by its own task (`t0024_port_de_rosenroll_2026_dsgc`) for the four-CSV
sweep, the score report, and the polar / Cartesian PNG plots. Downstream tasks can import the
`build_dsgc_cell` and `generate_ar2_batch` entry points to reuse the morphology and noise process in
larger experiments — e.g., a sensitivity sweep over Ra / eleak (the paper-text vs code-text
parameter disagreement noted in `research/research_internet.md`), or an AIS overlay study (Nav1.6 /
Nav1.2 split, also flagged as a follow-up).

Known limitations: the simplified port omits the upstream's full SAC varicosity network, NMDA
synapses, and plexus (ambient ACh) inputs. As a result, absolute DSI magnitudes will not match the
paper exactly; the port's value is in the relative correlated-vs-uncorrelated contrast and the
ability to run on a Windows workstation without the upstream's `statsmodels` and `h5py`
dependencies. A future task can port the full `SacNetwork` if absolute-magnitude fidelity is
required.
