---
spec_version: "1"
task_id: "t0050_audit_syn_distribution"
research_stage: "code"
tasks_reviewed: 8
tasks_cited: 8
libraries_found: 1
libraries_relevant: 1
date_completed: "2026-04-25"
status: "complete"
---
# Code Research: Audit Deposited Synapse Spatial Distribution

## Task Objective

Extract per-synapse `(x, y, z)` coordinates from the deposited Poleg-Polsky 2016 DSGC model (ModelDB
189347), compute per-channel (NMDA/AMPA/GABA) and per-side (PD vs ND) spatial densities, path
distances from soma, and counts, then compare against the paper's qualitative claims to test
hypothesis H1: that the deposited spatial distribution is responsible for the [t0049] GABA PD/ND
symmetry collapse under somatic SEClamp. The audit must NOT modify the model — it is a measurement
task that re-uses the existing `modeldb_189347_dsgc_exact` library and extends its
`read_synapse_coords()` helper with section, z-coordinate, length, and path-distance fields.

## Library Landscape

The project's library aggregator script is **not present** in this worktree
(`arf/scripts/aggregators/aggregate_libraries.py` does not exist; only `aggregate_categories`,
`aggregate_costs`, `aggregate_machines`, `aggregate_metric_results`, `aggregate_metrics`,
`aggregate_suggestions`, `aggregate_task_types`, and `aggregate_tasks` are available). Library
discovery was therefore done by direct inspection of `tasks/*/assets/library/` folders.

* **`modeldb_189347_dsgc_exact`** (created by [t0046]). Pinned to ModelDB 189347 commit
  `87d669dcef18e9966e29c88520ede78bc16d36ff`. Library path:
  `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/`. No
  corrections overlay is present. **Highly relevant** — this is the deposited DSGC the audit
  measures; the task description explicitly mandates re-use via `build_dsgc()`. Module imports the
  audit will use:
  * `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.build_cell import build_dsgc, read_synapse_coords, get_cell_summary, SynapseCoords, assert_bip_positions_baseline, reset_globals_to_canonical`
  * `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun import run_one_trial`
    (optional — only needed if a full `simplerun` call replaces a manual `placeBIP` invocation)
  * `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.constants import Direction, ExperimentType, V_INIT_MV, TSTOP_MS, DT_MS, B2GNMDA_CODE`
  * `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.neuron_bootstrap import ensure_neuron_importable`

No other libraries exist in `tasks/*/assets/library/` that are relevant to this audit (verified by
direct `ls` on every task folder). One additional library is present — `de_rosenroll_2026_dsgc`
from a different DSGC port — but it does not provide the deposited Poleg-Polsky 2016 morphology,
so it is excluded.

## Key Findings

### `placeBIP()` x-axis convention is "stimulus-axis position" (locx), not a sign-thresholded label

The deposited code does **not** classify synapses as PD vs ND by a hard `x > 0` / `x < 0` threshold.
Instead, the wave-direction logic in `placeBIP()`
(`assets/library/modeldb_189347_dsgc_exact/sources/main.hoc:228-236, 247-255, 267-275`; verbatim
copy in `dsgc_model_exact.hoc:201-209, 220-228, 239-247` [t0046]) treats every synapse's `locx`
field as the position along the stimulus axis, and computes the per-synapse arrival time of the
drifting bar as:

```hoc
if (lightreverse){
    starttime = (lightstart + (lightXend - RGC.BIPsyn[synnum].locx) / lightspeed)
} else {
    starttime = (lightstart + (RGC.BIPsyn[synnum].locx - lightXstart) / lightspeed)
}
```

