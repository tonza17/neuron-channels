---
spec_version: "1"
task_id: "t0027_literature_survey_morphology_ds_modeling"
research_stage: "papers"
papers_reviewed: 12
papers_cited: 10
categories_consulted:
  - "direction-selectivity"
  - "compartmental-modeling"
  - "dendritic-computation"
  - "retinal-ganglion-cell"
  - "synaptic-integration"
date_completed: "2026-04-21"
status: "complete"
---
## Task Objective

Survey existing corpus papers that build computational, biophysical, or theoretical models linking
neuronal morphology to direction selectivity (DS) in retinal direction-selective ganglion cells
(DSGCs), starburst amacrine cells (SACs), and other DS neurons. Identify which morphology variables
have been demonstrated in compartmental simulations, cable-theory derivations, or models with
explicit spatial structure to causally affect direction selectivity, by what mechanisms, and where
gaps remain. Findings here scope the internet-search and synthesis stages of this task.

## Category Selection Rationale

Consulted `direction-selectivity` because every relevant paper measures a directional outcome (DSI,
preferred-vs-null asymmetry, vector tuning). Consulted `compartmental-modeling` because the
inclusion criterion requires an explicit-morphology simulator (NEURON, custom solver) or cable
derivation. Consulted `dendritic-computation` to capture passive and active dendritic mechanisms
that operate on geometry. Consulted `retinal-ganglion-cell` to cover DSGC- and SAC-specific work.
Consulted `synaptic-integration` because morphology mediates how synaptic inputs combine. Excluded
purely point-neuron DS network papers (no morphology variable), pure NMDA-Mg-block papers without
geometry manipulation, and pure E/I-timing papers fitting one fixed morphology — none of these
satisfy the "morphology as a manipulated variable" criterion.

## Key Findings

### Electrotonic Compartmentalization Sets the Spatial Grain of DS

Multiple papers converge on the result that the DSGC dendritic tree is electrotonically fragmented —
DS computation happens in many small subunits rather than one global integration. [Schachter2010]
showed in a NEURON model of an ON-OFF DSGC that distal input resistance exceeds **1 GOhm**, that
local PSPs amplify from a presynaptic DSI of **~0.2** to a spike DSI of **~0.8** through a roughly
**4x** dendritic-spike thresholding nonlinearity, and that intrinsic dendritic geometry alone
produces a small but opposing DSI of **−0.1 to −0.2** that the synaptic asymmetry must overcome.
[Jain2020] then sharpened this picture with high-resolution two-photon calcium imaging plus a
177-synapse NEURON reconstruction: the dendritic space constant for fast EPSPs is **λ ≈ 5.3 µm**,
calcium hotspots have **FWHM 3.0 ± 1.2 µm**, and DS subunits are at the **5-10 µm** scale — far
finer than the dendritic-branch level previously assumed. [Morrie2018] complements this from the
input side: when SAC density on the SAC plexus is reduced, DSGC DS collapses, indicating that the
spatial tiling of inhibition onto DSGC dendrites is itself a morphology variable that matters as
much as DSGC geometry. **Best practice**: compartmental DSGC models must use ≥100-segment morphology
and small (≤10 µm) compartments — coarser discretizations average over the actual unit of
computation and overestimate global integration.

### Asymmetric SAC Inhibition Is the Dominant Mechanism, but Not the Only One

[Taylor2002] established three distinct synaptic asymmetries that produce DS in DSGCs: (1)
presynaptic preferred-direction excitation, (2) presynaptic null-direction inhibition, and (3)
postsynaptic spatially-offset inhibition (~**160 µm** offset in OFF-arbor models). The ON-arbor used
only the two presynaptic asymmetries, suggesting that DSGC sublamina morphology constrains which
mechanism dominates. [PolegPolsky2026], using a machine-learning sweep over a **352-segment** DSGC
model with varying bipolar-cell offsets, weights, kinetics, and dendritic biophysics, discovered
that classical SAC-mediated null-direction inhibition is sufficient but *not necessary* for DS —
velocity-dependent coincidence detection, distance-graded delay lines, and NMDA-mediated
multiplicative gating each independently produce robust DS when geometry and input arrangement
support them. [Hanson2019] reinforced this empirically: DSGCs retain DS even when SAC GABA release
is *symmetric*, indicating that asymmetric SAC tuning is not the sole cause and that downstream
dendritic processing on DSGC morphology contributes additional mechanisms. [deRosenroll2026] showed
via a network model fitted to two-photon Ca²⁺ imaging that local spatiotemporal perturbations of
acetylcholine — *without* changing global E/I balance — uncouple E/I within local dendritic DS
subunits and abolish local DS, again pointing to the **subcellular microarchitecture** rather than
global wiring as the locus of DS.

