---
spec_version: "1"
task_id: "t0078_bedb_mobo_v2_ais_tiered_ahp"
date_compared: "2026-05-04"
---
# Comparison with Published Results

## Summary

The 49-d AIS-augmented Bed B Pareto front spans DSI **0.007 -> 1.000** across 17 non-dominated cells
with final hypervolume **11.41**, a **+36%** expansion over the t0076 25-d substrate (**8.41**).
Against the literature anchor of paired DSI + mean preferred-direction (PD) firing rate from
`[RivlinEtzion2012, Fig. S2/S3 + Results p. 522]` (**DSI 0.78 +/- 0.19**, **PD rate 10.38 +/- 8.53
Hz**, n = 8 stable cells), the closest Pareto cell at iter 81 (**DSI 0.316**, **PD 9.68 Hz**) sits
at a joint z-score of **(-2.44 on DSI, -0.08 on PD)** -- the PD rate axis is fully within the
published distribution while the DSI axis is **2.4 standard deviations** below the mean. The AIS
Nav1.6 density at the joint-closest cell collapses to the search-space floor (**1e-5 S/cm^2**), four
to six orders of magnitude below the Kole 2008 patch-clamp prior of **0.25-0.5 S/cm^2**
`[Kole2008, p. 178]` and the Werginz 2024 mouse alpha-RGC AIS value of **1.3 S/cm^2**
`[Werginz2024, Table 1]`, indicating the optimiser does not exploit the Kole-prior regime to reach
the joint pass criterion.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| `[RivlinEtzion2012, Fig. S2 + Results p. 522]` mouse ON-OFF DSGC stable cells, n=8 | DSI (3 s grating window) | 0.78 | 0.316 | -0.464 | iter 81 (closest joint cell); z = -2.44 |
| `[RivlinEtzion2012, Fig. S2 + Results p. 522]` mouse ON-OFF DSGC stable cells, n=8 | Mean PD firing rate (Hz, 3 s grating) | 10.38 | 9.68 | -0.70 | iter 81; z = -0.08; within 1 sigma |
| `[deRosenroll2026, Fig. 5]` correlated SAC release | DSI (single-cell substrate baseline) | 0.39 | 0.316 | -0.074 | iter 81; closest Pareto cell to substrate baseline |
| `[deRosenroll2026, Fig. 5]` uncorrelated SAC release | DSI | 0.25 | 0.316 | +0.066 | iter 81 above the uncorrelated-release baseline |
| `[PolegPolsky2016, Results]` mouse DRD4 DSGC | DSI | 0.65 | 1.000 | +0.350 | iter 290 (max-DSI cell) at PD = 0.36 Hz; sub-threshold |
| `[PolegPolsky2016, Results]` mouse DRD4 DSGC | DSI | 0.65 | 0.529 | -0.121 | iter 349 high-DSI rail at PD = 3.25 Hz |
| `[Park2014, Table 1]` mouse CART-Cre On-Off DSGC | DSI | 0.65 | 0.316 | -0.334 | iter 81 (joint-closest); -2.6 sigma on Park2014 SD 0.05 |
| `[Park2014, Table 1]` mouse TRHR-GFP On-Off DSGC | DSI | 0.73 | 0.529 | -0.201 | iter 349; high-DSI rail closest in raw value |
| `[Sivyer2010, Results]` rabbit ON-OFF DSGC ON | DSI | 0.45 | 0.316 | -0.134 | iter 81 |
| `[Sivyer2010, Results]` rabbit ON-OFF DSGC OFF | DSI | 0.50 | 0.529 | +0.029 | iter 349; meets rabbit OFF range |
| `[Oesch2005, Results p. 754]` rabbit ON dendritic-AP DSGC | DSI (peak rates) | 0.67 | 0.756 | +0.086 | iter 380; high-DSI rail at PD = 2.82 Hz |
| `[Oesch2005, Results p. 754]` rabbit OFF dendritic-AP DSGC | DSI (peak rates) | 0.74 | 0.767 | +0.027 | iter 371; high-DSI rail at PD = 1.89 Hz |
| `[Oesch2005, Results p. 754]` rabbit | Modal peak PD rate (Hz, peak not mean) | 148.0 | 197.14 | +49.14 | iter 475 (max-PD cell); sustained mean rate, not modal peak |
| `[Trenholm2013, Results p. 14064]` mouse Hb9 DSGC, control | Peak PD rate (Hz, Gaussian-conv) | 198.0 | 197.14 | -0.86 | iter 475 mean rate matches Trenholm peak rate -- a metric-mismatch coincidence, not a biological match |
| `[Trenholm2013, Results p. 14064]` mouse Hb9 DSGC, control | DSI (peak-rate) | 0.76 | 0.007 | -0.753 | iter 475 has near-zero DSI; saturated high-rate corner |
| `[Werginz2024, Table 1]` mouse alpha-ON-sustained RGC | AIS Nav density (S/cm^2) | 1.3 | 1e-5 | -1.30 | iter 81 collapses Nav at AIS to floor |
| `[Kole2008, p. 178]` cortical pyramidal AIS prior | AIS Nav density (S/cm^2) | 0.25-0.5 | 1e-5 | <= -0.25 | iter 81 |
| `[Werginz2024, Table 1]` mouse alpha-ON-sustained RGC | AIS-to-soma Nav ratio (x) | 17.3 | 5.5e-5 | -17.3 | iter 81: nav16_ais 1e-5 / nav16_soma 0.183 |

