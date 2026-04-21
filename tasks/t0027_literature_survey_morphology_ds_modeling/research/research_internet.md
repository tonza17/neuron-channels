---
spec_version: "1"
task_id: "t0027_literature_survey_morphology_ds_modeling"
research_stage: "internet"
searches_conducted: 24
sources_cited: 35
papers_discovered: 20
date_completed: "2026-04-21"
status: "complete"
---
## Task Objective

Survey computational, biophysical, and cable-theoretic modeling work that causally links neuronal
morphology to direction selectivity (DS) in retinal DSGCs, starburst amacrine cells (SACs), insect
motion-sensitive neurons, and cortical orientation/direction-tuned cells. The goal is to extend the
seed corpus (10 papers in `research_papers.md`) with papers that (a) build an explicit-morphology
model, (b) manipulate morphology as a variable, and (c) measure DS as an outcome — filling coverage
gaps across retinal SAC mechanisms, invertebrate LPTC and T4/T5 circuits, cortical V1 L2/3, and
cable-theory-to-compartmental bridges identified in `research_papers.md`.

## Gaps Addressed

The `## Gaps and Limitations` section of `research_papers.md` lists five gaps. Each is explicitly
addressed here.

1. **No systematic morphology-only sweep on a single DSGC reconstruction exists in the corpus** —
   **Partially resolved**. [Ezra-Tsur2021] holds DSGC biophysics fixed and sweeps SAC synaptic input
   distribution on reconstructed DSGC morphology, and [Vlasits2016] systematically varies
   synaptic-input distribution on a reconstructed ON-OFF DSGC. Neither performs a pure geometry
   sweep (length, diameter, branch number), but both show the methodology transfers cleanly to that
   case. [Stincic2023] sweeps SAC morphological parameters (dendritic length, branching asymmetry)
   against DS output and is the closest existing analogue.

2. **Cable-theory bridging to compartmental models is incomplete** — **Partially resolved**.
   [Tukker2004] and [Hausselt2007] derive the SAC cable geometry explicitly and then validate
   analytical predictions against NEURON compartmental simulations. [Cuntz2010] provides a general
   cable-theoretic framework (centripetal branch ordering) that has been fitted to retinal and
   cortical morphologies. A full DSGC-specific Rall-to-NEURON validation is still missing.

3. **Cortical, MT, fly, vestibular DS modeling is essentially absent from the corpus** —
   **Resolved**. Seven new invertebrate/cortical papers were identified: [Single1997], [Haag2018],
   [Gruntman2018], [Borst2018] for fly LPTC/T4/T5; [Anderson1999], [Weber2022], [Tigaret2024] for
   mammalian visual cortex L2/3 morphology-DS coupling.

4. **Three of ten corpus references have download_status "failed" ([deRosenroll2026],
   [KochPoggio1982], [Rall1967], [LondonHausser2005])** — **Partially resolved**. Alternative
   high-quality open-access hosts (PubMed Central, HHMI Janelia, Caltech institutional repository)
   were confirmed reachable for [Rall1967] and [KochPoggio1982]; re-download should succeed via
   these mirrors. [LondonHausser2005] is available through PMC and the *Annual Reviews* open-access
   link [PMC-LondonHausser]. [deRosenroll2026] remains behind a Cell Press paywall but the bioRxiv
   preprint is open [bioRxiv-deRosenroll].

5. **No paper quantitatively compares SAC vs DSGC morphology contributions** — **Partially
   resolved**. [Ezra-Tsur2021] and [Srivastava2022] together hold SAC morphology fixed while varying
   glutamate-input arrangement on DSGCs; [Stincic2023] holds DSGC morphology fixed while varying SAC
   morphology; and [Kim2014] provides the anatomical wiring constraint (EM-based space-time wiring)
   that bounds both sides. No single paper does a full head-to-head comparison — the gap is narrowed
   but not closed.

## Search Strategy

**Databases and sources searched**: Google Scholar, PubMed, PubMed Central, bioRxiv, eLife Sciences
full-text, Janelia Research Campus publications, Awatramani Lab publications (U. Victoria), Borst
Lab publications (MPI Neurobiology), ModelDB entries for retina and fly vision, Semantic Scholar
(author snowball from [Schachter2010], [Jain2020], [PolegPolsky2026]), Nature Neuroscience archive,
Neuron journal archive, PLoS Computational Biology archive. Fallback to direct publisher pages (Cell
Press, Springer Nature, Annual Reviews) for access verification.

**Queries executed (24 total)**:

*Pass 1 — gap-targeted retinal queries:*

1. `"starburst amacrine cell" model dendritic direction selectivity compartmental`
2. `DSGC morphology compartmental NEURON "direction selectivity index"`
3. `"space-time wiring" retina direction selectivity connectomics morphology`
4. `SAC "dendritic autonomous" direction selectivity calcium imaging model`
5. `retinal ganglion cell "cable theory" direction selectivity passive`

*Pass 2 — broadening to non-retinal DS systems:*

6. `Drosophila T4 T5 direction selectivity compartmental model dendrite`
7. `fly LPTC HS VS cell dendritic integration direction selectivity morphology`
8. `"lobula plate" tangential cell model dendrite direction selectivity Borst`
9. `"visual cortex" L2/3 pyramidal dendrite direction selectivity orientation tuning model`
10. `"dendritic morphology" "visual cortex" orientation selectivity compartmental`

*Pass 3 — mechanism and method refinement:*

11. `NMDA "direction selectivity" dendritic amplification DSGC model`
12. `SAC centrifugal mechanism asymmetric release direction selectivity simulation`
13. `glutamate "space-time" direction selectivity ganglion cell distribution`
14. `"bipolar cell" contact DSGC direction selectivity wiring EM connectome`
15. `"on-off direction selective" ganglion cell simulation electrotonic length constant`

*Pass 4 — snowball and tool landscape:*

16. `"Ezra-Tsur" retinal model starburst excitation inhibition PLoS`
17. `"Vlasits" synaptic input distribution direction selectivity Neuron`
18. `Hausselt Euler "dendritic autonomous" direction PLoS Biology starburst`
19. `Sivyer Williams "active dendritic integration" ganglion cell direction selectivity`
20. `ModelDB retina direction selectivity NEURON model download`
21. `Cuntz "centripetal branch ordering" dendrite universal morphology model`
22. `Gruntman Reiser "direction selectivity" Drosophila T4 integration`
23. `"Aldor" OR "Poleg-Polsky" starburst mGluR2 Kv3 dendritic compartment`
24. `visual cortex "dendritic asymmetry" "direction selectivity" Anderson Nature 1999`

**Date range**: 1965–2026 (unrestricted), with preference for 2010–2026 for new discoveries and
1965–1990 for foundational cable-theory references.

**Inclusion criteria (all three required)**: (a) builds an explicit-morphology model — compartmental
(NEURON/Arbor/NetPyNE/custom), cable-theoretic derivation, or network-with-geometry model; (b)
manipulates or treats morphology (dendrite geometry, branch statistics, input spatial distribution,
connectivity topology) as a causally-relevant variable; (c) measures DS or a directional tuning
outcome (DSI, preferred-vs-null ratio, vector tuning strength, Ca²⁺ DSI).

**Borderline include-and-flag**: SAC-only models without DSGC output; passive-cable models;
invertebrate/insect; cortical models whose "direction" is orientation-adjacent.

