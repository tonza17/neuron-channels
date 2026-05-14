---
spec_version: "1"
task_id: "t0104_nsga2_2obj_dsi_pdrate_3seeds"
date_compared: "2026-05-14"
---
# Comparison with Project and Published Results

## Summary

t0104's 2-objective NSGA-II with the DSI silence guard active produces **0 strict joint-pass cells
across 2,208 evaluated cells**, replicating [t0102]'s 3-objective null at the same substrate. The
DSI extreme cleanly crosses 0.5 for the first time in the t0080-t0104 lineage (seed 55 gen 11, **DSI
= 0.5417**), but the joint-corner remains empirically empty. Compared with
[PolegPolsky2026][polegpolsky2026] the substrate is reachable in principle (the paper claims a
tractable DSI/PD coupling on the de Rosenroll Bed B cell), but at the algorithm budget tried here
NSGA-II cannot find the joint cells. [Mohacsi2024][mohacsi2024] benchmarks NSGA-II as a mid-pack
optimiser on neuron-fitting problems; t0104's null is consistent with their finding that **IBEA,
CMAES, and PSO consistently outperform NSGA-II on six neuron-fitting benchmarks**.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [t0102] 3-obj NSGA-II seed 44+55 (joint-pass yield) | count | 0 | 0 | +0 | t0104 replicates with 2-obj + DSI guard |
| [t0102] 3-obj NSGA-II seed 44 (max DSI, raw) | DSI | 1.000 | 0.4073 | -0.5927 | t0104 silence guard removes DSI = 1.0 artifact (REQ-3) |
| [t0102] 3-obj NSGA-II seed 55 (max DSI, raw) | DSI | 1.000 | 0.5417 | -0.4583 | First non-artifact DSI > 0.5 in t0080-t0104 lineage |
| [t0102] 3-obj NSGA-II seed 44 (max PD) | Hz | 64.29 | 75.00 | +10.71 | Higher PD ceiling at the no-DSI corner |
| [t0102] 3-obj NSGA-II seed 55 (max PD) | Hz | 66.96 | 65.00 | -1.96 | Similar PD ceiling |
| [t0099] 3-obj NSGA-II N=20 (joint-pass yield) | count | 0 | 0 | +0 | Original substrate null; t0104 confirms across noise/objective configs |
| [Mohacsi2024][mohacsi2024] Hay 2011 L5PC NSGA-II yield at 10K evals | strict-pass-rate | 0.40% | 0.00% | -0.40 | Different substrate (22-d L5PC vs 68-d Bed B DSGC); t0104 budget ~4.5x below Mohacsi's matched-budget floor |
| [Dang2023][dang2023] pop floor at n=68 (theoretical mu = n log n) | population | 290 | 96 | -194 | t0104 sits ~3x below the theoretical noise-survival floor |
| [PolegPolsky2026][polegpolsky2026] substrate DSI ceiling (claimed) | DSI | 0.62 (Fig 3) | 0.5417 | -0.0783 | t0104 random-init falls short of the warm-start-achievable ceiling but is the closest random-init reading so far |

## Methodology Differences

* **Objective vector size**: [t0102] used 3-objective `(DSI, PD-rate, robustness)`; t0104 uses
  2-objective `(DSI, PD-rate)`. The robustness field is still computed per cell but does not enter
  NSGA-II selection (REQ-2).
* **DSI silence guard**: [t0102] did not gate the DSI vector-sum formula; t0104 introduces
  `SILENCE_SPIKE_COUNT_THRESHOLD = 10` (REQ-3). 47 of 2,208 t0104 cells (2.1%) sit at the guard
  floor; in [t0102], 27 of 2,592 cells (1.0%) reached the spurious DSI = 1.0 artifact that the guard
  removes.
* **GA seeds**: [t0102] ran 2 seeds (44, 55); t0104 was planned for 3 (44, 55, 66) but the
  researcher stopped after seed 55 (see `intervention/early_stop_after_seed_55.md`). The 2-seed
  result is published.
* **Per-seed budget**: both [t0102] and t0104 set the per-seed watchdog at $4.00. Both tasks tripped
  the watchdog before reaching the planned gen 20.
