# Predictions: `dendritic-computation`

4 predictions asset(s).

[Back to all predictions](../README.md)

---

<details>
<summary>📊 <strong>NSGA-II seed=44 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS
random init)</strong> (<code>nsga2-seed44-bedb-morph-n4-gen20</code>) —
1344 instances (jsonl)</summary>

| Field | Value |
|---|---|
| **ID** | `nsga2-seed44-bedb-morph-n4-gen20` |
| **Model ID** | — |
| **Model** | Compartmental DSGC neuron model with the t0092-patched procedural morphology generator (canonical via correction C-0093-01) and the 54-d Bed B electrophys parameter vector applied via t0080's apply_parameter_vector. Each cell is evaluated with 16 stimulus directions x 4 noise replicates; NSGA-II minimises the negated triple (DSI vector-sum, PD-rate, robustness). |
| **Datasets** |  |
| **Format** | jsonl |
| **Instances** | 1344 |
| **Date created** | 2026-05-12 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |
| **Created by** | [`t0102_seedscale_n4_gen20`](../../../overview/tasks/task_pages/t0102_seedscale_n4_gen20.md) |
| **Documentation** | [`description.md`](../../../tasks\t0102_seedscale_n4_gen20\assets\predictions\nsga2-seed44-bedb-morph-n4-gen20\description.md) |

**Metrics at creation:**

* **n_generations_completed**: 14
* **n_cells**: 1344
* **max_dsi**: 1.0
* **max_pd_rate_hz**: 64.28571428571429
* **max_robustness**: 0.991628794830278
* **n_joint_pass**: 0
* **hypervolume_final**: 7.532779084144153
* **final_cost_usd**: 4.094182907241769

# NSGA-II seed=44 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS random init)

## Metadata

* **Name**: NSGA-II seed=44 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS random init)
* **Model**: DSGC compartmental model (t0092-patched procedural morphology + 54-d Bed B
  electrophys vector via t0080 apply_params)
* **Datasets**: none (simulator outputs)
* **Format**: jsonl
* **Instances**: 1,344 per-cell evaluations across 14 NSGA-II generations
* **Created by**: t0102_seedscale_n4_gen20

## Overview

This predictions asset records every cell evaluated by the NSGA-II run with GA seed=44 in
t0102. The run is one of two independent random-init restarts (44 and 55) that test whether
dropping per-cell noise replicates from t0099's N_EVAL_SEEDS=5 down to 4 and extending
generations from 8 up to 20 recovers the strict joint-pass corner of objective space (DSI >=
0.5, preferred-direction firing rate >= 30 Hz, robustness >= 0.7) that t0099 failed to find
with 3 random-init seeds.

Each line of the JSONL captures one DSGC compartmental simulation: the 68-d parameter vector
(54 electrophys knobs + 14 morphology knobs), the three NSGA-II objectives (DSI vector-sum,
preferred-direction firing rate, robustness as inverse CV across noise replicates), and a
precomputed strict joint-pass flag. Together with the matched seed-other asset and the
per-seed history JSONs in `results/data/`, this is the raw evidence for the t0102 answer
asset.

The seed terminated at generation 14 after the per-seed cost watchdog tripped at the $4
budget; final hypervolume was 7.5328 and final cost $4.0942.

## Model

DSGC compartmental neuron model with the t0092-patched procedural morphology generator
(`generate_fixed_morphology`, canonical via correction C-0093-01) and the 54-d Bed B
electrophys parameter vector applied via t0080's `apply_parameter_vector`. Per-cell evaluation
runs 16 stimulus directions x 4 noise replicates with objectives = (DSI vector-sum,
preferred-direction firing rate in Hz, robustness as inverse CV of DSI across the 4 noise
replicates), all maximised. Pymoo NSGA-II minimises the negated triple. Crossover SBX eta=15
with prob=0.9; polynomial mutation eta=20 with prob=1/68; elimination of duplicates enabled.
Population size 96, max generations 20, LHS-initialised initial population with explicit
`np.random.SeedSequence` seeding for reproducibility.

## Data

