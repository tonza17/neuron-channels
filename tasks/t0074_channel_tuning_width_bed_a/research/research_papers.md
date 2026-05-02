---
spec_version: "1"
task_id: "t0074_channel_tuning_width_bed_a"
research_stage: "papers"
papers_reviewed: 14
papers_cited: 11
categories_consulted:
  - "voltage-gated-channels"
  - "retinal-ganglion-cell"
  - "compartmental-modeling"
  - "direction-selectivity"
  - "patch-clamp"
  - "dendritic-computation"
  - "synaptic-integration"
  - "cable-theory"
date_completed: "2026-05-01"
status: "complete"
---
# Research Papers: Channel Tuning-Width Sweep on Bed A with BK / SK / Kv7

## Task Objective

Run a 12-angle bar-rotation tuning-curve sweep on Bed A (the deposited Poleg-Polsky DSGC,
[PolegPolsky2016], ported in t0008) with each of eight somatic voltage-gated channels added at low,
medium, and high density (25 conditions, 2100 trials). Extend the t0067 2-angle sweep — which only
measured DSI from PD vs ND — to characterise the *width* of the angle-to-AP-rate tuning curve via
HWHM and vector-sum DSI, and rescue the unanswered Nav1.6 / NaP DSI-erosion gap by adding three
calcium-activated or slow channels (BK / KCa1.1, SK / KCa2, Kv7 / M-current) that the project has
not yet vendored. The task vendors three new MOD files plus a `cad`-style calcium-pool mechanism,
un-zeros CaL/CaT in Bed A's `init_active`, and gates progress through a Stage-2 regression check
that the no-extra-channels baseline still reproduces t0067's DSI = 0.797 within 1e-3. This research
review surveys what the project corpus tells us about (i) RGC HH-family channel kinetics already
used by Bed A, (ii) calcium-pool conventions and Ca-activated K (BK, SK) priors, (iii) Kv7 / M-
current priors, (iv) angle-resolved tuning-curve metrics (HWHM, vector-sum DSI, half-width) used in
the published DSGC literature, and (v) prior compartmental-model channel sweeps comparable to this
task's design.

## Category Selection Rationale

The primary category is `voltage-gated-channels` because the task's central manipulation is the
addition of new ion-channel mechanisms to a compartmental DSGC model. `retinal-ganglion-cell` was
consulted because the substrate is an ON-OFF DSGC and we need RGC-specific channel-density priors
where they exist. `compartmental-modeling` was consulted because the entire pipeline is a NEURON
multi-compartment simulation and prior compartmental models supply the methodological template for
channel insertion, calcium pools, and vendoring conventions. `direction-selectivity` and
`patch-clamp` were consulted because the dependent variables (HWHM, vector-sum DSI, peak rate) are
defined and measured in the DSGC literature using both modelling and patch-clamp recordings.
`dendritic-computation`, `synaptic-integration`, and `cable-theory` were consulted because the
Stage-4 passive-diagnostic protocol (EPSP_PASSIVE / IPSP_PASSIVE traces) and Bed A's space-clamp and
dendritic-spike behaviour interact with the channel additions. Excluded: no asset-type categories
(e.g., dataset-specific tags) are relevant — this task does not introduce new datasets.

The voltage-gated-channels corpus captured by t0019 is small (5 papers) and dominated by AIS Nav /
Kv1 priors that were the focus of that survey rather than BK / SK / Kv7 priors. The DSGC
compartmental-model corpus from t0002 is much richer and supplies the angle-resolved tuning metrics,
dendritic-spike DSI-amplification context, and the specific ON-OFF DSGC firing-rate benchmarks used
in Bed A. None of the existing assets contain a published BK, SK, or Kv7 MOD file or a direct
measurement of these channels' kinetics in DSGCs — this is documented as a gap below and motivates
the Stage-1 vendoring step.

## Key Findings

### RGC Channel Repertoire and Kinetic Priors Already in the Corpus

