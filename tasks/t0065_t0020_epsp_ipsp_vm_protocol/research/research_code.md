---
spec_version: "1"
task_id: "t0065_t0020_epsp_ipsp_vm_protocol"
research_stage: "code"
tasks_reviewed: 5
tasks_cited: 5
libraries_found: 1
libraries_relevant: 0
date_completed: "2026-04-30"
status: "complete"
---
# Research Code: Test t0020 deposited DSGC under EPSP_PASSIVE / IPSP_PASSIVE / FULL protocol

## Task Objective

Apply the trial-mode protocol established in t0059 (`EPSP_PASSIVE`, `IPSP_PASSIVE`, `FULL`) to the
deposited Poleg-Polsky & Diamond 2016 ModelDB 189347 DSGC used in t0020. Decompose the somatic
voltage trace into pure-excitatory (HH off, GABA off) and pure-inhibitory (HH off, AMPA + NMDA off)
components in PD and ND directions, plus a reference HH-on FULL trace. Single seed per (mode,
direction) combination — six trials total. The result must show how a model that produces graded
direction selectivity decomposes its EPSP and IPSP drives, giving us a known-good reference for
debugging the binary regime trapping the from-scratch DSGC family.

## Library Landscape

The library aggregator surfaces `modeldb_189347_dsgc_gabamod` (created by t0020) as the only
relevant library asset for this work. It is a thin wrapper around the deposited cell that documents
the gabaMOD-swap protocol; its `code/` directory is not directly importable as a library because the
project does not currently install task assets as Python packages. The actual reusable code lives in
`tasks/t0008_port_modeldb_189347/code/`, which is imported as a Python package — a project
convention recorded in `CLAUDE.md` (`from tasks.tNNNN_slug.code.X import Y`). All other tasks in
this family (t0008, t0020, t0046, t0049) follow the same direct-import convention. No new library
asset is needed for this task: t0065 imports directly from t0008 and produces only diagnostic plots.

## Key Findings

### Cell construction is centralised in `tasks.t0008.code.build_cell`

`build_dsgc()` returns a NEURON `h` handle with the full deposited cell instantiated, point
processes wired, and HOC procs (`update`, `placeBIP`, `simplerun`, `init_active`) loaded [t0008].
`read_synapse_coords(h)` snapshots BIP/SACinhib/SACexc per-synapse positions so downstream code can
assert positions stay at baseline (the rotation-leak guard pioneered in t0008 and reused unchanged
in t0020 [t0020]).

`apply_params(h, seed=seed)` writes `b2gampa`, `b2gnmda`, `s2ggaba`, `s2gach`, `gabaMOD`, `achMOD`,
stimulus geometry, HHst tuning, and NMDA voltage-dependence to canonical paper values, then sets
`seed2 = seed` for the rBIP/rnoise/rtime random streams [t0008]. It does **not** touch `SpikesOn`
— the deposited HOC default is `SpikesOn=1` which is what t0008 and t0020 inherit.

### `simplerun()` clobbers conductance globals — overrides must be applied AFTER it

The deposited `simplerun(exptype, direction)` proc unconditionally rewrites `b2gampa = 0.25`,
`b2gnmda = 0.5 * nmdaOn`, `s2ggaba = 0.5`, `s2gach = 0.5`, `gabaMOD = 0.33 + 0.66 * direction`, and
`achMOD = 0.33` (`dsgc_model_exact.hoc:316-328`). It also rebinds `exptype = 2 - SpikesOn`, then
calls `init_active()`, `update()`, `placeBIP()`, and `run()` [t0046]. This means any Python-side
override of `b2gampa`, `b2gnmda`, or `gabaMOD` that is set *before* `simplerun()` is silently lost.

The t0049 channel-isolation code solves this with a four-step pattern: (1) call
`simplerun(int(ExperimentType.CONTROL), int(direction))` to trigger stimulus generation with
canonical conductances and discard its run, (2) write the desired conductance overrides directly to
`h`, (3) re-call `h("update()")` and `h("placeBIP()")` so the synaptic point processes pick up the
new globals, (4) attach fresh recorders and call `finitialize` + `continuerun`. The pattern is
documented at `tasks/t0049_seclamp_cond_remeasure/code/run_seclamp.py:74-148` [t0049].

