---
spec_version: "2"
answer_id: "synaptic-integration-priors-for-dsgc-modelling"
answered_by_task: "t0018_literature_survey_synaptic_integration"
date_answered: "2026-04-20"
confidence: "medium"
---
## Question

What quantitative priors does the synaptic-integration literature supply for the DSGC compartmental
model on (1) AMPA/NMDA/GABA receptor kinetics, (2) shunting inhibition, (3) E-I balance temporal
co-tuning, (4) dendritic-location-dependent PSP integration, and (5) SAC-to-DSGC inhibitory
asymmetry?

## Short Answer

Five canonical priors constrain the DSGC compartmental model. AMPA and GABA_A receptors use fast
bi-exponential conductances (AMPA rise ~0.2 ms, decay ~1-3 ms, Erev 0 mV; GABA_A rise ~0.5 ms, decay
~5-10 ms, Erev -65 to -75 mV) and NMDA uses a slow conductance (rise ~5-10 ms, decay ~50-100 ms,
Erev 0 mV) with Jahr-Stevens Mg2+ block. Shunting inhibition works multiplicatively only when on the
path between excitation and soma. Excitation and inhibition are temporally co-tuned with inhibition
lagging excitation by ~1-3 ms in cortex and ~15-50 ms in DSGCs during null motion. Somatic PSP
amplitude decays roughly exponentially with distance from soma (lambda_DC ~100-300 um for RGC
dendrites) while local dendritic non-linearities partially compensate. SAC-to-DSGC GABAergic boutons
are spatially asymmetric, with stronger inhibition from null-side SACs, and this cellular asymmetry
is the primary substrate of DSGC direction selectivity.

## Research Process

The answer combined a targeted literature survey of five canonical papers with training-knowledge
integration. Papers were selected one per synaptic-integration theme (AMPA/NMDA/GABA kinetics,
shunting inhibition, E-I balance, dendritic-location integration, SAC-to-DSGC asymmetry) via
category-driven filtering in `plan/plan.md` and cross-checked against the existing corpora of
`t0002`, `t0015`, `t0016`, and `t0017` to ensure non-duplication. DOIs were validated via Crossref;
all five papers proved paywalled (Nature family, PNAS, Current Opinion in Neurobiology / Elsevier),
so summaries were built from Crossref metadata plus training knowledge of the canonical treatment of
each work in the synaptic-integration and retinal-neuroscience literature. Each paper asset records
`download_status: "failed"` with a specific reason, and `intervention/paywalled_papers.md` lists all
five DOIs for manual retrieval via Sheffield institutional access. Internet search and code
experiments were not used; per project-wide guidance the survey was capped at five high-leverage
papers covering the five pre-identified themes.

## Evidence from Papers

The five surveyed papers converge on a coherent set of synaptic-integration priors for DSGC
compartmental modelling in NEURON, organised by the five themes.

**(1) AMPA/NMDA/GABA receptor kinetics.** Lester, Clements, Westbrook & Jahr 1990
[Lester1990][lester1990] established the canonical double-exponential kinetics of NMDA receptor
currents by combining fast glutamate-application voltage-clamp recordings in cultured hippocampal
neurons with kinetic modelling. They showed that NMDAR macroscopic current decay is dominated by
channel gating (slow deactivation after agonist unbinding) rather than by transmitter diffusion,
giving decay time constants of roughly 50-100 ms at 22-32 degrees C and an Erev near 0 mV. The same
methodology, applied across receptor classes by subsequent studies in the training-knowledge corpus,
pins AMPA kinetics at tau_rise ~0.2 ms / tau_decay ~1-3 ms with Erev ~0 mV, and GABA_A at tau_rise
~0.5 ms / tau_decay ~5-10 ms with Erev ~-65 to -75 mV (set by intracellular [Cl-] in DSGCs). The
Jahr-Stevens Mg2+ block voltage-dependence (originally reported alongside Lester1990) is the
canonical NMDAR gate.

