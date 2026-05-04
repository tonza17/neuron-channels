---
spec_version: "2"
task_id: "t0080_bedb_mobo_v3_dendritic_spike_nsga2"
date_completed: "2026-05-04"
status: "complete"
---
# Plan: Bed B v3 MOBO with Dendritic-Spike Machinery and NSGA-II

## Objective

Run a 54-d multi-objective optimisation (NSGA-II via pymoo, replacing t0078's BoTorch qLogNEHVI) on
the de Rosenroll 2026 Bed B DSGC compartmental model in NEURON, augmented with three additions
absent from the t0078 49-d substrate: (1) Mg-block NMDA at all dendritic compartments using the
existing t0024 `Exp2NMDA` POINT_PROCESS (no new MOD file); (2) Nav1.6 + NaP at distal-dendrite
densities using the t78 (renamed t80) MOD pack at densities informed by Sivyer 2013 / Oesch 2005 /
Schachter 2010 / Hay 2011 priors; (3) hard biological lower bounds on AIS-related parameters
(`nav16_ais` >= 0.25 S/cm^2 per Kole 2008 lower bound; AIS-to-soma Nav ratio >= 5 per Werginz 2024
mouse alpha-RGC measurement) so the optimiser cannot collapse to the AIS-disabled corner observed at
t0078 iter 81.

The optimiser jointly maximises the direction-selectivity index (DSI = (R_pref - R_null) / (R_pref +
R_null)) and the preferred-direction (PD) firing rate, computed as the peak rate of the
Gaussian-convolved (sigma = 25 ms) spike train per Trenholm 2013 convention.

The pass criterion is binary: locate at least one Pareto cell with **DSI >= 0.4 AND PD rate >= 10
Hz**, anchored to Rivlin-Etzion 2012 stable-cell joint distribution (DSI 0.78 +/- 0.19, mean PD rate
10.38 +/- 8.53 Hz, n = 8) and Trenholm 2013 peak-rate-under-Gaussian-convolution; OR rule out the
joint operating point architecturally with a clean negative-result document. Either outcome is a
strong project result. Done = a v3 library asset (`de_rosenroll_2026_dsgc_ais_dendritic_spike`); a
substrate-regression check at the t0076 iter-424 parameter vector mapped to the v3 54-d
parameterisation; a pre-launch smoke gate; one Pareto front
+ hypervolume trajectory + per-direction Vm-trace deep-dive PNGs; per-cell registered project
  metrics; an answer asset `mobo-on-biophysics-ais-disabled-corner` documenting the t0078 iter-81
  failure mode and the now-enforced biological-prior checklist; and a clean Vast.ai cost / teardown
  record at or below the **$2.00 hard cap**.

## Task Requirement Checklist

The operative task text quoted verbatim from `task.json` and `task_description.md`:

> Bed B v3 MOBO with dendritic-spike machinery and NSGA-II. Add dendritic-spike machinery to
> AIS-augmented Bed B; switch from BoTorch qLogNEHVI to NSGA-II via pymoo; enforce hard biological
> bounds; test joint DSI/PD pass.

> In scope: Build a new library asset extending the t0078 `de_rosenroll_2026_dsgc_ais` substrate
> with dendritic-spike machinery: Mg-block NMDA at active densities on dendrites (Exp2NMDA with
> voltage-dependent Mg block bound into the bipolar -> DSGC excitatory channel) and Nav1.6 + NaP at
> distal-dendrite densities sufficient for back-propagating APs and dendritic spikes per Sivyer 2013
> / Oesch 2005 priors.

> Replace the BoTorch qLogNEHVI optimiser with NSGA-II via pymoo
> (`pymoo.algorithms.moo.nsga2.NSGA2`). Configuration: pop 96, 40 generations (3,840 evaluations),
> SBX crossover eta=15, polynomial mutation eta=20, tournament selection, Latin Hypercube Sampling
> or Sobol initial population.

> Enforce hard biological lower bounds on AIS-related parameters: `nav16_ais` >= 0.25 S/cm^2 (Kole
> 2008 cortical pyramidal patch-clamp prior; lower bound of the Kole [0.25, 0.5] range); AIS-to-soma
> Nav ratio >= 5 (Werginz 2024 mouse alpha-RGC; biologically plausible lower bound, well below the
> measured 17.3).

> Pre-run substrate regression check (folded in from S-0078-02): re-evaluate the t0076 iter-424
> parameter vector (DSI 0.42 / PD 8.34 Hz) on the v3 49-d substrate as a one-shot validation cell
> before launching the NSGA-II loop. Document the substrate-regression delta.

> Produce one answer asset (folded in from S-0078-08) documenting the AIS-disabled-corner failure
> mode observed at t0078 iter 81 and the biological-prior checklist now enforced as hard MOBO
> bounds.

> Pass criterion: at least one Pareto cell with DSI >= 0.4 AND PD rate >= 10 Hz, OR rule it out
> architecturally with a clean negative result.

> Compute: Vast.ai 64-core CPU EPYC 7B13 class at ~$0.16/hr; cost target $1.00-$1.50 total; hard cap
> $2.00.

> Out of scope: `tau_ca_multiplier` upper bound stays at 20x (S-0078-03 NOT folded in).
> Single-objective scalarised BO comparison (S-0078-04 separate). Multi-replicate Sobol seed and BO
> chain replication (S-0078-06 separate). Promotion of the NSGA-II harness into a substrate-agnostic
> library (deferred until at least one more substrate uses it).

> Expected assets: 1 library asset, 1 answer asset.

Concrete requirements decomposed into checklist items with stable IDs (covered by step numbers in
parentheses):

* **REQ-1**: Build a v3 library asset extending the t0078 substrate with dendritic-spike machinery,
  registered at `assets/library/de_rosenroll_2026_dsgc_ais_dendritic_spike/`. Satisfied by Steps 1,
  2, 3, 4, 5, 12. Evidence: `details.json` + `description.md` + `module_paths` resolvable; verified
  by `verify_libraries.py` returning 0 errors.
* **REQ-2**: Add Exp2NMDA-based Mg-block NMDA at all dendritic compartments (proximal, mid,
  terminal) using the t0024 `Exp2NMDA` POINT_PROCESS unchanged. Satisfied by Steps 4, 5. Evidence:
  `code/trial_helpers.py` instantiates `h.Exp2NMDA` co-located with each ACh placement; smoke test
  inspects `cell.all_dends[0]` for the new point process count.
* **REQ-3**: Add Nav1.6 (`nav16t80`) and NaP (`napt80`) at the terminal-dendrite (distal) tier at
  densities `nav16_dend_distal` in [0, 0.05] S/cm^2 (Schachter 2010 / Sivyer 2013 prior) and
  `nap_dend_distal` in [0, 0.01] S/cm^2 (Hay 2011 somatic NaP upper bound). Satisfied by Steps 3, 5.
  Evidence: `apply_params.py` writes `gbar_nav16t80` and `gbar_napt80` on `cell.terminal_dends`;
  `psection()` smoke check confirms the densities at iter-0 of the substrate regression.
* **REQ-4**: Vendor the 13 t78 MOD files into the t80 namespace (rename SUFFIX `*t78` to `*t80` in
  each file). Satisfied by Step 2. Evidence: `grep -r "SUFFIX.*t78" code/mods/` returns 0 matches;
  `grep -r "SUFFIX.*t80" code/mods/` returns 13 matches.
* **REQ-5**: Reuse the t0024 `Exp2NMDA` POINT_PROCESS unchanged for dendritic NMDA (do NOT vendor a
  new NMDA MOD file). Satisfied by Step 4. Evidence: `code/mods/` does not contain any NMDA MOD;
  Step 4 imports `h.Exp2NMDA` from the t0024 vendored DLL.
* **REQ-6**: Replace the BoTorch qLogNEHVI optimiser with `pymoo.algorithms.moo.nsga2.NSGA2`,
  population 96, 40 generations, SBX `eta=15`, polynomial mutation `eta=20`, tournament selection,
  initial population from Latin Hypercube Sampling (`pymoo.operators.sampling.lhs.LHS`). Satisfied
  by Steps 6, 8. Evidence: `code/nsga2_loop.py` imports
  `from pymoo.algorithms.moo.nsga2 import NSGA2` and `from pymoo.operators.sampling.lhs import LHS`;
  `grep -r "qLogNoisyExpected" code/` returns 0 matches; `pyproject.toml` pins `pymoo>=0.6.1.6`.
* **REQ-7**: Enforce hard lower bound `nav16_ais >= 0.25 S/cm^2` (Kole 2008). Satisfied by Step 3.
  Evidence: `code/constants.py` `LOWER_BOUNDS[ParamIndex.NAV16_AIS_GBAR] == 0.25`; the LHS initial
  population samples nothing below this value.
* **REQ-8**: Enforce hard constraint AIS-to-soma Nav ratio >= 5 (Werginz 2024) via pymoo
  `n_ieq_constr` constraint. Satisfied by Step 6. Evidence: `BedBV3Problem.__init__` passes
  `n_ieq_constr=1`; `_evaluate(X, out)` computes `out["G"] = [5.0 - x[NAV16_AIS] / x[NAV16_SOMA]]`
  per row.
* **REQ-9**: Pre-launch substrate regression check at the t0076 iter-424 parameter vector mapped to
  the v3 54-d parameterisation. Satisfied by Step 7. Evidence: `code/regression_check.py` writes
  `results/regression_check.json` with the v3-mapped DSI / PD rate alongside the t0076 reference
  values (DSI 0.4244, PD 4.95 Hz at TSTOP=1000; t0078 reports the same cell at PD 8.34 Hz at
  TSTOP=1400).
* **REQ-10**: Stimulus protocol = 8 directions x 20 seeds, trial length 1400 ms, FULL HH-on mode.
  Satisfied by Step 5. Evidence: `code/constants.py` carries `TSTOP_MS = 1400.0`,
  `N_DIRECTIONS = 8`, `N_SEEDS_PER_DIRECTION = 20`, `STIMULUS_KIND = StimulusKind.FULL`.
* **REQ-11**: Compute per-cell registered metrics for every Pareto cell:
  `direction_selectivity_index`, PD firing rate (Hz), `tuning_curve_hwhm_deg`,
  `tuning_curve_reliability`, `tuning_curve_rmse`. Satisfied by Steps 9, 10. Evidence:
  `results/metrics.json` carries one variant per Pareto cell with all five registered keys.
* **REQ-12**: Generate Pareto-front, hypervolume-trajectory, and per-direction Vm-trace deep-dive
  PNGs in `results/images/`. Satisfied by Step 10. Evidence: `ls results/images/*.png | wc -l`
  returns >= 5 (1 Pareto front + 1 HV trajectory + at least 3 deep-dive Vm panels).
* **REQ-13**: NSGA-II loop checkpoints per generation; cost gating writes
  `intervention/budget_overrun.md` and halts cleanly at the $2.00 hard cap. Satisfied by Step 8.
  Evidence: `code/nsga2_loop.py` constants `SOFT_BUDGET_USD = 1.50`, `HARD_BUDGET_USD = 2.00`; the
  intervention file path is `intervention/budget_overrun.md`.
* **REQ-14**: Vast.ai 64-core CPU EPYC 7B13 class at ~$0.16/hr; fall back to 36- or 72-core EPYC
  family at <= $0.20/hr if unavailable. Satisfied by Step 8. Evidence: `code/run_remote.sh`
  documents the instance class; `results/remote_machines_used.json` records the actual instance type
  + hourly rate.
* **REQ-15**: Produce 1 answer asset `mobo-on-biophysics-ais-disabled-corner` documenting the t0078
  iter-81 AIS-disabled-corner failure mode, the biological-prior checklist (Kole 2008 / Werginz
  2024), and general guidance for future MOBO-on-biophysics tasks. Satisfied by Step 11. Evidence:
  `assets/answer/mobo-on-biophysics-ais-disabled-corner/` has `details.json`, `short_answer.md`,
  `full_answer.md`; `verify_answer_asset.py` returns 0 errors.
* **REQ-16**: Use Pareto-front data from t0076 iter-424
  (`tasks/t0076_bedb_dsi_firing_rate_mobo/results/data/pareto_front.json` lines 70-99) for the
  substrate-regression mapping. Satisfied by Step 7. Evidence: `code/regression_check.py` reads the
  exact 25-d parameter vector from that file; `regression_check.json` echoes the source path and
  iteration index.
* **REQ-17**: Reuse the t0078 NEURON-fresh-subprocess pattern (`ProcessPoolExecutor`, one fresh
  worker per cell evaluation) inside the NSGA-II `Problem._evaluate` to avoid the
  `Exp2NMDA name already exists` re-init error. Satisfied by Step 6. Evidence: `nsga2_loop.py`
  passes `Problem` (not `ElementwiseProblem`) so the trial driver's existing pool is reused; pymoo
  is invoked **without** `StarmapParallelization` to avoid double-nesting.
* **REQ-18**: Track `is_unstable = False` per cell; discard unstable evaluations from the Pareto
  computation. Satisfied by Steps 5, 9. Evidence: `_summarise_trials` records `is_unstable` per
  cell; the Pareto extraction filters them.
* **REQ-19**: Cost is at or below the $2.00 hard cap. Satisfied by Steps 8, 13. Evidence:
  `results/costs.json` `total_usd` <= $2.00; the cost-gate intervention file is absent or
  documented.
* **REQ-20**: Hold `tau_ca_multiplier` upper bound at 20x (NOT extended; S-0078-03 explicitly out of
  scope). Satisfied by Step 3. Evidence: `LOWER_BOUNDS / UPPER_BOUNDS` for `SKAHP_TAU_CA_MULTIPLIER`
  are `[1.0, 20.0]` identical to t0078.
* **REQ-21**: Hold the t0078 49-d ParameterVector layout invariant (do NOT reorder existing indices
  0-48); add the new dendritic-spike parameters strictly at indices 49-53. Satisfied by Step 3.
  Evidence: `ParamIndex` enum values 0-48 unchanged from t0078; values 49-53 are new (`GNMDA_DEND`,
  `MG_CONC_MM`, `VOFF_NMDA`, `NAV16_DEND_DISTAL`, `NAP_DEND_DISTAL`).

## Approach

### Recommended task type and influence on approach

The task is tagged `build-model` + `experiment-run` + `answer-question` in `task.json`. All three
apply: the build-model guidelines drive the v3 library construction (extending the t0078 substrate,
adding dendritic-spike machinery, registering `de_rosenroll_2026_dsgc_ais_dendritic_spike`); the
experiment-run guidelines drive the NSGA-II search loop, the per-cell metric computation, the
registered-metrics traceability, and the cost / teardown discipline; the answer-question guidelines
drive the `mobo-on-biophysics-ais-disabled-corner` answer asset that documents the t0078 iter-81
failure mode and the now-enforced biological-prior checklist as a transferable methodology. The plan
reflects all three: Steps 2-5 (build), Steps 6-10 (experiment), Step 11 (answer).

### Architectural additions over t0078

**Mg-block NMDA on all dendrites (REQ-2, REQ-5)**: Bed B's published model (Poleg-Polsky 2016
ModelDB 189347) places NMDARs only on ON-layer bipolar contacts. The v3 plan extends NMDA to all
dendritic compartments (ON + OFF) by instantiating one `h.Exp2NMDA` per existing ACh placement,
co-located on the same section / position, sharing the NetStim and gated by an additional NetCon
with weight `gnmda_dend`. The t0024 `Exp2NMDA.mod` (with parameters `tau1 = 50 ms`, `tau2 = 2 ms`,
`e = 0 mV`, voltage dependence `g = gmax / (1 + n * exp(-gama * v))` with `gama = 0.074 /mV`,
`Voff = 0`, `Vset = -60`) is mathematically equivalent to the canonical Jahr-Stevens form when `n`
is reinterpreted as `[Mg]/IC50_at_0mV`. Three new MOBO parameters are added: `gnmda_dend` (NetCon
weight in uS, log-uniform 1e-5 .. 1e-2), `mg_conc_mm` (linear 0.1 .. 0.5 /mM, written to
`Exp2NMDA.n`), and `voff_nmda` (currently held at the t0024 default; binary toggle deferred per
researcher decision).

