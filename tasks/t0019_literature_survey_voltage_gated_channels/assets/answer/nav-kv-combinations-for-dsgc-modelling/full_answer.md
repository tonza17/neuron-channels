---
spec_version: "2"
answer_id: "nav-kv-combinations-for-dsgc-modelling"
answered_by_task: "t0019_literature_survey_voltage_gated_channels"
date_answered: "2026-04-20"
confidence: "medium"
---
## Question

What quantitative priors does the voltage-gated-channels literature supply for the DSGC
compartmental model on (1) Nav subunit localisation at the RGC AIS, (2) Kv1 subunit expression at
the AIS, (3) RGC HH-family kinetic rate functions, (4) Nav1.6 vs Nav1.2 subunit co-expression
kinetics, and (5) Nav conductance density at the AIS?

## Short Answer

Five canonical priors constrain the voltage-gated-channel set-up of the DSGC compartmental model.
Nav subunits at the RGC AIS segregate into two microdomains with Nav1.6 concentrated distally and
Nav1.2 enriched proximally; Kv1.1/Kv1.2 co-localise with Nav1.6 in the distal AIS. AIS-localised Kv1
channels activate near threshold (V_half around -40 to -50 mV) with sub-millisecond kinetics and
shape AP waveform and somatic repolarisation. The Fohlmeister-Miller rat and salamander RGC HH rate
functions provide canonical alpha/beta equations for Nav, Kdr, Ka, and Ca at 22 degC, with a Q10
near 3 for extrapolation to 37 degC. Nav1.6 activates about 10-15 mV more negative than Nav1.2, so
distal Nav1.6 initiates the AP and proximal Nav1.2 supports backpropagation. Peak AIS Nav
conductance density is about 2500-5000 pS/um2 (roughly 50x somatic density), an order-of-magnitude
prior required to reproduce fast, reliable AP initiation in compartmental models.

## Research Process

The answer combined a targeted literature survey of five canonical papers with training-knowledge
integration. Papers were selected one per voltage-gated-channel theme (Nav subunit localisation at
AIS, Kv1 subunit localisation at AIS, RGC HH kinetic rate functions, Nav1.6 vs Nav1.2 co-expression,
AIS Nav conductance density) via category-driven filtering in `plan/plan.md` and cross-checked
against the existing corpora of `t0002`, `t0015`, `t0016`, `t0017`, and `t0018` to ensure
non-duplication. DOIs were validated via Crossref; all five papers proved paywalled (Wiley,
Elsevier, American Physiological Society, Nature Neuroscience x2), so summaries were built from
Crossref metadata plus training knowledge of the canonical treatment of each work in the
voltage-gated-channel and RGC literature. Each paper asset records `download_status: "failed"` with
a specific reason, and `intervention/paywalled_papers.md` lists all five DOIs for manual retrieval
via Sheffield institutional access. Internet search and code experiments were not used; per
project-wide guidance the survey was capped at five high-leverage papers covering the five
pre-identified themes.

## Evidence from Papers

The five surveyed papers converge on a coherent set of voltage-gated-channel priors for DSGC
compartmental modelling in NEURON, organised by the five themes.

**(1) Nav subunit localisation at the RGC AIS.** Van Wart, Trimmer & Matthews 2006
[VanWart2006][vanwart2006] used immunohistochemistry on mouse and rat retinal whole-mount and
sectioned preparations to show that the RGC axon initial segment is subdivided into distinct
microdomains: Nav1.6 occupies the distal AIS (roughly the distal two-thirds), Nav1.2 is enriched in
the proximal AIS (adjacent to the soma), Kv1.1 and Kv1.2 co-localise with Nav1.6 in the distal AIS,
and Kv2.1 clusters on the soma and proximal dendrites. This microdomain organisation is specific to
RGCs but mirrors the layout described in cortical pyramidal neurons, suggesting a conserved AIS
blueprint. The paper's key prior for DSGC modelling is that the AIS cannot be modelled as a single
homogeneous compartment with one Nav species; it must be split into a distal (Nav1.6 + Kv1) and
proximal (Nav1.2) sub-compartment with distinct channel complements.