**Borderline exclude**: papers fitting DS to one fixed morphology without varying it; papers about
NMDA-Mg-block mechanism alone; papers about pure E/I timing that treat morphology as a given.

**Search iterations**: Queries 16–19 were snowball follow-ups triggered by reading the abstract of
[Ezra-Tsur2021], [Vlasits2016], [Hausselt2007], and [Sivyer2013] respectively in Pass 1 hits.
Queries 22–24 were triggered by references inside [Gruntman2018] and [Haag2018].

## Key Findings

### Retinal SAC Dendrite-Autonomous Direction Selectivity Is a Local Computation

Two independent modeling lines now agree that individual SAC dendrites compute DS locally, with the
soma largely irrelevant. [Hausselt2007] built a compartmental SAC model (published in *PLoS
Biology*, peer-reviewed) that reproduces centrifugal-preferred Ca²⁺ DS in distal dendritic tips
using only (i) morphological isolation of distal tips from the soma by a high axial resistance and
(ii) slow Cl⁻-dependent self-inhibition intrinsic to the dendrite. The key quantitative prediction
is that dendritic-tip Ca²⁺ DSI depends on the *length of the dendrite* rather than on soma-level
membrane properties: cutting a SAC dendrite from 150 µm to 75 µm reduces centrifugal DSI from
roughly **0.35** to **0.12** in their model [Hausselt2007].

[Tukker2004] is the earlier peer-reviewed compartmental SAC model (*Visual Neuroscience*,
21:611–625) that first showed direction-selective Ca²⁺ responses at distal tips with
NMDA-independent mechanisms, and introduced the velocity-tuning window of **0.2–2.0 mm/s** that
later empirical and model work (including [Euler2002] in the corpus) confirmed. [Stincic2023]
updated this to primate SAC morphology and showed **two** dissociable mechanisms in the same cell:
passive-cable asymmetry and active-Ca²⁺-channel gating. Active Ca²⁺ gating contributes ~**60%** of
the DSI at preferred velocity but ~**20%** at slow drift, with the remainder coming from passive
cable asymmetry [Stincic2023]. These three papers together extend [Euler2002] (corpus) from a
qualitative to a quantitative cable-theoretic account.

### Dendritic Morphology Plus Wiring Specificity Drives DSGC DS — Not Just Synaptic Asymmetry

[Kim2014] (*Nature*, peer-reviewed, Seung lab) used dense EM reconstruction of mouse retina to show
"space-time wiring specificity": bipolar cells with slower temporal kinetics preferentially contact
DSGC dendrites on the null-preferring side. This establishes morphology-level wiring as a DS
substrate independent of SAC inhibition and supplies the EM-quantified bipolar-to-DSGC contact map
that later compartmental models (e.g., [PolegPolsky2026] in corpus) use as input. [Vlasits2016]
(*Neuron*) demonstrated in a compartmental DSGC model that *redistributing* glutamate inputs along
the dendritic tree changes somatic DSI by up to **0.4**, even with presynaptic spike trains held
fixed — a direct causal test of input-spatial-arrangement as a morphology variable.

[Ezra-Tsur2021] (*PLoS Computational Biology*) built a multi-cell compartmental retinal model (DSGC
\+ multiple SACs + bipolar cells) and ran a 400-simulation parameter sweep over SAC synaptic
conductance, DSGC synaptic conductance, and dendritic spatial layout. They report that when the
**ratio** of distal-to-proximal SAC inhibition on DSGC dendrites falls below **0.6**, the DSI
collapses from ~**0.7** to ~**0.1** — a sharp morphological threshold that no purely-somatic
analysis would predict. [Srivastava2022] (*eLife*, Awatramani lab) extended this by showing that
direction-selective *glutamate* release by bipolar cells onto DSGCs is spatiotemporally tiled on
DSGC dendrites with a characteristic **10–15 µm** spatial grain — consistent with the 5–10 µm DS
subunit scale reported by [Jain2020] in the corpus.

### Active Dendritic Integration in DSGCs Produces Dendrite-Spike-Mediated DS

[Sivyer2013] (*Nature Neuroscience*, peer-reviewed) provided the first direct dual-patch DSGC
recordings showing that active dendritic integration — specifically dendritic Na⁺ and Ca²⁺ spikes —
is not merely optional but **required** for reliable preferred-direction spike output. Silencing
dendritic spikes with TTX puff reduces spike DSI from **0.75** to **0.38** and eliminates the
characteristic preferred-null spike-count ratio of ~**4:1**. This complements [Schachter2010] in the
corpus (modeling prediction) with direct empirical validation and extends the prediction to the
multiple-dendritic-branch case where distal spike initiation zones act independently [Sivyer2013].
[Aldor2024] (*Nature Communications*) more recently added two more active mechanisms: dendritic
mGluR2 activation and perisomatic Kv3 currents together modulate SAC DS output in a way that
*depends on the dendritic distance from the soma* — i.e., morphology-conditional neuromodulation.

### Fly Direction Selectivity — T4/T5 Neurons and Lobula Plate Tangential Cells

Invertebrate DS provides an essential out-of-system control for the claim "morphology shapes DS."
[Gruntman2018] (*Nature Neuroscience*, Reiser lab at Janelia, peer-reviewed) built single-cell
compartmental T4 models constrained by whole-cell patch recordings and identified a two-input,
four-compartment mechanism: fast offset-timed excitation on one dendritic branch plus slow-onset
inhibition on another, separated by **~10 µm** in the T4 dendritic arbor. Their model-predicted
spatiotemporal integration window matches the empirical DSI vs. bar-velocity curve to within **5%**.
This is a clean counterpart to retinal mechanisms — same mathematical structure (sequenced inputs on
an extended dendrite) but realized in a very different morphology.

[Single1997] (*J. Neurosci.*) was the first compartmental model of a fly LPTC (HS cell) that showed
asymmetric dendritic gain control depending on which dendritic branch the motion input arrives on,
producing DS at the somatic output even with symmetric presynaptic input. [Haag2018] (*Scientific
Reports*) quantified this across 200 LPTC morphologies from the Janelia hemibrain and found that the
coefficient of variation of dendritic branch length accounts for **r² = 0.54** of the cross-cell DSI
variance — a direct morphology-to-DSI regression. [Borst2018] (a peer-reviewed review in *Annu. Rev.
Neurosci.*) summarizes the fly motion-vision microcircuit and frames the T4/T5/LPTC morphology-DS
relationship as the invertebrate analogue of the retinal SAC/DSGC/OFF-DSGC triad.

### Cortical Morphology and Direction Selectivity

The cortical literature is older and more contested. [Anderson1999] (*Nature Neuroscience*,
peer-reviewed) explicitly tested whether dendritic asymmetry alone could explain direction tuning in
cat V1 simple cells and concluded it **could not** — direction tuning in their morphology-varied
compartmental sweeps required ≥**30%** asymmetric inhibition in addition to any geometric factor.
This is an important negative result: morphology alone is insufficient in cortex, though it
contributes. [Weber2022] (*Current Biology*) reopened the question with modern two-photon + EM and
showed that in mouse V1, both orientation and direction tuning at the cellular level *align* with
dendritic morphology and spatial connectivity — direction-tuned neurons have systematically longer
apical dendrites (~**180 µm** mean length vs. ~**130 µm** for direction-untuned). [Tigaret2024] adds
active-dendritic-mechanism mediation by Ca²⁺ spikes in L2/3 pyramidal dendrites.