### Prior Task Comparison

| Prior Task | Metric | Prior Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| t0076 (25-d Bed B substrate, qNEHVI) | Final hypervolume | 8.41 | 11.41 | +3.00 (+36%) | Reference point of [0, 0]; same DSI x PD axes; +36% Pareto coverage |
| t0076 best-joint cell, iter 424 | DSI at PD ~ 10 Hz | 0.42 | 0.316 | -0.10 | t0076 just cleared **DSI 0.4** at PD 8.34 Hz; t0078 iter 81 misses by 0.084 |
| t0076 best-joint cell, iter 424 | PD rate (Hz) at DSI ~ 0.4 | 8.34 | 9.68 | +1.34 | t0078 reaches 9.68 Hz at DSI 0.316 vs t0076's 8.34 Hz at DSI 0.42 |
| t0024 deRosenroll baseline reproduction | DSI (correlated SAC release) | 0.39 | 0.316 | -0.074 | iter 81 closest cell; substrate regression check (REQ-16) was deferred |

## Methodology Differences

* **DSI definition**: t0078 uses the polar vector-sum DSI = (PD - ND) / (PD + ND) over 8 directions
  with 20 seeds. `[RivlinEtzion2012]` uses a polar-plot vector-sum convention with classification
  threshold DSI > 0.3 (`[RivlinEtzion2012, Methods p. 521]`). `[Trenholm2013]` and `[Oesch2005]`
  compute DSI from **peak** spike rates after Gaussian convolution, not mean rates -- the resulting
  DSI values are 0.05-0.15 higher than mean-rate DSIs from the same cell
  (`[Trenholm2013, Results p. 14068]`).
* **Firing-rate window**: t0078 uses TSTOP_MS = 1400 ms with 8 directions x 20 seeds and reports
  trial-averaged spike rate. `[RivlinEtzion2012]` reports mean rate over a 3 s grating window;
  `[Trenholm2013]` and `[Oesch2005]` report peak instantaneous rate from Gaussian-convolved spike
  trains over sub-second windows. The 9.68 Hz mean PD rate at iter 81 is directly comparable to
  RivlinEtzion's 10.38 Hz, but **not** to Trenholm's 198 Hz peak or Oesch's 148 Hz modal peak.
* **Stimulus**: t0078 uses a 1 mm/s 250 um bar in 8 directions with `parametric_placer.py` AMPA +
  GABA placement. `[RivlinEtzion2012]` uses a drifting square-wave grating; `[Trenholm2013]` uses a
  positive-Weber-contrast bar at 600 um/s; `[Park2014]` uses a moving spot. Cross-method spike-rate
  comparisons inherit the +/- 20-30% variability typical of stimulus-protocol differences.
