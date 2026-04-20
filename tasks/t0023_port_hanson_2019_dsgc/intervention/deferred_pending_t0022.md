# Intervention: Task Deferred Pending t0022 Outcomes

## Status

This task is **intervention_blocked** by researcher decision during brainstorm session 4
(t0021_brainstorm_results_4, 2026-04-20).

## Reason

The researcher wants a DSGC channel-testbed model before committing effort to a second independent
port. Task t0022_modify_dsgc_channel_testbed is the active build of that testbed, modifying the
existing modeldb_189347_dsgc library asset for dendritic-computation direction selectivity over a
12-angle moving-bar sweep.

Hanson et al. 2019 is a valuable comparison implementation, but the effort required to port a second
DSGC model is only justified once t0022 establishes whether the modify-existing approach is
sufficient for the project's channel-mechanism-testing goals. If t0022 succeeds, this port remains
worthwhile as an independent implementation but becomes lower priority. If t0022 fails or reveals
fundamental limitations in the Poleg-Polsky base model, this port becomes critical path.

## How to resolve

The researcher must explicitly unblock this task before execution. To unblock:

1. Review t0022 results in `tasks/t0022_modify_dsgc_channel_testbed/results/results_summary.md`.
2. Decide whether to proceed with this port, cancel, or defer further.
3. If proceeding: delete this intervention file and change `status` in `task.json` from
   `intervention_blocked` to `not_started`.
4. If cancelling: change `status` to `cancelled` and leave this file for audit trail.

## Context

* Source: brainstorm session 4 (t0021)
* Dependency on t0022: the 12-angle driver infrastructure from t0022 should be reusable here; soft
  dependency
* Active sibling task: t0022_modify_dsgc_channel_testbed
* Related deferred task: t0024_port_de_rosenroll_2026_dsgc (same intervention pattern)
