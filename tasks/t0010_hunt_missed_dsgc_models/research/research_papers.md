---
spec_version: "1"
task_id: "t0010_hunt_missed_dsgc_models"
research_stage: "papers"
papers_reviewed: 26
papers_cited: 26
categories_consulted:
  - "compartmental-modeling"
  - "direction-selectivity"
  - "dendritic-computation"
  - "retinal-ganglion-cell"
  - "synaptic-integration"
  - "voltage-gated-channels"
  - "patch-clamp"
  - "cable-theory"
date_completed: "2026-04-20"
status: "complete"
---
# Research: Hunt for DSGC Compartmental Models Missed by Prior Tasks

## Task Objective

This task hunts for direction-selective retinal ganglion cell (DSGC) compartmental models that the
t0002 literature survey (20 papers, seeded from `project/description.md`) and the t0008 ModelDB
189347 port (which focused on Poleg-Polsky & Diamond 2016 and its siblings) may have missed. Phase
A, documented here, audits the current project paper corpus to know what is already covered as a
compartmental DSGC model, what is cited but not ported, and which author / laboratory lines must be
forward-searched in the subsequent research-internet stage. Later phases download any new papers
passing the compartmental-model inclusion bar, attempt to port any that ship public code runnable in
Python 3.12 + NEURON 8.2.7, and summarise every candidate in a single answer asset.

## Category Selection Rationale

All eight project categories from `meta/categories/` were consulted because the inclusion bar (a
compartmental DSGC model) sits at the intersection of `compartmental-modeling`,
`direction-selectivity`, and `retinal-ganglion-cell`, but evidence about a paper's model class lives
elsewhere. `dendritic-computation` is where dendritic-spike and subunit-integration evidence is
tagged [Schachter2010, Oesch2005]; `synaptic-integration` covers the AMPA/NMDA/GABA synaptic wiring
that any DSGC model must specify [Park2014, Sethuramanujam2016]; `voltage-gated-channels` flags the
Nav/Kv/Ca conductances that distinguish active-dendrite from passive-dendrite models
[Fohlmeister2010, Werginz2020]; `patch-clamp` identifies papers whose conductance measurements feed
into models even if the paper itself is experimental only [Taylor2002, Chen2009]; `cable-theory` is
retained to catch theoretical papers whose predictions constrain compartmental models
[Branco2010, KochPoggio1982]. No category was excluded, because the intent of this task is
explicitly to catch cross-category papers that a narrow `compartmental-modeling` +
`direction-selectivity` query would miss.

## Key Findings

### DSGC-Specific Compartmental Models Already in the Corpus

Four papers in the corpus present a biophysically detailed, anatomically reconstructed compartmental
DSGC model as a primary methodological contribution. **[Schachter2010]** is the seminal rabbit
ON-OFF DSGC model: a NeuronC reconstruction with thousands of compartments, Hodgkin-Huxley Nav1.6
(40 mS/cm² uniform or 45 → 20 mS/cm² gradient), Kv, Kv4, Ca, and KCa channels, AMPA (E_rev = 0 mV,
τ_rise = 0.1 ms, τ_decay = 2 ms) and GABA-A (E_rev = -65 mV, τ_decay = 10 ms) synapses, driven by an
SAC-derived presynaptic DS template at 1 mm/s across 12 directions. Reported numbers include local
input resistance **150-200 MΩ** proximally vs **>1 GΩ** distally, **~4×** amplification of DSI from
subthreshold (~0.2) to spike level (~0.8), and an 85 nS shunt threshold for inhibition to block
dendritic-spike propagation vs ~6 nS for initiation. **[PolegPolsky2016]** is the mouse DRD4 ON-OFF
DSGC NEURON model with **177 AMPAR + 177 NMDAR + 177 GABA-A + nicotinic** synapses, passive
dendrites, Jahr-Stevens NMDAR Mg²⁺ block, and the multiplicative-NMDA prediction (slope **62.5° ±
14.2°** between PD and ND PSP amplitudes). **[Hanson2019]** uses a modified Poleg-Polsky
reconstruction (Cm = 1 µF/cm², Ra = 100 Ω·cm, active Na 150/150/30 mS/cm² soma/prox/term with
stochastic HH) to demonstrate that DSGCs remain direction-tuned when SAC output is rendered
non-directional (DSI drops from 0.33 to 0.07), via a **25-30 µm** cholinergic-GABA spatial offset.
**[Jain2020]** uses the same reconstructed morphology as [PolegPolsky2016] but with Na 150/200/30
mS/cm² and stochastic HH, and shows that a soft dendritic voltage threshold (-55 to -48 mV) is
sufficient to turn weakly-tuned local voltage into strongly-tuned (DSI **0.42-0.80**) local Ca²⁺
responses, with a dendritic noise-correlation space constant **λ = 5.3 µm**.

### DSGC Compartmental Models Already Ported or In Active Port Attempt

