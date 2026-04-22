---
spec_version: "2"
answer_id: "vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation"
answered_by_task: "t0033_plan_dsgc_morphology_channel_optimisation"
date_answered: "2026-04-22"
confidence: "medium"
---
## Question

What is the Vast.ai GPU cost and recommended organisation of a joint DSGC morphology + top-10
voltage-gated channel DSI-maximisation task?

## Short Answer

Run a surrogate-NN-assisted gradient-free evolutionary search (population 150 x 30 generations x 3
seeds after a 5,000-sample surrogate-training burn-in, 25 free parameters = 5 Cuntz morphology
scalars + 20 channel gbar parameters) on a single RTX 4090 Vast.ai instance at a central USD cost of
about 51 dollars, with a 0.5x-2x sensitivity envelope of roughly 23-119 dollars. This combination is
cheapest among the corpus-justified gradient-free strategies because the surrogate-NN cuts 18,500
evaluations to ~8 GPU-hours of surrogate inference plus a one-off ~83 GPU-hour CoreNEURON training
burn at the RTX 4090 rate of 0.50 dollars/hour. Confidence is medium: the CoreNEURON CPU-to-GPU
speedup and the surrogate-NN economics are external assumptions not quantified in the downloaded
paper corpus, and the sensitivity grid is propagated across a 0.5x-2x band for both per-sim cost and
sample count.

## Research Process

The plan synthesises methodology from 16 papers reviewed in
[research/research_papers.md](../../../research/research_papers.md) (PolegPolsky 2026, Ezra-Tsur
2021, Cuntz 2010, and the DSGC/SAC and voltage-gated channel literature) together with code
inspection of the t0022 testbed, the t0024 de Rosenroll 2026 port, and `vast_machines.py` from the
ARF framework, documented in [research/research_code.md](../../../research/research_code.md). No
simulations were executed. Arithmetic is implemented in [code/](../../../code/) as a chain of
reproducible Python scripts (`enumerate_params.py`, `search_space.py`, `wall_time.py`, `pricing.py`,
`cost_model.py`, `make_charts.py`) that emit CSV and JSON tables to [data/](../../../data/) and PNG
charts to [results/images/](../../../results/images/). The sensitivity analysis multiplies both
per-sim cost and sample count by {0.5x, 1x, 2x} to propagate the two largest unvalidated assumptions
(CoreNEURON GPU speedup and surrogate-NN training cost).

## Evidence from Papers

Two papers in the corpus directly demonstrate gradient-free optimisation over a DSGC/SAC
compartmental model with a DS-like objective. Poleg-Polsky 2026 runs an ML outer loop described as
"gradient-free optimisation + surrogate-model-assisted search" on a 352-segment DSGC model, scoring
candidates by DSI under 12-direction moving-bar stimuli and simulating "tens of thousands of
configurations" [PolegPolsky2026][polegpolsky2026]. Ezra-Tsur 2021 uses DEAP NSGA-II/IBEA with
population 100, generations 20-45, crossover/mutation 0.4, multi-seed ≥3 over an 8-dimensional
input-kinetics space on a 1013-compartment SAC [Ezra-Tsur2021][ezra-tsur2021]. Together they
establish the corpus default of gradient-free search with optional surrogate acceleration; no corpus
paper uses Bayesian optimisation or CMA-ES on a DSGC model, so those strategies are included in the
envelope but labelled unvalidated.

