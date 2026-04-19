# Literature survey: dendritic computation beyond DSGCs

## Motivation

Research question RQ4 (active vs passive dendrites) needs evidence from computational neuroscience
beyond the retinal literature. Cortical and cerebellar dendrites have been studied far more
extensively than DSGC dendrites, and the mechanisms and modelling conventions developed there (NMDA
spikes, Ca/Na plateaus, branch-level nonlinearities) are the natural reference for whether active
dendrites plausibly shape DSGC tuning curves. Source suggestion: S-0014-02 from
t0014_brainstorm_results_3.

## Scope

Target ~25 category-relevant papers covering:

1. NMDA spikes — thresholds, amplitudes, distance-dependence, supralinear integration.
2. Na+ and Ca2+ dendritic spikes — backpropagation, forward propagation, local spikes.
3. Plateau potentials — in-vivo evidence, role in coincidence detection, duration scaling.
4. Branch-level nonlinearities — independent subunits, clustered-vs-distributed input summation.
5. Sublinear-to-supralinear integration regimes — what controls the transition, which conditions
   make dendrites behave passively in practice.
6. Active-vs-passive modelling comparisons — cortical, cerebellar, hippocampal studies that built
   matched active and passive compartmental models and quantified the difference.

Exclusion: do not re-add any DOI already present in the t0002 corpus. Duplicates discovered mid task
must be dropped and the exclusion recorded in the task log.

## Approach

1. Run `/research-internet` targeting each of the six themes above with preference for review
   articles plus 2-4 primary studies per theme.
2. For each shortlisted paper, invoke `/download-paper`. Paywalled papers are recorded as
   `download_status: "failed"` and added to `intervention/paywalled_papers.md` for the researcher to
   retrieve manually.
3. Write one answer asset synthesising which dendritic-computation mechanisms plausibly transfer to
   DSGC dendrites, with explicit caveats about anatomical and biophysical differences.

## Expected Outputs

* ~25 paper assets under `assets/paper/` (v3 spec compliant), some possibly with
  `download_status: "failed"`.
* One answer asset under `assets/answer/` synthesising the six themes and flagging mechanisms most
  plausible for DSGC dendrites.
* `intervention/paywalled_papers.md` listing DOIs requiring manual retrieval.

## Compute and Budget

No paid services required. Task-type budget gate cleared by the $1 bump set in t0014.

## Dependencies

None.

## Verification Criteria

* At least 20 paper assets pass `verify_paper_asset.py`.
* The answer asset passes `verify_answer_asset.py` and explicitly addresses transferability to DSGC
  dendrites.
* No paper in this task's `assets/paper/` shares a DOI with the t0002 corpus.
