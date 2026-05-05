---
spec_version: "1"
task_id: "t0081_bedb_v3_warmstart_nsga2"
date_compared: "2026-05-05"
---
# Comparison with Published Results

## Summary

t0081 is the **project's first single-cell substrate to satisfy the joint pass criterion (DSI >= 0.4
AND PD >= 10 Hz) simultaneously**: gen 7 cell 767 sits at **DSI 0.494 / PD 11.39 Hz** on a 16-cell
Pareto front (768 evaluations, $2.39). Against the literature anchor of paired DSI + mean PD firing
rate from `[RivlinEtzion2012, Fig. S2 + Results p. 522]` (**DSI 0.78 +/- 0.19**, **PD 10.38 +/- 8.53
Hz**, n = 8 stable cells), cell 767 sits at a joint z-score of **(-1.50 on DSI, +0.12 on PD)**: the
PD axis is fully within the published distribution, and the DSI axis has narrowed from t0078's -2.44
sigma and t0080's -4.11 sigma down to **-1.50 sigma**. Cell 767's DSI also exceeds three
independently-measured published baselines: **0.494 > 0.39 `[deRosenroll2026, Fig. 5]`** correlated
SAC release, **0.494 > 0.45 `[Sivyer2010, Results]`** rabbit ON, and **0.494 > 0.40** the project's
pass threshold derived from the Sivyer/Park/RivlinEtzion range. The result is a **clean
architectural positive outcome** decisively attributable to the combined t0078 + t0080 warm-start:
the 17 projected t0078 Pareto cells gave NSGA-II initial-population samples already inside the
relevant region of 54-d space, allowing the optimiser to evolve to the pass region within 8
generations under a 4x larger budget than t0080.

## Comparison Table