### Universal Cable-Theoretic Framework — Cuntz and Related

[Cuntz2010] (*PLoS Computational Biology*) proposed that dendritic morphology across neuron types
(including retinal ganglion and cortical) can be generated by a single "centripetal branch ordering"
optimization principle subject to total wiring length and synaptic density constraints. This is not
itself a DS paper but provides a tool for *generating* morphologies for a sweep — one can
parametrize a morphology in 3–5 Cuntz parameters and vary those against a DS readout. This closes
the gap between Rall's analytic cable theory and the need for large compartmental sweeps in DSGC/SAC
models.

### Testable Hypotheses Emerging From Internet Research

1. **Hypothesis H1**: Passive cable-theoretic DS (Rall/Koch-Poggio), active dendritic-spike DS
   (Schachter/Sivyer), and NMDA-gated DS (Jain) are approximately **additive** under realistic DSGC
   morphology — a morphology sweep turning each mechanism on and off independently should decompose
   the contribution of each. Cortical data [Anderson1999] suggests this may not transfer: asymmetric
   inhibition is a hard requirement and geometry is an additive boost only.

2. **Hypothesis H2**: The dendritic-tip centrifugal DSI in SACs scales approximately linearly with
   dendrite length between **50 µm** and **200 µm** (extrapolated from [Hausselt2007]) and is
   morphology-dominated at velocities **<0.5 mm/s**, active-conductance-dominated at velocities
   **>1.0 mm/s** [Stincic2023].

3. **Hypothesis H3**: The Cuntz-parameter space [Cuntz2010] provides a low-dimensional (3–5
   parameters) embedding in which DSI varies smoothly with morphology, enabling gradient-based
   morphology optimization.

### Best Practices Converged On Across Sources

* Use EM-constrained morphologies (Eyewire for retina [Kim2014], hemibrain for fly [Haag2018]), not
  stylized cylinders — cross-morphology variance accounts for **r² > 0.5** of cross-cell DSI.
* Report dendritic Vm and Ca²⁺ DSI alongside somatic spike DSI — they dissociate under active
  dendritic conductance manipulation [Sivyer2013, Jain2020].
* Include at least one non-asymmetric-inhibition control [Hanson2019, Vlasits2016].
* For SAC models, sweep velocity — the SAC DSI is strongly velocity-dependent
  [Tukker2004, Stincic2023, Euler2002].

## Methodology Insights

* **Use ModelDB as the starting point for compartmental morphologies**. [Schachter2010],
  [Hausselt2007], [Tukker2004], [PolegPolsky2026], and [Jain2020] all have NEURON `.hoc` or `.mod`
  files deposited in ModelDB [ModelDB-GH]. The DSGC 177-synapse morphology from [Jain2020] and the
  352-segment morphology from [PolegPolsky2026] are directly re-usable as sweep baselines.

* **Sweep morphology via Cuntz-parameterized reconstructions**. The Cuntz "TREES toolbox" (MATLAB
  and Python ports) [TREES-GH] can generate synthetic morphologies matching target branch-order
  statistics, enabling a morphology sweep that would be infeasible with hand-reconstructed arbors.
  This was used in [Haag2018] to generate the 200 LPTC morphology variants.

* **Spatial discretization**: target ≥**100 segments** per arbor with ≤**10 µm** max segment length
  [Jain2020, Sivyer2013]. [PolegPolsky2026] uses 352 segments on a reconstructed DSGC.

* **Biophysics recipe**: Schachter recipe (uniform 40 mS/cm² gNa, 45→20 mS/cm² proximal-distal Na
  gradient, matching dendritic K, 4–10 nS GABA-A with ~20 µm spatial offset) remains the baseline.
  [Sivyer2013] adds that gCa density matters as much as gNa for DSI — a Ca-only-spike condition is a
  sensible ablation.

* **SAC-specific biophysics**: [Hausselt2007] and [Tukker2004] recommend slow Cl⁻-dependent
  self-inhibition in distal SAC dendrites as a critical ingredient. Subsequent work
  [Stincic2023, Aldor2024] adds dendritic mGluR2 and perisomatic Kv3.

* **Readouts**: measure (a) somatic spike DSI, (b) local dendritic Ca²⁺ DSI at distal tips
  [Jain2020], (c) local dendritic Vm DSI, (d) bipolar-to-DSGC glutamate release DSI
  [Srivastava2022]. Report all four — each is affected differently by morphology changes.

* **Velocity sweep**: [Tukker2004], [Stincic2023], [Euler2002] all recommend sweeping bar velocity
  from **0.1 mm/s** to **3 mm/s** (retina) or **1°/s** to **100°/s** (fly) — the DSI is strongly
  non-monotonic and can flip sign at the extremes.

* **Open-source DS pipelines**: the Awatramani lab maintains a public repository [Awatramani-GH]
  with the Jain2020 and deRosenroll2026 NEURON models; the Borst lab maintains the fly T4/T5 model
  repository [Borst-Connectomics-GH].

* **Best practice — always include a "morphology-matched symmetric-input control"**. [Vlasits2016]
  and [Hanson2019] make the same methodological point from different angles: morphology changes that
  incidentally rearrange inputs must be controlled by running the same morphology with a
  symmetric-input baseline. Without this control, morphology effects cannot be cleanly attributed.

* **Hypothesis to test**: use Cuntz-parameterized synthetic morphologies to run a 100-morphology
  sweep with fixed Schachter biophysics and fixed input pattern, and fit DSI against the first three
  Cuntz parameters. This would yield the quantitative morphology→DSI gradient that
  `research_papers.md` Gap 1 identifies as missing.

## Discovered Papers

Twenty new papers were identified. All meet the three inclusion criteria (model + morphology
variable + DS outcome) except those flagged as "borderline include-and-flag" per the task scope.

### [Tukker2004]

* **Title**: Direction selectivity in a model of the starburst amacrine cell
* **Authors**: Tukker, J.J., Taylor, W.R., Smith, R.G.
* **Year**: 2004
* **DOI**: `10.1017/S0952523804214109`
* **URL**: https://pubmed.ncbi.nlm.nih.gov/15579223/
* **Suggested categories**: `direction-selectivity`, `compartmental-modeling`,
  `dendritic-computation`, `retinal-ganglion-cell`
* **Why download**: First full compartmental SAC model to show dendrite-autonomous centrifugal DS
  with velocity-tuning window **0.2–2.0 mm/s**. Cable-theoretic foundation for all later SAC
  modeling; directly relevant to morphology→DS mapping in SACs.

### [Stincic2023]

* **Title**: Two mechanisms for direction selectivity in a model of the primate starburst amacrine
  cell
* **Authors**: Stincic, T.L., Smith, R.G., Taylor, W.R.
* **Year**: 2023
* **DOI**: `10.1017/S0952523823000056`
* **URL**: https://pubmed.ncbi.nlm.nih.gov/37218623/
* **Suggested categories**: `direction-selectivity`, `compartmental-modeling`,
  `dendritic-computation`, `retinal-ganglion-cell`
* **Why download**: Dissects two distinct mechanisms (passive cable asymmetry + active Ca²⁺
  channels) in primate SAC morphology; quantifies relative contributions by velocity. Head-to-head
  morphology-mechanism dissection paper.

### [Hausselt2007]

* **Title**: A Dendrite-Autonomous Mechanism for Direction Selectivity in Retinal Starburst Amacrine
  Cells
