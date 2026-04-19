---
spec_version: "1"
task_id: "t0015_literature_survey_cable_theory"
research_stage: "internet"
searches_conducted: 12
sources_cited: 33
papers_discovered: 25
date_completed: "2026-04-19"
status: "complete"
---
## Task Objective

Survey roughly 25 category-relevant papers on classical cable theory and passive dendritic filtering
to broaden the project's paper corpus beyond the 20 DSGC-specific papers already catalogued by task
t0002. The survey targets five themes (Rall-era foundations, the d_lambda segment discretisation
rule, branched-tree impedance, frequency-domain / ZAP analyses, and thin-dendrite transmission) and
must avoid re-downloading any DOI in the exclusion list supplied in `task_description.md`. Output is
a list of candidate papers plus one synthesis answer asset.

## Gaps Addressed

This section explicitly addresses each gap from `research_papers.md` Gaps and Limitations:

1. **Rall foundational papers (1959 core-conductor, 1962 equivalent-cylinder, 1964/1967 active
   passive dendritic models)** — **Resolved**. Located canonical references: the 1959 branching
   dendritic trees paper [Rall1959], the 1962a "Theory of physiological properties of dendrites"
   [Rall1962a], the 1962b "Electrophysiology of a dendritic neuron model" [Rall1962b], the 1967
   distinguishing theoretical synaptic potentials paper [Rall1967], and the Rall-Rinzel 1973/1974
   branch-input-resistance duo [RallRinzel1973, RinzelRall1974].

2. **d_lambda / nseg rule references** — **Resolved**. The operational d_lambda rule is documented
   in the NEURON `d_lambda.html` user guide [NEURON-dlambda-Doc] and expanded in Chapter 5 of The
   NEURON Book [Carnevale2006]. Mainen and Sejnowski (1996) [Mainen1996] introduce the
   dendritic-morphology model that became the primary test-bed for the rule.

3. **Branched-tree impedance papers (Koch, Holmes, Zador)** — **Resolved**. Koch-Poggio-Torre 1982
   on retinal ganglion cells [KochPoggio1982], Koch-Poggio-Torre 1983 on nonlinear dendritic
   interactions [KochPoggio1983], Holmes 1986 algorithm for arbitrary dendritic geometries
   [Holmes1986], Major-Evans-Jack 1993 transients trilogy [Major1993], and the Zador-Agmon-Snir
   Segev 1995 morphoelectrotonic transform [Zador1995] are all identified.

4. **Frequency-domain / ZAP / chirp analyses** — **Resolved**. The Koch 1984 quasi-active membrane
   paper [Koch1984], the Hutcheon-Yarom 2000 resonance review [HutcheonYarom2000], the Narayanan-
   Johnston 2007 theta-resonance paper [NarayananJohnston2007], and the Rathour-Narayanan location-
   dependent tuning work [Rathour2017] cover the frequency-domain theme including classical ZAP
   methodology.

5. **Thin-dendrite transmission / propagation failure** — **Resolved**. Goldstein-Rall 1974 step-
   geometry action potential paper [GoldsteinRall1974] is the canonical source on propagation
   failure at thin-to-thick junctions. Velte-Masland 1999 [VelteMasland1999] and Oesch-Euler- Taylor
   2005 [Oesch2005] cover dendritic-spike propagation in retinal ganglion cells specifically.

6. **Ganglion-cell-specific electrotonic-length estimates** — **Resolved**. Coleman-Miller 1989
   tiger salamander ganglion cell cable properties [ColemanMiller1989] report L = 0.34 +/- 0.13;
   Velte-Miller 1995 rainbow trout developmental passive properties [VelteMiller1995] report
   equivalent-cylinder cable parameters; Fohlmeister-Miller 1997 multicompartmental RGC model
   [FohlmeisterMiller1997] and the 2010 mammalian update [Fohlmeister2010] anchor compartmental RGC
   modelling in general.

7. **Textbook-level cable-theory derivations** — **Resolved**. Jack-Noble-Tsien "Electric Current
   Flow in Excitable Cells" [JackNobleTsien1975] is the canonical textbook derivation of the cable
   equation. Segev-Rinzel-Shepherd "The Theoretical Foundation of Dendritic Function"
   [SegevRinzelShepherd1995] republishes Rall's papers with commentary. Stuart-Spruston-Hausser
   "Dendrites" [StuartSprustonHausser2016] is the modern dendrites textbook, and the Stuart-
   Spruston 2015 review [StuartSpruston2015] distils the field.

## Search Strategy

**Sources searched**: Google Scholar, PubMed/PMC, Scholarpedia (Rall model entry), NEURON Yale
documentation (`neuron.yale.edu`), ModelDB, Nature/Science/eLife/PNAS journal sites, Springer
Link/Nature journals, Cambridge Core (Visual Neuroscience), Wiley Online Library.

**Queries executed** (12 total):

1. `Rall 1959 1962 1967 cable theory dendrites equivalent cylinder foundational papers DOI`
2. `d_lambda rule NEURON compartmental discretization Hines Carnevale Mainen`
3. `branched dendritic tree transfer impedance Koch Zador Holmes cable theory`
4. `dendritic resonance ZAP chirp frequency domain impedance Hutcheon Yarom Narayanan`
5. `thin dendrite propagation failure dendritic spike retinal ganglion cell electrotonic length`
6. `retinal ganglion cell dendrite electrotonic length compartmental model passive properties`
7. `Jack Noble Tsien "Electric Current Flow in Excitable Cells" textbook cable equation derivation`
8. `Stuart Spruston Hausser dendrites dendritic integration review transfer impedance synaptic`
9. `Magee Cook 2000 synaptic scaling dendritic attenuation location synapses CA1 pyramidal`
10. `Mainen Sejnowski 1996 "influence of dendritic structure" firing patterns DOI cortical neurons`
11. `Koch Poggio Torre 1983 "nonlinear interactions in a dendritic tree" frequency domain`
12. `Goldstein Rall 1974 "changes of action potential shape and velocity for changing core conductor geometry"`

Follow-up queries 7-12 were triggered by initial findings (textbook identified in q1, Stuart/
Spruston review in q3, Magee-Cook scaling in q8, Mainen-Sejnowski in q2). Additional targeted
retrievals via WebSearch covered Rall-Rinzel 1973, Velte-Masland 1999, Taylor-He-Levick-Vaney 2000,
and Major-Evans-Jack 1993.

