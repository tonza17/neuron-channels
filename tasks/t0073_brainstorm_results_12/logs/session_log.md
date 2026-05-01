# Brainstorm Session 12 — Full Transcript

## Project State Presented

**Project status**:

* Tasks: 71 total at session start; all completed; 6 cancelled (t0023, t0031, t0042-t0045). Last
  brainstorm: t0058 = session 11 on 2026-04-29. (A parallel session merged
  `t0072_synaptic_traces_pd_nd` to main mid-brainstorm; brainstorm-results task and child task
  indices were renumbered from 72 / 73 / 74 to 73 / 74 / 75 to preserve causal ordering.)
* Budget: $0.00 spent of $1.00 (entirely local-CPU work; no paid services touched yet).
* Active uncovered suggestions: 226 — 20 high, ~80 medium, ~126 low.

**Tasks completed since last brainstorm (13 tasks, three arcs):**

* **Arc 1 — From-scratch wave reaches a negative result (t0059)**: bar-locked GABA + AMPA-escape
  sweep on t0057. 5x5 grid x 12 angles x 10 trials x 3 modes = 9000 trials, ~11.6 h. Max FULL peak
  rate 2.143 Hz; max primary DSI 0.500 (artefact); max vector-sum DSI 0.209. No cell entered the
  5-50 Hz multi-spike band. Bar-locked window mechanism validated (8.5 ms IPSP centre-of-mass shift
  between theta=0 and 90).
* **Arc 2 — Diagnostic triplet localises the failure (t0060-t0064)**: PD-only quick tests on the
  t0059 substrate at GABA = 0. t0060 (AMPA only): substrate CAN multi-spike, peaks at 4 spikes at
  gAMPA = 20 nS. t0061 (NMDA only, Mg-block): regenerative escape between gNMDA = 1.0 (0 spikes) and
  2.0 nS (3 spikes). t0062 (AMPA priming + NMDA sweep): synergy peak 4 spikes at gAMPA = 0.5 / gNMDA
  = 2.0. t0063 / t0064 (HH voltage- / current-step diagnostics): clean F-I curve, rheobase 0.1-0.2
  nA, peak 90 Hz at 1.0 nA, depol-block at 2.0 nA. The HH machine itself is not the bottleneck.
* **Arc 3 — Cross-bed protocol unmasks the shunting-inhibition design (t0065-t0072)**: t0065 (Bed
  A under EPSP / IPSP / FULL): DSI = 0.875; IPSP_PASSIVE flat at e_SACinhib = -60 mV in both
  directions because `e_GABA = v_rest = -60 mV` makes inhibition purely shunting. t0066 (Bed B): DSI
  = 0.7391; IPSP_PASSIVE flat at -60 mV in both directions (PD / ND peak − baseline = 0.16 / 0.30
  mV). Cross-model convergence — two structurally independent DSGC implementations both place
  `e_GABA = v_rest = -60 mV`. t0067 (channel-addition sweep on Bed A soma): NaP_high inverts DSI
  (-0.18, sign flip!); Nav1.6 monotonically erodes DSI (0.80 → 0.23 high); NaR / Kv3 / Kv4 nearly
  inert. t0068 (Nav1.6 + Kv3 rescue test): hypothesis falsified; ΔDSI < 0.025 in all 8 conditions.
  t0069 (AIS-localised channels): hypothesis falsified; AIS+axon adds an electrical sink that
  quenches the cell. t0070 / t0071 / t0072: documentation tasks (writeup of two model beds + typeset
  PDF + synaptic conductance / current traces).

