---
spec_version: "2"
library_id: "procedural_dsgc_morphology_generator"
documented_by_task: "t0090_morphology_generator_diversity_test"
date_documented: "2026-05-07"
---
# Procedural DSGC Morphology Generator

## Metadata

* **Name**: Procedural DSGC Morphology Generator
* **Version**: 0.1.0
* **Task**: `t0090_morphology_generator_diversity_test`
* **Dependencies**: numpy, scipy, neuron, matplotlib
* **Modules**: `code/morphology_params.py`, `code/generator.py`, `code/verification.py`,
  `code/constants.py`, `code/paths.py`, `code/load_default_params.py`

## Overview

This library produces NEURON-compatible direction-selective ganglion-cell (DSGC) morphologies from a
14-knob parameter space. Up to t0088 every NSGA-II run in the project used the fixed Bed B
morphology ported from de Rosenroll 2026 (t0024). The generator removes that constraint: morphology
becomes part of the search vector. A deterministic `(MorphologyParams, morph_seed)` pair always
produces byte-identical NEURON sections, so cells are reproducible across processes and machines.

The generator emits a `MorphologyResult` whose field layout mirrors the t0080 `DSGCCellWithAIS`
dataclass, so downstream task code (`apply_parameter_vector`, `setup_synapses_parametric`, the trial
driver, the parametric synapse placer) consumes it without modification. The result also carries
extra metadata that the t0080 reference cell does not provide (`stability_flag`,
`morphometric_summary`, `connectivity`, `section_endpoints_xy`) — these are used by t0090 for
verification, visualisation, and Phase F reproducibility, and they are available to t0091 for the
joint 68-d (54-d electrophys + 14-d morphology) NSGA-II run.

The 14 knobs split into four families:

* **Topology (5)**: `num_primary_branches`, `branch_prob_per_um`, `max_strahler_depth`,
  `mean_branching_angle_deg`, `rall_exponent`.
* **Asymmetry (4)**: `soma_offset_pd_um`, `field_elongation_pd`, `branch_density_gradient_pd`,
  `primary_branch_pd_concentration` (von Mises kappa).
* **Geometry (3)**: `mean_segment_length_um`, `soma_diameter_um`, `ais_length_um`.
* **Stochastic (2)**: `morph_seed`, `branch_length_cv`.

Branching is recursive and bounded by `max_strahler_depth`; daughter diameters obey Rall's
generalised power law (`d_parent**rall = sum d_daughter**rall`). Every section's `nseg` is set by
NEURON's d_lambda rule (`freq=100 Hz`, `d_lambda=0.1`), inherited from t0080's
`extend_with_ais._compute_nseg`. The AIS is built as two concatenated sections (proximal + distal)
via the t0080 idiom, attached to `soma(1)`.

## API Reference

### `generate_morphology`

```python
def generate_morphology(
    *,
    params: MorphologyParams,
    morph_seed: int | None = None,
) -> MorphologyResult: ...
```

Builds the procedural cell from the 14 knobs. The optional `morph_seed` argument overrides
`params.morph_seed`; when omitted, `params.morph_seed` is used. Topology is generated as a Python
tree first (lightweight node objects), asymmetry transforms (`soma_offset_pd_um`,
`field_elongation_pd`) are applied in 2D, and the NEURON sections are materialised in a second pass.
The function loads NEURON, the t0024 nrnmech.dll, and the t0080 nrnmech.dll once per process via a
private guarded loader; subsequent calls reuse the cached HOC interpreter.

Returns a `MorphologyResult` containing `soma`, `all_dends`, `primary_dends`, `non_terminal_dends`,
`terminal_dends`, `terminal_locs_xy`, `origin_xy`, `ais_proximal`, `ais_distal`, `stability_flag`,
`morphometric_summary`, `connectivity`, `section_endpoints_xy`, plus `h` and `rgc` for
compatibility.

### `MorphologyParams`

```python
@dataclass(frozen=True, slots=True)
class MorphologyParams:
    num_primary_branches: int
    branch_prob_per_um: float
    max_strahler_depth: int
    mean_branching_angle_deg: float
    rall_exponent: float
    soma_offset_pd_um: float
    field_elongation_pd: float
    branch_density_gradient_pd: float
    primary_branch_pd_concentration: float
    mean_segment_length_um: float
    soma_diameter_um: float
    ais_length_um: float
    morph_seed: int
    branch_length_cv: float

    def to_dict(self) -> dict[str, float | int]: ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MorphologyParams: ...

    @classmethod
    def from_bedb_base_point(cls) -> MorphologyParams: ...
```

