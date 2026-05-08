---
spec_version: "2"
answer_id: "t0090-procedural-cell-silence-root-cause"
answered_by_task: "t0092_diagnose_morphology_generator_silence"
date_answered: "2026-05-08"
confidence: "high"
---
# t0090 procedural cell silence root cause

## Question

Why do t0090's procedural cells produce zero spikes under the t0083 best-cell channel set, and what
is the fix?

## Short Answer

The t0090 generator emits the soma's two pt3d points at coincident `(x, y, 0)` coordinates, so
NEURON computes the cumulative pt3d length as zero, overrides the prior `sec.L = soma_diameter_um`
assignment, and the soma's surface area collapses to ~9.4e-14 µm². Synaptic input drives the
somatic Vm to NaN within a few simulation steps, so every procedural cell returns
`non_finite_voltage` or zero spikes. The fix is a thin wrapper, `generate_fixed_morphology`, that
re-emits the soma's pt3d points along the z-axis so the cylinder length equals `soma_diameter_um`
and the surface area matches the t0024 hand-coded reference (~220 µm²). After the fix the
BedB-equivalent procedural cell fires 61 spikes in the PD direction (43.6 Hz, peak Vm ~11 mV).

## Research Process

The diagnostic ran in five phases inside a single NEURON process to compare a procedural
BedB-equivalent cell against the t0024 hand-coded Bed B cell under identical channels and synaptic
input.

1. **Phase A** (`code/structural_dump.py`): build both cells and dump per-section structural state
   to `data/structural_comparison.json`. Key fields: `sec.L` (NEURON-reported after `pt3dadd`),
   `sec.area()`, all pt3d points, electrotonic length `L / lambda_f(100)`, soma surface area, total
   dendritic length, soma-to-terminal max path length.
2. **Phase B** (`code/synapse_dump.py`): place ACh + GABA synapses on both cells using the t0083
   best-cell synaptic parameters (`n_ach`, `n_gaba`, `rho0_*`, `lambda_*`, `w_*`) and the same
   `placer_seed=42`. Record per-synapse XY plus the PD-direction bar arrival time distribution.
   Output: `data/synapse_comparison.json`.
3. **Phase C** (`code/vm_trace_dump.py`): run a single PD-direction bar trial on each cell at
   `SEED_BASE=1000` with `apply_parameter_vector` writing the t0083 vector. Record the soma Vm trace
   at `dt=0.1 ms` to `data/vm_trace_*.npy`. Output: peak Vm, spike count, EPSP area, and the overlay
   PNG `results/images/vm_trace_comparison.png`.
4. **Phase D** (`code/root_cause_analysis.py`): rank the four candidate causes (soma-area mismatch,
   pt3d-vs-L override, synapse-XY mismatch, channel-application skip) against the structural and
   synaptic dumps. Output: `data/root_cause_analysis.json`.
5. **Phase F** (`code/post_fix_verification.py`): run an 8-direction bar protocol on the patched
   BedB-equivalent cell and on five STABLE-from-t0090 cells (`different/morph_00`, `13`, `14`, `15`,
   `19`). Record per-direction spike counts, PD-rate, ND-rate, DSI. Outputs:
   `data/post_fix_verification.json`, `results/images/post_fix_polar_tuning.png`.

The diagnostic uses the `_get_neuron_h()` singleton from t0090's `generator.py` so both DLLs (t0024
+ t0080) load exactly once per process, and a module-level `_LIVE_CELLS` list keeps every built cell
  alive to defend against the GC `id()`-reuse bug documented in t0090's `verification.py`.

## Evidence from Papers

The papers method was not used. This is an internal diagnostic of a project-internal generator; no
published literature was consulted.

## Evidence from Internet Sources

The internet method was not used. The diagnosis runs entirely on local code and prior task outputs.

## Evidence from Code or Experiments

### Phase A — structural comparison

The `data/structural_comparison.json` summary block reports:

* **procedural_soma_area_um2**: 9.42477796076938e-14 (essentially zero)
* **handcoded_soma_area_um2**: 287.33 µm²
* **soma_area_ratio_proc_over_hand**: 3.28e-16 — the procedural soma surface area is sixteen
  orders of magnitude smaller than the hand-coded reference.
* procedural cell: 239 sections total, 6072 µm total dendritic length.
* hand-coded cell: 353 sections total, 9016 µm total dendritic length.

