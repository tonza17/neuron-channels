# ⏹ Tasks: Not Started

4 tasks. ⏹ **4 not_started**.

[Back to all tasks](../README.md)

---

## ⏹ Not Started

<details>
<summary>⏹ 0005 — <strong>Download candidate DSGC morphology</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0005_download_dsgc_morphology` |
| **Status** | not_started |
| **Effective date** | — |
| **Dependencies** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Expected assets** | 1 dataset |
| **Source suggestion** | — |
| **Task types** | [`download-dataset`](../../../meta/task_types/download-dataset/) |
| **Task page** | [Download candidate DSGC morphology](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Task folder** | [`t0005_download_dsgc_morphology/`](../../../tasks/t0005_download_dsgc_morphology/) |

# Download candidate DSGC morphology

## Motivation

Every downstream simulation task needs a concrete reconstructed morphology to load. Rather
than generating a synthetic branching structure, we want a published DSGC (or DSGC-like RGC)
reconstruction used by prior modelling work. The literature survey (t0002) produces the
shortlist; this task commits to one file.

## Scope

Download one reconstructed DSGC morphology in SWC format (or HOC / NeuroML if SWC is not
available) from a public source such as NeuroMorpho.org, ModelDB, or a paper's supplementary
materials. The morphology should be one of those flagged as suitable in t0002's answer asset.

## Approach

1. Read t0002's answer asset to pick the recommended morphology.
2. Download the file and verify it loads as a valid SWC / HOC structure.
3. Record its provenance (source URL, paper DOI, reconstruction protocol) in the dataset asset
   metadata.

## Expected Outputs

* One dataset asset under `assets/dataset/dsgc_baseline_morphology/` containing the morphology
  file(s) and metadata.

## Compute and Budget

No external cost.

## Dependencies

`t0002_literature_survey_dsgc_compartmental_models` — the literature survey produces the
morphology shortlist and rationale.

## Verification Criteria

* Dataset asset passes `verify_dataset_asset.py`.
* The asset's `details.json` links back to the source paper or NeuroMorpho record.
* The downloaded file loads without errors in at least one candidate simulator library.

</details>

<details>
<summary>⏹ 0004 — <strong>Generate canonical target angle-to-AP-rate tuning
curve</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0004_generate_target_tuning_curve` |
| **Status** | not_started |
| **Effective date** | — |
| **Dependencies** | — |
| **Expected assets** | 1 dataset |
| **Source suggestion** | — |
| **Task types** | [`feature-engineering`](../../../meta/task_types/feature-engineering/) |
| **Task page** | [Generate canonical target angle-to-AP-rate tuning curve](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md) |
| **Task folder** | [`t0004_generate_target_tuning_curve/`](../../../tasks/t0004_generate_target_tuning_curve/) |

# Generate canonical target angle-to-AP-rate tuning curve

## Motivation

The key project metric `tuning_curve_rmse` compares a simulated angle-to-AP-rate tuning curve
against a target. The researcher chose to **simulate** a canonical target curve rather than
digitise one from a paper. This task generates that canonical target and registers it as a
dataset asset so all later optimisation tasks share one fixed reference.

## Scope

Produce a single dataset asset containing:

* A cosine-like target tuning curve sampled at 12 or 24 angles around 360°.
* Explicit generator parameters: preferred direction (deg), baseline rate (Hz), peak rate
  (Hz), tuning half-width (deg or von Mises κ), and random seed.
* Per-angle mean rates plus a small number of synthetic noisy trial replicates so the
  `tuning_curve_reliability` metric has a well-defined ground-truth value.

Suggested functional form:

```
r(θ) = r_base + (r_peak - r_base) * ((1 + cos(θ - θ_pref)) / 2) ** n
```

with `n` controlling sharpness. Any equivalent von Mises formulation is fine. The exact values
of `r_base`, `r_peak`, `θ_pref`, and `n` should be chosen to give a biologically plausible DSI
(roughly 0.6-0.9) and reported in the dataset's `details.json`.

## Approach

1. Write a small Python script under `code/` that generates the curve, saves it to `data/` as
   CSV or JSON, and writes the dataset asset folder under `assets/dataset/`.
2. Include both a mean-rate table and a per-trial table (e.g., 20 synthetic trials) so
   `tuning_curve_reliability` has a real reference value.
3. Plot the curve and save to `results/images/target_tuning_curve.png`.

## Expected Outputs

* One dataset asset under `assets/dataset/target_tuning_curve/` containing the CSV/JSON
  tables, metadata, and description.
* A plot of the target curve in `results/images/`.

## Compute and Budget

Trivial. Runs locally in seconds; no external cost.

## Dependencies

None. Runs in parallel with t0002 and t0003. This task is the reference any later optimisation
task will compare against.

## Verification Criteria

* Dataset asset passes `verify_dataset_asset.py`.
* `details.json` records the generator parameters and random seed explicitly.
* The generated CSV/JSON has one row per angle and the noisy-trial table has at least 10
  trials per angle.

</details>

