# Brainstorm session 3 — Summary

## Outcome

Planned a five-task literature-survey wave (t0015-t0019) to broaden the project's paper corpus
beyond the DSGC-specific modelling focus of t0002. Authorised a $1 budget bump so
`literature-survey` tasks clear the project budget gate without incurring real spend. Confirmed a
paywalled-paper workflow where each survey emits an `intervention/paywalled_papers.md` file the
researcher resolves from their institutional account.

## Decisions

* **Five surveys, one per under-saturated category**: cable-theory, dendritic-computation,
  patch-clamp, synaptic-integration, voltage-gated-channels. Dropped `direction-selectivity`,
  `compartmental-modeling`, and `retinal-ganglion-cell` because t0002 plus t0010 already saturate
  them.
* **Target ~25 category-relevant papers per task** (not 20). Extra headroom compensates for the
  deduplication constraint and for papers that ultimately fail quality filters.
* **Exclude the 20 DOIs already in the t0002 corpus** from each survey. Duplicate hits must be
  dropped and recorded in the task log.
* **Budget bumped from $0 to $1** — nominal, only to clear the `has_external_costs: true` gate on
  `literature-survey`; no paid service is expected to bill.
* **Paywalled papers**: each survey task writes `intervention/paywalled_papers.md` with DOIs; the
  researcher downloads manually from their institutional account; a follow-up pass upgrades
  `download_status` from `"failed"` to `"success"` for each file retrieved.

## Outputs

* Five suggestions (S-0014-01 to S-0014-05) recorded in `results/suggestions.json`, one per
  surviving category.
* Five not-started child tasks created: `t0015_literature_survey_cable_theory`,
  `t0016_literature_survey_dendritic_computation`, `t0017_literature_survey_patch_clamp`,
  `t0018_literature_survey_synaptic_integration`, `t0019_literature_survey_voltage_gated_channels`.
* `project/budget.json` `total_budget` bumped from 0.0 to 1.0 USD.

## Next Steps

Execute t0015-t0019 in parallel (up to three worktrees concurrent). After execution, a follow-up
correction task resolves any paywalled-paper failures using manually retrieved PDFs from the
researcher.