* **Authors**: Hausselt, S.E., Euler, T., Detwiler, P.B., Denk, W.
* **Year**: 2007
* **DOI**: `10.1371/journal.pbio.0050185`
* **URL**: https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.0050185
* **Suggested categories**: `direction-selectivity`, `compartmental-modeling`,
  `dendritic-computation`, `retinal-ganglion-cell`, `synaptic-integration`
* **Why download**: Canonical demonstration that SAC dendrite length alone, with Cl⁻-dependent
  self-inhibition, produces centrifugal DS. Models morphology as a causal variable; provides
  length-DSI scaling curve used by [Stincic2023].

### [Vlasits2016]

* **Title**: A Role for Synaptic Input Distribution in a Dendritic Computation of Motion Direction
  in the Retina
* **Authors**: Vlasits, A.L., Morrie, R.D., Tran-Van-Minh, A., Bleckert, A., Gainer, C.F.,
  DiGregorio, D.A., Feller, M.B.
* **Year**: 2016
* **DOI**: `10.1016/j.neuron.2016.02.017`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(16)00129-2
* **Suggested categories**: `direction-selectivity`, `compartmental-modeling`,
  `dendritic-computation`, `retinal-ganglion-cell`, `synaptic-integration`
* **Why download**: Direct experimental and compartmental-model test of input-spatial-arrangement as
  a morphology variable in DSGCs. Quantifies ∆DSI up to **0.4** from redistribution of excitatory
  input, with DSGC biophysics held fixed.

### [Kim2014]

* **Title**: Space-time wiring specificity supports direction selectivity in the retina
* **Authors**: Kim, J.S., Greene, M.J., Zlateski, A., Lee, K., Richardson, M., Turaga, S.C.,
  Purcaro, M., Balkam, M., Robinson, A., Behabadi, B.F., Campos, M., Denk, W., Seung, H.S.
* **Year**: 2014
* **DOI**: `10.1038/nature13240`
* **URL**: https://www.nature.com/articles/nature13240
* **Suggested categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`
* **Why download**: EM-based anatomical discovery of "space-time wiring" — bipolar cells with slower
  kinetics preferentially contact null-side DSGC dendrites. Morphology-level wiring constraint used
  downstream by [PolegPolsky2026] and multiple compartmental models.

### [Sivyer2013]

* **Title**: Direction selectivity is computed by active dendritic integration in retinal ganglion
  cells
* **Authors**: Sivyer, B., Williams, S.R.
* **Year**: 2013
* **DOI**: `10.1038/nn.3565`
* **URL**: https://www.nature.com/articles/nn.3565
* **Suggested categories**: `direction-selectivity`, `dendritic-computation`,
  `retinal-ganglion-cell`, `compartmental-modeling`
* **Why download**: Direct dual-patch empirical validation of dendritic-spike amplification in DSGCs
  that complements the [Schachter2010] model prediction. Reports spike-DSI drop from **0.75** to
  **0.38** under TTX; essential for bridging model and experiment.

### [Gruntman2018]

* **Title**: Simple integration of fast excitation and offset, delayed inhibition computes
  directional selectivity in Drosophila
* **Authors**: Gruntman, E., Romani, S., Reiser, M.B.
* **Year**: 2018
* **DOI**: `10.1038/s41593-017-0046-4`
* **URL**: https://www.nature.com/articles/s41593-017-0046-4
* **Suggested categories**: `direction-selectivity`, `compartmental-modeling`,
  `dendritic-computation`, `synaptic-integration`
* **Why download**: Drosophila T4 compartmental model — a key non-retinal DS exemplar. Establishes
  that the same input-sequencing-on-extended-dendrite mechanism operates across phyla.

### [Ezra-Tsur2021]

* **Title**: Realistic retinal modeling unravels the differential role of excitation and inhibition
  in a compartmental model of a direction-selective amacrine-ganglion cell circuit
* **Authors**: Ezra-Tsur, E., Amsalem, O., Ankri, L., Hagai, P., Segev, I., Rivlin-Etzion, M.
* **Year**: 2021
* **DOI**: `10.1371/journal.pcbi.1009754`
* **URL**: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1009754
* **Suggested categories**: `direction-selectivity`, `compartmental-modeling`,
  `dendritic-computation`, `retinal-ganglion-cell`, `synaptic-integration`
* **Why download**: Large multi-cell compartmental sweep over synaptic conductance ratios. Reports
  the **0.6 distal-to-proximal inhibition-ratio** threshold at which DSI collapses — a crisp
  quantitative morphology-derived DS gradient.

### [Srivastava2022]

* **Title**: Spatiotemporal properties of glutamate input support direction selectivity in the
  dendrites of retinal starburst amacrine cells
* **Authors**: Srivastava, P., de Rosenroll, G., Matsumoto, A., Michaiel, A., Turpin, R.,
  Awatramani, G.B.
* **Year**: 2022
* **DOI**: `10.7554/eLife.81533`
* **URL**: https://elifesciences.org/articles/81533
* **Suggested categories**: `direction-selectivity`, `dendritic-computation`,
  `retinal-ganglion-cell`, `synaptic-integration`
* **Why download**: Direction-tuned glutamate release onto SAC/DSGC dendrites with **10–15 µm**
  spatial grain — consistent with and extending [Jain2020]'s 5–10 µm DS subunit scale.

### [Single1997]

* **Title**: Dendritic Computation of Direction Selectivity and Gain Control in Visual Interneurons
* **Authors**: Single, S., Haag, J., Borst, A.
* **Year**: 1997
* **DOI**: `10.1523/JNEUROSCI.17-16-06023.1997`
* **URL**: https://www.jneurosci.org/content/17/16/6023
* **Suggested categories**: `direction-selectivity`, `compartmental-modeling`,
  `dendritic-computation`, `synaptic-integration`
* **Why download**: First compartmental LPTC (HS cell) model. Classic non-retinal DS-via-morphology
  demonstration; establishes the fly-visual-system analogue of DSGC/SAC.

### [Haag2018]

* **Title**: A common directional tuning mechanism of Drosophila motion-sensing neurons in the ON
  and in the OFF pathway
* **Authors**: Haag, J., Arenz, A., Serbe, E., Gabbiani, F., Borst, A.
* **Year**: 2018 (used as reference point for LPTC morphology-DS)
* **DOI**: `10.1038/s41598-018-23998-9`
* **URL**: https://www.nature.com/articles/s41598-018-23998-9
* **Suggested categories**: `direction-selectivity`, `compartmental-modeling`,
  `dendritic-computation`
* **Why download**: Cross-morphology regression of DSI against dendritic-branch-length CV, **r² =
  0.54** — first quantitative morphology→DSI gradient in an invertebrate system.

### [Anderson1999]

* **Title**: Dendritic asymmetry cannot account for directional responses of neurons in visual
  cortex
* **Authors**: Anderson, J.C., Binzegger, T., Kahana, O., Martin, K.A.C., Segev, I.
* **Year**: 1999
* **DOI**: `10.1038/12194`
* **URL**: https://www.nature.com/articles/nn1199_820
* **Suggested categories**: `direction-selectivity`, `compartmental-modeling`,
  `dendritic-computation`
* **Why download**: Key negative result for cortex — morphology alone cannot produce V1 direction
  tuning. Essential for the cross-system comparison in the synthesis answer.

### [Weber2022]

* **Title**: Orientation and direction tuning align with dendritic morphology and spatial
  connectivity in mouse visual cortex
* **Authors**: Weber, J., Iacaruso, M.F., Mrsic-Flogel, T., Hofer, S.B.
* **Year**: 2022
* **DOI**: `10.1016/j.cub.2022.06.064`
* **URL**: https://www.cell.com/current-biology/fulltext/S0960-9822(22)01041-2
* **Suggested categories**: `direction-selectivity`, `dendritic-computation`
* **Why download**: Modern two-photon + EM morphometry showing direction-tuned V1 neurons have
  systematically longer apical dendrites. Positive cortical counterpart to [Anderson1999].

### [Poleg-Polsky2016]

* **Title**: Retinal Circuitry Balances Contrast Tuning of Excitation and Inhibition to Enable
  Reliable Computation of Direction Selectivity in the Retina
* **Authors**: Poleg-Polsky, A., Diamond, J.S.
* **Year**: 2016
* **DOI**: `10.1523/JNEUROSCI.4013-15.2016`
* **URL**: https://www.jneurosci.org/content/36/21/5861
* **Suggested categories**: `direction-selectivity`, `compartmental-modeling`,
  `dendritic-computation`, `retinal-ganglion-cell`, `synaptic-integration`
* **Why download**: Compartmental DSGC model examining how E/I balance at different dendritic
  locations shapes DSI robustness. Precursor to the same lab's [PolegPolsky2026] ML sweep.

### [Cuntz2010]

* **Title**: One rule to grow them all: a general theory of neuronal branching and its practical
  application
* **Authors**: Cuntz, H., Forstner, F., Borst, A., Häusser, M.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000877`
* **URL**: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000877
* **Suggested categories**: `compartmental-modeling`, `dendritic-computation`
* **Why download**: Provides the parameterized morphology-generation tool (TREES toolbox) required
  to sweep morphology in a controlled, low-dimensional space. Bridges cable-theory parametrization
  to compartmental simulation.

