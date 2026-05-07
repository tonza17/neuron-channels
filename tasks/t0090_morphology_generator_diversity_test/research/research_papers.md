---
spec_version: "1"
task_id: "t0090_morphology_generator_diversity_test"
research_stage: "papers"
papers_reviewed: 30
papers_cited: 26
categories_consulted:
  - "compartmental-modeling"
  - "dendritic-computation"
  - "direction-selectivity"
  - "retinal-ganglion-cell"
  - "voltage-gated-channels"
  - "cable-theory"
  - "synaptic-integration"
  - "patch-clamp"
date_completed: "2026-05-07"
status: "complete"
---
# Research Papers — Procedural DSGC Morphology Generator + Diversity Test + Validation

Bundle (t0090)

## Task Objective

t0090 implements a procedural DSGC morphology generator with 14 explicit knobs (5 topology + 4
asymmetry + 3 geometry + 2 stochastic control), generates 30 maximally different and 30 maximally
similar morphologies, runs verification simulations and visualisation, performs a Bed-B
reproducibility check, and bundles three biological-plausibility validation suggestions: S-0088-02
(AIS-to-soma Nav ratio audit, where t0088 cluster 1 reported a 116x ratio against Werginz 2024's
17.3 +/- 3 = +33 sigma), S-0086-02 (NMDA-units calibration of `gnmda_dend` against the Sivyer 2013
per-spine 0.1 nS prior, currently +85 to +116 sigma exotic across t0088 clusters), and S-0088-01
(causal NaP-knockout per cluster representative, attempting to falsify the >87 percent NaP
attribution from t0088). The validated generator is the input to t0091's joint 68-d (54-d
electrophys + 14-d morphology) NSGA-II optimisation.

## Category Selection Rationale

t0090's scope is unusually broad because it bundles a generator-implementation step with a 3-prior
validation triplet. Five categories are core. **`compartmental-modeling`** is consulted for the
generator-to-NEURON pipeline and for prior compartmental DSGC ports against which the Bed-B
reproducibility check is run. **`dendritic-computation`** is consulted for the dendritic-spike,
electrotonic-subunit, and intrinsic-DS literature that motivates many of the 14 knobs (especially
the asymmetry knobs). **`direction-selectivity`** is consulted for DSGC-specific morphological
asymmetry data (soma displacement, field elongation) and for the network priors needed to interpret
the validation bundle. **`retinal-ganglion-cell`** is consulted because all bio priors in the
project (AIS, NMDA, NaP, GABA) are RGC-targeted. **`voltage-gated-channels`** is consulted for the
AIS Nav and dendritic NaP density priors directly involved in Phase G.1 and G.3.

Three additional categories are consulted but yield smaller cited sets. **`cable-theory`** supplies
Rall's law and the equivalent-cylinder framework that motivates the `rall_exponent` knob.
**`synaptic-integration`** supplies the NMDA-spine literature (Sivyer 2013 source for the 0.1 nS
prior) that drives Phase G.2. **`patch-clamp`** is consulted as the ground-truth methodology
underlying the bio priors but does not directly motivate generator knobs.

The category **`wsd-evaluation`** and similar tags from the template were excluded as not relevant
to retinal compartmental modelling.

## Key Findings

### Single-Parameter Constructive Generators Suffice for Cell-Class-Level Morphological Realism

Cuntz and colleagues showed that a single scalar balancing factor `bf` (typical biological range
**0.2-0.7**) plus a target spanning-field density profile is enough to reproduce Sholl
intersections, branch-order distributions, total dendritic length within a few percent, and
electrotonic compartmentalisation across cell classes as different as fly LPTCs, hippocampal CA1
pyramidal cells, and cerebellar Purkinje cells [Cuntz2010]. The generator is a greedy
minimum-spanning-tree variant with cost `wiring_cost + bf * path_length_cost`, where `bf=0` reduces
to a pure MST and `bf -> infinity` approaches a star graph from the root. The TREES toolbox bundles
this generator with morphometric analyses and a Rall-law diameter-tapering routine that satisfies
the **3/2 power rule**. The headline practical lesson for t0090 is that the dimensionality of a
useful generator is small: the whole low-`bf` end of the family is electrotonically fragmented into
many independent subunits, the high-`bf` end is electrotonically compact, and biologically realistic
arbors live in a narrow intermediate band. A 14-parameter generator like t0090's is therefore
heavily over-parameterised relative to Cuntz, but the additional knobs are needed to capture the
**asymmetry** dimension that is central to DSGC morphology [Vaney2012, Briggman2011] and that Cuntz
explicitly excludes (Cuntz spans symmetric envelopes only).

A complementary lesson comes from the broader compartmental-modelling literature: morphology is a
first-class determinant of firing pattern, not just a passive scaffold. Mainen and Sejnowski showed
that applying the same set of Na, K, and Ca conductances to four different cortical morphologies
reproduces the four canonical firing patterns (regular-spiking, bursting, fast-spiking,
low-threshold) without changing any biophysical parameter [Mainen1996]. For t0090, this implies that
scoring 60 morphologies with a fixed t0083 best-cell channel set will reveal real morphology effects
(and therefore is a meaningful diversity test), but it also predicts that some of the 60
morphologies will fail the verification simulation (e.g., enter depolarisation block or silence)
even though their channels were tuned for the Bed-B morphology. The pass criterion of "60/60
simulate cleanly" is therefore optimistic; an acceptable negative is documented in the task
description ("if 60/60 do not all simulate cleanly, narrow the LHS bounds before t0091").

### DSGC Direction Selectivity Lives in a Combination of Wiring Asymmetry, Subcellular E/I, and

Active Dendrites — Not a Single Mechanism