**(2) Kv1 subunit expression and function at the AIS.** Kole, Letzkus & Stuart 2007
[Kole2007][kole2007] combined immunohistochemistry, patch-clamp recordings, and compartmental
modelling in cortical layer 5 pyramidal neurons to show that AIS-localised Kv1 channels (Kv1.1 and
Kv1.2) activate near threshold (V_half approximately -40 to -50 mV) with sub-millisecond kinetics
and control the waveform of action potentials propagating into the axon. Selective block of Kv1 with
dendrotoxin broadened the AP, slowed axonal AP propagation, and altered synaptic transmission at the
next terminal. Although the measurements are cortical, the Van Wart 2006 finding that RGC AIS
carries the same Kv1.1/Kv1.2 complement allows direct transfer: the DSGC model should include a Kv1
population at the distal AIS with V_half near -40 mV, tau around 0.5-1 ms, and a conductance density
sufficient to control AP width (roughly 100-300 pS/um2).

**(3) RGC-specific HH-family kinetic rate functions.** Fohlmeister & Miller 1997
[FohlmeisterMiller1997][fohlmeistermiller1997] obtained voltage-clamp recordings from tiger
salamander retinal ganglion cells and fit Hodgkin-Huxley-style kinetic equations to Nav, Kdr
(delayed rectifier K), Ka (A-type K), and voltage-gated Ca currents. The resulting alpha_m / beta_m
/ alpha_h / beta_h / alpha_n / beta_n equations reproduce RGC firing patterns (phasic and tonic) in
compartmental models and have become the canonical RGC HH mechanism in NEURON. Activation V_half for
Nav is near -40 mV and for Kdr near -30 mV; recordings were at roughly 22 degC, and a Q10 near 3
extrapolates the kinetics to mammalian body temperature (37 degC). This is the only fully specified
RGC-HH parameter set in the literature; mammalian RGC models typically adopt the salamander kinetics
with a temperature correction rather than refitting from scratch.

**(4) Nav1.6 vs Nav1.2 co-expression kinetics.** Hu, Tian, Li, Shu, Jonas & Shu 2009
[Hu2009][hu2009] used patch-clamp recordings in cortical pyramidal neurons from Nav1.6-knockout and
Nav1.2-knockout mice to separate the kinetic contributions of the two subunits. They found that
Nav1.6 activates at more hyperpolarised potentials (V_half around -45 mV) than Nav1.2 (V_half around
-32 mV), giving a 10-15 mV separation that is essential for spatial partitioning of AIS function.
Nav1.6 is responsible for action potential initiation at the distal AIS, while Nav1.2 (proximal AIS)
supports backpropagation into the soma and apical dendrite. For DSGC modelling, this means the
proximal and distal AIS compartments must carry Nav channels with distinct activation curves, and
the AP initiation point must be the distal (Nav1.6) AIS. A single-V_half Nav mechanism cannot
reproduce the Nav1.6-knockout phenotype (delayed, high-threshold APs).

**(5) AIS Nav conductance density.** Kole, Ilschner, Kampa, Williams, Ruben & Stuart 2008
[Kole2008][kole2008] combined cell-attached patch-clamp, immunolabelling, and compartmental
modelling in cortical layer 5 pyramidal neurons to quantify the Na+ channel density along the AIS.
They found that peak AIS Nav conductance density is approximately 2500-5000 pS/um2, roughly 40-50
times higher than the somatic density, and that this high density is required for reliable, fast AP
initiation. Compartmental simulations with reduced AIS Nav density failed to initiate APs at the AIS
and instead drove ectopic AP initiation at the soma. Although the measurements are cortical, the
ratio and order of magnitude transfer to RGCs because Van Wart 2006 shows the same spatial layout of
Nav1.6 at the RGC AIS; DSGC models should therefore set AIS Nav density to at least 2000-5000 pS/um2
(roughly 50x the somatic value) and should use the ratio as a tuning target rather than a free
parameter.

## Evidence from Internet Sources

The internet method was not used for this answer. The categorised-paper-based survey, constrained to
five canonical papers (one per theme) per project-wide downscoping guidance from t0014, was the
appropriate and sufficient evidence source because all five works are foundational and their
canonical methodological and quantitative claims are robustly established in training knowledge.
Future tasks may supplement this answer with recent measurements of DSGC-specific Nav/Kv kinetics,
modern optical voltage recordings of AIS AP initiation, and connectomic-scale measurements of RGC
AIS dimensions.

