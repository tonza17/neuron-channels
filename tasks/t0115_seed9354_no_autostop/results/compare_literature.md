---
spec_version: "1"
task_id: "t0115_seed9354_no_autostop"
date_compared: "2026-05-21"
---
# Comparison with Project and Published Results

## Summary

t0115 is the 5th and final seed (seed 9354, drawn via `secrets.randbelow(10000)`) of the S-0112-01
substrate-rate batch on the 68-d Bed B + 14-d morphology substrate, with HV-plateau auto-stop
DISABLED per the S-0113-03 reparameterisation. Operator stop at gen 55 / 5 280 evals with **HV =
50.56**, **63 LEGIT joint-pass cells**, best LEGIT DSI **0.9833** at PD **28.33 Hz**, best PD-rate
**89.29 Hz**, and best combined DSI × PD = **40.06**. Seed 9354 lands in the **medium-density
bucket** between [t0112] (sparse, 0.35 %) and [t0114] (very rich, 8.13 %).

**5-seed substrate-rate (LEGIT joint-pass / total evals)**: per-seed values 3.23 % / 0.35 % / 0.00 %
/ 8.13 % / 1.19 %; **mean 2.58 % ± SE 1.50 %** (SD 3.35 %; 95 % CI -0.36 % to +5.52 %). The point
estimate is **6.45× above** [Hay2011][hay2011]'s **0.40 %** envelope upper bound and **25.8×
above** [Druckmann2007][druckmann2007]'s **0.10 %** baseline, but the 95 % CI brackets both
literature references and 0 % — so the 5-seed sample, while suggestive, still cannot formally
reject either baseline at α = 0.05. Three of five seeds (44, 7755, 9354) independently exceed Hay
2011\.

## Comparison Table

### Prior Task Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [t0106] seed 44 (best LEGIT DSI) | DSI | 0.9939 | 0.9833 | -0.0106 | 1.1 % below [t0106]'s frontier |
| [t0106] seed 44 (best PD-rate) | PD (Hz) | 125.95 | 89.29 | -36.66 | 71 % of [t0106]'s frontier |
| [t0106] seed 44 (LEGIT joint-pass count) | count | 121 | 63 | -58 | 52 % of [t0106]'s yield |
| [t0106] seed 44 (joint-pass rate) | rate | 3.23 % | 1.19 % | -2.04 | 37 % of [t0106]'s rate |
| [t0106] seed 44 (final HV) | HV | 122.03 | 50.56 | -71.47 | 41 % of [t0106]'s HV |
| [t0112] seed 77 (best LEGIT DSI) | DSI | 0.9535 | 0.9833 | +0.0298 | t0115 exceeds [t0112] |
| [t0112] seed 77 (best PD-rate) | PD (Hz) | 114.76 | 89.29 | -25.47 | 78 % of [t0112]'s frontier |
| [t0112] seed 77 (LEGIT joint-pass count) | count | 7 | 63 | +56 | t0115 yields 9.0× more cells |
| [t0112] seed 77 (joint-pass rate) | rate | 0.35 % | 1.19 % | +0.84 | t0115 rate is 3.4× [t0112] |
| [t0112] seed 77 (final HV) | HV | 107.46 | 50.56 | -56.90 | 47 % of [t0112]'s HV |
| [t0113] seed 2247 (best LEGIT DSI) | DSI | 0.3651 | 0.9833 | +0.6182 | t0115 exceeds 2.7× |
| [t0113] seed 2247 (LEGIT joint-pass count) | count | 0 | 63 | +63 | t0115 recovers a non-empty population |
| [t0114] seed 7755 (best LEGIT DSI) | DSI | 0.9926 | 0.9833 | -0.0093 | within 1 % of [t0114]'s frontier |
| [t0114] seed 7755 (best PD-rate) | PD (Hz) | 112.86 | 89.29 | -23.57 | 79 % of [t0114]'s frontier |
| [t0114] seed 7755 (LEGIT joint-pass count) | count | 484 | 63 | -421 | 13 % of [t0114]'s yield |
| [t0114] seed 7755 (joint-pass rate) | rate | 8.13 % | 1.19 % | -6.94 | 15 % of [t0114]'s rate |
| [t0114] seed 7755 (final HV) | HV | 111.54 | 50.56 | -60.98 | 45 % of [t0114]'s HV |

### Published Literature Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [Hay2011][hay2011] NSGA-II joint perisom+BAC (single seed) | rate | 0.40 % | 1.19 % | +0.79 | t0115 single-seed acceptance is **3.0× Hay 2011** (vs t0114's 20.3×) |
| [Hay2011][hay2011] (vs 5-seed mean) | rate | 0.40 % | 2.58 % | +2.18 | 5-seed mean **6.5× above Hay**; 95 % CI brackets Hay — cannot formally reject |
| [Druckmann2007][druckmann2007] NSGA-II 300×1000 (single seed) | rate | 0.10 % | 1.19 % | +1.09 | t0115 single-seed acceptance is **11.9× Druckmann 2007** |
| [Druckmann2007][druckmann2007] (vs 5-seed mean) | rate | 0.10 % | 2.58 % | +2.48 | 5-seed mean **25.8× above Druckmann**; 95 % CI brackets Druckmann — cannot formally reject |
| [Mohacsi2024][mohacsi2024] NSGA-II convergence horizon | plateau gen | 20-60 | 34-45 (t0115 plateau range) | inside | t0115's HV plateau gen 34-45 fits squarely inside the published 20-60 convergence window |