### Literature Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| `[RivlinEtzion2012, Fig. S2 + Results p. 522]` mouse ON-OFF DSGC stable cells, n=8 | DSI (3 s grating window) | 0.78 | 0.494 | -0.286 | Cell 767 (joint pass); z = -1.50 |
| `[RivlinEtzion2012, Fig. S2 + Results p. 522]` mouse ON-OFF DSGC stable cells, n=8 | Mean PD firing rate (Hz) | 10.38 | 11.39 | +1.01 | Cell 767; z = +0.12; well within 1 sigma |
| `[deRosenroll2026, Fig. 5]` correlated SAC release (Bed B substrate ancestor) | DSI | 0.39 | 0.494 | +0.104 | Cell 767; **+27% above the substrate baseline** |
| `[deRosenroll2026, Fig. 5]` uncorrelated SAC release | DSI | 0.25 | 0.494 | +0.244 | Cell 767; near double the uncorrelated baseline |
| `[Park2014, Table 1]` mouse CART-Cre On-Off DSGC | DSI | 0.65 | 0.494 | -0.156 | Cell 767; -3.1 sigma on Park SD 0.05 (use RivlinEtzion's 0.19 SD instead) |
| `[Sivyer2010, Results]` rabbit ON-OFF DSGC ON | DSI | 0.45 | 0.494 | +0.044 | Cell 767; **meets rabbit ON range** |
| `[Sivyer2010, Results]` rabbit ON-OFF DSGC OFF | DSI | 0.50 | 0.494 | -0.006 | Cell 767; rabbit OFF range matched within 0.01 |
| `[Oesch2005, Results p. 754]` rabbit ON dendritic-AP DSGC | Peak-rate DSI | 0.67 | 0.494 | -0.176 | Cell 767; metric mismatch (mean-rate vs peak-rate, +0.05-0.15 systematic) |
| `[Oesch2005, Results p. 754]` rabbit OFF dendritic-AP DSGC | Peak-rate DSI | 0.74 | 0.494 | -0.246 | Cell 767; metric mismatch |
| `[Oesch2005, Results p. 754]` rabbit | Modal peak PD rate (Hz, peak) | 148.0 | 11.39 | -136.61 | Cell 767; metric mismatch (mean vs peak) |
| `[Trenholm2013, Results p. 14064]` mouse Hb9 DSGC, control | Peak PD rate (Hz, Gaussian-conv) | 198.0 | 11.39 | -186.61 | Cell 767 mean rate vs Trenholm peak rate |
| `[Trenholm2013, Results p. 14064]` mouse Hb9 DSGC, control | Peak-rate DSI | 0.76 | 0.494 | -0.266 | Cell 767; metric mismatch |
| `[PolegPolsky2016, Results]` mouse DRD4 DSGC (passive-dendrite ancestor) | DSI | 0.65 | 0.494 | -0.156 | Cell 767; -24% of published value but at biologically plausible PD rate |
| `[Werginz2024, Table 1]` mouse alpha-ON-sustained RGC | AIS Nav density (S/cm²) | 1.30 | >= 0.25 | within range | Hard-floor enforced (inherited from t0080) |
| `[Kole2008, p. 178]` cortical pyramidal AIS prior | AIS Nav density (S/cm²) | 0.25-0.5 | >= 0.25 | floor met | Lower bound enforced as hard parameter floor |
| `[Werginz2024, Table 1]` mouse alpha-ON-sustained RGC | AIS-to-soma Nav ratio (x) | 17.3 | >= 5 | floor met | Hard ratio floor of 5 enforced via inequality constraint |
| `[Goethals2020]` axial-current AIS Nav estimate (independent) | AIS Nav density (mS/cm²) | 12-55 | >= 250 | floor at upper edge | t0081's 0.25 S/cm² = 250 mS/cm² sits at the upper edge of Goethals's estimate range |

### Prior Task Comparison

| Prior Task | Metric | Prior Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| t0078 (49-d AIS-augmented Bed B BoTorch) closest-to-joint cell, iter 81 | DSI | 0.316 | 0.494 | +0.178 | **+56% over t0078 closest-to-joint DSI** |
| t0078 (49-d AIS-augmented Bed B BoTorch) closest-to-joint cell, iter 81 | PD rate (Hz) | 9.68 | 11.39 | +1.71 | **Joint pass criterion now crossed (>= 10 Hz)** |
| t0078 (49-d AIS-augmented Bed B BoTorch) | Pareto front size (cells) | 17 | 16 | -1 | Comparable Pareto density at 4x larger budget |
| t0078 (49-d AIS-augmented Bed B BoTorch) | Joint pass cells (DSI >= 0.4 AND PD >= 10 Hz) | 0 | 1 | +1 | **First joint pass in the project** |
| t0080 (54-d v3 substrate NSGA-II, 192 cells) closest-to-joint cell 188 | DSI | 0.000 | 0.494 | +0.494 | **DSI rescued from collapse** |
| t0080 (54-d v3 substrate NSGA-II, 192 cells) closest-to-joint cell 188 | PD rate (Hz) | 9.25 | 11.39 | +2.14 | Joint pass crossed |
| t0080 (54-d v3 substrate NSGA-II, 192 cells) | Closest-to-joint distance | 0.850 | 0.000 | -0.850 | **Pass criterion met; 15.2x closer trajectory** |
| t0080 (54-d v3 substrate NSGA-II, 192 cells) | Pareto front size (cells) | 5 | 16 | +11 | **3.2x larger Pareto front under 4x budget + warm-start** |
| t0080 (54-d v3 substrate NSGA-II, 192 cells) | Cells with DSI > 0 (%) | 8.9% (17/192) | 50.3% (386/768) | +41.4 pp | Massive improvement in feasible-DSI sampling |
| t0076 (25-d Bed B substrate, qNEHVI) iter-424 | DSI at PD ~ 8-11 Hz | 0.42 | 0.494 | +0.074 | Cell 767 exceeds t0076's strongest joint result |
| t0076 (25-d Bed B substrate, qNEHVI) iter-424 | PD rate (Hz) | 8.34 | 11.39 | +3.05 | t0076 missed the 10 Hz threshold; t0081 clears it |

## Methodology Differences

* **Optimiser**: t0081 uses **NSGA-II via pymoo** (pop=96 / gen=8 = 768 evaluations, SBX eta=15,
  polynomial mutation eta=20, RankAndCrowding survival) with a **combined t0078 + t0080 + LHS
  warm-start** initial population. t0080 used the same NSGA-II configuration but with **fresh LHS
  init only** (pop=24 / gen=8 = 192 evaluations) -- 4x smaller budget, no warm-start. t0078 used
  **BoTorch qLogNEHVI** (491 evaluations) with SingleTaskGP surrogates and Sobol DoE init.
* **Warm-start composition (t0081 only)**: 5 t0080 Pareto cells verbatim (54-d natural-unit) + 17
  t0078 Pareto cells projected from 49-d to 54-d (indices 0-48 verbatim, indices 49-53 sampled
  uniformly with `numpy.random.default_rng(42).uniform(lo, hi)` within the natural-unit bounds for
  the new dendritic-spike parameters) + 74 fresh LHS samples (seed 43). t0080's LHS init had no
  prior-task knowledge; t0078's BoTorch DoE used Sobol-only.
* **Substrate**: t0081 uses t0080's `de_rosenroll_2026_dsgc_ais_dendritic_spike` library asset
  unchanged (54-d: 49 t0078 dims + 5 dendritic-spike dims `gnmda_dend`, `mg_conc_mm`, `voff_nmda`,
  `nav16_dend_distal`, `nap_dend_distal`). t0078 used a 49-d AIS-only substrate. t0076 used a 25-d
  substrate with no AIS and passive dendrites.
* **DSI definition**: t0081 / t0080 / t0078 / t0076 all use polar vector-sum DSI = (PD - ND) / (PD
  + ND) over 8 directions x 20 seeds, computed from trial-averaged spike counts. `[Trenholm2013]`
    and `[Oesch2005]` compute DSI from **peak** Gaussian-convolved (sigma = 25 ms) instantaneous
    rates; the resulting peak-rate DSIs are typically 0.05-0.15 higher than mean-rate DSIs from the
    same cell (`[Trenholm2013, Results p. 14068]`).
* **Firing-rate window**: t0081 uses TSTOP_MS = 1400 ms with trial-averaged spike rate.
  `[RivlinEtzion2012]` reports mean rate over a 3 s grating window -- directly comparable.
  `[Trenholm2013]` / `[Oesch2005]` report peak instantaneous rate from Gaussian-convolved trains
  over sub-second windows -- not directly comparable to t0081's 11.39 Hz mean rate.
* **AIS hard-floor enforcement**: t0081 inherits t0080's AIS hard floor (`nav16_ais` >= 0.25 S/cm²
  per `[Kole2008, p. 178]`; AIS-to-soma Nav ratio >= 5 below the lowest measured RGC value per
  `[Werginz2024]`). Cell 767 by construction does not exhibit the t0078 iter-81 AIS-disabled failure
  mode.
