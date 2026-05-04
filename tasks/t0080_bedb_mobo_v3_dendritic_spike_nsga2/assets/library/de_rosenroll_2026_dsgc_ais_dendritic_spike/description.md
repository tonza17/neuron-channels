---
spec_version: "2"
library_id: "de_rosenroll_2026_dsgc_ais_dendritic_spike"
documented_by_task: "t0080_bedb_mobo_v3_dendritic_spike_nsga2"
date_documented: "2026-05-04"
---

# De Rosenroll 2026 DSGC with AIS and Dendritic-Spike Machinery

## Metadata

* **Name**: De Rosenroll 2026 DSGC with AIS and Dendritic-Spike Machinery
* **Version**: 0.1.0
* **Task**: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* **Dependencies**: neuron, numpy, pymoo
* **Modules**: 11 Python files in `code/` plus 13 vendored t80-namespace MOD files in `code/mods/`

## Overview

This library is the v3 substrate for the project's Bed B DSGC compartmental model. It extends
t0078's `de_rosenroll_2026_dsgc_ais` substrate with three architectural additions: (1) Mg-block
NMDA at every dendritic compartment, instantiated through the t0024-vendored `Exp2NMDA`
POINT_PROCESS sharing the same NetStim driver as the existing ACh `Exp2Syn`; (2) Nav1.6 + NaP
densities at the distal-dendrite tier sufficient for back-propagating action potentials and
dendritic-spike initiation per Sivyer 2013 / Oesch 2005; (3) hard biological lower bounds on
AIS-related parameters (`nav16_ais >= 0.25` S/cm^2 from Kole 2008; AIS-to-soma Nav ratio `>= 5`
from Werginz 2024) so that no MOBO algorithm can collapse to the AIS-disabled corner observed in
t0078 iter 81.

The library also packages the NSGA-II MOBO loop replacing t0078's BoTorch qLogNEHVI: pymoo
`NSGA2(pop_size=96, sampling=LHS())` with default SBX `eta=15` + polynomial mutation `eta=20` +
tournament selection. NSGA-II's per-generation cost is independent of accumulated history, which
eliminates the O(N^3) Cholesky scaling that forced t0078 to early-stop. The 54-d parameter space
is the t0078 49-d layout plus 5 new dendritic-spike entries appended at indices 49-53; index 0-48
semantics are invariant.