Only one library asset has been created: `modeldb_189347_dsgc` from [PolegPolsky2016] via the t0008
port (ModelDB 189347 mirrored at `github.com/ModelDBRepository/189347`). The t0008 research-internet
stage already surveyed four public-code candidates for sibling DSGC models and reached these
conclusions: the [Hanson2019] code lives at `geoffder/Spatial-Offset-DSGC-NEURON-Model` (7 files,
Python 2 + NEURON 7 – "Phase B port target") but was not ultimately ported in t0008; [Ding2016] is
on ModelDB as entry 223890 but is a **SAC network** (not a DSGC) implemented in NeuronC — flagged
low priority; [Jain2020] has no published model repository, only Awatramani-lab calcium-imaging
analysis code at `benmurphybaum/eLife_2020_Analysis`; [Koren2017] publishes no model repository and
experimental analysis only; [Schachter2010] uses NeuronC with no NEURON mirror. t0008's single
completed port therefore leaves at least **three known-candidate DSGC NEURON models unported**
([Hanson2019], any [Jain2020] supplementary code if it exists, and any post-2020 derivative that has
not yet been cataloged).

### DSGC Models Referenced but Not as Primary Contribution

Several corpus papers cite or rely on a DSGC model without publishing a new one. **[Ding2016]** is
referenced-but-not-ported: its NeuronC network model is about **SAC** wiring, not a DSGC model per
se, and so falls outside this task's inclusion bar despite being a "compartmental" model. Likewise
**[Koren2017]** builds on a SAC model to explain cross-compartmental modulation; the compartmental
analysis is on **SAC**, not DSGC, with DSGC firing-rate measurements only downstream. **[Park2014]**
(Demb-Borghuis lab) and **[Sethuramanujam2016]** / **[Sethuramanujam2017]** (Awatramani lab) report
patch-clamp and imaging data from DSGCs that constrain the Poleg-Polsky model but publish no model
of their own. **[Taylor2002]** similarly provides conductance measurements (~6 nS leading GABA, ~6.5
nS trailing AMPA for preferred direction) that feed every DSGC compartmental model in the corpus.
**[Oesch2005]** publishes no compartmental model but supplies the canonical in vitro evidence of
dendritic Na-dependent spikes in DSGCs that [Schachter2010] then models. **[ElQuessny2021]**
analyses DSGC synaptic distributions morphologically but without a biophysical simulation.

### DSGC Compartmental-Model Papers Unambiguously Outside Scope

Several papers in the corpus have `compartmental-modeling` or a DSGC-adjacent tag but are **not**
DSGCs. **[Werginz2020]** models the **OFF-alpha T** ganglion cell axon initial segment (Nav1.6
density, AIS length), not a DSGC; its method (NEURON compartmental model) is relevant only as a port
template. **[Fohlmeister2010]** provides temperature-dependent ion-channel kinetics for generic RGCs
and is an input to any DSGC model rather than a DSGC model itself. **[PolegPolsky2011]** is a
space-clamp-error study that uses a DSGC-like morphology to warn about voltage-clamp distortion,
without publishing a DS tuning simulation. **[Branco2010]** and **[Hines1997]** are cable-theory /
simulator-infrastructure references and not DSGC models. **[Hoshi2011]** reports an **ON-DSGC**
morphology (rabbit) but with no model. This clarifies that the t0002+t0008 miss is not that these
papers exist, but that any **recent** (post-2020) DSGC compartmental model, or any repository on
GitHub/OSF/Zenodo outside ModelDB, remains to be searched by internet research.

### Quantitative Targets a Missed Model Must Be Compared Against

Any newly discovered DSGC compartmental model must be scored against the same envelope targets t0008
used. [PolegPolsky2016] reports that AP5 (NMDAR block) reduces PD PSPs by **~35%** and ND PSPs by
**~34%** (n = 19), preserving DSI; suprathreshold control DSGC counts yield a DSI envelope of
**0.7-0.85** at 1 mm/s in noise-free conditions. [Hanson2019] reports wild-type IPSC DSI **0.33 ±
0.019** (n = 6) and spike DSI consistent with PolegPolsky, with preferred-vs-null E/I temporal
offsets peaking at **50-60 ms** at 1 mm/s. [Schachter2010] provides the complementary rabbit
envelope: PSP DSI ~0.2, spike DSI ~0.8, ~4× amplification, 1:1 dendritic-to-somatic spike
propagation, and an opposing intrinsic dendritic DS on the preferred-side of roughly **DSI -0.1 to
-0.2**. The [Jain2020] local-Ca²⁺ envelope adds a finer-grained subunit constraint: σ_θ = **31.6°**
across 353 ROIs (3-4 µm each) after averaging 3-5 sets, mean per-ROI DSI **0.19 ± 0.08**, with <2.5%
of ROIs miscoding the directional hemisphere. A missed model is useful to this project only if it
can produce at least a 12-angle somatic tuning curve with DSI in [0.5, 0.95], preferred peak 30-80
Hz, null residual <15 Hz, and HWHM 50-100°; anything outside is a finding rather than a model to
port.

