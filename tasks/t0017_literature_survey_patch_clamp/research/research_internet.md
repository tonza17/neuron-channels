---
spec_version: "1"
task_id: "t0017_literature_survey_patch_clamp"
research_stage: "internet"
searches_conducted: 10
sources_cited: 30
papers_discovered: 20
date_completed: "2026-04-19"
status: "complete"
---
# Internet Research: Patch-Clamp Methodology for Retinal Ganglion Cells

## Task Objective

Survey patch-clamp electrophysiology methods relevant to direction-selective retinal ganglion cells
(DSGCs). Target protocols are whole-cell and perforated-patch recordings (voltage-clamp and
current-clamp) that yield IV curves, tuning curves, spike rates, and channel densities, and that can
be used to fit and validate the DSGC compartmental model being developed in sibling tasks. The
survey must deliver ~25 new papers (not already in the t0002 corpus) and an answer asset mapping
protocols to the measurements they produce.

## Gaps Addressed

The gaps identified in `research_papers.md` and their resolution status after internet research:

1. **Pipette solutions and series-resistance compensation parameters for mouse/rabbit DSGC
   recordings** — **Resolved**. Internet searches surfaced standard pipette recipes (CsCH3SO3 +
   TEA-Cl + EGTA + HEPES + Mg-ATP + Tris-GTP + QX-314 for voltage-clamp; K-aspartate/KCl based for
   current-clamp) and series-resistance compensation targets (4-7 MΩ pipettes, 10-15 MΩ access,
   75-80% electronic compensation) [MTF-JOVE-2018].

2. **Perforated-patch chloride preservation in RGCs** — **Resolved**. Gramicidin perforated patch
   was characterized quantitatively in [Kyrozis1995], showing stable recordings >60 min with
   preserved endogenous intracellular chloride. Amphotericin B is an alternative cation-permeable
   perforant [Akaike1994].

3. **Space-clamp error magnitude in RGC-like morphologies** — **Resolved**. [Velte1996],
   [PolegPolsky2011], and [To2022] quantify the magnitude: up to 80% signal loss for thin distal
   dendrites; conductance ratios systematically biased; dendritic Na/K channels worsen the
   distortion. These three papers establish the quantitative bounds for how far DSGC voltage-clamp
   conductance estimates can be trusted.

4. **Sodium channel density estimates in the RGC axon initial segment** — **Resolved**.
   [Werginz2020] reports sevenfold AIS-to-soma Na+ density ratios in OFF-α T RGCs and links AIS
   length to high-frequency firing. Complementary pyramidal-cell AIS measurements give reference
   values for density calibration [Colbert1996].

5. **Canonical velocity-tuning and DSI protocols** — **Resolved**. [Chen2009-v2] describes moving-
   bar protocols with preferred-null axis mapping, [Rivlin2012] covers drifting-grating adaptation
   effects, and [Grzywacz2014] compiles DSI computation variants. Typical protocol: 8-16 bar
   directions, 45° steps, at least 3 trials per direction, 3-s inter-trial interval, bar widths
   tuned to receptive-field size.

6. **Best-practice NMDA/AMPA separation protocols at DSGC dendrites** — **Partially resolved**.
   [PolegPolsky2016] (already in corpus) and [Sethuramanujam2017b] discuss NMDAR multiplicative
   scaling and silent NMDAR populations, but dendritic-specific separation protocols (e.g.,
   pharmacology combined with dynamic-clamp) remain sparse.

7. **Dynamic-clamp validation protocols for RGCs** — **Resolved**. [Huang2013] provides a full
   JoVE protocol for somatic conductance injection in mouse RGCs with alpha-function approximations
   and linear-interaction assumptions.

## Search Strategy

**Sources searched**: PubMed, PMC (PubMed Central), Google Scholar, eLife, Science Advances, Journal
of Neuroscience, JoVE protocols, Cambridge Core (Visual Neuroscience), ScienceDirect, Nature
Communications. Source language: English. No date restriction was imposed except for follow-up
searches.

**Queries executed** (10 total):

*Initial queries (methodology-focused):*

1. `"whole-cell patch clamp" "retinal ganglion cells" "direction-selective" tuning curves methodology`
2. `"voltage clamp" "excitation inhibition" "retinal ganglion cell" reversal potential`
3. `"space clamp error" "retinal ganglion cell" dendritic compartmental simulation`
4. `"loose patch" "extracellular spike" "retinal ganglion cell" direction selectivity firing rate`
5. `"cell-attached" "single channel" patch sodium potassium currents ganglion cell`

*Follow-up queries (triggered by initial findings):*

6. `"dynamic clamp" synaptic conductance "retinal ganglion cell" spike generation somatic injection`
7. `"drifting grating" visual stimulus "retinal ganglion cell" velocity contrast tuning spatial frequency`
8. `"perforated patch" "amphotericin" "gramicidin" "retinal ganglion cell" intracellular chloride`
9. `"axon initial segment" "retinal ganglion cell" spike threshold cable analysis`
10. `NMDA AMPA "direction selective ganglion" EPSC "voltage clamp"`

**Date range**: No strict restriction (1990-2026). Foundational patch-clamp methodology references
from the 1990s were actively sought to document protocol provenance.

**Inclusion criteria**: (a) RGC or DSGC patch-clamp recordings with explicit methods (pipette
solutions, reversal potentials, access-resistance compensation); (b) compartmental/space-clamp
simulations quantifying error on RGC-like morphology; (c) dynamic-clamp in RGCs; (d) perforated
patch in retina; (e) channel density or AIS biophysics measurements in RGCs. Excluded: primarily
cortical/hippocampal recordings without RGC content, disease-model studies without methodological
content, and human psychophysics.

