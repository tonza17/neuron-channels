# Brainstorm Session 24 - Full Transcript (structured summary)

## Project State Presented

130 tasks: 121 completed, 1 in progress (t0128), 2 not started (t0031, t0075), 1 intervention
blocked (t0023), 5 cancelled. Budget $67.16 of $100 spent; $12.84 before the 80% warning. 412
uncovered suggestions (35 high, 316 medium, 61 low).

Key findings since brainstorm 23: t0120 geometry audit passed 60/60 checks (rendering-only
artefact); t0121 5-seed substrate rate 2.58% mean (bootstrap CI +0.38% to +5.53%); t0122 Cuntz
prediction confirmed with 10/10 cells at bf = 0.500 (possible degeneracy); t0123 Strong-Bialek
bits/s = 0 for all top cells; t0126 DSI 1.0 at 7.82e6 ATP/spike with n = 6 front (insufficient
evidence); t0127 found the t0126 cell_trace was synthesised; t0129 signed DSI on seed 3517 gave a
9-cell front and 95 of 5,496 viable cells (1.7%) with negative signed DSI.

Independent priority reassessment: raise S-0129-09, S-0129-10, S-0129-03/05/06, S-0122-02,
S-0118-03; stale or done: S-0113-01, S-0114-02, S-0116-06; downgrade S-0124-02.

## Clarification Questions

AI: Asked for notes, whether t0128 should continue or be replaced by a signed-DSI multi-seed task,
whether to adopt signed DSI project-wide, budget for the next wave, and focus area.

Researcher: Did not answer these; instead asked for simple modelling of an experimental finding:
blind-mouse FVB/N rd1 RGCs vs sighted controls, with smaller Na and larger K currents, smaller
evoked spiking, and what this does to direction selectivity.

## Discussion - Round 1: New Tasks

AI: Proposed a task applying Na/K scaling at soma and AIS on reference cells, with a current-clamp
phase and a direction-selectivity phase, and asked five questions (data targets, meaning of
"sustained firing", spontaneous activity, where to apply the change, bundling).

Researcher: Targets are in SomeResults.pdf (figures A to C). Spontaneous activity: whatever works,
exploratory. Soma and AIS is fine, add dendrites if it does not work. Standalone.

AI: Read the figures: WT silent vs rd1 ~7 Hz spontaneous; +60 pA gives ~4 spikes in WT and almost
none in rd1; sustained outward current ~2 nA vs ~3.5 nA. Reinterpreted the phenotype as hyperactive
at rest but poorly responsive to drive. Revised the design to calibrate on voltage clamp, then test
current clamp out of sample, then measure signed DSI, and offered to test panel D's saturation
prediction.

Researcher: Do parts 1-3. Panel D is a prediction by a much simpler model that should also be
reproduced or disproved. Loose ends (suggestion cleanup) next time.

## Discussion - Round 2: Suggestion Cleanup

AI: Proposed rejecting S-0113-01, S-0114-02, S-0116-06; downgrading S-0124-02; raising S-0129-03,
-05, -06 and S-0122-02; leaving t0128 untouched.

Researcher: Deferred all of it to the next session.

## Discussion - Round 3: Confirmation

AI: Summarised: create one rd1 task with four parts, write no corrections.

Researcher: Confirmed ("do 1-3", plus panel D, loose ends next time).

## Decisions Summary

1. Create `t0131_rd1_na_k_remodelling_dsgc_dsi` (voltage-clamp calibration, current-clamp
   prediction, signed-DSI protocol, panel D reproduce-or-refute); standalone, local, $0.
2. Soma and AIS scaling first; dendritic scaling arm as fallback.
3. Spontaneous activity via exploratory tonic bias or noise.
4. Suggestion cleanup deferred to brainstorm 25; no corrections written.
5. t0128 untouched.