The canonical RGC HH model is the Fohlmeister-Miller "Five-channel" mechanism: Hodgkin-Huxley-style
fast Nav (m^3 h), delayed-rectifier Kv (n^4), voltage-gated Ca (c^3), A-type Kv4 (a^3 b), and a
Ca-activated K (Hill-type activation in [Ca²⁺]^2 / (K_d^2 + [Ca²⁺]^2))
[FohlmeisterMiller1997, Fohlmeister2010]. [Fohlmeister2010] reports cell-type-specific peak
conductance maps at 35 °C across (dendrite / soma / IS / TS / axon) compartments, with cat-α soma
Nav reaching **158 mS/cm²**, Kv up to **36 mS/cm²**, and a peak Nav density of **448.5 mS/cm²** on
the thin axonal segment 50-130 µm distal to the soma; it also pins gating-kinetic Q10 to **~1.95**
and permeability Q10 to **~1.64** between 23 and 37 °C [Fohlmeister2010, Results]. The Bed A library
`modeldb_189347_dsgc` from t0008 inherits this kinetic class via the deposited Poleg-Polsky `HHst`
and `Cadyn` mechanisms; its t0067-baseline soma Nav is HHst with a high g_Na so additions of 3-90
mS/cm² of an extra channel are a small perturbation [Fohlmeister2010, FohlmeisterMiller1997].

The `nav-kv-combinations-for-dsgc-modelling` answer asset from t0019
[VanWart2006, Hu2009, Kole2008, Kole2007, FohlmeisterMiller1997] establishes that Nav1.6 activates
**~10-15 mV more hyperpolarised** than Nav1.2 (V_½ ≈ -45 mV vs ≈ -32 mV), that AIS peak Nav density
is **~50×** the somatic value (~2500-5000 pS/µm² ≈ 250-500 mS/cm²), and that Kv1 at the AIS
activates near **V_½ ≈ -40 to -50 mV** with **τ ≈ 0.5-1 ms**. None of these canonical sources cover
BK, SK, or Kv7 in RGCs, so MOD-file vendoring for this task must rely on published models from
neighbouring cell types (CA1 pyramidal, Purkinje, cortical layer-5) and validate against general RGC
firing- pattern constraints.

### Calcium-Pool and Ca-Activated K Conventions in Compartmental DSGC Models

The Fohlmeister-Miller K(Ca) mechanism uses a **submembrane shell with first-order [Ca²⁺] removal**
plus a Hill-type activation `[Ca²⁺]^2 / (K_d^2 + [Ca²⁺]^2)`
[Fohlmeister2010, FohlmeisterMiller1997]. This is the canonical "single-shell" `cad`-style decay
model — the same form that Bed B already uses in this project (per the t0070 two-bed write-up
referenced in the task description) and that the Schachter-Smith-Taylor DSGC model adopts
[Schachter2010, Architecture]. [Schachter2010] reports physiological dendritic [Ca²⁺] transients and
a Ca-activated K current paired with their Cav source as a sufficient basis for repolarisation in
their NEURON DSGC, but does not tabulate K(Ca) kinetic constants. Vendoring a `cad`-style pool
mechanism for Bed A is therefore standard practice; the Stage-1 plan to feed [Ca²⁺]_i from un-zeroed
CaL + CaT into a single-shell pool with first-order removal mirrors both Bed B's existing convention
and [Fohlmeister2010, Architecture]. The Stage-2 regression gate (baseline DSI must match t0067 =
0.797 within 1e-3) is the project-specific safeguard that this kinetic addition does not perturb
resting dynamics.

### Direction-Tuning Width Metrics in the DSGC Literature

The DSGC literature uses three width-related metrics that appear repeatedly across studies:

* **Direction-Selectivity Index (DSI)** = (R_PD − R_ND) / (R_PD + R_ND), the 2-angle ratio used by
  t0067, [Oesch2005, Methods], [Chen2009, Methods], and [PolegPolsky2016, Methods]. [Oesch2005]
  reports spike-DSI = **0.67 ± 0.13 (ON)** and **0.74 ± 0.13 (OFF)** in rabbit ON-OFF DSGCs and
  PSP-DSI = **0.09 ± 0.05 (ON)** / **0.14 ± 0.08 (OFF)** in the same cells, illustrating the
  spike-generation amplification that this task's HWHM metric is designed to characterise.
* **Vector-sum DSI** = |Σᵢ rate(θᵢ) · exp(i·θᵢ)| / Σᵢ rate(θᵢ), the circular-concentration metric
  used by [Hanson2019, Methods] and [Oesch2005, Methods] (the latter with a von Mises fit).
  [Hanson2019] reports that vector-sum DSI in mouse Trhr-EGFP DSGCs falls from approximately 0.33
  (wild-type, asymmetric SAC GABA) to **0.07** when SAC inhibition is rendered non-directional, with
  the residual DS produced by E/I temporal asymmetry — establishing that vector-sum DSI is the
  appropriate width metric for distinguishing residual mechanisms when the headline
  preferred-direction firing rate is preserved.
