# Brainstorm Session 18 -- Full Transcript

## Project State Presented

After running task / suggestion / cost aggregators and reading t0088's outputs:

**Budget**: $15.55 spent / $20.00 (77.8 percent); $4.44 remaining. t0083 only task over per-task
limit ($5.83 vs $5.00).

**Tasks since last brainstorm (t0087)**: just one new completed task -- t0088
(`recluster_marginals_and_vm_motifs`):

* Re-clustered the 13-cell pool (6 Genuine + 7 Marginal from t0086) into best_k = 4 by silhouette
  (0.164).
* Per-cluster representative Vm-trace deep-dive at 16 directions, all 64 sims stable, $0 cost.
* Verdict `shared_mechanism_different_scale`: all 4 clusters NaP-dominant in PD-minus-ND attribution
  (NaP frac 87.4-99.7 percent, Nav1.6 0.3-12.6 percent, NMDA 0 percent).
* All 4 clusters classified exotic by biological scorecard.
* New extreme prior violation: cluster 1 AIS-to-soma Nav ratio = 116x (vs Werginz 2024 17.3 +/- 3 =
  +33 sigma) -- most extreme single-prior violation in any t0086 / t0088 analysis.
* Cluster 3 closest to biological plausibility (only NMDA + NaP + GABA-rho0 violations).

**Where this leaves the project**: core mechanism question is settled (NaP-dominant sustained
dendritic depolarisation; NMDA provides baseline depolarisation but contributes 0 percent to
PD-vs-ND differential). The pressing question now: how much of the "exotic" verdict reflects genuine
biology vs measurement / units mismatches, and whether biologically plausible joint-pass cells exist
at all.

**Independent priority reassessment of 15 active high-priority suggestions**:

* PRIORITY UP (most urgent): S-0088-02 (audit AIS-to-soma Nav ratio computation, $0, 30 min);
  S-0086-02 (NMDA units calibration, $0.30, 1 h); S-0088-01 (causal NaP-knockout, $0, 64 min).
* STAYS HIGH: S-0086-01 (NSGA-II re-run with tightened NMDA bounds, $1.50); S-0070-01 (PD / ND
  encoding harmonisation across Bed A and Bed B).
* DOWN to MEDIUM (or REJECT as covered): S-0083-01 (out of budget); S-0083-03 (covered by t0088
  cluster 1); S-0084-01 (superseded); S-0084-02 (older single-cell scope); S-0084-05 (REJECT
  duplicate of S-0088-01); S-0067-01 / S-0074-01/02/03 / S-0076-04 (older lower priority).

**Initial proposed task**: t0089 (validation triplet bundle: Nav-ratio audit + NMDA units
calibration + causal NaP-knockout, ~$0.30, ~3-4 hours wall-clock).

## Researcher Strategic Pivot

> **Researcher**: "Optimisation technique seems to work. We now need to add a big and important part
> of cells - cell morphology. Propose a way to parametrise cell morphology and then create task
> where cell morphology is used along with electrophys and other parameters that we already used."

This is a major scope expansion: morphology had been sensitivity-tested one-axis-at-a-time (t0029,
t0030, t0034, t0035, t0041) but never inside the optimisation vector.

## Discussion -- Iteration 1: Tier-based scaling (Option A)

**AI**: Proposed three options:

* **Option A**: tier-based geometric scaling of Bed B (8 params: 3 tier length scales + 3 tier
  diameter scales + soma diameter + AIS length).
* **Option B**: library of pre-generated morphologies + categorical selector.
* **Option C**: stochastic L-system tree generator.

Recommended Option A as the cleanest extension (54-d -> 62-d).

**Researcher**: "No that's not enough. It has to reflect branching morphology and also asymmetry
etc. Think more"

## Discussion -- Iteration 2: Procedural generator with explicit DS knobs (Option H)