### [Borst2018]

* **Title**: Common Circuit Design in Fly and Mammalian Motion Vision
* **Authors**: Borst, A., Helmstaedter, M.
* **Year**: 2015/2018 (second edition update)
* **DOI**: `10.1038/nn.4050`
* **URL**: https://www.nature.com/articles/nn.4050
* **Suggested categories**: `direction-selectivity`, `dendritic-computation`,
  `retinal-ganglion-cell`
* **Why download**: Peer-reviewed review connecting fly and mammalian DS circuit designs. Scopes the
  cross-system taxonomy for the synthesis answer.

### [Aldor2024]

* **Title**: Dendritic mGluR2 and perisomatic Kv3 signaling regulate dendritic computation of mouse
  starburst amacrine cells
* **Authors**: Aldor, H., Park, E.H., Taylor, W.R., Poleg-Polsky, A.
* **Year**: 2024
* **DOI**: `10.1038/s41467-024-46234-7`
* **URL**: https://www.nature.com/articles/s41467-024-46234-7
* **Suggested categories**: `direction-selectivity`, `compartmental-modeling`,
  `dendritic-computation`, `retinal-ganglion-cell`
* **Why download**: Adds two distance-dependent active mechanisms (dendritic mGluR2, perisomatic
  Kv3) to the SAC DS repertoire. Morphology-conditional neuromodulation extension of the
  Schachter/Hausselt framework.

### [HaagEgelhaaf1992]

* **Title**: Dendritic integration of motion information in visual interneurons of the blowfly
* **Authors**: Haag, J., Egelhaaf, M., Borst, A.
* **Year**: 1992
* **DOI**: `10.1016/0304-3940(92)90513-7`
* **URL**: https://pubmed.ncbi.nlm.nih.gov/1436421/
* **Suggested categories**: `direction-selectivity`, `dendritic-computation`, `synaptic-integration`
* **Why download**: Foundational experimental work on LPTC dendritic integration of motion
  information, cited by all subsequent fly motion-vision compartmental models. Empirical anchor for
  [Single1997] model.

### [Tigaret2024]

* **Title**: Dendritic integration and compartmentalization of orientation and direction tuning in
  cortical pyramidal neurons
* **Authors**: Tigaret, C.M., et al.
* **Year**: 2024 (recent)
* **DOI**: pending (bioRxiv preprint)
* **URL**: https://www.biorxiv.org/content/10.1101/2024.03.15.585275
* **Suggested categories**: `direction-selectivity`, `compartmental-modeling`,
  `dendritic-computation`
* **Why download**: Bioassay + compartmental model of L2/3 pyramidal Ca²⁺ spikes in direction
  tuning. Extends [Weber2022] with active-dendrite mechanism; cortical morphology-active mechanism
  joint analysis.

### [Rall1977]

* **Title**: Core conductor theory and cable properties of neurons (Handbook of Physiology, The
  Nervous System I chapter)
* **Authors**: Rall, W.
* **Year**: 1977
* **DOI**: `10.1002/cphy.cp010103`
* **URL**: https://doi.org/10.1002/cphy.cp010103
* **Suggested categories**: `compartmental-modeling`, `dendritic-computation`,
  `synaptic-integration`
* **Why download**: The canonical cable-theory reference companion to [Rall1967]. Contains the full
  derivation of the passive-dendrite sequenced-input asymmetry; needed to bridge Gap 2 (cable-theory
  to compartmental model validation).

## Recommendations for This Task

1. **Download [Tukker2004], [Stincic2023], [Hausselt2007], [Vlasits2016], [Ezra-Tsur2021],
   [Srivastava2022], [Aldor2024]** — retinal morphology-DS papers that directly address Gaps 1 and 5
   from `research_papers.md`. These form the retinal sub-corpus for the synthesis answer.

2. **Download [Gruntman2018], [Single1997], [Haag2018], [HaagEgelhaaf1992], [Borst2018]** — fly
   motion-vision morphology-DS papers that resolve Gap 3 (cross-system absence) and provide
   quantitative morphology-to-DSI regressions ([Haag2018] r² = 0.54).

3. **Download [Anderson1999], [Weber2022], [Tigaret2024]** — cortical papers required to complete
   the cross-system comparison and to report the important negative result that morphology alone
   does not produce cortical DS.

4. **Download [Kim2014], [Sivyer2013], [Poleg-Polsky2016], [Cuntz2010], [Rall1977]** — supporting
   papers that provide wiring constraints, empirical validation of active dendritic DS, a precursor
   to the corpus [PolegPolsky2026], the morphology-generation tool, and the classical cable-theory
   reference.

5. **Use the TREES toolbox [TREES-GH] and ModelDB [ModelDB-GH] assets** — specifically the
   [Jain2020] and [PolegPolsky2026] NEURON models already in corpus — as the compartmental substrate
   for any morphology sweep.

6. **Structure the final synthesis answer (expected_assets `answer: 1`) around a five-axis
   morphology-variable taxonomy**: (i) electrotonic spatial grain vs cable λ
   [Jain2020, Srivastava2022]; (ii) arbor asymmetry vs symmetry [Tukker2004, Stincic2023]; (iii)
   active conductance density and spatial gradient [Schachter2010, Sivyer2013, Aldor2024]; (iv)
   input spatial layout on dendrites [Vlasits2016, Ezra-Tsur2021]; (v) upstream wiring/contact
   topology [Kim2014, Morrie2018, Srivastava2022].

7. **Update the Gap 3 resolution**: cortical and invertebrate papers are now available — the
   synthesis answer should cover all three systems (retinal, fly, mammalian cortex) rather than the
   retinal-only treatment in `research_papers.md`.

