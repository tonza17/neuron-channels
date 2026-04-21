---
spec_version: "3"
task_id: "t0024_port_de_rosenroll_2026_dsgc"
step_number: 13
step_name: "compare-literature"
status: "completed"
started_at: "2026-04-21T07:30:19Z"
completed_at: "2026-04-21T07:45:00Z"
---
## Summary

Wrote `results/compare_literature.md` (spec v1) comparing the t0024 port to the [deRosenroll2026]
published envelope and to the prior DSGC ports t0008, t0020, and t0022. The comparison documents the
REQ-5 port-fidelity miss quantitatively: port correlated DSI 0.8182 vs paper 0.39 (delta +0.43),
port uncorrelated DSI 0.8351 vs paper 0.25 (delta +0.59), port drop fraction 0.000 vs paper ~0.36
(delta -0.36), and port peak firing rate 5.15 Hz vs paper qualitative ~30-40 Hz. Also recorded the
positive angular-sharpness finding (HWHM 68.65 deg vs t0004 target 68.51 deg, delta +0.14) and the
lineage-wide firing-rate gap visible across t0008/t0020/t0022/t0024. Cross-model cross-reference for
t0023 (Hanson 2019) was marked as partial coverage since t0023 is `intervention_blocked`.

## Actions Taken

1. Read `arf/specifications/compare_literature_specification.md` (v1) for mandatory sections,
   frontmatter format, and verification rules (CL-E001..CL-E005, CL-W001..CL-W003).
2. Aggregated published envelope numbers from `research/research_internet.md` (deRosenroll2026
   correlated DSI 0.39, uncorrelated DSI 0.25, ~36% drop, AMB tau ~27 um) and
   `research/research_papers.md` (t0004 target DSI 0.8824, HWHM 68.51 deg; cross-model DSI values
   for t0008 0.316, t0020 0.784).
3. Pulled t0024 measured values from `results/results_summary.md` and `data/score_report.json` (DSI
   12-ang corr 0.7759, DSI 8-dir corr 0.8182, DSI 8-dir uncorr 0.8351, drop 0.000, peak 5.15, HWHM
   68.65, RMSE 15.49, reliability 0.984).
4. Wrote `results/compare_literature.md` with the 5 mandatory sections (Summary, Comparison Table,
   Methodology Differences, Analysis, Limitations), a 10-row comparison table covering published and
   cross-model baselines, and bolded quantitative values throughout.
5. Ran `uv run flowmark --inplace --nobackup` on the new markdown files.

## Outputs

* `tasks/t0024_port_de_rosenroll_2026_dsgc/results/compare_literature.md`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/logs/steps/013_compare-literature/step_log.md`

## Issues

t0023_port_hanson_2019_dsgc is `intervention_blocked` so its row in the cross-model comparison table
is absent; this matches the REQ-6 partial-coverage caveat already recorded in step 12. The
port-fidelity miss itself is not a step blocker — it is the headline finding of the port and is
recorded as a first-class result in `intervention/port_fidelity_miss.md` and
`metrics.json["de_rosenroll_port_fidelity_gate_pass"] = false` per plan step 13.
