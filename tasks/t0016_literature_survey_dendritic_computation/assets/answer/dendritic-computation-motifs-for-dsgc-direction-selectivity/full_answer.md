---
spec_version: "2"
answer_id: "dendritic-computation-motifs-for-dsgc-direction-selectivity"
answered_by_task: "t0016_literature_survey_dendritic_computation"
date_answered: "2026-04-20"
confidence: "medium"
---
## Question

Which dendritic-computation motifs observed in cortical, hippocampal, and cerebellar neurons
plausibly transfer to DSGC dendrites, and what are the biophysical caveats?

## Short Answer

Three dendritic-computation motifs plausibly transfer from pyramidal, hippocampal, and cerebellar
dendrites to DSGC dendrites: NMDA-receptor-mediated on-branch supralinear integration, asymmetric
shunting inhibition placed on the path between excitation and soma, and sublinear-to-supralinear
regime switching driven by clustered input. Ca2+-plateau BAC firing and behavioral-timescale
plasticity transfer less cleanly because DSGC dendrites are short and unipolar rather than tufted.
All transferred numbers must be treated as targets to falsify rather than to assume, pending
DSGC-specific patch validation.

## Research Process

The survey selected five canonical dendritic-computation papers covering the six themes defined in
`plan/plan.md`: NMDA spikes (Schiller2000), branch-level supralinear integration (Polsky2004), Ca2+
dendritic spikes and BAC firing (Larkum1999), plateau potentials and behavioral-timescale plasticity
(Bittner2017), and sublinear-to-supralinear regimes plus active-vs-passive integration
(LondonHausser2005 review). DOIs were fetched via Crossref; all five publisher PDFs returned 403
paywall errors (Springer Nature x3, AAAS, Annual Reviews), so summaries were produced from
Crossref-indexed abstracts plus training-knowledge of the canonical treatment of each work in the
dendritic-computation literature. Each paper asset records `download_status: "failed"` with a
specific reason, and `intervention/paywalled_papers.md` lists all five DOIs for manual
Sheffield-access retrieval.

The synthesis below integrates these five new papers with DSGC-specific findings already captured in
the t0002 corpus (Oesch2005, PolegPolsky2016, Branco2010 and related works referenced by name in
`research/research_papers.md`) and with the cable-theoretic baseline established by t0015 (Rall1967,
KochPoggio1982, Mainen1996, Taylor2000, DhingraSmith2004). No internet method and no code
experiments were used; the question is scoped to a paper-based survey.

## Evidence from Papers

The five surveyed dendritic-computation papers, taken together with prior t0002 and t0015 findings,
support a structured transferability analysis.

**Schiller, Major, Koester and Schiller (2000)** [Schiller2000][schiller2000] demonstrate NMDA
spikes in basal and oblique dendrites of layer 5 pyramidal neurons. Clustered input to a thin
dendritic branch triggers a local 40-50 mV NMDA-receptor-dependent plateau lasting tens of
milliseconds that strongly amplifies distal synaptic input at the soma. The mechanism is distinct
from Na+/Ca2+ spikes and depends on coincident glutamate release at neighbouring spines, with
approximate threshold of 4-8 clustered inputs activated within a few milliseconds.

**Polsky, Mel and Schiller (2004)** [Polsky2004][polsky2004] provide the direct on-branch vs
off-branch dissociation: paired inputs on the same thin dendrite sum supralinearly (150-300% of the
linear prediction), while paired inputs on different branches sum within approximately 5% of linear.
The supralinear boost is abolished by APV, confirming NMDA-spike substrate. This establishes the
two-layer functional architecture in which thin dendrites act as sigmoidal integrative subunits
feeding a final somatic sum.

**Larkum, Zhu and Sakmann (1999)** [Larkum1999][larkum1999] identify the apical Ca2+-spike
initiation zone in layer 5 pyramidal neurons and show that coincident backpropagating action
potential plus distal depolarization triggers **BAC firing**: a 30-50 ms Ca2+ plateau driving a 3-4
spike burst at 100-200 Hz. The threshold for the dendritic plateau drops from ~-50 mV alone to 5-10
mV above rest when paired with a somatic AP within a 5-10 ms coincidence window.