### Active Dendritic Conductances Convert Subthreshold Asymmetry into Spike Asymmetry

[Schachter2010] is the canonical reference for the active-conductance amplification mechanism:
uniform dendritic Na⁺ density of **40 mS/cm²** (or a proximal-to-distal gradient of **45→20
mS/cm²**) supports dendritic spikes that threshold the small subthreshold preferred-vs-null
asymmetry into a much larger spike-rate asymmetry. The same paper shows that **inhibition initiation
vs. propagation are dissociable** — a few nS of GABA shunt is sufficient to *block dendritic spike
initiation*, whereas blocking *propagation* of an already-initiated spike requires ~**85 nS** of
conductance over a comparable region. This means morphology determines where inhibition needs to be
placed: small distal inhibitory synapses can veto local dendritic spikes that would otherwise reach
the soma. [Jain2020] complements this with NMDA-receptor non-linearity: for soft voltage thresholds
of **−55 / −50 / −48 mV**, the dendritic DSI rises from **0.42 / 0.70 / 0.80** — a steeply nonlinear
amplification gated by local depolarization and therefore by local morphology. Both papers agree
that without active dendritic mechanisms, the synaptic asymmetry alone produces only modest
spike-rate DS.

### Cable Theory and Dendritic Geometry Provide the Substrate

The classical cable-theory framework underpins all of the above. [Rall1967] derived analytically
that distance from soma to synapse, dendritic diameter taper, and input arrival timing combine to
produce direction-dependent EPSPs even on a *passive* dendritic cylinder — input sequences arriving
*soma-ward* produce larger and faster-rising EPSPs than the same inputs arriving *distally*, giving
an intrinsic morphological DS for sequenced input. [KochPoggio1982] extended this to retinal
ganglion-cell branching morphology and showed that asymmetric branching patterns produce systematic
direction biases in voltage transfer to the soma — i.e., dendritic morphology *alone*, with no
active conductances and no asymmetric input, can support a measurable DSI. [LondonHausser2005]
synthesized two decades of dendritic-computation work and identified the morphology variables most
strongly implicated in dendritic DS: **branch order**, **dendritic diameter**, **distance from
soma**, and the **spatial layout of synapses on the dendrites**. **Hypothesis**: passive geometric
DS (Rall/Koch–Poggio mechanism) sets a baseline that active dendritic spikes (Schachter) and NMDA
gating (Jain) amplify. The three mechanisms should be testable as additive components in a sweep
over morphology.

### Dense, Symmetric SAC Tiling Onto DSGC Dendrites Is Itself a Morphology Variable

[Morrie2018] showed that reducing the density of SACs in the IPL plexus disproportionately disrupts
DSGC DS — i.e., the *topology* of the SAC→DSGC contact graph is a morphology variable in the DS
computation, even when each individual cell's morphology is held fixed. [deRosenroll2026] extended
this: minor regional perturbations of ACh signalling, which preserve global E/I balance but break
*local* alignment between SAC inhibition and bipolar excitation on DSGC dendrites, collapse local DS
subunits. Taken with [Jain2020]'s finding that DS is computed at **5-10 µm** spatial scale, this
argues that the *spatial co-registration* of inputs onto DSGC dendrites — not just the dendritic
geometry of the DSGC itself — is the morphological variable that determines whether DS emerges.

## Methodology Insights

