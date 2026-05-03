# Results Summary: Brainstorm Session 13

## Summary

Thirteenth strategic brainstorm, run on 2026-05-03 after t0074 (channel tuning-width sweep on Bed A)
and t0076 (25-d Bed B BoTorch qNEHVI multi-objective Bayesian optimisation) both completed. The
session is triggered by the t0076 headline negative result: the bare 25-d Bed B substrate cannot
reach DSI >= 0.4 AND PD rate >= 30 Hz simultaneously, with every Pareto cell trading off severely
between the two objectives. The t0076 compare-literature analysis identified three architectural
omissions that plausibly explain the trade-off: no AIS section, uniform-density channels, and absent
slow-AHP machinery. Decision: commission a single bundled MOBO task (t0078
`bedb_mobo_v2_ais_tiered_ahp`) covering all three architectural fixes plus the t0076 implementation
defects; reject sixteen suggestions (five covered by t0078, eleven stale from-scratch-family
follow-ups); cancel t0045 (CoreNEURON-on-GPU benchmark) as superseded by t0076's actual Vast.ai-CPU
run; no reprioritisations; no new suggestions; no answer assets.

## Session Overview

Date: 2026-05-03. Triggered by the t0076 headline negative result and the convergent
compare-literature analysis pointing to AIS / tier-stratification / slow-AHP as the missing
architectural ingredients on Bed B. The session opened with an independent priority reassessment of
the 20 high-priority active uncovered suggestions in light of the t0076 architectural-omission
triple and the t0074 channel-modulation map (NaP collapses DSI; SK halves HWHM; Kv3 / Kv4 / Kv7
inert at all somatic densities; Nav1.6 boosts firing without DSI loss; NaR broadens HWHM by +36 deg
with no DSI change). The researcher steered Round 1 by stating the focus area: MOBO follow-ups, with
S-0076-02 (AIS-augmented MOBO) declared the most important suggestion and S-0076-01 (tier-stratified
channel densities) and S-0076-05 (slow Kv-AHP) bundled in as additional MOBO parameters. AI proposed
a single bundled t0078 covering all three plus the t0076 implementation fixes (S-0076-03) and the
Bed B AIS library asset (S-0024-03). AI asked four scoping questions: slow-AHP implementation
choice, parameter budget, warm-start strategy, suggestion cleanup scope. Researcher answered: SK_E2
with extended Ca-binding; 40 - 50 d acceptable; restart fresh from Sobol; yes to deprioritising
stale from-scratch family. Round 2 received approval on the sixteen-rejection cleanup proposal (five
covered by t0078, eleven from-scratch-family stale). Round 3 received explicit "approve" plus "yes,
cancel it" for t0045, authorising the entire remaining lifecycle through PR merge.

## Decisions

1. **Create t0078** (`bedb_mobo_v2_ais_tiered_ahp`). Bundled Bed B v2 multi-objective Bayesian
   optimisation: build an AIS section onto Bed B with Van Wart 2007 / Werginz 2020 priors
   (AIS-to-soma Na ratio ~7x, AIS length 25-50 um, two-subsegment proximal Nav1.2 / distal Nav1.6 +
   Kv1.2); register the AIS-augmented Bed B as a new library asset (covers S-0024-03); tier-stratify
   Nav1.6 / Kv3 / NaP / BK / SK across 5 tiers (soma, proximal, mid, terminal, AIS) keeping other
   channels uniform — ~25 - 30 channel-density parameters (covers S-0076-01); add a slow
   Kv-mediated AHP via SK_E2 with extended Ca-binding at soma + AIS only, treating peak conductance
   and possibly tau_Ca as 1 - 2 free MOBO parameters (covers S-0076-05); migrate to qLogNEHVI; wrap
   GP inputs in Normalize transform on [0, 1]^d; fix the NEURON `Exp2NMDA name already exists`
   re-init bug via subprocess-per-deep-dive (covers S-0076-03). Total parameter space ~40 - 50 d.
   Restart fresh with Sobol DoE + qLogNEHVI (no warm-start from t0076). Pass criterion: locate at
   least one Pareto cell with DSI >= 0.4 AND PD rate >= 30 Hz, OR rule it out architecturally with a
   clean negative result. Compute estimate ~$2.50 - $4.00 over 9 - 12 h on a Vast.ai 72-core CPU.
   Source suggestion: S-0076-02. Dependencies: t0024 (de_rosenroll_2026_dsgc), t0069 (Bed A AIS
   architecture to crib from), t0076 (BO harness).

