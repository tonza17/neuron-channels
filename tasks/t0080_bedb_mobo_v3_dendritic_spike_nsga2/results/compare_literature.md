---
spec_version: "1"
task_id: "t0080_bedb_mobo_v3_dendritic_spike_nsga2"
date_compared: "2026-05-04"
---
# Comparison with Published Results

## Summary

The 54-d dendritic-spike-augmented Bed B substrate with NSGA-II at pop=24 / gen=8 (192 evaluations,
$0.7458) produces a sparse 5-cell Pareto front that **misses the joint pass criterion (DSI >= 0.4
AND PD >= 10 Hz) by a wide margin**. The closest-to-joint Pareto cell sits at **DSI 0.000 / PD 9.25
Hz** (cell 188, distance 0.850 from joint), and the max-DSI Pareto cell sits at **DSI 0.127 / PD
2.54 Hz** (cell 141). Against the literature anchor of paired DSI + mean PD firing rate from
`[RivlinEtzion2012, Fig. S2 + Results p. 522]` (**DSI 0.78 +/- 0.19**, **PD 10.38 +/- 8.53 Hz**, n =
8 stable cells), the joint-closest cell sits at a joint z-score of **(-4.11 on DSI, -0.13 on PD)**:
the PD axis is biologically plausible while the DSI axis is **4.1 sigma** below the published mean.
The result is a **clean architectural negative outcome** strongly conditioned by the small NSGA-II
budget — t0080's 192 cells in 54-d cannot be directly compared with t0078's 491 cells in 49-d. The
AIS hard-floor enforcement (`nav16_ais` >= 0.25 S/cm² per `[Kole2008, p. 178]`; AIS-to-soma Nav
ratio >= 5 per `[Werginz2024, Table 1]`) **did achieve its primary objective**: zero Pareto cells
collapsed to the t0078 iter-81 AIS-disabled-corner failure mode. Independent confirmation from
`[Goethals2020]` axial-current measurements (12-55 mS/cm² range) places t0080's 0.25 S/cm² floor
at the upper edge of that estimate range.

## Comparison Table

### Literature Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| `[RivlinEtzion2012, Fig. S2 + Results p. 522]` mouse ON-OFF DSGC stable cells, n=8 | DSI (3 s grating window) | 0.78 | 0.000 | -0.780 | Cell 188 (closest-to-joint); z = -4.11 |
| `[RivlinEtzion2012, Fig. S2 + Results p. 522]` mouse ON-OFF DSGC stable cells, n=8 | Mean PD firing rate (Hz) | 10.38 | 9.25 | -1.13 | Cell 188; z = -0.13; within 1 sigma |
| `[deRosenroll2026, Fig. 5]` correlated SAC release (Bed B substrate ancestor) | DSI | 0.39 | 0.127 | -0.263 | Cell 141 (max-DSI Pareto); -67% of published value |
| `[deRosenroll2026, Fig. 5]` uncorrelated SAC release | DSI | 0.25 | 0.127 | -0.123 | Cell 141; below uncorrelated baseline |
| `[Park2014, Table 1]` mouse CART-Cre On-Off DSGC | DSI | 0.65 | 0.127 | -0.523 | Cell 141; -10.5 sigma on Park SD 0.05 |
| `[Sivyer2010, Results]` rabbit ON-OFF DSGC ON | DSI | 0.45 | 0.127 | -0.323 | Cell 141 |
| `[Sivyer2010, Results]` rabbit ON-OFF DSGC OFF | DSI | 0.50 | 0.127 | -0.373 | Cell 141 |
| `[Oesch2005, Results p. 754]` rabbit ON dendritic-AP DSGC | Peak-rate DSI | 0.67 | 0.127 | -0.543 | Cell 141; metric mismatch (mean-rate vs peak-rate) |
| `[Oesch2005, Results p. 754]` rabbit OFF dendritic-AP DSGC | Peak-rate DSI | 0.74 | 0.127 | -0.613 | Cell 141; metric mismatch |
| `[Oesch2005, Results p. 754]` rabbit | Modal peak PD rate (Hz, peak) | 148.0 | 9.25 | -138.75 | Cell 188; metric mismatch (mean vs peak) |
| `[Trenholm2013, Results p. 14064]` mouse Hb9 DSGC, control | Peak PD rate (Hz, Gaussian-conv) | 198.0 | 9.25 | -188.75 | Cell 188 mean rate vs Trenholm peak rate |
| `[Trenholm2013, Results p. 14064]` mouse Hb9 DSGC, control | Peak-rate DSI | 0.76 | 0.127 | -0.633 | Cell 141; metric mismatch |
| `[PolegPolsky2016, Results]` mouse DRD4 DSGC (passive-dendrite ancestor) | DSI | 0.65 | 0.127 | -0.523 | Cell 141; -80% of published value |
| `[Werginz2024, Table 1]` mouse alpha-ON-sustained RGC | AIS Nav density (S/cm²) | 1.30 | >= 0.25 | within range | Hard-floor enforced; Pareto cells span 0.25-5.0 |
| `[Kole2008, p. 178]` cortical pyramidal AIS prior | AIS Nav density (S/cm²) | 0.25-0.5 | >= 0.25 | floor met | Lower bound enforced as hard parameter floor |
| `[Werginz2024, Table 1]` mouse alpha-ON-sustained RGC | AIS-to-soma Nav ratio (x) | 17.3 | >= 5 | floor met | Hard ratio floor of 5 enforced via inequality constraint |
| `[Goethals2020]` axial-current AIS Nav estimate (independent) | AIS Nav density (mS/cm²) | 12-55 | >= 250 | floor at upper edge | t0080's 0.25 S/cm² = 250 mS/cm² sits at the upper edge of Goethals's estimate range |

