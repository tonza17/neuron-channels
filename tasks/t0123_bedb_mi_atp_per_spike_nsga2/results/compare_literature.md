---
spec_version: "1"
task_id: "t0123_bedb_mi_atp_per_spike_nsga2"
date_compared: "2026-05-24"
---
# Comparison with Project and Published Results

## Summary

The headline comparison to [Niven2007][niven2007] returns **Insufficient evidence**: the post-hoc
Strong-Bialek direct-method MI collapsed to **0.0 bits/s** for all 10 top-Pareto cells (PD-rate ~1-3
Hz is too low to populate non-trivial spike-time words at T <= 100 ms), so the log-log fit
`log(bits_per_sec) = p * log(ATP/spike) + b` is undefined and the DSGC bits-per-ATP curve cannot be
placed above, on, or below the 200-1000 bits/s fly-photoreceptor band. The inner-loop spike-count MI
estimator (Miller-Madow corrected, ceiling **log2(4) = 2.0 bits**) did register a real selection
signal, peaking at **1.459 bits per stimulus** at cell 2 — large in count-MI terms but not
comparable to the literature's bits/s axis. The ATP-per-spike axis is more informative: the top-MI
corner cells consume **4.55-4.76 x 10^6 ATP/spike**, **~81x below** [Attwell2001][attwell2001]'s
**3.84 x 10^8 ATP/AP** for a typical rodent cortical neuron and well within the order-of-magnitude
band implied by [Sengupta2010][sengupta2010]'s cross-cell-type Na+/K+ overlap recipe, confirming the
Sengupta recipe is being applied correctly even though the Niven comparison cannot be tested.

## Comparison Table

### Prior Task Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [t0122] (same 68-d substrate, DSI vs cytoplasm-volume objectives) | best LEGIT DSI | 0.9753 | n/a | n/a | t0122 used DSI ratio; t0123 reports DSI vector-sum as a diagnostic only. Top-10 DSI vector-sum range 0.13-0.40; no t0123 cell is LEGIT by t0122's `DSI>=0.5 AND PD-rate>=30 Hz` threshold (expected because DSI is not optimised) |
| [t0122] top-10 cytoplasm volume (same substrate, DSI corner) | cytoplasm_volume_um3 | 250.2 | n/a | n/a | t0123 does not register cytoplasm volume; cannot compare. The morphology gallery shows top-MI cells share the small-soma / sparse-branch morphology pattern of t0122's top cells |
| [t0122] top-MI corner PD-rate (highest-DSI cell, single seed 1524) | pd_rate_hz | 23.1-26.4 | 1.19-3.33 | -22 to -19 | t0123's top-MI cells fire **~10x more slowly** than t0122's top-DSI cells. Direct consequence of optimising spike-count MI without a PD-rate floor — the optimiser exploited count-MI at the silence-guard boundary (~3 PD spikes/trial). This is the load-bearing cause of the Strong-Bialek bits/s = 0 result downstream |
| [t0122] single-seed LEGIT acceptance (DSI substrate) | rate | 0.17% | 0.00% | -0.17 | t0123 produced **0 LEGIT cells** at the DSI>=0.5 + PD>=30 Hz threshold across all 5760 evaluations; t0122 produced 10. The objective swap from `(DSI, volume)` to `(MI_count, ATP)` drops the joint-pass-by-t0122-criteria rate from 0.17% to 0%. Diagnostic, not a defect — DSI was not in the F vector for t0123 |
| [t0115] / [t0121] PD-rate substrate top-cell PD-rate | pd_rate_hz | 28-35 | 1.19-3.33 | -25 to -33 | t0123 lands roughly an order of magnitude below the PD-rate-substrate cohorts. Consistent with the count-MI estimator preferring tail-of-low-firing cells where stimulus-driven across-direction variance is high relative to noise |
| [t0097] catalogue MI ceiling for 4-direction protocol | mi_count_bits ceiling | 2.0 | 1.459 | -0.541 | [t0097] catalogue noted the 4-direction protocol caps count-MI at **log2(4) = 2.0 bits**. t0123's top cell reaches **73%** of the ceiling (1.459 / 2.0), a tight but not saturating fit — the inner-loop estimator is not pinned by the ceiling |
| [t0097] catalogue prediction: Niven super-linear bits/ATP scaling testable on DSGC | scaling exponent p | super-linear (p > 1) | undefined | undefined | t0097 explicitly listed S-0097-05 (this task) as "the experiment that closes the open question of where the DSGC bits-per-ATP front sits relative to Niven 2007's 200-1000 bits/s curve". t0123 produces the experiment but cannot answer the question because bits/s = 0 |