### Dendritic-Spike vs Passive-Dendrite Split Among DSGC Models

A subtle point the t0002 survey made but worth restating here: the DSGC modelling literature bakes
in a methodological fork. [Schachter2010] and [Oesch2005] argue that **rabbit** ON-OFF DSGCs require
voltage-gated Na in the dendrites to amplify DS from PSP to spike level, whereas [PolegPolsky2016]
writes "We did not detect dendritic spikes in DRD4 DSGCs, and our computer simulations did not
require regenerative dendritic events" for the **mouse** DRD4 subtype. [Hanson2019] and [Jain2020]
inherit the mouse Poleg-Polsky architecture but add stochastic HH Na at soma/primary/terminal
dendrites (Na 150/150-200/30 mS/cm²) while still attributing most of DS to synaptic timing rather
than dendritic spikes. Any newly discovered DSGC compartmental model therefore has to be classified
on this fork, and any port attempt must respect the original's choice rather than silently swapping
active-vs-passive dendrites. **Hypothesis**: the mouse vs rabbit DSGC compartmental literatures will
converge on an intermediate active-dendrite model in the next 3-5 years, but no such unified model
exists in the corpus as of 2026-04-20.

### Temporal Coverage and the Post-2020 Gap

The corpus has exactly three DSGC compartmental models from 2010-2016 ([Schachter2010],
[PolegPolsky2016], [Ding2016 SAC]), two derivative-model papers from 2019-2020 ([Hanson2019],
[Jain2020]), and **zero** compartmental DSGC model papers from 2021-2026. The corpus has only one
2021-2022 DSGC paper at all ([ElQuessny2021], morphological analysis without a simulation) and no
DSGC papers from 2023-2026. Given that retinal connectomics, NetPyNE, and Arbor have all matured in
the 2021-2025 window, and that groups such as Awatramani, Demb, Euler, and Fried remain active, the
a priori probability of at least one missed post-2020 DSGC compartmental model is high. This is the
primary justification for the subsequent research-internet phase of this task.

## Methodology Insights

* Use the **Poleg-Polsky + Hanson architecture** as the standard mouse DSGC NEURON template for any
  new port: Cm = **1 µF/cm²**, Ra = **100 Ω·cm**, leak reversal = **-60 mV**, stochastic HH Na **150
  / 150 / 30 mS/cm²** and K rectifier **70 / 70 / 35 mS/cm²** at soma / primary / terminal dendrites
  respectively [Hanson2019]. Any newly found model that differs by more than ~2× on these numbers is
  either a different subtype (e.g. ON-DSGC, OFF-DSGC) or out of the mouse DRD4 lineage and must be
  flagged as such in the answer asset.

* Adopt the **Schachter rabbit architecture** as the template for rabbit DSGC ports: Ri = **110
  Ω·cm**, Rm_dend = **10-22 kΩ·cm²**, dendritic Nav1.6 **40 mS/cm²** uniform (or 45 → 20 gradient),
  somatic gNa **150 mS/cm²**, AMPA τ_rise/τ_decay **0.1 / 2 ms**, GABA-A τ_rise/τ_decay **0.5 / 10
  ms**, peak compound g_exc/g_inh **6.5 / 3.5 nS** (PD) vs **2.5 / 6.0 nS** (ND) [Schachter2010].
  Rabbit ports must be scored against the rabbit envelope, not the mouse one.

* For any port, test **both uniform and gradient** dendritic Na distributions (40 mS/cm² uniform and
  45 → 20 mS/cm² gradient) as [Schachter2010] did; a single configuration is a weaker test of
  robustness. This is especially important for any newly discovered model that only reports one
  configuration.

* Use the **12-angle drifting-bar protocol** at 1 mm/s from t0008, not an 8-angle protocol, even for
  models whose original paper used 8 angles [PolegPolsky2016, Hanson2019]. t0008 has already
  established that 12 angles are needed to resolve the project's HWHM and DSI envelopes; fewer
  angles may pass the envelope flag but cannot support t0011's polar overlay plots.

* Correct any published **voltage-clamp conductance** used as a model constraint upward by
  **40-100%** for distal dendrites before using it to parameterise a model
  [Schachter2010, PolegPolsky2011]. A model that uses voltage-clamp conductances verbatim will
  systematically underestimate distal synaptic drive.

* For any port attempt, prefer a **stochastic** HH channel implementation (as in
  [Hanson2019, Jain2020]) over a purely deterministic one to preserve the trial-to-trial variability
  that determines whether a model matches experimental ROC accuracy numbers. Deterministic
  simulations pass envelope flags trivially but hide fragility.

