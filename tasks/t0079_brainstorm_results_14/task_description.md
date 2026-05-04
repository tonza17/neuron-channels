# Brainstorm Session 14: Bed B v3 MOBO with Dendritic-Spike Machinery and NSGA-II

Fourteenth brainstorming session. Run on 2026-05-04 after t0078 (49-d Bed B v2 BoTorch qLogNEHVI
multi-objective Bayesian optimisation with AIS, tier-stratified channels, and slow Kv-AHP)
completed. The session is triggered by t0078's headline architectural diagnostic: the AIS-augmented
49-d substrate expanded the achievable Pareto front by **+36% in hypervolume** over t0076 but still
missed the joint pass criterion of `DSI >= 0.4 AND PD rate >= 10 Hz` (closest cell iter 81: DSI
0.316 / PD 9.68 Hz, short by 0.084 on DSI and 0.32 Hz on PD). The compare-literature analysis
identified two follow-on diagnostics: (a) the high-DSI rail's PD ceiling pinned at ~2.86 Hz across
109 acquisitions signals the missing **dendritic-spike machinery** (Mg-block NMDA at active
densities on dendrites + Nav1.6 / NaP at distal-dendrite densities for back-propagating APs); (b)
the iter-81 closest-to-joint cell collapsed AIS Nav to the search-space floor (1e-5 S/cm^2, four
orders below the Kole 2008 patch-clamp prior of 0.25 - 0.5 S/cm^2) -- a generalisable
MOBO-on-biophysics failure mode where the optimiser exploits an AIS-disabled corner that contradicts
REQ-2 / REQ-3 / REQ-4's biological intent.

## Decisions

* **Create t0080** -- `bedb_mobo_v3_dendritic_spike_nsga2`. Bed B v3 multi-objective optimisation
  that bundles three follow-ups in a single run: (a) add **dendritic-spike machinery** to the t0078
  AIS-augmented substrate (Mg-block NMDA at active densities on dendrites; Nav1.6 + NaP at
  distal-dendrite densities sufficient for back-propagating APs and dendritic spikes per Sivyer 2013
  / Oesch 2005 priors); (b) switch the optimiser from BoTorch qLogNEHVI to **NSGA-II via pymoo**
  (pop 96, 40 generations, SBX crossover eta=15, polynomial mutation eta=20, tournament selection,
  LHS or Sobol initial population) eliminating O(N^3) GP-fit scaling that pushed t0078 to $3.93 at
  60% of planned acquisitions; (c) enforce **biological hard lower bounds** per Kole 2008 / Werginz
  2024 priors (`nav16_ais` >= 0.25 S/cm^2; AIS-to-soma Nav ratio >= 5) to eliminate the t0078
  iter-81 collapse-to-floor failure mode by construction. Folded-in scope: (i) S-0078-02 substrate
  regression check by re-evaluating the t0076 iter-424 parameter vector on the v3 substrate as a
  one-shot validation cell before the NSGA-II run launches; (ii) S-0078-08 produces an answer asset
  documenting the AIS-disabled-corner failure mode and the now-enforced biological-prior checklist.
  `tau_ca_multiplier` upper bound is kept at 20x (S-0078-03 NOT folded in per researcher decision,
  to keep the substrate identical to t0078 for cleaner architectural-delta comparison). Pass
  criterion: locate at least one Pareto cell with DSI >= 0.4 AND PD rate >= 10 Hz, OR rule it out
  architecturally with a clean negative result. Compute estimate ~$1.00 - $1.50 over ~0.8 - 1.2 h on
  a Vast.ai 64-core CPU; hard cap $2.00. Source suggestion: S-0078-01 (declared primary; S-0078-02
  and S-0078-08 also covered). Dependencies: t0024, t0069, t0076, t0078.

## Suggestion Cleanup

* **Reject three suggestions** as covered by t0080:

  * **S-0078-01** (high) -- Add dendritic-spike machinery and re-optimise with NSGA-II under an AIS
    Nav lower-bound prior. Primary scope of t0080.
  * **S-0078-02** (medium) -- Substrate regression check by re-evaluating t0076 iter-424 parameters
    on the AIS-augmented 49-d Bed B substrate. Folded into t0080 as a pre-run validation cell.
  * **S-0078-08** (medium) -- Investigate AIS-disabled-corner exploitation as a general
    MOBO-on-biophysics failure mode. Folded into t0080 as an answer asset documenting the failure
    mode and the now-enforced biological-prior checklist.

## Reprioritisations

None.

## Tasks Cancelled or Updated

* **Cancelled**: none.
* **Updated**: none.
* t0075 (Bed A bio-realistic AIS one-axis sweep) remains queued for later opportunistic pickup; it
  uses a different substrate (Bed A) from t0080 and provides complementary one-axis-at-a-time
  sensitivity vs t0080's joint optimisation.

## Assets Produced

No assets in this brainstorm task. The new task t0080 will produce one library asset (the
dendritic-spike-augmented Bed B v3 variant) plus one answer asset (the AIS-disabled-corner
failure-mode write-up) and the standard results bundle (Pareto front, hypervolume trajectory,
metrics, cost record, machine log) when executed downstream.