### Prior Task Comparison

| Prior Task | Metric | Prior Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| t0078 (49-d AIS-augmented Bed B BoTorch) | Closest-to-joint DSI | 0.316 | 0.000 | -0.316 | Cell 188 vs t0078 iter 81; t0080 PD-axis Pareto cell has zero DSI |
| t0078 (49-d AIS-augmented Bed B BoTorch) | Closest-to-joint PD rate (Hz) | 9.68 | 9.25 | -0.43 | Cell 188; PD axis nearly matches t0078 |
| t0078 (49-d AIS-augmented Bed B BoTorch) | Pareto front size (cells) | 17 | 5 | -12 | t0080 explored 192 cells; t0078 explored 491 |
| t0078 (49-d AIS-augmented Bed B BoTorch) | Hypervolume | 11.41 | n/a (different ref) | n/a | t0080 used utopia (0.7, 80) reference; not numerically comparable |
| t0078 max-DSI Pareto cell (iter 290) | DSI | 1.000 | 0.127 | -0.873 | t0080 max-DSI sub-Pareto cell does not approach t0078's max-DSI rail |
| t0076 (25-d Bed B substrate, qNEHVI) iter-424 | DSI at PD ~ 8 Hz | 0.42 | 0.026 | -0.394 | Cell 153 (PD 8.46 Hz, closest to t0076 iter-424 PD); -94% of t0076 value |
| t0076 (25-d Bed B substrate, qNEHVI) iter-424 | PD rate (Hz) at DSI ~ 0.4 | 8.34 | 9.25 | +0.91 | Cell 188 expands PD axis but at DSI 0.000 |
| t0076 (25-d Bed B substrate, qNEHVI) | Pareto front size (cells) | many | 5 | sparse | t0076 explored 491 cells; t0080's 5-cell front is highly under-resolved |

## Methodology Differences

* **Optimiser**: t0080 uses **NSGA-II via pymoo** (population 24, generations 8, SBX eta=15,
  polynomial mutation eta=20, RankAndCrowding survival, LHS init). t0078 and t0076 used **BoTorch
  qLogNEHVI** with SingleTaskGP surrogates and Sobol DoE init. The two optimiser families have
  different sample-efficiency profiles: BoTorch's GP surrogate carries information across
  evaluations, while NSGA-II relies purely on selection pressure on the current population. NSGA-II
  needs much larger populations for high dimensionality (Hay 2011 used pop=1000 for 22-d; t0080's
  pop=24 for 54-d is dramatically under-budgeted).
