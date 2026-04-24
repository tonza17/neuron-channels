---
spec_version: "2"
library_id: "modeldb_189347_dsgc_exact"
documented_by_task: "t0046_reproduce_poleg_polsky_2016_exact"
date_documented: "2026-04-24"
---

# ModelDB 189347 DSGC (exact reproduction)

## Metadata

* **Name**: ModelDB 189347 DSGC (exact reproduction)
* **Version**: 0.1.0
* **Task**: `t0046_reproduce_poleg_polsky_2016_exact`
* **Dependencies**: `matplotlib`, `numpy`, `tqdm` (NEURON 8.2.7 + NetPyNE 1.1.1 from t0007)
* **Modules**: see `details.json` `module_paths`
* **ModelDB pin**: accession 189347, commit
  `87d669dcef18e9966e29c88520ede78bc16d36ff` (2019-05-31, author tommorse,
  mirror `https://github.com/ModelDBRepository/189347`)

## Overview

This library is a from-scratch port of ModelDB accession 189347 (Poleg-Polsky and Diamond 2016,
Neuron, DOI `10.1016/j.neuron.2016.02.013`). It rebuilds the bundled DSGC compartmental model
exactly as the paper's authors deposited it, then exercises it against every figure the paper
reports (Figures 1-8). The library does NOT fork the existing t0008 / t0020 / t0022 ports; the
ModelDB HOC and MOD source files are copied verbatim into `code/sources/` and the only Python
glue layer is a thin wrapper around the original `simplerun(exptype, dir)` proc.

The library's primary purpose is to publish a paper-vs-code-vs-reproduction audit (the answer
asset `poleg-polsky-2016-reproduction-audit` produced alongside this library). Every parameter
the paper states is checked against the ModelDB code values; every quantitative claim in
Figures 1-8 is compared against the reproduction's actual output. Where paper text and code
disagree, the discrepancy is catalogued.

The HOC-embedded morphology in `RGCmodel.hoc` (~11,500 `pt3dadd` calls) is used verbatim, not
substituted with t0005's external SWC. `placeBIP()` in `main.hoc` depends on section ordering
and an ON/OFF cut plane (`z >= -0.16 * y + 46`) that only makes sense on the bundled
reconstruction; substituting an external SWC would itself be a reproduction bug.

## API Reference

### `code/build_cell.py`

```python
def load_neuron() -> Any:
    """Import NEURON, load nrnmech.dll, return ``h``. Idempotent."""

def build_dsgc() -> Any:
    """Source RGCmodel.hoc + dsgc_model_exact.hoc; return ``h`` with RGC instantiated."""

def get_cell_summary(*, h: Any) -> CellSummary:
    """Return the morphology counts: 1 soma + 350 dend sections, 282 ON synapses."""

def read_synapse_coords(*, h: Any) -> list[SynapseCoords]:
    """Snapshot every BIPsyn / SACinhibsyn / SACexcsyn (locx, locy)."""

def assert_bip_positions_baseline(*, h: Any, baseline: list[SynapseCoords]) -> None:
    """Guard: assert every BIP coord matches baseline; raises if any rotation re-engages."""
```

### `code/run_simplerun.py`

```python
@dataclass(frozen=True, slots=True)
class TrialResult:
    exptype: ExperimentType
    direction: Direction
    trial_seed: int
    flicker_var: float
    stim_noise_var: float
    b2gnmda_ns: float
    peak_psp_mv: float
    baseline_mean_mv: float
    spike_times_ms: list[float]


def run_one_trial(
    *,
    exptype: ExperimentType,        # CONTROL=1, ZERO_MG=2, HIGH_CL=3
    direction: Direction,            # PREFERRED=0 (gabaMOD=0.33), NULL=1 (gabaMOD=0.99)
    trial_seed: int,
    flicker_var: float = 0.0,        # luminance noise SD; main.hoc default 0.
    stim_noise_var: float = 0.0,     # extra stim-amplitude noise SD; main.hoc default 0.
    b2gnmda_override: float | None = None,  # None -> code value 0.5 nS; paper says 2.5.
    record_spikes: bool = False,
) -> TrialResult:
    ...
```

### `code/neuron_bootstrap.py`

```python
def ensure_neuron_importable() -> None:
    """Set NEURONHOME, put NEURON's bindings on sys.path, register DLL dir.

    Re-execs the Python process if NEURONHOME was missing (idempotent via sentinel
    env var ``_T0046_NEURONHOME_BOOTSTRAPPED``).
    """
```

### `code/run_all_figures.py`, `code/compute_metrics.py`, `code/render_figures.py`

CLI scripts producing the per-figure CSVs, the variant-format `metrics.json`, and the
`results/images/fig{1..8}_*.png` overlays respectively.

## Usage Examples

Run a single PD trial under control conditions:

```python
from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.neuron_bootstrap import (
    ensure_neuron_importable,
)
ensure_neuron_importable()

from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.constants import (
    Direction,
    ExperimentType,
)
from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun import run_one_trial

result = run_one_trial(
    exptype=ExperimentType.CONTROL,
    direction=Direction.PREFERRED,
    trial_seed=1,
    b2gnmda_override=0.5,  # code value; pass 2.5 for paper value.
)
print(result.peak_psp_mv, result.baseline_mean_mv)
```

Re-run the whole paper-figure sweep + metrics + figure overlays:

```bash
uv run python -m arf.scripts.utils.run_with_logs \
  --task-id t0046_reproduce_poleg_polsky_2016_exact -- \
  uv run python -u tasks/t0046_reproduce_poleg_polsky_2016_exact/code/run_all_figures.py
uv run python -u tasks/t0046_reproduce_poleg_polsky_2016_exact/code/compute_metrics.py
uv run python -u tasks/t0046_reproduce_poleg_polsky_2016_exact/code/render_figures.py
```

## Dependencies

* `matplotlib` — figure rendering for the per-figure overlays.
* `numpy` — numerical operations on PSP / spike traces.
* `tqdm` — progress bars during the trial sweeps.
* NEURON 8.2.7 + NetPyNE 1.1.1 at `C:\Users\md1avn\nrn-8.2.7` (validated by t0007).
* MinGW-gcc bundled with NEURON for compiling MOD files via
  `code/run_nrnivmodl.cmd`.

## Testing

The smoke test runs the library end-to-end on a single PD + ND trial under control:

```bash
uv run python -m arf.scripts.utils.run_with_logs \
  --task-id t0046_reproduce_poleg_polsky_2016_exact -- \
  uv run python -u tasks/t0046_reproduce_poleg_polsky_2016_exact/code/smoke_test.py
```

Expected output: cell builds with `countON=282 numsyn=282`, PD peak PSP > ND peak PSP, no
exceptions raised.

There is no formal pytest suite — the library's correctness is established by the audit table
and figure-reproduction table in the answer asset
`poleg-polsky-2016-reproduction-audit/full_answer.md`.

## Main Ideas

* **Verbatim ModelDB sources**: every `.hoc` and `.mod` file under `sources/` is the unmodified
  ModelDB 189347 release at commit `87d669dcef18e9966e29c88520ede78bc16d36ff`, plus a
  per-file provenance comment header. The only ARF-introduced HOC file is the GUI-free
  derivative `dsgc_model_exact.hoc`, which transcribes the parameter block + the four
  procedures (init_active, placeBIP, update, init_sim) plus simplerun verbatim from
  `main.hoc` with the GUI panels stripped. **`dsgc_model_exact.hoc` is NOT imported from
  t0008's `dsgc_model.hoc`**; it is authored from scratch to satisfy the no-fork rule.
* **`achMOD` is silently rebound by `simplerun()`**: the module-load default is
  `achMOD = 0.25` (`main.hoc` line 47), but `simplerun()` rewrites it to `0.33` on every
  call (line 352). Python drivers MUST NOT expose `achMOD` as a knob; setting it before
  `simplerun()` is silently overwritten. The constant `ACHMOD_SIMPLERUN = 0.33` in
  `code/constants.py` records the effective value used by every figure run.
* **`b2gnmda` post-call override**: `simplerun()` also writes `b2gnmda = 0.5 * nmdaOn` (line
  346). To reproduce the paper's claimed gNMDA = 2.5 nS or the AP5-analogue gNMDA = 0, the
  Python driver re-applies the override **after** `simplerun()` and re-runs `update()` +
  `placeBIP()` + `h.run()`. See `code/run_simplerun.py` for the exact sequence.
* **MOD files compile cleanly under NEURON 8.2.7 + MinGW-gcc** with no source edits
  required. The four "Default ... will be ignored and set by NEURON" warnings on
  `spike.mod` (cao, cai, ek, ena) are NEURON's standard treatment of ion-channel
  PARAMETER defaults and are not bugs.
* **Noise driver is present in `placeBIP()` but parameterised to zero by default**
  (`flickerVAR = 0`, `stimnoiseVAR = 0` at `main.hoc` lines 100-101). Figures 6-8 work by
  setting `h.flickerVAR = SD` and re-calling `placeBIP()` (which `simplerun()` does
  automatically). No new MOD file or HOC patch is required, contradicting one of the
  pre-flagged discrepancies in `task_description.md`.

## Summary

The library reproduces ModelDB 189347 verbatim under NEURON 8.2.7 + NetPyNE 1.1.1 on Windows.
It exposes a thin Python driver (`run_one_trial`) that wraps `h.simplerun(exptype, dir)` and
honours every relevant parameter knob the paper varies (gNMDA, noise SD, condition, direction).
Every figure-1-through-8 reproduction sweep is automated by `code/run_all_figures.py` and
materialised as CSVs, metrics JSON, and PNG figure overlays. The library is the technical
substrate of the answer asset `poleg-polsky-2016-reproduction-audit`, which publishes the
line-by-line paper-vs-code-vs-reproduction audit, the figure-reproduction table, and the
discrepancy catalogue.

The library fits into the project as the canonical, non-modified reference port of the
Poleg-Polsky 2016 model. Downstream optimisation tasks (e.g., t0033-style hyperparameter
sweeps) should build on this library rather than on t0008 (which used a rotation proxy for
direction selectivity) or t0020 (which validated the gabaMOD-swap protocol but did not
reproduce all paper figures).

The known limitation is that figure-reproduction trial counts are reduced (3-6 trials per
condition) compared to the paper's 12-19 cells. This is a wall-clock budget choice (the full
8-figure sweep would take >5 hours at the paper's trial counts on local CPU); the reduced
counts are sufficient to establish whether each metric falls inside or outside the paper's
1-SD tolerance band.
