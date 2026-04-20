---
spec_version: "2"
library_id: "modeldb_189347_dsgc"
documented_by_task: "t0008_port_modeldb_189347"
date_documented: "2026-04-20"
---
# ModelDB 189347 DSGC Port

## Metadata

* **Name**: ModelDB 189347 DSGC Port
* **Version**: 0.1.0
* **Task**: `t0008_port_modeldb_189347`
* **Upstream**: [ModelDB 189347](https://modeldb.science/189347) at commit
  `87d669dcef18e9966e29c88520ede78bc16d36ff` of
  [ModelDBRepository/189347](https://github.com/ModelDBRepository/189347)
* **Dependencies**: `neuron` (>= 8.2), `tqdm`
* **Modules**: `code/build_cell.py`, `code/constants.py`, `code/paths.py`,
  `code/run_tuning_curve.py`, `code/score_envelope.py`, `code/report_morphology.py`,
  `code/swc_io.py`, `code/run_nrnivmodl.cmd`

## Overview

This library is a Python driver around the verbatim HOC/MOD sources of Poleg-Polsky & Diamond 2016
(ModelDB 189347, "Reaching above synchrony: direction selectivity in the retina via a parallel
inhibitory microcircuit"). The upstream model is a single ON-OFF DRD4 starburst-amacrine-cell (SAC)-
driven retinal direction-selective ganglion cell (DSGC) with a fixed bundled morphology (1 soma +
350 dend sections, ~6.5 mm total cable), 282 ON-dendrite synapses bundled as
`(BIPsyn, SACinhibsyn, SACexcsyn)` triples, Jahr-Stevens NMDA kinetics bundled with AMPA inside a
single `bipNMDA` POINT_PROCESS, and a 1-D drifting bar driven via per-synapse `locx` arrival-time
computation.

The port keeps Poleg-Polsky's HOC and MOD files untouched — they are bundled under
`assets/library/modeldb_189347_dsgc/sources/` — and invokes them through `neuron.h.load_file` and
`neuron.h.nrn_load_dll`. Python only owns the things HOC cannot cleanly parameterise: 12-angle
sweeping via spatial rotation of `BIPsyn.locx`/`.locy`, per-trial seeding, threshold-crossing spike
counting, canonical-schema CSV emission, and scoring against the t0012 envelope. A GUI-free
derivative `dsgc_model.hoc` is provided so the model can be driven headless; `main.hoc` is preserved
verbatim for provenance.

Morphology swap (to the Horton-Strahler calibrated SWC from t0009) was scoped out: `RGCmodel.hoc`'s
`placeBIP`-driven synapse placement logic depends on the bundled section ordering and the z/y
ON-cut; replacing it with a SWC loader is a much larger rebuild than this port's plan envelope
allowed. The calibrated SWC is read and reported for comparison in `data/morphology_swap_report.md`,
and a rebuild around a calibrated morphology is logged as a downstream suggestion.

## API Reference

### `build_cell.py`

```python
def load_neuron() -> Any: ...
```

Imports `neuron`, loads the task-local compiled `nrnmech.dll`, and sources `stdrun.hoc` for
`run()`/`continuerun()`/`finitialize()`. Idempotent.

```python
def build_dsgc() -> Any:
    """Return h with RGC, numsyn, countON initialised."""
```

Sources `RGCmodel.hoc` and `dsgc_model.hoc` (the GUI-free main), then calls
`init_sim() -> init_active() -> access RGC.soma -> update()`. Resets `celsius=32 deg C`,
`dt=0.1 ms`, `tstop=1000 ms`, `v_init=-65 mV`.

```python
@dataclass(frozen=True, slots=True)
class SynapseCoords:
    index: int
    bip_locx_um: float
    bip_locy_um: float
    sac_inhib_locx_um: float
    sac_inhib_locy_um: float
    sac_exc_locx_um: float
    sac_exc_locy_um: float

def read_synapse_coords(h: Any) -> list[SynapseCoords]: ...
```

Snapshot `(locx, locy)` for every `BIPsyn`, `SACinhibsyn`, and `SACexcsyn` point process. Called
once after `build_dsgc` and then passed into every `run_one_trial` to serve as the rotation
baseline.

```python
def rotate_synapse_coords_in_place(
    *,
    h: Any,
    angle_deg: float,
    baseline: list[SynapseCoords],
    rotate_sac: bool = False,
) -> None:
```

Rotates BIP `locx`/`locy` around the soma by `angle_deg` while keeping SAC coords fixed (default).
This breaks the bundled BIP/SAC spatial symmetry that otherwise causes the bundled stimulus to
produce no direction selectivity. Setting `rotate_sac=True` rotates all three kinds together
(ablation).

```python
def run_one_trial(
    *,
    h: Any,
    angle_deg: float,
    seed: int,
    baseline_coords: list[SynapseCoords],
) -> float:
```

One closed-loop simulation: apply params, rotate, rerun `update()` and `placeBIP()`,
`finitialize(v_init)`, `continuerun(tstop)`, then count upward threshold crossings of `V_{soma}`
above `AP_THRESHOLD_MV=-10`. Restores baseline coords at the end so trials are independent. Returns
firing rate in Hz.

### `run_tuning_curve.py`

`main()` sweeps 12 angles (0, 30, ..., 330 deg) x 20 trials (seed=1..20), emits the canonical
`(angle_deg, trial_seed, firing_rate_hz)` CSV at `data/tuning_curves/curve_modeldb_189347.csv`.

### `score_envelope.py`

`main()` reads the emitted CSV and calls `tuning_curve_loss.score(simulated_curve_csv=...)`, writing
the full `ScoreReport` to `data/score_report.json` and the four registered metric keys to
`results/metrics.json`.

### `report_morphology.py`

`main()` builds the bundled DSGC, walks every section, computes total cable length and
synapse-location bounding box, reads the calibrated SWC via `swc_io.parse_swc_file`, and writes
`data/morphology_swap_report.md`.

## Usage Examples

```python
from tasks.t0008_port_modeldb_189347.code.build_cell import (
    build_dsgc, read_synapse_coords, run_one_trial,
)

h = build_dsgc()
baseline = read_synapse_coords(h=h)
for angle_deg in (0.0, 90.0, 180.0, 270.0):
    rate_hz = run_one_trial(
        h=h, angle_deg=angle_deg, seed=1, baseline_coords=baseline,
    )
    print(f"{angle_deg:6.1f} deg -> {rate_hz:.1f} Hz")
```

End-to-end from a fresh repo clone on Windows:

```powershell
# 1. build MOD files
cmd /c tasks\t0008_port_modeldb_189347\code\run_nrnivmodl.cmd `
    tasks\t0008_port_modeldb_189347\assets\library\modeldb_189347_dsgc\sources `
    tasks\t0008_port_modeldb_189347\build\modeldb_189347

# 2. smoke test
uv run python -u -m tasks.t0008_port_modeldb_189347.code.test_smoke_single_angle

# 3. run the full sweep (~10-15 min on a 2026-era laptop)
uv run python -u -m tasks.t0008_port_modeldb_189347.code.run_tuning_curve

# 4. score against the envelope
uv run python -u -m tasks.t0008_port_modeldb_189347.code.score_envelope
```

## Dependencies

* **`neuron`** — required. We import `from neuron import h` and call `h.nrn_load_dll`,
  `h.load_file`, `h.finitialize`, `h.continuerun`, and use `h.Vector` to record soma voltage. The
  compiled `nrnmech.dll` is produced by NEURON's bundled `nrnivmodl.bat` against the six bundled MOD
  files (`HHst`, `SAC2RGCexc`, `SAC2RGCinhib`, `SquareInput`, `bipolarNMDA`, `spike`). Tested with
  NEURON 8.2.7 on Windows 11.
* **`tqdm`** — for the tuning-curve sweep progress bar (already a top- level project dep).

The port does **not** use NetPyNE: attempts to wrap the bundled HOC template through
`netpyne.sim.importCellParams` hit the same synapse- placement coupling issue as a SWC swap; a pure
`neuron.h` driver turned out to be both simpler and more faithful.

## Testing

```bash
uv run python -u -m tasks.t0008_port_modeldb_189347.code.test_smoke_single_angle
uv run python -u -m tasks.t0008_port_modeldb_189347.code.test_scoring_pipeline
```

`test_smoke_single_angle` is the gate that the MOD compile, HOC sourcing, DLL load, parameter setup,
and spike-counting pipeline are all healthy: it builds the cell, runs one PD trial with `seed=1`,
and asserts the soma firing rate is strictly positive. `test_scoring_pipeline::test_identity`
asserts that feeding the t0004 target CSV through `score()` as both target and candidate yields
`loss_scalar == 0` and `rmse_vs_target == 0`. Both tests exit zero on success and nonzero on
failure.

## Main Ideas

* **HOC-first, Python-driver pattern.** The port keeps Poleg-Polsky's HOC and MOD sources pristine
  and drives them via `h.load_file`, rather than translating them into NetPyNE cellParams. This
  preserves the paper's synapse-placement logic and the `placeBIP` timing calculation exactly.
* **Rotation-only DS.** Direction-selective tuning is imposed by rotating `BIPsyn.locx`/`.locy`
  around the soma while keeping SAC synapse coords fixed. In the bundled morphology every ON
  dendrite has a co-located BIP+SACinhib+SACexc triple; rotating all three together preserves the
  BIP/SAC arrival-time phase and produces no DS. Rotating only BIP introduces a spatial-offset bias
  that recovers per-angle firing-rate modulation.
* **Synapse count = 282, not 177.** The t0008 plan's "177 AMPA + 177 NMDA + 177 GABA" figure does
  not match the bundled `RGCmodel.hoc`, which yields `countON=282`. The port is faithful to the
  released HOC; the 282 value is carried through `constants.N_SYNAPSES_EACH_TYPE` and the morphology
  swap report.
* **Morphology swap deferred.** Replacing the bundled 1-soma-350-dend `create` block with the t0009
  Horton-Strahler SWC requires rewriting `RGCmodel.hoc`'s topology, 3D-point placement, and
  `placeBIP` section-walking logic; doing so within the t0008 plan envelope would have hybridised
  the model in ways that break the envelope derivation. The comparison is reported instead; a full
  rebuild is suggested for a later task.

## Summary

This library ports ModelDB 189347 into a headless Python-driven simulation pipeline, executing at
the canonical parameters of Poleg-Polsky & Diamond 2016 and producing the four metrics that the
t0012 `tuning_curve_loss` library registers (`direction_selectivity_index`, `tuning_curve_hwhm_deg`,
`tuning_curve_reliability`, `tuning_curve_rmse`). The entire pipeline from MOD compile through
envelope scoring runs on a standard Windows 11 / NEURON 8.2.7 / Python 3.13 stack without GUI or
remote compute.

The library is consumed by t0008's own `run_tuning_curve.py` and `score_envelope.py` entry points,
and serves as a template for future tasks porting sibling DSGC models from ModelDB or elsewhere.
Known limitations: the bundled morphology (not the calibrated SWC) is used; the rotation scheme
imposes DS via spatial offset rather than via the paper's `gabaMOD` parameter-swap mechanism; and
the envelope targets (peak 40-80 Hz PD, <10 Hz ND, DSI 0.7-0.85, HWHM 60-90 deg) are not hit at the
bundled parameters — a parameter-sweep refinement and a calibrated-morphology rebuild are logged
as follow-up suggestions.
