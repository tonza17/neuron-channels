---
spec_version: "2"
library_id: "minimal_dsgc_mg_block_nmda"
documented_by_task: "t0055_nmda_mg_block_dsi_recovery"
date_documented: "2026-04-28"
---
# Minimal DSGC AMPA + Mg-Block NMDA + Scalar gabaMOD

## Metadata

* **Name**: Minimal DSGC AMPA + Mg-Block NMDA + Scalar gabaMOD
* **Version**: 0.1.0
* **Task**: `t0055_nmda_mg_block_dsi_recovery`
* **Dependencies**: neuron, numpy, matplotlib, pandas, tqdm
* **Modules**: `code/constants.py`, `code/paths.py`, `code/swc_io.py`, `code/neuron_bootstrap.py`,
  `code/cell.py`, `code/placement.py`, `code/synapses.py`, `code/trial.py`,
  `code/run_tuning_curve.py`, `code/render_figures.py`, `code/compute_metrics.py`,
  `code/metrics_extra.py`
* **Custom MOD**: `code/mod/NMDA_MgBlock.mod` (canonical artefact at
  `assets/library/minimal_dsgc_mg_block_nmda/sources/NMDA_MgBlock.mod`)

## Overview

This library extends the t0054 minimal DSGC by replacing the voltage-INDEPENDENT NMDA `Exp2Syn` with
a custom `NMDA_MgBlock` POINT_PROCESS implementing the Jahr-Stevens Boltzmann Mg block. Same
dual-exponential gating kinetics (`tau1 = 5 ms`, `tau2 = 80 ms`, `e = 0 mV`) but the conductance is
multiplied by

```text
1 / (1 + n * exp(-gama * local_v))
```

with `n = 0.25 / mM`, `gama = 0.08 / mV`, and `local_v = v * (1 - Voff) + Vset * Voff`. With
`Voff = 0` (default) the block is voltage-dependent (Mg block on); `Voff = 1` clamps `local_v` to
`Vset = -60 mV` to recover a voltage-independent ablation regime.

Every other parameter — morphology, AMPA, GABA, HH soma + AIS, placement seed, stimulus protocol
— is bit-identical to t0054. The library is the implementation backbone of t0055, which re-runs
t0054's 1,440-trial sweep (4 gNMDA values x 12 directions x 10 trials x 3 modes) on the new NMDA
mechanism to test whether Mg block recovers the vector-sum DSI that t0054 lost (DSI collapsed from
**0.746** at `gNMDA = 0` to **0.082** at `gNMDA = 0.25 nS`). The headline pass criterion is
**vector-sum DSI > 0.50 AND peak Hz >= 5 Hz at `gNMDA = 0.25 nS`, FULL mode**.

This is the first task in the minimal-architecture lineage `t0052 -> t0053 -> t0054 -> t0055` to
introduce a custom MOD compilation step (`nrnivmodl`) into the bootstrap. The build is invoked by a
13-line `code/run_nrnivmodl.cmd` shim that mirrors the t0046 reference pattern; the resulting
`code/mod/nrnmech.dll` is loaded via `h.nrn_load_dll(...)` inside `neuron_bootstrap.py` AFTER
`load_stdrun` and BEFORE any code constructs an `h.NMDA_MgBlock(seg)` handle.

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
passive with `Rm = 5999 Ohm cm^2`, `Ra = 100 Ohm cm`, `cm = 1 uF/cm^2`. Identical to t0054.

### `code/neuron_bootstrap.py`

```python
def ensure_neuron_importable() -> None: ...
def load_stdrun() -> None: ...
def enable_cvode(*, atol: float = 1e-3) -> None: ...
def ensure_nmda_mg_block_compiled() -> None: ...
```

`ensure_nmda_mg_block_compiled` (NEW vs t0054) builds `code/mod/NMDA_MgBlock.mod` into
`code/mod/nrnmech.dll` via `code/run_nrnivmodl.cmd` if the DLL is missing, then registers it with
the NEURON kernel via `h.nrn_load_dll`. Order: call AFTER `ensure_neuron_importable` and
`load_stdrun`, BEFORE any `h.NMDA_MgBlock(seg)` construction. Idempotent: re-runs are safe (the
build is incremental, the DLL load is a no-op for already-registered mechanisms).

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