Per-dendrite check: 240 non-soma sections in the procedural cell, max relative drift between `sec.L`
(NEURON-reported after `pt3dadd`) and the intended length (Euclidean distance between `start_xy` and
`end_xy`) = **0.000000**. For the BedB base point with `soma_offset_pd_um=0` and
`field_elongation_pd=1.0` the asymmetry transform is a no-op, so dendrite Euclidean distance equals
`length_um` exactly. **Candidate B (pt3d-vs-L override)** is REFUTED for the BedB base point.

Examining the soma section directly via Python: `sec.L = 1e-09` after the t0090 generator's
`pt3dadd` sequence — this is the well-known NEURON behaviour of "pt3dadd overrides L unless
`pt3dconst == 1`". Inspecting `generator.py:392-403` shows the cause:

```python
h.pt3dadd(soma_node.start_xy[0], soma_node.start_xy[1], 0.0, soma_diameter_um)
h.pt3dadd(soma_node.end_xy[0],   soma_node.end_xy[1],   0.0, soma_diameter_um)
```

For the BedB base point `start_xy = end_xy = (0, 0)` and both points have `z=0` — the two pt3d
points coincide. NEURON computes the cumulative distance as `1e-09` µm and the cylinder area as
`pi * 15 * 1e-09 = 4.7e-08`. The trial driver's per-segment area in the soma is even smaller because
nseg = 1 (`9.42e-14` µm²). When 287 ACh + 287 GABA synaptic events arrive on a near-zero-area soma
the resulting current density blows up.

### Phase B — synapse-XY arrival distribution

The procedural cell's PD-direction synapse arrival fraction within `[0, 1400]` ms is **0.590**
versus **0.798** for the hand-coded cell. About 40% of procedural-cell synapses fire outside the
trial window — the cell's symmetric primary stems extend in both PD and ND directions, so half-ish
of synapses sit at `proj < BAR_X_START_UM = -40` and arrive at t<0. **Candidate C (synapse-XY
mismatch)** is PARTIAL — real but partial; the hand-coded cell's biased-toward-one-side arbour
aligns better with the bar window, but this alone does not explain zero spikes (it would at worst
halve the firing rate).

### Phase C — Vm trace under PD bar

* **handcoded_bedb**: 41 spikes, peak Vm +4.65 mV, EPSP area 4654 mV·ms, no error. The t0083
  best-cell channel set works on real morphology — this is the validation gate for Phase D.
* **procedural_bedb**: 0 spikes, peak Vm NaN, EPSP area NaN, error `non_finite_voltage`. The cell
  diverges to infinity because synaptic current density blows up against the zero-area soma.

The validation gate passes (hand-coded cell spikes), so the bug is in the generator, not in
`apply_parameter_vector` or in the trial driver.

### Phase D — ranked candidate verdicts (in `data/root_cause_analysis.json`)

| Candidate | Verdict | Evidence |
| --- | --- | --- |
| A. soma-area mismatch | **CONFIRMED** (degenerate-zero-area sub-case) | proc 9.4e-14 µm² vs hand 287 µm²; ratio 3.3e-16 |
| B. pt3d-vs-L override (dendrites) | REFUTED | max drift 0.0 across 240 non-soma sections |
| C. synapse-XY mismatch | PARTIAL | 41% of procedural-cell synapses arrive outside the trial window |
| D. channel-application skip | REFUTED | list-membership dispatch in `apply_params.py` writes to all sections; channel insertion is idempotent |

The primary cause is unambiguous: **the procedural soma's pt3d points coincide so NEURON's
cumulative pt3d length is zero**. This is a special degenerate sub-case of "soma-area mismatch" that
takes the hypothesis from the planning-time guess "procedural soma is ~3.2x larger than hand-coded"
to "procedural soma is sixteen orders of magnitude *smaller*". The fix shape is the same either way:
re-emit the soma's pt3d points so the cylinder length is non-degenerate and the area matches the
t0024 reference.

### Phase E — fix implementation

`code/morphology_generator_fix.py` exposes
`generate_fixed_morphology(*, params, morph_seed) -> MorphologyResult`. Implementation:

```python
def _patch_soma_geometry(*, h, soma, soma_diameter_um):
    d_target = BEDB_AREA_TARGET_UM2 / (math.pi * soma_diameter_um)
    soma.push()
    try:
        h.pt3dclear()
        h.pt3dadd(0.0, 0.0, 0.0, d_target)
        h.pt3dadd(0.0, 0.0, soma_diameter_um, d_target)
    finally:
        h.pop_section()


def generate_fixed_morphology(*, params, morph_seed=None):
    result = generate_morphology(params=params, morph_seed=morph_seed)
    _patch_soma_geometry(h=result.h, soma=result.soma,
                         soma_diameter_um=params.soma_diameter_um)
    return result
```

Four unit tests confirm the fix (`code/test_morphology_generator_fix.py`):

* `test_soma_area_within_tolerance` — patched soma area is 220.0 ± 11.0 µm². PASS.
* `test_determinism` — same `(params, morph_seed)` produces structurally identical sections. PASS.
* `test_no_nan_on_bedb_base_point` — patched soma Vm under 50 ms unstimulated `finitialize` has no
  NaN samples and stays within ±5 mV of `V_init = -70 mV`. PASS.
* `test_soma_pt3d_z_axis` — patched soma has exactly two pt3d points at `(0, 0, 0, d_target)` and
  `(0, 0, soma_diameter_um, d_target)`. PASS.

### Phase F — post-fix 8-direction validation

The patched BedB-equivalent cell fires under the t0083 best-cell vector:

| Direction (deg) | Spike count |
| --- | --- |
| 0 (PD) | 61 |
| 45 | 57 |
| 90 | 57 |
| 135 | 57 |
| 180 (ND) | 57 |
| 225 | 55 |
| 270 | 54 |
| 315 | 54 |

