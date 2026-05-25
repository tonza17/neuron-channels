---
spec_version: "1"
task_id: "t0124_bedb_dsi_atp_per_spike_nsga2"
research_stage: "papers"
papers_reviewed: 21
papers_cited: 21
categories_consulted:
  - "compartmental-modeling"
  - "direction-selectivity"
  - "retinal-ganglion-cell"
  - "dendritic-computation"
  - "voltage-gated-channels"
  - "patch-clamp"
  - "synaptic-integration"
date_completed: "2026-05-25"
status: "complete"
---
# Research Papers - 68-d NSGA-II Maximising DSI and Minimising ATP-per-Spike on Bed B + Morphology

## Task Objective

t0124 runs a single-seed NSGA-II on the 68-d Bed B + 14-d morphology substrate validated by t0106-
t0115 and exercised verbatim by t0122 (DSI vs cytoplasm volume) and t0123 (MI vs ATP-per-spike).
Both objectives change from t0123: DSI replaces mutual information (function objective is the
silence-guarded antipodal ratio `(R_PD - R_ND) / (R_PD + R_ND)` with R_PD >= 3 spikes guard from
t0122), and the ATP-per-spike recipe of [Sengupta2010] is inherited verbatim from t0123 as the
energy objective (`(1/3) * (1/e) * sum_compartments int(I_Na^inward) dt`, lower is better). The
direction protocol drops from t0123's 4 angles (0/90/180/270 deg) to t0122's antipodal pair (0/180
deg) because DSI needs only one antipodal pair and ATP-per-spike is direction-independent under
per-spike normalisation. Hard constraints reproduced verbatim from t0122 / t0123 are
`_POOL_RESTART_EVERY=10`, `HV_PLATEAU_AUTO_STOP=False`, `POP_SIZE=96`, `N_EVAL_SEEDS=3`,
`N_GEN_MAX=60`, `COST_CAP_USD=6.0`. The smoke-gate verifies that the canonical Bed B cell's
AIS-compartment ATP-per-AP matches the Carter and Bean 2009 ~4 mM-mol/cm benchmark within 30% before
NSGA-II launches; if the smoke-gate fails, the recipe is debugged. This research stage extracts the
prior on (i) where the published DSGC DSI-vs-ATP-per-spike Pareto front sits relative to the
Attwell-Laughlin 2001 cortical signalling-ATP budget and the Carter-Bean 2009 AIS calibration
benchmark, (ii) which DSI biophysical mechanisms are consistent with low ATP cost vs which
mechanisms inflate the Na/K overlap factor, and (iii) what NSGA-II convergence and noise- handling
priors apply at the 68-d, 2-direction, pop = 96 operating point.

## Category Selection Rationale

Seven `meta/categories/` are consulted. **`compartmental-modeling`** is core because every relevant
NSGA-II / MOO methodology reference, the ATP-per-spike recipe paper [Sengupta2010], and the cortical
energy-budget anchor [Attwell2001] live here. **`direction-selectivity`** is core because the
function objective is DSI on a DSGC substrate; the quantitative DSI ceilings, the antipodal ratio
convention, and the spike-vs-PSP DSI amplification ratios
[Sivyer2013, Oesch2005, PolegPolsky2016a, PolegPolsky2026, deRosenroll2026, Trenholm2013] live in
this category. **`retinal-ganglion-cell`** is core because the Bed B substrate is a mouse DRD4
ON-OFF DSGC and the PD-rate / ND-rate calibration anchors [Trenholm2013, Oesch2005], the AIS Nav
density priors for the RGC family [Werginz2020, Werginz2024], and the dendritic-spike DSGC
literature all sit here. **`dendritic-computation`** is consulted because the 14-d morphology
substrate plus active dendritic Nav1.6 / NaP machinery is the t0080 design that t0122 / t0123
inherit unchanged [Branco2010, Sivyer2013, Schachter2010]; dendritic-spike density directly
co-controls DSI and ATP cost. **`voltage-gated-channels`** is consulted because the ATP-per-spike
recipe integrates inward Na+ current across every compartment with voltage-gated Na channels
(Nav1.6, Nav1.2, NaP), so the kinetic priors [Khaliq2003, Kole2008] and the AIS density priors live
here. **`patch-clamp`** is consulted because the Carter-Bean 2009 AIS calibration benchmark
referenced by the smoke-gate (quoted in [Sengupta2010] as alpha ~ 1.2 for mouse cortical pyramidal
cells) is a patch-clamp measurement; the closest in-corpus patch-clamp anchors for the RGC family
are [Werginz2020, Werginz2024]. **`synaptic-integration`** is consulted because NMDA Mg-block
multiplicative scaling shapes the DSI Pareto and indirectly controls Na+ inward current at dendrites
[PolegPolsky2016a, Branco2010].

Two categories were inspected and excluded. **`cable-theory`** sets the analytical priors on what
the morphology search is doing but does not constrain either DSI ceilings or ATP cost directly; the
historical cable-theory references (Koch and Poggio 1982; Mainen and Sejnowski 1996, both catalogued
in t0097's prior corpus) motivate including morphology as a free axis but do not address the
function-vs-energy Pareto front and are not cited here. The other category that would be relevant -
a dedicated `energy-cost` or `multi-objective-optimisation` slug - does not exist in
`meta/categories/`; all energy and MOO papers live under `compartmental-modeling`.

## Key Findings

### The Sengupta 2010 ATP-per-Spike Recipe is the Canonical Energy Objective

[Sengupta2010] is the project-canonical citation for the per-AP energy recipe. Per-spike per-
compartment ATP cost is the integrated inward Na+ current divided by elementary charge and by 3 (the
3-Na+/ATP stoichiometry of the Na+/K+ pump):
`N_ATP_per_spike = (1/3) * (1/e) * sum_compartments int_{AP_window} I_Na^inward(t) dt`. The recipe
assumes:

* Na+ entry during the AP is the dominant energy cost component (92-95% of per-AP energy is Na+ pump
  activity even in models with extra inward currents like RG / MTCR)
  [Sengupta2010, Table 1 text, p. 5].
* AP shape (height, half-width) is a poor predictor of energy cost: two APs with identical height /
  half-width can be produced by current pairs differing 1.76-fold in Na+ load (1275 vs 2244 nC/cm^2)
  [Sengupta2010, Figure S1].
* Resting energy is < 1.5% of per-AP energy across all seven models, so per-AP integrated
  `int(I_Na) dt / 3` is a valid stand-in for total metabolic cost during repetitive firing without
  separately accounting for resting Na+ leakage [Sengupta2010, Table S5].

Cross-species per-AP Na+ loads from [Sengupta2010, Table 1, before optimisation] anchor the
biological cost scale:

| Cell type | Na+ load (nC/cm^2) | ATP (cm^-2) | Overlap factor alpha |
| --- | --- | --- | --- |
| Squid giant axon (6.3 deg C) | 1098 | 2.3 x 10^12 | ~11.2 |
| Crab leg motor neuron | 364 | not tabulated | ~3.8 |
| Mouse fast-spiking cortical interneuron | 315 | not tabulated | ~3.3 |
| Honeybee Kenyon cell | 186 | not tabulated | ~2.0 |
| Rat hippocampal interneuron | 76 | not tabulated | ~1.3 |
| Rat cerebellar granule cell | 72 | not tabulated | ~1.04 |
| Mouse thalamocortical relay | 65 | 1.35 x 10^11 | ~1.0 |

The **17-fold spread** across cell types is almost entirely overlap load (R^2 = 0.99 with slope ~1
between overlap load and total Na+ load [Sengupta2010, Figure 4]). The capacitive-minimum Na+ load
varies only 2.3-fold (98 to 56 nC/cm^2). Mammalian central neurons sit at **alpha ~ 1.0 - 1.3**;
mouse cortical pyramidal cells from the Carter and Bean 2009 reference are cited at **alpha ~ 1.2**
[Sengupta2010, discussion, p. 9]; mouse fast-spiking interneurons sit at alpha ~ 2 (roughly 100%
above theoretical minimum, [Sengupta2010, p. 8 commentary on MFS model]).

**Hypothesis (Sengupta-anchor)**: t0124's optimised Pareto front should produce DSGC cells whose
AIS-segregated ATP-per-AP per-cm sits within 30% of the Carter-Bean ~4 mM-mol/cm canonical value
when the smoke-gate is satisfied. The DSGC is a non-fast-spiking cell, so the **expected operating
alpha is in the 1.0 - 2.0 band** (between rat hippocampal interneuron and mouse fast-spiking
interneuron). Cells with alpha > 3 (squid-like) indicate either a broken recipe or a
non-physiological NSGA-II solution and should be flagged in the analysis.

### NSGA-II at 28 896 - 5760 Evaluations Sits Above the Mohacsi 2024 Convergence Plateau

The 68-d substrate's NSGA-II convergence behaviour has been calibrated by the prior task lineage and
the broader compartmental-model NSGA-II literature. [Druckmann2007] ran NSGA-II with **population
300 x 1000 generations = 300 000 evaluations** on a 12-parameter cortical interneuron and verified
insensitivity to algorithm settings up to **8000 iterations** [Druckmann2007, Methods text].
[Hay2011] used **population 1000 x 500 generations = 500 000 evaluations** on a 22-parameter L5
pyramidal cell, producing ~2000 acceptable models [Hay2011, ModelDB 139653]. [Achard2006] used **9
independent runs of ~8000 evaluations each (~72 000 total) on a 24-parameter Purkinje cell**
[Achard2006, Methods]. The modern controlled benchmark [Mohacsi2024] ran **100 individuals x 100
generations = 10 000 evaluations per algorithm per benchmark across 22 algorithm variants** and
showed NSGA-II (Inspyred / Pygmo / BluePyOpt) asymptoting after roughly **20 - 60 generations on 3 -
12-parameter problems** [Mohacsi2024, Use Cases 1-6]. [PolegPolsky2026] used **pop = 10 x typical
300 generations x 100 GA seeds = 300 000 evaluations per configuration**, extending to **1000
generations only for low-performing configurations** [PolegPolsky2026, Methods].

t0124's planned total at **pop = 96 x 60 generations = 5760 evaluations** is roughly half t0106's 28
896 (which sat at the Achard 2006 level), still well below Druckmann 2007 / Hay 2011's 300 - 500k
budgets, and at the same order as Mohacsi 2024's controlled head-to-head budget (10 000) on a
problem with **5.7x more free parameters than Mohacsi's largest use case (12 conductances in
detailed CA1)**. The 2-direction protocol halves trial cost relative to t0123 (4 directions, $1
actual at $3-5 budget estimate), so t0124's expected actual cost falls in the **$1 - 3 band** based
on t0122 (DSI + cytoplasm volume on 2-direction) coming in well under $3
[Mohacsi2024 noise sensitivity, Dang2023 theoretical bounds].

