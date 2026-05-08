# Brainstorm Session 19 — Full Transcript

## Project State Presented

* 93 tasks total; all completed except t0091 (`not_started`).
* Last brainstorm: t0089 (session 18, 2026-05-07) — committed the morphology-extension pivot.
* Tasks completed since t0089:
  * **t0090** procedural DSGC morphology generator + diversity test — 9/60 STABLE due to
    soma-`pt3dadd` collapse bug.
  * **t0092** diagnose t0090 silence — root cause = soma `pt3dadd` collapse making soma area
    ~9.4e-14 um^2 instead of 287 um^2. Fix `generate_fixed_morphology` shim. 5/5 STABLE-from-t0090
    cells fire post-fix.
  * **t0093** patched-generator full re-sweep + correction overlay — 60/60 STABLE-firing post-fix
    (51 NAN→firing, 9 silent→firing, 0 regressions); 56/60 with PD-rate>0; mean DSI 0.32
    (different) / 0.35 (similar); 21/60 with DSI>0.5; 3/60 with DSI=1.0; correction overlay
    `C-0093-01` against t0090 generator committed and verified.
* Budget: $20.00 total, $15.55 spent (77.7%), **$4.45 remaining**; t0083 over its $5 limit.
* Pending tasks: t0091 (`morphology_extended_nsga2_v1`) only — first joint 68-d NSGA-II, estimated
  $3.00–3.50 / 14–16 h on Vast.ai. Currently broken: dependencies + import paths point at the
  unpatched t0090 generator.
* 12 active high-priority suggestions; AI's reassessment flagged S-0092-03 (already done in t0093)
  and S-0090-04 (premise invalidated by 60/60 STABLE post-fix) as reject candidates.

## Clarification Questions

(Asked but pre-empted by researcher's substantive question; brainstorm proceeded with the
researcher's questions instead of formal multi-choice clarification at this stage.)

## Discussion — Round 1: Researcher Questions

### Q1: Explain the bug + fix + validation + DSI spread

Researcher: "Explain me in simple words what was the bug with new morphologies generation and how
you fixed it? How do we know that everything is fine? Also, did all morphologies showed toughly the
same DSI or did they differ?"

AI: Plain-language explanation:

* **Bug**: each cell's soma in NEURON is built from a list of 3D anchor points connected by
  cylinders. The generator emitted both soma anchor points at `(0, 0, 0)` (coincident). NEURON
  computed the soma's length as ~0 and collapsed surface area to ~9e-14 um^2 (vs ~287 um^2
  expected). Synaptic current divided by near-zero area produced astronomical voltage steps -> NaN
  within first few simulation steps. Result: 51/60 NAN_VOLTAGE crashes, 9/60 silent stable.

* **Fix**: thin wrapper `generate_fixed_morphology` that re-emits the second soma anchor along the
  z-axis at distance `soma_diameter_um` from the first. Soma now has proper non-zero length and ~287
  um^2 area. Single-line bug, mechanical fix, applies identically to every cell.

* **Validation evidence (3 layers)**:
  1. Unit tests: 4/4 pass; soma area post-fix matches hand-coded reference within 5%.
  2. Pipeline gate: known-good hand-coded Bed B cell run through same pipeline + t0083 channels
     fired 41 spikes — proves the pipeline is healthy and bug was localised to the generator.
  3. Full re-sweep at scale (t0093):
     * 60/60 STABLE (vs 0/60 pre-fix)
     * 60/60 firing at some direction (vs 0/60 pre-fix)
     * 0 regressions
     * 51 cells NAN_VOLTAGE → STABLE-firing
     * 9 cells STABLE-silent → STABLE-firing
     * 16,107 total spikes vs 0 pre-fix
     * Pass criterion (≥50/60 with PD-rate>0) met at 56/60; stretch (≥55/60) also met
     * All verifiers clean (verify_corrections, mypy, ruff)
     * `C-0093-01` correction overlay redirects every downstream task to the fixed generator.

* **DSI spread across 60 cells**: they differ a lot.
  * Mean DSI 0.32 (different) / 0.35 (similar)
  * 3/60 cells with DSI=1.0 — but these are low-firing (7-8 spikes total) statistical artefacts
  * 21/60 cells with DSI>0.5
  * Some cells with DSI<0.1 (near-omnidirectional)
  * 4/60 cells with PD-rate=0 (fire at non-PD directions)
  * Total spike count range: 4 to 492 per cell (~100x spread)
  * Two important nuances:
    * DSI=1.0 cells are NOT strong tuning evidence — they're cells where 2-3 spikes happened to
      land at PD and 0 at ND. Statistical artefact.
    * "Similar" cells (small perturbations of Bed-B base) tend to fire heavily but with low tuning
      because asymmetry knobs are nearly neutral. Pair example: similar/morph_27 (479 spikes,
      DSI≈0.016) vs similar/morph_03 (slightly more asymmetric, DSI=0.62).
  * Honest read: morphology genuinely matters for DSI, but t0083 channel set was tuned for one
    specific morphology — that's exactly the gap t0091's joint NSGA-II is meant to close.