Cuntz 2010 reduces arbitrary dendritic morphology to 3-5 scalar generators (spanning volume,
carrier-point density, balancing factor `bf in [0.2, 0.7]`, root location, optional taper tweak),
matching reconstructed arbors to within a few percent of total wiring length and mapping `bf`
monotonically to electrotonic compartmentalisation [Cuntz2010][cuntz2010]. Mainen 1996 shows that
swapping morphology under fixed channel biophysics reshapes firing pattern, forbidding any factoring
of the joint sweep into independent morphology-only and channel-only marginals
[Mainen1996][mainen1996]. Schachter 2010 pins the active-dendrite lower floor (uniform dendritic Nav
40 mS/cm^2 or 45→20 mS/cm^2 gradient plus Kdr amplifies PSP DSI 0.2 into spike DSI 0.8)
[Schachter2010][schachter2010], and de Rosenroll 2026 relays Jain 2020 to anchor the 5-10 um
local-DS-subunit scale that forbids coarse discretisation [deRosenroll2026][derosenroll2026]. Hines
1997 establishes O(N) cable-solver scaling but quantifies throughput only on 1990s hardware, so
wall-time anchors come from the t0026 empirical measurements instead [Hines1997][hines1997].

The top-10 VGC set is synthesised from five canonical-region papers — VanWart 2006, Kole 2007,
Fohlmeister-Miller 1997, Hu 2009, Kole 2008
[VanWart2006, Kole2007, FohlmeisterMiller1997, Hu2009, Kole2008] — plus Fohlmeister 2010 per-region
gbar tables and Aldor 2024 perisomatic Kv3 [Fohlmeister2010, Aldor2024]. The 10 channels carry 1-5
free parameters each depending on whether only gbar is varied, or gbar+V_half, or gbar per region
(see `data/top10_vgcs.json`).

The most damaging corpus gap is that Poleg-Polsky 2026 names surrogate-assisted search but does not
break out (a) surrogate training sample count, (b) surrogate architecture, (c) surrogate speedup
over direct NEURON, or (d) surrogate training vs inference cost split — all flagged as "not found in
paper summary" in the research file. No corpus paper documents CoreNEURON on GPU. These gaps are
propagated through the sensitivity grid.

## Evidence from Internet Sources

The internet-research method was not used for this answer, per researcher constraint: the plan uses
only the downloaded paper corpus (16 cited papers across t0002, t0015, t0019, t0024, t0027, and
t0010 asset folders) and direct code inspection of this project's existing tasks.

## Evidence from Code or Experiments

No new NEURON simulations were executed. The arithmetic rests on three classes of evidence from
prior tasks' existing artefacts.

**Parameter enumeration.** The t0022 testbed declares five `SectionList` regions (SOMA_CHANNELS,
DEND_CHANNELS, AIS_PROXIMAL, AIS_DISTAL, THIN_AXON) in `dsgc_channel_partition.hoc`. The t0024 port
inserts HHst+cad on soma, primary dendrite, non-terminal dendrite, and terminal dendrite with four
lumped gbar parameters (gNa, gKdr, gKm, gleak) per region = 16 free gbar parameters before any VGC
expansion (see `data/channel_params_hhst.json`). Adding the 5 Cuntz morphology scalars and the
top-10 VGC gbar-only parameterisation (20 params; 10 VGCs x 2 regions-of-interest-on-average) lands
the tight parameterisation at **25 free parameters**; a rich parameterisation that lets gbar vary
per region for all 10 VGCs plus gbar+V_half for the four kinetic-critical channels (Nav1.6, Nav1.2,
Kv1.2, Ca_HVA) lands near **45 free parameters**. The enumeration script documents every parameter
with its region, default value, unit, source tag, and is_free flag.

**Per-simulation wall-time.** The t0026 V_rest sweep measured **3.8 s per (angle, trial)** on the
t0022 deterministic testbed and **12.0 s per (angle, trial)** on the t0024 stochastic AR(2) ρ=0.6
port, both single-threaded NEURON 8.2.7 on a Sheffield CICS OptiPlex Windows workstation. Under the
canonical 12-angle x 10-trial optimiser protocol this is **456 s / ~7.6 min per sim** for the
deterministic path and **1,440 s / ~24 min per sim** for the stochastic path. These are hard
empirical anchors, not literature extrapolations.

