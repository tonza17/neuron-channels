---
spec_version: "2"
answer_id: "pooled-survivors-displacement-from-init-dsi07-pd10"
answered_by_task: "t0116_pooled_pca_cluster_factor_dsi07_pd10"
date_answered: "2026-05-21"
confidence: "high"
---
# Per-seed mean displacement from gen-0 ranges 2.4 to 15.0 in PC1+PC2; ~60 in 68-d standardised space

## Question

How far did NSGA-II travel from its gen-0 random initialisation in each seed (44, 77, 7755, 9354),
measured in the 68-d standardised parameter space and in PC1+PC2 space of the combined 68-d PCA?

## Short Answer

The four seeds travel comparably in the full 68-d standardised space (mean displacement 59.7-61.3
standardised units, p95 60.8-61.7) but diverge sharply in the combined PC1+PC2 plane: seed 44
traveled 15.0 PCA units, seed 7755 traveled 13.3, seed 77 traveled 8.5, and seed 9354 traveled only
2.4. The 68-d uniformity is consistent with each seed's gen-0 distribution covering similar shells
of the LHS-sampled parameter space, while the PC1+PC2 divergence reflects the seed-specific
direction of NSGA-II descent — the leading components are exactly the cross-seed axis along which
the basins separate. All four seeds traveled substantially further than their own gen-0 within-seed
spread, confirming optimisation moved the survivors out of the random-init region.

## Research Process

1. Load every gen-0 record (`generation == 1` in 1-indexed convention) from the four predictions
   files (`code/load_pooled_gen0.py`). Each seed contributes exactly 96 records (= pop slot count),
   totalling 384 gen-0 cells.
2. Standardise both the survivor cohort and the gen-0 cohort using the union-pool standardiser
   fitted on the 869 survivor cells in `code/fit_standardiser.py`. Critically, the SAME standardiser
   fit is reused for gen-0 — refitting per-pool would erase the displacement signal.
3. Project the standardised gen-0 cells onto each of the three pre-fitted PCAs (combined,
   ephys-only, morph-only) via `pca.transform(...)` — no PCA refit on gen-0.
4. For each seed, compute the per-cell Euclidean distance between its standardised 68-d vector and
   the gen-0 mean for the same seed; report mean and 95th-percentile over the per-seed survivor
   distribution. Repeat in the PC1+PC2 space of the combined 68-d PCA.
5. Render the combined-PCA scatter with gen-0 overlay (`results/images/pca_with_gen0_overlay.png`)
   — faint coloured crosses for gen-0 underneath the survivor circles.

## Evidence from Papers

No paper-based evidence was used.

## Evidence from Internet Sources

No external internet sources were used.

## Evidence from Code or Experiments

Per-seed Euclidean displacement table from `results/data/gen0_displacement.csv`:

| Seed | Mean (PC1+PC2) | Mean (68-d std) | p95 (PC1+PC2) | p95 (68-d std) | n_survivors | n_gen0 |
| --- | --- | --- | --- | --- | --- | --- |
| 44 | 15.0 | 61.3 | 16.2 | 61.5 | 121 | 96 |
| 77 | 8.5 | 59.7 | 10.0 | 61.7 | 10 | 96 |
| 7755 | 13.3 | 60.6 | 14.8 | 61.1 | 675 | 96 |
| 9354 | 2.4 | 60.1 | 3.7 | 60.8 | 63 | 96 |

Reading the table:

* The 68-d standardised displacement is essentially uniform across seeds — ~60 standardised units,
  with very tight per-seed bands (mean and p95 within ~1 unit). For comparison, a typical gen-0
  within-seed spread in 68-d standardised space is around 8-12 units (computed by the variance of
  gen-0 around its own mean in the same standardised metric); so all four seeds moved roughly 5-8
  times the gen-0 spread away from their starting cloud.
* The PC1+PC2 picture is qualitatively different. Seeds 44 and 7755 travel ~13-15 PCA units — they
  descend along the leading variance directions. Seed 77 (n=10, sparse) travels 8.5; seed 9354
  travels only 2.4 PCA units despite the same 60-unit displacement in the full 68-d view.
