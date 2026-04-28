---
spec_version: "2"
task_id: "t0055_nmda_mg_block_dsi_recovery"
date_completed: "2026-04-28"
status: "complete"
---
# Plan: Add Mg-Block NMDA to Recover DSI in t0054 Minimal Architecture

## Objective

Replace the voltage-independent NMDA `Exp2Syn` in the t0054 minimal DSGC architecture with a custom
`NMDA_MgBlock` point process implementing the Jahr-Stevens Boltzmann Mg block, then re-run the
identical 1,440-trial sweep (4 `gNMDA` values × 12 directions × 10 trials × 3 trial modes) to
test whether voltage-dependent NMDA recovers the vector-sum DSI that t0054 lost (DSI collapsed from
**0.746** at `gNMDA = 0` to **0.082** at `gNMDA = 0.25 nS` and **0.017** at `gNMDA = 1.0 nS`). Every
other parameter — morphology, AMPA, GABA, HH soma + AIS, placement seed, stimulus protocol, random
seeds — is bit-identical to t0054. This task is the first in the minimal-architecture lineage to
introduce a custom MOD compilation step (`nrnivmodl`) into the bootstrap.

The headline pass criterion (S-0054-01): **vector-sum DSI > 0.50 AND peak Hz >= 5 Hz at
`gNMDA = 0.25 nS`, FULL mode**. Reporting must explicitly state PASS or FAIL against this criterion.

Done means: (a) the library asset `minimal_dsgc_mg_block_nmda` validates against
`meta/asset_types/library/specification.md`; (b) `results/metrics.json` contains 12 variants with
`variant_id` schema `gnmda_<value>_<mode>`; (c) all four validation gates pass — quiescent rest at
`-65 ± 0.5 mV`, `gNMDA = 0` FULL rows match t0054's `tuning_curve_full.csv` row-by-row within
`1e-6 Hz`, per-synapse placement is bit-identical to t0054's `placement_seed0.json`, and the new
NMDA voltage-dependence sanity test produces a monotonic peak-`gNMDA` curve where
`peak(-80 mV) <= 0.25 * peak(-20 mV)`; (d) all 240 per-direction PNGs and 4 sweep-summary PNGs (DSI
vs gNMDA, peak Hz vs gNMDA, EPSP-decay-tau vs gNMDA, Mg-block g(v) sanity) exist with t0054 overlays
where specified; (e) the headline summary explicitly states PASS or FAIL on the S-0054-01 criterion.

## Task Requirement Checklist

The operative task request from `task_description.md`:

> Replace the t0054 voltage-independent NMDA Exp2Syn with a Jahr-Stevens Mg-block point process at
> every E synapse, keep every other parameter identical, and re-run the same gNMDA sweep. The
> headline question is: does Mg block recover the DSI that t0054 lost? Identical to t0054 unless
> explicitly noted. Morphology: `dsgc-baseline-morphology-calibrated`, 100 dendritic locations
> sampled with seed = 0 (bit-identical placement to t0054). soma + axon_initial_segment use NEURON
> `hh` with the boosted AIS parameters (`AIS_LENGTH_UM=30`, `AIS_DIAMETER_UM=2`, `AIS_GNABAR=1.2`,
> `AIS_GKBAR=0.04`, `AIS_GL=0.008`, `AIS_EL_HH=-65`); all dendrites passive (`Rm=5999`, `Ra=100`,
> `cm=1`, `V_rest=-65 mV`). 100 E + 100 I co-located pairs. AMPA `Exp2Syn` `tau1=0.5 ms`,
> `tau2=2.5 ms`, `e=0 mV`, peak `0.5 nS`, driven by the same NetStim event as the NMDA point
> process. NMDA (CHANGED): a custom `NMDA_MgBlock` point process replacing the t0054 `Exp2Syn`. Same
> dual-exponential gating kinetics (`tau1=5 ms`, `tau2=80 ms`, `e=0 mV`) but multiplied by the
> Jahr-Stevens Mg-block factor `g_NMDA(v, t) = gNMDA_max * s(t) * 1 / (1 + n * exp(-gamma * v))`
> with `n = 0.25 / mM`, `gamma = 0.08 / mV` (the values used in `bipolarNMDA.mod` in t0046's ModelDB
> 189347 reproduction). `[Mg2+]` is folded into the `n` constant. A `Voff` parameter (default `0`)
> preserves the option to compare against the voltage-independent regime. Inhibition: scalar gabaMOD
> identical to t0054. 12 directions × 10 trials × 3 trial modes × 4 `gNMDA` values = 1,440
> trials. Bar 200 µm × full arena, 1.0 µm/ms, 1500 ms per trial, `BASE_OFFSET_MS = 100`. gNMDA
> sweep: `{0.0, 0.25, 0.5, 1.0}` nS. Trial modes: `FULL` (AMPA + NMDA + GABA active), `E_ONLY` (AMPA
> \+ NMDA active, GABA NetCon weights zeroed), `GABA_ONLY` (AMPA + NMDA NetCon weights zeroed, GABA
> active). Pass / Fail criterion: vector-sum DSI at `gNMDA = 0.25 nS` must exceed 0.50 AND peak Hz
> at `gNMDA = 0.25 nS` (preferred direction, FULL) must reach >= 5 Hz. Outputs: per `gNMDA` × per
> direction (4 × 12 = 48 panels per output type): soma `V(t)` (FULL, mean ± SD), aggregate EPSP
> (E_ONLY, mean ± SD), aggregate IPSP (GABA_ONLY, mean ± SD), PSTH (5 ms bins, FULL), per-synapse
> activation-time histogram. Sweep summaries: vector-sum DSI vs gNMDA with t0054 overlay; peak Hz vs
> gNMDA with t0054 overlay; EPSP decay-time-constant vs gNMDA with t0054 overlay; NMDA Mg-block g(v)
> sanity curve at `v ∈ [-80, +20] mV`. `metrics.json` (multi-variant): one variant per
> `(gNMDA, mode)` combination = 12 variants, `variant_id` schema `gnmda_<value>_<mode>`, registered
> keys `direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
> `tuning_curve_rmse`. `derived_quantities.json` per-variant: `peak_hz`, `null_hz`,
> `vector_sum_dsi`, `preferred_direction_deg`, `active_fraction`; per-`gNMDA`: `epsp_decay_to_1e_ms`
> for the `E_ONLY` variant at the preferred direction; plus `pass_criterion_dsi_at_gnmda_025`,
> `pass_criterion_peak_hz_at_gnmda_025`, `pass_criterion_overall` (boolean). Library asset:
> `minimal_dsgc_mg_block_nmda` under `tasks/t0055_*/assets/library/`. Validation gates: quiescent
> rest at `-65 ± 0.5 mV`; `gNMDA = 0` cross-task regression vs t0054 within `1e-6 Hz`; placement
> bit-identical to t0054; NMDA voltage-dependence sanity (single synapse, SEClamp at
> `v ∈ {-80, -60, -40, -20, 0, +20} mV`). Local CPU only; ~75 min wall-clock target for 1,440
> trials at ~3 s/trial; $0 cost.

Each requirement below has a stable ID used by the Step by Step section.

* `REQ-1` Author `code/mod/NMDA_MgBlock.mod` with the Jahr-Stevens Mg-block point process. Required
  parameters: `tau1 = 5 ms`, `tau2 = 80 ms`, `e = 0 mV`, `n = 0.25 / mM`, `gamma = 0.08 / mV`,
  `Voff` (default `0`), `Vset = -60 mV`. Required gating: dual-exponential `(A - B)` driven by
  `NET_RECEIVE` events, multiplied by Boltzmann factor `1 / (1 + n * exp(-gamma * local_v))` where
  `local_v = v * (1 - Voff) + Vset * Voff`. The MOD file header must cite `bipolarNMDA.mod` lines
  47-54 (parameters) and 108-109 (BREAKPOINT) under
  `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/sources/bipolarNMDA.mod`.
  Satisfied by Step 4.

* `REQ-2` Compile `code/mod/NMDA_MgBlock.mod` via `nrnivmodl` as part of the boot sequence. This
  task is the first in the minimal-architecture lineage to introduce a custom MOD compilation step.
  The compiled `nrnmech.dll` must live alongside the source in `code/mod/` (Windows MinGW toolchain
  writes the DLL into the source directory). The build is invoked by a 13-line
  `code/run_nrnivmodl.cmd` shim mirroring t0046's pattern. The DLL is loaded via
  `h.nrn_load_dll(str(NRNMECH_DLL))` inside an extended `neuron_bootstrap.py`, after
  `ensure_neuron_importable` and BEFORE `load_stdrun`. Idempotent: re-running is safe because
  `nrnivmodl` handles incremental rebuilds. Satisfied by Step 5.

* `REQ-3` Fork the t0054 codebase to t0055 with import-path rewrite
  `tasks.t0054_minimal_dsgc_ampa_nmda_scalar_gaba.code` ->
  `tasks.t0055_nmda_mg_block_dsi_recovery.code` and bootstrap-sentinel rename
  `_T0054_NEURONHOME_BOOTSTRAPPED` -> `_T0055_NEURONHOME_BOOTSTRAPPED`. 13 modules copied verbatim
  with the rewrite (`__init__.py`, `swc_io.py`, `cell.py`, `placement.py`, `paths.py`,
  `metrics_extra.py`, `test_quiescent_rest.py`, `test_gaba_mod.py`, `test_placement_seed0_match.py`,
  `compute_metrics.py`, `render_figures.py`, `run_tuning_curve.py`, `trial.py`); 3 modules extended
  (`constants.py`, `synapses.py`, `neuron_bootstrap.py`). Satisfied by Steps 1-3, 6, 7, 8.

* `REQ-4` Replace `h.Exp2Syn` for NMDA in `code/synapses.py` with `h.NMDA_MgBlock`. AMPA `Exp2Syn`
  is unchanged. The second-NetCon-on-the-same-NetStim wiring from t0054 is preserved verbatim (AMPA
  `NetCon` and NMDA `NetCon` both share the single per-pair `ampa_netstim`, guaranteeing
  byte-identical event times). The NMDA `NetCon.weight[0] = gnmda_ns * 1e-3` per-trial assignment is
  unchanged. New per-pair assignments: `nmda_syn.tau1 = NMDA_TAU1_MS`,
  `nmda_syn.tau2 = NMDA_TAU2_MS`, `nmda_syn.e = NMDA_E_MV`, `nmda_syn.n = MG_BLOCK_N`,
  `nmda_syn.gama = MG_BLOCK_GAMMA`, `nmda_syn.Voff = MG_BLOCK_VOFF`,
  `nmda_syn.Vset = MG_BLOCK_VSET_MV`. Satisfied by Step 8.

* `REQ-5` Validation gate — quiescent rest: `V_rest = -65 ± 0.5 mV` with no synapses constructed.
  Hard-fails before the full sweep. Identical to t0054. Satisfied by Step 11.

* `REQ-6` Validation gate — placement bit-identical to t0054. Per-synapse coordinates in t0055's
  `results/placement_seed0.json` must match
  `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/placement_seed0.json` within
  `POSITION_TOLERANCE = 1e-9`. Reference rebound from t0052 (in t0054) to t0054 (in t0055) via
  `paths.T0054_PLACEMENT_JSON`. Satisfied by Step 10 + Step 12.

* `REQ-7` Validation gate — `gNMDA = 0` cross-task regression vs t0054. Every row of t0055's
  `tuning_curve_full.csv` at `gnmda_ns = 0.0` must match the corresponding row of
  `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/tuning_curve_full.csv` (filtered to
  `gnmda_ns == 0.0`) within `1e-6 Hz`. With `gNMDA = 0` the Mg-block factor evaluates to a finite
  number but multiplies a zero conductance, so the result must be bit-identical to t0054 at
  `gnmda = 0` (which itself was bit-identical to t0052). Reference rebound from t0052 (in t0054) to
  t0054 (in t0055) via `paths.T0054_TUNING_CURVE_FULL_CSV`. Hard-fails before `metrics.json` is
  written. Satisfied by Step 16.

* `REQ-8` Validation gate (NEW) — NMDA voltage-dependence sanity test. With a single
  `h.NMDA_MgBlock` voltage-clamped via `h.SEClamp` at `v ∈ {-80, -60, -40, -20, 0, +20} mV`, drive
  a single `NetCon` event and record peak `gNMDA`. Assertions: (a) peak `gNMDA` is monotonically
  non-decreasing with depolarisation across the six voltages; (b)
  `peak(-80 mV) <= 0.25 * peak(-20 mV)`. Encoded as `code/test_nmda_mg_block_voltage_dep.py`. Order:
  AFTER `nrnivmodl` build but BEFORE the full sweep so a misconfigured MOD fails fast. Satisfied by
  Step 13.

* `REQ-9` Stimulus protocol identical to t0054: 12 directions (`0, 30, ..., 330 deg`), bar
  `200 µm × arena length`, speed `1.0 µm/ms = 1000 µm/s`, 1500 ms per trial,
  `BASE_OFFSET_MS = 100` (bar enters arena at `t = 100 ms`). Satisfied by Step 7 (constants) + Step
  14\.

* `REQ-10` Three trial modes identical to t0054: `FULL` (AMPA + NMDA + GABA active), `E_ONLY` (AMPA
  \+ NMDA active, GABA `NetCon` weights zeroed), `GABA_ONLY` (AMPA + NMDA `NetCon` weights zeroed,
  GABA active). Satisfied by Step 7.

* `REQ-11` 10 trials per `(angle, mode, gNMDA)` triple with deterministic per-trial seed
  `1000 * angle_idx + trial_idx + 1` (independent of `gNMDA`, ensuring the `gNMDA = 0` regression
  gate is exact). Satisfied by Step 14.

* `REQ-12` `gNMDA` outer sweep over `NMDA_PEAK_NS_VALUES = (0.0, 0.25, 0.5, 1.0)` nS, identical to
  t0054 to enable direct DSI deltas. Each per-mode CSV gains a `gnmda_ns` column. Satisfied by Step
  14\.

* `REQ-13` Run the full **4 `gNMDA` × 12 directions × 10 trials × 3 modes = 1,440 trials** sweep.
  Outputs: three 480-row tuning-curve CSVs, three long-form voltage-trace CSVs, three spike-time
  CSVs, one activation-times CSV. Satisfied by Step 14.

* `REQ-14` Compute 12 multi-variant metrics (4 `gNMDA` × 3 modes) using registered metric keys.
  `metrics.json` is in **explicit multi-variant format**. Variant `id = f"gnmda_{gnmda:.2f}_{mode}"`
  (e.g., `gnmda_0.50_full`).
  `dimensions = {"gnmda_ns": <float>, "mode": "<full|e_only|gaba_only>"}`. Each variant carries the
  registered keys `direction_selectivity_index`, `tuning_curve_hwhm_deg`,
  `tuning_curve_reliability`, `tuning_curve_rmse` (the last only if
  `tasks/t0004_generate_target_tuning_curve/results/target_tuning_curve.csv` exists; otherwise
  omitted with a documented note as in t0054). Satisfied by Step 16.

* `REQ-15` Render per-direction figures (4 `gNMDA` × 12 directions × 5 panel kinds = 240 PNGs):
  soma `V(t)` (FULL), aggregate EPSP (E_ONLY), aggregate IPSP (GABA_ONLY), PSTH (5 ms bins, FULL),
  per-synapse activation-time histogram. Satisfied by Step 15.

* `REQ-16` Render 4 sweep-summary PNGs: (a) `dsi_vs_gnmda.png` — vector-sum DSI vs gNMDA with
  t0054 (no-Mg) curve overlaid as a baseline; (b) `peak_hz_vs_gnmda.png` — peak Hz vs gNMDA with
  t0054 overlaid; (c) `epsp_decay_vs_gnmda.png` — EPSP decay-time-constant vs gNMDA with t0054
  overlaid (note: t0054 reports `null` for this metric due to the 1500 ms window; t0055 may inherit
  the same limitation); (d) `mg_block_g_v_curve.png` — NMDA Mg-block g(v) sanity plot showing the
  Boltzmann factor `1 / (1 + 0.25 * exp(-0.08 * v))` at `v ∈ [-80, +20] mV` overlaid with the
  empirical peak `gNMDA` values from the Step 13 voltage-clamp gate. Satisfied by Step 15.

* `REQ-17` Build the `minimal_dsgc_mg_block_nmda` library asset under
  `tasks/t0055_nmda_mg_block_dsi_recovery/assets/library/minimal_dsgc_mg_block_nmda/` with
  `details.json` (`spec_version="2"`, `library_id="minimal_dsgc_mg_block_nmda"`, etc.) and
  `description.md` (eight mandatory sections per `meta/asset_types/library/specification.md`). The
  asset must include a `sources/NMDA_MgBlock.mod` canonical artefact (in addition to the working
  copy under `code/mod/`). The README must document the Mg-block formula, parameter choices, and
  provenance from `bipolarNMDA.mod` lines 47-54 and 108-109 in t0046's `modeldb_189347_dsgc_exact`
  library. Satisfied by Step 17.

* `REQ-18` Headline pass criterion: `vector_sum_dsi > 0.50` AND `peak_hz >= 5 Hz` at
  `gNMDA = 0.25 nS`, FULL mode, must be evaluated and explicitly reported as PASS or FAIL. Encoded
  as three boolean fields in `derived_quantities.json`: `pass_criterion_dsi_at_gnmda_025`,
  `pass_criterion_peak_hz_at_gnmda_025`, `pass_criterion_overall`. Satisfied by Step 16.

* `REQ-19` `derived_quantities.json` per-variant fields: `peak_hz`, `null_hz`, `vector_sum_dsi`,
  `preferred_direction_deg`, `active_fraction = 1.0`. Per-`gNMDA` fields: `epsp_decay_to_1e_ms` for
  the `E_ONLY` variant at the preferred direction. Plus the three pass-criterion booleans from
  REQ-18. Plus existing t0054 fields (`gaba_mod_pd`, `gaba_mod_nd`, `ipsp_ratio_null_over_pref`,
  `aggregate_epsp_peak_per_direction`, `aggregate_ipsp_peak_per_direction`). Satisfied by Step 16.

* `REQ-20` Local CPU only; total cost $0; no remote machines, no paid API calls. Confirmed by Step
  18 (cost flag).

## Approach

The model is a **direct extension of t0054** with one mechanistic substitution (NMDA `Exp2Syn` ->
custom `NMDA_MgBlock` POINT_PROCESS) and one infrastructural addition (`nrnivmodl` build + DLL load
in `neuron_bootstrap.py`). Every other parameter — morphology, AMPA, GABA, HH soma + AIS,
placement seed, stimulus protocol, per-trial seeds — is bit-identical to t0054. This task is the
first in the minimal-architecture lineage `t0052 -> t0053 -> t0054 -> t0055` to introduce a custom
MOD compilation step.

**Why this hypothesis?** t0054's headline finding is that adding a voltage-INDEPENDENT NMDA
`Exp2Syn` (`tau1=5 ms`, `tau2=80 ms`, `e=0 mV`) at every AMPA location collapses vector-sum DSI from
**0.746** at `gNMDA = 0` to **0.082** at `gNMDA = 0.25 nS`. The interpretation in t0054's
`results_summary.md` is that the long-tail NMDA depolarisation (`tau2 = 80 ms`) keeps the cell above
threshold across both PD and ND trials, washing out the inhibition-driven directional asymmetry that
the scalar gabaMOD relies on (PD `gaba_mod = 0.33`, ND `gaba_mod = 0.99`). Mg block is the canonical
fix: it suppresses NMDA conductance at hyperpolarised voltages (when the cell is near `V_rest`) and
unblocks it once AMPA has already depolarised the cell. This restores multiplicative gain that
scales with the voltage trajectory, and so reinstates the directional asymmetry that GABA enforces.

**Mg-block formula.** The Boltzmann factor multiplying the dual-exponential gating is:

```text
g_NMDA(v, t) = gNMDA_max * (A(t) - B(t)) * 1 / (1 + n * exp(-gamma * v))
```

where `A' = -A/tau1`, `B' = -B/tau2`, `[Mg2+]` is folded into `n`, and `n = 0.25 / mM`,
`gamma = 0.08 / mV`. With these constants the Boltzmann factor is approximately 0.20 at `v = -80 mV`
(heavy block), 0.45 at `v = -40 mV`, 0.83 at `v = 0 mV`, and 0.95 at `v = +20 mV`. A `Voff`
parameter (default 0 = voltage-dependent) clamps `local_v` to `Vset = -60 mV` when set to 1
(voltage-independent regime, kept available for future ablation but NOT exercised in this task's
sweep). The formula and parameter values are taken verbatim from `bipolarNMDA.mod` lines 47-54
(parameters) and 108-109 (BREAKPOINT) at
`tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/sources/bipolarNMDA.mod`.

**Why a fresh minimal MOD instead of copying bipolarNMDA.mod verbatim?** `bipolarNMDA.mod` bundles
presynaptic vesicle release, AMPA conductance, and a calcium fraction (`ica` write) that t0055
explicitly does not want — AMPA in this architecture is a separate `Exp2Syn` and there is no `ica`
mechanism. A minimal MOD with only the Mg-block + dual-exponential gating + `NET_RECEIVE`-driven
event timing is a drop-in replacement for the t0054 NMDA `Exp2Syn`.

**Fork strategy: copy t0054 verbatim with single-line import-path rewrite.** The
minimal-architecture lineage [t0052] -> [t0053] -> [t0054] consistently uses the verbatim-copy
pattern where every Python module is duplicated into the next task's `code/` folder with a global
search-and-replace from `tasks.tNNNN_oldslug.code.*` to `tasks.tMMMM_newslug.code.*`. t0055 inherits
the same pattern: 13 modules will be copied verbatim from
`tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/code/` with the global rewrite
`tasks.t0054_minimal_dsgc_ampa_nmda_scalar_gaba.code` ->
`tasks.t0055_nmda_mg_block_dsi_recovery.code` and the bootstrap-sentinel rename
`_T0054_NEURONHOME_BOOTSTRAPPED` -> `_T0055_NEURONHOME_BOOTSTRAPPED`.

**MOD compilation pattern: lift from t0046 verbatim.** t0046's `code/run_nrnivmodl.cmd` is a 13-line
.cmd shim that pushd's into the source dir, calls `C:\Users\md1avn\nrn-8.2.7\bin\nrnivmodl.bat .`,
and pops back. The build is idempotent (safe to re-run). The DLL is loaded at NEURON startup via
`h.nrn_load_dll(str(NRNMECH_DLL))` after `ensure_neuron_importable` and BEFORE `load_stdrun`. The
Windows MinGW toolchain writes `nrnmech.dll` directly into the source directory
(`MOD_DIR / "nrnmech.dll"`, not `MOD_DIR / "x86_64" / "nrnmech.dll"` as on Linux).

**Validation-gate strategy: inherit t0054's three gates with reference rebound from t0052 to t0054,
plus add one new gate.** t0054's three gates are the quiescent-rest gate, the placement-match gate,
and the `gNMDA = 0` regression gate. t0055 inherits all three, with the placement reference rebound
to `T0054_PLACEMENT_JSON` and the regression reference rebound to `T0054_TUNING_CURVE_FULL_CSV`. The
new fourth gate is the NMDA voltage-dependence sanity test
(`code/test_nmda_mg_block_voltage_dep.py`): single `NMDA_MgBlock` under `h.SEClamp` at six clamp
voltages, single `NetCon` event, record peak `gNMDA`; assert monotonic in voltage and
`peak(-80 mV) <= 0.25 * peak(-20 mV)`. This catches any typo in the MOD file before the full
1,440-trial sweep starts.

**Why NMDA NetCon weight assignment unchanged?** With `gnmda_ns = 0` the Mg-block factor multiplies
a zero conductance, so the result must be bit-identical to t0054 at `gnmda = 0` (which itself was
bit-identical to t0052). The per-trial seed formula `1000 * angle_idx + trial_idx + 1` is explicitly
independent of `gnmda_ns`, ensuring the regression is exact.

**Alternatives considered.**

* **Copy `bipolarNMDA.mod` from [t0046] verbatim.** Rejected: brings in presynaptic vesicle release,
  AMPA, and `ica` write that t0055 explicitly does not want. The minimal MOD strips these to a pure
  NMDA point process driven by `NET_RECEIVE`.
* **Use NEURON's stock voltage-dependent NMDA mechanism (e.g., `nmda` from `nmodl/`).** Rejected: no
  stock NEURON NMDA mechanism implements the Jahr-Stevens form with the exact `(n=0.25, gamma=0.08)`
  parameters from the Poleg-Polsky 2016 reproduction. Authoring the MOD file directly preserves
  provenance.
* **Set `Voff = 1` to test the voltage-independent regime as a control variant.** Rejected: out of
  scope per the task description — `Voff = 0` is exercised only. The parameter is kept available
  in the MOD signature for future ablation tasks (e.g., S-0054-04).
* **Recompute placement rather than reading t0054's `placement_seed0.json`.** Rejected: the
  placement RNG is `numpy.random.default_rng(0)`, deterministic, and must be bit-identical to t0054.
  Reading t0054's placement JSON and asserting equality is the canonical pattern (used by t0053 and
  t0054 themselves).
* **Per-`gNMDA` CSV filenames.** Rejected: t0054 already established the single-CSV-per-mode
  convention with a `gnmda_ns` column for groupby ergonomics; no reason to deviate.

**Task types.** `task.json` lists `build-model` and `experiment-run`, both apply. `build-model`
drives the library-asset structure, hyperparameter logging (`MG_BLOCK_N`, `MG_BLOCK_GAMMA`,
`MG_BLOCK_VOFF`, `MG_BLOCK_VSET_MV`, `NMDA_PEAK_NS_VALUES`, `PLACEMENT_SEED = 0`, deterministic
per-trial seeds), and reproducibility-seed guidelines. `experiment-run` drives the multi-mode
multi-`gNMDA` sweep, the explicit multi-variant metrics format with one variant per `(gNMDA, mode)`
combination, the chart requirements (>= 2 charts; this plan delivers 244 PNGs), the validation-gate
pattern (small dry-run before the full 1,440-trial sweep), and the headline PASS/FAIL evaluation
against the S-0054-01 criterion. There is no remote compute, so the `build-model` GPU/cost guidance
is not exercised; `efficiency_*` metrics are not in the registry, so they are not written to
`metrics.json` (consistent with t0054).

**Registered metrics applicable to this task** (from `aggregate_metrics --format json`):

* `direction_selectivity_index` — applicable; written for every variant where it can be computed
  (FULL and E_ONLY at every `gNMDA`; not meaningful for `GABA_ONLY` which produces no spikes —
  emitted as `null`).
* `tuning_curve_hwhm_deg` — applicable; written for FULL at every `gNMDA`.
* `tuning_curve_reliability` — applicable; cross-trial Pearson on the per-mode CSV grouped by
  `gnmda_ns`.
* `tuning_curve_rmse` — applicable only if a target curve from t0004 is present; otherwise omitted
  with a documented note (same policy as t0054).

`efficiency_*` metrics are not in the registry. Total wall-clock is logged in `wallclock.json`
rather than `metrics.json` (consistent with t0054).

## Cost Estimation

* NEURON simulation: local CPU, **$0**.
* `nrnivmodl` MOD compilation: local CPU, **$0**.
* Plotting and analysis: local CPU, **$0**.
* No API calls (no LLM, no external data fetches).
* No remote machines (`available_services` is empty in `project/budget.json`).

**Total: $0.00.** Project budget is $1.00, current spend is $0.00. This task does not consume any of
the budget. `results/costs.json` will record `{}` (no paid services).

## Step by Step

### Milestone 1 — Bootstrap and Verbatim Module Copies

1. **Copy `code/__init__.py` and `code/swc_io.py` verbatim from t0054.** Source:
   `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/code/`. Destination:
   `tasks/t0055_nmda_mg_block_dsi_recovery/code/`. No logic changes; no import paths to rewrite.
   Expected output:
   `python -c "from tasks.t0055_nmda_mg_block_dsi_recovery.code.swc_io import parse_swc_file"`
   succeeds. Satisfies the loader prerequisite for REQ-3.

2. **Copy `code/cell.py`, `code/placement.py`, `code/metrics_extra.py` verbatim from t0054 with
   global import-path rewrite.** Replace `tasks.t0054_minimal_dsgc_ampa_nmda_scalar_gaba.code` with
   `tasks.t0055_nmda_mg_block_dsi_recovery.code`. No other changes. Satisfies REQ-3.

3. **Copy `code/test_quiescent_rest.py`, `code/test_gaba_mod.py`,
   `code/test_placement_seed0_match.py` verbatim from t0054 with import-path rewrite.** Then in
   `test_placement_seed0_match.py`, change the reference constant import from `T0052_PLACEMENT_JSON`
   (or whichever constant t0054 uses) to `T0054_PLACEMENT_JSON` so the placement-match test compares
   against t0054 instead of t0052. Satisfies REQ-3, REQ-5 (test code), REQ-6 (reference rebound).

### Milestone 2 — New MOD File and Build Infrastructure

4. **[CRITICAL] Author `code/mod/NMDA_MgBlock.mod`.** ~80 lines. Header comment cites
   `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/sources/bipolarNMDA.mod`
   lines 47-54 (parameters) and 108-109 (BREAKPOINT). Required NEURON blocks:

   * `NEURON { POINT_PROCESS NMDA_MgBlock RANGE tau1, tau2, e, n, gama, Voff, Vset, i, g NONSPECIFIC_CURRENT i }`
   * `PARAMETER` block with `tau1 = 5 (ms)`, `tau2 = 80 (ms)`, `e = 0 (mV)`, `n = 0.25 (/mM)`,
     `gama = 0.08 (/mV)`, `Voff = 0`, `Vset = -60 (mV)`.
   * `STATE { A B }` (dual-exponential gating states).
   * `INITIAL { A = 0 B = 0 }`.
   * `BREAKPOINT` with the gating expression: `local_v = v * (1 - Voff) + Vset * Voff`,
     `g = (B - A) / (1 + n * exp(-gama * local_v))`, `i = g * (v - e)`. (Sign convention: `B - A`
     because `tau2 > tau1` so `B` decays slower and `(B - A)` is positive after a brief rise —
     same convention as `Exp2Syn`.)
   * `DERIVATIVE state { A' = -A / tau1 B' = -B / tau2 }`.
   * `NET_RECEIVE(weight)` block: `A = A + weight`, `B = B + weight` so a single event deposits
     identical mass into both states; the dual-exponential `(B - A)` shape emerges from the
     difference of the two decay rates. (Equivalent to NEURON's stock `Exp2Syn.mod` event handling
     with the standard normalization factor; the unnormalised form is acceptable here because the
     per-pair NetCon weight is `gnmda_ns * 1e-3` in microsiemens, exactly matching t0054's NMDA
     Exp2Syn weight semantics.) Expected output: file exists with a syntactically valid MOD body
     that `nrnivmodl` accepts. Satisfies REQ-1.

5. **[CRITICAL] Author `code/run_nrnivmodl.cmd` (~13 lines).** Mirror exactly
   `tasks/t0046_reproduce_poleg_polsky_2016_exact/code/run_nrnivmodl.cmd` but point `MODDIR` at
   `code/mod/` instead of `code/sources/`. The shim must: `set "MODDIR=%~dp0mod"`,
   `pushd "%MODDIR%"`, `call "C:\Users\md1avn\nrn-8.2.7\bin\nrnivmodl.bat" .`, capture exit code,
   popd, exit. Idempotent (safe to re-run). Expected output after first invocation:
   `code/mod/nrnmech.dll` exists. (On the Windows MinGW toolchain `nrnmech.dll` is written into the
   source directory, NOT into a `x86_64/` subdirectory.) Satisfies REQ-2.

### Milestone 3 — Constants, Paths, Bootstrap Extension

6. **Copy and adapt `code/constants.py`.** Source: `tasks/t0054_*/code/constants.py` (138 lines).
   Destination: `tasks/t0055_*/code/constants.py`. Apply the import-path rewrite (no cross-task
   imports in this file, but rename references to t0054 in any docstrings). Then add the four new
   constants at the end of the existing constants block:

   ```python
   MG_BLOCK_N: float = 0.25  # per mM, [Mg2+] folded in (bipolarNMDA.mod L48)
   MG_BLOCK_GAMMA: float = 0.08  # per mV (bipolarNMDA.mod L49)
   MG_BLOCK_VOFF: float = 0.0  # 0 = voltage-dependent (Mg block on); 1 = voltage-independent
   MG_BLOCK_VSET_MV: float = -60.0  # used only when Voff = 1 (bipolarNMDA.mod L54)
   ```

   Rename the bootstrap-sentinel constant value from `_T0054_NEURONHOME_BOOTSTRAPPED` to
   `_T0055_NEURONHOME_BOOTSTRAPPED`. Document in a comment block that the four new constants are
   referenced verbatim from `bipolarNMDA.mod` lines 47-54. Satisfies REQ-3, REQ-4 (constants).

7. **Copy and adapt `code/paths.py`.** Source: `tasks/t0054_*/code/paths.py` (99 lines).
   Destination: `tasks/t0055_*/code/paths.py`. Update
   `TASK_ID = "t0055_nmda_mg_block_dsi_recovery"`, `LIBRARY_ID = "minimal_dsgc_mg_block_nmda"`.
   Replace `T0052_PLACEMENT_JSON` and `T0052_TUNING_CURVE_FULL_CSV` (or whichever constants t0054
   uses for the regression references) with `T0054_PLACEMENT_JSON` and `T0054_TUNING_CURVE_FULL_CSV`
   pointing at:

   * `T0054_PLACEMENT_JSON = REPO_ROOT / "tasks" / "t0054_minimal_dsgc_ampa_nmda_scalar_gaba" / "results" / "placement_seed0.json"`
   * `T0054_TUNING_CURVE_FULL_CSV = REPO_ROOT / "tasks" / "t0054_minimal_dsgc_ampa_nmda_scalar_gaba" / "results" / "tuning_curve_full.csv"`

   Add three new constants for the MOD build:

   * `NMDA_MOD_DIR = TASK_DIR / "code" / "mod"`
   * `NRNMECH_DLL = NMDA_MOD_DIR / "nrnmech.dll"`
   * `RUN_NRNIVMODL_CMD = TASK_DIR / "code" / "run_nrnivmodl.cmd"`

   Add the new sweep-summary PNG path:

   * `MG_BLOCK_G_V_PNG = IMAGES_DIR / "mg_block_g_v_curve.png"`

   Keep the existing three sweep-summary PNG path constants (`EPSP_DECAY_VS_GNMDA_PNG`,
   `PEAK_HZ_VS_GNMDA_PNG`, `DSI_VS_GNMDA_PNG`) unchanged. Satisfies REQ-3, REQ-6 (paths), REQ-7
   (paths), REQ-16 (paths).

8. **[CRITICAL] Copy and extend `code/neuron_bootstrap.py`.** Source:
   `tasks/t0054_*/code/neuron_bootstrap.py` (~82 lines). Destination:
   `tasks/t0055_*/code/neuron_bootstrap.py`. Apply the import-path rewrite and the sentinel rename
   (`_T0054_NEURONHOME_BOOTSTRAPPED` -> `_T0055_NEURONHOME_BOOTSTRAPPED`). Then add a new
   `ensure_nmda_mg_block_compiled()` function (~30 lines):

   * If `NRNMECH_DLL.exists()`, return immediately (idempotent).
   * Otherwise, run `subprocess.run([str(RUN_NRNIVMODL_CMD)], shell=True, check=True)`.
   * After the build, assert `NRNMECH_DLL.exists()` raises a clear error if not.

   Then in the existing top-level `ensure_neuron_importable()` flow, add a call to
   `ensure_nmda_mg_block_compiled()` AFTER `ensure_neuron_importable` succeeds and BEFORE
   `load_stdrun`. After `load_stdrun`, call `h.nrn_load_dll(str(NRNMECH_DLL))` to register the
   `NMDA_MgBlock` mechanism with the NEURON kernel. (Order matters: `nrn_load_dll` must happen
   before any code constructs an `h.NMDA_MgBlock(seg)` handle.) Add the imports for `NRNMECH_DLL`
   and `RUN_NRNIVMODL_CMD` from `paths.py`.

   Expected output after import:
   `python -c "from tasks.t0055_nmda_mg_block_dsi_recovery.code import neuron_bootstrap; neuron_bootstrap.ensure_neuron_importable(); from neuron import h; print(hasattr(h, 'NMDA_MgBlock'))"`
   prints `True`. Satisfies REQ-2, REQ-3.

### Milestone 4 — Synapse Builder Substitution

9. **[CRITICAL] Copy and adapt `code/synapses.py`.** Source: `tasks/t0054_*/code/synapses.py` (~222
   lines). Destination: `tasks/t0055_*/code/synapses.py`. Apply the import-path rewrite. Then in
   `build_ei_pairs`, locate the line that currently reads `nmda_syn: Any = h.Exp2Syn(seg)` (or
   equivalent) and replace it with `nmda_syn: Any = h.NMDA_MgBlock(seg)`. Set the attributes:

   ```python
   nmda_syn.tau1 = NMDA_TAU1_MS
   nmda_syn.tau2 = NMDA_TAU2_MS
   nmda_syn.e = NMDA_E_MV
   nmda_syn.n = MG_BLOCK_N
   nmda_syn.gama = MG_BLOCK_GAMMA
   nmda_syn.Voff = MG_BLOCK_VOFF
   nmda_syn.Vset = MG_BLOCK_VSET_MV
   ```

   AMPA `Exp2Syn` block is unchanged. The second-NetCon-on-the-same-NetStim wiring is unchanged
   (`h.NetCon(ampa_netstim, nmda_syn)`). The per-trial weight assignment in `schedule_ei_onsets`
   (`pair.nmda_netcon.weight[0] = gnmda_ns * 1e-3`) is unchanged. The `gaba_mod` helper is
   unchanged. Add new imports for `MG_BLOCK_N`, `MG_BLOCK_GAMMA`, `MG_BLOCK_VOFF`,
   `MG_BLOCK_VSET_MV` from `constants.py`. Satisfies REQ-4.

10. **Copy `code/trial.py` verbatim from t0054 with import-path rewrite only.** No logic changes.
    The existing `_apply_mode_weights` and post-trial weight-restore blocks already handle
    `nmda_netcon.weight[0]` correctly because the dual-exponential gating fires from `NetCon` events
    identically to `Exp2Syn`. Satisfies REQ-3, REQ-10.

### Milestone 5 — Validation Gates Before Full Sweep

11. **[VALIDATION GATE] Quiescent-rest test.** Run
    `uv run python -m arf.scripts.utils.run_with_logs --task-id t0055_nmda_mg_block_dsi_recovery -- uv run pytest tasks/t0055_nmda_mg_block_dsi_recovery/code/test_quiescent_rest.py -v`.
    **Baseline**: `V_rest = -65 mV` after a 50 ms continuerun with no synapses. **Failure
    condition**: if final soma voltage is outside `-65 ± 0.5 mV`, STOP, print the soma voltage
    trace at `t = 0, 25, 50 ms`, and debug `pas` / `e_pas` / `Ra` / `cm` values before proceeding.
    **Inspection**: read 5 dendrite-section conductance summaries to confirm `pas` is correctly
    inserted everywhere. Idempotent (re-runnable). Satisfies REQ-5.

12. **[VALIDATION GATE] Placement bit-identical to t0054.** Build the placement first by running a
    one-shot script that constructs a `CellHandles`, calls
    `sample_dendritic_locations(cell=cell, n_pairs=N_PAIRS, seed=PLACEMENT_SEED)`, and writes
    `results/placement_seed0.json`. Then run
    `uv run python -m arf.scripts.utils.run_with_logs --task-id t0055_nmda_mg_block_dsi_recovery -- uv run pytest tasks/t0055_nmda_mg_block_dsi_recovery/code/test_placement_seed0_match.py -v`.
    **Baseline**: zero pairs differ from `T0054_PLACEMENT_JSON` within `POSITION_TOLERANCE = 1e-9`.
    **Failure condition**: if any pair differs, STOP and dump the differing pair indices; the
    placement RNG state has drifted. Satisfies REQ-6.

13. **[VALIDATION GATE — NEW] NMDA voltage-dependence sanity test.** Author
    `code/test_nmda_mg_block_voltage_dep.py` (~80 lines). Test fixture: build a single one-section
    cell (one `Section` with `nseg = 1`, `L = 10 µm`, `diam = 1 µm`, `pas` inserted,
    `e_pas = -65`). Construct a single `h.NMDA_MgBlock(seg)` with `tau1 = 5`, `tau2 = 80`, `e = 0`,
    `n = 0.25`, `gama = 0.08`, `Voff = 0`, `Vset = -60`. For each
    `v_clamp_mv in [-80, -60, -40, -20, 0, +20]`:

    * Construct an `h.SEClamp(seg)` with `dur1 = 200 ms`, `amp1 = v_clamp_mv`, `rs = 0.001 MOhm`
      (very low series resistance to clamp tightly).
    * Construct an `h.NetStim(number=1, noise=0, start=100, interval=1)`.
    * Construct an `h.NetCon(netstim, nmda_syn, weight=1e-3)` (1 nS-equivalent).
    * `h.finitialize(v_clamp_mv)`, `h.continuerun(200)`.
    * Record `nmda_syn.g` over time via `h.Vector().record(nmda_syn._ref_g)`. Capture
      `peak_g_at_v[v_clamp_mv] = max(g_trace)`.

    Assertions:

    * `peak_g_at_v[-80] <= peak_g_at_v[-60] <= peak_g_at_v[-40] <= peak_g_at_v[-20] <= peak_g_at_v[0] <= peak_g_at_v[+20]`
      (monotonic non-decreasing).
    * `peak_g_at_v[-80] <= 0.25 * peak_g_at_v[-20]` (Boltzmann 0.20/0.74 ratio at the two voltages,
      with margin).

    Run:
    `uv run python -m arf.scripts.utils.run_with_logs --task-id t0055_nmda_mg_block_dsi_recovery -- uv run pytest tasks/t0055_nmda_mg_block_dsi_recovery/code/test_nmda_mg_block_voltage_dep.py -v`.
    Save the six `(v_clamp_mv, peak_g)` pairs to `results/mg_block_g_v_empirical.json` for use in
    Step 15's Mg-block g(v) sanity plot. **Failure condition**: if monotonicity fails or the ratio
    is wrong, STOP and inspect the MOD file's BREAKPOINT block — most likely the `local_v`
    expression sign is wrong or `gama` is in the wrong place. Satisfies REQ-8.

### Milestone 6 — Sweep Harness with Outer gNMDA Loop

14. **[CRITICAL] Copy and adapt `code/run_tuning_curve.py` from t0054.** Source:
    `tasks/t0054_*/code/run_tuning_curve.py` (~484 lines). Destination:
    `tasks/t0055_*/code/run_tuning_curve.py`. Apply import-path rewrite. Then prepend a call to
    `neuron_bootstrap.ensure_nmda_mg_block_compiled()` BEFORE the existing
    `ensure_neuron_importable()` call in the `if __name__ == "__main__"` block (or wherever the
    existing bootstrap is invoked) — this guarantees the MOD is built before NEURON is touched.

    The existing sweep loop is
    `for gnmda_ns in NMDA_PEAK_NS_VALUES: for angle_idx in range(N_ANGLES): for trial_idx in range(N_TRIALS_PER_ANGLE): for mode in TrialMode: run_one_trial(...)`.
    No structural changes — only the prepended bootstrap call.

    **Validation gate (small-scale dry run)** — already present in t0054's `run_tuning_curve.py`,
    inherited verbatim: before launching the full 1,440-trial sweep, run a 1-direction × 2-trial
    dry run for each `(gnmda_ns, mode)` combination at `gnmda_ns = 0.0` only — 6 trials total, ~10
    s wall-clock. **Trivial baseline**: at `gnmda_ns = 0.0`, FULL mode at theta = 0 must produce >=
    1 spike per trial (matches t0054's gnmda=0 row at theta=0). **Failure condition**: if 0 spikes
    are produced at `gnmda_ns = 0`, theta = 0, FULL, STOP and inspect 5 individual `NetStim.start`
    and `NetCon.weight[0]` values; verify `NMDA_MgBlock.tau1`, `tau2`, `e`, `n`, `gama`, `Voff` were
    correctly assigned; verify the AMPA `Exp2Syn.tau1`, `tau2`, `e` were correctly assigned; verify
    the `NetStim.start` window is inside `[0, TSTOP_MS]`.

    Then run the full 1,440-trial sweep with a `tqdm` progress bar that reports
    `(gnmda_ns, mode, angle_deg)`. Expected wall-clock: ~75 minutes target at ~3 s/trial; t0054's
    actual run was 4 h 19 min so up to ~5 hours is acceptable; abort and create a parallelisation
    task if wall-clock exceeds 6 hours (see Risks). Log the total wall-clock to
    `results/wallclock.json`.

    Expected outputs after the full sweep: three 480-row tuning-curve CSVs (`tuning_curve_full.csv`,
    `tuning_curve_e_only.csv`, `tuning_curve_gaba_only.csv`), three long-form voltage-trace CSVs
    (~2.4M rows each at `dt = 0.025 ms`), three spike-time CSVs, and one activation-times CSV (4 ×
    12 × 100 = 4,800 rows). Satisfies REQ-9, REQ-11, REQ-12, REQ-13.

### Milestone 7 — Figures

15. **Copy and extend `code/render_figures.py` from t0054.** Source:
    `tasks/t0054_*/code/render_figures.py` (~391 lines). Destination:
    `tasks/t0055_*/code/render_figures.py`. Apply import-path rewrite. Inherit the existing outer
    `gnmda_ns` loop and per-direction figure family (240 PNGs with the
    `f"{prefix}_gnmda_{gnmda:.2f}_dir_{angle_deg:03d}.png"` filename pattern: `v_soma_*` (FULL),
    `epsp_*` (E_ONLY), `ipsp_*` (GABA_ONLY), `psth_*` (FULL, 5 ms bins), `activation_*` per-synapse
    onset histogram). Satisfies REQ-15.

    Then update the three existing sweep-summary functions to add t0054 overlays:

    * `render_dsi_vs_gnmda(out_path)`: x-axis `gnmda_ns ∈ {0, 0.25, 0.5, 1.0}`, y-axis vector-sum
      DSI (FULL mode). One curve for t0055 (this task) plus a second curve for t0054 loaded from
      `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/derived_quantities.json` (the
      `vector_sum_dsi` per-variant `gnmda_*_full` field). Output: `dsi_vs_gnmda.png`.
    * `render_peak_hz_vs_gnmda(out_path)`: x-axis `gnmda_ns`, y-axis `peak_hz` (FULL). Two curves:
      t0055 vs t0054. Output: `peak_hz_vs_gnmda.png`.
    * `render_epsp_decay_vs_gnmda(out_path)`: x-axis `gnmda_ns`, y-axis `epsp_decay_to_1e_ms`
      (E_ONLY at preferred direction). Two curves: t0055 vs t0054. (Note: t0054 reports `null`
      across all `gNMDA` values; t0055 may inherit the same limitation. The plot should display "no
      data" annotations where values are null rather than crashing.) Output:
      `epsp_decay_vs_gnmda.png`.

    Add a new function `render_mg_block_g_v_curve(out_path)`: load
    `results/mg_block_g_v_empirical.json` (written by Step 13). Plot two curves on the same axes:
    (a) the analytical Boltzmann factor `f(v) = 1 / (1 + 0.25 * exp(-0.08 * v))` densely sampled at
    `v ∈ [-80, +20] mV`; (b) the empirical peak `gNMDA` at the six clamp voltages from Step 13,
    normalised to the empirical peak at `v = +20 mV` so it is directly comparable to the analytical
    curve. Output: `mg_block_g_v_curve.png`. Save under `IMAGES_DIR`.

    Total plots: 240 per-direction + 8 per-`gNMDA` polar/Cartesian overviews (inherited from t0054)
    \+ 4 sweep summary = 252 PNGs. Satisfies REQ-15, REQ-16.

### Milestone 8 — Metrics and Pass-Criterion Evaluation

16. **[CRITICAL] Copy and extend `code/compute_metrics.py` from t0054.** Source:
    `tasks/t0054_*/code/compute_metrics.py` (~445 lines). Destination:
    `tasks/t0055_*/code/compute_metrics.py`. Apply import-path rewrite. Update the `gNMDA = 0`
    regression-gate reference (t0054 used `T0052_TUNING_CURVE_FULL_CSV`; t0055 uses
    `T0054_TUNING_CURVE_FULL_CSV`).

    The 12-variant `metrics.json` writer is inherited verbatim from t0054 (one variant per
    `(gnmda_ns, mode)` combination, registered keys `direction_selectivity_index`,
    `tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse`). Variants for which a
    metric is not measurable use `null` (e.g., `direction_selectivity_index` for `gaba_only`).
    `tuning_curve_rmse` is added if and only if
    `tasks/t0004_generate_target_tuning_curve/results/target_tuning_curve.csv` exists; otherwise
    omitted with a documented note.

    **[VALIDATION GATE — gNMDA = 0 cross-task regression hard-fail]** After all variants are
    computed, load `T0054_TUNING_CURVE_FULL_CSV` with pandas; filter to `gnmda_ns == 0.0`; sort by
    `(angle_deg, trial_seed)`; do the same for t0055's `tuning_curve_full.csv`; assert
    `numpy.allclose(t0055_rates, t0054_rates, atol=1e-6)`. **Baseline**: 120 row-by-row firing-rate
    matches within `1e-6 Hz`. **Failure condition**: any row differs — STOP, print the offending
    `(angle_deg, trial_seed)` and both rates, exit non-zero before writing `metrics.json`. Failure
    means either NMDA is leaking at zero conductance, NetCon weight reuse is leaking state, the
    placement RNG drifted, or the per-trial seed formula changed. Inspection: verify the `gNMDA = 0`
    NetCon weights are exactly `0.0` after every trial; verify the placement-match test (Step 12)
    passed; verify per-trial seed is `1000 * angle_idx + trial_idx + 1`. Satisfies REQ-7.

    Add the **headline pass-criterion evaluation** to the `derived_quantities.json` writer:

    ```python
    pass_dsi = derived["per_variant"]["gnmda_0.25_full"]["vector_sum_dsi"] > 0.50
    pass_hz = derived["per_variant"]["gnmda_0.25_full"]["peak_hz"] >= 5.0
    derived["pass_criterion_dsi_at_gnmda_025"] = bool(pass_dsi)
    derived["pass_criterion_peak_hz_at_gnmda_025"] = bool(pass_hz)
    derived["pass_criterion_overall"] = bool(pass_dsi and pass_hz)
    ```

    Print the PASS/FAIL line to stdout at the end of the script:
    `print(f"S-0054-01 PASS={derived['pass_criterion_overall']} DSI={dsi:.3f} peakHz={hz:.3f}")`.

    `derived_quantities.json` per-variant fields, per-`gNMDA` fields, and the existing IPSP-ratio
    gate are inherited verbatim from t0054. Satisfies REQ-7, REQ-14, REQ-18, REQ-19.

### Milestone 9 — Library Asset

17. **Create the `minimal_dsgc_mg_block_nmda` library asset.** Create
    `tasks/t0055_nmda_mg_block_dsi_recovery/assets/library/minimal_dsgc_mg_block_nmda/details.json`
    with `spec_version="2"`, `library_id="minimal_dsgc_mg_block_nmda"`,
    `name="Minimal DSGC AMPA + Mg-Block NMDA + Scalar gabaMOD"`, `version="0.1.0"`,
    `short_description` (>= 10 words), `description_path="description.md"`, `module_paths` listing
    every code module under `tasks/t0055_*/code/`:
    `["code/constants.py", "code/paths.py", "code/swc_io.py", "code/neuron_bootstrap.py", "code/cell.py", "code/placement.py", "code/synapses.py", "code/trial.py", "code/run_tuning_curve.py", "code/render_figures.py", "code/compute_metrics.py", "code/metrics_extra.py"]`,
    `entry_points` listing
    `build_dsgc_from_swc, sample_dendritic_locations, build_ei_pairs, schedule_ei_onsets, gaba_mod, run_one_trial, TrialMode, compute_vector_sum_dsi, compute_preferred_direction_deg, ensure_nmda_mg_block_compiled`,
    `dependencies=["neuron", "numpy", "matplotlib", "tqdm", "pandas"]`,
    `test_paths=["code/test_quiescent_rest.py", "code/test_gaba_mod.py", "code/test_placement_seed0_match.py", "code/test_nmda_mg_block_voltage_dep.py"]`,
    `categories=["compartmental-modeling", "direction-selectivity", "synaptic-integration"]`,
    `created_by_task="t0055_nmda_mg_block_dsi_recovery"`, `date_created="2026-04-28"`.

    Also place the canonical MOD artefact at
    `tasks/t0055_*/assets/library/minimal_dsgc_mg_block_nmda/sources/NMDA_MgBlock.mod` (a copy of
    `code/mod/NMDA_MgBlock.mod`). The `code/mod/` location is the working build dir (where the DLL
    is written); the `sources/` subfolder under the library asset is the canonical artefact that
    will be aggregated.

    Create `assets/library/minimal_dsgc_mg_block_nmda/description.md` with YAML frontmatter and the
    eight mandatory sections per `meta/asset_types/library/specification.md`: Metadata, Overview,
    API Reference, Usage Examples, Dependencies, Testing, Main Ideas, Summary. The Main Ideas
    section must document the Mg-block formula, parameter choices (`n=0.25`, `gama=0.08`, `Voff=0`,
    `Vset=-60`), and provenance (citing `bipolarNMDA.mod` lines 47-54 and 108-109 in t0046's
    `modeldb_189347_dsgc_exact` library).

    Run the library verificator and confirm zero errors. Satisfies REQ-17.

### Milestone 10 — Cost Confirmation

18. **Confirm $0 cost.** Verify no remote machines were created and no paid API calls were made
    during steps 1-17. The implementation-side requirement is that nothing paid is invoked.
    Satisfies REQ-20.

## Remote Machines

None required. Local CPU only. The model has roughly 6,700 dendritic compartments, 200 synapses (100
AMPA + 100 NMDA + 100 GABA = 300 mechanisms; the substitution from `Exp2Syn` NMDA to `NMDA_MgBlock`
adds approximately 0 new ODE states on top of t0054's NMDA `Exp2Syn`), and a 1.5 s simulation window
at `dt = 0.025 ms` with CVODE (`atol = 1e-3`). One trial completes in ~3 s on a modern CPU on
average, though t0054's actual run took 4 h 19 min for the same 1,440-trial budget, so wall-clock
can be up to 5 hours. No GPU, no remote provisioning, no `available_services` consumed.

## Assets Needed

* `dsgc-baseline-morphology-calibrated` from `t0009_calibrate_dendritic_diameters`. Read directly
  from
  `tasks/t0009_calibrate_dendritic_diameters/assets/dataset/dsgc-baseline-morphology-calibrated/files/141009_Pair1DSGC_calibrated.CNG.swc`.
* Library `tuning_curve_viz` from `t0011_response_visualization_library`. Imported as
  `from tasks.t0011_response_visualization_library.code.tuning_curve_viz import plot_polar_tuning_curve, plot_cartesian_tuning_curve`.
* Library `tuning_curve_loss` from `t0012_tuning_curve_scoring_loss_library`. Imported as
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import load_tuning_curve, compute_dsi, compute_peak_hz, compute_null_hz, compute_hwhm_deg, compute_reliability`.
* Reference MOD file for provenance only:
  `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/sources/bipolarNMDA.mod`
  (lines 47-54 and 108-109 are the Mg-block formula and parameter values).