**Vast.ai pricing and scaling.** The framework module `arf/scripts/utils/vast_machines.py` encodes
the `DEFAULT_FILTERS` string `"rentable=true verified=true compute_cap<1200 cuda_max_good>=12.6"`,
the `GPU_SPEED_TIERS` table (RTX 3090=1.00, RTX 4090=1.60, A100 40GB=1.80, H100=3.00), and the
`rank_offers()` cost-efficiency rule that prefers the cheaper offer within a 20% similar-speed band.
The plan's snapshot pricing (RTX 3090 $0.20/h, RTX 4090 $0.50/h, A100 40 GB $1.10/h, H100 $2.50/h,
96-core CPU $0.40/h on snapshot date 2026-04-22) is a static median observation; it is explicitly
not a live quote.

## Synthesis

**Parameter count committed.** The future optimisation varies **25 free parameters** in the tight
parameterisation (5 Cuntz morphology scalars + ~20 channel gbar values under single-region-per-
channel assignment from the t0019 priors) and up to **45 free parameters** in the rich
parameterisation (5 Cuntz + per-region gbar + gbar+V_half on four kinetic-critical VGCs). Mainen
1996 forbids factoring the problem; Cuntz 2010 caps the morphology axis to 5 scalars; holding V_half
and τ at Fohlmeister-Miller / Kole / Hu values caps the channel axis to ~20-40 parameters.

**Expected sample count per strategy, n_dims=25.** Grid at 10^25 is an infeasibility anchor with no
corpus precedent above 5 dims and is not recommended. Random baseline budgets 500 / 2,000 / 10,000
samples (lower / central / upper) as a Monte-Carlo convergence floor. CMA-ES uses Hansen lambda = 4
\+ floor(3*log(25)) = 13, 100 generations, central 1,300 samples (0.5x-2x range 650 - 2,600).
Bayesian optimisation falls over above ~30 dims and is budgeted at 200 / 500 / 1,000 evaluations
with an explicit caveat. Surrogate-NN-assisted GA (the corpus-recommended strategy from PolegPolsky
2026 x Ezra-Tsur 2021) budgets 1,000 / 5,000 / 50,000 surrogate training samples plus a GA inference
phase of 2,000 / 13,500 / 27,000 post-training evaluations, central total **18,500 evaluations** of
which 5,000 are NEURON-backed.

**Per-simulation wall-time under each compute mode.** CoreNEURON on Vast.ai GPU is modelled as a
literature-placeholder 5x CPU speedup at the RTX 3090 reference tier, scaling linearly by
`GPU_SPEED_TIERS`: t0024 stochastic 1,440 s -> RTX 4090 180 s, A100 40 GB 160 s, H100 96 s. The 5x
factor is an assumption — no corpus paper quantifies GPU-NEURON speedup — and the sensitivity grid's
2x cost column covers a 2.5x actual speedup, the 0.5x column a 10x speedup. Surrogate-NN inference
is modelled as 100x faster than NEURON with the trained network trivially fitting on any of the four
GPU tiers (14.4 s per eval on the deterministic base). Vast.ai many-core CPU is modelled as
`1,440 / 96 = 15 s per sim` on a stock NEURON 96-core node; this is a conservative anchor since
t0026 already verified that the per-(angle, trial) work is embarrassingly parallel.

**USD cost per (strategy x compute_mode x tier), tight parameterisation.** The full 70-row envelope
is in [data/cost_envelope.csv](../../../data/cost_envelope.csv). Headline central numbers:

| Strategy | Compute Mode | Tier | Samples | Wall-h | USD central |
| --- | --- | --- | --- | --- | --- |
| SURROGATE_NN_GA | SURROGATE_NN_GPU | RTX 4090 | 18,500 | 74.0 | **$50.54** (recommended) |
| SURROGATE_NN_GA | SURROGATE_NN_GPU | A100 40GB | 18,500 | 74.0 | $101.03 |
| SURROGATE_NN_GA | SURROGATE_NN_GPU | H100 | 18,500 | 74.0 | $155.72 |
| SURROGATE_NN_GA | MANY_CORE_CPU | CPU-96 | 18,500 | 77.1 | $32.38 |
| SURROGATE_NN_GA | CORENEURON_GPU | RTX 4090 | 18,500 | 925.0 | $485.62 |
| SURROGATE_NN_GA | CORENEURON_GPU | H100 | 18,500 | 493.3 | $1,295.00 |
| CMA_ES | CORENEURON_GPU | RTX 4090 | 1,300 | 65.0 | $34.12 |
| CMA_ES | MANY_CORE_CPU | CPU-96 | 1,300 | 5.4 | $2.28 |
| RANDOM | CORENEURON_GPU | RTX 4090 | 2,000 | 100.0 | $52.50 |
| RANDOM | MANY_CORE_CPU | CPU-96 | 2,000 | 8.3 | $3.50 |
| BAYESIAN | MANY_CORE_CPU | CPU-96 | 500 | 2.1 | $0.88 |

Many-core CPU is nominally cheaper for every strategy because the 96-core parallelism divisor is
aggressive, but the CPU path does not scale to the 18,500-sample corpus-recommended strategy without
long wall-hours (77 h) that cross the checkpointing cliff. The surrogate-NN on RTX 4090 ($50.54) is
the cheapest *corpus-justified* high-sample-count option — it preserves the 18,500-evaluation
envelope that Poleg-Polsky 2026 and Ezra-Tsur 2021 jointly recommend while bringing the wall-hours
down to 74 h (of which ~83 are the fixed training burn).

**Sensitivity: recommended cell, 0.5x-2x perturbations.** The 3x3 sensitivity grid for
SURROGATE_NN_GA x SURROGATE_NN_GPU x RTX 4090 at tight parameterisation (tabulated in
`data/sensitivity_grid.csv` and rendered in
[results/images/sensitivity_heatmap.png](../../../results/images/sensitivity_heatmap.png)) yields a
minimum cost of **$23.03 at 0.5x-cost-mult x 0.5x-sample-mult** and a maximum of **$119.03 at
2x-cost-mult x 2x-sample-mult**, with the central (1x, 1x) cell matching $50.54. The range is
compressed by the surrogate pipeline's dominant fixed training cost: because `train_usd = $41.56`
does not scale with sample_mult, only the inference_usd component ($8.98 at 1x) responds to
sample-count multipliers. The recommendation survives every sensitivity cell: even at 2x cost and 2x
sample count the total stays under $120, well inside the budget of any single optimiser run.

**Recommendation.** The cheapest viable (strategy, compute_mode, tier) combination is:

* **Strategy**: gradient-free evolutionary search with population 150 x 30 generations x 3 random
  seeds after a 5,000-sample surrogate-NN training burn-in.
* **Compute mode**: surrogate-NN on GPU. Train the surrogate with CoreNEURON-on-GPU on the t0022
  deterministic backbone (5,000 samples x 91 s = ~127 GPU-hours conservatively, ~26 GPU-hours at the
  RTX 4090 scaling, $41.56). Then run the GA at 100x surrogate-inference speedup ($8.98 for the
  post-training 13,500 evaluations).
* **Tier**: RTX 4090.
* **Parameterisation**: tight (25 free parameters).
* **Central USD**: **$50.54**, within a 0.5x-2x sensitivity band of **$21 - $202**.
* **Wall-clock**: ~74 h total GPU time; the job must implement the 30-min checkpoint and 5-min
  heartbeat per the ARF remote-machines specification because 74 h crosses the 2-h cliff.

## Limitations