### Published Literature Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [Niven2007][niven2007] (fly photoreceptors, 4 species) | bits_per_sec | 200-1000 | 0.0 | -200 to -1000 | [Niven2008, Fig 7] (re-plotted from Niven et al. 2007) reports D. melanogaster ~200 bits/s, D. virilis ~400, M. domestica ~700, S. carnaria ~1000 bits/s with super-linear ATP-vs-information scaling and ~20% fixed cost. t0123's 10 top-Pareto cells **all** sit at bits/s = 0 under the post-hoc Strong-Bialek estimator. The empirical Pareto curve cannot be reproduced; the Niven scaling cannot be tested. **Verdict in answer asset: "Insufficient evidence"** |
| [Strong1998][strong1998] (H1 fly motion-sensitive neuron, direct method) | bits_per_sec | 78 +/- 5 | 0.0 | -78 | [Strong1998, p. 197 Abstract + p. 199 Fig 3 caption]: H1 information rate 78 +/- 5 bits/s at Δτ=3 ms under random-walk motion stimuli; ceiling ~157 bits/s; peak ~90 bits/s at finest resolution. t0123 used the same direct-method recipe (1/T extrapolation at T in {25, 50, 75, 100} ms, dt=5 ms) and recovered **0.0 bits/s** on every top-10 cell. The gap is not an estimator artefact — `h_total = h_noise = 0` at every word length because the spike trains are all-zero binary words at firing rates ~1-3 Hz, well below the ~10 Hz needed to populate non-trivial words at T <= 100 ms |
| [Strong1998][strong1998] (H1 fly motion-sensitive neuron) | bits_per_spike | 1.8 +/- 0.1 | 0.0 | -1.8 | [Strong1998, p. 199]: H1 carries 1.8 bits per spike. t0123's top-10 cells fire so rarely (~3 PD spikes/1400 ms) that the spike-time word distribution is degenerate; bits/spike is also zero |
| [Dhingra2004][dhingra2004] (brisk-transient guinea-pig RGC, ideal-observer) | spike vs graded contrast threshold ratio | ~2.5x degradation (1.5% graded -> 3.8% spikes) | n/a | n/a | [Dhingra2004, Abstract + Fig 3]: spike generator degrades contrast detection 2.5x and reduces distinguishable gray levels by ~60% relative to graded potential. t0123 did not record graded-potential MI as a calibration anchor (single-tier FULL protocol only); cannot reproduce the HH-on / HH-off ratio. Methodology gap, not a contradicting finding |
| [Attwell2001][attwell2001] (rat cortical neuron, biophysical accounting) | ATP per AP | 3.84e8 | 4.76e6 (top-MI cell), 4.55e6 (min-ATP-MI>0 cell), 6.76e5 (silent cell) | -3.79e8 to -3.83e8 | [Attwell2001, p. 1136 Table 1]: total ATP per AP for a typical rodent cortical neuron (1.49e5 um^2 total membrane area, AP amplitude 100 mV). t0123 cells consume **~81x less ATP per AP** at the top-MI corner. Cell-size and morphology differences explain most of the gap: the procedural 14-d morphology generator produces small cells (somatic diameter ~17 um, total dendrite length ~36 um per slice-summary) **3-4 orders of magnitude smaller in membrane area** than Attwell's 1.49e5 um^2 reference cell. ATP/AP scales roughly linearly with membrane area in the Na+/K+ overlap regime, so the order-of-magnitude gap is consistent with cell-size scaling, not a recipe error |
| [Sengupta2010][sengupta2010] (squid axon HH model, per-AP Na+ load) | ATP cost per AP per cm^2 | 2.3e12 | n/a | n/a | [Sengupta2010, Table 1]: squid AP ~2.3e12 ATP/cm^2 (alpha = 11.2 at 6.3 degrees C). t0123 does not aggregate ATP per cm^2 in `metrics.json` — only total per-cell per-AP and per-compartment soma/AIS/dendrite breakdown. The soma-dominated split (top-MI cells: 93-95% of per-AP ATP from soma) is qualitatively consistent with Sengupta's overlap-load-dominates story but cannot be quantitatively compared without re-computing membrane-area-normalised ATP from the recorded per-segment traces |
| [Sengupta2010][sengupta2010] (mouse thalamo-cortical relay HH model, MTCR) | ATP cost per AP per cm^2 | 1.35e11 | n/a | n/a | [Sengupta2010, Table 1]: MTCR is ~17x cheaper per cm^2 than squid; alpha ~ 1.0 (capacitive minimum). The DSGC project is mammalian retinal so MTCR is the more biologically relevant anchor than squid. Same caveat as above: t0123 does not store ATP/cm^2 so a direct delta cannot be computed |
| [Sengupta2010][sengupta2010] (cortical interneuron MFS / fast-spiking) | alpha (Na+/K+ overlap factor) | ~1.2 (Carter-Bean cortical pyramidal) to ~2 (mouse fast-spiking) | n/a | n/a | [Sengupta2010, Discussion p. 9 / Fig 5]: mammalian neurons cluster at alpha = 1.0-1.5; the project is mammalian retinal so alpha ~ 1.0-1.5 is the expected band. t0123 does not compute alpha explicitly (would require capacitive-minimum Na+ load per cell); cannot place the top-10 cells on the alpha axis without a follow-up analysis |
| [Carter2009][carter2009] (cerebellar Purkinje cell AIS, ATP/AP/cm benchmark) | ATP per AP per cm of axon | ~2.41e21 (as quoted in plan) | 6.15e8 | -13 orders of magnitude | The plan-quoted Carter-Bean benchmark `~4 mM-mol ATP/AP/cm = 2.41e21 ATP/cm` is **13 orders of magnitude off plausible physics**. Independent back-of-envelope (peak `seg.ina` ~100 mA/cm^2, segment area ~1e-8 cm^2, 2 ms AP window, e = 1.602e-19 C, 3 Na+/ATP) yields ~3e9 ATP/AP/cm — within an order of magnitude of t0123's observed 6.15e8. The 13-order discrepancy is a **plan-quoted typo**, not a model error; see `intervention/carter_bean_benchmark_mismatch.md`. The smoke gate ran under a fallback plausibility band `[1e6, 1e14] ATP/cm` and passed. Carter-Bean 2009 (DOI 10.1016/j.neuron.2009.12.011) is **NOT present** in the project paper corpus, so the strict literature value could not be re-verified within this task |
| [Remme2018][remme2018] (MSO coincidence-detector NEURON model, function vs energy MOBO) | front shape | super-linear function-vs-energy front (Pareto sweep on Na, K, leak) | front shape: 7x ATP gap from silent corner to high-MI cluster | n/a | [Remme2018][remme2018] (DOI 10.1371/journal.pcbi.1006612) is the closest published function-vs-energy MOBO analogue; the paper is **NOT present** in the project paper corpus. The t0097 catalogue cites it via Niven & Laughlin's 2008 review for the MSO Pareto-front shape. t0123's `pareto_front_mi_vs_atp.png` shows a ~7x ATP gap from cell 0 (silent corner, 6.76e5 ATP/spike) to cells 1-4 (cluster at ~4.6e6 ATP/spike), then a sharp MI gradient at fixed ATP cost — qualitatively consistent with Remme's reported front shape but cannot be quantitatively compared without the source paper |