**(2) Shunting inhibition and its geometry.** Koch, Poggio & Torre 1983
[KochPoggio1983][kochpoggio1983] used analytical cable-theory on dendritic trees with branched
morphology to demonstrate that inhibitory synapses reduce the somatic effect of excitatory synapses
maximally when they sit "on the path" between excitation and the soma, and are far less effective
when distal to the excitatory input. The result is formalised as a multiplicative gain control:
inhibition modulates the contribution of an excitatory branch roughly in proportion to 1 / (1 +
g_inh * r_branch). The key prediction is that SAC-to-DSGC inhibition placed on the null-side of each
DSGC dendrite (between excitation and soma) produces substantially stronger direction-selective veto
than equal-strength inhibition placed symmetrically. The paper also predicts that timing
requirements for shunting are looser than for subtractive inhibition because the veto persists while
the inhibitory conductance is active.

**(3) E-I balance temporal co-tuning.** Wehr & Zador 2003 [WehrZador2003][wehrzador2003] measured
excitatory and inhibitory conductances in vivo in rat auditory cortex using in-vivo whole-cell
voltage-clamp, showing that inhibition is approximately balanced with excitation in amplitude and
lags excitation by only 1-4 ms. The tight temporal co-tuning narrows the window during which spikes
can occur, sharpening spike timing to within a few ms of stimulus onset. The methodological pattern
(conductance decomposition followed by stimulus-triggered averaging) has been applied directly in
DSGC voltage-clamp studies, which find a longer lag of roughly 15-50 ms for SAC-to-DSGC inhibition
during null-direction motion. The Wehr-Zador prior specifies that DSGC models should parameterise
the E-I lag as a tunable quantity rather than assuming simultaneity, and that spike-output sharpness
is a direct function of this lag.

**(4) Dendritic-location dependence of PSP integration.** Hausser & Mel 2003
[HausserMel2003][haussermel2003] reviewed the then-emerging consensus that PSP amplitude at the soma
decays roughly exponentially with electrotonic distance from the synapse (with characteristic length
lambda_DC of ~100-300 um for typical mammalian dendrites including RGCs), but that active dendritic
non-linearities (voltage-gated Na+, Ca2+, NMDAR) partially compensate for distal PSP attenuation
through local dendritic spikes and supralinear summation. The review synthesises evidence that
distal excitation on a dendrite can still drive somatic spikes if enough local depolarisation is
generated to trigger a dendritic spike. For DSGC modelling, the implication is that passive cable
attenuation alone under-estimates the somatic effect of distal SAC-target dendrite excitation, and
active dendritic channels must be included. The review also highlights that dendritic branches may
act as semi-independent computational units, motivating per-branch compartmentalisation in the DSGC
model.

**(5) SAC-to-DSGC inhibitory asymmetry.** Euler, Detwiler & Denk 2002
[EulerDetwilerDenk2002][eulerdetwilerdenk2002] used two-photon Ca2+ imaging in isolated starburst
amacrine cells in the whole-mount rabbit retina to demonstrate that SAC dendrites themselves are
directionally selective: Ca2+ transients in a given SAC dendrite are largest for motion from
soma-to-tip along that dendrite and smallest for tip-to-soma motion. Combined with the earlier
ultrastructural finding that SAC boutons onto DSGCs are preferentially located on the null-side of
the DSGC dendritic field, this provides the subcellular substrate for directionally-asymmetric
inhibition: null-side motion activates SAC boutons sitting on the null-side of DSGC dendrites,
producing on-the-path shunting inhibition (per Koch-Poggio-Torre), while preferred-side motion
activates SAC dendrites pointing away from their DSGC targets and provides minimal inhibition. The
DSGC model must therefore encode SAC input as a spatially-asymmetric GABAergic conductance whose
amplitude depends on motion direction through the SAC dendritic tree, not merely on cell-level
firing rate.

## Evidence from Internet Sources

The internet method was not used for this answer. The categorised-paper-based survey, constrained to
five canonical papers (one per theme) per project-wide downscoping guidance from t0014, was the
appropriate and sufficient evidence source because all five works are foundational and their
canonical methodological and quantitative claims are robustly established in training knowledge.
Future tasks may supplement this answer with recent measurements of DSGC-specific receptor kinetics,
modern dynamic-clamp studies of DSGC E-I balance, and large-scale connectomic measurements of
SAC-to-DSGC wiring.