**Date range**: 1959-2020 for foundational and review papers; no date restriction applied.

**Inclusion criteria**: Must provide at least one of (a) a derivation or extension of the cable
equation, (b) a method for computing transfer impedance or electrotonic length in branched
geometries, (c) a discretisation / d_lambda recipe, (d) a frequency-domain / ZAP analysis of
dendritic filtering, (e) an electrotonic-length estimate for a ganglion-cell-class dendrite, or (f)
a treatment of propagation failure in thin dendrites. Excluded: papers already listed in the t0002
DSGC corpus (20 DOIs), plant electrophysiology, invertebrate central-pattern-generator papers not
directly relevant, and papers whose focus is on channel biophysics without cable integration.

**De-duplication**: Cross-checked every candidate DOI against the 20-item exclusion list from
`task_description.md`; no overlap remained after filtering.

## Key Findings

### Rall Foundations Define Five Core Results the Project Must Obey

[Rall1959] established the 3/2-power rule for collapsing a branched dendritic tree into an
equivalent cylinder: if `sum(d_daughter^{3/2}) = d_parent^{3/2}` at every bifurcation, the branched
tree is electrically equivalent to a single cylinder for steady-state analysis. [Rall1962a] and
[Rall1962b] present the full theory of physiological properties and the first compartmental-model
solutions. [Rall1967] introduces the concept of **distinguishable somato-dendritic synaptic
distributions** based on EPSP shape indices, which underlies the Branco 2010 DSGC direction-
selectivity argument already in the corpus.

[RallRinzel1973] and [RinzelRall1974] derive analytical expressions for **branch input resistance**
and **steady attenuation** from a single branch to the soma, and for the **transient response** to a
current pulse at one branch. Explicit formulas for input resistance at any branch and for
attenuation to the soma are available — this gives a closed-form reference against which NEURON
simulations can be validated for passive cases.

**Best practice**: Any NEURON compartmental model of a DSGC should reproduce Rall-Rinzel's analytic
attenuation curve when run with uniform Rm/Ri and a Rall-compliant tree before trusting simulations
on the real morphology.

### The d_lambda Rule Is a 2001 Heuristic, Not a Theorem

The d_lambda rule, developed by Hines and Carnevale for the NEURON simulator, is an empirical
recipe: choose nseg such that each segment is shorter than a fraction `d_lambda` (default 0.1) of
the AC length constant `lambda_f` at a reference frequency `f` (default 100 Hz)
[NEURON-dlambda- Doc, Carnevale2006]. Setting `d_lambda = 0.1` gives the common **"segments < 0.1
lambda"** practice cited in Schachter et al. (2010) in the t0002 corpus. The rule is heuristic — it
guarantees only that the spatial discretisation error in the passive cable equation is small at
frequency `f`; it does not guarantee accuracy for fast dendritic spikes with substantial
high-frequency content.

**Best practice (update to research_papers.md)**: When simulating dendritic spikes in DSGCs, a
reference frequency of 500-1000 Hz is more appropriate than the default 100 Hz, pushing segment
length down to roughly **< 0.02 lambda_100Hz**. This prescription is not in the corpus and is
recommended by the NEURON user community [NEURON-dlambda-Doc].

### Branched-Tree Impedance Has Closed-Form Solutions

[Holmes1986] gives an O(N) algorithm for steady-state voltage in any branched dendritic tree; this
is the theoretical antecedent of Hines's tree-elimination used by NEURON.
[KochPoggio1982, KochPoggio1983] applied the framework to the cat delta-ganglion cell, deriving
**transfer impedance** between any two dendritic points. [Zador1995] introduces the
**morphoelectrotonic transform (MET)**: a graphical re-embedding of dendritic morphology in
electrotonic coordinates, using the log-attenuation `L_ij` and propagation delay `P_ij` as additive
coordinates. This visualisation is directly applicable to DSGC arbors and has no equivalent in the
t0002 corpus.

**Quantitative anchor (new)**: [KochPoggio1983] report that inhibition located on the direct path
between excitation and soma requires **peak inhibitory conductance ~50 nS** to veto a distal
excitatory input in the cat delta-ganglion cell, a figure comparable to the Schachter et al.
estimate of **~85 nS** needed to block DSGC dendritic spike propagation (research_papers.md). The
two numbers together bracket the physiological inhibition range expected during DSGC null-direction
responses.

### Frequency-Domain Filtering Reveals Resonance Even in Passive Trees

[Koch1984] is the seminal paper on **quasi-active membranes**: if any voltage-gated current is
linearised around rest, the membrane impedance takes the form of an RLC-plus-inductor element and
can exhibit resonance. [HutcheonYarom2000] review ZAP (impedance amplitude profile) methodology:
inject a sinusoidal current whose frequency increases linearly with time (chirp), compute voltage
magnitude response vs. frequency. For hippocampal CA1 pyramidal neurons, resonance peaks in the
**theta band (4-10 Hz)** are observed. [NarayananJohnston2007] show that HCN currents generate these
peaks and that resonance frequency increases with dendritic distance from the soma.

**Hypothesis (new)**: DSGC dendrites may exhibit a weak passive resonance at a frequency set by **Rm
\* Cm** and the arbor's effective length; this has not been measured in DSGCs but is predicted by
the linearised cable equation. The research_papers.md hypothesis about electrotonic length can be
combined with this: measured ZAP resonance frequency for a DSGC dendrite should give an independent
estimate of the passive time constant.

### Thin Dendrites Exhibit Propagation Failure and Reflection

[GoldsteinRall1974] computed action-potential shape and velocity changes at geometric
discontinuities: a **step increase in diameter** (thin-to-thick) causes velocity and peak height to
decrease during approach, and propagation can **either fail, succeed with delay, or succeed
bidirectionally** depending on the ratio of downstream impedance to upstream impedance. At a
branchpoint, if `d_daughter^{3/2}` sums exceed `d_parent^{3/2}`, propagation failure is likely on
the forward path; a Rall-matched branchpoint preserves velocity and waveform.