### `SpikesOn` controls HH activation; setting it before `simplerun()` is sufficient

`init_active()` reads the `exptype` global to decide TTX state: `TTX = (exptype == 2)`. When TTX is
1, `RGCsomana = 0.4 * active * (1 - TTX) = 0`, and the subsequent `update()` writes
`gnabar_HHst = 0` to all soma sections (`dsgc_model_exact.hoc:115-150, 261-285`). Because
`simplerun()` rebinds `exptype = 2 - SpikesOn` before calling `init_active()`, setting
`h.SpikesOn = 0` from Python *before* `simplerun()` is enough to disable the somatic Na+ channel
density for that trial [t0046]. t0046's `run_simplerun.py:105` uses exactly this pattern for its
PSP-vs-AP measurements.

### Trial-mode enum from t0059 is the canonical naming

The from-scratch family standardised on a `TrialMode` enum (`FULL`, `EPSP_PASSIVE`, `IPSP_PASSIVE`)
[t0059]. Although the from-scratch substrate is unrelated to the deposited cell, the enum spelling
is reused here for consistency across the project's diagnostic protocols.

## Reusable Code and Assets

| Source | What it does | Reuse method | Adaptation |
| --- | --- | --- | --- |
| `tasks/t0008_port_modeldb_189347/code/build_cell.py::build_dsgc` | Builds deposited DSGC, returns `h` handle. | **import via task package** | None. Direct call. |
| `tasks/t0008_port_modeldb_189347/code/build_cell.py::apply_params` | Writes canonical paper params + per-trial seed. | **import via task package** | None. Direct call with `seed=1`. |
| `tasks/t0008_port_modeldb_189347/code/build_cell.py::read_synapse_coords` | Snapshots BIP/SAC synapse positions. | **import via task package** | None. Used to guard against rotation re-engagement. |
| `tasks/t0008_port_modeldb_189347/code/build_cell.py::SynapseCoords` | Dataclass holding per-synapse positions. | **import via task package** | None. Used as the type for `baseline` in the guard call. |
| `tasks/t0020_port_modeldb_189347_gabamod/code/run_gabamod_sweep.py::_assert_bip_positions_baseline` | Asserts BIP positions match baseline; guards against silent rotation re-engagement. | **copy into task** | Rename to `assert_bip_positions_baseline` (drop leading underscore for cross-module use). |
| `tasks/t0049_seclamp_cond_remeasure/code/run_seclamp.py::_apply_channel_overrides` (pattern) | Channel-isolation overrides applied AFTER `simplerun()`. | **adapt** | Re-implement for our three modes (`EPSP_PASSIVE` zeroes `gabaMOD`; `IPSP_PASSIVE` zeroes `b2gampa` and `b2gnmda`; `FULL` is the canonical `simplerun()` output, no override). |
| `tasks/t0046_reproduce_poleg_polsky_2016_exact/code/constants.py::ExperimentType.CONTROL`, `Direction.PREFERRED`, `Direction.NULL` | IntEnum mapping to simplerun args. | **copy into task** | Define equivalents locally rather than introduce a t0046 dependency for two int constants. |
| `tasks/t0008_port_modeldb_189347/code/constants.py::V_INIT_MV`, `TSTOP_MS`, `AP_THRESHOLD_MV`, `GABA_MOD`, `B2GAMPA_NS`, `B2GNMDA_NS` | Canonical paper values. | **import via task package** | None. Used for `finitialize`, `continuerun`, spike thresholding, and reporting. |

## Lessons Learned

* **t0020 finding** [t0020]: The deposited cell under `gabaMOD = 0.33` (PD) versus `gabaMOD = 0.99`
  (ND) produces DSI = 0.7838 inside the literature envelope but peak firing of only ~14.85 Hz
  (envelope is 40-80 Hz). The decomposition this task pursues will tell us whether the gap is
  excitatory under-drive, excessive inhibition, or HH calibration.
* **t0046 finding** [t0046]: The deposited `simplerun()` proc internally calls `init_active()` and
  `placeBIP()`, so any Python-side override of conductances must come **after** simplerun returns.
  The pattern of "discard one simplerun, then override + re-update + re-placeBIP" was proven correct
  in t0046 and t0049.
