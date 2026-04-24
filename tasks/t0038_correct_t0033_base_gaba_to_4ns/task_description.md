# Correct t0033 base GABA to 4 nS on t0022 variant

## Motivation

t0033's Vast.ai optimisation plan was written before the GABA-ladder rescue was available. At the
time, the plan implicitly assumed the t0022 default `GABA_CONDUCTANCE_NULL_NS = 12 nS` as the base
parameter for the joint morphology + channel optimisation. Subsequent experimental tasks showed this
default is incompatible with a working DSI objective:

* **t0030** — 7-diameter sweep at 12 nS: primary DSI pinned at 1.000; diameter effect
  unmeasurable.
* **t0036** — halved to 6 nS: primary DSI still pinned at 1.000; null firing = 0 Hz.
* **t0037** — ladder sweep across {4, 2, 1, 0.5, 0} nS: 4 nS is the operational sweet spot
  (primary DSI = 0.429, preferred direction = 40.8°, matches Park2014's biological range
  0.40–0.60). Below 2 nS the cell over-excites and preferred direction randomises.

Without this correction, any downstream task that reads t0033's plan and instantiates an optimiser
on t0022 with the legacy 12 nS default would burn compute on a pinned objective: the optimiser would
see a flat DSI=1.000 landscape and converge to anything.

## Scope

Create a correction file in `corrections/` that updates t0033's answer asset
(`vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation`) to document the new base-parameter
recommendation. The correction's `changes` payload adds or overrides a parameter note so that
aggregators and downstream consumers expose the corrected effective view.

This is a **correction-type task**. No sweep, no plan rewrite, no new answer asset. The completed
t0033 folder remains untouched, per the ARF immutability rule.

## Dependencies

* `t0033_plan_dsgc_morphology_channel_optimisation` — target of the correction
* `t0037_null_gaba_reduction_ladder_t0022` — source of the 4 nS evidence

## Approach

1. Read `arf/specifications/corrections_specification.md` to confirm the correction file format for
   `target_kind: "answer"` with `action: "update"`.
2. Read t0033's `assets/answer/vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation/`
   details and full answer document to understand what the correction must override.
3. Write `corrections/answer_vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation.json`
   with a concise `changes` object and a `rationale` citing t0037's DSI=0.429 result at 4 nS and
   t0036's pinned result at 6 nS.
4. Run `verify_correction.py` (or equivalent) to confirm the correction file is valid.
5. Run `aggregate_answers.py` to confirm the effective aggregated view of the answer reflects the
   new base parameter.

## Expected Outputs

* `corrections/answer_vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation.json` — single
  correction file with `correction_id: "C-0038-01"`, `action: "update"`, and
  `target_kind: "answer"`.
* `results/results_summary.md` — brief confirmation that the correction was written and verified.
* `results/suggestions.json` — empty or minimal; this task closes S-0037-02 and does not generate
  new experimental follow-ups.

## Expected Assets

None. This task produces a correction file and a results writeup, not new assets.

## Compute and Budget

* Local only. No remote machines. No paid APIs.
* Expected wall time: under 5 minutes total (metadata edit + verificator runs).
* Cost: $0.00.

## Cross-References

* Source suggestion: **S-0037-02** ("Update t0033 optimiser base GABA on t0022 variant to 4.0 nS")
* Evidence task: t0037 (DSI=0.429 at 4 nS; DSGC-like preferred direction 40.8°)
* Pinned baselines: t0030 (12 nS, DSI=1.000), t0036 (6 nS, DSI=1.000)

## Verification Criteria

1. `corrections/answer_vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation.json` exists
   and passes the corrections verificator.
2. The `correction_id` matches the regex `^C-0038-\d{2}$`.
3. `correcting_task` equals `t0038_correct_t0033_base_gaba_to_4ns` and `target_task` equals
   `t0033_plan_dsgc_morphology_channel_optimisation`.
4. Running `aggregate_answers` with the correction overlay in place surfaces the updated base
   parameter (or a field recording the update) in the effective answer object.