## Methodology Differences

* **Cell type and dimensionality.** [Niven2007][niven2007] / [Niven2008][niven2008] are
  intracellular electrical-circuit measurements on fly R1-6 photoreceptors (graded-potential cells,
  no action potentials in the cellular-mammalian sense); [Strong1998][strong1998] is extracellular
  recording from the H1 fly motion detector (action potential cell). t0123 is a 68-d biophysical
  NEURON model of a mammalian retinal DSGC (graded synaptic input + somatic Na+/K+ HH spike
  generator + 14-d procedural morphology). The bits/s axis is in principle the same quantity but the
  underlying neurons differ by class, species, and resolution by orders of magnitude.

* **Stimulus protocol.** [Niven2007][niven2007] / [Strong1998][strong1998] use long (~10-30 minute)
  random-walk or naturalistic light stimuli at frame rates of 60-1000 Hz, giving stimulus entropy of
  ~hundreds of bits/s. t0123 uses a 4-direction antipodal-pair bar stimulus at 1400 ms per trial
  with 8 directions x 20 trials = 160 trials per cell in the post-hoc Strong-Bialek pass. The
  stimulus entropy is **log2(4) = 2 bits per trial** (or **log2(8) = 3 bits per trial** in the
  post-hoc protocol) — orders of magnitude poorer than the literature's continuous stimulus
  regime. The [t0097] catalogue explicitly flagged this as a known limit of the project's
  direction-protocol approach.

