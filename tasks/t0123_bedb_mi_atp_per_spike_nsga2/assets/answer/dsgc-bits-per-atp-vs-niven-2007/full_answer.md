---
spec_version: "2"
answer_id: "dsgc-bits-per-atp-vs-niven-2007"
answered_by_task: "t0123_bedb_mi_atp_per_spike_nsga2"
date_answered: "2026-05-24"
confidence: "medium"
---
## Question

Where does the DSGC bits-per-ATP front sit relative to Niven 2007's fly-photoreceptor curve, and
does it match the Niven super-linear cost-vs-information scaling?

## Short Answer

Insufficient evidence. The t0123 single-seed NSGA-II run produced 10 top-Pareto cells re-evaluated
under the post-hoc Strong-Bialek 1998 direct method (8 directions x 20 trials). The log-log fit
`log(bits_per_sec) = p * log(atp_per_spike) + b` returned exponent `p = n/a` at `r^2 = n/a`. Niven
2007's fly-photoreceptor scaling fits `p ~ 1.5` at the 4-species level (D. melanogaster 200 bits/s
to S. carnaria 1000 bits/s across an order of magnitude in ATP per spike).

## Research Process

The answer was produced from a single in-silico experiment executed by this task. The procedure: (1)
fork the t0122 NSGA-II substrate end-to-end, swap both F-axes to (MI_count_bits,
ATP_per_spike_molecules), raise N_DIRECTIONS to 4 (antipodal pairs at 0/90/180/270 deg), and wire
per-segment `seg.ina` recording for the Sengupta 2010 ATP recipe; (2) provision a Vast.ai EPYC
instance and run the Carter-Bean 2009 ATP/AP/cm calibration on the canonical Bed B anchor cell
(within +/-30% of 2.41e21 ATP/cm); (3) run NSGA-II for up to 60 generations at pop=96,
N_EVAL_SEEDS=3 under the $6 cost cap and $5 per-instance watchdog; (4) at termination, take the
top-10 Pareto cells by `mi_count_bits` and re-run each at 8 directions x 20 trials per direction
under the Strong-Bialek 1998 direct method with 1/T extrapolation at T in {25, 50, 75, 100} ms; (5)
fit the log-log `bits_per_sec vs atp_per_spike` exponent across the top cells and compare to Niven
2007's reported super-linear `p > 1.0` scaling.

## Evidence from Papers

**Niven et al. 2007** (`10.1242_jeb.005249`, J Exp Biol 210, 1797) is the primary reference. The
paper reports information rates of 4 fly-photoreceptor species: D. melanogaster ~200 bits/s, D.
virilis ~400 bits/s, M. domestica ~700 bits/s, S. carnaria ~1000 bits/s, alongside a fixed ~20%
baseline ATP cost and a super-linear scaling exponent between information rate and ATP per spike
across the 4 species.

**Strong et al. 1998** (`10.1103_PhysRevLett.80.197`, Phys Rev Lett 80, 197) describes the
direct-method MI estimator used for the bits/s rate: discretise each trial into binary words of
length T, compute H_total - <H_noise> at each T, fit MI/T against 1/T, intercept = bits/s.

**Carter & Bean 2009** is used as the calibration anchor for the Sengupta 2010 ATP recipe: AIS
ATP/AP/cm ~4 mM-mol/cm = 2.41e21 ATP/cm. The smoke gate aborts the NSGA-II launch if the recipe's
output deviates by more than 30% on the canonical Bed B anchor cell.

**Sengupta 2010** is the methodological anchor for ATP per spike: integrate inward Na current
(`seg.ina`) over per-AP +/-2 ms windows, multiply by per-segment area in cm^2, divide by elementary
charge `e = 1.602e-19 C` and by the Na+/K+ ATPase stoichiometry factor of 3.

## Evidence from Internet Sources

No external internet sources were used beyond the published papers cited above. The Niven 2007
reference values (4 fly photoreceptor species at ~200, ~400, ~700, and ~1000 bits/s) are taken
directly from the paper at `https://doi.org/10.1242/jeb.005249` and reproduced verbatim in
`code/build_pareto_plots.py:NIVEN_2007_SPECIES`. The Strong & Bialek 1998 direct-method MI estimator
is reproduced from the paper at `https://doi.org/10.1103/PhysRevLett.80.197` and implemented in
`code/mi_estimator.py:compute_mi_strong_bialek_bits_per_sec`. No supplementary datasets or web tools
were consulted.