* **Best practice**: before attempting a port, check the original paper's simulator: NEURON (native
  port), NeuronC (Schachter, Ding — non-trivial port; NeuronC is a separate language),
  MATLAB/Python-only (likely not a compartmental model in the strict sense), Arbor (new in 2020-2025
  — possible target of forward citations). Reject NeuronC → NEURON rewrites for this task unless the
  original code is small and the rewrite can be unit-tested against Figure panels.

* **Hypothesis to test in next phase**: any model from Poleg-Polsky's post-2019 CU Anschutz period,
  any post-2020 NEURON model from the Awatramani lab, any NetPyNE-based DSGC model from any lab, and
  any Arbor-based retinal model from 2022-2026 are the highest-probability hits for "missed"
  compartmental DSGCs. This hypothesis drives the author watchlist below.

## Gaps and Limitations

* **Temporal gap 2021-2026**: the project corpus has zero DSGC compartmental model papers from this
  window. Any model published in the last four years is, by construction, missed by the project. The
  internet research step must target this window preferentially.

* **Non-ModelDB repositories**: every code source for a DSGC model in the current corpus was found
  on ModelDB (189347, 223890) or GitHub (`ModelDBRepository/189347`,
  `geoffder/Spatial-Offset-DSGC- NEURON-Model`). The project has not searched OSF, Zenodo (CERN's
  long-term archive), institutional repositories (e.g. CU Anschutz Scholar, UVic Scholar, Salk
  Scholar), nor the conference-code uploads typical of Cosyne, NeurIPS, and bioRxiv supplements.

* **Simulator diversity**: all ported DSGC code in the corpus is NEURON. NetPyNE, Arbor, MOOSE,
  Brian2, and JAX-based compartmental models are not represented. A 2023-2026 paper using Arbor or
  JAX for DSGC modelling would be missed.

* **ON-DSGC and OFF-DSGC subtypes**: the corpus concentrates on ON-OFF DSGCs (the Poleg-Polsky /
  Schachter / Hanson / Jain subtype). [Hoshi2011] describes rabbit ON-DSGCs anatomically but no
  ON-DSGC compartmental model is in the corpus. OFF-DSGC compartmental models (if any exist) are
  entirely absent. This is a subtype gap rather than a literature gap alone.

* **Species breadth**: the corpus covers **mouse** (Poleg-Polsky lineage) and **rabbit**
  (Schachter). No ferret, cat, primate, or zebrafish DSGC compartmental models are in the corpus.
  Any primate DSGC model would be high-impact for the project and must be explicitly searched.

* **Forward-citation chains not yet exhausted**: the task description names five seed papers
  ([PolegPolsky2016], [Schachter2010], [Park2014], [Sethuramanujam2016], [Hanson2019]) whose forward
  citations (Google Scholar "Cited by ...") have not been fully walked. Each of these is likely to
  yield 50-300 citing papers, of which a fraction will be new DSGC compartmental models.

* **Preprint servers**: bioRxiv and arXiv q-bio.NC have not been searched for 2023-2026 preprints
  that are not yet in PubMed/Crossref. Any in-press or just-accepted DSGC model will be on bioRxiv
  first.

## Recommendations for This Task

1. **Constrain the internet search to 2021-2026 first**, using the author watchlist below. Any
   pre-2021 DSGC compartmental model is very likely already in the corpus or deliberately excluded
   (e.g., [Ding2016] as a SAC, not DSGC, model). Spending search budget on the pre-2021 tail is low
   expected yield.

2. **Search three code hosts in parallel**: ModelDB full listing (keywords `direction selective`,
   `DSGC`, `RGC`, `retina`, `starburst`, `SAC`), GitHub (`DSGC`, `retinal ganglion direction`,
   `NetPyNE direction`, `Arbor retina`, `NEURON DSGC`), and the combined OSF + Zenodo + bioRxiv
   supplements. The t0008 research-internet step searched ModelDB and GitHub but not OSF or Zenodo;
   those two hosts are the biggest source of new signal.

3. **Port only models that run in Python 3.12 + NEURON 8.2.7 or Arbor 0.12.0 without manual source
   edits other than NEURON 8.2 MOD-file boilerplate fixes**. t0008 has already documented the
   standard boilerplate fixes for ModelDB 189347; any new port that needs more than that is a
   finding rather than a port target for this task.

4. **Prioritise the [Hanson2019] port** (`geoffder/Spatial-Offset-DSGC-NEURON-Model`) as the first
   concrete port attempt. t0008 explicitly flagged this as a Phase B target but did not complete it;
   doing so in this task fills the highest-confidence gap.

5. **Record every candidate in `data/candidates.csv`** with columns: doi, first_author, year, venue,
   simulator, code_url, code_available, python3_12_compatible, ported, exclusion_reason. A single
   row per candidate, grown across ModelDB / GitHub / Scholar passes.

6. **Port attempt budget**: top 3-5 candidates by a triage score of (citation count × 0.4) +
   (recency × 0.4) + (simulator-already-installed × 0.2). List the rest as new suggestions rather
   than attempting every port.