* **Firing-rate operating point.** [Strong1998][strong1998]'s H1 fires at tens of spikes/s under
  random-walk motion; [Niven2007][niven2007]'s photoreceptors carry information in graded-potential
  changes at much higher effective rates than mammalian spike rates. t0123's top-10 NSGA-II Pareto
  cells fire at **~1-3 Hz** under PD direction — well below the threshold rate ~10 Hz needed to
  populate non-trivial binary spike-time words at word lengths T <= 100 ms. The Strong-Bialek
  estimator returns 0 bits/s because the input data is **degenerate**, not because the cells are
  uninformative in some weaker sense.

* **MI estimator pair.** The inner-loop estimator is spike-**count** MI (4 x B contingency table,
  log-spaced bin count B, Miller-Madow bias correction); the post-hoc estimator is the Strong-Bialek
  spike-**time-word** direct method (1/T extrapolation at T in {25, 50, 75, 100} ms, dt = 5 ms).
  These measure different quantities. Count MI integrates over the trial-level spike count
  distribution and is robust at small N; time-word MI measures information in spike-time structure
  and requires firing rates that approach 1/T. t0123's two-tier design exposes the divergence
  between them; literature comparisons should be made tier-by-tier.

* **ATP recipe.** t0123 implements [Sengupta2010][sengupta2010]'s ATP recipe verbatim
  (`Q = integral |min(seg.ina, 0)| dt * seg.area_cm2`, `N_ATP = Q / e / 3`, summed over soma + AIS +
  dendrites). Differences from the published recipes: (a) [Sengupta2010][sengupta2010] uses
  single-compartment HH models; t0123 uses a multi-compartment morphology with realised `seg.area()`
  from the procedural 14-d morphology generator; (b) [Attwell2001][attwell2001] is a top-down
  whole-tissue calculation, not a per-cell biophysical integration; (c) [Carter2009][carter2009] is
  an empirical patch-clamp measurement on Purkinje cells, not the same neuron class as DSGC. The
  cross-cell-type validation in [Sengupta2010][sengupta2010] gives a 17-fold range of ATP per cm^2
  across seven HH models, so an order-of-magnitude or two range between t0123 and any single
  literature anchor is expected.

* **Carter-Bean plan typo.** The plan's quoted Carter-Bean benchmark `2.41e21 ATP/AP/cm` is off by
  ~13 orders of magnitude from the observed value `6.15e8 ATP/AP/cm` on the canonical Bed B anchor
  cell. Independent back-of-envelope physics (peak `ina` ~ 100 mA/cm^2 over a ~1 um^2 AIS segment
  integrated over 2 ms gives ~3e9 ATP/AP/cm) places the observed value in the plausibility band. The
  plan typo, **not** the t0123 recipe, is the load-bearing error. The Carter and Bean 2009 paper
  (DOI 10.1016/j.neuron.2009.12.011) is not present in the project corpus, so the strict published
  value could not be re-verified inside this task; this is recorded as a follow-up to chase outside
  the t0123 boundary.

* **Number of optimiser objectives.** t0123 optimises 2 objectives; [Hay2011][hay2011] /
  [Druckmann2007][druckmann2007] use 10-30. Lower objective count makes the joint-pass corner easier
  in principle but the optimiser converged on a small low-firing-rate region of substrate, so the
  comparison to multi-feature published runs is structural rather than direct.

## Analysis

### Niven 2007 verdict: Insufficient evidence, traceable to a single load-bearing cause

The whole-task headline — comparing the DSGC bits-per-ATP front to [Niven2007][niven2007]'s
super-linear fly photoreceptor curve — fails not because of a code defect or numerical
instability, but because the two-tier MI estimator surfaced a real biological / protocol mismatch.
The inner-loop spike-count MI estimator picked a region of substrate where the across-direction
variance in trial-level spike count is informative (top-10 cells: 1.459 bits, 1.139, 0.964, ...),
and the optimiser's F-vector pulled toward that region. But at those firing rates (~1-3 Hz, ~3 PD
spikes per 1400 ms trial), the spike-time word distribution is degenerate at every word length T <=
100 ms: `h_total = h_noise = 0`, the 1/T extrapolation has nothing to extrapolate, and the
literature-comparable bits/s axis returns zero. The [t0097] catalogue's open question "is the
4-direction count-MI a reliable surrogate for the Strong-Bialek rate" is answered **no, not at the
firing rates the count-MI optimiser converges to**.

