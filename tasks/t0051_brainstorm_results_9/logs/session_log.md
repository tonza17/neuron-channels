# Brainstorm Session 9 — Full Transcript

Date: 2026-04-25

## Project State Presented

50 tasks total: 44 completed, 4 `intervention_blocked` (t0023 Hanson port, t0042/t0043/t0044
t0022-substrate work), 2 `not_started` (t0031 paywalled morphology papers, t0045 CoreNEURON
benchmark). Budget: $0.00 / $1.00 used. 171 active uncovered suggestions; 49 high-priority.

Last brainstorm: t0040 session 8 on 2026-04-24. Six tasks completed since: t0041, t0046, t0047,
t0048, t0049, t0050.

### Headline findings since session 8

The reproduction wave (t0046–t0050) produced a coherent and significant negative result:
- **t0046** rebuilt 189347 from scratch, matched slope-angle and ROC-AUC targets, but PD PSP at
  b2gnmda=0.5 nS is 23.25 mV vs paper 5.8 +/- 3.1 mV (4x over). 12 paper-vs-code discrepancies
  catalogued.
- **t0047** confirmed deposited code does not reproduce paper Fig 3A-E: per-synapse-class summed
  conductances 6-9x over paper; DSI vs gNMDA peaks at 0.19 not paper's flat 0.30.
- **t0048** Voff=1 partially flattens DSI vs gNMDA but range 0.066, slope -0.024/nS still non-flat;
  absolute DSI 0.04-0.10, never reaches paper 0.30.
- **t0049** SEClamp re-measurement: GABA PD/ND under SEClamp is 0.99 (symmetric) vs paper 0.42
  (asymmetric). Modality cannot reconcile code with paper.
- **t0050** spatial audit: deposited code uses non-spatial scalar gabaMOD applied uniformly to
  spatially-symmetric synapses; mechanically incapable of producing paper Fig 3 GABA PD/ND
  asymmetry.

t0041 rejected the Rall electrotonic-length collapse hypothesis (Pearson r +0.42 / -0.68, both below
0.9 threshold).

### Reassessed priorities for top recent suggestions

| ID | Original | Reassessed | Rationale |
| --- | --- | --- | --- |
| S-0050-01 | high | critical | Re-implement placeBIP() spatial gating — single concrete patch aligning code with paper Fig 3 mechanism. |
| S-0050-02 | high | critical | Re-distribute SACinhib asymmetrically — companion to S-0050-01. |
| S-0046-02 | high | high | Root-cause 282 vs 177 synapse count. |
| S-0048-02 | high | medium | Premature; t0048 verdict was H2, not H1. |
| S-0049-02 | high | medium | Useful but only after S-0050-01/02 fix the mechanism. |
| S-0046-01 | high | low | Statistical refinement, not mechanism. |
| S-0046-03 | high | medium | iMK801 analogue, independent of Fig 3 gap. |
| S-0046-04 | medium | decide now | Fate of t0042/t0043/t0044 — should be a brainstorm decision. |

## Clarification Questions

AI: Do you have any notes, ideas, or context that should guide this session? And five specific
questions to set direction:

1. Headline strategic question: do you want the next wave to (a) fix the deposited code, (b)
   continue on t0022/t0024 substrates, or (c) some mix?
2. Fate of t0042/t0043/t0044?
3. Compute envelope — local CPU only or ready for t0045?
4. t0023 Hanson 2019 — unblock, cancel, or keep deferred?
5. Wave size — 1-3 tasks or 5-8?

Researcher (paraphrased): "I want you to generate another model from scratch. Take any morphology
from our repository and add 100 excitatory and 100 inhibitory synapses. Then excitation should be
direction independent (and waveform - classical EPSP) but should also depend on the position of the
stimulus. Synapse should only respond when stimulus covers the synapse. Stimulus is a moving bar.
Inhibition is direction dependent as in deRosenroll part. And standard Hodgkin Huxley excitability.
Report data as voltages EPSP, IPSP and firing rate as a function of time and for each different
direction. Position of the synapses, and other general parameters take from other models. Ask me
questions if needed."