No external dataset is consumed. Input vectors are 68-d points sampled by NSGA-II starting
from a 96-row Latin Hypercube Sample drawn with pymoo's `LatinHypercubeSampling` and
explicitly seeded with task_seed=44. Bounds for the 68 parameters are inherited unchanged from
the t0099 / t0091 substrate (the same 54-d electrophys bounds from t0080 plus the 14-d
morphology bounds from t0090). Noise replicates inside each evaluation use the four
deterministically spawned RNG seeds (2684470948, 4091952314, 233227757, 3276785861) drawn from
`np.random.SeedSequence(42).spawn(5)` -- one fewer than t0099's five replicates.

## Prediction Format

JSONL with one line per evaluated cell (1,344 lines total). Each line is a JSON object with
fields:

* `generation`: int, the NSGA-II generation at which this cell was evaluated (1 = initial LHS
  population, 2..N = offspring generations)
* `vector_68d`: list of 68 floats, the 54-d electrophys + 14-d morphology parameter vector
* `dsi_vector_sum`: float in [0, 1], vector-sum direction selectivity index averaged across
  the 4 noise replicates
* `pd_rate_hz`: float, preferred-direction mean firing rate in Hz (mean across the 4
  replicates)
* `robustness`: float in [0, 1], inverse CV of DSI across the 4 noise replicates
* `joint_pass`: bool, true iff `dsi_vector_sum >= 0.5` AND `pd_rate_hz >= 30` AND `robustness
  >= 0.7` (the strict task-level biological-plausibility corner)

Example line (formatted for readability):

```
{
  "generation": 14,
  "vector_68d": [0.4576, 0.0550, ..., 0.2229],
  "dsi_vector_sum": 0.4321,
  "pd_rate_hz": 22.43,
  "robustness": 0.8104,
  "joint_pass": false
}
```

## Metrics

Headline metrics computed at asset creation time:

| Metric | Value |
| --- | --- |
| Cells evaluated | **1,344** |
| Generations completed | **14** / 20 |
| Best DSI (vector sum) | **1.0000** |
| Best preferred-direction rate (Hz) | **64.29** |
| Best robustness (inverse CV) | **0.9916** |
| Strict joint-pass cells | **0** |
| Final hypervolume | **7.5328** |
| Final NSGA-II compute cost (USD) | **$4.0942** |

The strict joint-pass criterion (DSI >= 0.5 AND PD-rate >= 30 Hz AND robustness >= 0.7) is met
by **0** of the 1,344 evaluated cells.

## Main Ideas

* The run terminated at generation 14 after the per-seed cost watchdog tripped at $4.00, not
  at the planned generation 20 -- the per-cell wall-clock at N_EVAL_SEEDS=4 was higher than
  the optimistic projection in the plan's cost table.
* Zero of the 1,344 evaluated cells cleared the strict joint-pass corner. Best per-axis maxima
  are DSI=1.0000, PD-rate=64.29 Hz, robustness=0.9916, all individually inside their
  thresholds for some cell but never simultaneously for the same cell.
* The per-cell vector_68d is sufficient to re-evaluate or re-score any cell without re-running
  the optimiser, enabling downstream noise-budget studies and joint comparisons against
  t0091's warm-started Pareto and t0099's three random-init seeds.

## Summary

This asset captures all 1,344 NSGA-II evaluations from the t0102 random-init run with GA
seed=44, covering generations 1 through 14. Each cell is a 68-d point in the Bed B electrophys
+ procedural morphology parameter space, evaluated with 16 stimulus directions and 4 noise
replicates against the triple objective (DSI vector-sum, preferred-direction firing rate,
robustness).

The headline finding is that zero cells cleared the strict joint-pass corner. Best individual
axes were DSI=1.0000, PD=64.29 Hz, and robustness=0.9916. Combined with the matched
second-seed asset and the t0099 three-seed prior, this gives a 0/2 task-level reproducibility
outcome for the joint-pass corner, reinforcing the negative result that random initialisation
alone (no warm-start anchors) does not recover the biologically plausible region at this
compute budget.

The asset is the primary evidence channel for the t0102 answer asset. Cost watchdog triggered
at $4.00 of compute (actual $4.0942 final reading), terminating the run at generation 14 short
of the planned 20.

</details>

<details>
<summary>📊 <strong>NSGA-II seed=44 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS
random init, 2-objective DSI+PD, DSI silence guard)</strong>
(<code>nsga2-seed44-bedb-morph-n4-gen20-2obj</code>) — 1152 instances
(jsonl)</summary>

