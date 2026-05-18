---
spec_version: "3"
task_id: "t0106_long_pdnd_nsga2_300gen"
step_number: 5
step_name: "research-internet"
status: "completed"
started_at: "2026-05-16T22:52:18Z"
completed_at: "2026-05-16T22:58:38Z"
---
# Step 5 — research-internet

## Summary

Conducted internet research targeting four gaps left by the corpus-only research_papers.md stage:
long-horizon NSGA-II evidence on 40+ -d biophysical neuron problems, empirical pymoo / EMO
hypervolume-plateau heuristics, recent DSGC modelling using ratio DSI on a 2-direction protocol, and
operator-stop signalling patterns for long-running pymoo NSGA-II runs. Wrote research_internet.md
with 12 sources cited, 3 newly discovered papers queued for orchestrator ingestion, and all 6 gaps
from research_papers.md resolved to status (1 partially resolved, 2 unresolved with concrete
reasons, 3 partially resolved). Verificator passes with zero errors and zero warnings.

## Actions Taken

1. Read tasks/t0106_long_pdnd_nsga2_300gen/task.json, task_description.md, and
   research/research_papers.md to extract the four operator-supplied research questions and the six
   gaps the corpus stage left open.
2. Executed 11 WebSearch queries across three passes (gap-targeted, broadening, snowball) plus 3
   WebFetch deep-reads on pymoo termination docs, pymoo running_metric.py source, and the Chen 2024
   STN-model PMC article. Cross-referenced discovered DOIs against the existing paper corpus
   (Ankri2024 and Riccitelli2025 confirmed already-present; Chen2024-STN, DendroTweaks-2025, and
   BlankDeb2020 newly discovered).
3. Wrote tasks/t0106_long_pdnd_nsga2_300gen/research/research_internet.md following the v1
   specification with all 8 mandatory sections, ran flowmark formatting, fixed a citation-key
   inconsistency (Caval-Holme2025 -> CavalHolme2025), corrected the sources_cited frontmatter count
   from 12 to 13, and re-ran the verificator until clean.

## Outputs

* tasks/t0106_long_pdnd_nsga2_300gen/research/research_internet.md (~600 lines after flowmark; 13
  Source Index entries, 3 Discovered Papers, all 6 corpus gaps addressed)

## Issues

None. All operator-supplied questions received concrete answers grounded in the searched sources:
(1) no 2024-2026 NSGA-II run past 200 gens on 40+ -d biophysical models was found, though Chen 2024
demonstrates ~1M evals on 20-d STN; (2) pymoo's RunningMetric uses hardcoded threshold 0.005 with
sliding window 30 (Blank & Deb 2020) which makes t0106's 1% / 60-min heuristic conservative; (3) the
t0106 2-direction ratio-DSI reformulation is methodologically novel within the surveyed DSGC
literature, with the prior convention being 8-12-16 directions; (4) the convergent operator-stop
pattern is a pymoo Callback subclass setting algorithm.termination.force_termination = True on
stop-file detection, paired with dill checkpoint serialisation for crash recovery.
