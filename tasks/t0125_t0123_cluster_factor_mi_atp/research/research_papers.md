---
spec_version: "1"
task_id: "t0125_t0123_cluster_factor_mi_atp"
research_stage: "papers"
papers_reviewed: 19
papers_cited: 17
categories_consulted:
  - "compartmental-modeling"
  - "voltage-gated-channels"
  - "dendritic-computation"
  - "cable-theory"
  - "retinal-ganglion-cell"
  - "direction-selectivity"
  - "synaptic-integration"
date_completed: "2026-05-25"
status: "complete"
---
# Research Papers — Cluster + Factor Analysis of t0123 Cells (MI vs ATP-per-Spike)

## Task Objective

This task applies the canonical t0108 / t0116 / t0117 cluster-and-factor pipeline (PCA + KMeans on
electrophys (54-d) and morphology (14-d) subspaces + Kaiser-cap varimax factor analysis on the full
68-d vector) to the t0123 single-seed NSGA-II run that optimised spike-count mutual information
(`mi_count_bits`, Strong-Bialek-direct surrogate) against ATP-per-spike (Sengupta-style integrated
Na+ load), with 5 760 dedup-unique cells evaluated under seed 441. The substantive deliverables are
four answer assets: (1) is there a joint latent factor driving both MI and ATP, or are the two
objectives driven by decoupled factors; (2) which electrophys parameters most distinguish high-MI
from low-MI cells; (3) which morphology parameters most distinguish low-ATP from high-ATP cells; and
(4) which combined signature distinguishes the Pareto-favoured corner (high MI, low ATP) from the
dominated corner (low MI, high ATP). The literature review below establishes the prior on what such
a 68-d substrate is expected to look like once it is dissected by PCA, KMeans, and varimax factor
analysis, and what specific numbers (Na+ overlap factor, MI bits-per-spike ceiling, channel
co-variation patterns) the four answer assets should be calibrated against.

## Category Selection Rationale

Seven categories from `meta/categories/` were consulted. **`compartmental-modeling`** is the
methodological substrate — every MOO / parameter-ensemble paper this task relies on
[Hay2011, Druckmann2007, Achard2006, Prinz2004, VanGeit2016] is a compartmental-model fitting study,
and the cluster + factor pipeline (t0108 / t0116 / t0117) is itself a compartmental-model
ensemble-analysis tool. **`voltage-gated-channels`** is core because the 54-d electrophys subvector
is dominated by Na, K, Ca, and HCN channel densities whose interactions are the canonical site of
parameter degeneracy [Marder2006, Prinz2004, Achard2006] and whose Na+/K+ kinetic overlap directly
controls ATP-per-spike [Sengupta2010, Attwell2001]. **`dendritic-computation`** supports the
hypothesis that dendritic structure (14 morphology parameters) and dendritic channel density jointly
shape both MI and ATP [LondonHausser2005, Mainen1996]. **`cable-theory`** is consulted because cable
properties (axial resistance, compartment length and diameter) drive how dendritic Na+ load
translates into spike generation and therefore ATP cost [KochPoggio1982, Mainen1996, Cuntz2010].
**`retinal-ganglion-cell`** is core because the cells under analysis are mouse-style DSGCs, the only
RGC information-rate measurement in the corpus is in an RGC [Dhingra2004], and the RGC HH machinery
[FohlmeisterMiller1997] is what physically generates the Na+ load this task clusters. The
**`direction-selectivity`** and **`synaptic-integration`** categories are consulted because t0123
preserves a DSI/PD-rate diagnostic alongside MI/ATP and the question of whether high-MI cells are
also high-DSI cells (or anti-correlated) is one the cluster output should answer; however no DS or
synaptic-integration paper is directly cited because the task does not optimise DSI and the
canonical DS references are already extensively used by the t0078 / t0080 / t0091 lineage.

Excluded category: **`patch-clamp`** was scanned but contributes no paper that directly informs the
68-d cluster / factor analysis methodology — patch-clamp papers in this corpus supply the
experimental ground truth for channel densities but not the high-d parameter-space dissection
toolkit. No paper in the corpus is dedicated to clustering / factor-analysis methodology *per se*;
the methodological precedents are drawn from MOO papers that cluster the resulting ensembles
([Druckmann2007, Achard2006, Prinz2004]) and from Baden 2016's RGC functional taxonomy [Baden2016]
which uses an analogous unsupervised-clustering pipeline on real RGC functional fingerprints.

## Key Findings

### High-Dimensional Conductance-Density Spaces Form Loosely Connected Hyperplanes, Not Blobs or Points

The single most important precedent for this task is [Achard2006]'s analysis of the 24-parameter
cerebellar Purkinje-cell parameter landscape. After running nine independent (57+19) self-adaptive
evolution-strategy runs of ~8 000 evaluations each (415 generations on a 10-node cluster), they
retained 20 acceptable models with fitness 2.58 to 3.45 (Achard & De Schutter 2006, Methods, p. 4).
The geometry of the "good" region was neither a single connected blob nor a set of isolated points,
but **a collection of loosely connected hyperplanes** — thin lower-dimensional manifolds. They
explicitly state that a 6- or 10-points-per-dimension grid search would miss ~65% of these solutions
because the good region is structured (Achard & De Schutter 2006, Discussion). Several individual
channels (gCaTm, gKAm, gKMd, gKhs) varied across their entire allowed range while others (gNaFs,
gCaPd, gKdrs, gKdrm) remained tightly bounded across the 20 acceptable models. This is the
qualitative shape the t0125 PCA on the 68-d t0123 substrate is expected to recover: high-MI and
low-ATP cells are likely to form a thin manifold within the 68-d cube rather than a compact ball,
and the varimax factor analysis is the right tool for reading off which combinations of channels
co-vary along that manifold.

[Prinz2004] gives the quantitative back-up at network scale: brute-force simulation of **20 250 000
three-cell pyloric STG networks** yielded **4 047 375 networks (20%)** that produced a pyloric-like
triphasic rhythm and **452 516 networks (2.2%)** that matched all 15 quantitative criteria
[Prinz et al. 2004, Results, Table 2]. Every one of the 150 cell-combination configurations and the
full functional range of every synaptic conductance was represented in the matching set, with one
notable exception (LP-to-PY). This is the empirical demonstration of "many models, one behaviour"
that [Marder2006] reviews as parameter degeneracy: individual channel densities can vary two- to
fourfold across cells of the same identified type while activity profiles remain conserved, because
compensating channels co-vary [Marder & Goaillard 2006, Box 1, p. 565].