| Field | Value |
|---|---|
| **ID** | `nsga2-seed44-bedb-morph-n4-gen20-2obj` |
| **Model ID** | — |
| **Model** | Compartmental DSGC neuron model with the t0092-patched procedural morphology generator (canonical via correction C-0093-01) and the 54-d Bed B electrophys parameter vector applied via t0080's apply_parameter_vector. Each cell is evaluated with 16 stimulus directions x 4 noise replicates; NSGA-II minimises the negated pair (DSI vector-sum, PD-rate) — robustness is computed per cell but does NOT enter NSGA-II selection in t0104 (REQ-2). The DSI silence guard (REQ-3) clamps DSI to 0.0 when the cell's total mean spikes across directions fall below 10, eliminating the t0102 silence-corner artifact. |
| **Datasets** |  |
| **Format** | jsonl |
| **Instances** | 1152 |
| **Date created** | 2026-05-12 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |
| **Created by** | [`t0104_nsga2_2obj_dsi_pdrate_3seeds`](../../../overview/tasks/task_pages/t0104_nsga2_2obj_dsi_pdrate_3seeds.md) |
| **Documentation** | [`description.md`](../../../tasks\t0104_nsga2_2obj_dsi_pdrate_3seeds\assets\predictions\nsga2-seed44-bedb-morph-n4-gen20-2obj\description.md) |

**Metrics at creation:**

* **n_generations_completed**: 12
* **n_cells**: 1152
* **max_dsi**: 0.40725524513608247
* **max_pd_rate_hz**: 75.0
* **n_joint_pass**: 0
* **n_at_guard_floor**: 25
* **hypervolume_final**: 2.854543785086947
* **final_cost_usd**: 4.694470022747195

# NSGA-II seed=44 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS random init, 2-objective DSI+PD, DSI silence guard)

## Metadata

* **Name**: NSGA-II seed=44 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS random init,
  2-objective DSI+PD, DSI silence guard)
* **Model**: DSGC compartmental model (t0092-patched procedural morphology + 54-d Bed B
  electrophys vector via t0080 apply_params)
* **Datasets**: none (simulator outputs)
* **Format**: jsonl
* **Instances**: 1,152 per-cell evaluations across 12 NSGA-II generations
* **Created by**: t0104_nsga2_2obj_dsi_pdrate_3seeds

## Overview

This predictions asset records every cell evaluated by the t0104 NSGA-II run with GA seed=44.
The run is one of three independent random-init restarts (44, 55, 66) that test whether
dropping the robustness axis from NSGA-II's objective vector (3 -> 2) and applying the DSI
silence guard (S-0102-01) recover joint-pass cells where t0102's 3-objective N=4 run found
zero across 2,592 cells.

Each line of the JSONL captures one DSGC compartmental simulation: the 68-d parameter vector
(54 electrophys knobs + 14 morphology knobs), the two NSGA-II objectives (DSI vector-sum and
preferred-direction firing rate), and a precomputed strict 2-axis joint-pass flag (DSI >= 0.5
AND PD
>= 30 Hz). Robustness is computed internally per cell by the evaluator but is not persisted to this
JSONL because it is no longer an NSGA-II objective in t0104.

The seed terminated at generation 12 (either at the planned 20 cap or earlier via the cost
watchdog at $4.00 per seed); final hypervolume in the 2-D (DSI, PD) plane was 2.8545 and final
cost $4.6945.

## Model

DSGC compartmental neuron model with the t0092-patched procedural morphology generator
(`generate_fixed_morphology`, canonical via correction C-0093-01) and the 54-d Bed B
electrophys parameter vector applied via t0080's `apply_parameter_vector`. Per-cell evaluation
runs 16 stimulus directions x 4 noise replicates with objectives = (DSI vector-sum,
preferred-direction firing rate in Hz), both maximised. Pymoo NSGA-II minimises the negated
pair. Crossover SBX eta=15 with prob=0.9; polynomial mutation eta=20 with prob=1/68;
elimination of duplicates enabled. Population size 96, max generations 20, LHS-initialised
initial population with explicit `np.random.SeedSequence` seeding for reproducibility. The DSI
silence guard (REQ-3) is active: cells whose total mean spike count across the 16 directions
falls below 10 have DSI clamped to 0.0 before being returned to NSGA-II.

## Data

