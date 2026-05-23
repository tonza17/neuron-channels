# Brainstorm Results Session 23

## Trigger

Researcher inspected the t0115 `top50_morphologies_seed9354.png` morphology grid and flagged that in
several panels the soma appears far from the dendrite tree and not visually connected. Concern: if
the soma is genuinely disconnected from the dendrites (rather than a rendering artefact), every 68-d
morphology-extended NSGA-II result from t0091 onwards (t0091, t0099, t0102, t0104, t0106,
t0112-t0115) could be electrically invalid and would need to be re-run.

## Inputs Read

* Aggregator outputs: `aggregate_tasks`, `aggregate_suggestions --uncovered`, `aggregate_costs`.
* Recent task results: `results_summary.md` for t0112, t0113, t0114, t0115, t0116, t0117, t0118 and
  t0114's `compare_literature.md`.
* Generator code: `tasks/t0090_morphology_generator_diversity_test/code/generator.py` (the
  `_apply_asymmetry` transform) and
  `tasks/t0092_diagnose_morphology_generator_silence/code/morphology_generator_fix.py`.
* Synapse-placement code path:
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/trial_helpers.py` (`_section_midpoint_xy`)
  and `trial_driver.py` (`_bar_arrival_times`).
* The t0115 top-50 morphology PNG.

## Decisions

1. **Gating diagnostic** — create `t0120_morph_generator_geometry_audit`. Stratified-sample 15-20
   visually-diverse cells across asymmetry-parameter extremes (high `|soma_offset_pd_um|`, extreme
   `field_elongation_pd`, extreme `branch_density_gradient_pd`, high
   `primary_branch_pd_concentration`) plus symmetric controls. Dump full `section_endpoints_xy`,
   NEURON `h.x3d/h.y3d` pt3d, primary-stem origin verification, parent/child endpoint match check.
   Recompute one synapse-arrival projection per cell to confirm the synapse-vs-soma coordinate frame
   is consistent. Output: 1 answer asset, 1 PNG gallery, 1 CSV with per-cell pass/fail. Cost <$0.10.

2. **Canonical 5-seed substrate-rate report** — create
   `t0121_5seed_substrate_rate_canonical_report` covering S-0115-02. Pure write-up consolidating the
   t0106 / t0112 / t0113 / t0114 / t0115 5-seed batch into one comparable document with harmonised
   metric conventions, 5-seed mean / SD / SE / 95% CI, per-seed acceptance, and the Hay 2011 /
   Druckmann 2007 baselines. Cost <$0.20.

3. **New NSGA-II optimisation** — create `t0122_dsi_cytoplasm_volume_nsga2` covering S-0097-01.
   Bed B + 14-d morphology substrate, 2-objective NSGA-II maximising DSI and minimising cytoplasm
   volume (per-section pi * d * L summed over soma + dendrites + AIS), 1 random GA seed, pop=96,
   N_EVAL_SEEDS=3, HV-plateau auto-stop DISABLED, $8 cap. **Gated on t0120 passing.**

4. **Aggressive suggestion cleanup**:
   * **Reject (9)**: S-0106-01, S-0112-02, S-0112-03, S-0113-02, S-0114-01, S-0114-07, S-0115-01,
     S-0116-01, S-0116-02. (S-0113-02 and S-0114-07 reject reason: deferred to next NSGA-II driver
     iteration. S-0114-01, S-0115-01 reject reason: moot per project's DISABLED-autostop policy.)
   * **Downgrade high -> medium (21)**: S-0067-01, S-0070-01, S-0074-01, S-0074-02, S-0076-04,
     S-0086-01, S-0090-02, S-0090-03, S-0099-01, S-0099-02, S-0102-01, S-0102-02, S-0102-03,
     S-0102-04, S-0104-01, S-0104-02, S-0104-04, S-0105-01, S-0105-02, S-0105-04, S-0106-02.

5. **Framework infra note** — S-0116-06 (`verify_answer_asset.py`) remains active high; needs to
   be picked up by the `self-improvement` skill in a future infra session (not handled in this
   brainstorm per CLAUDE.md rule 0).

## Out of Scope

* No new research, paper downloads, or experiments in this brainstorm task itself.
* Suggestion creation: only the brainstorm-recording suggestions (none planned).
* All cohort-artefact follow-ups (S-0117-01, S-0117-02, S-0117-03, S-0116-03), S-0118-* mechanistic
  follow-ups, and the dill/autostop NSGA-II driver overhaul are deferred to later sessions.
