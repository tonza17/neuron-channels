---
spec_version: "2"
task_id: "t0036_rerun_t0030_halved_null_gaba"
date_completed: "2026-04-22"
status: "complete"
---
# Plan: Rerun Distal-Diameter Sweep on t0022 DSGC with Halved Null-GABA

## Objective

Rerun the t0030 distal-dendrite **diameter** sweep on the already-completed t0022 DSGC channel
testbed (library `modeldb_189347_dsgc_dendritic`) with **one schedule change**: reduce
`GABA_CONDUCTANCE_NULL_NS` from its default **12.0 nS** to **6.0 nS** (halved). The sweep uses seven
distal-diameter multipliers — **0.5×, 0.75×, 1.0×, 1.25×, 1.5×, 1.75×, 2.0×** — applied
uniformly to every distal branch (operationally: HOC leaves on the `h.RGC.ON` arbor with topological
depth ≥ 3 from soma). At each multiplier, execute the canonical t0022 protocol of 12 moving-bar
directions (30° spacing) × 10 trials per direction (120 trials per sweep point, **840 trials
total**). DSI is computed via the t0012 `tuning_curve_loss` scorer. t0030 produced a **null
mechanism-discrimination result** because primary peak-minus-null DSI was pinned at exactly 1.000
across every multiplier — null-direction firing was 0 Hz under the 12 nS GABA shunt. Schachter2010
reports ~6 nS compound null inhibition, so halving the conductance should leave enough residual
excitation for occasional null-direction spikes, unpin primary DSI, and restore a measurable slope
signal. The research question is mechanism discrimination: **positive** DSI-vs-diameter slope →
**Schachter2010 active-dendrite amplification**; **negative** slope → **passive filtering**;
**flat** → mechanism ambiguous. Success means producing (a) a tidy sweep CSV with 840 trial rows,
(b) seven per-diameter canonical 120-row tuning-curve CSVs, (c) `results/metrics.json` in explicit
multi-variant format with one DSI value per diameter, (d) four diagnostic charts including a new
`null_hz_vs_diameter.png` that confirms the schedule fix desaturated null firing, (e) a mechanism
classification label, and (f) a pre-condition-gated interpretation that is flagged **partial** if
mean null-Hz at the 1.0× baseline remains below 0.1 Hz. All work runs locally on CPU with $0
external cost. Expected runtime ~2 h end-to-end.

## Task Requirement Checklist

Operative task text from `tasks/t0036_rerun_t0030_halved_null_gaba/task_description.md`:

> 1. Use the t0022 DSGC testbed as-is (channel set, morphology, AIS partition, 12-direction
>    protocol, 10 trials per angle) — EXCEPT: set `GABA_CONDUCTANCE_NULL_NS = 6.0 nS` (half of the
>    default 12 nS). Preferred-direction GABA stays at its default.
> 2. Identify distal dendritic sections via t0030's selection rule (HOC leaves on `h.RGC.ON`, branch
>    order >= 3). COPY the helper into this task's `code/`; no cross-task imports.
> 3. Sweep 7 distal-diameter multipliers (0.5x, 0.75x, 1.0x, 1.25x, 1.5x, 1.75x, 2.0x) uniformly on
>    all distal branches. Same set as t0030.
> 4. 12-direction moving-bar tuning x 10 trials per angle per diameter = 840 trials total.
> 5. Compute primary DSI (peak-minus-null) as the operative metric. Also compute vector-sum DSI and
>    standard secondary metrics.
> 6. Plot primary DSI vs diameter and classify slope sign: positive → Schachter2010; negative →
>    passive filtering; flat → ambiguous.
>
> Primary metric: primary DSI (peak-minus-null) per diameter. Critical diagnostic: null-direction
> firing rate per diameter — must be non-zero to confirm the GABA change had the intended effect.
> Secondary: vector-sum DSI, peak Hz, HWHM, reliability, preferred-direction firing, per-direction
> spike counts, distal peak mV.
>
> Key Questions: (1) Does null-direction firing become non-zero at 6 nS? (pre-condition) (2) With
> null firing unpinned, what is the primary DSI-vs-diameter slope sign? (3) Does the slope match
> Schachter2010 (positive), passive filtering (negative), or neither? (4) How does halved-GABA t0022
> compare to t0035 (same sweep on t0024)?

Requirements:

* **REQ-1**: Use the t0022 testbed as-is — no channel changes, no input rewiring, no morphology
  file edits. Only `GABA_CONDUCTANCE_NULL_NS` (runtime attribute write) and distal `seg.diam`
  (in-memory per-trial) are mutated. Satisfied by steps 2, 4, 6, 7, 8. Evidence: no HOC or MOD files
  modified; per-trial `_assert_bip_and_gabamod_baseline` guard passes; per-trial midpoint-snapshot
  assertion confirms 3D coordinates are unchanged; runtime log records effective schedule
  `GABA_CONDUCTANCE_NULL_NS = 6.0`.
* **REQ-2**: Halve `GABA_CONDUCTANCE_NULL_NS` from 12 nS to **6.0 nS** before any t0022 driver
  import; preserve `GABA_CONDUCTANCE_PREFERRED_NS = 3.0 nS` at default. The override must be
  consistent across both the assertion at `run_tuning_curve.py:327`
  (`abs(null_weight_us - GABA_CONDUCTANCE_NULL_NS * 1e-3) < 1e-9`) and the
  `gaba_null_pref_ratio = GABA_CONDUCTANCE_NULL_NS / GABA_CONDUCTANCE_PREFERRED_NS` passed into
  `schedule_ei_onsets` (must become `6.0 / 3.0 = 2.0`, not `12.0 / 3.0 = 4.0`). Satisfied by steps
  3, 4. Evidence: `code/gaba_override.py` module sets
  `_t0022_constants.GABA_CONDUCTANCE_NULL_NS = 6.0` at import; `code/trial_runner_diameter.py`
  re-binds its local name to 6.0 so the computed ratio is 2.0; a smoke assertion in preflight logs
  `GABA_CONDUCTANCE_NULL_NS = 6.0` and `gaba_null_pref_ratio = 2.0`.
* **REQ-3**: Identify distal dendritic sections at branch order ≥ 3 (HOC leaves on `h.RGC.ON` with
  topological depth ≥ 3 from soma) via a **copied** helper inside this task's `code/`. No
  cross-task non-library imports. Satisfied by steps 2, 5. Evidence:
  `code/diameter_override.py::identify_distal_sections` is a verbatim copy from
  `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/diameter_override.py`; no
  `from tasks.t0030...` import appears anywhere in this task's code;
  `logs/preflight/distal_sections.json` records `count >= 50`, `min_depth >= 3`, and
  `identification_rule = "hoc_leaves_on_arbor_depth_ge_3"`.
* **REQ-4**: Sweep exactly the seven multipliers `(0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0)` uniformly
  across every distal branch. Identical grid to t0030. Satisfied by steps 3, 7. Evidence:
  `DIAMETER_MULTIPLIERS` constant in `code/constants.py`; `results/data/sweep_results.csv` contains
  exactly 7 unique `diameter_multiplier` values.