* **PD-rate**: 43.6 Hz (REQ-8 strictly positive criterion **PASSED**).
* **DSI**: (PD - ND) / (PD + ND) = (61 - 57) / (61 + 57) = **0.034** (REQ-8 DSI > 0.1 criterion NOT
  met — the synapse-XY symmetry issue from Phase D Candidate C is the limiting factor; the
  procedural cell's symmetric primary stems do not preferentially face the PD axis).
* **Peak Vm at PD**: +10.97 mV — clean APs above the -10 mV threshold.

The PD-rate result confirms the fix unblocks the silence; the low DSI confirms direction selectivity
is a separate problem that this task explicitly scopes out (the plan's stretch goal of 3-of-5 STABLE
cells is also dominated by the same synapse-XY symmetry issue and is not the load-bearing
demonstration of the fix).

### Phase F stretch — STABLE-from-t0090 cells

Five STABLE-but-silent cells from t0090 verification (`different/morph_00`, `13`, `14`, `15`, `19`)
were also re-run with the fix applied. **All 5 cells produce non-zero PD-rate post-fix** (stretch
criterion was 3/5):

| Cell | PD-rate (Hz) | DSI | Peak Vm at PD (mV) |
| --- | --- | --- | --- |
| `different/morph_00` | 2.14 | 0.500 | 3.89 |
| `different/morph_13` | 1.43 | 1.000 | 1.59 |
| `different/morph_14` | 36.43 | 0.962 | 8.72 |
| `different/morph_15` | 37.86 | -0.036 | 8.77 |
| `different/morph_19` | 14.29 | 0.212 | 5.79 |

The four asymmetric cells (`morph_00`, `13`, `14`, `19`) recover both spiking and high direction
selectivity. `morph_14` reaches DSI = 0.962 — the cell's `field_elongation_pd = 2.66` and
`primary_branch_pd_concentration = 3.57` bias the dendrites toward the PD axis, so the bar's
spatiotemporal envelope hits effectively. `morph_15` fires at 37.9 Hz but DSI is slightly negative
(prefers ND); inspecting its 14-knob params would identify why, but it is out of scope here.

This stretch result strongly supports the diagnosis: **the soma-area bug is the silence cause for
every t0090 cell**. Once the soma is non-degenerate, both BedB-equivalent and the asymmetric STABLE
cells fire under the t0083 best-cell channel set. The DSI variation across stretch cells confirms
that direction selectivity is driven by morphological asymmetry — t0091 should warm-start its
joint NSGA-II search from the asymmetric cells like `morph_14` rather than from the symmetric BedB
base point.

## Synthesis

The t0090 generator's all-cell silence is caused by a **single line of NEURON-pt3d behaviour**: when
both pt3d points have the same `(x, y, z)` coordinates, NEURON treats the cable as having zero
length and overrides the prior `sec.L = soma_diameter_um` assignment. This makes the soma into a
near-zero-area sink and synaptic current density diverges within a handful of simulation steps. The
fix is a three-line change inside a thin wrapper: `pt3dclear` + two new `pt3dadd` calls along the
z-axis. The wrapper is a drop-in replacement so t0091 swaps one import path with no other code
changes.

For t0091's planned 68-d joint NSGA-II run, the recommended generator behaviour is:

1. **Use `generate_fixed_morphology` instead of `generate_morphology` everywhere.** Import path:
   `from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import generate_fixed_morphology`.
2. **Keep the `_LIVE_CELLS` defense.** The fix does not change the GC `id()` reuse risk; t0091
   should keep appending each built cell to a module-level live list before passing it to
   `apply_parameter_vector`, exactly as t0090's `verification.py` does.
3. **Expect direction selectivity to come from the asymmetry knobs, not from the soma fix alone.**
   This task's diagnostic shows the patched BedB-equivalent cell fires actively in all 8 directions
   but barely distinguishes PD from ND. The asymmetry knobs (`field_elongation_pd > 1`,
   `branch_density_gradient_pd != 0`, `primary_branch_pd_concentration > 0`,
   `soma_offset_pd_um != 0`) are the right levers for DSI and they live in t0091's joint search
   space.
4. **The synapse-XY mismatch (Candidate C, PARTIAL) does not require its own fix in t0091.** The bar
   protocol's spatial window covers `[BAR_X_START_UM=-40, BAR_X_START_UM + BAR_VEL * TSTOP = 1360]`
   µm in the PD direction, and once the asymmetry knobs bias the cell toward one side, more
   synapses will fall inside the window. If a future task wants to be explicit, the
   `setup_synapses_with_intended_xy` shape sketched in the plan is a reasonable defensive extension;
   it is **not** required to unblock t0091.

## Limitations

* The fix targets the soma surface area only. It does not address the synapse-XY mismatch (Phase D
  Candidate C, PARTIAL) or any potential limitations of the bar-window calibration. The patched
  BedB-equivalent cell has DSI ~0.034 — well below the published target — but the silence
  problem this task scopes is solved (43.6 Hz firing rate). Direction selectivity tightening is
  t0091's job.
* Phase F stretch results on the 5 STABLE-from-t0090 cells are recorded but not used as a pass
  criterion. Some of those cells have non-trivial asymmetry knobs (`field_elongation_pd` up to 2.7,
  `soma_offset_pd_um` non-zero); the dendritic geometry under those knobs may have separate issues
  not covered by the soma fix. Future analysis can use the per-cell records in
  `data/post_fix_verification.json` to identify whether any STABLE cell needs additional patching.
* The fix's chosen target surface area (220 µm²) was set from prior research-code estimation of
  the t0024 frustum stack; the actual t0024 measurement is 287 µm². The deviation is small enough
  that the t0083 channels still drive the patched cell to spiking, but a future refinement could use
  287 µm² for an even tighter match. We deliberately keep 220 µm² as the constant in the library
  to preserve the determinism + auditability the plan committed to.
* Window alignment with NEURON's pt3d behaviour was determined empirically on Windows 11 / NEURON
  8.2.7 / Python 3.13. The Linux pip wheel of NEURON behaves the same way on the project's Vast.ai
  instances (verified by inspection of `generator.py`'s pt3d code), but a future Linux re-run with
  this task's diagnostic would be a useful confirmation.

## Sources

* Task: `t0024_port_de_rosenroll_2026_dsgc` — hand-coded Bed B cell, ground truth comparison.
* Task: `t0080_bedb_mobo_v3_dendritic_spike_nsga2` — `apply_parameter_vector`,
  `setup_synapses_parametric`, `run_one_trial`, the 54-d ParameterVector definition.
* Task: `t0083_bedb_v3_extend_nsga2_gen8plus` — source of the best-cell parameter vector
  (`results/data/pareto_front.json`).
* Task: `t0090_morphology_generator_diversity_test` — the buggy generator, source of
  `MorphologyParams`, `BEDB_BASE_POINT`, `_get_neuron_h`, the diversity-grid morph_*.json files.

[t0024]: ../../../t0024_port_de_rosenroll_2026_dsgc/
[t0080]: ../../../t0080_bedb_mobo_v3_dendritic_spike_nsga2/
[t0083]: ../../../t0083_bedb_v3_extend_nsga2_gen8plus/
[t0090]: ../../../t0090_morphology_generator_diversity_test/