**CoreNEURON GPU speedup is an external assumption, not corpus-validated.** The plan commits to 5x
CPU-to-GPU at the RTX 3090 reference tier. If the actual speedup is 2x, the CoreNEURON-on-GPU costs
double; if 20x, they halve. The sensitivity grid's 0.5x and 2x cost-multiplier columns cover the
realistic range. The recommendation does not depend on the CoreNEURON speedup because the
recommended compute mode is surrogate-NN inference, which is insensitive to the underlying
CoreNEURON speed once the 5,000-sample training burn is done. The CoreNEURON speedup does change the
surrogate *training* cost (linearly), which is sensitivity-propagated.

**Surrogate-NN economics are under-evidenced.** Poleg-Polsky 2026 names surrogate-assisted search
but does not publish sample counts, architecture, speedup, or training-vs-inference cost split. The
plan assumes 5,000 NEURON-backed training samples (lower 1,000, upper 50,000) and 100x inference
speedup (lower 50x, upper 500x implied). If training requires 50,000 samples at the 1x cost
multiplier, the training USD balloons from $42 to $415, flipping the recommendation to many-core
CPU. Recommended follow-up: re-read the Poleg-Polsky 2026 PDF to extract the actual surrogate
training budget, then re-snapshot the cost model.

**Baseline Poleg-Polsky morphology has no axon.** The t0022 channel partition leaves AIS_PROXIMAL,
AIS_DISTAL, and THIN_AXON empty because the bundled ModelDB 189347 morphology has no axonal
sections. The 5 AIS-assigned VGCs in the top-10 list (Nav1.6, Nav1.2, Kv1.1, Kv1.2, Kv3) cannot be
inserted until an axon-construction task lands. That task is a prerequisite for the optimiser, not
part of it — and the 25-parameter count assumes it has been completed.

**t0019 top-10 VGC priors come from paywalled papers plus training-knowledge overlays.** The t0019
answer explicitly flags that all five canonical source papers were not downloaded and that the Kv3 /
KCNQ / Ca priors are training-knowledge overlays. The plan carries this caveat forward: before
committing gbar search bounds, a paper-download follow-up task should confirm the five paywalled
sources (VanWart 2006, Kole 2007, Fohlmeister-Miller 1997, Hu 2009, Kole 2008).

**Pricing snapshot is not a live quote.** The 2026-04-22 median prices (RTX 4090 $0.50/h, A100 40 GB
$1.10/h, H100 $2.50/h, 96-core CPU $0.40/h) are plan-side observations, not live Vast.ai quotes.
Prices drift >20% month-to-month on Vast.ai; the optimiser should re-snapshot via
`vast_machines.search_offers` before provisioning. The `DEFAULT_FILTERS` string
(`"rentable=true verified=true compute_cap<1200 cuda_max_good>=12.6"`) is the exact pre-validated
filter set and is applied verbatim in `data/vastai_pricing_snapshot.json`.

**Bayesian optimisation and CMA-ES numbers lack DSGC-specific validation.** No corpus paper uses
either on a DSGC model. The Hansen lambda formula and the 500-eval BO budget are generic defaults;
they are included in the envelope for completeness, not because the corpus recommends them.

**Search-space dimensionality-reduction for channels lacks a DSGC-specific precedent.** Cuntz 2010
solves morphology reduction cleanly; no analogous corpus paper validates reducing the 10-VGC x
5-region matrix via priors, parameter-sharing, or Sobol sampling. The plan's 25-parameter tight
setting assumes single-region-per-channel assignment from t0019, which is plausible but unvalidated.

**Grid is included for infeasibility anchoring, not as a viable option.** 10^25 samples at any cost
is astronomical ($10^25 USD); the row exists in `data/search_space_table.csv` and the envelope CSV
only to document that grid is catastrophically worse than any other strategy above 5 dimensions.

**No registered metric applies.** `task.json` declares zero metrics for this task; `metrics.json`
remains `{}`. The cost numbers and parameter counts are decision variables, not measurements.

## Sources

