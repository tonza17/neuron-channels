# ⚠️ Tasks: Intervention Blocked

2 tasks. ⚠️ **2 intervention_blocked**.

[Back to all tasks](../README.md)

---

## ⚠️ Intervention Blocked

<details>
<summary>⚠️ 0023 — <strong>Port Hanson 2019 DSGC model</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0023_port_hanson_2019_dsgc` |
| **Status** | intervention_blocked |
| **Effective date** | 2026-04-20 |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Expected assets** | 1 library, 1 paper |
| **Source suggestion** | — |
| **Task types** | [`code-reproduction`](../../../meta/task_types/code-reproduction/) |
| **Task page** | [Port Hanson 2019 DSGC model](../../../overview/tasks/task_pages/t0023_port_hanson_2019_dsgc.md) |
| **Task folder** | [`t0023_port_hanson_2019_dsgc/`](../../../tasks/t0023_port_hanson_2019_dsgc/) |

# Port Hanson 2019 DSGC Model

## Motivation

The project currently has two direction-selective retinal ganglion cell (DSGC) ports, both
derived from the same underlying ModelDB 189347 (Poleg-Polsky & Diamond 2016) codebase. Task
t0008 produced the initial port `modeldb_189347_dsgc` using a spatial-rotation proxy driver
(DSI 0.316, peak 18.1 Hz), and task t0020 produced the sibling port
`modeldb_189347_dsgc_gabamod` using the paper's native gabaMOD scalar swap (DSI 0.7838, peak
14.85 Hz). Both share the same morphology, channel densities, and synaptic topology — so any
channel-mechanism finding drawn from them is a claim about one model, not about DSGCs in
general.

Hanson et al. 2019 published an independent DSGC implementation with distinct channel
densities, morphology detail, and synaptic placement patterns. Task t0010 identified this
model as a high-value alternative. Porting it adds a second, genuinely independent NEURON DSGC
that supports cross-model comparison of direction-selectivity mechanisms, channel
sensitivities, and dendritic computation patterns — the pattern of agreement (or disagreement)
between the two models is what makes any downstream claim robust.

## Scope

Port the Hanson et al. 2019 DSGC model into NEURON as a new library asset sibling to
`modeldb_189347_dsgc`. Reproduce the model's published direction-selective response under a
12-angle moving-bar sweep, reusing task t0022's driver infrastructure if compatible (soft
dependency) or copying from t0020 otherwise. Produce a tuning curve and score report directly
comparable to the existing ports.

## Deferred Status

This task is deferred. It is reserved and planned but must NOT be executed by the execute-task
loop until a human decision is made after reviewing t0022's outcomes. Upon creation, the
orchestrator will add an intervention file that blocks execute-task. The `status` field
remains `not_started`; the intervention file, not the status, is what suspends execution.

## Deliverables

1. New library asset (proposed slug `hanson_2019_dsgc`) containing the model's
   HOC/MOD/morphology files, `details.json`, and `description.md`, following the same layout
   as `modeldb_189347_dsgc`.
2. Source paper (Hanson et al. 2019) downloaded and registered as a paper asset, if not
   already present in the project.
3. A 12-angle moving-bar tuning curve producing `tuning_curves.csv` and `score_report.json`,
   using t0022's driver if compatible or a port of t0020's driver otherwise.
4. Comparison section in `results/results_detailed.md` reporting DSI, peak firing rate, HWHM,
   and reliability against t0008, t0020, and t0022.

## Dependencies

* `t0008_port_modeldb_189347` — reference HOC/MOD/asset layout for a NEURON DSGC library port.
* `t0012_tuning_curve_scoring_loss_library` — tuning-curve scorer applied to the new model.
* `t0022_modify_dsgc_channel_testbed` — soft dependency providing the 12-angle driver
  infrastructure; reuse if available, otherwise fall back to t0020's driver.

## Risks and Unknowns

* Simulator mismatch: Hanson et al. 2019 may use NEST, Brian, custom Python, or another
  simulator instead of NEURON. A non-NEURON source increases effort from roughly 1-2 days to
  up to a week.
* Morphology provenance: the model's morphology may come from NeuroMorpho.Org or another
  external repository and may require a separate retrieval step before porting can proceed.
* Channel mechanisms: the paper may rely on ion-channel MOD mechanisms not currently present
  in this project, requiring new `.mod` files and compilation into the existing mechanism set.

## Out of Scope

No analyses beyond the basic 12-angle tuning curve and score report. Channel-sensitivity
sweeps, parameter-space exploration, dendritic-computation decomposition,
optogenetic/pharmacological perturbation studies, or other downstream analyses belong to
follow-up tasks and must not be performed here.

</details>

<details>
<summary>⚠️ 0024 — <strong>Port de Rosenroll 2026 DSGC model</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0024_port_de_rosenroll_2026_dsgc` |
| **Status** | intervention_blocked |
| **Effective date** | 2026-04-20 |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Expected assets** | 1 library, 1 paper |
| **Source suggestion** | — |
| **Task types** | [`code-reproduction`](../../../meta/task_types/code-reproduction/) |
| **Task page** | [Port de Rosenroll 2026 DSGC model](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md) |
| **Task folder** | [`t0024_port_de_rosenroll_2026_dsgc/`](../../../tasks/t0024_port_de_rosenroll_2026_dsgc/) |