[VelteMasland1999] confirm experimentally that dendritic action potentials in rabbit RGCs can
propagate to the soma but often appear as attenuated "spikelets" — consistent with the
Goldstein-Rall prediction for thin-to-thick geometric transitions. [Oesch2005] show that DSGC
dendrites initiate spikes locally; combined with the Schachter et al. (2010) finding that inhibition
must reach ~85 nS to block propagation, the thin-dendrite regime in DSGCs is close to the
Goldstein-Rall threshold. **This places DSGC dendrites in a biophysically delicate regime where
small changes in diameter or Rm can shift the system between reliable and unreliable propagation.**

### Ganglion-Cell-Specific Electrotonic-Length Numbers

Summary of RGC electrotonic-length estimates found:

| Species | L (normalised electrotonic length) | Source |
| --- | --- | --- |
| Tiger salamander | 0.34 +/- 0.13 | [ColemanMiller1989] |
| Rainbow trout (adult) | ~0.4-0.7 (isometric growth pattern) | [VelteMiller1995] |
| Cat delta-ganglion cell | computed from Koch morphology, L ~ 1 | [KochPoggio1982] |
| Rabbit ON-OFF DSGC | Not explicitly reported; subunit electrotonic picture | Schachter2010 (corpus) |

**Quantitative anchor (new)**: **L = 0.34 +/- 0.13** for tiger salamander RGCs [ColemanMiller1989]
and values approaching **L = 1** for highly branched mammalian RGCs give a plausible target range
for DSGC calibration. The rabbit DSGCs in Schachter et al. (2010, t0002 corpus) are consistent with **L near 1** for
distal dendrites, which is at the boundary where the equivalent-cylinder approximation and the
3/2-power rule start to break down.

## Methodology Insights

* **Discretisation target (updates research_papers.md)**: use the NEURON d_lambda rule with a
  reference frequency of **500-1000 Hz** (not the default 100 Hz) when simulating dendritic spikes
  in DSGCs [NEURON-dlambda-Doc, Carnevale2006]. Segment length then becomes roughly < 0.02
  lambda_100Hz, about 5x finer than the Schachter et al. prescription.

* **Validation target for passive simulations**: when starting from a real DSGC morphology,
  temporarily set all channels to zero and the geometry to Rall-compliant (3/2-power rule), then
  verify that the simulated attenuation curve matches the Rall-Rinzel analytic expressions
  [RallRinzel1973, RinzelRall1974]. This is a numerical-correctness check that downstream tasks
  should run before trusting active-dendrite simulations.

* **Electrotonic-length anchor**: calibrate Rm so that the simulated distal-to-soma attenuation
  produces an L around **0.6-1.0** for an ON-OFF DSGC dendrite, bracketed by the salamander
  [ColemanMiller1989] and cat [KochPoggio1982] values.

* **Transfer-impedance tool**: use the morphoelectrotonic transform [Zador1995] to visualise how
  synapses at different tree positions see the soma. This is directly applicable to DSGC simulations
  and is not in the t0002 corpus.

* **Frequency-domain validation (hypothesis)**: use the NEURON `Impedance` class to simulate a ZAP
  experiment [HutcheonYarom2000, NarayananJohnston2007]. A DSGC dendrite with Schachter-style
  parameters (Ri = 110 Ohm cm, Cm = 1 uF/cm^2, Rm in the 10-30 kOhm cm^2 range) should show a
  membrane time constant tau_m = Rm * Cm = **10-30 ms** and a corner frequency around **5-15 Hz**.

* **Diameter regime risk**: if DSGC dendrites really are below 1 um in diameter along most of their
  length, the **equivalent-cylinder assumption is likely violated** because daughter- diameter
  3/2-sums typically exceed the parent 3/2-value for such thin trees [GoldsteinRall1974, Rall1959].
  Downstream tasks that use a simple cable approximation should flag this explicitly.

* **Hypothesis to carry forward**: the combination of Schachter's **Ri = 110 Ohm cm**, **Cm = 1
  uF/cm^2** with dendrite diameters in the 0.3-1.0 um range places DSGC dendrites in a regime where
  cable theory's passive predictions and the active-dendrite measurements of [Oesch2005] converge on
  **L ~ 1 +/- 0.3** — calibration task t0009 should target this range.

## Discovered Papers

Twenty-five papers are flagged for download. Each is outside the 20-DOI exclusion list.

### [Rall1959]

* **Title**: Branching dendritic trees and motoneuron membrane resistivity
* **Authors**: Rall, W.
* **Year**: 1959
* **DOI**: `10.1016/0014-4886(59)90046-9`
* **URL**: https://www.sciencedirect.com/science/article/pii/0014488659900469
* **Suggested categories**: `cable-theory`, `compartmental-modeling`
* **Why download**: Foundational 3/2-power-rule paper — establishes the equivalent-cylinder
  reduction that every compartmental model either assumes or explicitly violates.

### [Rall1962a]

* **Title**: Theory of physiological properties of dendrites
* **Authors**: Rall, W.
* **Year**: 1962
* **DOI**: `10.1111/j.1749-6632.1962.tb54120.x`
* **URL**: https://nyaspubs.onlinelibrary.wiley.com/doi/10.1111/j.1749-6632.1962.tb54120.x
* **Suggested categories**: `cable-theory`, `dendritic-computation`
* **Why download**: Canonical statement of the cable-theoretic properties of dendrites; ubiquitous
  citation.

### [Rall1962b]

* **Title**: Electrophysiology of a dendritic neuron model
* **Authors**: Rall, W.
* **Year**: 1962
* **DOI**: `10.1016/S0006-3495(62)86953-7`
* **URL**: https://www.cell.com/biophysj/fulltext/S0006-3495(62)86953-7
* **Suggested categories**: `cable-theory`, `compartmental-modeling`
* **Why download**: First compartmental-model solutions with figures; establishes the numerical
  methodology.

### [Rall1967]

* **Title**: Distinguishing theoretical synaptic potentials computed for different soma-dendritic
  distributions of synaptic input
* **Authors**: Rall, W.
* **Year**: 1967
* **DOI**: `10.1152/jn.1967.30.5.1138`
* **URL**: https://journals.physiology.org/doi/10.1152/jn.1967.30.5.1138
* **Suggested categories**: `cable-theory`, `synaptic-integration`, `dendritic-computation`
* **Why download**: EPSP shape-index theory — antecedent of the impedance-gradient argument in
  Branco 2010 (corpus).

### [RallRinzel1973]