No external dataset is consumed. Input vectors are 68-d points sampled by NSGA-II starting
from a 96-row Latin Hypercube Sample drawn with pymoo's `LatinHypercubeSampling` and
explicitly seeded with task_seed=44. Bounds for the 68 parameters are inherited unchanged from
the t0102 / t0099 substrate (the same 54-d electrophys bounds from t0080 plus the 14-d
morphology bounds from t0090). Noise replicates inside each evaluation use the four
deterministically spawned RNG seeds drawn from `np.random.SeedSequence(42).spawn(5)`.

## Prediction Format

JSONL with one line per evaluated cell (1,152 lines total). Each line is a JSON object with
fields:

* `generation`: int, the NSGA-II generation at which this cell was evaluated (1 = initial LHS
  population, 2..N = offspring generations)
* `vector_68d`: list of 68 floats, the 54-d electrophys + 14-d morphology parameter vector
* `dsi_vector_sum`: float in [0, 1], vector-sum direction selectivity index averaged across
  the 4 noise replicates (guard-cleaned per REQ-3 at threshold 10)
* `pd_rate_hz`: float, preferred-direction mean firing rate in Hz (mean across the 4
  replicates)
* `joint_pass`: bool, true iff `dsi_vector_sum >= 0.5` AND `pd_rate_hz >= 30` (the t0104
  strict 2-axis biological-plausibility corner; t0102's robustness >= 0.7 threshold is dropped
  because robustness is no longer an NSGA-II objective)

Example line (formatted for readability):

```
{
  "generation": 14,
  "vector_68d": [0.4576, 0.0550, ..., 0.2229],
  "dsi_vector_sum": 0.4321,
  "pd_rate_hz": 22.43,
  "joint_pass": false
}
```

## Metrics

Headline metrics computed at asset creation time:

| Metric | Value |
| --- | --- |
| Cells evaluated | **1,152** |
| Generations completed | **12** / 20 |
| Best DSI (vector sum, guard-cleaned) | **0.4073** |
| Best preferred-direction rate (Hz) | **75.00** |
| Strict joint-pass cells (DSI >= 0.5 AND PD >= 30) | **0** |
| Cells at DSI guard floor (DSI = 0.0) | **25** |
| Final hypervolume (2-D) | **2.8545** |
| Final NSGA-II compute cost (USD) | **$4.6945** |

The 2-axis strict joint-pass criterion (DSI >= 0.5 AND PD-rate >= 30 Hz) is met by **0** of
the 1,152 evaluated cells.

## Main Ideas

* The run terminated at generation 12 (either at the planned cap of 20 or earlier via the
  per-seed cost watchdog at $4.00). Per-cell wall-clock at N_EVAL_SEEDS=4 was the operative
  throughput constant; the predictions JSONL captures every evaluation up to the termination
  point.
* 0 of the 1,152 evaluated cells cleared the strict 2-axis joint-pass corner (DSI >= 0.5 AND
  PD >= 30 Hz). Best per-axis maxima are DSI=0.4073 and PD-rate=75.00 Hz on the guard-cleaned
  DSI.
* 25 of the 1,152 cells are at the DSI guard floor (DSI = 0.0 because total mean spikes < 10);
  these are the cells that would have produced the t0102 silence-corner artifact at DSI = 1.0
  without the guard. Per-cell `vector_68d` is sufficient to re-evaluate any cell without
  re-running the optimiser.

## Summary

This asset captures all 1,152 NSGA-II evaluations from the t0104 random-init 2-objective run
with GA seed=44, covering generations 1 through 12. Each cell is a 68-d point in the Bed B
electrophys + procedural morphology parameter space, evaluated with 16 stimulus directions and
4 noise replicates against the 2-dimensional objective (DSI vector-sum, preferred-direction
firing rate). The DSI silence guard from S-0102-01 is active throughout.

The headline finding for this seed is that 0 of the evaluated cells cleared the strict 2-axis
joint-pass corner. Best individual axes were DSI=0.4073 and PD=75.00 Hz. Combined with the
matched two-other-seed assets in t0104 and the t0102 three-objective prior, this contributes
one of three apples-to-apples comparisons of the 2-objective vs 3-objective NSGA-II
formulations on the same substrate.

The asset is a primary evidence channel for the t0104 answer asset. Cost watchdog and
HV-plateau termination jointly govern run length; the final cost reading was $4.6945 and the
run reached generation 12 of the planned 20.