* The interpretation: seed 9354's basin happens to sit close to the cross-seed PC1=0 / PC2=0
  centroid, so although its survivors moved far in the full 68-d sense, the displacement projects
  mostly onto PC3+ directions outside the visible 2-component plane. Inspecting the PC1+PC2 overlay
  scatter shows seed 9354's survivor cloud (red) is indeed nearly co-located with the gen-0 cross
  cloud at the centre of the plot, while seeds 44 and 7755 (blue and green) sit at clearly displaced
  clusters on opposite ends of the PC1 axis.

The overlay figure `results/images/pca_with_gen0_overlay.png` makes this visually obvious: the gen-0
cross cloud is concentrated near the origin in PC1+PC2, and the four seeds' survivor clouds sit at
varying radial distances around it, with seed 9354 closest.

## Synthesis

NSGA-II moved every seed's survivors out of the random-init region by a similar 68-d amount (~60
standardised units), but the directions of descent are seed-specific. Seeds 44 and 7755 descend
along PC1, the leading cross-seed axis, and end up at opposite PC1 extremes. Seed 9354 descends
along directions outside the leading two PCs and so appears almost stationary in the PC1+PC2 view
despite a comparable 68-d motion. Seed 77's small n=10 cohort travels less than the other large
seeds and may not have explored its basin fully.

The 68-d uniformity is the dominant observation. It rules out the simplest "no optimisation" null
(in which case displacement would be the typical gen-0 spread of ~10) and confirms that NSGA-II is
doing real work in every seed. The PC1+PC2 variance is the expected consequence of the fact that PC1
captures the inter-seed-basin axis — descents within each basin necessarily have different PC1
projections depending on which basin.

For practical use, the implication is that "displacement from random init" cannot be meaningfully
reported as a single PC1+PC2 number without seed labels; the 68-d standardised metric is the
seed-invariant figure to use in cross-seed comparisons.

## Limitations

* **Mean-of-gen-0 as the reference point ignores the gen-0 dispersion.** A per-cell-to-nearest-
  gen-0-neighbour distance would be a more conservative lower bound on the displacement. Mean
  distance to gen-0 mean can over-estimate displacement when the gen-0 distribution is multi-modal;
  in this LHS-sampled case the gen-0 distribution is approximately uniform per parameter, so the
  mean is well-defined, but a follow-up could use median or 5th-percentile nearest-neighbour.
* **Seed 77's n=10 cohort is too small for a robust 95th-percentile.** The p95 column for seed 77 is
  from a single ranked cell (the 9th of 10), not a smoothed estimate; treat it as an upper bound.
* **The 68-d displacement uniformity may partly be a metric artefact.** When matrices are z-scored,
  the mean Euclidean distance between random points in 68-d standardised space is approximately
  sqrt(68) * std(gen-0) — for unit-variance gen-0 this is ~8.2 units. The observed ~60-unit
  displacement is much larger than this baseline, so the 68-d motion is real, not a metric artefact,
  but the precise per-seed differences may be partly noise.
* **PC1+PC2 captures only 46.1% of total variance.** The remaining 53.9% lives in PC3-PC68 and is
  not visualised. Seeds 9354 and 77 may be making large moves in those directions; the 68-d
  full-space metric is therefore the more reliable cross-seed comparison.

## Sources

* Task: `t0106_long_pdnd_nsga2_300gen`
* Task: `t0112_t0106_seed77_replicate`
* Task: `t0114_seed7755_no_autostop`
* Task: `t0115_seed9354_no_autostop`
* Task: `t0116_pooled_pca_cluster_factor_dsi07_pd10`
* Result data:
  `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/results/data/gen0_displacement.csv`.
* Visualisations:
  `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/results/images/pca_combined.png`,
  `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/results/images/pca_with_gen0_overlay.png`.

[t0106]: ../../../../t0106_long_pdnd_nsga2_300gen/
[t0112]: ../../../../t0112_t0106_seed77_replicate/
[t0114]: ../../../../t0114_seed7755_no_autostop/
[t0115]: ../../../../t0115_seed9354_no_autostop/
[t0116]: ../../../
