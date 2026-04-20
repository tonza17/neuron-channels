# ⏳ Tasks: In Progress

1 tasks. ⏳ **1 in_progress**.

[Back to all tasks](../README.md)

---

## ⏳ In Progress

<details>
<summary>⏳ 0010 — <strong>Hunt DSGC compartmental models missed by prior survey;
port runnable ones</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0010_hunt_missed_dsgc_models` |
| **Status** | in_progress |
| **Effective date** | 2026-04-20 |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md) |
| **Expected assets** | 1 answer |
| **Source suggestion** | — |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/), [`download-paper`](../../../meta/task_types/download-paper/), [`code-reproduction`](../../../meta/task_types/code-reproduction/) |
| **Start time** | 2026-04-20T12:25:27Z |
| **Task page** | [Hunt DSGC compartmental models missed by prior survey; port runnable ones](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md) |
| **Task folder** | [`t0010_hunt_missed_dsgc_models/`](../../../tasks/t0010_hunt_missed_dsgc_models/) |

# Hunt DSGC compartmental models missed by t0002 and t0008; port any with code

## Motivation

The t0002 literature survey built a 20-paper corpus biased toward the six seed references from
`project/description.md` and adjacent DSGC papers. The t0008 ModelDB port focussed on entry
189347 (Poleg-Polsky & Diamond 2016) and its immediate siblings. Neither task exhaustively
searched post-2020 publications, non-ModelDB repositories (GitHub / OSF / Zenodo /
institutional pages), or adjacent computational neuroscience venues (NeurIPS, Cosyne, bioRxiv)
for DSGC compartmental models. This task closes that gap: actively hunt for DSGC compartmental
models the project might have missed, download their papers, and port any models that have
runnable code and are scientifically relevant.

## Scope

1. **Systematic search** across:
   * ModelDB full listing under keywords `direction selective`, `retina`, `DSGC`, `RGC`,
     `Starburst`, `SAC` (broader than the t0008 sweep).
   * GitHub search: `DSGC`, `retinal ganglion direction`, `NetPyNE direction`, `Arbor retina`,
     `NEURON DSGC`.
   * Google Scholar + Semantic Scholar forward-citation chains of:
     * Poleg-Polsky & Diamond 2016
     * Schachter et al. 2010
     * Park et al. 2014
     * Sethuramanujam et al. 2016
     * Hanson et al. 2019
   * bioRxiv + preprint servers, 2023-2025, keyword `direction-selective ganglion cell`.
2. **Download** any paper not already in `assets/paper/` that meets the inclusion bar:
   publishes a compartmental (not rate-coded / not purely statistical) DSGC model with at
   least partial biophysical detail.
3. **Port** any paper with public code that:
   * Runs in Python 3.12 + NEURON 8.2.7 (or Arbor 0.12.0).
   * Can load `dsgc-baseline-morphology-calibrated` or bring its own morphology.
   * Produces an angle-resolved tuning curve.
4. **Report** every candidate in a single answer asset with a per-model row: paper DOI, code
   URL, NEURON compatibility, whether ported, and if not, why not.

## Dependencies

* **t0008_port_modeldb_189347** — gives us a working NEURON-based reference implementation to
  contrast with any newly ported model and a pattern for how to port additional models.

## Expected Outputs

* **1 answer asset** (`assets/answer/missed-dsgc-models-hunt-report/`) summarising every
  candidate found and the outcome of each port attempt.
* **N paper assets** for any new papers (DOI-keyed, v3-spec-compliant). Exact count depends on
  what the search turns up.
* **0 or more library assets** for any successfully ported models
  (`assets/library/<model-slug>/`). Exact count depends on what was portable.
* **Simulated tuning-curve CSVs** under `data/tuning_curves/` for every ported model,
  formatted identically to the t0008 outputs so t0011 can render them side-by-side.

## Approach

Run the search in three passes (ModelDB full sweep, GitHub + OSF + Zenodo, Google Scholar
forward citations). Maintain a single `data/candidates.csv` that grows across passes and
records duplicate-vs-new status against t0002's corpus. Decide portability by actually cloning
the repo and running the demo, not by reading the README; record every port attempt's
stdout/stderr under `logs/` so reviewers can audit the call.

## Questions the task answers

1. Which DSGC compartmental models exist in the literature or in public code that the t0002
   survey and the t0008 ModelDB port missed?
2. Of those, which have runnable public code in this environment?
3. How does each successfully ported model's tuning curve compare with the t0008 Poleg-Polsky
   reproduction and with the canonical `target-tuning-curve`?
4. Are there consistent disagreements across ports (e.g., systematically narrower HWHM, higher
   null firing) that warrant new experiment suggestions?

## Risks and Fallbacks

* **Search finds no new portable models**: document the gap as a new suggestion; the answer
  asset's table should still be produced listing every candidate considered and why each was
  excluded.
* **Port attempts consistently fail**: surface that as a finding — published DSGC
  compartmental code is often fragile — rather than inventing fixes that change the original
  model's behaviour.
* **Search produces too many candidates to port within this task**: triage by (a) citation
  count, (b) publication year (newer first), (c) whether the code is in a simulator already on
  this workstation. Port the top 3-5 and list the rest as suggestions.

</details>
