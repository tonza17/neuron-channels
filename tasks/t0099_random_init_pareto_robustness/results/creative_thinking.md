# Creative Thinking: Out-of-the-Box Reading of t0099 Results

## What this task actually measured

Three random-init NSGA-II runs (no anchor warm-start) on the same 68-d substrate t0091 used.
Per-seed Pareto: 19, 22, 14 cells. Strict joint-pass count per seed: 0, 0, 0. The strongest
read of the warm-start question is: **t0091's warm-start is what got it the joint-pass cell**,
because three independent random-init seeds in 5–8 generations (with seed 22 going 1.6× deeper
than t0091 and 4× more compute) all failed to find one.

But the task surfaced four observations that reframe the question.

## 1. Symmetric anchor count = 0 in every seed (including t0091)

The symmetric anchor is the only one that drops to zero in **all four** datasets:

| Dataset | bedb_like | symmetric | pd_asymm | nd_asymm | alt_topology |
| --- | --- | --- | --- | --- | --- |
| t0091 | 20 | **0** | 12 | 9 | 16 |
| seed 11 | 2 | **0** | 7 | 5 | 5 |
| seed 22 | 4 | **0** | 4 | 2 | 12 |
| seed 33 | 1 | **0** | 9 | 0 | 4 |

This is independent of warm-start. The anchor classifier projects each Pareto cell to its
nearest of the 5 t0091 anchor centroids, and *no random-init Pareto cell ever lands closest
to the symmetric morphology*. Same conclusion the t0091 creative-thinking step reached, now
reproduced under random init: **the substrate's electrophys + spatial inhibition needs some
morphological asymmetry to produce DS-relevant cells**, regardless of where you start the
search. Symmetric morphologies are dominated everywhere on the joint Pareto.

## 2. Different seeds prefer different anchors

The anchor-domination patterns disagree across seeds:

* Seed 11 favours `pd_asymmetric` (7) and ties `nd_asymmetric` and `alt_topology` (5 each)
* Seed 22 strongly prefers `alt_topology` (12 of 22 cells)
* Seed 33 strongly prefers `pd_asymmetric` (9 of 14 cells)

This is **not** what reproducibility would look like. If random-init NSGA-II were finding the
same convex Pareto from different starting points, the anchor distributions would converge.
They don't — at 5–8 gens we're looking at three different *local* Paretos, each clustered
near a different morphological basin. **Three seeds aren't yet enough to claim NSGA-II has
explored the global Pareto** for this 68-d problem.

## 3. The PD-rate axis is what the optimizer struggles to bridge

The optimizer easily finds:
* Cells with DSI ≈ 1.0 (extreme tuning) at PD ≈ 0 Hz (artifacts of low firing)
* Cells with PD ≈ 35–47 Hz (high firing) at DSI ≈ 0 (omnidirectional)

It almost never finds cells in the joint-pass corner (DSI ≥ 0.5 AND PD ≥ 30 Hz). Seed 22's
lone exception was DSI=0.49 / PD=18.7 / robust=0.98 at gen 8 — it crossed the DSI threshold
but only got halfway to the PD threshold. **t0091's warm-start anchor 1 (Bed-B-like) seeds
the optimizer with cells that already fire at 30+ Hz**, so NSGA-II's job is just to climb DSI
without losing PD-rate. Random init has to find both axes simultaneously.

This is a stronger and more falsifiable claim than the loose "warm-start was load-bearing":
**warm-start was load-bearing specifically for the high-PD-rate dimension**. A future
experiment could test this directly by warm-starting only with anchor 1 (skip the other 4)
and seeing whether the joint-pass cell still emerges.

## 4. Per-gen wall-clock doubled across the run — diagnostically useful

| Gen | Seed 22 wall-clock | Seed 33 wall-clock |
| --- | --- | --- |
| 1 | 52 min | 28 min |
| 4 | 89 min | 87 min |
| 6 | 107 min | 222 min |
| 8 | 167 min | — |

This isn't a bug, it's a **selection pressure side-effect**: NSGA-II selects for cells that
stably fire across all 16 directions × 5 seeds, and high-firing-rate cells require finer
NEURON CVODE adaptive time-stepping. Late-gen survivors fire faster and take longer to
simulate. Three implications:

* **Future task budgets must scale super-linearly with generation count.** Estimating
  $X/gen × N gens underestimates real cost by ~50%.
* **Restarting NEURON workers between gens** (currently they live for the whole run) might
  reclaim 10–20% of late-gen wall-clock if there's any state accumulation.
* **A coarser `dt` for inter-spike intervals** could reduce per-cell simulation cost without
  affecting DSI or robust metrics that depend on spike counts, not fine spike timing. Could
  be a 30–50% speedup with negligible accuracy loss.

## What this run did NOT test

1. **Longer random-init runs.** With $5/seed cap and 8 gens, seeds 22/33 hit the max-gen
   termination, not HV plateau. We don't know if 12–20 generations would let random-init
   bridge the joint-pass gap. A future experiment could give one seed $10 and 20 gens.

2. **Hybrid warm-start.** Anchor 1 only (Bed-B-like) vs all 5 anchors vs random init.
   Three-way comparison would isolate which part of t0091's warm-start did the work.

3. **Different init samplers.** Sobol' / Halton low-discrepancy sequences vs LHS vs uniform
   random. LHS is good but maybe not optimal; the rall_exponent axis was sampled in [~0, 5]
   wider than t0091's [0.5, 2.0] bounds (a setup transcription difference flagged in the
   implementation step), so part of seed 11's poor performance may be explained by exploring
   that wider parameter range.

4. **Population diversity tracking.** NSGA-II preserves Pareto diversity but doesn't
   explicitly track population convergence. A diversity metric (e.g., per-generation 14-d
   morphology variance) would tell us whether random-init seeds 22/33 are still exploring at
   gen 8 or already collapsed to a small region.

## Practical follow-up recommendation

Given 3 seeds of random-init evidence, the cheapest next experiment is **anchor-1-only
warm-start** (test #2 above): launch NSGA-II with all 96 cells initialised as Bed-B-like
anchor variants (no symmetric/PD-asymm/ND-asymm/alt-topology). Cost ~$3.50 single seed × 8
gens. If this finds the joint-pass cell, then anchor 1 alone was load-bearing — the other 4
anchors were decoration. If it doesn't, then **the diversity of the 5-anchor warm-start was
itself the load-bearing factor** — t0091's joint-pass cell required the population to be
seeded across multiple morphological basins, not just one. Either outcome substantially
narrows the design question for future morphology-extended NSGA-II runs.