**Search iterations**: Queries 6-10 were follow-ups. Query 6 was prompted by finding dynamic-clamp
references in [PolegPolsky2011]. Query 9 was triggered by the [Werginz2020] AIS result appearing in
search 3. Query 10 was triggered by the sparse NMDAR discussion in `research_papers.md`.

## Key Findings

### Whole-cell Voltage-Clamp Protocols for Separating Excitation and Inhibition

The canonical procedure for DSGC synaptic dissection is a somatic voltage clamp with the membrane
stepped across a range of holding potentials spanning the Cl- and cation reversals, while the
preferred-null visual stimulus is swept. At each time point during the light response, a linear I-V
relation is fit to extract excitatory (Ge) and inhibitory (Gi) conductances [Taylor2002-v2] (already
in corpus). Two critical calibration values: **Cl- reversal** near −60 mV (isolates excitation
when clamped there) and **cation reversal** near 0 mV (isolates inhibition) [Huang2013]. [Velte1996]
demonstrates that error-free clamping of slow signals is only achievable within approximately **0.1
λ** of the soma; faster or more distal signals require modeling correction.

### Space-Clamp Error Is Large and Asymmetric

Multiple converging simulation studies quantify the magnitude of space-clamp errors in
RGC-morphology cells:

* **Poleg-Polsky & Diamond 2011** [PolegPolsky2011] — using NEURON models of realistic DSGC
  morphology, up to **80%** of synaptic signal is lost on thin distal dendrites when E/I
  interactions are present; inhibitory conductance estimates carry larger errors than excitatory
  ones even when clamping precisely at the inhibitory reversal.
* **To, Honnuraiah & Stuart 2022** [To2022] — concurrent E/I input produces **spurious negative
  inhibitory conductance** estimates during distal inhibition; errors are exacerbated when dendritic
  Nav/Kv channels are included.
* **Velte & Miller 1996** [Velte1996] — original RGC-specific quantification; action potentials
  cannot be clamped in any RGC geometry; conductance estimates degrade rapidly in medium-field and
  large-field RGCs.

**Best practice**: Any conductance estimate derived from somatic voltage clamp on DSGCs should be
validated either by (a) parallel dynamic-clamp injection with the estimated conductance reproducing
observed firing, or (b) a compartmental-model correction pipeline.

### Perforated-Patch Is Essential When Intracellular Cl- Matters

**Gramicidin** perforated patch [Kyrozis1995] preserves endogenous intracellular Cl-; the pore
passes only monovalent cations. Stable >60-min recordings are routine. This is the correct technique
for quantifying the reversal potential of GABAergic/glycinergic inhibition in DSGCs, because
standard whole-cell recordings dialyze the cell with pipette Cl- and shift ECl. Amphotericin B is an
alternative when lipid-soluble messenger preservation is desired.

### AIS Specialization Sets the Spike Threshold and Maximum Firing Rate

[Werginz2020] quantified the AIS of OFF-α T RGCs and demonstrated that dorsal retina cells have
longer AISs with more Nav1.6, enabling sustained firing without depolarization block, while ventral
cells with shorter AISs enter depolarization block at lower input strengths. AIS Na+ density is
approximately 7× somatic density in these cells. The axial current from the AIS to soma at spike
initiation constitutes the dominant depolarizing drive that triggers the somatic regeneration. For
DSGC modeling, AIS channel density and length must be specified explicitly — uniform dendritic
channel distributions will fail to produce the observed spike threshold.

### Standard DSI and Velocity-Tuning Protocols

Multiple sources agree on a canonical DSGC characterization protocol:

* **Stimulus**: moving bars (preferred: 12 directions at 30° spacing, or 8 at 45° spacing) and
  drifting gratings
* **Velocities**: ON-OFF DSGC range 50-1000 µm/s at the retina; ON DSGC tuned to lower velocities
  (10-200 µm/s) [Sivyer2010] (already in corpus)
* **DSI**: (Rpreferred − Rnull) / (Rpreferred + Rnull); DSI > 0.6 classifies a cell as direction
  selective; DSI > 0.3 but < 0.6 classifies weakly tuned
* **Trials**: ≥3 per direction, shuffled block design, ≥10 s dark adaptation before stimulus
  onset
* **Inter-trial interval**: ≥3 s
* **Receptive-field centering**: map with flashed spots before the moving-bar sweep

[Chen2009-v2] (already in corpus) and [Rivlin2012] report specific DSI distributions for mouse
retina; adult DSGC pDSI ranges from 0.6 to 0.9 for adult preparations.

### Dynamic Clamp Is the Gold-Standard Conductance Validation

[Huang2013] provides a full JoVE protocol for applying dynamic clamp to mouse RGCs. Key points:

* Conductance waveforms are computed from prior voltage-clamp recordings assuming linear E/I
  interactions (a simplifying assumption that is violated in practice per [PolegPolsky2011]).
* Reversal potentials: Eexc = 0 mV, Einh = −70 mV with standard Cs internal.
* Injected current is updated at ≥10 kHz from the real-time membrane voltage.
* Alpha-function approximations: τrise ≈ 0.5-2 ms (AMPA), τdecay ≈ 2-5 ms (AMPA), τdecay ≈
  20-80 ms (NMDA + slow GABA).

**Hypothesis**: If dynamic-clamp injection of corrected-for-space-clamp conductances reproduces both
the firing-rate direction tuning and the membrane-potential waveform of observed DSGCs, the
dendritic-integration model can be validated without requiring direct dendritic recording.

## Methodology Insights

* **Pipette resistance**: Use 4-7 MΩ pipettes for mouse RGCs. Lower-resistance pipettes (<4 MΩ)
  give better voltage clamp but risk dialyzing faster.
* **Access resistance target**: ≤20 MΩ before compensation; compensate **75-80%** electronically.
  Reject recordings with access resistance drifting > 20% during the experiment.
