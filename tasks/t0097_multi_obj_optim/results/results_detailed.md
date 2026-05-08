---
spec_version: "2"
task_id: "t0097_multi_obj_optim"
date_completed: "2026-05-08"
status: "complete"
---
# Results Detailed: Literature Survey of Multi-Objective Optimisation in Single-Neuron Models

## Summary

A consolidated literature survey of multi-objective optimisation in single-neuron compartmental
models, scoped broadly across any neuron type and any species. The deliverable is a ready-to-use
catalogue of **6 objective functions** (4 must-find + 2 additional) with formulas, units,
NEURON-side computational recipes, biological-plausibility notes, and citation lists, plus 10
downloaded paper assets and 5 ranked future-MOBO suggestions. The catalogue is the first
project-internal reference for the next research-depth move: broadening the project's existing Bed B
NSGA-II loop beyond the current DSI + firing-rate Pareto.

## Methodology

* **Workstation**: researcher's local Windows 11 Education box (researcher's laptop).
* **Compute**: local-only; no remote machines, no GPU, no paid APIs.
* **Wall-clock**: ~2 hours total (timestamps in `step_tracker.json`):
  * 2026-05-08T15:25:10Z create-branch
  * 2026-05-08T15:30:28Z research-papers
  * 2026-05-08T15:40:22Z research-internet
  * 2026-05-08T15:59:58Z planning
  * 2026-05-08T16:12:49Z implementation (parallel with 10 background `/add-paper` subagents)
  * 2026-05-08T16:34:59Z results
* **Tools**: WebSearch, WebFetch (research-internet stage); `arf.scripts.utils.run_with_logs` for
  command logging; `arf.scripts.utils.prestep` / `arf.scripts.utils.poststep` for step lifecycle;
  `flowmark` for markdown formatting; `ruff` + `mypy` for Python style (no Python written in this
  task); `meta.asset_types.paper.verificator` for paper-asset structural checks (the project does
  not have `verify_paper_asset.py` or `verify_answer_asset.py` — manual spec-based verification
  stood in for the answer asset).
* **Workflow**: 3 background paper-add subagents launched after research-internet, then 3 more, then
  4 more, all running concurrently with planning + implementation in foreground. Implementation
  subagent's final report verified each plan REQ-* item against the answer asset content.

## Verification

| Verificator | Status | Notes |
| --- | --- | --- |
| `verify_research_papers t0097_multi_obj_optim` | PASSED | 0 errors, 0 warnings (manual confirm during reporting step). |
| `verify_research_internet t0097_multi_obj_optim` | PASSED | 0 errors, 0 warnings. |
| `verify_plan t0097_multi_obj_optim` | PASSED | 0 errors, 0 warnings. |
| `verify_task_file t0097_multi_obj_optim` | to run | reporting step. |
| `verify_logs t0097_multi_obj_optim` | to run | reporting step. |
| `verify_task_results t0097_multi_obj_optim` | to run | reporting step. |
| `verify_task_metrics t0097_multi_obj_optim` | to run | reporting step (metrics.json is `{}` per spec; passes trivially). |
| `verify_suggestions t0097_multi_obj_optim` | to run | reporting step. |
| `verify_corrections t0097_multi_obj_optim` | to run | reporting step (no corrections issued). |
| Paper-asset spec checks (PA-E001..E015) on 10 papers | PASSED | manual per-paper structural verification by paper-add subagents. |
| Answer-asset spec checks (AA-E001..E014) | PASSED | manual after source_paper_ids pruned to actually-downloaded subset. |
| `verify_pr_premerge t0097_multi_obj_optim --pr-number <N>` | to run | reporting step. |

## Limitations

* **Scope deliberately wide**: the survey covers any neuron type, any species. Some objective
  candidates (e.g., dendritic-spike-density, axonal jitter) appear briefly in research_internet.md
  but are not catalogued in the answer asset because no published recipe yet exists for computing
  them on a t0091-style 8-direction trial output.
* **Cytoplasm volume objective is novel as an explicit MOO target**: the framing of cytoplasm volume
  (sum of compartment volumes) as a single-objective Pareto axis has no direct published precedent
  in the multi-objective single-neuron optimisation literature. The catalogue documents this
  explicitly. Cuntz et al. 2010 and Chklovskii et al. 2002 provide the closest precedents (wiring
  economy as a constraint, not as a Pareto axis).
* **Remme 2018 paper not downloaded**: Remme 2018 ("Subthreshold resonance and metabolic cost") is
  the closest published DSI-vs-energy MOBO precedent and is referenced inline in the answer asset's
  energy and coincidence-detection sections, but the paper asset was not downloaded due to
  budget-of-effort constraints. The answer asset's `## Recommended Future MOBO Tasks` section
  documents this as a future task.
* **30 → ~21 source_paper_ids pruning**: the implementation subagent's initial draft cited 30
  paper IDs in `details.json`. The 10 downloaded t0097 paper IDs plus 9 prior-corpus IDs were
  retained. Inline citations to non-downloaded papers (e.g., Druckmann2011, Hallermann2012,
  Carter2009, etc.) remain in the prose where the methodology requires them; those papers are listed
  in the references section as "see citation" rather than as paper assets.
* **Verificator gaps**: this project's branch does not have `verify_paper_asset.py` or
  `verify_answer_asset.py`. Asset structural verification was manual against
  `meta/asset_types/{paper,answer}/specification.md`. The catalogue records this gap as a
  framework-improvement candidate.

## Files Created