</details>

<details>
<summary>📊 <strong>NSGA-II seed=55 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS
random init)</strong> (<code>nsga2-seed55-bedb-morph-n4-gen20</code>) —
1248 instances (jsonl)</summary>

| Field | Value |
|---|---|
| **ID** | `nsga2-seed55-bedb-morph-n4-gen20` |
| **Model ID** | — |
| **Model** | Compartmental DSGC neuron model with the t0092-patched procedural morphology generator (canonical via correction C-0093-01) and the 54-d Bed B electrophys parameter vector applied via t0080's apply_parameter_vector. Each cell is evaluated with 16 stimulus directions x 4 noise replicates; NSGA-II minimises the negated triple (DSI vector-sum, PD-rate, robustness). |
| **Datasets** |  |
| **Format** | jsonl |
| **Instances** | 1248 |
| **Date created** | 2026-05-12 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |
| **Created by** | [`t0102_seedscale_n4_gen20`](../../../overview/tasks/task_pages/t0102_seedscale_n4_gen20.md) |
| **Documentation** | [`description.md`](../../../tasks\t0102_seedscale_n4_gen20\assets\predictions\nsga2-seed55-bedb-morph-n4-gen20\description.md) |

**Metrics at creation:**

* **n_generations_completed**: 13
* **n_cells**: 1248
* **max_dsi**: 1.0
* **max_pd_rate_hz**: 66.96428571428572
* **max_robustness**: 0.9999999999999982
* **n_joint_pass**: 0
* **hypervolume_final**: 3.3926397249887454
* **final_cost_usd**: 4.3626048569322275

# NSGA-II seed=55 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS random init)

## Metadata

* **Name**: NSGA-II seed=55 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS random init)
* **Model**: DSGC compartmental model (t0092-patched procedural morphology + 54-d Bed B
  electrophys vector via t0080 apply_params)
* **Datasets**: none (simulator outputs)
* **Format**: jsonl
* **Instances**: 1,248 per-cell evaluations across 13 NSGA-II generations
* **Created by**: t0102_seedscale_n4_gen20

## Overview

This predictions asset records every cell evaluated by the NSGA-II run with GA seed=55 in
t0102. The run is one of two independent random-init restarts (44 and 55) that test whether
dropping per-cell noise replicates from t0099's N_EVAL_SEEDS=5 down to 4 and extending
generations from 8 up to 20 recovers the strict joint-pass corner of objective space (DSI >=
0.5, preferred-direction firing rate >= 30 Hz, robustness >= 0.7) that t0099 failed to find
with 3 random-init seeds.

Each line of the JSONL captures one DSGC compartmental simulation: the 68-d parameter vector
(54 electrophys knobs + 14 morphology knobs), the three NSGA-II objectives (DSI vector-sum,
preferred-direction firing rate, robustness as inverse CV across noise replicates), and a
precomputed strict joint-pass flag. Together with the matched seed-other asset and the
per-seed history JSONs in `results/data/`, this is the raw evidence for the t0102 answer
asset.

The seed terminated at generation 13 after the per-seed cost watchdog tripped at the $4
budget; final hypervolume was 3.3926 and final cost $4.3626.

## Model

DSGC compartmental neuron model with the t0092-patched procedural morphology generator
(`generate_fixed_morphology`, canonical via correction C-0093-01) and the 54-d Bed B
electrophys parameter vector applied via t0080's `apply_parameter_vector`. Per-cell evaluation
runs 16 stimulus directions x 4 noise replicates with objectives = (DSI vector-sum,
preferred-direction firing rate in Hz, robustness as inverse CV of DSI across the 4 noise
replicates), all maximised. Pymoo NSGA-II minimises the negated triple. Crossover SBX eta=15
with prob=0.9; polynomial mutation eta=20 with prob=1/68; elimination of duplicates enabled.
Population size 96, max generations 20, LHS-initialised initial population with explicit
`np.random.SeedSequence` seeding for reproducibility.

## Data

No external dataset is consumed. Input vectors are 68-d points sampled by NSGA-II starting
from a 96-row Latin Hypercube Sample drawn with pymoo's `LatinHypercubeSampling` and
explicitly seeded with task_seed=55. Bounds for the 68 parameters are inherited unchanged from
the t0099 / t0091 substrate (the same 54-d electrophys bounds from t0080 plus the 14-d
morphology bounds from t0090). Noise replicates inside each evaluation use the four
deterministically spawned RNG seeds (2684470948, 4091952314, 233227757, 3276785861) drawn from
`np.random.SeedSequence(42).spawn(5)` -- one fewer than t0099's five replicates.