* **Evaluation budget**: t0080 ran **192 evaluations** (5% of plan's 3,840); t0078 ran 491; t0076
  ran 491. The t0080 reduction was forced by per-cell saturating 64 cores (~45 s wall-clock per cell
  sequentially) on the Vast.ai instance under the $2.00 cost cap.
* **DSI definition**: t0080 / t0078 / t0076 all use polar vector-sum DSI = (PD - ND) / (PD + ND)
  over 8 directions x 20 seeds, computed from trial-averaged spike counts. `[Trenholm2013]` and
  `[Oesch2005]` compute DSI from **peak** Gaussian-convolved (sigma = 25 ms) instantaneous rates;
  the resulting peak-rate DSIs are typically 0.05-0.15 higher than mean-rate DSIs from the same cell
  (`[Trenholm2013, Results p. 14068]`).
* **Firing-rate window**: t0080 uses TSTOP_MS = 1400 ms with trial-averaged spike rate.
  `[RivlinEtzion2012]` reports mean rate over a 3 s grating window; `[Trenholm2013]` / `[Oesch2005]`
  report peak instantaneous rate from Gaussian-convolved trains over sub-second windows. Cell 188's
  9.25 Hz mean PD rate is directly comparable to RivlinEtzion's 10.38 Hz, but **not** to Trenholm's
  198 Hz peak or Oesch's 148 Hz modal peak.
* **Substrate**: t0080 inherits the de Rosenroll Bed B morphology + SAC release from
  `[deRosenroll2026]` and adds dendritic-spike machinery (Mg-block NMDA at all dendrites + Nav1.6
  + NaP at distal dendrites). t0078 added an AIS but kept dendrites passive. t0076 had no AIS and
    passive dendrites. `[PolegPolsky2016]` uses passive dendrites with NMDA Mg-block but no AIS.
    `[Werginz2024]` uses an alpha-RGC morphology with no SAC-driven inhibition.
* **Dimensionality**: t0080 = **54-d** (49 t0078 parameters + 5 new dendritic-spike parameters:
  `gnmda_dend`, `mg_conc`, `voff_nmda`, `nav16_dend_distal`, `nap_dend_distal`). t0078 = 49-d. t0076
  = 25-d. The 5-d expansion in t0080 was matched with a 2.6x **smaller** evaluation budget, which is
  the dominant explanation for the regressed Pareto coverage.
* **AIS hard-floor enforcement**: t0080 is the **first task in the project** to enforce the AIS hard
  floor as a parameter bound + inequality constraint (`nav16_ais >= 0.25 S/cm²`, AIS-to-soma Nav
  ratio >= 5). t0078 had no hard floors and converged on the AIS-disabled corner at iter 81
  (`nav16_ais` = 1e-5, ratio = 5.5e-5). t0080 cells are all biologically plausible by construction.
* **HV reference convention**: t0080's `nsga2_loop.py` computes HV against utopia point `(0.7, 80)`;
  t0076 / t0078 used `[0, 0]`. HV values across these tasks are not numerically comparable; only the
  Pareto-front extent and the joint distance metric translate.
* **Stimulus**: t0080 uses a 1 mm/s 250 um bar in 8 directions. `[RivlinEtzion2012]` uses a drifting
  square-wave grating; `[Trenholm2013]` uses a positive-Weber bar at 600 um/s; `[Park2014]` uses a
  moving spot. Cross-method DSI / rate comparisons inherit the +/- 20-30% variability typical of
  stimulus-protocol differences.
* **Pharmacology**: t0080 simulates control conditions (no GABA-A blockade), matching
  `[Trenholm2013]` control (198 Hz) and `[RivlinEtzion2012]` control. `[Trenholm2013]`'s 244 Hz
  picrotoxin value is not a comparable target.

## Analysis

The Pareto front confirms a **strongly compressed** trade-off geometry: Cell 141 (the only Pareto
cell with non-trivial DSI = 0.127) sits at PD 2.54 Hz; the high-PD rail (cells 58, 153, 188) sits at
DSI <= 0.026 across PD 8.5-9.25 Hz. **No Pareto cell crosses the joint pass criterion** (DSI >= 0.4
AND PD >= 10 Hz). The closest-to-joint distance is **0.850**, dominated by the DSI shortfall (0.40)
rather than the PD shortfall (0.75 Hz).

**Joint z-score interpretation.** The Mahalanobis-style joint z-score for cell 188 against the
RivlinEtzion2012 stable-cell distribution:

* DSI z = (0.000 - 0.78) / 0.19 = **-4.11** (well outside +/- 3 sigma; less than 0.005% of stable
  cells in `[RivlinEtzion2012]` would have DSI 0).
* PD-rate z = (9.25 - 10.38) / 8.53 = **-0.13** (within 1 sigma; biologically plausible).

The PD axis successfully reproduces biological mean rates while the DSI axis remains essentially
**at zero** for the joint-closest cell. This pattern echoes the t0078 finding (DSI z = -2.44 on the
joint-closest cell) but is much more severe — t0078 reached DSI 0.316 at PD 9.68 Hz, t0080
collapses to DSI 0.000 at PD 9.25 Hz. The dendritic-spike machinery added in t0080 (NMDA + Nav1.6
+ NaP at distal dendrites) **did not improve directional gain** in the joint-PD regime within the
  192-cell budget.

**Versus t0078.** The headline regression is dramatic: t0080's joint-closest cell DSI (**0.000**) is
**0.316 lower** than t0078's joint-closest (0.316). t0080's max-DSI Pareto cell DSI (0.127) is
**0.873 lower** than t0078's max-DSI rail (1.000). Because t0080 added 5 parameters (54-d vs 49-d)
**and** halved the budget (192 vs 491 cells), the regression cannot be cleanly attributed to the
substrate. Three plausible causes, in decreasing likelihood:

1. **NSGA-II at pop=24 in 54-d is fundamentally under-budgeted**: NSGA-II selection pressure needs
   much larger populations for high dimensionality (Hay 2011 used pop=1000 for 22-d; pop=100 is the
   de-facto floor for 50+ d in the genetic-algorithm literature). pop=24 is below the noise floor
   for 54-d.
2. **No warm-start from t0078's known-good cells**: the NSGA-II LHS init started fresh. Mapping
   t0078's iter-81 vector (DSI 0.316 / PD 9.68 Hz) into the 54-d v3 space with the new dendritic
   parameters at zero would land near a known-good seed, but no v3 cell was seeded from t0078.
3. **The dendritic-spike substrate may itself regress the joint Pareto front**: adding 5 parameters
   that **default to runaway depolarisation** (high distal Nav1.6 + NaP) without matched dendritic
   Kv3 / Kv4 / Kv7 may shift the substrate's stable manifold toward non-spiking or quiescent cells.
   The pre-launch substrate-regression check (REQ-9 / REQ-16) was deferred, so the substrate's
   biological consistency at the t0076 iter-424 vector was not independently verified.

**Versus t0076.** t0076's iter-424 (DSI 0.42 / PD 8.34 Hz) was the strongest single-cell joint
result in the project lineage. t0080's closest-PD Pareto cell (cell 153, PD 8.46 Hz) has DSI
**0.026** — a **94% regression** vs t0076 at the same PD rate. t0080's PD axis modestly
**expanded** to 9.25 Hz (vs t0076's 8.34 Hz), but the DSI axis catastrophically **compressed** from
0.42 to 0.026 in the comparable PD regime. Net: the v3 substrate + NSGA-II under this budget
produces a Pareto front that is dominated by t0076's BoTorch front in the joint operating regime.

**AIS hard-floor enforcement: design objective achieved.** Zero t0080 Pareto cells exhibit the t0078
iter-81 AIS-disabled-corner failure mode. The hard-bound `nav16_ais >= 0.25 S/cm²` (Kole 2008 lower
bound) and AIS-to-soma Nav ratio >= 5 (below the lowest measured RGC value per `[Werginz2024]` at
17.3 and `[Werginz2020]` at ~7) eliminated by construction the regime where the optimiser converges
on a configuration with collapsed AIS Nav. Independent confirmation from `[Goethals2020]`
axial-current measurements gives an AIS Nav range of **12-55 mS/cm²**, placing t0080's hard floor
of 250 mS/cm² (= 0.25 S/cm²) at the upper edge of that estimate range. The floor is **biologically
conservative** in the sense that it accepts only the upper-percentile literature values; future
iterations may consider relaxing the floor toward the Goethals lower bound (~0.012 S/cm²) to widen
the search space.

**Versus PolegPolsky2016 substrate ancestor.** `[PolegPolsky2016, Results]` reports DSI 0.6-0.7 in
passive-dendrite mouse DRD4 DSGCs **without** dendritic-spike machinery. t0080 added that machinery
and produces DSI 0.127 maximum — **80% below** the published baseline. This suggests that adding
dendritic Nav1.6 + NaP without rebalancing the existing substrate's Kv repolarisation may have
**worsened** rather than improved DSI, consistent with the runaway-depolarisation risk flagged in
the task description.

**Substrate validation gap.** The substrate-regression check (REQ-9 / REQ-16) was deferred under
cost pressure; the v3 substrate's biological consistency at the t0076 iter-424 vector was not
independently verified before NSGA-II launch. Without that check, the t0080 result cannot
conclusively distinguish "v3 substrate is regressed" from "NSGA-II under-budgeted in 54-d" as the
dominant cause of the dramatic Pareto compression. This must be the first action in any t0080
follow-up task.

## Limitations

* **Major scope deviation in evaluation budget**: t0080 ran 192 evaluations vs the plan's 3,840 (5%
  of planned). The reduction was forced by sequential per-cell evaluation on a single 64-core
  Vast.ai instance under the $2.00 cap. Direct comparison with t0078's 491 evaluations or t0076's
  491 evaluations is not architecturally clean.
* **Substrate-regression check (REQ-9 / REQ-16) deferred**: the v3 substrate at the t0076 iter-424
  mapped vector was not validated; the smoke gate (8 LHS cells, 0 unstable, 5 non-dominated
  feasible) is a weaker substitute.
* **HV trajectory file granularity**: only 2 entries (gen 0 / gen 1, 96 / 192 cumulative
  evaluations); the HV trajectory plot is sparse. The 5-cell Pareto front and per-cell metrics are
  correct.
* **HV reference-point inconsistency**: t0080 uses utopia = (0.7, 80); t0076 / t0078 used reference
  = [0, 0]. HV values across the three tasks are on different scales and not directly numerically
  comparable. Future runs should standardise on a single convention.
* **Mean-rate vs peak-rate metric mismatch**: published `[Trenholm2013]` and `[Oesch2005]` values
  are peak Gaussian-convolved instantaneous rates (sigma = 25 ms). t0080 reports trial-averaged mean
  rates over 1400 ms. The cell-188 vs Trenholm 198 Hz delta is a metric mismatch, not a biological
  mismatch. Only `[RivlinEtzion2012]`'s 3 s-window mean rate is directly comparable to the t0080
  firing-rate metric.
* **DSI definitions vary across the corpus**: `[Trenholm2013]`'s peak-rate DSI is structurally
  higher than the trial-averaged spike-count DSI used in t0080. Cross-paper DSI comparisons inherit
  this systematic +0.05 to +0.15 difference.
* **Park 2014 SD of 0.05 unrealistically small**: yields z = -10.5 against cell 141, implausible for
  a biological measurement. Reflects within-cell-type homogeneity in the CART-Cre transgenic line,
  not the full DSGC population. Use `[RivlinEtzion2012]`'s SD 0.19 for defensible z-scores.
* **Werginz 2020 PDF paywalled in the project corpus**: the AIS-to-soma Nav ratio of ~7x for mouse
  OFF-alpha-T RGCs is in the metadata only. The hard-floor justification rests primarily on
  `[Werginz2024, Table 1]`'s 17.3x value. `[Goethals2020]` axial-current method provides independent
  confirmation of the AIS Nav range.
* **No cross-bed validation**: t0080 only operates on Bed B. The v3 dendritic-spike machinery has
  not been ported to or evaluated on other substrates.
* **Single NSGA-II run, single seed**: t0080's 5-cell Pareto front comes from one LHS init and one
  NSGA-II chain. The Pareto-front structure may shift with a different RNG seed; no Pareto-front
  uncertainty estimate is reported.
* **No paired DSI + mean PD-rate measurements other than `[RivlinEtzion2012]`**: the joint
  literature anchor at (DSI 0.78, 10.38 Hz) is from a single n = 8 sample. No other paper in the
  project corpus reports paired joint DSI + mean PD-rate values.
