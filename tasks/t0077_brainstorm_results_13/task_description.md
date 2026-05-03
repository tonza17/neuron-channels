# Brainstorm Session 13: Bed B v2 MOBO with AIS, Tier-Stratified Channels, and Slow Kv-AHP

Thirteenth brainstorming session. Run on 2026-05-03 after t0074 (channel tuning-width sweep on Bed
A) and t0076 (25-d Bed B BoTorch qNEHVI multi-objective Bayesian optimisation) both completed. The
session is triggered by the t0076 headline negative result: the bare 25-d Bed B (de Rosenroll 2026)
substrate cannot reach a biologically realistic joint operating point of DSI >= 0.4 AND PD rate >=
30 Hz, with every Pareto cell trading off severely between the two objectives. The t0076
compare-literature analysis identified three architectural omissions that plausibly explain the
trade-off: (a) no AIS section, (b) uniform-density channels rather than tier-stratified densities
(real RGCs have ~50x higher Nav at AIS than soma per Kole 2008), and (c) absent slow-AHP machinery
to cap the high-rate Pareto extremes (iter 319 reached 127.75 Hz with DSI = 0.003).

## Decisions

* **Create t0078** — `bedb_mobo_v2_ais_tiered_ahp`. Bed B v2 multi-objective Bayesian optimisation
  that bundles three high-priority follow-ups in a single run: build an AIS section onto Bed B (S-0
  076-02; covers S-0024-03 as the AIS library asset), tier-stratify channel densities into 5 tiers
  per Nav1.6 / Kv3 / NaP / BK / SK (S-0076-01), and add a slow Kv-mediated AHP via SK_E2 with
  extended Ca-binding as a new optimisation parameter (S-0076-05). Migrate the BoTorch loop to
  qLogNEHVI, wrap GP inputs in Normalize on [0, 1]^d, and fix the NEURON
  `Exp2NMDA name already exists` re-init bug via subprocess-per-deep-dive (covers S-0076-03). 40 -
  50 d total parameter space. Restart fresh with Sobol DoE + qLogNEHVI (no warm-start from t0076).
  Pass criterion: locate at least one Pareto cell with DSI >= 0.4 AND PD rate >= 30 Hz, OR rule it
  out architecturally. Compute estimate ~$2.50 - $4.00 over 9 - 12 h on a Vast.ai 72-core CPU (well
  within the $8.94 remaining budget). Source suggestion: S-0076-02 (declared primary; S-0076-01,
  S-0076-03, S-0076-05, and S-0024-03 also covered).

* **Cancel t0045** — `coreneuron_vastai_speedup_benchmark`. The task was originally framed as the
  5x CoreNEURON-on-GPU vs stock-NEURON-on-CPU benchmark to validate the assumption baked into
  t0033's cost model. t0076 has now actually run on a Vast.ai 72-core CPU instance for $1.0583 over
  6.4697 h with 68,800 NEURON simulations and produced useful science, validating that stock NEURON
  on Vast.ai CPU is cost-feasible for the project's scale. The original urgency (the t0033
  cost-model uncertainty) is gone, and CoreNEURON-on-GPU is no longer load-bearing for any planned
  task. The benchmark retains academic interest but is not on the project's critical path.

## Suggestion Cleanup

* **Reject four high-priority suggestions** as covered by t0078:

  * **S-0076-01** — tier-stratified channel densities. Folded into t0078 as the 5-tier expansion
    of the input space.
  * **S-0076-02** — AIS-augmented Bed B MOBO. Primary scope of t0078.
  * **S-0076-03** — three implementation fixes (qLogNEHVI migration, GP input normalisation,
    NEURON re-init bug). Folded into t0078 as required infrastructure for the new MOBO to run
    cleanly.
  * **S-0076-05** — slow Kv-mediated AHP mechanism. Folded into t0078 as the new optimisation
    parameter; SK_E2 with extended Ca-binding chosen as the implementation per researcher decision.

* **Reject one medium-priority suggestion** as covered by t0078:

  * **S-0024-03** — Van Wart + Werginz AIS overlay on the deRosenroll morphology. The AIS section
    construction is part of t0078's scope; the resulting AIS-augmented Bed B will be registered as a
    new library asset by t0078 (`de_rosenroll_2026_dsgc_ais` or similar).

* **Reject eleven high-priority suggestions** as stale (from-scratch DSGC family, t0052 - t0059):
  the project has pivoted to deposited Bed A (t0008) and Bed B (t0024) substrates where biological
  grounding is stronger. Recent work (t0067 - t0076) operates exclusively on the deposited beds. The
  from-scratch family remains in a binary regime (single-spike-trivial-DSI or
  full-suppression-zero-DSI) and these eleven follow-ups are no longer load-bearing for the
  project's research questions.

  S-0052-01 (AMPA per-synapse conductance sweep on t0052), S-0052-02 (GABA-synapse-count sweep on
  t0052), S-0054-02 (3D gAMPA / gNMDA / gGABA sweep on t0054), S-0055-02 (re-run t0055 Mg-block
  sweep on corrected protocol), S-0055-03 (GABA-reduction ladder on Mg-block t0055), S-0057-06
  (tonic GABA + Mg-block NMDA on t0054-style), S-0059-01 (active dendritic conductances on t0059),
  S-0059-02 (Mg-block NMDA + bar-locked tonic GABA on t0059), S-0059-03 (synapse-count scaling on
  t0059), S-0065-02 (match from-scratch GABA reversal to v_rest), S-0066-02 (EPSP / IPSP / FULL
  protocol on from-scratch family).

## Tasks Cancelled or Updated

* **Cancelled**: t0045 (CoreNEURON benchmark; superseded by t0076 actual Vast.ai run).
* **Updated**: none.

## Assets Produced

No assets in this brainstorm task. The new task t0078 will produce one library asset (the
AIS-augmented Bed B variant) plus the standard results bundle (Pareto front, hypervolume trajectory,
metrics, cost record, machine log) when executed downstream.
