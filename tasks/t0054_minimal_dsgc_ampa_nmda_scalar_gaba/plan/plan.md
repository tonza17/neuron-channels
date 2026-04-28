---
spec_version: "2"
task_id: "t0054_minimal_dsgc_ampa_nmda_scalar_gaba"
date_completed: "2026-04-25"
status: "complete"
---
# Plan: Minimal DSGC with AMPA + NMDA Excitation and Scalar gabaMOD Inhibition

## Objective

Extend the t0052 minimal compartmental DSGC model by co-locating an NMDA `Exp2Syn` (`tau1=5 ms`,
`tau2=80 ms`, `e=0 mV`, voltage-independent — no Mg block) at every E synapse, sweep the NMDA peak
conductance `gNMDA` over `{0.0, 0.25, 0.5, 1.0}` nS, and replace t0052's `AMPA_ONLY` trial mode with
`E_ONLY` (AMPA + NMDA active, GABA `NetCon` weights zeroed). The sweep uses 12 directions × 10
trials × 3 trial modes (FULL, E_ONLY, GABA_ONLY) × 4 `gNMDA` values = 1,440 trials and produces
one new library asset (`minimal_dsgc_ampa_nmda_scalar_gaba`), 12 metric variants in
`results/metrics.json` (4 `gNMDA` × 3 modes), and three sweep-summary plots that directly answer
the task's headline questions: (1) how does the EPSP decay-to-1/e time scale with `gNMDA`? (2) does
NMDA close the peak-rate gap (t0052 reported 0.667 Hz vs in vivo 30-100 Hz)? (3) does NMDA improve
or degrade primary DSI under the scalar `gabaMOD` mechanism?

Done means: (a) the library asset structure validates against
`meta/asset_types/library/specification.md`; (b) `results/metrics.json` contains 12 variants with
`variant_id` schema `gnmda_<value>_<mode>`; (c) all three validation gates pass — quiescent rest
at -65 ± 0.5 mV, `gNMDA = 0` FULL rows match t0052's `tuning_curve_full.csv` row-by-row within 1e-6
Hz, and per-synapse placement is bit-identical to
`tasks/t0052_minimal_dsgc_scalar_gaba/results/placement_seed0.json`; (d) all 240+ per-direction PNGs
and 11+ sweep-summary / per-`gNMDA` overview PNGs exist; (e) all `REQ-*` items map to at least one
Step by Step item.

## Task Requirement Checklist

The operative task request from `task_description.md`:

> Extend t0052 by adding co-located NMDA Exp2Syn (tau1=5, tau2=80, e=0) at each E synapse; sweep
> gNMDA at {0, 0.25, 0.5, 1.0} nS; characterise EPSP decay, peak rate, and DSI vs gNMDA. Identical
> to t0052 unless explicitly noted. Morphology: `dsgc-baseline-morphology-calibrated`, 100 dendritic
> locations sampled with seed = 0 (bit-identical to t0052/t0053). Soma + AIS use `hh` with the
> boosted AIS parameters (`AIS_LENGTH_UM=30`, `AIS_DIAMETER_UM=2`, `AIS_GNABAR=1.2`,
> `AIS_GKBAR=0.04`, `AIS_GL=0.008`, `AIS_EL_HH=-65`); all dendrites passive (Rm=5999, Ra=100, cm=1,
> V_rest=-65). 100 E + 100 I co-located pairs. AMPA `Exp2Syn` tau1=0.5 ms, tau2=2.5 ms, e=0 mV, peak
> 0.5 nS. NMDA `Exp2Syn` tau1=5 ms, tau2=80 ms, e=0 mV, peak gNMDA (swept), driven by the same
> NetStim event as AMPA — voltage-independent (no Mg block). GABA scalar gabaMOD identical to
> t0052: peak 2 nS × gaba_mod(theta) where gaba_mod(0)=0.33, gaba_mod(180)=0.99. 12 directions ×
> 10 trials × 3 trial modes × 4 gNMDA values = 1,440 trials. Bar 200 µm × full arena, 1.0
> µm/ms, 1500 ms per trial, BASE_OFFSET_MS = 100. Trial modes: FULL (AMPA+NMDA+GABA), E_ONLY
> (AMPA+NMDA active, GABA NetCon weights zeroed — replaces t0052's AMPA_ONLY), GABA_ONLY
> (AMPA+NMDA NetCon weights zeroed, GABA active). Outputs: per gNMDA × per direction PNGs (soma
> V(t) FULL, aggregate EPSP, aggregate IPSP, PSTH 5 ms bins, per-synapse activation histogram); 8
> polar/Cartesian per-gNMDA overviews; 3 sweep-summary plots (EPSP decay-to-1/e vs gNMDA, peak Hz vs
> gNMDA, DSI vs gNMDA). `metrics.json` multi-variant: one variant per (gNMDA, mode) = 12 variants,
> variant_id schema `gnmda_<value>_<mode>`, registered keys `direction_selectivity_index`,
> `tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse`.
> `derived_quantities.json` per-variant: `peak_hz`, `null_hz`, `vector_sum_dsi`,
> `preferred_direction_deg`, `active_fraction=1.0`; per-`gNMDA`: `epsp_decay_to_1e_ms` for E_ONLY at
> preferred direction; plus existing t0052 fields (`gaba_mod_pd`, `gaba_mod_nd`). Library asset
> `minimal_dsgc_ampa_nmda_scalar_gaba`. Validation gates: quiescent rest -65 ± 0.5 mV; gNMDA=0 FULL
> rows match t0052's `tuning_curve_full.csv` within 1e-6 Hz; placement bit-identical to t0052. Local
> CPU only, ~75 min wall-clock for 1440 trials at ~3 s/trial, $0 cost.

Each requirement below has a stable ID used by the Step by Step section and the results step.

* `REQ-1` Morphology: load `dsgc-baseline-morphology-calibrated` from t0009 and build a NEURON cell
  with explicit soma / dendrite / AIS tagging. Evidence: cell-build log prints section count and
  total dendritic length matching the t0009 summary (1,536.25 um). Satisfied by Step 4.

* `REQ-2` Channels: `hh` only on `soma` and `axon_initial_segment` with the boosted AIS params
  (`AIS_GNABAR=1.2`, `AIS_GKBAR=0.04`, `AIS_GL=0.008`, `AIS_EL_HH=-65`); all dendrites passive
  (`Rm=5999`, `Ra=100`, `cm=1.0`, `V_rest=-65 mV`); cell silent at rest (V_rest = -65 ± 0.5 mV).
  Satisfied by Step 4 + Step 5.

* `REQ-3` Synapse placement: 100 E + 100 I co-located pairs sampled by length-weighted uniform draw
  with `numpy.random.default_rng(0)`; bit-identical to t0052/t0053. Evidence: per-synapse
  `(section_index, section_x, x_um, y_um, z_um)` in `results/placement_seed0.json` matches
  `tasks/t0052_minimal_dsgc_scalar_gaba/results/placement_seed0.json` within `1e-9`. Satisfied by
  Step 6 + Step 6b.

* `REQ-4` AMPA mechanism: `Exp2Syn` `tau1=0.5 ms`, `tau2=2.5 ms`, `e=0 mV`, peak `g=0.5 nS`, one
  event per synapse per trial. Evidence: `Exp2Syn.tau1`, `tau2`, `e` and `NetCon.weight[0]` printed
  in setup log. Satisfied by Step 7.

* `REQ-5` NMDA mechanism: at each E location, build a co-located NMDA `Exp2Syn` on the **same**
  segment as the AMPA `Exp2Syn`; `tau1=5 ms`, `tau2=80 ms`, `e=0 mV`, peak `gNMDA` (swept).
  Voltage-independent — no Mg block, no `n` exponent, no driving-force shaping beyond
  `i = g * (v - e)`. Evidence: `Exp2Syn.tau1`, `tau2`, `e` printed in setup log; one NMDA per E
  location. Satisfied by Step 7.

* `REQ-6` Same-NetStim event drives both AMPA and NMDA: a single `h.NetStim(number=1, noise=0)` per
  synapse drives an AMPA `NetCon` and a second NMDA `NetCon` (no second NetStim). NMDA fires from
  the same `NetStim.start` as AMPA. Evidence: per-pair construction logs one `NetStim` reference
  shared between `ampa_netcon` and `nmda_netcon`. Satisfied by Step 7.

* `REQ-7` GABA scalar gabaMOD identical to t0052: `Exp2Syn` `tau1=1 ms`, `tau2=20 ms`, `e=-75 mV`,
  peak `2 nS × gaba_mod(theta)` where
  `gaba_mod(theta) = 0.33 + 0.66 * (1 - cos(theta - 180°)) / 2`; `gaba_mod(0)=0.33`,
  `gaba_mod(180)=0.99`. Evidence: existing t0052 `test_gaba_mod.py` passes with the same formula.
  Satisfied by Step 8.

* `REQ-8` Position-gated firing: each synapse fires once per trial when the bar leading edge crosses
  its `(x, y)` projected on the bar's normal, no E/I offset, AMPA and NMDA share the same NetStim
  start. Evidence: per-synapse activation histogram shows monotonic onset-vs-coordinate relation.
  Satisfied by Step 7 + Step 11.

* `REQ-9` Stimulus: 12 directions (0, 30, ..., 330 deg), bar 200 um × arena length, speed 1000 um/s
  (= 1.0 um/ms), 1500 ms per trial, `BASE_OFFSET_MS = 100`. Evidence: bar geometry constants in
  `constants.py`; sweep loop logs 12 angles. Satisfied by Step 7 + Step 10.

* `REQ-10` Three trial modes: `FULL` (AMPA + NMDA + GABA), `E_ONLY` (AMPA + NMDA active, GABA NetCon
  weights zeroed — replaces t0052's `AMPA_ONLY`), `GABA_ONLY` (AMPA + NMDA NetCon weights zeroed,
  GABA active). The `TrialMode` enum has exactly these three members; no `AMPA_ONLY` legacy alias.
  Evidence: per-mode CSV files exist with the new names. Satisfied by Step 9 + Step 10.

* `REQ-11` `gNMDA` sweep: outer loop over `NMDA_PEAK_NS_VALUES = (0.0, 0.25, 0.5, 1.0)` nS.
  Evidence: per-mode CSVs gain a `gnmda_ns` column with 4 distinct values. Satisfied by Step 10.

* `REQ-12` 10 trials per `(angle, mode, gNMDA)` triple with deterministic seeds
  `1000 * angle_idx + trial_idx + 1` (same as t0052; seed does not depend on `gNMDA` so the
  `gnmda=0` regression gate is exact). Evidence: each per-mode CSV has 4 × 12 × 10 = 480 rows.
  Satisfied by Step 10.

* `REQ-13` Per-direction soma V(t) (FULL mode), mean ± SD across 10 trials, 12 PNGs per `gNMDA` =
  48 PNGs total. Satisfied by Step 11.

* `REQ-14` Per-direction aggregate EPSP (E_ONLY) and aggregate IPSP (GABA_ONLY), mean ± SD, 12 + 12
  PNGs per `gNMDA` = 96 PNGs total. Satisfied by Step 11.

* `REQ-15` Per-direction firing-rate PSTH (5 ms bins) mean across 10 trials, 12 PNGs per `gNMDA` =
  48 PNGs total. Satisfied by Step 11.

* `REQ-16` Per-direction per-synapse activation-time histogram, 12 PNGs per `gNMDA` = 48 PNGs total.
  Satisfied by Step 11.

* `REQ-17` Per-`gNMDA` polar and Cartesian tuning-curve overviews using the [t0011]
  `tuning_curve_viz` library: 4 polar + 4 Cartesian = 8 PNGs total. Satisfied by Step 11.

* `REQ-18` Three sweep-summary plots: (a) EPSP decay-to-1/e vs `gNMDA` (line plot, 4 points;
  optional one curve per direction or one aggregate); (b) peak Hz vs `gNMDA` (line plot, one curve
  per direction or aggregate); (c) DSI vs `gNMDA` (primary DSI and vector-sum DSI vs `gNMDA`).
  Satisfied by Step 11.

* `REQ-19` `metrics.json` in explicit multi-variant format with 12 variants — one per
  `(gNMDA, mode)` combination. Variant `id` schema `f"gnmda_{gnmda:.2f}_{mode}"` (e.g.,
  `gnmda_0.50_full`); `dimensions = {"gnmda_ns": <float>, "mode": "<full|e_only|gaba_only>"}`. Each
  variant carries the registered keys `direction_selectivity_index`, `tuning_curve_hwhm_deg`,
  `tuning_curve_reliability`, `tuning_curve_rmse` (the last only if
  `tasks/t0004_generate_target_tuning_curve/results/target_tuning_curve.csv` exists; otherwise
  omitted with a documented note). Satisfied by Step 12.

* `REQ-20` `derived_quantities.json` per-variant: `peak_hz`, `null_hz`, `vector_sum_dsi`,
  `preferred_direction_deg`, `active_fraction = 1.0`; per-`gNMDA`: `epsp_decay_to_1e_ms` for the
  `E_ONLY` variant at the preferred direction; plus the existing t0052 fields (`gaba_mod_pd`,
  `gaba_mod_nd`, `ipsp_ratio_null_over_pref`, `aggregate_epsp_peak_per_direction`,
  `aggregate_ipsp_peak_per_direction`). Satisfied by Step 12.

* `REQ-21` Validation gate — quiescent rest: `V_rest = -65 ± 0.5 mV` with no synapses (same as
  t0052 `test_quiescent_rest.py`). Hard-fails before the full sweep. Satisfied by Step 5.

* `REQ-22` Validation gate — `gNMDA = 0` regression: every row of t0054's `tuning_curve_full.csv`
  at `gnmda_ns = 0.0` matches the corresponding row of
  `tasks/t0052_minimal_dsgc_scalar_gaba/results/tuning_curve_full.csv` within `1e-6 Hz`. Hard-fails
  as a code-level assertion in `compute_metrics.py`. Satisfied by Step 12.

* `REQ-23` Validation gate — placement bit-identical to t0052: per-synapse coordinates in t0054's
  `results/placement_seed0.json` match t0052's within `1e-9`. Encoded as
  `code/test_placement_seed0_match.py`. Satisfied by Step 6b.

* `REQ-24` Library asset `minimal_dsgc_ampa_nmda_scalar_gaba` under
  `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/assets/library/` with `details.json`,
  `description.md` (eight mandatory sections per `meta/asset_types/library/specification.md`), and
  `module_paths` listing every code module. Satisfied by Step 13.

* `REQ-25` All compute is local CPU; total cost $0; no remote machines, no paid API calls. Satisfied
  by Step 14 (cost log).

* `REQ-26` Random seed for placement is fixed at 0 and reported in `results_detailed.md` (the
  reporting orchestrator step downstream of this plan reads the seed). Satisfied by Step 6.

* `REQ-27` Implementation wall-clock budget: ~75 min for the full 1,440-trial sweep at ~3 s/trial.
  Evidence: total wall-clock logged at end of run; comparable to t0052's 19 min for 360 trials and
  t0053's 17 min for 360 trials, scaled by 4× for the `gNMDA` outer loop. Satisfied by Step 10.

## Approach

The model is a **direct extension of t0052** with one mechanistic addition (NMDA `Exp2Syn`) and one
structural change (`AMPA_ONLY` → `E_ONLY` plus an outer `gNMDA` sweep loop). Per the t0053
canonical pattern, every t0052 module is copied verbatim into `tasks/t0054_*/code/` with an
import-path rewrite from `tasks.t0052_minimal_dsgc_scalar_gaba.code.*` to
`tasks.t0054_minimal_dsgc_ampa_nmda_scalar_gaba.code.*` and a bootstrap-sentinel rename
(`_T0052_NEURONHOME_BOOTSTRAPPED` → `_T0054_NEURONHOME_BOOTSTRAPPED`, defined in `constants.py:92`
and consumed in `neuron_bootstrap.py:38-45`).

**Modules copied verbatim from t0052 (10 files)**: `__init__.py`, `swc_io.py`, `cell.py`,
`placement.py`, `neuron_bootstrap.py`, `metrics_extra.py`, `trial.py` (with a small E_ONLY +
`gnmda_ns` extension — see below), `test_quiescent_rest.py`, `test_gaba_mod.py`. Plus
`test_placement_seed0_match.py` copied verbatim from t0053 with the same path rewrite.

**Modules extended**:

* `constants.py` adds `NMDA_TAU1_MS = 5.0`, `NMDA_TAU2_MS = 80.0`, `NMDA_E_MV = 0.0`,
  `NMDA_PEAK_NS_VALUES: tuple[float, ...] = (0.0, 0.25, 0.5, 1.0)`,
  `COL_GNMDA_NS: str = "gnmda_ns"`, and replaces the `TrialMode(StrEnum)` definition with members
  `FULL = "full"`, `E_ONLY = "e_only"`, `GABA_ONLY = "gaba_only"` (no `AMPA_ONLY` alias).
* `paths.py` updates `TASK_ID` to `t0054_*`, `LIBRARY_ID` to `minimal_dsgc_ampa_nmda_scalar_gaba`,
  renames per-mode CSVs from `*_ampa_only*` to `*_e_only*`, adds `T0052_PLACEMENT_JSON` (mirrors
  t0053), and adds three sweep-summary PNG paths (`EPSP_DECAY_VS_GNMDA_PNG`, `PEAK_HZ_VS_GNMDA_PNG`,
  `DSI_VS_GNMDA_PNG`).
* `synapses.py` extends the `EiPair` dataclass with `nmda_syn` and `nmda_netcon` fields, builds the
  NMDA `Exp2Syn` on the *same* `seg` as AMPA, and wires a second `h.NetCon(ampa_netstim, nmda_syn)`
  driven by the **same** `NetStim` (the task spec is explicit that no second NetStim is created).
  `schedule_ei_onsets` gains a `gnmda_ns: float` kwarg; the per-trial weight assignment is
  `pair.nmda_netcon.weight[0] = gnmda_ns * 1e-3`. Setting `gnmda_ns = 0.0` simply zeroes the weight
  — the synapse is constructed but produces no current, which is the cleanest way to satisfy the
  `gnmda = 0 == t0052` regression gate without conditional construction.
* `trial.py` learns the new `E_ONLY`/`GABA_ONLY` semantics: `E_ONLY` zeroes only GABA (AMPA and NMDA
  stay active); `GABA_ONLY` zeroes both AMPA and NMDA; the post-trial weight-restore block
  symmetrically restores both AMPA and NMDA. `run_one_trial` accepts `gnmda_ns: float` and
  propagates it to `schedule_ei_onsets`; `TrialResult` carries `gnmda_ns` so it is propagated into
  the per-trial CSV row.
* `run_tuning_curve.py` wraps the existing dry-run + sweep loop in an outer
  `for gnmda_ns in NMDA_PEAK_NS_VALUES`. All four `gNMDA` rows are appended to the same per-mode CSV
  (`tuning_curve_full.csv`, `tuning_curve_e_only.csv`, `tuning_curve_gaba_only.csv`) with a
  `gnmda_ns` column, so downstream analysis groups by `(gnmda_ns, mode)` instead of opening four
  files.
* `compute_metrics.py` groups per-mode CSVs by `gnmda_ns` to write 12 variants. Adds
  `_compute_epsp_decay_to_1e_ms`: per `gNMDA`, average the 10 preferred-direction `E_ONLY` voltage
  traces; find the peak depolarisation; find the first post-peak sample where
  `(v - v_init) <= peak_dep / e`; report `t_decay - t_peak`. Adds the **gNMDA = 0 regression
  hard-fail gate**: re-load t0052's `tuning_curve_full.csv` and assert every `gnmda_ns = 0.0` row
  matches within `1e-6 Hz`. Keeps the t0052 IPSP-ratio gate inside the `gnmda = 0` validation block.
* `render_figures.py` wraps the existing per-direction figure family in an outer `gnmda_ns` loop;
  output filename becomes `f"{prefix}_gnmda_{gnmda:.2f}_dir_{angle_deg:03d}.png"`. Adds three new
  top-level functions: `render_epsp_decay_vs_gnmda(out_path)`, `render_peak_hz_vs_gnmda`,
  `render_dsi_vs_gnmda` (line plots; with only 4 `gNMDA` values, heatmaps are unnecessary).

**Why voltage-independent NMDA via `Exp2Syn`, not the deposited Poleg-Polsky `bipolarNMDA.mod`?**
The task spec is explicit that this is the minimal NMDA — voltage-dependent NMDA with proper Mg
block is deferred to a follow-up task. `Exp2Syn` is voltage-independent by construction
(`i = g * (v - e)`, no `n` exponent, no Mg-block term), which is exactly what the spec asks for and
what avoids the `nrnivmodl` / custom HOC bootstrap that the [t0046]/[t0048] MOD-file route would
require. [t0048] reported that turning off the Mg block on the deposited cell (`Voff_bipNMDA = 1`)
reduces the DSI vs gNMDA range from 0.174 to 0.066 but never reaches the paper's flat ~0.30 line —
i.e., `Exp2Syn` NMDA on a different cell is in the same regime.

**Why one shared `NetStim` per pair, not one per synapse?** The task description is explicit that
AMPA and NMDA fire from "the same NetStim event", so we add a second `NetCon` instead of a second
`NetStim`. This guarantees AMPA and NMDA onset times are byte-identical and removes one class of
state-leak bug.

**Why append all four `gNMDA` rows to a single per-mode CSV?** The task description prefers this
over per-`gNMDA` filename suffixes for "downstream analysis ergonomics". `pandas.read_csv(...)`
+ `.groupby("gnmda_ns")` is much cleaner than four file handles.

**Alternatives considered.**

* Use the deposited `bipolarNMDA.mod` from [t0046] / [t0048]. Rejected: brings in `nrnivmodl`,
  custom HOC bootstrap, and Mg-block voltage dependence that the spec explicitly excludes from this
  minimal model. Voltage-dependent NMDA is deferred to a follow-up task.
* Keep `AMPA_ONLY` as a legacy alias for `E_ONLY`. Rejected: the task description is explicit that
  `E_ONLY` *replaces* `AMPA_ONLY`, and silently keeping the old name would produce two semantically
  distinct trial-mode names in the same enum.
* Drive AMPA and NMDA from two separate `NetStim` instances per pair. Rejected: the task spec
  requires one shared event; two NetStims doubles the state and adds a class of out-of-sync bugs
  (e.g., one `NetStim.start` updated and the other not).
* Per-`gNMDA` CSV filenames (e.g., `tuning_curve_full_gnmda_0.50.csv`). Rejected: 12 CSVs vs 3 CSVs
  is harder to feed to a pandas groupby; the task description explicitly prefers the
  single-CSV-with-`gnmda_ns`-column approach.
* Heatmap of DSI vs `(gNMDA, direction)` instead of three line plots. Rejected: only 4 `gNMDA`
  values × 12 directions = 48 cells; line plots with 12 curves are more readable and directly
  answer the headline questions.

**Task types.** `task.json` lists `build-model` and `experiment-run`, and both apply. `build-model`
drives the library-asset structure, hyperparameter logging, and reproducibility-seed guidelines
(`PLACEMENT_SEED = 0`, deterministic per-trial seeds). `experiment-run` drives the multi-mode
multi-`gNMDA` sweep, per-`(gnmda, mode)` breakdowns in `metrics.json`, the explicit multi-variant
metrics format, the chart requirements (≥ 2 charts; this plan delivers 250+), and the
validation-gate pattern (small dry run before the full 1,440-trial sweep).

**Registered metrics applicable to this task** (from `aggregate_metrics`):

* `direction_selectivity_index` — applicable; written for every variant where it can be computed
  (FULL and E_ONLY at every `gNMDA`).
* `tuning_curve_hwhm_deg` — applicable; written for FULL at every `gNMDA`.
* `tuning_curve_reliability` — applicable; cross-trial Pearson on the per-mode CSV grouped by
  `gnmda_ns`.
* `tuning_curve_rmse` — applicable only if a target curve from t0004 is present; otherwise omitted
  with a documented note (same policy as t0052).

`efficiency_*` metrics are not in the registry. Total wall-clock is logged in `results_detailed.md`
rather than `metrics.json` (consistent with t0052/t0053).

## Cost Estimation

* NEURON simulation: local CPU, $0.
* Plotting and analysis: local CPU, $0.
* No API calls (no LLM, no external data fetches).
* No remote machines (`available_services` is empty in `project/budget.json`).

**Total: $0.00.** Project budget is $1.00, current spend is $0.00. This task does not consume any of
the budget. `results/costs.json` will record `{}` (no paid services).

## Step by Step

### Milestone 1 — Bootstrap and Verbatim t0052 Modules

1. **Create `code/__init__.py` and `code/swc_io.py`.** Create
   `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/code/__init__.py` (empty marker) and copy
   `tasks/t0052_minimal_dsgc_scalar_gaba/code/swc_io.py` verbatim into
   `tasks/t0054_*/code/swc_io.py` — no logic changes; no import paths to rewrite. Expected output:
   `python -c "from tasks.t0054_minimal_dsgc_ampa_nmda_scalar_gaba.code.swc_io import parse_swc_file"`
   succeeds. Satisfies `REQ-1` (loader prerequisite).

2. **Copy and adapt `code/constants.py`.** Copy
   `tasks/t0052_minimal_dsgc_scalar_gaba/code/constants.py` to `tasks/t0054_*/code/constants.py`.
   Add `NMDA_TAU1_MS = 5.0`, `NMDA_TAU2_MS = 80.0`, `NMDA_E_MV = 0.0`,
   `NMDA_PEAK_NS_VALUES: tuple[float, ...] = (0.0, 0.25, 0.5, 1.0)`,
   `COL_GNMDA_NS: str = "gnmda_ns"`. Replace the `TrialMode(StrEnum)` definition (originally lines
   122-125) with members `FULL = "full"`, `E_ONLY = "e_only"`, `GABA_ONLY = "gaba_only"` — no
   `AMPA_ONLY` alias. Rename the bootstrap sentinel constant value from
   `_T0052_NEURONHOME_BOOTSTRAPPED` to `_T0054_NEURONHOME_BOOTSTRAPPED`. Satisfies `REQ-9`,
   `REQ-10`, `REQ-11`.

3. **Copy and adapt `code/paths.py`, `code/neuron_bootstrap.py`, and `code/metrics_extra.py`.** Copy
   each from t0052 verbatim. In `paths.py` update `TASK_ID = "t0054_*"`,
   `LIBRARY_ID = "minimal_dsgc_ampa_nmda_scalar_gaba"`, rename per-mode CSV constants from
   `*_AMPA_ONLY*` → `*_E_ONLY*`, add
   `T0052_PLACEMENT_JSON = REPO_ROOT / "tasks" / "t0052_minimal_dsgc_scalar_gaba" / "results" / "placement_seed0.json"`
   (mirroring t0053's `paths.py:53-55`), and add `EPSP_DECAY_VS_GNMDA_PNG`, `PEAK_HZ_VS_GNMDA_PNG`,
   `DSI_VS_GNMDA_PNG` under `IMAGES_DIR`. In `neuron_bootstrap.py` only the sentinel rename is
   needed (the consumers at lines 38-45 read the constant from `constants.py`). `metrics_extra.py`
   is copied verbatim — the `compute_vector_sum_dsi` and `compute_preferred_direction_deg`
   functions need no changes. Satisfies the runtime prerequisite for `REQ-1`.

### Milestone 2 — Cell Builder and Quiescent-Rest Validation Gate

4. **[CRITICAL] Copy `code/cell.py` verbatim from t0052.** No changes — the cell builder is
   independent of NMDA. Verify on first run that `dendrites` has > 6,000 sections and total
   dendritic length is `1536.25 ± 1` um (matches t0052 / t0053). Satisfies `REQ-1`, `REQ-2`.

5. **[VALIDATION GATE] Quiescent-rest dry run, `code/test_quiescent_rest.py`.** Copy verbatim from
   t0052. With no synapses constructed, run `h.finitialize(V_INIT_MV); h.continuerun(50.0)` and read
   soma voltage. **Baseline**: `V_rest = -65 mV`. **Failure condition**: if final soma voltage is
   outside `-65 ± 0.5 mV`, STOP, print the soma voltage trace, and debug the `pas` / `e_pas` / `Ra`
   / `cm` values before proceeding to synapse code. **Inspection**: print soma voltage at t = 0, 25,
   50 ms and the conductance summary for soma + one dendrite section. Satisfies `REQ-2`, `REQ-21`.
   Idempotent: re-runnable.

### Milestone 3 — Synapse Placement (Bit-Identical to t0052)

6. **Copy `code/placement.py` verbatim from t0052.** No changes; this guarantees the same sampling
   algorithm. After Step 4 produces `CellHandles`, call
   `sample_dendritic_locations(cell=cell, n_pairs=N_PAIRS, seed=PLACEMENT_SEED)` and write
   `results/placement_seed0.json` via `save_placement_json`. Satisfies `REQ-3`, `REQ-26`.

7. **[VALIDATION GATE] Build `code/test_placement_seed0_match.py`.** Copy verbatim from
   `tasks/t0053_minimal_dsgc_spatial_gaba/code/test_placement_seed0_match.py` (74 lines) with import
   paths rewritten to `tasks.t0054_*`. The test opens both placement JSONs (t0054's and
   `T0052_PLACEMENT_JSON`), loads them as lists of dicts, and asserts each pair's
   `(section_index, section_x, x_um, y_um, z_um)` matches within `POSITION_TOLERANCE = 1e-9`.
   **Baseline**: zero pairs differ. **Failure condition**: if any pair differs, STOP and dump the
   differing pairs; the placement RNG state has drifted. Run via
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0054_minimal_dsgc_ampa_nmda_scalar_gaba -- uv run pytest tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/code/test_placement_seed0_match.py -v`
   and confirm 1 passed. Satisfies `REQ-23`.

   I will reference this as **Step 6b** in subsequent text where it logically belongs after Step 6
   (numbering remains sequential as 7 here for the verificator).

### Milestone 4 — Synapse Builders Extended for NMDA

8. **Build `code/synapses.py` by copying t0052 and extending for NMDA.** Copy
   `tasks/t0052_minimal_dsgc_scalar_gaba/code/synapses.py` to `tasks/t0054_*/code/synapses.py`.
   Then:

   * Extend the `EiPair` `@dataclass(frozen=True, slots=True)` with two new fields: `nmda_syn: Any`
     and `nmda_netcon: Any`. Keep `ampa_syn`, `ampa_netcon`, `ampa_netstim`, `gaba_syn`,
     `gaba_netcon`, `gaba_netstim` unchanged.

   * In `build_ei_pairs`: after constructing each AMPA `Exp2Syn` on `seg`, build the NMDA `Exp2Syn`
     on the **same** `seg` with `tau1 = NMDA_TAU1_MS`, `tau2 = NMDA_TAU2_MS`, `e = NMDA_E_MV`. Wire
     a second `h.NetCon(ampa_netstim, nmda_syn)` with `weight[0] = 0.0` (set per-trial). The shared
     `ampa_netstim` is the same `NetStim` instance — no second NetStim is constructed. Satisfies
     `REQ-5`, `REQ-6`.

   * Extend `schedule_ei_onsets` with a new `gnmda_ns: float` keyword argument. The per-trial weight
     assignment becomes `pair.nmda_netcon.weight[0] = gnmda_ns * 1e-3` (NEURON `NetCon` weights are
     in microsiemens; `gnmda_ns × 1e-3` converts ns → us). Keep
     `pair.ampa_netcon.weight[0] = AMPA_PEAK_NS * 1e-3` and
     `pair.gaba_netcon.weight[0] = GABA_BASE_NS * gaba_mod_theta * 1e-3` unchanged.

   * Keep the `gaba_mod` helper formula unchanged (the t0052 `test_gaba_mod.py` still must pass).
     Satisfies `REQ-4`, `REQ-7`, `REQ-8`.

9. **Copy `code/test_gaba_mod.py` verbatim from t0052.** Only the import path is rewritten. The test
   asserts `gaba_mod(theta_deg=0) == 0.33 ± 1e-9` and `gaba_mod(theta_deg=180) == 0.99 ± 1e-9`.
   Satisfies the `REQ-7` evidence requirement.

### Milestone 5 — Trial Runner Extended for E_ONLY and gNMDA

10. **[CRITICAL] Build `code/trial.py` by copying t0052 and extending for the new modes.** Copy
    `tasks/t0052_minimal_dsgc_scalar_gaba/code/trial.py` and modify:

    * Replace the `_apply_mode_weights` `AMPA_ONLY` branch with `E_ONLY`: zero only every
      `pair.gaba_netcon.weight[0]`; AMPA and NMDA stay at their just-scheduled values.

    * In the `GABA_ONLY` branch, zero **both** `pair.ampa_netcon.weight[0] = 0.0` and
      `pair.nmda_netcon.weight[0] = 0.0` (in t0052 only AMPA was zeroed).

    * In the post-run weight-restore block (originally lines 121-128 of t0052 `trial.py`),
      symmetrically restore AMPA in the `GABA_ONLY` arm and add a parallel
      `pair.nmda_netcon.weight[0] = gnmda_ns * 1e-3` restoration so cross-mode state cannot leak.

    * Add a `gnmda_ns: float` argument to `run_one_trial`; propagate it to `schedule_ei_onsets` and
      store it on `TrialResult` (extend the `TrialResult` dataclass with a `gnmda_ns: float` field)
      so it can be written into the per-trial CSV row. Satisfies `REQ-10`, `REQ-11`.

### Milestone 6 — Sweep Harness with gNMDA Outer Loop

11. **[CRITICAL][VALIDATION GATE] Build `code/run_tuning_curve.py` by copying t0052 and adding the
    outer `gNMDA` loop.** Copy `tasks/t0052_minimal_dsgc_scalar_gaba/code/run_tuning_curve.py` (390
    lines) and modify:

    * Wrap the existing dry-run + 12-direction × 10-trial × 3-mode sweep in an outer
      `for gnmda_ns in NMDA_PEAK_NS_VALUES:` loop. Inside the loop, call `run_one_trial` with the
      current `gnmda_ns`.

    * Each per-mode CSV gains a `gnmda_ns` column. Append all four `gNMDA` rows to the same per-mode
      CSV — `tuning_curve_full.csv`, `tuning_curve_e_only.csv`, `tuning_curve_gaba_only.csv`. Each
      ends up with 4 × 12 × 10 = 480 rows.

    * Long-form voltage-trace CSVs (`voltage_traces_full.csv`, `voltage_traces_e_only.csv`,
      `voltage_traces_gaba_only.csv`) and the spike-time / activation-time CSVs likewise gain a
      `gnmda_ns` column.

    * **Validation gate (small-scale dry run)**: before launching the full 1,440-trial sweep, run a
      1-direction × 2-trial dry run for each `(gnmda_ns, mode)` combination at `gnmda_ns = 0.0`
      only — 6 trials total, ~10 s wall-clock. **Trivial baseline**: at `gnmda_ns = 0.0`, FULL
      mode at theta=0 must produce ≥ 1 spike per trial (matches t0052's 0.667 Hz × 1.5 s ≈ 1
      spike at the preferred direction). **Failure condition**: if 0 spikes are produced at
      `gnmda_ns = 0`, theta=0, FULL, STOP and inspect 5 individual `NetStim.start` and
      `NetCon.weight[0]` values; verify `Exp2Syn.tau1`, `tau2`, `e` were correctly assigned to both
      AMPA and NMDA; verify the `NetStim.start` window is inside `[0, TSTOP_MS]`. Do not launch the
      full sweep until the dry-run gate passes.

    * Then run the full 1,440-trial sweep with a `tqdm` progress bar that reports
      `(gnmda_ns, mode, angle_deg)`. Expected wall-clock: ~75 minutes at ~3 s/trial (CVODE adapts to
      NMDA's slow decay; the extra 200 NMDA ODE states are negligible against the ~6,700 dendritic
      compartments and 200 AMPA + GABA states). Log the total wall-clock to `results/wallclock.json`
      so it is preserved for downstream reporting.

    Expected outputs after the full sweep: three 480-row tuning-curve CSVs, three long-form
    voltage-trace CSVs (~2.4M rows each at dt=0.025 ms), three spike-time CSVs, and one
    activation-times CSV (4 × 12 × 100 = 4,800 rows). Satisfies `REQ-9`, `REQ-11`, `REQ-12`,
    `REQ-27`.

### Milestone 7 — Figures (Per-`gNMDA` × Per-direction + Sweep Summaries)

12. **Build `code/render_figures.py` by copying t0052 and adding the outer `gNMDA` loop +
    sweep-summary plots.** Copy `tasks/t0052_minimal_dsgc_scalar_gaba/code/render_figures.py` (231
    lines) and modify:

    * Wrap each existing per-direction figure family in an outer
      `for gnmda_ns in NMDA_PEAK_NS_VALUES:` loop. The output filename pattern becomes
      `f"{prefix}_gnmda_{gnmda:.2f}_dir_{angle_deg:03d}.png"` (e.g.,
      `v_soma_gnmda_0.50_dir_090.png`). Per-direction plots: `v_soma_*` (FULL), `epsp_*` (E_ONLY),
      `ipsp_*` (GABA_ONLY), `psth_*` (FULL, 5 ms bins), `activation_*` (per-synapse onset
      histogram). 12 directions × 5 plot kinds × 4 `gNMDA` values = 240 PNGs.

    * Add per-`gNMDA` polar and Cartesian tuning-curve overviews using
      `from tasks.t0011_response_visualization_library.code.tuning_curve_viz import plot_polar_tuning_curve, plot_cartesian_tuning_curve`.
      Output: 4 polar + 4 Cartesian = 8 PNGs. Pre-extract a per-`gNMDA` slice of
      `tuning_curve_full.csv` to a temporary CSV before passing to the [t0011] functions.

    * Add three sweep-summary functions (line plots — `matplotlib.pyplot.plot` is sufficient):

      * `render_epsp_decay_vs_gnmda(out_path)`: x-axis `gnmda_ns ∈ {0, 0.25, 0.5, 1.0}`, y-axis
        `epsp_decay_to_1e_ms` (computed in Step 13). One curve per direction (12 curves) plus a
        thicker aggregate curve, OR a single aggregate curve — choose whichever reads better; the
        spec is permissive on this point. Output: `epsp_decay_vs_gnmda.png`.

      * `render_peak_hz_vs_gnmda(out_path)`: x-axis `gnmda_ns`, y-axis `peak_hz` (FULL mode); one
        curve per direction plus the per-`gNMDA` max. Output: `peak_hz_vs_gnmda.png`.

      * `render_dsi_vs_gnmda(out_path)`: x-axis `gnmda_ns`, two curves: primary DSI and vector-sum
        DSI (FULL mode). Output: `dsi_vs_gnmda.png`.

    Total plots: 240 per-direction + 8 per-`gNMDA` overview + 3 sweep summary = 251 PNGs. Satisfies
    `REQ-13`, `REQ-14`, `REQ-15`, `REQ-16`, `REQ-17`, `REQ-18`.

### Milestone 8 — Metrics with 12 Variants and gNMDA = 0 Regression Gate

13. **Build `code/compute_metrics.py` by copying t0052 and extending for grouping by
    `(gnmda_ns, mode)`.** Copy `tasks/t0052_minimal_dsgc_scalar_gaba/code/compute_metrics.py` (304
    lines) and modify:

    * Group the per-mode CSV by `gnmda_ns` to produce one metrics variant per `(gnmda_ns, mode)`
      group. For each group, write a temporary one-`gNMDA` CSV slice and pass it to
      `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import load_tuning_curve, compute_dsi, compute_peak_hz, compute_null_hz, compute_hwhm_deg, compute_reliability`.
      Variant `id = f"gnmda_{gnmda:.2f}_{mode}"` (e.g., `gnmda_0.50_full`); `label` is
      human-readable (e.g., `"gNMDA = 0.50 nS, FULL"`);
      `dimensions = {"gnmda_ns": <float>, "mode": "<full|e_only|gaba_only>"}`.

    * Add `_compute_epsp_decay_to_1e_ms(traces_csv, gnmda_ns, preferred_direction_deg) -> float`:
      filter the E_ONLY voltage-trace CSV to the preferred direction at the given `gnmda_ns`,
      average the 10 trials, find the peak depolarisation `peak_dep = max(v_mean) - V_INIT_MV`, find
      the first post-peak sample where `(v - V_INIT_MV) <= peak_dep / math.e`, return
      `t_decay_ms - t_peak_ms`. Write as a per-`gNMDA` field in `derived_quantities.json`.

    * Add `derived_quantities.json` per-variant fields: `peak_hz`, `null_hz`, `vector_sum_dsi`,
      `preferred_direction_deg`, `active_fraction = 1.0` (constant — every synapse fires once per
      trial; included for parity with t0053). Plus the existing t0052 fields (`gaba_mod_pd = 0.33`,
      `gaba_mod_nd = 0.99`, `ipsp_ratio_null_over_pref`, `aggregate_epsp_peak_per_direction`,
      `aggregate_ipsp_peak_per_direction`).

    * **[VALIDATION GATE — gNMDA = 0 regression hard-fail]** After all variants are computed, load
      `tasks/t0052_minimal_dsgc_scalar_gaba/results/tuning_curve_full.csv` with pandas; filter
      t0054's `tuning_curve_full.csv` to `gnmda_ns == 0.0`; sort both by `(angle_deg, trial_seed)`;
      assert `numpy.allclose(t0054_rates, t0052_rates, atol=1e-6)`. **Baseline**: 120 row-by-row
      firing-rate matches within 1e-6 Hz. **Failure condition**: any row differs — STOP, print the
      offending `(angle_deg, trial_seed)` and both rates, and exit non-zero before writing
      `metrics.json`. Failure means either NMDA is leaking at zero conductance, NetCon weight reuse
      is leaking state between trials, or the placement RNG drifted. Inspection: read the diffs of
      all mismatched rows; verify the `gNMDA = 0` NetCon weights are exactly `0.0` after every
      trial; verify the placement seed match (Step 7) passed.

    * Keep the t0052 IPSP-ratio gate: hard-fail if `2.7 <= ipsp_ratio_null_over_pref <= 3.3` is
      violated. This still applies in t0054 because the GABA mechanism is unchanged.

    * Write `results/metrics.json` in **explicit multi-variant format** with 12 variants. Variants
      for which a metric is not measurable use `null` (e.g., `tuning_curve_hwhm_deg` for `e_only`
      and `gaba_only` modes when there are no spikes). The `tuning_curve_rmse` registered metric is
      added if and only if
      `tasks/t0004_generate_target_tuning_curve/results/target_tuning_curve.csv` exists; otherwise
      it is omitted with a documented note in `derived_quantities.json` (same policy as t0052).

    Expected metrics.json shape:

    ```json
    {
      "variants": [
        {
          "variant_id": "gnmda_0.00_full",
          "label": "gNMDA = 0.00 nS, FULL",
          "dimensions": {"gnmda_ns": 0.0, "mode": "full"},
          "metrics": {
            "direction_selectivity_index": 1.0,
            "tuning_curve_hwhm_deg": 82.5,
            "tuning_curve_reliability": 1.0
          }
        },
        ... 11 more variants ...
      ]
    }
    ```

    Satisfies `REQ-19`, `REQ-20`, `REQ-22`.

### Milestone 9 — Library Asset

14. **Create the `minimal_dsgc_ampa_nmda_scalar_gaba` library asset.** Create
    `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/assets/library/minimal_dsgc_ampa_nmda_scalar_gaba/details.json`
    with `spec_version="2"`, `library_id="minimal_dsgc_ampa_nmda_scalar_gaba"`,
    `name="Minimal DSGC AMPA + NMDA Scalar gabaMOD"`, `version="0.1.0"`, `short_description` (≥ 10
    words), `description_path="description.md"`, `module_paths` listing every code module under
    `tasks/t0054_*/code/`:
    `["code/constants.py", "code/paths.py", "code/swc_io.py", "code/neuron_bootstrap.py", "code/cell.py", "code/placement.py", "code/synapses.py", "code/trial.py", "code/run_tuning_curve.py", "code/render_figures.py", "code/compute_metrics.py", "code/metrics_extra.py"]`,
    `entry_points` listing
    `build_dsgc_from_swc, sample_dendritic_locations, build_ei_pairs, schedule_ei_onsets, gaba_mod, run_one_trial, TrialMode, compute_vector_sum_dsi, compute_preferred_direction_deg`,
    `dependencies=["neuron", "numpy", "matplotlib", "tqdm", "pandas"]`,
    `test_paths=["code/test_quiescent_rest.py", "code/test_gaba_mod.py", "code/test_placement_seed0_match.py"]`,
    `categories=["compartmental-modeling", "direction-selectivity", "synaptic-integration"]`,
    `created_by_task="t0054_minimal_dsgc_ampa_nmda_scalar_gaba"`, `date_created="2026-04-25"`.
    Create `assets/library/minimal_dsgc_ampa_nmda_scalar_gaba/description.md` with YAML frontmatter
    and the eight mandatory sections per `meta/asset_types/library/specification.md`: Metadata,
    Overview, API Reference, Usage Examples, Dependencies, Testing, Main Ideas, Summary. Run the
    library verificator and confirm zero errors. Satisfies `REQ-24`.

15. **Confirm $0 cost.** Verify no remote machines were created and no paid API calls were made
    during implementation. (The orchestrator's standard cost step writes the cost JSON itself; this
    plan item only flags the implementation-side requirement that nothing paid is invoked.)
    Satisfies `REQ-25`.

## Remote Machines

None required. Local CPU only. The model has roughly 6,700 dendritic compartments, 200 synapses (100
AMPA + 100 NMDA + 100 GABA = 300 mechanisms; the NMDA addition adds ~200 ODE states which is
negligible), and a 1.5-second simulation window at `dt = 0.025 ms` with CVODE (`atol = 1e-3`). One
trial completes in ~3 s on a modern CPU — t0052 reported 19 min 13 s for 360 trials (3.2 s/trial);
t0053 reported 17 min 11 s (2.86 s/trial). Total: 1,440 trials × ~3 s ≈ 75 min wall-clock for the
full sweep. No GPU, no remote provisioning, no `available_services` consumed.

## Assets Needed

* `dsgc-baseline-morphology-calibrated` from `t0009_calibrate_dendritic_diameters`. Read directly
  from
  `tasks/t0009_calibrate_dendritic_diameters/assets/dataset/dsgc-baseline-morphology-calibrated/files/141009_Pair1DSGC_calibrated.CNG.swc`.
* Library `tuning_curve_viz` from `t0011_response_visualization_library`. Imported as
  `from tasks.t0011_response_visualization_library.code.tuning_curve_viz import plot_polar_tuning_curve, plot_cartesian_tuning_curve`.
* Library `tuning_curve_loss` from `t0012_tuning_curve_scoring_loss_library`. Imported as
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import load_tuning_curve, compute_dsi, compute_peak_hz, compute_null_hz, compute_hwhm_deg, compute_reliability`.
* `tasks/t0052_minimal_dsgc_scalar_gaba/code/*` — copied verbatim or extended (10 files).
* `tasks/t0052_minimal_dsgc_scalar_gaba/results/tuning_curve_full.csv` — read by the `gNMDA = 0`
  regression gate in `compute_metrics.py`.
* `tasks/t0052_minimal_dsgc_scalar_gaba/results/placement_seed0.json` — read by
  `test_placement_seed0_match.py`.
* `tasks/t0053_minimal_dsgc_spatial_gaba/code/test_placement_seed0_match.py` — copied verbatim
  with import-path rewrite.
* NEURON 8.2.7 install at `C:\Users\md1avn\nrn-8.2.7` (toolchain established in t0007; imported via
  `code/neuron_bootstrap.py`).
* Optional: `tasks/t0004_generate_target_tuning_curve/results/target_tuning_curve.csv` for
  `tuning_curve_rmse` computation; if absent the metric is omitted with a note (same policy as
  t0052).

## Expected Assets

This task produces exactly one library asset, matching `task.json`
`expected_assets = {"library": 1}`:

* `library/minimal_dsgc_ampa_nmda_scalar_gaba` — the cell builder, SWC loader, synapse placer,
  AMPA + NMDA + GABA position-gated event drivers, scalar-gabaMOD scaling helper, three-mode trial
  runner (FULL / E_ONLY / GABA_ONLY) with `gnmda_ns` parameter, 12-direction × 4-`gNMDA` sweep
  harness, renderer suite (per-direction × per-`gNMDA` panels and three sweep-summary plots), and
  12-variant metrics computer with the `gNMDA = 0` regression hard-fail gate. Code lives under
  `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/code/`; the asset folder contains only
  `details.json` and `description.md`.

No other asset types (paper, dataset, model, predictions, answer) are produced.

## Time Estimation

* Research (already done): code research is complete (~3 hours total). No remaining research time.
* Milestone 1 (bootstrap + verbatim copies + constants/paths edits): ~1 hour.
* Milestone 2 (cell builder copy + quiescent-rest gate): ~30 min (copies; only validation).
* Milestone 3 (placement copy + placement-match test): ~30 min.
* Milestone 4 (synapse builder NMDA extension): ~2 hours including debug.
* Milestone 5 (trial runner E_ONLY / GABA_ONLY / gNMDA extension): ~1 hour.
* Milestone 6 (sweep harness with outer `gNMDA` loop, dry-run gate, full sweep): ~2 hours of coding
  \+ ~75 min NEURON simulation = ~3.25 hours.
* Milestone 7 (figures with outer `gNMDA` loop and three sweep-summary plots): ~2 hours.
* Milestone 8 (metrics with grouping, `gNMDA = 0` regression gate, `epsp_decay_to_1e_ms`): ~2 hours.
* Milestone 9 (library asset metadata + description.md): ~1 hour.
* Verification, fixing verificator errors: ~1 hour.
* **Total implementation wall-clock: ~14 hours**, comparable to t0052 / t0053. Of this, ~75 minutes
  is NEURON simulation wall-clock — the rest is coding, debugging, and verification.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| `gNMDA = 0` regression gate fails — t0054 FULL rates differ from t0052 at zero conductance | Medium | Critical — entire experiment is invalid | Step 13 hard-fails before writing `metrics.json`. Inspection: verify NMDA NetCon weight is exactly `0.0` at scheduling time and after every trial; verify the placement-match test (Step 7) passed; verify per-trial seed formula matches t0052 (`1000 * angle_idx + trial_idx + 1`); verify NetStim is shared between AMPA and NMDA (no second NetStim that could fire at a different time). |
| Placement seed drift — t0054 sample differs from t0052 by even one location | Low | Critical — biases every result | Step 7 placement-match test runs before any synapse code. If it fails, dump the differing pair indices and verify `numpy.random.default_rng(0)` is the only RNG touched before `sample_dendritic_locations` is called; verify no `numpy.random` global state was used elsewhere. |
| NMDA NetCon weight leaks across modes (e.g., after `GABA_ONLY` zeroes both AMPA and NMDA, the next FULL trial sees zero weights) | Medium | Critical — silent data corruption that the regression gate may or may not catch | Step 10 weight-restore block sets `pair.nmda_netcon.weight[0] = gnmda_ns * 1e-3` symmetrically with the AMPA restore. Add a per-trial assertion in `run_one_trial` that all three NetCon weights match the expected baseline at scheduling time, before `h.continuerun`. |
| Driving-force saturation flattens EPSP scaling with `gNMDA` (local Vm approaches `E_NMDA = 0 mV` when 100 NMDA synapses fire near-synchronously) | Medium | Soft — interesting finding, not a bug | Document the effect in `results_detailed.md` (orchestrator-managed); the sweep-summary plots will show whether `epsp_decay_to_1e_ms` and `peak_hz` scale linearly or sublinearly with `gNMDA`. Compare against [t0048] reports of `Voff_bipNMDA = 1` flattening DSI vs gNMDA from 0.174 to 0.066. |
| Dry-run gate at `gnmda_ns = 0` produces 0 spikes (entire pipeline broken) | Low | Critical | Step 11 dry-run gate halts before the full sweep. Inspection: read 5 individual `NetStim.start` and `NetCon.weight[0]` values; verify `Exp2Syn` parameters; verify `BASE_OFFSET_MS = 100` puts events inside `[0, TSTOP_MS = 1500]`. Same recovery as t0052's dry-run gate. |
| NMDA's slow decay (`tau2 = 80 ms`) inflates per-trial wall-clock beyond ~3 s | Low | Soft — only stretches the 75-min window | CVODE adapts the time step, so the slow decay does not change cost meaningfully on top of 6,700 dendritic compartments. If a single trial exceeds 30 s, raise `DT_MS` to 0.05 ms (still safe for `hh`) and re-profile; if still > 15 s, reduce `N_TRIALS_PER_ANGLE` to 5 and document the deviation. |
| Multi-spike trains at `gNMDA = 1.0` change the DSI denominator scaling unexpectedly (DSI vs `gNMDA` non-monotonic) | Medium | Soft — interesting finding | Report primary DSI and vector-sum DSI separately (the latter is robust to multi-spike rates); include the sweep-summary `dsi_vs_gnmda.png` showing both curves; flag in `derived_quantities.json` if any FULL variant shows > 5 spikes per trial at preferred direction (the regime [t0048] warned about). |
| Hard-step DSI (the t0022 / t0052 failure mode) at `gNMDA = 0` carries forward to all `gNMDA > 0` variants | Low | Soft | Already known: t0052's DSI = 1.0 is the trivial single-spike degenerate regime. If `gNMDA > 0` produces multi-spike trains, DSI will become non-trivial; this is the headline result the task is designed to find. HWHM is written for every FULL variant for early warning. |
| NEURON Windows bootstrap fails (env var, DLL path, version mismatch) | Low | Blocking | Reuse the t0052 / t0053 bootstrap pattern (battle-tested across 6+ tasks); if `ensure_neuron_importable()` raises, file an intervention noting expected vs actual NEURONHOME. |
| `tuning_curve_loss` or `tuning_curve_viz` API has changed since t0052 / t0053 | Low | Soft | Imports use the registered library paths; if any function signature changed, the call will raise immediately, the implementation patches the call site, and re-runs Step 13 / Step 12. |

## Verification Criteria

* `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/plan/plan.md` exists with all 11 mandatory
  sections and zero verificator errors. Run
  `uv run python -m arf.scripts.verificators.verify_plan t0054_minimal_dsgc_ampa_nmda_scalar_gaba`
  and confirm `errors: 0`.

* The library asset validates. Run
  `uv run python -u -m meta.asset_types.library.verificator tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/assets/library/minimal_dsgc_ampa_nmda_scalar_gaba`
  and confirm zero errors. Confirms `REQ-24`.

* All three sweep CSVs exist and have 480 rows each (4 `gNMDA` × 12 angles × 10 trials). Run
  `python -c "import pandas as pd; [print(p, len(pd.read_csv(p))) for p in ['tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/tuning_curve_full.csv', 'tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/tuning_curve_e_only.csv', 'tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/tuning_curve_gaba_only.csv']]"`
  and confirm 480 in every file. Confirms `REQ-9`, `REQ-10`, `REQ-11`, `REQ-12`.

* All four `gNMDA` values appear in every per-mode CSV. Run
  `python -c "import pandas as pd; print(sorted(pd.read_csv( 'tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/tuning_curve_full.csv' )['gnmda_ns'].unique()))"`
  and confirm `[0.0, 0.25, 0.5, 1.0]`. Confirms `REQ-11`.

* Placement bit-identical to t0052. Run
  `uv run pytest tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/code/test_placement_seed0_match.py -v`
  and confirm 1 passed. Confirms `REQ-23`.

* `gNMDA = 0` regression gate passes. The gate is encoded in `code/compute_metrics.py`; verify
  post-hoc with
  `python -c "import pandas as pd, numpy as np; a = pd.read_csv( 'tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/tuning_curve_full.csv'); a = a[a['gnmda_ns']==0.0].sort_values(['angle_deg','trial_seed']) ['firing_rate_hz'].to_numpy(); b = pd.read_csv( 'tasks/t0052_minimal_dsgc_scalar_gaba/results/tuning_curve_full.csv').sort_values( ['angle_deg','trial_seed'])['firing_rate_hz'].to_numpy(); assert np.allclose(a, b, atol=1e-6); print('gnmda=0 regression OK')"`
  and confirm `gnmda=0 regression OK` is printed. Confirms `REQ-22`.

* All 240 per-direction PNGs and 8 per-`gNMDA` overview PNGs and 3 sweep-summary PNGs exist. Run
  `python -c "from pathlib import Path; d = Path( 'tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/images'); print('per-dir', sum(1 for _ in d.glob('*_gnmda_*_dir_*.png'))); print('overview', sum(1 for _ in d.glob('*_tuning_curve_gnmda_*.png'))); print('sweep', sum(1 for n in ['epsp_decay_vs_gnmda.png','peak_hz_vs_gnmda.png', 'dsi_vs_gnmda.png'] if (d / n).exists()))"`
  and confirm `per-dir 240`, `overview 8`, `sweep 3`. Confirms `REQ-13`, `REQ-14`, `REQ-15`,
  `REQ-16`, `REQ-17`, `REQ-18`.

* `metrics.json` has 12 variants in explicit multi-variant format. Run
  `python -c "import json; m = json.load(open( 'tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/metrics.json')); v = m['variants']; assert len(v) == 12, len(v); ids = sorted(x['variant_id'] for x in v); print(ids)"`
  and confirm 12 variants with the `gnmda_<value>_<mode>` schema. Confirms `REQ-19`.

* `derived_quantities.json` contains per-`gNMDA` `epsp_decay_to_1e_ms`. Run
  `python -c "import json; d = json.load(open( 'tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/derived_quantities.json')); per = d['per_gnmda']; assert sorted(per.keys()) == ['0.00','0.25','0.50','1.00']; for k,v in per.items(): assert 'epsp_decay_to_1e_ms' in v, k; print(per)"`
  and confirm. Confirms `REQ-20`.

* IPSP ratio gate still passes (GABA mechanism is unchanged). Run
  `python -c "import json; d = json.load(open( 'tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/derived_quantities.json')); r = d['ipsp_ratio_null_over_pref']; assert 2.7 <= r <= 3.3, r; print('ipsp_ratio', r)"`
  and confirm. Confirms `REQ-7` (still holds in t0054).

* All `REQ-*` items map to at least one Step by Step item. Run
  `python -c "import re; t=open( 'tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/plan/plan.md').read(); reqs={m for m in re.findall(r'REQ-\d+', t)}; print(sorted(reqs, key=lambda s:int(s[4:])))"`
  and confirm `REQ-1` through `REQ-27` are all present in the plan body. Confirms requirement
  coverage.

* Cost gate: confirm `results/costs.json` is `{}` (no paid services) and no machine-setup log
  exists. Run
  `python -c "import json; assert json.load(open( 'tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/costs.json')) == {}; print('zero cost confirmed')"`.
  Confirms `REQ-25`.