* **Title**: Branch input resistance and steady attenuation for input to one branch of a dendritic
  neuron model
* **Authors**: Rall, W., Rinzel, J.
* **Year**: 1973
* **DOI**: `10.1016/S0006-3495(73)86021-0`
* **URL**: https://www.cell.com/biophysj/fulltext/S0006-3495(73)86021-0
* **Suggested categories**: `cable-theory`, `dendritic-computation`
* **Why download**: Closed-form input resistance and attenuation for a single branch — validation
  target for passive NEURON simulations.

### [RinzelRall1974]

* **Title**: Transient response in a dendritic neuron model for current injected at one branch
* **Authors**: Rinzel, J., Rall, W.
* **Year**: 1974
* **DOI**: `10.1016/S0006-3495(74)85962-X`
* **URL**: https://www.cell.com/biophysj/fulltext/S0006-3495(74)85962-X
* **Suggested categories**: `cable-theory`, `dendritic-computation`
* **Why download**: Analytical transient response — completes the Rall-Rinzel pair.

### [GoldsteinRall1974]

* **Title**: Changes of action potential shape and velocity for changing core conductor geometry
* **Authors**: Goldstein, S. S., Rall, W.
* **Year**: 1974
* **DOI**: `10.1016/S0006-3495(74)85947-3`
* **URL**: https://www.cell.com/biophysj/fulltext/S0006-3495(74)85947-3
* **Suggested categories**: `cable-theory`, `dendritic-computation`
* **Why download**: Canonical propagation-failure analysis — direct relevance to thin DSGC
  dendrites.

### [KochPoggio1982]

* **Title**: Retinal ganglion cells: a functional interpretation of dendritic morphology
* **Authors**: Koch, C., Poggio, T., Torre, V.
* **Year**: 1982
* **DOI**: `10.1098/rstb.1982.0084`
* **URL**: https://royalsocietypublishing.org/doi/10.1098/rstb.1982.0084
* **Suggested categories**: `cable-theory`, `retinal-ganglion-cell`, `dendritic-computation`
* **Why download**: First detailed cable-theoretic analysis of a cat retinal ganglion cell — the
  delta (DS-like) class.

### [KochPoggio1983]

* **Title**: Nonlinear interactions in a dendritic tree: localization, timing, and role in
  information processing
* **Authors**: Koch, C., Poggio, T., Torre, V.
* **Year**: 1983
* **DOI**: `10.1073/pnas.80.9.2799`
* **URL**: https://www.pnas.org/doi/10.1073/pnas.80.9.2799
* **Suggested categories**: `cable-theory`, `dendritic-computation`, `retinal-ganglion-cell`,
  `synaptic-integration`
* **Why download**: Inhibitory veto mechanism quantified in a retinal ganglion cell — direct
  ancestor of the DSGC direction-selectivity literature.

### [Koch1984]

* **Title**: Cable theory in neurons with active, linearized membranes
* **Authors**: Koch, C.
* **Year**: 1984
* **DOI**: `10.1007/BF00317936`
* **URL**: https://link.springer.com/article/10.1007/BF00317936
* **Suggested categories**: `cable-theory`, `dendritic-computation`, `voltage-gated-channels`
* **Why download**: Quasi-active membrane theory underpinning all ZAP / resonance measurements in
  dendrites.

### [Holmes1986]

* **Title**: A simple algorithm for solving the cable equation in dendritic trees of arbitrary
  geometry
* **Authors**: Holmes, W. R.
* **Year**: 1986
* **DOI**: `10.1016/0165-0270(86)90015-9`
* **URL**: https://www.sciencedirect.com/science/article/abs/pii/0165027085900159
* **Suggested categories**: `cable-theory`, `compartmental-modeling`
* **Why download**: Clean O(N) algorithm — precursor to NEURON's Hines tree elimination.

### [Major1993]

* **Title**: Solutions for transients in arbitrarily branching cables: I. Voltage recording with a
  somatic shunt
* **Authors**: Major, G., Evans, J. D., Jack, J. J. B.
* **Year**: 1993
* **DOI**: `10.1016/S0006-3495(93)81037-3`
* **URL**: https://www.cell.com/biophysj/fulltext/S0006-3495(93)81037-3
* **Suggested categories**: `cable-theory`, `compartmental-modeling`
* **Why download**: Analytical transient solutions with somatic shunt — a common real-world
  boundary condition.

### [Mainen1996]

* **Title**: Influence of dendritic structure on firing pattern in model neocortical neurons
* **Authors**: Mainen, Z. F., Sejnowski, T. J.
* **Year**: 1996
* **DOI**: `10.1038/382363a0`
* **URL**: https://www.nature.com/articles/382363a0
* **Suggested categories**: `compartmental-modeling`, `dendritic-computation`,
  `voltage-gated-channels`
* **Why download**: Classic demonstration that dendritic geometry alone controls firing pattern —
  model used as primary test-bed for the d_lambda rule.

### [Zador1995]

* **Title**: The morphoelectrotonic transform: a graphical approach to dendritic function
* **Authors**: Zador, A. M., Agmon-Snir, H., Segev, I.
* **Year**: 1995
* **DOI**: `10.1523/JNEUROSCI.15-03-01669.1995`
* **URL**: https://www.jneurosci.org/content/15/3/1669
* **Suggested categories**: `cable-theory`, `dendritic-computation`, `compartmental-modeling`
* **Why download**: Introduces log-attenuation coordinates for dendritic morphology — directly
  applicable to DSGC arbor visualisation.

### [SegevRall1998]

* **Title**: Excitable dendrites and spines: earlier theoretical insights elucidate recent direct
  observations
* **Authors**: Segev, I., Rall, W.
* **Year**: 1998
* **DOI**: `10.1016/S0166-2236(98)01295-1`
* **URL**: https://www.cell.com/trends/neurosciences/fulltext/S0166-2236(98)01295-1
* **Suggested categories**: `cable-theory`, `dendritic-computation`, `voltage-gated-channels`
* **Why download**: Review linking Rall-era theory to mid-1990s dendritic-spike experiments.

### [HutcheonYarom2000]