**Hypothesis (HV-plateau)**: t0124's hourly hypervolume polling should show the largest HV gains in
the first 20 - 40 generations with diminishing returns past gen 40 and effective saturation past gen
50, given [Mohacsi2024]'s NSGA-II plateau at 20 - 60 gens on 3 - 12-parameter problems and the fact
that t0124's 5760-eval budget is **lower** than t0106's 28 896
[Druckmann2007, Mohacsi2024, PolegPolsky2026]. The operator-stop / 60-gen ceiling is likely to
trigger near gen 50 rather than gen 60.

### NSGA-II Is Provably Noise-Robust at Low Per-Trial Noise; pop = 96 at n = 68 Is Marginal

[Dang2023] provides the first theoretical runtime analysis of NSGA-II under noisy multi-objective
optimisation. Below per-evaluation noise probability **p = 1/2** NSGA-II covers the Pareto front in
**polynomial expected time** given a sufficiently large population (`mu = Omega(n log n)`); above
`p >= 10/19 ~ 0.526` the expected runtime is **provably exponential** `exp(Omega(n))`
[Dang2023, Theorems 8, 10]. Crowding distance is the protective mechanism: NSGA-II retains weakly
dominated individuals across generations, which preserves useful search points even when noisy
evaluations flip the dominance relation [Dang2023, proof of Theorem 8]. Algorithms that discard
dominated individuals on insertion (like GSEMO) collapse under any non-trivial noise
[Dang2023, Theorem 3].

t0124's per-cell objective values are inherently noisy: each cell is evaluated on
**`n_eval_seeds = 3` stochastic synaptic-input replicates**. The DSI silence guard (R_PD < 3 spikes
-> DSI = -1) is a hard threshold but mathematically the noise distribution remains well below the
Dang 2023 critical threshold p = 0.5 for the deterministic-protocol synaptic inputs used in this
project (each seed re-uses a fixed RNG protocol; noise comes from input timing, not output
generation). The population-size requirement at n = 68 is `mu >> n log n ~ 287`; **pop = 96 sits at
the lower end** of the asymptotic guarantee. Mohacsi 2024's empirical demonstration that pop = 100
NSGA-II works on 12-d biophysical problems is the reassurance that pop = 96 remains usable in
practice at 68 d [Mohacsi2024], but the substrate dimension is 5.7x higher than any reviewed
empirical benchmark. [Budszuhn2025] further shows empirically that **static N = 1 resampling wins
most chi-squared-noise scenarios in NSGA-II** [Budszuhn2025, Table 1] - confirming that N_EVAL_SEEDS
= 3 is conservative on the literature scale, not aggressive.

**Best practice (literature-converged, inherited from t0106 / t0122 / t0123)**: at fixed total
budget, **spend on parameter diversity (more pop or more generations) rather than noise averaging**
unless the noise distribution is heavy-tailed or unbounded [Druckmann2007, Hay2011, Budszuhn2025].
t0124's N_EVAL_SEEDS = 3 sits well above the [Budszuhn2025] static-N = 1 best-case for bounded noise
and well below the [Hay2011] feature-SD-based implicit averaging convention.

### Antipodal Ratio DSI on 2 Directions Is Mathematically Equivalent to Trenholm 2013's Vector-Sum DSI for the PD-ND Axis

[Trenholm2013] defines DSI for mouse Hb9::eGFP DSGCs as `(Pref - Null) / (Pref + Null)` from the
**vector sum of peak spike rates over 8 directions** [Trenholm2013, Methods]. Peak preferred-
direction rate is **198 +/- 14 Hz** under control conditions, peak null-direction rate is **27 +/-
12 Hz** [Trenholm2013, Results, p. 14817], giving a **peak-rate DSI of (198 - 27) / (198 + 27) =
0.76**. Under picrotoxin (GABA-A block), peak preferred rises to **244 +/- 18 Hz** and peak null to
**202 +/- 14 Hz** [Trenholm2013, Figure 4]. Intrinsic gain- control recovery `tau = 604 +/- 158 ms`
[Trenholm2013, Figure 5, p. 14820].

The vector-sum DSI over 2 antipodal vectors of magnitudes A and B is `(A - B)` and the sum of
magnitudes is `(A + B)`, so **vector-sum DSI = ratio DSI for the special case of opposed PD-ND**.
For higher direction counts the vector-sum DSI **is bounded above by the antipodal ratio DSI**
whenever the response is well-aligned with the PD axis [Trenholm2013, Methods]; off-axis side lobes
only reduce the vector sum magnitude relative to the antipodal subtraction. The 2-direction
antipodal protocol is therefore the **least-conservative** estimator of DSI in the sense that it
gives the optimiser the maximum DSI signal for a given spike count.

