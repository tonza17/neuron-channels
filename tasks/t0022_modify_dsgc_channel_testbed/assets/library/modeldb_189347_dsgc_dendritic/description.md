---
spec_version: "2"
library_id: "modeldb_189347_dsgc_dendritic"
documented_by_task: "t0022_modify_dsgc_channel_testbed"
date_documented: "2026-04-21"
---
# ModelDB 189347 DSGC -- Dendritic-Computation Driver

## Metadata

* **Name**: ModelDB 189347 DSGC -- Dendritic-Computation Driver
* **Version**: 0.1.0
* **Library ID**: `modeldb_189347_dsgc_dendritic`
* **Spec version**: 2
* **Task**: `t0022_modify_dsgc_channel_testbed`
* **Dependencies**: `neuron`, `numpy`, `pandas`, `tqdm`, `matplotlib`
* **Upstream libraries**: `modeldb_189347_dsgc` (t0008), `tuning_curve_loss` (t0012)
* **Modules**: `code/neuron_bootstrap.py`, `code/run_tuning_curve.py`, `code/score_envelope.py`,
  `code/plot_tuning_curve.py`, `code/constants.py`, `code/paths.py`,
  `code/dsgc_channel_partition.hoc`

* * *

## Overview

Per-dendrite excitation-inhibition driver for the Poleg-Polsky & Diamond 2016 DSGC HOC model
(ModelDB 189347). Produces direction selectivity through on-the-path shunting inhibition
(Koch-Poggio-Torre 1982/1983, Taylor 2000) rather than through the stimulus-rotation proxy used in
t0008 or the global `gabaMOD` scalar swap used in t0020. The driver also supplies a channel-modular
AIS partition (five `forsec` regions on top of the Poleg-Polsky morphology) that downstream
channel-swap tasks can target without editing the Python driver or the verbatim HOC sources.

Each ON-dendrite section gets a dedicated excitation-inhibition synapse pair: one AMPA `Exp2Syn`
placed distally at `sec(0.9)` (see `AMPA_SEG_LOCATION` in `constants.py`) and one GABA_A `Exp2Syn`
placed proximally at `sec(0.3)` (see `GABA_SEG_LOCATION`). The proximal location is the on-the-path
position that lets the shunt veto distally-generated EPSPs before they reach the soma. Each synapse
is driven by a dedicated NetStim point process in burst mode (`number=N_SYN_EVENTS`, `noise=0`,
`interval=SYN_EVENT_INTERVAL_MS`, and a `start` time set per trial). Using NetStim rather than
VecStim avoids a dependency on the optional `vecevent.mod` that is not bundled with the Windows
NEURON install at this workstation.

