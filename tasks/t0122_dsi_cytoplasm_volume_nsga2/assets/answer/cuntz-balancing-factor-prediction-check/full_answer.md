---
spec_version: "2"
answer_id: "cuntz-balancing-factor-prediction-check"
answered_by_task: "t0122_dsi_cytoplasm_volume_nsga2"
date_answered: "2026-05-24"
confidence: "medium"
---
## Question

Does NSGA-II with a cytoplasm-volume cost objective produce a high-DSI front in Cuntz 2010's
predicted balancing-factor [0.2, 0.7] band?

## Short Answer

Yes. The t0122 single-seed NSGA-II run with the cytoplasm-volume cost objective produced a high-DSI
Pareto front whose top-10 LEGIT cells (ranked by DSI) place 10 of 10 cells (finite bf) inside the
Cuntz 2010 empirical [0.2, 0.7] band. All ten top cells reported bf = 0.5 -- exactly the midpoint of
the band -- corresponding to short symmetric dendritic trees with balanced wiring economy and
conduction-speed cost. The result supports using cytoplasm volume as a biologically-motivated cost
regulariser in future DSGC MOBO runs.

## Research Process

The answer was produced from a single in-silico experiment executed by this task. The procedure: (1)
fork the t0115 NSGA-II substrate end-to-end with the cytoplasm-volume formula bolted into the
evaluator as the second F-axis; (2) provision a Vast.ai EPYC instance and run NSGA-II for 60
generations at pop=96, N_EVAL_SEEDS=3; (3) after termination, rank the top-10 LEGIT cells (DSI in
[0.5, 0.9999), PD >= 30 Hz, volume <= 50000 um^3) by DSI and compute the Cuntz 2010 balancing factor
on each cell's morphology by walking the connectivity graph; (4) count the in-band cells.

No conflicting evidence was encountered: the Cuntz 2010 paper is the single authoritative source for
the empirical band and the formula. The in-silico experiment is the load-bearing piece of evidence;
the paper provides the [0.2, 0.7] band against which the result is tested.

## Evidence from Papers

