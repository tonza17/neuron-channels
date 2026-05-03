---
spec_version: "2"
library_id: "de_rosenroll_2026_dsgc_ais"
documented_by_task: "t0078_bedb_mobo_v2_ais_tiered_ahp"
date_documented: "2026-05-03"
---
# De Rosenroll 2026 DSGC with AIS

## Metadata

* **Name**: De Rosenroll 2026 DSGC with AIS
* **Version**: 0.1.0
* **Task**: `t0078_bedb_mobo_v2_ais_tiered_ahp`
* **Dependencies**: neuron, numpy, botorch, torch, gpytorch
* **Modules**: `code/build_cell_ais.py`, `code/extend_with_ais.py`, `code/apply_params.py`,
  `code/constants.py`, plus 13 vendored MOD files in `code/mods/`

## Overview

This library is the AIS-augmented evolution of the t0024 `de_rosenroll_2026_dsgc` Bed B substrate.
It forks `build_dsgc_cell()` from t0024 and attaches a two-subsegment axon initial segment (AIS) at
the soma using priors from Van Wart 2007 / Werginz 2020 / Kole 2008. The proximal AIS subsegment
carries HHst as a Nav1.1/Nav1.2 stand-in; the distal subsegment carries `nav16t78` (Nav1.6),
`kv3t78` (Kv3), and `kv7t78` (Kv7 / KM). NaP, BK, SK, and the slow-AHP mechanism are explicitly
excluded from the AIS section per the project's biological-plausibility rule.

The library exposes a 49-dimensional parameter space designed for BoTorch multi-objective Bayesian
optimisation (qLogNEHVI). Twenty-five parameters are tier-stratified channel densities (5 channels
times 5 morphological tiers — soma, primary-dendrite, mid-dendrite, terminal-dendrite, AIS); seven
are uniform-density channels applied to soma + dendrites; two parameterise the slow Kv-AHP mechanism
(SK_E2 with extended Ca-binding: `gbar` and `tau_ca_multiplier` in `[1, 20]`); thirteen carry the
synaptic placement and passive properties unchanged from t0076; and two are free AIS geometry
parameters (`ais_length_um` in `[25, 50]`, `ais_diameter_um` in `[0.5, 1.2]`).

The library is the substrate for t0078's BO loop and is intended for downstream tasks that need
realistic AIS integration on Bed B (e.g., dendritic-spike experiments, AIS-localised channel sweeps,
or alternative slow-AHP architectures). The 49-d ParameterVector dataclass is the canonical
interface; `apply_parameter_vector(cell=cell, params=pv)` writes every parameter to the right
sections in one call.

## API Reference

### `build_cell_ais.py`

```python
def build_dsgc_cell_with_ais(
    *,
    ais_length_um: float = 30.0,
    ais_diameter_um: float = 0.8,
) -> DSGCCellWithAIS
```

Build a Bed B cell via t0024's `build_dsgc_cell()` and attach a two-subsegment AIS. Returns a
`DSGCCellWithAIS` dataclass that exposes every field of the t0024 `DSGCCell` (h, rgc, soma,
all_dends, primary_dends, non_terminal_dends, terminal_dends, terminal_locs_xy, origin_xy) plus the
new `ais_proximal` and `ais_distal` `h.Section` handles.

### `extend_with_ais.py`

```python
def extend_with_ais(
    *,
    h: Any,
    soma: Any,
    total_length_um: float = 30.0,
    diameter_um: float = 0.8,
) -> AISExtension
```

Build proximal + distal AIS sections, set passive Ra/cm, insert HHst basal Na+K, and connect them in
series at `soma(1.0)`. Segment count uses NEURON's d_lambda = 0.1 rule at 100 Hz.

```python
def update_ais_geometry(
    *,
    h: Any,
    extension: AISExtension,
    total_length_um: float,
    diameter_um: float,
) -> None
```

Update geometry on an existing AIS extension before channel insertion. Re-runs the d_lambda nseg
rule.

### `apply_params.py`

```python
def apply_parameter_vector(
    *,
    cell: DSGCCellWithAIS,
    params: ParameterVector,
) -> None
```