Per-synapse onset timing is a function of bar direction. For each pair, the bar's leading edge
reaches the dendrite midpoint `(x, y)` at
`t_bar = (x cos theta + y sin theta) / v + BAR_BASE_ONSET_MS`, where theta is the bar direction and
v is the bar velocity. For **preferred direction** trials (|delta_deg| < 90, where delta is the
angle between the dendrite's azimuth and the bar direction) AMPA fires at `t_bar` and GABA fires at
`t_bar + EI_OFFSET_PREFERRED_MS` (default +10 ms), so the EPSPs propagate to the soma before the
shunt arrives (Wehr-Zador 2003, Taylor 2000). For **null direction** trials (|delta_deg| >= 90) GABA
fires at `t_bar` and AMPA fires at `t_bar + |EI_OFFSET_NULL_MS|`, so the shunt is present when the
EPSPs arrive and vetoes them (Koch-Poggio-Torre 1982/1983). Per-direction conductance tuning follows
the Park 2014 priors (AMPA direction-untuned, GABA null/preferred ratio 4x) but with absolute values
calibrated against the bundled Poleg-Polsky cell's channel density.

What the driver explicitly does NOT do (guaranteed by a per-trial baseline assertion in
`run_one_trial_dendritic`): no BIP synapse-coordinate rotation (t0008's rejected approach), and no
global `gabaMOD` scalar swap (t0020's rejected approach). The driver zeros t0008's bundled
b2gampa/b2gnmda/s2ggaba/s2gach scalars and calls `update() + placeBIP()` so the BIP/SAC synapses are
silent. Direction selectivity comes exclusively from the per-dendrite E-I pairs.

* * *

## API Reference

### Function `run_one_trial_dendritic`

```python
run_one_trial_dendritic(
    *,
    h,                                 # NEURON HocObject
    pairs: list[EiPair],               # Output of build_ei_pairs
    angle_deg: float,                  # Bar direction, degrees
    trial_seed: int,                   # Seed for apply_params()
    baseline_coords: BaselineCoords,   # Snapshot of BIPsyn locx/locy
    baseline_gaba_mod: float,          # Snapshot of h.gabaMOD
) -> float                             # Somatic firing rate, Hz
```

Run one per-dendrite E-I trial at one bar direction and return the somatic firing rate in Hz.
Pre-conditions: the HOC cell is built via `build_dsgc()` and `dsgc_channel_partition.hoc` has been
sourced. `baseline_coords` and `baseline_gaba_mod` are snapshots captured once before any trial
runs, used by the per-trial baseline assertion that guards against accidental BIP rotation or
`gabaMOD` drift.

* Module: `code/run_tuning_curve.py`

### Function `build_ei_pairs`

```python
build_ei_pairs(*, h) -> list[EiPair]
```

Create one AMPA (distal 0.9) and one GABA_A (proximal 0.3) `Exp2Syn` per ON-dendrite with NetStim
drivers and return a list of `EiPair` dataclass instances. Each `EiPair` holds references to the
AMPA + GABA `Exp2Syn`, their `NetStim` drivers, their `NetCon`s, and the host section's midpoint
coordinates used for onset-timing math.

* Module: `code/run_tuning_curve.py`

### Function `schedule_ei_onsets`

```python
schedule_ei_onsets(
    *,
    h,
    pairs: list[EiPair],
    angle_deg: float,
    velocity_um_per_ms: float,
    gaba_null_pref_ratio: float,
    trial_seed: int,
) -> list[dict[str, float]]             # One debug dict per pair
```

Set per-pair NetStim start times and per-pair GABA NetCon weights for a given bar direction. Returns
a list of debug dicts (one per pair) suitable for dumping to `logs/preflight/onsets.json`. Each dict
contains `pair_index`, `angle_deg`, `delta_deg`, `is_preferred`, `t_bar_ms`, `ampa_start_ms`,
`gaba_start_ms`, `gaba_weight_uS`, and `x_um`/`y_um`.

* Module: `code/run_tuning_curve.py`

### Script `run_tuning_curve`

CLI driver with three modes: `--dry-run` (build cell + EiPairs, no simulation), `--preflight` (4
angles x 2 trials validation gate), or default (full 12 angles x 10 trials sweep).

* Invocation: `uv run python -u -m tasks.t0022_modify_dsgc_channel_testbed.code.run_tuning_curve`
* Output:
  `tasks/t0022_modify_dsgc_channel_testbed/data/tuning_curves/curve_modeldb_189347_dendritic.csv`
  with columns `(angle_deg, trial_seed, firing_rate_hz)`.

### Script `score_envelope`

Score the emitted tuning curve against the canonical t0004 target via t0012's
`tuning_curve_loss.score`. Emits `data/score_report.json` (full dump) and `results/metrics.json`
(four registered metric keys: `direction_selectivity_index`, `tuning_curve_hwhm_deg`,
`tuning_curve_reliability`, `tuning_curve_rmse`).

* Invocation: `uv run python -u -m tasks.t0022_modify_dsgc_channel_testbed.code.score_envelope`

### Script `plot_tuning_curve`

Emit a polar + Cartesian tuning-curve PNG from the emitted CSV.

* Invocation: `uv run python -u -m tasks.t0022_modify_dsgc_channel_testbed.code.plot_tuning_curve`
* Output: `tasks/t0022_modify_dsgc_channel_testbed/results/images/tuning_curve_dendritic.png`

* * *

## Usage Examples

### Preflight validation gate (4 angles x 2 trials, ~30 s)

```bash
uv run python -u -m tasks.t0022_modify_dsgc_channel_testbed.code.run_tuning_curve --preflight
```

Use before the full sweep to confirm that the DSI sign is correct (preferred > null) and peak firing
at the preferred direction lands above ~5 Hz.

### Full 12-angle sweep (120 trials, ~9-15 min)

```bash
uv run python -u -m tasks.t0022_modify_dsgc_channel_testbed.code.run_tuning_curve
uv run python -u -m tasks.t0022_modify_dsgc_channel_testbed.code.score_envelope
uv run python -u -m tasks.t0022_modify_dsgc_channel_testbed.code.plot_tuning_curve
```

Emits `data/tuning_curves/curve_modeldb_189347_dendritic.csv`, `data/score_report.json`,
`results/metrics.json`, and `results/images/tuning_curve_dendritic.png` in that order.

### Programmatic single-trial call

```python
from tasks.t0022_modify_dsgc_channel_testbed.code.neuron_bootstrap import (
    bootstrap_neuron,
)
from tasks.t0022_modify_dsgc_channel_testbed.code.run_tuning_curve import (
    build_ei_pairs,
    run_one_trial_dendritic,
    snapshot_baseline,
)

h = bootstrap_neuron()
pairs = build_ei_pairs(h=h)
baseline = snapshot_baseline(h=h)

rate_hz = run_one_trial_dendritic(
    h=h,
    pairs=pairs,
    angle_deg=120.0,
    trial_seed=1,
    baseline_coords=baseline.coords,
    baseline_gaba_mod=baseline.gaba_mod,
)
```

* * *

## Channel-Modular Partition

`code/dsgc_channel_partition.hoc` is sourced after `RGCmodel.hoc` and `dsgc_model.hoc`. It declares
five named `SectionList` objects that downstream channel-swap tasks can target with a one-line
`forsec <region> { ... }` edit, without touching the Python driver or the verbatim Poleg-Polsky HOC
sources.

Each region has a baseline `forsec` block that inserts no new channels (the cell inherits t0008's
HHst from `RGCmodel.hoc`). Downstream tasks replace each block's body with their own `uninsert` and
`insert` statements.

### Region Table

| Region | Membership | Baseline | Channel-swap target | Default gbar | Literature source |
| --- | --- | --- | --- | --- | --- |
| `SOMA_CHANNELS` | `RGC.soma` only | HHst (from `RGCmodel.hoc`) | Nav (soma) | 1.0 S/cm^2 | [ModelDB-189347] |
| `DEND_CHANNELS` | every section in `RGC.dends` | Passive (Ra + pas) | Nav (dend) / Kv / Ih | Nav 0.03 S/cm^2 | [ModelDB-189347] |
| `AIS_PROXIMAL` | axon sections with distance(0.5) <= 10 um from soma | (empty in baseline) | Nav1.1 | 1.5 S/cm^2 | [ModelDB-123623-KoleStuart] |
| `AIS_DISTAL` | axon sections with 10 < distance(0.5) <= 45 um | (empty in baseline) | Nav1.6 + Kv1.2 + optional Kv3 | 8.0 / 0.1 / 0.0033 S/cm^2 | [ModelDB-144526-Hallermann], [ModelDB-123623-KoleStuart], [ModelDB-Kv3-Akemann2006] |
| `THIN_AXON` | axon sections with distance(0.5) > 45 um | (empty in baseline) | Inherit soma Na at lower density | Task-dependent | VanWart 2006 |

The bundled Poleg-Polsky morphology in `RGCmodel.hoc` does NOT define axon sections -- only soma
plus 350 dend[]. The `AIS_PROXIMAL`, `AIS_DISTAL`, and `THIN_AXON` SectionLists are therefore empty
in this testbed, exactly as intended: they are hooks for downstream channel-swap tasks which will
(a) create axon[] sections and connect them to the soma, and (b) append to these lists before
calling their own `forsec` insertion. AIS partition thresholds are taken from VanWart2006 (~10 um
proximal/distal boundary; distal band extends to ~45 um before the thin axon).

### Adding a Channel Set: Worked Example

To insert Nav1.6 at distal AIS sections in a downstream task, append to `AIS_DISTAL` while creating
axon sections, then replace the `forsec AIS_DISTAL` block's body with:

```hoc
forsec AIS_DISTAL {
    uninsert HHst
    insert na16
    gbar_na16 = 8.0
    insert kv12
    gbar_kv12 = 0.1
}
```

Replace `na16` and `kv12` with the MOD suffix names introduced by the downstream task's MOD files.
The same pattern applies to `SOMA_CHANNELS`, `DEND_CHANNELS`, `AIS_PROXIMAL`, and `THIN_AXON`.

### Correction: Nav1.1 in the Proximal AIS (NOT Nav1.2)

The original task description referenced a "Nav1.6 distal + Nav1.2 proximal" AIS split drawn from
cortical-pyramidal literature (Kole and Stuart 2008). This split is NOT the correct prior for
retinal ganglion cells. In RGCs the proximal AIS partner of Nav1.6 is Nav1.1, not Nav1.2 (VanWart
2006 "Novel distribution of the sodium channel Nav1.1 in axon initial segments of retinal ganglion
cells and their central projections", RGC-AIS-Review-2022).

This library's `AIS_PROXIMAL` block is labelled for Nav1.1 insertion in follow-up channel-swap
tasks. Downstream tasks that insert a proximal Na channel must insert Nav1.1 (e.g., `insert na11`
with `gbar_na11 = 1.5`), not Nav1.2. The t0022 testbed itself does not insert any Nav isoform --
`AIS_PROXIMAL` is empty at baseline.

* * *

## Constants

All scheduler parameters live in `code/constants.py`. The most important new constants for this
driver:

| Constant | Value | Role |
| --- | --- | --- |
| `EI_OFFSET_PREFERRED_MS` | +10.0 | Preferred-direction GABA delay after AMPA |
| `EI_OFFSET_NULL_MS` | -10.0 | Null-direction GABA lead before AMPA (negative sign) |
| `EI_OFFSET_BAND_MS` | (5.0, 20.0) | Koch-Poggio-Torre 1982/1983 timing window |
| `AMPA_CONDUCTANCE_NS` | 6.0 | Per-synapse AMPA conductance (direction-untuned) |
| `GABA_CONDUCTANCE_PREFERRED_NS` | 3.0 | Per-synapse GABA conductance on preferred side |
| `GABA_CONDUCTANCE_NULL_NS` | 12.0 | Per-synapse GABA conductance on null side (4x preferred) |
| `GABA_NULL_PREF_RATIO` | 4.0 | Guard constant for null/preferred ratio (Park 2014) |
| `AMPA_SEG_LOCATION` | 0.9 | Distal placement on each dendrite section |
| `GABA_SEG_LOCATION` | 0.3 | Proximal (on-the-path) placement on each dendrite section |
| `N_SYN_EVENTS` | 6 | NetStim events per pair per trial |
| `SYN_EVENT_INTERVAL_MS` | 30.0 | NetStim interval (6 x 30 = 180 ms burst) |
| `BAR_BASE_ONSET_MS` | 200.0 | Offset to keep all per-pair onsets positive |
| `BAR_VELOCITY_UM_PER_MS` | 1.0 | Bar-sweep speed used in onset math |

The GABA null/preferred ratio 4x is preserved from Park 2014 single-event priors. Absolute
conductances are uprated from Park 2014's 0.3 / 0.6 / 2.4 nS because each `Exp2Syn` in this driver
receives only a short NetStim burst (vs. the bundled Poleg-Polsky BIPsyn which drives synapses
continuously across the bar-sweep window). Preferred GABA is held below Park 2014's single-event
default so the +10 ms E-I delay actually produces somatic spikes before the shunt arrives. Preflight
peak firing at the preferred direction lands at 13-14 Hz, matching the t0008 baseline of ~15 Hz.

* * *

## Outputs

Running the full sweep (no `--preflight` or `--dry-run` flag) emits:

* `data/tuning_curves/curve_modeldb_189347_dendritic.csv` -- 12 angles x 10 trials = 120 rows with
  the canonical t0004/t0012 schema `(angle_deg, trial_seed, firing_rate_hz)`. The per-trial seed is
  `1000 * angle_idx + trial_idx + 1`.

Running `score_envelope` emits:

* `data/score_report.json` -- full `ScoreReport` dataclass dump (loss, residuals, normalized
  residuals, weights, per-target pass flags, envelope pass flag, candidate + target metrics).
* `results/metrics.json` -- the four registered keys `direction_selectivity_index`,
  `tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse`.

Running `plot_tuning_curve` emits:

* `results/images/tuning_curve_dendritic.png` -- polar + Cartesian twin-panel tuning curve with the
  10 Hz peak-firing acceptance gate overlaid as a dashed line.

* * *

## Acceptance Gate (REQ-4)

The task accepts the run if both hold:

* `direction_selectivity_index >= 0.5`
* candidate peak firing rate >= 10 Hz

The t0022 baseline sweep achieves `direction_selectivity_index = 1.000` and peak = 15.0 Hz, passing
both gates. Matching the full t0004 shape envelope (HWHM and RMSE thresholds) is explicitly NOT
required -- see the plan's REQ-4 text.

* * *

## Dependencies

* `neuron` -- NEURON simulator (Windows build, `NEURONHOME` configured). Required for the HOC cell
  build, `Exp2Syn`/`NetStim`/`NetCon` point processes, and simulation driver.
* `numpy` -- vectorised onset-timing math and per-angle aggregation.
* `pandas` -- tuning-curve CSV read/write with the canonical t0004/t0012 schema.
* `tqdm` -- progress bar for the 12-angle x 10-trial sweep.
* `matplotlib` -- polar + Cartesian tuning-curve plot (only the `plot_tuning_curve` script needs
  it).
* Library `modeldb_189347_dsgc` from t0008 -- source of the HOC/MOD files, `build_dsgc()`,
  `apply_params()`, and synapse-coord helpers. The MOD-compiled `nrnmech.dll` is built locally
  inside `tasks/t0022_modify_dsgc_channel_testbed/build/modeldb_189347/` to avoid mutating t0008's
  folder.
* Library `tuning_curve_loss` from t0012 -- provides `score()` and `METRIC_KEY_*` constants used by
  `score_envelope`.

* * *

## Testing

No dedicated unit tests ship with this driver. The task's acceptance test is an end-to-end execution
of the full 12-angle sweep gated by the preflight validator:

```bash
# 1) Preflight gate (~30 s): 4 angles x 2 trials, DSI sign + >=5 Hz peak
uv run python -u -m tasks.t0022_modify_dsgc_channel_testbed.code.run_tuning_curve --preflight

# 2) Full sweep (~9-15 min) + scoring + plot
uv run python -u -m tasks.t0022_modify_dsgc_channel_testbed.code.run_tuning_curve
uv run python -u -m tasks.t0022_modify_dsgc_channel_testbed.code.score_envelope
uv run python -u -m tasks.t0022_modify_dsgc_channel_testbed.code.plot_tuning_curve
```

The preflight mode is itself the cheapest regression test -- it rebuilds the cell, rebuilds the
EiPairs, runs two trials each at four angles, and asserts DSI sign correctness and peak-firing
threshold before the full sweep is launched. `run_one_trial_dendritic` also runs a per-trial
baseline assertion that BIP synapse coordinates and `h.gabaMOD` match the snapshot captured before
the first trial -- this guards against silent regressions from accidental BIP rotation or `gabaMOD`
drift.

* * *

## Design Decisions

* **NetStim (not VecStim)**: The Windows NEURON 8.2.7 install at this workstation does not bundle
  `vecevent.mod`, so VecStim is unavailable. NetStim in burst mode
  (`number=N_SYN_EVENTS, noise=0, interval=SYN_EVENT_INTERVAL_MS, start=onset_ms`) is functionally
  equivalent for this driver.
* **Baseline synapses silenced**: t0008's bundled BIP/SAC synapses drive 13-15 Hz spontaneous
  spiking even with no moving bar. `_silence_baseline_hoc_synapses()` zeros the global scalars and
  calls `update() + placeBIP()` so the zeros propagate to every BIPsyn/SACinhibsyn/SACexcsyn
  instance; this ensures direction selectivity comes exclusively from the per-dendrite E-I pairs
  inserted by this driver.
* **Per-trial cell re-parameterisation**: `apply_params(h, seed=trial_seed)` is called at the start
  of every trial to ensure state is reset between trials. After that call, the driver re-silences
  the baseline synapses and re-asserts the BIP-coordinate + `gabaMOD` baseline.
* **Local build of `nrnmech.dll`**: `nrnivmodl` is run against the t0008-bundled MOD sources into
  `tasks/t0022_modify_dsgc_channel_testbed/build/modeldb_189347/`, not into the t0008 folder. The
  driver pre-loads this DLL via `h.nrn_load_dll` and sets t0008's `load_neuron._loaded` sentinel so
  the upstream bootstrap becomes a no-op re-entry.
* **5-region partition is empty at baseline**: The Poleg-Polsky morphology has no axon sections, so
  `AIS_PROXIMAL`, `AIS_DISTAL`, and `THIN_AXON` are empty. This is the correct testbed behaviour --
  follow-up channel-swap tasks will create axon sections and append to these SectionLists before
  calling their own `forsec` insertions.

* * *

## Main Ideas

* Direction selectivity is generated by **per-dendrite on-the-path shunting inhibition** with
  direction-dependent E-I timing offsets (+10 ms preferred, -10 ms null) and a 4x null/preferred
  GABA conductance ratio. The BIP-rotation proxy (t0008) and the global `gabaMOD`-swap proxy (t0020)
  are both explicitly rejected and guarded by a per-trial baseline assertion.
* The AIS is partitioned into **five named `SectionList` regions** (`SOMA_CHANNELS`,
  `DEND_CHANNELS`, `AIS_PROXIMAL`, `AIS_DISTAL`, `THIN_AXON`) with empty baseline `forsec` blocks.
  Downstream channel-swap tasks target a single region via a one-line `forsec <region> { ... }`
  edit, without editing the Python driver or the verbatim Poleg-Polsky HOC sources.
* The correct RGC proximal-AIS Na channel is **Nav1.1, not Nav1.2**. The original task description
  mis-cited cortical-pyramidal literature; VanWart 2006 is the correct RGC-specific source. The
  `AIS_PROXIMAL` SectionList is labelled for Nav1.1 insertion in follow-up tasks.
* The driver is **Windows-first**: it avoids VecStim in favour of NetStim bursts, builds
  `nrnmech.dll` locally rather than mutating the t0008 asset folder, and pre-loads the DLL via
  `h.nrn_load_dll` so the upstream bootstrap becomes a no-op re-entry.

* * *

## Summary

This library provides the Python driver, HOC channel-partition, and CLI scripts that turn the t0008
`modeldb_189347_dsgc` port into a per-dendrite on-the-path shunting-inhibition testbed. It replaces
t0008's bundled BIP/SAC synapse stack with direction-dependent AMPA + GABA_A `Exp2Syn` pairs placed
at sec(0.9) and sec(0.3) on every ON-dendrite, schedules them with Park 2014 / Koch-Poggio-Torre
timing priors, and runs the canonical 12-angle x 10-trial moving-bar sweep. The emitted tuning-curve
CSV is scored against the t0004 target via t0012's `tuning_curve_loss.score`, producing the four
registered metric keys plus a PNG plot.

The library is the seed testbed for a family of follow-up channel-swap tasks. Its five-region
`forsec` partition (`SOMA_CHANNELS`, `DEND_CHANNELS`, `AIS_PROXIMAL`, `AIS_DISTAL`, `THIN_AXON`)
lets downstream tasks edit a single region with a one-line block replacement, keeping the
direction-selectivity mechanism constant while varying individual channel isoforms. Suggestions
S-0022-01 through S-0022-08 enumerate the first wave of such experiments (Nav1.6 distal vs Nav1.1
proximal, Kv1.2 titration, Ih in dendrites, HCN-blocker comparison, etc.).

Known limitations: the AIS SectionLists are empty in the baseline testbed because the bundled
Poleg-Polsky morphology defines no axon sections. Downstream channel-swap tasks must first create
axon[] sections and connect them to the soma before appending to the AIS SectionLists. The
`tuning_curve_hwhm_deg` metric returns `null` at peak DSI because the shape envelope is degenerate
on a square-wave curve; only `direction_selectivity_index` and peak firing rate are gated at REQ-4.