## Prediction Format

JSONL with one line per evaluated cell (1,248 lines total). Each line is a JSON object with
fields:

* `generation`: int, the NSGA-II generation at which this cell was evaluated (1 = initial LHS
  population, 2..N = offspring generations)
* `vector_68d`: list of 68 floats, the 54-d electrophys + 14-d morphology parameter vector
* `dsi_vector_sum`: float in [0, 1], vector-sum direction selectivity index averaged across
  the 4 noise replicates
* `pd_rate_hz`: float, preferred-direction mean firing rate in Hz (mean across the 4
  replicates)
* `robustness`: float in [0, 1], inverse CV of DSI across the 4 noise replicates
* `joint_pass`: bool, true iff `dsi_vector_sum >= 0.5` AND `pd_rate_hz >= 30` AND `robustness
  >= 0.7` (the strict task-level biological-plausibility corner)

Example line (formatted for readability):

```
{
  "generation": 14,
  "vector_68d": [0.4576, 0.0550, ..., 0.2229],
  "dsi_vector_sum": 0.4321,
  "pd_rate_hz": 22.43,
  "robustness": 0.8104,
  "joint_pass": false
}
```

## Metrics

Headline metrics computed at asset creation time:

| Metric | Value |
| --- | --- |
| Cells evaluated | **1,248** |
| Generations completed | **13** / 20 |
| Best DSI (vector sum) | **1.0000** |
| Best preferred-direction rate (Hz) | **66.96** |
| Best robustness (inverse CV) | **1.0000** |
| Strict joint-pass cells | **0** |
| Final hypervolume | **3.3926** |
| Final NSGA-II compute cost (USD) | **$4.3626** |

The strict joint-pass criterion (DSI >= 0.5 AND PD-rate >= 30 Hz AND robustness >= 0.7) is met
by **0** of the 1,248 evaluated cells.

## Main Ideas

* The run terminated at generation 13 after the per-seed cost watchdog tripped at $4.00, not
  at the planned generation 20 -- the per-cell wall-clock at N_EVAL_SEEDS=4 was higher than
  the optimistic projection in the plan's cost table.
* Zero of the 1,248 evaluated cells cleared the strict joint-pass corner. Best per-axis maxima
  are DSI=1.0000, PD-rate=66.96 Hz, robustness=1.0000, all individually inside their
  thresholds for some cell but never simultaneously for the same cell.
* The per-cell vector_68d is sufficient to re-evaluate or re-score any cell without re-running
  the optimiser, enabling downstream noise-budget studies and joint comparisons against
  t0091's warm-started Pareto and t0099's three random-init seeds.

## Summary

This asset captures all 1,248 NSGA-II evaluations from the t0102 random-init run with GA
seed=55, covering generations 1 through 13. Each cell is a 68-d point in the Bed B electrophys
+ procedural morphology parameter space, evaluated with 16 stimulus directions and 4 noise
replicates against the triple objective (DSI vector-sum, preferred-direction firing rate,
robustness).

The headline finding is that zero cells cleared the strict joint-pass corner. Best individual
axes were DSI=1.0000, PD=66.96 Hz, and robustness=1.0000. Combined with the matched
second-seed asset and the t0099 three-seed prior, this gives a 0/2 task-level reproducibility
outcome for the joint-pass corner, reinforcing the negative result that random initialisation
alone (no warm-start anchors) does not recover the biologically plausible region at this
compute budget.

The asset is the primary evidence channel for the t0102 answer asset. Cost watchdog triggered
at $4.00 of compute (actual $4.3626 final reading), terminating the run at generation 13 short
of the planned 20.

</details>

<details>
<summary>📊 <strong>NSGA-II seed=55 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS
random init, 2-objective DSI+PD, DSI silence guard)</strong>
(<code>nsga2-seed55-bedb-morph-n4-gen20-2obj</code>) — 1056 instances
(jsonl)</summary>

