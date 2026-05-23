# Brainstorm Session 23 — Full Transcript

## Project State Presented

* **Budget**: $62.90 / $100 spent (62.9%); $37.10 remaining; no thresholds reached. 3 tasks over the
  $8 per-task default: t0083, t0102, t0106.
* **Completed since t0111** (the 5-seed substrate + cohort-artefact wave): 7 tasks.
  * t0112 seed-77 replicate: 7 LEGIT joint-pass, partial replication; cadence-10 cut wall-clock
    3.5x.
  * t0113 seed-2247 replicate: 0 LEGIT joint-pass; HV-plateau detector fired gen 14 (premature).
  * t0114 seed-7755 (autostop OFF): 484 LEGIT joint-pass; ran to gen 62; confirmed t0113 stop was
    premature; offline replay recommends (W=3, T=0.015).
  * t0115 seed-9354 (autostop OFF): 63 LEGIT joint-pass; closes the 5-seed S-0112-01 batch.
  * t0116 4-seed pooled FA (DSI>0.7 AND PD>10, 869 cells): NMI(cluster,seed) = 0.929 ephys / 0.889
    morph; no joint factor.
  * t0117 4-seed pooled FA (unfiltered, 4431 cells): F1 IS a joint DSI-PD factor (r=+0.42, +0.35);
    NMI dropped to 0.562/0.313. **Truncated-cohort artefact confirmed** -- t0116 headlines were
    strict-cohort artefacts.
  * t0118 re-sim 40 cells (10/cluster): g_I/g_E spans 6 orders of magnitude; only cluster 2 (s7755)
    shows DSGC-like asymmetry traces; **cell 77_15_1356 evaluator-disagreement bug found**: t0117
    DSI=0.93 but 0 spikes under canonical 1400 ms / -10 mV protocol.
* **5-seed substrate-rate result (S-0112-01 batch complete)**:
  * Per-seed LEGIT acceptance: 44=3.23%, 77=0.35%, 2247=0.00%, 7755=8.13%, 9354=1.19%
  * Mean 2.58% +/- SE 1.50%, 95% CI (-0.36%, +5.52%)
  * Point estimate 6.5x above Hay 2011 (0.40%), 25.8x above Druckmann 2007 (0.10%); 3 of 5 seeds
    individually beat Hay envelope.
* **Suggestions backlog**: 372 active uncovered (51 high, 261 medium, 60 low); up from 325 at t0111.
  20 new high-priority added by the t0112-t0118 wave.

## Independent Priority Reassessment

* **Promote to top of queue** (cheap, addresses correctness or unanswered headlines): S-0118-03
  (evaluator bug), S-0117-01 (DSI bracketed sweep), S-0117-02 (per-seed FA), S-0117-03 (bootstrap
  F1), S-0116-03 (topological basin test), S-0118-02 (g_I sweep).
* **Reject as superseded**: S-0114-01 + S-0115-01 (HV-plateau tuning -- moot per DISABLED-autostop
  policy), S-0113-02 + S-0114-07 (dill checkpoint -- deferred to next NSGA-II driver iteration),
  S-0112-02, S-0112-03 (superseded by t0114/t0115), S-0116-01 (5-seed pool adding t0113 --
  superseded by t0117), S-0116-02 (relaxed cohort -- subsumed by S-0117-01), S-0106-01 (multi-seed
  confirmation done by 5-seed batch).
* **Downgrade pre-t0111 stale highs**: S-0067-01, S-0070-01, S-0074-01, S-0074-02, S-0076-04,
  S-0086-01, S-0090-02, S-0090-03, S-0099-01, S-0099-02, S-0102-01, S-0102-02, S-0102-03, S-0102-04,
  S-0104-01, S-0104-02, S-0104-04, S-0105-01, S-0105-02, S-0105-04, S-0106-02.
