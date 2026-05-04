# Brainstorm Session 14 -- Full Transcript

Date: 2026-05-04. Triggered by t0078 completion (49-d Bed B v2 BoTorch qLogNEHVI MOBO with AIS,
tier-stratified channels, slow Kv-AHP).

## Project State Presented

### Budget

* Spent: $4.99 / $10.00 (49.9%)
* Remaining: $5.01 (warn threshold at $8.00, so $3.01 before warn)
* Last task t0078: $3.93 alone (slightly over its $4.00 envelope; under $5.00 hard limit)
* Earlier MOBO t0076: $1.06

### Tasks

* 78 total: 72 completed, 4 cancelled (t0042-t0045), 2 not_started, 1 intervention_blocked
* Not started: t0031 (paywalled morphology Kim2014/Sivyer2013), t0075 (Bed A bio-realistic AIS
  one-axis sweep -- still queued from session 13)
* Intervention-blocked: t0023 (Hanson 2019 DSGC port -- deferred since session 4)

### Headline result (t0078: 49-d Bed B MOBO with AIS + tier-stratification + slow Kv-AHP)

* HV +36% over t0076 (8.41 -> 11.41), but joint pass criterion missed by 0.084 DSI / 0.32 Hz
* Closest Pareto cell (iter 81): DSI 0.316, PD 9.68 Hz -- PD axis fully within Rivlin-Etzion 2012
  distribution (z=-0.08), DSI axis 2.4 sigma short
* High-DSI rail's PD ceiling pinned at ~2.86 Hz across 109 acquisitions -- saturated negative
  feedback
* BO stopped early at acq 416/700 due to O(N^3) GP-fit blow-up; per-cell wall-clock grew from 28 s
  -> 9-12 min by acq 480
* AIS Nav collapsed to search floor 1e-5 S/cm^2 at iter 81 -- four orders below Kole 0.25-0.5 prior;
  optimiser exploited an AIS-disabled corner that contradicts REQ-2/3/4's biological intent
* Compare-literature verdict: passive dendrites are the bottleneck; missing dendritic-spike
  machinery (Mg-block NMDA + distal Nav1.6/NaP for back-propagating APs) is the next architectural
  ingredient

### Suggestions backlog

* 229 active uncovered (7 high, 182 medium, 40 low)

7 high-priority active uncovered:
* S-0078-01 -- Add dendritic-spike machinery to AIS-augmented Bed B; re-optimise with NSGA-II via
  pymoo (not BoTorch qLogNEHVI) under hard AIS Nav lower-bound prior. The direct architectural
  follow-up to t0078's negative result.
* S-0067-01 -- NaP density at which DSI crosses zero (cheap ~25 min)
* S-0070-01 -- Cross-bed PD/ND encoding harmonisation (methodological)
* S-0074-01 -- SK polar-curve clipping check (cheap analysis on existing data)
* S-0074-02 -- NaR ND-floor verification (cheap)
* S-0074-03 -- AIS-localised Kv7 (covered by still-queued t0075)
* S-0076-04 -- t0076-vs-t0068 Nav1.6+Kv3 contradiction test

New from t0078:
* S-0078-01 (high) -- dendritic-spike + NSGA-II
* S-0078-02 (medium) -- substrate regression check on iter-424 t0076 vector (cheap)
* S-0078-03 (medium) -- tau_ca_multiplier upper bound 20x -> 200x test
* S-0078-04 (medium) -- single-objective scalarised BO comparison
* S-0078-05 (low) -- Vm-trace deep-dive PNGs for 3 closest cells
* S-0078-06 (low) -- multi-replicate HV uncertainty
* S-0078-07 (low) -- promote t0078 harness to library
* S-0078-08 (medium) -- AIS-disabled-corner failure-mode answer asset

### Independent priority reassessment

The clear architectural arc is now MOBO v3 following S-0078-01: dendritic-spike machinery + NSGA-II
\+ biological hard bounds. This directly tests t0078's headline diagnostic. Three other S-0078
follow-ups (S-0078-02 substrate regression, S-0078-03 tau_ca 200x, S-0078-08 AIS-floor failure-mode
write-up) are natural sub-scope to fold in -- same data, same substrate, related questions. The
cheap analyses (S-0074-01, S-0074-02, S-0067-01, S-0078-05) remain unaddressed and have been carried
forward across multiple brainstorms. t0075 (Bed A AIS one-axis sweep) still hasn't started -- queued
since session 13.

## Clarification Questions

AI: Before I propose specifics, a few questions:
1. Notes / context: Do you have any notes, ideas, or strategic direction that should guide this
   session?
2. MOBO v3 (S-0078-01) framing: Are you committed to the dendritic-spike + NSGA-II direction as the
   next big task? Or do you want to pause MOBO and do cheaper diagnostic tasks first?
3. Budget envelope for next MOBO: $5.01 remains. NSGA-II should be much cheaper than BoTorch at 49-d
   (S-0078-01 estimates $0.50-$1.00). Hard cap?
4. t0075 (Bed A AIS one-axis sweep) -- fish or cut bait. Still want it, fold its scope into MOBO v3,
   or cancel?
