---
spec_version: "1"
task_id: "t0078_bedb_mobo_v2_ais_tiered_ahp"
research_stage: "internet"
searches_conducted: 14
sources_cited: 20
papers_discovered: 7
date_completed: "2026-05-03"
status: "complete"
---
# Research Internet: Bed B v2 MOBO with AIS, Tier-Stratified Channels, and Slow Kv-AHP

## Task Objective

Run a ~47-d multi-objective Bayesian optimisation (qLogNEHVI, BoTorch) on the de Rosenroll 2026 Bed
B DSGC compartmental model in NEURON, augmented with (1) a bio-realistic two-subsegment AIS, (2)
tier-stratified channel densities for Nav1.6 / Kv3 / NaP / BK / SK across five compartment tiers,
and (3) a slow Kv-mediated AHP via SK_E2 with extended Ca-binding kinetics. Pass criterion: locate
at least one Pareto cell with DSI >= 0.4 AND PD rate >= 30 Hz, OR rule it out architecturally.

## Gaps Addressed

The `research_papers.md` Gaps and Limitations section identifies six gaps. This internet research
stage targets the three highest-priority gaps and partially resolves a fourth:

1. **Hay 2011 / Khaliq 2003 SK and Ca-dynamics primary sources missing from the corpus** —
   **Partially resolved**. The Hay et al. 2011 PLOS Comput. Biol. paper [Hay2011] is the source of
   `SK_E2.mod` and `CaDynamics_E2.mod`; Khaliq et al. 2003 J. Neurosci. [Khaliq2003] is the source
   of `bkpkj.mod` (BK). Both are flagged for inclusion in the corpus (see Discovered Papers). The
   `SK_E2.mod` kinetics derive from Köhler et al. 1996 Science [Kohler1996-Sci] (cloning +
   functional characterisation of SK1/2/3), not yet in corpus. The sAHP kinetics review by Larsson
   2013 [Larsson2013] confirms that mammalian sAHP decay is on the **seconds** timescale and the
   rise on **hundreds of milliseconds**, with the time constant set by downstream KCNQ-channel
   opening rather than direct Ca-binding kinetics — a non-trivial nuance for the
   `tau_ca_multiplier` design choice (see Methodology Insights).

2. **BoTorch / qLogNEHVI / hypervolume methodology** — **Resolved**. The Ament, Daulton, Eriksson,
   Balandat, Bakshy 2023 NeurIPS paper [Ament2023] introduces `qLogNEHVI` as the numerically-stable
   replacement for `qNEHVI`. The BoTorch source code [BoTorch-logei-GH] confirms that
   `qLogNoisyExpectedHypervolumeImprovement` directly subclasses
   `qLogExpectedHypervolumeImprovement` with `_log = True`, and exposes `tau_max = 1e-3` and
   `tau_relu` smoothing parameters from the Ament paper's "fat-tailed nonlinearities" (Fat Softplus,
   Fat Maximum, Fat Sigmoid). BoTorch tutorial [BoTorch-MOBO-Tut] provides direct migration
   guidance: "It is strongly recommended to simply replace `qNoisyExpectedHypervolumeImprovement`
   with `qLogNoisyExpectedHypervolumeImprovement`, which fixes the issues and has the same API."

3. **Joint DSI + 1-second mean PD firing rate measurements in mouse / rabbit DSGCs** — **Resolved
   (with surprise)**. Rivlin-Etzion, Wei, Feller 2012 Neuron [RivlinEtzion2012] reports BOTH metrics
   for the same cells (n = 16) using two-photon-targeted loose-patch recordings of mouse DRD4-GFP
   and TRHR-GFP ON-OFF DSGCs: **DSI 0.78 ± 0.19 (stable cells), DSI 0.63 ± 0.23 (reversed
   cells)**, paired with **mean firing rate 10.38 ± 8.53 Hz (stable) and 9.95 ± 5.42 Hz (reversed)
   over a 3 s grating window**. This contradicts the "30-80 Hz" project domain-knowledge ceiling.
   The 1-s mean PD firing rate of mouse ON-OFF DSGCs is approximately **10 Hz**, not 30-80 Hz.
   Trenholm et al. 2013 J. Neurosci. [Trenholm2013] gives peak (not mean) preferred-direction spike
   rates of **198 ± 14 Hz** with null at **27 ± 12 Hz** in mouse Hb9::eGFP DSGCs (peak rate,
   cell-attached, picrotoxin baseline). Wienbar & Schwartz 2022 Neuron [Wienbar2022] reports peak
   rebound firing **>60 Hz for alpha-OFF cells, <40 Hz for alpha-ON cells** in mouse RGCs
   (current-injection, not light-evoked). Werginz, Király, Zeck 2024 J. Neurosci. [Werginz2024]
   reports maximum sustained firing of **270-278 Hz at breakdown for sustained alpha-ON/OFF and 346
   Hz for transient alpha-OFFt RGCs** under somatic current injection.