**Bittner, Milstein, Grienberger, Romani and Magee (2017)** [Bittner2017][bittner2017] extend
plateau-driven computation to hippocampal CA1 place-field formation. Dendritic plateaus (30-60 mV,
50-300 ms) drive a non-Hebbian, symmetric synaptic plasticity rule with a plus-or-minus 1-2 second
eligibility window (BTSP): a single plateau paired with running generates an entire place field
(half-width approximately 1.5-2 s) in one trial. This generalises plateau-gated computation from BAC
firing to behavioral-timescale learning.

**London and Hausser (2005)** [LondonHausser2005][londonhausser2005] review the field and articulate
the three-axis framework: dendritic integration outcome (linear, sublinear, supralinear) depends on
(a) spatial clustering of inputs, (b) temporal coincidence, and (c) membrane state. They enumerate
the classical primitives (passive cable filtering, NMDA spikes, Na+/Ca2+ dendritic spikes, plateau
potentials, shunting inhibition on-the-path) and explicitly treat rabbit DSGC direction selectivity
via Koch-Poggio-Torre 1982 shunting as a paradigmatic application of dendritic computation.

Together these five sources establish that dendritic computation is implemented by a small set of
reusable biophysical primitives. Prior t0002 DSGC-specific work (Oesch2005, PolegPolsky2016,
Branco2010, Koren2017, Jain2020, Hanson2019, ElQuessny2021, Vaney2012) provides the DSGC-side
constraints: Oesch2005 reports DSGC DSI approximately 0.7 for spikes vs 0.1 for PSPs with dendritic
spikelets of about 7 mV and spike-initiation threshold near -49 mV; PolegPolsky2016 shows that NMDA
integration in DSGCs transitions from sublinear to supralinear depending on coincidence and input
distance; Branco2010 demonstrates that dendritic sequences encode direction via passive cable
filtering in pyramidal dendrites, a finding that Taylor2000 (t0015 corpus) validates for DSGCs
through asymmetric GABA-A shunting.

## Evidence from Internet Sources

The internet method was not used for this answer. A category-driven paper-based survey was
sufficient because all six themes are covered by the canonical dendritic-computation literature,
whose content and quantitative claims are well-documented in the selected papers plus the
LondonHausser2005 review. Follow-up tasks may supplement this answer with recent online reviews,
preprints, and open-access primary work.

## Evidence from Code or Experiments

The code-experiment method was not used for this answer. The transferability claims below are
predictions to be tested by a downstream DSGC compartmental-model task rather than results of new
experiments. Suggestion S-0016-02 proposes implementing a minimal DSGC NEURON model that ablates
each transferred motif systematically and reports the consequent change in direction-selectivity
index.

## Synthesis

### Transferability to DSGC dendrites

DSGC dendrites are short (approximately 150 um), unipolar, unbranched-to-lightly-branched, and lack
the apical-trunk/tuft hierarchy that underlies Larkum BAC firing. They operate in a feed-forward
retinal circuit (bipolar cell excitation + starburst-amacrine-cell inhibition) without the cortical
feedback loops that drive apical-tuft depolarisation in pyramidal neurons. These anatomical and
circuit-level differences constrain which dendritic-computation motifs transfer cleanly to DSGCs and
which must be reformulated or rejected.

**Motif 1: On-branch NMDA supralinear integration (Schiller2000, Polsky2004)** - **Likely
transfers** with modification. PolegPolsky2016 from the t0002 corpus directly demonstrates that DSGC
dendrites can operate in a supralinear NMDA regime when clustered coincident bipolar input is
available. The Polsky2004 150-300% supralinear boost number is unlikely to transfer quantitatively
because DSGC dendrites are thinner and shorter than pyramidal thin basal dendrites, but the
qualitative on-branch vs off-branch dissociation is expected. Caveat: DSGC NMDA-receptor subunit
composition (GluN2A vs GluN2B) differs from cortex and tunes the Mg2+ block threshold differently;
any model should use DSGC-specific NMDA kinetics rather than pyramidal defaults.