# Port de Rosenroll 2026 DSGC Model

## Motivation

The project currently has DSGC compartmental model ports derived from a single lineage: t0008
and t0020 both port ModelDB 189347 (Poleg-Polsky & Diamond 2016), and t0022 modifies that same
port for dendritic-computation DS. A sibling port of Hanson et al. 2019 is reserved in t0023.
Adding de Rosenroll et al. 2026 as an independent third implementation provides a third
structurally independent comparison point and, because the paper is recent, is the port most
likely to incorporate modern methodology and channel mechanisms. In particular, it may include
an explicit Nav1.6 / Nav1.2 split at the axon initial segment consistent with the patch-clamp
priors reviewed in t0017, and may use more recent Kv and Cav formulations than the older
Poleg-Polsky and Hanson models. This makes it especially relevant to the project's
channel-testbed goal of evaluating how specific channel combinations shape direction
selectivity.

## Scope

Port the de Rosenroll et al. 2026 DSGC model into the project as a new library asset (proposed
slug `de_rosenroll_2026_dsgc`) following the HOC/MOD/morphology layout established by t0008.
Fetch the paper as a paper asset if it is not already present. Run the standard 12-angle
moving-bar tuning-curve protocol using the driver infrastructure from t0022 where compatible,
producing `tuning_curves.csv` and a `score_report.json` against the target tuning curve from
t0004. Compare results against the Poleg-Polsky lineage (t0008, t0020, t0022) and the Hanson
port (t0023) in `results_detailed.md`.

## Deferred Status

This task is deferred. It is created and reserved now but must NOT be executed by the
execute-task loop until t0022 completes and the researcher explicitly reviews its outcomes.
After task-folder creation the orchestrator will write an intervention file to block
execution. The decision to proceed depends on what t0022 reveals about the channel-testbed
framework and whether a third independent implementation adds value.

## Deliverables

* New library asset `de_rosenroll_2026_dsgc` with HOC, MOD, and morphology files,
  `details.json`, and `description.md`.
* Source paper downloaded and registered as a paper asset if not already in the corpus.
* 12-angle moving-bar tuning curve: `tuning_curves.csv` and `score_report.json`.
* Cross-model comparison in `results_detailed.md` against t0008, t0020, t0022, and t0023.

## Dependencies

* `t0008_port_modeldb_189347` — reference HOC/MOD library-asset skeleton.
* `t0012_tuning_curve_scoring_loss_library` — scorer used for `score_report.json`.
* `t0022_modify_dsgc_channel_testbed` — driver infrastructure (soft dependency; reuse if
  compatible, otherwise adapt).

## Risks and Unknowns

* The 2026 paper may have restricted full-text access or be paywalled at porting time,
  limiting methodological detail.
* Original source code may not be publicly released or may not target NEURON, forcing partial
  reimplementation from the paper.
* Morphology may live in a different repository with different conventions.
* The model may rely on MOD mechanisms (Nav1.6, Nav1.2, modern Kv1, updated Cav) not yet in
  the project's MOD set, requiring new mechanism files and validation.
* Rough effort estimate: 1-2 days if source is NEURON and openly available; 3-5 days if
  partial reimplementation is needed.

## Out of Scope

* Parameter fitting or channel-density sweeps on the ported model (future task).
* Cross-simulator porting (e.g., NetPyNE, Brian) beyond the NEURON target.
* Re-running t0022's channel-testbed modifications on this model (future task if justified by
  t0022 outcomes).
* Executing this task now — execution is blocked pending t0022 review.

</details>
