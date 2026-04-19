---
spec_version: "3"
task_id: "t0014_brainstorm_results_3"
---
# Brainstorm session 3 — Researcher-AI Transcript

## Session context

Third brainstorm of the project. Called immediately after t0007 (NEURON/NetPyNE install) merged. The
researcher asked the AI to plan and execute more literature surveys to broaden the paper corpus.

## Transcript

**Researcher**: I want you to create 8 more tasks and execute them with high priority. You need to
find more papers, say 20 more for each of the categories of the project.

**AI** (after aggregating tasks, suggestions, costs and inspecting the t0002 paper corpus): Four
concerns before scaffolding eight tasks. (1) The 20 t0002 papers each carry 2-4 category tags, so
category tags overlap heavily — eight surveys at 20 papers each would produce large numbers of
duplicates. (2) `direction-selectivity`, `compartmental-modeling`, and `retinal-ganglion-cell` are
already saturated by t0002 plus t0010; a fresh survey in those categories would mostly re-discover
existing papers. (3) The `literature-survey` task-type has `has_external_costs: true`, which means
it cannot start while `project/budget.json` `total_budget` is 0.0 — a mechanical blocker,
unrelated to real spend. (4) Many relevant papers are behind institutional paywalls the agent cannot
bypass; but the researcher's institutional account can.

**AI** (options): Option (a) — run the 8 surveys as requested and accept the duplication and the
saturation; option (b) — drop the three saturated categories, run 5 surveys at ~25 papers each,
target ~125 total with ~80-100 unique after dedup; option (c) — run fewer surveys with narrower,
per-research-question scope.

**AI** (budget question): The budget gate can be cleared by (i) bumping `total_budget` to a nominal
$1 (the field tracks paid third-party services, not Claude tokens, so the actual spend for paper
downloads stays at $0), (ii) adding a `literature-survey` exception, or (iii) removing
`has_external_costs` from the literature-survey definition. Option (i) is least invasive.

**Researcher**: /remote-control then `b`.

**Researcher**: t0007 is finished now, no?

**AI**: Confirmed — t0007 merged as PR #7 while we were discussing. Ready to proceed.

**Researcher**: (b) + drop the 3 saturated categories, targeting 5 tasks × ~25 papers each, exclude
corpus dupes.

**Researcher**: Explain me the budget problem. Is it related to tokens or downloading papers behind
the paywall?

**AI**: The `total_budget` in `project/budget.json` tracks paid third-party services — OpenAI API,
paid compute, paid dataset subscriptions. It does not track Claude Code tokens (those are metered
separately and do not show up in `costs.json`). It also does not pay for paywalled papers — those
come from your institutional account, at no cost to the project. The gate is purely mechanical: the
literature-survey task type is flagged as potentially-paid, and the aggregator refuses to start
potentially-paid tasks while the budget is exactly $0.

**Researcher**: So if I don't want to pay any extra money which option should I choose? Also, I can
download papers behind the paywall manually from my account. You will just need me to tell which
ones.

**AI**: Pick option (i) — set `total_budget` to $1. Nothing will bill. For paywalled papers, the
paper-asset spec v3 supports `download_status: "failed"`; each survey will emit
`intervention/paywalled_papers.md` with a DOI list. You download them from your institutional
account into `files/`, then a follow-up correction pass flips `download_status` to `"success"`.

**Researcher**: Confirm. $1, 5 literature surveys, proceed.

**AI**: Proceeding. Creating branch `task/t0014_brainstorm_results_3`, scaffolding the brainstorm
task folder, writing 5 suggestions, bumping the budget to $1, creating t0015-t0019, running
verificators, materialising the overview, opening and merging the PR.