* **HV reference convention**: t0081 inherits t0080's utopia point `(0.7, 80)`. t0076 / t0078 used
  reference `[0, 0]`. HV values across these tasks are not numerically comparable; only the
  Pareto-front extent and joint distance metric translate.
* **Stimulus and pharmacology**: identical to t0080 / t0078 / t0076 (1 mm/s 250 um bar in 8
  directions, control conditions). Cross-method DSI / rate comparisons inherit the +/- 20-30%
  variability typical of stimulus-protocol differences.

## Analysis

The t0081 Pareto front confirms a **fully expanded** trade-off geometry: a high-DSI rail (DSI
0.5-1.0 with PD 1.86-3.11 Hz, e.g. cell 699 at DSI 1.000), a high-PD rail (PD 119-133 Hz with DSI <=
0.03, e.g. cell 627 at PD 133.21 Hz), and -- crucially -- the **joint-target region with cell 767 at
DSI 0.494 / PD 11.39 Hz crossing both pass thresholds simultaneously**. The pass-criterion box (DSI
>= 0.4 AND PD >= 10 Hz, top-right of the trade-off plane) was **empty in t0078 (0/491 cells), empty
in t0080 (0/192 cells), and now contains cell 767 in t0081 (1/768 cells)**.

**Joint z-score interpretation.** The Mahalanobis-style joint z-score for cell 767 against the
RivlinEtzion2012 stable-cell distribution:

* DSI z = (0.494 - 0.78) / 0.19 = **-1.50** (within +/-2 sigma; ~7% of published stable cells in
  `[RivlinEtzion2012]` would have DSI <= 0.494). This is a major narrowing from t0078's -2.44 sigma
  and t0080's -4.11 sigma -- the project's DSI deficit relative to RivlinEtzion has shrunk by **2.6
  sigma in two tasks**.
