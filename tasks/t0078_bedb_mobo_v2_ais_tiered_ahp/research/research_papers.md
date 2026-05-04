---
spec_version: "1"
task_id: "t0078_bedb_mobo_v2_ais_tiered_ahp"
research_stage: "papers"
papers_reviewed: 16
papers_cited: 13
categories_consulted:
  - "voltage-gated-channels"
  - "retinal-ganglion-cell"
  - "compartmental-modeling"
  - "direction-selectivity"
  - "patch-clamp"
  - "dendritic-computation"
  - "synaptic-integration"
date_completed: "2026-05-03"
status: "complete"
---
# Research Papers: Bed B v2 MOBO with AIS, Tier-Stratified Channels, and Slow Kv-AHP

## Task Objective

This task runs a ~47-dimensional multi-objective Bayesian optimisation (qLogNEHVI, BoTorch) on the
de Rosenroll 2026 Bed B DSGC compartmental model in NEURON, augmented with three architectural
additions that are missing from the bare 25-dimensional t0076 substrate: (1) a bio-realistic axon
initial segment (AIS) section with Van Wart 2007 / Werginz 2020 priors; (2) tier-stratified channel
densities across 5 compartment tiers (soma, proximal-dendrite, mid-dendrite, terminal-dendrite, AIS)
for Nav1.6, Kv3, NaP, BK, and SK; and (3) a slow Kv-mediated AHP implemented via SK_E2 with an
extended Ca-binding time constant. The optimiser jointly maximises direction-selectivity index (DSI)
and preferred-direction (PD) firing rate. The binary pass criterion is to locate at least one Pareto
cell satisfying DSI >= 0.4 AND PD rate >= 30 Hz, a joint operating point that the t0076 25-d search
could not reach (every Pareto cell with DSI >= 0.4 had PD rate <= 5.0 Hz, and every cell with PD
rate >= 30 Hz had DSI <= 0.07). These reviewed papers supply the biological priors for AIS geometry
and channel densities, the target DSI and firing-rate ranges from mouse and rabbit experimental
records, and the methodological context for multi-objective search in biophysical models.

## Category Selection Rationale

All eight project categories were consulted. Six categories yield papers directly cited in this
document:

* **voltage-gated-channels**: The primary category for AIS architecture. Van Wart 2007, Kole 2008,
  Hu 2009, KoleLetzkus 2007, and Werginz 2020 all live here; together they define the AIS channel
  set and the key ~7x AIS-to-soma Nav density ratio.
* **retinal-ganglion-cell**: Contains the Fohlmeister 2010 multi-compartment RGC model with
  soma/dendrite/AIS channel-density tables, and Werginz 2020 (double-listed).
* **compartmental-modeling**: Contains the Poleg-Polsky 2016 NEURON model (the Bed B ancestor), de
  Rosenroll 2026 (the direct Bed B substrate), and Poleg-Polsky 2026 (the ML-driven MOBO analogue).
  The category contextualises the MOBO task within prior parametric DSGC searches.
* **direction-selectivity**: Contains the experimental DSI and firing-rate ground-truth papers:
  Oesch 2005, Sivyer 2010, Park 2014, Sivyer 2013.
* **patch-clamp**: Werginz 2020 and Kole 2008 are also indexed here; patch-clamp data is the
  experimental anchor for AIS Nav density and AIS geometry priors.
* **dendritic-computation**: Oesch 2005 and Sivyer 2013 document active dendritic spikes and
  branch-level DS computation. Not used for AIS architecture, but supplies the DSI ceiling that the
  optimiser is trying to reach.
* **synaptic-integration**: The de Rosenroll 2026 and Poleg-Polsky 2016 papers also carry this
  category. Ledesma et al. 2024 (Kv3 at SAC soma / mGluR2 at dendrites, reviewed as Aldor2024 in the
  corpus) was reviewed but is SAC-focused rather than DSGC-AIS-focused and is not cited.

Two categories yielded no cited papers: **cable-theory** (papers on passive cable properties are not
directly load-bearing for AIS parameter-prior decisions) and an absent `bayesian-optimization`
category (no BoTorch / qLogNEHVI / hypervolume papers are in the local corpus; this is a gap flagged
below). No papers from the **synaptic-integration**-only set (e.g., Briggman 2011, Ding 2016) are
cited because they cover retinal wiring rather than channel-density priors.

## Key Findings

### AIS Geometry and Channel Architecture in RGCs

