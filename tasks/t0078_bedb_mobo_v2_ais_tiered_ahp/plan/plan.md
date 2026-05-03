---
spec_version: "2"
task_id: "t0078_bedb_mobo_v2_ais_tiered_ahp"
date_completed: "2026-05-03"
status: "complete"
---
# Plan: Bed B v2 MOBO with AIS, Tier-Stratified Channels, and Slow Kv-AHP

## Objective

Run a ~47-dimensional multi-objective Bayesian optimisation (BoTorch `qLogNEHVI`) on the de
Rosenroll 2026 Bed B DSGC compartmental model in NEURON, augmented with three architectural
additions absent from the bare 25-d t0076 substrate: (1) a bio-realistic two-subsegment axon initial
segment (AIS) attached at the soma with Van Wart 2007 / Werginz 2020 / Kole 2008 priors; (2)
tier-stratified channel densities for Nav1.6, Kv3, NaP, BK, and SK across five compartment tiers
(soma, proximal-dendrite, mid-dendrite, terminal-dendrite, AIS); (3) a slow Kv-mediated AHP via
SK_E2 with an `extended_tau_ca` parameter that scales the Ca-binding kinetics. The optimiser jointly
maximises direction selectivity index (DSI) and preferred-direction (PD) firing rate.

The pass criterion is **binary**: locate at least one Pareto cell with **DSI at or above 0.4 AND PD
rate at or above 10 Hz** (primary, biologically grounded by Rivlin-Etzion 2012 mean PD rate of 10.4
Hz at DSI 0.78 in mouse ON-OFF DSGCs), with **DSI at or above 0.4 AND PD rate at or above 30 Hz**
retained as a stretch goal, OR rule out the joint operating point architecturally with hypervolume
at least 1.5x the t0076 final HV (8.4129) after at least 600 acquisition iterations and no
qualifying cell observed. Either outcome is a strong project result. Done = a single library asset
(`de_rosenroll_2026_dsgc_ais`), full Pareto-front and hypervolume-trajectory plots, per-axis
sensitivity panels, registered project metrics for every non-dominated Pareto cell, and a clean
Vast.ai cost / teardown record.

## Task Requirement Checklist

The operative task text quoted verbatim from `task.json` and `task_description.md`:

> Bed B v2 MOBO with AIS, tier-stratified channels, and slow Kv-AHP. Bundled MOBO on Bed B with
> bio-realistic AIS, 5-tier channels, SK_E2 slow-AHP; pass = locate DSI >= 0.4 AND PD rate >= 30 Hz,
> or rule out.

> Substrate: AIS-augmented Bed B. Build a new library asset by forking the de Rosenroll 2026 DSGC
> builder from t0024 and attaching a two-subsegment AIS at the soma. AIS length 25-50 um (default
> 30), diameter ~0.8 um, two subsegments (proximal Nav1.1+Nav1.2, distal Nav1.6+Kv1.2), AIS-to-soma
> Na ratio ~7x. AIS channel set: HHst basal Na+K, Nav1.6, Kv3, Kv7. NaP, BK, SK explicitly excluded
> from the AIS section.

> Slow Kv-AHP mechanism: SK_E2 with extended Ca-binding time constant. Add an `extended_tau_ca`
> parameter to the SK_E2 MOD that lengthens the Ca-binding kinetics by a factor configurable per
> simulation (treat the multiplier as a free MOBO parameter). Insertion sites: soma + AIS only.

> Tier-stratified channel densities: 5 channels (Nav1.6, Kv3, NaP, BK, SK) x 5 tiers = 25 density
> parameters. Uniform channels: ~7 from the t0076 12-channel set. Slow Kv-AHP: peak conductance +
> Ca-binding multiplier (2 parameters). Synaptic placement parameters: ~13 from t0076. Total ~47 d.

> Optimiser: qLogNEHVI (migrating off deprecated qNEHVI). Wrap GP inputs in Normalize on `[0,1]^d`.
> Sobol DoE 50-100. Total budget 600-800 acquisition iterations after Sobol. Fresh restart, no
> warm-start from t0076. NEURON re-init fix via fresh subprocess per cell evaluation.

> Stimulus protocol: 8 directions, 1 mm/s bar, 250 um width, 20 seeds per direction. Trial length
> 1400 ms. Trial mode FULL (HH on for Vm / firing rate / DSI).

> Width metrics per cell: direction_selectivity_index, PD firing rate (Hz), tuning_curve_hwhm_deg,
> tuning_curve_reliability, tuning_curve_rmse vs the t0004 cosine target.

> Outputs: library asset `de_rosenroll_2026_dsgc_ais`; Pareto front; hypervolume trajectory plot;
> per-axis sensitivity plots; results/metrics.json with per-cell registered project metrics;
> results/costs.json; results/remote_machines_used.json.

Concrete requirements decomposed into checklist items with stable IDs (covered by step numbers in
parentheses):

* **REQ-1**: Build an AIS-augmented Bed B library asset (fork t0024 cell builder, register in
  `assets/library/de_rosenroll_2026_dsgc_ais/`). Satisfied by Steps 4, 11, 13. Evidence:
  `details.json` + `description.md` + `module_paths` resolvable.
* **REQ-2**: Implement two-subsegment AIS (proximal Nav1.1/Nav1.2 + distal Nav1.6/Kv1.2) attached at
  the soma. Satisfied by Step 4. Evidence: `code/extend_with_ais.py` builds two `h.Section` objects,
  smoke-test confirms `ais_proximal.connect(soma, 1.0, 0.0)` and
  `ais_distal.connect(ais_proximal, 1.0, 0.0)`.
* **REQ-3**: Apply Van Wart / Werginz / Kole AIS priors (length 25-50 um with default 30 um,
  diameter ~0.8 um, AIS-to-soma Na ratio ~7x). Satisfied by Step 4 + Step 6. Evidence: parameter
  bounds in `code/constants.py` set AIS Nav1.6 prior to `[0.0, 1.0]` S/cm^2 spanning the Kole 2008
  range of `[0.25, 0.5]` S/cm^2.
* **REQ-4**: Restrict AIS channel set to HHst basal Na+K, Nav1.6, Kv3, Kv7 only (exclude NaP, BK, SK
  from AIS). Satisfied by Steps 4, 6. Evidence: `apply_params.py` AIS-tier loop writes only the
  permitted SUFFIXes; smoke test inspects `psection()` output of AIS sections.
* **REQ-5**: Vendor SK_E2 with extended Ca-binding (`tau_ca_multiplier` free parameter); insert at
  soma + AIS only. Satisfied by Steps 3, 6. Evidence: `code/mods/skahpt78.mod` adds
  `tau_ca_multiplier`; sanity-check at multiplier=1 reproduces t0074 sk74 trace bit-for-bit.
* **REQ-6**: Stratify Nav1.6, Kv3, NaP, BK, SK across 5 tiers (soma, proximal-dendrite,
  mid-dendrite, terminal-dendrite, AIS) = 25 density parameters. Satisfied by Step 6. Evidence:
  `apply_params.py::apply_parameter_vector` exposes 5 per-channel tier loops.
