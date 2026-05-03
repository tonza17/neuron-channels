---
spec_version: "3"
task_id: "t0078_bedb_mobo_v2_ais_tiered_ahp"
step_number: 5
step_name: "research-internet"
status: "completed"
started_at: "2026-05-03T13:50:16Z"
completed_at: "2026-05-03T14:10:00Z"
---
# Step 5 — Research Internet

## Summary

Spawned a `/research-internet` subagent to fill the three gaps the research-papers step flagged
(SK_E2 / Khaliq sources, qLogNEHVI methodology, joint DSI + PD firing-rate measurements). The
subagent produced `research/research_internet.md` and listed seven new papers to add to the corpus.
Verificator passes 0 errors / 0 warnings. Headline finding: the project's domain-knowledge pass
criterion of "PD rate >= 30 Hz" is **not supported by literature** — Rivlin-Etzion 2012 reports
paired DSI + mean PD rate measurements in the same mouse ON-OFF DSGCs showing **DSI 0.78 ± 0.19
with mean PD rate 10.38 ± 8.53 Hz over 3 s**. The "30-80 Hz" figure appears to conflate peak
(sub-second) and mean rates. Recommendation surfaced: revise t0078 pass criterion to "DSI >= 0.4 AND
PD rate >= 10 Hz" with ">=30 Hz" as a stretch goal. The planning step will explicitly address this.

## Actions Taken

1. Ran `prestep research-internet`.
2. Spawned a `/research-internet` subagent with explicit framing on the three corpus gaps. The
   subagent produced 14 search queries, identified 7 new papers, recommended a `tau_ca_multiplier`
   range extension to `[1, 200x]` based on Larsson 2013 sAHP timescale (1 - 3 s, set by hippocalcin
   → KCNQ-like channels rather than SK Ca-binding), confirmed qLogNEHVI is a single-line drop-in
   replacement for qNEHVI per the BoTorch official tutorial, and surfaced the "30-80 Hz" / "10.38
   Hz" discrepancy in the project's pass criterion.
3. Verified `research/research_internet.md` exists with all required sections including the
   `## Discovered Papers` section listing 7 papers.
4. Ran `verify_research_internet.py` via `run_with_logs.py`: PASSED with 0 errors, 0 warnings.

## Outputs

* `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/research/research_internet.md` — internet research
  covering SK_E2 / Khaliq / Larsson sAHP kinetics, BoTorch qLogNEHVI methodology (Ament 2023),
  Wienbar 2022 NEURON AIS template (Zenodo public model), Werginz 2024 mouse alpha-RGC
  tier-stratified channel densities, Rivlin-Etzion 2012 / Trenholm 2013 paired DSI + firing-rate
  data.
* `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/logs/steps/005_research-internet/step_log.md` — this
  step log.

Discovered papers (to be added per skill rules; deferred to background paper-addition subagents):

| Citation key | DOI / arXiv | Why relevant |
| --- | --- | --- |
| Hay2011 | 10.1371/journal.pcbi.1002107 | SK_E2 / CaDynamics_E2 source paper |
| Khaliq2003 | 10.1523/JNEUROSCI.23-12-04899.2003 | NaR / bkpkj source paper |
| Ament2023 | arXiv 2310.20708 | qLogNEHVI methodology (NeurIPS 2023) |
| RivlinEtzion2012 | 10.1016/j.neuron.2012.08.041 | Paired DSI + PD firing-rate in mouse DSGC |
| Trenholm2013 | 10.1523/JNEUROSCI.0808-13.2013 | Peak vs mean PD rate distinction in DSGC |
| Wienbar2022 | 10.1016/j.neuron.2022.04.012 | Public NEURON AIS model (Zenodo) |
| Werginz2024 | 10.1523/JNEUROSCI.1592-24.2024 | Mouse αRGC tier-stratified channel densities |

## Issues

**Major project-level finding (NOT a step issue but flagged here)**: the t0078 pass criterion of "PD
rate >= 30 Hz" is not literature-supported. Mouse ON-OFF DSGC mean PD rate over 1 - 3 s is ~10 Hz
(Rivlin-Etzion 2012, Webvision review). The planning step must explicitly negotiate the revised
criterion with the researcher; the implementation step's BO utopia point should target (DSI 0.7, PD
rate 15 Hz) rather than (DSI 1.0, PD rate 30 Hz) to keep the optimisation focused on biologically
plausible cells.

Open follow-up questions documented by the subagent:
* Werginz 2020 NEURON model code remains paywalled; Wienbar 2022 Zenodo archive is the public
  substitute.
* Köhler 1996 SK cloning paper has no clean DOI in search results (PMID 8781233).
* Empirical guidance for the exact `tau_ca_multiplier` upper bound is not directly measured.
* "30-80 Hz mean PD rate" provenance unverified — flagged for researcher confirmation in planning.

Per the skill, the seven discovered papers should be added via parallel `/add-paper` subagents.
Given the practical context budget for this session (the orchestrator paused after planning per
researcher instruction), paper addition is deferred to a later step / session; the planning subagent
will use the citations and findings already in `research_internet.md` rather than require the corpus
updates first.