2. **Cancel t0045** (`coreneuron_vastai_speedup_benchmark`). Originally framed as the 5x
   CoreNEURON-on-GPU vs stock-NEURON-on-CPU benchmark to validate the t0033 cost-model assumption.
   t0076 has now actually run on Vast.ai 72-core CPU for $1.0583 over 6.4697 h with 68,800 NEURON
   simulations and produced useful science, validating that stock NEURON on Vast.ai CPU is
   cost-feasible at the project's scale. Original urgency gone; no longer load-bearing.

3. **Reject S-0076-01** — covered by t0078 (tier-stratified channel densities folded in as 5-tier
   expansion).

4. **Reject S-0076-02** — covered by t0078 (AIS-augmented Bed B MOBO; primary scope).

5. **Reject S-0076-03** — covered by t0078 (qLogNEHVI / GP-normalise / NEURON re-init fixes folded
   in).

6. **Reject S-0076-05** — covered by t0078 (slow Kv-AHP via SK_E2 with extended Ca-binding folded
   in as MOBO parameter).

7. **Reject S-0024-03** — covered by t0078 (Bed B AIS library asset built as part of bundled MOBO
   scope).

8. **Reject S-0052-01** — stale from-scratch family (AMPA per-synapse conductance sweep on t0052;
   project pivoted to deposited beds).

9. **Reject S-0052-02** — stale from-scratch family (GABA-synapse-count sweep on t0052; scalar
   gabaMOD design superseded by deposited beds).

10. **Reject S-0054-02** — stale from-scratch family (3-D conductance sweep on t0054; same
    question being answered on Bed B in t0078 with biologically grounded Mg-block NMDA + AIS + slow
    Kv-AHP).

11. **Reject S-0055-02** — stale from-scratch family (re-run t0055 Mg-block sweep on corrected
    protocol; corrected protocol already applied to deposited beds in t0065 / t0066).

12. **Reject S-0055-03** — stale from-scratch family (GABA-reduction ladder on Mg-block t0055;
    answered on Bed B in t0078).

13. **Reject S-0057-06** — stale from-scratch family (tonic GABA + Mg-block NMDA on t0054-style;
    answered on Bed B in t0078 where Mg-block NMDA + tonic GABA + AIS spike initiation + slow Kv-AHP
    all interact under joint optimisation).

14. **Reject S-0059-01** — stale from-scratch family (active dendritic Nav1.6 + Kv3 on t0059;
    Nav1.6 already characterised on Bed A in t0074, Kv3 / Nav1.6 being characterised on Bed B in
    t0078).

15. **Reject S-0059-02** — stale from-scratch family (Mg-block NMDA + bar-locked GABA +
    AMPA-escape on t0059; same combination natively present in Bed B substrate, answered in t0078).

16. **Reject S-0059-03** — stale from-scratch family (synapse-count scaling on t0059; Bed B
    already operates with > 1000 SAC varicosities by design).

17. **Reject S-0065-02** — stale from-scratch family (e_GABA = v_rest match on from-scratch;
    flagged in brainstorm 12 as highest-leverage uncommissioned but project has pivoted decisively
    to deposited beds since).

18. **Reject S-0066-02** — stale from-scratch family (EPSP / IPSP / FULL on from-scratch; protocol
    already applied to both deposited beds in t0065 / t0066).