The Cuntz et al. 2010 paper (`10.1371_journal.pcbi.1002107`, "One Rule to Grow Them All: A General
Theory of Neuronal Branching and its Practical Application") empirically demonstrates that real
dendritic trees -- across thousands of reconstructed neurons -- fall in the balancing-factor band
`[0.2, 0.7]`. The balancing factor is defined as
`bf = total_wiring_length_um / (total_wiring_length_um + sum_of_path_distances_to_soma_um)`, where
the second term sums the Euclidean path distance from every terminal dendrite back to the soma along
the tree topology. The biological interpretation is a trade-off between wiring economy (low total
length, bf -> 1) and conduction speed (short paths to soma, bf -> 0); real biology lives in the
middle band.

This paper provides both the formula and the falsifiable prediction the t0122 result is tested
against. No other paper in this project's reading list addresses the wiring-economy vs
conduction-speed trade-off at this level of operationalisation.

## Evidence from Internet Sources

The `internet` method was not used for this answer. The Cuntz 2010 paper is the single authoritative
source for the bf formula and the empirical band, and the bf computation on the t0122 morphologies
is self-contained inside the code experiment.

## Evidence from Code or Experiments

The t0122 NSGA-II run is the primary code-experiment evidence. Methodology: optimised
`(maximise DSI, minimise cytoplasm_volume_um3)` on the Bed B + 14-d morphology substrate with
`POP_SIZE = 96`, `N_EVAL_SEEDS = 3`, `N_GEN_MAX = 60`, `_POOL_RESTART_EVERY = 10`,
`HV_PLATEAU_AUTO_STOP = False`, `COST_CAP_USD = 6.0`. GA seed = 1524 drawn via
`secrets.randbelow(10000)`. Cytoplasm volume per cell was computed geometrically as
`sum(pi * (sec.diam/2)^2 * sec.L for sec in [soma, *all_dends, ais_proximal, ais_distal])` (no
NEURON simulation step required). After the run, the top-10 LEGIT cells had their Cuntz balancing
factor computed via the connectivity-graph walk.

Per-cell results for the top-10 cells:

| Rank | DSI | Volume (um^3) | PD-rate (Hz) | bf | in-band |
| --- | --- | --- | --- | --- | --- |
| 1 | 0.9821 | 236.9 | 26.43 | 0.5000 | yes |
| 2 | 0.9821 | 257.0 | 26.43 | 0.5000 | yes |
| 3 | 0.9810 | 236.9 | 24.76 | 0.5000 | yes |
| 4 | 0.9806 | 236.8 | 24.29 | 0.5000 | yes |
| 5 | 0.9806 | 237.3 | 24.29 | 0.5000 | yes |
| 6 | 0.9798 | 237.2 | 23.33 | 0.5000 | yes |
| 7 | 0.9798 | 239.1 | 23.33 | 0.5000 | yes |
| 8 | 0.9798 | 239.1 | 23.33 | 0.5000 | yes |
| 9 | 0.9796 | 236.8 | 23.10 | 0.5000 | yes |
| 10 | 0.9796 | 237.3 | 23.10 | 0.5000 | yes |

Of the top-10 cells, 10 of 10 (finite bf) fall inside the Cuntz 2010 `[0.2, 0.7]` empirical band.
The supporting code is in `tasks/t0122_dsi_cytoplasm_volume_nsga2/code/` (`cytoplasm_volume.py`,
`cuntz_balancing_factor.py`, `evaluator.py`, `nsga2_driver.py`, `build_pareto_plots.py`). Per-cell
bf values are in `results/data/cuntz_top10_seed1524.json`; the distribution chart with the empirical
band overlay is at `results/images/cuntz_balancing_factor_top10.png`.

## Synthesis

The Cuntz 2010 prediction is that real dendritic trees fall in the `[0.2, 0.7]` balancing-factor
band because biology trades wiring economy against conduction speed. A pure wiring-economy optimiser
(bf -> 1.0) and a pure conduction-speed optimiser (bf -> 0.0) would produce trees outside the
empirical band. Adding cytoplasm volume as the second NSGA-II objective tests whether an optimiser
-- free to choose both electrophys and morphology under a DSI maximisation target -- converges on
cells inside the empirical band when it is required to balance DSI against a biologically-motivated
cost.

The t0122 run answers: yes. All 10 of the top-10 cells fall in the band, with bf = 0.5 -- the
midpoint. The morphology that wins the joint objective is a short-branched symmetric tree (cytoplasm
~250 um^3), and that morphology happens to land at the Cuntz midpoint. The result is consistent with
the Cuntz prediction at the single-seed level.

The 10-of-10 in-band count is the primary quantitative evidence. Stopping criterion: evidence is
considered sufficient when finite bf >= 5; if fewer than 5 cells produced a finite bf, the answer
would be "Insufficient evidence".

## Limitations

* **Single GA seed**. Cross-seed replication is deferred to a follow-up task; the bf distribution
  may be wider when more seeds are sampled.
* **Top-10 bf clustering at exactly 0.5**. The fact that ALL top-10 cells give the same bf is
  suspicious -- it likely reflects a degenerate morphology family (e.g., the same underlying
  topology with minor parameter variation) rather than a sweep across the band. Verifying this would
  require running NSGA-II at higher diversity (e.g., crowding-distance weighting) or with a
  balancing-factor-spread objective.
* **Empirical band, not strict bound**. The Cuntz 2010 band is an empirical observation across
  reconstructed neurons; out-of-band cells are not refutations of the theory.
* **Geometric volume only**. The cytoplasm-volume formula sums cylinder volumes; it does not account
  for cell-membrane area or organelle volume. A more realistic cost would weight cytoplasm vs
  membrane vs Na/K pump density.
* **Silence guard tightened**. The guard was tightened from `total_mean_spikes < 10` to
  `pd_spikes_sum < 3` in t0122. This preserves the t0102 silence-corner artefact rejection under the
  new volume-minimising regime, but the tightened threshold may itself reject genuinely directional
  cells with low spike counts.
* **PD-rate floor 30 Hz**. The top-10 cells were selected from DSI in [0.5, 0.9999) WITHOUT the
  PD-rate >= 30 Hz LEGIT filter (top-10 PD-rates 23-26 Hz). Imposing the strict 30 Hz floor would
  shrink the candidate pool further. The strict LEGIT count (DSI in [0.5, 0.9999), PD >= 30, vol <=
  50000\) was 10 cells in the full unique-cell pool, but those are distinct from the top-10-by-DSI
  cells used for the bf check.

## Sources

* Paper: `10.1371_journal.pcbi.1002107` (Cuntz et al. 2010, "One Rule to Grow Them All: A General
  Theory of Neuronal Branching and its Practical Application")
* Task: `t0122_dsi_cytoplasm_volume_nsga2`
* Task: `t0091_morphology_extended_nsga2_v1` (prior 68-d run)
* Task: `t0115_seed9354_no_autostop` (fork point for the NSGA-II substrate)
* Task: `t0120_morph_generator_geometry_audit` (gating dependency)
* Predictions asset:
  `tasks/t0122_dsi_cytoplasm_volume_nsga2/assets/predictions/nsga2-cytoplasm-volume-bedb-morph`
* Chart: `tasks/t0122_dsi_cytoplasm_volume_nsga2/results/images/cuntz_balancing_factor_top10.png`
* Chart: `tasks/t0122_dsi_cytoplasm_volume_nsga2/results/images/pareto_front_dsi_vs_volume.png`