* **Use NEURON with ≥100-segment morphologies, ≤10 µm compartments**. [Schachter2010] and [Jain2020]
  both demonstrate that the relevant DS computation happens at **λ ≈ 5.3 µm** spatial scale; a
  coarser discretization will miss the local non-linearities that produce most of the spike DSI. Use
  realistic reconstructions (Eyewire / Bionet morphologies), not stylised cylinders, for any
  quantitative comparison.

* **Always include a "no asymmetric inhibition" condition**. [Hanson2019] and [PolegPolsky2026] both
  show DS persists without asymmetric SAC inhibition — so any morphology sweep must include that
  baseline to attribute DS to the morphology variable being manipulated rather than to inhibition
  asymmetry that the morphology change incidentally introduces.

* **Sweep input arrangement, not just dendrite geometry**. [Morrie2018] and [deRosenroll2026] show
  the spatial layout of synapses on dendrites is at least as important as the dendrites themselves.
  A morphology sweep that varies dendritic diameter without re-allocating synapses conflates the two
  factors.

* **Report local dendritic Vm and Ca²⁺ responses, not just somatic spikes**. [Jain2020]'s
  hotspot-FWHM measurements (3.0 ± 1.2 µm) only become visible when you record dendritic compartment
  state. Somatic spike DSI averages out the local DS-subunit structure that morphology actually
  affects.

* **Use the Schachter active-dendritic conductance recipe as a baseline biophysics**. Uniform **40
  mS/cm² gNa** with **45→20 mS/cm² proximal-to-distal taper**, dendritic K density to match, and
  ~4-10 nS GABA-A conductance with **~20 µm spatial offset**, reproduces the canonical PSP-DSI 0.2 →
  spike-DSI 0.8 amplification [Schachter2010]. This is the configuration to vary morphology *around*
  in a sweep.

* **Best practice — space-clamp correction**. [Schachter2010] reports **40-100% space-clamp error**
  in distal compartments. Any DS measurement that depends on somatic recordings must explicitly
  estimate and correct for this; otherwise distal contributions are systematically underestimated.

* **Hypothesis to test**: passive Rall/Koch–Poggio geometric DS, active dendritic-spike DS, and
  NMDA-gated DS are *additive* under realistic morphology. A morphology sweep that turns each
  mechanism on and off independently can decompose the contribution of each.

## Gaps and Limitations

* **No systematic morphology-only sweep on a single DSGC reconstruction exists in the corpus.** Each
  paper varies input timing, synapse placement, conductance density, *or* uses a different
  morphology — none holds biophysics fixed and sweeps morphology variables (length, branch count,
  diameter taper, asymmetric vs symmetric arbor) on the *same* reconstruction. The exact
  morphology→DSI gradient is therefore unknown.

* **Cable-theory bridging to compartmental models is incomplete.** [Rall1967] and [KochPoggio1982]
  give analytical predictions for passive geometric DS, but no corpus paper quantitatively validates
  those predictions in a NEURON model on a real DSGC morphology.

* **Cortical, MT, fly, vestibular DS modeling is essentially absent from the corpus.** All
  morphology→DS papers above are retinal. The general claim "morphology shapes DS" cannot be
  evaluated cross-system without including non-retinal models — this is a primary internet-search
  target.

* **Three of ten corpus references have download_status: "failed"** ([deRosenroll2026],
  [KochPoggio1982], [Rall1967], [LondonHausser2005]). Their summaries here are based on abstracts
  and prior reading; full-text re-validation may be needed during synthesis.

* **No paper quantitatively compares SAC vs DSGC morphology contributions.** [Morrie2018] varies SAC
  density; the others vary DSGC properties — but no head-to-head test exists for which arbor's
  morphology dominates the DS computation.

## Recommendations for This Task

1. **Use the 5 baseline papers + the 10 corpus papers cited here as the seed set** for the
   internet-search stage. Citation-graph expansion (forward via "Cited by" and backward via
   reference lists) of these 10 should yield most of the 12-25 new papers the task targets.

2. **Prioritize finding cortical and invertebrate DS-with-morphology papers.** This is the largest
   coverage gap and the highest-leverage extension target.

3. **In the synthesis answer, structure the morphology-variable taxonomy around five axes identified
   here**: (a) electrotonic spatial grain (compartment size vs λ), (b) asymmetric vs symmetric
   arbors, (c) active conductance density and gradient, (d) input spatial layout on dendrites, (e)
   SAC-tiling density on the contact plexus.