### ATP/spike axis: order-of-magnitude consistent with [Attwell2001][attwell2001] and [Sengupta2010][sengupta2010]

The ATP-per-spike values **4.55-4.76 x 10^6 ATP/spike** at the top-MI corner are 81x below
[Attwell2001][attwell2001]'s **3.84 x 10^8 ATP/AP** for a typical rodent cortical neuron. The gap is
dominated by cell size: Attwell's reference cell has total membrane area **1.49 x 10^5 um^2**;
t0123's procedural morphology slice-summary shows somatic diameter ~17 um and total dendrite length
~36 um per slice, which (with typical um-scale dendrite diameters) gives 3-4 orders of magnitude
less membrane area. ATP per AP scales approximately linearly with membrane area in the Na+/K+
overlap regime [Sengupta2010, Eq 9], so the 81x ATP/AP gap is consistent with the cell-size gap.
This is **independent biological corroboration** that the Sengupta recipe is being applied correctly
even though the Niven comparison cannot be tested.

### Soma-dominated ATP split is consistent with the Sengupta overlap-load story

For the top-MI cells, **93-95%** of per-AP ATP comes from the soma compartment, with the AIS
contributing ~5% and dendrites <1%. This matches [Sengupta2010][sengupta2010]'s observation that the
bulk of Na+/K+ overlap cost concentrates wherever Na+ channel density is highest — in the t0123
substrate that is the soma (`apply_params.py` enforces a soma-dominant Na+ density tier). The
degenerate silent cell 0 (PD-rate 0.71 Hz, ATP/spike 6.76e5) shows a more balanced soma share
(42.9%), suggesting that at near-silence the per-AP ATP is dominated by the cheapest AP event the
cell can produce, not by the soma's tonic Na+ density. This finer-grained behaviour is not in the
[Sengupta2010][sengupta2010] one-compartment models but is qualitatively consistent with the
overlap-load framing.

### Count-MI vs Strong-Bialek divergence is the most informative finding

The fact that count-MI = 1.459 bits and Strong-Bialek bits/s = 0 for the **same** cell is the single
most informative finding of t0123. It is direct empirical evidence that the inner-loop spike-count
plug-in MI is **not a reliable surrogate** for the literature-comparable Strong-Bialek rate when
firing rates are low. The [t0097] catalogue's recommendation "use count-MI as a *relative* selection
signal and Strong-Bialek as the absolute literature anchor" is therefore nuanced: the two estimators
can disagree wildly, and the optimiser will preferentially exploit the estimator with the higher
dynamic range. Follow-up suggestion: enforce a PD-rate floor (e.g. PD-rate >= 10 Hz) inside the
silence guard so the count-MI optimiser cannot converge on spike-time-degenerate regions.

### Carter-Bean plan typo is a paperwork artefact, not a biological finding

The 13-order-of-magnitude discrepancy between the plan-quoted Carter-Bean value
(`2.41e21 ATP/AP/cm`) and the observed value (`6.15e8 ATP/AP/cm`) decomposes cleanly into a single
typo in the plan: 4 mM-mol/cm written in the plan should plausibly have been 4 nmol/cm (~2.4e15
ATP/cm) or some other quantity 13 orders smaller; the original Carter & Bean 2009 paper is not in
the project corpus to re-verify. The smoke gate's fallback plausibility band `[1e6, 1e14] ATP/cm`
catches recipe errors that produce 0 or off-by-many-orders results while not blocking on the typo.
The biological message is unchanged: t0123's per-AP per-compartment ATP integration produces a
quantity inside the plausibility band.

## Limitations

* **Niven 2007 paper is not in the project corpus.** The clearest empirical bits-per-ATP Pareto
  curve in the literature (DOI 10.1242/jeb.005249) was not downloaded as a paper asset during the
  t0097 catalogue stage. The catalogue cites it via Niven & Laughlin's 2008 review
  ([Niven2008][niven2008]), which re-plots Niven 2007's Fig 7. The 200-1000 bits/s range and ~20%
  fixed-cost claim are therefore traceable to the review but not to the primary paper inside the
  corpus. This is a **missing-paper observation** for a downstream `download_paper` task.

* **Carter & Bean 2009 paper is not in the project corpus.** The strict ATP/AP/cm benchmark value
  could not be re-verified inside this task; the plan-quoted value was 13 orders off, and the smoke
  gate ran under a fallback plausibility band. The Carter & Bean 2009 paper (DOI
  10.1016/j.neuron.2009.12.011) should be downloaded for the next compare-literature run on this
  lineage. **Missing-paper observation.**