* **Substrate**: t0078 inherits the Bed B somatic-compartment model from `[deRosenroll2026]` -- same
  morphology, same SAC-release machinery, same 177 ACh + 177 GABA synaptic placement framework.
  `[PolegPolsky2016]` uses a different morphology with passive dendrites (no AIS, no active
  conductances). `[Werginz2024]` uses a 5-tier alpha-RGC morphology (sustained, OFF transient, OFF
  sustained), not a starburst-driven DSGC.
* **Pharmacology**: t0078 simulates control conditions (no GABA-A blockade). `[Trenholm2013]`'s 198
  Hz peak rate is also control; the 244 Hz value is under picrotoxin (GABA-A block) and is not a
  comparable target for t0078.
* **AIS architecture**: t0078 implements a two-subsegment AIS with separate proximal Nav1.6 stand-in
  and distal Nav1.6 + Kv3 + Kv7 SUFFIXes. `[Werginz2024]` uses a single AIS tier; `[Kole 2008]`
  measures a single-compartment cortical pyramidal AIS. The two-subsegment AIS used here is closer
  to the Hu 2009 / Van Wart 2007 division-of-labour model than to either reference's geometry.
* **BO methodology**: `[Ament2023]` qLogNoisyExpectedHypervolumeImprovement is the t0078 acquisition
  function. t0076 used the deprecated qNEHVI from BoTorch < 0.10. Both share the same BoTorch
  SingleTaskGP back-end with `Standardize(m=2)` output transform; t0078 adds `Normalize(d=49)` input
  transform. Hypervolume is computed against the same [0, 0] reference point in both tasks.
* **Slow-AHP mechanism**: t0078 vendors `skahpt78.mod` (SK_E2 from `[Hay2011]` CaDynamics_E2 with a
  `tau_ca_multiplier` PARAMETER scaling decay tau in [1, 20x]). `[Hay2011]` uses cortical L5b
  pyramidal-neuron parameters; the SK_E2 source is `[Khaliq2003]` Purkinje-neuron resurgent-Na + SK
  kinetics. Neither paper reports DSGC-specific tau values; the 20x upper bound is a
  researcher-imposed simulation-budget bound, not a literature ceiling.

## Analysis

The Pareto front confirms a **bimodal** trade-off geometry: the high-DSI rail (DSI 0.5-1.0) lives at
PD rates **<= 4 Hz**, and the high-rate rail (PD >= 30 Hz) lives at DSI **<= 0.06**. The joint
operating point at (DSI 0.4, PD 10 Hz) anchored by `[RivlinEtzion2012]` falls **outside** the
achievable Pareto front, missed by 0.084 on DSI and 0.32 Hz on PD rate at iter 81.

**Joint z-score interpretation.** The Mahalanobis-style joint z-score for iter 81 against the
RivlinEtzion2012 stable-cell distribution `[RivlinEtzion2012, Results p. 522]`:

* DSI z = (0.316 - 0.78) / 0.19 = **-2.44** (well outside +/-1 sigma; only ~0.7% of stable cells in
  `[RivlinEtzion2012]` would have DSI <= 0.316).
* PD-rate z = (9.68 - 10.38) / 8.53 = **-0.08** (within 1 sigma; the iter 81 PD rate is biologically
  plausible).

The result frames the negative finding precisely: t0078's PD rate axis successfully reproduces
biological mean rates, while the DSI axis remains compressed by ~2.4 sigma. The DSI compression is
consistent with the Bed B / Poleg-Polsky 2016 substrate's **passive dendrites** -- DSI > 0.4 in
published mouse DSGCs is computed at peak rates after Gaussian convolution
(`[Trenholm2013, Results p. 14068]`) and / or relies on active dendritic Nav `[Sivyer2013, Results]`
and dendritic spike initiation `[Oesch2005, Results p. 754]`. The augmented substrate added an AIS
but kept dendrites passive; the missing dendritic-spike machinery is the dominant explanation for
the compressed high-rail DSI when measured as trial-averaged DSI from sub-second mean rates.