4. **In the recommendations section of the synthesis**, propose at minimum: a passive-only Rall
   sweep, a morphology-only sweep with biophysics fixed at Schachter recipe, an input-rearrangement
   sweep on a fixed morphology, and a SAC-density sweep on the t0024 testbed.

5. **Treat [PolegPolsky2026]'s ML-discovered primitives as a hypothesis library** — each primitive
   (delay lines, coincidence detection, NMDA gating) becomes a candidate mechanism the morphology
   sweep should test.

## Paper Index

### [Schachter2010]

* **Title**: Dendritic Spikes Amplify the Synaptic Signal to Enhance Detection of Motion in a
  Simulation of the Direction-Selective Ganglion Cell
* **Authors**: Schachter, M.J., Oesch, N., Smith, R.G., Taylor, W.R.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000899`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1371_journal.pcbi.1000899/`
* **Categories**: `direction-selectivity`, `compartmental-modeling`, `dendritic-computation`,
  `retinal-ganglion-cell`
* **Relevance**: Canonical NEURON DSGC compartmental model. Establishes dendritic-spike
  amplification (PSP DSI 0.2 → spike DSI 0.8), inhibition initiation/propagation dissociation, and
  intrinsic geometric DSI. Baseline biophysics recipe for any morphology sweep.

### [Jain2020]

* **Title**: The functional organization of excitation and inhibition in the dendrites of mouse
  direction-selective ganglion cells
* **Authors**: Jain, V., Murphy-Baum, B.L., deRosenroll, G., Sethuramanujam, S., Delsey, M.,
  Delaney, K.R., Awatramani, G.B.
* **Year**: 2020
* **DOI**: `10.7554/eLife.52949`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.7554_eLife.52949/`
* **Categories**: `direction-selectivity`, `compartmental-modeling`, `dendritic-computation`,
  `retinal-ganglion-cell`, `synaptic-integration`
* **Relevance**: Establishes the 5-10 µm spatial grain of DS subunits, λ ≈ 5.3 µm cable constant,
  NMDA voltage-threshold nonlinearity. Shows DS is local, not global — directly motivates
  fine-grained morphology sweeps.

### [Morrie2018]

* **Title**: A Dense Starburst Plexus Is Critical for Generating Direction Selectivity
* **Authors**: Morrie, R.D., Feller, M.B.
* **Year**: 2018
* **DOI**: `10.1016/j.cub.2018.03.001`
* **Asset**: `tasks/t0013_resolve_morphology_provenance/assets/paper/10.1016_j.cub.2018.03.001/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `dendritic-computation`
* **Relevance**: SAC tiling density itself is a morphology variable in DS. Reducing SAC density
  abolishes DS even when individual SAC and DSGC morphology are intact. Argues for input-spatial-
  layout sweep alongside dendrite-geometry sweep.

### [PolegPolsky2026]

* **Title**: Machine learning discovers numerous new computational principles underlying direction
  selectivity in the retina
* **Authors**: Poleg-Polsky, A.
* **Year**: 2026
* **DOI**: `10.1038/s41467-026-70288-4`
* **Asset**: `tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/`
* **Categories**: `direction-selectivity`, `compartmental-modeling`, `retinal-ganglion-cell`,
  `dendritic-computation`, `synaptic-integration`
* **Relevance**: Largest morphology+input sweep in the corpus (352-segment DSGC, varied bipolar
  offsets, kinetics, dendritic biophysics). Discovers that classical SAC inhibition is sufficient
  but not necessary for DS — establishes a hypothesis library of alternative mechanisms.

### [deRosenroll2026]

* **Title**: Uncovering the "hidden" synaptic microarchitecture of the retinal direction selective
  circuit
* **Authors**: deRosenroll, G., Sethuramanujam, S., Awatramani, G.B.
* **Year**: 2026
* **DOI**: `10.1016/j.celrep.2025.116833`
* **Asset**: `tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1016_j.celrep.2025.116833/`
* **Categories**: `direction-selectivity`, `compartmental-modeling`, `retinal-ganglion-cell`,
  `dendritic-computation`, `synaptic-integration`