7. **If the search yields zero new portable models**, still produce the answer asset with every
   candidate considered and its exclusion reason; also generate a suggestion for a future task to
   hand-write a NEURON port of [Schachter2010] from the NeuronC source code rather than wait for an
   upstream NEURON version that may never come.

## Author / Laboratory Watchlist for Research-Internet

The following names and labs are the highest-yield forward-search targets for the subsequent
research-internet stage. Each entry combines the task description's seed authors, the corpus's
identified authors whose papers were tagged DSGC-compartmental-adjacent, and plausible adjacent
computational-retina labs.

* **Alon Poleg-Polsky** (CU Anschutz, 2019-present) — primary author of the project's canonical DSGC
  NEURON model [PolegPolsky2016]; any post-2019 publication of his is a high-probability hit for a
  new model or derivative.
* **Michael J. Schachter** (Taylor lab, OHSU) — primary author of the canonical rabbit DSGC model
  [Schachter2010]; any post-2010 publication is in scope.
* **W. Rowland Taylor** (OHSU / Oregon National Primate Research Center) — senior author of
  [Schachter2010], [Taylor2000], [Taylor2002], [Oesch2005]; runs the parent lab for rabbit DSGC
  modelling.
* **Silvia J. H. Park, Jonathan B. Demb, Bart G. Borghuis** (Yale / Louisville) — [Park2014]
  published untuned-excitation evidence that every DSGC model inherits; any follow-up DSGC model
  from this lineage is in scope.
* **Santhosh Sethuramanujam** and **Gautam B. Awatramani** (University of Victoria) —
  [Sethuramanujam2016], [Sethuramanujam2017], [Hanson2019], [Jain2020] are all from this group; any
  post-2020 DSGC paper from this lab is very likely a hit.
* **Laura Hanson** (Awatramani lab then ...) — first author of [Hanson2019]; watch for any
  independent post-doc or PI publication.
* **Geoff deRosenroll** (Awatramani lab) — author on [Sethuramanujam2016], [Sethuramanujam2017],
  [Hanson2019], [Jain2020]; maintainer of `geoffder/Spatial-Offset-DSGC-NEURON-Model`.
* **Varsha Jain** (Awatramani lab then ...) — first author of [Jain2020].
* **Kevin L. Briggman** (caesar → NIH) — senior connectomics author on [Ding2016], [Briggman2011],
  [Sethuramanujam2017]; any post-2020 compartmental model downstream of the Briggman connectomes is
  in scope.
* **David I. Vaney** and **W. Rowland Taylor** (joint) — senior authors on [Vaney2012],
  [Taylor2000], [Sivyer2010]; high probability of review or follow-up modelling from either
  retirement-era publication.
* **Thomas Euler** (University of Tübingen) — senior author of [Oesch2005], [EulerDetwilerDenk2002];
  runs an active retina-imaging + modelling group in Germany.
* **Jonathan B. Demb** (Yale) and **Bart G. Borghuis** (Louisville) — author line on [Park2014]
  whose post-2014 work (especially 2022-2026) is not in the corpus.
* **Shelley I. Fried** (MGH / Harvard) — senior author of [Werginz2020] on RGC AIS compartmental
  modelling; adjacent rather than DSGC directly but any DSGC paper from his group would be a strong
  hit.
* **Robert G. Smith** (UPenn) — NeuronC author and co-author on [Schachter2010], [Ding2016]; any
  NeuronC-or-NEURON DSGC model from this lab post-2016 is a hit.
* **Wei Wei** (University of Chicago) — senior author of [Koren2017]; lab has active DSGC work,
  probable post-2017 modelling publications.
* **Moritz Helmstaedter** (Max Planck) — connectomics co-author on [Briggman2011]; any
  connectome-plus-biophysics DSGC paper from his group is in scope.
* **Winfried Denk** (Max Planck) — co-senior on [Briggman2011], [EulerDetwilerDenk2002]; lab
  connectomes feed downstream models.
* **Tiago Branco** (UCL) — first author of [Branco2010]; any cable-theory-plus-compartmental work on
  direction-selectivity broadly is adjacent.
* **Michael Häusser** (UCL) — co-author on [Branco2010] and [HausserMel2003]; large
  dendritic-computation lab with a history of releasing NEURON models.
* **Greg J. Stuart** (Australian National University) — senior author on [To2022]; broad
  compartmental-modelling methodology overlap.

The research-internet phase must also search the simulator names **NetPyNE**, **Arbor**, **MOOSE**,
**Brian2**, and **JAX** in conjunction with `DSGC`, `retina`, `direction-selective`, or
`ganglion cell` to catch any model whose paper does not name a specific author from the list above.

## Paper Index

### [Barlow1965]