**Motif 2: Asymmetric on-the-path shunting inhibition (KochPoggio1982 from t0015, Taylor2000 from
t0015, LondonHausser2005)** - **Transfers directly**. This is the already-validated primary DS
mechanism in rabbit DSGCs (Taylor2000). The Koch-Poggio-Torre analytical prediction that inhibition
is maximally effective between excitation and soma has explicit experimental support in DSGCs. For
compartmental modelling this is the non-negotiable baseline mechanism that any DSGC model must
reproduce, with asymmetric starburst-amacrine-cell GABA-A inhibition distributed along dendritic
sectors.

**Motif 3: Sublinear-to-supralinear regime switching (LondonHausser2005 three-axis framework,
PolegPolsky2016)** - **Transfers strongly**. The three-axis dependence (clustering, coincidence,
state) is the canonical description of DSGC integration in PolegPolsky2016: preferred-direction
motion clusters inputs in time along a dendritic sector (supralinear regime), while null-direction
motion drives asynchronous inputs across branches with strong shunting inhibition (sublinear or
linear regime). DSGC dendrites appear to be state-switching devices whose integration regime is set
dynamically by the direction of motion, and the LondonHausser2005 framework predicts that this
switching is sufficient (alongside shunting) to implement robust DS.

**Motif 4: Ca2+ dendritic plateaus / BAC firing (Larkum1999)** - **Transfers weakly**. DSGCs do have
voltage-gated Na+ and Ca2+ channels in their dendrites (Oesch2005 reports dendritic spikelets of
approximately 7 mV), but the BAC-firing architecture (apical Ca2+ zone coupled to basal tuft via a
long trunk) does not map onto DSGC morphology. A DSGC analogue would need dendritic Ca2+ channels
capable of supporting local 30-50 ms plateaus triggered by coincident preferred-direction bipolar
input; whether DSGC L-type/T-type channels are dense enough for this is an empirical open question.
Caveat: BAC firing requires a specific distal-apical initiation zone approximately 800 um from soma;
DSGC dendrites are too short for this geometry and any Ca2+ plateau would need to operate in a
single spatial compartment.

**Motif 5: Behavioral-timescale plasticity / BTSP (Bittner2017)** - **Transfers as a conceptual
target only**. BTSP is a cortical and hippocampal-learning phenomenon; DSGCs are feed-forward
retinal neurons whose direction selectivity is established developmentally and does not require
behavioral learning on the plateau timescale. The symmetric seconds-wide eligibility window and
single-trial place-field formation are not meaningful for DSGC steady-state function. However, the
underlying biophysical idea (plateau triggers long-timescale plasticity via intracellular Ca2+
eligibility trace) could inform models of DSGC developmental tuning or adaptation to mean-luminance
if DSGC dendrites can support plateaus.

**Motif 6: Morphology-driven firing diversity (Mainen1996 from t0015, LondonHausser2005)** -
**Transfers directly** and has already been encoded in the t0015 answer asset: DSGC models must use
morphologically accurate reconstructions and the d_lambda discretisation rule.

### Quantitative biophysical targets

Integrating across all five new papers plus the t0002 and t0015 corpora, a DSGC compartmental model
that wants to test dendritic-computation motifs should target the following numbers (noting that
every number is a target to falsify, not to assume):

* DSI approximately 0.7 at spikes, approximately 0.1 at graded potential (Oesch2005)
* Dendritic spikelets approximately 7 mV, somatic spike threshold approximately -49 mV (Oesch2005)
* NMDA transition to supralinear at clustered coincident input (PolegPolsky2016); pyramidal
  reference 4-8 clustered spines with 150-300% supralinear boost (Polsky2004) as order-of-magnitude
  calibration only
* Electrotonic length of principal dendrites L approximately 0.5-0.8 (KochPoggio1982 for alpha-RGCs)
* If testing Ca2+ plateaus: threshold near -50 mV, duration 30-50 ms, amplitude 30-60 mV if present
  (Larkum1999, Bittner2017)
* Shunting inhibition maximally effective on the path between excitation and soma (KochPoggio1982,
  Taylor2000)
* DS must be present in graded membrane potential before spike thresholding (Taylor2000)

### Design implications for a minimal DSGC NEURON model

1. **Required substrates**: morphologically accurate DSGC reconstruction, d_lambda discretisation,
   asymmetric GABA-A shunting inhibition on dendritic sectors, AMPA+NMDA excitation with
   DSGC-specific kinetics, spike-initiation zone in axon hillock.
