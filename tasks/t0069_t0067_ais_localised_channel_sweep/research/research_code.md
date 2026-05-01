---
spec_version: "1"
task_id: "t0069_t0067_ais_localised_channel_sweep"
research_stage: "code"
tasks_reviewed: 3
tasks_cited: 3
libraries_found: 1
libraries_relevant: 1
date_completed: "2026-05-01"
status: "complete"
---
# Research: Code Survey for t0069

## Task Objective

Identify the t0067 code surface that t0069 reuses, and the minimal NEURON-side mechanism for
appending a virtual AIS + axon cable to the deposited cell after construction.

## Library Landscape

Same as t0067/t0068: deposited modeldb_189347_dsgc library asset (cell builder + HHst + bipNMDA +
SAC mechanisms) plus t0067's vendored 5 channel MODs, recompiled into a t0069-local DLL. The t0067
MOD files are reused verbatim.

## Methodology Review

Read in full:

* `tasks/t0067_t0065_soma_channel_addition_sweep/code/run_sweep.py` — soma-localised driver.
* `tasks/t0067_t0065_soma_channel_addition_sweep/code/constants.py` — CHANNEL_DEFS.
* `tasks/t0019_literature_survey_voltage_gated_channels/assets/answer/...` — AIS Nav/Kv density
  priors (2500-5000 pS/μm² for distal AIS Nav1.6 → 25-50 mS/cm²).

## Key Findings

### 1. AIS-extension mechanism in NEURON

* `h.Section(name=...)` creates a new Section. After construction, set `L`, `diam`, `nseg`
  attributes. `insert("HHst")` adds the active mechanism. `connect(parent, parent_x, this_x)`
  attaches.
* Per-segment property setting: `for seg in section: seg.HHst.gnabar = ...`
* The deposited cell's soma is `h.RGC.soma`. Calling `ais.connect(h.RGC.soma, 1.0, 0.0)` attaches
  the AIS at the distal end of the soma.

### 2. AIS / axon densities (per t0019 priors)

* Nav (HHst gnabar): AIS distal ~2500-5000 pS/μm² ↔ 25-50 mS/cm². We use 30.
* Kv (HHst gkbar): typically ~20 mS/cm² at the AIS. We use 20.
* Km (HHst gkmbar): low, ~3 mS/cm² across AIS and axon.
* Axon (passive-ish): low Na (~5 mS/cm²) sufficient for propagation, low K.

### 3. Reusable t0067 patterns

* MOD files: copy verbatim (Nav1.6, NaP, NaR, Kv3, Kv4) into t0069's `code/mods/`.
* Trial driver: copy structure but switch insertion target from soma to AIS.
* Channel-isolation: per-trial set ONE channel's gbar to non-zero on AIS; others zero.
* Spike detection: NetCon on `h.RGC.soma(0.5)._ref_v` at threshold -10 mV (recording somatic spikes
  is the experimental analogue).
* Idempotent DLL load via module-level flag.

### 4. Differences from t0067

* New module `code/extend_with_ais.py` adds the AIS + axon sections.
* Two new sections live alongside the deposited cell's existing sections (no modification to t0008's
  HOC).
* The 5 t0067 mechanisms are inserted on the AIS only — NOT the soma (the whole point is
  AIS-localisation).
* Baseline differs: t0069 baseline = "AIS + axon attached, no extra channels" — expected to differ
  from t0067 baseline because of the added electrical sink.

### 5. Expected sweep behaviour

* Smoke test (3 trials) showed the AIS + axon attachment HALVED baseline firing (14 → 7 PD spikes)
  and that Nav1.6_med + Kv3_high on AIS showed no immediate change. This suggests the soma-initiated
  spike still dominates. The full sweep will reveal whether ANY (channel, density, direction)
  combination on AIS shows measurable effect.

## Reusable Code and Assets

* t0008 cell builder + HOC.
* t0067 MOD files (5 channels, NONSPECIFIC_CURRENT pattern).
* t0067 trial driver pattern (apply_params → gabaMOD → exptype → ... pipeline).
* t0067/t0068 idempotent DLL-load pattern.

## Lessons Learned

* From t0067: build cell once, reuse across trials.
* From t0067/t0068: NONSPECIFIC_CURRENT MODs avoid USEION conflicts.
* From t0067/t0068: separate task-local DLL loaded after t0008's main DLL.
* From smoke test here: adding AIS+axon to a cell whose soma already has 400 mS/cm² Na is unlikely
  to relocate the spike-initiation site without REDUCING somatic Na first. This is a scope choice:
  t0069 preserves t0067 baseline cell behaviour and ADDS the AIS as a parallel compartment. A future
  task could reduce somatic Na to make the AIS the dominant initiator.

## Recommendations for This Task

1. Copy 5 MOD files from t0067 into t0069/code/mods.
2. Compile t0069-local DLL.
3. Write `code/extend_with_ais.py` to attach AIS + axon to the deposited cell after build.
4. Write `code/run_sweep.py` mirroring t0067 but with AIS-targeted channel insertion.
5. Plot with cross-task comparison to t0067.

## Task Index

* **t0008_port_modeldb_189347** — cell builder.
* **t0019_literature_survey_voltage_gated_channels** — AIS Nav/Kv density priors.
* **t0067_t0065_soma_channel_addition_sweep** — primary parent. MOD files, driver pattern,
  soma-anchor DSIs for cross-comparison.
* **t0065_t0020_epsp_ipsp_vm_protocol** — gabaMOD-swap protocol.