* **REQ-5**: For each multiplier, run the canonical t0022 12-direction tuning protocol (10 trials
  per angle) and compute primary DSI (peak-minus-null) via the t0012 scorer. 840 trials total.
  Satisfied by steps 7, 9. Evidence: 840 rows in `results/data/sweep_results.csv` (7 × 12 × 10);
  seven per-diameter canonical CSVs of 120 rows each in the t0012
  `(angle_deg, trial_seed, firing_rate_hz)` schema; `results/data/dsi_by_diameter.csv` with one row
  per multiplier; `results/metrics.json` variants populated with `direction_selectivity_index`.
* **REQ-6**: Also compute vector-sum DSI and the standard secondary metrics (peak Hz, null Hz, HWHM,
  reliability, `peak_mv` per trial). Satisfied by step 9. Evidence:
  `results/data/metrics_per_diameter.csv` columns `direction_selectivity_index`, `dsi_vector_sum`,
  `peak_hz`, `null_hz`, `hwhm_deg`, `reliability`, `mean_peak_mv`; tidy CSV columns `spike_count`,
  `peak_mv`, `firing_rate_hz`.
* **REQ-7**: Plot primary DSI vs diameter and **classify slope sign** into exactly three buckets:
  `schachter2010_amplification` (positive), `passive_filtering` (negative), `flat` (ambiguous).
  Satisfied by steps 10, 11. Evidence: `results/images/dsi_vs_diameter.png` exists;
  `results/data/curve_shape.json` records `mechanism_label`, `slope`, `slope_95_ci_low`,
  `slope_95_ci_high`, `slope_p_value`, `slope_sign`.
* **REQ-8**: Emit the new **null-Hz-vs-diameter diagnostic chart**
  (`results/images/null_hz_vs_diameter.png`) — the pre-condition gate that confirms the 6 nS
  schedule change unpinned null firing. Not present in t0030. Satisfied by step 11. Evidence: PNG
  exists in `results/images/`; `results/data/curve_shape.json` records
  `precondition_null_hz_at_baseline`, `precondition_pass` (boolean), and
  `precondition_threshold_hz = 0.1`.
* **REQ-9**: Emit the vector-sum DSI chart (`results/images/vector_sum_dsi_vs_diameter.png`) and
  peak-Hz chart (`results/images/peak_hz_vs_diameter.png`) — mitigation against primary-DSI
  saturation and the Key-Question-3 diagnostic that separates "general damping" from "null-rate-only
  change". Satisfied by step 11. Evidence: both PNGs exist in `results/images/`.
* **REQ-10**: Pre-condition gate: if mean null-Hz at the 1.0× baseline multiplier is **< 0.1 Hz**
  after the 6 nS fix, flag the whole DSI-slope analysis as **partial** and recommend a further
  reduction (e.g., 4 nS). Satisfied by steps 10, 11. Evidence: `results/data/curve_shape.json` field
  `precondition_pass`; if False, `mechanism_label` is suffixed with `_partial` and a warning banner
  is emitted to stdout and to `results/data/curve_shape.json::precondition_note`.
* **REQ-11**: Local CPU only, $0 external cost, no remote compute. Satisfied by all steps. Evidence:
  no setup-machines step; no paid API calls; `project/budget.json.available_services` is empty.
* **REQ-12**: Answer Key Question 4 via comparison to t0035 (diameter sweep on t0024). Recorded as a
  `comparator_t0035` pointer in `results/data/curve_shape.json` so the compare-literature stage can
  join on the shared axis. Satisfied by step 10. Evidence: `results/data/curve_shape.json` contains
  `comparator_task_ids = ["t0030", "t0035"]` and loads their `curve_shape.json` for the slope-sign
  cross-comparison in an info-only block.

## Approach

**Task type**: `experiment-run` (set in `task.json`). The task runs a controlled computational
experiment — one independent variable (`diameter_multiplier`, 7 values), one primary dependent
variable (primary DSI per diameter), a **schedule-fixed** testbed (null-GABA = 6 nS), a
deterministic driver, and a ternary mechanism-discrimination research question. The experiment-run
Planning Guidelines require naming every independent and dependent variable, listing baselines,
using the explicit multi-variant metrics format when comparing multiple conditions, and including at
least two charts. All are applied below (four charts in total).

**Architecture** (from `research/research_code.md`): copy the entire t0030 workflow verbatim and
apply two substantive edits — one schedule override and one new diagnostic plot. The t0030 code
already solved the structural problem this task faces (iterate seg-level distal override ×
diameter-sweep grid × 12 angles × 10 trials on the t0022 testbed) and completed in ~115 min
end-to-end on this workstation. t0036 inherits that budget unchanged — halving the null-GABA
conductance is a single scalar change in `schedule_ei_onsets`; it does not alter per-trial compute
cost.

**The override strategy** (from research_code.md, "The override strategy" finding): Python's
`from ... import X` creates a new binding of `X` in the importing module's namespace.
`run_tuning_curve.py` imports `GABA_CONDUCTANCE_NULL_NS` at module load time (line 77), so a
monkey-patch applied to the **source module**
(`tasks.t0022_modify_dsgc_channel_testbed.code. constants`) **before** `run_tuning_curve` is
imported propagates the new value to every downstream consumer, including the copied trial runner.
Concretely, this task introduces a new `code/gaba_override.py` module whose sole responsibility is
to execute the two-line patch

```python
from tasks.t0022_modify_dsgc_channel_testbed.code import constants as _t0022_constants
_t0022_constants.GABA_CONDUCTANCE_NULL_NS = GABA_CONDUCTANCE_NULL_NS_OVERRIDE  # 6.0
```

at module import time. Every other module in this task's `code/` that touches the t0022 driver
imports `gaba_override` as its **first** statement (line 1 of each file), guaranteeing that the
patch runs before any
`from tasks.t0022_modify_dsgc_channel_testbed.code.run_tuning_curve import ...` line in the process.
**Critical rebind**: the copied `code/trial_runner_diameter.py` also imports
`GABA_CONDUCTANCE_NULL_NS` from the t0022 constants module into its own namespace (copied from t0030
line 42), and this **local binding must also be replaced** because it feeds into
`gaba_null_pref_ratio = GABA_CONDUCTANCE_NULL_NS / GABA_CONDUCTANCE_PREFERRED_NS`. If the local
binding stays at 12.0, the ratio is 4.0, and the assertion at `run_tuning_curve.py:327`
(`abs(null_weight_us - GABA_CONDUCTANCE_NULL_NS * 1e-3) < 1e-9`) fires:
`null_weight_us = preferred * ratio = 3 * 4 * 1e-3 = 12e-3`, but the patched
`GABA_CONDUCTANCE_NULL_NS * 1e-3 = 6e-3`. The fix is to shadow the imported name in
`trial_runner_diameter.py` with a local `GABA_CONDUCTANCE_NULL_NS: float = 6.0` constant re-read
from this task's `constants.GABA_CONDUCTANCE_NULL_NS_OVERRIDE`, keeping the single source of truth
in one place.

