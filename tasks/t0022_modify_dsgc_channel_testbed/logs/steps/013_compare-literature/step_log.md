---
spec_version: "3"
task_id: "t0022_modify_dsgc_channel_testbed"
step_number: 13
step_name: "compare-literature"
status: "completed"
started_at: "2026-04-21T01:29:00Z"
completed_at: "2026-04-21T01:40:00Z"
---
## Summary

Authored `results/compare_literature.md` comparing the t0022 per-dendrite E-I scheduling port of
ModelDB 189347 against the published DSGC literature. The document reports our DSI 1.0 / peak 15 Hz
/ null 0 Hz / HWHM 116.25 deg / reliability 1.0 against the Poleg-Polsky & Diamond 2016, Oesch2005,
Park2014, Schachter2010, and Sivyer2013 envelopes; explains why our DSI saturates (clean baseline +
deterministic driver + 12 nS null GABA) and why peak rate is on the low end (HHst density caps
firing at 10-20 Hz regardless of DS mechanism); and places t0022 relative to t0008 (DSI 0.316, below
envelope) and t0020 (DSI 0.7838, matches envelope) as the first mechanistically faithful port in
this project.

## Actions Taken

1. **Read the specification and inputs.** Loaded
   `arf/specifications/compare_literature_specification.md` (v1) for the required frontmatter, the
   five mandatory sections (Summary / Comparison Table / Methodology Differences / Analysis /
   Limitations), the verificator error codes CL-E001 through CL-E005 and warnings CL-W001 through
   CL-W003, and the 150-word / 2-row minimums. Read
   `tasks/t0022_modify_dsgc_channel_testbed/research/research_papers.md` for the published
   quantitative envelopes (Park2014 null/pref I ratio 2-4x and 0.31 nS E / 2.43 nS I anchor,
   Oesch2005 spike DSI 0.67-0.74 and -41.5% TTX effect, Schachter2010 ~6 nS gating vs ~85 nS
   blocking, Sivyer2013 80-150 Hz peak, VanWart2006 AIS partition), read `plan/plan.md` for the
   target envelope (DSI at or above 0.5, peak firing rate at or above 10 Hz), and read
   `results/results_detailed.md` for our quantitative results and the t0008 / t0020 sibling port
   numbers (t0008 DSI 0.316 / peak 18.1 Hz rotation proxy; t0020 DSI 0.7838 / peak 14.85 Hz gabaMOD
   swap).
2. **Wrote `results/compare_literature.md`.** spec_version "1" YAML frontmatter with
   `task_id: t0022_modify_dsgc_channel_testbed` and `date_compared: 2026-04-21`. All 5 mandatory
   sections present. Comparison Table has 10 data rows covering 5 papers (Poleg-Polsky & Diamond
   2016 source with DSI / peak / null rows; Oesch2005 with DSI and peak; Park2014 with DSI,
   null/pref I ratio, and PD E conductance; Sivyer2013 with peak; Schachter2010 with PSP-to-spike
   amplification factor). All rows have numeric Published Value and Our Value columns with computed
   Delta and context Notes. Methodology Differences section lists six bullet points covering bar
   geometry, baseline synapse silencing, E-I scheduling rule, per-dendrite conductance magnitudes,
   trial-to-trial variability, and spike-initiation apparatus. Analysis section explains DSI
   saturation (three factors: cleaner baseline, 2x-gating-threshold GABA, deterministic scheduling),
   the 15 Hz peak gap (three factors: HHst density, single-bar stimulus, modest AMPA charge), and
   t0022's position relative to t0008 / t0020 (rotation proxy below envelope; gabaMOD swap numeric
   match without mechanism; t0022 first mechanistically faithful port). Limitations section covers
   six caveats including no tuning-curve-level replication, space-clamp attenuation of Park2014
   somatic numbers, Sivyer2013 peak rate inapplicability, HWHM incomparability, no SAC feedforward
   model, and no velocity sweep.
3. **Formatted the new markdown and this step log with flowmark** via the `run_with_logs.py` wrapper
   to normalise line width to 100 characters while preserving the comparison table rows (tables are
   exempt from the 100-character limit per the markdown style guide).
4. **Ran the verificator.** Executed
   `uv run python -u -m arf.scripts.verificators.verify_compare_literature t0022_modify_dsgc_channel_testbed`
   wrapped via `run_with_logs.py`. Result: **PASSED — no errors or warnings** (zero hits across
   CL-E001 through CL-E005 and CL-W001 through CL-W003). Evidence preserved in
   `logs/commands/*verify_compare_literature*` triple produced by the wrapper.

## Outputs

* `tasks/t0022_modify_dsgc_channel_testbed/results/compare_literature.md`
* `tasks/t0022_modify_dsgc_channel_testbed/logs/steps/013_compare-literature/step_log.md` (this
  file)

## Issues

No issues encountered. The verificator `verify_compare_literature.py` ran cleanly and reported zero
errors and zero warnings on the produced `compare_literature.md`. A minor detail worth noting for
downstream readers: flowmark occasionally wraps hyphenated compound words like `per-dendrite` across
a line break as `per-` + `dendrite` with a space in between; two such occurrences in the first-pass
output were manually un-wrapped and the file re-run through flowmark before the final verificator
check. Also, flowmark initially interpreted a numbered-list continuation line that began with
`>= 0.5` as a Markdown blockquote, which was resolved by rewording to "at or above 0.5" before the
final format pass.