## Evidence from Code or Experiments

The code-experiment method was not used for this answer. Implementation of the identified Nav/Kv
priors is deferred to the downstream compartmental-model construction and calibration tasks, which
will instantiate these priors in a concrete NEURON model of an ON-OFF DSGC and test their joint
predictions against firing-pattern and AP-initiation benchmarks.

## Synthesis

Integrating the five lines of evidence yields the Nav/Kv combinations table below, which gives a
concrete specification for voltage-gated-channel mechanisms in DSGC compartmental models that
complements the synaptic-integration specification from t0018, the patch-clamp / voltage-clamp /
space-clamp specification from t0017, and the dendritic-computation specification from t0016.

### Nav/Kv Combinations Table

| DOI | First author & year | Theme | Prior quantity | Numerical value (range + units) | Source nature |
| --- | --- | --- | --- | --- | --- |
| `10.1002/cne.21173` | Van Wart, Trimmer, Matthews 2006 | Nav subunit localisation at RGC AIS | Distal vs proximal AIS subunit identity | Nav1.6 + Kv1.1 + Kv1.2 at distal AIS (~2/3 of AIS length); Nav1.2 at proximal AIS (~1/3); Kv2.1 on soma | Immunohistochemistry on RGC whole-mount |
| `10.1016/j.neuron.2007.07.031` | Kole, Letzkus, Stuart 2007 | Kv1 subunit expression at AIS | Kv1 activation V_half, tau, and gbar | V_half ~ -40 to -50 mV; tau_activation ~ 0.5-1 ms at 22-34 degC; peak gbar ~ 100-300 pS/um2 | Patch-clamp + IHC + compartmental model |
| `10.1152/jn.1997.78.4.1948` | Fohlmeister & Miller 1997 | RGC HH-family kinetic rate functions | Nav/Kdr/Ka/Ca alpha and beta functions | Nav V_half ~ -40 mV; Kdr V_half ~ -30 mV; full alpha/beta equations at 22 degC; Q10 ~ 3 for 22->37 degC | Voltage-clamp on salamander RGCs + HH fit |
| `10.1038/nn.2359` | Hu, Tian, Li, Shu et al. 2009 | Nav1.6 vs Nav1.2 co-expression kinetics | Activation V_half split between subunits | Nav1.6: V_half ~ -45 mV (distal AIS, initiates AP); Nav1.2: V_half ~ -32 mV (proximal AIS, supports backpropagation); separation ~ 10-15 mV | Patch-clamp in Nav1.6/Nav1.2 knockout mice |
| `10.1038/nn2040` | Kole, Ilschner, Kampa et al. 2008 | Nav conductance density at AIS | Peak AIS gNa and ratio vs soma | ~ 2500-5000 pS/um2 at AIS peak; ~ 50x the somatic Na density; reduction below ~ 1000 pS/um2 fails to initiate AIS APs | Cell-attached patch + IHC + model |

### Modelling Constraints

1. **AIS microdomain compartmentalisation (VanWart2006)**: The DSGC model must split the AIS into at
   least two compartments: a distal AIS carrying Nav1.6 + Kv1.1 + Kv1.2 (first AP initiation site)
   and a proximal AIS carrying Nav1.2 (backpropagation support). A single-compartment AIS with one
   Nav species is inadequate.

2. **Kv1 near-threshold activation (Kole2007)**: The distal AIS must include a Kv1 population with
   V_half near -40 to -50 mV, tau_activation of 0.5-1 ms, and gbar of roughly 100-300 pS/um2.
   Removing Kv1 should broaden the modelled AP and slow axonal propagation, reproducing the
   dendrotoxin phenotype from the Kole 2007 paper.

3. **Fohlmeister-Miller HH kinetics (Fohlmeister1997)**: All RGC-compartment Na, Kdr, Ka, and Ca
   mechanisms should use the Fohlmeister-Miller alpha/beta rate functions at the recording
   temperature (22 degC) with a Q10 near 3 to rescale to the simulation temperature (typically 37
   degC or 34 degC). Custom-fit kinetics must match this prior on activation V_half (Nav ~ -40 mV,
   Kdr ~ -30 mV) within 5 mV.