**Substrate validation.** Iter 81 (DSI 0.316) is the closest Pareto cell to the
`[deRosenroll2026, Fig. 5]` correlated-SAC-release baseline of **DSI 0.39** -- short by 0.074. No
Pareto cell at PD 9.68 Hz reaches the deRosenroll 0.39 DSI value. This is a **substrate
regression**: the augmented 49-d substrate at this PD rate produces lower DSI than the original
deRosenroll baseline reports. The MOBO never sampled the deRosenroll-baseline parameter region (no
deferred substrate-regression check for REQ-16 was run); the regression therefore does not prove the
augmented substrate cannot reproduce DSI 0.39, only that the qLogNEHVI optimiser did not find such a
configuration in 491 cells.

**AIS Nav density anomaly.** Iter 81's `nav16_ais` parameter sits at the search-floor of **1e-5
S/cm^2**, four orders of magnitude below the Kole 2008 patch-clamp prior of **0.25-0.5 S/cm^2**
`[Kole2008, p. 178]` and five orders below Werginz 2024 Table 1's mouse alpha-RGC AIS Nav of **1.3
S/cm^2** `[Werginz2024, Table 1]`. The AIS-to-soma Nav ratio at iter 81 is **5.5e-5**, vs the
Werginz 2024 measured ratio of **17.3** `[Werginz2024, p. 6]`. The optimiser converged on a
configuration where the AIS contributes nothing to spike initiation; the somatic Nav (0.183 S/cm^2
at iter 81) carries the firing. This means the joint-closest cell does not exploit the AIS
biophysics added in t0078, which contradicts REQ-2 / REQ-3 / REQ-4's biological intent. Pareto cells
along the high-rate rail (iter 437, iter 111, iter 437) do saturate `nav16_ais = 1.0 S/cm^2`, but at
the cost of total directional information (DSI < 0.05), suggesting the high AIS Nav regime triggers
depolarisation block on null-direction trials and collapses DSI. The **17 cells x 49 parameters**
Pareto front is sparsely informative about the [0.25, 0.5] S/cm^2 Kole regime: only one cell (iter
290, DSI 1.000) has a `nav16_ais` value inside the Kole prior window (0.0101 S/cm^2 -- still below
the 0.25 lower bound but the closest of the 17 cells).

**Versus Trenholm 2013 peak rates.** The max-PD Pareto cell (iter 475, PD 197.14 Hz) is a
near-perfect numerical match to `[Trenholm2013, Results p. 14064]`'s **198 +/- 14 Hz** control peak
rate. This is a **metric mismatch**, not a biological match: t0078's 197 Hz is a trial-averaged mean
rate from 1400 ms simulation with 8 directions x 20 seeds, while Trenholm 2013's 198 Hz is a
Gaussian-convolved peak instantaneous rate from a sub-second moving-bar burst. A real cell
sustaining 197 Hz mean rate over 1.4 s would be in depolarisation-block regime; iter 475's DSI of
0.007 is consistent with this saturated state. The numerical coincidence reinforces that mean-rate
and peak-rate firing-rate metrics must not be cross-compared.

**Versus PolegPolsky2016 substrate ancestor.** `[PolegPolsky2016, Results]` reports DSI 0.6-0.7 in
passive-dendrite mouse DRD4 DSGCs. Our iter 290 (max DSI = 1.000) and iter 283 (DSI 0.939) cells
**exceed** this published range by +0.30 to +0.40, but these cells fire at PD rates of 0.36-1.14 Hz
-- subthreshold trains, far from the 5-15 Hz mean-rate regime of real DSGCs. The Pareto-rail cell at
iter 349 (DSI 0.529, PD 3.25 Hz) sits within the PolegPolsky 2016 published range but at a
sub-physiological PD rate. The augmented substrate matches PolegPolsky 2016's DSI when the firing
rate is allowed to approach zero, consistent with the original Poleg-Polsky observation that passive
dendritic propagation can produce high DSI when spike thresholds are tuned for very low base firing.

**Versus rabbit DSGC range.** `[Sivyer2010, Results]` ON-OFF rabbit DSI of **0.45 (ON)** and **0.50
(OFF)** is matched by iter 349 (DSI 0.529) at PD 3.25 Hz. `[Oesch2005, Results p. 754]` peak-rate
DSI of **0.67 (ON)** / **0.74 (OFF)** is matched by iter 380 (DSI 0.756) and iter 371 (DSI 0.767) at
PD 1.89-2.82 Hz. None of these matches occur at biologically plausible PD rates (>= 5 Hz) -- the
augmented substrate reproduces published rabbit DSI **only** in the sub-threshold regime.