**Hypothesis (the central question of answer asset 1)**: if [Achard2006]'s "loose hyperplanes" and
[Prinz2004]'s "many models" picture extends to the t0123 68-d substrate, then the varimax factor
analysis should recover a small number (3-10) of factors that capture a substantial fraction of the
variance, and the answer "is MI ↔ ATP a joint axis or two decoupled axes" turns on whether one
factor carries |r| > 0.3 on both `mi_count_bits` and `atp_per_spike_molecules`. The DSI/PD precedent
in t0117 (project-internal) showed F1 with r_DSI = +0.421 and r_PD = +0.352, a single joint DSI-PD
factor at 12.6% variance explained, in the unfiltered 4-seed pool. The t0125 question is whether MI
and ATP behave the same way in the single-seed t0123 pool. **Best practice** from
[Achard2006, Prinz2004, Marder2006]: every cluster/factor analysis of a MOO output ensemble should
report (a) the joint distribution of each parameter across the ensemble, (b) the compensatory
covariance structure (which channels co-vary), and (c) the per-cluster ranges of all parameters, not
just the per-parameter means.

### Per-AP ATP Cost Is Dominated by Na+/K+ Overlap, Not AP Shape

The ATP-per-spike axis of the t0123 Pareto front is set by Na+/K+ overlap during the action
potential, not by AP amplitude or width [Sengupta2010]. Across seven published Hodgkin-Huxley models
— squid axon, crab leg motor neuron, mouse fast-spiking interneuron, honeybee Kenyon cell, rat
hippocampal interneuron, rat cerebellar granule cell, mouse thalamo-cortical relay — per-AP Na+
load spans **17-fold** (squid = **1 098 nC/cm^2**, mouse thalamo-cortical relay = **65 nC/cm^2**;
Sengupta et al. 2010, Table 1, p. 5), while the capacitive-minimum Na+ load (the minimum charge
required to depolarise the membrane to the AP peak) varies only **2.3-fold** (98 to 56 nC/cm^2). The
difference is almost entirely the **overlap load**: Na+ that enters while K+ is also flowing
outward, dissipating without contributing to depolarisation. The linear regression of overlap load
vs total Na+ load across all seven models has slope ~1 and **R^2 = 0.99 (p < 0.0001)**
[Sengupta et al. 2010, Figure 3, p. 6]. AP efficiency (capacitive-minimum / total Na+ load) ranges
from **9% in the squid (6.3 °C)** through **20-40% in mammalian crab motor / mouse fast-spiking /
honeybee Kenyon**, **75% in rat hippocampal interneuron**, to **~100% in rat granule and mouse
thalamo-cortical relay** [Sengupta et al. 2010, Table 1, p. 5]. Two APs with identical height and
half-width can be produced by current pairs differing **1.76-fold in Na+ load** (1 275 vs 2 244
nC/cm^2; Sengupta et al. 2010, Figure S1).

The corresponding ATP-per-AP cost varies **~17-fold across the same seven models** (squid = **2.3 x
10^12 ATP/cm^2** vs mouse thalamo-cortical relay = **1.35 x 10^11 ATP/cm^2**) and the Na+/K+ pump
stoichiometry is **3 Na+ per 1 ATP**, so ATP per AP per cm^2 = (Na+ load) x N_A / (3 x F)
[Attwell2001, Eq. 9, p. 1136]. The Attwell-Laughlin canonical recipe — used as the t0123
implementation reference — converts integrated Na+ influx (in coulombs per compartment per AP) to
ATP molecules via division by `(3 * e)` with `e = 1.602e-19 C`
[Attwell & Laughlin 2001, Materials and Methods, p. 1136]. The benchmark per-AP cost in a rodent
cortical neuron is **3.84 x 10^8 ATP** (Na+ load **1.15 x 10^9 ions**), with **axon collaterals =
82%, dendrites = 14%, soma = 4%** [Attwell & Laughlin 2001, Table 4, p. 1140]. Total per-spike cost
including 2 000 released vesicles is **7.1 x 10^8 ATP/spike**
[Attwell & Laughlin 2001, Results, p. 1141].

**Hypothesis** (central to answer assets 2 and 3): high-ATP cells in the t0123 pool are expected to
sit at high Na+ overlap factor (`alpha = total Na+ / capacitive minimum`) — i.e., elevated somatic
+ AIS Nav densities and/or slowed K+ kinetics that delay repolarisation. The Cliff's-delta ranked
  bar chart from Step 8 should isolate parameters that control Nav density (`g_nav16_*`), Kv density
  (`g_kv3_*`, `g_kv4_*`), and Na+ inactivation time constant — these are the canonical "energy
  levers" identified in [Sengupta et al. 2010, Discussion, p. 11], where reducing Na+ inactivation
  tau is the single most effective biophysical lever for lowering AP energy (more effective than
  reducing channel density). **Best practice** from [Sengupta2010]: AP shape (amplitude, half-width)
  is **not** a reliable predictor of energy cost — the cluster analysis must therefore use the
  direct integrated Na+ recipe rather than a waveform proxy. The DSGC mammalian neurons in t0123 are
  expected to cluster around the mammalian alpha ~ 1.0-1.5 band rather than the squid alpha ~ 4-11
  band, because mammalian neurons are observed to lie close to the capacitive minimum
  [Sengupta et al. 2010, Table 1, p. 5; Carter & Bean cited in discussion at p. 11]. Carter & Bean
  (2009) is not in the asset corpus but is cited via [Sengupta2010] as the mouse cortical pyramidal
  benchmark at **alpha ~ 1.2** — the t0125 ATP histogram should cluster around this value if the
  NSGA-II found biologically plausible cells.

### Mutual Information in RGC Spike Trains Is Bounded by the Spike Generator, Not by Synaptic Input