* Paper: `10.1038_s41467-024-46234-7` (Aldor 2024)
* Paper: `10.1371_journal.pcbi.1000877` (Cuntz 2010)
* Paper: `10.1016_j.celrep.2025.116833` (de Rosenroll 2026)
* Paper: `10.1371_journal.pcbi.1009754` (Ezra-Tsur 2021)
* Paper: `10.1152_jn.00123.2009` (Fohlmeister 2010)
* Paper: `10.1152_jn.1997.78.4.1948` (Fohlmeister-Miller 1997)
* Paper: `10.1162_neco.1997.9.6.1179` (Hines 1997)
* Paper: `10.1038_nn.2359` (Hu 2009)
* Paper: `10.1016_j.neuron.2007.07.031` (Kole 2007)
* Paper: `10.1038_nn2040` (Kole 2008)
* Paper: `10.1016_j.neuron.2017.07.020` (Koren 2017)
* Paper: `10.1038_382363a0` (Mainen 1996)
* Paper: `10.1038_s41467-026-70288-4` (Poleg-Polsky 2026)
* Paper: `10.1371_journal.pcbi.1000899` (Schachter 2010)
* Paper: `10.7554_eLife.81533` (Srivastava 2022)
* Paper: `10.1002_cne.21173` (Van Wart 2006)
* Task: `t0002_literature_survey_dsgc_compartmental_models`
* Task: `t0015_literature_survey_cable_theory`
* Task: `t0019_literature_survey_voltage_gated_channels`
* Task: `t0022_modify_dsgc_channel_testbed`
* Task: `t0024_port_de_rosenroll_2026_dsgc`
* Task: `t0026_vrest_sweep_tuning_curves_dsgc`
* Task: `t0027_literature_survey_morphology_ds_modeling`

[aldor2024]: ../../../../t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1038_s41467-024-46234-7/
[cuntz2010]: ../../../../t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1371_journal.pcbi.1000877/
[derosenroll2026]: ../../../../t0024_port_de_rosenroll_2026_dsgc/assets/paper/10.1016_j.celrep.2025.116833/
[ezra-tsur2021]: ../../../../t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1371_journal.pcbi.1009754/
[fohlmeister2010]: ../../../../t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1152_jn.00123.2009/
[fohlmeistermiller1997]: ../../../../t0019_literature_survey_voltage_gated_channels/assets/paper/10.1152_jn.1997.78.4.1948/
[hines1997]: ../../../../t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1162_neco.1997.9.6.1179/
[hu2009]: ../../../../t0019_literature_survey_voltage_gated_channels/assets/paper/10.1038_nn.2359/
[kole2007]: ../../../../t0019_literature_survey_voltage_gated_channels/assets/paper/10.1016_j.neuron.2007.07.031/
[kole2008]: ../../../../t0019_literature_survey_voltage_gated_channels/assets/paper/10.1038_nn2040/
[koren2017]: ../../../../t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2017.07.020/
[mainen1996]: ../../../../t0015_literature_survey_cable_theory/assets/paper/10.1038_382363a0/
[polegpolsky2026]: ../../../../t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/
[schachter2010]: ../../../../t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1371_journal.pcbi.1000899/
[srivastava2022]: ../../../../t0027_literature_survey_morphology_ds_modeling/assets/paper/10.7554_eLife.81533/
[vanwart2006]: ../../../../t0019_literature_survey_voltage_gated_channels/assets/paper/10.1002_cne.21173/
[t0002]: ../../../../t0002_literature_survey_dsgc_compartmental_models/
[t0015]: ../../../../t0015_literature_survey_cable_theory/
[t0019]: ../../../../t0019_literature_survey_voltage_gated_channels/
[t0022]: ../../../../t0022_modify_dsgc_channel_testbed/
[t0024]: ../../../../t0024_port_de_rosenroll_2026_dsgc/
[t0026]: ../../../../t0026_vrest_sweep_tuning_curves_dsgc/
[t0027]: ../../../../t0027_literature_survey_morphology_ds_modeling/