* `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/code/*` — copied verbatim or extended (13
  files).
* `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/tuning_curve_full.csv` — read by the
  `gNMDA = 0` cross-task regression gate in `compute_metrics.py`.
* `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/placement_seed0.json` — read by
  `test_placement_seed0_match.py`.
* `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/derived_quantities.json` — read by
  `render_figures.py` for the t0054 overlay curves on the three sweep-summary plots.
* NEURON 8.2.7 install at `C:\Users\md1avn\nrn-8.2.7` (toolchain established in t0007; imported via
  `code/neuron_bootstrap.py`; `nrnivmodl.bat` invoked from `code/run_nrnivmodl.cmd`).
* Optional: `tasks/t0004_generate_target_tuning_curve/results/target_tuning_curve.csv` for
  `tuning_curve_rmse` computation; if absent the metric is omitted with a note (same policy as
  t0054).

## Expected Assets

This task produces exactly one library asset, matching `task.json`
`expected_assets = {"library": 1}`:

* `library/minimal_dsgc_mg_block_nmda` — the cell builder, SWC loader, synapse placer, AMPA +
  Mg-block NMDA + GABA position-gated event drivers, scalar-gabaMOD scaling helper, three-mode trial
  runner (FULL / E_ONLY / GABA_ONLY) with `gnmda_ns` parameter, 12-direction × 4-`gNMDA` sweep
  harness, renderer suite (per-direction × per-`gNMDA` panels and four sweep-summary plots
  including the new Mg-block g(v) sanity curve), 12-variant metrics computer with the `gNMDA = 0`
  regression hard-fail gate against t0054, and the new `NMDA_MgBlock.mod` point process. Code lives
  under `tasks/t0055_nmda_mg_block_dsi_recovery/code/`; the asset folder contains `details.json`,
  `description.md`, and `sources/NMDA_MgBlock.mod` (canonical MOD artefact).