* **REQ-7**: Keep ~7 uniform-density channels and ~13 synaptic placement parameters as in t0076,
  plus 2 slow-Kv-AHP parameters; total ~47 d parameter space. Satisfied by Steps 6, 7. Evidence:
  `ParamIndex` IntEnum lists 47 entries (or value within +/-2 documented as deliberate); a unit test
  asserts `len(ParameterVector) == N_PARAMS`.
* **REQ-8**: Migrate to `qLogNoisyExpectedHypervolumeImprovement`. Satisfied by Step 7. Evidence:
  `mobo_loop.py` imports from `botorch.acquisition.multi_objective.logei`; no remaining reference to
  `qNoisyExpectedHypervolumeImprovement`.
* **REQ-9**: Wrap GP inputs in `Normalize` on `[0, 1]^d`. Satisfied by Step 7. Evidence:
  `_fit_gp_models` constructs `SingleTaskGP(input_transform=Normalize(d=N_PARAMS), ...)`; GP fit log
  shows no "suboptimal" warning.
* **REQ-10**: Sobol DoE size 50-100, qLogNEHVI iterations 600-800, fresh restart with no t0076
  warm-start. Satisfied by Steps 7, 11. Evidence: `mobo_loop.py` constants `N_SOBOL_INITIAL = 75`
  and `N_ACQ_ITERATIONS = 700` (chosen mid-range); checkpoint loader does not read any t0076 path.
* **REQ-11**: Fix NEURON `Exp2NMDA name already exists` re-init bug in `plot_pareto.py` via
  subprocess-per-deep-dive. Satisfied by Step 9. Evidence: running `plot_pareto.py --n-deep-dives 3`
  emits 3 PNGs (not 1).
* **REQ-12**: Stimulus protocol = 8 directions x 20 seeds, 1 mm/s bar, 250 um width, trial length
  1400 ms (FULL HH-on mode). Satisfied by Step 8. Evidence: `constants.py` sets `TSTOP_MS = 1400.0`,
  `N_DIRECTIONS = 8`, `N_SEEDS_PER_DIRECTION = 20`, `STIMULUS_KIND = StimulusKind.FULL`.
* **REQ-13**: Compute per-cell registered metrics: `direction_selectivity_index`, PD firing rate
  (Hz), `tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse`. Satisfied by Steps
  12, 13. Evidence: `metrics.json` carries one variant per Pareto cell with all five metrics
  populated where computable.
* **REQ-14**: Generate Pareto front + hypervolume trajectory + per-axis sensitivity plots in
  `results/images/`. Satisfied by Step 13. Evidence: PNG files exist.
* **REQ-15**: Confirm hypervolume monotonically increases from Sobol baseline; if final HV does NOT
  exceed t0076 final HV (8.4129), report this as a diagnostic in the negative-result branch.
  Satisfied by Step 12. Evidence: `hv_trajectory.json` writes per-iteration HV values.
* **REQ-16**: Substrate regression sanity-check at the t0076 iter-424 parameter values (DSI 0.42, PD
  rate 4.95 Hz). The augmented substrate must match within +/-0.05 DSI and +/-1 Hz. Satisfied by
  Step 10. Evidence: `code/regression_check.py` writes `results/regression_check.json` with the
  matched values.
* **REQ-17**: Track `is_unstable = False` on every Pareto cell (peak Vm in [-80, +60] mV at every
  trial); discard unstable evaluations from the Pareto. Satisfied by Step 8. Evidence: trial driver
  records `peak_vm_mV` per trial; aggregator filters before Pareto compute.
* **REQ-18**: Vast.ai 72-core CPU instance, fall back to <= $0.20/hr if t0076 instance type is
  unavailable. Satisfied by Steps 11. Evidence: `results/remote_machines_used.json` records instance
  type, hourly rate, and total runtime.
* **REQ-19**: Generate `results/costs.json` with full Vast.ai cost breakdown. Satisfied by Step 14.
  Evidence: file exists with line-items.
* **REQ-20**: Run a fresh subprocess per cell evaluation in a `ProcessPoolExecutor` worker to bypass
  the non-idempotent NEURON loader. Satisfied by Step 8 (already the t0076 default; verify
  `_worker_run_trial` is preserved). Evidence: smoke test runs 3 cell evaluations in a single parent
  Python session without re-init error.
* **REQ-21**: Use `cadecay` SUFFIX from t0024's vendored DLL only (do NOT redeclare in the
  t78-namespace MOD library). Satisfied by Step 5. Evidence: `code/mods/` excludes any
  `cadecay.mod`; load order is t0024 DLL first, then t78 DLL.
* **REQ-22**: Use t78-namespace SUFFIXes for all copied t76 MODs (`*t78` not `*t76`). Satisfied by
  Step 5. Evidence: `grep -r "SUFFIX.*t76" code/mods/` returns no matches.

The original "DSI >= 0.4 AND PD rate >= 30 Hz" pass criterion conflicts with peer-reviewed mouse
DSGC measurements; the resolution adopted in REQ-15 / Objective is documented in the Approach
section "Pass-Criterion Re-calibration" subsection below.

## Approach

### Recommended task type and influence on approach

The task is tagged `build-model` + `experiment-run` in `task.json`. Both apply: the build-model
guidelines drive the library-asset construction (forking t0024, vendoring the SK_E2 MOD with
extended Ca-binding, registering `de_rosenroll_2026_dsgc_ais` as the project's standard
AIS-augmented substrate); the experiment-run guidelines drive the BoTorch search loop, the per-cell
metric computation, the registered-metrics traceability, and the cost / teardown discipline. The
plan reflects both: Step 4-6 (build), Steps 7-12 (experiment), Step 13 (charts and per-axis
sensitivity), Step 14 (cost / teardown record).

### Pass-criterion re-calibration

The original task description specifies pass = "DSI >= 0.4 AND PD rate >= 30 Hz" as a binary
criterion. The internet research stage (Rivlin-Etzion, Wei, Feller 2012 *Neuron*, two-photon-
targeted loose-patch on n=16 mouse DRD4-GFP and TRHR-GFP ON-OFF DSGCs) reports paired same-cell
measurements of DSI **0.78 +/- 0.19** with **mean PD firing rate 10.38 +/- 8.53 Hz over a 3 s
grating window**. Webvision-DSGC consensus places significant motion responses at **5 +/- 2 Hz**
mean. Trenholm 2013 reports **peak** PD spike rates of **198 +/- 14 Hz** but only over sub-second
peri-stimulus windows. No peer-reviewed mouse DSGC paper located reports a 1-s-or-longer mean PD
rate >= 30 Hz.

The plan adopts a **two-tier pass criterion**:

* **Primary (biologically grounded)**: locate at least one Pareto cell with DSI >= 0.4 AND PD rate
  > = 10 Hz. Anchored to Rivlin-Etzion 2012's mean rate of 10.4 Hz at DSI 0.78. A success at this
  > threshold establishes the AIS-augmented Bed B as a biologically faithful substrate for further
  > joint-optimisation work.
* **Stretch (supraphysiological)**: locate at least one Pareto cell with DSI >= 0.4 AND PD rate
  > = 30 Hz. Retained because it is the originally specified target and would establish that the
  > augmented substrate can reach a regime no published mouse DSGC measurement supports —
  > scientifically interesting either way.