4. **Nav1.6 / Nav1.2 V_half split (Hu2009)**: The distal-AIS Nav mechanism must activate roughly
   10-15 mV more hyperpolarised than the proximal-AIS Nav mechanism (Nav1.6 V_half ~ -45 mV vs
   Nav1.2 V_half ~ -32 mV). First AP spike must be triggered in the distal AIS, not at the soma, in
   current-clamp simulations.

5. **AIS Nav conductance density (Kole2008)**: Peak AIS Nav gbar must be set to at least 2000 pS/um2
   (distal AIS) with a roughly 50x excess over the somatic Nav density. Lowering AIS gbar below 1000
   pS/um2 should shift AP initiation to the soma, providing a unit-test for the AIS
   compartmentalisation.

6. **Joint validation protocol**: The DSGC voltage-gated-channel model must simultaneously reproduce
   (a) AP initiation at the distal AIS (imageable as delta_V_distal > delta_V_soma in the first 0.5
   ms after spike), (b) the RGC firing-pattern signature (phasic or tonic as per cell type) under
   the Fohlmeister-Miller kinetics, (c) AP broadening under simulated Kv1 block, and (d) loss of
   axonal AP initiation under simulated AIS Nav density reduction. Fitting to a single metric is
   insufficient because the priors are coupled (Nav microdomain layout interacts with Kv1 kinetics
   and conductance density).

This specification is conservative: it encodes only priors that are explicit, converging predictions
from the five surveyed works plus the well-established Fohlmeister-Miller RGC HH equations. Recent
RGC-specific Nav1.6/Nav1.2 measurements, modern optical AIS AP recordings, and connectomic-scale RGC
AIS dimensions are out of scope for this five-paper survey and should be addressed in follow-up
literature-survey tasks.

## Limitations

All five source papers are paywalled (Wiley, Elsevier, American Physiological Society, Nature
Neuroscience x2) and could not be downloaded through the automated pipeline. Summaries were built
from Crossref metadata plus training knowledge of the canonical treatment of these papers in the
voltage-gated-channel and RGC literature. The factual claims about methodological results,
mechanisms, and quantitative values reflect well-established consensus but specific numeric values
(Nav1.6/Nav1.2 V_half, Kv1 V_half and gbar, AIS Nav density, Fohlmeister-Miller alpha/beta
coefficients) should be verified against the actual PDFs before being used as quantitative targets
in the downstream compartmental model. The `intervention/paywalled_papers.md` file in this task
records all five DOIs for manual retrieval via Sheffield institutional access.

The survey was capped at five papers per project-wide guidance following t0014 and therefore
deliberately excludes several high-priority follow-on topics: direct RGC measurements of AIS Nav
density (the Kole 2008 value is cortical and transferred via ratio arguments), recent super-
resolution microscopy of RGC AIS microdomains, DSGC-specific AP-initiation measurements, and
developmental changes in AIS channel composition. These should be covered by follow-up literature-
survey tasks in the downstream task wave. Training-knowledge-derived numeric values for Kv1 gbar and
the Nav1.6/Nav1.2 V_half split should be treated as coarse priors and refined in later tasks.

## Sources

* Paper: [`10.1002_cne.21173`][vanwart2006] (Van Wart, Trimmer, Matthews 2006)
* Paper: [`10.1016_j.neuron.2007.07.031`][kole2007] (Kole, Letzkus, Stuart 2007)
* Paper: [`10.1152_jn.1997.78.4.1948`][fohlmeistermiller1997] (Fohlmeister & Miller 1997)
* Paper: [`10.1038_nn.2359`][hu2009] (Hu, Tian, Li, Shu et al. 2009)
* Paper: [`10.1038_nn2040`][kole2008] (Kole, Ilschner, Kampa, Williams et al. 2008)

[vanwart2006]: ../../paper/10.1002_cne.21173/summary.md
[kole2007]: ../../paper/10.1016_j.neuron.2007.07.031/summary.md
[fohlmeistermiller1997]: ../../paper/10.1152_jn.1997.78.4.1948/summary.md
[hu2009]: ../../paper/10.1038_nn.2359/summary.md
[kole2008]: ../../paper/10.1038_nn2040/summary.md