5. Cheap unaddressed analyses (S-0074-01, S-0074-02, S-0067-01, S-0078-05): commission any of these
   in this session, or keep deferring?

Researcher: It's option 2. But instead of BO I would like to todo a different algorithm, e.g. some
genetic algorithm. Suggest one.

## Discussion -- Round 1 (Algorithm Recommendation Sub-Round)

AI: To clarify: when you say "Option 2", I'll read it as the second clause of my question 2 -- the
dendritic-spike machinery follow-up as the next big task, just with a non-BO optimiser. Confirm if
I've misread.

GA recommendation: NSGA-II via pymoo. For our specific problem shape -- 49 d, 2 objectives (DSI, PD
rate), bound-constrained continuous parameters, biological hard bounds, ~$1 compute cap -- NSGA-II
is the clearest fit.

Why it lines up:
* Cost: O(N log N) per generation vs BoTorch's O(N^3) Cholesky. Directly fixes the t0078 cost
  blow-up -- pop 64-128 over 30-50 gens stays at $0.50-$1.00 on a 64-core Vast.ai CPU.
* Pareto front output is native -- non-dominated sorting + crowding distance produces the exact
  deliverable shape that t0076/t0078 produced.
* Hard biological bounds are trivial: lower/upper bounds per parameter, enforced by SBX crossover +
  polynomial mutation. No penalty terms, no log-priors. Solves the t0078 AIS-Nav-collapse-to-floor
  failure mode by construction.
* Mature pure-Python implementation in pymoo -- no GPU, no BoTorch/GPyTorch dependency hell.
* Project memory already pointing at it.

Alternatives considered and rejected: MO-CMA-ES (no pymoo first-class implementation), GDE3
(reasonable backup but not better), NSGA-III (only useful for >=4 objectives).

Recommended config: pop 96, 40 generations, SBX crossover (eta=15), polynomial mutation (eta=20),
tournament selection, LHS or Sobol initial population, hard bounds enforced per Kole 2008 / Werginz
2024 priors.

Confirm: NSGA-II in pymoo for the dendritic-spike + AIS-augmented Bed B follow-up, with the
failure-mode write-up (S-0078-08) and substrate regression check (S-0078-02) folded in?

Researcher: Confirm

## Discussion -- Round 1 (Task Proposal)

AI: Confirmed. Moving to Phase 2 Round 1.

Single bundled task: t0080_bedb_mobo_v3_dendritic_spike_nsga2

Source suggestion: S-0078-01

What it does: Add dendritic-spike machinery to the AIS-augmented Bed B substrate from t0078, then
re-optimise with NSGA-II (pymoo) under biological hard bounds. Tests whether the t0078 negative
result is broken by adding active dendrites, or persists even with full active machinery.

Substrate additions on top of t0078's 49-d substrate:
1. Mg-block NMDA on dendrites at active densities (Bed B's existing AMPA-only excitatory channel
   becomes AMPA + Exp2NMDA with voltage-dependent Mg block).
2. Nav1.6 + NaP at distal-dendrite densities sufficient for back-propagating APs and dendritic
   spikes (Sivyer 2013 / Oesch 2005 priors).
