---
spec_version: "1"
task_id: "t0102_seedscale_n4_gen20"
stage: "creative-thinking"
date_authored: "2026-05-12"
---
# Creative Analysis: Bimodal DSI/PD Anti-Correlation in t0102

## Headline

Both random-init NSGA-II seeds in t0102 converge on the *same* degenerate corner of objective space:
extreme DSI (max 1.0) at vanishing firing rate (PD < 5 Hz), or high PD (max 64-67 Hz) at vanishing
DSI (< 0.05). Out of 2,592 evaluations across seeds 44 and 55, **zero cells achieve DSI >= 0.5 AND
PD >= 5 Hz simultaneously**, let alone the strict joint-pass corner at PD >= 30 Hz. The closest cell
has DSI=0.958 with PD=4.107 Hz (seed 44, gen 7, robustness=0.500). This is not a near-miss but a
*structural* anti-correlation: DSI and PD live on opposite sides of the substrate. A 68-d parameter
post-hoc analysis below identifies the specific mechanism (slow Ca decay, weak ACh drive, and slow
sAHP) that the GA exploits to score perfect DSI at zero firing.

* * *

## 1. The Bimodality Finding: Mechanism, Not Artefact

### Empirical structure

The joint distribution of DSI vs PD across all 2,592 t0102 cells is bimodal along the DSI axis:

| DSI bin | PD<0.5 | PD[0.5, 5) | PD[5, 10) | PD[10, 30) | PD[30, 60) | PD[60, 100) |
| --- | --- | --- | --- | --- | --- | --- |
| [0.00, 0.05) | 35 | 612 | 276 | 700 | 397 | 23 |
| [0.05, 0.10) | 0 | 159 | 23 | 63 | 0 | 0 |
| [0.10, 0.20) | 7 | 107 | 12 | 33 | 0 | 0 |
| [0.20, 0.30) | 11 | 19 | 2 | 0 | 0 | 0 |
| [0.30, 0.50) | 27 | 3 | 7 | 4 | 0 | 0 |
| [0.50, 0.99) | 16 | 29 | 0 | 0 | 0 | 0 |
| [0.99, 1.00] | 27 | 0 | 0 | 0 | 0 | 0 |

Every cell with DSI >= 0.5 has PD < 5 Hz. Every cell with PD >= 30 Hz has DSI <= 0.042. The diagonal
of the table is empty.

### What 68-d parameter dimension separates the two corners?

A Cohen's d analysis between the 27 "degenerate-DSI" cells (DSI >= 0.99, PD < 0.1 Hz) and the 420
"high-PD" cells (PD >= 30 Hz) ranks the 68 dimensions by absolute effect size. The top six all point
to a coherent biophysical story:

| Dim | Parameter (ParamIndex) | Cohen's d | Deg mean | HighPD mean | Interpretation |
| --- | --- | --- | --- | --- | --- |
| 38 | `CAD_TAUR_MS` (Ca clearance tau) | **+3.29** | 65.1 ms | 7.7 ms | Slow Ca clearance loads sAHP |
| 46 | `W_GABA_US` (GABA weight) | -1.85 | 0.002 | 0.006 | Stronger GABA in high-PD (counter-intuitive) |
| 8 | `KV3_TERMINAL_GBAR` | -1.70 | 0.32 | 0.71 | Less Kv3 at terminals -> slower spiking |
| 52 | `NAV16_DEND_DISTAL` | +1.56 | 0.031 | 0.018 | More distal Nav1.6 in degenerate corner |
| 17 | `BK_MID_GBAR` | +1.48 | 0.81 | 0.48 | More BK in mid-dendrites |
| 33 | `SKAHP_TAU_CA_MULTIPLIER` | +1.46 | 14.1 | 6.2 | Slower Ca-dependent K integration |
| 39 | `N_ACH` (cholinergic syn count) | -1.39 | 94 | 208 | Half the excitatory drive |

The degenerate-DSI corner is biophysically a **silenced cell**: slow calcium clearance (Ca tau ~65
ms, near the upper bound of 100 ms) combined with a slower sAHP multiplier (~14x vs ~6x) produces an
effectively permanent hyperpolarising current after any spike, while halved cholinergic synapse
count (94 vs 208) cripples the drive. The cell does not fire in any direction. PD = 0 Hz, ND = 0 Hz,
and the vector-sum DSI is computed from a near-zero divisor with floating-point dust dominating the
numerator. The "perfect DSI" is a **division-by-near-zero artefact of the DSI objective**, not a
real direction selectivity signal.

