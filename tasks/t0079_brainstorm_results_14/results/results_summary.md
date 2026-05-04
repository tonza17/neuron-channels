# Results Summary: Brainstorm Session 14

## Summary

Fourteenth strategic brainstorm, run on 2026-05-04 after t0078 (49-d AIS-augmented Bed B v2 BoTorch
qLogNEHVI MOBO with tier-stratified channels and slow Kv-AHP) completed. The session is triggered by
the t0078 architectural diagnostic: the AIS-augmented substrate expanded the achievable Pareto front
by **+36% in hypervolume** over t0076 but still missed the joint pass criterion
`DSI >= 0.4 AND PD rate >= 10 Hz` -- the closest cell (iter 81) sits at DSI 0.316 / PD 9.68 Hz,
short by 0.084 on DSI and 0.32 Hz on PD. The compare-literature analysis identified two follow-on
diagnostics: passive dendrites are the bottleneck on the high-DSI rail (PD ceiling pinned at 2.86
Hz), and the optimiser exploited an AIS-disabled corner (nav16_ais collapsed to the search floor at
1e-5 S/cm^2, four orders below the Kole 2008 prior). Decision: commission a single bundled task
t0080 (`bedb_mobo_v3_dendritic_spike_nsga2`) covering dendritic-spike machinery, NSGA-II via pymoo
(replacing BoTorch qLogNEHVI), and biological hard lower bounds; reject three suggestions covered by
t0080 (S-0078-01, S-0078-02, S-0078-08); no reprioritisations; no other task changes. t0075 remains
queued.

## Session Overview

Date: 2026-05-04. Triggered by the t0078 architectural-diagnostic negative result and the convergent
compare-literature analysis pointing to dendritic-spike machinery as the missing architectural
ingredient on Bed B. The session opened with an independent priority reassessment of the 7
high-priority active uncovered suggestions in light of the t0078 architectural-omission diagnosis
(passive dendrites bottleneck the high-DSI rail; AIS-disabled-corner failure mode is a generalisable
MOBO-on-biophysics bug). The researcher chose the second clause of the AI's framing question 2 (the
dendritic-spike + next-big-task direction) but specifically requested switching the optimiser from
BoTorch qLogNEHVI to a genetic algorithm. AI recommended **NSGA-II via pymoo** with concrete
justification: O(N log N) per generation vs t0078's O(N^3) GP-fit blow-up; pop 96 / 40 gens fits the
budget; native Pareto front output matches t0076 / t0078 deliverables; hard bounds trivially
encoded; pure-Python no-GPU implementation eliminates the t0078 BoTorch / GPyTorch / NEURON re-init
pain. Researcher confirmed NSGA-II. AI proposed bundled t0080 covering S-0078-01 (dendritic-spike +
NSGA-II + AIS Nav lower bound), S-0078-02 (substrate regression check, folded as one-shot pre-run
validation cell), and S-0078-08 (AIS-disabled-corner failure mode, folded as an answer asset). AI
asked four scoping questions: bundled scope confirmation; S-0078-03 tau_ca_multiplier 200x fold-in;
t0075 disposition; cheap unaddressed analyses (S-0067-01 / S-0074-01 / S-0074-02). Researcher
answered: confirm bundled scope; do not fold in S-0078-03; t0075 stays queued (option a); defer
cheap analyses. Round 2 received approval on the three-rejection cleanup proposal (all three covered
by t0080). Round 3 received explicit "confirm" authorising the entire remaining lifecycle through PR
merge.

## Decisions

1. **Create t0080** (`bedb_mobo_v3_dendritic_spike_nsga2`). Bundled Bed B v3 multi-objective
   optimisation: add dendritic-spike machinery on top of the t0078 AIS-augmented substrate (Mg-block
   NMDA at active densities on dendrites; Nav1.6 + NaP at distal-dendrite densities sufficient for
   back-propagating APs and dendritic spikes per Sivyer 2013 / Oesch 2005); switch optimiser from
   BoTorch qLogNEHVI to NSGA-II via pymoo (pop 96, 40 gens, SBX crossover eta=15, polynomial
   mutation eta=20, tournament selection, LHS or Sobol initial population); enforce hard biological
   lower bounds per Kole 2008 / Werginz 2024 (`nav16_ais` >= 0.25 S/cm^2; AIS-to-soma Nav ratio >=
   5). Folded-in scope: S-0078-02 substrate regression check on the t0076 iter-424 parameter vector
   as a one-shot pre-run validation cell; S-0078-08 produces an answer asset documenting the
   AIS-disabled-corner failure mode and the biological-prior checklist now enforced as hard MOBO
   bounds. `tau_ca_multiplier` upper bound stays at 20x (S-0078-03 NOT folded in). Pass criterion:
   locate at least one Pareto cell with DSI >= 0.4 AND PD rate >= 10 Hz, OR rule it out
   architecturally. Compute estimate ~$1.00 - $1.50 over ~0.8 - 1.2 h on Vast.ai 64-core CPU; hard
   cap $2.00. Source suggestion: S-0078-01. Dependencies: t0024 (de_rosenroll_2026_dsgc), t0069 (Bed
   A AIS architecture reference), t0076 (BO harness), t0078 (AIS-augmented substrate library
   `de_rosenroll_2026_dsgc_ais`).