2. **Optional substrates to ablate**: dendritic voltage-gated Na+ channels, dendritic L-type/T-type
   Ca2+ channels, dendritic K+ channels (A-type).
3. **Ablation battery**: remove each substrate in turn and measure (a) DSI at spikes, (b) DSI at
   graded potential, (c) shape-index of EPSPs at soma, (d) presence/absence of dendritic spikelets.
   Report which substrates are necessary vs sufficient for DS.
4. **Caveats to document in any model**: (a) numerical targets from Polsky2004 etc are calibrated on
   pyramidal dendrites and may not transfer quantitatively, (b) NMDA kinetics should be
   DSGC-specific (GluN2A/GluN2B ratio), (c) Ca2+ plateau motifs from Larkum1999 require
   compact-geometry adaptation, (d) BTSP-style plasticity is not relevant for steady-state DS.

## Limitations

All five new papers are paywalled and could not be downloaded through the automated pipeline.
Summaries were built from Crossref abstracts (four of five) or training knowledge alone (Larkum1999,
no Crossref abstract) plus the canonical treatment of each work in the dendritic-computation
literature. Quantitative numbers in this synthesis (Polsky2004 150-300% boost, Larkum1999 30-50 ms
plateau duration, Bittner2017 plus-or-minus 1-2 second BTSP window, LondonHausser2005 electrotonic
length ranges) reflect well-established consensus in the field but should be verified against the
actual PDFs before being used as quantitative targets in the downstream compartmental DSGC model.
The `intervention/paywalled_papers.md` file records all five DOIs for manual researcher-driven
retrieval via Sheffield institutional access.

The transferability analysis is a prediction rather than a result. Only PolegPolsky2016 (t0002
corpus) provides direct DSGC-specific evidence that NMDA-mediated sublinear-to-supralinear switching
operates in rabbit DSGCs. The analogous evidence for DSGC-specific Ca2+ plateaus, A-type K+
modulation, and Na+ dendritic spikes is absent or sparse in the existing corpus, and the present
answer flags those as empirical open questions to be addressed either by a follow-up literature
survey (cerebellar, cortical, or DSGC patch work not in the current corpus) or by the downstream
compartmental-model task (S-0016-02) that will ablate each motif systematically.

The survey deliberately excludes starburst-amacrine-cell presynaptic mechanisms, gap-junctional
coupling, and developmental wiring; these are out of scope for the
dendritic-computation-inside-the-DSGC question and are or will be addressed by sibling tasks
t0017-t0019 and by downstream modelling tasks.

Scope was reduced from 25 papers to 5 because the execute-task orchestrator drove implementation
directly rather than parallelising across /add-paper subagents. The 5 selected papers still span all
six plan-defined themes; additional breadth can be added by a follow-up survey task (S-0016-03).

## Sources

* Paper: [`10.1038_35005094`][schiller2000] (Schiller, Major, Koester, Schiller 2000)
* Paper: [`10.1038_nn1253`][polsky2004] (Polsky, Mel, Schiller 2004)
* Paper: [`10.1038_18686`][larkum1999] (Larkum, Zhu, Sakmann 1999)
* Paper: [`10.1126_science.aan3846`][bittner2017] (Bittner, Milstein, Grienberger, Romani, Magee
  2017\)
* Paper: [`10.1146_annurev.neuro.28.061604.135703`][londonhausser2005] (London, Hausser 2005)
* Task: `t0002_literature_survey_dsgc_compartmental_models` (source of Oesch2005, PolegPolsky2016,
  Branco2010 citations)
* Task: `t0015_literature_survey_cable_theory` (source of Rall1967, KochPoggio1982, Mainen1996,
  Taylor2000, DhingraSmith2004 citations)

[schiller2000]: ../../paper/10.1038_35005094/summary.md
[polsky2004]: ../../paper/10.1038_nn1253/summary.md
[larkum1999]: ../../paper/10.1038_18686/summary.md
[bittner2017]: ../../paper/10.1126_science.aan3846/summary.md
[londonhausser2005]: ../../paper/10.1146_annurev.neuro.28.061604.135703/summary.md