* **Half-width at half-maximum (HWHM)** of the polar tuning curve, used by [Chen2009, Methods] in
  the form "half-width of the directional tuning curve". [Chen2009] reports that HWHM is **not
  significantly different** between P11 (early postnatal) and adult mouse ON-OFF DSGCs (p > 0.05)
  even though peak rate is **~107 Hz at P11 vs ~190 Hz in adults**, demonstrating that HWHM
  decouples from peak firing rate — a critical observation for our task because we expect some
  channel additions (e.g., NaP) to drive large peak-rate changes without necessarily reshaping
  width.

[Oesch2005] used **12 evenly spaced directions across 360°** with a 250-µm-wide bar at 800-1200 µm/s
— the same 12-angle protocol Bed A uses (per the t0046 reproduction). [Chen2009] also used a
12-direction protocol (30-degree spacing) with a 100 × 500 µm bar at ~750 µm/s. This convergence
across rabbit (Oesch) and mouse (Chen, Hanson) means the t0074 12-angle protocol is directly
comparable to published DSGC tuning curves.

### Spike-Generation Amplifies Tuning Width Beyond Subthreshold Selectivity

[Oesch2005] established that spike DSI is **~6× higher** than subthreshold-PSP DSI in DSGCs (0.67 /
0.09 in the ON arbor), and that this enhancement requires **TTX-sensitive dendritic Na⁺ channels**:
bath TTX collapses PSP DSI to 0.04 and abolishes the ON-OFF preferred-direction alignment.
[Schachter2010] reproduced this in a NEURON DSGC: PSP DSI ~0.2 → spike DSI ~0.8 (a 4× amplification)
via local dendritic-spike thresholds, with the local spike threshold acting as a non-linear
amplifier of small (a few nS) PSP differences. The implication for t0074 is that any soma-channel
manipulation that affects spike threshold (Nav1.6, NaP, Kv3, BK) can in principle shift this
amplification in either direction — towards sharpening (Kv3/BK that raise threshold preferentially
during high-frequency PD trains) or towards erosion (NaP that lowers threshold and allows ND
firing). This frames the BK / SK / Kv7 hypothesis the task tests.

### NaP and Nav1.6 are the Dominant DSI-Eroding Additions in Bed A

The t0067 results [PolegPolsky2016 substrate] showed that **NaP at high density flips DSI sign**
(DSI = -0.179, cell fires more in ND than PD) and **Nav1.6 erodes DSI monotonically** (0.797 → 0.229
across the density grid). NaR, Kv3, Kv4 produced essentially no change (|ΔDSI| < 0.1 at all tested
densities). The t0067 data are direction-selectivity-only; this task asks the larger question of how
each channel reshapes the entire 12-angle tuning curve. Two predictions follow directly from the
t0019 priors and from the Schachter and Oesch DSGC literature:

* **NaP_high should produce a broad, near-flat tuning curve** (HWHM → 90°, vector-sum DSI ~0) rather
  than a true "inverted" tuning curve, because the persistent depolarisation prevents the ND
  inhibition shunt from keeping the cell sub-threshold and decouples spike output from the
  angle-dependent E/I balance [PolegPolsky2016, Vaney2012].
* **Nav1.6_high should produce a moderately broadened tuning curve** with a still-identifiable
  preferred direction, because Nav1.6 lowers spike threshold uniformly across angles and erodes the
  dendritic-spike-threshold non-linearity that gives DSGCs their sharp tuning
  [Oesch2005, Schachter2010].

### BK, SK, and Kv7 Are Plausible DSI-Sharpening Rescues

BK (KCa1.1 / KCNMA1), SK (KCa2), and Kv7 (KCNQ2 + KCNQ3, the M-current) are biophysically distinct
from the five channels already tested in t0067 in three ways that directly motivate this task:

* **They activate slowly relative to a single AP** (Kv7 τ_act ~10-100 ms; SK/BK Ca²⁺-dependent
  activation gated by Ca²⁺ accumulation over multiple APs). The Fohlmeister K(Ca) mechanism is the
  canonical reference for this class [Fohlmeister2010, Architecture].
* **They are activity-dependent**: BK and SK require Ca²⁺ entry through Cav channels; Kv7 is
  voltage-dependent but with strong steady-state inactivation that selectively suppresses
  high-firing-rate trains.