**AI**: Acknowledged Option A only addressed geometry; topology and asymmetry are DS-functional
features (Schachter 2010 soma-displacement-toward-PD; Trenholm 2013 dendritic-field elongation;
Briggman 2011 branch-density gradient). Re-proposed Option H -- procedural DSGC morphology generator
with 14 explicit knobs:

| Group | Parameter | Range |
| --- | --- | --- |
| Topology | `num_primary_branches` | 3-7 (int) |
| Topology | `branch_prob_per_um` | 0.005-0.05 |
| Topology | `max_strahler_depth` | 2-6 (int) |
| Topology | `mean_branching_angle_deg` | 30-90 |
| Topology | `rall_exponent` | 0.5-2.0 |
| Asymmetry | `soma_offset_pd_um` | -150 to +150 |
| Asymmetry | `field_elongation_pd` | 1.0-3.0 |
| Asymmetry | `branch_density_gradient_pd` | -1 to +1 |
| Asymmetry | `primary_branch_pd_concentration` | 0-5 (von Mises kappa) |
| Geometry | `mean_segment_length_um` | 10-60 |
| Geometry | `soma_diameter_um` | 8-18 |
| Geometry | `ais_length_um` | 15-60 |
| Stochastic | `morph_seed` | int |
| Stochastic | `branch_length_cv` | 0-0.5 |

Total: 14 morphology params -> 68-d total parameter space (54-d v3 + 14 morph).

Proposed two-task split: t0089 (generator + sensitivity, ~$0.30) -> t0090 (joint NSGA-II,
~$3.00-3.50).

## Discussion -- Iteration 3: Architectural clarification round 1

**Researcher**: "why can't we incorporate generation of neurons into the optimisation?"

**AI**: Conceded the point: yes, in-loop generation is the architecture. Walked through
per-evaluation pseudocode showing where the generator is called inside the NSGA-II eval function.
Withdrew the two-task split in favour of a single bundled t0089. Listed three concerns that prompted
my over-mitigated de-risking and explained how each is addressable without splitting tasks.

## Discussion -- Iteration 4: Architectural clarification round 2

**Researcher**: "wait, I still don't understand. Why don't we generate morphologies during
optimisation? Or is it what you propose?"

**AI**: Confirmed yes -- explicitly contrasted Plan A (in-loop generation per evaluation) vs
alternatives (Plan B: pre-generated library + NSGA-II picks; Plan C: sensitivity-then- optimisation;
Plan D: fixed Bed B status quo). Clarified that "Phase A1: implement procedural generator" is just
the infrastructure work; the generator then lives inside the NSGA-II loop in Phase B and gets called
once per candidate.

## Discussion -- Round 1: New tasks (after researcher's two-task pivot)

**Researcher**: "OK, great. But you are right. Let's split it into two tasks. 1 - write and test
generator - generate and visualise say 30 random very different morphologies and 30 very similar
ones. U assume we can still use 64 core to parallelise the generation? And then second task - first
optimisation attempt. Use one seed that we currently have (WITH MORPHOLOGY SIMILAR TO WHAT WE HAVE)
and few more very different seeds - symmetric and asymmetric."

**AI**: Confirmed 64-core parallelisation works (generation embarrassingly parallel; verification
sims parallel on same 64-core EPYC; cost negligible). Designed:

* **t0090** (`morphology_generator_diversity_test`, ~$0.30, ~3-4 days local): generator
  implementation; 30 different morphologies (wide LHS); 30 similar morphologies (+/- 5 percent
  perturbations); verification simulation; 2D dendrogram + PCA / UMAP visualisation; Bed-B
  reproducibility check; validation bundle (S-0088-02 + S-0086-02 + S-0088-01) bundled in Phase G.
* **t0091** (`morphology_extended_nsga2_v1`, ~$3.00-3.50, ~14-16 hours Vast.ai): first joint 68-d
  NSGA-II with morphology generator inside eval loop; 5-anchor warm-start (Bed-B-like + symmetric +
  PD-asymmetric + ND-asymmetric + alt-topology); pop 96 x ~19 t0083 Pareto electrophys variants per
  anchor + 1 random sample; up to 8 generations, adaptive HV-plateau stop, $4.00 cost watchdog.