**Independent priority reassessment vs `suggestions.json`**: the AI flagged five high-priority
labels as stale. Most strategically important reassessment: S-0065-02 (match from-scratch GABA
reversal to v_rest) — highest-leverage single experiment given t0065 / t0066 cross-model
convergence on `e_GABA = v_rest = -60 mV`. Other reassessments: S-0065-01 / S-0066-02 are near-
duplicates (one should be kept, the other rejected); S-0069-01 + S-0069-02 should be bundled into
one task (per researcher's consolidated-task preference); S-0002-01 / S-0002-04 / S-0070-02 should
drop to medium given the post-shunting strategic frame.

**Strategic synthesis presented**:

1. The shunting-inhibition discovery (t0065 / t0066) reframes the whole project. RQ1 / RQ3 are now
   downstream of an *architectural* question: does inhibition deflect Vm hyperpolarisingly, or does
   it shunt at v_rest? Both deposited models answer "shunt at v_rest"; the from-scratch wave's
   binary trap may simply be the wrong choice of e_GABA.
2. Voltage-gated channels alone don't fix DSI (t0067 / t0068 / t0069 all converge): NaP inverts,
   Nav1.6 erodes, Kv3 doesn't rescue, AIS is a current sink. Channel additions cannot substitute for
   a working synaptic-shunt design — the inhibition / excitation conductance ratio is what drives
   DSI.
3. The from-scratch substrate's HH machinery is healthy (t0063 / t0064) and CAN multi-spike under
   sufficient drive (t0060 / t0061 / t0062). The 2.143 Hz ceiling in t0059 is *not* an
   HH-calibration issue.

## Clarification Questions

AI:

1. Do you have any notes, ideas, or context from the past few days that should steer this session?
2. Strategic direction: my reading is that the highest-leverage next move is S-0065-02 (e_GABA =
   v_rest test on the from-scratch wave). Do you agree, or do you want to push first on a different
   lineage?
3. Scope per task: bundle related axes into single tasks (per your consolidated-task preference)?
4. Compute cap per task?
5. How many tasks (small focused 2-3, or broader 5-7), and anything you want me to avoid?

Researcher:

> So we have several things to figure out. 1st - whether channels affect the width of direction
> tuning. 2nd - we need a reasonable parameters for DSGC with axonal initial segment. We need to
> bring there all channels that belong there (including HH, am I correct?) but still have a decent
> DSI (not 1 and also reasonable firing rate). So for second task create a range of tests to find
> the best combination of parameters. This shouldn't be optimisation problem - just vary one
> parameter at a time. Start with the first task and then the second

## Discussion — Round 1: New Tasks

### Task 1 proposal

AI proposed **t0074 — Channel effect on direction-tuning width on Bed A**:

* Substrate: Bed A only (deposited Poleg-Polsky, t0008).
* Channel set initial proposal: t0067 set {Nav1.6, NaP, NaR, Kv3, Kv4} at low / medium / high = 16
  conditions.
* Encoding: 12-angle bar rotation (Bed A's native protocol per t0046 reproduction).
* Compute: 16 conditions x 12 angles x 5 seeds = 960 FULL trials + 384 passive = ~90 min.
* Width metrics: HWHM (deg), vector-sum DSI, peak rate, RMSE vs t0004 cosine target.

AI asked two questions:

1. Bed A only (cleanest continuity with t0067), or also Bed B (de Rosenroll, t0024) so we test
   whether the channel→width relationship is bed-specific?
2. Restrict to t0067 channels, or also include BK / SK (S-0068-01) and Kv7 / M-current (S-0068-02)?

Researcher: "Let's use Bed A only for now. Add BK/SK and Kv7. Time is no issue."

AI confirmed final t0074 scope:

* 8 channel types x 3 densities + 1 baseline = 25 conditions.
* 1500 FULL + 600 passive = 2100 trials, ~2.2 h compute.
* Vendoring overhead: BK + SK + Kv7 MOD files + calcium-pool mechanism + un-zero CaL / CaT in Bed
  A's `init_active`, with regression gate against t0067 baseline DSI = 0.797 within 1e-3. ~3-4 h
  coding.

### Task 2 proposal

AI proposed **t0075 — Biologically-realistic AIS one-axis-at-a-time parameter sweep on Bed A**:

* AIS channel set: {HHst basal Na+K, Nav1.6, Kv3, Kv7}. Excluded: NaP (controversial in AIS; t0067
  NaP_high inverts DSI), BK and SK (more soma / dendrite than AIS in RGCs).
* Geometry baseline (literature-informed): AIS diameter 0.8 micrometre, length 30 micrometre, axon
  stub 1.0 mm, soma `gnabar_HHst` 200 mS / cm^2 (halved from t0069's 400), AIS `gnabar_HHst` 400 mS
  / cm^2, AIS Nav1.6 medium, AIS Kv3 medium, AIS Kv7 low.
* Stage 1 baseline calibration: 6 candidates (varying soma_gnabar across {100, 150, 200, 250, 300, 4
  0 0} mS / cm^2 at fixed AIS) at 12 angles x 1 seed = 72 trials. Pick the candidate that lands in
  {peak Hz in [5, 50], DSI in [0.3, 0.95]}. If none does, halt and report negative.
* Stage 2: 8-axis one-at-a-time sweep from Stage-1 baseline. 27 conditions x 12 angles x 5 seeds =
  1620 FULL trials, ~100 min wall-clock. Total compute ~2 h.
* Width metrics: same as t0074 for cross-task comparability.
* Outputs: per-axis sensitivity plots, biologically-plausible AIS recommendation table.

AI asked three questions:

1. AIS channel set {HHst, Nav1.6, Kv3, Kv7}? (Excluding NaP, BK, SK.)
2. Task 1 → Task 2 dependency (Task 1 vendors Kv7), or run both in parallel with Kv7 vendored
   redundantly?
3. Anything else for this round?

Researcher: "1. agree 2. Task 1 first. 3. Nothing else."

## Discussion — Round 2: Suggestion Cleanup

AI proposed:

**Reject 9 suggestions (covered or duplicate)**:

| ID | Title | Reason |
| --- | --- | --- |
| S-0068-01 | BK / SK with Nav1.6 | Covered by t0074 |
| S-0068-02 | Kv7 with Nav1.6 | Covered by t0074 |
| S-0068-04 | Move Nav1.6 + Kv3 to a virtual AIS | Covered by t0075 |
| S-0068-05 | Sweep Kv3 alone | Superseded by t0074 |
| S-0069-01 | Halve somatic gnabar before AIS | Covered by t0075 axis 1 |
| S-0069-02 | Shrink AIS diameter to 0.5 micrometre | Covered by t0075 axis 3 |
| S-0069-03 | Vary axon length to probe sink | Covered by t0075 axis 8 |
| S-0069-04 | Nav1.6 + Kv3 on AIS at biological densities | Covered by t0075 baseline + axes 5 + 6 |
| S-0065-01 | Apply EPSP / IPSP / FULL to from-scratch family | Duplicate of S-0066-02 (kept) |

**Reprioritise 3 suggestions high → medium**:

| ID | Title | Reason |
| --- | --- | --- |
| S-0002-01 | Factorial g_Na x g_K | Pre-shunting framing; project has moved on |
| S-0002-04 | Factorial morphology | Same |
| S-0070-02 | Unified model-bed-runner library | Pure infra; not blocking |

**Keep at high (12 explicitly listed)**: S-0052-01, S-0052-02, S-0054-02, S-0055-02, S-0055-03,
S-0057-06, S-0059-01, S-0059-02, S-0059-03, **S-0065-02** (the e_GABA unlock — flagged as
highest-leverage uncommissioned experiment), S-0066-02 (kept, S-0065-01 dropped as duplicate),
S-0067-01, S-0070-01.

Researcher: "all sounds good."

## Discussion — Round 3: Confirmation

AI presented the final decision list:

* New tasks (2): t0074 (channel tuning-width sweep on Bed A), t0075 (biologically-realistic AIS
  parameter sweep on Bed A, depends on t0074).
* Suggestions rejected (9): listed above.
* Suggestions reprioritised (3): listed above.
* Tasks cancelled / updated: none.
* New suggestions / answer assets: none.

AI reminded researcher that go-ahead authorises the entire remaining lifecycle through PR merge
without further pause for confirmation between phases.

Researcher: "go".

## Decisions Summary

1. Create t0074 — `channel_tuning_width_bed_a`. Source suggestion: S-0068-01 (primary; S-0068-02,
   S-0068-05 also covered).
2. Create t0075 — `bio_realistic_ais_param_sweep`. Source suggestion: S-0069-01 (primary;
   S-0068-04, S-0069-02, S-0069-03, S-0069-04 also covered). Depends on t0074.
3. Reject S-0065-01 (duplicate of S-0066-02).
4. Reject S-0068-01 (covered by t0074).
5. Reject S-0068-02 (covered by t0074).
6. Reject S-0068-04 (covered by t0075).
7. Reject S-0068-05 (superseded by t0074).
8. Reject S-0069-01 (covered by t0075 axis 1 + Stage 1).
9. Reject S-0069-02 (covered by t0075 axis 3).
10. Reject S-0069-03 (covered by t0075 axis 8).
11. Reject S-0069-04 (covered by t0075 baseline + axes 5 + 6).
12. Reprioritise S-0002-01 high → medium.
13. Reprioritise S-0002-04 high → medium.
14. Reprioritise S-0070-02 high → medium.
15. No tasks cancelled or updated.
16. No new suggestions or answer assets created.

End of transcript.