No other asset types (paper, dataset, model, predictions, answer) are produced.

## Time Estimation

* Research (already done): code research is complete (~3 hours). No remaining research time.
* Milestone 1 (verbatim copies, 6 files): ~30 min.
* Milestone 2 (NMDA_MgBlock.mod authoring + nrnivmodl.cmd): ~2 hours including MOD debugging.
* Milestone 3 (constants.py + paths.py + neuron_bootstrap.py extension): ~1 hour.
* Milestone 4 (synapses.py NMDA substitution + trial.py copy): ~1 hour.
* Milestone 5 (4 validation gates: quiescent, placement, NMDA voltage-dep, dry-run): ~2 hours
  (includes authoring `test_nmda_mg_block_voltage_dep.py` and saving the empirical g(v) data).
* Milestone 6 (sweep harness adaptation + full 1,440-trial sweep): ~1 hour coding + ~75 min
  simulation in the optimistic case, up to 5 h in the pessimistic case = ~1-6 hours.
* Milestone 7 (render_figures.py with t0054 overlays + Mg-block g(v) sanity plot): ~2 hours.
* Milestone 8 (compute_metrics.py extension with pass-criterion evaluation): ~1 hour.
* Milestone 9 (library asset metadata + description.md): ~1 hour.
* Verification, fixing verificator errors: ~1 hour.
* **Total implementation wall-clock: ~12-17 hours**, comparable to t0054. Of this, ~75 min to ~5 h
  is NEURON simulation wall-clock — the rest is coding, debugging, and verification.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Simulation wall-clock exceeds 6 hours (t0054's actual run was 4h19min, well above the 75-min target) | Medium | Soft — delays delivery, not invalidates results | If wall-clock projection at t = 1 hour into the sweep exceeds 6 h, ABORT the sweep, write an intervention file under `intervention/` describing the situation and projected wall-clock, and create a parallelisation-task suggestion (S-0054-06 covers exactly this). Do NOT silently reduce trial count or trial modes. Fallbacks (in priority order): (a) accept ~5 h wall-clock as in t0054; (b) abort and create the parallelisation task; (c) if intermediate, run the sweep overnight. |
| `NMDA_MgBlock.mod` fails to compile under `nrnivmodl` (syntax error, NEURON kernel API mismatch) | Medium | Critical — entire pipeline blocked | Step 5 invokes `nrnivmodl` and asserts `nrnmech.dll` exists. If compilation fails, inspect `nrnivmodl` stderr; common causes are missing `BREAKPOINT` block, undeclared RANGE variable, or tau/state mismatches. Compare against the t0046 `bipolarNMDA.mod` line by line. Fix and re-run; the build is idempotent. |
| `NMDA_MgBlock` mechanism not registered with NEURON (`hasattr(h, 'NMDA_MgBlock') == False`) | Low | Critical | Step 8's `ensure_nmda_mg_block_compiled` calls `h.nrn_load_dll(str(NRNMECH_DLL))` AFTER `load_stdrun`. If the import-time check fails, verify `NRNMECH_DLL.exists()`, verify the DLL was loaded BEFORE any code touches `h.NMDA_MgBlock`, and verify the MOD's `NEURON { POINT_PROCESS NMDA_MgBlock ... }` declaration. Fallback: if the Windows MinGW toolchain is broken, file an intervention. |
| `gNMDA = 0` cross-task regression gate fails — t0055 FULL rates differ from t0054 at zero conductance | Medium | Critical — entire experiment is invalid | Step 16 hard-fails before writing `metrics.json`. Inspection: verify NMDA `NetCon` weight is exactly `0.0` at scheduling time and after every trial; verify placement-match test (Step 12) passed; verify per-trial seed formula matches t0054 (`1000 * angle_idx + trial_idx + 1`); verify the `NetStim` is shared between AMPA and NMDA `NetCon`s. The most likely failure is that the MOD's `NET_RECEIVE` event handling differs subtly from `Exp2Syn` event handling — if so, fix the MOD's `A = A + weight; B = B + weight` lines to match `Exp2Syn.mod`. |
| Placement seed drift — t0055 sample differs from t0054 by even one location | Low | Critical — biases every result | Step 12 placement-match test runs before any synapse code. If it fails, dump the differing pair indices and verify `numpy.random.default_rng(0)` is the only RNG touched before `sample_dendritic_locations` is called. |
| NMDA voltage-dependence sanity gate fails (non-monotonic, or wrong ratio at -80/-20 mV) | Low | Critical — MOD is wrong | Step 13 hard-fails before the full sweep. Inspection: dump the six `(v_clamp, peak_g)` pairs; if peak_g is constant across voltages, the Boltzmann factor isn't being applied in the BREAKPOINT; if peak_g is anti-correlated with voltage, the `local_v` sign is wrong; if the ratio is off by an order of magnitude, the parameter values are wrong. |
| NMDA `NetCon` weight leaks across modes (e.g., after `GABA_ONLY` zeroes both AMPA and NMDA, the next FULL trial sees zero weights) | Low | Critical — silent data corruption | Inherited from t0054: the trial.py weight-restore block sets `pair.nmda_netcon.weight[0] = gnmda_ns * 1e-3` symmetrically. The dry-run gate in Step 14 catches this if it occurs. |
| Mg block recovers DSI but only at high gNMDA — DSI at 0.25 nS still below 0.50 (FAIL) | Medium | Soft — informative finding, not a bug | The pass criterion is explicitly evaluated and PASS/FAIL reported. A FAIL outcome is still a valid scientific result and informs the next step (e.g., suggesting that scalar gabaMOD is fundamentally insufficient even with Mg-block NMDA, motivating S-0053 spatial gabaMOD). Document the outcome plainly in the headline summary; do not retroactively adjust the criterion. |
| Driving-force saturation at high `gNMDA` (local Vm approaches `E_NMDA = 0 mV` when 100 NMDA synapses fire near-synchronously) | Medium | Soft — interesting finding | The Mg-block now suppresses NMDA at hyperpolarised voltages, partially offsetting saturation. Document in `results_detailed.md` (orchestrator-managed); the sweep-summary plots will show whether the curves remain monotonic. |
| EPSP-decay-tau-vs-gNMDA plot has all-null y-axis (t0054 inherited limitation: 1500 ms window too short for `tau2 = 80 ms` decay-to-1/e) | High | Soft — known limitation | The plot is rendered with explicit "no data" annotations for null values. Suggestion S-0054-03 covers an improved EPSP-decay metric and is out of scope here. |
| NEURON Windows bootstrap fails (env var, DLL path, version mismatch, or `nrnivmodl.bat` not found) | Low | Blocking | Reuse the t0054 bootstrap pattern (battle-tested across 6+ tasks); for the new MOD-build path, verify `C:\Users\md1avn\nrn-8.2.7\bin\nrnivmodl.bat` exists; if `ensure_neuron_importable()` raises, file an intervention noting expected vs actual NEURONHOME. |
| `tuning_curve_loss` or `tuning_curve_viz` API has changed since t0054 | Low | Soft | Imports use the registered library paths; if any function signature changed, the call will raise immediately, the implementation patches the call site, and re-runs Steps 15 / 16. |

## Verification Criteria

* **Plan verificator passes.** Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0055_nmda_mg_block_dsi_recovery -- uv run python -m arf.scripts.verificators.verify_plan t0055_nmda_mg_block_dsi_recovery`
  and confirm `errors: 0`.

* **Library asset validates.** Run
  `uv run python -u -m meta.asset_types.library.verificator tasks/t0055_nmda_mg_block_dsi_recovery/assets/library/minimal_dsgc_mg_block_nmda`
  and confirm zero errors. Confirms REQ-17.

* **MOD compilation succeeds.** Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0055_nmda_mg_block_dsi_recovery -- python tasks/t0055_nmda_mg_block_dsi_recovery/code/run_nrnivmodl.cmd`
  (or invoke `code/run_nrnivmodl.cmd` directly via the Windows shell) and confirm
  `tasks/t0055_nmda_mg_block_dsi_recovery/code/mod/nrnmech.dll` exists. Confirms REQ-2.

* **NMDA_MgBlock mechanism is registered.** Run
  `python -c "from tasks.t0055_nmda_mg_block_dsi_recovery.code import neuron_bootstrap; neuron_bootstrap.ensure_neuron_importable(); from neuron import h; assert hasattr(h, 'NMDA_MgBlock'); print('NMDA_MgBlock OK')"`
  and confirm `NMDA_MgBlock OK` is printed. Confirms REQ-1, REQ-2.

* **Quiescent-rest gate passes.** Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0055_nmda_mg_block_dsi_recovery -- uv run pytest tasks/t0055_nmda_mg_block_dsi_recovery/code/test_quiescent_rest.py -v`
  and confirm `1 passed`. Confirms REQ-5.

* **Placement bit-identical to t0054.** Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0055_nmda_mg_block_dsi_recovery -- uv run pytest tasks/t0055_nmda_mg_block_dsi_recovery/code/test_placement_seed0_match.py -v`
  and confirm `1 passed`. Confirms REQ-6.

* **NMDA voltage-dependence sanity gate passes.** Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0055_nmda_mg_block_dsi_recovery -- uv run pytest tasks/t0055_nmda_mg_block_dsi_recovery/code/test_nmda_mg_block_voltage_dep.py -v`
  and confirm `1 passed` and that
  `tasks/t0055_nmda_mg_block_dsi_recovery/results/mg_block_g_v_empirical.json` exists with six
  `(v_clamp_mv, peak_g)` entries. Confirms REQ-8.

* **All three sweep CSVs exist with 480 rows each (4 `gNMDA` × 12 angles × 10 trials).** Run
  `python -c "import pandas as pd; [print(p, len(pd.read_csv(p))) for p in ['tasks/t0055_nmda_mg_block_dsi_recovery/results/tuning_curve_full.csv', 'tasks/t0055_nmda_mg_block_dsi_recovery/results/tuning_curve_e_only.csv', 'tasks/t0055_nmda_mg_block_dsi_recovery/results/tuning_curve_gaba_only.csv']]"`
  and confirm 480 in every file. Confirms REQ-9, REQ-10, REQ-11, REQ-12, REQ-13.

* **All four `gNMDA` values appear in every per-mode CSV.** Run
  `python -c "import pandas as pd; print(sorted(pd.read_csv('tasks/t0055_nmda_mg_block_dsi_recovery/results/tuning_curve_full.csv')['gnmda_ns'].unique()))"`
  and confirm `[0.0, 0.25, 0.5, 1.0]`. Confirms REQ-12.

* **`gNMDA = 0` cross-task regression gate passes vs t0054.** Run
  `python -c "import pandas as pd, numpy as np; a = pd.read_csv('tasks/t0055_nmda_mg_block_dsi_recovery/results/tuning_curve_full.csv'); a = a[a['gnmda_ns']==0.0].sort_values(['angle_deg','trial_seed'])['firing_rate_hz'].to_numpy(); b = pd.read_csv('tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/tuning_curve_full.csv'); b = b[b['gnmda_ns']==0.0].sort_values(['angle_deg','trial_seed'])['firing_rate_hz'].to_numpy(); assert np.allclose(a, b, atol=1e-6), 'gnmda=0 cross-task regression FAIL'; print('gnmda=0 cross-task regression OK')"`
  and confirm `gnmda=0 cross-task regression OK`. Confirms REQ-7.

* **All 240 per-direction PNGs and 4 sweep-summary PNGs exist.** Run
  `python -c "from pathlib import Path; d = Path('tasks/t0055_nmda_mg_block_dsi_recovery/results/images'); print('per-dir', sum(1 for _ in d.glob('*_gnmda_*_dir_*.png'))); print('sweep', sum(1 for n in ['epsp_decay_vs_gnmda.png','peak_hz_vs_gnmda.png','dsi_vs_gnmda.png','mg_block_g_v_curve.png'] if (d / n).exists()))"`
  and confirm `per-dir 240` and `sweep 4`. Confirms REQ-15, REQ-16.

* **`metrics.json` has 12 variants in explicit multi-variant format with registered keys.** Run
  `python -c "import json; m = json.load(open('tasks/t0055_nmda_mg_block_dsi_recovery/results/metrics.json')); v = m['variants']; assert len(v) == 12, len(v); ids = sorted(x['variant_id'] for x in v); assert all(k in v[0]['metrics'] for k in ['direction_selectivity_index','tuning_curve_hwhm_deg','tuning_curve_reliability']); print(ids)"`
  and confirm 12 variants with the `gnmda_<value>_<mode>` schema. Confirms REQ-14.

* **Pass-criterion evaluation is recorded.** Run
  `python -c "import json; d = json.load(open('tasks/t0055_nmda_mg_block_dsi_recovery/results/derived_quantities.json')); assert 'pass_criterion_dsi_at_gnmda_025' in d; assert 'pass_criterion_peak_hz_at_gnmda_025' in d; assert 'pass_criterion_overall' in d; print(f'PASS_overall={d[\"pass_criterion_overall\"]} dsi_pass={d[\"pass_criterion_dsi_at_gnmda_025\"]} hz_pass={d[\"pass_criterion_peak_hz_at_gnmda_025\"]}')"`
  and confirm three booleans are present. Confirms REQ-18.

* **All `REQ-*` items map to at least one Step by Step item.** Run
  `python -c "import re; t = open('tasks/t0055_nmda_mg_block_dsi_recovery/plan/plan.md').read(); reqs = sorted({m for m in re.findall(r'REQ-\d+', t)}, key=lambda s: int(s[4:])); print(reqs); assert reqs == [f'REQ-{i}' for i in range(1, 21)], reqs"`
  and confirm `REQ-1` through `REQ-20` are all present in the plan body. Confirms requirement
  coverage.

* **Cost gate.** Confirm `results/costs.json` is `{}` (no paid services). Run
  `python -c "import json; assert json.load(open('tasks/t0055_nmda_mg_block_dsi_recovery/results/costs.json')) == {}; print('zero cost confirmed')"`.
  Confirms REQ-20.
