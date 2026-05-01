# Results Summary: Brainstorm Session 12

## Summary

Twelfth strategic brainstorm, run on 2026-05-01 after t0070 (two-bed writeup), t0071 (typeset PDF +
synaptic-current equations), and t0072 (synaptic conductance / current traces for PD and ND on both
beds) all completed. The session is triggered by two convergent gaps in the t0067-t0069
voltage-gated-channel arc on Bed A: the unmeasured tuning-width effect of channel addition (t0067
measured DSI at PD and ND only), and the absence of any DSGC + AIS configuration that simultaneously
contains all biologically-present AIS channels and produces non-trivial DSI at a biologically
reasonable peak rate. Decision: commission two new tasks (t0074 `channel_tuning_width_bed_a` —
12-angle bar-rotation tuning curves on Bed A with 8-channel set including newly vendored BK / SK /
Kv7; t0075 `bio_realistic_ais_param_sweep` — biologically-realistic AIS one-axis-at-a-time
parameter sweep on Bed A with channel set {HHst, Nav1.6, Kv3, Kv7}); reject nine covered or
duplicate suggestions; reprioritise three high-priority suggestions to medium where the t0065 /
t0066 shunting-inhibition discovery has changed the strategic frame.

## Session Overview

Date: 2026-05-01. Triggered by the convergent t0067-t0069 channel-arc findings: NaP_high inverts DSI
(sign flip), Nav1.6_high erodes DSI from 0.80 to 0.23, NaR / Kv3 / Kv4 nearly inert, Kv3 + Nav1.6
co-expression rescue falsified, AIS+axon adds an electrical sink that quenches the cell rather than
relocating spike initiation. The session opened with an independent priority reassessment of the 20
high-priority active uncovered suggestions in light of the new t0065 / t0066 shunting-inhibition
discovery (cross-bed convergence on `e_GABA = v_rest = -60 mV`) and the t0067 channel-arc outcomes.
The researcher steered Round 1 by stating two specific things to figure out: (1) whether channels
affect direction-tuning *width* (broaden vs sharpen vs flatten); (2) finding parameters for a DSGC
with a biologically-realistic AIS that retains decent DSI and reasonable firing rate. AI proposed
t0074 with the t0067 channel set; researcher chose to add BK / SK / Kv7 to the channel set ("time is
no issue"). AI proposed t0075 with AIS channel set {HHst, Nav1.6, Kv3, Kv7}; researcher confirmed
the channel set, the Task-1-first dependency, and chose not to add anything else. Round 2 received
"all sounds good" approval on nine rejections plus three reprioritisations. Round 3 received
explicit "go" go-ahead authorising the entire remaining lifecycle through PR merge. A parallel
session merged `t0072_synaptic_traces_pd_nd` to main during the brainstorm; the brainstorm-results
task and child tasks were renumbered from t0072 / t0073 / t0074 to t0073 / t0074 / t0075 to preserve
the Phase 3 step 19 ordering invariant.

## Decisions

1. **Create t0074** (`channel_tuning_width_bed_a`). Forks t0067's somatic channel-addition layer on
   Bed A and runs a 12-angle bar-rotation tuning-curve protocol per condition. Channel set: 5
   already-vendored {Nav1.6, NaP, NaR, Kv3, Kv4} plus 3 newly vendored {BK, SK, Kv7} at low / medium
   / high densities each, plus 1 baseline = 25 conditions. 25 x 12 angles x 5 seeds = 1500 FULL
   trials; 25 x 12 x 1 x 2 passive modes = 600 EPSP_PASSIVE / IPSP_PASSIVE trials; total 2100
   trials, ~2.2 h wall-clock. Vendoring overhead ~3-4 h coding (BK, SK, Kv7 MODs + calcium-pool
   mechanism + un-zero CaL / CaT in `init_active` with regression gate against t0067's DSI = 0.797
   baseline). Width metrics: HWHM (deg), vector-sum DSI, peak rate, RMSE vs t0004 cosine target.
   Source suggestion: S-0068-01 (declared primary; S-0068-02 and S-0068-05 also covered).

2. **Create t0075** (`bio_realistic_ais_param_sweep`). Forks t0069's AIS-attachment code on Bed A.
   AIS channel set: {HHst, Nav1.6, Kv3, Kv7}. Two-stage design: Stage 1 calibrates a working
   baseline by sweeping soma_gnabar across {100, 150, 200, 250, 300, 400} mS / cm^2 at the
   literature-informed AIS configuration (diameter 0.8 micrometre, length 30 micrometre, axon 1.0
   mm) and selects the candidate that lands inside {peak Hz in [5, 50], DSI in [0.3, 0.95]}; Stage 2
   runs 8 one-at-a-time axes from that baseline (soma `gnabar_HHst`, AIS `gnabar_HHst`, AIS
   diameter, AIS length, AIS Nav1.6 density, AIS Kv3 density, AIS Kv7 density, axon length); 27
   conditions x 12 angles x 5 seeds = 1620 FULL trials, ~100 min wall-clock. Total compute ~2 h.
   Source suggestion: S-0069-01 (declared primary; S-0068-04, S-0069-02, S-0069-03, S-0069-04 also
   covered). Depends on t0074 for Kv7 vendoring.

3. **Reject S-0065-01** ("apply EPSP / IPSP / FULL protocol to from-scratch DSGC family") —
   duplicate of the more recent and more sharply framed S-0066-02; keep S-0066-02.

4. **Reject S-0068-01** ("BK / SK calcium-activated K+ co-expression with Nav1.6") — covered by
   t0074 (BK and SK are in the 8-channel set with vendored MODs and calcium pool).

5. **Reject S-0068-02** ("M-current Kv7 co-expression with Nav1.6") — covered by t0074 (Kv7 in the
   8-channel set; vendored MOD inherited by t0075).

6. **Reject S-0068-04** ("move Nav1.6 + Kv3 to a virtual AIS instead of soma") — covered by t0075
   (AIS baseline includes Nav1.6 medium + Kv3 medium, and Stage 2 axes 5+6 sweep both densities).

7. **Reject S-0068-05** ("sweep Kv3 alone to validate kinetic-model effect") — superseded by t0074
   (Kv3 at 3 densities x 12 angles is a stricter test than the 2-direction probe).

8. **Reject S-0069-01** ("halve somatic gnabar before AIS") — covered by t0075 Stage 1
   (soma_gnabar candidate sweep) and Stage 2 axis 1.

9. **Reject S-0069-02** ("shrink AIS diameter to 0.5 micrometre") — covered by t0075 Stage 2 axis
   3 ({0.4, 0.6, 0.8, 1.0, 1.5} micrometre).

10. **Reject S-0069-03** ("vary axon length to probe sink") — covered by t0075 Stage 2 axis 8
    ({0.1, 0.5, 1.0, 2.0} mm).

11. **Reject S-0069-04** ("Nav1.6 + Kv3 on AIS at biological densities") — covered by t0075
    baseline + Stage 2 axes 5 + 6.

12. **Reprioritise S-0002-01 high → medium** (factorial g_Na x g_K grid) —
    pre-shunting-discovery framing; t0067 demonstrated somatic VGC sweeps cannot rescue DSI in
    isolation.

13. **Reprioritise S-0002-04 high → medium** (factorial morphology sweep) — same reason;
    morphology is downstream of the e_GABA / shunting architectural choice.

14. **Reprioritise S-0070-02 high → medium** (unified model-bed-runner library) — pure
    infrastructure, not blocking any current experiment; cross-bed harmonisation (S-0070-01) is
    upstream in the dependency chain.

15. **Keep at high priority** the suggestions still on the active critical path: S-0052-01,
    S-0052-02, S-0054-02, S-0055-02, S-0055-03, S-0057-06, S-0059-01, S-0059-02, S-0059-03,
    S-0065-02 (the e_GABA = v_rest unlock candidate — flagged as the highest-leverage
    uncommissioned experiment in the project), S-0066-02 (kept; S-0065-01 dropped as duplicate),
    S-0067-01, S-0070-01.

## Metrics

| Metric | Value |
| --- | --- |
| New tasks created | 2 (t0074, t0075) |
| Tasks cancelled | 0 |
| Tasks updated (other than cancellations) | 0 |
| Suggestions rejected | 9 (S-0065-01, S-0068-01, S-0068-02, S-0068-04, S-0068-05, S-0069-01, S-0069-02, S-0069-03, S-0069-04) |
| Suggestions reprioritised | 3 (S-0002-01, S-0002-04, S-0070-02) |
| Corrections written | 12 |
| New suggestions created | 0 |
| Answer assets created | 0 |
| Session duration | ~115 minutes interactive |
| Session cost | $0.00 |

## Verification

* `verify_task_file.py t0073_brainstorm_results_12` — target 0 errors.
* `verify_corrections.py t0073_brainstorm_results_12` — target 0 errors across 12 correction
  files.
* `verify_suggestions.py t0073_brainstorm_results_12` — target 0 errors (empty array).
* `verify_logs.py t0073_brainstorm_results_12` — target 0 errors; LG-W005 / LG-W007 / LG-W008
  acceptable per skill guidance and step-4 capture.
* `verify_task_file.py t0074_channel_tuning_width_bed_a` — target 0 errors.
* `verify_task_file.py t0075_bio_realistic_ais_param_sweep` — target 0 errors.
* `verify_pr_premerge.py t0073_brainstorm_results_12 --pr-number <N>` — target 0 errors.

## Next Steps

1. **t0074 execution**: independent of any in-flight task; can be commissioned to `/execute-task`
   immediately. Vendoring overhead is the main risk; the regression gate against t0067's DSI = 0.797
   baseline catches any unintended dynamics from un-zeroing CaL / CaT in `init_active`.

2. **t0075 execution**: blocked on t0074 (Kv7 vendoring). Stage 1 baseline calibration is time-cheap
   (~5 min wall-clock); if no in-band baseline is found, the task halts after Stage 1 with a
   negative result and a follow-up recommendation. If Stage 1 succeeds, Stage 2 runs ~100 min and
   produces the 8 per-axis sensitivity plots plus the biologically-plausible AIS recommendation
   table.

3. **Highest-leverage unaddressed experiment** (not commissioned in this session per researcher
   request): S-0065-02 (match from-scratch GABA reversal to v_rest). Both deposited beds use
   `e_GABA = v_rest = -60 mV` for pure shunting; the from-scratch wave (t0052-t0059) is in the
   binary regime. A single-line change to e_GABA in the from-scratch substrate may unlock the entire
   wave. Flagged as the highest-priority candidate for the next brainstorm.

4. **Decision point after t0074 + t0075**: if t0074 finds at least one channel that broadens tuning
   while preserving DSI > 0.5, that channel becomes a candidate for the t0075 AIS baseline in a
   follow-up. If t0075 Stage 1 finds an in-band baseline, the recommended AIS configuration can
   become the standard substrate for any future RQ4 active-dendrite experiments on Bed A.