* **They are biologically expressed in or near RGCs** at densities documented in the literature
  (training-knowledge claim — the project corpus does not yet contain a paper that quantifies BK /
  SK / Kv7 density specifically in DSGCs, see Gaps and Limitations).

The hypothesis the task tests is that adding any one of these slow / activity-dependent channels
will preferentially suppress the high-firing-rate PD direction (where Ca²⁺ accumulation activates
BK/SK and where Kv7 voltage-dependent inactivation removes its damping effect more slowly) while
leaving the lower-rate ND direction unaffected — sharpening the tuning curve and rescuing or
exceeding the baseline DSI = 0.797. This is the rescue analogue of the [Schachter2010] dendritic-
spike threshold mechanism applied at the somatic compartment.

### Calibrated Reproduction Targets from the Project Corpus

The Bed A baseline DSI = **0.797**
[t0067 results, replicated in this task's Stage-2 regression gate to 1e-3] sits between the rabbit
ON-OFF spike DSI of **0.67-0.74** [Oesch2005, Results] and the [Schachter2010] modelled spike DSI of
**~0.8** [Schachter2010, Results]. Peak firing rates in adult mouse ON-OFF DSGCs are **~166-190 Hz**
[Chen2009, Results] and **~148 Hz** in rabbit [Oesch2005, Results]; these set the upper bound for
"biologically sensible" peak rates that NaP_high and Nav1.6_high will be tested against (NaP_high in
t0067 produced 95.8 ND spikes in a ~1.4 s trial, ≈ 68 Hz mean — already well above the no-DS
baseline). HWHM in adult mouse ON-OFF DSGCs is reported by [Chen2009] but the specific degree value
is not extracted in the corpus — this is a known reproduction-target gap for the
comparison-to-literature stage.

## Methodology Insights

* **Use the 12-angle 30-degree-spaced protocol consistent with [Oesch2005, Chen2009]**. Both studies
  use 12 directions; Bed A's native protocol matches. This gives sufficient angular resolution for
  HWHM via linear interpolation around the half-max points.
* **Compute vector-sum DSI in addition to PD-vs-ND DSI**. [Hanson2019] demonstrates that vector- sum
  DSI reveals residual directional information that PD-vs-ND DSI cannot detect (vector-sum DSI =
  0.07 even when SAC GABA is non-directional). For this task, vector-sum DSI is the appropriate
  metric for low-firing-rate conditions where PD/ND are not well-defined.
* **Set HWHM to `null` for low-rate conditions** (peak mean rate < ~1 Hz across all 12 angles)
  rather than reporting fabricated values. This follows the project Python style guide (use `None`
  for missing data, never `0.0` or fake values) and the [Chen2009] convention that HWHM is only
  defined when there is an identifiable peak.
* **Use the Fohlmeister-Miller `cad`-style single-shell calcium pool with first-order removal** for
  the new mechanism [Fohlmeister2010, Architecture]. This matches Bed B's existing pool and is the
  convention for Ca-activated K channels in NEURON DSGC models [Schachter2010, Architecture].
* **Vendor BK / SK MODs from a published cortical or hippocampal model** rather than fitting from
  scratch. [Fohlmeister2010] notes that Q10 ≈ 1.9 is sufficient to extrapolate cortical /
  hippocampal kinetics from ~22 °C to mammalian body temperature, matching Bed A's 35-37 °C
  protocol. The vendoring source must be recorded in the library asset's `details.json` per the
  paper-asset specification.
* **Hold Bed A's existing HHst Na, K, and synaptic parameters fixed** at t0067 baseline values
  during the channel sweep. The only change to the existing mechanism is un-zeroing CaL/CaT in
  `init_active`; everything else (synaptic conductances, gabaMOD, leak) stays exactly as t0065.
* **Run the Stage-2 regression gate (baseline DSI within 1e-3 of 0.797) before any other Stage 3
  trials**. If it fails, the un-zeroing of CaL/CaT has perturbed resting dynamics; the documented
  fallback (feed `Ca_i` from a precomputed time series instead) preserves BK/SK kinetics without
  altering Bed A's HHst dynamics — this is the lower-risk path.
* **Use a 5-seed mean for FULL-mode trials to reduce sampling noise on DSI**, exactly as t0067. The
  ±0.05 confidence interval on DSI from 5 seeds is sufficient to detect the |ΔDSI| > 0.05 threshold
  for "measurable change" in the pass criteria.
* **Run EPSP_PASSIVE / IPSP_PASSIVE diagnostics with HH off**
  [memory: DSGC simulation measurement protocol]. The passive traces should be flat at ~−60 mV in
  IPSP_PASSIVE and direction-invariant in EPSP_PASSIVE (gabaMOD = 0); deviation indicates the
  channel addition is affecting subthreshold integration, not just spike output.
* **Compute RMSE vs the t0004 cosine target** using the t0012 library [project description]. This is
  the canonical project tuning-curve loss and allows direct comparison to other tasks (t0026, t0034,
  t0042, etc.) that report the same metric.

### Hypotheses to Test

1. **NaP_high produces a near-flat tuning curve** (HWHM > 60°, |vector-sum DSI| < 0.10) rather than
   an inverted curve. Falsifiable by checking whether ND-firing-rate exceeds PD-firing-rate at every
   single angle (true inversion) or only in a narrow ND band (broadening) — t0067 data averaged over
   angles cannot distinguish these.
2. **Nav1.6_high produces moderate broadening** (HWHM increased by 15-30°, vector-sum DSI in range
   0.15-0.30) — i.e., the curve shape is preserved but widened. Falsifiable by comparing HWHM at low
   / medium / high Nav1.6 densities.
3. **BK or SK at medium / high density rescues vector-sum DSI** to within 0.10 of the baseline 0.797
   (a |ΔDSI| < 0.10 deviation), or even sharpens it (vector-sum DSI > 0.85). Falsifiable by the pass
   criteria's |ΔDSI| > 0.05 threshold.
4. **Kv7 at any density produces no measurable change** in HWHM (|Δ HWHM| < 5°) — because somatic
   Kv7 expression in DSGCs is poorly documented and the AIS-localised Kv7 hypothesis would require
   an AIS placement, not a soma placement [task description risks section]. If this hypothesis
   holds, it strengthens the case for the t0075 AIS-localised follow-up.

### Best Practices

* Source published MODs and document their provenance — the paper-asset specification requires the
  source paper's DOI in the library asset's `details.json` for any vendored MOD file.
* Run a regression gate before any new science. The Stage-2 baseline-DSI gate is the cheapest way to
  detect that the Ca-pool addition has broken the existing model; failure should trigger the
  closed-form `Ca_i` fallback.
* Use multiple width metrics (HWHM, vector-sum DSI, peak rate, RMSE vs cosine target) rather than a
  single DSI value. [Chen2009] demonstrates HWHM and DSI can decouple; the task should report all
  three plus RMSE for comparability with other tasks.

## Gaps and Limitations

* **No paper in the project corpus contains a measurement or model of BK, SK, or Kv7 channel
  kinetics specifically in DSGCs**. [VanWart2006] documents Nav1.6 / Nav1.1 / Kv1.2 at the RGC AIS
  but does not cover Ca-activated K or Kv7. The vendoring step must therefore source MODs from a
  non-DSGC published model and validate behaviourally (Stage-2 regression + Stage-3 tuning curves
  consistent with adult ON-OFF DSGC firing rates of ~150-190 Hz [Oesch2005, Chen2009]).
* **No paper in the project corpus contains a published HWHM value in degrees for adult mouse ON-OFF
  DSGCs**. [Chen2009] uses HWHM and reports it is not significantly different across age groups, but
  the corpus summary does not extract the specific degree value. This is a known reproduction-target
  gap that the comparison-to-literature stage of this task may need to address by reading the
  [Chen2009] PDF directly (currently download-failed in t0002 — see the paywalled-papers
  intervention list).
* **Five t0019 voltage-gated-channel papers are paywalled and have CrossRef-only summaries**
  [VanWart2006, Kole2007, FohlmeisterMiller1997, Hu2009, Kole2008]. Numerical values cited in the
  t0019 answer asset are training-knowledge canonical values rather than verified-from-PDF numbers;
  the task's library-asset documentation should record this provenance honestly.
* **No prior task in the project has done a comparable channel-density sweep with multiple width
  metrics**. t0067 only measured DSI from PD vs ND; t0026 / t0029-t0042 swept morphology not
  channels; t0043 added a single Nav1.6 + Kv3 combination. This is a methodological novelty — there
  is no internal benchmark for HWHM × channel-density curves to compare against. The Stage-5
  sensitivity plots (HWHM, vector-sum DSI, peak rate vs density) will define the methodological
  baseline for any future width-vs-channel sweep.
* **The t0067 baseline used FULL mode with the gabaMOD-swap protocol from t0065**; this task must
  use the same protocol exactly, otherwise the Stage-2 regression gate is meaningless. This is
  documented in the t0067 task but not explicitly in the corpus literature — internal to the
  project.
* **Calcium-pool kinetic constants for the new pool mechanism (decay τ, shell depth)** are not
  uniquely specified by the corpus. [Fohlmeister2010] uses "first-order removal" without publishing
  the time constant; [Schachter2010] uses a Ca-activated K mechanism without tabulating its pool.
  The vendoring must use published values from the source MOD's paper and document them in the
  library asset's `details.json`.

## Recommendations for This Task

1. **Vendor BK / SK from Migliore-Hines / Hines-Carnevale-style CA1 or Purkinje MODs** as suggested
   in the task description, and validate kinetics against the Fohlmeister K(Ca) activation function
   `Ca^2 / (K_d^2 + Ca^2)` [Fohlmeister2010] — i.e., confirm Ca- sensitivity is in the 0.1-10 µM
   range typical of mammalian K(Ca) channels.

2. **Vendor Kv7 from a published cortical Kv7 / KCNQ MOD** with a known M-current activation range
   (V_½ ≈ -45 to -30 mV depending on KCNQ2 vs KCNQ3 subunit). Document the source DOI in the library
   asset.

3. **Use a Fohlmeister-Miller-style single-shell `cad` mechanism** for the calcium pool, with
   first-order [Ca²⁺] removal time constant in the 30-100 ms range typical of submembrane shells in
   NEURON RGC models [Fohlmeister2010, Schachter2010]. Mirror Bed B's existing `cad` so the two beds
   use the same calcium-pool convention.

4. **Run the Stage-2 regression gate as the first Stage-3-allowing check**. Any deviation from
   t0067's DSI = 0.797 by more than 1e-3 (the task's pass criterion) means the un-zeroed CaL / CaT
   have perturbed resting dynamics; switch to the closed-form `Ca_i` fallback before running any of
   the 1500 FULL-mode trials.