The single direct RGC information-rate measurement in the corpus comes from [Dhingra2004]:
brisk-transient guinea-pig RGCs at 37 °C, recorded with sharp electrodes, presented a flashed spot
over the receptive-field centre, analysed with ideal-observer decoders applied independently to the
graded-potential trace and to the spike train. Key quantitative results: **detection threshold from
graded potential = 1.5% contrast; from spikes = 3.8% contrast** (~2.5x degradation by the spike
generator); **spikes carry roughly 60% fewer distinguishable gray levels** than the graded
potential; the graded-potential dipper onsets at **~2% contrast** and the spike dipper at **~4%
contrast** [Dhingra & Smith 2004, Figs. 5-7, pp. 5345-5347]. The information loss is dominated by
the spike-generator threshold nonlinearity, not by stochastic noise
[Dhingra & Smith 2004, Discussion, p. 5349]. [Dhingra2004] also documents an explicit trade-off:
**depolarisation reduces detection threshold but also reduces dynamic range** — a Pareto trade-off
in the same RGC type the project simulates.

The corresponding ceiling-and-baseline for the t0123 4-direction protocol comes from [Strong1998]'s
direct-method information rate in the fly H1 motion-sensitive neuron: total spike-train entropy rate
at `Δτ = 3 ms` of **157 ± 3 bits/s**, noise entropy rate that yields information rate **78 ± 5
bits/s = 1.8 ± 0.1 bits/spike**, efficiency **~50%** across `Δτ ∈ [2 ms, 800 ms]`, peak
information rate up to **~90 bits/s** [Strong et al. 1998, Results, p. 198]. The t0123 inner-loop
estimator is **not** the full direct method (only 3 trials per direction is insufficient for the 1/T
extrapolation) but a Miller-Madow-corrected spike-count plug-in MI on a 4 x B contingency table with
ceiling `log2(4) = 2 bits/stimulus` (t0123 task_description.md, "MI Estimator Choice"). The post-hoc
validation on the top-10 Pareto cells uses 8 directions x 20 trials per direction = 160 trials with
Strong-Bialek direct-method MI in bits/s, exactly the [Strong1998] recipe at resolution `dt = 5 ms`
and `T ∈ {25, 50, 75, 100} ms`.

**Hypothesis** (relevant to answer 1 and answer 4): high-MI cells in the 68-d substrate likely
cluster around parameters that (a) keep the spike generator close to threshold without
depolarisation block — moderate Nav densities + moderate Kv densities — and (b) sustain enough
PD-rate that the 4-direction spike-count distributions can support `log2(4) = 2 bits`. The Miller-
Madow-corrected plug-in MI on only 12 trials per cell is biased, but as a **relative** selection
signal for NSGA-II it is well-defined. The factor analysis should reveal whether MI co-varies with
the parameters that control PD firing rate (Nav, AIS Nav, synaptic strength) or with a distinct axis
(channel kinetics that determine information per spike rather than spike count). **Best practice**
from [Strong1998] and [Dhingra2004]: any reported information rate must specify the resolution
`Δτ`, the window `T`, the number of trials, the bias-correction method, and the units (bits/spike,
bits/s, or bits/stimulus). The t0125 cluster analysis should treat `mi_count_bits` as the
bits/stimulus surrogate, not as the Strong-Bialek bits/s rate, and should defer claims about
absolute MI rates to the post-hoc 8-dir x 20-trials Pareto-cell validation.

### Morphology Is a Functional Axis, Not a Passive Scaffold

The cluster analysis on the 14-d morphology subvector (Step 6) rests on the established result that
morphology alone, with a fixed channel set, determines firing pattern. [Mainen1996] showed that
distributing the **same** channel set across reconstructions of layer 3 aspiny stellate (regular-
spiking) vs layer 5 pyramidal (intrinsic-bursting) vs layer 4 spiny stellate (fast-spiking) cells
reproduces the experimentally observed firing patterns of those cell types — morphology alone is
sufficient. [KochPoggio1982] gave the historical anchor: the first formal cable-theoretic argument
that **dendritic morphology has a functional interpretation** rather than being arbitrary, using
passive cable theory on cat retinal ganglion cells with **R_i = 70 Ω·cm, C_m = 2 µF/cm^2, R_m = 2
500 Ω·cm^2** to argue that branching geometry plus shunting inhibition can compute direction
selectivity. [FohlmeisterMiller1997] reinforces this in the project's home cell type: in
multicompartmental amphibian RGCs with five nonlinear ion channels plus leak, **cell geometry
(soma-dendritic-axon proportions) controls the f-I curve** — for the t0125 ATP question, this
means the 14 morphology parameters (segment count, branch order, segment diameter, segment length,
soma radius, soma share, etc.) should plausibly form distinct KMeans clusters with distinct mean
ATP-per-spike values.

[LondonHausser2005] is the canonical synthesis: dendrites can act as passive cables, active spike
conductors, amplifiers, coincidence detectors, and direction-discriminators, each with
characteristic biophysical signatures (London & Hausser 2005, Box 1). The review documents the menu
of single-cell computations that a multi-objective optimiser can target *for* (MI, coincidence
detection) and *against* (energy, cytoplasm). [Cuntz2010] formalises the morphology-vs-conduction-
time trade-off via the balancing factor `bf`, with biologically realistic dendritic arbors
clustering at **bf ∈ [0.2, 0.7]** (Cuntz et al. 2010, Figure 4) — for the t0125 morphology
cluster analysis, this is the prior on which morphology subspace is biologically plausible.

**Hypothesis** (answer 3): morphology clusters in the t0123 pool should split high-ATP from low-ATP
cells primarily along axes that control total membrane area (segment count, mean segment length,
mean segment diameter) — because total Na+ load per AP scales linearly with the dendritic membrane
area carrying Nav channels [Attwell2001, Sengupta2010]. **Best practice** from [Hay2011, Cuntz2010]:
every morphology-objective analysis should be tested for **discretisation invariance** — halving
or doubling compartment density should change the integrated Na+ objective by no more than a few
percent. **Best practice** from [Mainen1996]: do **not** interpret a morphology cluster in isolation
from its channel densities — the same morphology with different channels gives qualitatively
different firing patterns, so the t0125 corner heatmap (Step 9) is the right visualisation because
it shows the *joint* electrophys + morphology signature of each MI x ATP corner rather than treating
the two subspaces as independent.

### Unsupervised Clustering Is the Established Method for High-d Cell-Type Discovery in the Retina