3. Hard biological lower bounds per Kole 2008 / Werginz 2024:
   * nav16_ais >= 0.25 S/cm^2 (eliminates the t0078 iter-81 collapse-to-floor failure mode)
   * AIS-to-soma Nav ratio bounded >= 5 (biological plausibility per Werginz 2024's measured 17.3)

Optimiser switch:
* BoTorch qLogNEHVI -> NSGA-II via pymoo
* Pop 96, 40 generations = 3,840 evaluations
* SBX crossover eta=15, polynomial mutation eta=20, tournament selection
* LHS or Sobol initial population
* O(N log N) per generation vs t0078's O(N^3)

Folded-in scope:
* S-0078-02 (substrate regression check): re-evaluate t0076's iter-424 parameter vector on the v3
  substrate as a one-shot validation cell before the NSGA-II run launches.
* S-0078-08 (AIS-disabled-corner failure mode): produce an answer asset documenting the failure mode
  and the biological-prior checklist now enforced as hard bounds.
* (decision needed) S-0078-03: extend tau_ca_multiplier upper bound from 20x -> 200x.

Pass criterion: at least one Pareto cell with DSI >= 0.4 AND PD >= 10 Hz, OR architecturally rule it
out with a clean negative result.

Compute estimate: ~$1.00-$1.50 on Vast.ai 64-core CPU. Hard cap $2.00 to keep budget burn under
control.

Dependencies: t0024, t0069, t0076, t0078

Recommended task types: build-model, experiment-run, answer-question

Expected assets: 1 library asset, 1 answer asset

Questions:
1. Confirm bundled scope -- happy with the three-fold bundle (dendritic-spike + S-0078-02 regression
   \+ S-0078-08 failure-mode answer)?
2. Fold in S-0078-03 (tau_ca_multiplier 200x)? My recommendation: yes. Your call.
3. t0075 (Bed A bio-realistic AIS one-axis sweep) -- still queued. Three options: (a) keep queued
   for later pickup; (b) cancel; (c) run in parallel with t0080.
4. Cheap unaddressed analyses (S-0067-01 NaP DSI=0, S-0074-01 SK polar curves, S-0074-02 NaR
   ND-floor) -- commission as separate tiny tasks now, defer to next brainstorm, or fold into t0080?

Researcher:
1. Confirm
2. Do not add it.
3. a
4. defer

## Discussion -- Round 2 (Suggestion Cleanup)

AI: Confirmed. Moving to Round 2.

Suggestions covered by t0080 (recommend reject):
1. S-0078-01 (high) -- Add dendritic-spike machinery + NSGA-II under AIS Nav lower-bound prior.
   Reason: primary scope of t0080.
2. S-0078-02 (medium) -- Substrate regression check on t0076 iter-424 vector. Reason: folded into
   t0080 as the one-shot validation cell before the NSGA-II run.
3. S-0078-08 (medium) -- Investigate AIS-disabled-corner exploitation as MOBO-on-biophysics failure
   mode. Reason: folded into t0080 as an answer asset documenting the failure mode and the
   now-enforced biological-prior checklist.

Suggestions I considered and propose to keep:
* S-0078-03 (medium, tau_ca_multiplier 200x) -- explicitly excluded from t0080 per your decision
* S-0078-04 (medium, scalarised BO comparison) -- methodological side-quest
* S-0078-05 / S-0078-06 / S-0078-07 (low) -- small follow-ups on existing t0078 data
* S-0076-04 (high, Nav1.6+Kv3 isolation at t0076 best-joint) -- could be re-framed against t0080's
  best-joint cell once available
* All other S-0067-* / S-0070-* / S-0074-* -- mostly Bed-A-side or methodological, not superseded by
  t0080

No reprioritisations proposed. No new suggestions.

Confirm Round 2:
* Reject S-0078-01, S-0078-02, S-0078-08 (3 suggestions, all covered by t0080)?
* Any other suggestions you want pruned, reprioritised, or promoted that I missed?

Researcher: Confirm

## Discussion -- Round 3 (Confirmation)

AI: Confirmed. Moving to Round 3.

New tasks (1):
* t0080_bedb_mobo_v3_dendritic_spike_nsga2 -- Bed B v3 MOBO with dendritic-spike machinery and
  NSGA-II. Source S-0078-01. Dependencies t0024, t0069, t0076, t0078. Compute ~$1.00-$1.50 (cap
  $2.00).

t0080 scope summary:
* Add Mg-block NMDA on dendrites + Nav1.6/NaP at distal-dendrite densities
* Switch optimiser from BoTorch qLogNEHVI to NSGA-II via pymoo (pop 96, 40 gens)
* Enforce hard biological lower bounds (Kole 2008 AIS Nav >= 0.25 S/cm^2; Werginz 2024 AIS-to-soma
  Nav ratio >= 5)
* Fold in S-0078-02 (substrate regression check) and S-0078-08 (failure-mode answer asset)
* Keep tau_ca_multiplier cap at 20x (S-0078-03 NOT folded in)
* Pass criterion: DSI >= 0.4 AND PD >= 10 Hz, OR clean architectural negative result

Suggestions rejected (3):
* S-0078-01 (primary scope of t0080)
* S-0078-02 (folded in as pre-run validation)
* S-0078-08 (folded in as answer asset)

Suggestions reprioritised: 0 Tasks cancelled or updated: 0

Brainstorm-results task: t0079_brainstorm_results_14

Final confirmation requested. Once you say "approve" / "go", the remaining sequence runs without
further interruption: create both task folders (t0079, t0080), write 3 correction files, write the
brainstorm-results task contents, run all four verificators, run the overview materializer, push,
open PR, run pre-merge verificator, merge.

Researcher: Confirm

## Decisions Summary

1. Create t0080 (bedb_mobo_v3_dendritic_spike_nsga2). Bundled Bed B v3 MOBO covering dendritic-spike
   machinery (Mg-block NMDA on dendrites + Nav1.6/NaP at distal), NSGA-II via pymoo (replacing
   BoTorch qLogNEHVI), and hard biological lower bounds per Kole 2008 / Werginz 2024. Folded-in
   scope: S-0078-02 substrate regression check + S-0078-08 AIS-disabled-corner failure-mode answer
   asset. tau_ca_multiplier stays at 20x. Pass criterion: DSI >= 0.4 AND PD >= 10 Hz, OR clean
   architectural negative result. Compute ~$1.00-$1.50 with $2.00 hard cap on Vast.ai 64-core CPU.
   Source suggestion S-0078-01. Dependencies t0024, t0069, t0076, t0078.
2. Reject S-0078-01 -- covered by t0080 (primary scope).
3. Reject S-0078-02 -- covered by t0080 (folded in as one-shot pre-run validation).
4. Reject S-0078-08 -- covered by t0080 (folded in as answer asset).
5. No reprioritisations.
6. No tasks cancelled or updated.
7. t0075 stays queued for later pickup (option a).
8. Cheap unaddressed analyses (S-0067-01, S-0074-01, S-0074-02, S-0078-05) deferred to next
   brainstorm or opportunistic pickup.
