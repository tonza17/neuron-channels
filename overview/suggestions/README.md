# Research Suggestions Backlog

170 suggestions **148 open** (43 high, 86 medium, 19 low), **22 closed**.

**Browse by view**: By category: [`cable-theory`](by-category/cable-theory.md),
[`compartmental-modeling`](by-category/compartmental-modeling.md),
[`compartmental-modelling`](by-category/compartmental-modelling.md),
[`dendritic-computation`](by-category/dendritic-computation.md),
[`direction-selectivity`](by-category/direction-selectivity.md),
[`patch-clamp`](by-category/patch-clamp.md),
[`retinal-ganglion-cell`](by-category/retinal-ganglion-cell.md),
[`retinal-ganglion-cells`](by-category/retinal-ganglion-cells.md),
[`synaptic-integration`](by-category/synaptic-integration.md),
[`voltage-gated-channels`](by-category/voltage-gated-channels.md); [By date
added](by-date-added/README.md)

---

## High Priority

<details>
<summary>🧪 <strong>2-D distal length x diameter sweep on t0024 to disambiguate
cable-filtering vs local-spike-failure</strong> (S-0034-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0034-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0034_distal_dendrite_length_sweep_t0024`](../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md) |
| **Source paper** | — |
| **Categories** | [`cable-theory`](../../meta/categories/cable-theory/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../meta/categories/dendritic-computation/) |

t0034 produced a non-monotonic primary DSI (0.545-0.774, p=0.038) and a clean monotonic
vector-sum DSI decline (R^2=0.91) that falsified Dan2018's passive-TR prediction and did not
fit Sivyer2013's plateau. Creative-thinking flagged passive cable filtering past an optimal
electrotonic length (Tukker2004, Hausselt2007) as the best fit, with local-spike-failure
(Schachter2010) explaining the preferred-angle jumps at 1.5x and 2.0x. A marginal length sweep
alone cannot distinguish these two mechanisms because lambda = sqrt(d*Rm/(4*Ra)) couples
length and diameter nonlinearly. Run a 3x3 grid (length in {0.5, 1.0, 2.0} x diameter in {0.5,
1.0, 2.0}) on the t0024 port with AR(2) rho=0.6, 12-direction x 10-trial protocol per cell,
and classify each cell as cable-limited, spike-amplified, or threshold-transition. Distinct
from S-0030-04 (same approach on t0022 testbed, which was pinned at DSI=1.000 and cannot
resolve the effect). Recommended task types: experiment-run.

</details>

<details>
<summary>📚 <strong>Add a plan-stage DOI-nomination verificator that checks each
candidate DOI matches its human-written label</strong> (S-0013-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0013-02` |
| **Kind** | library |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0013_resolve_morphology_provenance`](../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md) |
| **Source paper** | — |
| **Categories** | — |

The Neuron-vs-CB mix-up in the t0005 plan (DOI 10.1016/j.neuron.2018.05.028 labelled 'Morrie &
Feller 2018 Neuron' when it actually belongs to Li et al. 2018 CSHL viral tracing) made it
through planning and into the t0005 implementation, triggering an entire follow-up task (this
one) to correct the downstream impact. Build a verificator under
arf/scripts/verificators/verify_plan_dois.py that scans plan/plan.md for every DOI-like
string, resolves each via the arf.scripts.utils.resolve_doi helper (S-0013-01), and
cross-checks the returned first-author last name, year, and venue against the label the plan
uses near the DOI. Report a warning when the label and resolved metadata disagree on author,
year, or venue, and an error when the DOI itself fails to resolve. Wire this verificator into
the planning-stage check so subsequent plans cannot silently mis-cite a DOI. Recommended task
types: write-library, experiment-run.

</details>

<details>
<summary>📚 <strong>Add a verify_library_asset.py framework verificator for library
asset structure and metadata</strong> (S-0012-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0012-01` |
| **Kind** | library |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0012_tuning_curve_scoring_loss_library`](../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md) |
| **Source paper** | — |
| **Categories** | — |

The t0012 library asset was hand-validated against meta/asset_types/library/specification.md
because arf/scripts/verificators/ has verify_suggestions.py, verify_metrics.py,
verify_research_papers.py, etc., but no verify_library_asset.py. Every future write-library
task (S-0002-08 SAC drive, S-0003-02 ModelDB 189347, S-0003-04 NetPyNE Batch harness,
S-0005-04 SWC loader, S-0009-08 Rall quaddiameter, t0011 response visualisation) will need the
same checks: details.json present with all required fields, library_id matches folder name and
the ^[a-z][a-z0-9]*(_[a-z0-9]+)*$ regex, module_paths resolve, description.md has the 8
mandatory sections, and categories exist in meta/categories/. Port the checks already
performed by hand on t0012 into a reusable verificator, wire it into step_registry.py, and
re-run it against existing library assets. Recommended task types: infrastructure-setup.

</details>

<details>
<summary>🧪 <strong>Add NMDA-block and TTX-sensitivity sweeps at each V_rest to
isolate biophysical mechanism</strong> (S-0026-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0026-06` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0026_vrest_sweep_tuning_curves_dsgc`](../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md) |
| **Source paper** | [`10.1016_j.neuron.2016.04.041`](../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/assets/paper/10.1016_j.neuron.2016.04.041/) |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

Our V_rest sweep shows t0022 loses tuning at depolarised V_rest (DSI 0.046 at V=-30 mV) while
t0024 stays flat (DSI>=0.36). Two candidate mechanisms are Na channel inactivation and NMDA
Mg-block relief. Run the sweep once with TTX-like Na-block (g_Na=0) and once with NMDA-block
(g_NMDA=0) to isolate which channel class drives each model's V_rest sensitivity.

</details>

<details>
<summary>🧪 <strong>AR(2) rho sweep at t0024 baseline morphology to isolate
stochastic-release smoothing from cable biophysics</strong> (S-0034-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0034-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0034_distal_dendrite_length_sweep_t0024`](../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |

Creative-thinking (alternative 5) proposed that AR(2)-correlated release with rho=0.6
temporally smooths the null-direction noise floor, potentially contributing to the observed
primary-DSI non-monotonicity independently of cable filtering. This hypothesis must be ruled
in or out before the cable-filtering interpretation is credible. Run the 12-direction x
10-trial protocol on t0024 at baseline morphology (length=1.0x, diameter=1.0x) with rho in
{0.0, 0.3, 0.6, 0.9} (four points) and compare primary-DSI, vector-sum DSI, null Hz, and HWHM
trajectories. If DSI is flat across rho, stochastic-release smoothing is not the driver; if
DSI varies with rho, the effect is release-noise-mediated. Distinct from S-0026-02 (which
crosses rho with V_rest to disambiguate noise vs depolarisation) because this sweeps rho at
fixed V_rest and fixed morphology to isolate the release-noise-vs-cable-biophysics axis.
Recommended task types: experiment-run.

</details>

<details>
<summary>📚 <strong>Build a headless-port scaffold library that wraps upstream NEURON
models</strong> (S-0010-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0010-05` |
| **Kind** | library |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0010_hunt_missed_dsgc_models`](../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

The three P2 failures all share the same root cause: upstream drivers assume a headful NEURON
GUI and hardcode paths/angles. A small library in assets/library/ that provides (a) a headless
NEURON loader that stubs out 'from neuron import gui', (b) a configurable output-path layer,
and (c) a canonical 12-angle stimulus generator would let future port tasks skip the
driver-rewrite step and go straight to P2/P3 scoring.

</details>

<details>
<summary>🧪 <strong>Build a minimal DSGC compartmental model implementing the 6-point
specification</strong> (S-0015-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0015-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0015_literature_survey_cable_theory`](../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modelling`](../../meta/categories/compartmental-modelling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

The answer asset cable-theory-implications-for-dsgc-modelling produces a concrete 6-point
specification for DSGC modelling in NEURON (morphology, d_lambda, DS mechanism, passive
parameters, validation suite, spike-generator tuning). A follow-up experiment task should
implement a minimal working DSGC model in NEURON/NetPyNE following the specification, using a
publicly-available DSGC morphology (e.g. NeuroMorpho.org) and validate it with the four-part
test battery (shape-index, graded DS, inhibition block, contrast-response).

</details>

<details>
<summary>📚 <strong>Build a reusable DSI-objective evaluation-harness library
separating scoring from the optimiser loop</strong> (S-0033-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0033-06` |
| **Kind** | library |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0033_plan_dsgc_morphology_channel_optimisation`](../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

The t0033 plan repeatedly treats evaluate(parameter_vector) -> DSI_scalar as the atomic unit
across CMA-ES / BO / surrogate-NN-GA strategies, but no library asset exposes this signature.
t0012 tuning_curve_loss scores full 12-angle rate vectors, not a DSI-objective scalar. Build a
library asset dsgc_dsi_objective that (a) wraps the t0022 or t0024 port behind a pure-function
evaluate_dsi(parameters, protocol, n_trials) -> DsiResult API, (b) batches (angle, trial)
pairs across an embarrassingly parallel pool, (c) returns a frozen dataclass with DSI, peak
Hz, null Hz, HWHM and a provenance dict, and (d) ships a thin CLI that accepts a parameter
JSON and emits a results JSON. Every strategy row in the t0033 cost model can then call a
single evaluator. Recommended task types: write-library, feature-engineering.

</details>

<details>
<summary>📚 <strong>Build a small reusable library for target-vs-simulated tuning
curve metrics</strong> (S-0004-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0004-03` |
| **Kind** | library |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0004_generate_target_tuning_curve`](../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

Factor the closed-form DSI, HWHM, tuning_curve_rmse, and tuning_curve_reliability computations
out of individual tasks into a shared library asset. Every later fitting task will need these
four functions; centralising them avoids divergent reimplementations and makes metric values
reproducible from parameters alone.

</details>

<details>
<summary>🔧 <strong>Calibrate active Nav / Kv / Ih densities to match Poleg-Polsky
2016 spike shape and distal Ih sag</strong> (S-0009-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-03` |
| **Kind** | technique |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0009_calibrate_dendritic_diameters`](../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../tasks/t0009_calibrate_dendritic_diameters/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

Geometry alone does not recover the Schachter Rin targets; the residual gap needs active and
passive membrane parameters. On dsgc-baseline-morphology-calibrated, install Fohlmeister-like
Nav, delayed-rectifier Kv, and Ih channels and fit their densities (somatic vs dendritic) so
that (1) the somatic action-potential shape (halfwidth, peak, afterhyperpolarisation) matches
Poleg-Polsky 2016 Figure 2, and (2) the voltage-sag response to hyperpolarising current at
distal tips matches the Ih-driven sag amplitude reported in Schachter 2010. This is distinct
from S-0002-01 (DSI-maximising g_Na/g_K grid) and S-0002-02 (passive-vs-active DSI ablation):
it tunes channel densities against single-cell electrophysiological waveforms, not tuning
curves. Output: a library asset exposing the fitted mechanism list for reuse in the DSI
experiments. Recommended task types: experiment-run, feature-engineering.

</details>

<details>
<summary>📊 <strong>Change the t0033 optimiser objective to a vector-sum-DSI-weighted
blend instead of pure primary DSI</strong> (S-0030-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0030-06` |
| **Kind** | evaluation |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

t0029 and t0030 both pinned primary DSI at 1.000 and only vector-sum DSI retained weak
sensitivity (ranges 0.021 and 0.012 respectively). The t0033 joint morphology-channel
optimisation plan currently proposes primary DSI as the objective; under the t0022 schedule
the optimiser will see a flat landscape and cannot discover morphology-channel interactions.
Change the t0033 objective to a weighted blend (e.g., 0.5 * vector_sum_DSI + 0.3 *
peak_Hz_match + 0.2 * HWHM_match) OR switch to vector-sum DSI outright. Distinct from
S-0029-07 which proposes promoting peak-Hz and HWHM to co-primary outcomes - this proposal
keeps DSI as the headline objective but replaces its pinned primary form with its unpinned
vector-sum form. Update tasks/t0012 tuning_curve_loss to expose a loss_kind='vector_sum_dsi'
option. Recommended task types: write-library, answer-question.

</details>

<details>
<summary>🧪 <strong>Excitation-side sensitivity sweep under gabaMOD-swap to close
the 25 Hz peak-firing-rate gap</strong> (S-0020-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0020_port_modeldb_189347_gabamod`](../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../tasks/t0020_port_modeldb_189347_gabamod/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

Under the native gabaMOD-swap protocol, DSI (0.7838) sits inside the [0.70, 0.85] envelope but
PD peak (14.85 Hz) is 25.15 Hz below the 40 Hz floor. Protocol is now ruled out, so the
shortfall must live on the excitation side. Run a factorial sweep over (a) BIP synapse count
{88, 177, 354}, (b) excMOD on AMPA+NMDA in {0.5, 1.0, 1.5, 2.0, 3.0}, (c) stimulus drive
{baseline, +50%, +100%}, holding gabaMOD at the 0.33/0.99 PD/ND pair. Report the smallest
config shift that moves peak into [40, 80] Hz without dragging DSI outside [0.70, 0.85].
Distinct from S-0008-04 (sweeps all parameters including GABA side under the rotation-proxy
protocol); this is excitation-only under the native driver, addressable only now that t0020
localised the gap. Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary>🧪 <strong>Experimentally test NMDA-spike contribution to DSGC direction
selectivity via compartmental simulation</strong> (S-0016-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0016-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0016_literature_survey_dendritic_computation`](../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md) |
| **Source paper** | [`10.1038_35005094`](../../tasks/t0016_literature_survey_dendritic_computation/assets/paper/10.1038_35005094/) |
| **Categories** | [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

The answer asset dendritic-computation-motifs-for-dsgc-direction-selectivity identifies NMDA
spikes as the highest-confidence transferable motif. Build a NEURON/NetPyNE compartmental DSGC
model with explicit NMDA synapses (dynamic Mg2+ block, NMDA:AMPA ratio swept from 0.5 to 2.0)
and test whether spatially-clustered co-directional bipolar-cell input produces supralinear
summation during preferred-direction motion and is suppressed by asymmetric inhibition during
null-direction motion. Compare the resulting DSI (direction selectivity index) against the
no-NMDA baseline to quantify the NMDA-spike contribution to DS.

</details>

<details>
<summary>🧪 <strong>Factorial (g_Na, g_K) grid search on a DSGC compartmental model
to locate the DSI-maximising conductance ridge</strong> (S-0002-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1152_jn.00123.2009`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1152_jn.00123.2009/) |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

No paper in the 20-paper corpus (including Fohlmeister2010, Schachter2010, PolegPolsky2016,
Vaney2012) reports a factorial grid search over somatic (g_Na, g_K) pairs for a DSGC — this is
the central gap identified for RQ1 by the survey. Run a grid with g_Na swept across 0.02-0.20
S/cm^2 and g_K (delayed rectifier) swept across 0.003-0.050 S/cm^2 on the baseline DSGC
morphology and 177+177 synaptic budget, record DSI, preferred peak, null residual, and
tuning-curve HWHM at each point, and publish the ridge of combinations that hit DSI 0.7-0.85
with peak 40-80 Hz and null < 10 Hz. This directly supplies the RQ1 answer the project needs.
Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Factorial morphology sweep (branch orders, segment length,
segment diameter) at fixed synapse count</strong> (S-0002-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1523_ENEURO.0261-21.2021`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_ENEURO.0261-21.2021/) |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

ElQuessny2021 concludes that global DSGC morphology has only a minor effect on the synaptic
E/I distribution, but the survey finds no paper that runs a clean factorial sweep over the
three local-electrotonic knobs separately. With synaptic count fixed at the PolegPolsky
177+177 baseline and dendrites set to active (Schachter2010 densities), vary (number of branch
orders, mean segment length, mean segment diameter) on an orthogonal grid, record DSI and HWHM
per point, and test whether segment diameter has the largest effect (as cable theory
predicts). This directly answers RQ2 and provides the morphology-sensitivity map the project
currently lacks. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Hand-port deRosenroll2026 ds-circuit-ei model and remap 8-angle
grid to 12 angles</strong> (S-0010-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0010-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0010_hunt_missed_dsgc_models`](../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md) |
| **Source paper** | [`10.1016_j.celrep.2025.116833`](../../tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1016_j.celrep.2025.116833/) |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |

Port geoffder/ds-circuit-ei-microarchitecture (Zenodo 10.5281/zenodo.17666157, MIT LICENSE).
Requires adding statsmodels, h5py, fastparquet, oiffile as optional deps (or extracting a
minimal driver subset without them), then extending the hardcoded 8-direction ANGLES_DEG list
to the canonical 12-angle protocol before scoring. t0010 exited at P2 within the 90-min cap;
budget 4-6 hours for full P3.

</details>

<details>
<summary>🧪 <strong>Implement AIS compartment, NMDARs, and simulated voltage-clamp
block in the downstream DSGC model build task</strong> (S-0017-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0017-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0017_literature_survey_patch_clamp`](../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`patch-clamp`](../../meta/categories/patch-clamp/) |

The answer asset patch-clamp-techniques-and-constraints-for-dsgc-modelling produces a 7-point
specification for DSGC modelling in NEURON extending the cable-theory and
dendritic-computation specifications from t0015 and t0016. The downstream DSGC
compartmental-model build task must implement: (1) an explicit AIS compartment with Nav1.6 at
7x the somatic Na+ density, with AIS length as a tunable parameter; (2) NMDARs with standard
Mg2+ block kinetics on DSGC dendrites alongside AMPARs; (3) a simulated somatic voltage-clamp
block (SEClamp) so experimental and simulated voltage-clamp readouts can be compared on the
same footing; (4) depolarisation-block threshold and AMPA/NMDA charge ratio during preferred
and null motion as named fitting objectives. Validation must include DSI reduction under
simulated NMDAR block to match Sethuramanujam2017 and maintained activity under simulated
synaptic blockade to resolve the MargolisDetwiler2007 intrinsic-vs-synaptic question for the
target DSGC subtype.

</details>

<details>
<summary>🧪 <strong>Implement AMPA + NMDA + GABA_A synapses with E-I temporal
co-tuning and SAC-to-DSGC asymmetric inhibition in downstream DSGC
model</strong> (S-0018-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0018-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0018_literature_survey_synaptic_integration`](../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |

The answer asset synaptic-integration-priors-for-dsgc-modelling produces a 6-point
specification for DSGC synaptic integration in NEURON extending the space-clamp/AIS/NMDAR
constraints from t0017. The downstream DSGC compartmental-model build task must implement: (1)
AMPA with dual-exponential kinetics (tau_rise 0.2-0.4 ms, tau_decay 1-3 ms) and NMDA with
Mg2+-block + tau_decay 100-200 ms at 32 degC on glutamatergic inputs, (2) GABA_A with shunting
(reversal near resting Vm) and tau_decay 5-20 ms on SAC inputs, (3) E->I temporal lag of 15-50
ms on preferred-direction stimuli reproducing Wehr & Zador 2003 co-tuning, (4) asymmetric
GABAergic inputs that are strong on null-side dendrites (to match Euler-Detwiler-Denk 2002 SAC
Ca2+ DS index 0.3-0.5) and weak on preferred-side dendrites, (5) dendritic-location-dependent
EPSP attenuation consistent with Hausser-Mel lambda_DC 100-300 um, (6) named fitting
objectives for DSI under shunting-inhibition block (should drop toward 0) and EPSP/IPSP charge
balance during null-direction motion.

</details>

<details>
<summary>📚 <strong>Instantiate AIS_PROXIMAL / AIS_DISTAL / THIN_AXON channel sets on
t0022 as a t0033 optimiser prerequisite</strong> (S-0033-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0033-02` |
| **Kind** | library |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0033_plan_dsgc_morphology_channel_optimisation`](../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

The t0022 testbed exposes AIS_PROXIMAL, AIS_DISTAL, and THIN_AXON channel-set hooks in its
modular architecture, but all three are empty because the Poleg-Polsky 2026 backbone has no
axon. The t0033 joint optimiser plans per-region gbar for Nav1.1, Nav1.6, Kv1.2, Kv2.1,
Kv3.1/3.2 and Km/KCNQ across these regions, which is impossible until the hooks are live.
Build a task that (a) adds a short axon hillock + AIS + thin-axon trunk to t0022 using Werginz
2020 / Van Wart 2007 geometry, (b) populates AIS_PROXIMAL with Nav1.1+Kv1.2, AIS_DISTAL with
Nav1.6+Kv3, and THIN_AXON with Nav1.6+Kdr at literature-consensus densities, (c) reruns the
t0022 12-angle sweep and checks DSI and peak rate do not regress, and (d) registers a new
sibling library asset. Recommended task types: infrastructure-setup, build-model,
write-library.

</details>

<details>
<summary>🧪 <strong>Integrate tuning_curve_loss into the t0008 Poleg-Polsky DSGC
reproduction to score the ported ModelDB 189347 curve</strong> (S-0012-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0012-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0012_tuning_curve_scoring_loss_library`](../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

t0008 (port ModelDB 189347) is the first downstream consumer that will produce a real
simulated 12-angle tuning curve. Wire tuning_curve_loss.score into t0008's verification step
so the Poleg-Polsky reproduction's simulated curve is scored against the t0004 target and the
resulting ScoreReport.to_metrics_dict() is written straight into t0008/results/metrics.json
under the four registered keys (direction_selectivity_index, tuning_curve_hwhm_deg,
tuning_curve_reliability, tuning_curve_rmse). Deliverable: a short task that runs t0008's
simulated curve through score(), records ScoreReport.loss_scalar and passes_envelope, and
produces a side-by-side overlay plot (simulated vs target). This is the first end-to-end
validation that the scorer library does what it promises on a non-trivial candidate.
Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary>🔧 <strong>Interpolate soma pt3dadd diameters along the principal axis to
replace the uniform 4.118 um soma radius</strong> (S-0009-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-02` |
| **Kind** | technique |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0009_calibrate_dendritic_diameters`](../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../tasks/t0009_calibrate_dendritic_diameters/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

All 19 CNG soma rows currently receive the same averaged 4.118 um radius, flattening the
bell-shaped taper (~3.07 um to 5.31 um) visible in the five central Poleg-Polsky pt3dadd soma
contour points. Run PCA on the 19 soma xyz coordinates, project each row onto the first
principal component, and assign a radius by linear interpolation over the 7 Poleg-Polsky
pt3dadd values mapped onto the same axis. Emit a corrections file that overrides the 19
soma-row radii in dsgc-baseline-morphology-calibrated. Fixes the on-soma current-density
distribution for downstream spike-initiation simulations without changing the mean soma radius
or any dendritic row. Creative_thinking.md section F4. Recommended task types:
feature-engineering, correction.

</details>

<details>
<summary>🔧 <strong>Inverse-fit three-bin dendritic radii against the Schachter 2010
proximal/distal input-resistance gradient</strong> (S-0009-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-01` |
| **Kind** | technique |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0009_calibrate_dendritic_diameters`](../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Source paper** | [`10.1371_journal.pcbi.1000899`](../../tasks/t0009_calibrate_dendritic_diameters/assets/paper/10.1371_journal.pcbi.1000899/) |
| **Categories** | [`cable-theory`](../../meta/categories/cable-theory/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

The calibrated proximal Rin (0.52 MOhm) and distal Rin (54 MOhm) are far below Schachter
2010's 150-200 MOhm proximal and >1 GOhm distal targets because the pure-literature
Poleg-Polsky three-bin radii are not tuned to our cell. Keep the three-bin (primary / mid /
terminal) structure but treat the three radii as free parameters; fit them in a NEURON
passive-properties simulation (Ra=100 Ohm-cm, Rm fit jointly) so that soma Rin lands in
150-200 MOhm and distal-tip Rin >= 1 GOhm. Seed the optimiser with the Poleg-Polsky means
(3.694/1.653/0.439 um) and emit a corrections file that overrides
dsgc-baseline-morphology-calibrated with the fitted radii. Blocks downstream DSI reproductions
against Schachter's tree. Recommended task types: feature-engineering, experiment-run.

</details>

<details>
<summary>🔧 <strong>Multi-fidelity surrogate-NN prototype to reduce the $41.56
training burn on the recommended optimiser cell</strong> (S-0033-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0033-03` |
| **Kind** | technique |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0033_plan_dsgc_morphology_channel_optimisation`](../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

The recommended Surrogate-NN-GA cell in t0033 has central cost $50.54, of which $41.56 is the
one-shot 5,000-sample training burn. Creative-thinking alternative #1 argued that a
multi-fidelity surrogate (train on coarse-dt or shallow-AR(2), filter, re-score top decile on
full fidelity) should cut training USD 2-3x. Build a prototype task that (a) defines two
fidelities on the existing t0022 or t0024 port — full (dt=0.1 ms, AR(2) rho=0.6, 10 trials) vs
coarse (dt=0.25 ms, deterministic or AR(1), 3 trials) — while keeping the Jain 2020 5-10 um
compartment floor, (b) trains a 3-layer MLP surrogate on a 500-sample Latin-hypercube over the
25 committed parameters at coarse fidelity, (c) measures regret between coarse-filtered top-k
and full-fidelity top-k, and (d) reports realised training-USD reduction. Recommended task
types: experiment-run, feature-engineering.

</details>

<details>
<summary>🧪 <strong>Nav1.1 proximal-AIS knockout channel-swap on the t0022
testbed</strong> (S-0022-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0022-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0022_modify_dsgc_channel_testbed`](../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Source paper** | [`10.1016_j.neuron.2007.07.031`](../../tasks/t0022_modify_dsgc_channel_testbed/assets/paper/10.1016_j.neuron.2007.07.031/) |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`patch-clamp`](../../meta/categories/patch-clamp/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

Use the t0022 modeldb_189347_dsgc_dendritic library's AIS_PROXIMAL forsec block to append a
proximal axon segment populated with Nav1.1 at ~7x somatic density, then knock it out (set
gbar to 0) and rerun the canonical 12-angle x 10-trial sweep. VanWart2006 reports Nav1.1
dominates the proximal AIS while Nav1.6 dominates the distal AIS; removing proximal Nav1.1
should drop excitability and test whether DSI survives reduced spike-initiation margin.
Expected outcome: peak rate drops below 10 Hz while DSI holds above 0.5 (inhibitory shunt
intact, spike threshold only moved). Dependencies: t0022 library asset. Effort ~6 hours.
Recommended task type: experiment-run.

</details>

<details>
<summary>🧪 <strong>Nav1.6 distal-AIS density sweep to close the 15 Hz -> 30-40 Hz
peak-rate gap</strong> (S-0022-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0022-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0022_modify_dsgc_channel_testbed`](../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Source paper** | [`10.1523_jneurosci.0130-07.2007`](../../tasks/t0022_modify_dsgc_channel_testbed/assets/paper/10.1523_jneurosci.0130-07.2007/) |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`patch-clamp`](../../meta/categories/patch-clamp/) |

Sweep Nav1.6 density in the AIS_DISTAL forsec block over {4, 6, 8, 10, 12, 14, 16} S/cm^2
(centred on the Kole-Stuart 2008 ~8 S/cm^2 published anchor) with Kv1.2 held constant, rerun
the 12-angle x 10-trial sweep at each setting, and report peak firing rate vs Nav1.6 density.
Peak-rate cap at 10-20 Hz is shared across t0008 (18.1 Hz), t0020 (14.85 Hz), and t0022 (15
Hz) and is inherited from the unchanged t0008 HHst Na/K density, so the fix lives in the
distal AIS. Expected outcome: peak rate scales monotonically with Nav1.6 density and lands
inside 30-40 Hz at ~8 S/cm^2, matching Poleg-Polsky & Diamond 2016 and Oesch2005.
Dependencies: t0022 library asset. Effort ~12 hours. Recommended task type: experiment-run,
comparative-analysis.

</details>

<details>
<summary>🧪 <strong>Per-dendrite E-I parameter sweep to map the DSI response
surface</strong> (S-0022-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0022-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0022_modify_dsgc_channel_testbed`](../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Source paper** | [`10.1523_JNEUROSCI.5017-13.2014`](../../tasks/t0022_modify_dsgc_channel_testbed/assets/paper/10.1523_JNEUROSCI.5017-13.2014/) |
| **Categories** | [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

The t0022 driver has three free per-dendrite parameters fixed at single points:
EI_OFFSET_PREFERRED_MS = 10 ms, GABA_NULL/GABA_PREF ratio = 4x (12 nS / 3 nS), AMPA
conductance = 6 nS. Run a factorial sweep over EI_OFFSET in {5, 10, 15} ms, GABA ratio in {2,
3, 4, 6}, and AMPA in {0.15, 0.3, 0.6} nS (the last anchored to Park2014's 0.31 nS somatic
measurement) to quantify mechanism robustness. Expected outcome: a (3 x 4 x 3) = 36-point DSI
response surface showing which E-I corner of the parameter space saturates DSI at 1.0 (driver
is too deterministic) vs produces a graded DSI in the Park2014 0.65 +/- 0.05 band (mechanism
tracks continuous inhibition as real DSGCs do). Dependencies: t0022 library asset. Effort ~20
hours with the existing process-pool orchestrator. Recommended task type: experiment-run,
data-analysis.

</details>

<details>
<summary>📚 <strong>Port Hanson 2019 Spatial-Offset-DSGC as a second DSGC
library</strong> (S-0008-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0008-01` |
| **Kind** | library |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0008_port_modeldb_189347`](../../overview/tasks/task_pages/t0008_port_modeldb_189347.md) |
| **Source paper** | [`10.7554_eLife.42392`](../../tasks/t0008_port_modeldb_189347/assets/paper/10.7554_eLife.42392/) |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

Port the Hanson et al. 2019 Spatial-Offset-DSGC-NEURON-Model
(github.com/geoffder/Spatial-Offset-DSGC-NEURON-Model) using the same HOC-driver pattern
proven in t0008. Hanson 2019 shares RGCmodel.hoc and HHst.mod with ModelDB 189347 and already
ships a Python driver (offsetDSGC.py); it implements DS via an explicit spatial-offset
mechanism that matches the rotation-based protocol used in t0008 more directly than
Poleg-Polsky's gabaMOD parameter swap. Expected effort ~8 hours; outcome is a second library
asset and a sanity comparison of the envelope miss pattern across two DSGC models. Recommended
task types: code-reproduction, write-library.

</details>

<details>
<summary>🔧 <strong>Port the full upstream SacNetwork with bp_locs/probs/deltas to
reproduce the deRosenroll correlation-drop effect</strong> (S-0024-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0024-01` |
| **Kind** | technique |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0024_port_de_rosenroll_2026_dsgc`](../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md) |
| **Source paper** | [`10.1016_j.celrep.2025.116833`](../../tasks/t0024_port_de_rosenroll_2026_dsgc/assets/paper/10.1016_j.celrep.2025.116833/) |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |

The t0024 port misses REQ-5 on all three sub-criteria (corr DSI 0.82 vs paper target
[0.30,0.50]; uncorr DSI 0.84 vs [0.18,0.35]; drop fraction 0.000 vs >=0.20) because the AR(2)
correlation was applied at per-terminal Exp2Syn drivers rather than across the
spatially-distributed SAC varicosity release network that the paper identifies as the causal
substrate. Port the upstream SacNetwork class (bp_locs, probs, deltas) from
geoffder/ds-circuit-ei-microarchitecture into a new sibling library asset, drive the same
cell, and rerun the 8-direction correlated/uncorrelated sweep. Target: reproduce the ~0.39 ->
~0.25 DSI drop.

</details>

<details>
<summary>📚 <strong>Port the Poleg-Polsky & Diamond 2016 DSGC ModelDB 189347 into
the project as a library asset</strong> (S-0003-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0003-02` |
| **Kind** | library |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0003_simulator_library_survey`](../../overview/tasks/task_pages/t0003_simulator_library_survey.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

Download ModelDB 189347 (the only public DSGC NEURON model), re-run its included demo, and
register the resulting Python package as a library asset under `assets/library/`. This makes
the DSGC reference implementation available to every downstream simulation task without
re-download.

</details>

<details>
<summary>📂 <strong>Record per-trial soma spike times from modeldb_189347_dsgc to
exercise plot_angle_raster_psth on real data</strong> (S-0011-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0011-01` |
| **Kind** | dataset |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0011_response_visualization_library`](../../overview/tasks/task_pages/t0011_response_visualization_library.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

The tuning_curve_viz raster+PSTH plot is currently exercised only by a deterministic synthetic
Poisson fixture (seed 42) because neither t0004 nor t0008 emits spike times. Extend the t0008
Poleg-Polsky NEURON driver to record soma membrane voltage, threshold-detect action
potentials, and write a spike-time CSV with columns (angle_deg, trial_seed, spike_time_s)
alongside the existing tuning-curve CSV. Target: 12 angles x 8 trials of spike times for the
baseline ModelDB 189347 port. Once available, re-point tuning_curve_viz.test_smoke.raster_psth
to the real CSV and add the resulting PNGs to assets/library/tuning_curve_viz/files/ via a
correction, replacing the synthetic fixture outputs. Recommended task types:
feature-engineering, code-reproduction.

</details>

<details>
<summary>📊 <strong>Reproduce Poleg-Polsky 2016 Fig 1D/H subthreshold validation
targets (PSP amplitude, NMDAR slope angle)</strong> (S-0020-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-02` |
| **Kind** | evaluation |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0020_port_modeldb_189347_gabamod`](../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../tasks/t0020_port_modeldb_189347_gabamod/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`patch-clamp`](../../meta/categories/patch-clamp/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

compare_literature.md flags that the paper reports concrete subthreshold validation targets
that this task did not measure: PD NMDAR-mediated PSP component 5.8 +/- 3.1 mV and ND 3.3 +/-
2.8 mV (Fig 1D, n=19), and NMDAR multiplicative scaling slope angle 62.5 +/- 14.2 deg (Fig 1H,
additive baseline 45 deg). Extend the gabaMOD-swap driver to record somatic whole-cell voltage
traces (v_soma, not just spike count) across the 40-trial sweep, compute (1) the peak PSP
amplitude in a 0-200 ms post-stimulus window per condition and (2) the slope-angle regression
over a scan of AMPA vs NMDA drive ratios, then gate each against the paper's n=19 mean +/- SD
intervals. This turns a single spike-output check into a multi-level subthreshold validation
that exercises the cell's passive and NMDA-block biophysics independently of spike
thresholding. Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary>🧪 <strong>Rerun t0039 7-diameter sweep on t0024 for active-vs-passive
testbed comparison</strong> (S-0039-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0039-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`cable-theory`](../../meta/categories/cable-theory/), [`dendritic-computation`](../../meta/categories/dendritic-computation/) |

t0039 on t0022 at GABA=4 nS produced a passive_filtering signature (slope=-0.034, p=0.008).
Rerun the same 7-diameter sweep on t0024 (de_rosenroll_2026_dsgc, richer channel inventory,
AR(2) stochastic release) at its equivalent operational GABA level to test whether the
Schachter2010 concave-down signature emerges when active dendritic machinery is available. If
t0024 shows concave-down and t0022 shows monotonic decrease, that is the cleanest
testbed-level discrimination between the two mechanisms the project has produced. If both show
passive_filtering, that rules out Schachter2010 across the substrates the project has
available.

</details>

<details>
<summary>🧪 <strong>Retrieve paywalled cable-theory PDFs via Sheffield access and
verify numerical claims</strong> (S-0015-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0015-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0015_literature_survey_cable_theory`](../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md) |
| **Source paper** | — |
| **Categories** | [`cable-theory`](../../meta/categories/cable-theory/), [`retinal-ganglion-cells`](../../meta/categories/retinal-ganglion-cells/) |

Five foundational cable-theory papers (Rall 1967, Koch-Poggio-Torre 1982, Mainen-Sejnowski
1996, Taylor 2000, Dhingra-Smith 2004) are documented in intervention/paywalled_papers.md but
were not downloaded. Retrieve their PDFs through Sheffield institutional access, update each
paper asset's download_status to 'success', replace summary Overview disclaimers with
PDF-verified content, and cross-check the numerical claims in the synthesis (electrotonic
length L ≈ 0.5-0.8, contrast thresholds 1.5% / 3.8%, ~60% gray-level loss) against the actual
papers.

</details>

<details>
<summary>🧪 <strong>Retrieve paywalled dendritic-computation PDFs via Sheffield
access and verify numerical claims</strong> (S-0016-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0016-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0016_literature_survey_dendritic_computation`](../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md) |
| **Source paper** | — |
| **Categories** | [`dendritic-computation`](../../meta/categories/dendritic-computation/) |

Five foundational dendritic-computation papers (Schiller 2000, Polsky 2004, Larkum 1999,
Bittner 2017, London & Hausser 2005) are documented in intervention/paywalled_papers.md but
were not downloaded. Retrieve their PDFs through Sheffield institutional access, update each
paper asset's download_status to 'success', replace summary Overview disclaimers with
PDF-verified content, and cross-check the numerical claims in the synthesis (NMDA-spike
threshold -50 mV, NMDA-spike duration 20-40 ms, 2-3x supralinear amplification, Ca2+ plateau
duration 30-50 ms, BAC burst 100-200 Hz, BTSP eligibility window of seconds) against the
actual papers.

</details>

<details>
<summary>🧪 <strong>Retrieve paywalled patch-clamp PDFs via Sheffield access and
verify numerical claims</strong> (S-0017-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0017-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0017_literature_survey_patch_clamp`](../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md) |
| **Source paper** | — |
| **Categories** | [`patch-clamp`](../../meta/categories/patch-clamp/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

Five patch-clamp / voltage-clamp / space-clamp papers (Poleg-Polsky & Diamond 2011, To et al.
2022, Werginz et al. 2020, Sethuramanujam et al. 2017, Margolis & Detwiler 2007) are
documented in intervention/paywalled_papers.md but were not downloaded. Retrieve their PDFs
through Sheffield institutional access, update each paper asset's download_status to
'success', replace summary Overview disclaimers with PDF-verified content, and cross-check the
numerical claims in the synthesis (~80% signal loss on thin distal dendrites, 7x AIS-to-soma
Na+ density ratio, AMPA/NMDA charge ratios during preferred and null motion, proportion of
OFF-cell maintained activity that survives synaptic blockade) against the actual papers.

</details>

<details>
<summary>🧪 <strong>Retrieve paywalled synaptic-integration PDFs via Sheffield access
and verify numerical priors</strong> (S-0018-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0018-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0018_literature_survey_synaptic_integration`](../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

Five synaptic-integration papers (Lester et al. 1990, Koch-Poggio-Torre 1983, Wehr & Zador
2003, Hausser & Mel 2003, Euler-Detwiler-Denk 2002) are documented in
intervention/paywalled_papers.md but were not downloaded. Retrieve their PDFs through
Sheffield institutional access, update each paper asset's download_status to 'success',
replace summary Overview disclaimers with PDF-verified content, and cross-check the numerical
priors tabulated in the Prior Distribution Table of the answer asset (NMDAR tau_decay 100-200
ms at 22-32 degC, AMPA tau_rise 0.2-0.4 ms / tau_decay 1-3 ms, GABA_A tau_decay 5-20 ms,
lambda_DC 100-300 um for RGC dendrites, DSGC E-I lag 15-50 ms, SAC dendritic Ca2+ DS index
0.3-0.5) against the actual papers before adopting them as tight compartmental-model fitting
targets.

</details>

<details>
<summary>🧪 <strong>Retrieve paywalled voltage-gated-channel PDFs via Sheffield
access and verify numerical priors</strong> (S-0019-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0019-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0019_literature_survey_voltage_gated_channels`](../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

Five voltage-gated-channel papers (Van Wart-Trimmer-Matthews 2006, Kole-Letzkus-Stuart 2007,
Fohlmeister & Miller 1997, Hu et al. 2009, Kole et al. 2008) are documented in
intervention/paywalled_papers.md but were not downloaded. Retrieve their PDFs through
Sheffield institutional access, update each paper asset's download_status to 'success',
replace summary Overview disclaimers with PDF-verified content, and cross-check the numerical
priors tabulated in the Nav/Kv Combinations Table of the answer asset (Nav1.6 V_half around
-45 mV, Nav1.2 V_half around -32 mV, AIS Nav gbar 2500-5000 pS/um2, Kv1 V_half -40 to -50 mV,
Fohlmeister-Miller alpha/beta coefficients at 22 degC, Q10 near 3) against the actual papers
before adopting them as tight compartmental-model fitting targets.

</details>

<details>
<summary>📊 <strong>Specify primary DSI as t0033 optimiser objective on t0024
substrate (not vector-sum) and drop monotonic-length priors</strong>
(S-0034-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0034-07` |
| **Kind** | evaluation |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0034_distal_dendrite_length_sweep_t0024`](../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

t0034 establishes two facts that directly constrain the t0033 joint morphology+VGC optimiser
design: (1) primary DSI on t0024 has measurable dynamic range (0.545-0.774, spread 0.229,
p=0.038), so the optimiser CAN use primary DSI as the objective - no need to fall back to
vector-sum DSI as S-0030-06 proposed for t0022; (2) the DSI-vs-length curve is non-monotonic
with a net negative slope, opposite to Dan2018's monotonic-increase prior - the optimiser must
NOT assume longer distal dendrites yield higher DSI. Register as a t0033 planning correction:
pick t0024 as the optimisation testbed, use primary DSI as the objective, and seed the
length-axis initial distribution near 0.75x-1.0x (observed peak). Distinct from S-0030-06
(vector-sum DSI on t0022) - this clarifies that t0024 is the correct substrate. Recommended
task types: comparative-analysis, answer-question.

</details>

<details>
<summary>🧪 <strong>Surface-density-rescaled Nav diameter sweep on t0024 to test
surface-vs-volume compensation</strong> (S-0035-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0035-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0035_distal_dendrite_diameter_sweep_t0024`](../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

Re-run a small diameter sweep (0.5x, 1.0x, 2.0x) on the t0024 DSGC with gnabar_HHst rescaled
by 1/d in the distal compartments so the total per-section Nav count is held fixed as diameter
varies. Creative_thinking hypothesis 2 proposes that the flat DSI-vs-diameter result (t0035)
arises because NEURON's surface-density gbar scales total channel current by d while axial
load scales by d^2, cancelling the net effect. If density rescaling produces a non-flat DSI
trend, the compensation confound is confirmed; if still flat, rule out this hypothesis.
Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Swap bipolar-cell sustained vs transient kinetics on t0024 to
discriminate kinetic tiling from cable delay</strong> (S-0027-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0027-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0027_literature_survey_morphology_ds_modeling`](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

Run t0024 (de Rosenroll 2026 port) with bipolar-cell kinetic identities swapped: assign
sustained kinetics to distal terminals and transient kinetics to proximal terminals, opposite
to the wild-type tiling. Prediction (creative_thinking.md #2): if [Srivastava2022]
kinetic-tiling is causally responsible for SAC DS, the swap reverses preferred direction; if
[Kim2014] cable delay is causal, the swap only reduces DSI magnitude without flipping
preferred direction. Critical for choosing between two competing centrifugal-DS mechanisms
before committing to a morphology sweep design.

</details>

<details>
<summary>🧪 <strong>Sweep AR(2) rho x V_rest for t0024 to separate noise correlation
from depolarisation effects</strong> (S-0026-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0026-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0026_vrest_sweep_tuning_curves_dsgc`](../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |

The t0024 V_rest sweep ran only at rho=0.6 and showed a 1.9x U-shaped DSI curve with HWHM
pinned at 65-83 deg. Repeat the sweep at rho in {0.0, 0.3, 0.6, 0.9} to test whether the
tuning-smoothing is dominated by AR(2) correlation or by the depolarisation itself. Expected
outcome: rho=0.0 should recover tuning sharpness closer to t0022 while preserving the
Na-inactivation-independent peak firing behaviour.

</details>

<details>
<summary>🧪 <strong>Validate custom khhchan.mod biophysics with a dedicated sanity
simulation</strong> (S-0007-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0007-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0007_install_neuron_netpyne`](../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

The t0007 sanity sims only exercise NEURON's built-in hh mechanism. khhchan.mod is compiled as
a smoke test but its biophysics are never run. Add a short task that inserts khhchan on a
1-compartment soma, drives it with the same IClamp protocol, and compares the resulting trace
against the built-in hh to confirm the custom mechanism produces physiologically plausible
spikes before downstream retinal tasks depend on it.

</details>

<details>
<summary>📚 <strong>Write a shared arf.scripts.utils.resolve_doi helper that returns
title, authors, venue, year, PMID, and PMCID</strong> (S-0013-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0013-01` |
| **Kind** | library |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0013_resolve_morphology_provenance`](../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md) |
| **Source paper** | — |
| **Categories** | — |

This task discovered that the t0005 plan nominated DOI 10.1016/j.neuron.2018.05.028 as 'Morrie
& Feller 2018 Neuron' but that DOI actually resolves to Li, Vaughan, Sturgill & Kepecs (2018),
an unrelated CSHL viral-tracing paper. The /add-paper skill already performs DOI resolution
internally via CrossRef and PubMed, but that logic is not exposed as a reusable utility, so
planning-stage agents have no cheap way to sanity-check a candidate DOI before locking it into
a plan. Build arf.scripts.utils.resolve_doi as a thin wrapper over CrossRef and PubMed
E-utilities that returns a typed dataclass with title, first-author last name, venue, year,
PMID, and PMCID; wire it into /add-paper to replace the inline resolution; and document the
callable interface so the verificator in S-0013-02 and other planning-time validators can
import it. Recommended task types: write-library.

</details>

## Medium Priority

<details>
<summary>🧪 <strong>5-parameter CMA-ES vs Bayesian-optimisation spike on t0022 to
validate sample-efficiency assumptions</strong> (S-0033-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0033-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0033_plan_dsgc_morphology_channel_optimisation`](../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/) |

The t0033 cost model commits literature-derived sample counts (CMA-ES=1,300, BO=500,
Surrogate-NN-GA=18,500) on 25 dims without empirical DSGC validation. Before the full joint
optimiser is commissioned, run a low-dim spike on t0022: (a) pick 5 representative parameters
from the committed 25 (3 Cuntz scalars: bf, distal-length, distal-diameter + gNa_dend +
gKdr_dend), (b) run 200-300 deterministic 12-angle evaluations each under CMA-ES and
sequential BO, (c) compare the DSI converged-to-within-1% sample count against the cost-grid
extrapolations, and (d) report whether either method actually converges on DSGC landscapes or
hits plateaus that the corpus did not flag. Outcome calibrates the strategy row of the cost
model before the 25-dim run. Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary>📊 <strong>Add a per-trial spike-count floor to the two-point envelope gate
to catch biologically implausible passes</strong> (S-0020-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-05` |
| **Kind** | evaluation |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0020_port_modeldb_189347_gabamod`](../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

Plan Risks & Fallbacks explicitly anticipated this scenario: DSI can land inside the envelope
while absolute firing rates stay unrealistically low (t0020 recorded DSI 0.7838 / peak 14.85
Hz exactly here). The current gate checks (mean_PD in [40, 80] Hz, DSI in [0.70, 0.85]) but
does not enforce biological plausibility at the trial level: the gate could pass with, say,
one trial firing 80 Hz and nineteen firing 0 Hz. Extend the envelope gate (in
tuning_curve_loss or the t0020 scorer) to add a trial-level floor: require that at least
N_pd_pass PD trials fire above a biological minimum threshold (e.g., 5 Hz). Report the
per-trial floor result alongside the mean-based envelope. Rerun scoring over t0020's existing
40-trial CSV to verify the new gate flags the current run as failed on the floor (baseline
expectation). Recommended task types: write-library, experiment-run.

</details>

<details>
<summary>📚 <strong>Add a Starburst Amacrine Cell feedforward layer to drive
inhibition physiologically</strong> (S-0022-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0022-04` |
| **Kind** | library |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0022_modify_dsgc_channel_testbed`](../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Source paper** | [`10.1038_nature00931`](../../tasks/t0022_modify_dsgc_channel_testbed/assets/paper/10.1038_nature00931/) |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

The t0022 driver schedules GABA directly onto each DSGC dendrite, skipping the SAC (Starburst
Amacrine Cell) layer that shapes DS inhibition in vivo (Euler-Detwiler-Denk 2002). Extend the
modeldb_189347_dsgc_dendritic library with a configurable SAC layer: an array of simplified
SAC models (single-compartment or 2-compartment) whose dendritic output drives DSGC GABA
synapses via NetCon, with SAC dendrites themselves direction-tuned per Euler2002. Expected
outcome: DSI becomes graded rather than saturated (real SAC output is not a hard half-plane
step) and peak firing rate may rise because SAC inhibition is timed to bar arrival not to a
global half-plane rule. This is a library extension not just a channel swap; produces a fourth
DSGC library asset modeldb_189347_dsgc_sac. Dependencies: t0022 library asset, Euler2002
paper. Effort ~40 hours. Recommended task type: write-library, code-reproduction.

</details>

<details>
<summary>📚 <strong>Add combined-report function that renders all four plot types
into one multi-page PDF/HTML per model</strong> (S-0011-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0011-03` |
| **Kind** | library |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0011_response_visualization_library`](../../overview/tasks/task_pages/t0011_response_visualization_library.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

The four tuning_curve_viz functions currently produce seven standalone PNGs per model. A
combined per-model report (one PDF with matplotlib.backends.backend_pdf.PdfPages or an HTML
file embedding the PNGs plus a parameter header) would give a single shareable artefact for
reviewers, brainstorm sessions, and any future project paper draft. Add
tuning_curve_viz.report.build_model_report(curve_csv, out_path, *, target_csv=None,
spike_times_csv=None, title=None, params=None) that collects the existing four plots plus a
header block of model metadata (name, git SHA, DSI, peak, null, HWHM from tuning_curve_loss)
and emits either PDF (default) or HTML (--format html). Exercise in the smoke test by
rendering a report for the target curve and for t0008. Recommended task types: write-library.

</details>

<details>
<summary>📚 <strong>Add statistical-comparison overlays (paired bootstrap, DSI/HWHM
annotations) to multi-model plots</strong> (S-0011-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0011-04` |
| **Kind** | library |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0011_response_visualization_library`](../../overview/tasks/task_pages/t0011_response_visualization_library.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

plot_multi_model_overlay currently draws every model as a coloured line with a shared legend
but provides no quantitative comparison on the figure itself. Extend the overlay to optionally
annotate each model with its DSI, peak rate, null rate, and HWHM (computed via
tuning_curve_loss.metrics) in the legend, and add a plot_model_comparison(model_a_csv,
model_b_csv, target_csv, out_png) function that computes a paired bootstrap
difference-of-means between two models at every angle, draws the difference curve with a
shaded 95 percent CI, and shades angles where the CI excludes zero. This turns qualitative
overlay comparisons into formally comparable figures suitable for the headline DSI-residual
reporting in S-0002-01 / S-0008-04 calibration sweeps. Recommended task types: write-library.

</details>

<details>
<summary>📚 <strong>Add strict angle-grid validation mode to
tuning_curve_viz.loaders.validate_angle_grid</strong> (S-0011-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0011-02` |
| **Kind** | library |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0011_response_visualization_library`](../../overview/tasks/task_pages/t0011_response_visualization_library.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

The current validate_angle_grid is permissive: it accepts 8/12/16 uniformly-spaced angle
counts and only warns on non-uniform grids. Downstream optimisation and scoring tasks (e.g.,
S-0002-01 g_Na/g_K grid search, S-0012-03 tuning_curve_loss integration) need hard guarantees
that every CSV is on the project-canonical 12-angle 30-degree grid before plots are compared.
Add a strict_mode=False parameter to validate_angle_grid that, when True, raises ValueError
unless angles exactly match np.arange(0, 360, 30.0) to within 1e-6 degree. Add a matching
--strict-angle-grid CLI flag to tuning_curve_viz.cli. Ship unit tests covering:
strict+canonical (pass), strict+8-angle (raise), strict+12-angle-shifted-by-1-degree (raise),
permissive (current behaviour preserved). Recommended task types: write-library.

</details>

<details>
<summary>🔧 <strong>Alternative loss formulations (L1, max-residual,
weighted-L-infinity) benchmarked against the Euclidean default</strong>
(S-0012-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0012-04` |
| **Kind** | technique |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0012_tuning_curve_scoring_loss_library`](../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

tuning_curve_loss currently computes loss_scalar as a weighted Euclidean (L2) norm of four
normalised residuals. Downstream optimisers may prefer L1 (more robust to a single bad metric,
sub-gradient at zero), max-residual / L-infinity (guarantees every individual target is within
a budget), or Huber (quadratic near zero, linear in the tails). Add pluggable
loss_kind='l2'|'l1'|'linf'|'huber' to score and score_curves, keep 'l2' as the default to
preserve the identity contract, and add parametrised tests that exercise each norm on the same
synthetic inputs used by test_envelope.py. Once downstream grid searches (S-0002-01,
S-0002-04, S-0002-05) have produced O(1000) points, compare how each loss norm ranks the top-k
configurations and whether ranking changes meaningfully. Recommended task types:
write-library, comparative-analysis.

</details>

<details>
<summary>📊 <strong>Benchmark NetPyNE harness overhead vs raw NEURON across problem
sizes</strong> (S-0007-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0007-03` |
| **Kind** | evaluation |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0007_install_neuron_netpyne`](../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

At the single-compartment size, NetPyNE's setup is ~6× slower than raw NEURON (38.7 ms vs 6.7
ms) but runtime is indistinguishable. Scan both harnesses across realistic retinal network
sizes (1, 10, 100, 1000 cells; dense and sparse connectivity) to quantify where NetPyNE's cost
becomes significant for downstream t0008 / t0010 / t0011 runs, and decide whether any hot-loop
experiments should stay in raw NEURON.

</details>

<details>
<summary>🧪 <strong>Benchmark NEURON vs Arbor on the project's actual DSGC
morphology</strong> (S-0003-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0003-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0003_simulator_library_survey`](../../overview/tasks/task_pages/t0003_simulator_library_survey.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

Once a DSGC model runs in NEURON (via S-0003-02), port the same morphology and channel set to
Arbor 0.12.0 and measure single-cell simulation wall-clock on the project's workstation.
Third-party benchmarks claim Arbor is 7-12x faster; this task validates that claim on our
actual use case and records the real cost of the NMODL `modcc` translation that t0003 flagged
as the main Arbor adoption risk.

</details>

<details>
<summary>📚 <strong>Build a reusable SWC -> NEURON/NetPyNE/Arbor section-translator
library for dsgc-baseline-morphology</strong> (S-0005-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-04` |
| **Kind** | library |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0005_download_dsgc_morphology`](../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

Every downstream compartmental-modelling task in this project will need to load the
dsgc-baseline-morphology SWC into a simulator and produce a section/segment graph indexed by
SWC compartment id, soma reference, and per-section parent links. NEURON's built-in Import3d
handling of CNG SWCs is fragile (soma-3point convention, branch-point splitting, axon stubs)
and other simulators have their own quirks (NetPyNE's netParams.cellParams, Arbor's morphology
builder). Write a small library asset that exposes a pure-function
load_dsgc_morphology(simulator: str) -> SimulatorMorphology API with verified-equivalent
loaders for NEURON, NetPyNE, and Arbor, plus a smoke test that compares total path length and
compartment count across loaders against validate_swc.py. This eliminates per-task SWC-loading
bugs and keeps morphology choice swappable when S-0005-03 lands. Recommended task types:
write-library.

</details>

<details>
<summary>🧪 <strong>Cross-testbed DSI comparison: t0022 at 4 nS GABA vs t0024 AR(2)
noise</strong> (S-0037-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0037-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0037_null_gaba_reduction_ladder_t0022`](../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../meta/categories/dendritic-computation/) |

t0034/t0035 already produce measurable primary DSI on t0024 via AR(2) stochastic release
(rho=0.6). t0037 now shows that t0022 at 4 nS GABA is a second valid substrate. A dedicated
comparison task should run matched 7-diameter and 5-length sweeps on both substrates with
identical stimulus schedules and report whether the two discriminators agree on
Schachter2010-vs-passive identification. If they disagree, that itself is a finding worth
investigating.

</details>

<details>
<summary>🧪 <strong>Dense distal-length sweep at {1.0, 1.05, 1.10, 1.15, 1.20, 1.25,
1.30} to localize the peak-Hz cliff</strong> (S-0029-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0029-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0029_distal_dendrite_length_sweep_dsgc`](../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md) |
| **Source paper** | [`10.1038_nn.3565`](../../tasks/t0029_distal_dendrite_length_sweep_dsgc/assets/paper/10.1038_nn.3565/) |
| **Categories** | [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

Peak somatic firing rate in t0029 steps from 15 Hz at multipliers <= 1.0x to 14 Hz at
multipliers >= 1.25x with no intermediate value, and mean peak membrane voltage drifts
linearly from -4.81 mV (1.0x) to -5.23 mV (2.0x) - a 0.42 mV loss scaling linearly with length
rather than as exp(-L/lambda). A linear drop is inconsistent with passive cable attenuation
but consistent with distal synapses sitting beyond an active boosting region whose gain
depends on spatial proximity (Poleg-Polsky2016 distal Nav/Cav contribution). Add a dense
7-point sweep at {1.00, 1.05, 1.10, 1.15, 1.20, 1.25, 1.30} to resolve whether the 15->14 Hz
step is smooth (passive) or sharp (local threshold crossing, i.e. Sivyer-like signature).
Record both peak Hz and mean peak somatic voltage at each point. Recommended task types:
experiment-run.

</details>

<details>
<summary>🔧 <strong>Deprioritise distal-diameter parameters in the t0033 DSI
optimiser search space</strong> (S-0035-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0035-06` |
| **Kind** | technique |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0035_distal_dendrite_diameter_sweep_t0024`](../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../meta/categories/dendritic-computation/) |

The t0033 DSGC optimisation plan treats distal length and distal diameter as co-equal
morphology parameters. t0034 (p=0.038 on length) and t0035 (p=0.88 on diameter) together show
that distal diameter has DSI leverage below the noise floor on the t0024 substrate, while
length is a strong discriminator. Concrete action: reduce distal-diameter weight in the
optimiser search space (smaller range, coarser grid, or drop it entirely) so the GPU budget
concentrates on axes that actually move DSI. Distinct from S-0034-07 which focuses on the
primary-vs-vector-sum objective; this one concerns the parameter search space itself.
Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary>🧪 <strong>Diagnose and fix t0022's 15 Hz peak-firing cap (inherited
AMPA-only drive issue)</strong> (S-0039-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0039-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

Peak firing at the preferred direction is 15 Hz across the diameter sweep, well below
Schachter2010's 40-80 Hz baseline. The same 15 Hz ceiling appeared in t0030 at 12 nS GABA, so
it is a pre-existing t0022 drive issue, not a diameter or GABA artefact. Duplicate of
S-0037-04 but now blocking quantitative literature comparisons for the discriminator task too.
Likely fix: add NMDA back into the E-I schedule, or boost AMPA conductance, or both. Run a
diagnostic trace of soma voltage at preferred direction and compare to Schachter2010's
published traces.

</details>

<details>
<summary>🧪 <strong>Diagnose and fix the low peak firing rate in t0022 (15 Hz vs
40-80 Hz Schachter2010)</strong> (S-0037-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0037-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0037_null_gaba_reduction_ladder_t0022`](../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

At the 4 nS sweet spot the preferred-direction peak firing is 15 Hz, an order of magnitude
below Schachter2010's 40-80 Hz baseline. The same low rate was observed in t0030 at 12 nS
GABA, so this is a pre-existing t0022 drive issue (likely the AMPA-only schedule lacking NMDA
or compensatory excitation), not a GABA ladder artefact. A task should add NMDA back into the
t0022 E-I schedule (or increase AMPA gain) and verify peak firing reaches 40+ Hz without
re-pinning DSI. Until this is fixed, any cross-testbed peak-rate comparison is invalid.

</details>

<details>
<summary>🧪 <strong>Distal Nav ablation crossed with distal-dendrite length sweep
on t0022</strong> (S-0029-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0029-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0029_distal_dendrite_length_sweep_dsgc`](../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md) |
| **Source paper** | [`10.1038_nn.3565`](../../tasks/t0029_distal_dendrite_length_sweep_dsgc/assets/paper/10.1038_nn.3565/) |
| **Categories** | [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

HWHM in t0029 oscillates non-monotonically across length multipliers (71.7 deg at 1.5x vs
115.8 deg at 1.75-2.0x), inconsistent with any passive cable theory and consistent with distal
Nav channels crossing or failing to cross dendritic-spike threshold at a critical length.
Rerun the 7-point length sweep with distal Nav channels ablated (`forsec DEND_CHANNELS {
gnabar_HHst = 0 }`) while keeping somatic and AIS Nav intact. If HWHM becomes monotonic with
length, the non-monotonicity is a Sivyer2013 dendritic-spike signature and active boosting is
the dominant mechanism. If HWHM still oscillates, the non-monotonicity is passive cable
resonance and Sivyer2013 can be provisionally rejected on this morphology. Pairs naturally
with S-0029-01 to form a 2x2 design (Nav ablation x Poisson noise). One-line HOC overlay. ~45
min CPU. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Distal voltage-trace capture at null direction on t0022 to
confirm sub-threshold-clamp hypothesis</strong> (S-0036-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0036-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0036_rerun_t0030_halved_null_gaba`](../../overview/tasks/task_pages/t0036_rerun_t0030_halved_null_gaba.md) |
| **Source paper** | — |
| **Categories** | [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

t0036 recorded per-trial scalar distal peak_mv only (~-55 mV at null direction) but did not
export the full distal membrane time course. Creative_thinking hypothesis 4 (distal Nav
channels sub-threshold at null regardless of diameter amplification) and limitation bullet 5
both flag missing voltage traces as blocking direct mechanistic confirmation. Extend the t0022
trial driver to save a 200-sample time-course of the most-distal compartment voltage (one
trial per direction at diameter 1.0x, GABA_NULL = 6 nS and 12 nS, 24 traces total, ~5 min
CPU). Plot v_distal(t) across directions and annotate Nav activation threshold (~-55 mV) and
AMPA/GABA event onsets. Expected: at null the distal membrane never crosses Nav threshold for
the whole AMPA window on either 6 nS or 12 nS; at preferred it crosses and fires. Closes
creative_thinking hypothesis 4 and confirms the sub-threshold-clamp failure mode. Recommended
task types: experiment-run, data-analysis.

</details>

<details>
<summary>📂 <strong>Download additional Feller-archive DSGC reconstructions to enable
cross-cell variability sensitivity analysis</strong> (S-0005-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-03` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0005_download_dsgc_morphology`](../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Source paper** | — |
| **Categories** | [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

The current dsgc-baseline-morphology commits the project to a single reconstructed cell
(141009_Pair1DSGC). Cell-to-cell variability in branching pattern, total path length, and
arbor extent is a known source of variance in DSGC tuning curves (RQ2), and the Feller archive
on NeuroMorpho hosts several sibling ON-OFF DSGC reconstructions from the same lab (e.g.,
141009_Pair2DSGC and other 2014 Pair* records). Download 3-5 additional Feller-archive ON-OFF
DSGC SWCs as separate dataset assets (each with its own NeuroMorpho neuron_id and provenance),
validate each with the existing validate_swc.py parser, and tabulate per-cell compartment
count, branch points, and total dendritic path length so a downstream morphology-sweep task
can quantify cross-cell variability without committing a priori to a specific morphology.
Recommended task types: download-dataset.

</details>

<details>
<summary>📂 <strong>Download the four discovered papers not included in the 20-paper
budget (Sivyer2017, Euler2002, Enciso2010, Webvision)</strong> (S-0002-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-07` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../meta/categories/dendritic-computation/) |

research_internet.md catalogues 22 peer-reviewed candidates but only 20 became paper assets.
The held-back items are Sivyer2017 (dendro-dendritic cholinergic control of dendritic spike
initiation, Nat Commun), Euler2002 (SAC dendritic Ca signals are themselves directional,
Nature), Enciso2010 (SAC-network compartmental model, J Comp Neurosci), and the Webvision-DSGC
review. Sivyer2017 and Euler2002 directly constrain RQ4 and the presynaptic drive for RQ3, and
Enciso2010 provides a compartmental SAC-network model that could seed the presynaptic GABA
input for the DSGC model. Download them via /add-paper in a dedicated task and extend the
corpus to 24 papers. Recommended task types: download-paper, literature-survey.

</details>

<details>
<summary>📂 <strong>Download the Morrie & Feller 2018 SAC reconstructions from
NeuroMorpho and build a paired SAC+DSGC morphology asset</strong>
(S-0013-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0013-03` |
| **Kind** | dataset |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0013_resolve_morphology_provenance`](../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md) |
| **Source paper** | [`10.1016_j.cub.2018.03.001`](../../tasks/t0013_resolve_morphology_provenance/assets/paper/10.1016_j.cub.2018.03.001/) |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

This task attributed the dsgc-baseline-morphology reconstruction (NeuroMorpho neuron 102976,
141009_Pair1DSGC) to Morrie & Feller 2018 Current Biology (PMID 29606419). That paper's
Methods describe paired SAC-DSGC patch recordings with 2-photon stacks of both cells
post-recording, and the SAC partner of the 141009_Pair1 recording is likely deposited in
NeuroMorpho alongside the DSGC. Search NeuroMorpho by reference_pmid=29606419 to list all
reconstructions linked to the paper, download the 141009_Pair1SAC companion SWC (and any
neighbouring Pair2/Pair3 SAC+DSGC pairs), validate with validate_swc.py, and register them as
dataset assets so downstream modelling tasks can drive dsgc-baseline-morphology with
anatomically paired SAC presynaptic input. Strengthens the SAC presynaptic drive asset of
S-0002-08. Recommended task types: download-dataset.

</details>

<details>
<summary>🧪 <strong>Extend cable-theory survey to frequency-domain and thin-dendrite
transmission</strong> (S-0015-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0015-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0015_literature_survey_cable_theory`](../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md) |
| **Source paper** | — |
| **Categories** | [`cable-theory`](../../meta/categories/cable-theory/), [`dendritic-computation`](../../meta/categories/dendritic-computation/) |

The scoped-down 5-paper survey covers 3 of the 5 originally-planned themes in depth (Rall
foundations, on-the-path shunting DS, morphology-driven firing) and references the other two
(frequency-domain cable analysis, thin-dendrite transmission) only indirectly. A follow-up
survey task should add ~5 papers on frequency-domain cable theory (Koch 1984, Segev & Rall
1988) and thin-dendrite active transmission (Stuart & Sakmann 1994, London & Hausser 2005
review, Stuart & Spruston 2015 review) to close the gap.

</details>

<details>
<summary>🧪 <strong>Extend dendritic-computation survey to cerebellar Purkinje and
STDP papers</strong> (S-0016-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0016-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0016_literature_survey_dendritic_computation`](../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md) |
| **Source paper** | — |
| **Categories** | [`dendritic-computation`](../../meta/categories/dendritic-computation/) |

The scoped-down 5-paper survey covers cortical and hippocampal dendritic-computation motifs
(NMDA spike, BAC firing, BTSP, branch-level integration, canonical review) but does not cover
cerebellar Purkinje-cell branch-specific computation or cortical / hippocampal
spike-timing-dependent plasticity. A follow-up survey task should add approximately 5 papers
on cerebellar Purkinje branch-strength (Llinas & Sugimori 1980, Rancz & Hausser 2006, Brunel
2016) and cortical / hippocampal STDP (Bi & Poo 1998, Markram 1997, Sjostrom 2008 review) to
close the gap.

</details>

<details>
<summary>🧪 <strong>Extend DSGC model corpus to Arbor and NetPyNE
reimplementations</strong> (S-0010-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0010-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0010_hunt_missed_dsgc_models`](../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

All three candidates hunted in t0010 use NEURON; t0010's DROP list includes Schachter2010
(NeuronC). A follow-up survey task should hunt for Arbor-based and NetPyNE-based DSGC
compartmental models specifically, since those simulators are becoming standard for
large-scale retinal circuit work. Extends REQ-1 of t0010 to a second simulator axis.

</details>

<details>
<summary>🧪 <strong>Extend patch-clamp survey to DSGC-specific dynamic-clamp, Ih/HCN
biophysics, and AIS measurements</strong> (S-0017-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0017-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0017_literature_survey_patch_clamp`](../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md) |
| **Source paper** | — |
| **Categories** | [`patch-clamp`](../../meta/categories/patch-clamp/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

The scaled-down 5-paper survey covers the four DSGC-modelling sub-areas identified in the plan
(space-clamp, AIS, NMDARs, maintained activity) but leaves several high-priority follow-on
topics uncovered: (a) DSGC-specific dynamic-clamp studies that use injected conductance
waveforms to test direction selectivity mechanisms, (b) DSGC Ih/HCN biophysics and resonance
properties, (c) DSGC-specific AIS measurements (the Werginz2020 paper is on OFF-alpha T cells,
not on ON-OFF DSGCs directly), and (d) large-scale compartmental-model fitting pipelines for
RGCs. A follow-up survey task should add ~5 papers across these four sub-areas to close the
gap.

</details>

<details>
<summary>🧪 <strong>Extend synaptic-integration survey with DSGC-specific
receptor-kinetic, dynamic-clamp, and connectomic SAC-DSGC papers</strong>
(S-0018-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0018-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0018_literature_survey_synaptic_integration`](../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

The scaled-down 5-paper survey covers the five canonical themes (AMPA/NMDA/GABA kinetics,
shunting inhibition, E-I balance, dendritic-location integration, SAC-to-DSGC asymmetry) but
with one paper per theme, selected from the most-cited classical literature. A follow-up
survey task should add ~5 DSGC-targeted papers across: (a) modern DSGC-specific AMPA and NMDA
kinetic measurements at near-physiological temperature, (b) DSGC dynamic-clamp studies that
inject measured conductance waveforms, (c) connectomic reconstructions of SAC-to-DSGC wiring
(Briggman et al. 2011, Kim et al. 2014), (d) recent E-I temporal co-tuning studies in retina
(rather than auditory cortex), and (e) DSGC dendritic computation (Oesch, Euler, Taylor,
Sivyer). This closes the gap between canonical theory and DSGC-specific parameters.

</details>

<details>
<summary>📚 <strong>Extend tuning_curve_loss with a two-point (PD/ND) scoring API to
make t0012 usable under the native protocol</strong> (S-0020-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-04` |
| **Kind** | library |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0020_port_modeldb_189347_gabamod`](../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

research_code.md records that t0012's high-level score() entry point rejects the two-condition
CSV because its loader's _validate_angle_grid requires exactly 12 angles on a 30-degree
spacing. t0020 worked around this by re-implementing the DSI formula inline in
score_envelope.py. Every future gabaMOD-swap task (including S-0020-01 and S-0020-03 above)
will hit the same wall. Add a score_two_point(pd_rates: np.ndarray, nd_rates: np.ndarray, *,
dsi_envelope, peak_envelope) -> TwoPointScore API to tuning_curve_loss that returns DSI, mean
PD, mean ND, per-condition stderr, gate.passed, plus optional per-trial CIs via bootstrap.
Keep the 12-angle score() untouched; the new API is an additional entry point. Register it in
the tuning_curve_loss library details.json entry_points. Recommended task types:
write-library.

</details>

<details>
<summary>🧪 <strong>Extend voltage-gated-channel survey with recent DSGC-specific
Nav/Kv patch-clamp and super-resolution AIS microdomain papers</strong>
(S-0019-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0019-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0019_literature_survey_voltage_gated_channels`](../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

The scaled-down 5-paper survey covers the five canonical themes (Nav subunit localisation at
AIS, Kv1 subunit expression at AIS, RGC HH-family kinetic rate functions, Nav1.6 vs Nav1.2
co-expression kinetics, AIS Nav conductance density) but with one classical paper per theme. A
follow-up survey task should add ~5 DSGC-targeted papers across: (a) DSGC-specific Nav/Kv
patch-clamp measurements at near-physiological temperature, (b) super-resolution microscopy of
AIS microdomains (panNav vs subtype-specific antibodies, STED/STORM), (c) developmental Nav/Kv
channel trajectory studies in RGC AIS, (d) M-current/Kv7/KCNQ channels at RGC AIS, (e) Kv3
fast-delayed-rectifier measurements in RGC. This closes the gap between canonical
voltage-gated-channel theory and DSGC-specific parameters.

</details>

<details>
<summary>🧪 <strong>Extended distal-dendrite length sweep (1.0x to 4.0x, 8.0x) to
reach Dan2018's critical regime</strong> (S-0029-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0029-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0029_distal_dendrite_length_sweep_dsgc`](../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md) |
| **Source paper** | [`10.1038_s41598-018-23998-9`](../../tasks/t0029_distal_dendrite_length_sweep_dsgc/assets/paper/10.1038_s41598-018-23998-9/) |
| **Categories** | [`cable-theory`](../../meta/categories/cable-theory/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

Dan2018 reports monotonic DSI-vs-length over 50-400 um distal branches; Sivyer2013's critical
length sits at ~150 um. The t0022 distal-leaf baseline is on the order of tens of um, so the
0.5-2.0x sweep likely spans only ~15-160 um, overlapping only the tail of Sivyer2013's range
and sitting entirely below Dan2018's critical length. Add three extreme sweep points at 3.0x,
5.0x, and 8.0x while keeping the rest of the t0022 testbed fixed. Watch for `d_lambda`
violations at extreme lengths (fallback: adaptive `nseg` at each point). Possible outcomes:
(a) DSI stays at 1.000 and peak Hz continues linear decline - testbed is cable-dominated at
the soma and no resolution is possible; (b) DSI drops at a specific high multiplier with
monotonic HWHM broadening - Dan2018 passive-TR regime emerges; (c) DSI drops with HWHM
narrowing at a specific multiplier - Sivyer2013 dendritic-spike-failure regime emerges. ~45
min CPU. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Extended distal-diameter sweep on t0024 (0.25x to 4.0x, 9 points)
to probe non-linear extremes</strong> (S-0035-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0035-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0035_distal_dendrite_diameter_sweep_t0024`](../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`cable-theory`](../../meta/categories/cable-theory/) |

Push the diameter multiplier beyond t0035's narrow 0.5x-2.0x range into a wider 0.25x-4.0x
sweep (nine multipliers) on the t0024 DSGC substrate to look for non-linear DSI effects that
the 4x range missed. Specifically targets two possibilities: (a) input-impedance saturation at
baseline may break at extreme thinning/thickening and (b) the cable-theory 1/sqrt(d)
prediction implies a detectable DSI shift over a 16x diameter range even if a 4x range is
inside the noise floor. Distinct from S-0030-03 which targets t0022. Recommended task types:
experiment-run.

</details>

<details>
<summary>🧪 <strong>Extended distal-length sweep on t0024 (0.25x to 4.0x, 9 points)
to characterise the electrotonic-length optimum</strong> (S-0034-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0034-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0034_distal_dendrite_length_sweep_t0024`](../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md) |
| **Source paper** | — |
| **Categories** | [`cable-theory`](../../meta/categories/cable-theory/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../meta/categories/dendritic-computation/) |

t0034 covered 0.5x-2.0x (7 points) and found the primary-DSI peak at 0.75x (0.774) with a
non-monotonic decline beyond. To fit Tukker2004's intermediate-electrotonic-length optimum
quantitatively and to test whether the curve continues falling or saturates beyond 2.0x,
extend the sweep to 0.25x, 0.375x, 0.5x, 0.75x, 1.0x, 1.5x, 2.0x, 3.0x, 4.0x (9 points). Keep
the standard 12-direction x 10-trial protocol and AR(2) rho=0.6. Expected outcomes: (a) a
clear DSI peak at intermediate length with symmetric falloff on both sides (supports
Tukker2004 optimum); (b) preferred-angle instability across 3.0x-4.0x (supports Schachter2010
local-spike-failure); (c) d_lambda violations at extreme lengths (engineering concern - apply
adaptive nseg at each point). Distinct from S-0029-03 (same approach on t0022 testbed which
was pinned at DSI=1.000). Recommended task types: experiment-run.

</details>

<details>
<summary>📚 <strong>Extract the t0022 GABA-override monkey-patch into a reusable
library asset for downstream tasks</strong> (S-0036-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0036-04` |
| **Kind** | library |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0036_rerun_t0030_halved_null_gaba`](../../overview/tasks/task_pages/t0036_rerun_t0030_halved_null_gaba.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

t0036 introduced code/gaba_override.py which monkey-patches
_t0022_constants.GABA_CONDUCTANCE_NULL_NS at import time and re-binds the local name inside
trial_runner_diameter.py so the schedule_ei_onsets ratio is computed against the overridden
value. This pattern is immediately needed for S-0036-01 (further null-GABA reductions) and
S-0036-02 (GABA-AMPA timing offset). Rather than each task reimplementing the monkey-patch,
lift it into a library asset (working name: dsgc_t0022_schedule_overrides) exposing a typed
context-manager or setup function accepting gaba_null_ns, gaba_preferred_ns,
gaba_to_ampa_lead_ms, returning a provenance dict logged at task start. Ships a smoke test
asserting the override survived a fresh import and that the null/preferred ratio matches the
requested value. Distinct from S-0033-06 (DSI objective evaluator) which wraps the scoring
side - this wraps the schedule-parameter side. Recommended task types: write-library.

</details>

<details>
<summary>🧪 <strong>Fine-grained thin-end diameter sweep D in {0.3, 0.4, 0.5, 0.6,
0.7} at GABA=4 nS on t0022</strong> (S-0039-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0039-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`cable-theory`](../../meta/categories/cable-theory/) |

t0039 found DSI saturates at 0.429 for D in {0.5, 0.75, 1.0}, matching the t0037 4 nS ceiling.
This is the discriminator's upper bound at this GABA level. A finer sweep thinner than 0.5x
would locate the saturation edge and bound the headroom available to any morphology optimiser
on t0022. 5 diameters x 12 angles x 10 trials = 600 trials, ~25 min local CPU, $0.00.

</details>

<details>
<summary>🧪 <strong>GABA-to-AMPA timing offset sweep on t0022 diameter testbed to
test timing-dominates-conductance hypothesis</strong> (S-0036-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0036-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0036_rerun_t0030_halved_null_gaba`](../../overview/tasks/task_pages/t0036_rerun_t0030_halved_null_gaba.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

t0036's creative_thinking cited 'timing dominates conductance' as the second-leading
explanation for why halving null-GABA from 12 nS to 6 nS did not unpin null firing: the t0022
schedule delivers GABA 10 ms BEFORE AMPA on null trials, and the integrated kinetic profile
(not the peak) may clamp the distal membrane below Nav threshold for the whole AMPA window.
Sweep the GABA-leads-AMPA offset across {10 ms (default), 5 ms, 0 ms, -5 ms (AMPA leads GABA)}
at two fixed GABA conductances (12 nS baseline and 6 nS) at diameter 1.0x only (12 angles x 10
trials x 4 offsets x 2 GABA = 960 trials, ~35 min CPU). Primary outcome: find the offset at
which null firing first exceeds 0.1 Hz, isolating timing as an independent rescue axis
orthogonal to S-0036-01's conductance axis. Distinct from S-0030-02 (Poisson) and S-0036-01
(conductance) - this targets the GABA-AMPA offset specifically. Recommended task types:
experiment-run.

</details>

<details>
<summary>🧪 <strong>GABA/AMPA density ratio scan at fixed 3-5x null/preferred IPSC
asymmetry</strong> (S-0002-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

PolegPolsky2016 sets GABA/AMPA at 1:1 (177/177), while Park2014 and Taylor2002 constrain the
null/preferred IPSC ratio to 3-5x but not the total GABA density. Scan the GABA/AMPA density
ratio from 0.5 to 4.0 (keeping the 3-5x null asymmetry fixed, the 40-80 Hz preferred peak
fixed by the Na/K ridge, and the morphology and dendritic conductances fixed) and report how
tuning-curve HWHM and preferred peak rate co-vary. The expected pattern (sharper tuning at the
cost of lower peak rate) is stated in research_internet.md as hypothesis H4 but is not yet
tested in the literature. This directly refines the RQ3 answer. Recommended task types:
experiment-run.

</details>

<details>
<summary>📂 <strong>Generate weaker-DSI variant target tuning curves</strong>
(S-0004-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0004-01` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0004_generate_target_tuning_curve`](../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

Create sibling dataset assets (e.g., target-tuning-curve-weak-dsi,
target-tuning-curve-mid-dsi) with the same generator but r_peak values chosen so DSI lands at
~0.65 and ~0.75. Lets downstream fitting tasks test whether the optimisation pipeline is
robust across the 0.6-0.9 band instead of only the upper end.

</details>

<details>
<summary>🧪 <strong>Hand-port Hanson2019 Spatial-Offset-DSGC model to headless
12-angle sweep</strong> (S-0010-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0010-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0010_hunt_missed_dsgc_models`](../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md) |
| **Source paper** | [`10.1038_s41467-019-09147-4`](../../tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-019-09147-4/) |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

Rewrite the upstream run.py driver from geoffder/Spatial-Offset-DSGC-NEURON-Model to remove
the headful 'from neuron import h, gui' import and the hardcoded C:\Users\geoff\NEURONoutput
path, then adapt it to the canonical 12-angle x 20-trial sweep scored against the t0012
tuning-curve API. t0010 exited at P2 within the 90-min per-candidate cap; a dedicated port
task can budget 3-4 hours and reach P3.

</details>

<details>
<summary>📊 <strong>Harmonised cross-comparison of the three ModelDB 189347 sibling
ports (t0008, t0020, t0022)</strong> (S-0022-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0022-07` |
| **Kind** | evaluation |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0022_modify_dsgc_channel_testbed`](../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

The project now has three independent implementations of DS on the same Poleg-Polsky & Diamond
2016 skeleton: t0008 (per-angle BIP rotation, DSI 0.316), t0020 (global gabaMOD scalar swap,
DSI 0.7838), and t0022 (per-dendrite E-I scheduling, DSI 1.0). Each used slightly different
scoring paths, trial counts, and metric key sets. Produce a shared analysis module that loads
each port's tuning_curves.csv, recomputes DSI / peak / null / HWHM / reliability under one
harmonised scorer (t0012 score() where applicable plus S-0020-04's score_two_point for t0020),
and produces one side-by-side comparison chart (polar plot overlay plus bar chart of headline
metrics). Outputs a consolidated comparison_report.md plus an overview/llm-context/ snapshot.
Dependencies: t0008, t0020, t0022 library assets, t0012 scorer. Effort ~12 hours. Recommended
task type: data-analysis, write-library.

</details>

<details>
<summary>🧪 <strong>Higher-statistics re-run of t0034 at 1.5x and 2.0x (30+ trials
per angle) to confirm the preferred-angle jumps</strong> (S-0034-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0034-06` |
| **Kind** | experiment |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0034_distal_dendrite_length_sweep_t0024`](../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

t0034's non-monotonicity hinges on two preferred-angle jumps: 0 deg -> 330 deg at 1.5x (DSI
dip to 0.623) and 0 deg -> 30 deg at 2.0x (DSI collapse to 0.545). These are based on only 10
trials per angle, and the compare-literature analysis notes the 95% CI on a 10-trial DSI is
~+/-0.1 - comparable to the 0.23 observed DSI spread. Re-run the protocol at 1.5x and 2.0x
with 30-50 trials per angle (3-5x the baseline count) and recompute bootstrap CIs on DSI and
preferred-angle estimates at each point. If the jumps persist, Schachter2010
local-spike-failure is strengthened; if they collapse to a single preferred direction, they
were small-N artefacts and the cable-filtering story becomes more parsimonious. Listed in
compare-literature.md as a concrete limitation. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Ih (HCN) conductance ablation sweep on t0024 distal dendrites to
test h-current role in distal cable behaviour</strong> (S-0035-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0035-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0035_distal_dendrite_diameter_sweep_t0024`](../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`cable-theory`](../../meta/categories/cable-theory/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

Sweep distal Ih (HCN) gbar from 0 to 2x baseline (five points) on the t0024 DSGC while holding
all other parameters fixed, and measure primary DSI, HWHM, and distal-compartment voltage. Ih
is a known resonance and input-impedance shaper that could partly explain why distal diameter
reads flat on both t0022 and t0024 (t0030 and t0035 both null). If ablation of Ih causes the
diameter sweep to become non-flat, h-current is masking the mechanism. Distinct from S-0009-03
which targeted Ih calibration, not ablation. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Inject Poisson background rate on the t0022 driver to moderate
DSI from 1.0 toward the 0.5-0.8 published band</strong> (S-0022-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0022-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0022_modify_dsgc_channel_testbed`](../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Source paper** | [`10.1016_j.neuron.2005.06.036`](../../tasks/t0022_modify_dsgc_channel_testbed/assets/paper/10.1016_j.neuron.2005.06.036/) |
| **Categories** | [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

The t0022 NetStim burst driver uses noise = 0 and baseline synapses are silenced, so DSI
saturates at 1.0 across all 60 null-direction trials. Park2014, Oesch2005, and Poleg-Polsky &
Diamond 2016 all report DSI in the 0.5-0.8 range because real DSGCs have 2-5 Hz per-trial
spike jitter from stochastic bipolar release. Extend the driver with a configurable background
Poisson process (1, 2, 3, 5 Hz baseline rate on all synapses) and rerun the 12-angle x
10-trial sweep at each noise level. Expected outcome: DSI curve drops from 1.0 to ~0.8 at 2 Hz
bg to ~0.6 at 5 Hz bg, bracketing the literature envelope, with per-angle std rising from 0 Hz
to ~2-4 Hz matching Schachter2010 trial-to-trial variability. Dependencies: t0022 library
asset. Effort ~8 hours. Recommended task type: experiment-run.

</details>

<details>
<summary>🧪 <strong>Intermediate-gabaMOD sensitivity sweep to map the PD-ND
transition curve</strong> (S-0020-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0020_port_modeldb_189347_gabamod`](../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../tasks/t0020_port_modeldb_189347_gabamod/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

The canonical protocol uses only the two endpoints gabaMOD = 0.33 (PD) and 0.99 (ND).
Task_description Scope explicitly deferred intermediate values as follow-up work. Run 20
trials per condition at gabaMOD in {0.20, 0.33, 0.50, 0.66, 0.83, 0.99} and plot firing rate
vs gabaMOD plus DSI computed as (rate_at_0.33 - rate_at_X)/(rate_at_0.33 + rate_at_X).
Outputs: (1) a firing-rate-vs-gabaMOD curve that shows whether the 0.33 -> 0.99 transition is
sigmoidal, threshold-like, or linear; (2) the critical gabaMOD value at which DSI crosses 0.5
(useful for later calibration); (3) a CSV with schema (gabamod, trial_seed, firing_rate_hz).
Probes whether the paper's two-point choice lies on a plateau or a steep-response region of
the inhibition axis, directly informing the inhibition-strength free parameter for later
optimisation. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Joint (GABA, diameter) sweep to separate passive filtering from
GABA-suppressed active amplification</strong> (S-0039-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0039-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

t0022 shows passive_filtering at 4 nS. Two explanations: (a) t0022 lacks active machinery, or
(b) 4 nS GABA shunts regenerative events that would otherwise produce Schachter2010
concave-down. A joint sweep GABA in {5, 4, 3, 2} x D in {0.5, 1.0, 2.0} = 12 conditions x 12
angles x 10 trials = 1440 trials (~60 min) would distinguish: if lower-GABA runs produce
concave-down curves, mechanism (b) is right; if all GABA levels show passive signatures,
mechanism (a) is right.

</details>

<details>
<summary>🧪 <strong>Joint distal length x diameter 2-D sweep on t0022 to catch
interactions the marginal sweeps miss</strong> (S-0030-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0030-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`cable-theory`](../../meta/categories/cable-theory/) |

t0029 (distal-length sweep) and t0030 (distal-diameter sweep) both produced flat vector-sum
DSI curves when run in isolation on the t0022 E-I schedule. Marginal sweeps cannot reveal
interactions: Schachter2010's active amplification depends on length (number of Nav-bearing
segments) AND diameter (Nav substrate per unit length) jointly, and the cable space constant
lambda = sqrt(d * Rm / (4 * Ra)) couples them nonlinearly. Run a focused 2-D grid (e.g., 5
length x 5 diameter = 25 configurations x 12 angles x 10 trials = 3000 trials) on the
schedule-fixed testbed (S-0030-01 prerequisite). Distinct from S-0002-04 (broad factorial
including branch orders at fixed synapse count) because it is 2-D, focused, and scheduled
after the desaturation fix. Expected local CPU wall time ~7 h. Recommended task types:
experiment-run.

</details>

<details>
<summary>🧪 <strong>Kv3 vs Kv1 AIS placement swap to test the Kole-Letzkus 2007
repolarisation prior</strong> (S-0022-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0022-06` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0022_modify_dsgc_channel_testbed`](../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Source paper** | [`10.1523_jneurosci.0130-07.2007`](../../tasks/t0022_modify_dsgc_channel_testbed/assets/paper/10.1523_jneurosci.0130-07.2007/) |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`patch-clamp`](../../meta/categories/patch-clamp/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

Kole & Letzkus 2007 report that Kv1 in the proximal AIS sets spike threshold while Kv3 in the
distal AIS sets repolarisation speed and thus maximum sustained firing rate. Use the t0022
AIS_PROXIMAL and AIS_DISTAL forsec blocks to implement four conditions: (a) Kv1 proximal + Kv3
distal (canonical), (b) Kv1 distal + Kv3 proximal (swap), (c) Kv1 both (no Kv3), (d) Kv3 both
(no Kv1), each with Nav1.6 held at 8 S/cm^2 in the distal AIS. Rerun the 12-angle x 10-trial
sweep for each condition. Expected outcome: condition (a) peaks near 30-40 Hz; condition (b)
drops peak because distal Kv1 fails to fast-repolarise; conditions (c) and (d) test whether
either K-channel alone suffices. Dependencies: t0022 library asset. Effort ~16 hours.
Recommended task type: experiment-run, comparative-analysis.

</details>

<details>
<summary>🧪 <strong>Localise the GABA unpinning threshold with a fine sweep (5.0,
4.5, 4.0, 3.5, 3.0 nS)</strong> (S-0037-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0037-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0037_null_gaba_reduction_ladder_t0022`](../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |

The current sweep places the unpinning threshold between 6 nS (t0036 pinned) and 4 nS (t0037
unpinned). A 0.5 nS-spaced sweep over {5.0, 4.5, 4.0, 3.5, 3.0} nS at baseline diameter on
t0022 (5 levels x 12 angles x 10 trials = 600 trials, ~20 min local CPU) would localise the
threshold to within 0.5 nS and reveal whether the DSI vs GABA curve is sharp or gradual.
Important for characterising how fragile the operational window really is.

</details>

<details>
<summary>🧪 <strong>NMDA multiplicative-gain ablation to isolate its contribution
to DSI</strong> (S-0002-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-06` |
| **Kind** | experiment |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

PolegPolsky2016 reports that NMDA receptors multiplicatively scale excitatory drive by ~2x and
sharpen directional discrimination, but the survey did not find a published ablation that
isolates the NMDA contribution independently of the AMPA+GABA core. Run three configurations
on the reproduced DSGC baseline (AMPA+GABA only, AMPA+GABA+NMDA with PolegPolsky2016 NMDA
parameters, AMPA+GABA+NMDA with NMDA_gain swept 1-4x) and report the DSI, peak rate, and HWHM
trajectories. This answers a specific open RQ3/RQ4-adjacent question that the literature
states but does not isolate experimentally. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Non-uniform proximal-to-distal diameter taper sweep on t0022 to
match Schachter2010 impedance gradient</strong> (S-0030-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0030-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`cable-theory`](../../meta/categories/cable-theory/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

t0030 applied a single multiplier uniformly to every distal leaf, producing a 4x range that
Schachter2010's 150-200 MOhm proximal -> >1 GOhm distal (5-7x) impedance gradient indicates is
too narrow and the wrong shape. Real DSGC dendrites taper from thick primary branches to thin
terminal tips; the uniform multiplier scales all terminals together without recreating that
gradient. Implement a taper parameter k such that a segment's diameter scales by (1 + k *
path_distance / L_max), sweep k in {-0.5, -0.25, 0, 0.25, 0.5, 0.75} to produce flattened,
nominal, and exaggerated tapers, and run the standard 12-direction x 10-trial protocol at each
k (after the S-0030-01 schedule fix). Expected outcome: the exaggerated-taper cell (high k,
very thin distal) maximises distal input impedance and should exhibit the Schachter2010
amplification signature if the mechanism is active on this morphology. Recommended task types:
experiment-run, feature-engineering.

</details>

<details>
<summary>🧪 <strong>Null-GABA conductance sweep (3, 6, 9, 12 nS) to release the
deterministic ceiling on t0022</strong> (S-0029-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0029-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0029_distal_dendrite_length_sweep_dsgc`](../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md) |
| **Source paper** | [`10.1371_journal.pcbi.1000899`](../../tasks/t0029_distal_dendrite_length_sweep_dsgc/assets/paper/10.1371_journal.pcbi.1000899/) |
| **Categories** | [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

The t0022 scheduler uses GABA_CONDUCTANCE_NULL_NS = 12 nS applied 10 ms before AMPA on
null-direction trials - about 4x the preferred value (3 nS) and 2x Schachter2010's measured
compound null inhibition (~6 nS). This oversized early shunt forces null-direction firing to
exactly 0 Hz, pinning the pref/null DSI denominator and the ratio at 1.000 before cable
mechanics have any effect. Sweep GABA_CONDUCTANCE_NULL_NS across {3, 6, 9, 12} nS at a fixed
length multiplier of 1.0x and locate the conductance at which null-direction firing first
exceeds 1 Hz. That value is the testbed's sensitivity edge. Prerequisite for S-0029-01 and
S-0029-02: rerunning the length sweep at 6 nS instead of 12 nS gives the
mechanism-discrimination experiment a fighting chance without needing to inject noise. ~30 min
CPU. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Overlay a Van Wart + Werginz AIS on the deRosenroll morphology
to test peak-rate recovery</strong> (S-0024-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0024-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0024_port_de_rosenroll_2026_dsgc`](../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/) |

Research-internet gap 2 showed that the upstream repository has no explicit AIS section, but
research-papers (Werginz 2020, Van Wart 2007) pins the AIS-to-soma Na ratio at ~7x and names
AIS length as the dominant predictor of maximum sustained firing rate. Fork t0024 into a new
library asset, add a two-subsegment AIS (proximal Nav1.2/Nav1.1, distal Nav1.6 + Kv1.2) with
Na ratio 7x and AIS length 25-50 um, rerun the 8-direction correlated/uncorrelated protocol,
and compare peak firing rate and HWHM to the t0024 baseline. Does not require rebuilding the
SAC network.

</details>

<details>
<summary>📚 <strong>Parallelise the t0024 sweep across CPU cores to cut wall time
from 3.21 h to under 1 h</strong> (S-0026-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0026-04` |
| **Kind** | library |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0026_vrest_sweep_tuning_curves_dsgc`](../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

The t0024 sweep took 11,562 s (3.21 h) because NEURON ran single-threaded on one CPU. Each
(V_rest, direction, trial) combination is embarrassingly parallel. Build a ProcessPoolExecutor
wrapper that farms out trials across cores; with 8 workers we expect wall time to drop below 1
h. This will make V_rest x rho and V_rest x velocity sweeps practical.

</details>

<details>
<summary>🧪 <strong>Parameter-sweep calibration of bundled 189347 toward the envelope
targets</strong> (S-0008-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0008-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0008_port_modeldb_189347`](../../overview/tasks/task_pages/t0008_port_modeldb_189347.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

Systematically vary the main free parameters of the 189347 HOC (bipolar-to-RGC synaptic
weight, SAC inhibition gain, NMDA/AMPA ratio, HHst gbar_ scaling) to find a parameter point
where the rotation-based protocol hits the envelope (DSI 0.7-0.85, peak 40-80 Hz, null <10 Hz,
HWHM 60-90 deg). Would produce a calibration_results.json and a mapping between
envelope-passing parameters and the paper's default values. Recommended task types:
code-reproduction.

</details>

<details>
<summary>📚 <strong>Parameterize t0011/t0012 tuning-curve plotter and scorer to
support N_ANGLES != 12</strong> (S-0024-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0024-04` |
| **Kind** | library |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0024_port_de_rosenroll_2026_dsgc`](../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

The t0011 tuning_curve_viz library and the t0012 tuning_curve_loss scorer both hardcode
N_ANGLES=12, which blocks native 8-direction visualisation and scoring for the deRosenroll
port (and any future paper that uses 4/6/8/16/24 directions). Refactor both libraries to
accept an N_ANGLES argument (default 12 for backward compatibility) and rerun the t0024
8-direction conditions through the plotter to produce polar/Cartesian PNGs for
results_detailed.md. Small infrastructure change with broad reuse benefit across the DSGC
lineage.

</details>

<details>
<summary>🔧 <strong>Parametric curve fitting (von Mises / wrapped Gaussian) for
sub-degree HWHM estimates on sparse 12-angle grids</strong> (S-0012-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0012-02` |
| **Kind** | technique |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0012_tuning_curve_scoring_loss_library`](../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

The current compute_hwhm_deg interpolates linearly between the two 30 deg samples bracketing
the half-maximum on each flank, limiting HWHM resolution to about 1 deg and producing a 5.5
deg deficit versus the closed-form 65.5 deg (measured 60.0 deg on the t0004 target). Add a
fit_parametric_tuning_curve helper to tuning_curve_loss.metrics that fits a von Mises or
wrapped Gaussian to the 12 angles via scipy.optimize.curve_fit, derives an analytic HWHM from
the fitted kappa or sigma, and exposes hwhm_deg_parametric and parametric_fit_residual_rms on
ScoreReport. Compare parametric HWHM against interpolated HWHM on t0004, t0008 (ModelDB
189347), and S-0002-01 grid-search points; document when interpolation suffices and when the
parametric fit is required. Recommended task types: write-library, experiment-run.

</details>

<details>
<summary>🧪 <strong>Per-compartment distal-spike detector on t0024 length sweep to
verify Schachter2010 local-spike-failure at 1.5x and 2.0x</strong>
(S-0034-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0034-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0034_distal_dendrite_length_sweep_t0024`](../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md) |
| **Source paper** | [`10.1371_journal.pcbi.1000899`](../../tasks/t0034_distal_dendrite_length_sweep_t0024/assets/paper/10.1371_journal.pcbi.1000899/) |
| **Categories** | [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

t0034 attributed the primary-DSI non-monotonicity and preferred-angle jumps (to 330 deg at
1.5x, to 30 deg at 2.0x) to Schachter2010 local-spike-failure in distal compartments, based
only on the somatic readout and the angular-instability fingerprint. This interpretation is
currently suggestive but not confirmed. Re-run the t0034 sweep with per-compartment V
recording at every distal terminal (177 sections) and compute the distal-to-soma spike-count
ratio per trial per angle. Under Schachter2010 local-spike-failure, the ratio should be >1 at
baseline (reliable distal spikes) and drop below 1 at 1.5x and 2.0x where cable length
decouples distal tips. If the ratio stays constant, the angle jumps are not a
local-spike-failure signature and another mechanism (NMDA recruitment, Kv3 rectification)
should be explored. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Poisson-noise desaturation rerun of the distal-dendrite diameter
sweep on t0022</strong> (S-0030-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0030-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |

Sibling of S-0029-01 (Poisson + length sweep) targeting the diameter axis. The t0030
deterministic testbed yields reliability = 1.000 and null firing 0 Hz at every diameter, which
collapses the rate-code noise floor that Schachter2010's dendritic-spike-threshold mechanism
and Dan2018's passive-TR derivation both assume. Add an independent 5 Hz background Poisson
NetStim per distal dendrite (independent seed, no direction bias) to the t0022 scheduler and
rerun the full 7-point diameter sweep (0.5x-2.0x, 12 angles x 10 trials = 840 trials).
Expected: DSI drops from 1.000 into the 0.6-0.8 Park2014 envelope, reliability drops below
1.0, and diameter regains discrimination power between Schachter2010 active amplification
(+slope) and passive filtering (-slope). Distinct from S-0022-05 (Poisson at a single
length/diameter) and S-0029-01 (length axis). Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Poisson-noise desaturation rerun of the distal-dendrite length
sweep on t0022</strong> (S-0029-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0029-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0029_distal_dendrite_length_sweep_dsgc`](../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md) |
| **Source paper** | [`10.1371_journal.pcbi.1000899`](../../tasks/t0029_distal_dendrite_length_sweep_dsgc/assets/paper/10.1371_journal.pcbi.1000899/) |
| **Categories** | [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

The t0029 sweep failed as a mechanism discriminator because pref/null DSI is pinned at 1.000
at every multiplier from 0.5x to 2.0x (null firing = 0 Hz on every trial, reliability =
1.000). Dan2018's passive-TR derivation and Schachter2010's compartmental DSGC both assume
stochastic Poisson drive with a rate-code noise floor; removing noise collapses the
mechanism-distinguishing regime. Add an independent 5 Hz background Poisson NetStim per distal
dendrite (independent seed, no direction bias) to the t0022 scheduler and rerun the full
7-point length sweep (12 angles x 10 trials x 7 lengths = 840 trials). Expected: DSI drops
from 1.000 to the 0.6-0.8 Park2014 envelope, reliability drops below 1.0, and length regains
discrimination power between Dan2018's monotonic-decrease and Sivyer2013's saturation
predictions. Distinct from S-0022-05 which runs at a single length only. Recommended task
types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Port additional DSGC models from t0010 hunt and exercise
plot_multi_model_overlay with >2 models</strong> (S-0011-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0011-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0011_response_visualization_library`](../../overview/tasks/task_pages/t0011_response_visualization_library.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

plot_multi_model_overlay caps at 6 models and was smoke-tested with only two (t0004 target +
t0008 ModelDB 189347). The t0010 hunt identified Hanson 2019 Spatial-Offset-DSGC, deRosenroll
2026 ds-circuit-ei, and other DSGC compartmental models but none have been ported to runnable
headless form yet. Run the headless-port scaffold proposed in S-0010-05 to produce
tuning-curve CSVs for 3-5 additional DSGC models, then regenerate the multi-model overlay
smoke test. This will surface any layout bugs (legend clipping, colour collisions,
preferred-direction arrow overlap) that single- or double-model overlays never exercise and
will give the project a real cross-model comparison figure. Recommended task types:
code-reproduction, write-library.

</details>

<details>
<summary>🧪 <strong>Port Hanson2019 DSGC model and repeat V_rest sweep to test
starburst-independent DS hypothesis</strong> (S-0026-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0026-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0026_vrest_sweep_tuning_curves_dsgc`](../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md) |
| **Source paper** | [`10.7554_eLife.42392`](../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/assets/paper/10.7554_eLife.42392/) |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

Hanson2019 reports DSI 0.33 in the absence of asymmetric starburst amacrine cell responses,
suggesting an alternative mechanism. If the Hanson model is ported and swept over the same
eight V_rest values, we can compare its V_rest sensitivity against our t0022 (strongly
V_rest-dependent) and t0024 (U-shaped) results. Would clarify whether V_rest-dependence of DSI
is a universal signature or specific to starburst-driven models.

</details>

<details>
<summary>📚 <strong>Port the TREES-toolbox Rall 3/2 quaddiameter rule to a
pure-Python calibrator and compare against the Strahler bins</strong>
(S-0009-08)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-08` |
| **Kind** | library |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0009_calibrate_dendritic_diameters`](../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Source paper** | — |
| **Categories** | [`cable-theory`](../../meta/categories/cable-theory/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

Rall's 3/2 power rule (r_parent^(3/2) = sum r_child^(3/2)) is the only biophysically
principled way to match impedance across a binary tree; our max-child Strahler bins have no
such guarantee. Implement TREES-toolbox's quaddiameter algorithm as ~80 lines of pure Python,
solve the system bottom-up from the 131 terminals with the Poleg-Polsky terminal mean fixed,
and produce a sibling asset dsgc-baseline-morphology-rall. Compare against the
Strahler-calibrated asset by per-branch axial resistance, total surface area, and
per-compartment radius deltas. Expected primary-radius shift ~15% (3.69 to ~3.1 um) at the
measured 2-way branching ratio. Creative_thinking.md section A2. Recommended task types:
write-library, comparative-analysis.

</details>

<details>
<summary>📊 <strong>Quantitative cable-theory fit of t0034 DSI-vs-length curve
against Rall 1/d^(3/2) and Tukker2004 predictions</strong> (S-0034-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0034-05` |
| **Kind** | evaluation |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0034_distal_dendrite_length_sweep_t0024`](../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md) |
| **Source paper** | — |
| **Categories** | [`cable-theory`](../../meta/categories/cable-theory/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

t0034's classify_shape.py assigns a categorical label (monotonic/saturating/non-monotonic) but
does not fit a parametric cable-theory model to the observed DSI vs length curve. Vector-sum
DSI declines monotonically from 0.507 (0.5x) to 0.357 (2.0x) with R^2=0.91, and peak firing
declines 40% across the sweep - both quantitative cable-filtering signatures. Write a
dedicated analysis task that fits (a) the Rall 1/d^(3/2) impedance-matching rule to the
peak-Hz decline, (b) Tukker2004's lambda-optimum function to the DSI vs length curve (extract
the fitted lambda at peak DSI), and (c) Hausselt2007's cable-length-to-DSI scaling. Output a
fitted parameter set with 95% CIs and a residual plot. This converts t0034's categorical
'cable-filtering best fit' into a falsifiable quantitative claim and enables direct
cross-paper comparison. Recommended task types: data-analysis.

</details>

<details>
<summary>🧪 <strong>Random terminal-branch ablation (25%) on t0022 to test branch
independence</strong> (S-0027-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0027-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0027_literature_survey_morphology_ds_modeling`](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

Ablate 25% of randomly-chosen terminal dendritic branches on t0022 (10 random seeds) and
measure global DSI. Prediction (creative_thinking.md #4): if [Sivyer2013, 10.1038_nn.3565]
dendritic-spike branch independence holds, global DSI drops by <15%; if global
transfer-resistance summation dominates, DSI drops by >40%. Also yields the first
DSI-vs-stochastic-pruning curve in the corpus, which would speak to in vivo robustness under
aging or disease perturbations and complement the broader factorial morphology sweep already
proposed in S-0002-04.

</details>

<details>
<summary>📊 <strong>Re-audit all existing dataset and library assets' source_paper_id
fields against resolved DOI metadata</strong> (S-0013-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0013-04` |
| **Kind** | evaluation |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0013_resolve_morphology_provenance`](../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md) |
| **Source paper** | — |
| **Categories** | — |

The t0005 nomination error that this task corrected was not caught by any automated check; it
was caught only because a follow-up task specifically downloaded both candidate papers and
inspected their Methods. Other already-registered dataset and library assets across the
project (e.g., under t0004, t0008, t0009, t0011, t0012) may carry similarly silent
source_paper_id errors that no downstream task has yet tripped over. Run a one-off audit task
that iterates over every registered dataset and library asset with a non-null source_paper_id,
resolves the referenced paper asset's DOI via arf.scripts.utils.resolve_doi (S-0013-01), and
flags any asset where the source_paper_id slug does not match what the asset's description.md
or originating plan claims as the source (wrong author, wrong year, wrong venue). File one
correction per disagreement following the corrections_specification.md pattern used by this
task. Recommended task types: data-analysis, correction.

</details>

<details>
<summary>🔧 <strong>Re-calibrate using a Poleg-Polsky xyz-registered 1:1 per-section
diameter lookup to drop Strahler binning entirely</strong> (S-0009-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-04` |
| **Kind** | technique |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0009_calibrate_dendritic_diameters`](../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../tasks/t0009_calibrate_dendritic_diameters/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

Our three-bin heuristic collapses 170 Poleg-Polsky mid-role sections into one 1.653 um radius
(section F1 of creative_thinking.md). A lossless alternative is to Procrustes-align the CNG
xyz points with the Poleg-Polsky RGCmodel.hoc pt3dadd points, then for each CNG compartment
copy the diameter of the nearest registered source section. Preserves all 350 source diameters
and eliminates both the tie-break-induced primary bin boundary (section F3) and the
bin-collapse interior variability. Deliverable: a sibling dataset asset
dsgc-baseline-morphology-registered with a registration-quality report (residual xyz distance
per compartment). Emit corrections if registration succeeds with sub-micron residuals.
Recommended task types: feature-engineering, data-analysis.

</details>

<details>
<summary>🧪 <strong>Re-enable NMDA (b2gnmda nonzero) crossed with distal-dendrite
length sweep on t0022</strong> (S-0029-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0029-06` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0029_distal_dendrite_length_sweep_dsgc`](../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

The t0022 `_silence_baseline_hoc_synapses` sets b2gnmda = 0 and installs single-component
AMPA-only E-I pairs, removing the Espinosa2010 AMPA/NMDA kinetic-tiling mechanism from the
testable space entirely. Espinosa2010 proposes that DSGC DS arises from different activation
time courses of AMPA and NMDA interacting with cable propagation delay - predicting
non-monotonic DSI-vs-length because NMDA's 50-150 ms time constant resonates with propagation
delay at specific lengths. Modify `_silence_baseline_hoc_synapses` to restore b2gnmda at 30%
of the 189347 baseline and rerun the 7-point length sweep. If DSI drops below 1.000 with
non-monotonic length dependence, kinetic tiling is a real third mechanism and the current null
result was partially a function of NMDA silencing. Requires a sibling library asset (clone of
t0022 with NMDA enabled) to preserve t0022's immutability. ~1 hour CPU plus ~1 hour coding.
Recommended task types: build-model, experiment-run.

</details>

<details>
<summary>📂 <strong>Re-type SWC by section role (soma / primary / mid / terminal)
as a sibling dataset asset</strong> (S-0009-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-06` |
| **Kind** | dataset |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0009_calibrate_dendritic_diameters`](../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

The calibrated SWC uses only SWC type codes 1 (soma) and 3 (dendrite); downstream NEURON tasks
that set section-specific conductance densities (e.g., Na 150/150/30 mS/cm^2, K 70/70/35) must
re-derive Strahler order every time. Produce a sibling dataset asset
dsgc-baseline-morphology-calibrated-typed that re-types each row to 1 (soma), 5 (primary), 3
(mid), or 6 (terminal) using the calibration's bin labels. Topology, xyz, and parent_id are
preserved; only type_code changes. Add a conversion script and a smoke test that confirms
NEURON's Import3d loader accepts the extended type codes. Cuts duplicated Strahler
recomputation from every downstream channel-placement task. Creative_thinking.md section A3.
Recommended task types: feature-engineering.

</details>

<details>
<summary>🧪 <strong>Rebuild ModelDB 189347 port on the calibrated Horton-Strahler
SWC from t0009</strong> (S-0008-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0008-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0008_port_modeldb_189347`](../../overview/tasks/task_pages/t0008_port_modeldb_189347.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

Replace the bundled 1-soma + 350-dend topology in RGCmodel.hoc with the calibrated SWC from
t0009 (6,736 compartments) and rewrite placeBIP()'s section-ordering-dependent synapse
placement. This was deferred in t0008 because the bundled HOC hardcodes 3D-point placement and
section indices. Outcome is a third variant of the port asset running on a morphology that
actually matches the measured dendritic diameter profile. Recommended task types:
code-reproduction.

</details>

<details>
<summary>🔧 <strong>Register dsi_at_vrest and peak_hz_at_vrest metric keys in
meta/metrics/</strong> (S-0026-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0026-01` |
| **Kind** | technique |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0026_vrest_sweep_tuning_curves_dsgc`](../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

This task produced direction_selectivity_index and peak firing rate per V_rest but the keys
dsi_at_vrest_<value> and peak_hz_at_vrest_<value> are not registered under meta/metrics/. Add
metric definitions so future V_rest sweeps can report through the registered key registry and
appear in aggregate_metric_results output. Also reshape t0026 metrics.json variants from the
current map form to the array form required by task_results_specification.md multi-variant
format.

</details>

<details>
<summary>📊 <strong>Register retinal-ganglion-cells and compartmental-modelling
categories</strong> (S-0015-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0015-03` |
| **Kind** | evaluation |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0015_literature_survey_cable_theory`](../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md) |
| **Source paper** | — |
| **Categories** | — |

The answer asset verificator emits AA-W001 warnings because categories
'retinal-ganglion-cells' and 'compartmental-modelling' are not registered in meta/categories/.
These categories are used by all five literature-survey tasks (t0015-t0019) and should be
formally registered to silence the warnings and enable category-based aggregation across those
tasks.

</details>

<details>
<summary>📚 <strong>Register SAC presynaptic drive model as an asset for downstream
DSGC input construction</strong> (S-0002-08)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-08` |
| **Kind** | library |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1038_nature09818`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nature09818/) |
| **Categories** | [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

Briggman2011 (SBEM wiring) and Ding2016 (cross-species comparison) supply the structural E/I
bias; Park2014 and Taylor2002 supply the 3-5x null/preferred IPSC amplitudes;
Sethuramanujam2016 adds ACh/GABA co-release; Hanson2019 challenges the pure SAC-asymmetry
model. Consolidate these findings into a pre-built SAC presynaptic drive asset (a reusable
library or dataset: angle-dependent GABA conductance time courses, AMPA time courses, and
their spatial distributions on a DSGC) so downstream DSGC simulation tasks do not each
re-implement the presynaptic waveform construction. The asset should expose a pure-function
API that takes (stimulus angle, velocity, asymmetry parameter) and returns per-synapse
conductance time courses. Recommended task types: write-library, feature-engineering.

</details>

<details>
<summary>📊 <strong>Render and QA-check 2D/3D visualisations of
dsgc-baseline-morphology for documentation and synapse placement</strong>
(S-0005-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-05` |
| **Kind** | evaluation |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0005_download_dsgc_morphology`](../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Source paper** | — |
| **Categories** | [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../meta/categories/dendritic-computation/) |

The dsgc-baseline-morphology asset is currently described only by tabulated statistics (6,736
compartments, 129 branch points, 1,536.25 um path length). Downstream tasks that place
AMPA/GABA synapses by spatial rule (e.g., Park2014 3-5x null/preferred IPSC asymmetry,
S-0002-05 GABA/AMPA density scan) need a visual reference for the dendritic arbor,
branch-order map, and soma orientation; reviewers also need a figure for any project paper.
Render three QA visualisations (2D top-down dendrogram coloured by Strahler order, 2D xy
projection coloured by path distance from soma, 3D rotating xyz scatter) using neurom +
matplotlib (or NEURON's PlotShape) and register the figures plus the rendering script as an
answer asset describing what was checked. Flag any visible reconstruction artefacts (dangling
branches, axon stubs, soma asymmetry) for downstream tasks. Recommended task types:
data-analysis, answer-question.

</details>

<details>
<summary>📂 <strong>Reproduce the Park2014 mouse ON-OFF DSGC tuning-curve dataset
as a validation benchmark</strong> (S-0002-10)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-10` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1523_JNEUROSCI.5017-13.2014`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_JNEUROSCI.5017-13.2014/) |
| **Categories** | [`patch-clamp`](../../meta/categories/patch-clamp/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

Park2014 (paper 10.1523_JNEUROSCI.5017-13.2014) and Chen2009 (paper
10.1113_jphysiol.2008.161240) are the two papers that set the mouse ON-OFF DSGC RQ5 targets
(DSI 0.6-0.9, peak 40-80 Hz, HWHM 60-90 deg). Park2014 is available open-access. Digitise the
published tuning-curve figure(s) into a reusable dataset asset (angle in degrees, spike rate
in Hz, error bars, cell counts) so the model can be scored against measured data rather than
only against the analytic target in t0004. This gives the project a literature-grounded
validation benchmark distinct from the canonical analytic target. Recommended task types:
download-dataset, data-analysis.

</details>

<details>
<summary>📊 <strong>Revisit envelope widening (DSI upper 0.85 to 0.9, peak lower 40
to 30 Hz) once real simulation results are in</strong> (S-0012-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0012-05` |
| **Kind** | evaluation |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0012_tuning_curve_scoring_loss_library`](../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

REQ-7 was satisfied by widening two envelope bounds away from the t0002 literature values: DSI
upper raised from 0.85 to 0.9 to admit t0004's DSI 0.8824, and peak lower lowered from 40 Hz
to 30 Hz to admit t0004's 32 Hz peak. This is explicit but anchored to the t0004 generator,
not to measured DSGC variability. After t0008 (ModelDB 189347) and the Na/K grid search
(S-0002-01) produce real simulated curves, re-evaluate: (a) re-parameterise t0004 so its curve
lands inside the literature envelope (reducing DSI_MAX from 0.9 to 0.83 would drop DSI to 0.8
and peak to about 37 Hz), or (b) formally widen the envelope with a citation justifying the
wider bounds. Deliverable: an answer asset recommending a resolution, with corresponding
corrections file. Recommended task types: answer-question, correction.

</details>

<details>
<summary>📚 <strong>Scaffold a NetPyNE `Batch` sweep harness for DSGC parameter
studies</strong> (S-0003-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0003-04` |
| **Kind** | library |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0003_simulator_library_survey`](../../overview/tasks/task_pages/t0003_simulator_library_survey.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

Build a small library that wraps NetPyNE's `Batch` class with the project's preferred sweep
axes (morphology scale, channel densities, synaptic weights) and an Optuna backend. Output: an
`assets/library/` entry plus a one-page usage example. This unblocks every downstream
tuning-curve experiment that needs to run more than one parameter combination.

</details>

<details>
<summary>📚 <strong>Script the full NEURON + NetPyNE install for clean-machine
reproduction</strong> (S-0007-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0007-02` |
| **Kind** | library |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0007_install_neuron_netpyne`](../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

The NSIS installer's /S flag ignored the /D= prefix, forcing an interactive GUI step. Ship a
PowerShell / bash installer script that (a) downloads nrn-8.2.7-setup.exe to a known path, (b)
drives the install with the correct prefix (either by default-install-then-move or by a
chocolatey recipe), (c) writes the .pth file into the uv venv, and (d) runs nrnivmodl + both
sanity sims end-to-end. This unblocks automated reproduction on a fresh Windows machine and
Linux / macOS CI runners.

</details>

<details>
<summary>📊 <strong>Sensitivity analysis: re-run DSGC simulations under alternative
Strahler tie-break rules and bin boundaries</strong> (S-0009-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-05` |
| **Kind** | evaluation |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0009_calibrate_dendritic_diameters`](../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`cable-theory`](../../meta/categories/cable-theory/) |

The primary bin (33 compartments) is set by max_strahler_order = 5 under a max-child
tie-break; a min-child or NeuroM section-based convention can push max_order to 6 and
reclassify the current 33 primary compartments as mid, jumping proximal Rin by ~15%
(creative_thinking.md section F3, E1). Produce 3-4 sibling calibrated SWCs under alternative
tie-break rules (max-child, min-child, NeuroM section_strahler_orders, two-bin collapse) and
run the downstream DSGC passive simulation from S-0009-01 on each. Report DSI, preferred peak,
HWHM, and proximal/distal Rin per variant; quantify the sensitivity of downstream metrics to
the heuristic choice. This makes the tie-break choice reviewable rather than arbitrary.
Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary>🧪 <strong>Single-compartment collapse of t0024 to test whether T4-style
geometry-nullity extends to DSGCs</strong> (S-0027-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0027-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0027_literature_survey_morphology_ds_modeling`](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

Collapse t0024 (de Rosenroll 2026 port) to a single isopotential compartment that retains full
synaptic input drive and biophysics, and re-run the DSI-vs-speed protocol. Prediction
(creative_thinking.md #5): if T4-style geometry-nullity [Gruntman2018] extends to mammalian
DSGCs, the collapsed model reproduces full-model DSI-vs-speed; if the de Rosenroll local-DSI
mechanism is load-bearing, it fails. Cheapest of the five testbed experiments and a strong
null-hypothesis test for the necessity of dendritic geometry.

</details>

<details>
<summary>🧪 <strong>Sweep bar velocity x V_rest on both DSGC ports to test
velocity-V_rest interaction</strong> (S-0026-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0026-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0026_vrest_sweep_tuning_curves_dsgc`](../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md) |
| **Source paper** | [`10.1113_jphysiol.2010.192716`](../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/assets/paper/10.1113_jphysiol.2010.192716/) |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

Sivyer2010 reports DSI varies with velocity (0.45-0.57) at natural V_rest. Our current sweep
fixed velocity at the t0022/t0024 defaults. Repeat the 8-value V_rest sweep at 3-5 bar
velocities to check whether V_rest modulates the velocity-tuning curve or only the
direction-tuning curve. Expected runtime: ~4x current (t0022) and ~4x current (t0024) if 4
velocities are tested.

</details>

<details>
<summary>🧪 <strong>Sweep paper-text biophysics (Ra 200, eleak -65, Na 200/70/35) to
test peak firing-rate shortfall</strong> (S-0024-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0024-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0024_port_de_rosenroll_2026_dsgc`](../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md) |
| **Source paper** | [`10.1016_j.celrep.2025.116833`](../../tasks/t0024_port_de_rosenroll_2026_dsgc/assets/paper/10.1016_j.celrep.2025.116833/) |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/) |

Peak firing rate is 5.15 Hz in t0024 versus the paper's qualitative ~30-40 Hz and the t0004
envelope of 40-80 Hz. The paper text and the companion repository disagree on Ra, eleak, and
Na/K densities; the repository values were used as authoritative. Run a 2x2x3 sensitivity
sweep varying Ra (100/200), eleak (-60/-65), and Na density regime (code/paper/intermediate)
with 10 trials per condition at PD/ND to isolate which single parameter change recovers peak
rate without destroying DS. Scorer: t0012 tuning_curve_loss against the t0004 envelope.

</details>

<details>
<summary>🧪 <strong>Test whether a Larkum-style Ca2+ plateau zone can be localised
in DSGC dendritic trees</strong> (S-0016-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0016-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0016_literature_survey_dendritic_computation`](../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md) |
| **Source paper** | [`10.1038_18686`](../../tasks/t0016_literature_survey_dendritic_computation/assets/paper/10.1038_18686/) |
| **Categories** | [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/) |

The answer asset identifies the cortical-style Ca2+-plateau initiation zone (Larkum 1999) as a
plausible but uncertain motif for DSGCs (caveat: DSGC dendritic trees lack the tuft / basal
two-compartment layout of cortical pyramidals). Build a compartmental DSGC model with
spatially-varying L-type / T-type Ca2+-channel densities to identify candidate initiation-zone
compartments, then test whether asymmetric inhibition at principal-branch bifurcations can
selectively enable Ca2+ plateaus during preferred-direction motion and suppress them during
null-direction motion. Report preferred-direction burst firing rate versus null-direction
burst rate and compare with published DSGC spiking statistics.

</details>

<details>
<summary>🔧 <strong>Transfer-learning surrogate warm-start from t0022 and t0024
V_rest-sweep evaluations</strong> (S-0033-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0033-04` |
| **Kind** | technique |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0033_plan_dsgc_morphology_channel_optimisation`](../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

Creative-thinking alternative #3 in t0033 noted that t0022, t0024 and the t0026 V_rest sweep
already produced thousands of (gbar-subset, DSI) evaluations on the 16-parameter HHst
topology. If half of the 5,000-sample surrogate training burn is replaced by these as
warm-start, the $41.56 training cost plausibly drops to ~$20, pulling the recommended cell to
~$30. Build a task that (a) reads t0026 V_rest-sweep and t0022 baseline outputs, (b) encodes
them as (parameter-vector, DSI) tuples in the 25-dim joint space by imputing the 9 unvaried
dimensions at Poleg-Polsky defaults with tagged uncertainty, (c) pre-trains the surrogate NN
on this warm-start set before the 2,500-sample cold-start burn, and (d) measures whether the
half-dataset warm-start matches the 5,000-sample cold-start surrogate. Recommended task types:
experiment-run, feature-engineering.

</details>

<details>
<summary>📊 <strong>Trial-count power analysis for the PD/ND DSI estimator (bootstrap
CI vs N_trials)</strong> (S-0020-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-06` |
| **Kind** | evaluation |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0020_port_modeldb_189347_gabamod`](../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

t0020 reports DSI 0.7838 from 20 trials per condition but quotes no confidence interval.
Before launching sensitivity sweeps (S-0020-01, S-0020-03), future tasks need to know how many
trials per condition are needed to resolve, say, a 0.05-DSI difference at 95% CI. Compute
bootstrap 95% CIs on DSI for N_trials per condition in {5, 10, 20, 40, 80} by resampling with
replacement (10,000 resamples) from a single long run (80 trials per condition, reusing
run_gabamod_sweep.py with --n-trials 80). Output: (1) a CSV
trial_count,dsi_mean,dsi_ci_low,dsi_ci_high,peak_mean,peak_ci_low,peak_ci_high; (2) a plot of
DSI CI width vs trial count; (3) a recommended N_trials for each sensitivity-analysis budget
tier. Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary>🧪 <strong>Unblock t0023 Hanson 2019 port so REQ-6 cross-comparison can
include 5/5 DSGC models instead of 4/5</strong> (S-0024-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0024-06` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0024_port_de_rosenroll_2026_dsgc`](../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md) |
| **Source paper** | [`10.7554_eLife.42392`](../../tasks/t0024_port_de_rosenroll_2026_dsgc/assets/paper/10.7554_eLife.42392/) |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

t0024 step 12 records t0023_port_hanson_2019_dsgc as intervention_blocked
(intervention/deferred_pending_t0022.md). The t0022 task has since completed (DSI 1.000, HWHM
116.25, RMSE 10.48) so the original blocking dependency is resolved. Triage t0023's
intervention file, resume the port, and then retrofit a Hanson 2019 row into the cross-model
comparison table in results_detailed.md of both t0024 and any subsequent DSGC port. Closes the
REQ-6 partial-coverage caveat.

</details>

<details>
<summary>🔧 <strong>Update t0033 optimiser headroom estimate to reflect narrow (0.06
DSI) morphology dynamic range on t0022</strong> (S-0039-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0039-05` |
| **Kind** | technique |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/) |

t0039 shows the t0022 discriminator's total DSI spread across a 4x diameter range is only
0.061 (0.368 to 0.429). Any pure-morphology optimiser running at GABA=4 nS on t0022 has a
ceiling of 0.429 (the 4 nS saturation value). If t0033's planned optimiser is scoped to
maximise DSI via morphology alone, the maximum achievable lift from the baseline is ~0.06 -
the headroom is much smaller than originally planned. Consider adding a channel-density
dimension to the optimiser search space, since DSI has more potential room through Nav/Cav
density than through morphology alone.

</details>

<details>
<summary>🧪 <strong>Wider distal-diameter sweep (0.25x to 4.0x) after the schedule
fix to probe extreme impedance regimes</strong> (S-0030-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0030-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`cable-theory`](../../meta/categories/cable-theory/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

The t0030 sweep used multipliers 0.5x-2.0x (a 4x range) and found vector-sum DSI moved by only
0.030 absolute, with Wu2023 reporting distal-diameter DSI saturation above ~0.8 um on primate
SAC - our baseline distal seg.diam straddles that threshold so our sweep likely sat in the
saturated regime throughout. Once the S-0030-01/S-0030-02 schedule fix has removed the DSI
ceiling, rerun the diameter sweep over a wider range {0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0,
4.0}x at the same 12-direction x 10-trial protocol. Provides the impedance-gradient dynamic
range Schachter2010's 5-7x proximal-to-distal input-resistance measurement implies, and tests
whether Wu2023's saturation threshold applies to mouse ON-OFF DSGC. Recommended task types:
experiment-run.

</details>

<details>
<summary>🧪 <strong>Write forward-only driver for PolegPolsky2026 DS-mechanisms model
and pursue LICENSE</strong> (S-0010-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0010-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0010_hunt_missed_dsgc_models`](../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md) |
| **Source paper** | [`10.1038_s41467-026-70288-4`](../../tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/) |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

PolegPolskyLab/DS-mechanisms ships only a GA-training harness (numGen=300, popSize=50) and has
no LICENSE file, which blocks library-asset registration under this project's rules. A
follow-up task should (a) email the authors to request a LICENSE addition, and (b) extract a
single-parameter-set forward-only 'simulate at angle theta' driver from the GA inner loop so
the model can be scored against the canonical 12-angle sweep without running the full GA.

</details>

<details>
<summary>📊 <strong>Zero-cost meta-analysis of primary-DSI vs vector-sum-DSI
discrepancy across t0029, t0030, t0034, t0035</strong> (S-0035-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0035-05` |
| **Kind** | evaluation |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0035_distal_dendrite_diameter_sweep_t0024`](../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

Combine metrics.json outputs from all four completed morphology sweeps (t0029 length t0022,
t0030 diameter t0022, t0034 length t0024, t0035 diameter t0024) into a single cross-task table
correlating primary DSI against vector-sum DSI. Key questions: when primary DSI is flat or at
ceiling, does vector-sum DSI pick up signal? Does the rank-order of variants agree between the
two metrics? This supports the t0033 optimiser choice and a standing evaluation-methodology
recommendation (compare against S-0029-07, S-0030-06, S-0034-07). No simulations needed; pure
re-analysis of existing CSVs. Recommended task types: data-analysis.

</details>

## Low Priority

<details>
<summary>📂 <strong>Add a Poisson-noise variant of the target trials</strong>
(S-0004-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0004-02` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0004_generate_target_tuning_curve`](../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

Replace the current Gaussian-noise trial replicates with Poisson counts converted to rates
(Fano factor ~1) and register it as a separate dataset asset. This would give
tuning_curve_reliability a noise model closer to real spike statistics while keeping the
closed-form mean curve unchanged.

</details>

<details>
<summary>📚 <strong>Add a verify_library_asset.py verificator to close the
framework-wide gap flagged during t0024 step 9</strong> (S-0024-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0024-05` |
| **Kind** | library |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0024_port_de_rosenroll_2026_dsgc`](../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md) |
| **Source paper** | — |
| **Categories** | — |

During t0024 step 9 the library asset structure was validated manually against
meta/asset_types/library/specification.md because no automated verificator exists. The other
asset types (paper, dataset, answer) have dedicated verificators. Add verify_library_asset.py
to arf/scripts/verificators/ enforcing the mandatory fields in library/specification.md
(manifest, source files, citation metadata, entry points) and wire it into the
prestep/poststep cycle for any task that produces a library asset. Framework infrastructure
task, not task-folder work.

</details>

<details>
<summary>🔧 <strong>Add Elsevier-login fallback to the paper-download
workflow</strong> (S-0010-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0010-06` |
| **Kind** | technique |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0010_hunt_missed_dsgc_models`](../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md) |
| **Source paper** | [`10.1016_j.celrep.2025.116833`](../../tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1016_j.celrep.2025.116833/) |
| **Categories** | — |

t0010 failed to download the deRosenroll2026 PDF (Elsevier HTTP 403 on anonymous access) but
succeeded on other publishers. A follow-up infrastructure task should add a Sheffield
institutional-login-aware download path (or a manual-fetch checkpoint) to the /add-paper skill
so future Elsevier-hosted papers can be registered with download_status=success instead of
requiring a failure record.

</details>

<details>
<summary>🧪 <strong>Add Ih (HCN) channel to dendrites and measure its effect on E-I
integration window</strong> (S-0022-08)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0022-08` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0022_modify_dsgc_channel_testbed`](../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`cable-theory`](../../meta/categories/cable-theory/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

The t0022 testbed currently has no Ih (HCN) channels in DEND_CHANNELS. Literature prior from
t0019 (voltage-gated-channels survey) flags Ih as a common dendritic modulator: it lowers
input resistance and shortens the E-I temporal window over which coincidence matters. Add Ih
at a realistic dendritic density (e.g., 1e-5 S/cm^2 following hippocampal CA1 values as a
start) to the DEND_CHANNELS forsec block and rerun the canonical 12-angle x 10-trial sweep
plus an EI_OFFSET sweep in {5, 10, 15, 20, 30} ms. Expected outcome: the E-I integration
window narrows (only tight E-I offsets produce DSI, long offsets stop working), quantifying
the dendritic-integration timescale imposed by Ih. Dependencies: t0022 library asset,
S-0022-03 infrastructure for EI offset sweeps if already done. Effort ~10 hours. Recommended
task type: experiment-run.

</details>

<details>
<summary>📊 <strong>Add PNG regression testing for tuning_curve_viz via pixel-level
image diff in CI</strong> (S-0011-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0011-06` |
| **Kind** | evaluation |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0011_response_visualization_library`](../../overview/tasks/task_pages/t0011_response_visualization_library.md) |
| **Source paper** | — |
| **Categories** | — |

The seven smoke-test PNGs currently ship as committed fixtures under
assets/library/tuning_curve_viz/files/ but no test guards against silent regressions when
matplotlib versions, rcParams defaults, or the Okabe-Ito palette change. Add a pytest module
code/tuning_curve_viz/test_image_regression.py that regenerates each of the seven PNGs into a
tmp_path, loads both the fixture and the regenerated image with Pillow, and asserts that the
per-pixel RMS difference is below a tight tolerance (e.g., 2.0 on 0-255 greyscale, masking
anti-aliased text regions). Wire the test into the ARF CI hook so any unintended figure-style
change fails loudly. Recommended task types: write-library, infrastructure-setup.

</details>

<details>
<summary>🔧 <strong>Add preferred-direction GABA asymmetry to t0022 (cartwheel SAC
offset)</strong> (S-0037-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0037-06` |
| **Kind** | technique |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0037_null_gaba_reduction_ladder_t0022`](../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |

t0022 applies only null-direction GABA. Published DSGC models (Park2014, Schachter2010)
include a directionally-offset SAC inhibition where preferred-direction trials see much lower
GABA than null. Implement the cartwheel asymmetry as a new parameter
`GABA_CONDUCTANCE_PREF_NS` (probably 0-1 nS based on t0037's over-excitation regime below 2
nS), and measure whether primary DSI improves toward the 0.5-0.6 Park2014 centre. This moves
t0022 closer to the canonical DSGC E-I motif rather than relying on a single null-only scalar.

</details>

<details>
<summary>📊 <strong>Cross-validate compute_reliability against independent split-half
implementations (odd-even, bootstrap, Spearman-Brown)</strong> (S-0012-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0012-06` |
| **Kind** | evaluation |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0012_tuning_curve_scoring_loss_library`](../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

compute_reliability implements one split-half estimator: partition trials into even/odd
indices, per-angle means, Pearson r, clamped to [0, 1]. Canonical alternatives differ in
defensible ways: (a) random-draw split rather than parity, (b) Spearman-Brown prophecy
correction to project split-half r back to full-length reliability, (c) Spearman rank
correlation for ordinal robustness, (d) bootstrap resampling to produce a confidence interval.
Build compute_reliability_variants returning all four on the same TuningCurve, run it on
t0004's trials.csv and downstream simulated trials, and write an answer asset documenting
where the estimates agree or diverge. If a variant is systematically preferred for our
approximately 20 trials per angle, promote it to the default via a corrections-aware revision.
Recommended task types: comparative-analysis, answer-question.

</details>

<details>
<summary>📊 <strong>Email the Feller lab to map the 141009_Pair1DSGC session to a
specific pair in Morrie & Feller 2018 CB</strong> (S-0013-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0013-05` |
| **Kind** | evaluation |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0013_resolve_morphology_provenance`](../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md) |
| **Source paper** | [`10.1016_j.cub.2018.03.001`](../../tasks/t0013_resolve_morphology_provenance/assets/paper/10.1016_j.cub.2018.03.001/) |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

The provenance decision in this task (source_paper_id = 10.1016_j.cub.2018.03.001) is grounded
in methodological consistency plus the NeuroMorpho.org curated attribution, not in an
exact-quote match: Morrie & Feller 2018 CB does not literally print 141009, Pair1DSGC,
biocytin, or Neurolucida in its Methods, and the paper publishes only SAC (not DSGC)
reconstructions. A downstream task should email the Feller lab (Murphy-Baum at
murphy-baum@berkeley.edu or Morrie at rmorrie@berkeley.edu) asking which specific paired
recording in the paper's Figure 2 cohort (n = 12 Control + 9 Sema6A-/- null + 6 Sema6A-/-
preferred) produced the 141009_Pair1DSGC reconstruction, and whether the companion SAC
reconstruction is deposited at NeuroMorpho. A one-sentence email-reply quote converts the
current 'methodologically consistent' attribution into a citeable exact-quote provenance, and
directly informs S-0013-03. Recommended task types: answer-question.

</details>

<details>
<summary>📊 <strong>Evaluate NEURON 9.0.x C++ MOD-file migration readiness for
project adoption</strong> (S-0003-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0003-05` |
| **Kind** | evaluation |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0003_simulator_library_survey`](../../overview/tasks/task_pages/t0003_simulator_library_survey.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

NEURON 9.0.0 and 9.0.1 (Sep-Nov 2025) migrate MOD-file semantics to C++ and add Python 3.14
wheels. The t0003 survey picked 8.2.7 for conservatism. Create a task that (1) installs 9.0.1
into a sandbox venv, (2) rebuilds the Poleg-Polsky 189347 DSGC model from S-0003-02 under
9.0.x, (3) runs the existing DSGC simulations under both 8.2.7 and 9.0.1, and (4) records any
behavioural differences. This decides whether the project should upgrade before or after the
first round of tuning-curve experiments.

</details>

<details>
<summary>🧪 <strong>Extend sweep upward to V_rest in {-15, -10, -5} mV to capture the
post-collapse regime in t0024</strong> (S-0026-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0026-07` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0026_vrest_sweep_tuning_curves_dsgc`](../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/) |

Model t0022 peak firing collapses from 129 Hz at V=-30 to 26 Hz at V=-20 due to Na
inactivation, but t0024 still rises monotonically to 7.6 Hz at V=-20 with no collapse.
Extending the t0024 sweep to V_rest >= -20 mV would reveal whether t0024 also exhibits a
Na-inactivation collapse (suggesting shared mechanism at higher depolarisations) or remains
depolarisation-insensitive (suggesting NMDA-dominated signalling).

</details>

<details>
<summary>📚 <strong>Extend t0011 response-visualisation library with a
condition-based (PD/ND) raster+PSTH plot</strong> (S-0020-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-07` |
| **Kind** | library |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0020_port_modeldb_189347_gabamod`](../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

t0011's tuning_curve_viz library supports angle-based rasters (one column per angle) but the
two-condition CSV produced by t0020 has no angle axis; only the bar chart (plot_pd_vs_nd.py,
t0020 local code) currently visualises it. Extend t0011 with
plot_condition_raster_psth(spike_times_df, *, conditions=('PD','ND'), out_png) that draws a
two-column raster (one per condition) above a PSTH panel. Requires t0020 (or a follow-up) to
first record per-trial spike times (not just rates) from run_gabamod_sweep.py. Complements
S-0011-01 (angle-based raster on the rotation-proxy port); this is the condition-based
analogue for the native-protocol port. Once merged, back-apply to t0020's existing sweep to
produce a publication-quality raster. Recommended task types: write-library, experiment-run.

</details>

<details>
<summary>📊 <strong>Introduce per-trial spike-count distribution metric to
distinguish failures from timing shifts</strong> (S-0039-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0039-06` |
| **Kind** | evaluation |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

t0039's peak firing drops from 15 Hz at D=0.5x to 13 Hz at D=2.0x - a 2 Hz difference could be
2 fewer spikes per trial at the same timing, or a shift in the spike-count DISTRIBUTION (e.g.,
bimodal failures). Currently metrics_per_diameter.csv reports only the mean; adding per-trial
spike-count histograms would separate 'failure rate' from 'timing shift' in cable-theory
interpretation. Low effort: reuse existing sweep_results.csv, add a standalone analysis script
that writes a histogram per diameter.

</details>

<details>
<summary>📂 <strong>Per-cell ex-vivo two-photon image segmentation of
141009_Pair1DSGC to produce a cell-specific diameter ground truth</strong>
(S-0009-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-07` |
| **Kind** | dataset |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0009_calibrate_dendritic_diameters`](../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Source paper** | — |
| **Categories** | [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

The calibration imposes a nearby cell's diameters on our topology; a cell-specific ground
truth would validate or refute the transfer. The 141009_Pair1DSGC reconstruction came from the
Murphy-Baum / Feller two-photon rig; contact the original authors to obtain the raw image
stack and run a segmentation + radius-estimation pipeline (e.g., Vaa3D or neuTube) to recover
per-compartment diameters. Register the result as dsgc-baseline-morphology-imaged and use it
as the authoritative reference for sensitivity analyses like S-0009-05. Depends on external
data availability; likely requires an intervention for author contact. Recommended task types:
download-dataset, data-analysis.

</details>

<details>
<summary>📚 <strong>Port Jain 2020 DSGC (ModelDB 267001) as a sibling DSGC
asset</strong> (S-0008-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0008-05` |
| **Kind** | library |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0008_port_modeldb_189347`](../../overview/tasks/task_pages/t0008_port_modeldb_189347.md) |
| **Source paper** | [`10.7554_eLife.52949`](../../tasks/t0008_port_modeldb_189347/assets/paper/10.7554_eLife.52949/) |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

Clone ModelDB 267001 (Jain et al. 2020 eLife 56404) and port under the same HOC-driver pattern
as t0008. Jain 2020 extends the Poleg-Polsky architecture with bipolar delays and likely
shares MOD mechanisms with 189347. Medium effort (~20 hours) because the morphology and
stimulus logic are separate from 189347. Recommended task types: code-reproduction,
write-library.

</details>

<details>
<summary>📊 <strong>Promote peak-Hz and HWHM to co-primary outcomes when DSI is at
ceiling (evaluation methodology)</strong> (S-0029-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0029-07` |
| **Kind** | evaluation |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0029_distal_dendrite_length_sweep_dsgc`](../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

The t0029 null result exposes a systematic evaluation weakness: whenever the t0022-lineage
testbed drives null firing to exactly 0 Hz, pref/null DSI is structurally pinned at 1.000
regardless of the manipulated variable, yet the secondary metrics (peak somatic firing rate,
HWHM, mean peak soma voltage, vector-sum DSI) contain usable length-dependent signal (e.g.,
the non-monotonic HWHM oscillation 71.7-116.3 deg and the 15->14 Hz peak-Hz cliff at 1.25x).
Adopt a co-primary-metric convention: whenever DSI is at ceiling (range across sweep points <
0.01 or null firing = 0 Hz on > 90% of trials), elevate peak-Hz, HWHM, and vector-sum DSI to
co-primary outcome variables and require all three to be reported alongside DSI in
results_summary.md and compare_literature.md. Encode the rule as an extension to the
task-results specification, add a verificator check for the DSI-ceiling condition, and
document the convention in arf/specifications. Recommended task types: infrastructure-setup.

</details>

<details>
<summary>📊 <strong>Register patch-clamp and compartmental-modeling categories if
not already present</strong> (S-0017-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0017-04` |
| **Kind** | evaluation |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0017_literature_survey_patch_clamp`](../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md) |
| **Source paper** | — |
| **Categories** | — |

The paper assets in this task use category slugs `patch-clamp`, `voltage-gated-channels`,
`compartmental-modeling`, `direction-selectivity`, `retinal-ganglion-cell`, and
`synaptic-integration`. Verify that all six categories exist in meta/categories/; register any
that are missing so that category-based asset aggregators (aggregate_papers --categories
patch-clamp) return the expected results. This is analogous to the S-0015-03 suggestion
registered by t0015 for retinal-ganglion-cells and compartmental-modelling but may now be
satisfied by category-registration tasks executed between t0015 and t0017.

</details>

<details>
<summary>📊 <strong>Register synaptic-integration category slugs if not already
present</strong> (S-0018-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0018-04` |
| **Kind** | evaluation |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0018_literature_survey_synaptic_integration`](../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md) |
| **Source paper** | — |
| **Categories** | — |

The paper assets in this task use category slugs `synaptic-integration`, `receptor-kinetics`,
`shunting-inhibition`, `ei-balance`, `dendritic-integration`, `direction-selectivity`, and
`starburst-amacrine`. Verify that all seven categories exist in meta/categories/; register any
that are missing so that category-based asset aggregators (aggregate_papers --categories
synaptic-integration) return the expected results. This mirrors the S-0017-04 registration
suggestion and the analogous S-0015-03 / S-0016-0X registrations; may already be satisfied by
category-registration tasks executed between t0015 and t0018.

</details>

<details>
<summary>📊 <strong>Register voltage-gated-channel category slugs if not already
present</strong> (S-0019-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0019-04` |
| **Kind** | evaluation |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0019_literature_survey_voltage_gated_channels`](../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md) |
| **Source paper** | — |
| **Categories** | — |

The paper assets in this task use category slugs `voltage-gated-channels`, `nav-channels`,
`kv-channels`, `axon-initial-segment`, `hodgkin-huxley-kinetics`, `retinal-ganglion-cell`, and
`patch-clamp`. Verify that all seven categories exist in meta/categories/; register any that
are missing so that category-based asset aggregators (aggregate_papers --categories
voltage-gated-channels) return the expected results. This mirrors the S-0018-04 registration
suggestion and the analogous S-0015-03 / S-0016-0X / S-0017-04 registrations; may already be
satisfied by category-registration tasks executed between t0015 and t0019.

</details>

<details>
<summary>🧪 <strong>Sweep dendritic spine density on t0022 distal terminals as an
unconventional morphology variable</strong> (S-0027-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0027-07` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0027_literature_survey_morphology_ds_modeling`](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

No paper in the t0027 corpus sweeps dendritic spines on DSGCs; all 20 papers treat distal
terminals as smooth cables. Add explicit spine compartments (varying spine density 0, 0.5,
1.0, 2.0 spines/um on distal branches) on t0022 and measure DSI. Tests whether spine-head
capacitance shifts the dendritic-spike threshold gradient in a DS-relevant way, complementing
predictions from [Schachter2010] and [Sivyer2013]. Lower priority than the five predictive
sweeps but uniquely fills a corpus-wide blindspot identified in creative_thinking.md.

</details>

## Closed

<details>
<summary>✅ <s>Calibrate realistic dendritic diameters for dsgc-baseline-morphology
to replace the 0.125 um placeholder radii</s> — covered by <a
href="../../tasks/t0009_calibrate_dendritic_diameters/"><code>t0009_calibrate_dendritic_diameters</code></a>
(S-0005-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-02` |
| **Kind** | technique |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0005_download_dsgc_morphology`](../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`cable-theory`](../../meta/categories/cable-theory/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

Every compartment in the downloaded CNG SWC carries the placeholder radius 0.125 um because
the original Simple Neurite Tracer reconstruction did not record diameters. Cable-theory
predicts segment diameter is the single most influential local-electrotonic knob (see
S-0002-04), so leaving the uniform placeholder in place will silently bias every downstream
biophysical simulation (axial resistance, attenuation, spike initiation threshold). Build a
diameter-calibration pipeline that applies a literature-derived order-dependent diameter taper
(e.g., Vaney/Sivyer/Taylor 2012 mouse ON-OFF DSGC profile, or the Poleg-Polsky 2016
distribution) keyed on Strahler order or path distance from the soma, write the calibrated SWC
as a new dataset asset (e.g., dsgc-baseline-morphology-calibrated), and report the per-order
diameter distribution against the original placeholder. Recommended task types:
feature-engineering, data-analysis.

</details>

<details>
<summary>✅ <s>CoreNEURON Vast.ai RTX 4090 benchmark to validate or replace the
assumed 5x speedup in the t0033 cost model</s> — covered by <a
href="../../tasks/t0045_coreneuron_vastai_speedup_benchmark/"><code>t0045_coreneuron_vastai_speedup_benchmark</code></a>
(S-0033-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0033-01` |
| **Kind** | evaluation |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0033_plan_dsgc_morphology_channel_optimisation`](../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

The t0033 cost envelope rests on an unvalidated 5x CoreNEURON-over-stock-CPU-NEURON speedup
(91 s deterministic sim on RTX 4090 vs 456 s on single CPU core). The corpus documents Hines
1997 O(N) cable-solver scaling but predates GPU NEURON variants, so the 5x figure is a
literature-less guess that drives the largest sensitivity-band column. Run a short task that
(a) provisions one Vast.ai RTX 4090 under the existing filters, (b) builds CoreNEURON against
NEURON 8.2.7 with OpenACC/CUDA, (c) runs the t0022 deterministic 12-angle x 10-trial protocol
under stock NEURON and under CoreNEURON back-to-back, and (d) reports measured speedup and
per-sim USD. Outcome replaces the assumed 5x with a measured value and tightens or widens the
$23-$119 sensitivity band before the joint optimiser is commissioned. Recommended task types:
experiment-run, baseline-evaluation.

</details>

<details>
<summary>✅ <s>Download both candidate Feller-lab 2018 source papers to resolve the
dsgc-baseline-morphology provenance ambiguity</s> — covered by <a
href="../../tasks/t0013_resolve_morphology_provenance/"><code>t0013_resolve_morphology_provenance</code></a>
(S-0005-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-01` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0005_download_dsgc_morphology`](../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

The dsgc-baseline-morphology asset (NeuroMorpho neuron 102976, 141009_Pair1DSGC) currently has
source_paper_id=null because two Feller-lab papers from 2018 are plausibly the source: the
plan-nominated Morrie & Feller 2018 Neuron (DOI 10.1016/j.neuron.2018.05.028) and the
NeuroMorpho-reported Murphy-Baum & Feller 2018 Current Biology (DOI
10.1016/j.cub.2018.03.001). Run /add-paper for both DOIs in a dedicated download-paper task,
read each paper's Methods to confirm which one introduced the 141009_Pair1DSGC reconstruction,
then file a corrections asset that updates dsgc-baseline-morphology source_paper_id to the
correct paper_id slug. This unblocks correct citation of the morphology in every downstream
paper-comparison task. Recommended task types: download-paper.

</details>

<details>
<summary>✅ <s>Implement gabaMOD parameter-swap protocol for ModelDB 189347</s> —
covered by <a
href="../../tasks/t0020_port_modeldb_189347_gabamod/"><code>t0020_port_modeldb_189347_gabamod</code></a>
(S-0008-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0008-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0008_port_modeldb_189347`](../../overview/tasks/task_pages/t0008_port_modeldb_189347.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../tasks/t0008_port_modeldb_189347/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

Re-run the ModelDB 189347 port under the paper's native DS protocol: sweep gabaMOD between PD
(0.33) and ND (0.99) instead of rotating BIP synapse coordinates. This is expected to
reproduce the paper's headline DSI (~0.8) and peak firing (~32-40 Hz) that the rotation-based
proxy in t0008 cannot reach. Would be a small extension (new trial-protocol branch in
run_one_trial) with a separate tuning_curves CSV and score_report for comparison with the
rotation protocol. Recommended task types: code-reproduction.

</details>

<details>
<summary>✅ <s>Implement Nav1.6/Nav1.2/Kv1/Kv3 channel mechanisms with AIS-specific
conductance densities in downstream DSGC model</s> — covered by <a
href="../../tasks/t0043_nav16_kv3_nmda_restoration_t0022/"><code>t0043_nav16_kv3_nmda_restoration_t0022</code></a>
(S-0019-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0019-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0019_literature_survey_voltage_gated_channels`](../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/) |

The answer asset nav-kv-combinations-for-dsgc-modelling produces a 6-point specification for
DSGC voltage-gated-channel distribution in NEURON extending the synaptic-integration
constraints from t0018. The downstream DSGC compartmental-model build task must implement: (1)
Nav1.6 with V_half around -45 mV and fast kinetics at distal AIS (densities 2500-5000 pS/um2),
(2) Nav1.2 with V_half around -32 mV at proximal AIS and soma (lower density around 100-500
pS/um2), (3) Kv1.1/Kv1.2 delayed-rectifier with V_half -40 to -50 mV at AIS (density 100-500
pS/um2), (4) Fohlmeister-Miller HH rate functions with Q10 near 3 for temperature scaling (all
mechanisms tested at 22 and 32 degC), (5) passive soma/dendrite compartments with no Nav
except for low-density Nav1.2 co-expression on proximal dendrites, (6) named fitting
objectives for AP threshold (AIS initiation at -55 mV +/- 5 mV), AP width (0.5-1.0 ms at 32
degC), and backpropagation attenuation (50% by 100 um into dendrite) to reproduce
Fohlmeister-Miller RGC firing properties.

</details>

<details>
<summary>✅ <s>Implement the tuning-curve scoring loss combining DSI, peak rate, null
residual, and HWHM targets</s> — covered by <a
href="../../tasks/t0012_tuning_curve_scoring_loss_library/"><code>t0012_tuning_curve_scoring_loss_library</code></a>
(S-0002-09)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-09` |
| **Kind** | library |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1113_jphysiol.2008.161240`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1113_jphysiol.2008.161240/) |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

The survey surfaces four concurrent numerical targets an optimised DSGC model must hit (DSI
0.7-0.85, preferred peak 40-80 Hz, null residual < 10 Hz, HWHM 60-90 deg), and the project has
four registered metrics (direction_selectivity_index, tuning_curve_hwhm_deg,
tuning_curve_reliability, tuning_curve_rmse). Build a scoring library that takes a simulated
angle-to-AP-rate tuning curve plus the canonical target curve from t0004 and returns a single
scalar loss combining all four targets with documented weights (e.g., weighted Euclidean
distance in normalised space), plus per-metric residuals. This is the tool every downstream
optimisation task (Na/K grid, morphology sweep, E/I ratio scan) will depend on. Recommended
task types: write-library.

</details>

<details>
<summary>✅ <s>Install and validate NEURON 8.2.7 + NetPyNE 1.1.1 toolchain on the
local workstation</s> — covered by <a
href="../../tasks/t0007_install_neuron_netpyne/"><code>t0007_install_neuron_netpyne</code></a>
(S-0003-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0003-01` |
| **Kind** | library |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0003_simulator_library_survey`](../../overview/tasks/task_pages/t0003_simulator_library_survey.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

Create a task that `uv pip install neuron==8.2.7 netpyne==1.1.1` into the project's
virtualenv, compiles the bundled Hodgkin-Huxley MOD files with `nrnivmodl`, runs a
1-compartment sanity simulation, and records the installed versions, install-time warnings,
and simulation wall-clock in a task asset. Rationale: the t0003 survey selected this toolchain
but did not install it; the next simulation task needs a validated environment.

</details>

<details>
<summary>✅ <s>Literature survey: cable theory and dendritic filtering (target ~25
papers)</s> — covered by <a
href="../../tasks/t0015_literature_survey_cable_theory/"><code>t0015_literature_survey_cable_theory</code></a>
(S-0014-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0014-01` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0014_brainstorm_results_3`](../../overview/tasks/task_pages/t0014_brainstorm_results_3.md) |
| **Source paper** | — |
| **Categories** | [`cable-theory`](../../meta/categories/cable-theory/) |

Systematically survey cable-theory and passive dendritic-filtering literature relevant to
direction-selective retinal ganglion cells. Target ~25 category-relevant papers spanning
Rall-era foundations, modern compartmental treatments, impedance / space-constant analyses,
and segment-discretisation guidelines. Exclude the 20 DOIs already in the t0002 corpus.
Output: paper assets + synthesis document organised by theme (classical cable theory, segment
discretisation, branched-tree impedance, frequency-domain analyses, transmission in thin
dendrites).

</details>

<details>
<summary>✅ <s>Literature survey: dendritic computation outside DSGCs (target ~25
papers)</s> — covered by <a
href="../../tasks/t0016_literature_survey_dendritic_computation/"><code>t0016_literature_survey_dendritic_computation</code></a>
(S-0014-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0014-02` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0014_brainstorm_results_3`](../../overview/tasks/task_pages/t0014_brainstorm_results_3.md) |
| **Source paper** | — |
| **Categories** | [`dendritic-computation`](../../meta/categories/dendritic-computation/) |

Systematically survey dendritic-computation literature beyond DSGC-specific work. Target ~25
category-relevant papers covering NMDA spikes, Na+/Ca2+ dendritic spikes, plateau potentials,
branch-level nonlinearities, sublinear-to-supralinear integration regimes, and
active-vs-passive comparisons in cortical and cerebellar neurons. Exclude the 20 DOIs already
in the t0002 corpus. Output: paper assets + synthesis highlighting which mechanisms plausibly
transfer to DSGC dendrites.

</details>

<details>
<summary>✅ <s>Literature survey: patch-clamp recordings of RGCs and DSGCs (target
~25 papers)</s> — covered by <a
href="../../tasks/t0017_literature_survey_patch_clamp/"><code>t0017_literature_survey_patch_clamp</code></a>
(S-0014-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0014-03` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0014_brainstorm_results_3`](../../overview/tasks/task_pages/t0014_brainstorm_results_3.md) |
| **Source paper** | — |
| **Categories** | [`patch-clamp`](../../meta/categories/patch-clamp/) |

Systematically survey patch-clamp recording literature relevant to validating DSGC
compartmental models. Target ~25 category-relevant papers covering somatic whole-cell
recordings of RGCs, voltage-clamp conductance dissections, space-clamp error analyses,
spike-train tuning-curve measurements, and in-vitro stimulus protocols. Exclude the 20 DOIs
already in the t0002 corpus. Output: paper assets + synthesis mapping each paper to the model
validation targets (AP rate, IPSC asymmetry, EPSP kinetics, null/preferred ratios).

</details>

<details>
<summary>✅ <s>Literature survey: synaptic integration in RGC-adjacent systems
(target ~25 papers)</s> — covered by <a
href="../../tasks/t0018_literature_survey_synaptic_integration/"><code>t0018_literature_survey_synaptic_integration</code></a>
(S-0014-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0014-04` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0014_brainstorm_results_3`](../../overview/tasks/task_pages/t0014_brainstorm_results_3.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../meta/categories/synaptic-integration/) |

Systematically survey synaptic-integration literature relevant to DSGC dendrites. Target ~25
category-relevant papers covering AMPA/NMDA/GABA receptor kinetics, shunting inhibition, E-I
balance, temporal summation, dendritic-location dependence, synaptic-density scaling, and
SAC/DSGC inhibitory asymmetry. Exclude the 20 DOIs already in the t0002 corpus. Output: paper
assets + synthesis of kinetics parameters and E-I ratios usable as prior distributions in
later optimisation tasks.

</details>

<details>
<summary>✅ <s>Literature survey: voltage-gated channels in retinal ganglion cells
(target ~25 papers)</s> — covered by <a
href="../../tasks/t0019_literature_survey_voltage_gated_channels/"><code>t0019_literature_survey_voltage_gated_channels</code></a>
(S-0014-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0014-05` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0014_brainstorm_results_3`](../../overview/tasks/task_pages/t0014_brainstorm_results_3.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/) |

Systematically survey voltage-gated-channel literature relevant to RGC/DSGC modelling. Target
~25 category-relevant papers covering Na_v 1.1-1.6 and K_v subtype expression, HH-family
kinetic models, subunit co-expression patterns in RGCs, ModelDB MOD-file provenance, and
Nav/Kv conductance-density estimates. Exclude the 20 DOIs already in the t0002 corpus. Output:
paper assets + synthesis mapping candidate Na/K conductance combinations to published DSGC
tuning-curve fits.

</details>

<details>
<summary>✅ <s>Paired active-vs-passive dendrite experiment to reproduce the
Schachter2010 DSI gain (~0.3 -> ~0.7)</s> — covered by <a
href="../../tasks/t0044_schachter_retest_on_t0043/"><code>t0044_schachter_retest_on_t0043</code></a>
(S-0002-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1371_journal.pcbi.1000899`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1371_journal.pcbi.1000899/) |
| **Categories** | [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

Schachter2010 reports that switching DSGC dendrites from passive to active (adding
Fohlmeister-like g_Na and g_K) raises DSI from ~0.3 to ~0.7 on the same morphology and
synaptic input, and Oesch2005 provides the TTX-sensitive dendritic Na+ spike patch-clamp data
that anchor this claim. Run two paired simulations that differ only in dendritic g_Na (0 vs
Schachter2010 density), holding morphology, synapse placement, and stimulus identical, and
report the DSI delta with 95% CI across synapse-placement seeds. This directly answers RQ4 and
isolates the dendritic-conductance contribution from morphology and synaptic effects.
Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary>✅ <s>Reproduce the PolegPolsky2016 baseline DSGC model from ModelDB 189347
as the project's starting compartmental simulation</s> — covered by <a
href="../../tasks/t0008_port_modeldb_189347/"><code>t0008_port_modeldb_189347</code></a>
(S-0002-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-03` |
| **Kind** | technique |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |

PolegPolsky2016 (paper 10.1016_j.neuron.2016.02.013) is the closest published match to this
project's goal — a NEURON multi-compartmental mouse ON-OFF DSGC model with 177 AMPA + 177 GABA
synapses and NMDA multiplicative gain — with public code at ModelDB entry 189347. Download the
ModelDB code, run the original published stimulus, and verify the reproduced tuning curve
lands inside the published DSI 0.7-0.85 / peak 40-80 Hz / null < 10 Hz / HWHM 60-90 deg
envelope. This creates the reference implementation the later parameter-variation tasks (Na/K
grid, morphology sweep, E/I ratio scan) will fork from. Recommended task types:
code-reproduction.

</details>

<details>
<summary>✅ <s>Rerun t0030's 7-diameter sweep at GABA=4 nS on t0022</s> — covered by
<a
href="../../tasks/t0039_distal_dendrite_diameter_sweep_t0022_gaba4/"><code>t0039_distal_dendrite_diameter_sweep_t0022_gaba4</code></a>
(S-0037-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0037-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0037_null_gaba_reduction_ladder_t0022`](../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`cable-theory`](../../meta/categories/cable-theory/) |

t0030's diameter sweep was uninformative because DSI was pinned at 1.000 (null firing = 0 Hz
at 12 nS GABA). With 4 nS, the t0037 sweet spot, the t0022 testbed produces biologically
realistic DSI (0.429) and preferred direction (40 deg). Rerun the original 7-diameter sweep
(0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0 um) with GABA_CONDUCTANCE_NULL_NS=4.0 to measure the
Schachter2010-vs-passive-filtering slope that has been the project's headline discriminator
target since t0030.

</details>

<details>
<summary>✅ <s>Rerun the distal-diameter sweep on t0022 with null-GABA conductance
reduced from 12 nS to 6 nS</s> — covered by <a
href="../../tasks/t0036_rerun_t0030_halved_null_gaba/"><code>t0036_rerun_t0030_halved_null_gaba</code></a>
(S-0030-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0030-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../meta/categories/dendritic-computation/) |

The t0030 sweep failed as a Schachter2010-vs-passive-filtering discriminator because primary
DSI is pinned at 1.000 at every diameter multiplier (null firing 0 Hz under the t0022 E-I
schedule). compare_literature.md traces the ceiling to GABA_CONDUCTANCE_NULL_NS = 12 nS
delivered 10 ms before AMPA on null trials, about 2x Schachter2010's compound null inhibition
(~6 nS). Rerun the full 7-point diameter sweep (0.5x-2.0x, 12 angles x 10 trials = 840 trials)
with GABA_CONDUCTANCE_NULL_NS lowered to 6 nS so null firing becomes non-zero and primary DSI
regains dynamic range. Distinct from S-0029-04 (null-GABA sweep at fixed length 1.0x) and
S-0029-01 (Poisson + length sweep): this targets the diameter axis specifically. Expected
cost: local CPU, ~2 h wall time. Recommended task types: experiment-run.

</details>

<details>
<summary>✅ <s>Retrieve paywalled Kim2014 and Sivyer2013 PDFs via Sheffield SSO and
upgrade their summaries to full-text grounding</s> — covered by <a
href="../../tasks/t0031_fetch_paywalled_morphology_papers/"><code>t0031_fetch_paywalled_morphology_papers</code></a>
(S-0027-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0027-06` |
| **Kind** | dataset |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0027_literature_survey_morphology_ds_modeling`](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../meta/categories/dendritic-computation/) |

Two papers (Kim2014, Sivyer2013) were flagged in t0027 intervention/ folder as paywalled and
summarised from abstract + secondary citations only. Both are load-bearing for predictions
S-0027-01 and S-0027-02. Resolve by retrieving full PDFs through Sheffield institutional SSO
(Cell Press, Nature Neuroscience), upgrading their summaries to full-text level, and updating
the t0027 synthesis answer asset citations from abstract-only to full-text grounding. Low-cost
prerequisite for confidently running S-0027-01 and S-0027-02.

</details>

<details>
<summary>✅ <s>Sequential further null-GABA reductions (4, 2, 1 nS) on the t0022
distal-diameter sweep</s> — covered by <a
href="../../tasks/t0037_null_gaba_reduction_ladder_t0022/"><code>t0037_null_gaba_reduction_ladder_t0022</code></a>
(S-0036-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0036-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0036_rerun_t0030_halved_null_gaba`](../../overview/tasks/task_pages/t0036_rerun_t0030_halved_null_gaba.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../meta/categories/dendritic-computation/) |

t0036 halved GABA_CONDUCTANCE_NULL_NS from 12 nS to 6 nS and null firing stayed pinned at 0.0
Hz at every diameter multiplier, falsifying the Schachter2010 ~6 nS compound-inhibition
rescue. The classifier auto-recommendation was 'reduce null-GABA further to ~4 nS'. Rerun the
t0036 diameter sweep at 4 nS, 2 nS, and 1 nS (stop as soon as mean null firing exceeds 0.1 Hz
at 1.0x); each rerun is ~30 min CPU so worst case ~1.5 h. If null firing unpins at 4 or 2 nS,
primary DSI becomes measurable and the Schachter2010-vs-passive slope discriminator is rescued
on deterministic t0022. If it stays 0 Hz down to 1 nS, the testbed is structurally
incompatible with primary DSI on morphology axes and the project must adopt Poisson rescue
(S-0030-02) or migrate the optimiser substrate to t0024 (S-0034-07). Distinct from S-0029-04
(3-12 nS at fixed length on t0029 code) - this extends below the 3 nS floor on the t0036
diameter-sweep code path. Recommended task types: experiment-run.

</details>

<details>
<summary>✅ <s>Sweep distal-dendrite scale on t0022 to discriminate passive TR
weighting vs dendritic-spike branch independence</s> — covered by <a
href="../../tasks/t0034_distal_dendrite_length_sweep_t0024/"><code>t0034_distal_dendrite_length_sweep_t0024</code></a>
(S-0027-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0027-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0027_literature_survey_morphology_ds_modeling`](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |

Run t0022 with distal dendritic segments scaled by 1.0x, 1.25x, and 1.5x at fixed synapse
count and biophysics. Prediction (creative_thinking.md #1): if passive transfer-resistance
weighting [Dan2018, 10.1101_2024.07.10.602901] dominates, DSI drops by >30% at 1.5x; if
dendritic-spike branch independence [Sivyer2013, 10.1038_nn.3565] dominates, DSI stays within
10%. High-information-gain experiment that resolves a core mechanism ambiguity in the surveyed
corpus and directly informs whether morphology-sweep design must preserve cable geometry or
only branch topology.

</details>

<details>
<summary>✅ <s>Thicken distal branches on t0022 (halve distal input resistance) to
separate active amplification from passive filtering</s> — covered by <a
href="../../tasks/t0035_distal_dendrite_diameter_sweep_t0024/"><code>t0035_distal_dendrite_diameter_sweep_t0024</code></a>
(S-0027-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0027-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0027_literature_survey_morphology_ds_modeling`](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Source paper** | [`10.1371_journal.pcbi.1000899`](../../tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1371_journal.pcbi.1000899/) |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

Halve the input resistance of distal dendritic branches on t0022 by doubling their diameter
and re-running the DSI protocol with active conductances (a) intact and (b) ablated.
Prediction (creative_thinking.md #3): if [Schachter2010, 10.1371_journal.pcbi.1000899]
dendritic-spike gain is essential, thickening abolishes active gain but preserves subthreshold
DSI; if passive filtering carries DSI, thickening preserves both. Disambiguates the active vs
passive contribution that the corpus does not separate cleanly.

</details>

<details>
<summary>✅ <s>Update t0033 optimiser base GABA on t0022 variant to 4.0 nS</s> —
covered by <a
href="../../tasks/t0038_correct_t0033_base_gaba_to_4ns/"><code>t0038_correct_t0033_base_gaba_to_4ns</code></a>
(S-0037-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0037-02` |
| **Kind** | technique |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0037_null_gaba_reduction_ladder_t0022`](../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |

t0033 is scoped to sweep t0022 parameters against a primary-DSI objective. With
GABA_CONDUCTANCE_NULL_NS=12 the objective is pinned and the optimiser sees no gradient. Update
t0033's t0022 variant to set GABA_CONDUCTANCE_NULL_NS=4.0 as the base parameter; this is the
first point at which the t0022 primary-DSI landscape can be optimised meaningfully. Without
this change the Vast.ai optimisation runs on t0022 will be wasted compute.

</details>

<details>
<summary>✅ <s>Zero-cost L/lambda collapse analysis of all t0034 length and t0035
diameter data</s> — covered by <a
href="../../tasks/t0041_electrotonic_length_collapse_t0034_t0035/"><code>t0041_electrotonic_length_collapse_t0034_t0035</code></a>
(S-0035-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0035-01` |
| **Kind** | evaluation |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0035_distal_dendrite_diameter_sweep_t0024`](../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md) |
| **Source paper** | — |
| **Categories** | [`cable-theory`](../../meta/categories/cable-theory/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |

Re-plot DSI from all existing t0034 (length sweep) and t0035 (diameter sweep) trials against
the computed distal electrotonic length L/lambda, using morphology and passive parameters
already stored in each task's outputs. If the length and diameter data collapse onto a single
curve, this confirms creative_thinking.md's primary hypothesis: the length/diameter asymmetry
is a consequence of cable theory (L/lambda is linear in length but scales as 1/sqrt(d)). No
new simulations required; ~1-2 hours of re-analysis work only. Recommended task types:
data-analysis.

</details>