The closest methodological precedent in real retinal data is [Baden2016]: two-photon Ca^2+ imaging
of >11 000 mouse RGCs, with each cell reduced to a functional feature vector (SVD of moving-bar
direction-by-time matrices + chirp average + full-field step + colour + receptive-field diameter +
soma area + ON/OFF index + DSi + OSi + response-quality + immunohistochemistry markers). The
clustering pipeline was an **unsupervised probabilistic Mixture-of-Gaussians model with the number
of clusters selected by the minimum BIC**, run independently on DS-positive cells (cell_dp < 0.05, n
= 1 757) and non-DS cells [Baden et al. 2016, Methods, p. 348]. The pipeline returned **24 DS
clusters and 48 non-DS clusters**, merged across DS / non-DS domains into **32 RGC functional
groups** plus 17 displaced amacrine groups [Baden et al. 2016, Results, Figure 2]. 8 DS-containing
groups (G2, G6, G12, G13, G16, G25, G26, G29) together account for **70% of all 1 757 DS cells
recorded**.

For the t0125 task the methodological parallels are exact: a high-d feature vector per cell, an
unsupervised clustering pipeline that auto-picks the cluster count by an objective criterion
(silhouette in t0125 rather than BIC in Baden 2016), separate clustering on a function-relevant
subspace (DS/non-DS in Baden 2016; electrophys-only and morphology-only in t0125), and a final
reading of which cluster captures which functional groups (RGC type in Baden 2016; MI / ATP / corner
in t0125). **Best practice** from [Baden2016]: the cluster count selection criterion (BIC or
silhouette) must be reported with its full curve, not just the peak — different curve shapes imply
different interpretations (a flat curve means the data does not strongly prefer any k; a sharp peak
supports the chosen k). The silhouette curve for k ∈ [3, 7] in t0125 Steps 5 and 6 is the exact
analogue of Baden's BIC curve and must be saved to disk.

### Multi-Objective Optimisation Methodology and the Pareto-Acceptable-Ensemble Reporting Convention

The MOO methodology line — [Hay2011], [Druckmann2007], [VanGeit2016] — establishes the reporting
convention this task should follow. [Hay2011] fit 22 free parameters of an L5b pyramidal cell to
**20 firing-feature objectives** (10 perisomatic + 10 BAP-activated Ca-spike "BAC" features) with
population 1 000 x 500 generations = **500 000 evaluations**, accepting all models whose every
feature lies within **2-3 SD** of the experimental mean and producing ~2 000 acceptable models that
are reported as a Pareto-acceptable ensemble (ModelDB 139653) rather than as a single best fit
[Hay et al. 2011, Results, p. 6]. Two single-target sub-fits give a quantitative case for joint
optimisation and joint cluster analysis: BAC-only fitting yields **899 acceptable models** but those
models then fail perisomatic targets (e.g., apical Nat density **82.5 pS/um^2** below the
BAC-acceptable range of **101-133.5 pS/um^2** when the perisomatic constraint is added back in);
perisomatic-only fitting yields only **52 acceptable models** [Hay et al. 2011, Discussion, p. 9].
The two single-target acceptable sets do not overlap on the joint feature space — exactly the "are
MI and ATP found in the same region or in disjoint clusters" question this task asks.

[Druckmann2007] introduced the per-feature SD-normalisation convention: every objective is expressed
in units of the corresponding experimental SD (or, when no SD is available, the best- effort
biological tolerance). The original Druckmann fit used a 12-parameter compartmental model with
NSGA-II at **300 organisms x 1 000 generations = 300 000 evaluations** to fit two electrical classes
of rat somatosensory cortical interneurons [Druckmann et al. 2007, Methods, p. 9]. [VanGeit2016]
packaged this methodology into BluePyOpt — wraps DEAP for the evolutionary algorithms (IBEA and
NSGA-II), NEURON as the simulator, and eFEL for feature extraction. Use Case 2 in [VanGeit2016]
reproduces the Hay 2011 18-parameter L5PC fit by matching 31 eFeatures from in vitro patch-clamp
recordings in **~4 hours on 50 cores with IBEA at 100 individuals x 100 generations = 10 000
evaluations** [Van Geit et al. 2016, Use Case 2, p. 11] — orders of magnitude smaller than
[Hay2011]'s original 500 000 because the search space is reduced and the algorithm is upgraded.

**Best practice** from this line for t0125's per-question verdicts: report the full Pareto front and
the per-cluster parameter distribution (Hay-style ensemble), not just the means; express
between-group differences in units of pooled SD (Druckmann-style); record the K-means cluster labels
next to the parameter vector for every cell, so a downstream task can re-analyse with a different
cluster count without re-running the simulation. **Hypothesis (cross-cutting)**: the "shape" of the
t0123 NSGA-II output ensemble should resemble [Achard2006]'s "loose hyperplanes" qualitatively,
while the per-channel ranges should be narrower than [Achard2006]'s 20-model Purkinje fit (because
the t0123 substrate has stronger biological priors on every parameter from t0078 / t0080 / t0091 /
t0102).

## Methodology Insights

* **Per-AP ATP recipe (Attwell-Laughlin canonical form)**: ATP per AP per compartment =
  `(integrated_Na_inward_current * area_cm2) / (3 * e)` with `e = 1.602e-19 C` and the Na+/K+ pump
  stoichiometry of 3 Na+ exported per ATP hydrolysed [Attwell2001, Eq. 9, p. 1136]. The t0123
  implementation already uses this; the t0125 cluster analysis must consume the resulting per-cell
  `atp_per_spike_molecules` directly from the predictions asset.

* **Sengupta calibration band for mammalian neurons**: AP efficiency (capacitive-minimum / total Na+
  load) for mammalian neurons sits at **75-100%**, alpha (overlap factor) at **1.0-1.5**
  [Sengupta2010, Table 1, p. 5]. The Carter-Bean (2009) cortical pyramidal benchmark at **alpha ~
  1.2** is the closest reference for a DSGC. Any t0123 cell with alpha > 2 (i.e., overlap load >
  total capacitive load) should be flagged as biologically implausible — this is a sanity check
  for the high-ATP corner of the t0125 cluster analysis.

* **MI bias-correction convention**: the inner-loop t0123 estimator uses Miller-Madow correction
  `bias_MM = (R-1)(C-1)/(2N ln 2)` with R = 4 (directions), C = B (bins), N = 12 (trials) on the 4 x
  B contingency table [Strong1998, Eqs. 4, 6]. The post-hoc validation uses Strong-Bialek direct
  method with 1/T extrapolation [Strong1998, Eq. 4, p. 198]. The t0125 cluster analysis consumes the
  inner-loop `mi_count_bits` values and should report MI in bits/stimulus, with the
  `log2(4) = 2 bits` ceiling noted in every chart caption.

