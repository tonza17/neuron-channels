---
spec_version: "1"
task_id: "t0077_brainstorm_results_13"
session_date: "2026-05-03"
---
# Brainstorm Session 13 — Full Transcript

## Project State Presented

AI: Aggregated project state and presented:

* **76 total tasks**; 70 completed, 3 not_started (`t0031`, `t0045`, `t0075`), 3 cancelled
  (`t0042`-`t0044`), 1 intervention_blocked (`t0023`).
* **Budget**: $1.0583 / $10.00 spent (10.6%); only `t0076` had non-zero cost.
* **Active uncovered suggestions**: 237 (20 high · 180 medium · ~37 low).
* **Last brainstorm**: t0073 (session 12); 2 completed tasks since (`t0074`, `t0076`).

Key findings since session 12:

* **t0074 — Channel tuning-width sweep on Bed A** (8 channels x 3 densities x 12 angles x 5 seeds
  = 2100 trials). Headlines: NaP_high collapses vector-sum DSI from 0.193 to 0.050 while pushing
  peak rate 17.4 to 74.2 Hz; SK_high halves HWHM (84 deg to 41 deg, but creative-thinking flagged
  potential flat-top clipping artefact); Nav1.6 boosts firing without DSI loss; NaR broadens HWHM by
  +36 deg without changing DSI (novel finding, no published comparison); Kv3 / Kv4 / Kv7 inert at
  all somatic densities (Hu 2007 predicted Kv7's site is the AIS not soma).

* **t0076 — Bed B (de Rosenroll 2026) 25-d Bayesian MOBO** (430 cells x 8 dirs x 20 seeds = 68,800
  NEURON sims on Vast.ai 72-core CPU, $1.06, 5 h 3 min). Headline negative result: 25-d Bed B search
  cannot reach DSI >= 0.4 AND rate >= 30 Hz simultaneously, with smooth monotone trade-off on the
  Pareto front. Reproduces deRosenroll baseline DSI 0.39 within +0.03 (substrate validated). Bed B
  is missing dendritic-spike machinery and AIS — uniform soma+dendrite channels can't bridge the
  gap. t0076 vs t0068 contradiction: t0068 said Nav1.6+Kv3 jointly rescues DSI + rate on Bed A; the
  25-d search on Bed B never finds such a cell. Three implementation defects identified: NEURON
  re-init bug (`Exp2NMDA name already exists`), qNEHVI deprecation, GP input normalisation missing.

AI presented an independent priority reassessment of the 20 high-priority active uncovered
suggestions, classifying:

* Naturally still high (act soon): S-0076-01, S-0076-02, S-0076-04, S-0074-01, S-0074-02, S-0067-01.
* Still high but reconsider scope: S-0076-03 (should bundle into next BO task), S-0074-03 (already
  subsumed by t0075).
* Stale or superseded: S-0052-01, S-0052-02, S-0054-02, S-0055-02, S-0055-03, S-0057-06, S-0059-01,
  S-0059-02, S-0059-03, S-0065-02, S-0066-02 (all from-scratch DSGC family t0052 - t0059 lineage
  which the project pivoted away from), S-0070-01 (heavy methodological work).

Strategic observations:

1. t0075 is highest-leverage queued work (planned, not_started, deps satisfied).
2. The Bed B story is unfinished — t0076 set up a falsifiable claim and pointed at the cure (AIS +
   tier-stratification).
3. The from-scratch family is generating low-value suggestions; ~10 high-priority entries from that
   lineage are deprioritisable.
4. t0045 (CoreNEURON benchmark) is dormant — t0076 already validated stock NEURON on Vast.ai.
5. Budget is healthy ($8.94 left).

## Clarification Questions

AI: Asked five clarifying questions — notes/context, t0075 status, from-scratch family cleanup,
Bed B v2 scope, compute appetite.

Researcher: "I would like to focus on MOBO. It looks to me that suggestion s0076-02 is the most
important. So we need to implement this. While we are doing this, can we also implement suggestion
01 (seems doable in one optimisation task) and also suggestion 05 as a separate optimisation
parameter?"

AI: Confirmed which suggestion the researcher meant by "suggestion 05" by listing all six
t0076-derived suggestions (S-0076-01 through S-0076-06) and matching the description. Identified
S-0076-05 (slow Kv-mediated AHP mechanism) as the intended target. Read full descriptions of
S-0076-01, S-0076-02, S-0076-05, and noted that S-0024-03 (Van Wart + Werginz AIS overlay on the
deRosenroll morphology) is still uncovered, so any AIS-augmented Bed B task must build the AIS
section as part of its scope.

## Discussion — Round 1: New Tasks

AI: Proposed a single bundled task `t0078_bedb_mobo_v2_ais_tiered_ahp` covering:

1. Add AIS section to Bed B (S-0076-02 + S-0024-03; Van Wart 2007 / Werginz 2020 priors).
2. Tier-stratify channel densities into 5 tiers across Nav1.6, Kv3, NaP, BK, SK (S-0076-01).
3. Add slow Kv-mediated AHP as a new optimisation parameter (S-0076-05).
4. Roll in the t0076 implementation fixes (S-0076-03; researcher didn't explicitly ask but these are
   required for the new MOBO to run cleanly per memory of the researcher's preference for
   consolidated tasks bundling related suggestions plus infra fixes).

Total parameter dimensionality: ~40 - 50 d. Compute estimate: ~$2.50 - $4.00 over 9 - 12 h on
Vast.ai 72-core CPU. Pass criterion: locate at least one Pareto cell with DSI >= 0.4 AND PD rate
> = 30 Hz, OR rule it out architecturally.

AI: Asked four follow-up scoping questions:

1. Slow-AHP scope: SK_E2 with extended Ca-binding (smallest change, reuses Hay 2011 SK code path) or
   a dedicated KAHP mechanism (more biologically faithful, more code)?
2. Parameter budget: 40 - 50 d acceptable, or stricter at ~35 d?
3. Warm-start strategy: inflate uniform-density t0076 Pareto front across all tiers (default), or
   restart fresh with Sobol only?
4. Other suggestions: also propose to deprioritise / reject the ~10 stale from-scratch-family
   high-priority suggestions in this session?

Researcher: "1. sk_e2 2. 40-50 should be acceptable. 3. restart fresh 4. yes."

## Discussion — Round 2: Suggestion Cleanup

AI: Proposed sixteen rejections (no reprioritisations) and one task cancellation:

* Reject 4 high-priority covered by t0078: S-0076-01 (tier-stratification), S-0076-02 (AIS-augmented
  MOBO primary), S-0076-03 (implementation fixes), S-0076-05 (slow Kv-AHP).
* Reject 1 medium-priority covered by t0078: S-0024-03 (Van Wart + Werginz AIS overlay; AIS library
  asset built as part of t0078 scope).
* Reject 11 high-priority stale from-scratch family: S-0052-01, S-0052-02, S-0054-02, S-0055-02,
  S-0055-03, S-0057-06, S-0059-01, S-0059-02, S-0059-03, S-0065-02, S-0066-02.
* Cancel t0045 (CoreNEURON-on-GPU benchmark) — t0076 already validated stock NEURON on Vast.ai
  72-core CPU; the original 5x speedup-assumption uncertainty in t0033's cost model is no longer
  load-bearing.

(The total count of correction files is 16, not 15 as initially stated to the researcher; the
discrepancy was internal accounting and resolved during writing of correction files. The S-0076-02
correction is technically redundant since t0078.source_suggestion = S-0076-02 already covers the
suggestion via the source-link mechanism, but is kept following the t0073 pattern of also writing an
explicit rejection correction so the "active" filter is clean.)

## Discussion — Round 3: Confirmation

AI: Presented the consolidated decision summary:

* New task to create: t0078 bedb_mobo_v2_ais_tiered_ahp (full scope, dependencies, source suggestion
  S-0076-02, compute estimate, pass criteria).
* Suggestions to reject — covered by t0078 (4): S-0076-01, S-0076-03, S-0076-05, S-0024-03 (and
  S-0076-02 added during writing).
* Suggestions to reject — stale from-scratch family (11).
* Task to cancel — propose, please confirm: t0045_coreneuron_vastai_speedup_benchmark.
* Suggestions and tasks NOT changing: t0075, t0031, S-0067-01, S-0070-01, S-0074-01, S-0074-02,
  S-0074-03, S-0076-04.
* Brainstorm-results task: t0077_brainstorm_results_13 created to record this session.
* Counts: 1 new task created, 16 corrections written, 0 or 1 task cancelled (pending t0045
  confirmation).
* Note on the redundant Sense-of-approval workflow: confirmation authorises the entire remaining
  lifecycle including push, PR, merge.

Researcher: "a. approve b. yes, cancel it"

## Decisions Summary

1. Create t0078_bedb_mobo_v2_ais_tiered_ahp (single bundled MOBO task, 40 - 50 d, fresh Sobol
   restart, qLogNEHVI, ~$2.50 - $4.00 on Vast.ai 72-core CPU).
2. Cancel t0045_coreneuron_vastai_speedup_benchmark (superseded by t0076's actual Vast.ai-CPU run).
3. Reject 16 suggestions: S-0024-03, S-0052-01, S-0052-02, S-0054-02, S-0055-02, S-0055-03,
   S-0057-06, S-0059-01, S-0059-02, S-0059-03, S-0065-02, S-0066-02, S-0076-01, S-0076-02,
   S-0076-03, S-0076-05.
4. No reprioritisations.
5. No new suggestions.
6. No answer assets.
7. Researcher approval covers the entire remaining lifecycle: branch, scaffold, write corrections,
   cancel t0045, create t0078, write step logs, capture sessions, run verificators, push, PR,
   pre-merge verificator, merge.