**Nav1.6 + NaP at distal-dendrite densities (REQ-3)**: Schachter 2010 used 40 mS/cm^2 uniform
dendritic Nav with a 45 -> 20 proximal-distal gradient; Sivyer 2013 argues qualitatively for
"physiologically plausible densities" without giving a number. The v3 plan bounds
`nav16_dend_distal` in [1e-5, 0.05] S/cm^2 (LHS biased toward 0.02-0.04) and `nap_dend_distal` in
[1e-5, 0.01] S/cm^2 (Hay 2011 somatic NaP upper bound carried over to distal as an upper biological
cap). Both densities are written to `cell.terminal_dends` only via the existing t78/t80 pack's
`nav16t80` and `napt80` SUFFIXes; no new MOD file is needed.

**Hard biological lower bounds on AIS Nav (REQ-7, REQ-8)**: t0078's iter 81 collapsed `nav16_ais` to
1e-5 S/cm^2 (five orders below Kole 2008's [0.25, 0.5] range; AIS-to-soma Nav ratio 5.5e-5 vs
Werginz 2024's measured 17.3 in mouse alpha-RGCs). The v3 plan replaces the soft prior with two hard
constraints: `LOWER_BOUNDS[NAV16_AIS_GBAR] = 0.25` (Kole 2008 lower bound) and an
inequality-constraint `5.0 - nav16_ais / nav16_soma <= 0` enforced via pymoo `n_ieq_constr`. NSGA-II
treats individuals violating constraints as dominated by any feasible individual, so no Pareto cell
ever has a sub-bound AIS Nav. Combined upper bound `nav16_ais` <= 5.0 S/cm^2 covers Werginz 2024's
1.3 S/cm^2 mouse alpha-RGC measurement with headroom.

### Optimiser switch from BoTorch qLogNEHVI to pymoo NSGA-II (REQ-6)

t0078 hit O(N^3) Cholesky scaling in BoTorch SingleTaskGP: per-cell wall-clock grew from 28 s in
early phase to 9-12 min after acq 480, forcing early stop at acq 416/700 and a final cost of $3.93.
NSGA-II per-generation cost is independent of accumulated history (only depends on `pop_size = 96`
fixed), so the O(N^3) blow-up is eliminated by algorithm choice. The canonical pymoo recipe from the
official documentation uses `NSGA2(pop_size=96, sampling=LHS())` with default operators (SBX
`eta=15`, polynomial mutation `eta=20`, binary tournament selection, `RankAndCrowding` survival).
`pymoo>=0.6.1.6` is pinned in `pyproject.toml` because earlier versions placed
`StarmapParallelization` in a different submodule (pymoo issue #763).

The NEURON evaluation is done **without** pymoo's `StarmapParallelization` to avoid double-nesting
the existing `ProcessPoolExecutor` worker pool inside the t0078 trial driver. Instead the NSGA-II
problem subclasses `pymoo.core.problem.Problem` (population-batch evaluation, NOT
`ElementwiseProblem`) and dispatches the entire generation's parameter vectors to
`evaluate_parameter_vector` in a single call, which fans out internally over `cpu_count()-1` worker
subprocesses. This preserves the t0078 NEURON-fresh-subprocess pattern verbatim (REQ-17).

Reference point for hypervolume tracking: `[0, 0]` in the negation-flipped (maximisation)
convention, matching t0076 / t0078. Objectives are negated for pymoo's minimisation convention:
`out["F"] = [-dsi, -pd_rate]`.

### Pre-launch substrate regression check (REQ-9, REQ-16)

Before launching the NSGA-II loop, evaluate the t0076 iter-424 parameter vector
(`tasks/t0076_bedb_dsi_firing_rate_mobo/results/data/pareto_front.json` lines 70-99: DSI 0.4245, PD
4.95 Hz at TSTOP=1000) mapped to the v3 54-d parameterisation. Mapping: each of the 12
uniform-density channels becomes 5 tier-stratified densities replicated across all 5 tiers (so all
tiers get the same density); `nav16_ais` is set to the Kole prior centre 0.375 S/cm^2; AIS geometry
is set to the midpoint (length 30 um, diameter 0.8 um); `tau_ca_multiplier = 1.0`; all new
dendritic-spike parameters are at 0 (`gnmda_dend = 0`, `nav16_dend_distal = 0`,
`nap_dend_distal = 0`, `mg_conc_mm = 0.5`). The expected v3 result is DSI in [0.37, 0.47] AND PD
rate in [3.95, 9.34] Hz (the wide PD band accommodates the t0076 1000-ms vs t0078/t0080 1400-ms
TSTOP discrepancy). Both numbers are written to `results/regression_check.json` alongside the t0076
reference values for unambiguous comparison. Pass: reproduce DSI within +/- 0.05.

### Alternatives considered

1. **NSGA-III instead of NSGA-II**. NSGA-III defaults SBX `eta=30` and is designed for >= 3
   objectives. With 2 objectives (DSI, PD rate), NSGA-II's pairwise crowding-distance survival is
   well-matched and is the literature default. Rejected.
2. **Soft regularisation term penalising AIS-disabled corner instead of hard bounds**. E.g., add
   `+lambda * max(0, 0.25 - nav16_ais)^2` to the loss. Rejected because the t0078 failure mode IS
   the case where the optimiser found the soft prior was cheaper to violate than to respect; a hard
   parameter bound is the only structural fix.
3. **Add Ca-plateau zone (Larkum BAC firing) instead of Nav1.6 / NaP**. Held as an explicit fallback
   if the v3 substrate fails the pass criterion. Not adopted pre-emptively because (a) the
   research-papers stage identifies dendritic Nav as the dominant DSGC mechanism per Sivyer 2013 /
   Oesch 2005 / Schachter 2010, and (b) the Ca-plateau requires a richer Ca handling chain (Ca_LVA +
   extended CaDynamics) that doubles the new-parameter count.
4. **Use pymoo `StarmapParallelization` with `multiprocessing.Pool(64)`**. Rejected because it
   double-nests the existing trial-driver pool; the NEURON re-init bug is silent and intermittent
   when subprocesses are nested.
5. **Vendor a separate NMDA MOD file (e.g., `bipolarNMDA.mod` from t0046 / ModelDB 189347)**.
   Rejected because the t0024 `Exp2NMDA` POINT_PROCESS is already loaded by every Bed B substrate
   and is mathematically equivalent to the canonical Jahr-Stevens form. Adding a second NMDA MOD
   would risk SUFFIX collisions (the same lesson as the `cadecay` collision avoided in t0078).

### Library asset name and v3 substrate scope

The v3 library asset is `de_rosenroll_2026_dsgc_ais_dendritic_spike` (the name suggested in the task
description). It exposes `build_dsgc_cell_with_ais_dendritic_spike()` as the primary entry point,
the v3 `ParameterVector` dataclass with 54 entries, the extended `apply_parameter_vector`, the
extended `SynapseBundle` (with `syns_nmda` and `ncs_nmda` fields), and the 13 vendored t80 MODs. The
`nsga2_loop.py` is task-private (NOT in the library) per the task description's "Out of scope" note
that promotion to a substrate-agnostic library is deferred until at least one more substrate uses
it.

## Cost Estimation

Itemised dollar amounts, anchored to the t0078 measured cost ($3.93 over 24.86 h on Vast.ai 64-core
EPYC 7B13 instance 36068067 at $0.1582/hr, for 78,560 NEURON simulations):

* **NSGA-II loop wall-clock**: 3,840 cells x 8 dirs x 20 seeds = 614,400 NEURON simulations. Per-
  trial wall-clock ~3.7 s (slightly above t0078's ~3.4 s including the new dendritic-NMDA + distal
  Nav inserts). Total per-core trial time ~3,549 s; parallelised across 64 effective cores
  (`cpu_count()-1 = 63` workers) ~= **0.93 wall-hours = 56 minutes** of pure NEURON evaluation.
* **NSGA-II overhead**: per-generation operator cost (SBX + PM + tournament + crowding-distance) is
  O(pop_size * n_var) = O(96 * 54) = trivial relative to NEURON evaluations. Add 1-2 minutes
  overhead total across 40 generations.
* **Vast.ai instance cost** at $0.1582/hr for ~1.0 wall-hours (NEURON eval) + 0.5 h (provisioning
  + teardown) = 1.5 h x $0.1582 = **$0.24**.
* **Provisioning + teardown overhead** (already counted): 30 min provisioning + 30 min teardown.
* **20% contingency** for any retry / restart overhead and any wall-clock surprise from the new
  dendritic-spike machinery: **$0.05-$0.10**.
* **Subtotal**: ~$0.29-$0.34 raw + setup.
* **Researcher-authorised envelope**: $1.00-$1.50 total.
* **Hard cap (cost gate trigger)**: **$2.00** per task description.

API call costs: $0 (no LLM inference; all compute is local NEURON simulation on the Vast.ai
instance).

Project budget remaining after this task: $5.01 - $1.50 (envelope-aligned estimate) = **$3.51**.
Comfortably below the warn threshold ($8.00) and the per-task $5.00 default limit.

The cost-gate threshold (per-task hard cap $2.00 from task description) IS armed in
`code/nsga2_loop.py`: the loop writes `intervention/budget_overrun.md` and exits cleanly when
elapsed hours x hourly rate >= $2.00.

## Step by Step

The implementation work is organised into four milestones.

### Milestone A: Substrate v3 construction (Steps 1-5)

1. **Set up code directory and copy t0078 harness verbatim into `code/`.** Copy these files verbatim
   from `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/code/` into
   `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/`: `bootstrap.py` (~116 LOC, no change),
   `paths.py` (~76 LOC, edit `resolve_t78_mod_library` -> `resolve_t80_mod_library`),
   `extend_with_ais.py` (~127 LOC, no change), `parametric_placer.py` (~105 LOC, no change),
   `recorder.py` (~122 LOC, no change), `trial_driver.py` (~422 LOC, import-path renames only),
   `plot_pareto.py` (~408 LOC, import-path renames only), `render_pdf.py` (~63 LOC, import-path
   renames only), `run_remote.sh` (~43 LOC, edit task-id constant). Update internal global names
   from `_T78_*` to `_T80_*` throughout where applicable. Leave `build_cell_ais.py` as a thin
   re-export of t0078's. **Expected output**: `ls code/` lists at least 9 Python files plus
   `run_remote.sh`. Satisfies REQ-1 (substrate plumbing).

2. **Vendor 13 t80 MOD files (t78 -> t80 SUFFIX rename).** For each of the 13 t78 MODs in
   `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/code/mods/` (`nav16t78.mod`, `napt78.mod`, `nart78.mod`,
   `kdrt78.mod`, `kv3t78.mod`, `kv4t78.mod`, `kv7t78.mod`, `iht78.mod`, `calt78.mod`, `catt78.mod`,
   `bkt78.mod`, `skt78.mod`, `skahpt78.mod`): copy into `code/mods/` and run `sed -i 's/t78/t80/g'`
   on each file (renames the SUFFIX line and any internal references) and rename the file
   `*t78.mod -> *t80.mod`. **Do NOT vendor `cadecay.mod`** (already in t0024 DLL; would collide).
   **Do NOT vendor any NMDA MOD** (REQ-5 - reuse t0024 `Exp2NMDA`). Compile on Linux with
   `nrnivmodl code/mods/`; verify the resulting `x86_64/.libs/libnrnmech.so` exposes 13 t80
   SUFFIXes. **Expected output**: `grep -r "SUFFIX.*t78" code/mods/` returns 0 matches;
   `grep -r "SUFFIX.*t80" code/mods/` returns 13 matches; the .so compiles cleanly. Satisfies REQ-4.

3. **Extend `code/constants.py` with the 5 new ParamIndex entries and the v3 bounds.** Copy
   `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/code/constants.py` (~471 LOC) into `code/constants.py`.
   Apply the following edits (preserving the t0078 invariant that indices 0-48 keep the same meaning
   \- REQ-21):
   * Add 5 new ParamIndex entries at indices 49-53: `GNMDA_DEND` (49, log-uniform [1e-5, 1e-2] uS),
     `MG_CONC_MM` (50, linear [0.1, 0.5] /mM), `VOFF_NMDA` (51, linear [-10.0, 10.0] mV; held at 0
     by the LHS bias for v3), `NAV16_DEND_DISTAL` (52, log-uniform [1e-5, 0.05] S/cm^2),
     `NAP_DEND_DISTAL` (53, log-uniform [1e-5, 0.01] S/cm^2).
   * Bump `N_PARAMS` from 49 to 54.
   * Extend `LOWER_BOUNDS` and `UPPER_BOUNDS` arrays to length 54, adding the 5 new bound rows.
   * Replace `LOWER_BOUNDS[ParamIndex.NAV16_AIS_GBAR=4] = 1e-5` with `0.25` (Kole 2008 hard floor;
     REQ-7). Keep `UPPER_BOUNDS[ParamIndex.NAV16_AIS_GBAR] = 5.0` (covers Werginz 2024's 1.3 S/cm^2
     with headroom).
   * Extend `LOG_PARAM_INDICES` to include indices 49, 52, 53 (`GNMDA_DEND`, `NAV16_DEND_DISTAL`,
     `NAP_DEND_DISTAL`). `MG_CONC_MM` (50) and `VOFF_NMDA` (51) stay linear.
   * Confirm `UPPER_BOUNDS[ParamIndex.SKAHP_TAU_CA_MULTIPLIER]` stays at `20.0` (REQ-20; not 200x).
   * Add new `@property` accessors on `ParameterVector` for the 5 new fields.
   * Replace t0078's BoTorch defaults (`N_SOBOL_INITIAL`, `N_ACQ_ITERATIONS`) with NSGA-II defaults:
     `POP_SIZE = 96`, `N_GENERATIONS = 40`, `SBX_ETA = 15`, `PM_ETA = 20`, `TOURNAMENT_K = 2`,
     `LHS_SEED = 1`. Add `SOFT_BUDGET_USD = 1.50`, `HARD_BUDGET_USD = 2.00`.

   **Expected output**:
   `uv run python -u -c "from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import N_PARAMS, LOWER_BOUNDS; assert N_PARAMS == 54; assert LOWER_BOUNDS[4] == 0.25"`
   exits with 0. Satisfies REQ-3, REQ-7, REQ-20, REQ-21.

4. **Extend `code/trial_helpers.py` with NMDA bundle fields and Exp2NMDA instantiation.** Copy
   `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/code/trial_helpers.py` (~285 LOC) into
   `code/trial_helpers.py`. Apply the following edits:
   * Extend the `SynapseBundle` dataclass (around line 138 in t0078) with two new fields:
     `syns_nmda: list[Any]` and `ncs_nmda: list[Any]`. Keep `slots=True`, no `frozen` (NEURON
     handles).
   * Extend `setup_synapses_parametric` (around line 202): for each ACh placement, additionally
     instantiate `h.Exp2NMDA(syn_section(0.5))` and a `h.NetCon` from the same NetStim that drives
     the ACh `Exp2Syn`, with weight = `gnmda_dend` (read from `ParameterVector.gnmda_dend`). Set
     RANGE parameters on each Exp2NMDA: `tau1 = 50.0`, `tau2 = 2.0`, `e = 0.0`, `n = mg_conc_mm`
     (read from `ParameterVector.mg_conc_mm`), `gama = 0.074`, `Voff = 0.0`, `Vset = -60.0`. Append
     to `bundle.syns_nmda` and `bundle.ncs_nmda`.

   **Expected output**: smoke test `code/test_synapse_bundle_nmda.py` (new, ~30 LOC) builds a v3
   cell with `gnmda_dend = 1e-3` and asserts `len(bundle.syns_nmda) == len(bundle.syns_ach)` and
   that each Exp2NMDA reports `n == 0.3` when `mg_conc_mm = 0.3`. Satisfies REQ-2, REQ-5.

5. **Extend `code/apply_params.py` with two new write steps for distal Nav1.6 + NaP and the NMDA
   range-parameter update.** Copy `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/code/apply_params.py`
   (~215 LOC) into `code/apply_params.py`. Apply the following edits (preserving the t0078 7-step
   write order; REQ-21 invariant):
   * Rename `ensure_t78_dll_loaded` to `ensure_t80_dll_loaded`; update `resolve_t78_mod_library`
     reference to `resolve_t80_mod_library` (paths.py change in Step 1).
   * Insert a new write step `_write_dendritic_distal_nav` (called between current step 5
     stratified-densities and current step 6 AIS-stratified-densities) that writes
     `gbar_nav16t80 = nav16_dend_distal` and `gbar_napt80 = nap_dend_distal` to every section in
     `cell.terminal_dends`. Note: terminal-tier `nav16t80` is already written by the existing
     stratified loop at index `NAV16_TERMINAL_GBAR`; the new write OVERLAYS the stratified value and
     ADDS NaP at terminal (NaP is not stratified in t0078 for terminal). Document this overlay in a
     code comment.
   * Insert a new write step `_write_dendritic_nmda` (called after `setup_synapses_parametric` so
     the SynapseBundle exists) that updates the NMDA point processes' `n` (Mg conc) range parameter
     from `mg_conc_mm`. The Exp2NMDA point processes themselves are instantiated by Step 4
     (trial_helpers); this step only updates RANGE values when the parameter vector changes per
     generation.
   * Confirm `TSTOP_MS` is read from the updated `code/constants.py` (REQ-10).

   **Expected output**: smoke test `code/test_apply_params_v3.py` (new, ~50 LOC) applies a v3
   ParameterVector with `nav16_dend_distal = 0.04` and `nap_dend_distal = 0.005`, builds the cell,
   then calls `psection()` on `cell.terminal_dends[0]` and asserts the printed dict contains
   `nav16t80: {'gbar': 0.04, ...}` and `napt80: {'gbar': 0.005, ...}`. Satisfies REQ-3, REQ-10.

### Milestone B: NSGA-II loop and substrate regression (Steps 6-8)

6. **Write `code/nsga2_loop.py` from scratch.** Estimated ~250-300 LOC. The module defines:
   * A `BedBV3Problem(pymoo.core.problem.Problem)` subclass with `n_var = 54`, `n_obj = 2`,
     `n_ieq_constr = 1` (REQ-8: AIS-to-soma Nav ratio), `xl = LOWER_BOUNDS`, `xu = UPPER_BOUNDS`.
     Note: bounds for log-space parameters are stored in natural units; the LHS sampler operates in
     natural units and `apply_parameter_vector` consumes natural units, so no in-loop log/exp
     transform is required.
   * `_evaluate(self, X: NDArray, out: dict, *args, **kwargs) -> None`: for each row `x` in `X`,
     call `evaluate_parameter_vector(ParameterVector(x))` (which fans out to its own
     `ProcessPoolExecutor` per cell - REQ-17, NO double-nesting via `StarmapParallelization`).
     Compute `dsi`, `pd_rate_hz`, `is_unstable`, `peak_vm_mv`. Set
     `out["F"][i] = [-dsi, -pd_rate_hz]` when feasible; if `is_unstable`, set both to a worst-case
     sentinel value (e.g., `1e6`). Set
     `out["G"][i] = [5.0 - x[NAV16_AIS_GBAR] / x[NAV16_SOMA_GBAR]]`. Per-cell wall-clock and the
     elapsed-cost gate are checked here; on cost-gate trip, write `intervention/budget_overrun.md`
     and raise a controlled exit (REQ-13, REQ-19).
   * `run_nsga2_loop(*, task_id: str, hourly_rate_usd: float, seed: int = 1) -> None`: the main
     entry-point. Constructs `BedBV3Problem(...)`, then
     `algorithm = NSGA2(pop_size=POP_SIZE, sampling=LHS(), crossover=SBX(eta=SBX_ETA), mutation=PM(eta=PM_ETA))`;
     `res = minimize(problem, algorithm, ('n_gen', N_GENERATIONS), seed=seed, verbose=True, save_history=True)`.
     Writes `results/data/pareto_front.json` (with
     `cells: [{params, dsi, pd_rate_hz, is_feasible, ...}]`) and `results/data/hv_trajectory.json`
     (`HV` indicator with ref point `[0, 0]` after objective sign-flip). Per-generation checkpoint
     pickle of the pymoo `Algorithm` state to `results/data/nsga2_checkpoint_gen_NNN.pkl`.
   * Constants pinned at top of file: `pop_size`, `n_gen`, etas, `SOFT_BUDGET_USD = 1.50`,
     `HARD_BUDGET_USD = 2.00`, `BUDGET_OVERRUN_FILE = 'intervention/budget_overrun.md'`.

   **Validation gate (small)**: before any full run, execute `code/nsga2_loop.py --smoke` which runs
   `pop_size=4, n_gen=2 = 8 evaluations` locally on Windows (~5 min). Confirm: (a) all 8 cells
   return DSI in [0.0, 1.0] and `pd_rate_hz >= 0`, (b) `is_unstable = False` on at least 6 of the 8,
   (c) the Pareto-front length is 1-4, (d) hypervolume is positive. **Trivial baseline**: t0078's
   iter-0 LHS mean DSI is approximately 0.10 (per t0078 results); v3's mean LHS DSI on the smoke run
   should land in [0.05, 0.40]. **Failure condition**: if mean smoke DSI is below 0.05 or above
   0.50, halt and inspect the v3 substrate; do NOT proceed to Vast.ai.

   **Expected output**: `code/nsga2_loop.py --smoke` exits 0; the printed Pareto front has 1-4
   non-dominated cells. Satisfies REQ-6, REQ-8, REQ-13, REQ-17, REQ-18.

7. **[CRITICAL] Pre-launch substrate regression check at t0076 iter-424 parameters.** Create
   `code/regression_check.py` (~120 LOC) that:
   * Reads the 25-d parameter vector from
     `tasks/t0076_bedb_dsi_firing_rate_mobo/results/data/pareto_front.json` lines 70-99 (iter index
     424; DSI 0.4245, PD 4.95 Hz at TSTOP=1000).
   * Maps the 25-d vector into the v3 54-d ParameterVector by replicating each of the 12
     uniform-density channel values across all 5 tier-stratified slots (so soma + 4 dendrite tiers
     get the same density), setting `nav16_ais` to the Kole prior centre 0.375 S/cm^2, AIS geometry
     to the midpoint (length 30 um, diameter 0.8 um), `tau_ca_multiplier = 1.0`,
     `skahp_gbar_soma_ais = 0.0` (skahp at zero so it does not perturb the t0076 baseline), and all
     5 new dendritic-spike parameters at their lowest meaningful values: `gnmda_dend = 0.0`,
     `mg_conc_mm = 0.5`, `voff_nmda = 0.0`, `nav16_dend_distal = 0.0`, `nap_dend_distal = 0.0`.
   * Calls `evaluate_parameter_vector(...)` once with the canonical 8 dirs x 20 seeds protocol.
   * Writes `results/regression_check.json` with the v3 DSI / PD rate alongside the t0076 reference
     (`dsi_t0076_ref = 0.4245`, `pd_rate_hz_t0076_tstop1000 = 4.95`,
     `pd_rate_hz_t0078_tstop1400 = 8.34`). Includes the source path and iteration index (REQ-16).

   **Failure mode**: if v3 DSI is outside [0.37, 0.47], STOP - the substrate-regression check
   reveals a bug in the v3 substrate. The most likely causes are (a) the t0076-vs-t78/t80 SUFFIX
   rename has missed a write site, (b) the new dendritic-NMDA bundle has nonzero NMDA contribution
   even at `gnmda_dend = 0` due to a NetCon weight bug, or (c) the AIS Nav floor of 0.25 S/cm^2
   distorts the t0076 baseline (this is the expected change; document it). PD rate band [3.95, 9.34]
   is wider to accommodate the t0076 1000-ms vs t0078/t0080 1400-ms TSTOP discrepancy.

   **Expected output**: `regression_check.json` exists with `dsi` in [0.37, 0.47] AND `pd_rate_hz`
   in [3.95, 9.34]. Satisfies REQ-9, REQ-16.

8. **[CRITICAL] Provision Vast.ai instance and run the NSGA-II loop.** Use the orchestrator's
   `setup-machines` step to provision a 64-core EPYC 7B13 at $0.16/hr (matching t0078 instance
   36068067); fallback documented in Risks. SSH into the instance, clone the worktree branch,
   `nrnivmodl code/mods/` to compile the t80 DLL on Linux, then launch
   `bash code/run_remote.sh --task-id t0080_bedb_mobo_v3_dendritic_spike_nsga2 --pop-size 96 --n-gen 40`.
   The NSGA-II loop checkpoint-writes `nsga2_checkpoint_gen_NNN.pkl` after every generation.

   **Validation gate (LHS-phase)**: after the 96 LHS initial cells complete (~8 minutes), check
   `results/data/lhs_summary.json` - mean DSI should be in [0.05, 0.40] (matches the v3 smoke
   baseline from Step 6) and at least 90% of cells should have `is_unstable = False`. If unstable
   cells exceed 10%, halt and inspect parameter ranges (most likely the new `nav16_dend_distal`
   upper bound 0.05 S/cm^2 is too high for runaway-depolarisation safety - tighten to 0.03 before
   re-launching).

   **Validation gate (mid-run, generation 20)**: at generation 20, check that hypervolume has
   increased by >= 25% from the LHS baseline; if not, the NSGA-II convergence is failing and the
   pass criterion is unlikely to be met - halt and inspect the front geometry. (If front geometry
   shows the optimiser saturating, the negative-result case is engaged; that is acceptable per the
   pass criterion clause.)

   Total wall-clock 0.8-1.5 h (NEURON eval) plus 0.5 h provisioning + 0.5 h teardown = 1.8-2.5 h
   total. **Expected output**: `results/data/pareto_front.json` with at least one non-dominated
   cell; `results/data/hv_trajectory.json` per-generation HV; 40 checkpoint pickles in
   `results/data/`. Satisfies REQ-6, REQ-13, REQ-14, REQ-19.

### Milestone C: Pareto extraction, metrics, and visualisation (Steps 9-10)

9. **Compute per-cell registered metrics on the Pareto front.** Create `code/compute_metrics.py`
   (~150 LOC) that walks the Pareto-front cells from `results/data/pareto_front.json`, builds
   per-cell 8-direction tuning curves from the trial driver outputs, and computes:
   * `direction_selectivity_index` (registered metric, key=`direction_selectivity_index`) - already
     in the trial driver output; copy verbatim.
   * PD firing rate (Hz) - already in the trial driver output; this is the `out["F"][1]` value after
     sign-flip back to maximisation.
   * `tuning_curve_hwhm_deg` (registered metric) - via
     `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.metrics.compute_hwhm_deg`.
   * `tuning_curve_reliability` (registered metric) - via
     `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.metrics.compute_reliability`.
   * `tuning_curve_rmse` (registered metric) - via
     `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.metrics.compute_tuning_curve_rmse`
     against the t0004 cosine target.

   Discard unstable cells (peak Vm outside [-80, +60] mV at any trial; REQ-18). Write
   `results/metrics.json` using the **explicit multi-variant** format (per
   `arf/specifications/metrics_specification.md`) with one variant per Pareto cell, named
   `pareto_cell_iter_NNN`, plus a `pareto_best_joint` variant pointing to the cell with the smallest
   distance to the bio-grounded target (DSI 0.4, PD rate 10 Hz). Each variant carries all five
   registered metrics where computable; `None` is used where not computable (never `0.0` per Python
   style guide). The substrate-regression-check cell (Step 7) is also written as a separate variant
   `substrate_regression_t0076_iter_424`.

   **Expected output**: `results/metrics.json` exists with at least 2 variants and registered-metric
   keys for every Pareto cell. Satisfies REQ-11, REQ-18.

10. **Generate Pareto-front, hypervolume-trajectory, and per-direction Vm-trace deep-dive plots.**
    Run
    `uv run python -u -m tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.plot_pareto --task-id t0080_bedb_mobo_v3_dendritic_spike_nsga2 --n-deep-dives 3`,
    which produces:
    * `results/images/pareto_front.png` - 2D scatter (DSI vs PD rate) with t0076 and t0078 Pareto
      fronts overlaid as comparisons; bio-grounded threshold (DSI 0.4 / PD rate 10 Hz) drawn as a
      dashed line.
    * `results/images/hypervolume_trajectory.png` - per-generation hypervolume (utopia point
      `[0.7, 80]` for cross-task comparison with t0076 final HV 8.41 and t0078 final HV 11.41).
    * `results/images/deep_dive_NNN.png` (3 files) - per-Pareto-cell tuning curves and per-direction
      Vm trace panels for the 3 picks: closest-to-joint (smallest distance to (DSI 0.4, PD rate 10
      Hz)), max-DSI on the Pareto front, max-PD on the Pareto front.

    Use
    `tasks.t0011_response_visualization_library.code.tuning_curve_viz.cartesian.plot_cartesian_tuning_curve`
    and `plot_polar_tuning_curve` for the deep-dive panels. The deep-dive subprocess pattern
    (`ProcessPoolExecutor(max_workers=1)`) is preserved from t0078 for the
    `Exp2NMDA name already exists` re-init-bug avoidance.

    **Expected output**: at least 5 PNGs in `results/images/` (1 Pareto front + 1 HV trajectory + 3
    deep-dive). Satisfies REQ-11, REQ-12.

### Milestone D: Answer asset (Step 11)

11. **Create the answer asset `assets/answer/mobo-on-biophysics-ais-disabled-corner/`.** Per
    `meta/asset_types/answer/specification.md`:
    * Question: "Why did the t0078 BoTorch qLogNEHVI MOBO collapse `nav16_ais` to the search-space
      floor (1e-5 S/cm^2) at iter 81, and what biological-prior checklist prevents this failure mode
      in future MOBO-on-biophysics tasks?"
    * `details.json` with `spec_version: "2"`,
      `answer_id: "mobo-on-biophysics-ais-disabled-corner"`, `short_answer_path: "short_answer.md"`,
      `full_answer_path: "full_answer.md"`,
      `answer_methods: ["existing_papers", "prior_tasks", "code_experiments"]`, `source_paper_ids`
      listing Kole 2008 (DOI `10.1038/nn2040`), Werginz 2024 (DOI `10.1523/JNEUROSCI.1592-24.2024`),
      Werginz 2020 (DOI `10.1126/sciadv.abb6642`), Hay 2011 (DOI `10.1371/journal.pcbi.1002107`);
      `source_task_ids` listing t0076, t0078, and t0080 itself; `confidence: "high"`.
    * `short_answer.md` (2-5 sentences in `## Answer`, no inline citations): identifies the failure
      as a soft-prior collapse where the optimiser found that violating the biological prior on AIS
      Nav density was cheaper than respecting it, and states the fix (hard parameter bounds
      `nav16_ais >= 0.25 S/cm^2` from Kole 2008 and AIS-to-soma ratio `>= 5` from Werginz 2024).
    * `full_answer.md` mini-paper format: research process, evidence by source type, the iter-81
      canonical case study, an audit of t0076 + t0078 Pareto fronts for similar collapse-to-floor
      patterns on biologically-priored parameters, the biological-prior checklist (Kole 2008 AIS Nav
      lower bound; Werginz 2024 AIS-to-soma ratio; Hay 2011 NaP upper bound; Schachter 2010 / Sivyer
      2013 dendritic Nav range; Jahr-Stevens NMDA Mg-block convention), general guidance for future
      MOBO-on-biophysics tasks, and limitations (DRD4 ON-OFF DSGCs may sit outside the alpha-RGC AIS
      range; the 5x ratio floor is inferred from non-DSGC patch-clamp).
    * `## Sources` section in `full_answer.md` includes markdown reference link definitions for all
      cited papers and tasks.

    **Expected output**: `verify_answer_asset.py t0080_bedb_mobo_v3_dendritic_spike_nsga2` returns 0
    errors. Satisfies REQ-15.

### Milestone E: Library asset (Step 12)

12. **Create the library asset folder
    `assets/library/de_rosenroll_2026_dsgc_ais_dendritic_spike/`.** Per
    `meta/asset_types/library/specification.md`:
    * `details.json` with `spec_version: "2"`,
      `library_id: "de_rosenroll_2026_dsgc_ais_dendritic_spike"`,
      `name: "De Rosenroll 2026 DSGC with AIS and Dendritic-Spike Machinery"`, `version: "0.1.0"`,
      `description_path: "description.md"`. `module_paths` lists: `code/build_cell_ais.py`,
      `code/extend_with_ais.py` (re-export), `code/apply_params.py`, `code/constants.py`,
      `code/trial_helpers.py`, `code/parametric_placer.py`, `code/trial_driver.py`,
      `code/recorder.py`, `code/bootstrap.py`, `code/paths.py`, plus the 13 t80 MODs in
      `code/mods/`. Entry points: `build_dsgc_cell_with_ais_dendritic_spike` (function),
      `apply_parameter_vector` (function), `DSGCCellWithAIS` (class re-exported from t0078),
      `ParameterVector` (class). `dependencies` lists `["neuron", "numpy"]`.
      `created_by_task: "t0080_bedb_mobo_v3_dendritic_spike_nsga2"`.
    * `description.md` with the mandatory sections (Metadata, Overview, API Reference, Usage
      Examples, Dependencies, Testing, Main Ideas, Summary). The Overview must explain the v3
      additions over t0078 (dendritic NMDA, distal Nav1.6 + NaP, hard biological bounds). API
      Reference must list `build_dsgc_cell_with_ais_dendritic_spike` signature, the v3
      `ParameterVector` (54 fields), and the new `apply_parameter_vector` write steps.

    **Expected output**: `verify_libraries.py t0080_bedb_mobo_v3_dendritic_spike_nsga2` returns 0
    errors. Satisfies REQ-1.

The Step by Step ends here at metric writing, chart generation, library asset, and answer asset.
Results synthesis, suggestions generation, compare-literature, and reporting are
orchestrator-managed steps in execute-task and are NOT part of this implementation plan.

## Remote Machines

One Vast.ai 64-core CPU instance (EPYC 7B13 family, target $0.1582/hr matching t0078 instance
36068067). VRAM not required; this is a CPU-only NEURON simulation workload. Estimated runtime
0.8-1.5 h for the NSGA-II loop plus 30 min provisioning + 30 min teardown + ~10 min for deep-dive
plotting. Fallback if the t0078 instance type is unavailable: any 36- to 72-core CPU instance at <=
$0.20/hr satisfies the per-trial wall-clock requirement; see Risks for the fallback procedure. The
`code/run_remote.sh` launcher (copied from t0078, edited task-id) handles git checkout + nrnivmodl +
nohup background launch + log streaming.

## Assets Needed

* **t0024 library `de_rosenroll_2026_dsgc`** - Bed B substrate. Imported via
  `from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import build_dsgc_cell`.
* **t0024 vendored sources** at
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/` -
  `RGCmodelGD.hoc`, `HHst_noiseless.mod`, `cadecay.mod`, `Exp2NMDA.mod` (REQ-5), `nrnmech.dll`. Used
  at runtime by `build_dsgc_cell()`.
* **t0078 library `de_rosenroll_2026_dsgc_ais`** - AIS-augmented Bed B substrate. The t0078 code is
  the direct ancestor of the t0080 code: `bootstrap.py`, `paths.py`, `extend_with_ais.py`,
  `parametric_placer.py`, `recorder.py`, `trial_driver.py`, `plot_pareto.py`, `render_pdf.py`,
  `run_remote.sh`, `constants.py`, `apply_params.py`, `trial_helpers.py`, `build_cell_ais.py`, and
  the 13 t78 MODs are all copied into `tasks/t0080_*/code/` in Steps 1, 2, 3, 4, 5.
* **t0076 Pareto front data** at
  `tasks/t0076_bedb_dsi_firing_rate_mobo/results/data/pareto_front.json` lines 70-99 - read in Step
  7 (regression check) and Step 10 (Pareto-front overlay).
* **t0078 Pareto front data** at
  `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/results/data/pareto_front.json` - read in Step 10
  (Pareto-front overlay).
* **t0011 visualization library `tuning_curve_viz`** - imported in Step 10.
* **t0012 metrics library `tuning_curve_loss`** - imported in Step 9.
* **t0004 cosine target tuning curve** - read in Step 9 for `tuning_curve_rmse`.
* **`pymoo` (>= 0.6.1.6) and `numpy`** - new pip dependencies added to `pyproject.toml`. `pymoo` is
  the only new dependency vs t0078 (which used `botorch`).

No external assets (datasets, papers) need to be downloaded by the implementation step; the research
stages have already collected the cited papers.

## Expected Assets

`task.json` `expected_assets` declares `{"library": 1, "answer": 1}`. The implementation produces:

* **Library asset** `de_rosenroll_2026_dsgc_ais_dendritic_spike` at
  `assets/library/de_rosenroll_2026_dsgc_ais_dendritic_spike/`:
  * `details.json` per Step 12 - includes 12 module paths + 13 t80 MOD paths.
  * `description.md` with the 8 mandatory sections.
* **Answer asset** `mobo-on-biophysics-ais-disabled-corner` at
  `assets/answer/mobo-on-biophysics-ais-disabled-corner/`:
  * `details.json` per Step 11.
  * `short_answer.md` with the `## Answer` section (2-5 sentences, no inline citations).
  * `full_answer.md` with the mini-paper format and `## Sources` section with reference links.

The Pareto-front, hypervolume-trajectory, and deep-dive PNGs in `results/images/`, plus
`results/metrics.json`, `results/data/pareto_front.json`, `results/data/hv_trajectory.json`, and the
regression-check JSON, are not asset-typed but are required outputs.

## Time Estimation

| Phase | Wall-clock |
| --- | --- |
| Research (already complete) | - |
| Planning (this step) | ~1 h |
| Steps 1-5: substrate v3 construction (local Windows) | ~2.5 h |
| Step 6: NSGA-II loop module + smoke gate | ~1 h |
| Step 7: substrate regression check (local 1 cell x 160 trials) | ~30 min |
| Step 8: Vast.ai provisioning + NSGA-II loop | ~1.8-2.5 h |
| Step 9: per-cell metrics computation (local) | ~20 min |
| Step 10: chart generation + 3 deep-dives (local) | ~30 min |
| Step 11: answer asset (local) | ~45 min |
| Step 12: library asset (local) | ~30 min |
| **Total (planning + implementation)** | **~7-9 h wall-clock** |

Most of the 7-9 h is active developer time spread across Steps 1-7, 9-12. Step 8 (the Vast.ai
NSGA-II loop) runs unattended for ~1.8-2.5 h.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| NSGA-II fails to match t0078's HV 11.41 (negative methodological result) | Medium | Negative result | Itself a useful methodological finding; document the comparison and the Pareto-front geometry per BluePyOpt failure-pattern analysis. The pass-criterion is satisfied either by reaching DSI 0.4 + PD 10 Hz OR by a clean architectural negative result. |
| Vast.ai 64-core EPYC 7B13 unavailable | Medium | Cost overrun or delay | Fall back to 36-core or 72-core EPYC family at <= $0.20/hr. NSGA-II scaling is linear in cores; 36-core roughly doubles wall-clock to 1.8 h, still within the $2.00 cap at $0.10/hr rates. |
| Substrate regression check fails (REQ-9 / REQ-16) | Medium | Block on Step 7 | If v3 DSI is outside [0.37, 0.47] or PD rate is outside [3.95, 9.34], halt and inspect: (a) t78 -> t80 SUFFIX rename incomplete (Step 2), (b) NMDA bundle has nonzero contribution at `gnmda_dend = 0` (NetCon weight bug), (c) AIS Nav floor of 0.25 distorts the t0076 baseline (expected; document). The substrate-regression check is a documented diagnostic per the task description, NOT a hard blocker - if the delta is structural (e.g., the AIS Nav floor itself causes the delta), document and proceed. |
| Dendritic-spike machinery destabilises the substrate (runaway depolarisation) | Medium | Smoke gate / LHS gate failure | Detect at the Step 6 smoke gate or the Step 8 LHS-phase gate (if `is_unstable >= 10%` of cells). Fallback: tighten `nav16_dend_distal` upper bound from 0.05 to 0.03 S/cm^2 (closer to Schachter 2010's distal-tip target) and `nap_dend_distal` from 0.01 to 0.005 S/cm^2; re-launch. |
| `Exp2NMDA name already exists` re-init bug appears in deep-dive | Low | Deep-dive PNGs missing | Step 10 inherits the t0078 `ProcessPoolExecutor(max_workers=1)` subprocess wrap; verified by running with `--n-deep-dives 3` and confirming all 3 PNGs are emitted. |
| pymoo `StarmapParallelization` import path mismatch (pymoo issue #763) | Low | Loop launch fails | Pin `pymoo>=0.6.1.6` in `pyproject.toml`; the Step 6 smoke gate catches this immediately. |
| NMDA bundle co-location bug (NMDA placed without ACh on a section) | Low | Silent under-counting | Step 4 smoke test asserts `len(syns_nmda) == len(syns_ach)` per cell; halt if violated. |
| Cost cap hit before convergence (>= $2.00) | Low | Run truncated | Step 6 cost gate writes `intervention/budget_overrun.md` and exits cleanly; the partial Pareto front is reported with the cost-of-progress decision. Do NOT extend the cap beyond $2.00 without a brainstorm consult. |
| pymoo objective sign-flip mistake (forget to negate DSI / PD) | Medium | Pareto front collapses to a single bad cell | Step 6 explicitly documents `out["F"] = [-dsi, -pd_rate_hz]`; the smoke gate checks that the resulting Pareto-front cells have positive DSI and positive PD rate after sign-flip-back. |
| New pymoo dependency conflicts with existing `botorch` / `gpytorch` install | Low | Local install fails | `pyproject.toml` keeps `botorch` for backward compat with t0076 / t0078 if needed; pymoo and BoTorch install side-by-side on the same Python via independent dependency trees (verified by t0078 release-notes ecosystem). |
| t0076 iter-424 vector mapping has a unit mismatch | Medium | Substrate regression fails Step 7 | The mapping function in `regression_check.py` must replicate per-tier densities **in S/cm^2** (the 25-d t0076 vector reports natural units in S/cm^2 already; t0078 ParameterVector uses the same units). A unit smoke check at the top of `regression_check.py` asserts `LOWER_BOUNDS[NAV16_SOMA_GBAR] < t0076_iter_424.nav16 < UPPER_BOUNDS[NAV16_SOMA_GBAR]`. |
| AIS-to-soma Nav ratio constraint is too aggressive (>= 5) and shrinks the feasible region too much | Medium | Optimiser stalls | Start at the documented 5x floor; if the LHS-phase gate shows < 50% of cells are feasible, relax to >= 3x as documented in the v3 answer asset's "limitations" section. The 5x floor is below any measured RGC value, so this relaxation does not contradict the literature. |

## Verification Criteria

Concrete, testable checks. Each criterion lists the exact command to run and the expected output:

* **VC-1**: Run
  `cd tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2 && uv run python -u -c "from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import N_PARAMS, LOWER_BOUNDS; assert N_PARAMS == 54; assert LOWER_BOUNDS[4] == 0.25"`
  - exits with 0. Confirms REQ-3, REQ-7, REQ-21.
* **VC-2**: Run the t80 MOD smoke compile + load:
  `cd tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods && nrnivmodl . && cd .. && uv run python -u -c "import grep; pass"; grep -r "SUFFIX.*t78" mods/ | wc -l`
  - returns 0. And: `grep -r "SUFFIX.*t80" mods/ | wc -l` returns 13. Confirms REQ-4.
* **VC-3**: Run the NMDA-bundle smoke test:
  `uv run python -u -m tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.test_synapse_bundle_nmda`
  - 0 failures, 0 errors. Confirms REQ-2, REQ-5.
* **VC-4**: Run the apply-params smoke test:
  `uv run python -u -m tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.test_apply_params_v3`
  - 0 failures. Confirms REQ-3, REQ-10.
* **VC-5**: Confirm the NSGA-II import migration:
  `grep -n "from pymoo.algorithms.moo.nsga2 import NSGA2" code/nsga2_loop.py` returns >= 1 line;
  `grep -n "qLogNoisyExpected" code/` returns 0 lines. Confirms REQ-6.
* **VC-6**: Confirm the inequality constraint is wired: `grep -n "n_ieq_constr" code/nsga2_loop.py`
  returns >= 1 line in `BedBV3Problem.__init__` and at least one line setting `out["G"] = ...` in
  `_evaluate`. Confirms REQ-8.
* **VC-7**: Run the regression check in isolation:
  `uv run python -u -m tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.regression_check`
  - writes `results/regression_check.json` with `dsi` in [0.37, 0.47] AND `pd_rate_hz` in
    [3.95, 9.34]. Confirms REQ-9, REQ-16.
* **VC-8**: Run the smoke NSGA-II:
  `uv run python -u -m tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.nsga2_loop --smoke`
  - exits 0; the printed Pareto front has 1-4 non-dominated cells. Confirms REQ-6, REQ-13, REQ-17.
* **VC-9**: After the Vast.ai run, confirm the Pareto front exists:
  `test -s results/data/pareto_front.json && jq '.cells | length' results/data/pareto_front.json`
  returns >= 1. Confirms REQ-13.
* **VC-10**: Confirm metrics file structure with REQ coverage:
  `jq '.variants | keys | length' results/metrics.json` returns >= 2;
  `jq '.variants[].direction_selectivity_index' results/metrics.json` is non-null on all variants.
  Confirms REQ-11, REQ-18.
* **VC-11**: Confirm at least 5 PNGs in `results/images/`: `ls results/images/*.png | wc -l` returns
  >= 5 (1 Pareto + 1 HV + 3 deep-dive). Confirms REQ-12.
* **VC-12**: Confirm cost record at or below $2.00: `jq '.total_usd' results/costs.json` returns a
  value <= 2.00. Confirms REQ-19.
* **VC-13**: Run the plan verificator:
  `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0080_bedb_mobo_v3_dendritic_spike_nsga2 -- uv run python -m arf.scripts.verificators.verify_plan t0080_bedb_mobo_v3_dendritic_spike_nsga2`
  returns 0 errors. Confirms plan structural quality.
* **VC-14**: Run the library asset verificator after Step 12:
  `uv run python -u -m arf.scripts.verificators.verify_libraries t0080_bedb_mobo_v3_dendritic_spike_nsga2`
  returns 0 errors. Confirms REQ-1.
* **VC-15**: Run the answer asset verificator after Step 11:
  `uv run python -u -m arf.scripts.verificators.verify_answer_asset t0080_bedb_mobo_v3_dendritic_spike_nsga2`
  returns 0 errors. Confirms REQ-15.
* **VC-16**: Confirm REQ coverage map - every REQ-N appears at least once in
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/results/results_detailed.md` after the
  orchestrator's results step (this is a downstream verifier check; the implementation step does not
  write `results_detailed.md`). Confirms full REQ traceability.

## Task Requirement Checklist Coverage Matrix

For traceability, every REQ-* maps to at least one Step and one Verification Criterion:

| REQ | Steps | Verification Criteria |
| --- | --- | --- |
| REQ-1 | 1, 2, 3, 4, 5, 12 | VC-14 |
| REQ-2 | 4, 5 | VC-3 |
| REQ-3 | 3, 5 | VC-1, VC-4 |
| REQ-4 | 2 | VC-2 |
| REQ-5 | 4 | VC-3 |
| REQ-6 | 6, 8 | VC-5, VC-8 |
| REQ-7 | 3 | VC-1 |
| REQ-8 | 6 | VC-6 |
| REQ-9 | 7 | VC-7 |
| REQ-10 | 5 | VC-4 |
| REQ-11 | 9, 10 | VC-10 |
| REQ-12 | 10 | VC-11 |
| REQ-13 | 8 | VC-8, VC-9 |
| REQ-14 | 8 | VC-12 |
| REQ-15 | 11 | VC-15 |
| REQ-16 | 7 | VC-7 |
| REQ-17 | 6 | VC-8 |
| REQ-18 | 5, 9 | VC-10 |
| REQ-19 | 8, 13 | VC-12 |
| REQ-20 | 3 | VC-1 |
| REQ-21 | 3 | VC-1 |
