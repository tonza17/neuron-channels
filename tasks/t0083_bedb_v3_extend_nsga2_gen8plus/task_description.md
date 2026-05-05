# Extend t0081 NSGA-II from gen-7 with Adaptive HV-Plateau Stop

## Motivation

t0081 (`bedb_v3_warmstart_nsga2`) delivered the project's first joint-pass cell at gen 7 cell 767
(DSI 0.494 / PD 11.39 Hz) on a 16-cell Pareto front across 768 evaluations ($2.39 on Vast.ai 64-core
EPYC 7B13, $0.2382/hr). Three observations from t0081's results motivate continuing the run:

1. **Hypervolume grew monotonically with no plateau**: 6.59 (gen 0) -> 8.99 (gen 1) -> 9.24 (gen 2)
   -> 11.08 (gen 3) -> 11.57 (gen 4) -> 13.14 (gen 5) -> 15.22 (gen 6) -> 16.33 (gen 7). The 7.4%
   increase from gen 6 to gen 7 indicates the Pareto front is still actively expanding; the
   optimiser stopped not because it converged but because the planned gen=8 budget ran out.

2. **Single joint-pass cell out of 768 evaluations.** Cell 767 is the only cell in the (DSI >= 0.4
   AND PD >= 10 Hz) box. The pass region of the parameter space is **discovered but not
   characterised**. A neighbourhood cluster (cell 637 at distance 0.063, cell 762 at distance 0.086)
   sits just outside the box. Additional generations should populate this cluster and produce more
   joint-pass cells.

3. **The natural extension preserves t0081's evolutionary trajectory.** Continuing from t0081's
   gen-7 final population (96 surviving individuals after RankAndCrowding survival) avoids the cost
   of re-evaluating the warm-start initial population and lets NSGA-II continue evolving from a
   known good state.

This task addresses project research question **Q4** (active vs passive dendritic conductances on
directional tuning sharpness) by extending the search budget on the v3 dendritic-spike-augmented Bed
B substrate that t0081 established as the project's working substrate. Source suggestion:
**S-0081-02** (extend t0081 NSGA-II to gen 12-15).

## Scope

### In scope

* Reuse t0081's harness (`tasks/t0081_bedb_v3_warmstart_nsga2/code/`) verbatim with two
  modifications:
  * Replace the Sobol/LHS + projected-Pareto warm-start init with a direct load of t0081's gen-7
    final population (96 individuals, with objective values pre-computed and re-injected into
    pymoo's `Algorithm` state to skip re-evaluation).
  * Add an **adaptive HV-plateau watchdog** that terminates NSGA-II when
    `(HV(gen N) - HV(gen N-3)) / HV(gen N-3) < 0.01` averaged over the last 3 generations, AND only
    after a minimum of **5 additional generations** has been run (i.e., earliest possible stop is
    gen 12). The watchdog evaluates after every generation starting at gen 11 (so gen 11 needs HV
    from gens 8, 9, 10, 11 -- a 3-gen lookback window starting at gen 8 is the first eligible
    window).
* Hard cap on total additional generations: **10** (gen 8 through gen 17 maximum). If the watchdog
  never fires, terminate at gen 17.
* Hard cost cap: **$5.00**. Spawn a budget watchdog identical to t0081's that monitors
  `instance_lifetime_hr * $0.2382/hr` and forces graceful termination if the projected
  end-of-generation cost would exceed $5.00.
* Reuse the `de_rosenroll_2026_dsgc_ais_dendritic_spike` library asset from t0080 unchanged. No
  substrate changes.
* Same Vast.ai instance class as t0081 (AMD EPYC 7B13 64-core, 503 GB RAM, $0.2382/hr).
* Compare final Pareto front, joint-pass cell count, HV trajectory, and per-generation
  parameter-distribution diagnostics against t0081 and t0080 baselines.

### Out of scope

* Substrate changes (no new dendritic-spike parameters; no new channels; no AIS modifications).
* Optimiser changes (NSGA-II via pymoo only; no NSGA-III, hybrid, or BO comparison).
* Multi-replicate confirmation (S-0081-01 covers that; deferred to a later task).
* Vm-trace analysis of cell 767 (S-0081-03 covers that; addressed in t0084 in parallel with this
  task).
* Bed A cross-bed replication (S-0081-05).

## Pass Criteria

* **Primary**: at least one **additional** Pareto cell with `DSI >= 0.4 AND PD >= 10 Hz` beyond
  t0081's cell 767 (i.e., total joint-pass cells
  > = 2). Characterises the joint-passing region by populating the near-pass cluster (cells 637 and
  > 762 from t0081 should evolve into the joint-pass box if the cluster is robust).

* **Secondary**: HV trajectory continues monotonically; final HV > t0081's 16.33; HV-plateau stop
  rule fires before the gen-17 hard cap OR the budget watchdog fires.

* **Acceptable negative**: zero additional joint-pass cells but final HV
  > t0081's 16.33 with HV-plateau detected before gen 17 -- documented as evidence that t0081's cell
  > 767 is an isolated point in the parameter space rather than a cluster, with implications for
  > downstream multi-replicate strategy.

## Estimated Compute Cost

* Per-cell wall-clock on t0081's instance: ~30 s (768 cells / 10.045 h instance lifetime ~= 47
  s/cell including overhead; NSGA-II gen 7 cells averaged ~30 s each).
* 5 additional generations at pop 96 = 480 cells @ 30 s = 4.0 h optimiser time; with 30 min Vast.ai
  instance overhead = 4.5 h * $0.2382 = ~$1.07.
* 10 additional generations at pop 96 = 960 cells @ 30 s = 8.0 h optimiser time; with overhead = 8.5
  h * $0.2382 = ~$2.02.
* Most-likely range: **$1.50 - $3.00** depending on when the HV-plateau rule fires.
* **Hard cost cap: $5.00** (allows up to ~21 hours of instance lifetime, enough to absorb any
  per-cell wall-clock variance from the v3 substrate's dendritic-spike machinery).

## Dependencies

* **t0081_bedb_v3_warmstart_nsga2**: provides gen-7 final population (96 individuals with parameter
  vectors and objective values), the NSGA-II harness to extend, and the warm-start projection logic
  to inherit unchanged.
* **t0080_bedb_mobo_v3_dendritic_spike_nsga2**: provides the
  `de_rosenroll_2026_dsgc_ais_dendritic_spike` library asset (54-d v3 substrate) used unchanged.
* **t0078_bedb_mobo_v2_ais_tiered_ahp**: provides the AIS-augmented parent substrate from which
  t0080 derived the v3 substrate.
* **t0024_port_de_rosenroll_2026_dsgc**: provides the de Rosenroll 2026 DSGC NEURON port (Bed B base
  substrate before AIS / dendritic-spike augmentation).

## Recommended Task Types

* `experiment-run` -- the primary mode (NSGA-II continuation).

## Notes

The watchdog logic must be additive, not destructive: each new generation appends to t0081's saved
evaluation history rather than overwriting it. The final `all_evaluations.json` should contain the
union of t0081's 768 cells plus this task's additional cells (480-960), with consistent generation
numbering (t0081 ends at gen 7; this task starts at gen 8).