Robustness in this corner averages 0.366 (vs 0.578 in the high-PD corner) which is consistent with:
the noisier the near-zero spike count is across the 4 replicates, the lower the inverse-CV. This is
why robustness >= 0.7 filters out the degenerate corner, but the corner still dominates the Pareto
because two of three objectives (DSI and rob) get pulled toward it by different cell families.

### Is this biology or parameterisation?

Both, in a structured way:

* **The mechanism is biologically plausible**. Slow Ca clearance (tau > 50 ms) and amplified sAHP do
  silence SACs/DSGCs in real preparations. The Poleg-Polsky 2026 SAC computational paper explicitly
  used a Ca-buffer time constant near 100 ms to suppress runaway firing. The substrate is letting
  NSGA-II find a real biological solution -- silence -- it just happens to game the objective.
* **The objective is mis-specified**. DSI vector-sum on a silent cell should be undefined or clipped
  to zero, not 1.0. The current implementation in `evaluator.py` returns vector-sum DSI even when
  total spike count across all 16 directions is < 10, which is below any reasonable SNR floor.
  **This is the single biggest bug in the optimisation stack** and likely the principal reason t0099
  and t0102 both fail to find joint-pass cells with random init.
* **The bimodality is real, not algorithmic**. NSGA-II's crowding-distance selection actively
  *promotes* diverse Pareto points. The substrate's response is to deliver two equally Pareto-
  optimal extremes (perfect DSI at PD=0; perfect PD at DSI=0) and nothing in the middle. NSGA-II is
  doing its job; the search space has no joint-corner cells with rob>=0.7.

* * *

## 2. Warm-Start Revisited: Was t0091 Really an NSGA-II Success?

t0091 found **1 strict joint-pass cell** (DSI=0.511, PD=35.1 Hz, rob=0.79) at `source_generation=2`
out of a 57-cell Pareto front. The question is whether this was NSGA-II discovering the joint
corner, or the warm-start anchor cells already being joint-pass and the GA preserving them.

### The evidence

t0091's warm-start population was 95 anchor clones (5 anchors x 19 clones) + 1 random fill = 96
cells. Reading `tasks/t0091_*/results/data/warm_start_population.json` and computing Euclidean
distance in the 68-d parameter space, the joint-pass cell's 5 nearest warm-start rows are:

| Rank | Row | Anchor | Clone | Distance |
| --- | --- | --- | --- | --- |
| 1 | 84 | `alt_topology` | 8 | 3.55 |
| 2 | 27 | `symmetric` | 8 | 11.47 |
| 3 | 92 | `alt_topology` | 16 | 37.18 |
| 4 | 35 | `symmetric` | 16 | 38.74 |
| 5 | 93 | `alt_topology` | 17 | 90.22 |

The cell sits **3.55 normalised units from the alt_topology anchor row 84**, with a 3x larger gap to
the next-nearest anchor. `source_generation=2` means it was the first offspring of the
initial-population evaluation pass. **The cell is essentially a one-generation crossover/mutation
descendant of a single alt_topology anchor clone.** NSGA-II did not search the 68-d space and find
the joint corner; it took an anchor that was already close to the joint corner, applied one round of
SBX crossover (eta=15, p=0.9) and polynomial mutation (eta=20, p=1/68 ~ 0.015 per dim), and
preserved the result. With a per-dim mutation probability of 0.015 and 68 dims, the *expected*
number of dims mutated per cell per generation is ~1.0, so this is a near-clone of the anchor.

### Implication for the warm-start claim

t0091 demonstrates that the joint-pass corner is **reachable via deterministic perturbation of
specific anchor cells in t0083's empirical library**, but it does NOT demonstrate that random 68-d
search can find that corner in 8 generations. The "warm-start was load-bearing for the high-PD-rate
dimension" claim in t0099's `results_summary.md` is correct, and t0102's null strengthens it: two GA
seeds, 14-13 generations each, 2,592 evaluations -- and the closest cell (DSI=0.958, PD=4.1 Hz) is
on a clearly different lineage from the t0091 joint-pass anchor.