`build_ei_pairs` constructs three synaptic mechanisms per location on the same `seg`: an AMPA
`h.Exp2Syn`, an NMDA `h.NMDA_MgBlock` (the new POINT_PROCESS), and a GABA `h.Exp2Syn`. AMPA and NMDA
share a single `NetStim` driven by two separate `NetCon` instances — there is NO second NetStim
— so AMPA and NMDA fire at byte-identical times. `schedule_ei_onsets` writes per-trial weights:
AMPA at `AMPA_PEAK_NS x 1e-3` uS, NMDA at `gnmda_ns x 1e-3` uS (so `gnmda_ns = 0` yields a
wired-but-inert mechanism), and GABA at `GABA_BASE_NS x gaba_mod(theta) x 1e-3` uS. The NMDA_MgBlock
parameters (`n`, `gama`, `Voff`, `Vset`) are written once in `build_ei_pairs` and never modified per
trial.

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
their FULL-mode baselines so cross-mode state cannot leak. Inherited from t0054 verbatim because the
dual-exponential gating fires from `NetCon` events identically to `Exp2Syn`.

### `code/run_tuning_curve.py`

```python
def setup_sweep_artifacts() -> SweepArtifacts: ...
def run_dry_run_validation(*, artifacts: SweepArtifacts, gnmda_ns: float = 0.0) -> None: ...
def run_full_sweep(*, voltage_sample_stride: int = 8) -> None: ...
```

`setup_sweep_artifacts` invokes `ensure_nmda_mg_block_compiled()` after `load_stdrun` so the
`NMDA_MgBlock` POINT_PROCESS is registered before any synapse construction. The full sweep iterates
the four `gNMDA` values in the outer loop. All four `gNMDA` rows are appended to a single per-mode
CSV (one CSV per mode); each ends up with 4 x 12 x 10 = 480 rows including the `gnmda_ns` column.

### `code/compute_metrics.py` and `code/metrics_extra.py`

`compute_metrics.main()` groups each per-mode CSV by `gnmda_ns` and writes 12 metrics variants (4
gNMDA x 3 modes) with `variant_id = f"gnmda_{gnmda:.2f}_{mode}"`. Hard-fails with `AssertionError`
if (a) the IPSP conductance ratio `gabaMOD(180)/gabaMOD(0)` is outside `[2.7, 3.3]`, or (b) any
`gnmda_ns = 0` FULL row differs from t0054's `tuning_curve_full.csv` (filtered to `gnmda_ns == 0.0`)
by more than `1e-6` Hz. After variants are written, the script evaluates the S-0054-01 pass
criterion (`vector_sum_dsi > 0.50` AND `peak_hz >= 5.0` at `gNMDA = 0.25 nS`, FULL mode) and writes
three boolean fields to `derived_quantities.json`: `pass_criterion_dsi_at_gnmda_025`,
`pass_criterion_peak_hz_at_gnmda_025`, `pass_criterion_overall`.

### `code/render_figures.py`