The direction-selectivity literature converges on three coupled mechanisms. **(1) Wiring
asymmetry**: Briggman, Helmstaedter and Denk's serial block-face EM reconstruction of mouse retina
mapped 831 putative SAC-to-DSGC synapses across 6 DSGCs and 24 SACs; null-side SAC somata
contributed **524 synapses** vs only **41** from preferred-side somata (a **~12.8:1 ratio**), and
the SAC dendrite-to-null-direction angle was **165.2 +/- 51.7 degrees** [Briggman2011]. Vaney,
Sivyer and Taylor's review confirms a **~9x** larger inhibitory current from null-side vs
preferred-side SACs in rabbit DSGCs and synthesises this with developmental, pharmacological, and
modelling evidence [Vaney2012]. **(2) Subcellular E/I co-tuning**: deRosenroll, Sethuramanujam and
Awatramani showed that locally co-correlated ACh+GABA release at single starburst varicosities
sustains DSI ~**0.39**, while decorrelating release collapses DSI to ~**0.25** even when global E/I
balance is preserved [deRosenroll2026]. **(3) Active dendritic integration**: Sivyer and Williams
demonstrated by simultaneous somatic and terminal-dendritic patch-clamp that preferred-direction
moving bars elicit fast dendritic spikes that precede somatic APs and that null-direction inhibition
vetoes spike initiation locally [Sivyer2013]. Schachter, Oesch, Smith and Taylor quantified this in
a compartmental model: PSP DSI **~0.2** at the soma is amplified to spike DSI **~0.8** through ~4x
non-linear gain at local dendritic-spike thresholds, with ~**1 nS** sufficient to trigger a distal
spike vs **3-4 nS** near the soma [Schachter2010].

Importantly for t0090, all three mechanisms are **morphology-sensitive but not
morphology-determined**. El-Quessny and Feller showed that asymmetric Hb9::GFP DSGCs have
significantly higher IPSC DSI (ON DSI **0.48 +/- 0.19**) than symmetric Trhr::GFP DSGCs (ON DSI
**0.34 +/- 0.14**), but both subtypes still produce strongly direction-selective spike output —
indicating that morphology contributes a measurable but not dominant fraction of DS [ElQuessny2021].
Hanson, Sethuramanujam and colleagues extended this by showing that DSGCs retain DS even when SAC
asymmetry is genetically removed, demonstrating that direction selectivity is a robust,
multi-mechanism phenotype [Hanson2019]. Vlasits and Feller showed that synaptic input
**distribution** (proximal-skewed for SACs) is independently computational — input location
matters beyond the dendritic envelope [Vlasits2016]. The implication for t0090 is that a successful
morphology sweep should produce a wide range of DSI values across the 60 morphologies but that
**none** should silence DSI completely — the t0083 best-cell channels carry their own DS through
network mechanisms.

### Biological Priors for AIS Nav, NMDA per Spine, and Distal NaP — and the Resulting Validation

Bundle

The validation bundle in Phase G targets three priors that t0086 and t0088 flagged as exotic. **AIS
Nav density and AIS-to-soma ratio**: Werginz, Kiraly and Zeck reported a calibrated five-tier
compartmental model of mouse alpha-RGCs with explicit channel densities (Table 1). The AIS-to-soma
Nav ratio is **17.3** (gNa_AIS = **1300 mS/cm^2** vs gNa_soma = **75 mS/cm^2**), and AIS Kv ratio is
**16.7** [Werginz2024]. Werginz, Raghuram and Fried independently reported an AIS-to-soma Nav
density ratio of **~7x** in OFF-alpha-T RGCs based on patch-clamp + Nav1.6 immunohistochemistry +
NEURON modelling [Werginz2020]. Goethals and Brette inferred AIS Nav conductance density of **~5500
S/m^2** (best fit; conservative lower bound **~1200 S/m^2** at d=1 um) from axial-current
measurements on mouse RGCs (n=14), with mean AIS length **31 +/- 6 um** and distal AIS diameter
**0.5 +/- 0.2 um** [Goethals2020]. Earlier foundational work by Kole and collaborators established
that the AIS requires high Nav density to support reliable spike initiation [Kole2008] and that Kv1
channels at the AIS shape the AP waveform [KoleLetzkus2007]. Hu and colleagues established the
Nav1.6/Nav1.2 functional split that motivates the AIS-vs-soma Nav-isoform partition in current DSGC
models [Hu2009].

t0088 cluster 1 reported AIS-to-soma Nav ratio = **116** (= +33 sigma above Werginz2024's 17.3 +/-
3), the most extreme single-prior violation across t0086 / t0088. The G.1 audit is necessary because
the project's `centroid_unnormalised.NAV16_AIS_GBAR / centroid_unnormalised.NAV16_SOMA_GBAR` ratio
could either be a real biological signal or could reflect (i) a near-zero soma value pinned by the
lower bound and inflating the ratio, (ii) heterogeneous individual cells averaged into a misleading
centroid, or (iii) a units mismatch. The published anchor (Werginz2024 = 17.3) is quantitatively
sharp [Werginz2024, Table 1] and the dispersion is small (sigma ~3), so the project should not
retreat from the prior — it should audit the ratio computation.

**NMDA per-spine conductance**: The project applies the Sivyer 2013 prior of **0.1 nS = 0.0001 uS**
per spine to the t0080 ParameterVector field `gnmda_dend`, producing +85 to +116 sigma exotic
verdicts across t0088 cluster centroids [Sivyer2013, abstract; t0088 compare_literature.md]. The
Sivyer 2013 number is a per-spine voltage-clamp measurement on RGC dendritic spines; the t0080
`gnmda_dend` is a NetCon weight feeding the Exp2NMDA synaptic mechanism. These two quantities can
differ by a per-cell area normalisation factor, by an effective open-channel-fraction factor, or by
a synapse-count normalisation. The G.2 calibration ablation maps NetCon weight to per-spine
effective open conductance during a stimulus and re-scores the cluster verdicts in corrected units.
The deRosenroll 2026 NEURON port uses gmax_NMDA = **140.85 pS** (= 0.000141 uS) per synapse
[deRosenroll2026], consistent in order of magnitude with Sivyer 2013, providing a sanity-check
target for the calibrated value.

**Distal NaP density**: t0088 reported distal NaP densities of **0.00242 to 0.00723 S/cm^2** across
the 4 cluster representatives, all rated exotic at +9 to +34 sigma above the Stuart 1999 /
Goldfinger 2000 cortical pyramidal prior of **0.0005 +/- 0.0002 S/cm^2** (note: those papers were
not downloadable in the project's corpus, but the prior values are inherited from t0086's
pre-existing literature comparison in `compare_literature.md`). t0088 attributed PD-minus-ND
fractional contributions correlationally as **NMDA 0%, Nav1.6 0.3-12.6%, NaP 87.4-99.7%** across the
4 representatives. The G.3 causal knockout sets `nap_dend_distal = 0` and re-measures DSI at 16
directions in cells 1604, 1634, 767 and 1639 to falsify the correlational attribution.