The honest reframing is: **t0091's joint-pass cell was an empirical finding from the t0083 anchor
library, dressed up as an NSGA-II discovery by one generation of polynomial mutation.** This is a
load-bearing methodological clarification for any future paper.

* * *

## 3. Is N=4 Noise Replicates Enough? Noise Floor from Smoke-Gate

t0102's local smoke gate at `N_EVAL_SEEDS=4` against the t0093 bedb_like anchor fingerprint
(calibrated at `N_EVAL_SEEDS=20`, expected PD=43.6 +/- 1.0 Hz) measured:

* PD-rate = **45.36 Hz** (offset +1.76 Hz from t0093 calibration)
* DSI vector sum = 0.0262
* Robustness = 0.837
* Source: `tasks/t0102_*/logs/steps/008_setup-machines/smoke_gate.json`

The +1.76 Hz drift is consistent with the predicted sqrt(20/4) = 2.24x amplification of per-cell
standard error vs the N=20 calibration. The smoke-gate JSON explicitly flags this as
"proceed_with_caveat" -- outside the strict +/- 1 Hz tolerance, inside the relaxed +/- 2 Hz
tolerance.

### Does this noise floor explain the null?

Probably not, by the following argument: even doubling N to 8 (cutting SE by sqrt(2) ~ 1.41x) would
not move any of the 16 cells with DSI >= 0.5 AND robustness >= 0.7 *from PD < 1 Hz to PD >= 30 Hz*.
The closest cell at DSI=0.958, PD=4.107 Hz, rob=0.500 would need either ~30x higher PD or a
different lineage entirely. The noise floor explains why t0102 can't *distinguish* between PD=4.0
and PD=4.5 reliably, but it does not create a 7.5x gap to PD=30 Hz.

The hypothesis "N=4 is too noisy" is therefore probably wrong as a single-factor explanation. The
combination "N=4 + the DSI-objective division-by-near-zero bug + no anchor warm-start" is the joint
explanation. Each factor alone is recoverable; together they're hostile.

* * *

## 4. Substrate Limitation vs Algorithm Failure: What Distinguishes Them?

The standard test in the literature (e.g., Mohacsi 2024 / Neuroptimus benchmarks) for "search
exhaustion" vs "algorithm failure" is:

1. Run multiple algorithms (NSGA-II, IBEA, CMAES) on the same substrate, same budget.
2. If they all miss the same corner, that's substrate-limitation evidence.
3. If one algorithm finds it, that's algorithm failure evidence.

t0102 only tested NSGA-II. The Mohacsi 2024 Neuroptimus paper (research_papers.md, section
"Algorithm comparison from Mohacsi 2024") reports IBEA is "clearly the best among the multi-
objective methods" and CMAES converged in ~3500 evaluations on neuron-fitting problems -- *both
outperformed NSGA-II*. t0102's 2,592 evaluations is below CMAES's 3,500-eval convergence point, but
the bimodality finding is sharper than what 700 extra evaluations should resolve.

### A cheaper diagnostic that t0102 could not run

Take the t0083 anchor library used by t0091 (alt_topology clones) and **directly re-evaluate them at
N_EVAL_SEEDS=4** (no NSGA-II, no LHS, no mutation -- just re-evaluate the anchors). If 0 of the 95
anchors clear DSI>=0.5 AND PD>=30 AND rob>=0.7, the joint corner is empirically unreachable at N=4
on this substrate (substrate-limited at N=4 even if N=20 worked). If >=1 anchor clears the corner,
then NSGA-II at random init is failing to find what is empirically present (algorithm- limited).
This is a < $0.20 follow-up that resolves the ambiguity directly.

A second diagnostic: take t0091's single joint-pass cell vector and **re-evaluate at N=4**. If its
DSI/PD/rob drop below the corner thresholds, the corner exists but is unreachable from N=4 ranking
(which is what the noise-floor argument predicts).

* * *

## 5. Cross-Seed Convergence: Why Both Seeds Hit DSI=1.0 So Fast

* Seed 44: first cell with DSI >= 0.99 at **generation 6**, 480 evaluations.
* Seed 55: first cell with DSI >= 0.99 at **generation 4**, 288 evaluations.

Both seeds converge to the degenerate-DSI corner in fewer evaluations than a random walk would need
to explore the 68-d space meaningfully. The reason is the silence corner is *huge* in parameter
space:

* Any parameter combination with simultaneously (Ca tau > 40 ms, sAHP multiplier > 10x, N_ACH < 150)
  silences the cell.
* The substrate Ca tau bound is [5, 100] ms; (40, 100] is **60% of the range**.
* The sAHP multiplier bound is [1, 20]; (10, 20] is **50% of the range**.
* N_ACH bound is [50, 350]; [50, 150] is **33% of the range**.
* Joint probability under LHS (uniform in each dim, independent): 0.6 * 0.5 * 0.33 ~ **10%** of the
  initial 96-cell LHS population is *already* in or near the silence corner.

The "perfect DSI" trick is reached in ~5 generations because every cell that lands in the silence
basin gets DSI = +inf in the vector-sum formula, and NSGA-II's non-dominated front cannot reject a
"free" DSI = 1.0 on a Pareto objective. The silence basin is a **gradient sink** for the DSI
objective. NSGA-II is doing exactly what it should; the objective function is the bug.

* * *

## 6. Alternative Optimisation Strategies: Would IBEA/CMAES/NSGA-III Help?

| Algorithm | Expected behaviour on this substrate | Likely outcome |
| --- | --- | --- |
| **NSGA-III** (reference-point-based) | Reference points placed near (0.5, 30, 0.7) bias selection toward the desired corner. | Some help if the corner is reachable; no help if it's empty. |
| **IBEA** (hypervolume-based selection) | Mohacsi 2024 reports IBEA outperforms NSGA-II on compartmental neurons. Tends to fill the front interior rather than the extremes. | Likely shifts mass away from degenerate corners but does not invent corner cells that don't exist. |
| **CMAES** (single-objective with HV scalarisation) | Mohacsi 2024 reports CMAES converges in ~3500 evals on neuron problems. CMAES does not produce a Pareto front by default; needs HV-scalarised formulation. | Probably best on single-objective subproblems but loses the multi-objective trade-off view. |
| **2-objective NSGA-II (DSI, PD only) + post-hoc rob filter** | Eliminates the "robustness=high at silence" pull. Recovers a cleaner DSI/PD front. | The bimodality finding suggests this won't change the structural anti-correlation but will produce a more interpretable front. |

The bigger leverage is **fixing the DSI objective to reject silenced cells** (e.g., gating by total
spike count > N or returning DSI=0 when PD < 1 Hz). With that fix in place, NSGA-II would no longer
chase the silence corner and the available compute would all go into the high-PD manifold. This is a
1-line change in `evaluator.py` and is the highest-leverage follow-up.

### Per Mohacsi 2024 benchmark in `research_papers.md`

The internet research notes (research_internet.md lines 184-204) explicitly recommend IBEA over
NSGA-II for compartmental neuron problems with our objective structure. The substrate bimodality
finding makes this recommendation stronger: IBEA's hypervolume-density selection avoids placing half
the front in the degenerate DSI=1, PD=0 corner that NSGA-II's crowding distance happily keeps.

* * *

## 7. Out-of-the-Box Mechanistic Reading: What the Silenced High-DSI Cells Tell Us

The degenerate cells are not "bugs to be filtered out" -- they tell us something biological. The 27
DSI >= 0.99 / PD < 0.1 cells are the **GA's discovery of the lateral-inhibition silencing regime**
that gates SAC/DSGC output in real retina. Their parameter profile (slow Ca clearance, strong sAHP,
weak excitation) matches the description of "SAC gating by intracellular Ca- dependent K currents"
in Briggman 2011 and Poleg-Polsky 2026.

If the t0102 substrate is *retina-faithful*, then the existence of a large basin of silenced cells
with strong nominal DSI is itself a finding: it suggests that **DSGC direction selectivity in vivo
is held in check by intracellular calcium dynamics**, not just by inhibitory synapses, and that
perturbing Ca buffering should disinhibit the entire population. This would be a testable prediction
in slice physiology -- chelate intracellular Ca with BAPTA -> SAC firing rate should jump from ~0 to
~30 Hz at preserved DSI.

The follow-up question is whether the silenced cells, when their Ca dynamics are released, all
collapse into the high-PD low-DSI corner (cells become indiscriminate firers) or whether some
fraction lands in the joint corner (DSI preserved, PD restored). t0102 has all the parameter vectors
needed to test this in silico by perturbing dim 38 (Ca tau) on the 27 degenerate cells and
re-evaluating -- a < $0.20 follow-up.