**Distal identification** (from research_code.md, "Distal sections are identified by HOC leaf +
ON-arbor membership"): define "distal" as HOC leaves on the ON arbor — a section `sec` is distal
iff `sec in h.RGC.ON` AND `h.SectionRef(sec=sec).nchild() == 0`. The t0030 helper
`identify_distal_sections(*, h)` already encodes this rule. Per CLAUDE.md rule 3 (no cross-task
non-library imports) this helper **must be copied verbatim** into `code/diameter_override.py`. A
preflight assertion `min_depth >= 3` (topological depth from soma) and `count >= 50` is required
before the full sweep launches — identical to t0030's validation gate, which passed with ~258
distal sections.

**Null-Hz pre-condition gate** (from research_code.md, "Null-Hz-vs-diameter is the pre-condition
diagnostic"): before interpreting any DSI slope, the t0036 analysis must first confirm that
null-direction firing is **non-zero** after the 6 nS fix. The t0030 sweep emitted null-Hz via
`compute_null_hz(curve=...)` from the t0012 library, and every row was exactly 0.0 Hz. The t0036
diagnostic PNG `results/images/null_hz_vs_diameter.png` is new (not in t0030) and its role is
pre-conditional: if any diameter's null-Hz is still 0.0, the 6 nS reduction failed to unpin null
firing and the discrimination experiment is still blocked. Pre-condition threshold: **mean null-Hz
at the 1.0× baseline multiplier ≥ 0.1 Hz**; below that, record as a partial result and suggest a
further reduction to 4 nS in the follow-up suggestion file.

**Reusable code** (imports via registered libraries — not copied):

* From `modeldb_189347_dsgc_dendritic` (t0022 library):
  `from tasks.t0022_modify_dsgc_channel_testbed.code.neuron_bootstrap import ensure_neuron_importable`.
  From `tasks.t0022_modify_dsgc_channel_testbed.code.run_tuning_curve` import: `EiPair`,
  `build_ei_pairs`, `schedule_ei_onsets`, `_preload_nrnmech_dll`, `_source_channel_partition_hoc`,
  `_silence_baseline_hoc_synapses`, `_assert_bip_and_gabamod_baseline`,
  `_count_threshold_crossings`. From `tasks.t0022_modify_dsgc_channel_testbed.code.constants`
  import: `TSTOP_MS`, `DT_MS`, `CELSIUS_DEG_C`, `N_ANGLES`, `N_TRIALS`, `ANGLE_STEP_DEG`,
  `AP_THRESHOLD_MV`, `V_INIT_MV`, `BAR_VELOCITY_UM_PER_MS`, `BAR_BASE_ONSET_MS`,
  `AMPA_CONDUCTANCE_NS`, `GABA_CONDUCTANCE_PREFERRED_NS`, `AMPA_SEG_LOCATION`, `GABA_SEG_LOCATION`.
  Do **not** import `GABA_CONDUCTANCE_NULL_NS` from the t0022 module after `gaba_override` has been
  imported; read `GABA_CONDUCTANCE_NULL_NS_OVERRIDE` from this task's `code/constants.py` instead.
* From `modeldb_189347_dsgc` (t0008 library):
  `from tasks.t0008_port_modeldb_189347.code.build_cell import build_dsgc, apply_params, read_synapse_coords, SynapseCoords`.
* From `tuning_curve_loss` (t0012 library):
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import (compute_dsi, compute_peak_hz, compute_null_hz, compute_hwhm_deg, compute_reliability, load_tuning_curve, TuningCurve, METRIC_KEY_DSI, METRIC_KEY_HWHM, METRIC_KEY_RELIABILITY)`.
* From `tuning_curve_viz` (t0011 library, optional): `plot_multi_model_overlay` for the per-diameter
  polar overlay and the Okabe-Ito palette from `tuning_curve_viz.constants.OKABE_ITO`.

**Reusable code** (copies into `code/` — structural clones only, per CLAUDE.md rule 3):

* `code/paths.py` (~50 lines) — clone of t0030's `paths.py`; add
  `NULL_HZ_VS_DIAMETER_PNG = IMAGES_DIR / "null_hz_vs_diameter.png"` and
  `PEAK_HZ_VS_DIAMETER_PNG = IMAGES_DIR / "peak_hz_vs_diameter.png"`.
* `code/constants.py` (~95 lines) — clone of t0030's `constants.py`; add two named constants:
  `GABA_CONDUCTANCE_NULL_NS_OVERRIDE: float = 6.0` (single source of truth for the override) and
  `NULL_HZ_MIN_PRECONDITION_HZ: float = 0.1` (pre-condition threshold).
* `code/gaba_override.py` (**NEW**, ~25 lines) — applies the monkey-patch. Imports
  `GABA_CONDUCTANCE_NULL_NS_OVERRIDE` from this task's `constants.py`, then writes
  `_t0022_constants.GABA_CONDUCTANCE_NULL_NS = GABA_CONDUCTANCE_NULL_NS_OVERRIDE`. Exposes a
  `GABA_CONDUCTANCE_NULL_NS: float = 6.0` module-level constant for other files that need the
  rebound local value in their namespaces. Emits a one-line module-load print:
  `[gaba_override] Patched t0022 GABA_CONDUCTANCE_NULL_NS: 12.0 -> 6.0`.
* `code/diameter_override.py` (~119 lines) — clone of t0030's `diameter_override.py` verbatim;
  rewrite the two cross-task imports (pointing at t0030 constants) to point at this task's
  `code/constants.py`.
* `code/preflight_distal.py` (~175 lines) — clone of t0030's `preflight_distal.py` with two edits:
  (i) `import tasks.t0036_rerun_t0030_halved_null_gaba.code.gaba_override # noqa: F401` on line 1;
  (ii) rewrite three cross-task imports; (iii) add a 3-angle × 2-trial × 3-diameter (multipliers
  0.5, 1.0, 2.0 = 18 trials) null-Hz sanity block that runs after the section-count preflight and
  asserts `mean_null_hz >= 0.0` (i.e., simulation didn't crash) and that `schedule_ei_onsets`
  accepted `gaba_null_pref_ratio = 2.0` without assertion failure.
* `code/trial_runner_diameter.py` (~226 lines) — clone of t0030's `trial_runner_diameter.py` with
  three edits: (i) line 1: `import tasks.t0036_rerun_t0030_halved_null_gaba.code.gaba_override
  # noqa: F401  # MUST precede t0022 run_tuning_curve import`; (ii) replace the

  `from tasks.t0022_modify_dsgc_channel_testbed.code.constants import ..., GABA_CONDUCTANCE_NULL_NS, ...`
  line with an import that omits `GABA_CONDUCTANCE_NULL_NS`, then adds
  `from tasks.t0036_rerun_t0030_halved_null_gaba.code.constants import GABA_CONDUCTANCE_NULL_NS_OVERRIDE as GABA_CONDUCTANCE_NULL_NS`
  (shadow rebind); (iii) rewrite cross-task imports to point at t0036 folder.
* `code/run_sweep.py` (~239 lines) — clone of t0030's `run_sweep.py` with line-1 `gaba_override`
  import plus cross-task rewrites. CLI flags preserved: `--preflight`, `--output`,
  `--wall-time-output`.
* `code/analyse_sweep.py` (~336 lines) — clone of t0030's `analyse_sweep.py` with cross-task
  rewrites only. Already computes `compute_null_hz` per diameter; no new metric needed.
* `code/classify_slope.py` (~314 lines) — clone of t0030's `classify_slope.py` with two edits: (i)
  cross-task rewrites; (ii) add the pre-condition gate: before writing `mechanism_label`, compute
  `precondition_null_hz_at_baseline = metrics_per_diameter[multiplier=1.0].null_hz` and
  `precondition_pass = (precondition_null_hz_at_baseline >= NULL_HZ_MIN_PRECONDITION_HZ)`. If
  `precondition_pass == False`, suffix the label with `_partial` (e.g., `flat_partial`) and add a
  `precondition_note` string to the output JSON. Emit `precondition_threshold_hz = 0.1` for
  traceability.
* `code/plot_sweep.py` (~421 lines = 396 + 25 delta) — clone of t0030's `plot_sweep.py`; add a new
  `_plot_null_hz_vs_diameter` function that renders `results/images/null_hz_vs_diameter.png`
  (single-panel Cartesian, `null_hz` vs `diameter_multiplier`, horizontal dashed line at
  `NULL_HZ_MIN_PRECONDITION_HZ = 0.1 Hz` labelled "pre-condition threshold"). The existing
  `_plot_peak_hz_vs_diameter` path already emits `peak_hz_vs_diameter.png` — confirm it fires
  unconditionally.

**Alternatives considered**:

* **Symmetric reduction (`GABA_CONDUCTANCE_NULL_NS = 3.0`)** — matching PREFERRED. Rejected: too
  aggressive for a first attempt; risks overshooting into a regime where null firing dominates and
  primary DSI collapses toward 0, obscuring both mechanism slopes. 6 nS matches Schachter2010's
  reported compound null inhibition and leaves preferred-null asymmetry intact (2:1 ratio instead of
  4:1).
* **Intermediate reduction (8 nS or 9 nS)** — more conservative. Rejected: t0030's
  `compare_literature.md` and t0029's `creative_thinking.md` both converge on 6 nS as the
  Schachter2010 biophysical reference point; 8-9 nS has no independent biological prior and risks
  still saturating the GABA shunt.
* **Rebuild the cell per sweep point** — rejected for the same reasons as t0030: wastes ~11 s on 7
  rebuilds, introduces stochastic cell-build state drift, and breaks the midpoint-snapshot guard.
* **Edit the t0022 HOC/MOD files in place** to change the null-GABA default. Rejected: violates
  CLAUDE.md rule 3 ("NEVER modify files outside the task folder"). The runtime attribute patch in
  `gaba_override.py` is a memory-only change within this task's process.
* **Use vector-sum DSI as the primary metric** — rejected for the same reason as t0030: the task
  description explicitly names primary DSI (peak-minus-null) as the operative metric. Vector-sum DSI
  is computed alongside as the secondary fallback.
* **Inject the override via a `--gaba-null-ns` CLI flag on `run_sweep.py`** — rejected: puts the
  override outside the monkey-patched import path, so on a fresh Python process the first
  `import run_tuning_curve` would still see 12.0 before the CLI argparser runs. The `gaba_override`
  module approach guarantees the patch executes at import time, before any driver import.

## Cost Estimation

Itemized estimate in USD:

* API calls (LLM / commercial): **$0.00** — no API calls.
* Remote compute (GPU / cloud): **$0.00** — all simulation runs on the local Windows workstation
  CPU.
* Local compute: **$0.00** — already-paid workstation time.
* Storage / network: **$0.00** — all outputs stay on local disk (~50 MB for CSVs + PNGs).
* Registered paid services in `project/budget.json.available_services`: empty list; nothing to spend
  on.

**Total estimated cost: $0.00**.

Project budget is $1.00 USD total, currently unspent. This task stays within budget by the full
margin; no cost cap is needed.

## Step by Step

### Milestone A: Setup, override, and preflight

1. **[CRITICAL] Create `code/paths.py` and `code/constants.py`**. Copy t0030's
   `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/paths.py` and `.../code/constants.py`
   verbatim, then add to `paths.py`:
   `NULL_HZ_VS_DIAMETER_PNG = IMAGES_DIR / "null_hz_vs_diameter.png"` and
   `PEAK_HZ_VS_DIAMETER_PNG = IMAGES_DIR / "peak_hz_vs_diameter.png"`. Add to `constants.py`:
   `GABA_CONDUCTANCE_NULL_NS_OVERRIDE: float = 6.0` and `NULL_HZ_MIN_PRECONDITION_HZ: float = 0.1`.
   Expected observable output: running
   `uv run python -u -c "from tasks.t0036_rerun_t0030_halved_null_gaba.code.constants import DIAMETER_MULTIPLIERS, GABA_CONDUCTANCE_NULL_NS_OVERRIDE, NULL_HZ_MIN_PRECONDITION_HZ; print(DIAMETER_MULTIPLIERS, GABA_CONDUCTANCE_NULL_NS_OVERRIDE, NULL_HZ_MIN_PRECONDITION_HZ)"`
   prints `(0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0) 6.0 0.1`. Satisfies REQ-4, REQ-11.

2. **[CRITICAL] Create `code/gaba_override.py`** (NEW — ~25 lines). The module body:
   ```python
   """Monkey-patch t0022 GABA_CONDUCTANCE_NULL_NS to 6.0 nS (halved from 12.0 nS).

   Import this module FIRST — before any t0022 run_tuning_curve import — in every
   file that touches the t0022 driver. The patch must run at module-import time so that
   `from tasks.t0022_modify_dsgc_channel_testbed.code.run_tuning_curve import ...` lines
   elsewhere see the reduced conductance in their module-load snapshots.
   """
   from tasks.t0022_modify_dsgc_channel_testbed.code import constants as _t0022_constants
   from tasks.t0036_rerun_t0030_halved_null_gaba.code.constants import (
       GABA_CONDUCTANCE_NULL_NS_OVERRIDE,
   )

   _PREVIOUS_VALUE_NS: float = _t0022_constants.GABA_CONDUCTANCE_NULL_NS
   _t0022_constants.GABA_CONDUCTANCE_NULL_NS = GABA_CONDUCTANCE_NULL_NS_OVERRIDE
   print(
       "[gaba_override] Patched t0022 GABA_CONDUCTANCE_NULL_NS: "
       f"{_PREVIOUS_VALUE_NS} -> {GABA_CONDUCTANCE_NULL_NS_OVERRIDE}",
       flush=True,
   )
   GABA_CONDUCTANCE_NULL_NS: float = GABA_CONDUCTANCE_NULL_NS_OVERRIDE
   ```
   Expected observable output: running
   `uv run python -u -c "import tasks.t0036_rerun_t0030_halved_null_gaba.code.gaba_override as g; print(g.GABA_CONDUCTANCE_NULL_NS)"`
   prints the patch banner plus `6.0`. Satisfies REQ-2.

3. **[CRITICAL] Create `code/diameter_override.py`** by copying
   `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/diameter_override.py` verbatim (~119
   lines). Rewrite the two imports of t0030 constants to import from this task's `code/constants.py`
   (specifically `DIAMETER_ASSERT_TOL_UM`). Do not touch `identify_distal_sections`,
   `snapshot_distal_diameters`, `set_distal_diameter_multiplier`, or `assert_distal_diameters`
   function bodies. Expected observable output: smoke test
   `uv run python -u -c "from tasks.t0036_rerun_t0030_halved_null_gaba.code.diameter_override import identify_distal_sections, snapshot_distal_diameters, set_distal_diameter_multiplier, assert_distal_diameters; print('ok')"`
   prints `ok`. Satisfies REQ-3.

4. **[CRITICAL] Create `code/trial_runner_diameter.py`** by copying
   `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/trial_runner_diameter.py` (~221 lines) and
   applying three edits:
   * **Edit 1** (line 1): insert `import tasks.t0036_rerun_t0030_halved_null_gaba.code.gaba_override
     # noqa: F401  # MUST precede any t0022 run_tuning_curve import`. This triggers the patch

     BEFORE the t0022 driver is imported in the lines below.
   * **Edit 2** (imports block, around original line 42): remove `GABA_CONDUCTANCE_NULL_NS` from the
     `from tasks.t0022_modify_dsgc_channel_testbed.code.constants import ...` line, then add
     `from tasks.t0036_rerun_t0030_halved_null_gaba.code.constants import GABA_CONDUCTANCE_NULL_NS_OVERRIDE as GABA_CONDUCTANCE_NULL_NS`.
     Local name remains `GABA_CONDUCTANCE_NULL_NS = 6.0` so the downstream
     `gaba_null_pref_ratio = GABA_CONDUCTANCE_NULL_NS / GABA_CONDUCTANCE_PREFERRED_NS` evaluates to
     `6.0 / 3.0 = 2.0`.
   * **Edit 3** (cross-task imports elsewhere in the file): rewrite any
     `from tasks.t0030_distal_dendrite_diameter_sweep_dsgc.code.<mod>` imports to point at this
     task's `code/<mod>`. Preserve the exact override sequence inside `run_one_trial_diameter`:
     `apply_params` → `_silence_baseline_hoc_synapses` → `_assert_bip_and_gabamod_baseline` →
     midpoint-snapshot assert → `set_distal_diameter_multiplier` → `assert_distal_diameters` →
     `schedule_ei_onsets` (with `gaba_null_pref_ratio=2.0`) → `h.finitialize(V_INIT_MV)` →
     `h.continuerun(TSTOP_MS)` → `_count_threshold_crossings`. Expected observable output: module
     import succeeds and prints the `[gaba_override]` banner exactly once per process. Satisfies
     REQ-1, REQ-2, REQ-5.

5. **[CRITICAL] Create `code/preflight_distal.py`** by copying
   `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/preflight_distal.py` (~175 lines). Apply
   three edits: (i) line 1: `import tasks.t0036_rerun_t0030_halved_null_gaba.code.gaba_override
   # noqa: F401`; (ii) rewrite cross-task imports; (iii) append a **null-Hz sanity block** after

   the existing section-count assertions: build the cell context, run a 3-angle × 2-trial ×
   3-diameter (multipliers 0.5, 1.0, 2.0 = 18 trials) subset via `run_one_trial_diameter`, score the
   resulting 18 rows through the canonical per-diameter CSV path, compute `compute_null_hz` and
   `compute_peak_hz` on the 1.0× subset, and **assert** (a) the 18 trials completed without raising
   `AssertionError` in `schedule_ei_onsets` (i.e., the GABA override rebind is consistent —
   satisfies REQ-2 at runtime), (b) `peak_hz >= 5` on the 1.0× preferred direction (sanity: the
   testbed still fires), (c) warn (not halt) if `null_hz == 0.0` on 1.0× — this is informational
   and the partial-result flag is decided later in classify_slope. Write the enriched result to
   `logs/preflight/distal_sections.json` with the extra keys `preflight_null_hz_1p0x`,
   `preflight_peak_hz_1p0x`, `gaba_null_pref_ratio_asserted = 2.0`,
   `gaba_conductance_null_ns_effective = 6.0`. Expected observable output:
   `logs/preflight/distal_sections.json` exists; `count >= 50`; `min_depth >= 3`;
   `gaba_conductance_null_ns_effective == 6.0`; 18 preflight trials complete without exception.
   Satisfies REQ-1, REQ-2, REQ-3.

### Milestone B: Driver implementation and full sweep

6. **Create `code/run_sweep.py`** by copying
   `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/run_sweep.py` (~239 lines). Apply two
   edits: (i) line 1: `import tasks.t0036_rerun_t0030_halved_null_gaba.code.gaba_override
   # noqa: F401`; (ii) rewrite cross-task imports. Preserve `fh.flush()` after every row (crash

   recovery). CLI flags preserved: `--preflight` (runs 3 angles × 2 trials × 3 multipliers = 18
   trials), `--output`, `--wall-time-output`. Outputs: `results/data/sweep_results.csv` (840 rows
   full run, 18 rows preflight), seven per-diameter canonical CSVs, and
   `results/data/wall_time_by_diameter.json`. Expected observable output: module imports and
   `--help` prints the CLI usage. Satisfies REQ-4, REQ-5, REQ-11.

7. **[CRITICAL] Validation gate: run `run_sweep.py --preflight`**. Execute:
   `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0036_rerun_t0030_halved_null_gaba -- uv run python -u -m tasks.t0036_rerun_t0030_halved_null_gaba.code.run_sweep --preflight`.
   Expected runtime: ~1 minute (18 trials).

   **Validation gate thresholds** (expensive-operation gate per experiment-run guidelines):

   * **Trivial baseline** to compare against: the t0030 baseline result at diameter multiplier 1.0
     with 12 nS null-GABA was DSI = 1.0 (pinned), peak Hz ~15. t0036 at 1.0× with 6 nS is
     **expected to produce** primary DSI < 1.0 (because null firing should unpin above 0 Hz) and
     peak Hz ≈ 12-18 (preferred-direction firing should stay intact — the preferred GABA is
     unchanged). The preflight at multiplier 1.0 must satisfy **peak Hz ≥ 10** — anything below
     means preferred firing is broken by the override.
   * **Pre-condition sanity** (informational, not a halt): **null Hz > 0 on at least one of the 6
     preferred+null subset trials at 1.0×**. If it is still 0.0 on every preflight trial (2 trials
     × 3 angles = 6 trials at 1.0×), warn — the 6 nS reduction may be insufficient. Do NOT halt:
     continue to the full sweep because 10 trials of the full protocol may uncover sporadic null
     spikes the subset missed.
   * **[SPECIFIC] `[gaba_override]` banner must print exactly once**: inspect stdout for the line
     `[gaba_override] Patched t0022 GABA_CONDUCTANCE_NULL_NS: 12.0 -> 6.0`. If absent, the override
     module was not imported first — STOP and fix the line-1 import in every affected file.
   * **Inspect 5 individual trial outputs** at `multiplier=1.0, angle∈{0,180}, trial∈{0,1}`:
     manually confirm that `spike_count` at the preferred direction is 5-20 (unchanged from t0030)
     and that `spike_count` at the null direction is 0-3 (up from t0030's 0). If any of the 5 trials
     yields > 25 spikes or an exception, STOP and debug the override sequencing in
     `run_one_trial_diameter`.
   * **Failure condition**: if preflight peak Hz at 1.0× < 10, STOP. Do not proceed to the full
     840-trial sweep. Debug by running `run_one_trial_diameter` on a single
     `(angle=0, trial=0, multiplier=1.0)` case and comparing the output to t0030's baseline at the
     same seed with 12 nS GABA (expected DSI ≈ 1.0 when reverting the override). Satisfies REQ-1,
     REQ-2, REQ-5.

8. **[CRITICAL] Run the full sweep**. Execute:
   `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0036_rerun_t0030_halved_null_gaba -- uv run python -u -m tasks.t0036_rerun_t0030_halved_null_gaba.code.run_sweep --output results/data/sweep_results.csv --wall-time-output results/data/wall_time_by_diameter.json`.
   Expected runtime: **~100-130 min** (840 trials, extrapolated from t0030's 6,900 s full-sweep wall
   time at identical protocol; 6 nS GABA adds no measurable compute cost). Outputs:
   `results/data/sweep_results.csv` (841 lines: 1 header + 840 data rows), seven per-diameter
   canonical CSVs at `results/data/per_diameter/tuning_curve_D<label>.csv`, and
   `results/data/wall_time_by_diameter.json`. Expected observable output: 840 `direction_deg` rows,
   7 distinct `diameter_multiplier` values, no NaN `firing_rate_hz`, and at least one row per
   diameter with `direction_deg` in the null half-plane having `spike_count >= 1`. Post-run: assert
   all baseline distal diameters are restored via
   `assert_distal_diameters(..., multiplier=1.0, tol=1e-9)`. Satisfies REQ-1, REQ-4, REQ-5.

### Milestone C: Metrics, classification, and visualisation

9. **Create `code/analyse_sweep.py`** by copying
   `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/analyse_sweep.py` (~336 lines). Rewrite
   cross-task imports only; no functional edits. For each `diameter_multiplier` group, call
   `compute_dsi(curve=load_tuning_curve(csv_path=per_diameter_csv))` on the per-diameter canonical
   CSV from step 6, plus `compute_peak_hz`, `compute_null_hz`, `compute_hwhm_deg`,
   `compute_reliability`, `_vector_sum_dsi`. Outputs:
   * `results/data/metrics_per_diameter.csv` — columns `diameter_multiplier`,
     `direction_selectivity_index`, `dsi_vector_sum`, `peak_hz`, `null_hz`, `hwhm_deg`,
     `reliability`, `mean_peak_mv`. **`null_hz` is the key new signal**: unlike t0030, it should be
     non-zero at every multiplier.
   * `results/data/dsi_by_diameter.csv` — focused 3-column table (multiplier, primary DSI,
     vector-sum DSI).
   * `results/data/metrics_notes.json` — records why `tuning_curve_rmse` is omitted.
   * `results/metrics.json` — explicit multi-variant format with 7 variants
     (`variant_id = "diameter_<m>"`, `dimensions = {"diameter_multiplier": <m>}`,
     `metrics = {"direction_selectivity_index": <dsi>, "tuning_curve_hwhm_deg": <hwhm>, "tuning_curve_reliability": <rel>}`).
     Expected observable output: `metrics.json` contains `variants` with 7 entries;
     `dsi_by_diameter.csv` has 7 data rows; `null_hz` column in `metrics_per_diameter.csv` has at
     least one non-zero row. Satisfies REQ-5, REQ-6.

10. **Create `code/classify_slope.py`** by copying
    `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/classify_slope.py` (~314 lines). Apply two
    edits: (i) rewrite cross-task imports; (ii) add a **pre-condition gate** block at the top of
    `classify()`:
    ```python
    precondition_null_hz_at_baseline: float = float(
        metrics_per_diameter.loc[
            metrics_per_diameter["diameter_multiplier"] == 1.0, "null_hz"
        ].iloc[0]
    )
    precondition_pass: bool = (
        precondition_null_hz_at_baseline >= NULL_HZ_MIN_PRECONDITION_HZ
    )
    ```
    If `precondition_pass` is False, suffix the final `mechanism_label` with `_partial` (e.g.,
    `flat_partial`) and write the warning string to a new `precondition_note` field in
    `curve_shape.json`. Also emit `comparator_task_ids = ["t0030", "t0035"]` for the
    compare-literature stage (Key Question 4). Outputs unchanged from t0030 plus the three new
    fields (`precondition_null_hz_at_baseline`, `precondition_pass`, `precondition_threshold_hz`,
    `precondition_note`, `comparator_task_ids`). Expected observable output:
    `results/data/curve_shape.json` exists with every field. Satisfies REQ-7, REQ-10, REQ-12.

11. **Create `code/plot_sweep.py`** by copying
    `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/plot_sweep.py` (~396 lines). Apply three
    edits: (i) rewrite cross-task imports; (ii) add a new `_plot_null_hz_vs_diameter` function (~25
    lines) that renders `results/images/null_hz_vs_diameter.png` — single-panel Cartesian,
    `null_hz` (y-axis, Hz) vs `diameter_multiplier` (x-axis, unitless), Okabe-Ito palette,
    horizontal dashed red line at `NULL_HZ_MIN_PRECONDITION_HZ = 0.1` labelled "pre-condition
    threshold", title "Null-direction firing rate vs distal diameter (halved null-GABA)"; (iii)
    verify the `_plot_peak_hz_vs_diameter` function already exists in t0030's `plot_sweep.py` and
    calls it unconditionally (produce `results/images/peak_hz_vs_diameter.png`). Four charts total
    are produced:
    * `results/images/dsi_vs_diameter.png` — primary DSI + peak Hz two-panel (copied, unchanged
      from t0030).
    * `results/images/vector_sum_dsi_vs_diameter.png` — single-panel vector-sum DSI (copied,
      unchanged).
    * `results/images/peak_hz_vs_diameter.png` — single-panel peak Hz (confirmed to fire).
    * `results/images/null_hz_vs_diameter.png` — **NEW pre-condition diagnostic**.
    * `results/images/polar_overlay.png` — optional overlay (cheap to produce). Expected
      observable output: all four required PNGs exist with size > 15 000 bytes. Satisfies REQ-7,
      REQ-8, REQ-9.

## Remote Machines

**None required.** The entire sweep runs on the local Windows workstation CPU. The schedule change
(null-GABA 12 nS → 6 nS) is one scalar multiplication in `schedule_ei_onsets`; it does not alter
per-trial compute cost. t0030 executed the identical 840-trial protocol in ~115 min end-to-end on
the same testbed; t0036 budgets ~2 h wall time comfortably. No GPU, no cloud, no paid API.

## Assets Needed

Input assets this task depends on:

* **`modeldb_189347_dsgc_dendritic`** — library asset from t0022. Source:
  `tasks/t0022_modify_dsgc_channel_testbed/assets/library/modeldb_189347_dsgc_dendritic/`. Provides
  the HOC model (`RGCmodel.hoc`, `dsgc_model.hoc`), compiled MOD mechanisms (`nrnmech.dll`), the
  per-dendrite E-I driver, the channel-partition HOC overlay, the canonical constants (including
  `GABA_CONDUCTANCE_NULL_NS = 12.0` as the default that this task patches to 6.0 at import time),
  the Windows NEURON bootstrap, and the per-trial baseline-drift guardrails.
* **`modeldb_189347_dsgc`** — library asset from t0008. Source:
  `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/`. Provides `build_dsgc`,
  `apply_params`, `read_synapse_coords`, `SynapseCoords`.
* **`tuning_curve_loss`** — library asset from t0012. Source:
  `tasks/t0012_tuning_curve_scoring_loss_library/assets/library/tuning_curve_loss/`. Provides the
  canonical DSI / peak / null / HWHM / reliability scorer — `compute_null_hz` is the key metric
  for the new pre-condition diagnostic.
* **`tuning_curve_viz`** — library asset from t0011 (optional). Source:
  `tasks/t0011_response_visualization_library/assets/library/tuning_curve_viz/`. Provides
  `plot_multi_model_overlay` and the Okabe-Ito palette.
* **t0030 non-library code** — `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/` files are
  used only as **copy sources** (structural templates); t0036 never imports them. t0030's
  `compare_literature.md` and `results/data/curve_shape.json` are also read downstream at the
  compare-literature stage (not during implementation).
* **t0035 results** —
  `tasks/t0035_distal_dendrite_diameter_sweep_t0024/results/data/ curve_shape.json` is consulted at
  the compare-literature stage (not during implementation) for cross-testbed comparison (Key
  Question 4).

## Expected Assets

`task.json` declares `expected_assets: {}` — no paper, dataset, library, model, predictions, or
answer assets are produced. This is a pure experiment-run task whose deliverables are metrics,
charts, and the mechanism classification under `results/`. The expected output artefacts
(non-assets) are:

* `results/data/sweep_results.csv` — 840 tidy trial rows, columns
  `(diameter_multiplier, trial, direction_deg, spike_count, peak_mv, firing_rate_hz)`.
* `results/data/per_diameter/tuning_curve_D<label>.csv` × 7 — canonical 120-row tuning-curve CSVs
  in the t0012 `(angle_deg, trial_seed, firing_rate_hz)` schema.
* `results/data/metrics_per_diameter.csv` — one row per multiplier with primary DSI, vector-sum
  DSI, peak Hz, **null Hz (non-zero — the key new signal)**, HWHM, reliability, mean peak mV.
* `results/data/dsi_by_diameter.csv` — focused DSI table.
* `results/data/curve_shape.json` — mechanism label (with `_partial` suffix if pre-condition
  fails), slope, 95 % CI, p-value, sign, fallback flag, peak-Hz trend, null-Hz trend, pre-condition
  gate fields (`precondition_null_hz_at_baseline`, `precondition_pass`,
  `precondition_threshold_hz = 0.1`, `precondition_note`), comparator pointer
  (`comparator_task_ids = ["t0030", "t0035"]`).
* `results/data/wall_time_by_diameter.json` — per-sweep-point wall time.
* `results/data/metrics_notes.json` — RMSE omission rationale.
* `results/metrics.json` — explicit multi-variant format with 7 variants.
* `results/images/dsi_vs_diameter.png` — primary two-panel chart.
* `results/images/vector_sum_dsi_vs_diameter.png` — secondary single-panel chart.
* `results/images/peak_hz_vs_diameter.png` — peak-Hz diagnostic chart.
* `results/images/null_hz_vs_diameter.png` — **NEW** pre-condition diagnostic chart.
* `results/images/polar_overlay.png` — optional polar overlay of 7 tuning curves.
* `logs/preflight/distal_sections.json` — distal identification rule + counts + preflight-null-Hz
  sanity fields + effective GABA schedule.

## Time Estimation

* Research: already complete (research_code.md synthesised 10 prior tasks incl. t0022, t0030,
  t0035). **0 h**.
* Planning: this document. **~1 h**.
* Implementation (milestones A + B + C, steps 1-11):
  * Milestone A (steps 1-5, setup + gaba_override + preflight): **~45 min coding + ~5 min preflight
    runtime**.
  * Milestone B step 6 (sweep-driver clone): **~20 min coding**.
  * Milestone B step 7 (preflight sweep run + inspection): **~1 min runtime + ~10 min triage**.
  * Milestone B step 8 (full sweep run): **~100-130 min runtime** (unattended).
  * Milestone C steps 9-11 (metrics + classifier + charts): **~1 h coding + <1 min runtime**.
* Validation and coverage check: **~30 min**.

**Total implementation wall time: ~4-5 h** (most of which is unattended simulation time).

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| **GABA override rebind miss** — if the local `GABA_CONDUCTANCE_NULL_NS` binding inside `trial_runner_diameter.py` is not replaced with 6.0, the `gaba_null_pref_ratio` computed at the call site stays at `12.0 / 3.0 = 4.0`, and the assertion at `run_tuning_curve.py:327` (`abs(null_weight_us - GABA_CONDUCTANCE_NULL_NS * 1e-3) < 1e-9`) fires on the first trial because `null_weight_us = 12e-3` but the patched `GABA_CONDUCTANCE_NULL_NS * 1e-3 = 6e-3`. | Medium | High | The preflight in step 5 runs 18 real trials through `run_one_trial_diameter` and will surface this mismatch immediately as an `AssertionError` from `schedule_ei_onsets`. Mitigation: Step 4 edit-2 explicitly rebinds the local name. Validation gate in step 7 verifies the `[gaba_override]` banner prints exactly once and no assertion fires in preflight. If the assertion fires at step 7, halt — do not proceed to the full sweep. |
| **Still-pinned primary DSI** — null firing could stay at 0 Hz even with 6 nS if the per-trial E-I schedule is too rigid (e.g., the 10 ms head-start of GABA before AMPA is still enough to veto every spike). | Medium | Medium | The new `null_hz_vs_diameter.png` chart and the `precondition_pass` flag in `curve_shape.json` both surface this failure mode. If `mean_null_hz at 1.0× < 0.1 Hz`, step 10 suffixes `mechanism_label` with `_partial` and a follow-up suggestion is emitted pointing to a further reduction (4 nS). The task result is still informative — it tightens the bound on how far null-GABA must drop to unpin DSI. Does not block task completion. |
| **t0022 channel partitioning assumption breaks** under 6 nS — e.g., if the reduced inhibition lets preferred-direction activity leak into the null half-plane via lateral spread. | Low | Medium | The per-trial `_assert_bip_and_gabamod_baseline` guard remains enabled (unchanged from t0030). If baseline BIP synapse weights or `h.gabaMOD` drift during the sweep, the guard raises and the full sweep halts. The sweep driver writes every row with `fh.flush()`, so partial results are preserved for a restart. |
| **NEURON crash or Windows-specific DLL issue during the ~2 h unattended run.** | Low | High | Crash-recovery pattern: tidy CSV written row-by-row with `fh.flush()` (step 6). On restart, the sweep can resume from the last completed `(diameter_multiplier, trial, direction_deg)` tuple. Acceptance: at least 836/840 trials (99.5 %) must succeed; if fewer, halt and debug. |
| **Baseline distal `seg.diam` not restored after the sweep** — would corrupt any downstream use of the live cell handle. | Low | Medium | Post-sweep assertion in step 8 calls `assert_distal_diameters(..., multiplier=1.0, tol=1e-9)`; failure raises `AssertionError`. The t0022 per-trial `_assert_bip_and_gabamod_baseline` guard is an independent safety net. |
| **Diameter override perturbs 3D midpoint coordinates**, breaking bar-arrival-time schedule. | Very Low | High | NEURON does not mutate 3D points when `seg.diam` is assigned. Step 4 keeps t0030's per-trial midpoint-snapshot assertion (`pair.x_mid_um`, `pair.y_mid_um` compared to build-time snapshot within 1e-9 µm) that fires if this invariant is ever violated. |
| **Import-order bug**: if any module in this task's `code/` imports `gaba_override` after already importing a t0022 driver module, the patch silently no-ops on that driver's cached bindings. | Medium | High | Step 2 documents the line-1 import requirement. Step 7 validation gate checks the `[gaba_override]` banner prints **exactly once** per process. If it prints more than once, one file has a duplicate import; if it prints zero times, one file is missing the line-1 import and must be fixed before proceeding. The one-scalar runtime assertion in `run_tuning_curve.py:327` is an independent safety net that catches any binding drift. |

## Verification Criteria

Testable checks run at the end of implementation (all commands use the Windows worktree prefix
`cd "C:/Users/md1avn/Documents/GitHub/neuron-channels-worktrees/t0036_rerun_t0030_halved_null_gaba" &&`
and `PYTHONIOENCODING=utf-8 PYTHONUTF8=1` where required for aggregators/verificators):

* Run
  `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0036_rerun_t0030_halved_null_gaba -- uv run python -u -m arf.scripts.verificators.verify_plan t0036_rerun_t0030_halved_null_gaba`;
  expect **zero errors**.
* Run
  `uv run python -u -c "import csv; rows = list(csv.DictReader(open( 'tasks/t0036_rerun_t0030_halved_null_gaba/results/data/sweep_results.csv'))); assert len(rows) == 840, len(rows); assert len({r['diameter_multiplier'] for r in rows}) == 7; print('OK', len(rows))"`;
  expect `OK 840` (confirms REQ-4 and REQ-5).
* Run
  `uv run python -u -c "import json, pathlib; m = json.loads(pathlib.Path( 'tasks/t0036_rerun_t0030_halved_null_gaba/results/metrics.json').read_text()); assert 'variants' in m and len(m['variants']) == 7; assert all('direction_selectivity_index' in v['metrics'] for v in m['variants']); print('OK')"`;
  expect `OK` (confirms REQ-5 and REQ-6 — DSI present for all 7 variants).
* Run
  `uv run python -u -c "import pathlib; p = pathlib.Path( 'tasks/t0036_rerun_t0030_halved_null_gaba/results/images/dsi_vs_diameter.png'); assert p.exists() and p.stat().st_size > 15000; print('OK', p.stat().st_size)"`;
  expect `OK <size>` > 15 000 bytes (confirms REQ-7).
* Run
  `uv run python -u -c "import pathlib; p = pathlib.Path( 'tasks/t0036_rerun_t0030_halved_null_gaba/results/images/null_hz_vs_diameter.png'); assert p.exists() and p.stat().st_size > 15000; print('OK', p.stat().st_size)"`;
  expect `OK <size>` > 15 000 bytes (confirms REQ-8 — the new pre-condition diagnostic chart).
* Run
  `uv run python -u -c "import pathlib; p = pathlib.Path( 'tasks/t0036_rerun_t0030_halved_null_gaba/results/images/vector_sum_dsi_vs_diameter.png'); assert p.exists() and p.stat().st_size > 15000; p2 = pathlib.Path( 'tasks/t0036_rerun_t0030_halved_null_gaba/results/images/peak_hz_vs_diameter.png'); assert p2.exists() and p2.stat().st_size > 15000; print('OK')"`;
  expect `OK` (confirms REQ-9 — both secondary charts present).
* Run
  `uv run python -u -c "import json, pathlib; s = json.loads(pathlib.Path( 'tasks/t0036_rerun_t0030_halved_null_gaba/results/data/curve_shape.json').read_text()); assert s['mechanism_label'].rstrip('_partial') in ('schachter2010_amplification','passive_filtering', 'flat'); assert 'precondition_pass' in s; assert 'precondition_null_hz_at_baseline' in s; print('OK', s['mechanism_label'], s['precondition_pass'])"`;
  expect `OK <label> <bool>` (confirms REQ-7 and REQ-10 — classification plus pre-condition gate).
* Run
  `uv run python -u -c "import json, pathlib; p = json.loads(pathlib.Path( 'tasks/t0036_rerun_t0030_halved_null_gaba/logs/preflight/distal_sections.json').read_text()); assert p['min_depth'] >= 3 and p['count'] >= 50; assert abs(p[ 'gaba_conductance_null_ns_effective'] - 6.0) < 1e-9; print('OK', p['count'], p['gaba_conductance_null_ns_effective'])"`;
  expect `OK <count> 6.0` (confirms REQ-2 and REQ-3 — effective GABA schedule and distal
  identification).
* Run
  `uv run python -u -c "import pandas as pd; df = pd.read_csv( 'tasks/t0036_rerun_t0030_halved_null_gaba/results/data/metrics_per_diameter.csv'); assert len(df) == 7; assert 'null_hz' in df.columns; print('OK null_hz range:', df['null_hz'].min(), df['null_hz'].max())"`;
  expect `OK null_hz range: <min> <max>` — informational; the pre-condition gate in
  `curve_shape.json` interprets whether the range crosses 0.1 Hz.
* Run
  `uv run ruff check --fix . && uv run ruff format . && uv run mypy tasks/t0036_rerun_t0030_halved_null_gaba`;
  expect zero errors.
* REQ-coverage check: every `REQ-*` ID in `## Task Requirement Checklist` appears in at least one
  numbered step. Run
  `uv run python -u -c "import re, pathlib; t = pathlib.Path( 'tasks/t0036_rerun_t0030_halved_null_gaba/plan/plan.md').read_text(); reqs = set(re.findall( r'REQ-\d+', t)); print(sorted(reqs))"`;
  expect at least
  `['REQ-1','REQ-2','REQ-3','REQ-4','REQ-5','REQ-6','REQ-7','REQ-8','REQ-9','REQ-10','REQ-11', 'REQ-12']`.