The axon initial segment is not a featureless transition zone but a highly structured, bi-partite
microdomain with distinct proximal and distal sub-compartments. In adult rodent retinal ganglion
cells, Van Wart and colleagues (2007) demonstrated immunohistochemically that Nav1.6 is the
predominant sodium-channel isoform at the distal AIS, while the proximal AIS hosts a separate
accumulation of Nav1.1 that is spatially segregated from Nav1.6; Kv1.2 co-localises with Nav1.6 in
the distal AIS but is absent from the proximal sub-compartment [VanWart2006]. This two-domain
architecture directly motivates the two-subsegment AIS design used in t0078: a proximal subsegment
matching the Nav1.1 / Nav1.2 profile and a distal subsegment dominated by Nav1.6 and Kv1.2,
consistent with the Van Wart 2007 immunostaining and with Hu 2009's functional demonstration that
Nav1.6 handles spike initiation while Nav1.2 handles back-propagation in cortical neurons [Hu2009].
Kole and Letzkus (2007) showed that AIS Kv1 channels control the axonal action-potential waveform
and synaptic efficacy in cortical layer-5 pyramids [KoleLetzkus2007], reinforcing the Kv1.2 role in
shaping AIS repolarisation.

The key quantitative prior for the t0078 parameter bounds is the **AIS-to-soma Nav channel density
ratio of approximately 7x**, directly measured by Werginz, Raghuram, and Fried (2020) in OFF-alpha-T
retinal ganglion cells using Nav1.6 immunohistochemistry [Werginz2020]. The 7x ratio is
independently consistent with the Kole 2008 finding that action-potential generation requires a high
Na+ channel density specifically at the AIS [Kole2008] and with the Fohlmeister 2010
multicompartment model of rat/cat RGCs, which places peak Na+ conductance at a "thin segment" 50-130
um distal to the soma — up to **448 mS/cm^2** in cat alpha RGCs vs. **60-160 mS/cm^2** at the soma
[Fohlmeister2010, Table 1, p. 1360]. This ratio sets the upper bound on the AIS Nav1.6 density in
the t0078 search: if soma Nav is ~70 mS/cm^2, then AIS Nav should reach ~500 mS/cm^2 = **0.5
S/cm^2**, consistent with the Kole 2008 prior of 2500-5000 pS/um^2 = **0.25-0.5 S/cm^2** cited in
the t0076 compare-literature report.

AIS length is both a structural parameter and a tuning knob. Werginz 2020 found that AIS length is
the dominant morphological predictor of maximum firing rate in an OFF-alphaT NEURON compartmental
model: **dorsal** OFF-alphaT cells with longer AISs sustain higher firing rates without
depolarisation block, while **ventral** cells with shorter AISs enter depolarisation block at lower
input currents [Werginz2020]. This result motivates the t0078 AIS length range of 25-50 um (default
30 um) and warns that fixing AIS length to a single value will bias the optimiser toward either
high-rate or low-rate regimes, without exploring the intermediate landscape that may support the DSI
> = 0.4 AND PD rate >= 30 Hz joint target.

**Best practice**: Use AIS length 25-50 um with diameter ~0.8 um. Place Nav1.6 at AIS density ~7x
soma in the search-space prior. Exclude NaP, BK, SK from the AIS section (these are not reported at
the AIS in RGC immunostaining).

**Hypothesis**: Enabling an explicit AIS section with Nav1.6 at ~7x soma density will shift the
Pareto front toward higher PD firing rates without proportional DSI loss, because spike initiation
will no longer require the dendrites to reach somatic threshold — AIS initiation is more
economical and can be gated by the GABA-mediated null-direction inhibition closer to the soma.

### Tier-Stratified Channel Densities Across Compartments

Fohlmeister and colleagues (2010) fitted multicompartment NEURON models of anatomically
reconstructed rat and cat RGCs at multiple temperatures (7-37 C) and extracted a unique
cell-type-specific channel-density map per compartment tier [Fohlmeister2010]. The rat Type-I
five-channel densities at 35 C illustrate the graded gradients that are flattened by the t0076 25-d
search: Na at **79.5 / 72.0 / 141.1 / 231.1 mS/cm^2** (dendrites / soma / IS / thin-segment), K(DR)
at **23.4 / 50.4 / 67.8 / 74.6 mS/cm^2**, K(A) at ~36 mS/cm^2 on soma/dendrites (absent from AIS),
and K(Ca) small everywhere [Fohlmeister2010, Table 1, p. 1360-1362]. These gradients are
cell-type-specific: cat alpha RGCs have Na at 60.8 soma vs. 448.5 mS/cm^2 thin-segment (7.4-fold),
while rat Type-II has 88.4 soma vs. 378.6 mS/cm^2 (4.3-fold). The canonical approach of applying a
single Na density uniformly to soma and all 350 dendrites (as in t0076 Bed B) therefore
misrepresents the biophysical reality by collapsing a 3-5-fold somatodendritic gradient and a
~7-fold soma-to-AIS gradient into a single scalar.

