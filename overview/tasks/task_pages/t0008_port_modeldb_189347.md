# ⏹ Port ModelDB 189347 and similar DSGC compartmental models to NEURON

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0008_port_modeldb_189347` |
| **Status** | ⏹ not_started |
| **Dependencies** | [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md) |
| **Source suggestion** | `S-0002-03` |
| **Task types** | `code-reproduction`, `write-library` |
| **Expected assets** | 1 library, 1 answer |
| **Task folder** | [`t0008_port_modeldb_189347/`](../../../tasks/t0008_port_modeldb_189347/) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0008_port_modeldb_189347/task_description.md)*

# Port ModelDB 189347 and similar DSGC compartmental models to NEURON as library assets

## Motivation

Poleg-Polsky & Diamond 2016 (paper `10.1016_j.neuron.2016.02.013`, ModelDB 189347) is the
closest published match to this project's goal: a NEURON multi-compartmental mouse ON-OFF DSGC
model with **177 AMPA + 177 GABA** synapses and NMDA multiplicative gain. Reproducing it
creates the reference implementation that every later parameter-variation task (Na/K grid
S-0002-01, morphology sweep S-0002-04, E/I ratio scan S-0002-05, active-vs-passive dendrites
S-0002-02) will fork from. It is also the cleanest end-to-end test that the NEURON+NetPyNE
install from t0007 and the calibrated morphology from t0009 are fit for purpose.

Covers suggestions **S-0002-03** and **S-0003-02** (merged — the two suggestions describe the
same work from slightly different angles).

## Scope

### Phase A — Port the Poleg-Polsky 2016 baseline

1. Download ModelDB entry 189347 and register the resulting Python package under
   `assets/library/dsgc-polegpolsky-2016/` with a description, module paths, test paths, and a
   smoke-test that instantiates the model and runs a single angle.
2. Swap in the calibrated morphology produced by t0009 (`dsgc-baseline-morphology-calibrated`)
   in place of the ModelDB-bundled morphology. Document the swap and any geometric differences
   (compartment count, dendritic path length, branch points) vs the original ModelDB
   morphology.
3. Run the published stimulus: drifting bar / moving spot at 12 angles (30° spacing), synaptic
   configuration matching the paper, Poleg-Polsky NMDA parameters.
4. Compute the simulated tuning curve (firing rate vs angle, 20 trials per angle with fresh
   seeds) and score it with the t0012 scoring loss library against the envelope: DSI
   **0.7-0.85**, preferred peak **40-80 Hz**, null residual **< 10 Hz**, HWHM **60-90°**.

### Phase B — Hunt for sibling DSGC compartmental models

5. Search ModelDB, SenseLab, OSF, and GitHub for additional DSGC compartmental models cited or
   adjacent in the literature (Schachter2010 derivatives, Briggman-lineage forks, 2017-2025
   updates of the Poleg-Polsky model, any post-2020 published code).
6. For each model found, record: source URL, NEURON compatibility, morphology it ships with,
   synaptic configuration, and whether it runs out-of-the-box in this environment.
7. Port any model that has public code and runs cleanly as a separate library asset under
   `assets/library/<model-slug>/`. If a model fails to run, record the failure in the Phase B
   answer asset and do not register a broken library.

## Dependencies

* **t0005_download_dsgc_morphology** — source of `dsgc-baseline-morphology`
* **t0007_install_neuron_netpyne** — NEURON+NetPyNE must work before any simulation runs
* **t0009_calibrate_dendritic_diameters** — needs calibrated morphology to avoid biasing the
  reproduction with placeholder 0.125 µm radii
* **t0012_tuning_curve_scoring_loss_library** — envelope verification must use the canonical
  scoring library, not an ad-hoc check

## Expected Outputs

* **1 library asset** (`assets/library/dsgc-polegpolsky-2016/`) — the ported ModelDB 189347.
* **1 answer asset** (`assets/answer/dsgc-modeldb-port-reproduction-report/`) covering:
  * Phase A: envelope verification table (DSI, peak, null, HWHM) vs targets
  * Phase B: a survey row-per-model listing each candidate found, its source, its NEURON
    compatibility, whether it was ported, and if not, why
* **0 or more additional library assets** for any sibling models successfully ported.
* **Simulated tuning-curve CSVs** under `data/tuning_curves/` (per model, per seed) for t0011
  to consume.

## Approach

* Write `code/port_modeldb_189347.py` that downloads the ModelDB zip, unpacks it into the
  library asset folder, compiles its MOD files with `nrnivmodl`, and runs the published demo
  to confirm the port is intact before any morphology swap.
* Write `code/run_tuning_curve.py` that takes a library name and a morphology (calibrated
  SWC), runs 12 angles × 20 seeded trials, writes `tuning_curve.csv` with `(angle_deg,
  trial_seed, firing_rate_hz)`.
* Write `code/score_envelope.py` that imports the t0012 scoring library and produces the
  verification table.
* For Phase B: write `code/hunt_sibling_models.py` that scrapes ModelDB's category listings
  (the author's own follow-up entries, neighbouring DSGC entries, 2017+ entries citing 189347)
  and writes a candidate-list CSV. Human review selects which candidates to attempt porting
  before Phase B code runs.

## Compute and Budget

Local only. 12 angles × 20 trials × ~5-10 s wall-clock per trial ≈ 20-40 minutes per model on
this workstation. Budget remains `$0.00`.

## Questions the task answers

1. Does the reproduced Poleg-Polsky 2016 model hit the envelope: DSI 0.7-0.85, peak 40-80 Hz,
   null < 10 Hz, HWHM 60-90°?
2. Does swapping the ModelDB morphology for the calibrated Feller morphology preserve envelope
   compliance, or does it shift the model outside the envelope?
3. Which sibling DSGC compartmental models exist in public repositories, and which run in this
   environment?
4. Are there published DSGC compartmental models whose tuning curves systematically disagree
   with the Poleg-Polsky envelope, and if so, by how much?

## Risks and Fallbacks

* **ModelDB 189347 has drifted or the Python wrapper is stale**: port the `hoc`/`mod` files
  directly and wrap in a minimal Python loader; record the drift in the answer asset.
* **Swapping to the calibrated morphology produces envelope failure**: treat that as a
  scientific finding, not a blocker — report it verbatim and surface a new suggestion for
  morphology- conditioned parameter retuning.
* **Phase B finds no portable sibling models**: document the gap as a new suggestion and do
  not invent models to port.

</details>