with `lightXstart = -100`, `lightXend = 200`, `lightspeed = 1` µm/ms (`main.hoc:69, 72-73`;
`dsgc_model_exact.hoc:53-57` [t0046]). PD ↔ ND is implemented as the `lightreverse` flag passed
through `simplerun(exptype, dir)` as the `$2` argument, which sets the scalar
`gabaMOD = 0.33 + 0.66*$2` (`dsgc_model_exact.hoc:316-334` [t0046]; PD ($2=0) → 0.33, ND ($2=1)
→ 0.99 per [t0046]'s `Direction` enum in `code/constants.py:146-154`). The same `gabaMOD` scalar
multiplies every SAC inhibitory synapse uniformly (`dsgc_model_exact.hoc:234`,
`mulnoise.fill(VampT*gabaMOD,...)`); there is no spatial gating of PD-side vs ND-side gain. This is
the structural reason [t0049] found GABA PD/ND symmetry collapse under SEClamp: the deposited GABA
conductance is identical at every synapse, and the `gabaMOD` swap only adjusts wave-arrival
amplitude through the `placeBIP()` noise vectors.

For the audit, the operationally useful PD vs ND classification is therefore based on `locx`
relative to the stimulus midline, not on any HOC label. The midline can be taken as the soma center
`x_soma` (ideally) or the centroid of the synapse population (fallback). PD-side ⇔ the synapses
that the wave reaches **first** in the PD direction (`lightreverse=0`, increasing x), so PD-side is
**smaller-x** synapses (closer to `lightXstart=-100`) and ND-side is **larger-x** synapses (closer
to `lightXend=200`). The audit must document which midline it uses and report the count split for
the alternative midlines as a sensitivity check.

### Synapse `locx` / `locy` are set from section midpoint at construction time

In `RGCmodel.hoc:11839-11857` [t0046], the DSGC template iterates `forsec ON` and for each ON
section places exactly one BIPsyn, one SACinhibsyn, one SACexcsyn, all at segment `0.5`:

```hoc
forsec ON {
    if (skip == 0) {
        for i = 0, numsynperdend - 1 {
            SACinhibsyn[countn] = new SACinhib(.5)
            SACexcsyn[countn]   = new SACexc(.5)
            BIPsyn[countn]      = new bipNMDA(.5)
            SACinhibsyn[countn].locx = (x3d(1) - x3d(0)) / (numsynperdend + 1) * (i + 1) + x3d(0)
            SACinhibsyn[countn].locy = (y3d(1) - y3d(0)) / (numsynperdend + 1) * (i + 1) + y3d(0)
            // ... same for SACexcsyn and BIPsyn ...
            countn = countn + 1
        }
    }
    skip = skip + 1
    if (skip == numdendskip) { skip = 0 }
}
```

With `numsynperdend = 1` and `numdendskip = 1` (`RGCmodel.hoc:8, 11832`), every ON section gets one
synapse and `locx = (x3d(0) + x3d(1)) / 2`, `locy = (y3d(0) + y3d(1)) / 2`. **Note**: only the first
two 3D points of each section are used; for sections with > 2 3D points the synapse is placed near
the proximal end, not at the geometric centroid. The audit should compare the deposited `locx`
against a **proper** section midpoint (averaging all `n3d()` points) to log this as a discrepancy.
The synapse z-coordinate is **never stored** — `bipNMDA`, `SACinhib`, `SACexc` have only `locx`
and `locy` RANGE variables. To produce a true 3D coordinate we must extract `z` from the parent
section's `z3d()` points after locating the section.

### `read_synapse_coords()` already exists in [t0046] but only captures (locx, locy)

The library helper `read_synapse_coords` in
`tasks/t0046_reproduce_poleg_polsky_2016_exact/code/build_cell.py:124-140` [t0046] iterates
`for idx in range(int(h.RGC.numsyn))` and returns a list of frozen `SynapseCoords` dataclasses with
six fields: `index`, `bip_locx_um`, `bip_locy_um`, `sac_inhib_locx_um`, `sac_inhib_locy_um`,
`sac_exc_locx_um`, `sac_exc_locy_um` (lines 38-48). **It does not capture** the parent section name,
the section length, the z-coordinate, or the path distance from soma. The audit must extend this
with a new helper (in this task's `code/`, not the library — adding fields would force a library
version bump and break [t0049]'s baseline-position assertion via `assert_bip_positions_baseline`).
The new helper is **not** a "fork" of the library — it consumes the library's `h` handle and adds
derived measurements.

### Section access from a synapse uses NEURON Python's `Section.x3d(i)` API directly, no `sec.push()` needed

[t0022]'s `_section_midpoint(*, sec: Any) -> tuple[float, float]` in
`code/run_tuning_curve.py:181-196` is a working precedent. It calls `int(sec.n3d())` for the point
count and `float(sec.x3d(i))`, `float(sec.y3d(i))` for each point — Python uses dot-notation on
the section object, no HOC `push/pop` required. `z3d(i)` is available the same way (verified by
inspecting the 3D point format in `RGCmodel.hoc:221+`, where `pt3dadd(x, y, z, diam)` creates
4-tuples). For the audit:

```python
def section_centroid_3d(*, sec: Any) -> tuple[float, float, float]:
    n_points: int = int(sec.n3d())
    if n_points == 0:
        return (0.0, 0.0, 0.0)
    return (
        sum(float(sec.x3d(i)) for i in range(n_points)) / n_points,
        sum(float(sec.y3d(i)) for i in range(n_points)) / n_points,
        sum(float(sec.z3d(i)) for i in range(n_points)) / n_points,
    )
```

The synapse's z-coordinate is the centroid `z` of its parent section (averaged over all `n3d()`
points). For a z-coordinate at the segment center specifically (the synapse's `0.5` location),
NEURON does not expose a built-in `seg → 3D point` mapping at single-segment granularity for
`nseg=1` sections; `forall { nseg=1 }` (`RGCmodel.hoc:11824`) means each section has one segment and
the centroid is the right approximation. Document this approximation in the helper docstring.

### Mapping synapse index → parent section uses `for sec in h.RGC.ON` enumeration

Because `placeBIP()` constructs synapses in a single deterministic walk over `forsec ON` with
`skip=0` (numdendskip=1), synapse index `i` corresponds 1:1 to the i-th section in the ON
SectionList iteration order. The audit code can therefore build the `index → section` map by:

```python
on_sections: list[Any] = list(h.RGC.ON)
assert len(on_sections) == int(h.RGC.numsyn), (
    f"ON sections {len(on_sections)} != numsyn {int(h.RGC.numsyn)}"
)
for idx, sec in enumerate(on_sections):
    sec_name: str = str(sec.name())  # e.g., "DSGC[0].dend[5]"
    sec_length_um: float = float(sec.L)
    centroid_xyz: tuple[float, float, float] = section_centroid_3d(sec=sec)
```

[t0029] / [t0030]'s `_on_arbor_section_names()` in `code/length_override.py:30-34` and
`code/diameter_override.py:30-39` confirm `for sec in h.RGC.ON` works; [t0022]'s
`build_ei_pairs(*, h)` at `code/run_tuning_curve.py:212` uses
`for dendrite_index, sec in enumerate(h.RGC.ON)` — exact same pattern. **Section name parsing**:
`sec.name()` returns strings like `"DSGC[0].dend[5]"` (with the template instance prefix); the audit
may strip the prefix for cleaner reporting using `name.rsplit(".", 1)[-1]`.

### `h.distance()` requires explicit origin via `h.distance(0, soma(0.5))`, then `h.distance(syn_seg)`

NEURON's `distance()` is a stateful function: the first call sets the path-distance origin, the
second call returns the path distance from the origin to a target segment. In Python:

```python
h.distance(0, h.RGC.soma(0.5))  # set origin = soma center
for idx in range(int(h.RGC.numsyn)):
    syn = h.RGC.BIPsyn[idx]
    syn_seg = syn.get_segment()  # returns Segment for the synapse's 0.5 position
    path_um: float = float(h.distance(syn_seg))
```

No prior task in the project has called `h.distance()` from Python (verified by grep over
`tasks/**/*.py`); the HOC source uses `distance()` in `RGCmodel.hoc:11819, 11821` as
`access soma; distance(); ... diam = .5 + 2.58*exp(-(distance(01)-10)/10)` (the diameter taper
formula), so the mechanism is well-tested in HOC. The Python equivalent must be exercised carefully:

* The `0` first-arg variant sets the origin; subsequent calls without that variant return distances
* `syn.get_segment()` is the documented NEURON Python API for retrieving the `Segment` a
  POINT_PROCESS is attached to; `.sec` then gives the parent `Section`.
* The audit should assert that the origin was set before the per-synapse loop:
  `h.distance(0, h.RGC.soma(0.5))` returns 0 (the soma-center-to-soma-center distance), so the
  return value of the origin-setting call can be checked:
  `assert abs(h.distance(0, h.RGC.soma(0.5))) < 1e-9`.

### Total dendritic length per side via `for sec in h.allsec(): sum(sec.L)`

[t0008]'s `report_morphology.py:56-65` already demonstrates the total-cable-length pattern:

```python
bundled_total_length_um: float = 0.0
for sec in h.allsec():
    bundled_total_length_um += float(sec.L)
```

For the per-side density metric, the audit needs total dendritic length **filtered by side**. The
straightforward implementation iterates all sections, computes each section's centroid x, and
classifies the section as PD-side or ND-side using the same midline as the synapses:

```python
total_length_pd_um: float = 0.0
total_length_nd_um: float = 0.0
for sec in h.RGC.ON:           # only ON sections; OFF sections have no synapses
    centroid: tuple[float, float, float] = section_centroid_3d(sec=sec)
    if centroid[0] < x_midline:
        total_length_pd_um += float(sec.L)
    else:
        total_length_nd_um += float(sec.L)
```

For full audit completeness, the metric should also be computed including OFF sections (which have
no synapses but contribute to the morphology); document both flavours.

### The `simplerun()` rebinds globals on every call — `placeBIP()` must be run via the deposited path

[t0049]'s research_code.md (lines 84-91) [t0049] documents that `simplerun()` writes
`b2gnmda = 0.5*nmdaOn`, `b2gampa = 0.25`, `s2ggaba = 0.5`, `s2gach = 0.5`, `gabaMOD = 0.33+0.66*$2`,
`achMOD = 0.33` unconditionally on every call (`dsgc_model_exact.hoc:316-334` [t0046]). For the
audit, this means we **must** call `placeBIP()` (either via `simplerun(exptype=1, direction=0)` or
via direct `h("placeBIP()")` after `update()`) for the canonical positions to be populated. The
synapse positions themselves are set in `init_sim()` → `RGCmodel.hoc:11839-11857` at cell
construction time and **do not depend on the simulation parameters** — the `(locx, locy)` values
are baked in at `build_dsgc()` and remain constant across `placeBIP()` invocations. Calling
`placeBIP()` after `build_dsgc()` is required only to populate the noise vectors; the audit's
coordinate measurements are valid immediately after `build_dsgc()` returns. This is verified by
[t0046]'s `_ensure_cell` (`code/run_simplerun.py:67-78`) which calls `read_synapse_coords(h=h)`
**before** any `simplerun()` invocation and uses the result as the baseline for
`assert_bip_positions_baseline` across the entire sweep.

## Reusable Code and Assets

### Library: `modeldb_189347_dsgc_exact` (created by [t0046])

* **Source**:
  `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/`
* **Reuse method**: **import via library**.
* **Import paths used by this task**:
  * `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.build_cell import build_dsgc, read_synapse_coords, get_cell_summary, SynapseCoords, assert_bip_positions_baseline, reset_globals_to_canonical`
  * `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.constants import Direction, ExperimentType, V_INIT_MV, TSTOP_MS, DT_MS, B2GNMDA_CODE`
  * `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.neuron_bootstrap import ensure_neuron_importable`
* **Key signatures**:
  * `build_dsgc() -> Any` (`code/build_cell.py:84-109`) — builds the DSGC, runs `init_sim()` and
    `init_active()` and `update()`, returns NEURON `h` handle. After this call,
    `h.RGC.numsyn = 282`, `h.RGC.countON = 282`.
  * `read_synapse_coords(*, h: Any) -> list[SynapseCoords]` (`code/build_cell.py:124-140`) —
    returns
    `(index, bip_locx_um, bip_locy_um, sac_inhib_locx_um, sac_inhib_locy_um, sac_exc_locx_um, sac_exc_locy_um)`
    per synapse. **No section name, no z, no path distance.**
  * `get_cell_summary(*, h: Any) -> CellSummary` (`code/build_cell.py:112-121`) — returns
    `(num_synapses=282, num_on_sections=282, num_soma_sections=1, num_dend_sections=350)`.
* **Adaptation needed**: none for the imports themselves. The audit code wraps these in a new helper
  (next item) that adds the missing fields.
* **Line count to write in this task**: ~150 lines for the audit driver
  (`extract_synapse_coords.py`, ~80 lines), the analysis script (`compute_density_stats.py`, ~120
  lines), the figure renderer (`render_figures.py`, ~100 lines), `paths.py` (~30 lines),
  `constants.py` (~30 lines), and `main.py` orchestrator (~50 lines).

### Pattern: Section centroid via `x3d/y3d` averaging (copy from [t0022])

* **Source**: `tasks/t0022_modify_dsgc_channel_testbed/code/run_tuning_curve.py:181-196` — the
  `_section_midpoint(*, sec: Any) -> tuple[float, float]` helper.
* **Reuse method**: **copy into task** — extend to 3D by adding the `z3d` average. ~16 lines
  including the extension.
* **What it does**: For a NEURON section, returns the average of `(x3d, y3d)` across all `n3d()` 3D
  points. The extension adds `z3d` for the third dimension.
* **Adaptation needed**: rename to `_section_centroid_3d` and return `tuple[float, float, float]`;
  add `z_sum` / `z3d(i)` calls.
* **Line count to copy / extend**: ~20 lines.

### Pattern: ON-arbor enumeration via `for sec in h.RGC.ON` (copy from [t0029])

* **Source**: `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/length_override.py:30-34` — the
  `_on_arbor_section_names(*, h: Any) -> set[str]` helper. Plus [t0022]'s
  `for dendrite_index, sec in enumerate(h.RGC.ON):` at `code/run_tuning_curve.py:212`.
* **Reuse method**: **copy into task** — adapt for the audit's per-section data record (name,
  length, centroid, side classification).
* **What it does**: Enumerates the 282 ON sections that hold synapses; the order matches the synapse
  construction order in `placeBIP()`.
* **Adaptation needed**: build a list of section objects (not just names) so the audit can call
  `sec.x3d(i)`, `sec.y3d(i)`, `sec.z3d(i)`, `sec.L`, `sec.name()` for each.
* **Line count to write**: ~15 lines.

### Pattern: Path management & constants modules (copy template from [t0049])

* **Source**: `tasks/t0049_seclamp_cond_remeasure/code/paths.py` and `code/constants.py`.
* **Reuse method**: **copy into task** — rename for the audit's outputs
  (`syn_x_hist_per_channel.png`, `syn_radial_distance_per_channel.png`,
  `syn_count_pd_vs_nd_per_channel.png`, `synapse_coordinates.csv`, `per_channel_density_stats.csv`).
* **What it does**: Defines `RESULTS_DIR`, `IMAGES_DIR`, `DATA_DIR` constants pointing to this
  task's `results/`; defines column names and per-channel labels.
* **Adaptation needed**: trivial path / filename rename.
* **Line count to copy**: ~30 lines for paths.py, ~30 lines for constants.py (PD/ND midline,
  per-channel labels, dtypes).

### Pattern: Cell-build cache (re-affirm from [t0046]/[t0049])

* **Source**: `tasks/t0046_reproduce_poleg_polsky_2016_exact/code/run_simplerun.py:64-78` —
  `_CELL_STATE: dict[str, Any] = {}` and `_ensure_cell()` idempotent builder.
* **Reuse method**: **import via library** — call `build_dsgc()` directly once at top of `main.py`
  and reuse the `h` handle for both the synapse-coordinate extraction and the per-section morphology
  pass.
* **What it does**: Avoids the 30-60 s NEURON cell build cost on repeated calls.
* **Adaptation needed**: none — the audit builds once and never rebuilds.

### NEW: `extract_synapse_coords_with_section_3d` helper (write in this task's `code/`)

* **Reuse method**: **new code** in this task's `code/extract_synapse_coords.py` (~80 lines).

* **What it does**: For each of the 282 synapses, returns a frozen dataclass with: `index`,
  `bip_locx_um`, `bip_locy_um`, `bip_z_um`, `sac_inhib_locx_um`, `sac_inhib_locy_um`,
  `sac_inhib_z_um`, `sac_exc_locx_um`, `sac_exc_locy_um`, `sac_exc_z_um`, `parent_section_name`,
  `parent_section_length_um`, `parent_section_centroid_x_um`, `parent_section_centroid_y_um`,
  `parent_section_centroid_z_um`, `path_distance_um` (from soma via `h.distance(0, soma(0.5))` then
  `h.distance(syn.get_segment())`), `radial_distance_um`
  (`sqrt((x - x_soma)^2 + (y - y_soma)^2 + (z - z_soma)^2)`).

* **Function signature**:

  ```python
  @dataclass(frozen=True, slots=True)
  class SynapseAuditRecord:
      index: int
      bip_locx_um: float
      bip_locy_um: float
      sac_inhib_locx_um: float
      sac_inhib_locy_um: float
      sac_exc_locx_um: float
      sac_exc_locy_um: float
      parent_section_name: str
      parent_section_length_um: float
      parent_section_centroid_x_um: float
      parent_section_centroid_y_um: float
      parent_section_centroid_z_um: float
      path_distance_um: float
      radial_distance_from_soma_um: float

  def extract_synapse_audit(
      *,
      h: Any,
      soma_centroid: tuple[float, float, float],
  ) -> list[SynapseAuditRecord]: ...
  ```

  All three channel classes share the same parent section (because `placeBIP()` places
  BIP/SACinhib/SACexc on the same `forsec ON` iteration), so the section-derived fields
  (`parent_section_*`, `path_distance_um`) are channel-independent. The per-channel `(locx, locy)`
  may differ slightly only because the 3D-point arithmetic in `RGCmodel.hoc:11844-11850` uses
  `(i+1)/(numsynperdend+1)` interpolation; with `numsynperdend=1` the value is identical across all
  three channels.

## Lessons Learned

* **NEURON cell-build is 30-60 s; never rebuild mid-script** — [t0046]'s `_CELL_STATE` cache and
  [t0047]'s reuse pattern are essential. The audit builds once at startup and runs all measurements
  on the cached `h` handle.
* **`simplerun()` rebinds globals on every call** — [t0046] / [t0049] both flag this. The
  `(locx, locy)` values themselves are NOT touched by `simplerun()`; they are set once in
  `RGCmodel.hoc:11839-11857` at construction time. The audit's coordinate snapshot is therefore
  invariant across `simplerun()` invocations and can be taken before any simulation runs.
* **`gabaMOD` is a single scalar applied uniformly to all SAC inhibitory synapses** — there is no
  spatial gating. This is the structural mechanism behind [t0049]'s GABA PD/ND symmetry collapse:
  the somatic SEClamp sees identical GABA conductance regardless of `direction` because the
  per-synapse positions are unchanged and the only difference is the wave-arrival timing through
  `placeBIP()`.
* **Synapse `(locx, locy)` is the section's first-two-3D-points midpoint, NOT the geometric
  centroid** — the formula `(x3d(0) + x3d(1)) / 2` in `RGCmodel.hoc:11844-11850` ignores 3D points
  beyond the second, which means for sections with > 2 3D points the synapse is placed near the
  proximal end. The audit should report the deviation between the deposited `locx` and the true
  section centroid as a discrepancy.
* **Synapse z-coordinate is never stored** — `bipNMDA`, `SACinhib`, `SACexc` only have `locx` and
  `locy` RANGE variables. To produce a true 3D coordinate the audit must compute `z` from the parent
  section's `z3d()` points. The bundled morphology has full 3D data (`pt3dadd(x, y, z, diam)` calls
  in `RGCmodel.hoc:221+`) so this is straightforward.