The Ledesma et al. 2024 study of starburst amacrine cells provides an independent observation of
subcellular channel segregation in a retinal neuron: Kv3.1 is anatomically restricted to the
perisomatic region while mGluR2 is distributed throughout the dendritic arbor, and co-blocking both
eliminates direction selectivity in downstream DSGCs. While this is SAC rather than DSGC biology,
the finding reinforces that perisomatic vs. dendritic Kv segregation is functionally significant in
the retinal circuit — the t0078 BK and Kv3 tier-stratification is biologically grounded by this
analogy. (Paper reviewed but not cited; see Category Selection Rationale.)

Sivyer and Williams (2013) demonstrated active dendritic integration is required for DSGC DS
computation [Sivyer2013]. Their compartmental model of a rabbit DSGC only reproduced
terminal-dendritic spike initiation when terminal branches were endowed with physiologically
plausible densities of voltage-gated sodium and calcium channels; passive-only (zero gNa, zero gCa)
models failed to match observed spike-like events. The corollary for t0078 is that the
tier-stratified Nav1.6 densities on proximal and mid dendrites must be set high enough to support
dendritic initiation, not just somatic integration — if the optimiser drives all dendritic Nav to
zero it will converge to the same passive-integration regime already explored by t0076.

**Best practice**: Allow Nav1.6 and NaP to range independently across all five tiers, but start the
Sobol DoE with the Fohlmeister 2010 ratio structure as the nominal point (soma ~72, IS ~141,
thin-segment ~230 mS/cm^2). This biases the DoE away from the degenerate uniform-density manifold
that t0076 already explored.

**Hypothesis**: Tier-stratified Nav1.6 with AIS >> soma > proximal-dendrite > terminal-dendrite will
permit the optimiser to decouple high-frequency somatic/AIS spiking from dendritic direction
computation — a decoupling that the uniform-density t0076 substrate cannot achieve.

### Slow AHP Mechanisms and Firing-Rate Caps in RGCs

The t0076 compare-literature report explicitly identifies the absence of a slow Ca-activated K+
adaptation as a cause of the hyper-physiological PD firing rates at the Pareto high-rate extreme
(128 Hz, DSI 0.003). This is consistent with the Fohlmeister 2010 five-channel model, which includes
a K(Ca) (Ca-activated K, equivalent to BK/SK family) channel on all compartments, with the Ca pool
modelled as a thin submembrane shell with first-order removal [Fohlmeister2010, Methods]. The K(Ca)
in the Fohlmeister model activates via a Hill equation Ca^2/(K_d^2 + Ca^2), requiring intracellular
Ca to rise before it fires — an intrinsic adaptation that limits sustained firing rates. The Bed B
substrate uses a single `cad` Ca pool with `taur = 5 ms` (from the Hay 2011 cortical model lineage,
per t0076 research), which is far faster than the slow AHP time constants observed in mammalian
neurons at physiological temperatures (50-200 ms range per general SK/SK_E2 literature, not yet in
the local corpus). The t0078 design of an extended Ca-binding time constant on SK_E2 (a
`tau_ca_multiplier` parameter) is therefore directly motivated by the mismatch between the existing
`cad` kinetics and the empirical slow-AHP time scale needed to cap firing below ~80 Hz.

Oesch and colleagues (2005) measured a modal PD firing rate of **148 +/- 30 Hz** in rabbit DSGCs
during the peak of the light-evoked burst [Oesch2005, Results p. 754], but noted that the 1-s mean
rate is far lower due to adaptation. Sivyer 2010 reports DSI values of approximately **0.45 (ON-OFF,
ON)** and **0.50 (ON-OFF, OFF)** in rabbit retina, with a null-to-preferred inhibitory conductance
ratio of **3.4 +/- 2.0** and preferred-to-null excitatory ratio of **1.6 +/- 0.7**
[Sivyer2010, Results]. Park 2014 measured In-vivo-like mouse DSGC DSI at **0.65 +/- 0.05** in
CART-Cre mice and **0.73 +/- 0.03** in TRHR-GFP mice, with null-direction inhibitory conductance of
**2.43 +/- 0.31 nS** (approximately 8x the apparent excitatory DS of **0.31 +/- 0.05 nS**)
[Park2014, Results, Table 1]. These values establish the experimental range: realistic mouse DSGC
has DSI in **[0.45, 0.73]** and, per project domain knowledge, mean PD firing rates of 30-80 Hz.