The library is task-private — promotion to a substrate-agnostic shared MOBO harness is deferred
until at least one more substrate uses it (per the t0080 task description's "Out of scope" note).

## API Reference

### `code/build_cell_ais.py`

```python
def build_dsgc_cell_with_ais() -> DSGCCellWithAIS:
    """Build a Bed B DSGC cell with AIS extension; v3 reuses the t0078 builder."""
```

### `code/apply_params.py`

```python
def apply_parameter_vector(*, cell: DSGCCellWithAIS, params: ParameterVector) -> None:
    """Write a 54-d v3 parameter vector to all sections / segments. Order:
    1. AIS geometry update; 2. DLL load; 3. channel insertion;
    4. passive + uniform-density write; 5. tier-stratified write;
    6. AIS-stratified write; 7. v3 distal Nav1.6 + NaP overlay on terminal;
    8. slow-AHP soma + AIS write."""
```

### `code/constants.py`

```python
class ParamIndex(IntEnum):
    # 0-48: t0078 invariant indices.
    NAV16_SOMA_GBAR = 0
    ...
    AIS_DIAMETER_UM = 48
    # 49-53: v3 additions.
    GNMDA_DEND = 49        # log-uniform [1e-5, 1e-2] uS NetCon weight
    MG_CONC_MM = 50        # linear [0.1, 0.5] /mM written to Exp2NMDA n
    VOFF_NMDA = 51         # linear [-10, 10] mV; held at 0 for v3 LHS
    NAV16_DEND_DISTAL = 52 # log-uniform [1e-5, 0.05] S/cm^2
    NAP_DEND_DISTAL = 53   # log-uniform [1e-5, 0.01] S/cm^2

@dataclass(frozen=True, slots=True)
class ParameterVector:
    values: NDArray[np.float64]  # shape (54,)
    # @property accessors include gnmda_dend, mg_conc_mm, voff_nmda,
    # nav16_dend_distal, nap_dend_distal, nav16_ais_gbar, nav16_soma_gbar.

LOWER_BOUNDS: NDArray[np.float64]  # shape (54,); LOWER_BOUNDS[4]=0.25 (Kole 2008)
UPPER_BOUNDS: NDArray[np.float64]  # shape (54,); UPPER_BOUNDS[4]=5.0
```

### `code/nsga2_loop.py`

```python
class BedBV3Problem(pymoo.core.problem.Problem):
    """n_var=54, n_obj=2, n_ieq_constr=1.
    Constraint: g(x) = 5 - nav16_ais / nav16_soma <= 0 (Werginz 2024)."""

def run_nsga2_loop(*, pop_size: int, n_gen: int, seed: int,
                   max_workers: int, hourly_rate_usd: float) -> None:
    """NSGA-II loop with cost-cap watchdog. Writes pareto_front.json,
    all_evaluations.json, hv_trajectory.json. On cost-cap trip writes
    intervention/budget_overrun.md and exits cleanly."""
```

### `code/trial_driver.py`

```python
def evaluate_parameter_vector(*, params: ParameterVector,
                              angles_deg: tuple[int, ...], n_seeds: int,
                              max_workers: int = 0) -> EvalResult:
    """Run angles_deg x n_seeds trials in parallel via ProcessPoolExecutor.
    Returns EvalResult(dsi, pd_rate_hz, n_trials, n_errors, elapsed_s,
    is_unstable, peak_vm_mv)."""
```

## Usage Examples

```python
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import (
    ParameterVector, ANGLES_8DIR_DEG, N_SEEDS,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_driver import (
    evaluate_parameter_vector,
)

# Evaluate the default literature-anchored vector.
pv = ParameterVector.default()
result = evaluate_parameter_vector(
    params=pv,
    angles_deg=ANGLES_8DIR_DEG,
    n_seeds=N_SEEDS,
    max_workers=0,  # cpu_count()-1
)
print(f"DSI={result.dsi:.3f}  PD_rate_hz={result.pd_rate_hz:.2f}")
```

```python
# Run the full NSGA-II loop with the cost watchdog.
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.nsga2_loop import (
    run_nsga2_loop,
)
run_nsga2_loop(
    pop_size=96, n_gen=40, seed=1,
    max_workers=0, hourly_rate_usd=0.2382,
)
```

## Dependencies

* `neuron` (8.2.7+) — compartmental simulator; the t80 MODs in `code/mods/` and the t0024 sources
  are compiled with `nrnivmodl` on Linux.
* `numpy` — vectorised parameter handling and trial-result aggregation.
* `pymoo` (>= 0.6.1.6) — NSGA-II implementation and hypervolume indicator.

## Testing

The library does not ship dedicated unit tests in this version. Functional smoke testing is via:

```bash
# Per-cell trial-driver smoke test.
uv run python -u -m tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_driver \
    --n-seeds 1 --n-directions 8 --max-workers 0

# NSGA-II smoke test (8 cells, 1 generation).
uv run python -u -m tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.nsga2_loop \
    --pop-size 8 --n-gen 1 --max-workers 0 --hourly-rate-usd 0.2382
```

## Main Ideas

* The v3 substrate adds three architectural extensions over t0078: dendritic Mg-block NMDA,
  distal Nav1.6 + NaP, and hard biological bounds on AIS Nav (Kole 2008 / Werginz 2024).
* Hard parameter bounds are pre-registered in `LOWER_BOUNDS` / `UPPER_BOUNDS`; hard inequality
  constraints (e.g., AIS-to-soma Nav ratio) are enforced through pymoo's `n_ieq_constr` mechanism.
* The optimiser switch from BoTorch qLogNEHVI to NSGA-II eliminates the O(N^3) Cholesky scaling
  that bottlenecked t0078 after acq 480.
* The cost-cap watchdog (`HARD_BUDGET_USD = 2.00`) writes `intervention/budget_overrun.md` and
  exits cleanly; the partial Pareto front is preserved in `results/data/pareto_front.json`.
* The 54-d ParamIndex layout extends t0078's 49-d layout strictly at indices 49-53; indices 0-48
  retain the same meaning so t0078 ParameterVectors can be lifted to v3 by zero-padding.

## Summary

The library packages the v3 Bed B substrate and the NSGA-II MOBO harness used to search it. It
extends the t0078 substrate with dendritic-spike machinery (Mg-block NMDA, distal Nav1.6 + NaP)
and replaces the BoTorch qLogNEHVI optimiser with pymoo NSGA-II, eliminating the O(N^3) scaling
that bottlenecked t0078. Hard biological bounds on the AIS Nav parameters are enforced through the
parameter bounds and a single inequality constraint, preventing the AIS-disabled-corner failure
mode observed at t0078 iter 81.

The library is consumed by t0080's NSGA-II loop (entry-point `run_nsga2_loop`) and is the
substrate of record for the joint DSI / PD-rate optimisation experiment that motivated the task.
Future MOBO-on-biophysics tasks on Bed B should adopt the same hard-bounds discipline (pre-register
every measurement-grounded prior as a hard constraint, never as a soft penalty) regardless of the
acquisition algorithm chosen. Limitations: the library is currently task-private; promotion to a
substrate-agnostic shared harness is deferred until at least one more substrate uses it. The
distal Nav1.6 / NaP density bounds are based on qualitative priors from Sivyer 2013 / Oesch 2005
and may need tightening if direct dendritic-Nav measurements appear.