## Discussion -- Phase A time-estimate pushback

**Researcher**: "Why phase A takes 4 days?"

**AI**: Conceded the estimate was inflated. Honest sub-step breakdown:

| Sub-step | Time |
| --- | --- |
| Recursive tree builder | ~3-4 h |
| Asymmetry transforms | ~2-3 h |
| NEURON section translation | ~2-3 h |
| Determinism + unit tests | ~3-4 h |
| Bed-B reproducibility | ~2-3 h |

**Total: ~12-17 h ≈ 1.5-2 days wall-clock**, not 3-4. Inflation was anchored on human-developer
pace; agent-execution time is closer to 1.5 days.

Updated t0090 timeline: ~3-4 days total wall-clock (was 5-6).

## Discussion -- Round 2: Suggestion cleanup

**AI**: Proposed cleanup based on the independent priority reassessment from Phase 1:

* **REJECT 5**:
  * S-0086-02 (NMDA units calibration) -- covered by t0090 Phase G.
  * S-0088-01 (causal NaP-knockout) -- covered by t0090 Phase G.
  * S-0088-02 (AIS-to-soma Nav ratio audit) -- covered by t0090 Phase G.
  * S-0084-05 (channel-knockout DSI variant) -- duplicate of S-0088-01.
  * S-0083-03 (per-direction Vm-trace of cell 1304) -- covered by t0088 cluster 1 attribution.

* **REPRIORITISE 3 high -> medium**:
  * S-0083-01 (NSGA-II to gen 25 with pop 144, $8-12) -- out of budget; superseded.
  * S-0084-01 (NaP density sweep on cells 767 / 637 / 762) -- superseded.
  * S-0084-02 (per-seed mechanism decomposition of cell 767) -- superseded.

* **STAY HIGH**:
  * S-0086-01 (NSGA-II re-run with tightened NMDA bounds, $1.50) -- post-t0091 follow-up.
  * S-0070-01 (PD / ND encoding harmonisation) -- independent infra.

## Discussion -- Round 3: Confirmation

**AI**: Presented compact decision summary:

1. Create t0090 (generator + 30 different + 30 similar + viz + Bed-B repro + validation bundle).
2. Create t0091 (joint 68-d NSGA-II with 5-anchor warm-start).
3. Reject 5 + reprioritise 3 suggestions.
4. Validation triplet S-0088-02 + S-0086-02 + S-0088-01 bundled into t0090 Phase G.

**Researcher**: "all approved. fire away"

This is the explicit Phase 2 Round 3 confirmation authorising the entire remaining lifecycle
including push, PR, premerge, and merge per the `/human-brainstorm` skill specification.

## Decisions Summary

1. **Create t0090** (`morphology_generator_diversity_test`, $0.30, ~3-4 days local). 14-knob
   procedural DSGC morphology generator + 30 different + 30 similar morphologies + visualisation
   + Bed-B reproducibility + validation triplet bundle.

2. **Create t0091** (`morphology_extended_nsga2_v1`, $3.00-3.50, ~14-16 hours Vast.ai). First joint
   68-d NSGA-II with morphology generator inside eval loop; 5-anchor warm-start.

3. **Reject 5 suggestions** (covered or duplicate): S-0086-02, S-0088-01, S-0088-02, S-0084-05,
   S-0083-03.

4. **Reprioritise 3 suggestions high -> medium**: S-0083-01, S-0084-01, S-0084-02.

5. **Stay high**: S-0086-01 (post-t0091 follow-up), S-0070-01 (independent infra).

6. **Total estimated cost of commissioned tasks**: $3.30-3.80; buffer remaining after $0.94-1.44 of
   the $20.00 project budget.
