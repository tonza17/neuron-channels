# Results Summary: Brainstorm Session 9

## Summary

Ninth strategic brainstorm, run on 2026-04-25 after the t0046–t0050 reproduction wave. Produced a
strategic pivot: step away from modifying the deposited Poleg-Polsky 2016 ModelDB 189347 code and
from the t0022 channel-testbed lineage; build a from-scratch minimal DSGC on the project's
calibrated baseline morphology with two parallel inhibition mechanisms (scalar `gabaMOD` and spatial
PD/ND-asymmetric); cancel three obsolete `intervention_blocked` tasks; reprioritise six follow-up
suggestions whose urgency the new substrate dissolves.

## Session Overview

Date: 2026-04-25. Triggered by the researcher reading the t0046–t0050 reproduction wave findings
(deposited code mismatches paper Fig 3A-E in synapse count, conductances, and mechanism; spatial
GABA asymmetry mechanically impossible in the deposited synapse layout). The session opened with an
independent priority reassessment of the 49 high-priority active suggestions, focusing on those
superseded by the new substrate. The researcher specified the new model design directly during Round
1 (100 E + 100 I co-located synapses, position-gated AMPA-only EPSPs, classical IPSPs, soma+AIS HH
on `dsgc-baseline-morphology-calibrated`) and asked for the deRosenroll-style direction- dependent
inhibition to be implemented in two separate tasks. Round 2 confirmed cancellation of
t0042/t0043/t0044 and reprioritisation of six t0046–t0050 follow-up suggestions. Round 3 received
explicit go-ahead.

## Decisions

1. **Create t0052** (`minimal_dsgc_scalar_gaba`). From-scratch minimal DSGC on
   `dsgc-baseline-morphology-calibrated` with 100 E + 100 I co-located synapses, position-gated
   AMPA-only excitation (Exp2Syn, rise 0.5 ms, decay 2.5 ms, peak 0.5 nS), scalar gabaMOD-scaled
   inhibition (Exp2Syn, rise 1 ms, decay 20 ms, peak 2 nS, scaling 0.33–1.0 across directions),
   soma + AIS NEURON `hh` standard, passive dendrites, V_rest -65 mV. Local CPU, ~1 week wall-clock,
   $0 budget.

2. **Create t0053** (`minimal_dsgc_spatial_gaba`). Identical model to t0052 except the inhibition
   mechanism: each I synapse fires only when `cos(theta_stim - theta_centrifugal_synapse) < 0`
   (centripetal-only firing). Same morphology, same E synapses, same fixed placement seed so the two
   tasks can be compared trial-for-trial in a downstream analysis. Local CPU, ~1 week, $0.

3. **Cancel t0042** (fine null-GABA ladder on t0022). All `intervention_blocked` t0022 substrate
   tasks become obsolete now that the from-scratch wave supersedes the t0022 testbed.

4. **Cancel t0043** (Nav1.6 + Kv3 + NMDA restoration on t0022). Same reason.

5. **Cancel t0044** (Schachter retest on t0043). Same reason; depended on t0043 anyway.

6. **Reprioritise S-0046-01** (re-run t0046 figure sweeps at paper-N) from high to medium —
   superseded by the from-scratch wave; statistical-power refinement of the deposited code
   reproduction is no longer urgent.

7. **Reprioritise S-0046-03** (iMK801-analogue MOD modification for Fig 8 AP5 reproduction) from
   high to medium — the new wave excludes NMDA entirely, so dendritic-NMDAR-block tooling is no
   longer critical-path.

8. **Reprioritise S-0048-02** (adopt exptype=2 voltage-independent NMDA as canonical) from high to
   medium — the new wave abandons NMDA entirely.

9. **Reprioritise S-0049-02** (GABA scan under SEClamp toward paper PD/ND values) from high to
   medium — deposited-code calibration is no longer urgent.

10. **Reprioritise S-0050-01** (re-implement placeBIP with spatial gating) from high to medium —
    t0053 implements the equivalent mechanism natively from scratch.

11. **Reprioritise S-0050-02** (re-distribute SACinhib synapses asymmetrically) from high to medium
    — same reason as S-0050-01.

12. **Keep deferred** t0023 (Hanson 2019 port), t0031 (Sheffield paywalled papers), t0045
    (CoreNEURON Vast.ai benchmark). None on the from-scratch wave's critical path.

## Metrics

| Metric | Value |
| --- | --- |
| New tasks created | 2 (t0052, t0053) |
| Tasks cancelled | 3 (t0042, t0043, t0044) |
| Suggestions reprioritised | 6 (S-0046-01, S-0046-03, S-0048-02, S-0049-02, S-0050-01, S-0050-02) |
| Suggestions rejected | 0 |
| Tasks updated (other than cancellations) | 0 |
| Corrections written | 6 |
| Session duration | ~30 minutes interactive |
| Session cost | $0.00 |

## Verification

* `verify_task_file.py t0051_brainstorm_results_9` — target 0 errors.
* `verify_corrections.py t0051_brainstorm_results_9` — target 0 errors across 6 correction files.
* `verify_suggestions.py t0051_brainstorm_results_9` — target 0 errors (empty array).
* `verify_logs.py t0051_brainstorm_results_9` — target 0 errors; LG-W005 / LG-W007 / LG-W008
  acceptable per skill guidance and step-4 capture.
* `verify_task_file.py` for t0052 and t0053 — target 0 errors each.
* `verify_pr_premerge.py t0051_brainstorm_results_9 --pr-number <N>` — target 0 errors.

## Next Steps

1. **Wave execution order**: t0052 and t0053 are independent and can run in parallel worktrees.
   Recommend sequencing t0052 first to validate the position-gating infrastructure under the simpler
   scalar-gabaMOD policy, then t0053 reusing the cell builder and placement code with the
   centripetal-gating inhibition driver swapped in.
2. **Cross-task comparison** is deferred to a downstream task (to be commissioned by a future
   brainstorm) that takes the t0052 + t0053 outputs and produces a head-to-head tuning-curve, DSI,
   and PSTH comparison.
3. **t0033 optimiser** stays deferred until a working from-scratch substrate is in hand. Re-evaluate
   t0033's relevance after t0052 and t0053 deliver baseline DSI numbers.