### Q2: Where's the per-cell DSI data?

Researcher: "where can I find DSI for each individual cell from these 60 cells?"

AI: Two JSON files under `tasks/t0093_resweep_and_t0090_correction/data/`:

1. **`post_fix_verification_summary.json`** — canonical per-cell record. 60 entries with
   `morph_id`, `population`, `dsi`, `pd_rate_hz`, `peak_vm_mv`, `n_dendrites`,
   `per_direction_spikes`, `pre_fix_stability_flag`, `pre_fix_spike_count_total`.
2. **`pre_post_delta.json`** — same 60 cells joined to pre-fix values plus per-cell
   `transition_label` and aggregate counts.

Plus 7 individual cell rows embedded as Examples 1-7 in `results_detailed.md` lines 171-308.

### Q3: Launch directive + budget

Researcher: "well it's time to run an optimisation. Update the t0091 if you haven't yet done so and
run it. How much budget do we need? Is there enough?"

AI budget answer:

|  | $ |
| --- | --- |
| Total budget | 20.00 |
| Spent | 15.55 |
| Remaining | 4.45 |
| t0091 plan estimate | 3.00–3.50 |
| Cost watchdog hard cap | 4.00 |
| Post-t0091 buffer | 0.45–1.45 |

Yes, enough — but tight. The $4.00 watchdog leaves $0.45 of safety margin against the $4.45 cap.
If realistic $3.00–3.50 holds, $0.95–1.45 left — enough for one cheap follow-up (S-0086-01,
~$1.50) only if lower estimate holds. No headroom for a second remote-compute task this budget
cycle.

## Discussion — Round 2: Clarifying Multi-Choice Questions

### Q: NMDA calibration scope

AI presented two options:
1. Keep separate (Recommended) — t0091 launches with current units; if Phase C bio-plausibility
   scoring shows NMDA exotic-ness signal is robust, run S-0090-03 afterward and re-score.
2. Fold into t0091 as Phase A.5 — adds ~30 min local wall-clock; Phase C bio-plausibility uses
   calibrated units from start.

Researcher: chose option 1 (Keep separate).

### Q: Cost watchdog level

AI presented two options:
1. Keep at $4.00 as planned (Recommended) — matches existing plan; gives NSGA-II room for 8 gens;
   $0.45 buffer.
2. Tighten to $3.50 — forces 6-gen fallback; $0.95 buffer; weaker signal but safer.

Researcher: chose option 1 (Keep at $4.00).

## Discussion — Round 3: Confirmation

The researcher's launch directive ("well it's time to run an optimisation. Update the t0091... and
run it.") combined with the two recommended-option selections constituted the Phase 2 Round 3
confirmation. AI proceeded with the full remaining lifecycle (Phases 3-6) without additional
authorization gate.

## Decisions Summary

1. **Update t0091 in place** (allowed because `not_started`):
   * Add `t0092_diagnose_morphology_generator_silence` and `t0093_resweep_and_t0090_correction` to
     dependencies
   * Refresh `short_description` to reference t0092-patched generator
   * `task_description.md` Motivation: acknowledge bug → diagnosis → fix → correction overlay
   * `task_description.md` In Scope: reference t0092 patched generator + C-0093-01
   * `task_description.md` Phase A anchor 1: source = t0093 post-fix Bed-B reproducibility
   * `task_description.md` Phase B per-cell eval: explicit
     `from tasks.t0092_..code.morphology_generator_fix import generate_fixed_morphology`
   * `task_description.md` Risks: refresh "Generator instability" to cite t0093's 60/60 STABLE
   * `task_description.md` Cross-References: add t0092, t0093, t0094

2. **Reject S-0092-03** (correction overlay against t0090 generator) — already done by t0093's
   `C-0093-01`.

3. **Reject S-0090-04** (tighten t0091 LHS bounds with 9 STABLE cells) — premise invalidated by
   t0093's 60/60 STABLE.

4. **Keep S-0090-03 separate** (G.2 NMDA units calibration) — post-t0091 follow-up.

5. **Cost watchdog at $4.00** — matches existing plan.

6. **No new tasks created.** t0091 is launched as-is via execute-task in a fresh worktree after this
   brainstorm merges.