* **Title**: The mechanism of directionally selective units in rabbit's retina.
* **Authors**: Barlow, H. B., Levick, W. R.
* **Year**: 1965
* **DOI**: `10.1113/jphysiol.1965.sp007638`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1113_jphysiol.1965.sp007638/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`
* **Relevance**: Foundational paper defining retinal direction selectivity; cited as the phenomenon
  reference every DSGC compartmental model must reproduce.

### [Branco2010]

* **Title**: Dendritic Discrimination of Temporal Input Sequences in Cortical Neurons
* **Authors**: Branco, T., Clark, B. A., Häusser, M.
* **Year**: 2010
* **DOI**: `10.1126/science.1189664`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1126_science.1189664/`
* **Categories**: `cable-theory`, `compartmental-modeling`, `dendritic-computation`
* **Relevance**: Cable-theory reference for sequence-direction selectivity via dendritic impedance
  gradients; not a DSGC model but an adjacent compartmental template for any future cortical-DS
  comparison.

### [Briggman2011]

* **Title**: Wiring specificity in the direction-selectivity circuit of the retina
* **Authors**: Briggman, K. L., Helmstaedter, M., Denk, W.
* **Year**: 2011
* **DOI**: `10.1038/nature09818`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nature09818/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`
* **Relevance**: Connectomics paper whose SAC-DSGC wiring feeds any DSGC model; no compartmental
  model itself but the experimental substrate for [Ding2016].

### [Ding2016]

* **Title**: Species-specific wiring for direction selectivity in the mammalian retina
* **Authors**: Ding, H., Smith, R. G., Poleg-Polsky, A., Diamond, J. S., Briggman, K. L.
* **Year**: 2016
* **DOI**: `10.1038/nature18609`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nature18609/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `compartmental-modeling`,
  `synaptic-integration`
* **Relevance**: Often cited as a "DSGC model" but is actually a **SAC** network model in NeuronC;
  confirms that ModelDB 223890 is out of scope for this task's DSGC inclusion bar.

### [ElQuessny2021]

* **Title**: Dendrite Morphology Minimally Influences the Synaptic Distribution of Excitation and
  Inhibition in Retinal Direction-Selective Ganglion Cells
* **Authors**: El-Quessny, M., Feller, M. B.
* **Year**: 2021
* **DOI**: `10.1523/ENEURO.0261-21.2021`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_ENEURO.0261-21.2021/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`,
  `dendritic-computation`, `patch-clamp`
* **Relevance**: Rare post-2020 DSGC paper in the corpus; morphology-focused without a biophysical
  compartmental model, so does not close the post-2020 gap.

### [EulerDetwilerDenk2002]

* **Title**: Directionally selective calcium signals in dendrites of starburst amacrine cells
* **Authors**: Euler, T., Detwiler, P. B., Denk, W.
* **Year**: 2002
* **DOI**: `10.1038/nature00931`
* **Asset**: `tasks/t0018_literature_survey_synaptic_integration/assets/paper/10.1038_nature00931/`
* **Categories**: `direction-selectivity`, `dendritic-computation`, `synaptic-integration`
* **Relevance**: Foundational two-photon demonstration of intrinsic dendritic DS in SACs; frames why
  every DSGC compartmental model separates SAC-intrinsic from DSGC-intrinsic direction selectivity.

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
* **Relevance**: Generic RGC ion-channel kinetics used as inputs to any DSGC compartmental model;
  itself not a DSGC model.

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
* **Relevance**: Modified [PolegPolsky2016] NEURON model with stochastic HH and spatial-offset
  synapses; the primary unported NEURON DSGC model (`geoffder/Spatial-Offset-DSGC-NEURON-Model`) and
  the top Phase B port candidate for this task.

### [HausserMel2003]

* **Title**: Dendrites: bug or feature?
* **Authors**: Häusser, M., Mel, B.
* **Year**: 2003
* **DOI**: `10.1016/s0959-4388(03)00075-8`
* **Asset**:
  `tasks/t0018_literature_survey_synaptic_integration/assets/paper/no-doi_HausserMel2003_s0959-4388-03-00075-8/`
* **Categories**: `dendritic-computation`, `cable-theory`
* **Relevance**: Classic review framing dendrites as computational units; supplies the conceptual
  vocabulary (subunits, nonlinear integration) used by every DSGC compartmental model discussion.

### [Hines1997]