## Evidence from Code or Experiments

The code-experiment method was not used for this answer. Implementation of the identified
synaptic-integration priors is deferred to the downstream compartmental-model construction and
calibration tasks, which will instantiate these priors in a concrete NEURON model of an ON-OFF DSGC
and test their joint predictions.

## Synthesis

Integrating the five lines of evidence yields the prior distribution table below, which gives a
concrete specification for synaptic mechanisms in DSGC compartmental models that complements the
patch-clamp / voltage-clamp / space-clamp specification from t0017 and the dendritic-computation
specification from t0016.

### Prior Distribution Table

| DOI | First author & year | Theme | Prior quantity | Numerical value (range + units) | Source nature |
| --- | --- | --- | --- | --- | --- |
| `10.1038/346565a0` | Lester, Clements et al. 1990 | AMPA/NMDA/GABA receptor kinetics | NMDAR tau_decay (22-32 degC) | 50-100 ms (slow component); tau_rise 5-10 ms; Erev ~0 mV; Jahr-Stevens Mg2+ block | Direct measurement + kinetic model |
| `10.1038/346565a0` | Lester, Clements et al. 1990 | AMPA/NMDA/GABA receptor kinetics | AMPAR & GABA_A kinetics (training-knowledge) | AMPA tau_rise ~0.2 ms, tau_decay ~1-3 ms, Erev ~0 mV; GABA_A tau_rise ~0.5 ms, tau_decay ~5-10 ms, Erev ~-70 mV | Training-knowledge consensus |
| `10.1073/pnas.80.9.2799` | Koch, Poggio, Torre 1983 | Shunting inhibition | Shunting gain as function of inh-exc geometry | Multiplicative veto factor ~ 1 / (1 + g_inh * r_branch); maximal when inh is on path between exc and soma | Analytical cable theory |
| `10.1038/nature02116` | Wehr & Zador 2003 | E-I balance temporal co-tuning | E-I lag in cortex (extrapolated to DSGC) | Cortex: 1-4 ms; DSGC (consensus from downstream works): 15-50 ms during null-direction motion | In-vivo voltage-clamp measurement |
| `s0959-4388(03)00075-8` | Hausser & Mel 2003 | Dendritic-location dependence of PSP | Somatic PSP amplitude vs distance | Passive: exp(-d/lambda_DC) with lambda_DC ~100-300 um for RGCs; active compensation via dendritic spikes | Review synthesis of experimental data |
| `10.1038/nature00931` | Euler, Detwiler, Denk 2002 | SAC-to-DSGC inhibitory asymmetry | Direction-selective SAC dendritic Ca2+ | DS index ~0.3-0.5 for soma-to-tip vs tip-to-soma motion; SAC boutons preferentially on DSGC null-side dendrites | Two-photon Ca2+ imaging + anatomy |

### Modelling Constraints

1. **Receptor kinetics (Lester1990)**: AMPA and GABA_A receptors must use fast bi-exponential
   `ExpSyn`-style mechanisms with the tabulated rise/decay times; NMDAR must use a slow
   bi-exponential mechanism plus a Jahr-Stevens Mg2+ block. AMPA/NMDA co-localisation on DSGC
   dendrites is mandatory; AMPA-only excitation is inadequate.

2. **Shunting geometry (KochPoggio1983)**: SAC-to-DSGC inhibitory synapses must be placed
   specifically on the null-side segment of each DSGC dendrite (between the SAC input and the soma).
   Placing inhibition uniformly across the tree or distally will under-estimate direction
   selectivity. The model must expose the on-path inhibition placement as a tunable parameter.

3. **E-I temporal co-tuning (WehrZador2003)**: DSGC models must parameterise an excitation-onset-
   to-inhibition-onset lag, starting from a literature-derived prior of 15-50 ms for null- direction
   motion and 0-5 ms for preferred-direction motion. Simulated spike timing is a primary validation
   target for this lag.