* **Substrate vs [Mohacsi2024][mohacsi2024]**: Mohacsi benchmarks on Hay 2011 L5PC (22-d, ~16,000
  evaluations per algorithm). t0104 runs on 68-d Bed B DSGC at 2,208 evaluations across 2 seeds —
  ~4.5x below Mohacsi's matched-budget floor and on a 3x higher-dimensional substrate.
* **Algorithm vs [Dang2023][dang2023]**: t0104 pop = 96 is ~3x below the theoretical Dang
  `mu = Omega(n log n)` floor at n = 68 (mu ≈ 290). The Dang noise-survival theorem requires the
  pop floor; t0104's null is consistent with under-population.

## Analysis

The cross-task picture is highly consistent: every random-init NSGA-II configuration tried on the
68-d Bed B + morphology substrate ([t0099], [t0102], t0104 — across noise budgets N = 4 and N =
20, across 2 and 3 objectives, across the silence-guard-on and silence-guard-off settings) produces
**zero strict joint-pass cells**. The t0091 single joint-pass cell observed at the warm-start
setting therefore now reads as warm-start-dependent (its parent was a 5-anchor seed cell at distance
< 1 standard deviation), and **not as a feature of NSGA-II's random-init reach on this substrate at
any of the tried budgets**.

The DSI extreme cleanly above 0.5 in seed 55 gen 11 (**0.5417**) is the most significant t0104 delta
vs [t0102]. Combined with the guard removing the 27-cell silence-corner artifact, t0104 confirms
that the upper-DSI plateau on this substrate is real — but real only at near-silent PD. The DSI vs
PD anti-correlation in the L-shape is structural; flattening it requires either an algorithm that
better explores the interior of the trade-off ([Mohacsi2024][mohacsi2024]'s IBEA recommendation), a
population large enough to satisfy [Dang2023][dang2023]'s noise-survival theorem (mu >= 290 at n =
68), or a substrate change (additional dendritic compartments, GABAergic-asymmetry preservation per
[PolegPolsky2026][polegpolsky2026]'s circuit details).

A useful framing: t0104 closes the "drop the third objective and turn the guard on" branch of the
search space. Two algorithm-side branches remain open as project priorities — IBEA (S-0102-03,
renewed as S-0104-04) and Dang-floor NSGA-II (S-0102-04). One substrate-side branch remains open
(circuit-level GABAergic asymmetry per PolegPolsky2026, deferred).

## Limitations

* **Two seeds only**: variance estimate is under-sampled. The binary answer (0 cells in 2,208) is
  high-confidence, but the per-seed HV variance is enormous (seed 44 climbed steadily, seed 55 made
  a discontinuous jump at gen 8).
* **Watchdog truncation**: both seeds stopped at gens 11-12 of the planned 20. The asymptotic HV is
  unknown. The slope of seed 55 between gens 8 and 11 is too modest to argue a joint-pass cell was
  about to be discovered, but "did not reach gen 20" is weaker than "reached gen 20 and observed
  nothing".
* **PolegPolsky2026 DSI = 0.62 ceiling**: read from Figure 3 of the cached paper summary; the paper
  does not report a single-cell ceiling explicitly, so the 0.62 figure is an upper estimate of the
  warm-start-achievable region rather than a published claim.
* **Dang2023 mu floor at n = 68**: the formula `mu = Omega(n log n)` carries a hidden constant; the
  exact mu floor for n = 68 sits in the range [200, 350] depending on the constant. The 290 figure
  used in the table assumes a constant of ~1.
* **No IBEA comparison run yet**: the strongest single follow-up (S-0104-04) would close the
  algorithm-side reading directly.

[t0091]: ../../../tasks/t0091_morphology_extended_nsga2_v1/
[t0099]: ../../../tasks/t0099_random_init_pareto_robustness/
[t0102]: ../../../tasks/t0102_seedscale_n4_gen20/
[mohacsi2024]: ../../../tasks/t0102_seedscale_n4_gen20/assets/paper/10.1371_journal.pcbi.1012039/summary.md
[dang2023]: ../../../tasks/t0102_seedscale_n4_gen20/assets/paper/10.48550_arXiv.2306.04525/summary.md
[polegpolsky2026]: ../../../tasks/t0024_port_de_rosenroll_2026_dsgc/assets/paper/10.1016_j.celrep.2025.116833/summary.md