[Oesch2005] reports spike-based DSI in rabbit ON-OFF DSGCs of **0.67 +/- 0.13 (ON)** and **0.74 +/-
0.13 (OFF)** [Oesch2005, Results]; PSP-based (spike-blanked) DSI is only **0.09 +/- 0.05 (ON) and
0.14 +/- 0.08 (OFF)** [Oesch2005, Figure 4], so spike generation sharpens tuning by **roughly
6-fold**. [PolegPolsky2026] reports DSI values measured as **vector-sum subthreshold peak voltage
over 12 directions x 5 speeds**: maximally unconstrained reaches **DSI = 73.1 +/- 2.4%**;
**Barlow-Levick weight-only** reaches **50.8 +/- 0.8%**; **symmetric negative control** reaches
**2.4 +/- 0.1%** [PolegPolsky2026, Figure 3]. The "DSI >= 0.5" threshold used by t0124's downstream
joint-pass classification sits **slightly below the B&L floor (51%)** and well below the
unconstrained ceiling (73%).

**Best practice (DSI silence guard)**: ratio DSI is **only well-defined when `PD + ND > 0`**. The
silence guard inherited from t0122 (R_PD < 3 PD spikes -> DSI = -1) is mechanically correct but is a
**hard threshold** that shapes what NSGA-II converges to near the low-activity corner of parameter
space. The 3-spike floor is **lower than [Trenholm2013]'s empirical 10-spikes-per- direction
reliability floor** but matches t0122's 2-direction guard convention exactly; this is load-bearing
because t0124 must reproduce t0122's DSI ceiling distribution so the function-vs-energy comparison
is calibrated.

### Dendritic Na Spikes are Necessary to Reach DSI >= 0.7; They Inflate ATP Cost

Multiple lines of evidence converge on the claim that DSGC DSI > 0.4 - 0.5 requires active dendritic
Nav, and active dendritic Nav directly inflates the per-AP integrated `int(I_Na) dt`.

[Sivyer2013] performed dual soma + terminal-dendrite whole-cell recordings in rabbit ON-OFF DSGCs
and showed that preferred-direction moving bars elicit fast dendritic spikes that **precede the
somatic AP by several milliseconds** and are **larger at the dendritic site than at the soma**. Bath
TTX at low dose selectively attenuates the dendritic-spike component, **collapsing the somatic spike
DSI toward zero** [Sivyer2013, Figures 4-5]. Their compartmental model reproduces this only when
terminal dendrites are endowed with physiologically plausible densities of voltage-gated Na+ and
Ca2+ channels [Sivyer2013, Figure 6]. [Schachter2010] uses a quantitative DSGC compartmental model
with **40 mS/cm^2 uniform dendritic Nav** (alternative gradient 45 -> 20 mS/cm^2 proximal / distal),
**150 mS/cm^2 somatic Nav**, **local dendritic input resistance 150 - 200 MOhm proximally scaling to
\> 1 GOhm at distal tips**, reaching **spike DSI ~ 0.8** from **PSP DSI ~ 0.2** - a ~4x
amplification [Schachter2010, Table 1, Figure 5]. Single excitatory synapse of **~1 nS** can trigger
a local spike at the tip but **3 - 4 nS** is required near the soma [Schachter2010, Figure 4].
**Initiation can be vetoed by 4 - 10 nS of inhibition** but **propagation of an already- initiated
spike requires ~85 nS** [Schachter2010, Figure 7].

Each dendritic spike that initiates contributes to per-AP `int(I_Na) dt`. Per [Attwell2001, p. 1140]
of the bottom-up cortical energy budget, somatic + dendritic compartments together account for **18%
of the AP-cost component (4% soma + 14% dendrites)**, with axon collaterals dominating at **82%**.
Translated to t0124's compartment set (soma + AIS proximal + AIS distal + dendrites - no axon
collaterals in the Bed B substrate), the recorded ATP-per-spike will under-count the cortical
reference of **3.84 x 10^8 ATP per AP** by roughly **5x** (the 82% axonal share is anatomically
absent in the substrate). The smoke-gate must compare to the AIS-only Carter-Bean ~4 mM-mol/cm
benchmark, **not** the whole-cell Attwell-Laughlin per-spike figure, because the substrate lacks
axon collaterals.

**Hypothesis (DSI inflates ATP)**: the t0124 Pareto front should exhibit a positive correlation
between DSI and ATP-per-spike across non-dominated cells, because dendritic Na spike density
controls both the DSI ceiling (via [Sivyer2013, Schachter2010] amplification) and the per-spike
dendritic Na+ load. If this correlation is positive and convex, the front shows a Carter-Bean-style
Na/K-overlap penalty for high-DSI cells (extra Na+ enters the cell without contributing to
threshold-crossing depolarisation). If the front is flat (DSI varies freely at fixed ATP), the
substrate has degenerate parameter ranges that produce DSI from non-Na+ mechanisms (NMDA Mg-block
multiplicative gating from [PolegPolsky2016a]).

### NMDA Mg-Block Multiplicative Scaling Provides a Lower-ATP Alternative DSI Mechanism

[PolegPolsky2016a] reports that NMDAR blockade with AP5 in mouse DRD4-GFP DSGCs reduces preferred-
direction PSPs by **35%** and null-direction PSPs by **34%** (n = 19) - proportional, multiplicative
reduction; **DSI is unchanged** (p > 0.5) [PolegPolsky2016a, Figure 2]. The multiplicativity is
voltage-dependent: removing extracellular Mg2+ collapses the slope angle from **62.5 +/- 14.2
degrees** (multiplicative) to **45.5 +/- 5.3 degrees** (additive, p < 0.001)
[PolegPolsky2016a, Figure 3]. Their NEURON model uses **177 AMPAR + 177 NMDAR + 177 GABA_A
synapses** distributed homogeneously on ON dendrites with Jahr-Stevens-type Mg2+ block kinetics
(ModelDB 189347) and reproduces multiplicative scaling **without dendritic spikes**
[PolegPolsky2016a, Figure 7].

[Branco2010] establishes the underlying biophysical principle: dendritic impedance gradients
combined with NMDA non-linearity generate direction-selective summation. IN-direction (tip-to-soma)
sequences produce somatic EPSPs **31 +/- 4% larger** than OUT-direction sequences (p < 0.0001, n =
20), with **38 +/- 9% higher spike probability** (p = 0.0013). D-AP5 abolishes the supralinearity
(**223 +/- 9%** of linear sum -> **103 +/- 3%**, p < 0.0001) and reduces the IN-vs-OUT difference to
a non-significant **0.4 +/- 0.4 mV** [Branco2010, Figure 3]. Optimal velocity is **2.0 - 2.6 um/ms**
(matched to the DSGC bipolar wave-speed range).

NMDA-driven DSI relies on synaptic Na+ entry through the NMDAR ion pore (~84% of synaptic energy is
postsynaptic Na+ entry per [Attwell2001, Figure 1]), but the Na+ load per spike is **synapse-
gated**, not channel-density-gated: each NMDAR contributes Na+ entry only when both pre- and
postsynaptic activation align. Per-spike `int(I_Na) dt` from NMDA is therefore proportional to the
number of multiplicatively-engaged synapses, which scales much more weakly with DSI than a uniform
dendritic Nav density increase.

**Hypothesis (NMDA-cheap DSI)**: cells on the **low-ATP, mid-DSI** corner of the t0124 Pareto front
should preferentially express **high `gnmda_dend`** and **low `nav16_dend_distal`** - achieving DSI
via NMDA Mg-block multiplicativity rather than dendritic Na spikes. Cells on the **high-DSI,
high-ATP** corner should show the reverse parameter profile (high Nav, lower NMDA reliance). This is
testable from the t0124 Pareto-front parameter distributions and provides the answer asset's core
mechanistic claim.

### AIS Nav Density: Calibrating the Carter-Bean Smoke-Gate

