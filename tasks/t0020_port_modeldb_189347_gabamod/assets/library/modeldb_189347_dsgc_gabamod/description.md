---
spec_version: "2"
library_id: "modeldb_189347_dsgc_gabamod"
documented_by_task: "t0020_port_modeldb_189347_gabamod"
date_documented: "2026-04-20"
---
# ModelDB 189347 DSGC Port -- gabaMOD-swap protocol

## Metadata

* **Name**: ModelDB 189347 DSGC Port -- gabaMOD-swap protocol
* **Version**: 0.1.0
* **Task**: `t0020_port_modeldb_189347_gabamod`
* **Upstream model**: Poleg-Polsky & Diamond 2016 (ModelDB 189347), at the same pinned commit
  (`87d669dcef18e9966e29c88520ede78bc16d36ff`) used by t0008's `modeldb_189347_dsgc` port
* **Sibling library**: `modeldb_189347_dsgc` (from task `t0008_port_modeldb_189347`) -- reused
  unchanged; this library does **not** vendor a second copy of the HOC/MOD sources
* **Dependencies**: `neuron` (>= 8.2), `numpy`, `pandas`, `pydantic`, `tqdm`, `matplotlib`
* **Modules**: `code/constants.py`, `code/paths.py`, `code/run_gabamod_sweep.py`,
  `code/score_envelope.py`, `code/plot_pd_vs_nd.py`

## Overview

This library is a sibling of `modeldb_189347_dsgc` (t0008) that shares the NEURON cell and parameter
set but changes the direction-selectivity protocol. The cell construction, HOC sourcing, and
canonical paper parameters are imported verbatim from t0008's library asset; the only new code is
the per-trial driver. Where t0008 imposes direction tuning by rotating BIPsyn `locx`/`locy`
coordinates around the soma and holding the inhibitory scalar `gabaMOD` fixed at 0.33, this library
holds the BIP coordinates fixed and swaps `gabaMOD` between two values: **0.33 for preferred
direction (PD) trials** and **0.99 for null direction (ND) trials**. This matches the native
direction-selectivity test that Poleg-Polsky & Diamond 2016 run in `main.hoc` when their interactive
GUI button executes the "DS test": the stimulus is identical between PD and ND, only the inhibitory
scalar changes.

Why both protocols are kept side by side: the rotation proxy (t0008) produces an explicit
`angle_deg` axis suitable for tuning-curve fitting, HWHM measurement, and per-angle scoring, at the
cost of exercising a mechanism the paper does not rely on. The gabaMOD-swap (t0020) produces a
two-condition result directly comparable to the paper's published DSI and PD firing-rate numbers, at
the cost of losing the angle axis -- null firing rate and HWHM are not defined when only two
conditions exist. Downstream tasks select whichever protocol matches their question.

The port targets the unwidened literature envelope: **DSI in [0.70, 0.85]** and **peak firing rate
in [40, 80] Hz**. These are the ranges quoted directly in Poleg-Polsky 2016 for wild-type ON-OFF
DRD4 DSGC responses to drifting-bar stimuli. The sister library `tuning_curve_loss` from t0012
widened these ranges to `[0.7, 0.9]` and `[30, 80]` so that its identity test
`score(target, target).passes_envelope is True` would hold on the canonical t0004 target; this
library uses the unwidened literature values because it is quoting the paper's envelope directly
rather than gating against a widened test target.

## API Reference

### `constants.py`

Re-exports `TSTOP_MS`, `V_INIT_MV`, `AP_THRESHOLD_MV`, `GABA_MOD`, `N_TRIALS`, and related canonical
paper parameters from `tasks.t0008_port_modeldb_189347.code.constants`, and adds the following
gabaMOD-swap-specific constants:

```python
GABA_MOD_PD: float = 0.33           # preferred-direction gabaMOD scalar (weak inhibition)
GABA_MOD_ND: float = 0.99           # null-direction gabaMOD scalar (strong inhibition)
N_TRIALS_PER_CONDITION: int = 20    # default trial count per condition
DSI_ENVELOPE: tuple[float, float] = (0.70, 0.85)
PEAK_ENVELOPE_HZ: tuple[float, float] = (40.0, 80.0)

class Condition(StrEnum):
    PD = "PD"
    ND = "ND"
```

### `paths.py`

Centralized `pathlib.Path` constants rooted at the task root. Exposes `DATA_DIR`,
`TUNING_CURVES_CSV` (`data/tuning_curves.csv`), `RESULTS_DIR`, `SCORE_REPORT_JSON`
(`results/score_report.json`), `METRICS_JSON` (`results/metrics.json`), `IMAGES_DIR`
(`results/images`), and `PD_VS_ND_PNG` (`results/images/pd_vs_nd_firing_rate.png`).