* **Cluster count selection**: silhouette sweep over k ∈ [3, 7] with the chosen k = argmax of mean
  silhouette is the t0117 convention this task inherits. The full silhouette curve must be saved to
  disk, not just the peak [Baden2016 methodological parallel: BIC curve, p. 348].

* **Per-feature SD-normalisation**: when reporting between-group differences (high-MI vs low-MI,
  high-ATP vs low-ATP), express each parameter difference in units of the pooled SD of that
  parameter across the full cohort [Druckmann2007, Methods, p. 10]. The t0125 corner heatmap (Step
  9\) already does this by z-scoring on the full cohort. The Cliff's delta bar charts (Step 8) are
  the non-parametric SD-free analogue and should be reported alongside the parametric mean ± SD per
  group.

* **Pareto-acceptable-ensemble reporting, not single-best-cell reporting**: the four answer assets
  should report per-cluster means and per-cluster ranges, not the single hypervolume-maximising cell
  [Hay2011, Discussion, p. 9]. The "Pareto-favoured corner signature" (answer 4) is a population
  statement: the 5 parameters with the largest absolute z-score difference between the
  high-MI/low-ATP corner and the low-MI/high-ATP corner, averaged across the cells in each corner,
  not the difference between two individual Pareto cells.

* **Joint-factor threshold**: a varimax factor counts as "joint" if |Pearson r| > 0.30 against both
  `mi_count_bits` AND `atp_per_spike_molecules`; "decoupled" if |r| > 0.30 against exactly one. The
  t0117 precedent (project-internal) used the same threshold and found one joint DSI-PD factor
  (r_DSI = +0.421, r_PD = +0.352). The threshold is the same here; the substantive question is
  whether the count is 0, 1, or >1, and what the variance-explained fraction of the joint factor is.
  Parallel reporting convention to Druckmann/Hay's per-objective SD normalisation.

* **Discretisation-invariance regression**: any morphology-integrated objective (ATP-per-spike
  included, because it integrates Na+ across compartments) must be regression-tested across two
  compartment-density settings (e.g., 20 µm and 10 µm). [Hines1997, Hay2011] 20-µm convention is
  the floor; doubling resolution should not change the objective by more than a few percent or the
  recipe needs revisiting. The t0123 implementation already uses the standard 20-µm spec; the t0125
  cluster analysis does not need to repeat this check but should cite it.

* **Best practice from RGC-type clustering [Baden2016]**: cluster on the function-relevant subspace
  (DS / non-DS in Baden; electrophys-only and morphology-only in t0125) rather than on the full
  joint vector — separate clustering yields more interpretable cluster identities. The t0123 /
  t0125 design already does this (separate KMeans on the 54-d electrophys subspace and the 14-d
  morphology subspace) — this is the right choice per Baden's precedent.

## Gaps and Limitations

* **No paper in the corpus measures bits-per-ATP in a DSGC**: Niven et al. 2007 (fly photoreceptors,
  the canonical bits-per-ATP Pareto curve, 200-1000 bits/s scaling super-linearly with ATP cost at
  fixed cost of ~20% of maximum consumption) is not in the asset corpus — it appears only via
  internet research in `tasks/t0097_multi_obj_optim/research/research_internet.md`. The t0125
  cluster analysis cannot directly cite Niven 2007; the parent task t0123 explicitly notes this
  measurement is "unmeasured in the published literature" for DSGCs and the t0125 Pareto-corner
  analysis is the project's contribution to closing that gap.

* **No paper in the corpus measures the AIS-vs-dendrite-vs-soma ATP share for a real DSGC**:
  [Attwell2001] gives the rodent cortical breakdown (axon collaterals 82%, dendrites 14%, soma 4%;
  Table 4 p. 1140), but neither the asset corpus nor any internet-discovered paper provides a
  DSGC-specific measurement. The t0125 ternary plot (Step 10) is therefore an exploratory output
  with no published comparison; the **Hallermann2012** state-and-location-dependence-of-metabolic-
  cost paper that would supply a cortical-pyramidal-cell precedent is also only in internet
  research, not in the asset corpus.

* **No paper in the corpus provides factor analysis on a high-d compartmental-model parameter
  vector**: [Achard2006] explicitly says the good-region is a "set of loosely connected hyperplanes"
  but does not run PCA or factor analysis on the resulting 20-model ensemble — instead it reports
  per-channel ranges. [Prinz2004] reports per-parameter histograms across the ~452 K matching
  networks but does not run PCA or KMeans. The t0125 pipeline (t0108 / t0116 / t0117 precedent) is
  the project's internal methodology contribution; the literature precedent for the analytical tool
  itself is [Baden2016] on **functional fingerprints of real cells**, not on simulated parameter
  vectors. This means the t0125 cluster identities are interpretable only within the t0123 substrate
  and should not be claimed as cell-type discoveries.

* **No paper in the corpus directly couples MI and ATP as joint optimisation objectives**: the
  closest published precedent is Remme et al. 2018 (MSO neurons, coincidence detection vs energy)
  which is **not** in the asset corpus — only available via internet research. The MOO-methodology
  papers in the corpus ([Hay2011, Druckmann2007, VanGeit2016, Achard2006]) optimise to multiple
  *electrophysiological-feature* objectives all of which are derived from spike-waveform statistics;
  none of them includes information-theoretic or energy objectives in the optimised set. This is the
  genuine novelty of the t0123 / t0125 lineage and the reason the four answer assets cannot
  benchmark their numbers against a directly comparable published result.

* **No paper in the corpus uses bias-corrected spike-count MI on a 4-direction protocol**: the only
  RGC information-rate measurement [Dhingra2004] is contrast-detection on a single spot, not
  direction-decoding on 4 antipodal directions; [Strong1998] uses a continuous random-walk stimulus,
  not a 4-class discrete stimulus. The Miller-Madow correction is a standard tool but its
  appropriateness for the small-N (N = 12 trials per cell) regime is not directly validated by any
  corpus paper. The cross-validation against the 8-direction x 20-trial Strong-Bialek post-hoc MI is
  the project's internal sanity check — this should be reported in t0125 if the predictions asset
  includes it.