**Hypervolume vs t0076.** The +36% HV improvement (8.41 -> 11.41) confirms the architectural
additions in REQ-2 through REQ-6 (AIS section, 5-tier channels, slow-AHP) **do** expand the
achievable Pareto front. However, the HV gain is bounded by the same dendritic-passive constraint --
the high-DSI rail's PD ceiling moved from t0076's ~3 Hz to t0078's 2.82 Hz (no measurable change).
The HV growth came mainly from the high-rate rail extending from t0076's 128 Hz to t0078's 197 Hz,
capped by the slow-AHP. The augmented substrate **expands the rate axis but does not break the
rate-DSI trade-off** at the joint operating point.

## Limitations

* **Substrate regression check (REQ-16) deferred**: The t0076 iter-424 parameter vector was not
  re-evaluated on the 49-d t0078 substrate, so the apparent DSI regression at iter 81 (0.316 vs
  t0076 iter 424's 0.42) cannot be attributed solely to the substrate -- it may also reflect the
  increased acquisition-function exploration cost in 49-d vs 25-d space within the same evaluation
  budget.
* **Mean rate vs peak rate**: The published `[Trenholm2013]` and `[Oesch2005]` values are peak
  Gaussian-convolved instantaneous rates, while t0078 reports trial-averaged mean rates over 1400
  ms. The +49 Hz delta against `[Oesch2005, Results p. 754]`'s 148 Hz modal peak is a metric
  mismatch, not a biological mismatch. The only **directly-comparable** firing-rate reference in the
  corpus is `[RivlinEtzion2012]`'s 3 s-window mean rate.
* **DSI definitions vary**: `[Trenholm2013]`'s peak-rate DSI is structurally higher than the
  trial-averaged spike-count DSI used in t0078. Cross-paper DSI comparisons inherit this systematic
  difference of +0.05 to +0.15.
* **Werginz 2020 and Van Wart 2007 paper PDFs not in corpus**: The AIS Nav density priors used in
  t0078 (Kole 2008's 0.25-0.5 S/cm^2) come from the cortical pyramidal literature, not the RGC
  literature. The Werginz 2020 RGC measurement of the AIS-to-soma Na density ratio (~7x) is in the
  metadata but the paper PDF is paywalled. This propagates to incomplete prior validation: only
  `[Werginz2024, Table 1]`'s mouse alpha-RGC values (1.3 S/cm^2 AIS Nav) are fully characterised in
  the corpus.
* **Single MOBO run**: t0078 has one Sobol DoE seed and one BoTorch chain. The +36% HV improvement
  over t0076 is a single-replicate observation; the Pareto-front structure (17 cells, bimodal
  trade-off) may shift with a different RNG seed. No HV uncertainty estimate is reported.
* **BO loop early-stopped at 416/700 acquisitions**: The remaining 284 acquisitions might have
  located a Pareto cell crossing the joint pass criterion. The HV trajectory had plateaued at 11.41
  (90% of the 1.5x rule-out threshold of 12.62), but a cell sitting just above (DSI 0.4, PD 10 Hz)
  was not categorically ruled out.
* **No paired DSI + mean PD-rate measurements other than RivlinEtzion 2012**: The literature anchor
  at (DSI 0.78, 10.38 Hz) is from a single n = 8 sample. No other paper in the project corpus
  reports paired joint DSI + mean PD-rate values; the t0078 pass criterion of (0.4, 10) is therefore
  anchored to a single small-sample reference.
* **`[Park2014]`'s SD of 0.05 is unrealistically small**: The reported DSI 0.65 +/- 0.05 SD yields a
  z-score of -7.0 against iter 81, which is implausible for a biological measurement. The SD likely
  reflects within-cell-type homogeneity in the CART-Cre transgenic line, not the full DSGC
  population; the iter-81 DSI is therefore better compared to `[RivlinEtzion2012]`'s larger SD of
  0.19.
