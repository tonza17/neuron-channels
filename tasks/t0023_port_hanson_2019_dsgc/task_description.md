# Port Hanson 2019 DSGC Model

## Motivation

The project currently has two direction-selective retinal ganglion cell (DSGC) ports, both derived
from the same underlying ModelDB 189347 (Poleg-Polsky & Diamond 2016) codebase. Task t0008 produced
the initial port `modeldb_189347_dsgc` using a spatial-rotation proxy driver (DSI 0.316, peak 18.1
Hz), and task t0020 produced the sibling port `modeldb_189347_dsgc_gabamod` using the paper's native
gabaMOD scalar swap (DSI 0.7838, peak 14.85 Hz). Both share the same morphology, channel densities,
and synaptic topology — so any channel-mechanism finding drawn from them is a claim about one
model, not about DSGCs in general.

Hanson et al. 2019 published an independent DSGC implementation with distinct channel densities,
morphology detail, and synaptic placement patterns. Task t0010 identified this model as a high-value
alternative. Porting it adds a second, genuinely independent NEURON DSGC that supports cross-model
comparison of direction-selectivity mechanisms, channel sensitivities, and dendritic computation
patterns — the pattern of agreement (or disagreement) between the two models is what makes any
downstream claim robust.

## Scope

Port the Hanson et al. 2019 DSGC model into NEURON as a new library asset sibling to
`modeldb_189347_dsgc`. Reproduce the model's published direction-selective response under a 12-angle
moving-bar sweep, reusing task t0022's driver infrastructure if compatible (soft dependency) or
copying from t0020 otherwise. Produce a tuning curve and score report directly comparable to the
existing ports.

## Deferred Status

This task is deferred. It is reserved and planned but must NOT be executed by the execute-task loop
until a human decision is made after reviewing t0022's outcomes. Upon creation, the orchestrator
will add an intervention file that blocks execute-task. The `status` field remains `not_started`;
the intervention file, not the status, is what suspends execution.

## Deliverables

1. New library asset (proposed slug `hanson_2019_dsgc`) containing the model's HOC/MOD/morphology
   files, `details.json`, and `description.md`, following the same layout as `modeldb_189347_dsgc`.
2. Source paper (Hanson et al. 2019) downloaded and registered as a paper asset, if not already
   present in the project.
3. A 12-angle moving-bar tuning curve producing `tuning_curves.csv` and `score_report.json`, using
   t0022's driver if compatible or a port of t0020's driver otherwise.
4. Comparison section in `results/results_detailed.md` reporting DSI, peak firing rate, HWHM, and
   reliability against t0008, t0020, and t0022.

## Dependencies

* `t0008_port_modeldb_189347` — reference HOC/MOD/asset layout for a NEURON DSGC library port.
* `t0012_tuning_curve_scoring_loss_library` — tuning-curve scorer applied to the new model.
* `t0022_modify_dsgc_channel_testbed` — soft dependency providing the 12-angle driver
  infrastructure; reuse if available, otherwise fall back to t0020's driver.

## Risks and Unknowns

* Simulator mismatch: Hanson et al. 2019 may use NEST, Brian, custom Python, or another simulator
  instead of NEURON. A non-NEURON source increases effort from roughly 1-2 days to up to a week.
* Morphology provenance: the model's morphology may come from NeuroMorpho.Org or another external
  repository and may require a separate retrieval step before porting can proceed.
* Channel mechanisms: the paper may rely on ion-channel MOD mechanisms not currently present in this
  project, requiring new `.mod` files and compilation into the existing mechanism set.

## Out of Scope

No analyses beyond the basic 12-angle tuning curve and score report. Channel-sensitivity sweeps,
parameter-space exploration, dendritic-computation decomposition, optogenetic/pharmacological
perturbation studies, or other downstream analyses belong to follow-up tasks and must not be
performed here.