Rationale for choosing option (a) recommendation: the >= 30 Hz threshold is unsupported by 1-s mean
PD-rate literature, so a "fail to reach 30 Hz" result alone is not a valid architectural negative
result — it conflates a measurement-window mismatch with a biophysical limit. Reporting both
thresholds preserves the original target while anchoring success to the literature. The stretch goal
is documented in the results regardless of whether it is reached.

The BO **utopia point** is set at (DSI 0.7, PD rate 80 Hz) for cross-task hypervolume comparability
with t0076 (which used the same reference); a secondary HV is computed at (DSI 0.7, PD rate 15 Hz)
in the post-hoc analysis using the bio-grounded reference, so the Pareto-front results can be
interpreted under both conventions.

### Architectural additions

**AIS attachment (REQ-2, REQ-3, REQ-4)**: Fork the t0069 Bed A AIS code
(`tasks/t0069_t0067_ais_localised_channel_sweep/code/extend_with_ais.py`, 75 lines). Split the
single AIS into two `h.Section` objects (`ais_proximal_t78`, `ais_distal_t78`), each ~15 um, with
`ais_proximal.connect(soma, 1.0, 0.0)` and `ais_distal.connect(ais_proximal, 1.0, 0.0)`. Apply
NEURON's `d_lambda = 0.1` segment-count rule via
`nseg = int((sec.L / (0.1 * h.lambda_f(100, sec=sec))) / 2) * 2 + 1`. Insert HHst (basal Na/K), plus
`nav16t78`, `kv3t78`, `kv7t78` SUFFIXes; explicitly exclude `napt78`, `bkt78`, `skt78`, `skahpt78`.
AIS Nav1.6 density bound: `[0.0, 1.0]` S/cm^2, spanning the Kole 2008 / Werginz 2020 biological
prior of `[0.25, 0.5]` S/cm^2. Cells outside the prior range are flagged biologically marginal in
compare-literature (Step 13 produces this annotation as raw data; the orchestrator's later
compare-literature step renders the final document).

**Tier-stratified channel densities (REQ-6, REQ-7)**: Stratify 5 channels (Nav1.6, Kv3, NaP, BK, SK)
across 5 tiers (soma, primary-dendrite, non-terminal-dendrite, terminal-dendrite, AIS) = 25 density
parameters. The 5 tier-mappings reuse the t0024 dendrite labels: `cell.soma`, `cell.primary_dends`
(8 sections), `cell.non_terminal_dends` (165), `cell.terminal_dends` (177), plus the new AIS
sections. Keep 7 uniform-density channels (Kdr, Kv4, NaR, HCN, CaL, CaT, Im) at single density per
channel applied everywhere = 7 parameters. Slow Kv-AHP (SK_E2 extended) at soma + AIS only with peak
conductance + `tau_ca_multiplier` = 2 parameters. Synaptic placement = 13 parameters identical to
t0076 (AMPA / NMDA / GABA spatial decay, density ratios, per-synapse drive scaling). **Total = 25 +
7 + 2 + 13 = 47 d.**

**Slow Kv-AHP via SK_E2 with extended Ca-binding (REQ-5)**: Copy
`tasks/t0074_channel_tuning_ width_bed_a/code/mods/sk74.mod` to `code/mods/skahpt78.mod`. Add
`tau_ca_multiplier` PARAMETER (default 1.0); replace `m' = (minf - m) / tau_m` with
`m' = (minf - m) / (tau_m * tau_ca_multiplier)`; SUFFIX-rename to `skahpt78`. Internet research
(Larsson 2013) shows that mammalian sAHP decay is on the **seconds** timescale, not Ca-binding
kinetics; a `tau_ca_multiplier` of 200x on a 1 ms baseline gives 200 ms which is between fast SK
(~10 ms) and true sAHP (1-3 s). The plan extends the multiplier range to `[1, 200x]` (log-uniform);
if the optimiser pushes the multiplier to its upper bound, the negative-result interpretation is
that a separate KCNQ-like seconds-scale mechanism is the next architectural extension.

### BoTorch optimiser migration (REQ-8, REQ-9, REQ-10)

* `qNoisyExpectedHypervolumeImprovement` -> `qLogNoisyExpectedHypervolumeImprovement` (single-line
  import + class change at `mobo_loop.py:24,350`). Per Ament et al. 2023 NeurIPS, this addresses the
  GP-vanishing-acquisition-value failure mode that affects EI-family functions in high-dimensional
  input spaces (47 d here vs the 25 d of t0076).
* Add `from botorch.models.transforms.input import Normalize` and pass
  `input_transform=Normalize(d=N_PARAMS)` to every `SingleTaskGP` constructor. `Standardize(m=1)`
  outcome transform is already present in t0076. Together these fix the "GP fit suboptimal" warning
  observed in t0076.
* Sobol DoE size: 75 (mid-range of 50-100). qLogNEHVI iterations: 700 (mid-range of 600-800). Fresh
  restart - no warm-start from t0076 per researcher decision.

### NEURON re-init bug fix (REQ-11, REQ-20)

The trial driver in t0076 already uses `ProcessPoolExecutor` worker-per-trial, so the bug never
manifests during the BO loop. The bug surfaces in `plot_pareto.py::_save_deep_dive` (line 264 in
t0076 source) where `build_dsgc_cell()` is called multiple times in the parent process. The fix:
wrap each pick's `_save_deep_dive` call in a single-worker `ProcessPoolExecutor` so each deep-dive
runs in its own subprocess. Verified by running with `--n-deep-dives 3` and confirming all 3 PNGs
are emitted.

### Implementation traps explicitly addressed

These are gotchas the implementation step must avoid; each is referenced by a specific REQ:

1. **`cadecay.mod` SUFFIX collision (REQ-21)**: t0024's vendored `nrnmech.dll` already defines
   `cadecay`. Do NOT include `cadecay.mod` in `code/mods/`. Load order: t0024 DLL first (HHst,
   cadecay, Exp2NMDA), t78 DLL second (12 t78-namespace channels + skahpt78).
2. **`Exp2NMDA name already exists` in deep-dive (REQ-11)**: Already addressed - subprocess-per-
   deep-dive in `plot_pareto.py`.
3. **`TSTOP_MS = 1000.0` from t0076 must change to 1400.0 (REQ-12)**: per the project's standard
   mode trio EPSP_PASSIVE / IPSP_PASSIVE / FULL.
4. **t78-namespace SUFFIX rename for all copied MODs (REQ-22)**: 12 t76 MODs `sed s/t76/t78/g` when
   copied. Covered explicitly in Step 5.
5. **NEURON HOC chdir trap**: t0024's `build_dsgc_cell()` chdirs to its sources directory then
   restores; downstream code must use absolute paths for all I/O after this call. Already idempotent
   in t0024 but worth a sanity-check assertion.

### Alternatives considered

1. **Single-objective rescaled scalarisation (e.g., DSI - lambda * deviation_from_15Hz)** instead of
   MOBO. Rejected because (a) it requires choosing a lambda, which is itself a research question,
   and (b) the t0076 MOBO Pareto front is the comparison anchor; scalarisation discards that
   information.