<details>
<summary>⏹ 0003 — <strong>Simulator library survey for DSGC compartmental
modelling</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0003_simulator_library_survey` |
| **Status** | not_started |
| **Effective date** | — |
| **Dependencies** | — |
| **Expected assets** | 1 answer |
| **Source suggestion** | — |
| **Task types** | [`internet-research`](../../../meta/task_types/internet-research/) |
| **Task page** | [Simulator library survey for DSGC compartmental modelling](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md) |
| **Task folder** | [`t0003_simulator_library_survey/`](../../../tasks/t0003_simulator_library_survey/) |

# Simulator library survey for DSGC compartmental modelling

## Motivation

`project/description.md` mentions NEURON as the canonical simulator but the researcher wants
to evaluate several libraries before committing. A bad simulator choice locks the project into
poor cable-model fidelity, slow parameter sweeps, or brittle tooling for months. A short
survey up front prevents this.

## Scope

Evaluate the following candidate libraries:

* NEURON (plus NEURON+Python bindings)
* NetPyNE (higher-level NEURON wrapper)
* Brian2 with cable-model extensions
* MOOSE
* Arbor

For each library, collect:

1. **Cable-model fidelity** — does it solve the full compartmental cable equation, support
   voltage-gated conductances in arbitrary compartments, and handle reconstructed morphologies
   (SWC, HOC, NeuroML)?
2. **Python ergonomics** — pure Python vs wrapped C++/MOD files, packaging on `uv`, quality of
   current documentation and examples.
3. **Speed and parallelism** — single-cell simulation speed and support for running large
   parameter sweeps.
4. **DSGC examples available** — whether any published DSGC or broader RGC compartmental model
   has been released in that library.
5. **Long-term maintenance** — last release, community activity, active maintainers.

## Approach

1. Run `/research-internet` to gather documentation, benchmarks, and user reports for each
   library.
2. Build a comparison table covering the five axes above.
3. Produce a single answer asset that recommends a **primary** simulator plus one **backup**,
   with explicit rationale.

## Expected Outputs

* One answer asset under `assets/answer/` summarising the library comparison and stating the
  primary plus backup recommendation.

## Compute and Budget

No external cost. Local LLM CLI and internet search only.

## Dependencies

None. Runs in parallel with t0002 and t0004.

## Verification Criteria

* The answer asset passes `verify_answer_asset.py`.
* The `## Answer` section states the primary and backup simulator in one or two sentences.
* The full answer includes the five-axis comparison table for every candidate library.

</details>

<details>
<summary>⏹ 0002 — <strong>Literature survey: compartmental models of DS retinal
ganglion cells</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0002_literature_survey_dsgc_compartmental_models` |
| **Status** | not_started |
| **Effective date** | — |
| **Dependencies** | — |
| **Expected assets** | 20 paper, 1 answer |
| **Source suggestion** | — |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/) |
| **Task page** | [Literature survey: compartmental models of DS retinal ganglion cells](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Task folder** | [`t0002_literature_survey_dsgc_compartmental_models/`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/) |

# Literature survey: compartmental models of DS retinal ganglion cells

## Motivation

This is the project's first research task. Before building any simulation we need a shared
knowledge base of what prior compartmental modelling work has done on direction-selective
retinal ganglion cells (DSGCs) and what each of the project's five research questions (RQs)
looks like in the literature. The survey feeds every downstream task: the target tuning curve
generator (t0004) needs published tuning-curve shapes, the morphology download (t0005) needs a
shortlist of reconstructed DSGCs, and the later Na/K optimisation and active-vs-passive
dendrite experiments need candidate channel models and parameter ranges.

## Scope

Cover all five project research questions at survey level:

1. **RQ1 Na/K combinations** — how published DSGC and related RGC models parameterise somatic
   sodium and potassium conductances, and what combinations reproduce directional AP firing.
2. **RQ2 morphology sensitivity** — how branching pattern, dendritic diameter, and compartment
   length have been shown to affect DS tuning.
3. **RQ3 AMPA/GABA balance** — ratio and spatial distribution of excitatory and inhibitory
   inputs, and their measured effect on DS sharpness.
4. **RQ4 active vs passive dendrites** — evidence for dendritic voltage-gated conductances in
   DSGCs, and modelling studies that compare active with passive dendrites.
5. **RQ5 angle-to-AP-frequency tuning curves** — reported tuning-curve shapes, peak rates,
   half-widths, and null-direction suppression levels that can serve as optimisation targets.

Minimum breadth:

* Include the six references already listed in `project/description.md` (Barlow & Levick 1965,
  Hines & Carnevale 1997, Vaney/Sivyer/Taylor 2012, Poleg-Polsky & Diamond 2016,
  Oesch/Euler/Taylor 2005, Branco/Clark/Häusser 2010).
* Add at least 14 more papers found by internet search, spread across the five research
  questions.
* Prefer papers with a clearly described compartmental model, published morphology, or
  quantitative angle-to-rate measurements.

## Approach

1. Run `/research-papers` using the six seed references to build initial paper assets.
2. Run `/research-internet` to find additional compartmental DSGC modelling papers and any
   patch-clamp studies that report tuning curves.
3. Download each selected paper via `/download-paper` so every cited paper becomes a paper
   asset with a summary.
4. Produce one answer asset that synthesises, across all five RQs, what the existing
   literature says about how to structure the DSGC modelling problem and what numbers to aim
   for.

## Expected Outputs

* ~20 paper assets under `assets/paper/` (each with `details.json`, `summary.md`, and the
  paper file under `files/`).
* One answer asset under `assets/answer/` summarising how existing compartmental DSGC models
  structure the five research questions and what numerical targets they provide.

## Compute and Budget

No external cost. Local LLM CLI only; no paid APIs or remote machines.

## Dependencies

None. This is the first research task.

## Verification Criteria

* At least 20 paper assets pass `verify_paper_asset.py`.
* The answer asset passes `verify_answer_asset.py` and explicitly addresses each of the five
  research questions.
* `compare_literature.md` is not required for a pure literature survey.

</details>
