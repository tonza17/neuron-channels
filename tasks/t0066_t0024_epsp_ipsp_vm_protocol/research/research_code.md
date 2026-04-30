---
spec_version: "1"
task_id: "t0066_t0024_epsp_ipsp_vm_protocol"
research_stage: "code"
tasks_reviewed: 2
tasks_cited: 2
libraries_found: 1
libraries_relevant: 1
date_completed: "2026-04-30"
status: "complete"
---
# Research: Code Survey for t0066

## Task Objective

Identify the t0024 de Rosenroll 2026 DSGC code surface that t0066 reuses, and the exact knobs to
toggle for EPSP_PASSIVE / IPSP_PASSIVE / FULL channel isolation. The goal is to define a precise
implementation recipe before writing `code/run_protocol.py`.

## Library Landscape

The relevant library asset is `de_rosenroll_2026_dsgc` (registered as a library asset in
`tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/`). This is the only
project library used by t0066. It supplies the compiled `nrnmech.dll` containing `HHst`, `Exp2NMDA`,
`cadecay`, and the `RGCmodelGD.hoc` morphology template (341 sections, 177 terminal dendrites).
t0066 also reuses Python infrastructure from `tasks/t0024_port_de_rosenroll_2026_dsgc` itself: the
cell builder, AR(2) noise generator, synapse setup helpers, and per-trial driver template (see
Reusable Code section).

## Methodology Review

Read the following five t0024 files in full:

* `tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/code/ar2_noise.py`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/code/paths.py`

## Key Findings

### 1. Cell construction

* **API**: `build_dsgc_cell()` from `tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell`
  (`build_cell.py:251`).
* **Returns** a frozen dataclass `DSGCCell` (`build_cell.py:94-107`) exposing: `h`, `rgc`, `soma`,
  `all_dends`, `primary_dends`, `non_terminal_dends`, `terminal_dends`, `terminal_locs_xy` (numpy n
  × 2 array), `origin_xy` tuple.
* **Synapses are NOT in this dataclass** — they are constructed on-demand in
  `run_tuning_curve.py::_setup_synapses()` (`run_tuning_curve.py:189`) which returns a
  `SynapseBundle` (`run_tuning_curve.py:178-186`) with `syns_ach`, `syns_gaba`, `ncs_ach`,
  `ncs_gaba`, `netstims`.

### 2. HH channel knobs

* Mechanism is `HHst` (NOT `HHst_noiseless`). Inserted on soma + all dendrites.
* Parameter names: `gnabar_HHst`, `gkbar_HHst`, `gkmbar_HHst`, `gleak_HHst`, `eleak_HHst`
  (`build_cell.py:195-199, 220-224, 231-233, 242-246`).
* Per-tier densities (S/cm²):
  * Soma: `gnabar = 0.15`, `gkbar = 0.035`, `gkmbar = 0.003`.
  * Primary dendrites: `gnabar = 0.20`, `gkbar = 0.035`, `gkmbar = 0.003`.
  * Non-terminal mid dendrites: `gnabar = 0.0`, `gkbar = 0.025`, `gkmbar = 0.003`.
  * Terminal dendrites: `gnabar = 0.03`, `gkbar = 0.025`, `gkmbar = 0.003`.
* Calcium decay mechanism `cad` is also inserted but is buffering only — not an active
  conductance. No Cav, Kca, or other ligand-gated active mechanisms.
* **HH-off recipe**: zero `gnabar_HHst` and `gkbar_HHst` on every section after build (or just zero
  `gnabar_HHst` since that is the spike-generating channel). To match t0065's full HH-off semantics,
  also zero `gkmbar_HHst`.

### 3. Synapse silencing knobs

* Both ACh and GABA are `Exp2Syn` objects, one of each per terminal dendrite (177 ACh + 177 GABA =
  354 total).
* `NetCon` weights are accessible via `bundle.ncs_ach[i].weight[0]` and
  `bundle.ncs_gaba[i].weight[0]` (`run_tuning_curve.py:210, 217`).
* **Cleanest silence recipe**: set `nc.weight[0] = 0` on all NetCons of the class to silence before
  queuing events. Exp2Syn `gmax` is bound at conductance level so direct gmax manipulation is not
  exposed in current API and would require accessing `bundle.syns_ach[i]`.
* Default weights: `ACH_WEIGHT_US = 0.001`, `GABA_WEIGHT_US = 0.003` (`constants.py:48, 53`).

### 4. Per-trial driver

* `run_single_trial()` (`run_tuning_curve.py:235-321`) is the per-trial entry point. It:
  1. Computes per-synapse bar arrival times via `_bar_arrival_times()` (`run_tuning_curve.py:250`).
  2. Generates AR(2) noise traces with cross-correlation `rho` via `generate_ar2_batch()`
     (`run_tuning_curve.py:257`).
  3. Computes directional GABA release probability via `_gaba_prob_for_direction()` sigmoid
     (`run_tuning_curve.py:267`).
  4. Converts rates to Poisson events per synapse (`run_tuning_curve.py:272-284`).
  5. Schedules events via `FInitializeHandler` + `NetCon.event()` (`run_tuning_curve.py:298`).
  6. Records soma Vm into `v_vec`, runs `h.continuerun(TSTOP_MS)` (`run_tuning_curve.py:301-311`).
  7. Counts spikes by post-hoc threshold crossings on `v_vec` (`run_tuning_curve.py:313-321`).
* **Returns** `TrialResult(trial, direction_deg, spike_count, peak_mv)` — scalars only. The Vm
  trace is discarded.
* **Override injection point**: set NetCon `weight[0]` values on `bundle.ncs_ach` /
  `bundle.ncs_gaba` AFTER `_setup_synapses()` returns and BEFORE `_queue()` runs (i.e., at the top
  of `run_single_trial()`).

### 5. Direction encoding

Three independent mechanisms (more than t0065's single `gabaMOD` scalar):

1. **Bar geometry**: `_bar_arrival_times()` projects each synapse's (x, y) onto the velocity axis at
   angle `direction_deg` (`run_tuning_curve.py:92-109`).
2. **GABA release-probability sigmoid**: `_gaba_prob_for_direction()` maps `direction_deg` to
   release probability in [PREF_GABA_PROB=0.05, NULL_GABA_PROB=0.80] (`run_tuning_curve.py:80-89`).
3. **No cell rotation** — the cell is fixed; `CELL_PREF_DEG = 0.0` (rightward) is hard-coded
   (`run_tuning_curve.py:57`).

For t0066, PD = `direction_deg = 0.0` and ND = `direction_deg = 180.0`.

### 6. Resting potential and inhibitory reversal — CRITICAL FINDING

* `V_INIT_MV = -60.0` (`constants.py:23`)
* `ELEAK_MV = -60.0` (`constants.py:30`)
* `GABA_EREV_MV = -60.0` (`constants.py:52`)

**All three are identical.** The de Rosenroll model uses **the same design pattern as the deposited
Poleg-Polsky cell**: GABA reversal pinned to the leak/resting potential, producing **pure shunting
inhibition**. This corrects the original task description's hypothesis that t0066's IPSP_PASSIVE
would be hyperpolarising — it will likely be flat at -60 mV in both PD and ND, just like t0065.
The design pattern is **recurring, not idiosyncratic to Poleg-Polsky**, and t0066's value is
precisely confirming this convergence across two structurally independent implementations.

The `*_PAPER_TEXT` constants in `constants.py:93-94` show the paper text actually specifies
`ELEAK_MV_PAPER_TEXT = -70.0` mV (a true hyperpolarising rest below e_GABA), but the upstream code
authority used -60 mV. This is itself a useful finding — published papers often diverge from their
accompanying code.

### 7. Trial duration and sampling

* `TSTOP_MS = 1000.0` ms.
* `DT_MS = 0.1` ms.
* `STEPS_PER_MS = 10.0`.
* Samples per trial: ~10,001 (consistent with t0065).

### 8. Per-trial wall-clock

* No hardcoded estimate. Per-trial timing is logged at runtime
  (`run_tuning_curve.py:345, 354, 358-360`).
* External estimate from t0024 results: 4h15m / 240 trials ≈ **64 s/trial**.
* For HH-off trials, CVODE/fixed-step time may be similar or slightly faster; allow ~64 s/trial
  conservatively.

### 9. Spike detection

* `_count_spikes()` (`run_tuning_curve.py:229-232`) counts rising-edge threshold crossings on the
  recorded Vm trace at `AP_THRESHOLD_MV = -10.0 mV` (`constants.py:24`).
* Implementation: `np.sum((~above[:-1]) & above[1:])` where `above = v_trace > threshold`.
* This is post-hoc, not via `NetCon` — so spike counting works for FULL trials and trivially
  returns 0 for passive trials where Vm never crosses -10 mV.

### 10. Return data format

* `TrialResult` (`run_tuning_curve.py:64-68`) is scalar-only.
* The per-sample Vm trace is captured into `v_vec` (h.Vector) and discarded after spike counting.
* **For t0066**: extract the Vm trace before discard. Easiest approach: copy `run_single_trial` into
  t0066's `code/run_protocol.py` and modify the return dataclass to include
  `v_trace: NDArray[np.float64]` and `t_trace: NDArray[np.float64]`. Also add a `mode` field.

## Reusable Code and Assets

* **Library asset**: `de_rosenroll_2026_dsgc` — provides `nrnmech.dll`, `RGCmodelGD.hoc`,
  morphology files. Loaded via `paths.py` constants and `nrn_load_dll`.
* **Cell builder**: `tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell.build_dsgc_cell()` —
  reusable verbatim. Returns `DSGCCell` dataclass.
* **Synapse setup**:
  `tasks.t0024_port_de_rosenroll_2026_dsgc.code.run_tuning_curve._setup_synapses()` — must be
  copied (private function). Returns `SynapseBundle` with the NetCon lists we need to silence.
* **AR(2) noise**: `tasks.t0024_port_de_rosenroll_2026_dsgc.code.ar2_noise.generate_ar2_batch()` —
  reusable.
* **Direction helpers**: `_bar_arrival_times` and `_gaba_prob_for_direction` from
  `run_tuning_curve.py` — must be copied.
* **t0065 reference**: `tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/run_protocol.py` — the
  EPSP_PASSIVE / IPSP_PASSIVE / FULL trial-mode pattern. Different cell, but same loop shape and
  same per-trial CSV layout convention.

## Lessons Learned

* From t0065 (immediate predecessor): silencing one synapse class is not enough — also need
  belt-and-braces zeroing of any auxiliary input pathway (t0065 had to additionally zero ACh on
  IPSP_PASSIVE because the deposited code had a SAC ACh drive that wasn't covered by zeroing bipolar
  AMPA/NMDA alone). For t0066, the synapse model is simpler (one ACh + one GABA per terminal), so a
  single `nc.weight[0] = 0` per class should suffice.
* From t0065: the IPSP_PASSIVE trace was flat at e_SACinhib because the cell's resting potential
  equals the chloride reversal. The same constraint applies here (V_INIT = ELEAK = GABA_EREV = -60
  mV) — IPSP_PASSIVE is expected to be flat in t0066 too.
* From t0024: per-trial wall-clock is ~64 s; budget accordingly.
* From t0024: the Vm trace is captured but discarded; t0066 must extract it.

## Recommendations for This Task

1. Copy and adapt `run_tuning_curve.py::run_single_trial` into a new `code/run_protocol.py` in
   t0066. Modify to:
   * Accept a `mode` argument (`FULL`, `EPSP_PASSIVE`, `IPSP_PASSIVE`).
   * After `_setup_synapses()`, apply per-mode silencing:
     * `EPSP_PASSIVE`: `for nc in bundle.ncs_gaba: nc.weight[0] = 0`. Zero `gnabar_HHst`,
       `gkbar_HHst`, `gkmbar_HHst` on soma + all dendrites.
     * `IPSP_PASSIVE`: `for nc in bundle.ncs_ach: nc.weight[0] = 0`. Zero HHst as above.
     * `FULL`: no overrides.
   * Capture `v_vec` and `t_vec` into numpy arrays and return them in `TrialResult`.
2. Reuse t0024's `paths.py` constants for the library asset DLL location (it's the same NEURON
   mechanism set).
3. Use t0024's `_setup_synapses`, `_bar_arrival_times`, `_gaba_prob_for_direction`, AR(2) noise
   helpers verbatim — no need to re-derive.
4. Plot script: separate from run script. Reads CSV, computes per-trial mean trace ± IQR per (mode,
   direction), emits 5 PNGs (FULL/EPSP/IPSP per-mode PD vs ND with IQR shading; PD and ND three-mode
   overlays) plus a 6th cross-model comparison panel against t0065's IPSP_PASSIVE traces.

## Risk Assessment

* **Risk: GABA shunt won't be visible in IPSP_PASSIVE Vm trace** — likely true, given e_GABA =
  v_rest. Acceptable; this becomes the headline finding (cross-model convergence on shunting
  design).
* **Risk: Setting `weight[0] = 0` doesn't actually silence the synapse** — Exp2Syn current is
  `g * (V - E)`, and `g` is integrated from synaptic events scaled by NetCon weight. Zero weight ⇒
  no `g` increase ⇒ no current. Should work, but verify in a smoke trial.
* **Risk: Zeroing `gnabar_HHst` on soma alone is insufficient** — terminal dendrites also carry
  `gnabar_HHst = 0.03 S/cm²` (`build_cell.py:242`), so passive trials may still spike
  dendritically. Solution: zero across all sections (soma, primary, non-terminal, terminal).

## Task Index

Prior tasks reviewed for this research stage:

* **t0024_port_de_rosenroll_2026_dsgc** — primary code source. Cell builder, AR(2) noise, synapse
  setup, per-trial driver template, trial-duration constants. All Python infrastructure reused or
  adapted by t0066.
* **t0065_t0020_epsp_ipsp_vm_protocol** — protocol reference. Different cell substrate (deposited
  Poleg-Polsky), but same EPSP_PASSIVE / IPSP_PASSIVE / FULL trial-mode pattern, same per-trial CSV
  layout, same results-detailed.md spec_version 2 structure.

Other DSGC tasks in the project (t0008, t0020, t0022, t0023, t0030, t0033-t0036, t0046, t0049,
t0052-t0064) were considered but not relevant: they all use the deposited Poleg-Polsky lineage, not
the de Rosenroll substrate. t0023 (Hanson port) was reserved as a third independent implementation
but was not used here.

## References

* `tasks/t0024_port_de_rosenroll_2026_dsgc/code/{build_cell,run_tuning_curve,constants,ar2_noise,paths}.py`
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/run_protocol.py` — t0065 reference for the
  EPSP/IPSP/FULL trial loop pattern.