Per-direction renderers (`render_soma_voltage_per_direction`, `render_aggregate_epsp`,
`render_aggregate_ipsp`, `render_psth`, `render_activation_histogram`) each loop over
`NMDA_PEAK_NS_VALUES`, producing 4 x 12 x 5 = 240 PNGs. Plus per-`gNMDA` polar and Cartesian
tuning-curve overviews via the t0011 `tuning_curve_viz` library, and FOUR sweep-summary plots:
`epsp_decay_vs_gnmda.png`, `peak_hz_vs_gnmda.png`, `dsi_vs_gnmda.png` (each with a t0054 overlay
curve loaded from t0054's `derived_quantities.json`), and the new `mg_block_g_v_curve.png` showing
the analytical Boltzmann factor alongside the empirical peak `gNMDA` from the voltage-clamp sanity
gate.

### `code/mod/NMDA_MgBlock.mod`

The custom NMDA POINT_PROCESS. ~80-line MOD with `tau1`, `tau2`, `e`, `n`, `gama`, `Voff`, `Vset`
RANGE/PARAMETER variables; `STATE { A B }`; `DERIVATIVE state { A' = -A/tau1; B' = -B/tau2 }`;
`BREAKPOINT` evaluating `local_v = v * (1 - Voff) + Vset * Voff` and
`g = (B - A) / (1 + n * exp(-gama * local_v))`, with `i = g * (v - e)` as a `NONSPECIFIC_CURRENT`.
`NET_RECEIVE(weight)` deposits identical mass into A and B so a single event produces the
dual-exponential `(B - A)` shape. Drop-in replacement for an `Exp2Syn` NMDA: at `gnmda_ns = 0` the
mechanism is wired-but-inert and yields exactly zero NMDA current at any voltage, ensuring the
`gNMDA = 0` cross-task regression to t0054 is bit-identical.

## Usage Examples

End-to-end sweep (1,440 trials, ~75 min to ~5 h wall-clock):

```python
from tasks.t0055_nmda_mg_block_dsi_recovery.code.run_tuning_curve import (
    run_full_sweep,
)

# Setup, dry-run gate, full 1,440 trials, write all CSVs.
run_full_sweep()
```

Single trial outside the sweep harness:

```python
from tasks.t0055_nmda_mg_block_dsi_recovery.code.cell import build_dsgc_from_swc
from tasks.t0055_nmda_mg_block_dsi_recovery.code.constants import TrialMode
from tasks.t0055_nmda_mg_block_dsi_recovery.code.neuron_bootstrap import (
    enable_cvode,
    ensure_neuron_importable,
    ensure_nmda_mg_block_compiled,
    load_stdrun,
)
from tasks.t0055_nmda_mg_block_dsi_recovery.code.paths import MORPHOLOGY_SWC_PATH
from tasks.t0055_nmda_mg_block_dsi_recovery.code.placement import (
    sample_dendritic_locations,
)
from tasks.t0055_nmda_mg_block_dsi_recovery.code.synapses import build_ei_pairs
from tasks.t0055_nmda_mg_block_dsi_recovery.code.trial import run_one_trial

ensure_neuron_importable()
load_stdrun()
ensure_nmda_mg_block_compiled()
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

NMDA voltage-dependence sanity test (used as a validation gate before the full sweep):

```bash
uv run python -m arf.scripts.utils.run_with_logs \
  --task-id t0055_nmda_mg_block_dsi_recovery -- \
  uv run python -u tasks/t0055_nmda_mg_block_dsi_recovery/code/test_nmda_mg_block_voltage_dep.py
```

Asserts peak `g` is monotonic in voltage across `[-80, +20] mV` and that
`peak_g(-80 mV) <= 0.25 * peak_g(-20 mV)`; persists the six `(v_clamp_mv, peak_g_us)` pairs to
`results/mg_block_g_v_empirical.json` for the Mg-block g(v) sweep-summary plot.

## Dependencies

* `neuron` — NEURON 8.2.7, imported via the sentinel-guarded bootstrap in
  `code/neuron_bootstrap.py`. Required for `h.Section`, `h.Exp2Syn`, `h.NetStim`, `h.NetCon`,
  `h.SEClamp`, `h.finitialize`, `h.continuerun`, the `hh` / `pas` mechanisms, and `h.nrn_load_dll`.
  Voltage-dependent NMDA is provided by the custom MOD; its DLL (`code/mod/nrnmech.dll`) is built by
  `code/run_nrnivmodl.cmd` via the NEURON 8.2.7 MinGW toolchain at
  `C:\Users\md1avn\nrn-8.2.7\bin\nrnivmodl.bat`.
* `numpy` — used for length-weighted placement sampling, tuning-curve aggregation, voltage-clamp
  trace recording, and metric computation (including the gNMDA = 0 cross-task regression check).
* `matplotlib` — figure rendering for soma V(t), EPSP, IPSP, PSTH, activation histograms,
  per-gNMDA polar / Cartesian overviews, and the four sweep-summary plots (DSI vs gNMDA, peak Hz vs
  gNMDA, EPSP decay vs gNMDA, Mg-block g(v) sanity).
* `pandas` — long-form CSV manipulation for voltage traces, spikes, and activation times,
  including per-gNMDA slicing in `compute_metrics.py` and `render_figures.py`.
* `tqdm` — progress bars for the 1,440-trial sweep.

## Testing

Four pytest-style test modules live in `code/`:

```bash
uv run python -m arf.scripts.utils.run_with_logs --task-id t0055_nmda_mg_block_dsi_recovery -- \
  uv run python -u tasks/t0055_nmda_mg_block_dsi_recovery/code/test_gaba_mod.py

uv run python -m arf.scripts.utils.run_with_logs --task-id t0055_nmda_mg_block_dsi_recovery -- \
  uv run python -u tasks/t0055_nmda_mg_block_dsi_recovery/code/test_quiescent_rest.py

uv run python -m arf.scripts.utils.run_with_logs --task-id t0055_nmda_mg_block_dsi_recovery -- \
  uv run python -u tasks/t0055_nmda_mg_block_dsi_recovery/code/test_placement_seed0_match.py

uv run python -m arf.scripts.utils.run_with_logs --task-id t0055_nmda_mg_block_dsi_recovery -- \
  uv run python -u tasks/t0055_nmda_mg_block_dsi_recovery/code/test_nmda_mg_block_voltage_dep.py
```

`test_gaba_mod.py` checks `gaba_mod(0) == 0.33` and `gaba_mod(180) == 0.99`.
`test_quiescent_rest.py` is the **REQ-5 validation gate**: with no synapses, the soma must rest at
`-65 +/- 0.5 mV` after a 200 ms `continuerun`. `test_placement_seed0_match.py` is the **REQ-6
validation gate**: per-synapse coordinates in `placement_seed0.json` must match t0054's within
`1e-9`. `test_nmda_mg_block_voltage_dep.py` is the **REQ-8 validation gate** (NEW vs t0054):
single-section cell with one `NMDA_MgBlock` under `h.SEClamp` at six voltages must produce a
monotonic peak-`g` curve with `peak(-80 mV) <= 0.25 * peak(-20 mV)`.

## Main Ideas

* **Mg-block formula and parameters lifted verbatim from `bipolarNMDA.mod`.** Lines 47-54
  (parameters: `n = 0.25 / mM`, `gama = 0.08 / mV`, `Voff = 0`, `Vset = -60 mV`, `e = 0 mV`) and
  108-109 (BREAKPOINT: `local_v = v * (1 - Voff) + Vset * Voff`,
  `gNMDA = (A - B) / (1 + n * exp(-gama * local_v))`) of
  `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/sources/bipolarNMDA.mod`.
  The new `NMDA_MgBlock.mod` strips the t0046 bundling (presynaptic vesicle release, AMPA, calcium
  fraction) to a minimal POINT_PROCESS with only the Mg-block + dual-exponential gating + a
  NET_RECEIVE event handler.
* **Single shared NetStim per pair drives both AMPA and NMDA.** A second `NetCon` is wired to the
  same `NetStim`. This guarantees AMPA and NMDA fire at byte-identical times and removes one class
  of out-of-sync bugs. Inherited from t0054.
* **Wired-but-inert NMDA at `gNMDA = 0`.** The NMDA `NMDA_MgBlock` is always built; only the
  per-trial `nmda_netcon.weight[0]` is set to zero when `gnmda_ns = 0.0`. This is the cleanest way
  to satisfy the gNMDA = 0 cross-task regression gate (results bit-identical to t0054 at gNMDA = 0)
  without conditional construction.
* **MOD compilation is the first new step in the minimal-architecture lineage.** t0052/t0053/t0054
  used only NEURON built-ins (`Exp2Syn`, `NetStim`, `NetCon`, `hh`). t0055 introduces
  `code/mod/NMDA_MgBlock.mod`, `code/run_nrnivmodl.cmd`, and the `ensure_nmda_mg_block_compiled()`
  bootstrap step. The MOD compilation pattern is lifted verbatim from t0046; the build is idempotent
  and the DLL is loaded via `h.nrn_load_dll(...)` AFTER `load_stdrun` and BEFORE any
  `h.NMDA_MgBlock(seg)` construction.
* **All four gNMDA rows in a single per-mode CSV.** Each per-mode CSV gains a `gnmda_ns` column and
  ends up with 480 rows. Downstream analysis groups by `(gnmda_ns, mode)` to produce the 12 metric
  variants.
* **Hard cross-task regression gate against t0054.** `compute_metrics.py` reloads
  `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/tuning_curve_full.csv`, filters to
  `gnmda_ns == 0.0`, and asserts every row matches within `1e-6` Hz. Failure halts metrics-writing
  and surfaces the offending rows. With `gnmda_ns = 0` the Mg-block factor multiplies a zero
  conductance, so the result must be bit-identical to t0054 at gnmda = 0 (which itself was
  bit-identical to t0052).
* **Headline pass criterion encoded as three booleans in `derived_quantities.json`.** The S-0054-01
  question — "Does Mg block recover DSI > 0.50 at gNMDA = 0.25 nS while keeping peak Hz >= 5 Hz?"
  — is answered by `pass_criterion_dsi_at_gnmda_025`, `pass_criterion_peak_hz_at_gnmda_025`, and
  `pass_criterion_overall`. The values are also printed to stdout at the end of
  `compute_metrics.main()` for fast inspection.

## Summary

This library is the implementation backbone of t0055. It extends the t0054 minimal DSGC by
substituting the voltage-INDEPENDENT NMDA `Exp2Syn` with a custom voltage-DEPENDENT `NMDA_MgBlock`
POINT_PROCESS while keeping every other parameter — morphology, AMPA, GABA, HH soma + AIS,
placement seed, stimulus protocol, per-trial seeds — bit-identical to t0054. The Mg-block formula
and parameter values are taken verbatim from t0046's `bipolarNMDA.mod` (ModelDB 189347), stripped to
a minimal NMDA point process driven by `NET_RECEIVE` events. The library introduces the first custom
MOD compilation step (`nrnivmodl`) into the minimal-architecture lineage via the
`ensure_nmda_mg_block_compiled` bootstrap helper.

The library produces the same 1,440-trial sweep as t0054 (4 gNMDA values x 12 directions x 10 trials
x 3 modes), plus four validation gates (quiescent rest, placement bit-identity to t0054, gNMDA = 0
cross-task regression to t0054, and the new NMDA voltage-dependence sanity test). The 12-variant
metrics computer encodes the S-0054-01 headline gate (`vector_sum_dsi > 0.50` AND `peak_hz >= 5.0`
at `gNMDA = 0.25 nS`, FULL mode) as three boolean fields in `derived_quantities.json` and prints
PASS/FAIL to stdout. Sweep-summary plots overlay t0054's curves directly so DSI / peak Hz /
EPSP-decay deltas are visible at a glance, and the new Mg-block g(v) sanity plot juxtaposes the
analytical Boltzmann factor with the empirical peak-`g` values from the voltage-clamp gate.

The library can be imported from any downstream task that wants the same minimal DSGC with
voltage-dependent NMDA: extend `NMDA_PEAK_NS_VALUES` to sweep more conductances, set `Voff = 1` to
compare the voltage-independent regime, or modify `code/synapses.py` to test alternative gating
kinetics. Limitations: (1) the EPSP decay-to-1/e metric inherits t0054's null limitation because
NMDA `tau2 = 80 ms` exceeds the 1500 ms trial window; suggestion S-0054-03 covers an improved
metric. (2) Placement is uniform over total dendritic length; spatial bias variants are deferred to
follow-up tasks. (3) The architecture remains MINIMAL — no calcium dynamics, no presynaptic
vesicle release, no morphology refinement.