* **Infra (no tXXXX folder per CLAUDE.md rule 0)**: S-0116-06 (`verify_answer_asset.py`) -- record
  as note for next self-improvement skill invocation.

## Clarification Questions

The AI offered a 4-question questionnaire (researcher notes, focus area, backlog pruning, budget
envelope). The researcher interrupted with a more pressing question about morphology rendering.

## Diversion: Morphology Generator Geometry Concern

**Researcher**: "I do not understand the morphology. Why is some som much further away from the
dendrites and not connected? Is it a bug of the presentation of actually constructing of the cell
morphology? This is important as it may lead us to necessity to redo all the optimisations we did so
far."

**AI investigation**:

1. Read `tasks/t0090_morphology_generator_diversity_test/code/generator.py` end-to-end. Key
   findings:
   * `_apply_asymmetry` (lines 333-355): moves the soma to `(soma_offset_pd_um, 0)`. For each
     dendrite node it adds `soma_offset` then stretches along x:
     `sx = soma_offset + elong * (sx - soma_offset)`.
   * For a primary stem with pre-asymmetry `start_xy=(0,0)`: after offset `sx=soma_offset`, after
     stretch `sx_dx=0` so `sx=soma_offset`. Primary stem starts at the same `(soma_offset, 0)` as
     the moved soma. Topology consistent.
   * For non-primary dendrites: `start_xy = parent.end_xy` pre-asymmetry; after the same transform
     applied to both, they continue to share endpoints.
   * NEURON sections joined via `sec.connect(parent, 1.0, 0.0)` -- the electrical topology does NOT
     depend on xy coordinates at all.
2. Read `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/trial_helpers.py`
   `_section_midpoint_xy` and `trial_driver.py` `_bar_arrival_times`. Confirmed:
   * Synapse xy comes from `h.x3d(mid), h.y3d(mid)` -- the same `pt3dadd` calls in
     `_materialise_neuron_sections` that the rendering reads.
   * Bar arrival time projects `(syn_xy - origin_xy)` onto the bar direction. Both `syn_xy` and
     `origin_xy` are in the same post-asymmetry coordinate frame by construction.
3. Inspected `top50_morphologies_seed9354.png` from t0115:
   * Many panels show a small soma dot in a corner with the dendrite tree appearing offset.
   * Auto-zoomed bounding box covers both, leaving apparent empty space between.
   * The thin connecting primary stem (drawn at line-width 0.4) is visually lost at this scale.

**AI preliminary verdict**: most likely a rendering / visual interpretation issue -- soma circle is
small (6 um radius), primary stem is thin (0.4 px), and auto-zoom on extreme-asymmetry cells
exaggerates the visual gap. Electrical simulation is `sec.connect()`-based and indifferent to xy.
Synapse arrival timing uses consistent `(syn_xy, origin_xy)` pairs in the same frame.

**But**: this needs a focused diagnostic before we can rule out a real bug. If `_apply_asymmetry`
has an off-by-one or operator-order subtlety, synapse arrival timing could be wrong for cells with
large `soma_offset_pd_um` or extreme `field_elongation_pd`.

**AI proposed gating task**: `t0119_morph_generator_geometry_audit` -- 5 cells stratified across
asymmetry-parameter extremes, dump generator coords, verify primary stems start at `origin_xy` and
that synapse pt3d xy is in the same frame as `origin_xy`. <$0.10.

**Researcher**: "Mke it a task but select more suspicious cells, not just 5. Say 15-20 differently
looking cells."

**AI**: Confirmed scope expansion to 15-20 cells stratified across the asymmetry parameter axes plus
symmetric controls, with output as 1 answer asset, 1 PNG gallery, 1 CSV with per-cell pass/fail.
Cost still <$0.10.

## Discussion -- Round 1: New Tasks

**AI**: Re-asked questions accounting for the morphology diversion: if-pass branch direction,
pruning aggressiveness, infra bundle structure.