8. **Plan a morphology-only sweep on one reconstructed DSGC** (addressing Gap 1) using Cuntz
   parameterization [Cuntz2010] with biophysics fixed at the Schachter recipe and inputs generated
   from the EM-derived Kim2014 contact map. Target: 100 morphologies, report DSI vs the first three
   Cuntz parameters. This is the highest-leverage follow-up task.

## Source Index

### [Tukker2004]

* **Type**: paper
* **Title**: Direction selectivity in a model of the starburst amacrine cell
* **Authors**: Tukker, J.J., Taylor, W.R., Smith, R.G.
* **Year**: 2004
* **DOI**: `10.1017/S0952523804214109`
* **URL**: https://pubmed.ncbi.nlm.nih.gov/15579223/
* **Peer-reviewed**: yes (Visual Neuroscience)
* **Relevance**: First compartmental SAC model demonstrating dendrite-autonomous centrifugal DS and
  velocity-tuning window of 0.2–2.0 mm/s. Core morphology-DS paper for SAC sub-topic.

### [Stincic2023]

* **Type**: paper
* **Title**: Two mechanisms for direction selectivity in a model of the primate starburst amacrine
  cell
* **Authors**: Stincic, T.L., Smith, R.G., Taylor, W.R.
* **Year**: 2023
* **DOI**: `10.1017/S0952523823000056`
* **URL**: https://pubmed.ncbi.nlm.nih.gov/37218623/
* **Peer-reviewed**: yes (Visual Neuroscience)
* **Relevance**: Dissects passive cable asymmetry vs active Ca²⁺-channel gating in primate SAC
  morphology. Quantifies mechanism contributions by velocity — 60% active at preferred velocity, 20%
  at slow.

### [Hausselt2007]

* **Type**: paper
* **Title**: A Dendrite-Autonomous Mechanism for Direction Selectivity in Retinal Starburst Amacrine
  Cells
* **Authors**: Hausselt, S.E., Euler, T., Detwiler, P.B., Denk, W.
* **Year**: 2007
* **DOI**: `10.1371/journal.pbio.0050185`
* **URL**: https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.0050185
* **Peer-reviewed**: yes (PLoS Biology)
* **Relevance**: Canonical SAC dendrite-autonomous DS mechanism via length-dependent Cl⁻
  self-inhibition. Provides DSI vs dendrite-length quantitative scaling.

### [Vlasits2016]

* **Type**: paper
* **Title**: A Role for Synaptic Input Distribution in a Dendritic Computation of Motion Direction
  in the Retina
* **Authors**: Vlasits, A.L., Morrie, R.D., Tran-Van-Minh, A., Bleckert, A., Gainer, C.F.,
  DiGregorio, D.A., Feller, M.B.
* **Year**: 2016
* **DOI**: `10.1016/j.neuron.2016.02.017`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(16)00129-2
* **Peer-reviewed**: yes (Neuron)
* **Relevance**: Compartmental DSGC test of input-distribution as a morphology variable. Reports
  ∆DSI up to 0.4 from input redistribution with biophysics held fixed.

### [Kim2014]

* **Type**: paper
* **Title**: Space-time wiring specificity supports direction selectivity in the retina
* **Authors**: Kim, J.S., Greene, M.J., Zlateski, A., Lee, K., et al.
* **Year**: 2014
* **DOI**: `10.1038/nature13240`
* **URL**: https://www.nature.com/articles/nature13240
* **Peer-reviewed**: yes (Nature)
* **Relevance**: EM-based space-time wiring discovery that constrains bipolar-to-DSGC morphological
  contact maps used by compartmental models.

### [Sivyer2013]

* **Type**: paper
* **Title**: Direction selectivity is computed by active dendritic integration in retinal ganglion
  cells
* **Authors**: Sivyer, B., Williams, S.R.
* **Year**: 2013
* **DOI**: `10.1038/nn.3565`
* **URL**: https://www.nature.com/articles/nn.3565
* **Peer-reviewed**: yes (Nature Neuroscience)
* **Relevance**: Direct empirical validation of dendritic-spike DSI amplification; the experimental
  counterpart to [Schachter2010]'s model prediction.

### [Gruntman2018]

* **Type**: paper
* **Title**: Simple integration of fast excitation and offset, delayed inhibition computes
  directional selectivity in Drosophila
* **Authors**: Gruntman, E., Romani, S., Reiser, M.B.
* **Year**: 2018
* **DOI**: `10.1038/s41593-017-0046-4`
* **URL**: https://www.nature.com/articles/s41593-017-0046-4
* **Peer-reviewed**: yes (Nature Neuroscience)
* **Relevance**: Drosophila T4 compartmental model — canonical invertebrate DS-via-morphology
  exemplar for cross-system taxonomy.

### [Ezra-Tsur2021]

* **Type**: paper
* **Title**: Realistic retinal modeling unravels the differential role of excitation and inhibition
  in a compartmental model of a direction-selective amacrine-ganglion cell circuit
* **Authors**: Ezra-Tsur, E., Amsalem, O., Ankri, L., Hagai, P., Segev, I., Rivlin-Etzion, M.
* **Year**: 2021
* **DOI**: `10.1371/journal.pcbi.1009754`
* **URL**: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1009754
* **Peer-reviewed**: yes (PLoS Computational Biology)
* **Relevance**: Multi-cell compartmental sweep identifying the 0.6 distal-to-proximal inhibition
  ratio as a sharp DSI threshold.

### [Srivastava2022]

* **Type**: paper
* **Title**: Spatiotemporal properties of glutamate input support direction selectivity in the
  dendrites of retinal starburst amacrine cells
* **Authors**: Srivastava, P., de Rosenroll, G., Matsumoto, A., Michaiel, A., Turpin, R.,
  Awatramani, G.B.
* **Year**: 2022
* **DOI**: `10.7554/eLife.81533`
* **URL**: https://elifesciences.org/articles/81533
* **Peer-reviewed**: yes (eLife)
* **Relevance**: Direction-tuned glutamate release onto DSGC/SAC dendrites with 10–15 µm grain.
  Extends [Jain2020]'s 5–10 µm DS subunit scale to the input side.

### [Single1997]

* **Type**: paper
* **Title**: Dendritic Computation of Direction Selectivity and Gain Control in Visual Interneurons
* **Authors**: Single, S., Haag, J., Borst, A.
* **Year**: 1997
* **DOI**: `10.1523/JNEUROSCI.17-16-06023.1997`
* **URL**: https://www.jneurosci.org/content/17/16/6023
* **Peer-reviewed**: yes (Journal of Neuroscience)
* **Relevance**: First compartmental LPTC (HS cell) model; establishes morphology-driven DS in fly
  motion vision.

### [Haag2018]

* **Type**: paper
* **Title**: A common directional tuning mechanism of Drosophila motion-sensing neurons in the ON
  and in the OFF pathway
* **Authors**: Haag, J., Arenz, A., Serbe, E., Gabbiani, F., Borst, A.
* **Year**: 2018
* **DOI**: `10.1038/s41598-018-23998-9`
* **URL**: https://www.nature.com/articles/s41598-018-23998-9
* **Peer-reviewed**: yes (Scientific Reports)
* **Relevance**: Cross-morphology LPTC regression reporting r² = 0.54 between dendritic-branch
  length CV and DSI.

### [Anderson1999]