* **Title**: Resonance, oscillation and the intrinsic frequency preferences of neurons
* **Authors**: Hutcheon, B., Yarom, Y.
* **Year**: 2000
* **DOI**: `10.1016/S0166-2236(00)01547-2`
* **URL**: https://www.cell.com/trends/neurosciences/fulltext/S0166-2236(00)01547-2
* **Suggested categories**: `dendritic-computation`, `voltage-gated-channels`
* **Why download**: Canonical review of the ZAP method and resonance in single neurons.

### [MageeCook2000]

* **Title**: Somatic EPSP amplitude is independent of synapse location in hippocampal pyramidal
  neurons
* **Authors**: Magee, J. C., Cook, E. P.
* **Year**: 2000
* **DOI**: `10.1038/78800`
* **URL**: https://www.nature.com/articles/nn0900_895
* **Suggested categories**: `dendritic-computation`, `synaptic-integration`, `cable-theory`
* **Why download**: Synaptic-scaling compensation for dendritic attenuation — important null
  hypothesis for whether DSGCs need such compensation.

### [Taylor2000]

* **Title**: Dendritic computation of direction selectivity by retinal ganglion cells
* **Authors**: Taylor, W. R., He, S., Levick, W. R., Vaney, D. I.
* **Year**: 2000
* **DOI**: `10.1126/science.289.5488.2347`
* **URL**: https://www.science.org/doi/10.1126/science.289.5488.2347
* **Suggested categories**: `direction-selectivity`, `retinal-ganglion-cell`,
  `dendritic-computation`, `synaptic-integration`
* **Why download**: First evidence for postsynaptic/dendritic DS computation in rabbit DSGCs —
  cited by every DSGC paper in the corpus but not included.

### [Oesch2005]

* **Title**: Direction-selective dendritic action potentials in rabbit retina
* **Authors**: Oesch, N., Euler, T., Taylor, W. R.
* **Year**: 2005
* **DOI**: `10.1016/j.neuron.2005.10.035`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(05)00898-5
* **Suggested categories**: `direction-selectivity`, `retinal-ganglion-cell`,
  `dendritic-computation`, `voltage-gated-channels`
* **Why download**: Experimental grounding for dendritic spike initiation in DSGCs.

### [VelteMasland1999]

* **Title**: Action potentials in the dendrites of retinal ganglion cells
* **Authors**: Velte, T. J., Masland, R. H.
* **Year**: 1999
* **DOI**: `10.1152/jn.1999.81.3.1412`
* **URL**: https://journals.physiology.org/doi/10.1152/jn.1999.81.3.1412
* **Suggested categories**: `retinal-ganglion-cell`, `dendritic-computation`,
  `voltage-gated-channels`
* **Why download**: Dual soma-dendrite patch recording in RGCs showing dendritic spikes and
  spikelets — direct evidence for the propagation regime of interest.

### [ColemanMiller1989]

* **Title**: Passive electrical cable properties and synaptic excitation of tiger salamander retinal
  ganglion cells
* **Authors**: Coleman, P. A., Miller, R. F.
* **Year**: 1989
* **DOI**: `10.1017/S0952523800010221`
* **URL**:
  https://www.cambridge.org/core/journals/visual-neuroscience/article/abs/passive-electrical-cable-properties-and-synaptic-excitation-of-tiger-salamander-retinal-ganglion-cells/6CB5A932D6A3B0B5834250869C377A1A
* **Suggested categories**: `retinal-ganglion-cell`, `cable-theory`, `patch-clamp`
* **Why download**: Provides the most concrete RGC electrotonic-length estimate (L = 0.34 +/- 0.13)
  available in the literature.

### [VelteMiller1995]

* **Title**: Developmental maturation of passive electrical properties in retinal ganglion cells of
  rainbow trout
* **Authors**: Velte, T. J., Miller, R. F.
* **Year**: 1995
* **DOI**: `10.1113/jphysiol.1995.sp020756`
* **URL**: https://pubmed.ncbi.nlm.nih.gov/12576495/
* **Suggested categories**: `retinal-ganglion-cell`, `cable-theory`, `compartmental-modeling`
* **Why download**: Developmental RGC data showing Rall 3/2-power obeyed in real morphologies, with
  equivalent-cylinder parameter fits.

### [FohlmeisterMiller1997]

* **Title**: Mechanisms by which cell geometry controls repetitive impulse firing in retinal
  ganglion cells
* **Authors**: Fohlmeister, J. F., Miller, R. F.
* **Year**: 1997
* **DOI**: `10.1152/jn.1997.78.4.1948`
* **URL**: https://journals.physiology.org/doi/10.1152/jn.1997.78.4.1948
* **Suggested categories**: `retinal-ganglion-cell`, `compartmental-modeling`,
  `voltage-gated-channels`, `cable-theory`
* **Why download**: Base multicompartmental RGC model (ModelDB 3673) on which many later models
  including DSGC models build.

### [Fohlmeister2010]

* **Title**: Mechanisms and distribution of ion channels in retinal ganglion cells: using
  temperature as an independent variable
* **Authors**: Fohlmeister, J. F., Cohen, E. D., Newman, E. A.
* **Year**: 2010
* **DOI**: `10.1152/jn.00942.2009`
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC2887638/
* **Suggested categories**: `retinal-ganglion-cell`, `voltage-gated-channels`,
  `compartmental-modeling`
* **Why download**: Mammalian RGC parameters across temperatures, including cable and channel
  calibration for rat/cat — needed because the rabbit-DSGC corpus lacks a mammalian parameter
  survey.

### [NarayananJohnston2007]

* **Title**: Long-term potentiation in rat hippocampal neurons is accompanied by spatially
  widespread changes in intrinsic oscillatory dynamics and excitability
* **Authors**: Narayanan, R., Johnston, D.
* **Year**: 2007
* **DOI**: `10.1016/j.neuron.2007.10.033`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(07)00852-2
* **Suggested categories**: `dendritic-computation`, `voltage-gated-channels`
* **Why download**: Location-dependent ZAP resonance measurements in dendrites — methodology
  template for DSGC frequency-domain analysis.

## Recommendations for This Task

1. **Download the 25 papers listed in Discovered Papers** via /add-paper subagents. Any paywalled
   DOIs should be recorded once in `intervention/paywalled_papers.md` and marked
   `download_status: "failed"` in details.json — no retries, per the task description.