`to_dict()` and `from_dict()` provide round-trip JSON serialisation;
`MorphologyParams.from_bedb_base_point()` returns the BedB-equivalent point calibrated to the de
Rosenroll 2026 morphology (4 primary branches, branch_prob_per_um=0.04, max_strahler_depth=6,
mean_segment_length_um=25, rall_exponent=1.5, soma_diameter_um=15, ais_length_um=31).

### `MorphologyResult`

```python
@dataclass(frozen=True, slots=True)
class MorphologyResult:
    h: Any
    rgc: Any
    soma: Any
    all_dends: list[Any]
    primary_dends: list[Any]
    non_terminal_dends: list[Any]
    terminal_dends: list[Any]
    terminal_locs_xy: Any
    origin_xy: tuple[float, float]
    ais_proximal: Any
    ais_distal: Any
    stability_flag: StabilityKind
    morphometric_summary: MorphometricSummary
    connectivity: dict[str, str]
    section_endpoints_xy: dict[str, tuple[float, float, float, float]]
```

The first 11 fields mirror the t0080 `DSGCCellWithAIS` interface 1:1 so that
`apply_parameter_vector(cell=morph_result, params=...)` consumes a procedural cell without
modification. `connectivity` maps each child section name to its parent (the soma is the root).
`section_endpoints_xy` maps section names to `(x0, y0, x1, y1)` 2D endpoints, used by the
visualisation module.

### `MorphometricSummary`

```python
@dataclass(frozen=True, slots=True)
class MorphometricSummary:
    total_dendritic_length_um: float
    branch_count: int
    max_strahler_depth: int
    electrotonic_length_lambda: float
    soma_displacement_um: float
    field_major_axis_length_um: float
```

Six summary features used by Phase E PCA / UMAP. `electrotonic_length_lambda` is the maximum path
`L / lambda` from soma to any terminal under canonical passive parameters (`Rm = 6000 ohm.cm^2`,
`Ra = 100 ohm.cm`).

### `StabilityKind`

```python
class StabilityKind(Enum):
    STABLE = "stable"
    NAN_VOLTAGE = "nan_voltage"
    DIVERGED = "diverged"
    DISCONNECTED = "disconnected"
```

Verification outcome enum.

### `verify_one_morphology`

```python
def verify_one_morphology(
    *,
    morph_id: str,
    population: str,
    morph_index: int,
    params: MorphologyParams,
    default_params: ParameterVector,
) -> VerificationResult: ...
```

Build the procedural cell, insert HHst + cad on soma + dendrites, apply the 54-d `ParameterVector`,
run a 50 ms no-stim stability check at -70 mV, and run an 8-direction bar protocol with one seed per
direction (1400 ms each). Returns a `VerificationResult` with `stability_flag`, `dsi`, `pd_rate_hz`,
`nd_rate_hz`, `peak_vm_mv`, `n_dendrites`, `n_terminals`, and per-direction spike counts.

### `BEDB_BASE_POINT` and `PARAM_BOUNDS`

```python
BEDB_BASE_POINT: dict[str, float]    # 14 parameters at the BedB-equivalent point
PARAM_BOUNDS: dict[str, tuple[float, float]]  # (lo, hi) per parameter
```

Used directly by `MorphologyParams.from_bedb_base_point()` and by Phase B / Phase C samplers.

## Usage Examples

### Minimal example: build the BedB-equivalent cell

```python
from tasks.t0090_morphology_generator_diversity_test.code.generator import (
    generate_morphology,
)
from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
)

params = MorphologyParams.from_bedb_base_point()
cell = generate_morphology(params=params, morph_seed=1234)
print(f"built {len(cell.all_dends)} dendrites, {len(cell.terminal_dends)} terminals")
print(f"total length: {cell.morphometric_summary.total_dendritic_length_um:.1f} um")
```

### Realistic Phase D verification workflow

```python
from tasks.t0090_morphology_generator_diversity_test.code.load_default_params import (
    load_t0083_best_cell_param_vector,
)
from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
)
from tasks.t0090_morphology_generator_diversity_test.code.verification import (
    verify_one_morphology,
)

default_params = load_t0083_best_cell_param_vector()
bedb = MorphologyParams.from_bedb_base_point()
result = verify_one_morphology(
    morph_id="bedb_test",
    population="similar",
    morph_index=0,
    params=bedb,
    default_params=default_params,
)
print(f"stability: {result.stability_flag}")
print(f"DSI: {result.dsi}, PD rate: {result.pd_rate_hz} Hz")
```