### Active Dendritic Integration in DSGCs Requires Distributed Voltage-Gated Sodium and Calcium

Schachter et al.'s NEURON model uses dendritic Nav at **40 mS/cm^2** (uniform) or **45-to-20
mS/cm^2** (gradient), Rm_dend **10-22 kOhm cm^2**, and Ri = **110 Ohm cm**, producing distal input
resistances **>1 GOhm** that support local spike generation [Schachter2010]. They quantify
space-clamp underestimation of distal conductances at **40-100%** — a critical correction factor
when calibrating any model against somatic voltage-clamp measurements. Sivyer and Williams confirmed
this experimentally [Sivyer2013]. London and Hausser reviewed dendritic computation more broadly,
emphasising that compartmentalised dendrites enable parallel computations within a single cell
[LondonHausser2005]. For t0090's verification phase, the take-away is that any 50-ms no-stim
stability check at V_rest = -70 mV must use the t0083 best-cell channels (which include dendritic
Nav, NaP, NMDA and GABA at distal locations) and tolerate the distal high-impedance that produces
larger noise voltages than at the soma. Failed simulations should be flagged but not necessarily
treated as morphology bugs — they may reflect channel-morphology incompatibility.

### Network Coupling and Subtype Heterogeneity Set Realistic Firing Targets

Trenholm and colleagues established peak firing rates for Hb9+ DSGCs in mouse retina under standard
moving-bar protocols (300 x 300 um bar at 600 um/s, 96 percent contrast, 8 directions): **198 +/- 14
Hz** preferred direction and **27 +/- 12 Hz** null direction under control, rising to **244 +/- 18
Hz** preferred and **202 +/- 14 Hz** null under picrotoxin (GABA-A block) [Trenholm2013]. Coupling
among Hb9+ DSGCs was reciprocal and weak (CC = **0.14 +/- 0.01**, gap-junction conductance **~1
nS**, low-pass cutoff **~10 Hz**). Werginz, Kiraly and Zeck extended firing-rate priors across
alpha-RGC subtypes: alpha-ON **278 +/- 37 Hz**, alpha-OFF sustained **270 +/- 53 Hz**, alpha-OFF
transient **346 +/- 44 Hz** at depolarisation block; AP duration FWHM **0.21-0.31 ms**
[Werginz2024]. Sivyer, Van Wyk and colleagues showed that ON-OFF DSGCs have broader velocity tuning
than ON-DSGCs, which is relevant context for interpreting the 8-direction bar protocol used in Phase
D [Sivyer2010]. These firing-rate ranges are the targets that t0090's Phase F Bed-B reproducibility
check should match within 5 percent for the 5 t0083 Pareto cells.

### Realistic Mouse-Retina Compartmental Models Set the Bar for Bed-B Reproducibility

Existing DSGC compartmental ports define the precision target. The deRosenroll 2026 NEURON model
implements a single ON-OFF DSGC with **341 membrane sections**, Ra = **100-200 Ohm cm**, Cm = **1
uF/cm^2**, gleak = **5e-5 S/cm^2**, eleak = **-60 to -65 mV**; gbar_Na = **150, 200, 30 mS/cm^2** at
soma / primary / distal; gbar_K = **35, 40, 25 mS/cm^2** [deRosenroll2026]. There is no explicit AIS
section. Synaptic mechanisms: ACh Exp2Syn (0.5/6 ms, 140.85 pS), GABA Exp2Syn (0.5/35 ms, 450.72
pS), NMDA Exp2NMDA (2/80 ms, 140.85 pS); SAC varicosities placed on the DSGC per the Briggman 2011
connectome (minimum 30 um SAC-soma to contact offset). The bed-B reference morphology is imported
through `RGCmodelGD.hoc` and is the substrate for t0024's port. Ezra-Tsur and colleagues built the
RSME (Retinal Stimulation Modeling Environment) framework that demonstrated SAC-DSGC simulations at
similar fidelity using a different software stack [Ezra-Tsur2021]. Poleg-Polsky's 2026 ML pipeline
explored compartmental models with 352 segments under bipolar inputs with varying offsets, weights,
kinetics, and dendritic biophysics, showing that direction selectivity admits multiple distinct
parameter regimes [PolegPolsky2026]. Srivastava, de Rosenroll and colleagues mapped the
spatiotemporal glutamate input distribution that drives DSGC dendrites [Srivastava2022]. These
papers establish that a successful bed-B reproducibility match should be quantified at the DSI /
PD-rate level rather than at the section-by-section voltage trace, because there are many parameter
combinations that produce equivalent macroscopic behaviour.

### Rall's Law and Dendritic Taper Connect Morphology to Cable Behaviour

Rall's 1967 paper established that an EPSP's somatic shape (rise time, half-width) is a predictable
function of input location along an equivalent-cylinder dendrite, and that the **3/2 power rule**
(d_parent^(3/2) = sum d_daughter^(3/2)) preserves the equivalent-cylinder reduction across branch
points [Rall1967]. Koch and Poggio extended this framework to retinal ganglion cells specifically,
arguing that RGC dendritic morphology can be functionally interpreted via cable theory
[KochPoggio1982]. Cuntz uses a quadratic taper that satisfies Rall's 3/2 rule on the spanning-tree
output [Cuntz2010]; Fohlmeister and Miller used cell geometry constraints in their RGC modelling
[FohlmeisterMiller1997]. Hines and Carnevale's NEURON simulator is the canonical platform used by
all these models and the one t0090 generates sections for [Hines1997].