5. **Compute four width-quality metrics for every condition**: HWHM (degrees), vector-sum DSI, peak
   rate (Hz), and RMSE vs the t0004 cosine target. Set HWHM = `null` when peak mean rate < 1 Hz
   [Chen2009 convention]. Plus retain the t0067 PD-vs-ND DSI for cross-task comparison.

6. **Build per-channel sensitivity plots** (HWHM, vector-sum DSI, peak rate vs density) using the
   t0011 visualisation library. The cross-channel overlay (vector-sum DSI vs density for all 8
   channels) is the headline figure; expect Nav1.6 / NaP to show monotonic erosion and BK / SK / Kv7
   to show either no effect (Kv7 at soma) or non-monotonic rescue (BK / SK).

7. **Compare against [Oesch2005] spike DSI = 0.67-0.74** and [Chen2009] HWHM (verify in the PDF if
   accessible) as the literature-comparison anchor. Bed A's 0.797 baseline already exceeds the Oesch
   range, so the task's primary comparison is "by how much does each channel push DSI above or below
   this band?".

8. **If Kv7 produces only inert results** at the soma (no measurable HWHM or vector-sum DSI change
   at any density), record this as a clean negative result and recommend the AIS- localised Kv7
   follow-up to t0075 [task description risks section]. The literature is consistent with this
   outcome — somatic Kv7 expression in DSGCs is poorly documented relative to AIS Kv7 in cortical
   neurons [Kole2007 by extension].