* **Cluster-validation methodology**: [Baden2016] used BIC for cluster-count selection on a
  Mixture-of-Gaussians model; t0125 uses silhouette on a KMeans model. The two criteria can
  disagree. No paper in the corpus directly compares them for the kind of parameter-ensemble
  clustering this task does. The silhouette + per-cluster purity (NMI vs MI / ATP quartile groups)
  combination from t0117 is the project's internal best-of-both convention.

## Recommendations for This Task

1. **Interpret the varimax factor loadings as Achard-style "loose hyperplanes," not as discrete
   cell-type axes**: the 68-d substrate is expected to admit a small number of factors with
   substantial variance explained per factor, but per-factor variances of ~10-15% are normal in this
   kind of MOO ensemble [Achard2006, Druckmann2007]. Do not over-interpret a single joint-factor
   result as definitive evidence for a single MI ↔ ATP trade-off — verify by also checking
   whether two decoupled factors (MI-only + ATP-only) together capture more variance than the joint
   factor alone.

2. **Calibrate the high-ATP corner against the Sengupta mammalian band**: report
   `alpha = total integrated Na+ load per AP / capacitive minimum` for the high-ATP corner cells. If
   alpha > 2, flag these cells as biologically implausible in the answer asset for question 3
   [Sengupta2010, Table 1, p. 5]. The Carter-Bean cortical pyramidal alpha ~ 1.2 cited in
   [Sengupta2010, Discussion, p. 11] is the closest mammalian benchmark.

3. **Frame the answer-1 verdict (joint vs decoupled factor) as the central result, with the t0117
   DSI-PD result as the methodological precedent**: the t0117 finding (one joint factor F1 with
   r_DSI = +0.421, r_PD = +0.352, 12.6% variance explained, in the unfiltered 4-seed pool) provides
   the analog the t0125 result should be compared against. State explicitly in
   `compare_literature.md` whether the MI-ATP case looks the same (one joint factor + multiple
   decoupled factors), opposite (no joint factor, only decoupled), or richer (multiple joint
   factors).

4. **Report Cliff's delta with both magnitudes and directions for the top-5 parameters per
   question** (answers 2 and 3): the 68-parameter ranked bar charts (Steps 8) are the primary
   visualisation. State the top-5 parameters with effect size (Cliff's delta) AND direction (which
   group has the higher value) AND a one-sentence biological interpretation tied to [Sengupta2010]
   for ATP-relevant parameters and [Dhingra2004, Strong1998] for MI-relevant parameters.

5. **Report the per-corner morphology gallery alongside the corner heatmap** (Step 9): the corner
   heatmap is the central quantitative answer to question 4, but a 5 x 3 representative-cell gallery
   (full dendrite trees, per the project memory `feedback_top50_morphologies_full_dendrites.md`) for
   the high-MI/low-ATP and low-MI/high-ATP corners gives the **biological** plausibility check that
   the corner heatmap alone cannot — interpret each gallery using the
   [Mainen1996, Cuntz2010, FohlmeisterMiller1997] morphology-as-functional-axis framework.

6. **Cite [Achard2006] and [Prinz2004] as the precedents for "many parameter combinations, one
   functional output"**: when the cluster analysis reveals that the high-MI / low-ATP corner is
   composed of cells with substantially different per-parameter values (which is the expected
   outcome based on these precedents), state this explicitly as confirmation of degeneracy rather
   than as a failure of the cluster to identify a clean signature [Marder2006, Box 1, p. 565].

7. **Validate the silhouette-selected cluster count k by reporting the full silhouette curve and
   per-cluster cell counts**: the silhouette peak can be weak in MOO-output ensembles where the true
   underlying structure is hyperplanar rather than blob-like [Achard2006]. If the peak is flat
   (<0.05 difference from neighbouring k), report this as a "k not strongly preferred" caveat and
   run a sensitivity check at k ± 1 [Baden2016 methodological parallel for the BIC curve].

8. **For the MI ceiling, always report the `log2(4) = 2 bits/stimulus` upper bound alongside the
   measured MI**: t0123 hit a best `mi_count_bits = 1.459` (73% of ceiling). The t0125 cluster
   analysis should show what fraction of cells in each corner reach what fraction of ceiling and not
   over-state absolute MI values without the ceiling context
   [Strong1998, Dhingra2004 caveat on bits-per-stimulus vs bits-per-second].

## Paper Index

### [Achard2006]

* **Title**: Complex Parameter Landscape for a Complex Neuron Model
* **Authors**: Achard, P., De Schutter, E.
* **Year**: 2006
* **DOI**: `10.1371/journal.pcbi.0020094`
* **Asset**: `tasks/t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.0020094/`
* **Categories**: `compartmental-modeling`, `voltage-gated-channels`
* **Relevance**: The single most important methodological precedent for this task. Demonstrates that
  the high-d parameter space of an MOO-acceptable neuron-model ensemble forms "a collection of
  loosely connected hyperplanes" rather than a single blob or set of isolated points — exactly the
  geometric prior the t0125 PCA + KMeans + varimax factor analysis is designed to reveal in the
  t0123 68-d substrate.

### [Prinz2004]

* **Title**: Similar Network Activity from Disparate Circuit Parameters
* **Authors**: Prinz, A. A., Bucher, D., Marder, E.
* **Year**: 2004
* **DOI**: `10.1038/nn1352`
* **Asset**: `tasks/t0097_multi_obj_optim/assets/paper/10.1038_nn1352/`
* **Categories**: `compartmental-modeling`, `voltage-gated-channels`
* **Relevance**: Empirical quantitative case for parameter degeneracy at network scale (20.25 M
  simulated networks, 2.2% match all 15 criteria). Supports the t0125 interpretation that high-MI /
  low-ATP cells in the t0123 pool are likely to comprise multiple distinct parameter combinations
  rather than a single tight cluster — directly relevant to answer 4 (Pareto- favoured corner
  signature).

### [Marder2006]

* **Title**: Variability, Compensation and Homeostasis in Neuron and Network Function
* **Authors**: Marder, E., Goaillard, J.-M.
* **Year**: 2006
* **DOI**: `10.1038/nrn1949`
* **Asset**: `tasks/t0097_multi_obj_optim/assets/paper/10.1038_nrn1949/`
* **Categories**: `compartmental-modeling`, `voltage-gated-channels`
* **Relevance**: Canonical review framing of parameter degeneracy: channel densities can vary two-
  to fourfold across cells of the same identified type while activity profiles remain conserved
  because compensating channels co-vary. Provides the conceptual frame for interpreting the t0125
  Cliff's-delta and corner-heatmap results — channel pairs co-varying along factor axes are the
  signature of compensation.