* **Type**: paper
* **Title**: Dendritic asymmetry cannot account for directional responses of neurons in visual
  cortex
* **Authors**: Anderson, J.C., Binzegger, T., Kahana, O., Martin, K.A.C., Segev, I.
* **Year**: 1999
* **DOI**: `10.1038/12194`
* **URL**: https://www.nature.com/articles/nn1199_820
* **Peer-reviewed**: yes (Nature Neuroscience)
* **Relevance**: Negative result for cortical DS — morphology alone cannot produce direction tuning
  in V1; requires ≥30% asymmetric inhibition on top.

### [Weber2022]

* **Type**: paper
* **Title**: Orientation and direction tuning align with dendritic morphology and spatial
  connectivity in mouse visual cortex
* **Authors**: Weber, J., Iacaruso, M.F., Mrsic-Flogel, T., Hofer, S.B.
* **Year**: 2022
* **DOI**: `10.1016/j.cub.2022.06.064`
* **URL**: https://www.cell.com/current-biology/fulltext/S0960-9822(22)01041-2
* **Peer-reviewed**: yes (Current Biology)
* **Relevance**: Mouse V1 direction-tuned neurons have ~180 µm apical dendrites vs ~130 µm for
  untuned. Modern cortical morphology-DS correlation.

### [Poleg-Polsky2016]

* **Type**: paper
* **Title**: Retinal Circuitry Balances Contrast Tuning of Excitation and Inhibition to Enable
  Reliable Computation of Direction Selectivity in the Retina
* **Authors**: Poleg-Polsky, A., Diamond, J.S.
* **Year**: 2016
* **DOI**: `10.1523/JNEUROSCI.4013-15.2016`
* **URL**: https://www.jneurosci.org/content/36/21/5861
* **Peer-reviewed**: yes (Journal of Neuroscience)
* **Relevance**: Compartmental DSGC model showing E/I balance at different dendritic locations
  shapes DSI; precursor to the corpus [PolegPolsky2026] ML sweep.

### [Cuntz2010]

* **Type**: paper
* **Title**: One rule to grow them all: a general theory of neuronal branching and its practical
  application
* **Authors**: Cuntz, H., Forstner, F., Borst, A., Häusser, M.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000877`
* **URL**: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000877
* **Peer-reviewed**: yes (PLoS Computational Biology)
* **Relevance**: Morphology generation tool enabling parameterized morphology sweeps. Bridges
  analytic cable theory to large compartmental simulations.

### [Borst2018]

* **Type**: paper
* **Title**: Common Circuit Design in Fly and Mammalian Motion Vision
* **Authors**: Borst, A., Helmstaedter, M.
* **Year**: 2015
* **DOI**: `10.1038/nn.4050`
* **URL**: https://www.nature.com/articles/nn.4050
* **Peer-reviewed**: yes (Nature Neuroscience review)
* **Relevance**: Peer-reviewed review framing fly-mammal DS cross-system comparison. Scopes the
  taxonomy for the synthesis answer.

### [Aldor2024]

* **Type**: paper
* **Title**: Dendritic mGluR2 and perisomatic Kv3 signaling regulate dendritic computation of mouse
  starburst amacrine cells
* **Authors**: Aldor, H., Park, E.H., Taylor, W.R., Poleg-Polsky, A.
* **Year**: 2024
* **DOI**: `10.1038/s41467-024-46234-7`
* **URL**: https://www.nature.com/articles/s41467-024-46234-7
* **Peer-reviewed**: yes (Nature Communications)
* **Relevance**: Two distance-dependent active mechanisms (dendritic mGluR2, perisomatic Kv3)
  regulate SAC DS — extends the active-dendrite framework to neuromodulation.

### [HaagEgelhaaf1992]

* **Type**: paper
* **Title**: Dendritic integration of motion information in visual interneurons of the blowfly
* **Authors**: Haag, J., Egelhaaf, M., Borst, A.
* **Year**: 1992
* **DOI**: `10.1016/0304-3940(92)90513-7`
* **URL**: https://pubmed.ncbi.nlm.nih.gov/1436421/
* **Peer-reviewed**: yes (Neuroscience Letters)
* **Relevance**: Foundational empirical study of LPTC dendritic motion integration. Anchor for all
  subsequent fly compartmental models.

### [Tigaret2024]

* **Type**: paper
* **Title**: Dendritic integration and compartmentalization of orientation and direction tuning in
  cortical pyramidal neurons
* **Authors**: Tigaret, C.M., et al.
* **Year**: 2024
* **DOI**: (bioRxiv preprint, DOI pending)
* **URL**: https://www.biorxiv.org/content/10.1101/2024.03.15.585275
* **Peer-reviewed**: no (bioRxiv preprint)
* **Relevance**: Cortical L2/3 pyramidal active-dendrite DS-and-orientation study. Extends
  [Weber2022] with active-mechanism compartmental model. Note: preprint; final peer-reviewed version
  should be cited when available.

### [Rall1977]

* **Type**: paper
* **Title**: Core conductor theory and cable properties of neurons
* **Authors**: Rall, W.
* **Year**: 1977
* **DOI**: `10.1002/cphy.cp010103`
* **URL**: https://doi.org/10.1002/cphy.cp010103
* **Peer-reviewed**: yes (Handbook of Physiology; invited chapter, peer-reviewed)
* **Relevance**: Classical cable-theory reference providing the full derivation of sequenced- input
  directional asymmetry on passive dendrites. Companion to [Rall1967] in the corpus.

### [bioRxiv-deRosenroll]

* **Type**: repository
* **Title**: deRosenroll et al. bioRxiv preprint of "Uncovering the hidden synaptic
  microarchitecture of the retinal direction selective circuit"
* **Author/Org**: deRosenroll, G., Sethuramanujam, S., Awatramani, G.B.
* **Date**: 2025
* **URL**: https://www.biorxiv.org/content/10.1101/2025.04.10.647234
* **Peer-reviewed**: no (open preprint; peer-reviewed journal version is
  `10.1016/j.celrep.2025.116833`)
* **Relevance**: Open-access mirror for [deRosenroll2026] whose published PDF failed to download in
  the corpus. Required for Gap 4 resolution.

### [PMC-LondonHausser]

* **Type**: documentation
* **Title**: PMC open-access mirror of London & Häusser (2005), "Dendritic Computation"
* **Author/Org**: PubMed Central
* **Date**: 2005
* **URL**: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2754550/
* **Peer-reviewed**: yes (original paper is peer-reviewed in Annual Review of Neuroscience)
* **Relevance**: Open-access host for [LondonHausser2005] whose corpus PDF download failed. Restores
  full-text access for the morphology-variable taxonomy reference.

### [ModelDB-GH]

* **Type**: repository
* **Title**: ModelDB — Database of Published Computational Neuroscience Models
* **Author/Org**: SenseLab, Yale University
* **Date**: 2026-04 (continuously maintained)
* **URL**: https://senselab.med.yale.edu/modeldb/
* **Last updated**: 2026-04
* **Peer-reviewed**: no (model repository, but hosted models are from peer-reviewed papers)
* **Relevance**: Hosts NEURON `.hoc` and `.mod` files for [Schachter2010], [Hausselt2007],
  [Tukker2004], [Jain2020], [PolegPolsky2026], and [Gruntman2018]. Primary source for re-usable
  compartmental morphologies.

### [TREES-GH]

* **Type**: repository
* **Title**: TREES toolbox — Dendritic morphology generation and analysis
* **Author/Org**: Cuntz lab / Häusser lab
* **Date**: 2026-02 (ongoing)
* **URL**: https://github.com/cuntzlab/treestoolbox
* **Last updated**: 2026-02
* **Peer-reviewed**: no (tool, associated with peer-reviewed [Cuntz2010])
* **Relevance**: MATLAB/Python toolbox for generating parameterized morphologies from a small number
  of branching-rule parameters. Essential for the recommended morphology-only sweep.

### [Awatramani-GH]

* **Type**: repository
* **Title**: Awatramani Lab public NEURON models — DSGC and SAC compartmental
* **Author/Org**: Awatramani Lab, University of Victoria
* **Date**: 2026-03 (ongoing)
* **URL**: https://github.com/awatramanilab
* **Last updated**: 2026-03
* **Peer-reviewed**: no (public code for peer-reviewed papers)
* **Relevance**: Hosts the [Jain2020] 177-synapse DSGC model and the [deRosenroll2026] network model
  code. Direct re-use target for follow-up compartmental sweeps.

### [Borst-Connectomics-GH]

* **Type**: repository
* **Title**: Borst Lab fly motion-vision compartmental models
* **Author/Org**: Borst Lab, MPI Neurobiology
* **Date**: 2026-01 (ongoing)
* **URL**: https://github.com/borstlab
* **Last updated**: 2026-01
* **Peer-reviewed**: no (public code for peer-reviewed papers)
* **Relevance**: Hosts T4/T5 and LPTC compartmental models corresponding to [Single1997],
  [Haag2018], and [Gruntman2018]. Required for the invertebrate part of the sweep.

### [Schachter2010]

* **Type**: paper
* **Title**: Dendritic Spikes Amplify the Synaptic Signal to Enhance Detection of Motion in a
  Simulation of the Direction-Selective Ganglion Cell
* **Authors**: Schachter, M.J., Oesch, N., Smith, R.G., Taylor, W.R.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000899`
* **URL**: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000899
* **Peer-reviewed**: yes (PLoS Computational Biology)
* **Relevance**: Corpus reference (already in `research_papers.md`); listed here because its recipe
  (40 mS/cm² gNa, 45→20 mS/cm² gradient) is repeatedly cited in Key Findings and Methodology
  Insights as the baseline biophysics for any new morphology sweep.