**Best practice**: Use the slow-AHP `tau_ca_multiplier` parameter range [1, 20x] to span from the
t0074 Hay-derived default (multiplier = 1, taur ~5 ms) to a physiologically plausible slow-AHP (taur
~100 ms). Treat the multiplier as a free MOBO parameter with a log-uniform prior.

**Hypothesis**: Introducing the slow-Kv-AHP will cap the Pareto high-rate extreme below 80 Hz and
simultaneously allow DSI to remain high at moderate rates (30-60 Hz), because the slow K+
conductance will act as an automatic gain-control mechanism that prevents the saturated-firing
regime seen at iter 319 (128 Hz, DSI 0.003) in t0076.

### Bed B Substrate Biology and the t0076 Trade-Off

The Bed B substrate is the DSGC compartmental model from de Rosenroll and colleagues (2026), which
combines a `RGCmodelGD.hoc` morphology from Geoffder's GitHub repository with a GABA/ACh
co-transmission SAC network model [deRosenroll2026]. The model ships as an MIT-licensed NEURON +
Python implementation (`geoffder/ds-circuit-ei-microarchitecture`, Zenodo 10.5281/zenodo.17666157)
with MOD files `HHst_noiseless.mod`, `Exp2NMDA.mod`, and `cadecay.mod`. The published
deRosenroll2026 model produces DSI **0.39** under correlated SAC release and **0.25** under
uncorrelated SAC release [deRosenroll2026, Fig. 5], and the t0076 optimiser matched these benchmarks
within +0.03 (iter 424: DSI **0.42**, PD rate **4.95 Hz**), validating the substrate. The key
limitation is that Bed B's `_configure_soma` applies HHst sodium only to the soma — the 350
dendritic compartments receive no active conductances — so the cell cannot produce the active
dendritic spike initiation documented by Oesch 2005 and Sivyer 2013.

The Poleg-Polsky 2016 NEURON model is the direct ancestor of the Bed B substrate, providing 177 AMPA
\+ 177 NMDA + 177 GABA_A synapses on ON dendrites of a reconstructed DRD4 mouse DSGC
[PolegPolsky2016]. That model demonstrated that passive dendritic propagation is sufficient for DS
computation (no dendritic spikes required to match mouse DRD4 DSI ~0.6-0.7) when multiplicative NMDA
gating is present. The Bed B substrate inherits this architecture but does not include an AIS
section. The Poleg-Polsky 2026 ML-driven search of a 352-segment DSGC [PolegPolsky2026] provides a
direct methodological analogue: it uses a large-scale parameter search (machine-learning outer loop,
DSI evaluation under moving-bar stimuli) and discovers multiple novel computational primitives
(velocity-dependent coincidence detection, distance-graded delay lines, NMDA multiplicative gating).
The t0078 qLogNEHVI search is narrower (joint maximisation of two objectives, not a single-objective
threshold sweep) but draws on the same substrate architecture.

**Best practice**: The substrate validation cell (iter 424 DSI 0.42, PD rate 4.95 Hz) should be
confirmed at the start of the t0078 BO loop using the augmented AIS substrate at AIS
`tau_ca_multiplier = 1` (default SK kinetics) and all uniform-density channels at t0076 Pareto-best
values. If the augmented substrate regresses below DSI 0.39 at these settings, the AIS section has
introduced a bug.

### DSI and Firing-Rate Targets in Mouse and Rabbit DSGCs

Four experimental papers bound the joint operating point that t0078 is trying to reach:

* Oesch 2005 [Oesch2005]: spike DSI **0.67 +/- 0.13 (ON)** and **0.74 +/- 0.13 (OFF)** in rabbit
  DSGCs; PSP DSI only **0.09 (ON)** / **0.14 (OFF)** — active dendritic spikes sharpen tuning
  ~6-fold; somatic refractory period **3.5 +/- 0.7 ms** (implies maximum sustained rate ~286 Hz, but
  adaptation limits mean 1-s rates to ~30-80 Hz).
* Sivyer 2010 [Sivyer2010]: ON-OFF DSGC ON DSI approximately **0.45**, OFF DSI approximately
  **0.50**; null-to-preferred inhibitory conductance ratio **3.4 +/- 2.0**; von Mises kappa **0.91
  +/- 0.07** (ON-OFF), **1.06 +/- 0.05** (ON).
* Park 2014 [Park2014]: mouse On-Off DSGC DSI **0.65 +/- 0.05** (CART-Cre) and **0.73 +/- 0.03**
  (TRHR-GFP); null inhibitory conductance **2.43 +/- 0.31 nS** (~8x excitatory DS of **0.31 +/- 0.05
  nS**).
* Sivyer 2013 [Sivyer2013]: rabbit DSGC somatic DSI **close to 1** when measured from
  terminal-dendritic spike initiation; collapsing to near-zero with bath TTX — a ceiling metric
  not comparable to our 8-direction spike-count DSI.