* * *

## Concrete Follow-Up Suggestions

### S-0102-CT-01: Fix the DSI objective for silenced cells

**Kind**: technique **Priority**: high **Why**: The single highest-leverage change. Modify
`evaluator.py` so that `dsi_vector_sum` returns 0 (or NaN, gated upstream) when
`total_spike_count < 10` across all 16 directions. This removes the divide-by-near-zero artefact
that pulls half the NSGA-II Pareto into the silence corner. Re-running t0099-style random-init
NSGA-II with the fixed objective should shift the front interior toward PD > 0 cells. **Expected
outcome**: Joint-pass yield > 0 even at N_EVAL_SEEDS=4 with random init. **Cost**: ~$2-3 (one
Vast.ai run at pop=96, gens=8, single GA seed).

### S-0102-CT-02: Direct re-evaluation of t0083 anchor library at N=4

**Kind**: evaluation **Priority**: high **Why**: Resolves the "substrate limitation vs algorithm
failure" ambiguity directly. Take the 5 anchor families used in t0091's warm-start, re-evaluate each
at `N_EVAL_SEEDS=4` (no NSGA-II, just direct evaluation), and count how many clear DSI>=0.5 AND
PD>=30 AND rob>=0.7. If 0 clear, the joint corner is unreachable at N=4 regardless of algorithm; if
>=1 clears, NSGA-II at random init is the bottleneck. **Expected outcome**: a definitive answer to
whether t0091's warm-start strategy is still viable at N=4. **Cost**: < $0.20 (~95 single-cell
evaluations, no GA).

### S-0102-CT-03: NSGA-III with reference-points biased to joint corner

**Kind**: experiment **Priority**: medium **Why**: Tests whether NSGA-III's reference-point
selection (with points clustered near (0.5, 30, 0.7) in normalised objective space) can pull the
front into the joint corner where NSGA-II's crowding distance cannot. Same substrate, same budget as
t0102; replaces only the selection operator. **Expected outcome**: front mass shifts away from
degenerate-DSI corner; joint-pass count may or may not increase depending on whether the corner is
empty (substrate-limited) or just unfindable by NSGA-II (algorithm-limited). Combined with
S-0102-CT-02 disambiguates definitively. **Cost**: ~$5-6 (one run at pop=96, gens=15, two GA seeds).

### S-0102-CT-04: Calcium-dynamics perturbation of degenerate cells (in-silico knockout)

**Kind**: experiment **Priority**: medium **Why**: Test the mechanistic-reading hypothesis from
Section 7. Take the 27 t0102 cells with DSI >= 0.99 / PD < 0.1, fix their 68-d parameter vector
except `CAD_TAUR_MS` (dim 38), sweep that dim from current value down to 5 ms in 10 steps, and
re-evaluate DSI/PD/rob at N_EVAL_SEEDS=8. Question: do these cells collapse into the high-PD low-DSI
corner (i.e., silence is the *only* way they can maintain DSI), or do some land in the joint corner
(i.e., Ca clearance is the active constraint and the rest of the parameter vector is joint-corner
viable)? **Expected outcome**: a 27 x 10 grid of (DSI, PD, rob) trajectories that maps the
silence-to-joint escape paths. **Cost**: < $0.50 (270 cell evaluations, no GA).

### S-0102-CT-05: IBEA replacement for NSGA-II on the joint substrate

**Kind**: experiment **Priority**: medium **Why**: Per Mohacsi 2024 and `research_papers.md` line
195-204, IBEA outperforms NSGA-II on compartmental neuron fitting in the published Neuroptimus
benchmark suite. With t0102's bimodal result in hand, IBEA's hypervolume-density selection is the
textbook recommendation. The suggestion is to port the t0099 substrate to BluePyOpt's IBEA (or
pymoo's IBEA-equivalent) at matched budget (pop=96, gens=15, N_EVAL_SEEDS=4, 2 GA seeds) and compare
front structure. **Expected outcome**: less degenerate-DSI mass in the IBEA front; better joint-pass
yield even if the corner remains hard to reach. **Cost**: ~$6-8 (matched to t0102 envelope; possibly
higher because IBEA's pairwise indicator adds O(N^2) overhead per generation).