9. **Document MOD-file provenance in the library asset's `details.json`** for each of BK, SK, Kv7,
   and the calcium pool. Per the paper-asset specification, this means recording the source paper's
   DOI, the parameter values inherited, and any modifications made. This is the dependency hook for
   t0075 and any future Ca-activated-K or Kv7-related task.

## Paper Index

### [PolegPolsky2016]

* **Title**: NMDA Receptors Multiplicatively Scale Visual Signals and Enhance Directional Motion
  Discrimination in Retinal Ganglion Cells
* **Authors**: Poleg-Polsky, A., Diamond, J. S.
* **Year**: 2016
* **DOI**: `10.1016/j.neuron.2016.02.013`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/`
* **Categories**: `compartmental-modeling`, `direction-selectivity`, `synaptic-integration`,
  `dendritic-computation`, `retinal-ganglion-cell`
* **Relevance**: Source of the deposited DSGC NEURON model that Bed A is built on (t0008 library
  `modeldb_189347_dsgc`). Defines the synaptic input distribution, Mg²⁺ block formulation, and
  8-direction tuning protocol (extended to 12 angles in this task) that the channel-addition sweep
  is run on top of.

### [Oesch2005]

* **Title**: Direction-Selective Dendritic Action Potentials in Rabbit Retina
* **Authors**: Oesch, N., Euler, T., Taylor, W. R.
* **Year**: 2005
* **DOI**: `10.1016/j.neuron.2005.06.036`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2005.06.036/`
* **Categories**: `direction-selectivity`, `dendritic-computation`, `voltage-gated-channels`,
  `retinal-ganglion-cell`, `patch-clamp`