2. **Reject S-0078-01** -- covered by t0080 (primary scope: dendritic-spike + NSGA-II + AIS Nav
   lower-bound prior).

3. **Reject S-0078-02** -- covered by t0080 (substrate regression check folded in as one-shot
   pre-run validation cell on the t0076 iter-424 parameter vector).

4. **Reject S-0078-08** -- covered by t0080 (AIS-disabled-corner failure mode folded in as an answer
   asset documenting the failure mode and the now-enforced biological-prior checklist).

## Metrics

| Metric | Value |
| --- | --- |
| New tasks created | 1 (t0080) |
| Tasks cancelled | 0 |
| Tasks updated (other than cancellations) | 0 |
| Suggestions rejected | 3 (S-0078-01, S-0078-02, S-0078-08) |
| Suggestions reprioritised | 0 |
| Corrections written | 3 |
| New suggestions created | 0 |
| Answer assets created | 0 |
| Session duration | ~75 minutes interactive |
| Session cost | $0.00 |

## Verification

* `verify_task_file.py t0079_brainstorm_results_14` -- target 0 errors.
* `verify_corrections.py t0079_brainstorm_results_14` -- target 0 errors across 3 correction files.
* `verify_suggestions.py t0079_brainstorm_results_14` -- target 0 errors (empty array).
* `verify_logs.py t0079_brainstorm_results_14` -- target 0 errors; LG-W005 / LG-W007 / LG-W008
  acceptable per skill guidance and step-4 capture.
* `verify_task_file.py t0080_bedb_mobo_v3_dendritic_spike_nsga2` -- target 0 errors.
* `verify_pr_premerge.py t0079_brainstorm_results_14 --pr-number <N>` -- target 0 errors.

## Next Steps

1. **t0080 execution**: ready to commission to `/execute-task` immediately. The task is the
   project's highest-leverage queued experiment: it directly tests whether the t0078 architectural
   diagnostic (passive dendrites bottleneck the high-DSI rail) is correct, and whether the
   AIS-disabled-corner failure mode can be eliminated by hard biological bounds. Compute estimate
   $1.00 - $1.50 fits comfortably in the $5.01 remaining budget.

2. **t0075 (Bed A bio-realistic AIS one-axis sweep)**: still not_started, blocked on no remote
   compute requirement; can run in parallel with t0080 once a worktree opens. Different substrate
   (Bed A) from t0080 (Bed B), complementary one-axis-at-a-time sensitivity vs t0080's joint
   optimisation.

3. **Highest-leverage unaddressed experiments deferred to next brainstorm**: S-0067-01 (NaP density
   crossing DSI = 0; cheap ~25 min sweep), S-0074-01 (SK polar-curve clipping check; pure data
   analysis, ~30 min), S-0074-02 (NaR ND-floor verification; ~15 min), S-0078-05 (Vm-trace deep-dive
   PNGs for three closest-to-joint t0078 Pareto cells; ~30 min). All four are inexpensive analyses
   on existing data; flagged for opportunistic pickup or the next brainstorm.

4. **Decision point after t0080 completes**: if t0080 finds a Pareto cell with DSI >= 0.4 AND PD
   rate >= 10 Hz, the dendritic-spike-augmented Bed B v3 becomes the project's standard substrate
   for further joint-optimisation work. If t0080 rules out the joint operating point even with
   dendritic-spike machinery + NSGA-II + biological hard bounds, the negative result has clear
   implications: the trade-off may be intrinsic to the de Rosenroll Bed B substrate's morphology or
   SAC-release machinery, and the project pivots to alternative dendritic mechanisms (Ca^2+ plateau
   zones per Larkum / Branco-Hausser; Ih / HCN conductances) or substrate redesign.

5. **NSGA-II vs BO methodological side-quest**: S-0078-04 (single-objective scalarised BO comparison
   on the 49-d Bed B substrate) becomes more interesting if NSGA-II in t0080 also struggles -- it
   would test whether the bottleneck is the BO O(N^3) cost or the multi-objective formulation
   itself. Kept active at medium priority.