| Field | Value |
|---|---|
| **ID** | `nsga2-seed55-bedb-morph-n4-gen20-2obj` |
| **Model ID** | — |
| **Model** | Compartmental DSGC neuron model with the t0092-patched procedural morphology generator (canonical via correction C-0093-01) and the 54-d Bed B electrophys parameter vector applied via t0080's apply_parameter_vector. Each cell is evaluated with 16 stimulus directions x 4 noise replicates; NSGA-II minimises the negated pair (DSI vector-sum, PD-rate) — robustness is computed per cell but does NOT enter NSGA-II selection in t0104 (REQ-2). The DSI silence guard (REQ-3) clamps DSI to 0.0 when the cell's total mean spikes across directions fall below 10, eliminating the t0102 silence-corner artifact. |
| **Datasets** |  |
| **Format** | jsonl |
| **Instances** | 1056 |
| **Date created** | 2026-05-12 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |
| **Created by** | [`t0104_nsga2_2obj_dsi_pdrate_3seeds`](../../../overview/tasks/task_pages/t0104_nsga2_2obj_dsi_pdrate_3seeds.md) |
| **Documentation** | [`description.md`](../../../tasks\t0104_nsga2_2obj_dsi_pdrate_3seeds\assets\predictions\nsga2-seed55-bedb-morph-n4-gen20-2obj\description.md) |

**Metrics at creation:**

* **n_generations_completed**: 11
* **n_cells**: 1056
* **max_dsi**: 0.541672311572628
* **max_pd_rate_hz**: 65.0
* **n_joint_pass**: 0
* **n_at_guard_floor**: 22
* **hypervolume_final**: 7.5934794279519995
* **final_cost_usd**: 4.187365977185278

# NSGA-II seed=55 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS random init, 2-objective DSI+PD, DSI silence guard)

## Metadata

* **Name**: NSGA-II seed=55 Bed B + morphology N_EVAL_SEEDS=4 N_GEN=20 (LHS random init,
  2-objective DSI+PD, DSI silence guard)
* **Model**: DSGC compartmental model (t0092-patched procedural morphology + 54-d Bed B
  electrophys vector via t0080 apply_params)
* **Datasets**: none (simulator outputs)
* **Format**: jsonl
* **Instances**: 1,056 per-cell evaluations across 11 NSGA-II generations
* **Created by**: t0104_nsga2_2obj_dsi_pdrate_3seeds

## Overview

This predictions asset records every cell evaluated by the t0104 NSGA-II run with GA seed=55.
The run is one of three independent random-init restarts (44, 55, 66) that test whether
dropping the robustness axis from NSGA-II's objective vector (3 -> 2) and applying the DSI
silence guard (S-0102-01) recover joint-pass cells where t0102's 3-objective N=4 run found
zero across 2,592 cells.

Each line of the JSONL captures one DSGC compartmental simulation: the 68-d parameter vector
(54 electrophys knobs + 14 morphology knobs), the two NSGA-II objectives (DSI vector-sum and
preferred-direction firing rate), and a precomputed strict 2-axis joint-pass flag (DSI >= 0.5
AND PD
>= 30 Hz). Robustness is computed internally per cell by the evaluator but is not persisted to this
JSONL because it is no longer an NSGA-II objective in t0104.

The seed terminated at generation 11 (either at the planned 20 cap or earlier via the cost
watchdog at $4.00 per seed); final hypervolume in the 2-D (DSI, PD) plane was 7.5935 and final
cost $4.1874.

## Model

DSGC compartmental neuron model with the t0092-patched procedural morphology generator
(`generate_fixed_morphology`, canonical via correction C-0093-01) and the 54-d Bed B
electrophys parameter vector applied via t0080's `apply_parameter_vector`. Per-cell evaluation
runs 16 stimulus directions x 4 noise replicates with objectives = (DSI vector-sum,
preferred-direction firing rate in Hz), both maximised. Pymoo NSGA-II minimises the negated
pair. Crossover SBX eta=15 with prob=0.9; polynomial mutation eta=20 with prob=1/68;
elimination of duplicates enabled. Population size 96, max generations 20, LHS-initialised
initial population with explicit `np.random.SeedSequence` seeding for reproducibility. The DSI
silence guard (REQ-3) is active: cells whose total mean spike count across the 16 directions
falls below 10 have DSI clamped to 0.0 before being returned to NSGA-II.

## Data