* **t0008 finding** [t0008]: Direction selectivity in the deposited cell can be driven *either* by
  spatial rotation of synapse positions *or* by the gabaMOD scalar swap. The task description for
  t0065 explicitly takes the gabaMOD-swap route, matching t0020. The
  `_assert_bip_positions_baseline` guard catches accidental engagement of the rotation path.
* **t0049 lesson** [t0049]: Releasing the Python reference to a SEClamp object mid-trial lets NEURON
  garbage-collect it, killing the recording. We do not insert a clamp in t0065, but the same care
  applies to recording vectors — keep them bound throughout the trial.

## Recommendations for This Task

1. **Cell construction**: Build once via `build_dsgc()` at module load, snapshot synapse coords via
   `read_synapse_coords`, then reuse the same `h` handle across all six trials. Matches t0008 /
   t0020 / t0046 practice.
2. **Trial structure**: For each `(mode, direction)` pair, run the four-step t0049 pattern —
   `apply_params` + set `SpikesOn` before `simplerun`, run a discarded `simplerun`, override
   conductances, re-`update` + re-`placeBIP`, attach Vm + t recorders, call `finitialize` +
   `continuerun`.
3. **Mode encoding**: `FULL` keeps `SpikesOn = 1` and applies no override. `EPSP_PASSIVE` sets
   `SpikesOn = 0` and zeroes `gabaMOD`. `IPSP_PASSIVE` sets `SpikesOn = 0` and zeroes both `b2gampa`
   and `b2gnmda`.
4. **Direction encoding**: Pass `Direction.PREFERRED` (`= 0`) for PD and `Direction.NULL` (`= 1`)
   for ND as the second arg of `simplerun()`. Internally simplerun writes
   `gabaMOD = 0.33 + 0.66 * direction`, matching t0020's convention.
5. **Output schema**: Long-format trace CSV `(mode, direction, t_ms, v_mv)` so a single matplotlib
   read can produce per-mode and three-mode-overlay plots. Per-trial scalar metrics (`peak_v_mv`,
   `baseline_v_mv`, `peak_minus_baseline_mv`, `spike_count`) in `metrics.json`.
6. **Verification**: Re-use the BIP-position guard at every trial; this is the same guard t0020 used
   [t0020].

## Task Index

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 DSGC under spatial-rotation drifting-bar protocol
* **Status**: completed
* **Relevance**: Original port of the deposited cell. Source of `build_dsgc`, `apply_params`,
  `read_synapse_coords`, and `SynapseCoords` — every t0065 trial calls these helpers.

### [t0020]

* **Task ID**: `t0020_port_modeldb_189347_gabamod`
* **Name**: Port ModelDB 189347 DSGC under native gabaMOD parameter-swap protocol
* **Status**: completed
* **Relevance**: Direct dependency. Establishes the PD = 0.33 / ND = 0.99 gabaMOD-swap convention
  and provides the `_assert_bip_positions_baseline` guard pattern; produced DSI = 0.7838 with peak
  14.85 Hz — the FULL-mode reference t0065 will record.

### [t0046]

* **Task ID**: `t0046_reproduce_poleg_polsky_2016_exact`
* **Name**: Reproduce Poleg-Polsky 2016 figures via deposited model
* **Status**: completed
* **Relevance**: Documents `simplerun()` semantics in detail (`run_simplerun.py:1-50, 102-152`) and
  shows that `SpikesOn = 0` followed by `simplerun(...)` yields a clean sub-threshold PSP
  measurement. t0065 reuses the same `SpikesOn` toggle.

### [t0049]

* **Task ID**: `t0049_seclamp_cond_remeasure`
* **Name**: SEClamp channel-isolation conductance re-measurement
* **Status**: completed
* **Relevance**: Source of the channel-isolation override-then-rerun pattern
  (`run_seclamp.py:74-148`). t0065 adapts the same pattern without the SEClamp insertion.

### [t0059]

* **Task ID**: `t0059_bar_locked_gaba_ampa_sweep_t0057`
* **Name**: Bar-arrival-locked tonic GABA + AMPA escape sweep on the from-scratch substrate
* **Status**: completed
* **Relevance**: Established the `TrialMode` naming convention (`FULL`, `EPSP_PASSIVE`,
  `IPSP_PASSIVE`) that t0065 reuses for cross-task consistency.
