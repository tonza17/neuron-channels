# Suggestions: `synaptic-integration`

10 suggestion(s) in category
[`synaptic-integration`](../../../meta/categories/synaptic-integration/) **8 open** (3 high, 5
medium), **2 closed**.

[Back to all suggestions](../README.md)

---

## High Priority

<details>
<summary>🧪 <strong>Hand-port deRosenroll2026 ds-circuit-ei model and remap 8-angle
grid to 12 angles</strong> (S-0010-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0010-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md) |
| **Source paper** | [`10.1016_j.celrep.2025.116833`](../../../tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1016_j.celrep.2025.116833/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

Port geoffder/ds-circuit-ei-microarchitecture (Zenodo 10.5281/zenodo.17666157, MIT LICENSE).
Requires adding statsmodels, h5py, fastparquet, oiffile as optional deps (or extracting a
minimal driver subset without them), then extending the hardcoded 8-direction ANGLES_DEG list
to the canonical 12-angle protocol before scoring. t0010 exited at P2 within the 90-min cap;
budget 4-6 hours for full P3.

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
| **Source task** | [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

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
<summary>🧪 <strong>Retrieve paywalled synaptic-integration PDFs via Sheffield access
and verify numerical priors</strong> (S-0018-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0018-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

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

## Medium Priority

<details>
<summary>📂 <strong>Download the four discovered papers not included in the 20-paper
budget (Sivyer2017, Euler2002, Enciso2010, Webvision)</strong> (S-0002-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-07` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

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
<summary>🧪 <strong>Extend synaptic-integration survey with DSGC-specific
receptor-kinetic, dynamic-clamp, and connectomic SAC-DSGC papers</strong>
(S-0018-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0018-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

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
<summary>🧪 <strong>GABA/AMPA density ratio scan at fixed 3-5x null/preferred IPSC
asymmetry</strong> (S-0002-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

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
<summary>🧪 <strong>NMDA multiplicative-gain ablation to isolate its contribution
to DSI</strong> (S-0002-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-06` |
| **Kind** | experiment |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

PolegPolsky2016 reports that NMDA receptors multiplicatively scale excitatory drive by ~2x and
sharpen directional discrimination, but the survey did not find a published ablation that
isolates the NMDA contribution independently of the AMPA+GABA core. Run three configurations
on the reproduced DSGC baseline (AMPA+GABA only, AMPA+GABA+NMDA with PolegPolsky2016 NMDA
parameters, AMPA+GABA+NMDA with NMDA_gain swept 1-4x) and report the DSI, peak rate, and HWHM
trajectories. This answers a specific open RQ3/RQ4-adjacent question that the literature
states but does not isolate experimentally. Recommended task types: experiment-run.

</details>

<details>
<summary>📚 <strong>Register SAC presynaptic drive model as an asset for downstream
DSGC input construction</strong> (S-0002-08)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-08` |
| **Kind** | library |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1038_nature09818`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nature09818/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

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

## Closed

<details>
<summary>✅ <s>Literature survey: synaptic integration in RGC-adjacent systems
(target ~25 papers)</s> — covered by <a
href="../../../tasks/t0018_literature_survey_synaptic_integration/"><code>t0018_literature_survey_synaptic_integration</code></a>
(S-0014-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0014-04` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0014_brainstorm_results_3`](../../../overview/tasks/task_pages/t0014_brainstorm_results_3.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

Systematically survey synaptic-integration literature relevant to DSGC dendrites. Target ~25
category-relevant papers covering AMPA/NMDA/GABA receptor kinetics, shunting inhibition, E-I
balance, temporal summation, dendritic-location dependence, synaptic-density scaling, and
SAC/DSGC inhibitory asymmetry. Exclude the 20 DOIs already in the t0002 corpus. Output: paper
assets + synthesis of kinetics parameters and E-I ratios usable as prior distributions in
later optimisation tasks.

</details>

<details>
<summary>✅ <s>Reproduce the PolegPolsky2016 baseline DSGC model from ModelDB 189347
as the project's starting compartmental simulation</s> — covered by <a
href="../../../tasks/t0008_port_modeldb_189347/"><code>t0008_port_modeldb_189347</code></a>
(S-0002-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-03` |
| **Kind** | technique |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

PolegPolsky2016 (paper 10.1016_j.neuron.2016.02.013) is the closest published match to this
project's goal — a NEURON multi-compartmental mouse ON-OFF DSGC model with 177 AMPA + 177 GABA
synapses and NMDA multiplicative gain — with public code at ModelDB entry 189347. Download the
ModelDB code, run the original published stimulus, and verify the reproduced tuning curve
lands inside the published DSI 0.7-0.85 / peak 40-80 Hz / null < 10 Hz / HWHM 60-90 deg
envelope. This creates the reference implementation the later parameter-variation tasks (Na/K
grid, morphology sweep, E/I ratio scan) will fork from. Recommended task types:
code-reproduction.

</details>