2. **Warm-start from t0076 12-cell Pareto front instead of fresh Sobol restart**. Rejected per
   explicit researcher decision (the fresh restart is non-negotiable). Rationale recorded by the
   researcher: a 47-d search initialised from a 25-d Pareto would inherit the uniform-density bias
   the new substrate is trying to escape.
3. **Add a separate KCNQ-like slow K+ MOD (3-channel slow-AHP architecture) instead of SK_E2 with
   extended `tau_ca_multiplier`**. Rejected because it expands the parameter space by another 1-3 d
   and is not what the researcher chose; the smaller change reuses the t0074 SK code path. If the
   optimiser pushes `tau_ca_multiplier` to its upper bound the negative-result branch recommends
   KCNQ as the next follow-up.
4. **Drop NaP and BK from tier stratification, keeping only Nav1.6, Kv3, SK stratified (~35 d
   total)**. Held in reserve as a Risks fallback if the GP fit is unstable on 47 d. Not adopted
   pre-emptively because the researcher explicitly authorised the 40-50 d band.
5. **Run on local CPU instead of Vast.ai**. Rejected because t0076 measured 6.47 h on a 72-core
   instance for 25 d / 430 cells; the 47-d / ~700 cell run would take 30+ h on local 8-core
   hardware, exceeding the time budget.

### Library asset name

The plan adopts `de_rosenroll_2026_dsgc_ais` (suggested in task description) as the library ID. This
is explicit, consistent with the t0024 ancestor name, and matches the slug pattern for existing
libraries. The library exposes `build_dsgc_cell_with_ais()` as the primary entry point and
re-exports the t0024 `DSGCCell` dataclass so downstream tasks can drop-in replace t0024 calls.

## Cost Estimation

Itemised dollar amounts, anchored to the t0076 measured cost ($1.0583 over 6.4697 h on Vast.ai
72-core CPU at $0.16357/hr, for 430 cells x 8 directions x 20 seeds = 68,800 NEURON simulations):

