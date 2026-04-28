# Results Summary: Brainstorm Session 10

## Summary

Tenth strategic brainstorm, run on 2026-04-28 after the from-scratch minimal DSGC wave (t0052,
t0053, t0054) completed and t0055 (Mg-block NMDA recovery test) started. Triggered by a researcher
observation that t0053's GABA conductance is only present in a narrow ~100-200 ms window per trial
because each spatial-gating GABA synapse fires exactly once at the bar-arrival time and the Exp2Syn
decay is only `tau2 = 20 ms`. Decision: commission a single new task (t0057) that replaces the
per-event Exp2Syn GABA mechanism with a tonic conductance gated by stimulus window and sweeps the
per-synapse peak conductance to recover non-zero FULL-mode tuning curves; reject four covered
high-priority suggestions; reprioritise nineteen high-priority suggestions to medium where the
brainstorm-9 pivot or recent results have de-urgented them.

## Session Overview

Date: 2026-04-28. Triggered by the researcher reading t0053's traces and noticing that GABA
inhibition collapses ~200 ms into the trial, leaving the cell uninhibited for the remaining ~1100
ms. The session opened with an independent priority reassessment of the 50 high-priority active
suggestions in light of the t0052-t0054 findings (t0052's perfect-but-trivial single-spike DSI;
t0053's degenerate flat-zero FULL tuning under 100 nS mean GABA; t0054's NMDA-driven peak-rate
recovery but DSI collapse under voltage-independent NMDA). The researcher then specified the new
task design directly during Round 1 (Option C: tonic conductance gated by stimulus window, applied
only to t0053; let t0055 complete on the existing GABA timing). Round 2 confirmed four rejections
and nineteen reprioritisations. Round 3 received explicit "approved" go-ahead.

## Decisions

1. **Create t0057** (`tonic_gaba_sweep_t0053`). Replace t0053's per-event Exp2Syn GABA mechanism
   with a new `gaba_tonic.mod` point process exposing `(g, e, t_on, t_off)` — sustained
   conductance `g` between `t_on` and `t_off`, zero elsewhere; reversal `e = -75 mV`. Default
   window: `t_on = 100 ms`, `t_off = 1400 ms`. Preserve t0053's spatial centripetal-gating rule
   (`cos(theta_stim - theta_centrifugal_synapse) < 0` selects active synapses); each gated synapse
   gets `g = GABA_BASE_NS`, silent synapses get `g = 0`. Same morphology, same E synapses, same
   placement seed as t0053 — only the GABA mechanism changes. Sweep
   `GABA_BASE_NS in {0.25, 0.5, 1.0, 1.5, 2.0}` nS — five conductance values. 12 directions x 10
   trials x 3 modes (FULL / AMPA_ONLY / GABA_ONLY) x 5 conductances = 1800 trials, ~25-30 min
   wall-clock on local CPU. Source suggestion: S-0053-01 (covered).

2. **Reject S-0015-04** ("build minimal DSGC implementing 6-point spec") — covered by t0052.

3. **Reject S-0016-03** ("test NMDA-spike contribution to DSGC DS") — covered by t0054 + t0055.

4. **Reject S-0017-03** ("implement AIS, NMDARs, voltage-clamp block in DSGC model") — AIS+NMDA
   done in t0052/t0054, voltage-clamp block in t0049.

5. **Reject S-0018-03** ("AMPA + NMDA + GABA_A with E-I temporal co-tuning + asymmetric inhibition")
   — main parts done in t0053 + t0054; the temporal co-tuning piece belongs in a future fresh
   suggestion.

6. **Reprioritise nineteen suggestions from high to medium**:

   * t0022 testbed lineage (de-emphasised by brainstorm 9): S-0022-01, S-0022-02, S-0022-03.
   * t0024 testbed follow-ups: S-0026-02, S-0026-06, S-0034-01, S-0034-02, S-0034-07, S-0035-02,
     S-0039-01.
   * t0033 optimiser prerequisites (deferred until from-scratch substrate is mature): S-0033-02,
     S-0033-03, S-0033-06.
   * Sheffield paywalled-paper retrievals (already bundled into not-started t0031): S-0015-01,
     S-0016-01, S-0017-01, S-0018-01, S-0019-01.
   * Retired deposited-DSGC line: S-0048-01.

7. **Keep deferred** t0023 (Hanson 2019 port, intervention_blocked), t0031 (Sheffield paywalled
   papers, not_started), t0045 (CoreNEURON Vast.ai benchmark, not_started). None on the tonic-GABA
   wave's critical path.

8. **Keep at high priority** the from-scratch wave's natural next steps not covered by t0057:
   S-0052-01 (AMPA sweep on t0052), S-0052-02 (GABA-count sweep on t0052), S-0052-04 (t0052 vs t0053
   cross-comparison), S-0053-02 (stricter centripetal threshold sweep — alternative to t0057's
   amplitude path), S-0053-03 (conductance-matched t0052 vs t0053 at fixed mean GABA mass),
   S-0054-02 (joint conductance sweep on t0054 — wait for t0055 results), S-0002-01 (factorial
   g_Na x g_K — research Q1, untouched).

9. **Let t0055 complete on existing GABA timing**. Brainstorm decisions do not modify the t0055 task
   folder; t0055 will produce results under the per-event Exp2Syn GABA, and any retroactive re-run
   on the new tonic-GABA architecture is deferred to a future brainstorm informed by both t0055 and
   t0057 outputs.

## Metrics

| Metric | Value |
| --- | --- |
| New tasks created | 1 (t0057) |
| Tasks cancelled | 0 |
| Tasks updated (other than cancellations) | 0 |
| Suggestions rejected | 4 (S-0015-04, S-0016-03, S-0017-03, S-0018-03) |
| Suggestions reprioritised | 19 |
| Corrections written | 23 |
| New suggestions created | 0 |
| Session duration | ~60 minutes interactive |
| Session cost | $0.00 |

## Verification

* `verify_task_file.py t0056_brainstorm_results_10` — target 0 errors.
* `verify_corrections.py t0056_brainstorm_results_10` — target 0 errors across 23 correction
  files.
* `verify_suggestions.py t0056_brainstorm_results_10` — target 0 errors (empty array).
* `verify_logs.py t0056_brainstorm_results_10` — target 0 errors; LG-W005 / LG-W007 / LG-W008
  acceptable per skill guidance and step-4 capture.
* `verify_task_file.py` for t0057 — target 0 errors.
* `verify_pr_premerge.py t0056_brainstorm_results_10 --pr-number <N>` — target 0 errors.

## Next Steps

1. **Wave execution order**: t0057 is independent of t0055; the two can run concurrently in separate
   worktrees once t0055 hits its own implementation step. t0057 reuses t0053's cell builder,
   placement, and trial loop; only the GABA mechanism module changes.
2. **Cross-task comparison** between t0053 (per-event Exp2Syn GABA) and t0057 (tonic GABA at matched
   per-synapse amplitude) is implicit in t0057's reporting — the 1.0 nS sweep value matches
   t0053's amplitude and provides a direct head-to-head against t0053's degenerate flat-zero FULL
   result.
3. **Decision point after t0057** for whether to (a) propagate the tonic-GABA mechanism back to
   t0052 (scalar `gabaMOD`) and t0054 (AMPA + NMDA), or (b) move to other research questions (Q1
   g_Na/g_K factorial, Q4 active dendrites). To be commissioned by a future brainstorm.
4. **t0055 results** will inform whether S-0054-02 (joint conductance sweep on t0054) becomes active
   immediately or stays on the high-priority shelf pending the Mg-block outcome.
