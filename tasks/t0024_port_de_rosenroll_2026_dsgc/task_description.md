# Port de Rosenroll 2026 DSGC Model

## Motivation

The project currently has DSGC compartmental model ports derived from a single lineage: t0008 and
t0020 both port ModelDB 189347 (Poleg-Polsky & Diamond 2016), and t0022 modifies that same port for
dendritic-computation DS. A sibling port of Hanson et al. 2019 is reserved in t0023. Adding de
Rosenroll et al. 2026 as an independent third implementation provides a third structurally
independent comparison point and, because the paper is recent, is the port most likely to
incorporate modern methodology and channel mechanisms. In particular, it may include an explicit
Nav1.6 / Nav1.2 split at the axon initial segment consistent with the patch-clamp priors reviewed in
t0017, and may use more recent Kv and Cav formulations than the older Poleg-Polsky and Hanson
models. This makes it especially relevant to the project's channel-testbed goal of evaluating how
specific channel combinations shape direction selectivity.

## Scope

Port the de Rosenroll et al. 2026 DSGC model into the project as a new library asset (proposed slug
`de_rosenroll_2026_dsgc`) following the HOC/MOD/morphology layout established by t0008. Fetch the
paper as a paper asset if it is not already present. Run the standard 12-angle moving-bar
tuning-curve protocol using the driver infrastructure from t0022 where compatible, producing
`tuning_curves.csv` and a `score_report.json` against the target tuning curve from t0004. Compare
results against the Poleg-Polsky lineage (t0008, t0020, t0022) and the Hanson port (t0023) in
`results_detailed.md`.

## Deferred Status

This task is deferred. It is created and reserved now but must NOT be executed by the execute-task
loop until t0022 completes and the researcher explicitly reviews its outcomes. After task-folder
creation the orchestrator will write an intervention file to block execution. The decision to
proceed depends on what t0022 reveals about the channel-testbed framework and whether a third
independent implementation adds value.

## Deliverables

* New library asset `de_rosenroll_2026_dsgc` with HOC, MOD, and morphology files, `details.json`,
  and `description.md`.
* Source paper downloaded and registered as a paper asset if not already in the corpus.
* 12-angle moving-bar tuning curve: `tuning_curves.csv` and `score_report.json`.
* Cross-model comparison in `results_detailed.md` against t0008, t0020, t0022, and t0023.

## Dependencies

* `t0008_port_modeldb_189347` — reference HOC/MOD library-asset skeleton.
* `t0012_tuning_curve_scoring_loss_library` — scorer used for `score_report.json`.
* `t0022_modify_dsgc_channel_testbed` — driver infrastructure (soft dependency; reuse if
  compatible, otherwise adapt).

## Risks and Unknowns

* The 2026 paper may have restricted full-text access or be paywalled at porting time, limiting
  methodological detail.
* Original source code may not be publicly released or may not target NEURON, forcing partial
  reimplementation from the paper.
* Morphology may live in a different repository with different conventions.
* The model may rely on MOD mechanisms (Nav1.6, Nav1.2, modern Kv1, updated Cav) not yet in the
  project's MOD set, requiring new mechanism files and validation.
* Rough effort estimate: 1-2 days if source is NEURON and openly available; 3-5 days if partial
  reimplementation is needed.

## Out of Scope

* Parameter fitting or channel-density sweeps on the ported model (future task).
* Cross-simulator porting (e.g., NetPyNE, Brian) beyond the NEURON target.
* Re-running t0022's channel-testbed modifications on this model (future task if justified by t0022
  outcomes).
* Executing this task now — execution is blocked pending t0022 review.