* **`h.distance()` is stateful** — the first call sets the origin, subsequent calls return path
  distances. Failing to set the origin gives wrong distances. The audit code must set the origin
  exactly once via `h.distance(0, h.RGC.soma(0.5))` before the per-synapse loop and assert the
  return value is 0.
* **HOC section names include the template prefix** — `sec.name()` returns `"DSGC[0].dend[5]"`;
  for clean reporting use `name.rsplit(".", 1)[-1]` to get `"dend[5]"`. The task description (under
  Anticipated Risks) explicitly flags this.
* **`for sec in h.RGC.ON` iterates the ON SectionList directly in Python** — verified by [t0022],
  [t0029], [t0030]. No `sec.push()` / `h.pop_section()` needed for `x3d` / `y3d` / `z3d` / `L` /
  `name` access; NEURON Python's `Section` proxy exposes them as methods/attributes.
* **There is a 282 vs 177 synapse-count discrepancy already documented** by [t0046]'s audit
  (`assets/answer/poleg-polsky-2016-reproduction-audit/full_answer.md:181-184`): paper Methods state
  177 synapses, deposited code has 282. The audit will simply re-confirm the 282 count and flag the
  gap.

## Recommendations for This Task

1. **Import [t0046]'s library and reuse `build_dsgc()` and `read_synapse_coords()`** — do not
   reimplement cell building. Build the cell once at the top of `main.py` and use the cached `h`
   handle for all measurements.