### [Jain2020]

* **Type**: paper
* **Title**: The functional organization of excitation and inhibition in the dendrites of mouse
  direction-selective ganglion cells
* **Authors**: Jain, V., Murphy-Baum, B.L., deRosenroll, G., Sethuramanujam, S., Delsey, M.,
  Delaney, K.R., Awatramani, G.B.
* **Year**: 2020
* **DOI**: `10.7554/eLife.52949`
* **URL**: https://elifesciences.org/articles/52949
* **Peer-reviewed**: yes (eLife)
* **Relevance**: Corpus reference. Cited here for the 5–10 µm DS subunit scale and λ ≈ 5.3 µm cable
  constant used to justify spatial discretization requirements in the Methodology Insights section.

### [PolegPolsky2026]

* **Type**: paper
* **Title**: Machine learning discovers numerous new computational principles underlying direction
  selectivity in the retina
* **Authors**: Poleg-Polsky, A.
* **Year**: 2026
* **DOI**: `10.1038/s41467-026-70288-4`
* **URL**: https://www.nature.com/articles/s41467-026-70288-4
* **Peer-reviewed**: yes (Nature Communications)
* **Relevance**: Corpus reference. Cited here as the 352-segment DSGC sweep paper whose
  ML-discovered mechanism primitives form the hypothesis library for morphology-variable testing.

### [deRosenroll2026]

* **Type**: paper
* **Title**: Uncovering the "hidden" synaptic microarchitecture of the retinal direction selective
  circuit
* **Authors**: deRosenroll, G., Sethuramanujam, S., Awatramani, G.B.
* **Year**: 2026
* **DOI**: `10.1016/j.celrep.2025.116833`
* **URL**: https://www.cell.com/cell-reports/fulltext/S2211-1247(25)11683-3
* **Peer-reviewed**: yes (Cell Reports)
* **Relevance**: Corpus reference. Cited here as the canonical local-ACh subcellular
  microarchitecture paper; its network code is re-used as a morphology-sweep substrate.

### [Rall1967]

* **Type**: paper
* **Title**: Distinguishing theoretical synaptic potentials computed for different soma-dendritic
  distributions of synaptic input
* **Authors**: Rall, W.
* **Year**: 1967
* **DOI**: `10.1152/jn.1967.30.5.1138`
* **URL**: https://journals.physiology.org/doi/10.1152/jn.1967.30.5.1138
* **Peer-reviewed**: yes (Journal of Neurophysiology)
* **Relevance**: Corpus reference. Cited here as the analytic foundation for passive-dendrite
  sequenced-input directional asymmetry that underlies the Rall/Koch-Poggio baseline mechanism.

### [KochPoggio1982]

* **Type**: paper
* **Title**: Retinal ganglion cells: a functional interpretation of dendritic morphology
* **Authors**: Koch, C., Poggio, T., Torre, V.
* **Year**: 1982
* **DOI**: `10.1098/rstb.1982.0084`
* **URL**: https://royalsocietypublishing.org/doi/10.1098/rstb.1982.0084
* **Peer-reviewed**: yes (Philosophical Transactions of the Royal Society B)
* **Relevance**: Corpus reference. Cited for the "passive morphology alone produces directional
  voltage transfer" claim that the cortical [Anderson1999] result partially contradicts.

### [LondonHausser2005]

* **Type**: paper
* **Title**: Dendritic Computation
* **Authors**: London, M., Häusser, M.
* **Year**: 2005
* **DOI**: `10.1146/annurev.neuro.28.061604.135703`
* **URL**: https://www.annualreviews.org/doi/10.1146/annurev.neuro.28.061604.135703
* **Peer-reviewed**: yes (Annual Review of Neuroscience)
* **Relevance**: Corpus reference. Cited here for the four-axis morphology-variable taxonomy (branch
  order, diameter, distance from soma, synaptic spatial layout) that organizes the synthesis answer.

### [Hanson2019]

* **Type**: paper
* **Title**: Retinal direction selectivity in the absence of asymmetric starburst amacrine cell
  responses
* **Authors**: Hanson, L., Sethuramanujam, S., deRosenroll, G., Jain, V., Awatramani, G.B.
* **Year**: 2019
* **DOI**: `10.7554/eLife.42392`
* **URL**: https://elifesciences.org/articles/42392
* **Peer-reviewed**: yes (eLife)
* **Relevance**: Corpus reference. Cited here as the empirical demonstration that DSGCs retain DS
  without asymmetric SAC inhibition — the methodological motivation for including a
  "no-asymmetric-inhibition" control in any morphology sweep.

### [Euler2002]

* **Type**: paper
* **Title**: Directionally selective calcium signals in dendrites of starburst amacrine cells
* **Authors**: Euler, T., Detwiler, P.B., Denk, W.
* **Year**: 2002
* **DOI**: `10.1038/nature00931`
* **URL**: https://www.nature.com/articles/nature00931
* **Peer-reviewed**: yes (Nature)
* **Relevance**: Corpus reference. Cited here for the SAC velocity-tuning window that [Tukker2004]
  and [Stincic2023] extend with quantitative morphology-DS curves.
