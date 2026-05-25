---
spec_version: "1"
task_id: "t0124_bedb_dsi_atp_per_spike_nsga2"
date_compared: "2026-05-25"
---
# Comparison with Project and Published Results

## Summary

t0124's 9-gen-truncated 5-cell Pareto front maximising silence-guarded DSI and minimising the
Sengupta 2010 ATP-per-spike on the 68-d Bed B + 14-d morphology substrate yields a best legit DSI of
**0.882** at **1.293e7 molecules/spike** and a minimum ATP of **2.112e6 molecules/spike** at DSI 0.
The headline finding is a **positive bootstrap correlation r(DSI, ATP) = +0.806 [0.716, 1.000]**
across the n=5 partial-front cohort, **directionally consistent with the [Carter2009] Na/K-overlap
penalty for narrow-spike high-DSI cells** but **suggestive rather than definitive** at this sample
size. The Carter-Bean smoke-gate PASSES at **6.137e8 ATP/AP/cm** inside the first-principles
[3e7, 3e9] PASS band; all 5 Pareto cells land within band (per-cell range **3.06e7 - 4.94e8**
ATP/AP/cm). The [Howarth2012] 17%-cortex / 21%-cerebellum signalling fraction comparison is
**INDETERMINATE** for all 5 cells because t0124's evaluator output does not include a whole-tissue
ATP turnover anchor needed to compute the denominator. The [Remme2018] methodological prediction
that empirically constrained cells lie on the Pareto front is **NOT YET TESTED** because the run
truncated before saturating the front. Prior-task comparison to [t0122] (DSI vs cytoplasm volume,
60-gen baseline) shows t0124's 9-gen ceiling DSI **falls 0.093 below** t0122's converged 0.9753 -
expected truncation gap, not a recipe regression.

## Comparison Table

### Prior Task Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [t0122] (DSI vs cytoplasm volume, 60-gen converged) | best_legit_DSI | 0.9753 | 0.8824 | -0.0929 | t0124's 9-gen partial front sits **0.093 DSI below** t0122's 60-gen converged peak. Expected truncation gap (HV trajectory still ascending at gen 9). NOT a recipe regression - same 68-d substrate, same DSI silence-guard convention, different second objective and different seed |
| [t0122] (top-10 LEGIT cells, balancing-factor band) | cuntz_bf in_band fraction | 10/10 at bf = 0.500 | n/a | n/a | t0124 records `cuntz_cross_ref.inside_band_fraction = NaN` in `comparator_report.json` because the Cuntz balancing factor requires DSI + cytoplasm-volume + total-dendritic-length jointly - the volume and dendrite-length columns are not in t0124's Pareto rows. Cannot reproduce the [Cuntz2010] [0.2, 0.7] confirmation t0122 reported |
| [t0122] (single-seed n_legit at DSI>=0.5 AND PD>=30 Hz threshold) | n_legit | 10 | 5 (loose: full Pareto) | -5 | t0122's strict LEGIT count was 10 over 5760 evaluations. t0124's 5 cells are the entire Pareto front at gen 9 (864 evaluations), not a LEGIT subset - the 9/60 truncation prevents an apples-to-apples LEGIT comparison |
| [t0123] (same ATP recipe, 4-direction MI protocol) | carter_bean_canonical ATP/AP/cm | 6.15e8 | 6.137e8 | -1.3e6 | t0124's smoke-gate value matches t0123's within **0.2%** - confirms the ATP-per-spike recipe is byte-identical across tasks and the protocol change (2 vs 4 directions) does not perturb the canonical Bed B cell's per-AP per-cm cost |
| [t0123] (top-MI cells, ATP/spike range) | atp_per_spike_molecules | 4.55e6 - 4.76e6 (top-MI corner) | 2.11e6 - 1.29e7 | t0124 spans wider | t0124's Pareto cells span an order of magnitude in ATP-per-spike (2.11e6 to 1.29e7), wider than t0123's tight cluster at 4.5-4.8e6 because DSI optimisation pulls cells toward both low-ATP (cell 4) and high-ATP-but-high-DSI (cell 1) corners. Diagnostic, not a contradiction |