* **BO loop wall-clock**: 650-900 cells (50-100 Sobol + 600-800 acquisitions) x 8 dirs x 20 seeds =
  104,000 - 144,000 NEURON simulations. Per-trial wall-clock ~3.4 s including AIS overhead (~10%
  slower than t0076's ~3.1 s). Total per-core trial time ~4900-6800 s, parallelised across 72 cores
  ~= **9.7 - 13.6 h**.
* **Vast.ai instance cost** at $0.16357/hr for 9.7-13.6 h = **$1.59 - $2.22**.
* **Provisioning + teardown overhead**: 30 min provisioning + 30 min teardown = 1 h at $0.16/hr =
  **$0.16**.
* **20% contingency** for BoTorch acquisition computation time on the larger 47-d input space and
  any retry / restart overhead = **$0.35 - $0.48**.
* **Subtotal**: $2.10 - $2.86.
* **Round up to ceiling**: **$3.50** (well within the $8.94 remaining project budget and the
  researcher-authorised $2.50-$4.00 range from the t0077 brainstorm session 13).

API call costs: $0 (no LLM inference; all compute is local NEURON simulation on the Vast.ai
instance).

Total project budget remaining after this task: $8.94 - $3.50 = **$5.44**.

The cost-gate threshold (per-task default limit $5.00 from `project/budget.json`) is NOT reached;
the cost gate is in advisory mode for this task.

## Step by Step

The implementation work is organised into three milestones.

### Milestone A: Substrate construction (Steps 1-6)

1. **Set up code directory and copy t0076 harness into `code/`.** Copy these files verbatim from
   `tasks/t0076_bedb_dsi_firing_rate_mobo/code/` to `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/code/`:
   `bootstrap.py` (~117 LOC), `trial_driver.py` (~400 LOC), `mobo_loop.py` (~484 LOC),
   `apply_params.py` (~89 LOC -> extend in Step 6), `parametric_placer.py` (~105 LOC, no change),
   `trial_helpers.py` (~283 LOC), `recorder.py` (~122 LOC), `plot_pareto.py` (~397 LOC -> extend in
   Step 9), `render_pdf.py` (~63 LOC), `run_remote.sh` (~43 LOC). Update internal global names from
   `_T76_*` to `_T78_*` in `bootstrap.py` and `apply_params.py`. **Expected output**: `ls code/`
   lists all 10 Python files plus `run_remote.sh`. Satisfies REQ-1 (substrate plumbing).

2. **Update `code/constants.py` with the t0078 parameter dimensionality and stimulus protocol.**
   Replace `TSTOP_MS = 1000.0` with `TSTOP_MS = 1400.0` (REQ-12). Replace t0076's 25-entry
   `ParamIndex` IntEnum with a 47-entry IntEnum: 25 tier-stratified densities (5 channels x 5 tiers,
   with names like `NAV16_SOMA_GBAR`, `NAV16_PRIMARY_GBAR`, ..., `SK_AIS_GBAR`); 7 uniform-density
   channels (`KDR_GBAR`, `KV4_GBAR`, `NAR_GBAR`, `HCN_GBAR`, `CAL_GBAR`, `CAT_GBAR`, `IM_GBAR`); 2
   slow-AHP (`SKAHP_GBAR_SOMA_AIS`, `SKAHP_TAU_CA_MULTIPLIER`); 13 synaptic placement parameters
   identical to t0076 (`AMPA_RHO_0`, `AMPA_LAMBDA_DECAY`, ...). Add `LOG_PARAM_INDICES` set for
   log-uniform parameters (all gbar densities + the `tau_ca_multiplier`). Define the 47-row
   natural-units bounds table `PARAM_BOUNDS_NATURAL` with each row `(low, high)` in physical units;
   the AIS Nav1.6 row uses `[0.0, 1.0]` S/cm^2. **Expected output**:
   `python -c "from code.constants import N_PARAMS; print(N_PARAMS)"` prints 47. Satisfies REQ-7,
   REQ-12.

3. **Vendor `code/mods/skahpt78.mod` (slow-AHP SK_E2 with extended Ca-binding).** Copy
   `tasks/t0074_channel_tuning_width_bed_a/code/mods/sk74.mod` to `code/mods/skahpt78.mod`. Edit:
   change `SUFFIX sk74` to `SUFFIX skahpt78`, add `tau_ca_multiplier = 1.0` to the PARAMETER block
   (default makes it backward-compatible with sk74), replace `m' = (minf - m) / tau_m` in the
   DERIVATIVE block with `m' = (minf - m) / (tau_m * tau_ca_multiplier)`. Update the citation
   header. Sanity-check with a single-segment NEURON simulation: insert `skahpt78` with
   `tau_ca_multiplier = 1.0` on a soma with the t0074 step-Ca protocol; confirm the resulting m
   trajectory matches the t0074 sk74 trace bit-for-bit (within numerical noise <= 1e-9). **Expected
   output**: `code/test_skahpt78_smoke.py` passes 0 failures. Satisfies REQ-5.

4. **Build `code/extend_with_ais.py` for two-subsegment AIS attachment.** Copy
   `tasks/t0069_t0067_ais_localised_channel_sweep/code/extend_with_ais.py` (75 LOC) to
   `code/extend_with_ais.py`. Extend it: split the single AIS into two `h.Section` objects
   (`ais_proximal_t78`, `ais_distal_t78`), each ~15 um at default 30 um total length, with
   `ais_proximal.connect(soma, 1.0, 0.0)` and `ais_distal.connect(ais_proximal, 1.0, 0.0)`. Compute
   `nseg` per subsegment using `nseg = int((sec.L / (0.1 * h.lambda_f(100, sec=sec))) / 2) * 2 + 1`.
   Insert HHst (basal Na+K) on both subsegments; insert `nav16t78` (Nav1.6), `kv3t78`, `kv7t78` on
   the distal subsegment only; insert HHst-derived Nav1.1/Nav1.2-like conductance on the proximal
   subsegment as a single `nav16t78` instance with proximal-specific density. Explicitly exclude
   `napt78`, `bkt78`, `skt78`, `skahpt78` from both AIS sections. Wire AIS length and diameter as
   parameters consumable from `apply_parameter_vector`. Smoke-test with
   `code/test_ais_attach_smoke.py`: build a cell, attach AIS, run `psection()` on `ais_proximal` and
   `ais_distal`, confirm the printed mechanism list matches the expected inserts. **Expected
   output**: smoke test passes. Satisfies REQ-2, REQ-3, REQ-4.

5. **Copy and rename t0076 MOD files into `code/mods/` with t78 namespace.** Copy 12 MODs from
   `tasks/t0076_bedb_dsi_firing_rate_mobo/code/mods/`: `bkt76.mod`, `calt76.mod`, `catt76.mod`,
   `iht76.mod`, `kdrt76.mod`, `kv3t76.mod`, `kv4t76.mod`, `kv7t76.mod`, `napt76.mod`, `nart76.mod`,
   `nav16t76.mod`, `skt76.mod`. For each file, run `sed -i 's/t76/t78/g' <file>` to rename SUFFIXes
   and references; rename the file from `*t76.mod` to `*t78.mod`. **Do NOT copy `cadecay.mod`** - it
   lives in t0024's vendored DLL and copying it causes a SUFFIX collision (REQ-21). Add
   `code/mods/skahpt78.mod` from Step 3. Compile on Linux: `nrnivmodl code/mods/`. Verify the
   resulting `x86_64/.libs/libnrnmech.so` exposes 13 SUFFIXes (12 t78 channels + skahpt78).
   **Expected output**: a Linux-compiled `.so` plus a `code/mods/test_t78_dll_smoke.py` that loads
   it and `assert h.t78_loaded()` style sanity. (The actual sanity is `nrn_load_dll` returning
   success and `h.psection()` listing the SUFFIXes.) Satisfies REQ-22, REQ-21.

6. **Extend `code/apply_params.py` for tier-stratified writes.** Replace the single t0076 write-loop
   (lines 78-88) with five tier-specific loops: (a) soma-tier densities to `cell.soma`, (b)
   proximal-dendrite densities to `cell.primary_dends` (8 sections), (c) mid-dendrite densities to
   `cell.non_terminal_dends` (165 sections), (d) terminal-dendrite densities to
   `cell.terminal_dends` (177 sections), (e) AIS densities to `cell.ais_proximal` and
   `cell.ais_distal`. The 5 stratified channels (Nav1.6, Kv3, NaP, BK, SK) each have 5 tier
   densities indexed in the 47-d ParameterVector; the 7 uniform channels have a single density each
   applied to all of soma + dendrites (not AIS, since AIS channel set is restricted). Add SK_E2
   `tau_ca_multiplier` and `skahpt78_gbar` writes to soma + AIS only (REQ-5). `cell.ais_proximal`
   and `cell.ais_distal` come from the AIS attacher in Step 4. Update the t78 DLL load in
   `ensure_t78_dll_loaded`. Smoke-test by applying a known parameter vector and inspecting
   `psection()` on representative sections from each tier. **Expected output**:
   `code/test_apply_params_tiered.py` passes 0 failures. Satisfies REQ-6.

### Milestone B: Optimiser migration and validation (Steps 7-10)

7. **Migrate `code/mobo_loop.py` to qLogNEHVI + Normalize.** Edit `mobo_loop.py` at line 24: replace
   `from botorch.acquisition.multi_objective.monte_carlo import qNoisyExpectedHyper- volumeImprovement`
   with
   `from botorch.acquisition.multi_objective.logei import qLogNoisyExpectedHypervolumeImprovement`.
   Edit line 350: replace `acq = qNoisyExpectedHypervolumeImprovement(...)` with
   `acq = qLogNoisyExpectedHypervolumeImprovement(...)`. Edit `_fit_gp_models` (lines 240-257): add
   `from botorch.models.transforms.input import Normalize`, then change every
   `SingleTaskGP(train_X=train_x, train_Y=y_i, outcome_transform=Standardize(m=1))` to
   `SingleTaskGP(train_X=train_x, train_Y=y_i, outcome_transform=Standardize(m=1), input_transform=Normalize(d=N_PARAMS))`.
   Update constants: `N_SOBOL_INITIAL = 75`, `N_ACQ_ITERATIONS = 700`, `WARM_START = False`. Verify
   by importing the loop module and running 1 Sobol point + 1 acquisition step on a small mock
   objective (a 47-d unit-test double): the BoTorch logger should emit no "fit suboptimal" warning.
   **Expected output**: `code/test_mobo_migration_smoke.py` passes; one acquisition step completes
   in <60 s on local CPU. Satisfies REQ-8, REQ-9, REQ-10.

8. **Update `code/trial_driver.py` for the AIS-augmented cell builder.** Edit `_worker_get_cell()`
   to call `build_dsgc_cell()` (from t0024 library import) and then `extend_with_ais(cell, ...)`
   (from `code.extend_with_ais`). The returned object is a new `DSGCCellWithAIS` dataclass extending
   `DSGCCell` with `ais_proximal` and `ais_distal` fields. Update the `_worker_run_trial` import to
   use the new cell type. Confirm `TSTOP_MS` is read from the updated `code/constants.py` (REQ-12).
   Confirm `is_unstable` is still tracked via `peak_vm_mV` recording on every trial (REQ-17).
   **Validation gate (small)**: before any full BO loop, run 5 random Sobol cells x 8 directions x 5
   seeds = 200 NEURON simulations locally on Windows (~10 min). Confirm `is_unstable = False` on all
   200 trials. If any cell evaluates unstable, halt and inspect peak Vm trace; do NOT proceed to
   Vast.ai. **Trivial baseline**: t0076's iter-0 Sobol DSI is 0.06 (mean of 30 Sobol points);
   t0078's mean Sobol DSI should land in [0.05, 0.30]. If the mean Sobol DSI is below 0.05, the
   substrate has a regression. **Expected output**: 200 trials pass `is_unstable = False`; mean
   Sobol DSI in the expected range. Satisfies REQ-17, REQ-20, REQ-12.

9. **Fix `code/plot_pareto.py` deep-dive to use subprocess-per-deep-dive.** Edit the
   `for idx, pick in enumerate(picks)` loop (around line 376 in t0076 source). Wrap the
   `_save_deep_dive` call:
   ```python
   from concurrent.futures import ProcessPoolExecutor
   for idx, pick in enumerate(picks):
       with ProcessPoolExecutor(max_workers=1) as ex:
           ex.submit(_save_deep_dive, pick=pick, idx=idx).result()
   ```
   Smoke-test on a hand-built fake `mobo_loop_state.json` with 3 deep-dive picks and confirm 3 PNGs
   are produced (without the fix, only the first PNG is produced). **Expected output**:
   `ls results/images/deep_dive_*.png | wc -l` returns 3. Satisfies REQ-11.

10. **[CRITICAL] Substrate regression check at t0076 iter-424 parameters.** Create
    `code/regression_check.py` that loads
    `tasks/t0076_bedb_dsi_firing_rate_mobo/results/ pareto_front.json`, finds the cell at iter 424
    (DSI 0.42, PD rate 4.95 Hz), maps its 25-d parameter vector into the t0078 47-d space (the 25
    t0076 parameters become the soma-tier values for the 5 stratified channels + the 7 uniform
    channels + the 13 synaptic placement parameters; the new 22 parameters - 4 dendrite tiers x 5
    channels = 20, plus 2 slow-AHP - are set to "default" = `tau_ca_multiplier = 1.0`,
    `skahpt78_gbar = 0.0`, all dendrite-tier densities matching the corresponding soma-tier value to
    recover uniform-density behaviour, AIS-tier densities at the Kole 2008 prior 0.3 S/cm^2 for
    Nav1.6, 0.0 for the others). Evaluate this cell with the full 8 dir x 20 seed protocol; assert
    DSI in [0.37, 0.47] AND PD rate in [3.95, 5.95] Hz. **Failure mode**: if the assertion fails by
    more than 0.1 in DSI or 5 Hz in PD rate, STOP - the AIS attachment or apply_params extension has
    introduced a bug. Inspect peak Vm traces and `psection()` outputs for AIS sections before
    proceeding. Save `results/regression_check.json` with the matched values. **Expected output**:
    `regression_check.json` exists with `dsi` in [0.37, 0.47] and `pd_rate_hz` in [3.95, 5.95].
    Satisfies REQ-16.

### Milestone C: BO loop, Pareto extraction, and metrics (Steps 11-14)

11. **[CRITICAL] Provision Vast.ai instance and run the 47-d BO loop.** Use the orchestrator's
    `setup-machines` step to provision a 72-core Xeon E5-2686 v4 or equivalent at <= $0.20/hr;
    fallback condition documented in Risks. SSH into the instance, clone the worktree branch,
    `nrnivmodl code/mods/` to compile the t78 DLL on Linux, then launch
    `bash code/run_remote.sh --task-id t0078_bedb_mobo_v2_ais_tiered_ahp --n-sobol 75 --n-acq 700`.
    The BO loop checkpoint-writes `mobo_loop_state.json` after every cell. **Validation gate
    (Sobol-phase)**: after the 75 Sobol cells complete (~70 min), check `results/sobol_summary.json`
    \- mean DSI should be in [0.05, 0.30] (matching the t0078 Step 8 baseline) and at least 90% of
    cells should have `is_unstable = False`. If unstable cells exceed 10%, halt and inspect
    parameter ranges. **Validation gate (acquisition-phase midway)**: at iteration 350, check that
    hypervolume has increased by >= 25% from the Sobol baseline; if not, the GP fit is failing -
    halt and check GP warnings in the logs. Total wall-clock 9-12 h. **Expected output**:
    `results/mobo_loop_state.json` with 775 cells evaluated; `results/pareto_front.json` with the
    non-dominated front; `results/ hv_trajectory.json` per-iteration HV. Satisfies REQ-10, REQ-15,
    REQ-18.

12. **Compute per-cell registered metrics.** Create `code/compute_metrics.py` that walks the
    Pareto-front cells, builds per-cell 8-direction tuning curves from the trial driver outputs, and
    computes:
    * `direction_selectivity_index` (registered metric - already in t0076 trial-driver output; copy
      verbatim into `metrics.json`).
    * PD firing rate (Hz) - already in t0076 trial-driver output.
    * `tuning_curve_hwhm_deg` (registered metric) - via
      `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.metrics.compute_hwhm_deg`.
    * `tuning_curve_reliability` (registered metric) - via
      `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.metrics.compute_reliability`.
    * `tuning_curve_rmse` (registered metric) - via
      `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.metrics.compute_tuning_curve_rmse`
      against the t0004 cosine target.

    Discard unstable cells (peak Vm outside [-80, +60] mV at any trial - REQ-17). Write
    `results/metrics.json` using the **explicit multi-variant** format (per
    `arf/specifications/metrics_specification.md`) with one variant per Pareto cell, named
    `pareto_cell_iter_NNN`, plus a `pareto_best_joint` variant pointing to the cell with the
    smallest distance to the bio-grounded target (DSI 0.4, PD rate 10 Hz). Each variant carries all
    five metrics where computable; `None` is used where not computable (never `0.0` per Python style
    guide). **Expected output**: `results/metrics.json` exists with the variants structure and
    registered-metric keys for every Pareto cell. Satisfies REQ-13, REQ-15, REQ-17.

13. **Generate Pareto-front, hypervolume-trajectory, and per-axis sensitivity plots.** Run
    `python -u -m tasks.t0078_bedb_mobo_v2_ais_tiered_ahp.code.plot_pareto --task-id t0078_bedb_mobo_v2_ais_tiered_ahp --n-deep-dives 5`,
    which produces:
    * `results/images/pareto_front.png` - 2D scatter (DSI vs PD rate) with t0076 Pareto front
      overlaid as a comparison; bio-grounded threshold (DSI 0.4 / PD rate 10 Hz) drawn as a dashed
      line; supraphysiological threshold (DSI 0.4 / PD rate 30 Hz) drawn as a dotted line.
    * `results/images/hv_trajectory.png` - per-iteration hypervolume (utopia point as documented in
      Approach: (0.7, 80 Hz) for cross-task comparison with t0076 final HV 8.4129).
    * `results/images/deep_dive_NNN.png` (5 files) - per-Pareto-cell tuning curves and trace panels
      for the 5 picks (max DSI, max rate, knee, max DSI s.t. rate >= 10 Hz, max rate s.t. DSI >=
      0.4).
    * `results/images/sensitivity_<channel>.png` - per-stratified-channel marginal effect of density
      on DSI and PD rate at the Pareto-best joint operating point. 5 channels x 1 plot = 5 PNGs.

    Use
    `tasks.t0011_response_visualization_library.code.tuning_curve_viz.cartesian. plot_cartesian_tuning_curve`
    and `plot_polar_tuning_curve` for the deep-dive panels. **Expected output**: at least 12 PNGs in
    `results/images/`. Satisfies REQ-14, REQ-1, REQ-3 (annotation).

14. **Emit raw cost / machine telemetry into the implementation step log.** The orchestrator's
    `setup-machines` and `teardown` steps own the machine lifecycle and produce
    `logs/steps/*setup-machines*/machine_log.json` and the final summary files in `results/`. The
    implementation step's responsibility is to record per-iteration NEURON-trial wall-clock plus
    BoTorch-acquisition wall-clock into the structured implementation step log
    (`logs/steps/*implementation*/step_log.json`), and to record any non-machine paid API spend
    (none expected for this task). **Expected output**: `logs/steps/*implementation*/step_log.json`
    exists with a `total_neuron_wallclock_s` field and a `total_acquisition_wallclock_s` field;
    orchestrator-owned machine telemetry is captured on instance teardown. Satisfies REQ-18 and
    REQ-19 instrumentation requirements. Final summary files in `results/` are written by the
    orchestrator's downstream results step.

The Step by Step ends here at chart generation and metric writing. Results synthesis, suggestions
generation, compare-literature, and reporting are orchestrator-managed steps in execute-task and are
NOT part of the implementation plan.

## Remote Machines

One Vast.ai 72-core CPU instance (Xeon E5-2686 v4 or equivalent at ~$0.16/hr). VRAM not required;
this is a CPU-only NEURON simulation workload. Estimated runtime 9-12 h for the BO loop plus 30 min
provisioning + 30 min teardown + ~30 min for deep-dive plotting. Fallback if the t0076 instance type
is unavailable: any 72-core CPU instance at <= $0.20/hr satisfies the per-trial wall-clock
requirement; see Risks for the fallback procedure. The `code/run_remote.sh` launcher (copied from
t0076) handles git checkout + nrnivmodl + nohup background launch + log streaming.

## Assets Needed

* **t0024 library `de_rosenroll_2026_dsgc`** - Bed B substrate. Imported via
  `from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import build_dsgc_cell`.
* **t0024 vendored sources** at
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/ de_rosenroll_2026_dsgc/sources/` -
  `RGCmodelGD.hoc`, `HHst_noiseless.mod`, `cadecay.mod`, `Exp2NMDA.mod`, `nrnmech.dll`. Used at
  runtime by `build_dsgc_cell()`.
* **t0069 AIS attachment code** at
  `tasks/t0069_t0067_ais_localised_channel_sweep/code/ extend_with_ais.py` - copied and extended in
  Step 4.
* **t0074 SK_E2 MOD** at `tasks/t0074_channel_tuning_width_bed_a/code/mods/sk74.mod` - copied and
  extended in Step 3.
* **t0076 BoTorch harness** - 11 files copied verbatim then surgically edited in Steps 1, 7, 9.
* **t0011 visualization library `tuning_curve_viz`** - imported in Step 13.
* **t0012 metrics library `tuning_curve_loss`** - imported in Step 12.
* **t0076 Pareto front** at `tasks/t0076_bedb_dsi_firing_rate_mobo/results/pareto_front.json` - read
  in Step 10 (regression check) and Step 13 (overlay).
* **t0004 cosine target tuning curve** - read in Step 12 for `tuning_curve_rmse`.

No external assets (datasets, papers) need to be downloaded by the implementation step; the research
stages have already collected the cited papers.

## Expected Assets

`task.json` `expected_assets` declares `{"library": 1}`. The implementation produces:

* **Library asset** `de_rosenroll_2026_dsgc_ais` at `assets/library/de_rosenroll_2026_dsgc_ais/`:
  * `details.json` with `spec_version: "2"`, `library_id: "de_rosenroll_2026_dsgc_ais"`,
    `name: "De Rosenroll 2026 DSGC with AIS"`, `version: "0.1.0"`, `module_paths` listing
    `code/build_cell_ais.py`, `code/extend_with_ais.py`, `code/apply_params.py`,
    `code/constants.py`, `code/mods/skahpt78.mod`, plus the 12 t78 MODs,
    `description_path: "description.md"`. Entry points: `build_dsgc_cell_with_ais` (function),
    `apply_parameter_vector` (function), `DSGCCellWithAIS` (class).
  * `description.md` with the mandatory sections (Metadata, Overview, API Reference, Usage Examples,
    Dependencies, Testing, Main Ideas, Summary).

The Pareto-front, hypervolume-trajectory, deep-dive, and sensitivity PNGs in `results/images/`, plus
`results/metrics.json` and `results/costs.json` and `results/remote_machines_used.json`, are not
asset-typed but are required outputs per the task description Outputs section.

## Time Estimation

| Phase | Wall-clock |
| --- | --- |
| Research (already complete) | - |
| Planning (this step) | ~1.5 h |
| Steps 1-6: substrate construction (local Windows) | ~3 h |
| Step 7: BoTorch migration | ~1 h |
| Step 8: trial driver update + 200-trial validation | ~30 min |
| Step 9: plot_pareto deep-dive fix + smoke test | ~30 min |
| Step 10: regression check (local 1 cell x 160 trials) | ~30 min |
| Step 11: Vast.ai provisioning + BO loop | ~10-13 h |
| Step 12: metrics computation (local) | ~30 min |
| Step 13: chart generation (local) | ~30 min |
| Step 14: cost / machine record finalisation | ~10 min |
| **Total (planning + implementation)** | **~17-20 h wall-clock** |

Most of the 17-20 h is the 10-13 h Vast.ai BO loop, which runs unattended. Active developer time is
approximately 7 h spread across Steps 1-10, 12, 13.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| AIS section adds significant per-trial wall-clock overhead | Medium | Cost overrun ~$1 | Apply NEURON `lambda_f`-based segment rule (`d_lambda = 0.1` at 100 Hz); keep AIS to 5-10 segments. If wall-clock grows >25%, reduce DoE from 75 to 50 and target 600 acquisitions. |
| GP fit unstable on 47 d | Medium | Search degrades | qLogNEHVI is more numerically stable than qNEHVI on high-D. If GP fit warnings persist after migration, drop tier-stratification on NaP and BK (saves 10 d, restores 37 d), keeping Nav1.6, Kv3, SK stratified. |
| No DSI >= 0.4 AND PD rate >= 10 Hz Pareto cell found | Medium | Negative result | Clean architectural negative; report compare-literature with the diagnostic on which ingredient (AIS / tier-stratification / slow Kv-AHP) was insufficient; propose dendritic-spike machinery as the next architectural extension. |
| `Exp2NMDA name already exists` re-init bug returns | Low | Deep-dive PNGs missing | Subprocess-per-deep-dive in Step 9. Verified by running `--n-deep-dives 3` and confirming all 3 PNGs are emitted. If the bug recurs, fall back to `subprocess.run(["python", "-m", ..., "--idx", str(i)])` from the parent process. |
| `cadecay.mod` SUFFIX collision (REQ-21 violated) | Low | Cell-build failure | `code/mods/` MUST exclude `cadecay.mod`. Pre-compile sanity check: `nrnivmodl code/mods/` then `nrn_load_dll` should not error. The bootstrap test in Step 5 validates this. |
| Vast.ai instance availability or pricing shifts | Low | Cost overrun or delay | Fall back to a different 72-core CPU instance at <= $0.20/hr. If no comparable instance is available, run on local 8-core CPU at reduced iteration count (300 acquisitions, 75 Sobol = 375 total) and report the truncated result with the truncation documented in `results_detailed.md`. |
| Vast.ai instance crashes mid-run | Low | 0-13 h compute lost | The BO loop checkpoint-writes `mobo_loop_state.json` after every cell. The launcher can resume from the checkpoint. Manual fallback: `setup-machines` can re-provision and re-launch. |
| Substrate regression check fails (REQ-16) | Low | Block on Step 10 | If DSI delta > 0.1 or PD rate delta > 5 Hz, halt and inspect AIS attachment + apply_params writes. The most likely causes: (a) AIS section accidentally inserted into `cell.all_dends`, breaking parametric_placer assumptions, (b) tier-mapping sends a soma density to dendrites or vice versa. |
| `TSTOP_MS = 1000.0` not updated to 1400.0 | Medium | DSI / PD rate values not comparable | Step 2 explicitly changes `TSTOP_MS`. Verification command in Step 8 includes a check on the recorded trial length. |
| t78-namespace SUFFIX rename incomplete (REQ-22) | Low | Channel insertion fails silently | Step 5 explicitly runs `sed s/t76/t78/g`; the smoke test then attempts to insert each t78 SUFFIX and fails-fast if any is missing. |
| BoTorch checkpoint format incompatibility | Low | Cannot resume from checkpoint | The qLogNEHVI migration preserves the existing checkpoint format (state is a dict of arrays + GP hyperparameters); but legacy checkpoints written by qNEHVI may not deserialise. Workaround: this is a fresh restart, so no legacy checkpoint is read - pre-empted by REQ-10. |
| AIS Nav1.6 priors do not match Kole 2008 in any Pareto cell | Medium | Biological plausibility flag | Report the optimiser's preferred density range; flag cells where AIS Nav1.6 falls outside [0.25, 0.5] S/cm^2 as biologically marginal in compare-literature. Do NOT constrain the search to the prior - one of the questions is whether biologically plausible densities reach the joint operating point. |

## Verification Criteria

Concrete, testable checks. Each criterion lists the exact command to run and the expected output:

* **VC-1**: Run
  `cd tasks/t0078_bedb_mobo_v2_ais_tiered_ahp && uv run python -u -c "from code.constants import N_PARAMS; assert N_PARAMS == 47, N_PARAMS"`
  \- exits with 0. Confirms REQ-7.
* **VC-2**: Run the t78 MOD smoke test:
  `cd tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/code/mods && nrnivmodl . && cd .. && uv run python -u -c "from neuron import h; from bootstrap import load_neuron_t78; load_neuron_t78(); seg = h.Section(name='test'); seg.insert('skahpt78'); print(seg.psection())"`
  \- prints a `psection()` string containing `skahpt78`. Confirms REQ-5, REQ-22.
* **VC-3**: Run
  `uv run python -u -m tasks.t0078_bedb_mobo_v2_ais_tiered_ahp.code.test_ais_attach_smoke` - 0
  failures, 0 errors. Confirms REQ-2, REQ-3, REQ-4.
* **VC-4**: Run the regression check in isolation:
  `uv run python -u -m tasks.t0078_bedb_mobo_v2_ais_tiered_ahp.code.regression_check` - writes
  `results/regression_check.json` with `dsi` in [0.37, 0.47] AND `pd_rate_hz` in [3.95, 5.95].
  Confirms REQ-16.
* **VC-5**: Inspect `code/mobo_loop.py` for the qLogNEHVI migration:
  `grep -n "qLogNoisyExpectedHypervolumeImprovement" code/mobo_loop.py` returns >=2 lines (import +
  class call); `grep -n "qNoisyExpectedHypervolumeImprovement" code/mobo_loop.py` returns 0 lines.
  Confirms REQ-8.
* **VC-6**: Confirm the input Normalize transform: `grep -n "Normalize(d=" code/mobo_loop.py`
  returns >= 1 line within `_fit_gp_models`. Confirms REQ-9.
* **VC-7**: After the Vast.ai run, confirm Pareto front exists:
  `test -s results/pareto_front.json && jq '.cells | length' results/pareto_front.json` returns >=
  1\. Confirms REQ-15.
* **VC-8**: Confirm metrics file structure with REQ coverage:
  `jq '.variants | keys | length' results/metrics.json` returns >= 1;
  `jq '.variants[].direction_selectivity_index' results/metrics.json` is non-null on all variants.
  Confirms REQ-13.
* **VC-9**: Confirm hypervolume trajectory monotonicity (or report the negative-result diagnostic):
  `uv run python -u -c "import json; hv = json.loads(open('results/hv_trajectory.json').read())['values']; assert all(hv[i+1] >= hv[i] for i in range(len(hv)-1)), 'HV not monotone'"`
  \- either succeeds, OR the assertion failure is documented in `results_detailed.md` as the
  negative-result diagnostic. Confirms REQ-15.
* **VC-10**: Confirm at least 12 PNGs in `results/images/`: `ls results/images/*.png | wc -l`
  returns >= 12. Confirms REQ-14.
* **VC-11**: Run the plan verificator:
  `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0078_bedb_mobo_v2_ais_tiered_ahp -- uv run python -m arf.scripts.verificators.verify_plan t0078_bedb_mobo_v2_ais_tiered_ahp`
  returns 0 errors. Confirms plan structural quality.
* **VC-12**: Run the library asset verificator after Step 13:
  `uv run python -u -m arf.scripts.verificators.verify_libraries t0078_bedb_mobo_v2_ais_tiered_ahp`
  returns 0 errors. Confirms REQ-1 + asset structural quality.
* **VC-13**: Confirm cost record matches actual instance hours: `jq '.total_usd' results/costs.json`
  returns a value in [$1.50, $4.00]; `jq '.[0].duration_hours' results/remote_machines_used.json`
  returns a value in [9, 14]. Confirms REQ-18, REQ-19.
* **VC-14**: Confirm REQ coverage map - every REQ-N appears at least once in
  `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/results/results_detailed.md` after the orchestrator's
  results step (this is a downstream verifier check; the implementation step itself does not write
  `results_detailed.md`). Confirms full REQ traceability.

## Task Requirement Checklist Coverage Matrix

For traceability, every REQ-* maps to at least one Step and one Verification Criterion:

| REQ | Steps | Verification Criteria |
| --- | --- | --- |
| REQ-1 | 4, 11, 13 | VC-12 |
| REQ-2 | 4 | VC-3 |
| REQ-3 | 4, 6 | VC-3 |
| REQ-4 | 4, 6 | VC-3 |
| REQ-5 | 3, 6 | VC-2 |
| REQ-6 | 6 | VC-3 |
| REQ-7 | 6, 7 | VC-1 |
| REQ-8 | 7 | VC-5 |
| REQ-9 | 7 | VC-6 |
| REQ-10 | 7, 11 | VC-7 |
| REQ-11 | 9 | VC-10 |
| REQ-12 | 8 | VC-1 (TSTOP via constants) |
| REQ-13 | 12, 13 | VC-8 |
| REQ-14 | 13 | VC-10 |
| REQ-15 | 12 | VC-7, VC-9 |
| REQ-16 | 10 | VC-4 |
| REQ-17 | 8 | VC-8 |
| REQ-18 | 11 | VC-13 |
| REQ-19 | 14 | VC-13 |
| REQ-20 | 8 | VC-3 (smoke test invocation) |
| REQ-21 | 5 | VC-2 |
| REQ-22 | 5 | VC-2, VC-5 |