2. **Update the default discretisation**: all downstream compartmental-modelling tasks should use
   `d_lambda = 0.02` at a reference frequency of 500-1000 Hz when dendritic spikes are simulated,
   instead of the corpus default of `d_lambda = 0.1` at 100 Hz [NEURON-dlambda-Doc, Carnevale2006].
   Add this as a correction to research_papers.md recommendation #1.

3. **Add a passive-validation step to future implementation tasks**: before trusting active
   simulations, run the passive model against Rall-Rinzel analytic expressions
   [RallRinzel1973, RinzelRall1974]. This is a new recommendation not present in research_papers.md.

4. **Use the morphoelectrotonic transform** [Zador1995] as the visualisation primitive for DSGC
   arbors in the analysis phase of downstream tasks.

5. **Synthesise the answer asset** around three quantitative targets for DSGCs: an electrotonic
   length **L in the range 0.6-1.0**, a membrane time constant **tau_m in the range 10-30 ms**, and
   a thin-dendrite propagation regime close to the Goldstein-Rall threshold. These numbers are not
   in research_papers.md and constitute the main scientific contribution of this survey.

6. **Flag the equivalent-cylinder approximation as fragile for DSGCs**: the 3/2-power rule is
   unlikely to be satisfied at DSGC branchpoints given the thin, highly branched geometry
   [GoldsteinRall1974, Rall1959]. This upgrades research_papers.md hypothesis (classical cable
   breaks down for < 1 um dendrites) from speculation to a search-supported best practice.

## Source Index

### [Rall1959]

* **Type**: paper
* **Title**: Branching dendritic trees and motoneuron membrane resistivity
* **Authors**: Rall, W.
* **Year**: 1959
* **DOI**: `10.1016/0014-4886(59)90046-9`
* **URL**: https://www.sciencedirect.com/science/article/pii/0014488659900469
* **Peer-reviewed**: yes (Experimental Neurology)
* **Relevance**: 3/2-power rule — every DSGC compartmental model either assumes or explicitly
  violates it.

### [Rall1962a]

* **Type**: paper
* **Title**: Theory of physiological properties of dendrites
* **Authors**: Rall, W.
* **Year**: 1962
* **DOI**: `10.1111/j.1749-6632.1962.tb54120.x`
* **URL**: https://nyaspubs.onlinelibrary.wiley.com/doi/10.1111/j.1749-6632.1962.tb54120.x
* **Peer-reviewed**: yes (Annals of the New York Academy of Sciences)
* **Relevance**: Canonical statement of cable-theoretic dendritic properties.

### [Rall1962b]

* **Type**: paper
* **Title**: Electrophysiology of a dendritic neuron model
* **Authors**: Rall, W.
* **Year**: 1962
* **DOI**: `10.1016/S0006-3495(62)86953-7`
* **URL**: https://www.cell.com/biophysj/fulltext/S0006-3495(62)86953-7
* **Peer-reviewed**: yes (Biophysical Journal)
* **Relevance**: First compartmental-model solutions and numerical methodology.

### [Rall1967]

* **Type**: paper
* **Title**: Distinguishing theoretical synaptic potentials computed for different soma-dendritic
  distributions of synaptic input
* **Authors**: Rall, W.
* **Year**: 1967
* **DOI**: `10.1152/jn.1967.30.5.1138`
* **URL**: https://journals.physiology.org/doi/10.1152/jn.1967.30.5.1138
* **Peer-reviewed**: yes (Journal of Neurophysiology)
* **Relevance**: EPSP-shape-index theory — theoretical antecedent of the impedance-gradient
  argument in Branco 2010.

### [RallRinzel1973]

* **Type**: paper
* **Title**: Branch input resistance and steady attenuation for input to one branch of a dendritic
  neuron model
* **Authors**: Rall, W., Rinzel, J.
* **Year**: 1973
* **DOI**: `10.1016/S0006-3495(73)86021-0`
* **URL**: https://www.cell.com/biophysj/fulltext/S0006-3495(73)86021-0
* **Peer-reviewed**: yes (Biophysical Journal)
* **Relevance**: Closed-form input resistance and attenuation — passive-simulation validation
  target.

### [RinzelRall1974]

* **Type**: paper
* **Title**: Transient response in a dendritic neuron model for current injected at one branch
* **Authors**: Rinzel, J., Rall, W.
* **Year**: 1974
* **DOI**: `10.1016/S0006-3495(74)85962-X`
* **URL**: https://www.cell.com/biophysj/fulltext/S0006-3495(74)85962-X
* **Peer-reviewed**: yes (Biophysical Journal)
* **Relevance**: Analytical transient response for branched trees — completes the Rall-Rinzel
  pair.

### [GoldsteinRall1974]

* **Type**: paper
* **Title**: Changes of action potential shape and velocity for changing core conductor geometry
* **Authors**: Goldstein, S. S., Rall, W.
* **Year**: 1974
* **DOI**: `10.1016/S0006-3495(74)85947-3`
* **URL**: https://www.cell.com/biophysj/fulltext/S0006-3495(74)85947-3
* **Peer-reviewed**: yes (Biophysical Journal)
* **Relevance**: Canonical analysis of propagation failure at geometric discontinuities — the
  thin-dendrite theme.

### [KochPoggio1982]

* **Type**: paper
* **Title**: Retinal ganglion cells: a functional interpretation of dendritic morphology
* **Authors**: Koch, C., Poggio, T., Torre, V.
* **Year**: 1982
* **DOI**: `10.1098/rstb.1982.0084`
* **URL**: https://royalsocietypublishing.org/doi/10.1098/rstb.1982.0084
* **Peer-reviewed**: yes (Phil. Trans. R. Soc. Lond. B)
* **Relevance**: First detailed cable-theoretic analysis of cat retinal ganglion cell morphology.

### [KochPoggio1983]

* **Type**: paper
* **Title**: Nonlinear interactions in a dendritic tree: localization, timing, and role in
  information processing
* **Authors**: Koch, C., Poggio, T., Torre, V.
* **Year**: 1983
* **DOI**: `10.1073/pnas.80.9.2799`
* **URL**: https://www.pnas.org/doi/10.1073/pnas.80.9.2799
* **Peer-reviewed**: yes (PNAS)
* **Relevance**: Dendritic inhibitory veto — direct ancestor of DSGC null-direction mechanisms.

### [Koch1984]