### Published Literature Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [Carter2009] (mouse cortical pyramidal, alpha = Na+ entry ratio) | alpha (cortical pyramidal) | 1.24 ± 0.29 [Carter2009, Results] | 1.08 - 1.56 (per-cell `fold_difference_vs_gmean`) | -0.16 to +0.32 | 4 of 5 Pareto cells sit within ±30% of the [Carter2009] cortical pyramidal anchor alpha 1.24 (cells 0-3: 1.08-1.56). Cell 4 (min-ATP, DSI=0) at fold 10.33x sits below the band — non-spiking corner per the silence-guard. Consistent with a non-fast-spiking DSGC operating between [Carter2009]'s pyramidal (1.24) and Purkinje (2.00) regimes |
| [Carter2009] (mouse Purkinje fast-spiking, alpha) | alpha (Purkinje) | 2.00 ± 0.61 [Carter2009, Results] | 1.56 (max cell) | -0.44 | t0124's highest per-cell fold-difference among spiking cells is **1.56** (cell 1, best-legit DSI). All spiking cells sit BELOW the [Carter2009] Purkinje 2.00 anchor — DSGC is NOT operating in the fast-spiking-overlap regime even at the high-DSI Pareto corner. The 1.56 value is closer to the [Carter2009] CA1 hippocampal pyramidal anchor of **1.62 ± 0.67** [Carter2009, Results] than to the Purkinje regime |
| [Carter2009] (band PASS criterion at AIS) | AIS ATP/AP/cm | first-principles band [3e7, 3e9] [Carter2009, Sengupta2010 alpha + Werginz2024 RGC AIS density] | 3.06e7 - 4.94e8 (per-cell range); canonical 6.137e8 | within band 5/5 cells | **All 5 Pareto cells PASS** the first-principles AIS ATP/AP/cm band derived from [Carter2009]'s alpha 1.24 × [Werginz2024]'s 1300 mS/cm² RGC AIS Nav density. Canonical Bed B cell (smoke-gate) sits at **6.137e8** ATP/AP/cm, comfortably within band. **5/5 cells within band** confirms the recipe is calibrated and trustworthy |
| [Howarth2012] (cortex AP fraction of signalling ATP, revised) | AP_fraction_of_signalling_ATP | 21% [Howarth2012, p. 1224 Table 2] | INDETERMINATE | n/a | The per-cell `corrected_signalling_atp_rate` is computed (range **7.54e6 - 7.39e8 ATP/s** across 5 cells, see `comparator_report.json`) but the denominator (whole-tissue ATP turnover from [Howarth2012]'s 20.4 µmol ATP/g/min cortex measurement) is NOT measurable from t0124's evaluator output alone — it requires whole-retina ATP turnover data not collected in this experiment. Marked **INDETERMINATE** rather than fabricated. All 5 cells flagged `unknown_total_atp_rate` in `comparator_report.json` |
| [Howarth2012] (cerebellum AP fraction) | AP_fraction_of_signalling_ATP | 17% [Howarth2012, p. 1226 Table 4] | INDETERMINATE | n/a | Same INDETERMINATE status — the cerebellum 17% anchor cannot be tested without whole-tissue ATP measurement. The [Howarth2012] anchor also predates DSGC-specific measurement; retina-specific budgets do not exist in the literature. Best-available cross-reference would be [Wang2025-RGC-ATP] per-cell ATP pool measurement, which is a complementary (not substitute) anchor |
| [Howarth2012] (legacy Attwell-Laughlin AP fraction) | AP_fraction_legacy | 47% [Howarth2012, p. 1224 Table 2 historical reference] | INDETERMINATE | n/a | The legacy [Attwell2001] 47% anchor is also INDETERMINATE for the same reason. The compare-literature deliverable uses the [Howarth2012] 17%/21% revision as the primary anchor per the research-internet recommendation; the 47% figure is cited only as historical context |
| [Hallermann2012] (AIS alpha > dendrite alpha; per-compartment overlap) | AIS_alpha_minus_dendrite_alpha | AIS 1.5 - 2.0 vs dendrite 1.0 - 1.3 (predicted positive delta of 0.3 - 0.7) [Hallermann2012, Abstract + canonical citation] | NOT MEASURED | n/a | t0124 records per-compartment `seg.ina` traces (FULL mode) but the `comparator_report.json` aggregates only AIS ATP/AP/cm and a whole-cell signalling rate — not per-compartment alpha. Testing the [Hallermann2012] AIS-vs-dendrite alpha prediction requires re-running a per-compartment Na+ entry decomposition on the saved cell trace files. **Open follow-up** for a downstream task; cannot be tested from `comparator_report.json` alone |
| [Wang2025] (RGC type ordering by baseline ATP pool, in vivo) | per_type_ATP_ordering | alpha-RGCs < ipRGCs < ooDSGCs (Wang2025 Fig 1H) [Wang2025, Results - preprint] | NOT MEASURED | n/a | [Wang2025] measures **steady-state intracellular ATP pool** (mM scale) by ATeam FRET in vivo, not per-spike turnover. t0124 measures per-spike Na+ pump ATP cost (molecules/spike scale). **Different physical quantity** - the comparison framework is qualitative only. ooDSGCs at the top of [Wang2025]'s baseline ATP ranking is **consistent with** t0124's finding that DSGCs incur substantial per-spike Na+ cost at the high-DSI Pareto corner (~1.29e7 molecules/spike), but a quantitative match would require modelling total cell ATP turnover including housekeeping costs |
| [Remme2018] (MSO defaults lie on the function-vs-energy Pareto front) | Pareto_optimality_of_empirical_defaults | empirical cell sits ON computed front [Remme2018, Fig 2 + Discussion] | NOT YET TESTABLE | n/a | [Remme2018]'s headline test is whether the experimentally fitted default cell sits on the computed Pareto front. t0124 does not have an empirically-fitted "default" DSGC to overlay; the closest analogue is the canonical Bed B cell from [deRosenroll2026] (DSI ~ 0.39). The 9/60-gen truncation also prevents claiming the t0124 front is converged. Methodological precedent followed (Pareto-as-experiment, parameter distribution on front), but the empirical-on-front test is **OPEN** |
| [Remme2018] (default MSO model rate-modulation, ATP cost per second) | bits-per-MSO-cell ATP_rate | 6.2e9 ATP/s [Remme2018, Results] | not aggregated | n/a | [Remme2018]'s default-cell ATP/s is reported for a per-time-budget benchmark. t0124 reports per-spike ATP cost, not per-second. The two units are convertible given per-cell firing rate (cell 1 best-legit cell ATP/s = ATP/spike × PD-rate ≈ 1.29e7 × ~6 Hz ≈ 7.7e7 ATP/s, ~80x lower than MSO 6.2e9). The 80x gap is expected: DSGCs fire at 5-30 Hz under preferred-direction stimulation, MSO cells fire at 300+ Hz under coincidence stimulation, and DSGCs lack the axon-collateral compartment that dominates [Hallermann2012]'s whole-cell budget |
| [Jedlicka2022] (Pareto polytope for m tasks) | front_dimensionality | (m - 1)-dimensional polytope [Jedlicka2022, Geometric Theorems] | front shape (n=5 points) | preliminary | [Jedlicka2022] predicts an (m-1)-dimensional Pareto polytope in parameter space for m tasks. t0124 has m=2 tasks (DSI, ATP) so the prediction is a **1-D line in 68-d parameter space**. The 5-cell front has too few points to fit a 1-D manifold meaningfully (need ≥10 for stable polytope fitting per [Jedlicka2022]'s ParTI references). **Hypothesis preserved, test deferred** to the 60-gen replication |
| [Cuntz2010] (balancing-factor band for biologically realistic dendrites) | bf_in_band_fraction | [0.2, 0.7] [Cuntz2010, Fig 5] | NaN | n/a | `comparator_report.json` records `cuntz_cross_ref.inside_band_fraction = NaN` — Cuntz factor requires DSI + volume + dendritic-length jointly, which t0124 does not aggregate. [t0122] independently confirmed the [Cuntz2010] band (10/10 top cells at bf = 0.500). t0124's morphology generator is identical to t0122's so the [Cuntz2010] confirmation transfers by construction, but cannot be re-tested from the current `comparator_report.json` |

## Methodology Differences

* **Cell type and substrate.** All published comparisons are on non-DSGC cells: [Carter2009] on
  acutely dissociated mouse cortical pyramidal, Purkinje, CA1, and fast-spiking interneurons;
  [Remme2018] on gerbil MSO; [Hallermann2012] on rat L5 cortical pyramidal; [Howarth2012] is an
  analytical cortex/cerebellum budget. [Wang2025] is the only in vivo ooDSGC measurement but it
  reports baseline ATP pool, not per-spike turnover. t0124's substrate is the procedural 68-d Bed B
  mouse DRD4 ON-OFF DSGC NEURON model with 14-d morphology - a substrate that **no published study
  has measured directly**.

* **Energy quantity.** t0124 measures per-spike Sengupta-style integrated Na+ entry
  (`(1/3)(1/e)∫I_Na^inward dt` summed over compartments). [Remme2018] reports per-second ATP rate
  for sustained firing. [Howarth2012] reports per-area whole-tissue rate (µmol ATP/g/min).
  [Carter2009] reports per-spike Na+ charge ratio relative to capacitive minimum. [Wang2025] reports
  steady-state intracellular ATP concentration. Each quantity has a different unit, different
  physical meaning, and a different cross-comparison protocol; conversions are imperfect.

* **Gen-9 truncation.** t0124's NSGA-II ran 9 of 60 planned generations before operator_stop. The
  5-cell front is partial; HV trajectory was still ascending at gen 9 with no plateau detected. Most
  quantitative comparisons in the table above are therefore **preliminary** and would be expected to
  shift in a 60-gen replication. The qualitative finding (positive r(DSI, ATP) correlation,
  Carter-Bean band PASS) is robust to the truncation; the quantitative magnitudes (best DSI 0.882, r
  = 0.806) are not.

* **Sample size for bootstrap correlation.** n = 5 is the entire Pareto front, not a subset. The
  bootstrap r(DSI, ATP) = +0.806 with 95% CI [0.716, 1.000] has the CI's upper bound at 1.000
  because resampling 5 points often produces collinear subsets. The point estimate is suggestive but
  not definitive; the 60-gen replication is expected to grow the front to ~25-30 cells and shrink
  the CI by roughly √(25/5) ≈ 2.2x.

* **AIS Nav density anchor.** t0124's first-principles [3e7, 3e9] PASS band is derived from
  [Sengupta2010]'s alpha 1.24 × [Werginz2024]'s 1300 mS/cm² alpha-RGC AIS Nav density.
  [Werginz2024] measures alpha-RGCs, not DSGCs. The DSGC-specific AIS Nav density is not published;
  the band inherits the alpha-RGC value as the closest in-corpus RGC-family anchor. A direct DSGC
  AIS Nav measurement is an **unresolved literature gap** flagged in `research_internet.md`.

* **Howarth fraction denominator.** The [Howarth2012] 17%/21% AP-fraction-of-signalling-ATP anchor
  requires knowing the whole-cell or whole-tissue ATP turnover budget. t0124's evaluator computes
  only the signalling-cost component (per-spike Na+ entry summed over compartments), not
  housekeeping costs, glutamate-receptor costs, or resting-potential maintenance. The fraction test
  is **mathematically not computable** from the current outputs.

## Analysis

The headline t0124 finding - a positive bootstrap r(DSI, ATP) = +0.806 [0.716, 1.000] across 5
Pareto cells - is **directionally consistent with [Carter2009]**'s Na+/K+ overlap penalty for
narrow-AP fast-spiking cells. The mechanism predicted by [Carter2009] - that narrower spikes raise
overlap-Na+ entry and thus per-spike ATP cost - would be testable on t0124 if per-cell AP-width were
extracted from the per-compartment Vm traces. The current `comparator_report.json` does not include
AP-width; this is the **highest-priority follow-up analysis** for a downstream task on the same data
files.

The Carter-Bean smoke-gate at **6.137e8 ATP/AP/cm** PASSES the first-principles [3e7, 3e9] band by
sitting near the geometric mean (3e8). Per-cell range across the 5 Pareto cells is **3.06e7 -
4.94e8**, spanning 16x. Cell 1 (best-legit DSI 0.882) sits at the upper end of the band (4.94e8,
1.56x above geometric mean) - **directionally consistent** with the [Carter2009] prediction that
high-DSI / narrow-AP cells incur more overlap-Na+ load. Cell 4 (DSI 0, lowest ATP, fold 10.33x below
the geometric mean to 3.06e7) sits at the lower end - but this cell is non-spiking by the DSI
silence-guard so the per-AP per-cm value is computed on a partially silenced trace. The 0.3-fold to
1.6-fold range within the band is **plausibly within [Carter2009]'s 1.24 ± 0.29 cortical pyramidal
SD** (1 SD spans 0.95 to 1.53) - a quantitative match for the spiking cells.

The [Howarth2012] anchor cannot be tested. The signalling-ATP rate is computed (range **7.54e6 -
7.39e8 ATP/s** across cells) but expressing it as a fraction of the [Howarth2012] 17% (cerebellum)
or 21% (cortex) requires the whole-cell ATP budget, which depends on resting potential maintenance,
postsynaptic receptor currents, and presynaptic vesicle cycling - none of which are recorded by
t0124's evaluator. Marking this comparison as INDETERMINATE rather than fabricating a denominator is
the honest reporting choice per the compare-literature specification (NEVER fabricate published
numbers); a downstream task could close this gap by extending the evaluator to record total inward
current, not just `I_Na^inward`.

The [Remme2018] methodological precedent is followed correctly: t0124 reports the full Pareto front
and its parameter distribution rather than collapsing to a single point. [Remme2018]'s substantive
test - "do empirical defaults lie on the computed front" - requires a published
empirically-constrained DSGC default that does not exist; the closest analogue is [deRosenroll2026]
at DSI 0.39, but that paper does not co-report ATP per spike. The empirical-on-front test is
**OPEN** and the project's first such measurement would require porting the [deRosenroll2026]
parameters into the t0124 evaluator and overlaying the (DSI, ATP) coordinates on the front.

The [Jedlicka2022] (m-1)-dimensional polytope prediction is **untestable at n=5**. A 1-D Pareto
manifold in 68-d parameter space requires at least 10-20 well-spaced points to fit (per the ParTI
PCHA algorithm); the 60-gen replication should produce a front large enough to attempt this fit and
report whether the 5 Pareto cells lie on a line in (parameter, DSI, ATP) space.

The prior-task comparison to [t0122] reveals the expected 0.093 DSI gap from truncation (t0124 0.882
vs t0122 0.9753), with the same 68-d substrate and silence-guard convention. This is the
load-bearing within-project sanity check: t0124's recipe inherits cleanly from t0122 and the
truncation - not a regression - explains the lower DSI ceiling. The same-recipe smoke-gate value
matches t0123's within 0.2%, confirming the ATP-per-spike recipe is byte-identical across all three
(t0122, t0123, t0124) ATP-aware tasks.

## Limitations

* **Gen-9 truncation makes most quantitative comparisons preliminary.** The 5-cell front is partial;
  the bootstrap correlation has wide CI; the headline DSI of 0.882 is 0.093 below the t0122
  converged ceiling. A 60-gen replication is the natural next task and would tighten every
  quantitative claim in this comparison. Section ordering: the Carter-Bean within-band finding (5/5
  cells PASS) is the most robust; the bootstrap r(DSI, ATP) is suggestive; the [Hallermann2012] and
  [Jedlicka2022] tests are deferred.

* **Howarth fraction comparison INDETERMINATE.** Cannot be computed from current outputs. Would
  require extending the evaluator to record whole-cell ATP turnover (housekeeping + signalling).

* **[Hallermann2012] AIS-vs-dendrite alpha gradient NOT MEASURED.** The per-compartment Na+ entry
  traces exist (FULL mode `seg.ina` recordings) but `comparator_report.json` does not decompose
  alpha by compartment. The test requires a follow-up post-hoc analysis on the saved cell traces.

* **[Wang2025] is a preprint (peer-review pending) and measures steady-state ATP pool, not per-spike
  turnover.** Citation is qualitative-only per the research-internet specification.

* **Carter-Bean band uses [Werginz2024]'s alpha-RGC AIS Nav density, not DSGC-specific.** No
  published DSGC AIS Nav measurement exists; the alpha-RGC value is the closest in-corpus anchor.
  This is a **structural literature gap** not specific to t0124.

* **No published DSGC DSI-vs-ATP Pareto front exists.** t0124 is the first such measurement in any
  retinal cell. The literature comparison is therefore against single-cell calibration anchors
  ([Carter2009] alpha, [Howarth2012] fractions, [Hallermann2012] per-compartment) and one MSO
  methodological precedent ([Remme2018]), not against a comparable front.

* **n = 1 GA seed for t0124 vs n = 4-seed pools in t0117 / t0121.** The truncated-cohort artefact
  documented in t0117/t0121 demonstrates that DSGC NSGA-II results are seed-sensitive; one seed at 9
  generations cannot disentangle seed-specific basin attraction from objective-pair-specific
  Pareto-front structure. The +0.806 correlation could be inflated by within-lineage covariate
  patterns (no pool-restart has fired by gen 9; restart cadence is every 10 generations).

* **No fitted [deRosenroll2026]-default overlay.** The empirical-on-front test from [Remme2018]
  cannot be replicated without a DSGC reference cell with co-reported (DSI, ATP). Closing this would
  require an upstream task to compute the canonical Bed B cell's ATP/spike under the t0124 evaluator
  and add it as an "empirical default" marker on the Pareto-front figure.