### `run_gabamod_sweep.py`

```python
def run_one_trial_gabamod(
    *,
    h: Any,
    gabamod_value: float,
    seed: int,
    baseline_coords: list[SynapseCoords],
) -> float:
```

Apply canonical paper parameters for this trial, override `h.gabaMOD` to `gabamod_value`, call
`placeBIP()` so the inhibitory point processes pick up the new scalar, record the soma voltage, run
`finitialize(V_INIT_MV)` + `continuerun(TSTOP_MS)`, and return the somatic spike count divided by
the stimulus window in seconds. The function also asserts, on every invocation, that every
`h.RGC.BIPsyn[i].locx` and `.locy` match the baseline snapshot -- this guards against the t0008
rotation silently re-engaging via leftover state.

```python
def main() -> int:
```

Build the cell once via t0008's `build_dsgc`, snapshot the baseline synapse coordinates, then loop
over `N_TRIALS_PER_CONDITION` seeds and for each seed run a PD trial followed by an ND trial. Writes
`data/tuning_curves.csv` with header `condition,trial_seed,firing_rate_hz`. Supports `--n-trials`
(default 20) and `--limit` (default None) for quick validation runs.

### `score_envelope.py`

Reads `data/tuning_curves.csv` with explicit pandas dtypes, computes
`DSI = (mean_PD - mean_ND) / (mean_PD + mean_ND)` and `peak_hz = mean_PD`, gates them against the
literature envelope, and writes a structured `ScoreReport` to `results/score_report.json` plus a
flat metrics payload to `results/metrics.json`.

### `plot_pd_vs_nd.py`

Bar chart with two bars (PD mean, ND mean), per-condition standard-deviation error bars, and a
per-trial scatter overlay. Saves a 5x4-inch PNG at 200 DPI to
`results/images/pd_vs_nd_firing_rate.png`.

## Usage Examples

```python
from tasks.t0008_port_modeldb_189347.code.build_cell import (
    build_dsgc,
    read_synapse_coords,
)
from tasks.t0020_port_modeldb_189347_gabamod.code.constants import (
    GABA_MOD_PD,
    GABA_MOD_ND,
)
from tasks.t0020_port_modeldb_189347_gabamod.code.run_gabamod_sweep import (
    run_one_trial_gabamod,
)

h = build_dsgc()
baseline = read_synapse_coords(h=h)

rate_pd = run_one_trial_gabamod(
    h=h, gabamod_value=GABA_MOD_PD, seed=1, baseline_coords=baseline,
)
rate_nd = run_one_trial_gabamod(
    h=h, gabamod_value=GABA_MOD_ND, seed=1, baseline_coords=baseline,
)
print(f"PD rate: {rate_pd:.1f} Hz, ND rate: {rate_nd:.1f} Hz")
```

End-to-end from the worktree root, assuming the t0008 `nrnmech.dll` has already been built via
`run_nrnivmodl.cmd`:

```bash
# 1. Validation gate (2 trials)
uv run python -m arf.scripts.utils.run_with_logs \
    --task-id t0020_port_modeldb_189347_gabamod \
    -- uv run python -m tasks.t0020_port_modeldb_189347_gabamod.code.run_gabamod_sweep \
        --limit 2 --n-trials 1

# 2. Full canonical sweep (40 trials)
uv run python -m arf.scripts.utils.run_with_logs \
    --task-id t0020_port_modeldb_189347_gabamod \
    -- uv run python -m tasks.t0020_port_modeldb_189347_gabamod.code.run_gabamod_sweep \
        --n-trials 20

# 3. Score against the literature envelope
uv run python -m arf.scripts.utils.run_with_logs \
    --task-id t0020_port_modeldb_189347_gabamod \
    -- uv run python -m tasks.t0020_port_modeldb_189347_gabamod.code.score_envelope

# 4. Generate the PD vs ND bar chart
uv run python -m arf.scripts.utils.run_with_logs \
    --task-id t0020_port_modeldb_189347_gabamod \
    -- uv run python -m tasks.t0020_port_modeldb_189347_gabamod.code.plot_pd_vs_nd
```

## Dependencies

* **`neuron`** -- loads the compiled `nrnmech.dll` from t0008's build directory and sources
  `RGCmodel.hoc` + `dsgc_model.hoc` through t0008's `build_dsgc` helper. Tested with NEURON 8.2.7.
