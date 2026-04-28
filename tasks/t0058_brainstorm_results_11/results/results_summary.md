# Results Summary: Brainstorm Session 11

## Summary

Eleventh strategic brainstorm, run on 2026-04-29 after t0055 (Mg-block NMDA recovery test) and t0057
(tonic-GABA amplitude sweep on t0053 spatial substrate) completed. The session is triggered by the
convergent finding across the from-scratch minimal DSGC family (t0052/t0053/t0054/t0055/ t0057) that
every variant is locked in a binary regime — either single-spike-per-trial (peak Hz = 0.667, DSI =
1.0 trivially) or full inhibitory suppression (peak Hz = 0, DSI = 0). Decision: commission a single
combined task (t0059 — bar-arrival-locked tonic GABA + AMPA escape sweep + bundled
measurement-protocol fix) covering S-0057-01, S-0057-02, S-0057-04, and S-0055-01 in one
experimental run; reject seven covered or superseded high-priority suggestions; reprioritise
eighteen high-priority suggestions to medium where the brainstorm-9 from-scratch pivot or recent
results have de-urgented them.

## Session Overview

Date: 2026-04-29. Triggered by the convergent binary-regime finding across t0052-t0057. The session
opened with an independent priority reassessment of the 32 high-priority active suggestions in light
of the new t0055 / t0057 evidence (Mg-block NMDA recovers DSI but peak Hz stays at 0.667 under
scalar gabaMOD; tonic-GABA at any swept conductance produces either single-spike or full
suppression, never an intermediate operating point). The researcher steered Round 1 by combining
S-0057-01 (sub-veto GABA), S-0057-02 (AMPA escape), and S-0057-04 (bar-arrival-locked windows) into
a single task. The AI proposed bundling the S-0055-01 measurement-protocol fix into the same task;
the researcher chose Option (b) — bundle into t0059 — and adjusted (window_ms fixed at 200 ms,
no sweep; AMPA top trimmed from 5.0 to 4.0 nS). Round 2 received "OK with the proposed" approval on
seven rejections + eighteen reprioritisations. Round 3 received explicit "Create task and execute as
discussed" go-ahead.

## Decisions

1. **Create t0059** (`bar_locked_gaba_ampa_sweep_t0057`). Forks t0057's
   `minimal_dsgc_tonic_gaba_sweep` library and (a) replaces the global `(t_on, t_off) = (100, 1400)`
   ms tonic GABA window with a per-synapse bar-arrival-locked window (each centripetally-active I
   synapse gets `t_on_i = (x_i cos(theta) + y_i sin(theta)) / v + 100 ms`,
   `t_off_i = t_on_i + 200 ms`), (b) bundles the project-wide measurement-protocol fix (drop legacy
   `E_ONLY` / `GABA_ONLY` modes, add `EPSP_PASSIVE` / `IPSP_PASSIVE` modes that save-and-zero
   `gnabar_hh` / `gkbar_hh` on `soma` + AIS so synaptic envelopes are spike-free; drop the
   per-synapse activation-time histogram; standardise trial length at 1400 ms), and (c) sweeps a 5x5
   (gAMPA, GABA_BASE_NS) grid: `gAMPA in {0.5, 1.0, 2.0, 3.0, 4.0}` nS x
   `GABA_BASE_NS in {0.1, 0.2, 0.5, 1.0, 2.0}` nS. 25 grid cells x 12 directions x 10 trials x 3
   modes = 9000 trials, ~8.75 h wall-clock on local CPU. Source suggestions: S-0057-04 (primary),
   S-0057-02, S-0057-01, S-0055-01 (all four covered).

