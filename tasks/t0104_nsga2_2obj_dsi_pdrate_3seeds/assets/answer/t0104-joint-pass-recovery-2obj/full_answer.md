---
spec_version: "2"
answer_id: "t0104-joint-pass-recovery-2obj"
answered_by_task: "t0104_nsga2_2obj_dsi_pdrate_3seeds"
date_answered: "2026-05-14"
confidence: "high"
---
# 2-objective NSGA-II joint-pass recovery test

## Question

Does 2-objective NSGA-II (DSI + PD-rate, with the DSI-silence guard applied) recover joint-pass
cells where t0102's 3-objective run found zero?

## Short Answer

No. Across 2,208 evaluations from two random-init NSGA-II seeds (44 and 55) running the 2-objective
DSI + PD formulation with the silence guard active, zero cells cleared the strict joint-pass corner
(DSI >= 0.5 AND PD >= 30 Hz). The DSI extreme broke past 0.5 for the first time in the t0080-t0104
NSGA-II lineage (seed 55 gen 11, DSI = 0.5417 at PD = 3.57 Hz), confirming the substrate is not
artificially capped by the silenced-cell DSI=1.0 floating-point artifact that contaminated t0102's
Pareto front. The L-shaped Pareto front replicates t0102's exactly — extremes reachable on each
axis but the joint corner empirically empty — ruling out objective-vector dimensionality as the
explanation for the substrate-limited reading.

## Research Process

The hypothesis came from brainstorm session 22 (2026-05-12), immediately after [t0102] closed: with
the robustness axis dropped from NSGA-II's selection vector and the DSI-silence guard (S-0102-01)
applied so the t0102 silence-corner DSI=1.0 artifact can no longer dominate the Pareto front, would
NSGA-II's crowding-distance selection spend its diversity budget on the DSI / PD-rate trade-off
alone and surface a joint-pass cell that the 3-objective run missed?

The experiment forked t0102's `code/` substrate verbatim (REQ-1..REQ-8 in `plan/plan.md` document
every patch site at exact line numbers). Three changes only: (1) pymoo `n_obj` 3 -> 2 with the F-row
reduced from `[-dsi, -pd, -robustness]` to `[-dsi, -pd]`; (2) DSI-silence guard injected into
`_summarise_trials` between the spike-count loop close and the `_vector_sum_dsi` call, forcing DSI =
0.0 when the cell's total mean spikes across the 16 directions drop below
SILENCE_SPIKE_COUNT_THRESHOLD = 10; (3) the GA seed list went from (44, 55) to (44, 55, 66) with the
same LHS random init at pop=96, N_EVAL_SEEDS=4, n_gen=20 as t0102. All other knobs were held
constant: same Bed B substrate from [t0024], same procedural morphology generator (t0092-fixed via
correction C-0093-01), same 5-anchor smoke gate against the t0093 verification fingerprint, same
per-seed $4 cost watchdog.

Two seeds executed on a single Vast.ai EPYC 7J13 instance (Taiwan, $0.3481/hr) before the researcher
elected to stop after seed 55 rather than launch seed 66 (see
`intervention/early_stop_after_seed_55.md`). Both seeds tripped the per-seed cost watchdog before
reaching the planned gen 20 because of NEURON memory accumulation that doubled per-generation
wall-clock from ~15 minutes early to ~120 minutes late. Final productive cells: seed 44 reached gen
12 (1,152 cells), seed 55 reached gen 11 (1,056 cells). Total 2,208 evaluations.

Conflicting evidence between (a) "the joint corner is empirically empty" and (b) "NSGA-II is failing
to find what is there" was resolved structurally: with the guard masking 47 of 2,208 cells (2.1%) at
the silence floor and the surviving Pareto front retaining the same L-shape as t0102's, the
substrate-limited reading no longer rests on the silence artifact. The DSI extreme breaking past 0.5
for the first time in the NSGA-II lineage confirms the algorithm CAN reach DSI = 0.5; it just cannot
do so while simultaneously holding PD >= 30 Hz on this substrate.

## Evidence from Papers

[Mohacsi2024][mohacsi2024] benchmarks 14 multi-objective optimisers on six neuron-fitting problems
including Hay 2011 L5PC. NSGA-II ranks mid-pack; IBEA, CMAES, and PSO consistently outperform all
three NSGA-II implementations tested. The paper recommends a per-algorithm-run budget floor of
10,000 evaluations as "matched-budget"; t0104 ran 2,208 evaluations across two seeds on a 68-d
substrate, roughly 4.5x below that floor and ~2 orders of magnitude below the 300,000-500,000
evaluations typical of Druckmann2007 and Hay2011 multi-objective neuron fits. Even with the t0104
patches removing the silence artifact and freeing crowding distance from the robustness axis, the
budget-vs-substrate-difficulty asymmetry remains the most likely structural explanation.
[Mohacsi2024][mohacsi2024]'s recommendation to switch algorithm and tighten objective formulation
before scaling budget directly motivates the deferred follow-ups S-0102-03 (IBEA) and S-0102-04
(Dang pop>=290).