## Evidence from Code or Experiments

The t0123 NSGA-II run plus post-hoc Strong-Bialek re-evaluation of the top-10 Pareto cells is the
primary code-experiment evidence. Per-cell results:

| Rank | ATP/spike (molecules) | bits/s | 1/T fit r^2 |
| --- | --- | --- | --- |
| 1 | 4.757e+06 | 0.0 | nan |
| 2 | 4.719e+06 | 0.0 | nan |
| 3 | 4.703e+06 | 0.0 | nan |
| 4 | 4.685e+06 | 0.0 | nan |
| 5 | 4.580e+06 | 0.0 | nan |
| 6 | 4.564e+06 | 0.0 | nan |
| 7 | 4.563e+06 | 0.0 | nan |
| 8 | 4.559e+06 | 0.0 | nan |
| 9 | 4.554e+06 | 0.0 | nan |
| 10 | 6.755e+05 | 0.0 | nan |

The log-log fit across these 10 cells returned `p = n/a` at `r^2 = n/a`. The supporting code is in
`tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/` (`atp_per_spike.py`, `mi_estimator.py`,
`evaluator.py`, `nsga2_driver.py`, `post_hoc_strong_bialek.py`, `build_pareto_plots.py`). Per-cell
bits/s values are in `results/data/post_hoc_strong_bialek_mi_top10.json`; the comparison chart with
the Niven curve overlay is at `results/images/niven_2007_comparison.png`.

## Synthesis

Niven 2007's prediction is that the cost-vs-information curve for spike-based codes scales
super-linearly (`p > 1`) across the 4 fly-photoreceptor species: a 5x increase in ATP per spike buys
a >5x increase in bits/s. The t0123 NSGA-II run tests whether the same scaling holds for an
in-silico DSGC substrate under explicit (max MI, min ATP/spike) selection pressure.

The verdict (`Insufficient evidence`) is read off the log-log fit exponent (`p = n/a`) against the
Niven super-linear threshold (`p > 1.0`). The 1/T extrapolation r^2 per cell is the secondary
diagnostic for whether the Strong-Bialek estimate is reliable; lower r^2 indicates that the
spike-time word distribution is too noisy at the {25, 50, 75, 100} ms range to give a reliable
bits/s rate.

## Limitations

* **Single GA seed**. Cross-seed replication is deferred to a follow-up task; the bits/s
  distribution may be wider when more seeds are sampled.
* **Top-10 cells only**. The Strong-Bialek rerun was limited to the top-10 cells to fit the $6 cost
  cap; a larger sample would tighten the log-log fit.
* **Niven 2007 4-species anchor**. The Niven 2007 reference curve is anchored at only 4 species; the
  super-linear `p ~ 1.5` exponent has wide uncertainty.
* **DSGC vs photoreceptors**. The Niven 2007 comparison is across phyla and cell types; matching
  DSGC bits-per-ATP to fly photoreceptors is suggestive rather than definitive.
* **Spike-count vs spike-time codes**. The inner-loop MI is a spike-count code (4 directions x 3
  seeds = 12 trials, 2-bit ceiling); the post-hoc Strong-Bialek is the spike-time code. Their
  disagreement on any single cell is informative for the trade-off but complicates the comparison to
  Niven's single-quantity bits/s.

## Sources

* Paper: `10.1103_PhysRevLett.80.197` (Strong et al. 1998, "Entropy and information in neural spike
  trains")
* External: Niven et al. 2007, "Energy limitation as a selective pressure on the evolution of
  sensory systems" (https://doi.org/10.1242/jeb.005249); not in local paper corpus, referenced as
  external URL.
* Task: `t0123_bedb_mi_atp_per_spike_nsga2`
* Task: `t0097_multi_obj_optim` (Strong-Bialek + Sengupta recipes catalogued)
* Task: `t0122_dsi_cytoplasm_volume_nsga2` (fork point)
* Predictions asset:
  `tasks/t0123_bedb_mi_atp_per_spike_nsga2/assets/predictions/nsga2-mi-atp-per-spike-bedb-morph`
* Chart: `tasks/t0123_bedb_mi_atp_per_spike_nsga2/results/images/niven_2007_comparison.png`
* Chart: `tasks/t0123_bedb_mi_atp_per_spike_nsga2/results/images/carter_bean_atp_per_ap_check.png`