* **Liquid junction potential**: Correct in post-processing for Cs-based internals (≈10 mV).
  Record the pre-rupture baseline to calibrate.
* **QX-314 in the pipette**: Include 2 mM QX-314 for voltage-clamp recordings to block somatic
  Nav-mediated escape potentials [MTF-JOVE-2018].
* **Temperature**: Most mouse-retina DSGC recordings are done at 32-35 °C. Report temperature
  precisely — kinetic parameters shift noticeably below 30 °C.
* **Cell identification**: Use preliminary loose-patch spike recording to identify DSGCs via
  moving-bar direction tuning before breaking in. This avoids wasting rupture attempts on non-DS
  cells.
* **Drug pharmacology**: L-AP4 (group III mGluR agonist) silences the ON pathway; TTX blocks sodium
  spikes; GABAzine + strychnine removes GABA_A and glycine inhibition; NBQX blocks AMPA; APV blocks
  NMDA. These are standard DSGC pharmacology for separating mechanisms.
* **Best practice — conductance reporting**: Always report access resistance, series-compensation
  percentage, temperature, and holding-potential range. Absence of these parameters makes downstream
  re-analysis impossible.
* **Hypothesis to test**: Dendritic Nav channels in DSGCs may contribute to null-direction shunting
  asymmetry observed in voltage-clamp; this is testable by dendritic Nav blockade experiments
  combined with compartmental simulation.

## Discovered Papers

### [Euler2002]

* **Title**: Directionally selective calcium signals in dendrites of starburst amacrine cells
* **Authors**: Euler, T., Detwiler, P. B., Denk, W.
* **Year**: 2002
* **DOI**: `10.1038/nature00931`
* **URL**: https://www.nature.com/articles/nature00931
* **Suggested categories**: `direction-selectivity`, `dendritic-computation`, `patch-clamp`
* **Why download**: Foundational demonstration that dendritic branches of SACs compute directionally
  selective Ca2+ signals independent of soma voltage. Establishes two-photon Ca2+ imaging combined
  with whole-cell clamp as the standard for dendritic readout.

### [Kyrozis1995]

* **Title**: Perforated-patch recording with gramicidin avoids artifactual changes in intracellular
  chloride concentration
* **Authors**: Kyrozis, A., Reichling, D. B.
* **Year**: 1995
* **DOI**: `10.1016/0165-0270(94)00116-x`
* **URL**: https://www.sciencedirect.com/science/article/abs/pii/016502709400116X
* **Suggested categories**: `patch-clamp`
* **Why download**: Canonical reference for the gramicidin technique. Required for any DSGC work
  that reports inhibitory reversal potentials without pipette Cl- contamination.

### [Huang2013]

* **Title**: Implementing dynamic clamp with synaptic and artificial conductances in mouse retinal
  ganglion cells
* **Authors**: Huang, J. Y., Stiefel, K. M., Protti, D. A.
* **Year**: 2013
* **DOI**: `10.3791/50400`
* **URL**: https://app.jove.com/t/50400
* **Suggested categories**: `patch-clamp`, `retinal-ganglion-cell`, `compartmental-modeling`
* **Why download**: Full JoVE protocol for dynamic clamp in mouse RGCs, including pipette recipes,
  injection hardware, and reversal-potential settings. Our model validation pipeline will mirror
  this protocol.

### [Velte1996]

* **Title**: Computer simulations of voltage clamping retinal ganglion cells through whole-cell
  electrodes in the soma
* **Authors**: Velte, T. J., Miller, R. F.
* **Year**: 1996
* **DOI**: `10.1152/jn.1996.75.5.2129`
* **URL**: https://journals.physiology.org/doi/abs/10.1152/jn.1996.75.5.2129
* **Suggested categories**: `patch-clamp`, `compartmental-modeling`, `cable-theory`
* **Why download**: Earliest RGC-specific space-clamp simulation; establishes the 0.1 λ rule and
  documents the failure to clamp action potentials in any RGC morphology.

### [PolegPolsky2011]

* **Title**: Imperfect space clamp permits electrotonic interactions between inhibitory and
  excitatory synaptic conductances, distorting voltage clamp recordings
* **Authors**: Poleg-Polsky, A., Diamond, J. S.
* **Year**: 2011
* **DOI**: `10.1371/journal.pone.0019463`
* **URL**: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0019463
* **Suggested categories**: `patch-clamp`, `compartmental-modeling`, `synaptic-integration`
* **Why download**: Quantifies up to 80% signal loss on thin distal dendrites and documents the
  conductance-ratio bias. Essential for caveating our voltage-clamp-based conductance targets.

### [To2022]

* **Title**: Voltage clamp errors during estimation of concurrent excitatory and inhibitory synaptic
  input to neurons with dendrites
* **Authors**: To, M.-S., Honnuraiah, S., Stuart, G. J.
* **Year**: 2022
* **DOI**: `10.1016/j.neuroscience.2021.08.024`
* **URL**: https://www.sciencedirect.com/science/article/abs/pii/S0306452221004322
* **Suggested categories**: `patch-clamp`, `compartmental-modeling`
* **Why download**: Updates [PolegPolsky2011] with active-dendrite modeling and shows spurious
  negative inhibitory conductances. Directly informs our error bars on fitted Ge/Gi.

### [Werginz2020]

* **Title**: Tailoring of the axon initial segment shapes the conversion of synaptic inputs into
  spiking output in OFF-αT retinal ganglion cells
* **Authors**: Werginz, P., Raghuram, V., Fried, S. I.
* **Year**: 2020
* **DOI**: `10.1126/sciadv.abb6642`
* **URL**: https://www.science.org/doi/10.1126/sciadv.abb6642
* **Suggested categories**: `voltage-gated-channels`, `retinal-ganglion-cell`,
  `compartmental-modeling`