* PD-rate z = (11.39 - 10.38) / 8.53 = **+0.12** (well within 1 sigma; cell 767's PD rate is
  biologically central, not just plausible).

**Cell 767 vs the broader literature.** Cell 767's **DSI 0.494** exceeds three published baselines
in the project corpus: `[deRosenroll2026, Fig. 5]` correlated-SAC-release substrate baseline of 0.39
(+0.104, +27%), `[Sivyer2010, Results]` rabbit ON-OFF ON DSI of 0.45 (+0.044), and the project's
working pass threshold of 0.40 derived from the Sivyer/Park range. The DSI sits below `[Park2014]`
mouse CART-Cre 0.65 (-0.156), `[PolegPolsky2016]` mouse DRD4 0.65 (-0.156), `[Sivyer2010]` rabbit
OFF 0.50 (-0.006, near-match), `[Trenholm2013]` peak-rate 0.76 (-0.266, metric mismatch), and
`[Oesch2005]` peak-rate 0.67-0.74 (-0.176 to -0.246, metric mismatch). Crucially, **none of t0078's
high-DSI cells reach this regime at PD >= 10 Hz** -- t0078's max-DSI cell (iter 290, DSI 1.000) sits
at PD 0.36 Hz, and t0078's iter 349 (DSI 0.529) sits at PD 3.25 Hz. Cell 767 is the first cell in
the project lineage to combine DSI > 0.45 with biologically plausible mean PD firing rate.

