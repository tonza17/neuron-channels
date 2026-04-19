# Literature survey: voltage-gated channels in retinal ganglion cells

## Motivation

Research question RQ1 (Na/K combinations) drives the project's main optimisation experiment. Good
priors on which Nav and Kv subunits are expressed in RGCs, their kinetic parameters, and their
conductance densities are needed to constrain the search space before optimisation begins. The t0002
corpus provides DSGC modelling context but does not systematically cover channel-expression or
channel-kinetics literature. Source suggestion: S-0014-05 from t0014_brainstorm_results_3.

## Scope

Target ~25 category-relevant papers covering:

1. Nav subunit expression in RGCs — Nav1.1, Nav1.2, Nav1.6 distributions across soma, AIS,
   dendrite.
2. Kv subunit expression in RGCs — Kv1, Kv2, Kv3, Kv4, BK, SK distributions.
3. HH-family kinetic models — published rate functions, activation/inactivation curves, time
   constants.
4. Subunit co-expression patterns — Nav + Kv combinations reported in specific RGC types.
5. ModelDB MOD-file provenance — which published MOD files implement which Nav/Kv kinetics.
6. Nav/Kv conductance-density estimates — somatic vs AIS vs dendritic densities.

Exclusion: do not re-add any DOI already present in the t0002 corpus. Duplicates discovered mid task
must be dropped and the exclusion recorded in the task log.

## Approach

1. Run `/research-internet` targeting each theme, including explicit ModelDB searches for
   RGC-relevant Nav and Kv MOD files.
2. For each shortlisted paper, invoke `/download-paper`. Paywalled papers are recorded as
   `download_status: "failed"` and added to `intervention/paywalled_papers.md`.
3. Write one answer asset mapping candidate Nav/Kv combinations to published DSGC tuning-curve fits,
   with a row per combination giving the subunits, their densities, and the source paper.

## Expected Outputs

* ~25 paper assets under `assets/paper/` (v3 spec compliant).
* One answer asset under `assets/answer/` mapping Nav/Kv combinations to DSGC tuning-curve fits.
* `intervention/paywalled_papers.md` listing DOIs requiring manual retrieval.

## Compute and Budget

No paid services required. Task-type budget gate cleared by the $1 bump set in t0014.

## Dependencies

None.

## Verification Criteria

* At least 20 paper assets pass `verify_paper_asset.py`.
* The answer asset passes `verify_answer_asset.py` and contains a combination table with at least
  five rows keyed by Nav/Kv subunits and source paper DOI.
* No paper in this task's `assets/paper/` shares a DOI with the t0002 corpus.