No external dataset is consumed. Input vectors are 68-d points sampled by NSGA-II starting
from a 96-row Latin Hypercube Sample drawn with pymoo's `LatinHypercubeSampling` and
explicitly seeded with task_seed=55. Bounds for the 68 parameters are inherited unchanged from
the t0102 / t0099 substrate (the same 54-d electrophys bounds from t0080 plus the 14-d
morphology bounds from t0090). Noise replicates inside each evaluation use the four
deterministically spawned RNG seeds drawn from `np.random.SeedSequence(42).spawn(5)`.

## Prediction Format

JSONL with one line per evaluated cell (1,056 lines total). Each line is a JSON object with
fields:

* `generation`: int, the NSGA-II generation at which this cell was evaluated (1 = initial LHS
  population, 2..N = offspring generations)
* `vector_68d`: list of 68 floats, the 54-d electrophys + 14-d morphology parameter vector
* `dsi_vector_sum`: float in [0, 1], vector-sum direction selectivity index averaged across
  the 4 noise replicates (guard-cleaned per REQ-3 at threshold 10)
* `pd_rate_hz`: float, preferred-direction mean firing rate in Hz (mean across the 4
  replicates)
* `joint_pass`: bool, true iff `dsi_vector_sum >= 0.5` AND `pd_rate_hz >= 30` (the t0104
  strict 2-axis biological-plausibility corner; t0102's robustness >= 0.7 threshold is dropped
  because robustness is no longer an NSGA-II objective)

Example line (formatted for readability):

```
{
  "generation": 14,
  "vector_68d": [0.4576, 0.0550, ..., 0.2229],
  "dsi_vector_sum": 0.4321,
  "pd_rate_hz": 22.43,
  "joint_pass": false
}
```

## Metrics

Headline metrics computed at asset creation time:

| Metric | Value |
| --- | --- |
| Cells evaluated | **1,056** |
| Generations completed | **11** / 20 |
| Best DSI (vector sum, guard-cleaned) | **0.5417** |
| Best preferred-direction rate (Hz) | **65.00** |
| Strict joint-pass cells (DSI >= 0.5 AND PD >= 30) | **0** |
| Cells at DSI guard floor (DSI = 0.0) | **22** |
| Final hypervolume (2-D) | **7.5935** |
| Final NSGA-II compute cost (USD) | **$4.1874** |

The 2-axis strict joint-pass criterion (DSI >= 0.5 AND PD-rate >= 30 Hz) is met by **0** of
the 1,056 evaluated cells.

## Main Ideas

* The run terminated at generation 11 (either at the planned cap of 20 or earlier via the
  per-seed cost watchdog at $4.00). Per-cell wall-clock at N_EVAL_SEEDS=4 was the operative
  throughput constant; the predictions JSONL captures every evaluation up to the termination
  point.
* 0 of the 1,056 evaluated cells cleared the strict 2-axis joint-pass corner (DSI >= 0.5 AND
  PD >= 30 Hz). Best per-axis maxima are DSI=0.5417 and PD-rate=65.00 Hz on the guard-cleaned
  DSI.
* 22 of the 1,056 cells are at the DSI guard floor (DSI = 0.0 because total mean spikes < 10);
  these are the cells that would have produced the t0102 silence-corner artifact at DSI = 1.0
  without the guard. Per-cell `vector_68d` is sufficient to re-evaluate any cell without
  re-running the optimiser.

## Summary

This asset captures all 1,056 NSGA-II evaluations from the t0104 random-init 2-objective run
with GA seed=55, covering generations 1 through 11. Each cell is a 68-d point in the Bed B
electrophys + procedural morphology parameter space, evaluated with 16 stimulus directions and
4 noise replicates against the 2-dimensional objective (DSI vector-sum, preferred-direction
firing rate). The DSI silence guard from S-0102-01 is active throughout.

The headline finding for this seed is that 0 of the evaluated cells cleared the strict 2-axis
joint-pass corner. Best individual axes were DSI=0.5417 and PD=65.00 Hz. Combined with the
matched two-other-seed assets in t0104 and the t0102 three-objective prior, this contributes
one of three apples-to-apples comparisons of the 2-objective vs 3-objective NSGA-II
formulations on the same substrate.

The asset is a primary evidence channel for the t0104 answer asset. Cost watchdog and
HV-plateau termination jointly govern run length; the final cost reading was $4.1874 and the
run reached generation 11 of the planned 20.

</details>