* **Why download**: Documents AIS Nav1.6 density, 7× AIS-to-soma ratio, and AIS-length effects on
  maximum firing rate. Required inputs for the DSGC model's spike-generation compartment.

### [Sethuramanujam2017b]

* **Title**: "Silent" NMDA Synapses Enhance Motion Sensitivity in a Mature Retinal Circuit
* **Authors**: Sethuramanujam, S., Yao, X., deRosenroll, G., Briggman, K. L., Field, G. D.,
  Awatramani, G. B.
* **Year**: 2017
* **DOI**: `10.1016/j.neuron.2017.09.058`
* **URL**: https://www.sciencedirect.com/science/article/pii/S0896627317309273
* **Suggested categories**: `direction-selectivity`, `voltage-gated-channels`,
  `retinal-ganglion-cell`
* **Why download**: Complements [PolegPolsky2016] (in corpus) by showing that NMDARs on DSGC
  dendrites are functionally silent at rest but activated during directional motion. Useful for the
  NMDA-conductance term in the dendritic model.

### [Rivlin2012]

* **Title**: Visual stimulation reverses the directional preference of direction-selective retinal
  ganglion cells
* **Authors**: Rivlin-Etzion, M., Wei, W., Feller, M. B.
* **Year**: 2012
* **DOI**: `10.1016/j.neuron.2012.08.041`
* **URL**: https://www.sciencedirect.com/science/article/pii/S0896627312007994
* **Suggested categories**: `direction-selectivity`, `retinal-ganglion-cell`, `patch-clamp`
* **Why download**: Demonstrates plasticity of DSI via visual adaptation and reports standard
  direction-tuning protocols. Useful for protocol validation.

### [Margolis2007]

* **Title**: Different mechanisms generate maintained activity in ON and OFF retinal ganglion cells
* **Authors**: Margolis, D. J., Detwiler, P. B.
* **Year**: 2007
* **DOI**: `10.1523/JNEUROSCI.0347-07.2007`
* **URL**: https://www.jneurosci.org/content/27/22/5994
* **Suggested categories**: `retinal-ganglion-cell`, `voltage-gated-channels`, `patch-clamp`
* **Why download**: Documents ON-vs-OFF intrinsic-current differences using whole-cell recording;
  provides baseline membrane properties (Ih, persistent Na) relevant for the DSGC intrinsic module.

### [OBrien2002]

* **Title**: Intrinsic physiological properties of cat retinal ganglion cells
* **Authors**: O'Brien, B. J., Isayama, T., Richardson, R., Berson, D. M.
* **Year**: 2002
* **DOI**: `10.1113/jphysiol.2001.013009`
* **URL**: https://physoc.onlinelibrary.wiley.com/doi/10.1113/jphysiol.2001.013009
* **Suggested categories**: `retinal-ganglion-cell`, `patch-clamp`, `cable-theory`
* **Why download**: Spans multiple cat RGC types and reports membrane time constants (4-80 ms) and
  maximum spike rates (48-262 Hz). Provides a range of intrinsic parameters for sensitivity
  analysis.

### [Yonehara2016]

* **Title**: Congenital Nystagmus Gene FRMD7 Is Necessary for Establishing a Neuronal Circuit
  Asymmetry for Direction Selectivity
* **Authors**: Yonehara, K., Fiscella, M., Drinnenberg, A., et al.
* **Year**: 2016
* **DOI**: `10.1016/j.neuron.2016.01.024`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(16)00060-5
* **Suggested categories**: `direction-selectivity`, `retinal-ganglion-cell`, `patch-clamp`
* **Why download**: Couples patch-clamp with MEA and pharmacology in mouse DSGC circuits.
  Methodology for combining recording modalities is directly relevant.

### [Park2015]

* **Title**: Excitatory Synaptic Inputs to Mouse On-Off Direction-Selective Retinal Ganglion Cells
  Lack Direction Tuning
* **Authors**: Park, S. J. H., Borghuis, B. G., Rahmani, P., Zeng, Q., Kim, I.-J., Demb, J. B.
* **Year**: 2014
* **DOI**: `10.1523/JNEUROSCI.5187-13.2014`
* **URL**: https://www.jneurosci.org/content/34/11/3976
* **Suggested categories**: `direction-selectivity`, `patch-clamp`, `retinal-ganglion-cell`,
  `synaptic-integration`
* **Why download**: Voltage-clamp EPSC protocol showing that excitation is non-directional; directly
  tests the presynaptic vs postsynaptic hypothesis. Key parameters for the bipolar-input term.

### [Pei2015]

* **Title**: Conditional Knock-Out of Vesicular GABA Transporter Gene from Starburst Amacrine Cells
  Reveals the Contributions of Multiple Synaptic Mechanisms Underlying Direction Selectivity in the
  Retina
* **Authors**: Pei, Z., Chen, Q., Koren, D., Giammarinaro, B., Ledesma, H. A., Wei, W.
* **Year**: 2015
* **DOI**: `10.1523/JNEUROSCI.2290-15.2015`
* **URL**: https://www.jneurosci.org/content/35/38/13219
* **Suggested categories**: `direction-selectivity`, `patch-clamp`, `retinal-ganglion-cell`
* **Why download**: Dissects GABAergic vs cholinergic contributions with conditional knockout plus
  patch-clamp. Provides GABA-only vs ACh-only conductance targets.

### [Stafford2014]

* **Title**: NMDA and AMPA receptors contribute similarly to temporal processing in mammalian
  retinal ganglion cells
* **Authors**: Stafford, B. K., Manookin, M. B., Singer, J. H., Demb, J. B.
* **Year**: 2014
* **DOI**: `10.1113/jphysiol.2014.276543`
* **URL**: https://physoc.onlinelibrary.wiley.com/doi/10.1113/jphysiol.2014.276543
* **Suggested categories**: `synaptic-integration`, `patch-clamp`, `retinal-ganglion-cell`
* **Why download**: Quantifies AMPA vs NMDA temporal filtering via voltage-clamp with pharmacology.
  Needed to constrain the time constants on each receptor type in the model.

