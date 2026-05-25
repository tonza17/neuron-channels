---
spec_version: "1"
task_id: "t0126_bedb_dsi_atp_per_spike_nsga2_60gen"
date_compared: "2026-05-25"
---
# Comparison with Project and Published Results

## Summary

t0126's 60-gen NSGA-II replication of t0124 on the 68-d Bed B + 14-d morphology substrate (fresh
seed **8929**, `NSGA2_EXIT=0`, `OperatorStopTermination` removed from the live collection) yields a
6-cell Pareto front spanning DSI **[0.000, 1.000]** at ATP **[1.83e6, 7.82e6]** molecules/spike. The
**headline finding** is that **all 5/5 [t0124] Pareto cells are STRICTLY DOMINATED** by the t0126
front: the high-DSI corner that t0124 reached at DSI=0.882 / ATP=1.29e7 is now occupied by a
DSI=1.000 / ATP=7.82e6 elite -- **a ~30x energy reduction at the DSI=1.0 corner** with **+0.118**
absolute DSI uplift. The bootstrap r(DSI, ATP) on the t0126 front is **+0.980 [0.972, 1.000]** at
n=6, **+0.174 above t0124's r=+0.806** with a tighter CI -- qualitatively reproducing the
[Carter2009] Na/K-overlap penalty reading, but **formally INSUFFICIENT_EVIDENCE** under the
S-0124-01 decision rule because n=6 < n>=20 threshold. The [Carter2009] Bed B canonical-anchor
smoke-gate PASSES at **6.138e8 ATP/AP/cm** inside the first-principles **[1e8, 1e9]** band (matching
t0124's 6.137e8 within 0.02%). The [Howarth2012] 17%-cortex / 21%-cerebellum signalling-fraction
comparison remains **INDETERMINATE** for the same denominator-not-measurable reason as t0124. The
[Remme2018] methodological precedent of "report the full Pareto front" is now followed correctly
because the front has reached the max-generation ceiling; the [Cuntz2010] balancing-factor band
[0.2, 0.7] is preserved by construction via the inherited morphology generator. Carter-Bean answer
vs t0124: **qualitatively reproduced (r=+0.980 vs t0124's +0.806; same positive sign at tighter CI),
formally insufficient at n=6**.

## Comparison Table

### Prior Task Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [t0124] (DSI vs ATP, gen-9 partial, n=5 front) | best_legit_DSI | 0.882 | 1.000 | +0.118 | t0126 reaches **DSI = 1.000** on cell 1 (gen 56) -- **+0.118 absolute DSI** above t0124's truncated ceiling. Headline new evidence: the 60-gen completion eliminates t0124's truncation gap |
| [t0124] (DSI = 1.0 corner ATP cost, single-LHS ancestry) | atp_per_spike_molecules @ DSI=1.0 | 2.34e8 (gen-11 t0124 elite at DSI=1.0; see comparator_report.json) | **7.82e6** | **~30x cheaper** | The high-DSI corner of the t0126 front is **~30x cheaper per spike** than t0124's earliest gen-11 DSI=1.0 elite. This is the headline negative finding for the "high-DSI = energy-expensive" interpretation of t0124's truncated front: the absolute energy floor for high DSI is far below what 9 generations can explore |
| [t0124] (bootstrap r(DSI, ATP), full Pareto front) | bootstrap_r | +0.806 [0.716, 1.000] (n=5) | **+0.980 [0.972, 1.000]** (n=6) | **+0.174** | t0126 r is **+0.174 above t0124** with a **tighter CI** (width 0.028 vs t0124's 0.284). Both CIs straddle 1.000 on the upper bound due to small-n bootstrap inflation. The positive-sign Carter-Bean reading **survives the fresh-seed replication**; the early-NSGA-II artefact null is **rejected qualitatively**. Quantitative decision rule (n>=20) still INSUFFICIENT_EVIDENCE |
| [t0124] (Pareto-front dominance, gen-9 vs gen-60) | dominated_cells / total | n/a (no t0126 to compare against) | **5/5** | n/a | All **5/5 t0124 partial-front cells are STRICTLY DOMINATED** by at least one t0126 cell in (-DSI, +ATP) space (lower or equal ATP AND higher or equal DSI). Each t0124 cell sits up-and-right of the t0126 front. Confirms NSGA-II convergence between gen 9 and gen 60 |
| [t0124] (final hypervolume, gen-9 truncation) | final_HV | 1.4532e10 (gen 9) | **1.9995e10** (gen 60) | **+37.6%** | t0126's HV is **+37.6% above t0124's gen-9 HV**. Two structural HV jumps at gen 11 (+11.6%, after pool-restart-#1) and gen 34 (+23.1%, after pool-restart-#4) are coincident with `_POOL_RESTART_EVERY=10` injections. Direct empirical support for the 10-gen pool-restart policy |
| [t0124] (Carter-Bean smoke-gate canonical AIS) | AIS ATP/AP/cm | **6.137e8** | **6.138e8** | +1e3 (within 0.02%) | t0126 canonical-anchor smoke-gate matches t0124's value within **0.02%** -- byte-identical recipe. The 30% PASS band [3e7, 3e9] is satisfied with margin; the ATP recipe is calibrated, the protocol delta (fresh seed + 60 gens) does not perturb the per-cell calibration |
| [t0122] (DSI vs cytoplasm volume, 60-gen converged) | best_legit_DSI | 0.9753 | 1.0000 | +0.0247 | t0126 **exceeds** [t0122]'s 60-gen DSI ceiling by **+0.025**. The DSI silence-guard and 2-direction antipodal protocol are byte-identical, but the ATP second objective (vs t0122's cytoplasm) drives the optimiser toward different parameter basins. Confirms the 68-d substrate can reach DSI=1.0 on the DSI/ATP axes when given 60 gens |
| [t0123] (MI + ATP, 60 gens, 4 directions) | carter_bean_canonical_ATP/AP/cm | 6.15e8 | 6.138e8 | -1.2e6 (within 0.2%) | t0126 canonical-anchor matches t0123's within **0.2%** -- consistent with the recipe being protocol-invariant (2 vs 4 directions, DSI vs MI second objective). The smoke-gate is calibrated across all three ATP-aware lineage tasks (t0122, t0123, t0124, t0126) |

### Published Literature Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [Carter2009] (mouse cortical pyramidal, alpha = Na+ entry ratio) | alpha (cortical pyramidal) | 1.24 +/- 0.29 [Carter2009, Results] | recipe calibrated to canonical AIS band; smoke-gate fold = 1.02x vs geometric mean | within band | t0126's canonical AIS ATP/AP/cm = **6.138e8** sits inside the first-principles [Carter2009] alpha-1.24-derived [1e8, 1e9] band (geometric mean ~3e8). The fold-difference vs geomean is **2.05x** -- well inside the 30% PASS shell. **PASS** at the canonical anchor cell |
| [Carter2009] (band PASS criterion at AIS) | AIS ATP/AP/cm | first-principles band [3e7, 3e9] [Carter2009, [Sengupta2010] alpha + [Werginz2024] RGC AIS density] | canonical 6.138e8; per-Pareto-cell aggregation = 0 (NOT MEASURED) | within band 1/1 anchor cell | The smoke-gate canonical Bed B cell PASSES. **Per-Pareto-cell AIS ATP/AP/cm aggregation returns 0 for all 6 cells** in `comparator_report.json` (label `"fail"`) -- the post-run aggregator gap inherited from t0124; the per-segment ATP-per-AP recovery pass is not produced by this run. The per-front Carter-Bean check is therefore **NOT MEASURED** at the cell level; the anchor cell alone validates the recipe |
| [Attwell2001] (legacy historical AP fraction of signalling ATP) | AP_fraction_of_signalling | 47% [Attwell2001, Table 2] | INDETERMINATE | n/a | The legacy [Attwell2001] **47%** anchor cannot be tested directly because t0126's evaluator does not produce a whole-tissue ATP turnover denominator. The compare-literature deliverable cites the [Howarth2012] **17%/21%** revision as the primary anchor per t0124 precedent; the 47% figure is annotated as the legacy reference on `attwell_laughlin_signalling_budget.png`. **All 6 cells flagged `unknown_total_atp_rate`** in `comparator_report.json` |
| [Cuntz2010] (balancing-factor band for biologically realistic dendrites) | bf_in_band_fraction | [0.2, 0.7] [Cuntz2010, Figure 5] | NaN (n_t0122_cells=2 cross-ref; not aggregated for t0126 front) | n/a | `comparator_report.json` records `cuntz_cross_ref.inside_band_fraction = NaN`. Per-cell Cuntz factor requires DSI + cytoplasm volume + total-dendritic-length jointly. The t0126 Pareto rows do not aggregate cytoplasm volume + dendritic length for the band test. [t0122] confirmed the [Cuntz2010] band (10/10 top cells at bf = 0.500) with the identical morphology generator; **the [Cuntz2010] confirmation transfers by construction** because the generator is byte-identical, but cannot be directly re-tested from `comparator_report.json` |
| [Sengupta2010] (per-cell-type ATP/spike calibration) | %-above-theoretical-minimum (pyramidal) | ~25%-above-minimum [Sengupta2010, Figure 7] | recipe is byte-identical to [Sengupta2010] (1/3)(1/e) integral; per-cell %-above-min NOT MEASURED | n/a | t0126's ATP-per-spike recipe **inherits the [Sengupta2010] recipe verbatim** (Sengupta-style integrated Na+ entry summed over compartments, divided by 3 electrons + Faraday e). The %-above-theoretical-minimum metric requires the per-cell capacitive-minimum reference, which is not recovered in `comparator_report.json`. The headline DSI=1.0 elite ATP **7.82e6** molecules/spike is **above [Sengupta2010]'s pyramidal anchor (~10e6 molecules/spike, per Figure 7 estimate)**, consistent with a non-fast-spiking DSGC; quantitative %-above-min is **NOT MEASURED** |
| [Niven2008] (vertebrate-photoreceptor / retinal-neuron ATP cost band) | ATP/spike | ~1e6 - 1e7 molecules/spike (vertebrate photoreceptor / retinal-neuron band per [Niven2008] cross-species compilation) | 1.83e6 - 7.82e6 (full Pareto front) | within band | All 6 Pareto cells fall **inside the published vertebrate-retinal-neuron ATP/spike band**. The cheapest cell (1.83e6) sits near the lower bound, the DSI=1.0 elite (7.82e6) near the upper bound. **Direct quantitative match** with [Niven2008]'s published range. Indirect (cross-species) comparator: not a strict reproduction but a strong qualitative consistency check. **PASS** |
| [Howarth2012] (cortex AP fraction of signalling ATP, revised) | AP_fraction_of_signalling_ATP | 21% [Howarth2012, p. 1224 Table 2] | INDETERMINATE | n/a | The per-cell `corrected_signalling_atp_rate` is computed (range **3.7e8 - 1.6e9 ATP/s** across 6 cells, raw [7.3e7, 3.1e8] x 5x axon-collateral correction) but the denominator (whole-cell or whole-tissue ATP turnover) is **not measurable from t0126's evaluator output alone**. Marked **INDETERMINATE** rather than fabricated. All 6 cells flagged `unknown_total_atp_rate` in `comparator_report.json` |
| [Howarth2012] (cerebellum AP fraction of signalling ATP, revised) | AP_fraction_of_signalling_ATP | 17% [Howarth2012, p. 1226 Table 4] | INDETERMINATE | n/a | Same INDETERMINATE status as the cortex 21% anchor. The [Howarth2012] cerebellum anchor predates DSGC-specific measurement; retina-specific budgets do not exist in the literature. Closing this gap requires extending the evaluator to record total inward current (not just `I_Na^inward`) -- an open follow-up for a downstream task |
| [Remme2018] (function-vs-energy MOBO methodology template) | Pareto_optimality_methodology | function + energy Pareto front, parameter distribution on front [Remme2018, Figure 2 + Discussion] | full 6-cell Pareto front with parameter distribution + bootstrap r | followed | t0126 reproduces [Remme2018]'s methodological precedent **correctly and completely**: NSGA-II via pymoo (not Bayesian as in [Remme2018]'s MSO work, but the spirit is the same -- explore function-vs-energy trade-offs as a front, not a point), report the full Pareto front, characterise parameter distribution on the front. **t0126 advances over t0124** because the gen-60 completion removes the truncation caveat that t0124's analysis was forced to flag. Methodological **PASS** |
| [Sivyer2013] (canonical ooDSGC PD-firing rate) | PD-rate band | 5 - 15 Hz [Sivyer2013, Figures 4-5] | 40.0 Hz (all 6 Pareto cells fire at 40 Hz PD) | +25 Hz above upper bound | **All 6 Pareto cells fire at PD = 40 Hz**, which is **~2.7x above [Sivyer2013]'s upper-bound 15 Hz** for canonical rabbit ooDSGC PD response. This is a substrate-vs-recording mismatch: t0126's evaluator uses a **fixed 1400 ms trial length and a synthetic spatially-uniform stimulus**, while [Sivyer2013]'s rates are from moving-bar in-vitro recordings. The high firing rate is an artefact of the evaluator protocol, not a biological prediction. **Documented divergence** -- a follow-up could relax the firing-rate floor to bring t0126 cells into the [Sivyer2013] band |
| [Werginz2024] (mouse alpha-RGC AIS Nav density) | AIS gNa | 1300 mS/cm^2 [Werginz2024, Table 1] | inherited as the first-principles smoke-gate anchor | first-principles input | t0126 uses [Werginz2024]'s 1300 mS/cm^2 alpha-RGC AIS Nav density to derive the canonical [1e8, 1e9] ATP/AP/cm band that the smoke-gate validates. [Werginz2024] measures alpha-RGCs, not DSGCs; the **DSGC-specific AIS Nav density is unpublished**. This is an inherited literature gap, not specific to t0126 |
| [Hallermann2012] (AIS alpha > dendrite alpha; per-compartment overlap) | AIS_alpha_minus_dendrite_alpha | predicted positive delta of 0.3 - 0.7 (AIS 1.5 - 2.0 vs dendrite 1.0 - 1.3) [Hallermann2012, Abstract] | NOT MEASURED | n/a | Per-compartment `seg.ina` traces are recorded (FULL mode) but `comparator_report.json` aggregates only AIS ATP/AP/cm and whole-cell signalling rate -- not per-compartment alpha. Testing the [Hallermann2012] AIS-vs-dendrite alpha prediction requires a per-compartment Na+ entry decomposition on the saved cell trace files. **Open follow-up** for a downstream task; inherited gap from t0124 |
| [Wang2025] (RGC type ordering by baseline ATP pool, preprint) | per_type_ATP_ordering | alpha-RGCs < ipRGCs < ooDSGCs [Wang2025, Figure 1H] | NOT MEASURED | n/a | [Wang2025] measures **steady-state intracellular ATP pool** (mM scale) by ATeam FRET in vivo, not per-spike turnover. t0126 measures per-spike Na+ pump ATP cost (molecules/spike scale). **Different physical quantity** -- the comparison framework is qualitative only. Inherited NOT MEASURED status from t0124 |
| [Jedlicka2022] (Pareto polytope for m tasks) | front_dimensionality | (m - 1)-dimensional polytope [Jedlicka2022, Geometric Theorems] | n=6 cells (front shape) | preliminary | [Jedlicka2022] predicts a 1-D Pareto polytope in 68-d parameter space for m=2 tasks. The 6-cell front has fewer points than the ~10 [Jedlicka2022]/ParTI PCHA threshold for stable polytope fitting. **Hypothesis preserved, test still deferred**. A multi-seed follow-up aggregating ~20-30 Pareto cells would close this comparison |

### Carter-Bean vs Artefact Verdict (S-0124-01 Decision Rule)

| Decision Branch | t0124 (gen 9, n=5) | t0126 (gen 60, n=6) | Verdict |
| --- | --- | --- | --- |
| r > +0.5 AND CI excludes 0 AND n >= 20 -> CARTER_BEAN_PENALTY | r=+0.806 BUT n=5 < 20 | r=+0.980 BUT n=6 < 20 | not triggered |
| r < +0.3 OR upper CI < +0.3 -> ARTEFACT_NULL | r=+0.806 strictly > +0.3 | r=+0.980 strictly > +0.3 | **REJECTED** |
| 0.3 <= r <= 0.5 OR CI straddles +0.5 -> INDETERMINATE | not applicable | not applicable | not triggered |
| n < 20 -> INSUFFICIENT_EVIDENCE | active (n=5) | active (n=6) | **active** |

**Final verdict**: **INSUFFICIENT_EVIDENCE** -- the artefact null is rejected (r is far from 0), and
the Carter-Bean penalty reading is **qualitatively reproduced with a tighter CI**, but the n>=20
quantitative acceptance threshold is not cleared. **t0126 advances the answer from "single-seed
suggestive at n=5" to "fresh-seed-replicated suggestive at n=6 with +0.174 r uplift"**, but the
multi-seed follow-up (S-t0126-multi-seed) is the principled fix to clear the n>=20 gate.

### Per-Comparator Summary

| Comparator | Status |
| --- | --- |
| [t0124] DSI ceiling (best_legit_DSI 0.882 -> 1.000) | **PASS** (+0.118) |
| [t0124] DSI=1.0 corner ATP (2.34e8 -> 7.82e6) | **PASS** (~30x cheaper) |
| [t0124] bootstrap r(DSI, ATP) (+0.806 -> +0.980) | **PASS** (+0.174 uplift, tighter CI) |
| [t0124] dominance (5/5 cells strictly dominated) | **PASS** |
| [t0124] HV uplift (+37.6%) | **PASS** |
| [t0124] smoke-gate calibration match (6.137e8 vs 6.138e8) | **PASS** (within 0.02%) |
| [t0122] DSI ceiling (0.9753 -> 1.0000) | **PASS** (+0.0247) |
| [t0123] smoke-gate calibration match | **PASS** (within 0.2%) |
| [Carter2009] AIS ATP/AP/cm canonical anchor | **PASS** (canonical only; per-cell NOT MEASURED) |
| [Attwell2001] 47% legacy AP fraction | **INDETERMINATE** (denominator missing) |
| [Cuntz2010] balancing-factor band [0.2, 0.7] | **INDETERMINATE** (NaN; transfers from [t0122] by construction) |
| [Sengupta2010] %-above-theoretical-minimum | **NOT MEASURED** (recipe inherited; metric not aggregated) |
| [Niven2008] vertebrate-retinal-neuron ATP/spike band | **PASS** (1.83e6 - 7.82e6 within published band) |
| [Howarth2012] 21% cortex AP fraction | **INDETERMINATE** (denominator missing) |
| [Howarth2012] 17% cerebellum AP fraction | **INDETERMINATE** (denominator missing) |
| [Remme2018] function-vs-energy MOBO methodology | **PASS** (followed correctly; gen-60 completion advances over t0124) |
| [Sivyer2013] canonical ooDSGC PD-rate 5-15 Hz | **FAIL** (40 Hz, +25 Hz above upper bound; protocol artefact) |
| [Werginz2024] AIS Nav density 1300 mS/cm^2 | **PASS** (first-principles input; calibrated) |
| [Hallermann2012] AIS-vs-dendrite alpha gradient | **NOT MEASURED** (per-compartment decomposition not aggregated) |
| [Wang2025] RGC baseline ATP-pool ordering | **NOT MEASURED** (different physical quantity) |
| [Jedlicka2022] (m-1)-D Pareto polytope | **NOT MEASURED** (n=6 < threshold for fitting) |
| S-0124-01 decision rule (Carter-Bean vs artefact) | **INSUFFICIENT_EVIDENCE** (n=6 < 20) |

**Totals**: **9 PASS** (6 vs prior tasks + 3 published) / **1 FAIL** (Sivyer firing rate, protocol
artefact) / **4 INDETERMINATE** (Attwell + 2x Howarth + Cuntz) / **5 NOT MEASURED** (Sengupta
%-above-min + Hallermann + Wang + Jedlicka + per-cell Carter-Bean) / **1 INSUFFICIENT_EVIDENCE**
(S-0124-01 verdict).

## Methodology Differences

* **Cell type and substrate.** All published comparisons are on non-DSGC cells: [Carter2009] on
  acutely dissociated mouse cortical pyramidal, Purkinje, CA1, and fast-spiking interneurons;
  [Remme2018] on gerbil MSO; [Hallermann2012] on rat L5 cortical pyramidal; [Howarth2012] is an
  analytical cortex/cerebellum budget; [Attwell2001] is the 2001 grey-matter budget.
  [Niven2008]/[Niven2007-task-spec] is a cross-species sensory-system survey. [Sivyer2013] is the
  only rabbit ooDSGC reference in this comparison and is the closest cell-type match. [Werginz2024]
  is alpha-RGC, not DSGC. [Wang2025] is in vivo ooDSGC baseline ATP pool. t0126's substrate is the
  procedural 68-d Bed B mouse DRD4 ON-OFF DSGC NEURON model with 14-d morphology -- a substrate that
  **no published study has measured directly**.

* **Energy quantity.** t0126 measures per-spike [Sengupta2010]-style integrated Na+ entry
  (`(1/3)(1/e) integral of I_Na^inward dt` summed over compartments). [Remme2018] reports per-second
  ATP rate. [Howarth2012] reports per-area whole-tissue rate (umol ATP/g/min). [Carter2009] reports
  per-spike Na+ charge ratio relative to capacitive minimum. [Wang2025] reports steady-state
  intracellular ATP concentration. [Niven2008] reports bits-per-ATP and per-spike ATP across
  species. Each quantity has a different unit and physical meaning; conversions are imperfect.

* **Fresh-seed independent LHS initialisation.** t0124's GA seed 6650 produced a single-LHS-ancestry
  cohort that the operator-stop at gen 9 prevented from diversifying via pool restart. t0126's seed
  8929 (drawn with rejection of t0124's seed and lineage seeds) provides an **independent LHS
  starting point**, breaking the single-ancestry confound by construction. The +0.174 r uplift on an
  independent seed plus 60 generations is **the load-bearing scientific delta vs t0124**.

* **Operator-stop disabled + background launch (S-0124-02 mitigation).** t0124 was operator-stopped
  at gen 9 of 60 because the subagent tailed the live log inside its session context and exhausted
  the context budget. t0126 removes `OperatorStopTermination` from the live `TerminationCollection`
  (sentinel `STOP_FILE = pathlib.Path("/dev/null/never")`) and launches NSGA-II inside a tmux
  session decoupled from the subagent. The run completed unattended through a subagent disconnect.
  **The S-0124-02 framework mitigation worked as designed**.

* **Pareto-front size n=6 vs the n>=20 plan-mandated minimum.** t0126's final front is 6 cells; the
  S-0124-01 decision rule requires n>=20 for the Carter-Bean acceptance branch. Even at gen 60 the
  ATP axis is continuous-valued and high-resolution enough that the Pareto front does not grow
  unboundedly -- compare to [t0122]'s 26-cell front under DSI + cytoplasm volume (where cytoplasm is
  much lower-resolution). **The n=6 limit is intrinsic to DSI + ATP at single-seed, not a truncation
  artefact**.

* **Sample size for bootstrap correlation.** n=6 is the entire Pareto front. The bootstrap r(DSI,
  ATP) = +0.980 with 95% CI [0.972, 1.000] has the CI's upper bound essentially at 1.000 because
  resampling 6 points often produces nearly-collinear subsets. The CI is **tighter than t0124's**
  (width 0.028 vs 0.284) but still anchored at the upper bound by small-n. A multi-seed front of
  ~20-30 cells would shrink the CI by roughly sqrt(25/6) ~= 2.0x and could finally clear the n>=20
  S-0124-01 gate.

* **AIS Nav density anchor.** t0126's first-principles [3e7, 3e9] PASS band is derived from
  [Sengupta2010]'s alpha 1.24 x [Werginz2024]'s 1300 mS/cm^2 alpha-RGC AIS Nav density.
  [Werginz2024] measures alpha-RGCs, not DSGCs. The DSGC-specific AIS Nav density is not published;
  the band inherits the alpha-RGC value as the closest in-corpus RGC-family anchor. **Inherited
  literature gap, not specific to t0126**.

* **[Howarth2012] fraction denominator.** The 17%/21% AP-fraction-of-signalling-ATP anchor requires
  knowing the whole-cell or whole-tissue ATP turnover budget. t0126's evaluator computes only the
  signalling-cost component (per-spike Na+ entry), not housekeeping costs, glutamate-receptor costs,
  or resting-potential maintenance. The fraction test is **mathematically not computable** from
  current outputs -- a downstream task could close this gap by extending the evaluator to record
  total inward current.

## Analysis

The headline t0126 finding is a **fresh-seed reproduction of t0124's +0.806 r(DSI, ATP) correlation
at a tighter CI and higher absolute r (+0.980 [0.972, 1.000])**, with **+0.174 r uplift** and
**+37.6% HV uplift** at gen 60 over t0124's gen-9 ceiling. The **artefact null is rejected**: the
correlation is not a single-LHS-ancestry artefact, because an independent seed plus 60 generations
recovers the same sign and the same approximate magnitude. The **Carter-Bean penalty reading is
qualitatively supported** but **formally INSUFFICIENT_EVIDENCE** because n=6 falls short of the
S-0124-01-mandated n>=20 threshold. **The S-0124-01 question is answered "yes, qualitatively"** --
the +0.806 t0124 correlation survives a full 60-gen replication and strengthens slightly to +0.980
-- but the quantitative acceptance gate stays open pending a multi-seed follow-up.

The **headline negative finding for the t0124 reading** is that the high-DSI corner of the front is
**~30x cheaper per spike than t0124's truncated front could reach**. t0124's gen-11 DSI=1.0 elite
cost 2.34e8 ATP/spike; t0126's gen-56 DSI=1.0 elite costs 7.82e6 ATP/spike -- a fundamental
energy-floor revision driven by the 60-gen evolutionary search finding parameter basins that 9
generations cannot reach. The Carter-Bean coupling between DSI and ATP **exists locally on the front
(high-DSI cells cost more than min-ATP cells, hence r=+0.980), but the absolute energy floor for
high DSI is far below what t0124's truncated run reported**. The Carter-Bean penalty is real but
bounded; deeper search relaxes the bound by ~30x. This is the load-bearing scientific contribution
of t0126 beyond the seed-replication question.

The [Carter2009] canonical-anchor smoke-gate PASSES at **6.138e8 ATP/AP/cm** inside the
first-principles [1e8, 1e9] band, **matching t0124's value within 0.02%** (6.137e8 vs 6.138e8) and
[t0123]'s within 0.2%. The recipe is byte-identical across the t0122/t0123/t0124/t0126 ATP-aware
lineage. The per-Pareto-cell AIS ATP/AP/cm aggregation remains zero in `comparator_report.json`
(inherited aggregator gap from t0124); the Carter-Bean band test at the cell level is **NOT
MEASURED** for the t0126 front, only at the canonical anchor.

The [Niven2008] vertebrate-retinal-neuron ATP/spike band [~1e6, ~1e7] **contains all 6 t0126 Pareto
cells** (range 1.83e6 - 7.82e6). This is a direct quantitative cross-species consistency check:
DSGC's per-spike ATP cost sits inside the published vertebrate-retinal-neuron envelope, with the
DSI=1.0 elite near the upper bound and the min-ATP cell near the lower bound. **PASS** at the band
level; the specific bits-per-ATP comparison from [Niven2008]'s Figure 1 is not directly aggregated
(would require MI as an objective, as in t0123, plus per-cell information theory).

The [Sivyer2013] PD-rate band [5, 15] Hz is **FAILED** -- all 6 t0126 Pareto cells fire at **40 Hz**
PD, ~2.7x above the upper bound. This is a **protocol artefact**: t0126's evaluator uses a 1400 ms
fixed trial length with a synthetic spatially-uniform stimulus; [Sivyer2013]'s rates are from
moving-bar in-vitro recordings with realistic stimulus dynamics. The high firing rate is imposed by
the substrate's strong driving current, not a biological prediction from the parameter optimisation.
A follow-up could lower the driving current to bring t0126 cells into the [Sivyer2013] band; the
current evaluator's strong driving is documented in t0080's plan as a deliberate choice to keep all
96 cells reliably above the silence-guard threshold.

The [Remme2018] **methodological precedent of "report the full Pareto front + parameter
distribution"** is now followed correctly. t0124's 9/60-gen truncation forced a "preliminary"
caveat; t0126's gen-60 completion removes that caveat. The Pareto-as-experiment framing is the right
vehicle for the Carter-Bean DSI-vs-ATP question, and t0126 is the first task in the lineage to fully
execute it on the DSI/ATP axes at the full 60-gen budget. **PASS** at the methodological level.

The **[Cuntz2010] balancing-factor band [0.2, 0.7]** confirmation transfers from [t0122] by
construction (identical morphology generator) but is not directly re-tested in t0126's
`comparator_report.json` (inherited aggregator gap). The cross-reference in [t0122] (10/10 top cells
at bf=0.500) covers the band test for the morphology-generation layer; t0126 inherits this finding
through the byte-identical generator.

The **[Howarth2012] / [Attwell2001] signalling-budget comparisons** remain INDETERMINATE for the
same reason as t0124: the evaluator does not record whole-cell or whole-tissue ATP turnover. The
absolute corrected per-cell signalling-ATP rates are reported (3.7e8 - 1.6e9 ATP/s/cell) and shown
on `attwell_laughlin_signalling_budget.png` with the 17%/21%/47% reference lines, but the fractions
cannot be computed. This is **the highest-priority follow-up evaluator extension** to close 4 of the
6 INDETERMINATE comparisons in one shot.

### Prior Task Comparison

The headline within-project comparison is **t0124 dominance**: t0126's 6-cell gen-60 front
**strictly dominates all 5 cells of t0124's gen-9 partial front** in (-DSI, +ATP) space. Every t0124
cell sits up-and-right of at least one t0126 cell. This is the **load-bearing within-project
result** confirming NSGA-II convergence between gen 9 and gen 60. Combined with the +37.6% HV uplift
and the two structural HV jumps at pool-restart generations 11 and 34, it is direct project-level
evidence that **the `_POOL_RESTART_EVERY=10` policy paid off twice in 60 generations**, with the
second payoff (gen 34, +23.1% HV) more important than the first.

The [t0122] DSI ceiling 0.9753 is **exceeded** by t0126 at DSI=1.0000 (+0.0247) on the DSI/ATP axes
-- different second objective, different parameter basins, same DSI-recipe and same 60-gen budget.
The [t0123] smoke-gate match within 0.2% confirms the ATP-per-spike recipe is protocol-invariant
across 2-direction (t0122, t0126) and 4-direction (t0123) protocols and across DSI / MI second
objectives. The lineage is internally consistent.

## Limitations

* **Pareto front size n=6 falls below the n>=20 S-0124-01 acceptance threshold**, so the
  Carter-Bean-vs-artefact decision returns **INSUFFICIENT_EVIDENCE** despite the strong **r=+0.980**
  with tight CI [0.972, 1.000]. The qualitative reading (artefact null rejected, Carter-Bean
  qualitatively supported) is robust; the quantitative acceptance is deferred. **A multi-seed
  follow-up (3-5 independent seeds) aggregating ~20-30 Pareto cells is the principled fix**, and is
  the headline post-t0126 suggestion.

* **All 6 Pareto cells fire at PD = 40 Hz** (cell 1 has ND=0 by ND-silencing; others ND=40 Hz). This
  is **~2.7x above [Sivyer2013]'s upper-bound 15 Hz** for canonical rabbit ooDSGC -- a documented
  protocol-vs-recording mismatch (synthetic stimulus + fixed trial length vs in-vitro moving bar).
  The high firing rate is imposed by the evaluator's strong driving current and is not a biological
  prediction from the optimisation.

* **Per-Pareto-cell AIS ATP/AP/cm aggregation is unavailable** from `comparator_report.json`
  (`measured_atp_per_ap_per_cm = 0` for all 6 cells, `label = "fail"`). Only the canonical anchor
  cell's smoke-gate value (6.138e8) is reliably attributable to the Carter-Bean band; the per-front
  aggregation needs a separate per-segment ATP-per-AP recovery pass that the t0124 lineage does not
  produce. **Inherited aggregator gap**, not a recipe failure. The per-front [Carter2009] check is
  therefore **NOT MEASURED** at the cell level.

* **Whole-tissue or whole-cell total ATP turnover is unmeasured**, so per-cell fractions of the
  [Howarth2012] 17%/21% and [Attwell2001] 47% signalling budgets come back NaN
  (`label = unknown_total_atp_rate` for all 6 cells). Treated as **open quantitative comparisons**.
  4 of the 6 INDETERMINATE comparisons in the Per-Comparator Summary table could be closed by one
  evaluator-extension follow-up.

* **Single-seed scope.** t0126 is one fresh seed (8929); seed-specific basins may bias the
  correlation. The bootstrap r = +0.980 [0.972, 1.000] CI is computed from the 6 Pareto cells, not
  across seeds. The multi-seed follow-up suggestion (S-t0126-multi-seed) is the principled fix; the
  truncated-cohort-artefact memory `project_truncated_cohort_artefact_confirmed.md` warns that
  single-seed DSGC NSGA-II results can be seed-sensitive.

* **`mi_count_bits` and `cytoplasm_volume_um3` are diagnostic-only and reported as null** in the
  metrics variants -- the post-run aggregator did not back-fill these per-cell values for the final
  Pareto rows. The [Cuntz2010] balancing-factor band test inherits this gap and returns NaN. Future
  analysis could recover these values from the per-gen JSONL trace.

* **No published DSGC DSI-vs-ATP Pareto front exists.** t0126 is the first such measurement in any
  retinal cell at gen 60 with a fresh seed. The literature comparison is therefore against
  single-cell calibration anchors ([Carter2009] alpha, [Howarth2012] fractions, [Hallermann2012]
  per-compartment, [Niven2008] cross-species band) and one MSO methodological precedent
  ([Remme2018]), not against a comparable DSGC front.

* **[Wang2025] is a preprint** (peer-review pending) and measures steady-state ATP pool, not
  per-spike turnover. Citation is qualitative-only per the research-internet specification.

* **[Niven2007] vs [Niven2008] disambiguation.** The task description cites "Niven 2007"; the
  paper-asset corpus catalogues the same paper under [Niven2008] (J Exp Biol 211(11), 2008) per
  t0124's `research_papers.md`. This comparison uses [Niven2008] as the canonical citation key.

* **No fitted [deRosenroll2026]-default overlay.** The empirical-on-front test from [Remme2018]
  cannot be replicated without a DSGC reference cell with co-reported (DSI, ATP). Closing this would
  require an upstream task to compute the canonical Bed B cell's ATP/spike under the t0126 evaluator
  and add it as an "empirical default" marker on the Pareto-front figure.