The smoke-gate verifies the canonical Bed B cell's AIS-segregated per-AP per-cm ATP cost against the
Carter and Bean 2009 mouse Purkinje-cell ~4 mM-mol/cm benchmark within 30%. The exact Carter- Bean
2009 paper is not in the project corpus (research-internet must download it for the final literature
comparison), but the AIS Nav density priors that determine the smoke-gate's expected outcome are
well anchored.

[Kole2008] is the landmark cortical-pyramidal AIS Nav patch-clamp study that established the **0.25
\- 0.5 S/cm^2** AIS Nav range as the canonical biophysical-modelling prior. The exact patch- clamp
values were not extracted from the paper PDF (the file is paywalled in the project's previous
download attempts and the local summary is built from CrossRef metadata only - **not found in
paper**); the 0.25 - 0.5 S/cm^2 range is cited consistently in downstream biophysical-modelling work
[Hay2011, Werginz2020, Werginz2024] as a robust lower bound. [Werginz2024] reports **gNa = 1300
mS/cm^2 at the AIS** vs **75 mS/cm^2 at the soma** for mouse alpha-RGCs - an **AIS-to-soma Nav ratio
of 17.3x** [Werginz2024, Table 1]. [Werginz2020] confirms **AIS-to-soma Nav density ratio
approximately 7x** in mouse OFF-alpha transient RGCs [Werginz2020, Methods]. The published mouse
alpha-RGC AIS Nav range, normalised to S/cm^2, is approximately **0.7 - 2.0 S/cm^2** across the
three alpha RGC types in [Werginz2024]. [Sengupta2010] cites the Carter and Bean 2009 reference as
**alpha ~ 1.2** for mouse cortical pyramidal cells (overlap factor 20% above theoretical minimum),
with **mouse fast-spiking Purkinje / interneuron** sitting at **alpha ~ 2** (roughly 100% above
minimum) [Sengupta2010, discussion p. 8-9].

**Smoke-gate calibration**: the Bed B canonical cell's AIS proximal + AIS distal contribution to
per-AP per-cm Na+ load should produce an ATP figure that, when expressed in mM-mol/cm (the units
Carter and Bean 2009 use), sits within 30% of the canonical ~4 mM-mol/cm value. The 30% window is
inherited from t0123 verbatim (t0124 re-runs the gate to confirm it still passes after the
2-direction protocol change). The expected per-AP per-cm value depends on the alpha factor for mouse
RGCs (not directly measured in the corpus; closest references are [Werginz2024] for AIS density and
[Sengupta2010] for the Carter-Bean alpha ~ 1.2 quote). The DSGC is **not fast-spiking** in the
[Sengupta2010] sense, so the expected operating alpha is in the **1.0 - 2.0** band - plausibly
cheaper than Purkinje, comparable to or cheaper than the Carter-Bean cortical pyramidal calibration
target.

### Attwell-Laughlin 47% Signalling-ATP Budget Anchor

[Attwell2001] establishes that **action potentials and postsynaptic glutamate currents jointly
account for 81% of signaling energy** in rodent grey matter at 4 Hz mean firing, with **47% of total
signalling ATP going to APs** (the canonical "47% signalling-ATP" anchor that t0124's analysis layer
compares against). Per AP, **3.84 x 10^8 ATP** are consumed (Na+ load 1.15 x 10^9 ions); **axon
collaterals dominate at 82%**, **dendrites take 14%**, **soma only 4%**
[Attwell2001, p. 1140, Table 1]. Per glutamate vesicle, **1.64 x 10^5 ATP** total: **postsynaptic
ion fluxes 84% (137 000 ATP)**, presynaptic Ca2+ entry 7% (12 000 ATP), glutamate recycling 7% (11
000 ATP), metabotropic spine signaling 2%, vesicle cycling 0.5% [Attwell2001, Figure 1].

The total ATP per neuron per spike (AP + 2000 released vesicles) is **7.1 x 10^8 ATP/spike**
[Attwell2001, summary calculation, p. 1142]. Scaling rule: **1 spike/neuron/s = 6.5 umol ATP/g/min =
145 mL O2/100 g/h** [Attwell2001, Eq. 9 + p. 1140]. The 47%-of-signalling figure assumes the neuron
has anatomically complete axon collaterals; for the Bed B substrate with no axon collaterals, the
"AP cost" is structurally bounded above by the **18% somatodendritic component** of the cortical
budget. **The t0124 ATP-per-spike figure should be expected to be ~5x lower than the
Attwell-Laughlin whole-cell reference** of 3.84 x 10^8 ATP/AP because of this anatomical truncation;
the comparison to the 47%-signalling-budget anchor must explicitly correct for the missing axon
collateral compartment in the answer asset.

**Hypothesis (Attwell-Laughlin anchor)**: t0124 top-N cells' implied per-cell **signalling ATP
rate** (ATP/spike * PD-rate) for top-N cells should sit **below** the 47%-of-cortical-budget figure
when corrected for the 5x axon-collateral truncation - i.e., the corrected signalling rate should
sit at the cortical-DSGC operating point inferred from in vivo firing rates. Cells that exceed the
47%-corrected anchor indicate either pathologically high firing or pathological Na+ overlap.

### Cuntz 2010 Wiring-vs-Conduction-Time Trade-off: Cross-Reference to t0122

[Cuntz2010] grows synthetic dendritic arbors as the solution to a locally optimised graph that
simultaneously minimises (i) total wiring length and (ii) path length from root to every carrier
point, combined via a balancing factor `bf`:

```text
total_cost = wiring_cost + bf * path_length_cost
```

Biologically realistic arbors cluster at **`bf` in [0.2, 0.7]** across fly LPTCs, mammalian CA1
pyramidal cells and cerebellar Purkinje cells [Cuntz2010, Figure 5]; **`bf = 0`** (pure minimum-
spanning-tree) and **`bf -> infinity`** (star graph) are unphysical. Synthetic Cuntz arbors match
real reconstructions on **total dendritic length within a few percent** [Cuntz2010, Figure 4].

For t0124, the Cuntz balancing factor is a **cross-reference** to t0122 (DSI + cytoplasm volume),
not a direct objective. t0122 ran the same 14-d morphology substrate with cytoplasm volume as the
second objective; its Pareto front traces the cell's `bf` value indirectly. t0124's
comparison-to-literature layer must overlay the t0122 cytoplasm-vs-DSI front on the t0124 ATP-vs-
DSI front so the answer asset can ask: do high-DSI cells pay both a wiring cost (t0122) and an
ATP-per-spike cost (t0124), or do they trade off the two costs? This is a **novel comparison** - no
published study has measured the joint Cuntz-balance and Carter-Bean-overlap trade-offs on the same
morphology substrate.

### deRosenroll 2026 Substrate Ceiling: DSI ~ 0.4 at the Bed B Floor

[deRosenroll2026] is the direct upstream source of the Bed B substrate (t0024 port). Their
correlated-release model reaches **DSI ~ 0.39 under faithful E/I co-correlation** but **DSI ~ 0.25
under uncorrelated release** [deRosenroll2026, Figure 5]. This confirms that **the passive Bed B
dendrites cannot reach DSI 0.4 robustly without additional active dendritic mechanisms**, which is
exactly the t0078 / t0080 finding the 68-d substrate is designed to address. For t0124, this is
load-bearing because:

* The substrate ceiling at the passive-dendrite floor is DSI ~ 0.4 (correlated release) / DSI ~ 0.25
  (uncorrelated release) per [deRosenroll2026]. Cells in the t0124 Pareto front that reach DSI > 0.5
  must be using active dendritic mechanisms (Nav1.6 / NaP / NMDA Mg-block) - this is the prediction
  the answer asset confirms or refutes from the Pareto-front parameter distribution.
* The Carter-Bean smoke-gate at the canonical Bed B cell (DSI ~ 0.39) tests the **passive-dendrite
  floor** ATP cost. Any t0124 Pareto cell with DSI > 0.4 has by construction more active dendritic
  current than the canonical cell, so its ATP-per-spike should be **higher** than the canonical
  cell's ATP-per-spike.