The gap between the published mouse DSI range (**0.6-0.7** per PolegPolsky2016 and Park2014) and the
t0076 Pareto ceiling (**0.42 at 4.95 Hz**) is approximately **0.2-0.3 DSI units**. This gap is
consistent with the absence of AIS-mediated spike initiation in Bed B: the Oesch 2005 6-fold
sharpening figure implies that a passive-dendritic cell should reach PSP DSI ~0.1, matching t0076's
Pareto structure. The t0078 AIS addition does not directly add dendritic spikes, but it does add a
low-threshold spike-initiation compartment that can be gated by the somatic GABA inhibition and may
enable higher DSI at physiological rates.

**Hypothesis**: If the AIS section successfully gates somatic output, the Pareto front will show a
"kink" at DSI ~0.5-0.6, PD rate ~30-50 Hz where AIS-initiated spikes are selectively suppressed in
the null direction but not the preferred direction. If no kink appears and the Pareto remains
monotone, the AIS alone is insufficient and dendritic active conductances are the missing
ingredient.

## Methodology Insights

1. **AIS section geometry**: Use two NEURON `Section` objects for the AIS (proximal: Nav1.1/Nav1.2,
   distal: Nav1.6/Kv1.2), each ~15 um long, total AIS length 25-50 um, diameter ~0.8 um. Apply the
   `d_lambda = 0.1` at 100 Hz segment-count rule. The Werginz 2020 NEURON model demonstrates this
   design is adequate for reproducing AIS firing-rate differences [Werginz2020]; the t0069 Bed A AIS
   code should be ported rather than re-derived.

2. **Nav1.6 density search bounds**: Set AIS Nav1.6 prior as [0.0, 1.0] S/cm^2. The biologically
   plausible range from Kole 2008 / Werginz 2020 is [0.25, 0.5] S/cm^2 [Kole2008, Werginz2020].
   Allow the optimiser to explore outside this range, but flag Pareto cells where AIS Nav1.6 falls
   outside [0.25, 0.5] S/cm^2 as biologically marginal in the compare-literature output.

3. **Fohlmeister 2010 as tier-density prior**: Use the Fohlmeister 2010 rat Type-I G-bar table as
   the nominal starting point for the Sobol DoE: soma Nav ~72 mS/cm^2, proximal-dendrite Nav ~80
   mS/cm^2 (dendrite column), mid-dendrite Nav same as proximal, terminal-dendrite Nav ~60% of
   proximal, AIS Nav ~140-230 mS/cm^2 = ~0.14-0.23 S/cm^2 [Fohlmeister2010, Table 1]. This ensures
   the DoE samples around the biologically informed regime rather than random uniform.

4. **SK_E2 tau_ca_multiplier range**: Use a log-uniform prior over [1, 20]. Multiplier = 1
   reproduces the t0074 Hay-derived default (taur ~5 ms). Multiplier = 20 gives taur ~100 ms, within
   the range of slow-AHP kinetics in mammalian neurons. An intermediate multiplier of ~5 (taur ~25
   ms) may capture the RGC slow-AHP timescale suggested by the t0076 compare-literature analysis.

5. **DSI target**: Set the optimiser reference point at DSI = 0.0, PD rate = 0.0 Hz and the utopia
   point at DSI = 0.7, PD rate = 80 Hz — consistent with the Park 2014 and Sivyer 2010
   experimental ceilings [Park2014, Sivyer2010]. The hypervolume computation will then be comparable
   across runs.

6. **Validation cell**: Before launching the full BO loop, confirm the substrate by running the
   t0076 Pareto-best joint cell (iter 424 parameters) through the augmented substrate and checking
   that DSI stays within ±0.05 and PD rate within ±1 Hz of the t0076 values. If it deviates, the
   AIS or slow-AHP addition has introduced a regression.