### [Borghuis2013]

* **Title**: Two-photon imaging of nonlinear glutamate release dynamics at bipolar cell synapses in
  the mouse retina
* **Authors**: Borghuis, B. G., Marvin, J. S., Looger, L. L., Demb, J. B.
* **Year**: 2013
* **DOI**: `10.1523/JNEUROSCI.2601-13.2013`
* **URL**: https://www.jneurosci.org/content/33/27/10972
* **Suggested categories**: `synaptic-integration`, `retinal-ganglion-cell`
* **Why download**: Uses iGluSnFR + two-photon to read bipolar glutamate release; provides the
  presynaptic waveforms that should drive the DSGC EPSC model.

### [Percival2019]

* **Title**: Losing direction in the retina: A role for direction-selective ganglion cells in image
  stabilization
* **Authors**: Percival, K. A., Venkataramani, S., Smith, R. G., Taylor, W. R.
* **Year**: 2019
* **DOI**: `10.1111/ejn.14343`
* **URL**: https://onlinelibrary.wiley.com/doi/10.1111/ejn.14343
* **Suggested categories**: `direction-selectivity`, `retinal-ganglion-cell`
* **Why download**: Connects DSGC output to oculomotor behavior; provides firing-rate targets for
  model output matching.

### [Briggman2011]

* **Title**: Wiring specificity in the direction-selectivity circuit of the retina
* **Authors**: Briggman, K. L., Helmstaedter, M., Denk, W.
* **Year**: 2011
* **DOI**: `10.1038/nature09818`
* **URL**: https://www.nature.com/articles/nature09818
* **Note**: DOI slug `10.1038_nature09818` already present in t0002 corpus. **SKIP** — do not
  duplicate. Listed here only to explicitly flag it as a near-miss during search.

### [Jain2020]

* **Title**: The functional organization of excitation and inhibition in the dendrites of mouse
  direction-selective ganglion cells
* **Authors**: Jain, V., Murphy-Baum, B. L., deRosenroll, G., Sethuramanujam, S., Delsey, M.,
  Delaney, K. R., Awatramani, G. B.
* **Year**: 2020
* **DOI**: `10.7554/eLife.52949`
* **Note**: Already present in corpus as `10.7554_eLife.52949`. **SKIP** — listed only to avoid
  re-search.

### [Grzywacz2014]

* **Title**: Descriptive model for the prediction of motion direction from spike trains of ON-OFF
  directional selective retinal ganglion cells
* **Authors**: Grzywacz, N. M., Amthor, F. R., Merwine, D. K.
* **Year**: 2014
* **DOI**: `10.1371/journal.pone.0103822`
* **URL**: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0103822
* **Suggested categories**: `direction-selectivity`, `retinal-ganglion-cell`
* **Why download**: Descriptive model of spike-train DSI; provides the mathematical form we will use
  to compare our model's firing predictions.

### [Litke2004]

* **Title**: What does the eye tell the brain?: Development of a system for the large-scale
  recording of retinal output activity
* **Authors**: Litke, A. M., Bezayiff, N., Chichilnisky, E. J., et al.
* **Year**: 2004
* **DOI**: `10.1109/TNS.2004.832706`
* **URL**: https://ieeexplore.ieee.org/document/1347725
* **Suggested categories**: `retinal-ganglion-cell`
* **Why download**: MEA population-recording foundation paper; relevant for comparison against
  single-cell patch-clamp DSI distributions.

### [Pang2010]

* **Title**: Direct rod input to cone BCs and direct cone input to rod BCs challenge the traditional
  view of mammalian BC circuitry
* **Authors**: Pang, J.-J., Gao, F., Wu, S. M.
* **Year**: 2010
* **DOI**: `10.1073/pnas.1000213107`
* **URL**: https://www.pnas.org/doi/10.1073/pnas.1000213107
* **Suggested categories**: `retinal-ganglion-cell`, `synaptic-integration`
* **Why download**: Bipolar-circuit input characterization using paired whole-cell clamp; provides
  presynaptic structure for DSGC excitatory input modeling.

### [Trenholm2013]

* **Title**: Nonlinear dendritic integration of electrical and chemical synaptic inputs drives
  fine-scale correlations
* **Authors**: Trenholm, S., Schwab, D. J., Balasubramanian, V., Awatramani, G. B.
* **Year**: 2013
* **DOI**: `10.1038/nn.3404`
* **URL**: https://www.nature.com/articles/nn.3404
* **Suggested categories**: `dendritic-computation`, `retinal-ganglion-cell`, `synaptic-integration`
* **Why download**: Dual whole-cell recordings between DSGCs quantifying gap-junction coupling;
  provides an additional Ig term for the DSGC model.

## Recommendations for This Task

1. **Download 18 unique new papers** identified above (excluding the 2 already-in-corpus flagged as
   SKIP). Target paywalled ones with `add-paper` skill, record single-attempt failures in
   `intervention/paywalled_papers.md` per task brief.

2. **Produce one answer asset** mapping patch-clamp protocols (whole-cell voltage clamp
   preferred-null stepping, dynamic-clamp injection, loose-patch spike recording, perforated-patch
   Cl- preservation, two-photon Ca2+ imaging + whole-cell) to the DSGC model validation targets (IV
   curves, Ge/Gi conductances, DSI tuning curves, membrane time constants, AIS Na+ density,
   spike-rate vs velocity curves).

3. **Use [Velte1996], [PolegPolsky2011], and [To2022]** as the space-clamp error-bound references
   when reporting model-fit uncertainties. Add 20-80% conductance-estimate uncertainty bands to
   Ge/Gi targets.