## Methodology Insights

* **ATP-per-spike recipe (inherited from t0123 verbatim)**: per-cell-per-spike ATP =
  `(1/3) * (1/e) * sum_compartments int_{AP_window} I_Na^inward(t) dt` where I_Na^inward is
  `-min(I_Na, 0)` and `seg.ina` (mA/cm^2) is multiplied by per-segment surface area
  (`seg.area() * 1e-2` for cm^2) before integration [Sengupta2010, Methods]. AP windows are detected
  from somatic Vm threshold-crossing at -20 mV with a 2 ms refractory and a +/-2 ms window around
  the peak (t0123 recipe). Record compartments are soma + AIS proximal + AIS distal + all dendritic
  segments. **No axon collaterals are recorded** because the Bed B substrate does not include them;
  correct the answer asset's comparison to [Attwell2001]'s 7.1 x 10^8 ATP/spike for the missing 82%
  axon-collateral share.

* **Carter-Bean smoke-gate threshold**: verify the canonical Bed B cell's AIS-segregated per-AP
  per-cm ATP cost matches the Carter and Bean 2009 ~4 mM-mol/cm benchmark **within 30%** before
  launching NSGA-II. If the gate fails, debug the recipe (most common cause from t0123: a surface-
  area unit-conversion bug; second most common: missing compartments in the seg.ina record list).
  Follow up on S-0123-04 by re-deriving the Carter-Bean canonical value in `plan/plan.md` from first
  principles (mouse Purkinje AIS sodium influx per AP per cm length, using [Werginz2024] alpha-RGC
  AIS Nav density of **1300 mS/cm^2** as a cross-reference for the order of magnitude).

* **DSI silence-guard threshold (inherited from t0122)**: `DSI = -1` if R_PD < 3 PD spikes. This is
  lower than [Trenholm2013]'s empirical 10-spikes-per-direction reliability floor but matches
  t0122's 2-direction guard convention exactly. **Do not change the threshold** in t0124 - the
  function-vs-energy comparison to t0122 requires matched DSI definitions.

* **Direction protocol N_DIRECTIONS = 2**: antipodal 0 deg (PD) / 180 deg (ND) per t0122 convention
  [Trenholm2013 vector-sum DSI = 2-direction antipodal ratio DSI on the PD-ND axis]. The 4-direction
  protocol of t0123 was driven by the MI count-entropy ceiling (1-bit ceiling for 2 directions vs
  2-bit ceiling for 4); MI is only diagnostic in t0124, not the function objective, so 2 directions
  suffice and halve per-evaluation cost.

* **NSGA-II via pymoo with default operators**: SBX crossover (eta = 15), polynomial mutation (eta =
  20), tournament selection of size 2. Inherited from t0080 / t0102 / t0104 / t0122 / t0123 verbatim
  [Druckmann2007, Hay2011, Mohacsi2024 default operator choices]. Latin Hypercube Sampling for the
  initial 96-cell population [Druckmann2007, Hay2011 convention].

* **Hard constraints (assert at module import in `code/constants.py`)**: `_POOL_RESTART_EVERY = 10`
  (project standing 10-gen rule per t0112), `HV_PLATEAU_AUTO_STOP = False` (per memory
  `feedback_disable_hv_plateau_autostop.md`), `POP_SIZE = 96`, `N_EVAL_SEEDS = 3`,
  `N_DIRECTIONS = 2`, `N_GEN_MAX = 60`, `COST_CAP_USD = 6.0`. The plan verification criteria must
  surface each one explicitly per the t0114 / t0115 / t0122 / t0123 convention
  [PolegPolsky2026, Druckmann2007 default-vs-extended convention].

* **Pareto front analysis pattern (Hay 2011 ensemble-as-experiment)**: report the **full Pareto
  front and ensemble parameter distribution**, not the single hypervolume-maximising point
  [Hay2011, Druckmann2007]. For t0124, compute the joint-pass cells (DSI >= 0.5 AND PD-rate >= 30 Hz
  AND ATP-per-spike <= median of the front) and characterise the parameter ranges they occupy vs the
  rest of the Pareto front. This identifies which knobs (Nav1.6, NaP, NMDA, AIS densities) are
  **necessary** (range collapses to a narrow band on the joint-pass subset) vs **sufficient** (range
  stays broad).

* **Compare-literature layer**: t0124 must compute three cross-literature anchors in
  `compare_literature.md`:
  1. **Carter-Bean 2009 ATP/AP/cm benchmark** on the canonical cell + top-3 Pareto cells, with
     within-30% / over-by-Xx / under-by-Xx labels per
     [Sengupta2010 discussion p. 9 reference to Carter and Bean 2009].
  2. **Attwell-Laughlin 2001 47%-signalling anchor**: top-N cells' (ATP/spike * PD-rate) signalling
     rate, **corrected for the 5x axon-collateral truncation**, plotted vs the
     [Attwell2001, p. 1140] 47% reference.
  3. **Cuntz 2010 balancing-factor band [0.2, 0.7]** cross-reference to t0122's cytoplasm-vs-DSI
     front [Cuntz2010, Figure 5].

* **Best practice - peak firing rate from Gaussian-convolved spike trains with sigma = 25 ms**
  [Trenholm2013, Methods]. The downstream PD-rate >= 30 Hz joint-pass criterion must use the same
  convention to be directly comparable to the [Trenholm2013] 198 +/- 14 Hz peak preferred-direction
  rate (where 30 Hz is roughly 15% of the published peak).

* **Hypothesis to test in analysis**: the joint correlation between DSI and ATP-per-spike across the
  t0124 Pareto front identifies whether the DSGC pays a Carter-Bean overlap penalty for high DSI.
  **Positive convex correlation** -> overlap penalty present, dendritic Na spikes are the dominant
  DSI mechanism. **Flat / weak correlation** -> NMDA-cheap DSI mechanism dominates,
  [PolegPolsky2016a] multiplicative scaling supplants [Sivyer2013] dendritic spikes. **Negative
  correlation** -> non-Na+ DSI mechanism dominates (Ca2+ or K+-modulated multiplicative gating),
  which would be a novel finding worth a follow-up suggestion.

## Gaps and Limitations