* **Relevance**: Network model with explicit anatomical wiring shows local ACh perturbations that
  preserve global E/I but uncouple local DS subunits — argues for subcellular spatial alignment of
  inputs as a primary morphology-related variable. (PDF download failed; summary based on verbatim
  abstract and companion code.)

### [Taylor2002]

* **Title**: Diverse synaptic mechanisms generate direction selectivity in the rabbit retina
* **Authors**: Taylor, W.R., Vaney, D.I.
* **Year**: 2002
* **DOI**: `10.1523/JNEUROSCI.22-17-07712.2002`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_JNEUROSCI.22-17-07712.2002/`
* **Categories**: `direction-selectivity`, `compartmental-modeling`, `retinal-ganglion-cell`,
  `synaptic-integration`
* **Relevance**: Identifies three distinct synaptic asymmetries (presynaptic excitation, presynaptic
  inhibition, postsynaptic spatial offset of ~160 µm) and shows ON vs OFF arbor use different
  combinations — supports sublamina-morphology-dependent mechanism choice.

### [Hanson2019]

* **Title**: Retinal direction selectivity in the absence of asymmetric starburst amacrine cell
  responses
* **Authors**: Hanson, L., Sethuramanujam, S., deRosenroll, G., Jain, V., Awatramani, G.B.
* **Year**: 2019
* **DOI**: `10.7554/eLife.42392`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.7554_eLife.42392/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`
* **Relevance**: Empirical demonstration that DSGCs retain DS even when SAC GABA release is
  symmetric. Falsifies the strong claim that asymmetric SAC inhibition is the sole DS mechanism;
  motivates morphology-focused alternative mechanisms.

### [Rall1967]

* **Title**: Distinguishing theoretical synaptic potentials computed for different soma-dendritic
  distributions of synaptic input
* **Authors**: Rall, W.
* **Year**: 1967
* **DOI**: `10.1152/jn.1967.30.5.1138`
* **Asset**: `tasks/t0015_literature_survey_cable_theory/assets/paper/10.1152_jn.1967.30.5.1138/`
* **Categories**: `compartmental-modeling`, `dendritic-computation`, `synaptic-integration`
* **Relevance**: Foundational cable-theory derivation showing that on a *passive* dendrite,
  sequenced inputs arriving soma-ward vs distally produce direction-dependent EPSPs. The geometric
  origin of dendritic DS, on which all later active-mechanism work rests. (PDF download failed;
  summary based on prior reading and abstract.)

### [KochPoggio1982]

* **Title**: Retinal ganglion cells: a functional interpretation of dendritic morphology
* **Authors**: Koch, C., Poggio, T., Torre, V.
* **Year**: 1982
* **DOI**: `10.1098/rstb.1982.0084`
* **Asset**: `tasks/t0015_literature_survey_cable_theory/assets/paper/10.1098_rstb.1982.0084/`
* **Categories**: `compartmental-modeling`, `dendritic-computation`, `retinal-ganglion-cell`
* **Relevance**: Extends Rall to retinal ganglion-cell branching morphology and shows that
  asymmetric branching alone produces measurable directional bias in voltage transfer to soma.
  Direct theoretical support for the "morphology variable as causal" claim. (PDF download failed;
  summary based on prior reading and abstract.)

### [LondonHausser2005]

* **Title**: Dendritic Computation
* **Authors**: London, M., Häusser, M.
* **Year**: 2005
* **DOI**: `10.1146/annurev.neuro.28.061604.135703`
* **Asset**:
  `tasks/t0016_literature_survey_dendritic_computation/assets/paper/10.1146_annurev.neuro.28.061604.135703/`
* **Categories**: `dendritic-computation`, `compartmental-modeling`, `synaptic-integration`
* **Relevance**: Authoritative review identifying branch order, diameter, distance-from-soma, and
  synaptic spatial layout as the morphology variables that most strongly affect dendritic
  computation, including DS. Provides the variable taxonomy the synthesis section will use. (PDF
  download failed; summary based on prior reading and abstract.)