* **Title**: The NEURON Simulation Environment
* **Authors**: Hines, M. L., Carnevale, N. T.
* **Year**: 1997
* **DOI**: `10.1162/neco.1997.9.6.1179`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1162_neco.1997.9.6.1179/`
* **Categories**: `compartmental-modeling`, `cable-theory`
* **Relevance**: NEURON simulator reference paper; cited here as the simulator-infrastructure
  baseline against which any candidate port (NetPyNE, Arbor, MOOSE, Brian2, JAX) must be compared.

### [Hoshi2011]

* **Title**: Two distinct types of ON directionally selective ganglion cells in the rabbit retina
* **Authors**: Hoshi, H., Tian, L.-M., Massey, S. C., Mills, S. L.
* **Year**: 2011
* **DOI**: `10.1002/cne.22678`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1002_cne.22678/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `patch-clamp`,
  `dendritic-computation`
* **Relevance**: Rabbit ON-DSGC morphological characterisation; flags that no ON-DSGC compartmental
  model is in the corpus, identifying a subtype gap for the internet search.

### [Jain2020]

* **Title**: The functional organization of excitation and inhibition in the dendrites of mouse
  direction-selective ganglion cells
* **Authors**: Jain, V., Murphy-Baum, B. L., deRosenroll, G., Sethuramanujam, S., Delsey, M.,
  Delaney, K. R., Awatramani, G. B.
* **Year**: 2020
* **DOI**: `10.7554/eLife.52949`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.7554_eLife.52949/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `dendritic-computation`,
  `synaptic-integration`, `compartmental-modeling`, `patch-clamp`
* **Relevance**: [PolegPolsky2016]-based NEURON model with 700-compartment voltage recording and
  soft dendritic threshold (-55 to -48 mV) producing local-DSI 0.42-0.80; no independent public code
  repository, only the analysis code at `benmurphybaum/eLife_2020_Analysis`.

### [Koren2017]

* **Title**: Cross-compartmental Modulation of Dendritic Signals for Retinal Direction Selectivity
* **Authors**: Koren, D., Grove, J. C. R., Wei, W.
* **Year**: 2017
* **DOI**: `10.1016/j.neuron.2017.07.020`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2017.07.020/`
* **Categories**: `dendritic-computation`, `direction-selectivity`, `retinal-ganglion-cell`,
  `synaptic-integration`, `voltage-gated-channels`, `patch-clamp`
* **Relevance**: Often treated as a "DSGC compartmental" paper but the compartmental modelling is
  entirely on **SACs**, with DSGC measurements downstream; correctly classed as
  referenced-but-not-ported for this task.

### [Oesch2005]

* **Title**: Direction-Selective Dendritic Action Potentials in Rabbit Retina
* **Authors**: Oesch, N., Euler, T., Taylor, W. R.
* **Year**: 2005
* **DOI**: `10.1016/j.neuron.2005.06.036`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2005.06.036/`
* **Categories**: `direction-selectivity`, `dendritic-computation`, `voltage-gated-channels`,
  `retinal-ganglion-cell`, `patch-clamp`
* **Relevance**: Patch-clamp evidence of Na-dependent dendritic spikes in rabbit DSGCs; the key
  experimental validation target for [Schachter2010] and the canonical reason an active-dendrite
  model is needed for rabbit DSGCs.

### [Park2014]

* **Title**: Excitatory Synaptic Inputs to Mouse On-Off Direction-Selective Retinal Ganglion Cells
  Lack Direction Tuning
* **Authors**: Park, S. J. H., Kim, I.-J., Looger, L. L., Demb, J. B., Borghuis, B. G.
* **Year**: 2014
* **DOI**: `10.1523/JNEUROSCI.5017-13.2014`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_JNEUROSCI.5017-13.2014/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`,
  `patch-clamp`
* **Relevance**: Establishes untuned excitation in mouse DSGCs — the experimental basis for
  [PolegPolsky2016]'s tuned-inhibition, untuned-excitation model architecture.

### [PolegPolsky2011]

* **Title**: Imperfect Space Clamp Permits Electrotonic Interactions between Inhibitory and
  Excitatory Synaptic Conductances, Distorting Voltage Clamp Recordings
* **Authors**: Poleg-Polsky, A., Diamond, J. S.
* **Year**: 2011
* **DOI**: `10.1371/journal.pone.0019463`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1371_journal.pone.0019463/`
* **Categories**: `patch-clamp`, `compartmental-modeling`, `synaptic-integration`
* **Relevance**: Space-clamp compartmental analysis; provides the 40-100% conductance-correction
  factor any DSGC model must apply to voltage-clamp-derived constraints.

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
* **Relevance**: Canonical mouse DSGC NEURON model (ModelDB 189347), already ported by t0008 as
  `modeldb_189347_dsgc`. The baseline every newly discovered model must be compared against.

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
* **Relevance**: Canonical rabbit DSGC NeuronC model; referenced-but-not-ported because NeuronC →
  NEURON rewrite is outside this task's automatic-port bar. Primary source of the rabbit envelope
  targets.

### [Sethuramanujam2016]

* **Title**: A Central Role for Mixed Acetylcholine/GABA Transmission in Direction Coding in the
  Retina
* **Authors**: Sethuramanujam, S., McLaughlin, A. J., deRosenroll, G., Hoggarth, A., Schwab, D. J.,
  Awatramani, G. B.
* **Year**: 2016
* **DOI**: `10.1016/j.neuron.2016.04.041`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.04.041/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`,
  `patch-clamp`
* **Relevance**: Patch-clamp evidence for mixed ACh/GABA co-release from SACs to DSGCs; no
  compartmental model itself, but a critical synaptic-wiring constraint for any ported or newly
  discovered DSGC model.