* **Carter and Bean 2009 paper is NOT in the project corpus.** The smoke-gate references the "~4
  mM-mol/cm" benchmark via [Sengupta2010]'s discussion (alpha ~ 1.2 for mouse cortical pyramidal
  cells) and via the [Werginz2024] / [Werginz2020] AIS Nav density measurements. The exact Carter
  and Bean 2009 value must be re-derived in the smoke-gate's `plan/plan.md` from first principles,
  per S-0123-04. **Research-internet must download the actual Carter and Bean 2009 paper**
  (10.1016/j.neuron.2009.07.013 - "Sodium entry during action potentials of mammalian neurons:
  incomplete inactivation and reduced metabolic efficiency in fast-spiking neurons") for the final
  compare-literature layer.

* **Remme et al. 2018 MSO function-vs-energy MOBO paper is NOT in the project corpus.** The task
  description cites Remme 2018 as the direct methodological template for function-vs-energy MOBO on
  a single neuron. Without the paper, t0124's methodology comparison must rely on [Hay2011]'s
  22-parameter MOO precedent and [PolegPolsky2026]'s ML-based DSGC search. Research-internet should
  download Remme et al. 2018 (J Neurosci or similar venue; "Pareto-coding - ITD discrimination vs
  Na+ ATP in the MSO") for the analysis stage.

* **Kole 2008 PDF is paywalled and the local summary is metadata-only.** The 0.25 - 0.5 S/cm^2 AIS
  Nav range is cross-referenced from [Hay2011, Werginz2024] not extracted from the source - flagged
  as `not found in paper`. Verify against the manual PDF before publishing the t0124 answer asset.

* **Sivyer 2013 PDF is paywalled** [project-internal status flagged in t0080 research notes].
  Specific quantitative values for terminal dendritic gNa and gCa densities in Sivyer and Williams's
  compartmental model are not extractable. The dendritic Nav density range used by t0124 is set by
  [Schachter2010] (40 mS/cm^2 uniform; 45 -> 20 proximal-distal gradient) rather than by the
  Sivyer-Williams compartmental model directly.

* **No DSGC patch-clamp study reports AIS-to-soma Nav ratio directly.** The 5x hard floor used by
  t0080 / t0122 / t0123 / t0124 is inferred from non-DSGC RGCs ([Werginz2020] OFF-alpha transient
  ~7x; [Werginz2024] alpha-ON sustained ~17.3x). Whether DRD4 ON-OFF DSGCs sit in the same range is
  unknown. The smoke-gate's expected ATP-per-AP magnitude depends on this assumption.

* **No published study reports the DSGC DSI-vs-ATP-per-spike Pareto front.** t0124 is generating the
  first such front. The novelty implies that the answer asset's claim about whether the front shows
  a Carter-Bean-style Na/K-overlap penalty is **not pre-anchored by a literature precedent**; the
  comparison is to single-cell Carter-Bean / Sengupta calibration anchors, not to a published Pareto
  trajectory.

* **No reviewed paper runs NSGA-II to 60+ generations on a >40-dimensional biophysical problem with
  a metabolic cost objective.** The closest analogue is [Hay2011] at 22 parameters and 500
  generations on firing-feature objectives, not energy. [Mohacsi2024] caps at 12 parameters and 100
  generations. The high-d-and-energy-objective corner that t0124 occupies is **unstudied in the
  literature** beyond the inherited t0123 prior.

* **No reviewed paper reports negative-result NSGA-II runs.** Hay 2011 and Druckmann 2007 publish
  only successful fits; we do not know how often their runs produced zero joint-pass cells before
  settling on the reported ones. **Publication-selection bias** means our prior on "the Pareto front
  showing no Na/K-overlap penalty is a publishable null" is weakly informed by the literature.

* **The 30 Hz PD-rate joint-pass threshold is not directly comparable to the [Trenholm2013] peak-
  rate convention (198 Hz preferred).** The threshold inherits from t0086 / t0091 / t0099 without
  literature-derived recalibration for the 2-direction reformulation - flagged as a known
  threshold-mismatch risk in the analysis.

## Recommendations for This Task

1. **Adopt the [Sengupta2010] ATP-per-spike recipe verbatim from t0123**:
   `(1/3) * (1/e) * sum_compartments int(I_Na^inward) dt` over AP windows defined by somatic Vm
   threshold-crossing at -20 mV with a 2 ms refractory and +/-2 ms window. Record compartments are
   soma + AIS proximal + AIS distal + all dendritic segments. **Lower is better**;
   `atp_per_spike = +inf` sentinel for cells with total spike count == 0.

2. **Set the DSI silence-guard threshold at R_PD < 3 PD spikes -> DSI = -1** per t0122 convention
   [PolegPolsky2026 floor convention]. Do NOT change this threshold - the function-vs-energy
   comparison to t0122 requires matched DSI definitions across both tasks.

3. **Run the Carter-Bean smoke-gate before NSGA-II launch** on the canonical Bed B cell. AIS
   proximal + AIS distal per-AP per-cm ATP must match Carter and Bean 2009 ~4 mM-mol/cm within 30%.
   Re-derive the canonical value in `plan/plan.md` from first principles using [Werginz2024] AIS Nav
   density 1300 mS/cm^2 and [Sengupta2010] Na/K overlap alpha ~ 1.2 cross-reference per S-0123-04.

4. **Use the [Trenholm2013] peak-rate Gaussian-convolution convention (sigma = 25 ms) for PD-rate
   and ND-rate diagnostics**. The 30 Hz joint-pass threshold is **~15% of the [Trenholm2013] 198 Hz
   peak preferred-direction rate** - flag this as a downstream-threshold risk in the answer asset.

5. **Use Latin Hypercube Sampling for the initial 96-cell population** at the t0080 / t0122 / t0123
   convention [Druckmann2007, Hay2011]. No warm-start anchors; t0124 is a random-init NSGA-II
   single-seed run.

6. **Plan for HV-plateau between gen 30 and gen 50**
   [Mohacsi2024 NSGA-II asymptote at 20 - 60 gens on 3 - 12-parameter problems; PolegPolsky2026 default 300-gen convergence].
   Operator-stop is likely to trigger near gen 50 rather than the 60-gen hard cap.

7. **Build the compare_literature.md layer around three explicit anchors**:
   * Carter-Bean 2009 ATP/AP/cm benchmark (within 30% / over by Xx / under by Xx) using the
     [Sengupta2010] alpha ~ 1.2 mouse cortical pyramidal reference [Sengupta2010 discussion p. 9].
   * Attwell-Laughlin 2001 47% signalling-budget anchor on top-N cells' (ATP/spike * PD-rate),
     corrected for the 5x axon-collateral truncation [Attwell2001, p. 1140].
   * Cuntz 2010 `bf` band [0.2, 0.7] cross-reference to t0122's cytoplasm-vs-DSI front
     [Cuntz2010, Figure 5].

8. **Test the joint-correlation hypothesis** between DSI and ATP-per-spike across the Pareto front:
   positive convex -> Carter-Bean overlap penalty (dendritic-Na DSI mechanism); flat / weak ->
   NMDA-cheap DSI mechanism dominates [PolegPolsky2016a multiplicative scaling]; negative -> non-Na+
   DSI mechanism, novel finding -> spawn follow-up suggestion.

9. **Report the parameter-distribution split between joint-pass cells and the rest of the Pareto
   front** [Hay2011 ensemble-as-experiment pattern]. Identify which Nav / NaP / NMDA / AIS knobs are
   necessary (joint-pass range narrows) vs sufficient (joint-pass range broad).

10. **Acknowledge the t0080 / t0115 substrate-limitation risk in the answer asset.** [Hay2011]'s
    perisomatic-only counterexample shows that some parameter spaces are genuinely thin even at 500
    000-evaluation budgets [Hay2011]. A null result at 5760 evals on t0124 cannot conclusively prove
    substrate emptiness; **rule out only the [Hay2011] / [Druckmann2007] acceptance-rate regime at
    > 99% confidence if zero joint-pass cells are returned**.

## Paper Index

### [Sengupta2010]

* **Title**: Action Potential Energy Efficiency Varies Among Neuron Types in Vertebrates and
  Invertebrates
* **Authors**: Sengupta, B., Stemmler, M., Laughlin, S. B., Niven, J. E.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000840`
* **Asset**: `tasks/t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.1000840/`
* **Categories**: `voltage-gated-channels`, `compartmental-modeling`
* **Relevance**: Project-canonical citation for the ATP-per-spike recipe and source of the Na/K
  overlap factor `alpha` cross-species calibration table. Cites the Carter and Bean 2009 alpha ~ 1.2
  mouse cortical pyramidal benchmark that anchors t0124's smoke-gate. Directly inherited from t0123
  verbatim.

### [Attwell2001]

* **Title**: An Energy Budget for Signaling in the Grey Matter of the Brain
* **Authors**: Attwell, D., Laughlin, S. B.
* **Year**: 2001
* **DOI**: `10.1097/00004647-200110000-00001`
* **Asset**: `tasks/t0097_multi_obj_optim/assets/paper/10.1097_00004647-200110000-00001/`
* **Categories**: `compartmental-modeling`
* **Relevance**: Source of the canonical 47% signalling-ATP-budget anchor for APs and the 18%
  somatodendritic share of the per-AP energy that t0124's substrate captures (the remaining 82% is
  axon-collateral, anatomically absent in Bed B). Provides the 1 spike/neuron/s -> 6.5 umol
  ATP/g/min scaling rule.

### [Niven2008]

* **Title**: Energy limitation as a selective pressure on the evolution of sensory systems
* **Authors**: Niven, J. E., Laughlin, S. B.
* **Year**: 2008
* **DOI**: `10.1242/jeb.017574`
* **Asset**: `tasks/t0097_multi_obj_optim/assets/paper/10.1242_jeb.017574/`
* **Categories**: `compartmental-modeling`
* **Relevance**: Frames the function-vs-energy Pareto frontier in single neurons (bits per ATP) and
  motivates the Law of Diminishing Returns - excess functional capacity is super-linearly penalised
  in metabolic cost. Indirect comparator for the t0124 DSI-vs-ATP front against the fly
  photoreceptor bits-per-ATP curve. (Task description cites as Niven 2007; paper is published in J
  Exp Biol 211(11) 2008.)

### [Druckmann2007]

* **Title**: A novel multiple objective optimization framework for constraining conductance-based
  neuron models by experimental data
* **Authors**: Druckmann, S., Banitt, Y., Gidon, A., Schurmann, F., Markram, H., Segev, I.
* **Year**: 2007
* **DOI**: `10.3389/neuro.01.1.1.001.2007`
* **Asset**: `tasks/t0097_multi_obj_optim/assets/paper/10.3389_neuro.01.1.1.001.2007/`
* **Categories**: `compartmental-modeling`
* **Relevance**: Canonical NSGA-II precedent for compartmental neuron fitting. 300 organisms x 1000
  generations = 300 000 evaluations on a 12-parameter cortical interneuron with insensitivity-to-
  iteration claim. Anchors the operator-stop heuristic for t0124's 60-gen ceiling.

### [Hay2011]

* **Title**: Models of Neocortical Layer 5b Pyramidal Cells Capturing a Wide Range of Dendritic and
  Perisomatic Active Properties
* **Authors**: Hay, E., Hill, S., Schurmann, F., Markram, H., Segev, I.
* **Year**: 2011
* **DOI**: `10.1371/journal.pcbi.1002107`
* **Asset**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1371_journal.pcbi.1002107/`
* **Categories**: `voltage-gated-channels`, `compartmental-modeling`, `dendritic-computation`
* **Relevance**: Upper end of the compartmental-model NSGA-II budget envelope (1000 x 500 = 500 000
  evals, ~2000 acceptable joint models). Provides the ensemble-as-experiment reporting pattern for
  the t0124 Pareto-front parameter distribution and the SK_E2 / CaDynamics_E2 mechanism set and
  somatic NaP upper bound that bound the active dendritic Nav search axis.

### [Achard2006]

* **Title**: Complex Parameter Landscape for a Complex Neuron Model
* **Authors**: Achard, P., De Schutter, E.
* **Year**: 2006
* **DOI**: `10.1371/journal.pcbi.0020094`
* **Asset**: `tasks/t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.0020094/`
* **Categories**: `compartmental-modeling`
* **Relevance**: Lower bound of the literature NSGA-II budget envelope (~72 000 evals across 9 runs
  on a 24-parameter Purkinje cell). Empirical demonstration that good-model regions are thin
  hyperplanes in high-dimensional parameter space - directly relevant to whether 5760 evaluations on
  a single seed can reach a thin lower-dimensional manifold of joint-pass cells in t0124's 68-d
  space.

### [Mohacsi2024]

* **Title**: Evaluation and comparison of methods for neuronal parameter optimization using the
  Neuroptimus software framework
* **Authors**: Mohacsi, M., Torok, M. P., Saray, S., Tar, L., Farkas, G., Kali, S.
* **Year**: 2024
* **DOI**: `10.1371/journal.pcbi.1012039`
* **Asset**: `tasks/t0102_seedscale_n4_gen20/assets/paper/10.1371_journal.pcbi.1012039/`
* **Categories**: `compartmental-modeling`
* **Relevance**: Only modern controlled head-to-head benchmark of >20 parameter-search algorithms
  (including three NSGA-II implementations) on neuron-modelling problems. Empirical "when does
  NSGA-II flatten" anchor (~20 - 60 gens on 3 - 12-parameter problems) that informs t0124's
  HV-plateau expectation between gens 30 and 50.

### [Dang2023]

* **Title**: Analysing the Robustness of NSGA-II under Noise
* **Authors**: Dang, D.-C., Opris, A., Salehi, B., Sudholt, D.
* **Year**: 2023
* **DOI**: `10.48550/arXiv.2306.04525`
* **Asset**: `tasks/t0102_seedscale_n4_gen20/assets/paper/10.48550_arXiv.2306.04525/`
* **Categories**: `compartmental-modeling`
* **Relevance**: First theoretical runtime analysis of NSGA-II under noisy multi-objective
  optimisation. Provides the polynomial-vs-exponential phase transition at noise probability p = 1/2
  and the population-size bound `mu = Omega(n log n)` that frames t0124's pop = 96 at n = 68 as
  marginal-but-empirically-defensible. Justifies NSGA-II's noise tolerance via crowding- distance
  retention of weakly dominated individuals.

### [Budszuhn2025]

* **Title**: Adaptive Resampling with Bootstrap for Noisy Multi-Objective Optimization Problems
* **Authors**: Budszuhn, T., Krallmann, M. J., Horn, D.
* **Year**: 2025
* **DOI**: `10.48550/arXiv.2503.21495`
* **Asset**: `tasks/t0102_seedscale_n4_gen20/assets/paper/10.48550_arXiv.2503.21495/`
* **Categories**: `compartmental-modeling`
* **Relevance**: Shows empirically that the static N = 1 resampling strategy wins most chi-squared-
  noise scenarios in NSGA-II - confirming that low replicate counts are correct when noise is
  bounded. Justifies t0124's N_EVAL_SEEDS = 3 as conservative on the literature scale.

### [Trenholm2013]

* **Title**: Intrinsic and synaptic mechanisms shaping the OFF response of mouse direction-
  selective ganglion cells
* **Authors**: Trenholm, S., McLaughlin, A. J., Schwab, D. J., Awatramani, G. B.
* **Year**: 2013
* **DOI**: `10.1523/JNEUROSCI.0808-13.2013`
* **Asset**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.0808-13.2013/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `patch-clamp`
* **Relevance**: Canonical mouse Hb9-DSGC paper defining ratio DSI as
  `(Pref - Null) / (Pref + Null)` from peak spike rates (198 Hz / 27 Hz / DSI = 0.76 reference).
  Provides the peak-rate Gaussian-convolution convention (sigma = 25 ms) and the empirical PD-rate
  ranges that ground t0124's 30 Hz joint-pass floor. Establishes the slow-AHP recovery tau ~ 604 ms.

### [Oesch2005]

* **Title**: Direction-selective dendritic action potentials in rabbit retinal ganglion cells
* **Authors**: Oesch, N., Euler, T., Taylor, W. R.
* **Year**: 2005
* **DOI**: `10.1016/j.neuron.2005.06.036`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2005.06.036/`
* **Categories**: `direction-selectivity`, `dendritic-computation`, `voltage-gated-channels`,
  `retinal-ganglion-cell`, `patch-clamp`
* **Relevance**: Rabbit ON-OFF DSGC reference spike-based DSI values (0.67 +/- 0.13 ON, 0.74 +/-
  0.13 OFF) that bracket t0124's joint-pass 0.5 threshold. Provides the spike-vs-PSP DSI 6-fold
  amplification ratio that motivates active dendritic mechanisms over passive integration.

### [Sivyer2013]

* **Title**: Direction selectivity is computed by active dendritic integration in retinal ganglion
  cells
* **Authors**: Sivyer, B., Williams, S. R.
* **Year**: 2013
* **DOI**: `10.1038/nn.3565`
* **Asset**: `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1038_nn.3565/`
* **Categories**: `direction-selectivity`, `dendritic-computation`, `retinal-ganglion-cell`,
  `patch-clamp`
* **Relevance**: First dual soma + terminal-dendrite recordings showing dendritic spikes precede
  somatic APs in rabbit DSGCs and that null inhibition vetoes them locally. Establishes that passive
  dendrites cannot reach DSGC DSI > 0.4 - 0.5 without active dendritic Nav, which predicts the joint
  correlation between DSI and ATP-per-spike in the t0124 Pareto front (active Na current is both
  DSI-amplifying and ATP-expensive).

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
* **Relevance**: Quantitative dendritic-Nav DSGC compartmental model with 40 mS/cm^2 dendritic gNa,
  dendritic spike threshold ~ 1 nS at distal tips vs 3 - 4 nS proximal, and the initiation-vs-
  propagation inhibition asymmetry (4 - 10 nS vetos initiation; 85 nS needed for propagation block).
  Sets the dendritic Nav density range and the local subunit-independence constraint that bounds the
  t0124 search space.

### [PolegPolsky2016a]

* **Title**: NMDA Receptors Multiplicatively Scale Visual Signals and Enhance Directional Motion
  Discrimination in Retinal Ganglion Cells
* **Authors**: Poleg-Polsky, A., Diamond, J. S.
* **Year**: 2016
* **DOI**: `10.1016/j.neuron.2016.02.013`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/`
* **Categories**: `compartmental-modeling`, `direction-selectivity`, `synaptic-integration`,
  `dendritic-computation`, `retinal-ganglion-cell`
* **Relevance**: NMDA Mg-block multiplicative-scaling mechanism for DSI; provides the mouse DRD4
  DSGC NEURON model (ModelDB 189347) that Bed B descends from and the alternative low-ATP DSI
  mechanism (NMDA-cheap DSI) that t0124's Pareto-front analysis tests against the
  dendritic-Na-expensive DSI mechanism of [Sivyer2013].

### [Branco2010]

* **Title**: Dendritic Discrimination of Temporal Input Sequences in Cortical Neurons
* **Authors**: Branco, T., Clark, B. A., Hausser, M.
* **Year**: 2010
* **DOI**: `10.1126/science.1189664`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1126_science.1189664/`
* **Categories**: `cable-theory`, `compartmental-modeling`, `dendritic-computation`,
  `synaptic-integration`
* **Relevance**: Establishes the impedance-gradient + NMDA-Mg-block direction-selectivity mechanism
  in passive cortical dendrites. Provides the biophysical principle for the NMDA-cheap DSI corner of
  the t0124 Pareto front and the 31% IN-vs-OUT EPSP-amplitude / 38% spike-probability asymmetry that
  motivates NMDA-only DSI mechanisms.

### [PolegPolsky2026]

* **Title**: Machine learning discovers numerous new computational principles underlying direction
  selectivity in the retina
* **Authors**: Poleg-Polsky, A.
* **Year**: 2026
* **DOI**: `10.1038/s41467-026-70288-4`
* **Asset**: `tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/`
* **Categories**: `compartmental-modeling`, `direction-selectivity`, `retinal-ganglion-cell`,
  `synaptic-integration`, `dendritic-computation`
* **Relevance**: ML-based enumeration of dendritic DS mechanisms in a 352-segment DSGC model.
  Provides the 300/1000-generation default-vs-extended convention, the DSI thresholds (B&L floor
  51%, unconstrained ceiling 73%) that bracket the t0124 joint-pass 0.5 target, and the
  deterministic-forward-pass design that informs t0124's noise-replicate choice.

### [deRosenroll2026]

* **Title**: Uncovering the "hidden" synaptic microarchitecture of the retinal direction selective
  circuit
* **Authors**: de Rosenroll, G., Sethuramanujam, S., Awatramani, G. B.
* **Year**: 2026
* **DOI**: `10.1016/j.celrep.2025.116833`
* **Asset**: `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/paper/10.1016_j.celrep.2025.116833/`
* **Categories**: `compartmental-modeling`, `direction-selectivity`, `retinal-ganglion-cell`,
  `synaptic-integration`, `dendritic-computation`
* **Relevance**: Direct upstream source of the Bed B substrate (t0024 port). Reports DSI ~ 0.39 with
  correlated SAC release vs DSI ~ 0.25 with uncorrelated release in the published model - the
  substrate-floor DSI that anchors the Carter-Bean smoke-gate's "canonical Bed B cell" expectation
  and the joint-pass DSI ceiling t0124's Pareto front must exceed.

### [Kole2008]

* **Title**: Action potential generation requires a high sodium channel density in the axon initial
  segment
* **Authors**: Kole, M. H. P., Ilschner, S. U., Kampa, B. M., Williams, S. R., Ruben, P. C., Stuart,
  G. J.
* **Year**: 2008
* **DOI**: `10.1038/nn2040`
* **Asset**: `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1038_nn2040/`
* **Categories**: `voltage-gated-channels`, `patch-clamp`
* **Relevance**: Canonical AIS Nav patch-clamp prior (cited 0.25 - 0.5 S/cm^2 range; PDF paywalled -
  range cross-referenced from [Hay2011, Werginz2024], not extracted from source - flag as
  `not found in paper`). Anchors the AIS Nav density that determines the smoke-gate's expected AIS
  ATP-per-AP magnitude.

### [Werginz2024]

* **Title**: Differential Intrinsic Firing Properties in Sustained and Transient Mouse alpha-RGCs
  Match Their Light Response Characteristics
* **Authors**: Werginz, P., Kiraly, V., Zeck, G.
* **Year**: 2024
* **DOI**: `10.1523/JNEUROSCI.1592-24.2024`
* **Asset**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.1592-24.2024/`
* **Categories**: `voltage-gated-channels`, `compartmental-modeling`, `retinal-ganglion-cell`,
  `patch-clamp`
* **Relevance**: Mouse alpha-RGC five-tier multi-compartment model with Table 1 channel densities
  (gNa AIS 1300 mS/cm^2 vs soma 75 mS/cm^2; AIS-to-soma Nav ratio 17.3x). Closest in-corpus proxy
  for the Carter and Bean 2009 RGC-family AIS calibration; the 1300 mS/cm^2 AIS Nav anchors the
  smoke-gate's expected per-AP per-cm Na+ load magnitude.

### [Werginz2020]

* **Title**: Tailoring of the axon initial segment shapes the conversion of synaptic inputs into
  spiking output in OFF-alpha T retinal ganglion cells
* **Authors**: Werginz, P., Raghuram, V., Fried, S. I.
* **Year**: 2020
* **DOI**: `10.1126/sciadv.abb6642`
* **Asset**: `tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1126_sciadv.abb6642/`
* **Categories**: `voltage-gated-channels`, `retinal-ganglion-cell`, `compartmental-modeling`,
  `patch-clamp`
* **Relevance**: Independent confirmation that AIS-to-soma Nav density ratio is approximately 7x in
  mouse OFF-alpha-T RGCs. Second anchor below the [Werginz2024] 17.3x; together they bracket the AIS
  Nav range that determines the smoke-gate's tolerance window.

### [Cuntz2010]

* **Title**: One Rule to Grow Them All: A General Theory of Neuronal Branching and Its Practical
  Application
* **Authors**: Cuntz, H., Forstner, F., Borst, A., Hausser, M.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000877`
* **Asset**:
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1371_journal.pcbi.1000877/`
* **Categories**: `compartmental-modeling`, `dendritic-computation`, `cable-theory`
* **Relevance**: Cajal cytoplasm-conservation balancing-factor `bf` framework. Cross-reference to
  t0122's cytoplasm-vs-DSI Pareto front - t0124's compare_literature.md must overlay both fronts to
  ask whether high-DSI cells pay both wiring (t0122) and ATP (t0124) costs jointly.