### [Hay2011]

* **Title**: Models of Neocortical Layer 5b Pyramidal Cells Capturing a Wide Range of Dendritic and
  Perisomatic Active Properties
* **Authors**: Hay, E., Hill, S., Schurmann, F., Markram, H., Segev, I.
* **Year**: 2011
* **DOI**: `10.1371/journal.pcbi.1002107`
* **Asset**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1371_journal.pcbi.1002107/`
* **Categories**: `voltage-gated-channels`, `compartmental-modeling`, `dendritic-computation`
* **Relevance**: Canonical multi-objective optimisation reference and source for the Pareto-
  acceptable-ensemble reporting convention. The two-target sub-fit finding (BAC-only 899 models vs
  perisomatic-only 52 models, non-overlapping acceptable sets) is the direct precedent for asking
  whether high-MI and low-ATP cells in t0123 occupy the same or disjoint regions of the 68-d
  substrate.

### [Druckmann2007]

* **Title**: A Novel Multiple Objective Optimization Framework for Constraining Conductance-Based
  Neuron Models by Experimental Data
* **Authors**: Druckmann, S., Banitt, Y., Gidon, A., Schurmann, F., Markram, H., Segev, I.
* **Year**: 2007
* **DOI**: `10.3389/neuro.01.1.1.001.2007`
* **Asset**: `tasks/t0097_multi_obj_optim/assets/paper/10.3389_neuro.01.1.1.001.2007/`
* **Categories**: `compartmental-modeling`, `voltage-gated-channels`
* **Relevance**: The original MOO-for-single-neuron-models framework. Establishes the per-feature-
  SD-normalisation reporting convention that the t0125 between-group comparison should adopt. Also
  relevant as the historical precedent for using NSGA-II-like algorithms on conductance- based
  compartmental models, which is the t0123 substrate this task analyses.

### [VanGeit2016]

* **Title**: BluePyOpt: Leveraging Open Source Software and Cloud Infrastructure to Optimise Model
  Parameters in Neuroscience
* **Authors**: Van Geit, W., Gevaert, M., Chindemi, G., et al.
* **Year**: 2016
* **DOI**: `10.3389/fninf.2016.00017`
* **Asset**: `tasks/t0097_multi_obj_optim/assets/paper/10.3389_fninf.2016.00017/`
* **Categories**: `compartmental-modeling`
* **Relevance**: Packages the [Hay2011] / [Druckmann2007] methodology into a reusable open-source
  framework (DEAP + NEURON + eFEL). Confirms that the per-objective evaluator + per-feature SD
  scoring pattern is the field standard, supporting t0125's choice to report per-cluster parameter
  distributions and Cliff's delta with the same explicit per-feature decomposition.

### [Attwell2001]

* **Title**: An Energy Budget for Signaling in the Grey Matter of the Brain
* **Authors**: Attwell, D., Laughlin, S. B.
* **Year**: 2001
* **DOI**: `10.1097/00004647-200110000-00001`
* **Asset**: `tasks/t0097_multi_obj_optim/assets/paper/10.1097_00004647-200110000-00001/`
* **Categories**: `voltage-gated-channels`, `compartmental-modeling`
* **Relevance**: Foundational reference for the ATP-per-spike axis of the t0123 NSGA-II. Supplies
  the canonical Na+ load / 3 conversion (Eq. 9) that t0123 implements, the per-event reference
  values (3.84 x 10^8 ATP per AP, 7.1 x 10^8 ATP/spike), and the compartmental breakdown (axon 82%,
  dendrites 14%, soma 4%) against which the t0125 ATP-compartment-share ternary plot (Step 10)
  should be compared.

### [Sengupta2010]

* **Title**: Action Potential Energy Efficiency Varies Among Neuron Types in Vertebrates and
  Invertebrates
* **Authors**: Sengupta, B., Stemmler, M., Laughlin, S. B., Niven, J. E.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000840`
* **Asset**: `tasks/t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.1000840/`
* **Categories**: `voltage-gated-channels`, `compartmental-modeling`
* **Relevance**: The single most quantitatively useful reference for the high-ATP vs low-ATP cluster
  signature (answer 3). Establishes that AP shape is a poor predictor of energy cost (1.76-fold
  Na+-load differences at identical waveform); that Na+/K+ overlap is the dominant cost driver (R^2
  = 0.99); that mammalian neurons cluster at alpha ~ 1.0-1.5 vs squid alpha ~ 4-11; and that
  reducing Na+ inactivation tau is the single highest-leverage energy lever. Directly informs the
  biological interpretation of the t0125 Cliff's-delta and factor-loadings for Nav-related
  parameters.

### [Strong1998]

* **Title**: Entropy and Information in Neural Spike Trains
* **Authors**: Strong, S. P., Koberle, R., de Ruyter van Steveninck, R. R., Bialek, W.
* **Year**: 1998
* **DOI**: `10.1103/PhysRevLett.80.197`
* **Asset**: `tasks/t0097_multi_obj_optim/assets/paper/10.1103_PhysRevLett.80.197/`
* **Categories**: `compartmental-modeling`
* **Relevance**: The methodological foundation for the t0123 MI estimator and for the post-hoc
  Pareto-cell direct-method validation. Establishes the practical recipe (`R_info = S - N`,
  bin-and-window, Ma lower bound, 1/T extrapolation, 1/size finite-data correction) and the
  reference rates (~50% efficiency, ~1.8 bits/spike, up to 90 bits/s in H1). The t0125 cluster
  analysis consumes `mi_count_bits` directly but must respect the `log2(4) = 2 bits/stimulus`
  ceiling on the 4-direction protocol and not over-interpret absolute MI values without the
  Strong-Bialek context.

### [Dhingra2004]

* **Title**: Spike Generator Limits Efficiency of Information Transfer in a Retinal Ganglion Cell
* **Authors**: Dhingra, N. K., Smith, R. G.
* **Year**: 2004
* **DOI**: `10.1523/jneurosci.5346-03.2004`
* **Asset**:
  `tasks/t0015_literature_survey_cable_theory/assets/paper/10.1523_jneurosci.5346-03.2004/`