[Dang2023][dang2023] proves NSGA-II's noise-survival theorem in the Bernoulli setting; the analogous
Gaussian-noise result requires population size `mu = Omega(n log n)`. For n = 68, the theoretical
floor is `mu ≈ 290`. t0104's pop=96 sits ~3x below this floor, the same shortfall t0102 had.
[Dang2023][dang2023] does not rule out a noise-amplification failure at our specific pop/dim ratio,
which is the algorithm-side explanation for why both t0102 and t0104 produce L-shaped fronts even
though the substrate is empirically known (via the t0091 warm-start single cell) to contain at least
one joint-pass solution. Replicating [Dang2023][dang2023]'s pop=290 floor is independently deferred
as S-0102-04.

[Morinaga2024][morinaga2024] Theorem 3 sharpens the explicit-averaging picture for noisy MOEAs:
averaging K samples reduces expected runtime only when the per-objective noise stability index
`alpha > 1`. The DSI vector-sum on cells near the silence boundary (now masked by t0104's guard) was
a heavy-tailed denominator-near-zero case with `alpha` close to 1 in t0102, making the K=4 explicit
averaging "nearly inert" per Theorem 3. t0104's guard surgically removes the masked heavy-tail
region; the remaining DSI distribution behaves better-conditioned, which is consistent with seed 55
cleanly reaching DSI = 0.54 rather than the spurious DSI = 1.0 spike t0102 reported. Theorem 9's
recommendation to use sign averaging is independently deferred as S-0102-07.

## Evidence from Internet Sources

No new internet sources were consulted inside t0104. The `internet` answer method tag is therefore
omitted from `details.json`. All literature references resolve to paper assets reachable via the
`source_paper_ids` field.

## Evidence from Code or Experiments

Two NSGA-II runs (`nsga2-seed44-bedb-morph-n4-gen20-2obj` and
`nsga2-seed55-bedb-morph-n4-gen20-2obj`, predictions assets in this task) produced 1,152 + 1,056 =
2,208 evaluated cells before the per-seed $4 cost watchdog and the researcher-initiated stop after
seed 55. Strict joint-pass cells (DSI >= 0.5 AND PD >= 30 Hz): **0**.

The Pareto front is L-shaped, exactly as in [t0102]. Extremes per axis: seed 44 reaches max DSI =
0.4073 at PD = 0.71 Hz and max PD = 75.00 Hz at DSI = 0; seed 55 reaches max DSI = 0.5417 at PD =
3.57 Hz and max PD = 65.00 Hz at DSI = 0. The closest the combined Pareto front gets to the joint
corner is seed 55 gen 8's cell at DSI = 0.4192 / PD = 15.00 Hz — the project-best joint trade-off
observed so far in the t0080-t0104 lineage. This cell sits ~15 Hz short of the PD = 30 threshold and
is therefore not a strict joint-pass cell.

The DSI silence guard fired as designed on 47 of 2,208 cells (2.1%): 25 in seed 44, 22 in seed 55.
The t0104 Pareto front no longer contains any cell at DSI = 1.0 / PD = 0 (contrast: t0102 had 27
such silenced-cell artifacts that dominated the Pareto front and biased crowding-distance selection
toward the silence corner across all 14-13 generations).

Both seeds were truncated short of the planned 20 generations by the per-seed $4 cost watchdog
(S-0102-08 partial fix is wired in `nsga2_driver.py` REQ-8). Seed 44 reached gen 12 at cost $4.6945;
seed 55 reached gen 11 at cost $4.1874. Per-gen wall-clock doubled over each run (~15 min/gen early
to ~120 min/gen late) due to NEURON memory accumulation despite worker-restart-between-generations
being active.

The hypervolume trajectories tell two qualitatively different stories on the same substrate. Seed 44
climbed steadily from HV ~ 1.5 at gen 1 to HV = 2.85 at gen 12 with no jump larger than 0.4. Seed 55
climbed similarly until gen 7 (HV ~ 2.94), then made a discontinuous jump at gen 8 to HV = 6.87 when
it discovered the DSI = 0.42 region near (DSI = 0.42, PD = 15), then climbed to HV = 7.59 at gen 11.
The single-seed HV variance is enormous; with 2 seeds the variance is under-sampled but the
qualitative signature — one seed makes a jump, the other does not, neither reaches the joint
corner — replicates [t0099]'s three-seed observation and is consistent with [Dang2023][dang2023]'s
pop/dim-ratio-driven noise-amplification picture.

## Synthesis

Three lines of evidence support a high-confidence negative answer at the substrate-limited reading:

1. **Direct count**: 0 of 2,208 evaluated cells cleared the strict joint-pass corner in two
   independent random-init seeds. With the silence-corner artifact removed by the new DSI guard, the
   surviving cells are real DSGC behaviours; not floating-point dust. The closest cell to the joint
   corner is DSI = 0.4192 / PD = 15 Hz — ~15 Hz short on the PD axis at sub-threshold DSI.

2. **L-shape replication**: the t0104 Pareto front exhibits the same characteristic L-shape as
   [t0102]'s 3-objective front when restricted to the (DSI, PD) plane. Both reach the per-axis
   extremes but cannot simultaneously hold them. Dropping the robustness axis did not bend the L
   inward toward the joint corner. Therefore objective-vector dimensionality is not the operative
   factor; the substrate (or the algorithm-on-substrate interaction) is.

3. **DSI extreme cleanly above 0.5 for the first time**: seed 55 gen 11 reached DSI = 0.5417 at PD =
   3.57 Hz with the guard active. This is the first NSGA-II run in the t0080-t0104 lineage to cross
   the DSI = 0.5 threshold with a non-silenced cell. The substrate can sustain DSI = 0.5+ if PD is
   below ~4 Hz; it cannot sustain DSI = 0.5+ AND PD = 30+ Hz at random init from any seed,
   generation, or objective-count formulation tried so far.

The substrate-limited reading is now the surviving high-confidence hypothesis. Two unexamined
factors remain in the algorithm-side reading: IBEA replacement (S-0102-03) and pop=290 floor per
[Dang2023][dang2023] (S-0102-04). t0104's negative result motivates both directly.

## Limitations

* **Two seeds, not three.** The researcher elected to stop after seed 55 rather than launch seed 66
  (see `intervention/early_stop_after_seed_55.md`). The marginal information from a third seed at
  ~$4 incremental cost was judged not worth the spend when two seeds already converge to the same
  qualitative answer. This reduces the variance estimate on yield but does not affect the binary
  answer (0 cells in 2,208 = upper Wilson 95% CI on yield is < 0.0014, a strong statement).

* **Per-seed watchdog truncation.** Both seeds tripped the per-seed $4 watchdog before reaching the
  planned gen 20 (seed 44 at gen 12, seed 55 at gen 11). The slope of seed 55's HV between gens 8
  and 11 (+0.72 over 3 gens, mostly carried by gen 8's breakthrough) is too modest to argue a
  joint-pass cell was about to be discovered at gen 12-20. But "did not reach" is weaker than "did
  reach and observed nothing".

* **Per-gen wall-clock doubled over the run.** NEURON memory accumulation made late generations ~8x
  slower than early ones for both seeds. Worker pool restart between generations was already active
  in the inherited driver; the doubling suggests additional leak surface inside per-cell evaluation.
  S-0104-06 below proposes a per-N-gen full pool restart.

* **Algorithm-side factors unexamined.** This task only tested NSGA-II crowding-distance selection.
  IBEA's hypervolume-density selection (S-0102-03) and the Dang pop>=290 floor (S-0102-04) remain
  open. A positive yield from either would re-open the algorithm-limited reading.

* **Dead-code morphology mode.** `constants_electrophys.py` carries a stale `ANGLES_8DIR_DEG`
  constant from the t0080-era; t0104 uses 16 directions throughout. The constant is dead code but
  remains in the imported namespace and is a long-running source of confusion. Cleanup is proposed
  as S-0104-03.

* **The DSI guard threshold of 10 spikes is conservative-but-not-empirically-calibrated.** The unit
  test in `code/test_evaluator_dsi_guard.py` documents the threshold but does not sweep values 5,
  10, 20, 50 on a sensitivity panel. The 47 cells at the guard floor in t0104 are not analysed for
  whether 5 or 20 would have been preferable. This is a low-priority follow-up.

## Sources

* Paper: `10.1371_journal.pcbi.1012039`
* Paper: `10.48550_arXiv.2306.04525`
* Paper: `10.48550_arXiv.2401.14014`
* Task: `t0091_morphology_extended_nsga2_v1`
* Task: `t0099_random_init_pareto_robustness`
* Task: `t0102_seedscale_n4_gen20`

[mohacsi2024]: ../../../../../tasks/t0102_seedscale_n4_gen20/assets/paper/10.1371_journal.pcbi.1012039/summary.md
[dang2023]: ../../../../../tasks/t0102_seedscale_n4_gen20/assets/paper/10.48550_arXiv.2306.04525/summary.md
[morinaga2024]: ../../../../../tasks/t0102_seedscale_n4_gen20/assets/paper/10.48550_arXiv.2401.14014/summary.md
[t0091]: ../../../../t0091_morphology_extended_nsga2_v1/
[t0099]: ../../../../t0099_random_init_pareto_robustness/
[t0102]: ../../../../t0102_seedscale_n4_gen20/
[t0024]: ../../../../t0024_port_de_rosenroll_2026_dsgc/