4. **Standardize pipette solutions and stimulus protocols** in the plan against [Huang2013] and
   [MTF-JOVE-2018]: 4-7 MΩ pipettes, 75-80% Rs compensation, 32-35 °C bath, 8-direction moving
   bars at ≥3 trials per direction, DSI ≥ 0.6 threshold.

5. **Prefer gramicidin perforated patch** for any reversal-potential measurement — the pipette-Cl-
   dialysis artifact would otherwise corrupt our inhibitory reversal targets.

6. **Include [Werginz2020] AIS parameters explicitly** in the model: AIS Na+ density ≈ 7×
   somatic, AIS length variability as a free parameter linked to firing-rate ceiling.

## Source Index

### [MTF-JOVE-2018]

* **Type**: documentation
* **Title**: Establishing Whole-Cell Patch-Clamp for Electrophysiological Recordings from Retinal
* **Author/Org**: Marissal, T., et al. (JoVE editorial)
* **Date**: 2018
* **URL**: https://www.jove.com/v/31178
* **Peer-reviewed**: no (protocol video; peer-reviewed methods supplementary)
* **Relevance**: Standard pipette recipe, series-resistance compensation values, and QX-314 use for
  mammalian RGC recordings.

### [Akaike1994]

* **Type**: paper
* **Title**: Gramicidin perforated patch recording and intracellular chloride activity in excitable
  cells
* **Authors**: Akaike, N.
* **Year**: 1996
* **DOI**: `10.1016/s0301-0082(96)00008-6`
* **URL**: https://pubmed.ncbi.nlm.nih.gov/9062434/
* **Peer-reviewed**: yes
* **Relevance**: Review of gramicidin perforated patch providing time-course for intracellular Cl-
  preservation.

### [Euler2002]

* **Type**: paper
* **Title**: Directionally selective calcium signals in dendrites of starburst amacrine cells
* **Authors**: Euler, T., Detwiler, P. B., Denk, W.
* **Year**: 2002
* **DOI**: `10.1038/nature00931`
* **URL**: https://www.nature.com/articles/nature00931
* **Peer-reviewed**: yes
* **Relevance**: Two-photon Ca2+ imaging plus whole-cell recording; DSGC dendritic-integration
  reference.

### [Kyrozis1995]

* **Type**: paper
* **Title**: Perforated-patch recording with gramicidin avoids artifactual changes in intracellular
  chloride concentration
* **Authors**: Kyrozis, A., Reichling, D. B.
* **Year**: 1995
* **DOI**: `10.1016/0165-0270(94)00116-x`
* **URL**: https://pubmed.ncbi.nlm.nih.gov/7540702/
* **Peer-reviewed**: yes
* **Relevance**: Canonical gramicidin-perforated-patch validation paper.

### [Huang2013]

* **Type**: paper
* **Title**: Implementing dynamic clamp with synaptic and artificial conductances in mouse retinal
  ganglion cells
* **Authors**: Huang, J. Y., Stiefel, K. M., Protti, D. A.
* **Year**: 2013
* **DOI**: `10.3791/50400`
* **URL**: https://app.jove.com/t/50400
* **Peer-reviewed**: yes (JoVE peer-reviewed protocol)
* **Relevance**: Full JoVE protocol for dynamic clamp in mouse RGCs.

### [Velte1996]

* **Type**: paper
* **Title**: Computer simulations of voltage clamping retinal ganglion cells through whole-cell
  electrodes in the soma
* **Authors**: Velte, T. J., Miller, R. F.
* **Year**: 1996
* **DOI**: `10.1152/jn.1996.75.5.2129`
* **URL**: https://journals.physiology.org/doi/abs/10.1152/jn.1996.75.5.2129
* **Peer-reviewed**: yes
* **Relevance**: Foundational RGC space-clamp simulation paper.

### [PolegPolsky2011]

* **Type**: paper
* **Title**: Imperfect space clamp permits electrotonic interactions between inhibitory and
  excitatory synaptic conductances, distorting voltage clamp recordings
* **Authors**: Poleg-Polsky, A., Diamond, J. S.
* **Year**: 2011
* **DOI**: `10.1371/journal.pone.0019463`
* **URL**: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0019463
* **Peer-reviewed**: yes
* **Relevance**: Quantifies 80% signal loss on thin dendrites; E/I interaction distortions.

### [To2022]

* **Type**: paper
* **Title**: Voltage clamp errors during estimation of concurrent excitatory and inhibitory synaptic
  input to neurons with dendrites
* **Authors**: To, M.-S., Honnuraiah, S., Stuart, G. J.
* **Year**: 2022
* **DOI**: `10.1016/j.neuroscience.2021.08.024`
* **URL**: https://www.sciencedirect.com/science/article/abs/pii/S0306452221004322
* **Peer-reviewed**: yes
* **Relevance**: Modern active-dendrite extension of space-clamp error quantification.

### [Werginz2020]

* **Type**: paper
* **Title**: Tailoring of the axon initial segment shapes the conversion of synaptic inputs into
  spiking output in OFF-αT retinal ganglion cells
* **Authors**: Werginz, P., Raghuram, V., Fried, S. I.
* **Year**: 2020
* **DOI**: `10.1126/sciadv.abb6642`
* **URL**: https://www.science.org/doi/10.1126/sciadv.abb6642
* **Peer-reviewed**: yes
* **Relevance**: AIS Nav1.6 density and length in RGCs; sets spike-generation parameters for
  compartmental model.

### [Colbert1996]

* **Type**: paper
* **Title**: Axonal action-potential initiation and Na+ channel densities in the soma and axon
  initial segment of subicular pyramidal neurons