**Researcher (answered Q1 + Q2, deferred Q3)**:
* Q1 (if-pass branch): "Skip follow-ups, pivot to new NSGA-II objective".
* Q2 (pruning): "Aggressive -- reject/downgrade clearly superseded items now".

**Researcher**: "We have decided what you are going to do - check that morphology is correct and if
so proceed with other optimiosation tasks."

**AI**: Proposed final wave structure:

1. `t0119_morph_generator_geometry_audit` -- gating diagnostic, <$0.10.
2. `t0120_5seed_substrate_rate_canonical_report` -- write-up, <$0.20.
3. `t0121_dsi_cytoplasm_volume_nsga2` -- new NSGA-II run, ~$4-8, gated on t0120 (later renumbered to
   t0120 -> geometry audit, t0121 -> 5-seed report, t0122 -> cytoplasm-volume NSGA-II to preserve
   the brainstorm-task task-index ordering invariant).

Asked for selection of NSGA-II objective and 5-seed-report inclusion.

**Researcher**: Selected S-0097-01 (DSI vs cytoplasm volume, ~$4-8); Yes to S-0115-02 5-seed
substrate-rate canonical report.

## Discussion -- Round 2: Suggestion Cleanup

**AI proposal**:
* **Reject 8 suggestions**:
  * S-0106-01 -- done by 5-seed batch
  * S-0112-02 (cadence isolation) -- superseded by t0114/t0115
  * S-0112-03 (autostop sensitivity) -- superseded by t0114
  * S-0113-02 + S-0114-07 (dill checkpoint) -- deferred to next NSGA-II driver iteration
  * S-0114-01 + S-0115-01 (W=3/T=0.015 plateau defaults) -- moot per DISABLED-autostop policy
  * S-0116-01 (5-seed pool adding t0113) -- superseded by t0117 unfiltered
  * S-0116-02 (DSI>0.5 cohort) -- subsumed by S-0117-01 sweep
* **Downgrade high -> medium (21 suggestions)**: S-0067-01, S-0070-01, S-0074-01, S-0074-02,
  S-0076-04, S-0086-01, S-0090-02, S-0090-03, S-0099-01, S-0099-02, S-0102-01, S-0102-02, S-0102-03,
  S-0102-04, S-0104-01, S-0104-02, S-0104-04, S-0105-01, S-0105-02, S-0105-04, S-0106-02.
* **Keep at high** (12): S-0091-01, S-0091-02, S-0101-01, S-0103-01, S-0103-02, S-0103-03,
  S-0116-03, S-0116-06, S-0117-01, S-0117-02, S-0117-03, S-0118-01, S-0118-02, S-0118-03.

## Discussion -- Round 3: Confirmation

**AI summary**:
* New tasks: t0120 morph_generator_geometry_audit, t0121 5seed_substrate_rate_canonical_report,
  t0122 dsi_cytoplasm_volume_nsga2 (gated on t0120).
* Suggestions rejected: 8.
* Suggestions downgraded: 21.
* Suggestions kept high: 12.
* Budget envelope: ~$5-9 of $37 remaining.

**Researcher**: "confirm"

## Decisions Summary

1. Create `t0120_morph_generator_geometry_audit` -- gating diagnostic, no dependencies, <$0.10.
2. Create `t0121_5seed_substrate_rate_canonical_report` -- covers S-0115-02, depends on t0106 +
   t0112-t0115, <$0.20.
3. Create `t0122_dsi_cytoplasm_volume_nsga2` -- covers S-0097-01, depends on t0120, ~$4-8 ($8 cap),
   one Vast.ai EPYC NSGA-II run.
4. Reject 8 suggestions via correction files (with per-suggestion rationale).
5. Downgrade 21 high-priority suggestions to medium via correction files (with per-suggestion
   rationale).
6. Note in session log: S-0116-06 (`verify_answer_asset.py`) is framework infra; needs to be picked
   up by the `self-improvement` skill in a future session per CLAUDE.md rule 0.