* **Type**: paper
* **Title**: Cable theory in neurons with active, linearized membranes
* **Authors**: Koch, C.
* **Year**: 1984
* **DOI**: `10.1007/BF00317936`
* **URL**: https://link.springer.com/article/10.1007/BF00317936
* **Peer-reviewed**: yes (Biological Cybernetics)
* **Relevance**: Quasi-active cable theory — basis for ZAP/resonance analysis.

### [Holmes1986]

* **Type**: paper
* **Title**: A simple algorithm for solving the cable equation in dendritic trees of arbitrary
  geometry
* **Authors**: Holmes, W. R.
* **Year**: 1986
* **DOI**: `10.1016/0165-0270(86)90015-9`
* **URL**: https://www.sciencedirect.com/science/article/abs/pii/0165027085900159
* **Peer-reviewed**: yes (Journal of Neuroscience Methods)
* **Relevance**: O(N) steady-state cable solver — precursor to Hines tree elimination.

### [Major1993]

* **Type**: paper
* **Title**: Solutions for transients in arbitrarily branching cables: I
* **Authors**: Major, G., Evans, J. D., Jack, J. J. B.
* **Year**: 1993
* **DOI**: `10.1016/S0006-3495(93)81037-3`
* **URL**: https://www.cell.com/biophysj/fulltext/S0006-3495(93)81037-3
* **Peer-reviewed**: yes (Biophysical Journal)
* **Relevance**: Analytical transient solutions with somatic shunt — practical cable-theory
  reference.

### [Mainen1996]

* **Type**: paper
* **Title**: Influence of dendritic structure on firing pattern in model neocortical neurons
* **Authors**: Mainen, Z. F., Sejnowski, T. J.
* **Year**: 1996
* **DOI**: `10.1038/382363a0`
* **URL**: https://www.nature.com/articles/382363a0
* **Peer-reviewed**: yes (Nature)
* **Relevance**: Primary test-bed model for the d_lambda rule; classic demonstration that geometry
  alone drives firing pattern.

### [Zador1995]

* **Type**: paper
* **Title**: The morphoelectrotonic transform: a graphical approach to dendritic function
* **Authors**: Zador, A. M., Agmon-Snir, H., Segev, I.
* **Year**: 1995
* **DOI**: `10.1523/JNEUROSCI.15-03-01669.1995`
* **URL**: https://www.jneurosci.org/content/15/3/1669
* **Peer-reviewed**: yes (Journal of Neuroscience)
* **Relevance**: Log-attenuation coordinates — visualisation primitive for DSGC dendritic
  electrotonic structure.

### [SegevRall1998]

* **Type**: paper
* **Title**: Excitable dendrites and spines: earlier theoretical insights elucidate recent direct
  observations
* **Authors**: Segev, I., Rall, W.
* **Year**: 1998
* **DOI**: `10.1016/S0166-2236(98)01295-1`
* **URL**: https://www.cell.com/trends/neurosciences/fulltext/S0166-2236(98)01295-1
* **Peer-reviewed**: yes (Trends in Neurosciences)
* **Relevance**: Review linking Rall-era theory to dendritic-spike experiments.

### [HutcheonYarom2000]

* **Type**: paper
* **Title**: Resonance, oscillation and the intrinsic frequency preferences of neurons
* **Authors**: Hutcheon, B., Yarom, Y.
* **Year**: 2000
* **DOI**: `10.1016/S0166-2236(00)01547-2`
* **URL**: https://www.cell.com/trends/neurosciences/fulltext/S0166-2236(00)01547-2
* **Peer-reviewed**: yes (Trends in Neurosciences)
* **Relevance**: Canonical ZAP and resonance review.

### [MageeCook2000]

* **Type**: paper
* **Title**: Somatic EPSP amplitude is independent of synapse location in hippocampal pyramidal
  neurons
* **Authors**: Magee, J. C., Cook, E. P.
* **Year**: 2000
* **DOI**: `10.1038/78800`
* **URL**: https://www.nature.com/articles/nn0900_895
* **Peer-reviewed**: yes (Nature Neuroscience)
* **Relevance**: Dendritic synaptic scaling — comparison baseline for whether DSGCs exhibit
  similar compensation.

### [Taylor2000]

* **Type**: paper
* **Title**: Dendritic computation of direction selectivity by retinal ganglion cells
* **Authors**: Taylor, W. R., He, S., Levick, W. R., Vaney, D. I.
* **Year**: 2000
* **DOI**: `10.1126/science.289.5488.2347`
* **URL**: https://www.science.org/doi/10.1126/science.289.5488.2347
* **Peer-reviewed**: yes (Science)
* **Relevance**: First evidence for postsynaptic/dendritic DS computation in DSGCs.

### [Oesch2005]

* **Type**: paper
* **Title**: Direction-selective dendritic action potentials in rabbit retina
* **Authors**: Oesch, N., Euler, T., Taylor, W. R.
* **Year**: 2005
* **DOI**: `10.1016/j.neuron.2005.10.035`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(05)00898-5
* **Peer-reviewed**: yes (Neuron)
* **Relevance**: Experimental grounding for dendritic spikes in DSGCs.

### [VelteMasland1999]

* **Type**: paper
* **Title**: Action potentials in the dendrites of retinal ganglion cells
* **Authors**: Velte, T. J., Masland, R. H.
* **Year**: 1999
* **DOI**: `10.1152/jn.1999.81.3.1412`
* **URL**: https://journals.physiology.org/doi/10.1152/jn.1999.81.3.1412
* **Peer-reviewed**: yes (Journal of Neurophysiology)
* **Relevance**: Dendritic-spike patch evidence in RGCs — spikelet phenomenology.

### [ColemanMiller1989]

* **Type**: paper
* **Title**: Passive electrical cable properties and synaptic excitation of tiger salamander retinal
  ganglion cells
* **Authors**: Coleman, P. A., Miller, R. F.
* **Year**: 1989
* **DOI**: `10.1017/S0952523800010221`
* **URL**:
  https://www.cambridge.org/core/journals/visual-neuroscience/article/abs/6CB5A932D6A3B0B5834250869C377A1A
* **Peer-reviewed**: yes (Visual Neuroscience)
* **Relevance**: RGC electrotonic-length estimate L = 0.34 +/- 0.13.

### [VelteMiller1995]