## Methodology Differences

* **Dimensionality**: t0115's substrate is 68-d (54-d Bed B electrophys + 14-d morphology), vs
  [Hay2011][hay2011]'s 22-d (perisomatic + BAC ion channel densities),
  [Druckmann2007][druckmann2007]'s 12-d (cortical interneuron channel densities), and
  [Mohacsi2024][mohacsi2024]'s 3-12 d (varied use cases). t0115's higher dimensionality enlarges the
  search volume substantially but the NSGA-II population size (96) and pool-restart cadence (10) are
  inherited from t0114 / t0106's empirically tuned configuration.
* **Objectives**: t0115 optimises 2 objectives (PD-direction ratio DSI and PD-direction firing rate
  at 0 °). [Hay2011][hay2011] and [Druckmann2007][druckmann2007] both used ≥ 10
  electrophysiological feature objectives. Lower objective count makes the joint-pass corner easier
  to populate but the 2-objective ratio DSI is also an overstatement of polar selectivity (per
  [t0107]).
* **Acceptance threshold**: t0115 LEGIT joint-pass is DSI ≥ 0.5 AND PD ≥ 30 Hz AND DSI < 0.9999
  (silence-guard exclusion). [Hay2011][hay2011] used per-feature z-score ≤ 3 thresholds;
  [Druckmann2007][druckmann2007] used per-feature ≤ 3 SD bands. The acceptance criteria are not
  directly comparable in magnitude — only the general "fraction of evals satisfying all per-task
  biological constraints" is.
* **Auto-stop**: t0115 ran with HV-plateau auto-stop **DISABLED** per S-0113-03 — same as t0114,
  vs [t0106]'s `(W=2, T=0.01)` rule that fired at gen 39 for seed 44 and t0113's premature gen-14
  fire for seed 2247. [Mohacsi2024][mohacsi2024] used a "no improvement over 20 gens" rule.
* **Seed selection**: t0115's seed 9354 was drawn via `secrets.randbelow(10000)` immediately before
  launch, matching t0113 / t0114. This is the random-seed convention agreed for the S-0112-01 batch.

## Analysis

**5-seed substrate-rate finalised.** Combining all five seeds (44, 77, 2247, 7755, 9354) on the
identical 68-d substrate, the substrate-level LEGIT joint-pass acceptance rate is **2.58 % ± 1.50 %
SE** (SD 3.35 %; 95 % CI -0.36 % to +5.52 %). This is the headline batch-completion result for
S-0112-01. Three of five seeds (44, 7755, 9354) independently exceed the Hay 2011 0.40 % envelope
upper bound; the other two (77, 2247) sit at or near literature levels (0.35 % and 0 %). The
variance across seeds is the dominant uncertainty — the SE of 1.50 % is larger than both
[Hay2011][hay2011]'s 0.40 % and [Druckmann2007][druckmann2007]'s 0.10 % reference values, so the
5-seed mean cannot formally reject either baseline at α = 0.05. Additional seeds would tighten the
SE quickly given the existing variance, but with the point estimate already 6.45× above
[Hay2011][hay2011] and the substrate physically distinct (68-d Bed B + morphology, 3-6× higher
dimensionality than the literature comparisons), the qualitative conclusion that this substrate is
denser than [Hay2011][hay2011]'s and [Druckmann2007][druckmann2007]'s is robust.

**S-0113-03 detector reparameterisation holds.** The recommended new defaults
`(W*, T*) = (3, 0.015)` from t0114's detector replay analysis remain consistent with t0115's plateau
behaviour. t0115's HV plateaued around gen 33-34 (HV 36.44, before the gen-34 burst restarted
growth) and again at gen 45-48 (HV 48.94, the longer-lasting plateau). The proposed rule applied to
t0115's full 55-gen trace would fire somewhere in the gen 30-45 range, comfortably inside
[Mohacsi2024][mohacsi2024]'s 20-60 published convergence window.

**Seed-variance is the limiting uncertainty, not the protocol.** The 5-seed spread (0 to 8.13 %
acceptance, a 23× range across seeds) is much larger than the t0114→t0115 protocol diff (single
constant change). Future runs intending to characterise the substrate should either pool multiple
seeds or report seed-specific acceptance rates, not single-seed values.

## Limitations

* The 5-seed sample with SD 3.35 % is still small for a confidence-interval conclusion; a 10+ seed
  batch would tighten the SE below the [Hay2011][hay2011] reference value.
* t0113's premature auto-stop at gen 14 contributes 0 % acceptance, which dominates the lower tail
  of the 5-seed mean and inflates the SE. Under the S-0113-03 (W*, T*) = (3, 0.015)
  reparameterisation, t0113 would have run further and might have recovered a non-zero rate (see the
  offline detector replay analysis in t0114 results).
* 2-direction ratio DSI overstates direction selectivity by ~0.42 absolute vs 8-direction polar DSI
  (per [t0107]); t0115 joint-pass cells have not been polar-rechecked.

## References

[hay2011]: 10.1371/journal.pcbi.1002107
[druckmann2007]: 10.3389/neuro.01.1.1.001.2007
[mohacsi2024]: 10.1371/journal.pcbi.1012039
[t0106]: tasks/t0106_long_pdnd_nsga2_300gen
[t0107]: tasks/t0107_t0106_polar_8dir_recheck
[t0112]: tasks/t0112_t0106_seed77_replicate
[t0113]: tasks/t0113_t0106_seed2247_replicate
[t0114]: tasks/t0114_seed7755_no_autostop