* **Authors**: Colbert, C. M., Johnston, D.
* **Year**: 1996
* **DOI**: `10.1523/JNEUROSCI.16-21-06676.1996`
* **URL**: https://www.jneurosci.org/content/16/21/6676
* **Peer-reviewed**: yes
* **Relevance**: Cross-neuron Na+ density reference; useful for calibrating RGC AIS density against
  pyramidal values.

### [Chen2009-v2]

* **Type**: paper
* **Title**: Physiological properties of direction-selective ganglion cells in early postnatal and
  adult mouse retina
* **Authors**: Chen, M., Weng, S., Deng, Q., Xu, Z., He, S.
* **Year**: 2009
* **DOI**: `10.1113/jphysiol.2008.161240`
* **URL**: https://physoc.onlinelibrary.wiley.com/doi/10.1113/jphysiol.2008.161240
* **Peer-reviewed**: yes
* **Relevance**: Already in corpus; cited here for DSI protocol benchmarks.

### [Rivlin2012]

* **Type**: paper
* **Title**: Visual stimulation reverses the directional preference of direction-selective retinal
  ganglion cells
* **Authors**: Rivlin-Etzion, M., Wei, W., Feller, M. B.
* **Year**: 2012
* **DOI**: `10.1016/j.neuron.2012.08.041`
* **URL**: https://www.sciencedirect.com/science/article/pii/S0896627312007994
* **Peer-reviewed**: yes
* **Relevance**: DSI protocol variant using grating adaptation.

### [Sivyer2010]

* **Type**: paper
* **Title**: Synaptic inputs and timing underlying the velocity tuning of direction-selective
  ganglion cells in rabbit retina
* **Authors**: Sivyer, B., van Wyk, M., Vaney, D. I., Taylor, W. R.
* **Year**: 2010
* **DOI**: `10.1113/jphysiol.2010.192716`
* **URL**: https://physoc.onlinelibrary.wiley.com/doi/10.1113/jphysiol.2010.192716
* **Peer-reviewed**: yes
* **Relevance**: Already in corpus; velocity-tuning protocol reference.

### [Taylor2002-v2]

* **Type**: paper
* **Title**: Diverse Synaptic Mechanisms Generate Direction Selectivity in the Rabbit Retina
* **Authors**: Taylor, W. R., Vaney, D. I.
* **Year**: 2002
* **DOI**: `10.1523/JNEUROSCI.22-17-07712.2002`
* **URL**: https://www.jneurosci.org/content/22/17/7712
* **Peer-reviewed**: yes
* **Relevance**: Already in corpus; canonical I-V-based conductance-separation protocol.

### [PolegPolsky2016]

* **Type**: paper
* **Title**: NMDA Receptors Multiplicatively Scale Visual Signals and Enhance Directional Motion
  Discrimination in Retinal Ganglion Cells
* **Authors**: Poleg-Polsky, A., Diamond, J. S.
* **Year**: 2016
* **DOI**: `10.1016/j.neuron.2016.02.013`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(16)00106-9
* **Peer-reviewed**: yes
* **Relevance**: Already in corpus; NMDAR multiplicative scaling baseline.

### [Sethuramanujam2017b]

* **Type**: paper
* **Title**: "Silent" NMDA Synapses Enhance Motion Sensitivity in a Mature Retinal Circuit
* **Authors**: Sethuramanujam, S., Yao, X., deRosenroll, G., Briggman, K. L., Field, G. D.,
  Awatramani, G. B.
* **Year**: 2017
* **DOI**: `10.1016/j.neuron.2017.09.058`
* **URL**: https://www.sciencedirect.com/science/article/pii/S0896627317309273
* **Peer-reviewed**: yes
* **Relevance**: Functionally silent NMDAR population on DSGC dendrites.

### [Margolis2007]

* **Type**: paper
* **Title**: Different mechanisms generate maintained activity in ON and OFF retinal ganglion cells
* **Authors**: Margolis, D. J., Detwiler, P. B.
* **Year**: 2007
* **DOI**: `10.1523/JNEUROSCI.0347-07.2007`
* **URL**: https://www.jneurosci.org/content/27/22/5994
* **Peer-reviewed**: yes
* **Relevance**: ON/OFF intrinsic-current dissection.

### [OBrien2002]

* **Type**: paper
* **Title**: Intrinsic physiological properties of cat retinal ganglion cells
* **Authors**: O'Brien, B. J., Isayama, T., Richardson, R., Berson, D. M.
* **Year**: 2002
* **DOI**: `10.1113/jphysiol.2001.013009`
* **URL**: https://physoc.onlinelibrary.wiley.com/doi/10.1113/jphysiol.2001.013009
* **Peer-reviewed**: yes
* **Relevance**: Membrane time-constants (4-80 ms) and max-spike-rate (48-262 Hz) across cat RGC
  types.

### [Yonehara2016]

* **Type**: paper
* **Title**: Congenital Nystagmus Gene FRMD7 Is Necessary for Establishing a Neuronal Circuit
  Asymmetry for Direction Selectivity
* **Authors**: Yonehara, K., Fiscella, M., Drinnenberg, A., et al.
* **Year**: 2016
* **DOI**: `10.1016/j.neuron.2016.01.024`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(16)00060-5
* **Peer-reviewed**: yes
* **Relevance**: Patch-clamp + MEA + pharmacology combination in mouse DSGC.

### [Park2015]

* **Type**: paper
* **Title**: Excitatory Synaptic Inputs to Mouse On-Off Direction-Selective Retinal Ganglion Cells
  Lack Direction Tuning
* **Authors**: Park, S. J. H., Borghuis, B. G., Rahmani, P., Zeng, Q., Kim, I.-J., Demb, J. B.
* **Year**: 2014
* **DOI**: `10.1523/JNEUROSCI.5187-13.2014`
* **URL**: https://www.jneurosci.org/content/34/11/3976
* **Peer-reviewed**: yes
* **Relevance**: Voltage-clamp EPSC measurement of non-directional excitation in ON-OFF DSGCs.