## Discussion — Round 1: New Tasks

AI proposed default model spec: morphology `dsgc-baseline-morphology-calibrated`, 100 E + 100 I
co-located synapses with light distal bias, AMPA-only Exp2Syn (rise 0.5, decay 2.5 ms, 0.5 nS),
position-gated single-event firing per synapse, GABA_A Exp2Syn (rise 1, decay 20 ms, 2 nS) with
scalar gabaMOD scaling, soma+AIS standard HH, 12 dirs x 10 trials, bar 200 um at 1000 um/s, V_rest
-65 mV. Proposed five outputs (soma V, EPSP, IPSP, PSTH, polar tuning, synapse-activation
histogram). Asked five questions:

1. Morphology — `dsgc-baseline-morphology-calibrated` or t0024's de Rosenroll morphology?
2. deRosenroll inhibition mechanism — scalar gabaMOD or true spatial PD/ND asymmetry?
3. E/I pairing — co-located or independent uniform?
4. HH coverage — soma+AIS only or throughout dendrites?
5. NMDA at all — confirming AMPA-only.

Researcher: "1 former. Yes, for now let's do both in two separate tasks. 3. Collocated. 4. Some plus
ais. 5. No nmda."

AI confirmed two-task split (Task A scalar gabaMOD, Task B spatial PD/ND-asymmetric) and asked two
follow-up questions:

1. Spatial-asymmetry threshold for Task B — `cos(theta_stim - theta_centrifugal) < 0`?
2. Synapse spatial bias — uniform random no bias or biased toward distal?

Researcher: "I meant 2. Implement both solutions in two separate tasks."

AI committed to defaults (threshold = `cos < 0`; uniform random synapse distribution) and presented
the final scope table for both tasks.

## Discussion — Round 2: Suggestion Cleanup

AI proposed:
- **Cancel** t0042, t0043, t0044 (all `intervention_blocked` on the obsolete t0022 testbed; the new
  minimal model supersedes them).
- **Keep as-is** t0023, t0031, t0045 — deferred but no critical-path conflict.
- **Reprioritise** S-0046-01, S-0046-03, S-0048-02, S-0049-02, S-0050-01, S-0050-02 from high to
  medium (superseded by from-scratch tasks).
- **Leave** the 43 other high-priority suggestions untouched.

## Discussion — Round 3: Confirmation

AI: Final confirm-or-push-back on three line items:

1. Two new tasks (Task A scalar + Task B spatial) as scoped.
2. Cancel t0042 / t0043 / t0044.
3. Reprioritize the 6 listed t0046–t0050 follow-up suggestions to medium.

Researcher: "Round 1 q1. Ok, happy with default option. Q2 uniform. Round two — confirm. Round 3.
1\. Yes 2. Yes 3. Yes"

## Decisions Summary

1. Create t0052 (`minimal_dsgc_scalar_gaba`) — from-scratch minimal DSGC with scalar
   gabaMOD-scaled inhibition.
2. Create t0053 (`minimal_dsgc_spatial_gaba`) — from-scratch minimal DSGC with spatial
   PD/ND-asymmetric (centripetal-only) inhibition.
3. Cancel t0042 (fine null-GABA ladder).
4. Cancel t0043 (Nav1.6 + Kv3 + NMDA restoration).
5. Cancel t0044 (Schachter retest on t0043).
6. Reprioritise S-0046-01 high to medium.
7. Reprioritise S-0046-03 high to medium.
8. Reprioritise S-0048-02 high to medium.
9. Reprioritise S-0049-02 high to medium.
10. Reprioritise S-0050-01 high to medium.
11. Reprioritise S-0050-02 high to medium.
12. Keep deferred t0023, t0031, t0045 unchanged.

The Phase 2 Round 3 confirmation authorises the entire remaining lifecycle (Phase 5 apply decisions,
Phase 6 record / verify / push / PR / merge) without further confirmation gates.