## Dependencies

* **numpy** (>=2.4): random number generation (`np.random.default_rng`), array ops for morphometric
  features, von Mises sampling.
* **scipy** (>=1.17): `scipy.stats.qmc.LatinHypercube` for the Phase B sampler.
* **neuron** (8.2.7): the simulator. The procedural cell uses `h.Section`, `h.pt3dadd`,
  `h.lambda_f`, plus the t0024 `HHst` / `cad` / `Exp2NMDA` channels from the t0024 nrnmech.dll and
  the t0080 t80-namespaced channels from the t0080 nrnmech.dll. Both DLLs are loaded once per
  process by the generator's internal guarded loader.
* **matplotlib** (>=3.10): visualisation modules only.

Internal libraries this library depends on at runtime:

* `tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell` for `_ensure_neuron_on_path` (NEURON
  initialization helper).
* `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params` for `ensure_t80_dll_loaded` and
  `apply_parameter_vector`.
* `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants` for `ParameterVector` and
  `ParamIndex`.
* `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_driver.run_one_trial` and
  `trial_helpers.setup_synapses_parametric` (for the verification harness).

## Testing

Run the unit tests with:

```bash
uv run pytest tasks/t0090_morphology_generator_diversity_test/code/ -v
```

Tests cover:

* Determinism: same `(params, morph_seed)` produces byte-identical sections.
* Round-trip: `MorphologyParams.to_dict() -> from_dict()` returns an equal object.
* Edge cases: minimum (3 primaries, depth 2) and maximum (7 primaries, depth 6) topology.
* No-NaN: 10 random parameter draws produce only positive section lengths and diameters.
* d_lambda: `_compute_nseg` returns an odd integer >= 1 for `L` in [10, 600] um.
* Connectivity: every child section has a parent in the topology.

## Main Ideas

* The generator separates topology generation (Python tree of `_Node` objects) from NEURON section
  materialisation. Asymmetry transforms operate on the tree before NEURON sees the geometry; this
  makes `field_elongation_pd` and `soma_offset_pd_um` explicit coordinate operations that do not
  perturb diameters or branch counts.
* Determinism is a hard requirement. Every random draw uses `np.random.default_rng(morph_seed)`;
  different seeds produce different morphologies, but the same seed produces byte-identical sections
  across runs and processes. This is what t0091 needs for warm-start anchors.
* Compatibility with the t0080 substrate is a structural requirement, not a runtime check. The
  `MorphologyResult` field layout mirrors `DSGCCellWithAIS` so `apply_parameter_vector` writes the
  54-d vector to procedural cells without modification. Verification (`verify_one_morphology`)
  inserts HHst + cad on soma + dendrites before applying the parameter vector — t0024's
  `build_cell` does this implicitly via its HOC template, but the procedural builder must do it
  explicitly because the t0080 `apply_parameter_vector` assumes those channels are already present.
* Cells must remain alive in Python until they are no longer referenced by NEURON. The verification
  driver maintains a module-level `_LIVE_CELLS` list that pins each built cell so Python's GC does
  not free a cell whose Python id is then reused by a fresh allocation, which would silently break
  t0080's idempotency caches.

## Summary

`procedural_dsgc_morphology_generator` is the deliverable library of t0090 and the input substrate
for t0091's joint 68-d NSGA-II run. It exposes 14 explicit knobs spanning topology, asymmetry, and
geometry; produces deterministic NEURON sections; and emits a `MorphologyResult` that is
structurally compatible with the t0080 `apply_parameter_vector` harness without any changes to
upstream code. The library was validated by a 60-morphology diversity test (30 LHS-sampled "very
different" + 30 +/- 5 percent jittered "very similar") and a 5-cell Bed-B reproducibility check;
both are reproducible from the unit tests, the sampling scripts (`sample_different.py`,
`sample_similar.py`), the verification driver (`verification.py`), and the reproducibility driver
(`reproducibility.py`).

The library does not include a real-cell warm-start archive (NeuroMorpho.Org imports are out of
scope per the task description). Downstream tasks that need a starting morphology should use
`MorphologyParams.from_bedb_base_point()` as the canonical anchor, or build their own warm-start
archive from the validated 60-morphology set in `data/different_morphologies/` plus
`data/similar_morphologies/`. The diversity test demonstrates that the 14-d space covers visibly
distinct morphology classes, but it does not statistically certify the coverage; t0091 should
include morphology-anchored archive checkpoints to detect collapse to a narrow basin.
