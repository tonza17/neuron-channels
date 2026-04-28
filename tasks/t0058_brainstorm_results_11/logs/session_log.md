# Brainstorm Session 11 — Full Transcript

## Project State Presented

**Date**: 2026-04-29. **Project**: DSGC compartmental model — optimise morphology / synapses /
VGCs to match a target angle-to-AP-frequency tuning curve. **Stats at session open**: 57 tasks
completed across 10 brainstorm sessions. Budget $1.00 total, $0.00 spent. Last brainstorm: t0056
(session 10, 2026-04-28).

### Tasks completed since brainstorm 10 (the new evidence)

| Task | Headline result |
| --- | --- |
| t0055_nmda_mg_block_dsi_recovery | Mg-block NMDA recovers vector-sum DSI to **0.7464** (vs t0054's 0.082) — but peak Hz stuck at **0.667 Hz** in FULL because Mg-block keeps NMDA blocked under scalar gabaMOD inhibition. PARTIAL pass on S-0054-01. |
| t0057_tonic_gaba_sweep_t0053 | **Negative result**. Tonic GABA on t0053 spatial substrate at any of {0.25, 0.5, 1.0, 1.5, 2.0} nS produces DSI = 0. Below 1.5 nS: single-spike regime (peak = null = 0.667 Hz). At 1.5+ nS: full suppression. Spatial gating intact, IPSP envelope sustained as designed. |

### Convergent problem identified

Across the entire from-scratch minimal-DSGC family (t0052/t0053/t0054/t0055/t0057), the cell is
stuck in a **binary regime** — either single-spike-per-trial (DSI = 1.0 trivially) or full
suppression (DSI = 0). The cell needs to escape into the **5-50 Hz multi-spike** band before DSI
metrics are biologically informative. The Mg-block result (t0055) shows the substrate *can* recover
DSI structurally but only when GABA is so weak the cell never depolarises enough to unblock NMDA,
leaving peak rate trivially low.

### AI's reassessed priority of the 32 active high-priority suggestions

Highest-value actionable suggestions:

1. **S-0055-01** — project-wide measurement-protocol fix (EPSP_PASSIVE/IPSP_PASSIVE/FULL trio with
   HH save-and-zero, 1400 ms window). Memory note from earlier session confirmed.
2. **S-0055-03** — GABA-reduction ladder on Mg-block t0055 architecture.
3. **S-0057-06** — combine tonic GABA + Mg-block NMDA on a single architecture (synthesis of t0055
   and t0057).
4. **S-0057-02 / S-0052-01** — AMPA conductance escape sweep.
5. **S-0002-01** — factorial g_Na × g_K (RQ1, untouched).

Suggestions to revise downward (proposed, presented as preview):

* Older tooling/scaffold: S-0007-01, S-0010-05, S-0011-01, S-0012-01, S-0013-01, S-0013-02.
* Deposited-DSGC / Hanson / deRosenroll line: S-0003-02, S-0008-01, S-0024-01, S-0046-02, S-0020-01,
  S-0020-02.
* Morphology calibration: S-0009-01, S-0009-02, S-0009-03.
* Bipolar kinetics tied to t0024: S-0027-02.
* From-scratch comparisons: S-0052-04, S-0053-03, S-0053-02.

## Clarification Questions

AI asked five clarifying questions:

1. Notes / context — anything beyond the saved memory note on the EPSP_PASSIVE/IPSP_PASSIVE/FULL
   protocol?
2. Priority axis — measurement-protocol fix first, escape single-spike regime first, or both in
   parallel?
3. Wave size — small focused (1-3) or broader batch (4-6)?
4. Compute — local CPU or commission t0045 CoreNEURON Vast.ai benchmark first?
5. Stale-suggestion pruning — OK to propose rejections / reprioritisations of older items?

The researcher answered Round 1 directly without separate clarification, by specifying which
suggestions to combine into a single task — which implicitly answered the wave-size and priority-
axis questions.

## Discussion — Round 1: New Tasks

**Researcher**: "I like the s0057-02 suggestion. However, I would like you to combine it with
s0057-01 (add sub 0.25 conductances) and also s0057-04 in one single task. They biologically
plausible"

**AI proposed combined task design** — t0058 (later renumbered to t0059):

* Substrate: forks t0057's `minimal_dsgc_tonic_gaba_sweep` library; same morphology, placement seed,
  100 E + 100 I co-located synapses, AMPA-only (no NMDA) excitation.
* Mechanism change (from S-0057-04): per-synapse bar-arrival-locked GABA windows.
  `t_on_i = (x_i cos(theta) + y_i sin(theta)) / v + 100 ms`; `t_off_i = t_on_i + window_ms`.
* Sweep:
  * `gAMPA` ∈ {0.5, 1.0, 2.0, 3.0, 5.0} nS (S-0057-02 escape range)
  * `GABA_BASE_NS` ∈ {0.1, 0.2, 0.5, 1.0, 2.0} nS (combines S-0057-01 sub-veto + multi-spike)
  * `window_ms` = 200 ms (fixed, biologically motivated midpoint of 100-300 ms SAC IPSC range)
* 25 grid cells × 360 trials = 9000 trials, ~8.75 h wall-clock on local CPU.
* Trial mode trio: corrected EPSP_PASSIVE/IPSP_PASSIVE/FULL per memory note (implies S-0055-01 needs
  to land first OR be bundled).

AI asked four design questions:

1. Window_ms: fix at 200 ms or sweep across {100, 200, 400}?
2. Protocol fix dependency: separate task first (option a), or bundle into t0058 (option b)?
3. AMPA top: keep 5 nS or trim to 4 nS?
4. Grid resolution: 5×5 acceptable or denser?

**Researcher**: "1. just one grid, no need to sweep at this point. 2. b. 3. trim. 4. acceptable"

**AI confirmed locked design**:

* `gAMPA` ∈ {0.5, 1.0, 2.0, 3.0, **4.0**} nS (top trimmed)
* `GABA_BASE_NS` ∈ {0.1, 0.2, 0.5, 1.0, 2.0} nS
* `window_ms` = 200 ms (fixed)
* Protocol fix bundled — t0059 will be the first task to ship the EPSP_PASSIVE/IPSP_PASSIVE/FULL
  trio with HH save-and-zero, drop activation histogram, fix trial length at 1400 ms.
* Covers S-0057-01, S-0057-02, S-0057-04, **and** S-0055-01.

## Discussion — Round 2: Suggestion Cleanup

AI proposed:

### Reject (7)

| ID | Title | Reason |
| --- | --- | --- |
| S-0055-01 | Project-wide DSGC measurement-protocol fix | Covered by t0058 (bundled). |
| S-0057-01 | Sub-0.25 nS tonic GABA finer sweep on t0057 | Covered by t0058 (GABA grid 0.1, 0.2 nS). |
| S-0057-02 | AMPA conductance escape sweep on t0057 | Covered by t0058 (AMPA grid axis). |
| S-0057-04 | Per-synapse stimulus-window-tied tonic GABA on t0057 | Covered by t0058 (bar-arrival mechanism). |
| S-0011-01 | Record per-trial soma spike times from `modeldb_189347_dsgc` | Deposited line retired; PSTH already exercised on from-scratch wave. |
| S-0012-01 | Add `verify_library_asset.py` framework verificator | Already exists and in active use. |
| S-0012-03 | Integrate `tuning_curve_loss` into t0008 Poleg-Polsky reproduction | Deposited line retired; already integrated via metrics.json RMSE on from-scratch. |

### Reprioritise high → medium (presented as 17, actual count 18)

* Deposited-DSGC and deRosenroll lineage: S-0003-02, S-0008-01, S-0010-02, S-0010-05, S-0024-01,
  S-0027-02, S-0046-02, S-0020-01, S-0020-02.
* Morphology and active-channel calibration: S-0009-01, S-0009-02, S-0009-03.
* Channel/tooling infrastructure: S-0007-01, S-0013-01, S-0013-02.
* From-scratch comparisons: S-0052-04, S-0053-02, S-0053-03.

(AI miscounted the reprioritisation list as 17 in the summary text — actual count is 18; this was
identified during correction authoring and noted in `results_detailed.md`.)

### Keep at high priority (8)

S-0002-01, S-0002-04, S-0052-01, S-0052-02, S-0054-02, S-0055-02, S-0055-03, S-0057-06.

**Researcher**: "OK with the proposed. Create task and execute as discussed"

## Discussion — Round 3: Confirmation

AI summarised all decisions:

* New tasks: t0058_brainstorm_results_11 (this brainstorm), t0059
  (`bar_locked_gaba_ampa_sweep_t0057`, covering 4 suggestions).
* Suggestions rejected (7): S-0011-01, S-0012-01, S-0012-03, S-0055-01, S-0057-01, S-0057-02,
  S-0057-04.
* Suggestions reprioritised high → medium (18, summary text said 17): listed above.
* Tasks cancelled / updated: none.

Researcher's "OK with the proposed. Create task and execute as discussed" message in Round 2 is
interpreted as the explicit confirmation. Per skill guidance, no second authorization required
between Phase 5 and Phase 6.

## Decisions Summary

1. Create t0059 (`bar_locked_gaba_ampa_sweep_t0057`) — combined bar-arrival-locked GABA + AMPA
   escape sweep + bundled measurement-protocol fix; 5x5 grid; ~8.75 h on local CPU; covers
   S-0057-01, S-0057-02, S-0057-04, S-0055-01.
2. Reject S-0011-01, S-0012-01, S-0012-03, S-0055-01, S-0057-01, S-0057-02, S-0057-04.
3. Reprioritise high → medium: S-0003-02, S-0007-01, S-0008-01, S-0009-01, S-0009-02, S-0009-03,
   S-0010-02, S-0010-05, S-0013-01, S-0013-02, S-0020-01, S-0020-02, S-0024-01, S-0027-02,
   S-0046-02, S-0052-04, S-0053-02, S-0053-03.
4. Keep at high priority: S-0002-01, S-0002-04, S-0052-01, S-0052-02, S-0054-02, S-0055-02,
   S-0055-03, S-0057-06.
5. No tasks cancelled or updated.
6. No new suggestions proposed.
