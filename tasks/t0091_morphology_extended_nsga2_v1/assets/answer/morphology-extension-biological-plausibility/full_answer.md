---
spec_version: "2"
answer_id: "morphology-extension-biological-plausibility"
answered_by_task: "t0091_morphology_extended_nsga2_v1"
date_answered: "2026-05-08"
confidence: "medium"
---

## Question

Did enabling the 14-d procedural morphology variation as an optimisation axis open biologically-plausible joint-pass regions of parameter space that the fixed-Bed-B substrate of t0080-t0088 could not reach?

## Short Answer

No, 0 of 57 Pareto cells reach the joint biological-plausibility region under the 13-prior worst-case aggregation.

## Research Process

The implementation ran a joint 68-d NSGA-II via pymoo (pop 96, up to 8
generations, SBX eta=15, polynomial mutation eta=20 prob=1/68, eliminate
duplicates) with the t0092 patched morphology generator inside the per-cell
evaluation loop. The warm-start population was assembled from 5 morphology
anchors (Bed-B-like, symmetric, PD-asymmetric, ND-asymmetric,
alternative-topology) each cloned with electrophys vectors from t0083's
Pareto archive (preferring t0086 Genuine + Marginal cells), plus 1 random
LHS fill = 96 cells. Per-cell evaluation ran 16 directions x 5 seeds with
objectives = (DSI vector-sum, PD firing rate, robustness as inverse CV of
DSI across seeds). The Pareto front was extracted via pymoo
NonDominatedSorting on the 3-objective evaluations across all generations.
Per-cell biological scoring used 9 electrophys priors (Kole 2008, Werginz
2024, Sivyer 2013 corrected, Branco 2010, Oesch 2005, Stuart 1999,
de Rosenroll 2026, ratio-derived) and 4 morphology priors
(Schachter/Trenholm soma offset, Briggman field elongation, Vaney 2012
anatomical-symmetry pair). Per-cell verdict was the worst-case across all
13 priors (`plausible` if all |dev| <= 2 sigma; `stretched` if up to 5
sigma; `exotic` otherwise).

## Evidence from Papers

The 13 biological priors are grounded in published measurements:

* Kole 2008 — AIS Nav density 0.25-0.5 S/cm^2 prior.
* Werginz 2024 — AIS Nav 1.3 S/cm^2; AIS-to-soma ratio 17.3x.
* Sivyer 2013 (corrected units per t0090 Phase G.2) — dendritic NMDA conductance.
* Schachter 2010 / Trenholm 2013 — soma displacement bounds.
* Briggman 2011 — dendritic field aspect ratio prior.
* Vaney 2012 — anatomical-symmetry priors.
* Anderson 1999 — cable-theoretic v_opt = 2 lambda / tau_m.
* Hausselt 2007 — DSI scales with dendritic length.

See `research/research_papers.md` for the full bibliography.

## Evidence from Internet Sources

The pymoo NSGA-II algorithm parameters (SBX eta=15, polynomial mutation
eta=20, eliminate_duplicates) were chosen following the pymoo 0.6 docs
and Lopez-Camacho 2022 default settings for moderate-d MOEA. NSGA-II
was preferred over BoTorch qLogNEHVI for d=68 per the project's standing
preference (NSGA-II for d > 40, BoTorch only for d <= 40) — see
`research/research_internet.md` for the full discussion.

## Evidence from Code or Experiments

* Pareto front: 57 cells.
* Verdict distribution: 0 plausible / 0 stretched /
  57 exotic.
* Anchor distribution (count per anchor): [20, 0, 12, 9, 16].
* PD-asymmetric vs ND-asymmetric over-representation: one-sided permutation
  p-value = 0.3311 (1000 bootstrap resamples).

See:

* `tasks/t0091_morphology_extended_nsga2_v1/results/data/pareto_front.json`
* `tasks/t0091_morphology_extended_nsga2_v1/results/data/biological_scorecard_68d.json`
* `tasks/t0091_morphology_extended_nsga2_v1/results/data/anchor_tracking.json`
* `tasks/t0091_morphology_extended_nsga2_v1/results/images/biological_plausibility_heatmap_68d.png`
* `tasks/t0091_morphology_extended_nsga2_v1/results/images/anchor_tracking_bar.png`
* `tasks/t0091_morphology_extended_nsga2_v1/results/images/dsi_vs_length.png`

## Synthesis

The morphology extension does not reach
biologically-plausible joint-pass regions in this run. The v3 electrophys
substrate's existing prior violations (NaP, GABA spatial gradient, NMDA
scaling) carry through to all Pareto cells, suggesting that morphology
variation alone cannot rescue biological plausibility within this
parametrisation. The PD-asymmetric vs ND-asymmetric over-representation
(p=0.331) is below the 5:1 effect-size threshold from
Briggman 2011 needed to claim that soma-displacement-toward-PD asymmetry
is functional given pop 96 / 5 anchors / ~19 cells per anchor.

## Limitations

* 8-generation NSGA-II cap may have terminated before full convergence.
* The 4 morphology priors used wide sigma values from anatomical-symmetry
  arguments rather than direct measurements.
* Robustness was estimated from 5 seeds; larger seed counts would tighten
  the inverse-CV estimate.

## Sources

* Task: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* Task: `t0083_bedb_v3_extend_nsga2_gen8plus`
* Task: `t0086_robustness_cluster_bio_comparison`
* Task: `t0088_recluster_marginals_and_vm_motifs`
* Task: `t0090_morphology_generator_diversity_test`
* Task: `t0092_diagnose_morphology_generator_silence`
* Task: `t0093_resweep_and_t0090_correction`