* **`numpy`** -- soma voltage vector conversion for threshold-crossing counting.
* **`pandas`** -- CSV I/O for `data/tuning_curves.csv` with explicit nullable dtypes.
* **`pydantic`** -- `BaseModel` schemas for the structured `results/score_report.json` output.
* **`tqdm`** -- progress bar for the 40-trial sweep.
* **`matplotlib`** -- bar chart generation for `results/images/pd_vs_nd_firing_rate.png`.

This library imports directly from `tasks.t0008_port_modeldb_189347.code.*` and does not vendor a
second copy of the HOC/MOD sources. The t0008 library asset is a registered `library` asset, so
cross-task imports of `build_cell.py` and `constants.py` are permitted under the project's
cross-task import rules.

## Testing

The library reuses t0008's test infrastructure for cell construction and relies on its own
validation gate at run time. A quick smoke test is to run the driver with `--limit 2 --n-trials 1`
and inspect `data/tuning_curves.csv`: the PD firing rate should be substantially higher than the ND
firing rate. A per-trial assertion inside `run_one_trial_gabamod` guarantees the BIP coordinates
stay at baseline, so a silent regression back to the rotation proxy would raise `AssertionError`
before any rows are written.

No dedicated pytest test files are provided: the expensive end-to-end simulation (40 trials, ~1.5-3
minutes) is the practical verification, and mocking NEURON for a unit test would not exercise the
gabaMOD-swap pathway that the library is built to validate. The full-sweep score report
(`results/score_report.json`) and the canonical CSV (`data/tuning_curves.csv`) serve as the
library's integration-test artifacts.

## Main Ideas

* **Protocol separation**: two sibling libraries now share the same NEURON cell but expose different
  direction-selectivity protocols. The rotation-proxy port (t0008) is kept for tuning- curve fits;
  this gabaMOD-swap port is kept for envelope comparison against the published paper.
* **No source duplication**: the HOC and MOD files live only under t0008's library asset. This
  library imports `build_dsgc`, `read_synapse_coords`, `apply_params`, and `get_cell_summary` from
  `tasks.t0008_port_modeldb_189347.code.build_cell`, keeping the model canonical and avoiding the
  maintenance cost of a second copy.
* **Two-point schema**: `data/tuning_curves.csv` carries `(condition, trial_seed, firing_rate_hz)`
  rather than t0008's `(angle_deg, trial_seed, firing_rate_hz)`. This is an intentional schema
  divergence. `condition` is a string (`"PD"` or `"ND"`); `HWHM` and `null` are undefined for a
  two-point protocol and are reported as `N/A` in downstream comparison tables.
* **Unwidened envelope**: the literature envelope (DSI in [0.70, 0.85], peak in [40, 80] Hz) is used
  directly. The t0012 widened envelope ([0.7, 0.9] and [30, 80]) is not applied here because this
  library is quoting the paper's published ranges, not gating against the t0004 target.
* **Per-trial position assertion**: the driver asserts `h.RGC.BIPsyn[i].locx == baseline[i]` for all
  `i` on every trial. A silent re-engagement of the rotation proxy would raise immediately.

## Summary

This library provides a second direction-selectivity protocol for the ModelDB 189347 DSGC cell. The
cell, mechanisms, and canonical parameters are reused from t0008's `modeldb_189347_dsgc` library
asset; only the per-trial driver and a small scorer are new. The driver holds BIP synapse
coordinates fixed at their baseline values and swaps the inhibitory `h.gabaMOD` scalar between 0.33
(preferred direction, weak inhibition, strong spike output) and 0.99 (null direction, strong
inhibition, suppressed spike output). The resulting tuning curve has two conditions rather than
twelve angles, and DSI is computed directly from the PD/ND ratio.

The library fits into the project's research pipeline alongside `modeldb_189347_dsgc` (rotation
proxy, t0008) and `tuning_curve_loss` (scoring, t0012). It gives downstream tasks a biologically
faithful reproduction of the Poleg-Polsky & Diamond 2016 direction-selectivity test and is the
starting point for sensitivity analyses that manipulate `gabaMOD` directly -- a family of follow-up
suggestions raised in the project's suggestion pool.

Known limitations: the two-point protocol does not produce an angle axis, so HWHM and null firing
rate cannot be measured; trial-to-trial reliability is reported only per-condition rather than
per-angle; and the underlying morphology is still the bundled Poleg-Polsky 1-soma-350-dend cell
rather than the t0009 calibrated SWC. Follow-up tasks extending this library are scoped in the
project's suggestion backlog.