19. **Keep at high priority** the suggestions still on the active critical path: S-0067-01 (NaP
    density crossing zero DSI), S-0070-01 (cross-bed PD/ND encoding harmonisation), S-0074-01 (SK
    polar-curve clipping check), S-0074-02 (NaR ND-floor verification), S-0074-03 (AIS-localised Kv7
    — covered by the still-not-started t0075 but kept active in case t0075 is delayed), S-0076-04
    (t0076-vs-t0068 contradiction test), S-0076-06 (BoTorch MOBO library extraction).

## Metrics

| Metric | Value |
| --- | --- |
| New tasks created | 1 (t0078) |
| Tasks cancelled | 1 (t0045) |
| Tasks updated (other than cancellations) | 0 |
| Suggestions rejected | 16 (S-0024-03; S-0052-01, S-0052-02; S-0054-02; S-0055-02, S-0055-03; S-0057-06; S-0059-01, S-0059-02, S-0059-03; S-0065-02; S-0066-02; S-0076-01, S-0076-02, S-0076-03, S-0076-05) |
| Suggestions reprioritised | 0 |
| Corrections written | 16 |
| New suggestions created | 0 |
| Answer assets created | 0 |
| Session duration | ~115 minutes interactive |
| Session cost | $0.00 |

## Verification

* `verify_task_file.py t0077_brainstorm_results_13` — target 0 errors.
* `verify_corrections.py t0077_brainstorm_results_13` — target 0 errors across 16 correction
  files.
* `verify_suggestions.py t0077_brainstorm_results_13` — target 0 errors (empty array).
* `verify_logs.py t0077_brainstorm_results_13` — target 0 errors; LG-W005 / LG-W007 / LG-W008
  acceptable per skill guidance and step-4 capture.
* `verify_task_file.py t0078_bedb_mobo_v2_ais_tiered_ahp` — target 0 errors.
* `verify_task_file.py t0045_coreneuron_vastai_speedup_benchmark` — target 0 errors after the
  cancellation edit.
* `verify_pr_premerge.py t0077_brainstorm_results_13 --pr-number <N>` — target 0 errors.

## Next Steps

1. **t0078 execution**: ready to commission to `/execute-task` immediately. The task is the
   project's highest-leverage queued experiment: it directly tests whether the t0076 negative result
   (no DSI >= 0.4 AND rate >= 30 Hz operating point) is an artefact of missing architectural
   ingredients (AIS, tier-stratification, slow-AHP) or a fundamental Bed B limitation. Either
   outcome is a strong project result. Compute estimate $2.50 - $4.00 fits comfortably in the $8.94
   remaining budget.

2. **t0075 (Bed A bio-realistic AIS one-axis sweep)**: still not_started, blocked on no remote
   compute requirement; can run in parallel with t0078 once a worktree opens. Different substrate
   from t0078, complementary one-axis-at-a-time sensitivity vs t0078's joint optimisation.

3. **Highest-leverage unaddressed experiments** (not commissioned in this session): S-0067-01 (NaP
   density crossing DSI = 0; cheap ~25 min sweep), S-0074-01 (SK polar-curve clipping check; pure
   data analysis, ~30 min), S-0074-02 (NaR ND-floor verification; ~15 min). All three are
   inexpensive analyses on existing data; flagged for the next brainstorm or for opportunistic
   pickup.

4. **Decision point after t0078 completes**: if t0078 finds a Pareto cell with DSI >= 0.4 AND PD
   rate >= 30 Hz, the AIS-augmented Bed B becomes the project's standard substrate for further
   joint-optimisation work and the AIS library asset becomes a permanent reusable component. If
   t0078 rules out the joint operating point even with AIS + tier-stratification + slow-AHP, the
   negative result has clear architectural implications (likely dendritic-spike machinery is the
   remaining missing ingredient) and the project pivots to dendritic-spike modelling on Bed B.