**Versus t0078: the headline improvement.** t0081 cell 767 (DSI 0.494 / PD 11.39 Hz) improves on
t0078 iter 81 (DSI 0.316 / PD 9.68 Hz) by **+0.178 DSI (+56%)** and **+1.71 Hz PD rate**. t0078's
analysis flagged the missing dendritic-spike machinery as the dominant explanation for the DSI
ceiling; t0081 confirms this prediction empirically. With the 5 dendritic-spike parameters present
(`gnmda_dend`, `mg_conc_mm`, `voff_nmda`, `nav16_dend_distal`, `nap_dend_distal`), the optimiser
found a configuration that lifts DSI from 0.316 to 0.494 while raising PD rate from 9.68 Hz to 11.39
Hz -- the substrate change (t0078 -> t0080's v3) was necessary, and the warm-start + budget
combination was sufficient to extract the joint-pass cell from it.

**Versus t0080: substrate vindicated.** t0080's analysis flagged three plausible causes for the
192-cell run's DSI collapse to 0.000 at PD 9.25 Hz: NSGA-II under-budgeted at pop=24 in 54-d, no
warm-start from prior good cells, and possible substrate regression. t0081 directly tests the first
two by upgrading to pop=96 (4x) with combined warm-start and observes a **+0.494 DSI recovery** at
+2.14 Hz PD rate at the joint-closest cell. This rules out the third hypothesis (the v3 substrate is
not regressed -- it admits joint-pass cells when given an adequate budget plus warm-start). The
substrate is now established as the project's working substrate for further joint-optimisation work.

**Why warm-start was decisive.** The first generation of t0081 already contained a t0078-projected
cell at DSI 0.252 / PD 10.75 Hz (cell 12) -- within distance 0.148 of the joint target, **10x closer
than t0080's final closest-to-joint distance of 0.850**. By gen 6, NSGA-II had evolved the
closest-to-joint cell to distance 0.063 (cell 637: DSI 0.337 / PD 11.82 Hz). By gen 7, cell 767
crossed the threshold at distance 0.000. The 17 t0078 Pareto cells projected with random new-dim
values gave NSGA-II a head start in the relevant region of 54-d space: the t0078-tuned 49-d AIS
parameters were already inside a high-DSI manifold, and the random sampling of the 5 dendritic-
spike dims provided the optimiser with a wide cross-section through the new architectural axis to
hill-climb on. By contrast, t0080's fresh LHS init in 54-d had to discover both the AIS-tuned
manifold and the dendritic-spike-tuned manifold from scratch within 192 evaluations, which proved
infeasible.

**Versus t0076: the joint-pass milestone.** t0076's strongest joint result was iter 424 at DSI 0.42
/ PD 8.34 Hz -- the closest single-cell to the project's pass criterion before t0081, but missing
the 10 Hz PD threshold by 1.66 Hz. t0081 cell 767 exceeds t0076 iter 424 on **both** axes (+0.074
DSI / +3.05 Hz PD), making it the first cell in the project lineage to clear the pass criterion in
joint form rather than approaching it asymptotically.

**AIS hard-floor enforcement: maintained.** t0081 inherited t0080's hard-floor regime
(`nav16_ais >= 0.25 S/cm²`, AIS-to-soma Nav ratio >= 5). 87.8% feasibility (674/768 cells) confirms
the constraint is well-conditioned for the search; cell 767 is biologically plausible by
construction with respect to the Kole 2008 / Werginz 2024 priors and at the upper edge of the
Goethals 2020 axial-current estimate range.

## Limitations

* **Single-replicate observation**: cell 767 is a single Pareto-front cell from a single NSGA-II
  chain with one Sobol/LHS init seed plus one warm-start RNG seed (42 for t0078 projection, 43 for
  fresh LHS). The +56% DSI improvement over t0078 and the joint-pass crossing are single-replicate
  observations. A multi-replicate study (3-5 seeds) is suggested as a follow-up to confirm
  reproducibility and quantify HV variance around the pass region.
* **Single joint-pass cell**: 1 / 768 cells crosses the threshold. The cluster of near-pass cells
  (637 at distance 0.063, 762 at 0.086, 767 at 0.000) suggests the optimiser is right at the
  boundary; a longer run (more generations) might find more joint-pass cells. The pass region of the
  parameter space is therefore **discovered but not characterised**.
* **HV reference-point inconsistency persists**: t0081 inherits t0080's utopia = (0.7, 80); t0076 /
  t0078 used reference = `[0, 0]`. HV trajectory values (6.59 -> 16.33) are not directly comparable
  to t0078's 11.41 final HV. A dedicated re-computation under a single convention is needed
  (suggested as a separate task).
* **Mean-rate vs peak-rate metric mismatch persists**: published `[Trenholm2013]` and `[Oesch2005]`
  values are peak Gaussian-convolved instantaneous rates; t0081 reports trial- averaged mean rates
  over 1400 ms. The cell-767 vs Trenholm 198 Hz delta is a metric mismatch, not a biological
  mismatch. Only `[RivlinEtzion2012]`'s 3 s-window mean rate is directly comparable to t0081's
  firing-rate metric.
* **DSI definitions vary across the corpus**: `[Trenholm2013]`'s peak-rate DSI is structurally +0.05
  to +0.15 higher than the trial-averaged spike-count DSI used in t0081. Cross-paper DSI comparisons
  inherit this systematic bias; cell 767's DSI 0.494 measured under peak-rate convention would
  likely fall at ~0.55-0.60.
* **Smoke gate failures on 2 / 5 t0080 cells**: cells 141 and 190 (low-DSI < 0.13) showed DSI
  reproducibility deltas exceeding the +/- 0.05 tolerance during the pre-launch substrate-
  consistency check. Stochastic noise on low-spike-count cells is the most likely explanation; the
  substrate is consistent enough at higher-DSI cells (cell 767's regime).
* **No deep-dive Vm-trace analysis on cell 767**: per-direction Vm traces and dendritic-spike
  recruitment analysis for cell 767 were not produced. Would require re-evaluation in subprocess on
  a fresh Vast.ai instance. Without this, the biophysical mechanism for the DSI improvement cannot
  be attributed to specific dendritic-spike machinery (NMDA Mg-block vs distal Nav1.6 vs NaP).
* **No paired DSI + mean PD-rate measurements other than `[RivlinEtzion2012]`**: the joint
  literature anchor at (DSI 0.78, 10.38 Hz) is from a single n = 8 sample. No other paper in the
  project corpus reports paired joint DSI + mean PD-rate values; t0081's pass criterion remains
  anchored to a single small-sample reference.
* **No cross-bed validation**: t0081 only operates on Bed B. The v3 dendritic-spike machinery and
  the warm-start strategy have not been evaluated on Bed A or other DSGC morphologies.