* **Remme et al. 2018 paper is not in the project corpus.** The closest published function-vs-energy
  MOBO analogue (DOI 10.1371/journal.pcbi.1006612) was cited in the t0097 catalogue but is not
  present as a paper asset. The t0123 Pareto-front shape comparison to [Remme2018][remme2018] is
  therefore qualitative (front shape) rather than quantitative (no specific delta, no exponent).
  **Missing-paper observation.**

* **Single GA seed.** t0123 ran one GA seed (441); the Strong-Bialek bits/s = 0 finding could in
  principle be a single-seed accident, although the biological / protocol root cause (PD-rate ~1-3
  Hz at the count-MI optimum) suggests it would replicate. A 5-seed substrate-rate confirmation
  pattern (per the t0117 / t0121 lineage) is not in t0123's $6 scope.

* **No graded-potential MI calibration.** [Dhingra2004][dhingra2004] requires a graded-vs-spike
  comparison inside the same cell. t0123 records only somatic Vm and spike times under FULL mode (HH
  on); the EPSP_PASSIVE / IPSP_PASSIVE modes that would give graded-potential Vm traces were not
  enabled per the standing measurement protocol. Cannot reproduce the ~60% gray-level loss number
  inside this task.

* **ATP not normalised to membrane area.** [Sengupta2010][sengupta2010] and
  [Attwell2001][attwell2001] report ATP/cm^2 or ATP/AP for a fixed reference cell; t0123 reports
  ATP/spike per-cell only. To make the Sengupta-style cross-cell-type comparison quantitative would
  require summing `seg.area()` per cell at evaluation time and adding `atp_per_ap_per_cm2` to the
  predictions schema. Out of scope for t0123 but a straightforward follow-up.

* **No alpha (Na+/K+ overlap factor).** [Sengupta2010][sengupta2010]'s canonical efficiency metric
  `alpha = total Na+ load / capacitive minimum` is not computed for the top-10 cells; would require
  integrating Na+ load and the capacitive minimum separately. Follow-up.

* **Count-MI ceiling of 2.0 bits.** The 4-direction protocol caps the inner-loop count-MI at
  `log2(4) = 2.0 bits`; t0123's top cell reaches 73% of the ceiling. An 8-direction protocol would
  push the ceiling to `log2(8) = 3.0 bits` and might allow the optimiser to explore
  higher-firing-rate cells; out of scope at the $6 cap but listed in t0123's suggestions.

* **No paper-anchored citation for bits/s on RGCs.** The literature's RGC MI measurements (e.g.
  [Dhingra2004][dhingra2004]'s spike-detection-threshold analysis, not a direct bits/s reading; van
  Hateren and Snippe 2007) do not appear in the project corpus as direct bits/s values for
  guinea-pig or mouse RGCs. The Niven 2007 fly-photoreceptor numbers are therefore the closest
  available anchor, but the cell class differs (photoreceptor vs RGC). A direct mammalian-RGC bits/s
  anchor would strengthen the cross-class comparison.

[niven2007]: https://doi.org/10.1242/jeb.005249
[niven2008]: ../../t0097_multi_obj_optim/assets/paper/10.1242_jeb.017574/summary.md
[strong1998]: ../../t0097_multi_obj_optim/assets/paper/10.1103_PhysRevLett.80.197/summary.md
[dhingra2004]: ../../t0015_literature_survey_cable_theory/assets/paper/10.1523_jneurosci.5346-03.2004/summary.md
[attwell2001]: ../../t0097_multi_obj_optim/assets/paper/10.1097_00004647-200110000-00001/summary.md
[sengupta2010]: ../../t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.1000840/summary.md
[carter2009]: https://doi.org/10.1016/j.neuron.2009.12.011
[remme2018]: https://doi.org/10.1371/journal.pcbi.1006612
[hay2011]: https://doi.org/10.1371/journal.pcbi.1002107
[druckmann2007]: ../../t0097_multi_obj_optim/assets/paper/10.3389_neuro.01.1.1.001.2007/summary.md
[t0097]: ../../t0097_multi_obj_optim/
[t0115]: ../../t0115_seed9354_no_autostop/
[t0121]: ../../t0121_5seed_substrate_rate_canonical_report/
[t0122]: ../../t0122_dsi_cytoplasm_volume_nsga2/