For t0090's Phase A, the `rall_exponent` knob (range 0.5-2.0) generalises the canonical exponent of
1.5 (Rall's 3/2 power rule) to capture deviations observed in real DSGCs; values >1.5 produce
relative dendritic thickening (more compact), values <1.5 produce more attenuation. The knob range
is appropriate; the centre value should be 1.5 (Rall canonical) for the Bed-B base point.

## Methodology Insights

* **Generator design follows Cuntz's parameter-economy lesson but adds asymmetry**. Cuntz's `bf`
  works at 1 parameter, but Cuntz envelopes are symmetric. t0090's 14-knob generator adds 4 explicit
  asymmetry parameters (`soma_offset_pd_um`, `field_elongation_pd`, `branch_density_gradient_pd`,
  `primary_branch_pd_concentration`) on top of 5 topology and 3 geometry knobs, which is appropriate
  for DSGC morphology where wiring and dendritic asymmetries are biologically necessary
  [Briggman2011, Vaney2012, ElQuessny2021]. The von Mises distribution for primary branch angles
  (kappa range 0-5) is a defensible choice given that EM reconstructions of DSGC primary branches
  show concentrated rather than uniform angular distributions [Briggman2011].

* **Use Rall canonical 1.5 as the centre of the `rall_exponent` knob**. The 0.5-2.0 range proposed
  in the task description is appropriate; **1.5** should be used as the Bed-B base-point value
  [Rall1967, Cuntz2010]. Values <1.0 produce strongly attenuating arbors that are unlikely to
  support electrotonic compartmentalisation; values >1.8 produce nearly cylindrical arbors that lose
  the natural DSGC distal high-impedance.

* **Diameter conventions**: target distal d = **0.5 +/- 0.2 um** (Goethals2020 AIS distal diameter
  is similar); proximal primary d in the 1.5-3 um range; soma d **8-18 um** matches the ranges
  reported for DSGCs and alpha-RGCs in mouse retina [Werginz2024, Goethals2020]. The published Bed-B
  morphology has soma ~15 um [Schachter2010, deRosenroll2026].

* **AIS length range and centre**: Goethals2020 reports mean **31 +/- 6 um** and Werginz2020 reports
  **dorsal > ventral** AIS lengths in OFF-alpha-T cells; the t0090 range of 15-60 um is appropriate,
  with the Bed-B base point matching the published AIS length (or 31 um if Bed-B has no explicit
  AIS, in which case the generator's AIS is a new compartment).

* **Verification simulation protocol matches the recorded researcher protocol**: 1400 ms trial
  length, HH off for EPSP/IPSP traces, HH on for Vm / firing rate / DSI mode (per the recorded
  preference). Standard mode trio EPSP_PASSIVE / IPSP_PASSIVE / FULL. Drop the per-synapse
  activation histogram. 50 ms no-stim stability check at V_rest = -70 mV before each direction
  trial. **Best practice**: catch NaN voltages, divergence, and disconnected sections per morphology
  and write a stability flag — do not silently skip failed cells.

* **Bed-B base-point choice**: published anchor values are `num_primary_branches` matching the
  published count (deRosenroll2026 / Bed-B from t0024); `mean_segment_length_um` calibrated to match
  the published total dendritic length (~341 sections in deRosenroll2026 implies a coarse segment
  length, ~1300 um total dendritic extent given 4 primary branches and the rabbit On-Off envelope
  reported in [Schachter2010]); `soma_offset_pd_um=0`; `field_elongation_pd=1.0`;
  `branch_density_gradient_pd=0`; `primary_branch_pd_concentration=0`; `rall_exponent=1.5`;
  `soma_diameter_um=15`; `ais_length_um=31`. These produce a near-symmetric Bed-B equivalent.

* **DSI / firing-rate target ranges for the Bed-B reproducibility check**: peak preferred-direction
  rate **198 +/- 14 Hz** and peak null-direction rate **27 +/- 12 Hz** under control [Trenholm2013];
  spike DSI **~0.8** [Schachter2010, Sivyer2013]. The 5 percent Bed-B match criterion in the task
  description is stricter than the natural cell-to-cell variability (which is order of 10-15
  percent) — be prepared for the criterion to fail and document it as a warning rather than a hard
  fail.

* **Validation bundle execution sequence**: do G.1 (AIS-to-soma audit) first because it requires
  only existing JSON outputs from t0088 and t0086 (~30 min, $0). Do G.2 (NMDA calibration) second;
  it is one cell, varying `gnmda_dend` from 1e-5 to 1e-2 uS in a log sweep (probably 10 levels), and
  reading per-spine effective open conductance from the NEURON state during stimulus (~1 hour,
  ~$0.30 on Vast.ai). Do G.3 (NaP knockout) last because it is the most expensive (~64 min wall
  clock for 4 cells x 16 directions on local CPU, $0).

* **Hypothesis: a 14-knob generator over-parameterises DSGC morphology relative to Cuntz**. Cuntz
  shows 1-3 parameters suffice for cell-class-level realism. The extra asymmetry knobs in t0090 are
  biologically motivated by DSGC-specific data, but the topology knobs (especially
  `branch_prob_per_um` and `max_strahler_depth`) likely correlate strongly with each other and with
  `mean_segment_length_um`. The diversity test should reveal this through morphometric PCA: if PC1
  + PC2 explain >80 percent of variance across the 30 different morphologies, the effective
    dimensionality is much lower than 14 and t0091's joint NSGA-II should warm-start at a reduced
    morphology basis.

## Gaps and Limitations

* **No DSGC-specific procedural morphology generator in the literature**. Cuntz's TREES toolbox was
  validated on fly LPTCs, hippocampal CA1, and cerebellar Purkinje cells but never explicitly on
  DSGCs [Cuntz2010]. The asymmetry knobs in t0090 are therefore extrapolations from generic
  morphometric reasoning + DSGC-specific wiring data [Briggman2011, ElQuessny2021] — there is no
  paper validating that this combination produces realistic DSGC morphologies. The diversity-test
  output should be visually compared against published DSGC reconstructions to provide partial
  validation.

* **Stuart 1999 and Goldfinger 2000 NaP priors are not in the project's paper corpus**. The +9-34
  sigma exotic verdicts on distal NaP rely on prior values inherited from t0086's pre-existing
  literature comparison. This means the Phase G.3 NaP knockout uses an indirect prior. The Sivyer
  2010 paper [Sivyer2010] addresses DSGC velocity tuning but is silent on dendritic NaP density.
  This gap is a known limitation and motivates a future targeted RGC-NaP paper search (mentioned as
  S-0086-05 in the t0086 compare_literature.md).

* **Hu2009, Kole2008, Sivyer2013 download-blocked summaries are sparse**. These three papers are in
  the corpus but their full PDFs were not retrieved (paywalled), so the project relies on the
  abstract + secondary citations for AIS Nav1.6/1.2 split, AIS Nav density, and dendritic spike
  thresholds respectively [Hu2009, Kole2008, Sivyer2013]. Numerical priors quoted from these sources
  should be cross-checked against [Werginz2024], which provides a fully accessible five-tier
  compartmental Table 1 for mouse alpha-RGCs.

* **No validation framework specifically for procedural morphology generators in DSGCs**. Cuntz
  validates against Sholl, branch order, total length [Cuntz2010]; t0090 follows this pattern with
  PCA and visual side-by-side panels but does not have an explicit acceptance criterion for "the
  generator covers the DSGC space" beyond the qualitative pass criteria in the task description.
  This is a real gap — the diversity test is essentially exploratory rather than statistically
  certifiable.

* **The Bed-B 5 percent match criterion may not be achievable**. Cell-to-cell variability in
  measured DSI / firing rate is typically 10-20 percent [Trenholm2013, Werginz2024], so requiring
  the procedural generator to reproduce a single Bed-B point within 5 percent across 5 different
  Pareto cells is asking for less variability than exists biologically. Document an acceptable
  fall-back of 10 percent in the implementation.

* **NMDA per-spine vs per-synapse vs NetCon-weight units mismatch is not resolved in the
  literature**. Sivyer 2013's 0.1 nS prior is per-spine voltage-clamp, deRosenroll 2026 uses 140.85
  pS in Exp2NMDA NetCon weight [Sivyer2013, deRosenroll2026], and the project's `gnmda_dend` is a
  third quantity. No paper provides a calibrated mapping between these three units. Phase G.2 is
  therefore producing a calibration that is not reproducible from existing literature alone.

## Recommendations for This Task

1. **Use Rall canonical 1.5 as the `rall_exponent` Bed-B base point** [Rall1967, Cuntz2010]. The
   0.5-2.0 range is correct; the centre matters because diameter taper directly determines distal
   input impedance, which controls dendritic spike threshold [Schachter2010].

2. **Set the von Mises kappa upper bound at 5** as proposed in the task description, but also test
   kappa=0 (uniform) at the Bed-B base point. Real DSGC primary-branch angular distributions are
   moderately concentrated [Briggman2011] but published values for kappa do not exist; the diversity
   test will reveal whether kappa>0 produces visibly different field geometries than kappa=0.

3. **Match the deRosenroll 2026 NEURON Ra / gleak / eleak / dimensions in the Bed-B base point**: Ra
   = 100 Ohm cm, gleak = 5e-5 S/cm^2, eleak = -60 mV; soma diameter 15 um; ~341 sections target
   [deRosenroll2026]. This makes the Phase F reproducibility comparison apples-to-apples.

4. **Write the verification simulation to log NaN / divergence / disconnected-section flags
   per-morphology**, not as a single pass / fail [Mainen1996, Schachter2010]. Some of the 30
   different morphologies will likely fail the verification because the t0083 best-cell channels
   were tuned for the Bed-B morphology, not arbitrary morphologies. Failed morphologies are
   informative; preserve them in `verification_summary.json` for t0091's warm-start filter.

5. **Phase G.1 audit should check three things in order**: (i) units of
   `centroid_unnormalised.NAV16_AIS_GBAR` and `centroid_unnormalised.NAV16_SOMA_GBAR` are both
   S/cm^2 (dimensionless ratio); (ii) per-cell ratios of the 4 cluster-1 cells (1304, 1504, 1624,
   1634\) — if individual cells are near 116 then it is real; if cells span a wide range and the
   centroid is the average then the centroid is misleading; (iii) whether the soma lower bound is
   pinning the denominator [Werginz2024].

6. **Phase G.2 calibration should use a single t0080 cell at multiple `gnmda_dend` levels (e.g.,
   1e-5, 5e-5, 1e-4, 5e-4, 1e-3, 5e-3, 1e-2 uS) and measure NEURON state during stimulus**. The
   target sanity-check is that the deRosenroll 2026 value of 140.85 pS / Exp2NMDA equates to ~0.1 nS
   effective open conductance under typical voltage trajectories [Sivyer2013, deRosenroll2026]. If
   the calibration shifts t0088 cluster verdicts from exotic to plausible, the 85+ sigma verdict is
   a units artefact; if not, the verdict is genuine and motivates tightened gnmda_dend bounds for
   t0091.

7. **Phase G.3 NaP knockout pass criterion**: DSI < **0.2** in all 4 cluster representatives if NaP
   is causally responsible (consistent with the +87.4 to +99.7 percent attribution from t0088). If
   DSI remains > 0.4 after `nap_dend_distal = 0`, the correlation between NaP density and
   PD-minus-ND is misleading and another mechanism (likely NMDA + GABA cooperation) carries the DS
   signal. A partial collapse (DSI 0.2-0.4) confirms NaP as a major contributor but rules out
   exclusive dominance [Sivyer2013, Schachter2010].

8. **Bed-B base-point firing-rate target**: peak PD rate ~**198 Hz**, peak ND rate ~**27 Hz**, spike
   DSI ~**0.8** [Trenholm2013, Schachter2010]. Document the achieved values explicitly in the answer
   asset; if they fall outside +/-15 percent, treat as a generator-vs-Bed-B unit issue rather than a
   t0083-channel issue.

9. **Document the limitation that the morphology generator is not validated against DSGC
   reconstructions**. The task should explicitly note that the diversity test is exploratory and
   that t0091's NSGA-II warm-start should weigh Bed-B-equivalent and 4 other anchors more heavily
   than wild LHS samples [Cuntz2010, ElQuessny2021].

## Paper Index

### [Briggman2011]

* **Title**: Wiring specificity in the direction-selectivity circuit of the retina
* **Authors**: Briggman, K. L., Helmstaedter, M., Denk, W.
* **Year**: 2011
* **DOI**: `10.1038/nature09818`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nature09818/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`
* **Relevance**: First connectomic proof that DSGC direction selectivity has a structural wiring
  basis (12.8:1 null-vs-preferred SAC synapse ratio, mean dendrite-to-null angle 165.2 +/- 51.7
  degrees). Motivates the asymmetry knobs in t0090's generator and supports the
  `branch_density_gradient_pd` and `field_elongation_pd` parameters as biologically grounded.

### [Cuntz2010]

* **Title**: One Rule to Grow Them All: A General Theory of Neuronal Branching and Its Practical
  Application
* **Authors**: Cuntz, H., Forstner, F., Borst, A., Hausser, M.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000877`
* **Asset**:
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1371_journal.pcbi.1000877/`
* **Categories**: `compartmental-modeling`, `dendritic-computation`, `cable-theory`
* **Relevance**: Canonical procedural neuron morphology generator (TREES toolbox). Establishes the
  parameter-economy benchmark (single bf parameter for cell-class realism) that t0090's 14-knob
  generator should be compared against, and provides the Rall-3/2 diameter taper used by t0090's
  `rall_exponent` knob. Identified as the fall-back if t0090's generator slips beyond 3 days.

### [deRosenroll2026]

* **Title**: Uncovering the "hidden" synaptic microarchitecture of the retinal direction selective
  circuit
* **Authors**: deRosenroll, G., Sethuramanujam, S., Awatramani, G. B.
* **Year**: 2026
* **DOI**: `10.1016/j.celrep.2025.116833`
* **Asset**: `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/paper/10.1016_j.celrep.2025.116833/`
* **Categories**: `direction-selectivity`, `dendritic-computation`, `compartmental-modeling`,
  `retinal-ganglion-cell`, `synaptic-integration`
* **Relevance**: Bed-B reference morphology for the Phase F reproducibility check. Provides concrete
  passive parameters (Ra=100-200, Cm=1, gleak=5e-5, eleak=-60 to -65, 341 sections, Briggman 2011
  wiring with 30 um soma-contact offset) and Exp2NMDA gmax=140.85 pS as the sanity-check target for
  the Phase G.2 NMDA calibration.

### [ElQuessny2021]

* **Title**: Dendrite Morphology Minimally Influences the Synaptic Distribution of Excitation and
  Inhibition in Retinal Direction-Selective Ganglion Cells
* **Authors**: El-Quessny, M., Feller, M. B.
* **Year**: 2021
* **DOI**: `10.1523/ENEURO.0261-21.2021`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_ENEURO.0261-21.2021/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `dendritic-computation`
* **Relevance**: Demonstrates that asymmetric vDSGCs have higher IPSC DSI (0.48 vs 0.34) than
  symmetric nDSGCs but both still show strong spike DS. Constrains how much of the DSI variance in
  t0090's diversity test should be attributable to morphology vs network mechanisms.

### [Ezra-Tsur2021]

* **Title**: Realistic retinal modeling unravels the differential role of excitation and inhibition
  to starburst amacrine cells
* **Authors**: Ezra-Tsur, E., Amsalem, O., et al.
* **Year**: 2021
* **DOI**: `10.1371/journal.pcbi.1009754`
* **Asset**:
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1371_journal.pcbi.1009754/`
* **Categories**: `compartmental-modeling`, `direction-selectivity`, `retinal-ganglion-cell`
* **Relevance**: Alternative SAC-DSGC simulation framework (RSME) showing that multiple software
  stacks reproduce the canonical DS phenotype. Supports the t0090 conclusion that bed-B
  reproducibility should be tested at the macroscopic DSI level rather than at section-by-section
  voltages.

### [FohlmeisterMiller1997]

* **Title**: Mechanisms by Which Cell Geometry Controls Repetitive Impulse Firing in Retinal
  Ganglion Cells
* **Authors**: Fohlmeister, J. F., Miller, R. F.
* **Year**: 1997
* **DOI**: `10.1152/jn.1997.78.4.1948`
* **Asset**:
  `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1152_jn.1997.78.4.1948/`
* **Categories**: `voltage-gated-channels`, `retinal-ganglion-cell`, `compartmental-modeling`
* **Relevance**: Early demonstration that RGC cell geometry (soma size, dendritic field) controls
  repetitive firing patterns through Rall-cable coupling between active dendrites and the spike
  initiation zone. Supports the t0090 hypothesis that soma diameter and AIS length are first-order
  morphology knobs.

### [Goethals2020]

* **Title**: Electrical match between initial segment and somatodendritic compartment for action
  potential backpropagation in retinal ganglion cells
* **Authors**: Goethals, S., Sierksma, M. C., et al.
* **Year**: 2020
* **DOI**: `10.1101/2020.09.15.297937`
* **Asset**:
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/paper/10.1101_2020.09.15.297937/`
* **Categories**: `voltage-gated-channels`, `retinal-ganglion-cell`, `compartmental-modeling`,
  `patch-clamp`
* **Relevance**: Direct functional measurement of mouse RGC AIS axial current (-6.7 +/- 1.8 nA) and
  inferred AIS Nav conductance density (~5500 S/m^2 best fit, conservative lower bound 1200 S/m^2).
  Calibrates the AIS Nav density bounds for t0090's `ais_length_um` knob (mean AIS length 31 +/- 6
  um, distal d 0.5 +/- 0.2 um) and provides the resistive coupling theory underlying Phase G.1.

### [Hanson2019]

* **Title**: Retinal direction selectivity in the absence of asymmetric starburst amacrine cell
  responses
* **Authors**: Hanson, L., Sethuramanujam, S., et al.
* **Year**: 2019
* **DOI**: `10.7554/eLife.42392`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.7554_eLife.42392/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`
* **Relevance**: Shows DSGCs retain direction selectivity even without asymmetric SAC responses,
  proving the multi-mechanism nature of DS. Constrains the t0090 expectation that no morphology in
  the diversity sweep should completely abolish DSI under the t0083 best-cell channels.

### [Hines1997]

* **Title**: The NEURON Simulation Environment
* **Authors**: Hines, M. L., Carnevale, N. T.
* **Year**: 1997
* **DOI**: `10.1162/neco.1997.9.6.1179`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1162_neco.1997.9.6.1179/`
* **Categories**: `compartmental-modeling`
* **Relevance**: Canonical reference for the NEURON simulator that t0090's generator emits sections
  for. Defines the d_lambda discretisation rule that t0090's Phase D verification simulations must
  follow.

### [Hu2009]

* **Title**: Distinct contributions of Nav1.6 and Nav1.2 in action potential initiation and
  backpropagation
* **Authors**: Hu, W., Tian, C., et al.
* **Year**: 2009
* **DOI**: `10.1038/nn.2359`
* **Asset**: `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1038_nn.2359/`
* **Categories**: `voltage-gated-channels`, `patch-clamp`
* **Relevance**: Establishes the Nav1.6/Nav1.2 functional split that motivates the project's
  AIS-vs-soma Nav-isoform partition. Cited but with the caveat that the local summary is sparse
  (paywall-blocked); numerical claims default to Werginz 2024.

### [KochPoggio1982]

* **Title**: Retinal ganglion cells: a functional interpretation of dendritic morphology
* **Authors**: Koch, C., Poggio, T.
* **Year**: 1982
* **DOI**: `10.1098/rstb.1982.0084`
* **Asset**: `tasks/t0015_literature_survey_cable_theory/assets/paper/10.1098_rstb.1982.0084/`
* **Categories**: `cable-theory`, `dendritic-computation`, `retinal-ganglion-cell`
* **Relevance**: Foundational cable-theory interpretation of RGC dendritic morphology. Justifies the
  focus on dendritic geometry as a first-class computational variable in t0090.

### [Kole2008]

* **Title**: Action potential generation requires a high sodium channel density in the axon initial
  segment
* **Authors**: Kole, M. H. P., Ilschner, S. U., et al.
* **Year**: 2008
* **DOI**: `10.1038/nn2040`
* **Asset**: `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1038_nn2040/`
* **Categories**: `voltage-gated-channels`, `patch-clamp`
* **Relevance**: Foundational AIS Nav density paper. The project's t0086 / t0088 prior comparison
  cites Kole 2008 for the AIS Nav band 0.25-0.5 S/cm^2 against which Werginz 2024's 1.3 S/cm^2 is
  ~3x higher. Motivates the "AIS prior conflict" gap discussed in the validation bundle.

### [KoleLetzkus2007]

* **Title**: Axon Initial Segment Kv1 Channels Control Axonal Action Potential Waveform and Synaptic
  Efficacy
* **Authors**: Kole, M. H. P., Letzkus, J. J., Stuart, G. J.
* **Year**: 2007
* **DOI**: `10.1016/j.neuron.2007.07.031`
* **Asset**:
  `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1016_j.neuron.2007.07.031/`
* **Categories**: `voltage-gated-channels`, `patch-clamp`
* **Relevance**: Establishes Kv1 channel role at the AIS in shaping AP waveform. Supports the
  five-tier compartmental partitioning in Werginz 2024 that t0090's `ais_length_um` knob feeds into.

### [LondonHausser2005]

* **Title**: Dendritic Computation
* **Authors**: London, M., Hausser, M.
* **Year**: 2005
* **DOI**: `10.1146/annurev.neuro.28.061604.135703`
* **Asset**:
  `tasks/t0016_literature_survey_dendritic_computation/assets/paper/10.1146_annurev.neuro.28.061604.135703/`
* **Categories**: `dendritic-computation`, `cable-theory`
* **Relevance**: Foundational review of dendritic computation. Provides conceptual framework for why
  morphology + active conductances jointly determine cell function — relevant to the
  diversity-test rationale.

### [Mainen1996]

* **Title**: Influence of dendritic structure on firing pattern in model neocortical neurons
* **Authors**: Mainen, Z. F., Sejnowski, T. J.
* **Year**: 1996
* **DOI**: `10.1038/382363a0`
* **Asset**: `tasks/t0015_literature_survey_cable_theory/assets/paper/10.1038_382363a0/`
* **Categories**: `cable-theory`, `compartmental-modeling`, `dendritic-computation`
* **Relevance**: Landmark demonstration that dendritic morphology alone (with fixed channels) can
  reproduce four canonical firing patterns. Predicts that some of t0090's 60 morphologies will
  produce qualitatively different firing under the t0083 best-cell channels, justifying the
  per-morphology stability flag.

### [PolegPolsky2026]

* **Title**: Machine learning discovers numerous new computational principles underlying direction
  selectivity in the retina
* **Authors**: Poleg-Polsky, A.
* **Year**: 2026
* **DOI**: `10.1038/s41467-026-70288-4`
* **Asset**: `tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/`
* **Categories**: `direction-selectivity`, `compartmental-modeling`
* **Relevance**: ML pipeline exploring 352-segment compartmental DSGC models showing multiple
  parameter regimes produce similar DS phenotypes. Justifies the t0090 expectation that the
  generator's diversity test will reveal multiple distinct morphology classes that all support
  meaningful DS.

### [Rall1967]

* **Title**: Distinguishing theoretical synaptic potentials computed for different soma-dendritic
  distributions of synaptic input
* **Authors**: Rall, W.
* **Year**: 1967
* **DOI**: `10.1152/jn.1967.30.5.1138`
* **Asset**: `tasks/t0015_literature_survey_cable_theory/assets/paper/10.1152_jn.1967.30.5.1138/`
* **Categories**: `cable-theory`, `dendritic-computation`
* **Relevance**: Establishes the equivalent-cylinder framework and the 3/2 power rule for dendrite
  diameter taper. Defines the canonical 1.5 value at the centre of t0090's `rall_exponent` knob
  (range 0.5-2.0).

### [Schachter2010]

* **Title**: Dendritic Spikes Amplify the Synaptic Signal to Enhance Detection of Motion in a
  Simulation of the Direction-Selective Ganglion Cell
* **Authors**: Schachter, M. J., Oesch, N., Smith, R. G., Taylor, W. R.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000899`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1371_journal.pcbi.1000899/`
* **Categories**: `compartmental-modeling`, `direction-selectivity`, `dendritic-computation`,
  `retinal-ganglion-cell`, `voltage-gated-channels`
* **Relevance**: Reference compartmental DSGC model. Provides Rm/Ri/Cm conventions, dendritic Nav
  densities (40 mS/cm^2 uniform or 45-to-20 mS/cm^2 gradient), distal Rin >1 GOhm, and the 4x
  PSP-to-spike DSI amplification target (PSP DSI ~0.2, spike DSI ~0.8). Sets the expected
  firing-rate target for the Bed-B reproducibility check and the >1 nS distal / 3-4 nS proximal
  spike threshold.

### [Sivyer2010]

* **Title**: Synaptic inputs and timing underlying the velocity tuning of direction-selective
  ganglion cells in rabbit retina
* **Authors**: Sivyer, B., Van Wyk, M., Vaney, D. I., Taylor, W. R.
* **Year**: 2010
* **DOI**: `10.1113/jphysiol.2010.192716`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1113_jphysiol.2010.192716/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`,
  `patch-clamp`
* **Relevance**: Establishes velocity-tuning differences between ON-OFF and ON DSGCs. Provides
  context for why t0090's 8-direction bar protocol at fixed velocity is appropriate for ON-OFF DSGCs
  but a velocity sweep would be needed to fully characterise an ON-DSGC port.

### [Sivyer2013]

* **Title**: Direction selectivity is computed by active dendritic integration in retinal ganglion
  cells
* **Authors**: Sivyer, B., Williams, S. R.
* **Year**: 2013
* **DOI**: `10.1038/nn.3565`
* **Asset**: `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1038_nn.3565/`
* **Categories**: `direction-selectivity`, `dendritic-computation`, `retinal-ganglion-cell`,
  `patch-clamp`
* **Relevance**: Source paper for the per-spine NMDA conductance prior used in the project's
  bio-comparison framework. The 0.1 nS = 1e-4 uS per-spine value is the basis for the +85 to +116
  sigma exotic verdicts in t0088 and the target of the Phase G.2 calibration ablation. Also
  establishes that DS computation requires active dendritic integration (TTX collapses DSI) — a
  load-bearing claim for Phase G.3.

### [Srivastava2022]

* **Title**: Spatiotemporal properties of glutamate input support direction selectivity in the
  dendrites of retinal ganglion cells
* **Authors**: Srivastava, P., de Rosenroll, G., et al.
* **Year**: 2022
* **DOI**: `10.7554/eLife.81533`
* **Asset**:
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.7554_eLife.81533/`
* **Categories**: `direction-selectivity`, `synaptic-integration`, `retinal-ganglion-cell`
* **Relevance**: Maps the spatiotemporal glutamate input distribution that drives DSGC dendrites,
  complementing the Briggman 2011 wiring-asymmetry connectome that informs t0090's asymmetry knobs.

### [Trenholm2013]

* **Title**: Dynamic Tuning of Electrical and Chemical Synaptic Transmission in a Network of Motion
  Coding Retinal Neurons
* **Authors**: Trenholm, S., McLaughlin, A. J., Schwab, D. J., Awatramani, G. B.
* **Year**: 2013
* **DOI**: `10.1523/JNEUROSCI.0808-13.2013`
* **Asset**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.0808-13.2013/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `patch-clamp`,
  `synaptic-integration`
* **Relevance**: Authoritative source for mouse Hb9+ DSGC peak firing rates: 198 +/- 14 Hz
  preferred, 27 +/- 12 Hz null under control. Sets the firing-rate target for the Phase F Bed-B
  reproducibility check.

### [Vaney2012]

* **Title**: Direction selectivity in the retina: symmetry and asymmetry in structure and function
* **Authors**: Vaney, D. I., Sivyer, B., Taylor, W. R.
* **Year**: 2012
* **DOI**: `10.1038/nrn3165`
* **Asset**: `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nrn3165/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `dendritic-computation`,
  `synaptic-integration`
* **Relevance**: Canonical review establishing that DSGC directional asymmetry has structural,
  synaptic and active-dendritic components. Motivates t0090's 4 explicit asymmetry knobs and
  contextualises the diversity test as a sweep over a biologically meaningful asymmetry space.

### [Vlasits2016]

* **Title**: A Role for Synaptic Input Distribution in a Dendritic Computation of Motion Direction
  in the Retina
* **Authors**: Vlasits, A. L., Morrie, R. D., et al.
* **Year**: 2016
* **DOI**: `10.1016/j.neuron.2016.02.020`
* **Asset**:
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1016_j.neuron.2016.02.020/`
* **Categories**: `direction-selectivity`, `dendritic-computation`, `synaptic-integration`,
  `retinal-ganglion-cell`
* **Relevance**: Shows that synaptic input location along a dendrite is a computational variable
  independent of morphology. Constrains the t0090 interpretation that the diversity test is
  measuring morphology-only effects (synaptic placement is held fixed at Bed-B convention).

### [Werginz2020]

* **Title**: Tailoring of the axon initial segment shapes the conversion of synaptic inputs into
  spiking output in OFF-alphaT retinal ganglion cells
* **Authors**: Werginz, P., Raghuram, V., Fried, S. I.
* **Year**: 2020
* **DOI**: `10.1126/sciadv.abb6642`
* **Asset**: `tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1126_sciadv.abb6642/`
* **Categories**: `voltage-gated-channels`, `retinal-ganglion-cell`, `compartmental-modeling`,
  `patch-clamp`
* **Relevance**: Reports an AIS-to-soma Nav density ratio of ~7x in OFF-alpha-T mouse RGCs and
  establishes AIS length as the dominant morphological predictor of maximum firing rate. Provides a
  second AIS-to-soma anchor (alongside Werginz 2024's 17.3) for the Phase G.1 audit.

### [Werginz2024]

* **Title**: Differential Intrinsic Firing Properties in Sustained and Transient Mouse alpha-RGCs
* **Authors**: Werginz, P., Kiraly, V., Zeck, G.
* **Year**: 2024
* **DOI**: `10.1523/JNEUROSCI.1592-24.2024`
* **Asset**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.1592-24.2024/`
* **Categories**: `voltage-gated-channels`, `compartmental-modeling`, `retinal-ganglion-cell`,
  `patch-clamp`
* **Relevance**: Five-tier compartmental model of mouse alpha-RGCs with explicit per-tier channel
  densities (gNa AIS=1300, soma=75 mS/cm^2; AIS-to-soma Nav ratio = 17.3 +/- 3). The reference prior
  against which t0088 cluster 1's 116x ratio is rated +33 sigma exotic; primary source for the Phase
  G.1 audit.