2. **Write a new `extract_synapse_audit(*, h, soma_centroid)` helper** in
   `code/extract_synapse_coords.py` that wraps [t0046]'s `read_synapse_coords()` and adds: parent
   section name, parent section length, parent section centroid (x, y, z), per-synapse z (taken from
   parent section centroid), per-synapse path distance from soma, per-synapse radial distance from
   soma. Do NOT modify the library — add the new fields locally.

3. **Set the path-distance origin once** at the start of the extraction loop:
   `h.distance(0, h.RGC.soma(0.5))` and assert the return value is < 1e-9. Then call
   `h.distance(syn.get_segment())` per synapse where `syn = h.RGC.BIPsyn[idx]` (BIP/SACinhib/SACexc
   share the same section, so a single call per synapse index suffices).

4. **Compute the soma 3D centroid** using `for sec in h.allsec(): if sec.name().endswith(".soma")`
   (pattern from [t0008]'s `report_morphology.py:63`) and average `x3d/y3d/z3d` across the soma's
   `n3d()` points. Use this as the radial-distance reference and the PD/ND midline.

5. **Classify PD vs ND** by `synapse.bip_locx_um < x_soma` (PD-side) or
   `synapse.bip_locx_um >= x_soma` (ND-side), based on the convention that the wave runs
   `lightXstart=-100 → lightXend=200` and reaches smaller-x synapses first in PD. Document the
   convention in the helper docstring and report a sensitivity table for two alternative midlines:
   (a) `x = 0`, (b) median of `BIPsyn.locx`. If all three yield similar splits, the PD/ND
   classification is robust.

6. **Compute the per-side density** as `density_pd = count_pd / total_section_length_um(side="PD")`
   where the section-length sum is over `h.RGC.ON` sections (synapse-bearing only) classified by
   their own `centroid_x` against the same midline. Also report the density over `h.RGC.dends` (all
   dendrites, including OFF) as an alternative denominator and document the choice.

7. **Run `placeBIP()` once before measurements** via `simplerun(exptype=1, direction=0)` (PD
   control, gNMDA = 0.5 nS) to honour the task description's "Build cell once + simplerun() call"
   requirement, but document that the synapse positions themselves are independent of `simplerun()`
   invocation. Use [t0046]'s
   `run_one_trial(exptype=ExperimentType.CONTROL, direction=Direction.PREFERRED, trial_seed=1, b2gnmda_override=0.5)`
   for the call.

8. **Assert post-extraction** that `len(records) == int(h.RGC.numsyn) == 282`,
   `int(h.RGC.countON) == 282`, that the BIP/SACinhib/SACexc `locx` values are identical for each
   index (because all three are placed at `0.5` of the same ON section), and that the parent section
   name does NOT change between channels.

9. **Centralise paths and constants** in `code/paths.py` and `code/constants.py` per the project
   style guide; copy the template from [t0049] and rename for the audit outputs.

10. **Verdict logic**: report `count_pd / count_nd` ratio per channel; H1 SUPPORTED if all three
    channels are in `[0.9, 1.1]` (symmetric); H1 REJECTED if GABA shows asymmetric ratio matching
    paper's ND-bias claim; H1 PARTIAL if weakly asymmetric (one channel only or `[0.7, 1.3]`).

## Task Index

### [t0007]

* **Task ID**: `t0007_install_neuron_netpyne`
* **Name**: Install and validate NEURON 8.2.7 + NetPyNE 1.1.1 toolchain
* **Status**: completed
* **Relevance**: Establishes the NEURON 8.2.7 environment that this task runs in. Direct dependency
  of [t0046]'s library, which the audit imports.

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 and similar DSGC compartmental models to NEURON
* **Status**: completed
* **Relevance**: Origin of the `read_synapse_coords()` helper pattern (later refined by [t0046]).
  Its `report_morphology.py:56-65` is the working precedent for the total-cable-length sum the audit
  needs for per-side density.

### [t0022]

* **Task ID**: `t0022_modify_dsgc_channel_testbed`
* **Name**: Modify DSGC channel testbed (per-dendrite EI tuning curves)
* **Status**: completed
* **Relevance**: Source of the section-centroid-from-`x3d/y3d` helper (`_section_midpoint` at
  `code/run_tuning_curve.py:181-196`) and the `for sec in h.RGC.ON` iteration pattern that the audit
  copies (and extends to 3D).

### [t0029]

* **Task ID**: `t0029_distal_dendrite_length_sweep_dsgc`
* **Name**: Distal dendrite length sweep on DSGC
* **Status**: completed
* **Relevance**: Provides the canonical `_on_arbor_section_names` / `identify_distal_sections`
  pattern (`code/length_override.py:30-52`) for ON-arbor enumeration. The audit uses the same
  `for sec in h.RGC.ON` walk for per-section centroid computation.

### [t0030]

* **Task ID**: `t0030_distal_dendrite_diameter_sweep_dsgc`
* **Name**: Distal dendrite diameter sweep on DSGC
* **Status**: completed
* **Relevance**: Confirms (`research/research_code.md:81-96`) that the bundled morphology has 282 ON
  sections and that synapse placement uses `pt3dadd` 3D coordinates. Replicates the ON-arbor section
  enumeration the audit needs.

### [t0046]

* **Task ID**: `t0046_reproduce_poleg_polsky_2016_exact`
* **Name**: Exact reproduction of Poleg-Polsky 2016 (ModelDB 189347) with audit
* **Status**: completed
* **Relevance**: Direct dependency. Provides the `modeldb_189347_dsgc_exact` library (the only
  library imported by this audit), the `build_dsgc()` / `read_synapse_coords()` /
  `assert_bip_positions_baseline` helpers, the `Direction` / `ExperimentType` enums, the
  `simplerun(exptype, dir)` HOC proc that exposes the deposited model's per-direction behaviour, and
  the audit answer asset that already documented the 282-vs-177 synapse-count discrepancy.

### [t0047]

* **Task ID**: `t0047_validate_pp16_fig3_cond_noise`
* **Name**: Validate Poleg-Polsky 2016 Fig 3A-F conductances and extend noise sweep
* **Status**: completed
* **Relevance**: Established the per-synapse-direct conductance baseline (NMDA: PD 69.55 / ND 33.98
  nS; AMPA: PD 10.92 / ND 10.77 nS; GABA: PD 106.13 / ND 215.57 nS). Notably, GABA shows PD/ND ~1:2
  in the per-synapse direct measurement, whereas [t0049] found ~1:1 in the somatic SEClamp
  measurement — the gap that motivates this audit.

### [t0049]

* **Task ID**: `t0049_seclamp_cond_remeasure`
* **Name**: Re-measure Fig 3A-E conductances under somatic SEClamp on the deposited DSGC
* **Status**: completed
* **Relevance**: Direct dependency and the explicit motivation for this audit. Documented the GABA
  PD/ND symmetry collapse under SEClamp (PD 47.47 / ND 48.04 nS, DSI ≈ -0.006) and identified the
  spatial-distribution hypothesis (H1) as candidate cause. Its `research/research_code.md` contains
  the canonical description of `simplerun()`'s global rebind behaviour and the soma-section access
  pattern (`h.RGC.soma(0.5)`) the audit reuses.