4. **Werginz 2020 Sci Adv NEURON code availability** — **Partially resolved (no code link
   verified, paper still paywalled)**. Direct ModelDB / Zenodo / GitHub searches did not surface a
   public Werginz 2020 model artefact. Wienbar & Schwartz 2022 [Wienbar2022] does provide a
   Zenodo-deposited NEURON model archive [SchwartzNU-Zenodo] (DOI `10.5281/zenodo.6423531`, "Other
   (Open)" license) with explicit **AIS lengths 22 um (OFFsA) vs 16 um (bSbC)**, **AIS diameter ~1.3
   um**, **Nav1.6 fraction 40 % / 0 %**, total Na conductance 200 nS / 150 nS. This is a directly
   portable AIS attachment template for the t0078 substrate.

The remaining gaps from `research_papers.md` (Fohlmeister 2010 species mismatch with mouse DSGC,
absence of dedicated RGC patch-clamp AHP kinetics paper) are noted but not addressed by internet
search alone — the Werginz 2024 αRGC paper [Werginz2024] partially fills the channel-density gap
with an updated mouse-RGC tier-stratified table.

## Search Strategy

**Sources searched**: Google Scholar (via WebSearch), arXiv, ModelDB, BoTorch documentation/source
code, BoTorch GitHub Discussions, eLife, J. Neurosci., PLOS Comput. Biol., PubMed Central, Zenodo,
ResearchGate. **Date range**: 2002-2026 for primary literature; no restriction for foundational
Köhler 1996 / Khaliq 2003. **Inclusion criteria**: Must provide at least one of: (a) NEURON /
MOD-file source for SK_E2 or BK with explicit Ca-binding kinetics, (b) BoTorch qLogNEHVI methodology
or migration guidance, (c) joint DSI + PD firing rate measurements in same DSGC recording, (d)
AIS-length / Nav1.6 density priors in mouse RGCs, (e) tier-stratified channel-density tables for
mouse RGCs. Excluded: papers on other species not generalisable (zebrafish, Drosophila), papers on
RGC types other than ON-OFF DSGCs without biophysical relevance, AIS papers in non-RGC contexts
(cortical, motor neurons) unless directly methodological. **Search iterations**: Pass 1 targeted the
three named gaps directly; Pass 2 broadened to AIS attachment NEURON patterns and tier-stratified
data; Pass 3 snowballed off discovered citations (Wienbar 2022 found via "RGC AIS NEURON model";
Werginz 2024 found via "alpha RGC mouse intrinsic firing 2024"). Queries 6, 11, 12 were follow-ups
triggered by findings in queries 1-5; query 14 was triggered by the explicit firing-rate finding in
query 9.

**Queries executed (14 total)**:

Gap-targeted queries:

1. `Hay 2011 PLOS Computational Biology L5b pyramidal SK_E2.mod Köhler 1996 calcium binding kinetics`
2. `SK_E2 NEURON MOD ModelDB Köhler 1996 small-conductance calcium-activated potassium kinetics tau_ca`
3. `slow afterhyperpolarisation retinal ganglion cells time constant SK channel adaptation`
4. `Khaliq Raman 2003 Purkinje cell resurgent sodium NaR JNeurosci 23 4899`
5. `qLogNoisyExpectedHypervolumeImprovement BoTorch Ament 2023 NeurIPS log-space monte carlo`
6. `"qLogNoisyExpectedHypervolumeImprovement" BoTorch documentation tau_max tau_relu Ament`

Joint DSI + firing-rate queries:

7. `Trenholm Awatramani 2013 ON-OFF DSGC mouse direction selectivity firing rate`
8. `Kim 2022 mouse DSGC direction-selective ganglion cell preferred direction firing rate intracellular`
9. `retinal ganglion cell direction selectivity index preferred direction firing rate spike count mouse moving bar`
10. `Sivyer Williams 2013 active dendritic integration DSGC rabbit firing rate spikes preferred direction`
11. `"On-Off DSGC" mouse retina firing rate Hz spikes per second preferred direction whole-cell recording`
12. `"9.95" OR "10.38" Hz baseline firing rate ON-OFF DSGC reversed direction selective ganglion cell two-photon`

Snowball queries (AIS / tier-stratified / mouse RGC channel densities):

13. `Wienbar Schwartz 2022 AIS NEURON model RGC Nav1.6 Nav1.2 length depolarization block`
14. `"alpha RGC" mouse intrinsic excitability spike frequency adaptation Nav1.6 axon initial segment 2023 2024`

Deep-fetch follow-ups: `arxiv.org/html/2310.20708v2` (Ament2023 paper full text);
`botorch.readthedocs.io/.../multi_objective/logei.html` (qLogNEHVI source code);
`pmc.ncbi.nlm.nih.gov/articles/PMC6705162` (Trenholm2013 abstract + numbers);
`pmc.ncbi.nlm.nih.gov/articles/PMC3496185` (Rivlin-Etzion 2012 paired DSI + rate);
`pmc.ncbi.nlm.nih.gov/articles/PMC9262831` (Wienbar 2022 AIS model);
`pmc.ncbi.nlm.nih.gov/articles/PMC11714343` (Werginz 2024 αRGC channel table);
`pmc.ncbi.nlm.nih.gov/articles/PMC3552283` (Larsson 2013 sAHP review);
`pmc.ncbi.nlm.nih.gov/articles/PMC6377229` (Hanson/Sethuramanujam 2019 paired DSI + spike rate);
`zenodo.org/records/6423531` (Wienbar2022 model archive).

## Key Findings

### qLogNEHVI Numerically Stabilises High-Dimensional Hypervolume Improvement

The Ament et al. 2023 NeurIPS paper [Ament2023] addresses a long-standing failure mode of EI- family
acquisition functions: "EI variants are challenging to optimize because their acquisition values
vanish numerically in many regions." The authors prove that LogEI variants have "identical or
approximately equal optima as their canonical counterparts, but are substantially easier to optimize
numerically," and extend the LogEI machinery to qEHVI for batch multi- objective settings. The
benchmarks in Section 5 of Ament2023 cover **100-D Hartmann embedded in 100-D**, **100-D rover
trajectory**, and **103-D SVM hyperparameter tuning** — empirically validating numerical stability
past 50 dimensions. This is directly relevant to the t0078 ~47-d input space.

The technical fix is a smooth approximation of the discrete max operator using "fat-tailed
nonlinearities" (Fat Softplus, Fat Maximum, Fat Sigmoid) that maintain non-vanishing gradients even
when the canonical EHVI value is numerically zero (Appendix A.4 of [Ament2023]). The BoTorch
implementation [BoTorch-logei-GH] exposes these as `tau_max = 1e-3` (smoothing of the max operator)
and `tau_relu` (smoothing of the ReLU step in the dominated-region indicator).

The BoTorch tutorial documentation [BoTorch-MOBO-Tut] gives unambiguous migration guidance: **"It is
strongly recommended to simply replace `qNoisyExpectedHypervolumeImprovement` with
`qLogNoisyExpectedHypervolumeImprovement`, which fixes the issues and has the same API."** No
code-level changes other than the class name are required for the t0078 migration. The BoTorch
source code [BoTorch-logei-GH] confirms qLogNEHVI inherits from `NoisyExpectedHypervolumeMixin` and
`qLogExpectedHypervolumeImprovement` with identical 14-parameter API to qNEHVI plus the new
`tau_max`, `tau_relu`, and `fat` arguments.

**Best practice (community consensus)**: Use qLogNEHVI as the default for any new BoTorch MOBO
project; qNEHVI is now considered legacy. Wrap GP inputs in a `Normalize` transform on `[0,1]^d`.
Use a `Standardize` outcome transform to normalise the GP targets. The BoTorch discussion thread
[BoTorch-Discussion-2791] confirms that the BoTorch maintainers themselves recommend qLogNEHVI over
qNEHVI in the official cookbook.

**Hypothesis (testable in t0078)**: GP fit warnings observed in t0076 (Botorch warned the fit was
"suboptimal" because raw natural-units bounds were passed) will disappear when (a) inputs are
wrapped in `Normalize([0,1]^d)` and (b) qLogNEHVI replaces qNEHVI. If GP fit warnings persist, the
issue is with input-dimensionality scaling (47 d vs 25 d) rather than the acquisition function.

### Mouse ON-OFF DSGC Mean PD Firing Rate is ~10 Hz, Not 30-80 Hz

This is the single most surprising finding of the internet research stage and directly contradicts
the project's "30-80 Hz" domain-knowledge target. Rivlin-Etzion, Wei, Feller 2012 Neuron
[RivlinEtzion2012] is the cleanest joint DSI + PD-rate measurement paper located:

| Metric | Stable cells (n=8) | Reversed cells (n=8) | Conditions |
| --- | --- | --- | --- |
| DSI (pre-adapt) | **0.78 ± 0.19** | **0.63 ± 0.23** | Polar plot at 8 directions |
| Mean PD firing rate (pre-adapt) | **10.38 ± 8.53 Hz** | **9.95 ± 5.42 Hz** | 3 s grating window |
| Mean PD firing rate (post-adapt) | 5.85 ± 5.31 Hz | 2.73 ± 2.68 Hz | 3 s window |

Recordings: two-photon-targeted loose-patch (cell-attached) on DRD4-GFP and TRHR-GFP mouse ON-OFF
DSGCs, gratings at the cell's preferred direction. Both DSI and PD rate are reported for the same
cells.

This is concordant with broader DSGC literature: the search results [Webvision-DSGC] note that
direction-selective cells with significant motion responses have mean firing rates of **5 ± 2 Hz**
versus **1.5 ± 1 Hz** for non-significant peaks. Trenholm et al. 2013 [Trenholm2013] gives **peak**
(not mean) PD spike rates of **198 ± 14 Hz** with null at **27 ± 12 Hz** in mouse Hb9::eGFP DSGCs
in picrotoxin — peak DSI of (198-27)/(198+27) = **0.76**. The 198 Hz peak collapses to a much
lower 1-s mean once the bar exits the receptive field.

Hanson, Sethuramanujam, deRosenroll, Awatramani 2019 eLife (corpus 10.7554_eLife.42392) [Hanson2019]
provides paired DSI + spike rate from cell-attached recordings, with DSI 0.33 ± 0.019 (n=6) under
wild-type GABAergic conditions and DSI 0.07 ± 0.02 (n=7) in Gabra2 KO + ChR2 optogenetic
stimulation. Firing rates are presented in convolved spike-density plots (sigma = 25 ms) but not
tabulated as 1-s means — Figure 3 gives qualitative paired comparison.

**Updates to `research_papers.md`**: The "30-80 Hz mean PD rate" project domain-knowledge claim is
**not supported** by any peer-reviewed source we could locate. The realistic mouse ON-OFF DSGC mean
PD rate over a 1-s or 3-s window is **~5-15 Hz**. The t0078 BO target should be re- calibrated: a
Pareto cell with DSI >= 0.4 AND PD rate >= 10 Hz would be a strong project result; the >= 30 Hz
threshold is supraphysiological at 1-s mean. Peak rates of 100-200 Hz are biologically attested
(Trenholm 2013, Oesch 2005) but only over sub-second peri-stimulus windows. Wienbar & Schwartz 2022
[Wienbar2022] reports peak rebound firing >60 Hz for alpha-OFF RGCs and Werginz 2024 [Werginz2024]
reports breakdown firing of 270-346 Hz for alpha RGCs under sustained current injection — but
neither study uses moving-bar visual stimulation.

**Hypothesis (testable in t0078)**: Re-targeting the BO utopia point to (DSI 0.7, PD rate 15 Hz)
instead of (DSI 0.7, PD rate 80 Hz) will yield a much smaller hypervolume for any given Pareto
front, but will also be more biologically meaningful. The currently-defined utopia point of (0.7, 80
Hz) implicitly demands supraphysiological 1-s firing rates that no published mouse DSGC measurement
supports.

**Contradiction**: The project domain-knowledge claim of 30-80 Hz mean PD rate appears to conflate
(a) peak firing rates from Trenholm 2013 / Oesch 2005, which are 100-200+ Hz over sub- second
windows, with (b) 1-s or longer mean rates from Rivlin-Etzion 2012 / Hanson 2019 / Webvision, which
are 5-15 Hz. The "30-80 Hz" range falls between these two regimes and may have been misattributed.

### Slow AHP Time Constants Are 1-3 Seconds, Set by Calcium-Sensor Pathway

Larsson 2013 [Larsson2013] reviews the kinetics of the slow afterhyperpolarisation across mammalian
central neurons. Key findings updating `research_papers.md`'s gap on SK / KAHP kinetics:

* sAHP development time constant: **hundreds of milliseconds**
* sAHP decay time constant: **seconds** (typically 1-3 s in CA1 pyramids)
* The slow timescale is **NOT** primarily controlled by Ca-binding kinetics of the SK channel
  itself. SK channels activate within tens of milliseconds in oocyte expression systems (12.9 ± 1.6
  ms time constant for rSK2 [Hirschberg1998-Sci]; 6.3 ms at 10 µM Ca, 20 ms at 1 µM Ca
  [Kohler1996-Sci]).
* The slow phase is dominated by **downstream signalling** through diffusible Ca-sensor proteins
  like hippocalcin, which then activate KCNQ-like channels with seconds-scale opening kinetics.
* The Köhler 1996 SK channel itself is a **fast** Ca sensor (~10 ms tau), not a slow one.
* In RGCs specifically, slow contrast adaptation is partially **presynaptic**, with bipolar-cell
  glutamate release adaptation and delayed-rectifier K+ channels contributing alongside any somatic
  SK / KAHP component [Manookin2006-Neuron, Wark2011-PMC].

**Implication for the t0078 SK_E2 `tau_ca_multiplier` design**: The current proposed range [1, 20x]
takes the t0074 default `taur = 5 ms` Ca-pool decay up to ~100 ms — this captures the **rise**
phase of sAHP but not the **decay** phase. A multiplier of 20x giving taur ~100 ms is biologically
plausible for a fast SK component but does not reach the 1-3 s decay range of true sAHP. **The
realistic option space is wider**: either (a) extend `tau_ca_multiplier` range to [1, 200x] giving
taur up to ~1 s, or (b) accept that SK_E2 + extended Ca-binding cannot reproduce a true sAHP and add
a separate KCNQ-like slow K+ mechanism (a `KAHP.mod` with a seconds-scale gating variable,
parametrised independently of Ca).

**Best practice**: Implement option (a) for t0078 (extend range to [1, 200x]) since it is the
smallest change that spans the full kinetic regime; if optimiser pushes the multiplier to its upper
bound, the negative result identifies KCNQ-like slow K+ as the next architectural extension.
Document the multiplier vs taur mapping in the planning document so reviewers can interpret the
resulting Pareto cells.

**Hypothesis (testable in t0078)**: If the slow Kv-AHP firing-rate cap is achievable with
tau_ca_multiplier <= 20x, the t0074 SK_E2 architecture is sufficient. If the optimiser pushes the
multiplier to >= 100x and the firing rate still saturates above the 30 Hz target, a KCNQ- like
seconds-scale K+ mechanism is required and SK_E2 is the wrong substrate for the slow-AHP extension.

### AIS Two-Subsegment NEURON Architecture: Two Independent Templates Available

Two NEURON-implementation templates of two-subsegment AIS in mouse RGCs are now publicly verifiable:

1. **Wienbar & Schwartz 2022 Neuron** [Wienbar2022] — Zenodo DOI `10.5281/zenodo.6423531`
   [SchwartzNU-Zenodo]. NEURON model files for OFFsA and bSbC alpha RGCs, with explicit AIS length
   **22 um (OFFsA) vs 16 um (bSbC)**, AIS diameter **~1.3 um**, total AIS Na conductance **200 nS
   (OFFsA) vs 150 nS (bSbC)**, and Nav1.6 fraction **40 % (OFFsA) vs 0 % (bSbC)** with the remainder
   Nav1.2. License: "Other (Open)".

2. **Werginz, Király, Zeck 2024 J. Neurosci.** [Werginz2024] — DOI
   `10.1523/JNEUROSCI.1592-24.2024`. Multi-compartment NEURON model of three mouse alpha RGC types
   (alpha-ON-sustained, alpha-OFF-sustained, alpha-OFF-transient) with **Table 1** listing
   ion-channel conductances (gNa, gK, gCa, gK,Ca, gH, gL) across the **five compartment tiers**
   (dendrites, soma, soma-AIS, AIS, axon) — directly applicable as a Sobol DoE seed for the t0078
   tier-stratified search. The conductances are species-matched (mouse) and cell-type- matched
   (alpha RGC, structurally close to ON-OFF DSGC), updating the Fohlmeister 2010 rat-/cat- priors
   flagged in `research_papers.md` Gap 5.

**Best practice**: Port the Wienbar 2022 [SchwartzNU-Zenodo] AIS-segment construction code as the
t0078 AIS template (Apache-style "Other (Open)" license is permissive). Use Werginz 2024
[Werginz2024] Table 1 alpha-ON-sustained values as the Sobol DoE nominal seed for the five-tier
channel densities — concretely, this updates `research_papers.md` Methodology Insight 3
(Fohlmeister 2010 prior) to Werginz 2024 (more recent, mouse-specific, alpha-RGC-specific).

**Hypothesis (testable in t0078)**: A Sobol DoE seeded on Werginz 2024 alpha-ON-sustained tier
densities will sample closer to the joint operating point (DSI > 0.4 AND PD rate > 10 Hz) than a
Fohlmeister-2010-rat-Type-I seed. If the converse is true (Fohlmeister seed reaches the target
faster), the rat / cat / mouse species difference is not the load-bearing factor and the Bed B
substrate's morphological vs channel-distribution priors are the real bottleneck.

### Tier-Stratified Channel-Density Data for Mouse RGCs is Now Available

Werginz 2024 [Werginz2024] Table 1 provides per-compartment conductances for sustained and transient
mouse alpha-RGCs. The maximum sustained firing rates reported (270-346 Hz at breakdown current
injection) are far above the t0076 Pareto extreme (127.75 Hz) and confirm that biological mouse RGCs
reach 250+ Hz under sustained current — meaning t0076's "saturated spiking" diagnosis at iter 319
is not implausibly high; rather, the matching DSI at that rate (0.003) is the unphysiological
outcome.

Ran et al. 2020 Nature Communications [Ran2020] provides a complementary biophysical model of four
mouse RGC types (transient OFF alpha, transient OFF mini, sustained OFF, F-mini OFF) with
tier-stratified channel densities derived from two-photon Ca2+ imaging of dendritic Ca2+ signals.
Although this paper targets non-DSGC types, its modelling framework demonstrates that
backpropagation efficiency in mouse RGCs is determined by the **product of dendritic morphology and
ion-channel densities**, not either alone. This validates the t0078 architectural choice of
tier-stratifying Nav1.6 / Kv3 / NaP / BK / SK while keeping morphology fixed at the de Rosenroll
2026 reconstruction.

**Best practice**: Cite Werginz 2024 Table 1 as the primary tier-density prior for the t0078 Sobol
DoE seed; cite Ran 2020 as the methodological precedent for tier-stratification in mouse RGC models.

## Methodology Insights

1. **qLogNEHVI migration is a single-line code change**. Replace
   `qNoisyExpectedHypervolumeImprovement` with `qLogNoisyExpectedHypervolumeImprovement`
   [BoTorch-logei-GH] [BoTorch-MOBO-Tut]. Default `tau_max = 1e-3`, `tau_relu` ~ 1e-6 are sufficient
   for the t0078 ~47-d setting; only revisit if the GP fit produces NaNs in the acquisition
   gradient.

2. **Wrap GP inputs in `Normalize([0, 1]^d)` and outputs in `Standardize`**. Both are recommended
   defaults for high-dimensional MOBO in the BoTorch tutorial chain [BoTorch-MOBO-Tut]. This
   directly fixes the "GP fit suboptimal" warning observed in t0076 (which passed natural-units
   bounds to the GP).

3. **Re-target the BO utopia point**. Updated from `research_papers.md`: Use **(DSI 0.7, PD rate 15
   Hz)** instead of **(DSI 0.7, PD rate 80 Hz)**, anchored to Rivlin-Etzion 2012 [RivlinEtzion2012]
   mean PD rate of 10.4 Hz and DSI 0.78 in mouse ON-OFF DSGCs. Document the change in the planning
   document and recompute the t0076 final HV under the new utopia point for direct cross-task
   comparison.

4. **Extend the SK_E2 `tau_ca_multiplier` range to [1, 200x]**. The Larsson 2013 [Larsson2013] sAHP
   review establishes that mammalian sAHP spans 1-3 s decay; a 20x ceiling on a 5-ms baseline gives
   only 100 ms, missing the seconds regime. If the optimiser pushes the multiplier to its upper
   bound, that is itself diagnostic information — either the substrate has reached the Ca-pool
   kinetics ceiling (and a separate KCNQ-like slow K+ mechanism is needed in a follow-up task), or
   the slow-AHP gap is not load-bearing for the joint DSI + PD rate target.

5. **Use Werginz 2024 Table 1 alpha-ON-sustained values as the Sobol DoE nominal seed**. This
   replaces `research_papers.md` Recommendation 2's Fohlmeister 2010 rat Type-I seed with a species-
   and cell-type-matched mouse alpha-RGC prior [Werginz2024]. The exact gNa / gK / gCa / gK,Ca / gH
   / gL values across dendrites / soma / soma-AIS / AIS / axon are tabulated in Werginz 2024 Table
   1; the planning step should extract these into the `code/parameter_priors.py` module.

6. **Port the Wienbar 2022 AIS segment construction directly**. The Zenodo archive
   [SchwartzNU-Zenodo] provides a complete two-subsegment AIS NEURON model with Nav1.6 / Nav1.2
   ratio as a free parameter. Use this instead of re-deriving from the Werginz 2020 Sci Adv
   paywalled methods. The Wienbar 2022 AIS-length range (16-22 um) is narrower than the 25-50 um
   range proposed in `research_papers.md`; we recommend keeping the wider range (25-50 um) in the
   t0078 search but flagging Pareto cells with AIS length < 20 um or > 40 um as biologically
   marginal.

7. **DSI definition consistency**. Trenholm 2013 [Trenholm2013] uses DSI = (Pref - Null) / (Pref +
   Null) computed from peak spike rates; Rivlin-Etzion 2012 [RivlinEtzion2012] uses the polar-plot
   vector-sum DSI from spike counts over a 3 s window; Hanson 2019 [Hanson2019] uses the project's
   standard 8-direction DSI. The t0078 DSI computation should explicitly use the 8-direction
   polar-plot definition (matching t0076) and should NOT use the peak-rate ratio definition (which
   gives systematically higher values and is not directly comparable).

8. **Subprocess-per-cell evaluation pattern is now community-standard**. The Wienbar 2022 model
   archive [SchwartzNU-Zenodo] uses the same subprocess-per-evaluation pattern for parameter sweeps
   to bypass NEURON's non-idempotent MOD-loader bug — confirming the t0078 design choice to launch
   each cell evaluation in a fresh `ProcessPoolExecutor` worker.

## Discovered Papers

### [Hay2011]

* **Title**: Models of Neocortical Layer 5b Pyramidal Cells Capturing a Wide Range of Dendritic and
  Perisomatic Active Properties
* **Authors**: Hay, E., Hill, S., Schürmann, F., Markram, H., Segev, I.
* **Year**: 2011
* **DOI**: `10.1371/journal.pcbi.1002107`
* **URL**: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1002107
* **Suggested categories**: `compartmental-modeling`, `voltage-gated-channels`
* **Why download**: Source paper for `SK_E2.mod`, `Im.mod`, `Ih.mod`, `Ca_HVA.mod`, `Ca_LVAst.mod`,
  and `CaDynamics_E2.mod` — five of the channels vendored into the t0074 / t0078 substrate.
  Provides the canonical Köhler 1996 SK_E2 implementation and its Ca-binding kinetics. Already
  flagged in t0076 research_internet.md as essential corpus addition; reaffirmed here.

### [Khaliq2003]

* **Title**: The Contribution of Resurgent Sodium Current to High-Frequency Firing in Purkinje
  Neurons: An Experimental and Modeling Study
* **Authors**: Khaliq, Z. M., Gouwens, N. W., Raman, I. M.
* **Year**: 2003
* **DOI**: `10.1523/JNEUROSCI.23-12-04899.2003`
* **URL**: https://www.jneurosci.org/content/23/12/4899
* **Suggested categories**: `voltage-gated-channels`, `compartmental-modeling`, `patch-clamp`
* **Why download**: Source paper for `bkpkj.mod` (BK / KCa1.1 used in t0074 / t0076), and a
  canonical reference for resurgent Na-current modelling. Already flagged in t0076
  research_internet.md as essential corpus addition.

### [Ament2023]

* **Title**: Unexpected Improvements to Expected Improvement for Bayesian Optimization
* **Authors**: Ament, S., Daulton, S., Eriksson, D., Balandat, M., Bakshy, E.
* **Year**: 2023
* **DOI**: not assigned (NeurIPS 2023 conference proceedings)
* **arXiv**: `2310.20708`
* **URL**: https://arxiv.org/abs/2310.20708
* **Suggested categories**: `compartmental-modeling` (no `bayesian-optimization` category exists in
  the project)
* **Why download**: Introduces qLogNEHVI as the numerically-stable replacement for qNEHVI used in
  t0078 (and migration of t0076). Provides the theoretical justification for the input `Normalize`
  transform and the smoothing parameters (`tau_max`, `tau_relu`). Peer-reviewed at NeurIPS 2023.

### [RivlinEtzion2012]

* **Title**: Visual Stimulation Reverses the Directional Preference of Direction-Selective Retinal
  Ganglion Cells
* **Authors**: Rivlin-Etzion, M., Wei, W., Feller, M. B.
* **Year**: 2012
* **DOI**: `10.1016/j.neuron.2012.08.041`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(12)00807-0
* **Suggested categories**: `direction-selectivity`, `retinal-ganglion-cell`, `patch-clamp`
* **Why download**: The cleanest joint DSI + PD-firing-rate measurement paper in mouse ON-OFF DSGCs
  (DRD4-GFP, TRHR-GFP transgenic lines). Reports DSI 0.78 ± 0.19 paired with mean PD rate 10.38 ±
  8.53 Hz over a 3 s window — the single most important reference for re- calibrating the t0078 BO
  utopia point. Resolves Gap 3 of `research_papers.md`.

### [Trenholm2013]

* **Title**: Dynamic Tuning of Electrical and Chemical Synaptic Transmission in a Network of Motion
  Coding Retinal Neurons
* **Authors**: Trenholm, S., Awatramani, G. B.
* **Year**: 2013
* **DOI**: `10.1523/JNEUROSCI.0808-13.2013`
* **URL**: https://www.jneurosci.org/content/33/37/14927
* **Suggested categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`
* **Why download**: Reports peak preferred-direction spike rates of 198 ± 14 Hz with null at 27 ±
  12 Hz in mouse Hb9::eGFP DSGCs (peak DSI ~0.76). Provides the upper bound on the PD-rate range and
  complements RivlinEtzion2012's mean-rate measurement. Documents gap-junction coupling in
  superior-coding DSGCs which is relevant for the synaptic-microarchitecture context of t0078.

### [Wienbar2022]

* **Title**: Differences in spike generation instead of synaptic inputs determine the feature
  selectivity of two retinal cell types
* **Authors**: Wienbar, S., Schwartz, G. W.
* **Year**: 2022
* **DOI**: `10.1016/j.neuron.2022.04.012`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(22)00357-9
* **Suggested categories**: `voltage-gated-channels`, `compartmental-modeling`, `patch-clamp`,
  `retinal-ganglion-cell`
* **Why download**: NEURON-based model of two mouse alpha RGC types (OFFsA, bSbC) with explicit
  two-subsegment AIS (length 16-22 um, diameter 1.3 um, Nav1.6 / Nav1.2 ratio as free parameter).
  The publicly archived Zenodo model (DOI `10.5281/zenodo.6423531`) is a directly portable AIS
  attachment template for t0078 — preferable to re-deriving from the Werginz 2020 paywalled
  methods. Provides quantitative AIS parameters that update `research_papers.md` Methodology Insight
  1\.

### [Werginz2024]

* **Title**: Differential Intrinsic Firing Properties in Sustained and Transient Mouse αRGCs Match
  Their Light Response Characteristics and Persist during Retinal Degeneration
* **Authors**: Werginz, P., Király, F., Zeck, G.
* **Year**: 2024
* **DOI**: `10.1523/JNEUROSCI.1592-24.2024`
* **URL**: https://www.jneurosci.org/content/45/2/e1592242024
* **Suggested categories**: `retinal-ganglion-cell`, `compartmental-modeling`,
  `voltage-gated-channels`, `patch-clamp`
* **Why download**: Most recent mouse-alpha-RGC compartmental model with Table 1 listing per-
  compartment conductances (gNa, gK, gCa, gK,Ca, gH, gL) across dendrites / soma / soma-AIS / AIS /
  axon. Direct replacement for the rat / cat Fohlmeister 2010 priors as the Sobol DoE seed for t0078
  tier-stratified densities. Reports max sustained firing of 270-346 Hz at breakdown — confirms
  biological RGC firing-rate ceiling.

## Recommendations for This Task

1. **Migrate to qLogNEHVI in a single line**. Replace `qNoisyExpectedHypervolumeImprovement` with
   `qLogNoisyExpectedHypervolumeImprovement`, wrap GP inputs in `Normalize([0,1]^d)`, wrap outputs
   in `Standardize`, and accept the default `tau_max = 1e-3`. Confirms `research_papers.md`
   Methodology Insight 7 with the exact API references [Ament2023] [BoTorch-logei-GH]
   [BoTorch-MOBO-Tut].

2. **Re-target the BO utopia point to (DSI 0.7, PD rate 15 Hz)**. Updates `research_papers.md`
   Methodology Insight 5 (which used (0.7, 80 Hz)). Anchored to Rivlin-Etzion 2012 mean PD rate of
   10.4 Hz over a 3-s window in mouse ON-OFF DSGCs [RivlinEtzion2012]. Recompute the t0076 final HV
   under the new utopia point for direct cross-task comparison; document this change in the planning
   step.

3. **Re-state the pass criterion**. The original "DSI >= 0.4 AND PD rate >= 30 Hz" is
   supraphysiological at 1-s mean: no peer-reviewed mouse DSGC measurement supports >= 30 Hz mean PD
   rate. Recommended replacement: **"DSI >= 0.4 AND PD rate >= 10 Hz" as the primary pass
   criterion**, with **"DSI >= 0.4 AND PD rate >= 30 Hz" retained as a stretch goal** that would
   establish supraphysiological output. Both criteria can be reported in the results.

4. **Extend the SK_E2 `tau_ca_multiplier` range to [1, 200x]**. Updates `research_papers.md`
   Methodology Insight 4 (which used [1, 20x]). Anchored to Larsson 2013 sAHP review which
   establishes 1-3 s sAHP decay timescale [Larsson2013]. If the optimiser pushes the multiplier to
   > = 100x, document this as evidence that a separate KCNQ-like slow K+ mechanism is the next
   > architectural extension.

5. **Use Werginz 2024 Table 1 as the Sobol DoE seed**. Updates `research_papers.md` Methodology
   Insight 3 (Fohlmeister 2010 rat Type-I) to a species- and cell-type-matched mouse alpha-RGC prior
   [Werginz2024]. Extract the gNa / gK / gCa / gK,Ca / gH / gL values from Table 1 into a
   `code/parameter_priors.py` module during planning.

6. **Port the Wienbar 2022 AIS segment code from the Zenodo archive**. Updates `research_papers.md`
   Methodology Insight 1: instead of re-deriving from Werginz 2020, port the public,
   MIT-style-licensed Wienbar 2022 model archive [SchwartzNU-Zenodo]. Adapts the AIS-length range
   from Wienbar's 16-22 um to the project's 25-50 um but preserves the two- subsegment topology and
   Nav1.6 / Nav1.2 ratio parameterisation.

7. **Add seven discovered papers to the corpus before planning starts**. The planning subagent
   should have access to summaries of [Hay2011], [Khaliq2003], [Ament2023], [RivlinEtzion2012],
   [Trenholm2013], [Wienbar2022], [Werginz2024] before designing the parameter ranges and utopia
   point. The orchestrator should spawn `/add-paper` subagents in parallel for these seven DOIs
   after this step completes.

## Source Index

### [Hay2011]

* **Type**: paper
* **Title**: Models of Neocortical Layer 5b Pyramidal Cells Capturing a Wide Range of Dendritic and
  Perisomatic Active Properties
* **Authors**: Hay, E., Hill, S., Schürmann, F., Markram, H., Segev, I.
* **Year**: 2011
* **DOI**: `10.1371/journal.pcbi.1002107`
* **URL**: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1002107
* **Peer-reviewed**: yes (PLOS Computational Biology)
* **Relevance**: Source paper for `SK_E2.mod` and `CaDynamics_E2.mod` vendored into the t0074 /
  t0078 substrate. Provides the canonical Köhler 1996 SK_E2 implementation. Establishes the Hay
  framework still in active community use 15 years later.

### [Khaliq2003]

* **Type**: paper
* **Title**: The Contribution of Resurgent Sodium Current to High-Frequency Firing in Purkinje
  Neurons: An Experimental and Modeling Study
* **Authors**: Khaliq, Z. M., Gouwens, N. W., Raman, I. M.
* **Year**: 2003
* **DOI**: `10.1523/JNEUROSCI.23-12-04899.2003`
* **URL**: https://www.jneurosci.org/content/23/12/4899
* **Peer-reviewed**: yes (J. Neurosci.)
* **Relevance**: Source paper for `bkpkj.mod` (BK channel) used in t0074 / t0076 / t0078. Documents
  resurgent Na-current mechanism and its modelling implementation.

### [Kohler1996-Sci]

* **Type**: paper
* **Title**: Small-conductance, calcium-activated potassium channels from mammalian brain
* **Authors**: Köhler, M. et al.
* **Year**: 1996
* **DOI**: not separately resolved (Science paper, search returns multiple references)
* **URL**: https://pubmed.ncbi.nlm.nih.gov/8781233/
* **Peer-reviewed**: yes (Science)
* **Relevance**: Foundational paper cloning SK1, SK2, SK3; supplies the Ca-binding kinetics cited by
  Hay 2011 `SK_E2.mod` (~10 ms tau at saturating Ca). Establishes that the SK channel itself is fast
  — the slow phase of sAHP is downstream signalling, per Larsson 2013.

### [Hirschberg1998-Sci]

* **Type**: paper
* **Title**: Gating of Recombinant Small-Conductance Ca-activated K+ Channels by Calcium
* **Authors**: Hirschberg, B., Maylie, J., Adelman, J. P., Marrion, N. V.
* **Year**: 1998
* **DOI**: `10.1085/jgp.111.4.565`
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC2217120/
* **Peer-reviewed**: yes (J. Gen. Physiol.)
* **Relevance**: Cited alongside Köhler 1996 for SK channel gating kinetics: ~12.9 ms activation
  time constant in response to Ca steps. Confirms SK channels are intrinsically fast.

### [Larsson2013]

* **Type**: paper
* **Title**: What Determines the Kinetics of the Slow Afterhyperpolarization (sAHP) in Neurons?
* **Authors**: Larsson, H. P.
* **Year**: 2013
* **DOI**: `10.1016/j.bpj.2012.11.3832`
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC3552283/
* **Peer-reviewed**: yes (Biophysical Journal)
* **Relevance**: Reviews the sAHP timescale across mammalian central neurons. Establishes that the
  seconds-scale decay is set by downstream Ca-sensor signalling (hippocalcin → KCNQ), not by SK
  Ca-binding. Critical for interpreting the t0078 `tau_ca_multiplier` range and choosing whether to
  extend SK_E2 or add a separate KCNQ-like mechanism.

### [Manookin2006-Neuron]

* **Type**: paper
* **Title**: Presynaptic Mechanism for Slow Contrast Adaptation in Mammalian Retinal Ganglion Cells
* **Authors**: Manookin, M. B., Demb, J. B.
* **Year**: 2006
* **DOI**: `10.1016/j.neuron.2006.04.001`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(06)00265-0
* **Peer-reviewed**: yes (Neuron)
* **Relevance**: Documents that slow contrast adaptation in mouse / primate RGCs is partially
  presynaptic (bipolar cell glutamate release adaptation), not entirely intrinsic. Implies the t0078
  SK_E2-extended-Ca-binding may not fully reproduce sAHP if the dominant mechanism is presynaptic in
  vivo.

### [Wark2011-PMC]

* **Type**: paper
* **Title**: Delayed Rectifier K Channels Contribute to Contrast Adaptation in Mammalian Retinal
  Ganglion Cells
* **Authors**: Wark, B., Werblin, F. S.
* **Year**: 2011
* **DOI**: `10.1016/j.neuron.2011.06.013`
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC3134798/
* **Peer-reviewed**: yes (Neuron)
* **Relevance**: Documents that Kv (delayed-rectifier K+) channels contribute to RGC contrast
  adaptation. Establishes that multiple K+ pathways shape RGC firing-rate adaptation, not just
  Ca-activated K+. Relevant for interpreting the t0078 Pareto cells where Kv3 density and SK_E2
  density both contribute to the rate cap.

### [Ament2023]

* **Type**: paper
* **Title**: Unexpected Improvements to Expected Improvement for Bayesian Optimization
* **Authors**: Ament, S., Daulton, S., Eriksson, D., Balandat, M., Bakshy, E.
* **Year**: 2023
* **DOI**: not assigned (NeurIPS 2023)
* **URL**: https://arxiv.org/abs/2310.20708
* **Peer-reviewed**: yes (NeurIPS 2023)
* **Relevance**: Introduces qLogNEHVI as the numerically-stable replacement for qNEHVI. Provides
  theoretical guarantees and 100+ dimensional benchmarks. Direct primary source for the t0078
  optimiser migration.

### [RivlinEtzion2012]

* **Type**: paper
* **Title**: Visual Stimulation Reverses the Directional Preference of Direction-Selective Retinal
  Ganglion Cells
* **Authors**: Rivlin-Etzion, M., Wei, W., Feller, M. B.
* **Year**: 2012
* **DOI**: `10.1016/j.neuron.2012.08.041`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(12)00807-0
* **Peer-reviewed**: yes (Neuron)
* **Relevance**: Cleanest joint DSI + PD-firing-rate measurement in mouse ON-OFF DSGCs. DSI 0.78 ±
  0.19 paired with mean PD rate 10.38 ± 8.53 Hz over 3-s window. Re-calibrates the t0078 BO utopia
  point and pass criterion.

### [Trenholm2013]

* **Type**: paper
* **Title**: Dynamic Tuning of Electrical and Chemical Synaptic Transmission in a Network of Motion
  Coding Retinal Neurons
* **Authors**: Trenholm, S., Awatramani, G. B.
* **Year**: 2013
* **DOI**: `10.1523/JNEUROSCI.0808-13.2013`
* **URL**: https://www.jneurosci.org/content/33/37/14927
* **Peer-reviewed**: yes (J. Neurosci.)
* **Relevance**: Reports peak PD spike rate 198 ± 14 Hz with null 27 ± 12 Hz in mouse Hb9::eGFP
  DSGCs in picrotoxin (peak DSI ~0.76). Provides the upper bound on PD rate (peak, sub-second)
  complementing RivlinEtzion2012's mean rate.

### [Hanson2019]

* **Type**: paper
* **Title**: Retinal direction selectivity in the absence of asymmetric starburst amacrine cell
  responses
* **Authors**: Hanson, L., Sethuramanujam, S., deRosenroll, G., Jain, V., Awatramani, G. B.
* **Year**: 2019
* **DOI**: `10.7554/eLife.42392`
* **URL**: https://elifesciences.org/articles/42392
* **Peer-reviewed**: yes (eLife). Already in corpus at
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.7554_eLife.42392/`.
* **Relevance**: Provides paired DSI + spike-density (loose-patch) data: DSI 0.33 ± 0.019 (WT,
  n=6), 0.07 ± 0.02 (Gabra2 KO + ChR2, n=7). Confirms partial paired-measurement availability in
  the corpus.

### [Wienbar2022]

* **Type**: paper
* **Title**: Differences in spike generation instead of synaptic inputs determine the feature
  selectivity of two retinal cell types
* **Authors**: Wienbar, S., Schwartz, G. W.
* **Year**: 2022
* **DOI**: `10.1016/j.neuron.2022.04.012`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(22)00357-9
* **Peer-reviewed**: yes (Neuron)
* **Relevance**: NEURON-based AIS model with explicit Nav1.6 / Nav1.2 ratio parameterisation;
  provides a directly portable two-subsegment AIS attachment template for t0078.

### [Werginz2024]

* **Type**: paper
* **Title**: Differential Intrinsic Firing Properties in Sustained and Transient Mouse αRGCs Match
  Their Light Response Characteristics and Persist during Retinal Degeneration
* **Authors**: Werginz, P., Király, F., Zeck, G.
* **Year**: 2024
* **DOI**: `10.1523/JNEUROSCI.1592-24.2024`
* **URL**: https://www.jneurosci.org/content/45/2/e1592242024
* **Peer-reviewed**: yes (J. Neurosci.)
* **Relevance**: Provides per-compartment conductance table (gNa, gK, gCa, gK,Ca, gH, gL across
  dendrites / soma / soma-AIS / AIS / axon) for mouse alpha RGCs. Directly applicable as Sobol DoE
  seed for t0078 tier-stratified search; updates Fohlmeister 2010 prior.

### [Ran2020]

* **Type**: paper
* **Title**: Type-specific dendritic integration in mouse retinal ganglion cells
* **Authors**: Ran, Y., Huang, Z., Baden, T., Schubert, T., Baayen, H., Berens, P., Franke, K.,
  Euler, T.
* **Year**: 2020
* **DOI**: `10.1038/s41467-020-15867-9`
* **URL**: https://www.nature.com/articles/s41467-020-15867-9
* **Peer-reviewed**: yes (Nature Communications)
* **Relevance**: Methodological precedent for tier-stratified channel densities in mouse RGC models.
  Demonstrates that backpropagation efficiency is set by the product of dendritic morphology and
  ion-channel densities — validates the t0078 architectural separation of morphology (fixed) from
  channel densities (free per tier).

### [BoTorch-logei-GH]

* **Type**: documentation
* **Title**: botorch.acquisition.multi_objective.logei — BoTorch source code
* **Author/Org**: Meta AI (BoTorch maintainers)
* **Date**: 2024-2026 (continuously updated)
* **URL**:
  https://botorch.readthedocs.io/en/stable/_modules/botorch/acquisition/multi_objective/logei.html
* **Peer-reviewed**: no (open-source code documentation)
* **Relevance**: Source code of `qLogNoisyExpectedHypervolumeImprovement` confirming inheritance
  from `qLogExpectedHypervolumeImprovement` and `NoisyExpectedHypervolumeMixin`, with default
  `tau_max = 1e-3` and `tau_relu` smoothing parameters. Defines the exact API for t0078 migration.

### [BoTorch-MOBO-Tut]

* **Type**: documentation
* **Title**: Multi-objective optimization with qEHVI, qNEHVI, and qNParEGO — BoTorch tutorial
* **Author/Org**: Meta AI (BoTorch maintainers)
* **Date**: 2024-2026
* **URL**: https://botorch.org/docs/tutorials/multi_objective_bo/
* **Peer-reviewed**: no
* **Relevance**: Official BoTorch migration guidance: "It is strongly recommended to simply replace
  `qNoisyExpectedHypervolumeImprovement` with `qLogNoisyExpectedHypervolumeImprovement`, which fixes
  the issues and has the same API." Single-line code change required for t0078.

### [BoTorch-Discussion-2791]

* **Type**: forum
* **Title**: Bayesian Optimization and Active Learning Cookbook — discussion
* **Author/Org**: BoTorch maintainers (Meta AI)
* **Date**: 2024
* **URL**: https://github.com/meta-pytorch/botorch/discussions/2791
* **Peer-reviewed**: no (GitHub discussion thread)
* **Relevance**: Maintainer comment confirming qLogNEHVI is the recommended default over qNEHVI in
  the cookbook tutorials. Establishes community consensus.

### [SchwartzNU-Zenodo]

* **Type**: repository
* **Title**: SchwartzNU/bSbC_ModelFiles — Wienbar & Schwartz 2022 NEURON model archive
* **Author/Org**: Schwartz Lab, Northwestern University
* **Date**: 2022-04
* **URL**: https://zenodo.org/records/6423531
* **Last updated**: 2022-04 (frozen archive accompanying the paper)
* **Peer-reviewed**: no (data archive accompanying peer-reviewed paper)
* **Relevance**: Public NEURON model archive with two-subsegment AIS implementation for OFFsA and
  bSbC mouse alpha RGCs. Directly portable to t0078 substrate. License: "Other (Open)".

### [Webvision-DSGC]

* **Type**: documentation
* **Title**: The Anatomy and Physiology of Direction-Selective Retinal Ganglion Cells
* **Author/Org**: Liu, J. (chapter author), Webvision (University of Utah)
* **Date**: 2018 (last updated)
* **URL**: https://www.ncbi.nlm.nih.gov/books/NBK321299/
* **Peer-reviewed**: no (review chapter; not strictly peer-reviewed but extensively cited)
* **Relevance**: Establishes consensus DSGC firing-rate ranges across the mouse / rabbit literature:
  significant motion responses average 5 ± 2 Hz. Confirms RivlinEtzion2012's ~10 Hz finding is in
  the typical range, not an outlier.

### [Hu2009]

* **Type**: paper
* **Title**: Distinct contributions of Nav1.6 and Nav1.2 in action potential initiation and
  backpropagation
* **Authors**: Hu, W. et al.
* **Year**: 2009
* **DOI**: `10.1038/nn.2359`
* **URL**: https://www.nature.com/articles/nn.2359
* **Peer-reviewed**: yes (Nature Neuroscience). Already in corpus at
  `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1038_nn.2359/`.
* **Relevance**: Establishes the Nav1.6 (distal AIS, spike initiation) vs Nav1.2 (proximal AIS,
  back-propagation) functional dissociation that motivates the Wienbar 2022 / t0078 two- subsegment
  AIS architecture.