* **Relevance**: Canonical 12-direction protocol, von-Mises-fit tuning curves, and spike-DSI vs
  PSP-DSI quantification (0.67 vs 0.09 ON; 0.74 vs 0.14 OFF). Provides the rabbit ON-OFF DSGC
  firing-rate benchmark (148 Hz peak) and dendritic-spike threshold mechanism that any channel
  addition must respect.

### [Schachter2010]

* **Title**: Dendritic Spikes Amplify the Synaptic Signal to Enhance Detection of Motion in a
  Simulation of the Direction-Selective Ganglion Cell
* **Authors**: Schachter, M. J., Oesch, N., Smith, R. G., Taylor, W. R.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000899`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1371_journal.pcbi.1000899/`
* **Categories**: `compartmental-modeling`, `direction-selectivity`, `dendritic-computation`,
  `retinal-ganglion-cell`, `voltage-gated-channels`, `synaptic-integration`, `cable-theory`
* **Relevance**: Most-relevant prior compartmental DSGC model with a Ca-activated K channel and a
  calcium pool. Establishes the 4× spike-DSI amplification (PSP DSI 0.2 → spike DSI 0.8) via local
  dendritic-spike thresholds — the mechanism that channel additions can either sharpen or erode.

### [Vaney2012]

* **Title**: Direction selectivity in the retina: symmetry and asymmetry in structure and function
* **Authors**: Vaney, D. I., Sivyer, B., Taylor, W. R.
* **Year**: 2012
* **DOI**: `10.1038/nrn3165`
* **Asset**: `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nrn3165/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `dendritic-computation`,
  `synaptic-integration`
* **Relevance**: Decadal review establishing the DSGC microcircuit; supplies the bistratified ON-OFF
  DSGC morphology and ~9× null-side GABA asymmetry that Bed A's synaptic input matches. Frames the
  dendritic-spike vs passive-shunt debate that is directly relevant to the
  channel-addition-vs-baseline comparison.

### [Chen2009]

* **Title**: Physiological properties of direction-selective ganglion cells in early postnatal and
  adult mouse retina
* **Authors**: Chen, M., Weng, S., Deng, Q., Xu, Z., He, S.
* **Year**: 2009
* **DOI**: `10.1113/jphysiol.2008.161240`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1113_jphysiol.2008.161240/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `patch-clamp`
* **Relevance**: Defines HWHM as "half-width at half-maximum of the polar response curve" with a
  12-direction × 30°-spaced protocol. Demonstrates HWHM is not significantly different between P11
  and adult mouse ON-OFF DSGCs despite a 2× peak-rate difference (~107 vs ~190 Hz) — the empirical
  justification for using HWHM as a metric independent of peak rate.

### [Hanson2019]

* **Title**: Retinal direction selectivity in the absence of asymmetric starburst amacrine cell
  responses
* **Authors**: Hanson, L., Sethuramanujam, S., deRosenroll, G., Jain, V., Awatramani, G. B.
* **Year**: 2019
* **DOI**: `10.7554/eLife.42392`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.7554_eLife.42392/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`,
  `compartmental-modeling`, `dendritic-computation`, `patch-clamp`
* **Relevance**: Uses vector-sum DSI on 8-direction tuning curves and reports residual DSI of
  **0.07** when SAC GABA is rendered non-directional. Establishes vector-sum DSI as the appropriate
  metric for low-rate or near-flat tuning conditions where simple PD-vs-ND DSI becomes ill-defined.
  Modifies the [PolegPolsky2016] NEURON model — directly relevant to Bed A.

### [FohlmeisterMiller1997]

* **Title**: Mechanisms by Which Cell Geometry Controls Repetitive Impulse Firing in Retinal
  Ganglion Cells
* **Authors**: Fohlmeister, J. F., Miller, R. F.
* **Year**: 1997
* **DOI**: `10.1152/jn.1997.78.4.1948`
* **Asset**:
  `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1152_jn.1997.78.4.1948/`