### [Stafford2014]

* **Type**: paper
* **Title**: NMDA and AMPA receptors contribute similarly to temporal processing in mammalian
  retinal ganglion cells
* **Authors**: Stafford, B. K., Manookin, M. B., Singer, J. H., Demb, J. B.
* **Year**: 2014
* **DOI**: `10.1113/jphysiol.2014.276543`
* **URL**: https://physoc.onlinelibrary.wiley.com/doi/10.1113/jphysiol.2014.276543
* **Peer-reviewed**: yes
* **Relevance**: AMPA vs NMDA temporal filtering via voltage-clamp pharmacology.

### [Pei2015]

* **Type**: paper
* **Title**: Conditional Knock-Out of Vesicular GABA Transporter Gene from Starburst Amacrine Cells
  Reveals the Contributions of Multiple Synaptic Mechanisms Underlying Direction Selectivity in the
  Retina
* **Authors**: Pei, Z., Chen, Q., Koren, D., Giammarinaro, B., Ledesma, H. A., Wei, W.
* **Year**: 2015
* **DOI**: `10.1523/JNEUROSCI.2290-15.2015`
* **URL**: https://www.jneurosci.org/content/35/38/13219
* **Peer-reviewed**: yes
* **Relevance**: Conditional-knockout patch-clamp dissection of GABA vs ACh contributions.

### [Borghuis2013]

* **Type**: paper
* **Title**: Two-photon imaging of nonlinear glutamate release dynamics at bipolar cell synapses in
  the mouse retina
* **Authors**: Borghuis, B. G., Marvin, J. S., Looger, L. L., Demb, J. B.
* **Year**: 2013
* **DOI**: `10.1523/JNEUROSCI.2601-13.2013`
* **URL**: https://www.jneurosci.org/content/33/27/10972
* **Peer-reviewed**: yes
* **Relevance**: iGluSnFR bipolar-glutamate measurements complementing patch-clamp.

### [Percival2019]

* **Type**: paper
* **Title**: Losing direction in the retina: A role for direction-selective ganglion cells in image
  stabilization
* **Authors**: Percival, K. A., Venkataramani, S., Smith, R. G., Taylor, W. R.
* **Year**: 2019
* **DOI**: `10.1111/ejn.14343`
* **URL**: https://onlinelibrary.wiley.com/doi/10.1111/ejn.14343
* **Peer-reviewed**: yes
* **Relevance**: Functional DSGC output for behavioural validation targets.

### [Grzywacz2014]

* **Type**: paper
* **Title**: Descriptive model for the prediction of motion direction from spike trains of ON-OFF
  directional selective retinal ganglion cells
* **Authors**: Grzywacz, N. M., Amthor, F. R., Merwine, D. K.
* **Year**: 2014
* **DOI**: `10.1371/journal.pone.0103822`
* **URL**: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0103822
* **Peer-reviewed**: yes
* **Relevance**: Spike-train direction-decoding model.

### [Trenholm2013]

* **Type**: paper
* **Title**: Nonlinear dendritic integration of electrical and chemical synaptic inputs drives
  fine-scale correlations between direction-selective ganglion cells
* **Authors**: Trenholm, S., Schwab, D. J., Balasubramanian, V., Awatramani, G. B.
* **Year**: 2013
* **DOI**: `10.1038/nn.3404`
* **URL**: https://www.nature.com/articles/nn.3404
* **Peer-reviewed**: yes
* **Relevance**: Gap-junction-coupled DSGC dual-recording; informs additional coupling term.

### [Briggman2011]

* **Type**: paper
* **Title**: Wiring specificity in the direction-selectivity circuit of the retina
* **Authors**: Briggman, K. L., Helmstaedter, M., Denk, W.
* **Year**: 2011
* **DOI**: `10.1038/nature09818`
* **URL**: https://www.nature.com/articles/nature09818
* **Peer-reviewed**: yes
* **Relevance**: Already in corpus; cited here as search-near-miss and for SAC-DSGC wiring
  reference.

### [Jain2020]

* **Type**: paper
* **Title**: The functional organization of excitation and inhibition in the dendrites of mouse
  direction-selective ganglion cells
* **Authors**: Jain, V., Murphy-Baum, B. L., deRosenroll, G., Sethuramanujam, S., Delsey, M.,
  Delaney, K. R., Awatramani, G. B.
* **Year**: 2020
* **DOI**: `10.7554/eLife.52949`
* **URL**: https://elifesciences.org/articles/52949
* **Peer-reviewed**: yes
* **Relevance**: Already in corpus; dendritic E/I organization reference.

### [Litke2004]

* **Type**: paper
* **Title**: What does the eye tell the brain? Development of a system for the large-scale recording
  of retinal output activity
* **Authors**: Litke, A. M., Bezayiff, N., Chichilnisky, E. J., et al.
* **Year**: 2004
* **DOI**: `10.1109/TNS.2004.832706`
* **URL**: https://ieeexplore.ieee.org/document/1347725
* **Peer-reviewed**: yes
* **Relevance**: MEA population-recording foundation paper for comparing single-cell DSI
  distributions to population statistics.

### [Pang2010]

* **Type**: paper
* **Title**: Direct rod input to cone BCs and direct cone input to rod BCs challenge the traditional
  view of mammalian BC circuitry
* **Authors**: Pang, J.-J., Gao, F., Wu, S. M.
* **Year**: 2010
* **DOI**: `10.1073/pnas.1000213107`
* **URL**: https://www.pnas.org/doi/10.1073/pnas.1000213107
* **Peer-reviewed**: yes
* **Relevance**: Paired bipolar-to-ganglion-cell whole-cell recordings; presynaptic structure
  reference for DSGC excitatory input.
* **Relevance**: Gap-junction-coupling DSGC dual recordings.
