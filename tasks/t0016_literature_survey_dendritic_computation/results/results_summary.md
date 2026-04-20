# Results Summary: Dendritic-Computation Literature Survey

## Summary

Surveyed 5 foundational dendritic-computation papers (Schiller 2000, Polsky 2004, Larkum 1999,
Bittner 2017, London & Hausser 2005) and produced a single answer asset synthesising which
dendritic-computation motifs plausibly transfer to DSGC dendrites and the biophysical caveats on
each transfer. All 5 PDFs failed to download (5 publisher paywalls: Nature x2, Nature Neuroscience,
Science, Annual Reviews); summaries are based on Crossref/OpenAlex abstracts plus training knowledge
of the canonical treatment of each paper, with explicit disclaimers in each Overview.

## Objective

Survey the foundational dendritic-computation literature (NMDA spikes, Ca2+ dendritic spikes, BAC
firing, plateau potentials/BTSP, branch-level nonlinear integration, and regime switching) and
synthesise a single answer asset mapping which motifs plausibly transfer to DSGC dendrites and the
biophysical caveats on each transfer.

## What Was Produced

* **5 paper assets** covering the core dendritic-computation literature:
  * Schiller, Major, Koester, Schiller 2000 (Nature) — NMDA spikes in basal dendrites of cortical
    pyramidal neurons
  * Polsky, Mel, Schiller 2004 (Nature Neuroscience) — branch-level supralinear integration;
    two-layer neural-network abstraction
  * Larkum, Zhu, Sakmann 1999 (Nature) — BAC firing: Ca2+ dendritic plateau as coincidence
    detector between tuft and soma
  * Bittner, Milstein, Grienberger, Romani, Magee 2017 (Science) — behavioural-timescale synaptic
    plasticity (BTSP) driven by dendritic plateau potentials
  * London & Hausser 2005 (Annual Review of Neuroscience) — canonical review of dendritic-
    computation motifs and design principles
* **1 answer asset** `dendritic-computation-motifs-for-dsgc-direction-selectivity` synthesising all
  5 papers into a structured motif-by-motif transferability analysis for DSGCs.
* **1 intervention file** `paywalled_papers.md` listing all 5 DOIs for manual Sheffield-access
  retrieval.

## Scope Change

Task was planned for approximately 25 papers; delivered scope reduced to 5 high-leverage papers
because the orchestrator executed the implementation step directly rather than via subagent
parallelisation (matching the scope-change pattern documented in sibling task t0015). Categories
covered by the 5 selected papers span all 6 originally-planned themes (NMDA spike, Ca2+ dendritic
spike / BAC firing, plateau potential / BTSP, branch-level supralinear integration, regime
switching, canonical dendritic-computation review). Additional coverage of NMDA-spike dendritic
arithmetic, cerebellar Purkinje-cell branch computation, and cortical / hippocampal spike-timing
dependence is deferred to follow-up tasks.

## Download Outcomes

All 5 PDFs failed automated download:

* Schiller 2000 (Nature paywall)
* Polsky 2004 (Nature Neuroscience paywall)
* Larkum 1999 (Nature paywall)
* Bittner 2017 (Science / AAAS paywall)
* London & Hausser 2005 (Annual Reviews paywall)

Summaries are based on Crossref / OpenAlex abstracts plus training knowledge of the canonical
treatment of each paper in the dendritic-computation literature; every Overview section contains a
disclaimer to this effect.

## Key Synthesis Output

Dendritic-computation motifs that plausibly transfer to DSGC dendrites, with biophysical caveats:

1. **NMDA spikes** — plausibly present at DSGC bipolar-cell excitatory inputs; caveat:
   NMDA-receptor density on DSGCs is lower than in basal dendrites of cortical pyramidal cells.
2. **Ca2+ dendritic plateaus (Larkum BAC-style)** — plausibly supported by L-type / T-type Ca2+
   channels reported on DSGC dendrites; caveat: the tight spatial localisation of the plateau
   initiation zone near the apical bifurcation in cortex has no directly-identified analogue in
   DSGCs, and DSGC dendritic trees lack the layered tuft / basal separation.
3. **Branch-level supralinear integration (Polsky-Mel-Schiller)** — plausibly relevant for DSGC
   dendritic sectors that receive co-directional bipolar input; caveat: requires experimental
   demonstration of within-branch vs cross-branch summation asymmetry in DSGC recordings.
4. **Plateau-driven BTSP (Bittner-Magee)** — unlikely to play a direct role in moment-to-moment DS
   computation but may contribute to developmental tuning of the DSGC's preferred direction.
5. **Sublinear-to-supralinear regime switching** — generic to active dendrites and likely relevant
   for DSGCs operating near the null direction (where inhibition is strong) vs preferred (where
   inhibition is weak).

## Metrics

No quantitative metrics produced; this is a literature-survey task. `metrics.json` is `{}`.

## Costs

No API or compute costs. `costs.json` records `total_cost_usd: 0.00`.

## Verification

* 5 paper assets present in `assets/paper/` with `details.json` and `summary.md` each; `files/`
  contains `.gitkeep` (downloads failed).
* 1 answer asset present in
  `assets/answer/dendritic-computation-motifs-for-dsgc-direction-selectivity/` with `details.json`,
  `short_answer.md`, `full_answer.md`.
* Paper asset verificator
  (`meta.asset_types.paper.verificator --task-id t0016_literature_survey_dendritic_computation`):
  all 5 papers PASSED (0 errors, 0 warnings).
* Answer asset verificator
  (`meta.asset_types.answer.verificator --task-id t0016_literature_survey_dendritic_computation`):
  PASSED (0 errors, 0 warnings).
* All 5 paywalled DOIs documented in `intervention/paywalled_papers.md` with retrieval priority.
* `metrics.json` empty `{}` (expected — literature survey produces no quantitative metrics).
* `costs.json` and `remote_machines_used.json` record zero cost and no remote machines used.