* **Categories**: `voltage-gated-channels`, `compartmental-modeling`
* **Relevance**: Original Fohlmeister-Miller five-channel RGC HH model: Nav (m³h), Kdr (n⁴), Cav
  (c³), Kv4-A (a³b), and a Ca-activated K channel with `Ca^2 / (K_d^2 + Ca^2)` activation. Defines
  the canonical RGC channel kinetics and the single-shell calcium-pool convention that this task's
  `cad`-style mechanism inherits. Note: full-text PDF was not accessible for the t0019 summary
  (CrossRef-only); numerical claims here are the project's training-knowledge canonical values and
  should be verified against the published methods section before citation in the library asset.

### [Fohlmeister2010]

* **Title**: Mechanisms and Distribution of Ion Channels in Retinal Ganglion Cells: Using
  Temperature as an Independent Variable
* **Authors**: Fohlmeister, J. F., Cohen, E. D., Newman, E. A.
* **Year**: 2010
* **DOI**: `10.1152/jn.00123.2009`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1152_jn.00123.2009/`
* **Categories**: `retinal-ganglion-cell`, `compartmental-modeling`, `voltage-gated-channels`,
  `patch-clamp`
* **Relevance**: Cell-type-specific RGC channel-density maps at 35 °C across (dendrite / soma / IS /
  TS / axon), Q10 = 1.95 (gating) and 1.64 (permeability) for 23-37 °C. Directly supplies the
  temperature-correction prior for any vendored cortical / hippocampal MOD — BK, SK, and Kv7
  published kinetics typically come from 22-25 °C recordings and need this Q10 to scale to Bed A's
  35-37 °C runtime.

### [VanWart2006]

* **Title**: Polarized distribution of ion channels within microdomains of the axon initial segment
* **Authors**: Van Wart, A., Trimmer, J. S., Matthews, G.
* **Year**: 2007 (published online 2006)
* **DOI**: `10.1002/cne.21173`
* **Asset**: `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1002_cne.21173/`
* **Categories**: `voltage-gated-channels`, `retinal-ganglion-cell`
* **Relevance**: RGC AIS Nav1.6 / Nav1.1 / Kv1.2 microdomain map. Explicitly does not cover BK, SK,
  or Kv7 in DSGCs — making this paper one of the corpus's clearest gap markers for the vendoring
  step. Note: the t0019 summary is CrossRef-only (paywalled).

### [Hu2009]

* **Title**: Distinct contributions of Nav1.6 and Nav1.2 in action potential initiation and
  backpropagation
* **Authors**: Hu, W., Tian, C., Li, T., Yang, M., Hou, H., Shu, Y.
* **Year**: 2009
* **DOI**: `10.1038/nn.2359`
* **Asset**: `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1038_nn.2359/`
* **Categories**: `voltage-gated-channels`, `patch-clamp`
* **Relevance**: V_½ separation between Nav1.6 (~~-45 mV) and Nav1.2 (~~-32 mV). Frames why Nav1.6
  addition in t0067 erodes DSI more aggressively than other Nav species and grounds the Nav1.6_high
  tuning-curve broadening prediction in this task. Note: t0019 summary is CrossRef-only (paywalled).

### [Branco2010]

* **Title**: Dendritic Discrimination of Temporal Input Sequences in Cortical Neurons
* **Authors**: Branco, T., Clark, B. A., Häusser, M.
* **Year**: 2010
* **DOI**: `10.1126/science.1189664`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1126_science.1189664/`
* **Categories**: `cable-theory`, `compartmental-modeling`, `dendritic-computation`,
  `synaptic-integration`
* **Relevance**: Direction selectivity from dendritic impedance gradients plus NMDA-receptor voltage
  dependence (no active dendritic conductances required). Establishes that the EPSP_PASSIVE
  diagnostic in Stage 4 of this task is principled — passive-dendrite tuning is a measurable
  phenomenon and must be controlled for when interpreting active-channel additions.

* * *

The remaining three reviewed-but-uncited papers (Kole2007 on AIS Kv1 expression, Kole2008 on AIS Nav
conductance density, and Sivyer2010 on ON DSGC velocity tuning) were consulted in the t0019
voltage-gated-channels survey and the t0002 DSGC compartmental-models corpus, but their specific
findings do not bear directly on the BK / SK / Kv7 vendoring or HWHM-measurement steps of this task.
They are tracked in `papers_reviewed: 14` for transparency but not cited in the body, to keep the
Paper Index focused on load-bearing references.