Write the 49-d parameter vector to the cell. Order of operations: (1) update AIS geometry, (2)
ensure t78 DLL is loaded, (3) insert all channels (idempotent), (4) write passive + uniform-density
channels on soma + dendrites, (5) write tier-stratified densities per tier, (6) write AIS-tier
densities (Nav1.6, Kv3 only — NaP, BK, SK forbidden at AIS), (7) write slow-AHP gbar +
tau_ca_multiplier on soma + AIS only.

### `constants.py`

```python
class ParameterVector:
    values: NDArray[np.float64]  # shape (49,)
    @classmethod
    def default(cls) -> ParameterVector: ...
    def stratified_density(*, channel_idx: int, tier: Tier) -> float: ...
    def uniform_density(*, suffix: str) -> float: ...
    @property
    def ais_length_um(self) -> float: ...
    @property
    def ais_diameter_um(self) -> float: ...
    @property
    def skahp_gbar_soma_ais(self) -> float: ...
    @property
    def skahp_tau_ca_multiplier(self) -> float: ...
```

The `ParamIndex` IntEnum lists the 49 parameter slots; `LOWER_BOUNDS` and `UPPER_BOUNDS` are `(49,)`
numpy arrays of natural-units bounds. `LOG_PARAM_INDICES` is the tuple of indices that the optimiser
should sample in log10 space (all density gbar parameters + slow-AHP gbar + tau_ca_multiplier +
gleak + synaptic weights).

### MOD library

`code/mods/` contains 13 vendored MOD files compiled by `nrnivmodl` into a NEURON shared library:
`nav16t78`, `napt78`, `nart78`, `kdrt78`, `kv3t78`, `kv4t78`, `kv7t78`, `iht78`, `calt78`, `catt78`,
`bkt78`, `skt78`, plus the new `skahpt78` (SK_E2 with `tau_ca_multiplier`-scaled Ca-binding
kinetics). The t0024 vendored DLL provides `HHst`, `cadecay`, and `Exp2NMDA`; do NOT duplicate these
in the t78 library — load order is t0024 DLL first, t78 DLL second.

## Usage Examples

```python
import numpy as np

from tasks.t0078_bedb_mobo_v2_ais_tiered_ahp.code.build_cell_ais import (
    build_dsgc_cell_with_ais,
)
from tasks.t0078_bedb_mobo_v2_ais_tiered_ahp.code.constants import (
    N_PARAMS,
    LOWER_BOUNDS,
    UPPER_BOUNDS,
    ParameterVector,
)
from tasks.t0078_bedb_mobo_v2_ais_tiered_ahp.code.apply_params import (
    apply_parameter_vector,
)


# Build a cell with default AIS geometry.
cell = build_dsgc_cell_with_ais(ais_length_um=30.0, ais_diameter_um=0.8)

# Sample a candidate uniformly in the natural-units bounding box.
rng = np.random.default_rng(42)
values = rng.uniform(low=LOWER_BOUNDS, high=UPPER_BOUNDS)
params = ParameterVector(values=values)

# Write the parameters to every section of the cell.
apply_parameter_vector(cell=cell, params=params)

# The cell is now ready for h.run() — see code/trial_driver.py for the
# 8-direction x 20-seed evaluation pattern used by t0078's BO loop.
```

```python
# Smoke-test the default ParameterVector with the trial driver:
#   uv run python -u -m tasks.t0078_bedb_mobo_v2_ais_tiered_ahp.code.trial_driver \
#       --n-seeds 2 --n-directions 2 --max-workers 1
```

## Dependencies

* **neuron 8.2.7** — NEURON simulator. `build_dsgc_cell_with_ais()` calls `h.Section`,
  `h.lambda_f`, `h.nrn_load_dll`. The t0024 vendored DLL (Windows) or `.so` (Linux compiled by
  `bootstrap.compile_t0024_mods_linux`) provides HHst / cadecay / Exp2NMDA.
* **numpy** — `ParameterVector.values` is a `NDArray[np.float64]`; bounds, defaults, and bounds
  builders all use numpy.
* **botorch / torch / gpytorch** — only `mobo_loop.py` uses these (Sobol DoE, qLogNEHVI
  acquisition, GP fits). The library itself can be used without torch if the consumer only needs to
  build cells and write parameters.

## Testing

No standalone unit tests yet (the library is exercised end-to-end by t0078's BO loop in
`code/mobo_loop.py` and by the trial-driver smoke test). Smoke tests:

```bash
# Local Windows (1 cell, 2 dirs x 2 seeds, single-process):
uv run python -u -m tasks.t0078_bedb_mobo_v2_ais_tiered_ahp.code.trial_driver \
    --n-seeds 2 --n-directions 2 --max-workers 1

# Verify the constants module round-trips:
uv run python -c "from tasks.t0078_bedb_mobo_v2_ais_tiered_ahp.code.constants \
import N_PARAMS, ParameterVector; assert N_PARAMS == 49; \
pv = ParameterVector.default(); assert pv.values.shape == (49,)"
```

## Main Ideas

* **Two-subsegment AIS for biological realism**: the proximal subsegment uses HHst as a
  Nav1.1/Nav1.2 stand-in (no separate Nav1.2 MOD vendored per researcher decision); the distal
  subsegment carries Nav1.6 + Kv3 + Kv7. NaP, BK, SK are EXCLUDED from the AIS — RGC AIS
  immunostaining literature does not support their presence there.
* **Tier-stratified channel densities decouple compartments**: 5 stratified channels (Nav1.6, Kv3,
  NaP, BK, SK) get independent densities at soma, primary-dendrite, mid-dendrite, terminal-dendrite,
  AIS. The 7 uniform-density channels share one density across soma + dends but are NOT inserted on
  the AIS.
* **Slow Kv-AHP via SK_E2 with `tau_ca_multiplier`**: instead of vendoring a separate KCNQ-like slow
  K+ MOD, t0078 extends the Hay 2011 SK_E2 with a free `tau_ca_multiplier` parameter in `[1, 20]`.
  This is the smallest additive change that lets the BO test whether a slower-than-fast-SK
  Ca-binding timescale is sufficient for any biologically plausible joint operating point.
* **Free AIS geometry parameters**: `ais_length_um` (25-50 um, default 30) and `ais_diameter_um`
  (0.5-1.2 um, default 0.8) are exposed as MOBO parameters per researcher decision. This brings the
  parameter space from 47 d to 49 d.
* **NEURON re-init bug bypass via subprocess-per-evaluation**: the trial driver uses
  `ProcessPoolExecutor` worker-per-trial; `plot_pareto.py::_save_deep_dive` wraps each deep-dive
  call in a single-worker pool to avoid the `Exp2NMDA name already exists` error.
* **`cadecay` SUFFIX collision avoidance**: the t78 MOD library deliberately EXCLUDES `cadecay.mod`
  because the t0024 vendored DLL already exposes that SUFFIX; loading t78 second works only because
  no SUFFIX is duplicated.

## Summary

This library is the AIS-augmented Bed B DSGC substrate that t0078 uses as the search space for a
multi-objective Bayesian optimisation over channel densities, slow-AHP kinetics, and synaptic
placement. It forks the t0024 `de_rosenroll_2026_dsgc` library and attaches a two-subsegment AIS
with the appropriate channel set per the Van Wart / Werginz / Kole biological priors; it stratifies
five channels across five morphological tiers; and it vendors a `tau_ca_multiplier`-extended SK_E2
to test the Larsson 2013 slow-AHP hypothesis without committing to a separate KCNQ-like MOD.

The library fits into the project as the canonical substrate for downstream AIS-aware DSGC tasks.
Where t0024 was the bare Bed B builder and t0076 was the 25-d MOBO-ready harness, t0078 unifies
these into a 49-d substrate that any future task can `apply_parameter_vector(...)` against without
re-implementing the tier-stratified write logic. The substrate is designed so that the
`tau_ca_multiplier = 1.0` setting bit-for-bit reproduces the t0074 sk74 dynamics, ensuring backward
compatibility with the un-augmented Bed B family.

Limitations: the AIS proximal subsegment uses HHst as a Nav1.1/Nav1.2 stand-in (no separate Nav1.2
MOD); the slow-AHP mechanism scales SK_E2 Ca-binding kinetics directly rather than introducing a
true seconds-scale KCNQ-like channel; and the synaptic placement excludes the AIS automatically
because the placer's candidate set is `cell.all_dends`, which does not include the AIS sections.
Future tasks may extend with a separate Nav1.2 MOD or a true KCNQ slow-K mechanism if the t0078
optimiser pushes `tau_ca_multiplier` to its `[1, 20]` upper bound.