* **Categories**: `retinal-ganglion-cell`, `voltage-gated-channels`, `compartmental-modeling`
* **Relevance**: The only direct RGC information-rate measurement in the corpus. Anchors the MI axis
  of the t0123 Pareto front in real RGC physiology: spike generator degrades graded-potential
  information by ~2.5x (1.5% vs 3.8% contrast threshold, ~60% gray-level loss), and depolarisation
  trades off detection-threshold against dynamic-range — a Pareto trade-off in the same RGC type
  the t0123 substrate simulates. Supports the answer-1 framing that MI in t0123 is bounded by the
  spike generator, not by synaptic input.

### [Mainen1996]

* **Title**: Influence of dendritic structure on firing pattern in model neocortical neurons
* **Authors**: Mainen, Z. F., Sejnowski, T. J.
* **Year**: 1996
* **DOI**: `10.1038/382363a0`
* **Asset**: `tasks/t0015_literature_survey_cable_theory/assets/paper/10.1038_382363a0/`
* **Categories**: `cable-theory`, `dendritic-computation`, `compartmental-modeling`
* **Relevance**: Establishes that morphology alone (with fixed channel set) is sufficient to
  determine firing pattern across regular-spiking / intrinsic-bursting / fast-spiking neuron types.
  Foundational support for the t0125 morphology KMeans cluster analysis (Step 6) and for the
  expectation that morphology clusters will split high-ATP from low-ATP cells primarily along
  total-membrane-area axes (segment count, segment length, segment diameter).

### [FohlmeisterMiller1997]

* **Title**: Mechanisms by Which Cell Geometry Controls Repetitive Impulse Firing in Retinal
  Ganglion Cells
* **Authors**: Fohlmeister, J. F., Miller, R. F.
* **Year**: 1997
* **DOI**: `10.1152/jn.1997.78.4.1948`
* **Asset**:
  `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1152_jn.1997.78.4.1948/`
* **Categories**: `voltage-gated-channels`, `compartmental-modeling`
* **Relevance**: Project home cell type (amphibian RGC) with the canonical 5-channel HH model that
  defines what RGC repetitive firing looks like in a compartmental simulation. Demonstrates that
  cell geometry (soma-dendrite-axon proportions) controls the f-I curve — directly relevant to the
  t0125 question of whether morphology clusters in the t0123 pool predict ATP-per-spike and
  spike-count MI.

### [KochPoggio1982]

* **Title**: Retinal ganglion cells: a functional interpretation of dendritic morphology
* **Authors**: Koch, C., Poggio, T.
* **Year**: 1982
* **DOI**: `10.1098/rstb.1982.0084`
* **Asset**: `tasks/t0015_literature_survey_cable_theory/assets/paper/10.1098_rstb.1982.0084/`
* **Categories**: `cable-theory`, `retinal-ganglion-cell`, `dendritic-computation`
* **Relevance**: Historical anchor for the claim that dendritic morphology has a functional
  interpretation rather than being arbitrary. Justifies the inclusion of the 14-d morphology
  subvector as an analysis axis on equal footing with the 54-d electrophys subvector in the t0125
  cluster pipeline, and supplies canonical passive-cable parameters that the t0123 substrate
  inherits.

### [LondonHausser2005]

* **Title**: Dendritic Computation
* **Authors**: London, M., Hausser, M.
* **Year**: 2005
* **DOI**: `10.1146/annurev.neuro.28.061604.135703`
* **Asset**:
  `tasks/t0016_literature_survey_dendritic_computation/assets/paper/10.1146_annurev.neuro.28.061604.135703/`
* **Categories**: `dendritic-computation`, `cable-theory`, `compartmental-modeling`
* **Relevance**: Canonical review of dendritic computation. Provides the conceptual menu (passive
  cables, active spike conductors, amplifiers, coincidence detectors, direction-discriminators) for
  interpreting what kind of computation each KMeans cluster in the t0125 electrophys subspace is
  performing, and justifies why MI and ATP are both biologically meaningful objectives rather than
  arbitrary engineering metrics.

### [Cuntz2010]

* **Title**: One Rule to Grow Them All: A General Theory of Neuronal Branching and Its Practical
  Application
* **Authors**: Cuntz, H., Forstner, F., Borst, A., Hausser, M.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000877`
* **Asset**:
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1371_journal.pcbi.1000877/`
* **Categories**: `compartmental-modeling`, `dendritic-computation`, `cable-theory`
* **Relevance**: Formalises the morphology-vs-conduction-time trade-off via the balancing factor
  `bf`, with biologically realistic dendritic arbors clustering at `bf ∈ [0.2, 0.7]`. Supplies the
  biological-plausibility prior for the t0125 morphology KMeans (Step 6) and the
  discretisation-invariance reasoning for the ATP-per-spike integration over compartments.

### [Hines1997]

* **Title**: The NEURON Simulation Environment
* **Authors**: Hines, M. L., Carnevale, N. T.
* **Year**: 1997
* **DOI**: `10.1162/neco.1997.9.6.1179`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1162_neco.1997.9.6.1179/`
* **Categories**: `compartmental-modeling`, `cable-theory`, `voltage-gated-channels`
* **Relevance**: Canonical reference for the NEURON simulation substrate that t0123 runs on.
  Establishes the <= 20-µm compartment discretisation convention that the t0123 per-compartment Na+
  integration relies on; cited to justify why the t0125 cluster analysis can consume the per-cell
  `atp_per_spike_molecules` directly without re-checking discretisation invariance.

### [Baden2016]

* **Title**: The functional diversity of retinal ganglion cells in the mouse
* **Authors**: Baden, T., Berens, P., Franke, K., Roman Roson, M., Bethge, M., Euler, T.
* **Year**: 2016
* **DOI**: `10.1038/nature16468`
* **Asset**: `tasks/t0103_extract_baden_2016_ds_morphologies/assets/paper/10.1038_nature16468/`
* **Categories**: `retinal-ganglion-cell`, `direction-selectivity`
* **Relevance**: The closest methodological precedent for the t0125 unsupervised-clustering pipeline
  on a high-d feature vector. Used Mixture-of-Gaussians with BIC-based cluster-count selection on
  >11 000 mouse RGC functional fingerprints, separating DS-positive from non-DS cells before
  clustering — the analytical analogue of t0125's separate KMeans on the electrophys-only and
  morphology-only subspaces. Supplies the best-practice convention of reporting the full
  cluster-count selection curve, not just the chosen k.