### [Sethuramanujam2017]

* **Title**: "Silent" NMDA Synapses Enhance Motion Sensitivity in a Mature Retinal Circuit
* **Authors**: Sethuramanujam, S., Yao, X., deRosenroll, G., Briggman, K. L., Field, G. D.,
  Awatramani, G. B.
* **Year**: 2017
* **DOI**: `10.1016/j.neuron.2017.09.058`
* **Asset**: `tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1016_j.neuron.2017.09.058/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`,
  `patch-clamp`
* **Relevance**: Patch-clamp + connectomics evidence that silent NMDAR synapses amplify low-contrast
  DS in DSGCs; no compartmental model itself, but an experimental constraint for any NMDAR
  parameterisation in a ported DSGC model.

### [Sivyer2010]

* **Title**: Synaptic inputs and timing underlying the velocity tuning of direction-selective
  ganglion cells in rabbit retina
* **Authors**: Sivyer, B., Vaney, D. I.
* **Year**: 2010
* **DOI**: `10.1113/jphysiol.2010.192716`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1113_jphysiol.2010.192716/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`,
  `patch-clamp`
* **Relevance**: Rabbit DSGC velocity-tuning patch-clamp data constraining PD/ND E/I timing offsets;
  no compartmental model itself, but supplies the velocity-tuning envelope any ported rabbit model
  must match.

### [Taylor2000]

* **Title**: Dendritic Computation of Direction Selectivity by Retinal Ganglion Cells
* **Authors**: Taylor, W. R., He, S., Levick, W. R., Vaney, D. I.
* **Year**: 2000
* **DOI**: `10.1126/science.289.5488.2347`
* **Asset**:
  `tasks/t0015_literature_survey_cable_theory/assets/paper/10.1126_science.289.5488.2347/`
* **Categories**: `direction-selectivity`, `dendritic-computation`, `cable-theory`,
  `retinal-ganglion-cell`
* **Relevance**: First cable-theoretic argument that DSGC dendrites perform local subunit
  computation; the canonical motivation for any compartmental DSGC model to include multiple
  dendritic subunits rather than a single point neuron.

### [Taylor2002]

* **Title**: Diverse Synaptic Mechanisms Generate Direction Selectivity in the Rabbit Retina
* **Authors**: Taylor, W. R., Vaney, D. I.
* **Year**: 2002
* **DOI**: `10.1523/JNEUROSCI.22-17-07712.2002`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_JNEUROSCI.22-17-07712.2002/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`,
  `patch-clamp`
* **Relevance**: Provides the ~6 nS leading GABA and ~6.5 nS trailing AMPA conductance values used
  verbatim (or after space-clamp correction) by every rabbit DSGC compartmental model, including
  [Schachter2010].

### [To2022]

* **Title**: Voltage Clamp Errors During Estimation of Concurrent Excitatory and Inhibitory Synaptic
  Input
* **Authors**: To, M.-S., Honnuraiah, S., Stuart, G. J.
* **Year**: 2022
* **DOI**: `10.1016/j.neuroscience.2021.08.024`
* **Asset**:
  `tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1016_j.neuroscience.2021.08.024/`
* **Categories**: `patch-clamp`, `compartmental-modeling`, `cable-theory`, `synaptic-integration`
* **Relevance**: Post-2020 compartmental-modelling paper on voltage-clamp error quantification;
  extends [PolegPolsky2011]'s correction factor to concurrent E/I and is relevant methodology for
  any port that uses voltage-clamp constraints.

### [Vaney2012]

* **Title**: Direction selectivity in the retina: symmetry and asymmetry in structure and function
* **Authors**: Vaney, D. I., Sivyer, B., Taylor, W. R.
* **Year**: 2012
* **DOI**: `10.1038/nrn3165`
* **Asset**: `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nrn3165/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `dendritic-computation`,
  `synaptic-integration`
* **Relevance**: Canonical review of retinal DS mechanisms; no compartmental model itself but the
  authoritative reference for the synaptic-asymmetry vs dendritic-asymmetry fork that any ported
  DSGC model must declare.

### [Werginz2020]

* **Title**: Tailoring of the axon initial segment shapes the conversion of synaptic inputs into
  spiking output in OFF-alpha T retinal ganglion cells
* **Authors**: Werginz, P., Raghuram, V., Fried, S. I.
* **Year**: 2020
* **DOI**: `10.1126/sciadv.abb6642`
* **Asset**: `tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1126_sciadv.abb6642/`
* **Categories**: `compartmental-modeling`, `retinal-ganglion-cell`, `voltage-gated-channels`,
  `patch-clamp`
* **Relevance**: NEURON compartmental model of OFF-alphaT RGC AIS with Nav1.6 density ratio ~7x and
  AIS length as the dominant firing-rate parameter; not a DSGC model but a methodology template (AIS
  compartment, Nav1.6 density, depolarisation-block constraint) for any ported DSGC model.