2. **Reject S-0011-01** ("record per-trial soma spike times from `modeldb_189347_dsgc` to exercise
   `plot_angle_raster_psth`") — deposited-DSGC line retired in brainstorm 9; PSTH library has been
   exercised on the from-scratch wave's real spike data.

3. **Reject S-0012-01** ("add a `verify_library_asset.py` framework verificator") — already exists
   and is in active use as a hard-fail pass gate across t0052/t0053/t0054/t0057 library assets.

4. **Reject S-0012-03** ("integrate `tuning_curve_loss` into the t0008 Poleg-Polsky DSGC
   reproduction") — deposited-DSGC line retired; loss is integrated into the from-scratch lineage
   instead via `metrics.json` RMSE entries.

5. **Reject S-0055-01** (project-wide DSGC measurement-protocol fix) — bundled into t0059 per
   researcher decision.

6. **Reject S-0057-01** (sub-0.25 nS finer GABA sweep on t0057) — covered by t0059's GABA grid
   (includes 0.1 / 0.2 nS).

7. **Reject S-0057-02** (AMPA conductance escape sweep on t0057) — covered by t0059's AMPA grid
   axis (top trimmed from 5.0 to 4.0 nS by researcher decision).

8. **Reject S-0057-04** (per-synapse stimulus-window-tied tonic GABA on t0057) — covered by
   t0059's bar-arrival-locked window mechanism (window_ms fixed at 200 ms by researcher decision
   rather than swept across {50, 100, 200, 400} ms).

9. **Reprioritise eighteen suggestions from high to medium**:

   * Deposited-DSGC and deRosenroll port lineage (retired by brainstorm 9): S-0003-02, S-0008-01,
     S-0010-02, S-0010-05, S-0024-01, S-0027-02, S-0046-02, S-0020-01, S-0020-02.
   * Morphology and active-channel calibration (deferred to RQ2 / RQ4 follow-ups once a working
     multi-spike substrate exists): S-0009-01, S-0009-02, S-0009-03.
   * Channel and tooling infrastructure (no longer top-of-queue): S-0007-01, S-0013-01, S-0013-02.
   * From-scratch comparisons (defer until working spatial operating point exists): S-0052-04,
     S-0053-02, S-0053-03.

10. **Keep at high priority** the suggestions still on the active critical path:

    * S-0002-01 (factorial g_Na x g_K — RQ1 untouched).
    * S-0002-04 (factorial morphology sweep — RQ2).
    * S-0052-01 (AMPA escape sweep on t0052 substrate).
    * S-0052-02 (GABA-synapse-count sweep on t0052 — driving-force saturation curve).
    * S-0054-02 (joint gAMPA, gNMDA, gGABA sweep on t0054).
    * S-0055-02 (re-run t0055 Mg-block sweep on corrected protocol).
    * S-0055-03 (GABA-reduction ladder on t0055 Mg-block architecture).
    * S-0057-06 (tonic GABA + Mg-block NMDA combination — natural follow-up to t0059).

11. **Keep deferred** t0023 (Hanson 2019 port, intervention_blocked), t0031 (Sheffield paywalled
    papers, not_started), t0045 (CoreNEURON Vast.ai benchmark, not_started). None on t0059's
    critical path.

## Metrics

| Metric | Value |
| --- | --- |
| New tasks created | 1 (t0059) |
| Tasks cancelled | 0 |
| Tasks updated (other than cancellations) | 0 |
| Suggestions rejected | 7 (S-0011-01, S-0012-01, S-0012-03, S-0055-01, S-0057-01, S-0057-02, S-0057-04) |
| Suggestions reprioritised | 18 |
| Corrections written | 25 |
| New suggestions created | 0 |
| Session duration | ~120 minutes interactive |
| Session cost | $0.00 |

## Verification

* `verify_task_file.py t0058_brainstorm_results_11` — target 0 errors.
* `verify_corrections.py t0058_brainstorm_results_11` — target 0 errors across 25 correction
  files.
* `verify_suggestions.py t0058_brainstorm_results_11` — target 0 errors (empty array).
* `verify_logs.py t0058_brainstorm_results_11` — target 0 errors; LG-W005 / LG-W007 / LG-W008
  acceptable per skill guidance and step-4 capture.
* `verify_task_file.py` for t0059 — target 0 errors.
* `verify_pr_premerge.py t0058_brainstorm_results_11 --pr-number <N>` — target 0 errors.

## Next Steps

1. **t0059 execution**: independent of any in-flight task; can be commissioned to `/execute-task`
   immediately. ~8.75 h wall-clock on local CPU; can run overnight.

2. **Decision point after t0059**:

   * If a multi-spike DSI > 0.3 operating point is found on the swept grid: propagate the bar-
     locked GABA mechanism back to t0054 (AMPA + Mg-block NMDA) via S-0057-06 to test whether the
     NMDA multiplicative-gain rescue holds under biologically realistic GABA timing.
   * If no operating point is found in the swept range: characterise the failure mode (fully
     suppressed even at 0.1 nS GABA at high gAMPA, or single-spike at low gAMPA across the GABA
     range), then either extend the AMPA range above 4.0 nS or pivot to RQ1 (factorial g_Na x g_K
     via S-0002-01) and RQ4 (active dendrites) to test whether somatic / dendritic voltage-gated
     channels — not just synaptic conductance — are required to escape the binary regime.

3. **Mg-block NMDA + bar-locked GABA combination (S-0057-06)** stays at high priority and is the
   natural follow-up to t0059 regardless of outcome.

4. **t0055 re-run on corrected protocol (S-0055-02)** stays at high priority; useful to validate the
   t0055 DSI = 0.7464 headline against spike-free EPSP / IPSP traces. Can be done on t0059's
   corrected library after t0059 completes.