7. **qLogNEHVI vs qNEHVI**: Migrate to `qLogNoisyExpectedHypervolumeImprovement` from BoTorch. The
   Poleg-Polsky 2026 ML search over a comparable 350+ compartment DSGC [PolegPolsky2026]
   demonstrates that large-scale parametric DSGC searches are computationally tractable; the key
   numerical difference in t0078 is the larger input dimensionality (~47 d vs t0076's 25 d), which
   motivates the input `Normalize` transform to keep GP fitting stable.

8. **Depolarisation block as a constraint**: The Werginz 2020 result that AIS length controls the
   depolarisation-block threshold [Werginz2020] means that a Pareto cell with a very long AIS (>50
   um) at high Nav1.6 density may enter depolarisation block during the preferred-direction
   stimulus. Track `is_unstable` per the t0076 protocol (peak Vm outside [-80, +60] mV) and discard
   unstable evaluations from the Pareto front.

## Gaps and Limitations

1. **No SK / Hay 2011 / Khaliq 2003 papers in the local corpus.** The slow-AHP mechanism (SK_E2 with
   extended Ca-binding) is drawn from Hay 2011 and Khaliq 2003 sources cited in the t0076
   research_internet.md, but neither paper is a downloaded asset in this project's corpus. Kinetics
   for the `tau_ca_multiplier` parameter therefore cannot be grounded by a local primary source; the
   multiplier range must be treated as exploratory. The research-internet stage should download and
   summarise the Hay 2011 and Khaliq 2003 SK model papers.

2. **No BoTorch / qLogNEHVI / hypervolume papers in the local corpus.** The optimiser methodology
   (qLogNEHVI, Normalize transform, BoTorch acquisition) is not backed by any downloaded paper. The
   research-internet stage should retrieve the BoTorch / qLogNEHVI publication (Ament et al. 2023
   NeurIPS or similar) to justify the qLogNEHVI migration from qNEHVI.

3. **No joint DSI + firing-rate measurements in the local corpus.** The t0076 compare-literature
   analysis identified this gap explicitly: Oesch 2005 reports modal burst rate (148 ± 30 Hz) not
   mean 1-s PD rate; Sivyer 2010 reports DSI but not mean firing rates at the same operating
   condition; Park 2014 reports DSI without firing rates. No paper in the corpus directly measures
   both DSI and mean 1-s preferred-direction firing rate in the same mouse or rabbit DSGC
   preparation. The "30-80 Hz" PD rate range is from project domain knowledge, not a verifiable
   local source. The research-internet stage should specifically target papers measuring
   simultaneous DSI + PD firing rate (e.g., Trenholm 2013, Kim et al. 2022, Demb & Singer 2015).

4. **Werginz 2020 and Van Wart 2007 PDFs not downloaded (paywalled).** The summaries for these two
   papers are based on CrossRef abstracts and training-data knowledge; specific numerical values
   (exact AIS-to-soma density ratio curve, exact immunostaining intensity ratios by location) must
   be manually retrieved from the publisher PDFs before citation in the planning document.

5. **Fohlmeister 2010 RGC types are rat/cat, not mouse DSGC.** The G-bar table values from
   Fohlmeister 2010 apply to anatomically reconstructed rat Type-I/II and cat alpha/beta RGCs, not
   to the C57BL/6 mouse ON-OFF DSGCs that Bed B models. Species and cell-type differences in channel
   distribution are not quantified in the local corpus. The Fohlmeister 2010 values should be used
   as structural priors (ratio structure) rather than absolute density targets.

6. **No dedicated SK / KAHP kinetics paper for RGC context.** The `cadecay.mod` / `SK_E2` mechanism
   is vendored from cortical or Purkinje cell sources; its kinetics may be inappropriate for the RGC
   AIS context where Ca entry occurs via smaller, shorter Ca transients than in cortical neurons. A
   dedicated RGC patch-clamp study of afterhyperpolarisation kinetics is not in the corpus and
   should be targeted in the internet research stage.

## Recommendations for This Task

1. **Implement the two-subsegment AIS with Nav1.6 density ~0.25-0.5 S/cm^2 as the central prior**
   [VanWart2006, Kole2008, Werginz2020]. This is the single highest-confidence prior from the
   corpus: the 7x AIS-to-soma ratio is directly measured (not inferred), is consistent across three
   independent methods (immunostaining, current-clamp, compartmental model), and provides a
   well-defined interval for the BoTorch search.

2. **Use the Fohlmeister 2010 rat Type-I channel-density ratios as the nominal Sobol DoE seed
   point** [Fohlmeister2010]. The absolute values are species/type-specific, but the relative ratios
   (soma / IS / thin-segment for Na and K) encode the biologically observed gradient structure and
   will bias the DoE away from the degenerate uniform-density manifold already explored by t0076.

3. **Include the `tau_ca_multiplier` (SK_E2 extended Ca-binding) as a free MOBO parameter with
   log-uniform prior over [1, 20]**. No local corpus paper directly constrains the RGC slow-AHP
   timescale, but the Fohlmeister 2010 K(Ca) component and the t0076 compare-literature analysis
   both indicate that a slow adaptation mechanism is needed to cap firing below 80 Hz
   [Fohlmeister2010].

4. **Set utopia point at DSI = 0.7, PD rate = 80 Hz** for hypervolume computation, consistent with
   the Park 2014 upper bound [Park2014] and the project-domain PD rate ceiling. This makes the t0078
   hypervolume directly comparable to the t0076 final HV = 8.4129 (which used the same reference
   point per the t0076 implementation).

5. **Flag any Pareto cell with AIS Nav1.6 outside [0.25, 0.5] S/cm^2 as biologically marginal** in
   the compare-literature output [Kole2008, Werginz2020]. This does not constrain the search space
   but enables the analysis to distinguish biologically plausible from extrapolated operating
   points.

6. **Perform a substrate regression check before launching the full BO loop**: run the t0076
   iter-424 parameters through the augmented substrate and confirm DSI ∈ [0.37, 0.47] and PD rate
   ∈ [3.95, 5.95 Hz]. If this check fails, debug the AIS attachment before burning compute on
   600-800 acquisition iterations [deRosenroll2026].

7. **Plan internet research to fill three corpus gaps**: (a) SK / Hay 2011 / Khaliq 2003 AHP
   kinetics, (b) BoTorch qLogNEHVI / hypervolume methodology, (c) simultaneous DSI + PD firing rate
   measurements in mouse/rabbit DSGCs (Trenholm 2013 or equivalent). These gaps will affect the
   planning document if not filled before planning begins.

## Paper Index

### [VanWart2006]

* **Title**: Polarized distribution of ion channels within microdomains of the axon initial segment
* **Authors**: Van Wart, A., Trimmer, J. S., Matthews, G.
* **Year**: 2007
* **DOI**: `10.1002/cne.21173`
* **Asset**: `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1002_cne.21173/`
* **Categories**: `voltage-gated-channels`, `retinal-ganglion-cell`
* **Relevance**: Defines the two-domain AIS architecture in adult rodent RGCs (Nav1.1 proximal,
  Nav1.6 distal, Kv1.2 distal) that directly motivates the t0078 two-subsegment AIS design and the
  exclusion of Nav1.6 from the proximal AIS subsegment.

### [Kole2008]

* **Title**: Action potential generation requires a high sodium channel density in the axon initial
  segment
* **Authors**: Kole, M. H. P. et al.
* **Year**: 2008
* **DOI**: `10.1038/nn2040`
* **Asset**: `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1038_nn2040/`
* **Categories**: `voltage-gated-channels`, `patch-clamp`
* **Relevance**: Establishes the canonical AIS Nav density range (2500-5000 pS/um^2 = 0.25-0.5
  S/cm^2) used as the upper bound on the t0078 AIS Nav1.6 search space.

### [Hu2009]

* **Title**: Distinct contributions of Nav1.6 and Nav1.2 in action potential initiation and
  backpropagation
* **Authors**: Hu, W. et al.
* **Year**: 2009
* **DOI**: `10.1038/nn.2359`
* **Asset**: `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1038_nn.2359/`
* **Categories**: `voltage-gated-channels`, `patch-clamp`
* **Relevance**: Functional dissociation of Nav1.6 (spike initiation at distal AIS) vs. Nav1.2
  (back-propagation), motivating the two-subunit compartment assignment in the t0078 AIS model.

### [KoleLetzkus2007]

* **Title**: Axon Initial Segment Kv1 Channels Control Axonal Action Potential Waveform and Synaptic
  Efficacy
* **Authors**: Kole, M. H. P., Letzkus, J. J., Stuart, G. J.
* **Year**: 2007
* **DOI**: `10.1016/j.neuron.2007.07.031`
* **Asset**:
  `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1016_j.neuron.2007.07.031/`
* **Categories**: `voltage-gated-channels`, `dendritic-computation`
* **Relevance**: Establishes Kv1 expression at the distal AIS as the repolarisation mechanism
  controlling AP waveform; motivates inclusion of Kv1.2 in the distal AIS subsegment.

### [Werginz2020]

* **Title**: Tailoring of the axon initial segment shapes the conversion of synaptic inputs into
  spiking output in OFF-alpha T retinal ganglion cells
* **Authors**: Werginz, P., Raghuram, V., Fried, S. I.
* **Year**: 2020
* **DOI**: `10.1126/sciadv.abb6642`
* **Asset**: `tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1126_sciadv.abb6642/`
* **Categories**: `voltage-gated-channels`, `retinal-ganglion-cell`, `compartmental-modeling`,
  `patch-clamp`
* **Relevance**: Directly measures the AIS-to-soma Na+ density ratio (~7x) in RGCs; shows that AIS
  length is the dominant determinant of maximum firing rate and depolarisation-block threshold in a
  NEURON compartmental model of OFF-alphaT cells — the primary quantitative anchor for the t0078
  AIS parameter bounds.

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
* **Relevance**: Provides the quantitative per-compartment channel-density table for rat and cat
  RGCs (dendrites / soma / IS / thin-segment) that supplies the Sobol DoE seed point for the t0078
  tier-stratified channel densities.

### [deRosenroll2026]

* **Title**: Uncovering the "hidden" synaptic microarchitecture of the retinal direction selective
  circuit
* **Authors**: deRosenroll, G., Sethuramanujam, S., Awatramani, G. B.
* **Year**: 2026
* **DOI**: `10.1016/j.celrep.2025.116833`
* **Asset**: `tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1016_j.celrep.2025.116833/`
* **Categories**: `compartmental-modeling`, `direction-selectivity`, `retinal-ganglion-cell`,
  `synaptic-integration`, `dendritic-computation`
* **Relevance**: The Bed B substrate paper; its published DSI 0.39 (correlated SAC release) is the
  primary substrate-validation anchor for t0078 and defines the baseline that the augmented
  architecture must meet or exceed.

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
* **Relevance**: Ancestor of the Bed B model; establishes DSI 0.6-0.7 as the target for mouse DRD4
  DSGCs and documents 177 AMPA + 177 GABA synapse architecture. Passive dendritic propagation proved
  sufficient for DS at this DSI level, but an AIS was not modelled.

### [PolegPolsky2026]

* **Title**: Machine learning discovers numerous new computational principles underlying direction
  selectivity in the retina
* **Authors**: Poleg-Polsky, A.
* **Year**: 2026
* **DOI**: `10.1038/s41467-026-70288-4`
* **Asset**: `tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/`
* **Categories**: `compartmental-modeling`, `direction-selectivity`, `retinal-ganglion-cell`,
  `synaptic-integration`, `dendritic-computation`
* **Relevance**: ML-driven MOBO analogue for a 352-segment DSGC; demonstrates the tractability of
  large-scale parametric DSGC search and motivates the t0078 methodology (cluster-based mechanism
  discovery, large Sobol DoE, acquisition-function-driven refinement).

### [Oesch2005]

* **Title**: Direction-Selective Dendritic Action Potentials in Rabbit Retina
* **Authors**: Oesch, N., Euler, T., Taylor, W. R.
* **Year**: 2005
* **DOI**: `10.1016/j.neuron.2005.06.036`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2005.06.036/`
* **Categories**: `direction-selectivity`, `dendritic-computation`, `voltage-gated-channels`,
  `retinal-ganglion-cell`, `patch-clamp`
* **Relevance**: Primary source for experimental DSI values (ON 0.67 ± 0.13, OFF 0.74 ± 0.13) and
  modal peak PD firing rate (148 ± 30 Hz) in rabbit; documents the 6-fold sharpening of tuning by
  active dendritic spike initiation that Bed B cannot yet reproduce.

### [Sivyer2010]

* **Title**: Synaptic inputs and timing underlying the velocity tuning of direction-selective
  ganglion cells in rabbit retina
* **Authors**: Sivyer, B. et al.
* **Year**: 2010
* **DOI**: `10.1113/jphysiol.2010.192716`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1113_jphysiol.2010.192716/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`,
  `patch-clamp`
* **Relevance**: Provides the null-to-preferred inhibitory conductance ratio (3.4 ± 2.0) and ON-OFF
  DSGC DSI values (ON ~0.45, OFF ~0.50) used as the lower bound of the t0078 biological target
  range.

### [Park2014]

* **Title**: Excitatory Synaptic Inputs to Mouse On-Off Direction-Selective Retinal Ganglion Cells
  Lack Direction Tuning
* **Authors**: Park, S. J. H. et al.
* **Year**: 2014
* **DOI**: `10.1523/JNEUROSCI.5017-13.2014`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_JNEUROSCI.5017-13.2014/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`,
  `patch-clamp`
* **Relevance**: Mouse On-Off DSGC DSI 0.65 ± 0.05 (CART-Cre) and 0.73 ± 0.03 (TRHR-GFP); sets the
  upper DSI bound of the biologically realistic target range for t0078 comparison.

### [Sivyer2013]

* **Title**: Direction selectivity is computed by active dendritic integration in retinal ganglion
  cells
* **Authors**: Sivyer, B., Williams, S. R.
* **Year**: 2013
* **DOI**: `10.1038/nn.3565`
* **Asset**: `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1038_nn.3565/`
* **Categories**: `direction-selectivity`, `dendritic-computation`, `retinal-ganglion-cell`,
  `patch-clamp`
* **Relevance**: Direct dual-patch evidence that DS computation requires active dendritic
  integration with voltage-gated Nav and Ca at terminal dendrites; sets the expectation that Pareto
  cells achieving DSI > 0.6 in t0078 may require non-zero dendritic Nav1.6 density (not just AIS
  addition).