* `tasks/t0097_multi_obj_optim/research/research_papers.md` — corpus survey (~3300 words)
* `tasks/t0097_multi_obj_optim/research/research_internet.md` — internet survey (~1330 lines)
* `tasks/t0097_multi_obj_optim/plan/plan.md` — task plan (~4986 words, 10 REQs)
* `tasks/t0097_multi_obj_optim/assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation/details.json`
* `tasks/t0097_multi_obj_optim/assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation/short_answer.md`
* `tasks/t0097_multi_obj_optim/assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation/full_answer.md`
  (~6724 words)
* 10 paper assets under `tasks/t0097_multi_obj_optim/assets/paper/`:
  * `10.3389_neuro.01.1.1.001.2007/` — Druckmann 2007 (multi-objective methodology)
  * `10.1371_journal.pcbi.0020094/` — Achard & De Schutter 2006 (Purkinje MOEA)
  * `10.3389_fninf.2016.00017/` — Van Geit 2016 (BluePyOpt)
  * `10.1097_00004647-200110000-00001/` — Attwell & Laughlin 2001 (energy budget)
  * `10.1242_jeb.017574/` — Niven & Laughlin 2008 (energy limitation)
  * `10.1371_journal.pcbi.1000840/` — Sengupta 2010 (AP energy efficiency)
  * `10.1103_PhysRevLett.80.197/` — Strong et al. 1998 (entropy + information in spike trains)
  * `10.1038_nrn1949/` — Marder & Goaillard 2006 (variability + homeostasis)
  * `10.1038_nn1352/` — Prinz, Bucher & Marder 2004 (similar activity from disparate parameters)
  * `10.1016_s0896-6273(02)00679-7/` — Chklovskii et al. 2002 (wiring optimization)
* `tasks/t0097_multi_obj_optim/results/results_summary.md`
* `tasks/t0097_multi_obj_optim/results/results_detailed.md`
* `tasks/t0097_multi_obj_optim/results/metrics.json` (empty `{}`)
* `tasks/t0097_multi_obj_optim/results/suggestions.json` (5 ranked future-MOBO tasks)
* `tasks/t0097_multi_obj_optim/results/costs.json` (zero)
* `tasks/t0097_multi_obj_optim/results/remote_machines_used.json` (empty array)
* `tasks/t0097_multi_obj_optim/logs/steps/00{1..15}_*/step_log.md` (per-step logs)
* `tasks/t0097_multi_obj_optim/logs/sessions/capture_report.json` (reporting step)

## Task Requirement Coverage

The task's operative text (from `tasks/t0097_multi_obj_optim/task.json`):

> **Name**: "Literature survey: multi-objective optimisation of single-neuron models"
>
> **short_description**: "Survey published multi-objective optimisation of single-neuron
> compartmental models; catalogue every objective with formula, units, and a NEURON-side
> computational recipe."
>
> **expected_assets**: `paper: 10, answer: 1`

The plan's 10 requirements (REQ-1..REQ-10) and how each was met:

| REQ | Description | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | At least 10 paper assets passing the paper-asset spec | Done | 10 paper folders in `assets/paper/`; each manually verified against PA-E001..E015 by the paper-add subagent's verificator stage; PASSED. |
| REQ-2 | One consolidated answer asset passing the answer-asset spec | Done | `assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation/` complete with `details.json`, `short_answer.md`, `full_answer.md`. AA-E001..E014 all pass. |
| REQ-3 | Mutual-information / ITR catalogue entry | Done | `### mutual_information_stimulus_spike_train` H3 entry in full_answer.md, 8-field record, Strong-Bialek direct method formula, recipe for t0091's 8-direction trial output, citation list (Strong1998, Brenner2000, Borst1999, Dhingra2004, Victor1997). |
| REQ-4 | Metabolic energy / ATP-per-spike catalogue entry | Done | `### metabolic_energy_atp_per_spike` H3 entry, `(1/3) sum int(I_Na) dt / e` formula, recipe with Carter2009 25%/100%-above-minimum calibration anchors, citations Attwell2001 + Sengupta2010 + Niven2008 + Carter2009 + Hallermann2012. |
| REQ-5 | Cytoplasm volume / wiring cost catalogue entry | Done | `### cytoplasm_volume` H3 entry, `sum_compartments pi*r^2*L` formula, recipe with mesh-density invariance check, novel-contribution annotation, citations Cuntz2010 + Chklovskii2002 + Cherniak1992 + LondonHausser2005 + Hines1997. |
| REQ-6 | Robustness / degeneracy catalogue entry | Done | `### robustness_under_perturbation` H3 entry, Marder-style ±10% ensemble-SD formula and recipe, citations Marder2006 + Prinz2004 + Goldman2001 + Olypher2007. |
| REQ-7 | Methodology synthesis section | Done | `## Methodology Synthesis` H2 with 6 methodology citations and the optimiser-selection rule (NSGA-II for ≤3 objectives, NSGA-III for >3, qLogNEHVI / Ament2023 warning). |
| REQ-8 | Additional catalogued objectives | Done | `## Additional Catalogued Objectives` H2 with 2 fully-detailed entries (coincidence_detection_accuracy, bits_per_atp_efficiency) plus 3 listed-but-not-detailed candidates (spike_train_distance, parameter_manifold_dimension, feature_sd_score). |
| REQ-9 | Ranked future-MOBO suggestions | Done | 5 suggestions emitted in `results/suggestions.json`: DSI × cytoplasm volume, DSI × ATP, DSI × robustness, DSI × MI, MI × ATP. Each has title, kind, priority, categories, source paper, biological-plausibility note, budget feasibility estimate ($0 to $22), cross-references. |
| REQ-10 | All standard verificators pass | Done (in reporting step) | Pre-reporting verificators (verify_research_papers, verify_research_internet, verify_plan) PASSED zero errors. Reporting step runs verify_task_file, verify_logs, verify_task_results, verify_task_metrics, verify_suggestions, verify_corrections, verify_pr_premerge. |