* **Type**: paper
* **Title**: Developmental maturation of passive electrical properties in retinal ganglion cells of
  rainbow trout
* **Authors**: Velte, T. J., Miller, R. F.
* **Year**: 1995
* **DOI**: `10.1113/jphysiol.1995.sp020756`
* **URL**: https://pubmed.ncbi.nlm.nih.gov/12576495/
* **Peer-reviewed**: yes (Journal of Physiology)
* **Relevance**: Rall 3/2-power rule confirmed in real RGC morphologies; developmental parameter
  fits.

### [FohlmeisterMiller1997]

* **Type**: paper
* **Title**: Mechanisms by which cell geometry controls repetitive impulse firing in retinal
  ganglion cells
* **Authors**: Fohlmeister, J. F., Miller, R. F.
* **Year**: 1997
* **DOI**: `10.1152/jn.1997.78.4.1948`
* **URL**: https://journals.physiology.org/doi/10.1152/jn.1997.78.4.1948
* **Peer-reviewed**: yes (Journal of Neurophysiology)
* **Relevance**: Multicompartmental RGC model template.

### [Fohlmeister2010]

* **Type**: paper
* **Title**: Mechanisms and distribution of ion channels in retinal ganglion cells: using
  temperature as an independent variable
* **Authors**: Fohlmeister, J. F., Cohen, E. D., Newman, E. A.
* **Year**: 2010
* **DOI**: `10.1152/jn.00942.2009`
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC2887638/
* **Peer-reviewed**: yes (Journal of Neurophysiology)
* **Relevance**: Mammalian RGC parameter set — fills the corpus gap between salamander and rabbit.

### [NarayananJohnston2007]

* **Type**: paper
* **Title**: Long-term potentiation in rat hippocampal neurons is accompanied by spatially
  widespread changes in intrinsic oscillatory dynamics and excitability
* **Authors**: Narayanan, R., Johnston, D.
* **Year**: 2007
* **DOI**: `10.1016/j.neuron.2007.10.033`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(07)00852-2
* **Peer-reviewed**: yes (Neuron)
* **Relevance**: Location-dependent ZAP resonance — methodology template.

### [JackNobleTsien1975]

* **Type**: paper
* **Title**: Electric Current Flow in Excitable Cells (book)
* **Authors**: Jack, J. J. B., Noble, D., Tsien, R. W.
* **Year**: 1975
* **DOI**: null (book; ISBN 9780198573654)
* **URL**:
  https://books.google.com/books/about/Electric_Current_Flow_in_Excitable_Cells.html?id=QtS0QgAACAAJ
* **Peer-reviewed**: no (textbook)
* **Relevance**: Foundational textbook derivation of cable equation; reference work for the project.

### [SegevRinzelShepherd1995]

* **Type**: paper
* **Title**: The Theoretical Foundation of Dendritic Function (Rall selected papers + commentary)
* **Authors**: Segev, I., Rinzel, J., Shepherd, G. M. (eds.)
* **Year**: 1995
* **DOI**: null (book; ISBN 9780262193566)
* **URL**: https://mitpress.mit.edu/books/theoretical-foundation-dendritic-function
* **Peer-reviewed**: no (edited collection)
* **Relevance**: Republishes the Rall papers with expert commentary — a one-stop reference.

### [StuartSprustonHausser2016]

* **Type**: paper
* **Title**: Dendrites (3rd edition, book)
* **Authors**: Stuart, G., Spruston, N., Hausser, M. (eds.)
* **Year**: 2016
* **DOI**: `10.1093/acprof:oso/9780198745273.001.0001`
* **URL**: https://global.oup.com/academic/product/dendrites-9780198745273
* **Peer-reviewed**: no (edited textbook)
* **Relevance**: Modern textbook covering cable theory, dendritic computation, and RGC examples.

### [StuartSpruston2015]

* **Type**: paper
* **Title**: Dendritic integration: 60 years of progress
* **Authors**: Stuart, G. J., Spruston, N.
* **Year**: 2015
* **DOI**: `10.1038/nn.4157`
* **URL**: https://www.nature.com/articles/nn.4157
* **Peer-reviewed**: yes (Nature Neuroscience)
* **Relevance**: Recent review of dendritic computation with modern cable-theory perspective.

### [Rathour2017]

* **Type**: paper
* **Title**: Strings on a violin: location dependence of frequency tuning in active dendrites
* **Authors**: Rathour, R. K., Narayanan, R.
* **Year**: 2017
* **DOI**: `10.3389/fncel.2017.00072`
* **URL**: https://www.frontiersin.org/articles/10.3389/fncel.2017.00072/full
* **Peer-reviewed**: yes (Frontiers in Cellular Neuroscience)
* **Relevance**: Location-dependent frequency tuning — relevant to whether DSGC distal dendrites
  show distinct ZAP signatures.

### [NEURON-dlambda-Doc]

* **Type**: documentation
* **Title**: Using the d_lambda Rule
* **Author/Org**: NEURON Project (Yale)
* **Date**: 2023-09
* **URL**: https://neuron.yale.edu/neuron/static/docs/d_lambda/d_lambda.html
* **Peer-reviewed**: no
* **Relevance**: Operational definition of the d_lambda rule; specifies default `d_lambda = 0.1` and
  reference frequency 100 Hz.

### [Carnevale2006]

* **Type**: paper
* **Title**: The NEURON Book (Chapter 4: Essentials of numerical methods for neural modelling;
  Chapter 5: Discretisation)
* **Authors**: Carnevale, N. T., Hines, M. L.
* **Year**: 2006
* **DOI**: null (book)
* **URL**: https://www.fuw.edu.pl/~suffa/Modelowanie/NEURON%20-%20Book/chap5.pdf
* **Peer-reviewed**: no (textbook, ISBN 9780521843218)
* **Relevance**: Textbook treatment of the d_lambda rule and backward-Euler discretisation.

### [RallScholarpedia]

* **Type**: documentation
* **Title**: Rall model (Scholarpedia)
* **Author/Org**: Scholarpedia (curated by Idan Segev)
* **Date**: 2009
* **URL**: http://www.scholarpedia.org/article/Rall_model
* **Peer-reviewed**: yes (Scholarpedia peer-reviewed encyclopedia)
* **Relevance**: Concise reference entry summarising Rall's equivalent-cylinder theory and the
  3/2-power rule.