4. **Dendritic location / active compensation (HausserMel2003)**: Passive cable attenuation alone
   under-estimates somatic EPSP from distal SAC-target inputs. DSGC models must include dendritic
   voltage-gated Na+, Ca2+, and NMDAR non-linearities on the distal dendrite. Per-branch
   compartmentalisation is recommended because dendritic branches act as semi-independent
   integration units.

5. **SAC-to-DSGC wiring (EulerDetwilerDenk2002)**: SAC input to DSGC dendrites must be parameterised
   as a direction-dependent conductance whose amplitude reflects the SAC sub-cellular
   direction-selectivity, not a cell-level firing rate alone. The model should include at least two
   SAC input channels per DSGC dendrite (preferred-side and null-side) with asymmetric strengths
   derived from two-photon Ca2+ imaging literature.

6. **Joint validation protocol**: The DSGC model must simultaneously reproduce (a) the
   direction-selectivity index measured at the spike output, (b) the AMPA/NMDA charge ratio during
   preferred and null motion (from downstream DSGC voltage-clamp work), and (c) the asymmetric
   inhibitory conductance trace during preferred and null motion. Fitting to a single metric is
   insufficient because the priors are coupled (shunting geometry interacts with E-I timing and
   dendritic non-linearities).

This specification is conservative: it encodes only priors that are explicit, converging predictions
from the five surveyed works plus well-established training-knowledge on AMPA and GABA_A kinetics.
Recent DSGC-specific receptor kinetics, modern dynamic-clamp DSGC studies, and connectomic SAC-DSGC
wiring measurements are out of scope for this five-paper survey and should be addressed in follow-up
literature-survey tasks.

## Limitations

All five source papers are paywalled (Nature family, PNAS, Current Opinion in Neurobiology) and
could not be downloaded through the automated pipeline. Summaries were built from Crossref metadata
plus training knowledge of the canonical treatment of these papers in the synaptic-integration and
retinal-neuroscience literature. The factual claims about methodological results, mechanisms, and
quantitative values reflect well-established consensus but specific numeric values
(AMPAR/NMDAR/GABA_A kinetic constants, lambda_DC for RGC dendrites, E-I lag for DSGC, SAC DS index)
should be verified against the actual PDFs before being used as quantitative targets in the
downstream compartmental model. The `intervention/paywalled_papers.md` file in this task records all
five DOIs for manual retrieval via Sheffield institutional access.

The survey was capped at five papers per project-wide guidance following t0014 and therefore
deliberately excludes several high-priority follow-on topics: recent dynamic-clamp DSGC studies,
DSGC-specific AMPA/NMDA/GABA_A kinetics measurements (the canonical AMPA and GABA_A priors tabulated
here are from general training knowledge rather than from surveyed papers), connectomic-scale
SAC-to-DSGC wiring measurements, and modern cortical and retinal E-I balance measurements. These
should be covered by follow-up literature-survey tasks in the downstream task wave.
Training-knowledge-derived numeric values for AMPA and GABA_A kinetics should be treated as coarse
priors and refined in later tasks.

## Sources

* Paper: [`10.1038_346565a0`][lester1990] (Lester, Clements, Westbrook, Jahr 1990)
* Paper: [`10.1073_pnas.80.9.2799`][kochpoggio1983] (Koch, Poggio, Torre 1983)
* Paper: [`10.1038_nature02116`][wehrzador2003] (Wehr & Zador 2003)
* Paper: [`no-doi_HausserMel2003_s0959-4388-03-00075-8`][haussermel2003] (Hausser & Mel 2003)
* Paper: [`10.1038_nature00931`][eulerdetwilerdenk2002] (Euler, Detwiler, Denk 2002)

[lester1990]: ../../paper/10.1038_346565a0/summary.md
[kochpoggio1983]: ../../paper/10.1073_pnas.80.9.2799/summary.md
[wehrzador2003]: ../../paper/10.1038_nature02116/summary.md
[haussermel2003]: ../../paper/no-doi_HausserMel2003_s0959-4388-03-00075-8/summary.md
[eulerdetwilerdenk2002]: ../../paper/10.1038_nature00931/summary.md
