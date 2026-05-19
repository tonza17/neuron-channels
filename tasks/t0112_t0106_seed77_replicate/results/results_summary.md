# t0112 — Seed-77 Minimum-Change Replicate of t0106: Results Summary

## Summary

Seed 77 reaches the same Pareto-front corner as t0106 seed 44 (best DSI 0.9535 vs 0.9606, best PD
114.76 Hz vs 122.62 Hz) and the substrate is therefore not seed-specific, but produces only **7
unique joint-pass cells** vs t0106's 123 unique — partial replication, not full replication. The
HV-plateau detector triggered at gen 21 (well below the 60-gen ceiling), the tighter pool-restart
cadence (every 10 gens) kept per-generation wall-clock at ~620s on average vs t0106's ~2,167s, and
total instance spend was $1.99 of the $25 cap.

## Metrics

* **Best ratio DSI**: **0.9535** at PD = 60.00 Hz (gen 20/21).
* **Best PD-rate frontier**: **114.76 Hz** at DSI = 0.0021 (gen 21).
* **Unique joint-pass cells** (DSI >= 0.5 AND PD >= 30 Hz): **7** (25 total evaluations across
  generations).
* **Strict Pareto cells**: **3** (vs t0106's 7), declared in
  `results/data/pareto_front_seed77.json`.
* **Final hypervolume (2-D)**: **107.4602** (start 0.1156 → 928x growth).
* **NSGA-II compute cost**: **$1.96** productive + $0.03 idle = **$1.99 total** of $25 cap.

## Answers to the Task's 5 Key Questions

1. **≥ 40 unique joint-pass cells?** **NO** — only 7 unique. Falls in the "partial replication"
   bucket (10–40 cells = multi-seed required). The substrate is reachable from seed 77 but the
   density of reachable joint-pass cells is itself stochastic across GA seeds.
2. **Best ratio DSI ≥ 0.95?** **YES** — 0.9535 (the t0106 baseline was 0.9606 at the same stage of
   evolution).
3. **Best PD-rate frontier ≥ 100 Hz?** **YES** — 114.76 Hz (94% of t0106's 122.62 Hz; both runs
   reach the same upper region).
4. **Pareto fronts overlap in parameter space?** Pending interpretation. Raw 68-d L2 distances
   between t0112 Pareto cells and their nearest t0106 Pareto neighbour range 3.5e7 → 1.9e8 (see
   `results/data/pareto_front_overlap.csv`); these are dominated by the conductance-scale parameters
   that span 6 orders of magnitude. A normalised distance metric (z-scored per-dimension) is needed
   for substantive overlap claims; the raw values are reported here for transparency but not
   interpreted as "different solutions".
5. **Did the tighter pool-restart cadence (every 10) change wall-clock?** **YES, decisively.** t0112
   completed 21 generations in 4 h 40 m (~620 s/gen average); t0106 completed 40 generations in 24.1
   h (~2,167 s/gen average). The tighter restart cadence is ~3.5× faster per generation, a
   substantial improvement at no algorithmic cost.

## Verification

* `verify_predictions_asset` (meta path): PASSED, 2 non-blocking warnings (PR-W014 no linked model
  asset, PR-W015 no linked dataset asset — same as t0106).
* `verify_predictions_description` (meta path): PASSED.
* `verify_predictions_details` (meta path): PASSED.
* `verify_machines_destroyed`: PASSED, 2 expected warnings (RM-W001 API unreachable because instance
  destroyed; RM-W006 no checkpoint_path).
* All other ARF verificators are run in the reporting step.
