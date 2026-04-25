---
spec_version: "2"
task_id: "t0050_audit_syn_distribution"
date_completed: "2026-04-25"
status: "complete"
---
# Plan: Audit Deposited GABA/NMDA/AMPA Synapse Spatial Distribution vs Paper

## Objective

Extract the (x, y, z) coordinates, parent section, parent-section length, and
path-distance-from-soma of every BIPsyn (NMDA + AMPA), SACexcsyn, and SACinhibsyn instance in the
deposited Poleg-Polsky 2016 DSGC (ModelDB 189347), compute per-channel and per-side (PD vs ND)
spatial statistics, render three diagnostic PNGs, and produce one answer asset comparing the
deposited spatial distribution against the paper's qualitative claims and the t0049 GABA SEClamp
symmetry collapse. Done means: per-channel synapse counts confirmed at 282 each; per-channel PD-side
and ND-side counts and midline ratio reported numerically; H1 (spatial-distribution hypothesis)
verdict stated as SUPPORTED, REJECTED, or PARTIAL with both structural (no spatial threshold in
`gabaMOD`) and numerical (per-side counts/density) evidence; one answer asset
`synapse-distribution-audit-deposited-vs-paper` produced under `assets/answer/` with the three
diagnostic PNGs embedded in `full_answer.md`. The model itself is not modified — this is a pure
measurement and audit task.

## Task Requirement Checklist

The operative task text from `task.json` and `task_description.md`:

```text
Task name: Audit deposited GABA/NMDA/AMPA synapse spatial distribution vs paper
Short description: Extract per-synapse (x,y,z) coordinates from deposited DSGC, compute PD-side
vs ND-side spatial densities for NMDA/AMPA/GABA, compare to paper text descriptions; explain t0049
GABA symmetry collapse.

Long description (key requirements from task_description.md):
- Re-use the existing modeldb_189347_dsgc_exact library produced by t0046. No code copy or fork.
- Build the cell once via build_dsgc(), then call simplerun(exptype=1, direction=0) (control,
  gNMDA = 0.5 nS) to populate placeBIP(). Extract for every synapse the (x, y, z) center
  coordinate of its parent section, plus the section name and section length.
- Compute per-channel-class spatial statistics:
  * Per-channel synapse counts: total, PD-side, ND-side. Reproduce/confirm the 282 count from
    t0046's audit.
  * Per-channel x-position histograms: bimodal (PD vs ND).
  * Per-channel mean radial distance from soma: mean +- SD. Also broken down by PD-side vs ND-side.
  * Per-channel mean dendritic-tree distance from soma (path length): mean +- SD per channel x side.
  * PD-side vs ND-side density: number of synapses per unit dendritic length on each side, per
    channel.
- Compare these statistics against the paper's text: paper Methods state 177 BIP synapses (vs
  deposited 282 - already known); paper text describes GABA likely ND-asymmetric and BIP likely
  symmetric.
- Identify the synapse-distribution discrepancies that explain t0049's GABA symmetry collapse.

Deliverables:
- Answer asset (1): assets/answer/synapse-distribution-audit-deposited-vs-paper/ per
  meta/asset_types/answer/specification.md v2 with details.json + short_answer.md + full_answer.md.
  full_answer.md must contain question framing, per-channel synapse-count + spatial-statistics
  table, per-channel x-coordinate histogram, H1 verdict with numerical evidence, synthesis
  paragraph reconciling t0049 GABA collapse.
- PNGs under results/images/: syn_x_hist_per_channel.png, syn_radial_distance_per_channel.png,
  syn_count_pd_vs_nd_per_channel.png.

Pass criterion:
- Per-channel synapse counts confirmed (BIP = SACexc = SACinhib = 282 expected).
- Per-channel PD-side vs ND-side count ratio reported numerically (symmetric if ratio in
  [0.9, 1.1]; asymmetric otherwise).
- H1 verdict (SUPPORTED, REJECTED, PARTIAL) stated with numerical evidence.
- Spatial-distribution discrepancy catalogue updated (any per-channel x per-side asymmetry or
  symmetry that differs from paper text).

Out of scope:
- Any modification to the model.
- Re-running the SEClamp protocol.
- Higher-N reruns or new sweeps.
- Reading the supplementary PDF.
- iMK801 or any other model modification.
```

Concrete requirements decomposed into stable IDs:

* **REQ-1**: Re-use the existing `modeldb_189347_dsgc_exact` library from t0046; no code copy or
  fork. Satisfied by Step 1 importing
  `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.build_cell import build_dsgc, read_synapse_coords`
  and not duplicating cell-build logic. Evidence: `code/extract_coordinates.py` contains only
  `from tasks.t0046_...` imports and no embedded HOC strings.
* **REQ-2**: Build the cell once via `build_dsgc()` and run `simplerun(exptype=1, direction=0)`
  (control, gNMDA = 0.5 nS) once to populate `placeBIP()`. Satisfied by Step 3. Evidence:
  `code/extract_coordinates.py` calls `build_dsgc()` exactly once and
  `run_one_trial(exptype=ExperimentType.CONTROL, direction=Direction.PREFERRED, trial_seed=1, b2gnmda_override=0.5)`
  exactly once before extraction.
* **REQ-3**: For every synapse, extract (x, y, z) center coordinate of its parent section, plus
  parent section name and parent section length. Satisfied by Step 4. Evidence: each row of
  `results/synapse_coordinates.csv` has columns `parent_section_name`, `parent_section_length_um`,
  `parent_section_centroid_x_um`, `parent_section_centroid_y_um`, `parent_section_centroid_z_um`.
* **REQ-4**: Compute per-channel synapse counts (total, PD-side, ND-side) and confirm the 282 count
  for all three channels. Satisfied by Step 5 and the assertion in Step 4. Evidence:
  `results/per_channel_density_stats.csv` rows `count_total`, `count_pd`, `count_nd`; explicit
  Python `assert` that `len(records) == int(h.RGC.numsyn) == 282`.
* **REQ-5**: Compute per-channel x-position bimodal histograms (PD vs ND). Satisfied by Step 6.
  Evidence: `results/images/syn_x_hist_per_channel.png` (3 subplots, one per channel) with PD/ND
  median lines.
* **REQ-6**: Compute per-channel mean radial distance from soma, broken down by PD-side vs ND-side,
  with mean +- SD. Satisfied by Step 5. Evidence: `per_channel_density_stats.csv` columns
  `mean_radial_distance_pd_um`, `sd_radial_distance_pd_um`, `mean_radial_distance_nd_um`,
  `sd_radial_distance_nd_um`.
* **REQ-7**: Compute per-channel mean dendritic-tree path distance from soma, broken down by PD-side
  vs ND-side, with mean +- SD. Satisfied by Step 5. Evidence: same CSV with columns
  `mean_path_distance_pd_um` / `sd_path_distance_pd_um` and `..._nd_um`.
* **REQ-8**: Compute PD-side vs ND-side density (synapses per unit dendritic length on each side,
  per channel). Satisfied by Step 5. Evidence: same CSV with columns `density_pd_per_um` and
  `density_nd_per_um`, and intermediate `total_length_pd_um` / `total_length_nd_um` columns.
* **REQ-9**: Compare statistics against paper text claims (177 BIP vs 282 deposited; GABA
  ND-asymmetric per paper; BIP symmetric per paper) and identify discrepancies that explain the
  t0049 GABA SEClamp symmetry collapse. Satisfied by Step 7 (full_answer.md Synthesis section).
  Evidence: `full_answer.md` contains a "Paper claim vs deposited reality" comparison table and a
  Synthesis paragraph explicitly tying the structural finding (`gabaMOD` is a uniform scalar) plus
  the per-side count ratios to the t0049 PD ~47.47 / ND ~48.04 nS GABA collapse.
* **REQ-10**: Render three PNGs under `results/images/`: `syn_x_hist_per_channel.png`,
  `syn_radial_distance_per_channel.png`, `syn_count_pd_vs_nd_per_channel.png`. Satisfied by Step 6.
  Evidence: all three files exist after `render_figures.py` runs.
* **REQ-11**: Produce one answer asset
  `assets/answer/synapse-distribution-audit-deposited-vs-paper/` per
  `meta/asset_types/answer/specification.md` v2 with `details.json` + `short_answer.md` +
  `full_answer.md`. Satisfied by Step 7. Evidence: all three files exist; verificator
  `verify_answer_asset` (or direct inspection) reports 0 errors.
* **REQ-12**: H1 verdict (SUPPORTED, REJECTED, PARTIAL) stated with numerical evidence in
  `full_answer.md`. Satisfied by Step 7. Evidence: `## Synthesis` (or dedicated `## H1 Verdict`)
  section in `full_answer.md` contains one of the three verdict words and cites the numerical PD/ND
  count ratio per channel from `per_channel_density_stats.csv`.
* **REQ-13**: All Python code follows the project Python style guide (absolute imports, paths
  centralised in `code/paths.py`, constants in `code/constants.py`, keyword-only args for
  multi-param functions, frozen dataclasses, explicit type annotations). Satisfied by Steps 2-7.
  Evidence: `uv run ruff check . && uv run ruff format . && uv run mypy .` returns 0 errors.

## Approach

Recommended task type: **`data-analysis`** (already declared in `task.json`). The Planning
Guidelines from `meta/task_types/data-analysis/instruction.md` specify: identify the input dataset
and confirm it exists from prior tasks (the `modeldb_189347_dsgc_exact` library from t0046 is the
input); define the specific questions before writing code (the H1 spatial-distribution hypothesis is
the specific question); list all metrics and chart types upfront (done in `## Step by Step`); follow
the Python style guide; centralise paths in `code/paths.py`; use matplotlib for charts; log per-side
breakdowns alongside aggregates. No statistical hypothesis test is needed — the verdict is a
numerical-threshold rule (`count_pd / count_nd in [0.9, 1.1]` symmetric).

Technical approach grounded in the research:

1. **Cross-task imports from t0046's library**: The library `modeldb_189347_dsgc_exact` at
   `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/`
   provides the deposited DSGC. Direct imports from t0046's `code/` are allowed because t0046 is a
   registered dependency of t0050 and exposes a stable Python module surface. Specific imports:
   `build_dsgc, read_synapse_coords` from `code.build_cell`;
   `run_one_trial, ExperimentType, Direction` from `code.run_simplerun`;
   `V_INIT_MV, TSTOP_MS, DT_MS` from `code.constants`; `ensure_neuron_importable` from
   `code.neuron_bootstrap`.

2. **Critical structural finding from research_code.md** (this is what makes H1 a near-certain
   SUPPORTED before any numbers are extracted): The deposited code's PD/ND swap is a single scalar
   `gabaMOD = 0.33 + 0.66 * direction` applied uniformly across **all** SAC inhibitory synapses
   (`dsgc_model_exact.hoc:316-334`, `mulnoise.fill(VampT*gabaMOD,...)` at line 234). There is **no
   spatial threshold** in the protocol — the wave-arrival timing in `placeBIP()` uses each
   synapse's `locx` to compute per-synapse `starttime`, but the gain modulation `gabaMOD` is a
   single scalar, not a function of `locx`. This means even before measuring counts, we know that
   the somatic SEClamp in t0049 cannot detect a PD/ND GABA asymmetry from the deposited model under
   the control protocol. The numerical per-side counts then quantify *how* symmetric the underlying
   spatial layout is, completing the SUPPORTED verdict with two independent lines of evidence
   (structural + numerical).

3. **Why the synapse coordinates need extension**: t0046's `read_synapse_coords()` returns only
   `(index, bip_locx_um, bip_locy_um, sac_inhib_locx_um, sac_inhib_locy_um, sac_exc_locx_um, sac_exc_locy_um)`
   — no z, no parent section name, no path distance. The HOC mechanisms `bipNMDA`, `SACinhib`,
   `SACexc` only have RANGE variables `locx` and `locy`; z is never stored. The audit therefore
   wraps t0046's helper and adds the missing fields by enumerating `for sec in h.RGC.ON`, computing
   each section's centroid-3D via averaging `sec.x3d(i)/y3d(i)/z3d(i)` over `int(sec.n3d())` points,
   and calling `h.distance(syn_seg)` after setting `h.distance(0, h.RGC.soma(0.5))` as the
   path-distance origin. The synapse index → ON section mapping is 1:1 because `numsynperdend = 1`
   and `numdendskip = 1` in `RGCmodel.hoc:11839-11857`.

4. **Midline classification**: The deposited code does NOT classify synapses as PD vs ND with a sign
   threshold; the wave-direction logic uses each synapse's continuous `locx` as a position along the
   stimulus axis. For audit reporting, we adopt our own classification rule:
   `synapse.bip_locx_um < x_soma` => PD-side (the synapses the wave reaches first when running
   `lightXstart=-100 → lightXend=200`); `synapse.bip_locx_um >= x_soma` => ND-side. We compute the
   soma centroid by averaging `x3d/y3d/z3d` over the soma section's 3D points. As a robustness check
   the same classification is reported for two alternative midlines: (a) `x = 0`, (b) median of all
   `BIPsyn.locx` values; both reported in `per_channel_density_stats.csv`.

5. **Density computation**: For each side classified by the chosen midline,
   `density_side = count_side / total_section_length_side_um`, where the section length is summed
   over `for sec in h.RGC.ON` filtered by the section's centroid-x against the same midline.
   `h.RGC.ON` is the synapse-bearing section list, which is the correct denominator for synapse
   density.

6. **No simulation required for the measurement**: As `research_code.md` clarifies, synapse
   `(locx, locy)` values are baked in at `build_dsgc()` time and are NOT modified by `simplerun()`
   — `simplerun()` only rebinds globals (`b2gnmda`, `b2gampa`, `gabaMOD`, etc.) and rebuilds the
   noise vectors. We still call `simplerun(exptype=1, direction=0)` once via t0046's
   `run_one_trial(exptype=ExperimentType.CONTROL, direction=Direction.PREFERRED, trial_seed=1, b2gnmda_override=0.5)`
   to honour the task description's literal instruction; but no `h.run()` is needed and no AP traces
   are recorded — `run_one_trial` is invoked only for its side effect of calling `placeBIP()`.
   Wall-clock budget: ~30-60 s for `build_dsgc()` (NEURON cell compilation), ~10 s for
   `run_one_trial` (which itself does run the simulation per its contract; if undesirable for
   budget, an alternative is to call `h("placeBIP()")` directly after `build_dsgc()`). The cell
   build and `placeBIP()` both run on local CPU.

**Alternatives considered**:

* *Alternative A: extend `read_synapse_coords()` in t0046's library directly.* Rejected: this would
  force a library version bump in t0046, break t0049's `assert_bip_positions_baseline()` baseline
  assertion (which depends on the exact 7-field `SynapseCoords` dataclass), violate ARF rule 5
  (nothing in a completed task folder may be changed), and require a corrections overlay. The
  selected approach (a new helper in this task's `code/extract_coordinates.py` that consumes the
  library's `h` handle) keeps the library immutable and the dependency boundary clean.

* *Alternative B: skip the `simplerun()` call and only run `build_dsgc()`.* Rejected: the task
  description literally instructs "Build the cell once via `build_dsgc()`, then call
  `simplerun(exptype=1, direction=0)`". Even though `(locx, locy)` is invariant across `simplerun()`
  invocations, executing the literal instruction preserves audit fidelity: any future investigator
  can re-run the script and confirm `placeBIP()` executed without error in the documented control
  condition. The cost is one ~10 s simulation, well within budget.

* *Alternative C: use a continuous spatial-asymmetry metric (e.g., x-coordinate-weighted dipole)
  instead of a binary PD/ND midline split.* Rejected: the task pass criterion explicitly requires a
  per-side count ratio with a threshold rule (`[0.9, 1.1]` => symmetric). A continuous metric would
  be a useful supplement but cannot replace the binary verdict. The plan reports both: the binary
  per-side split is the headline; the continuous distributions are visible in the histograms.

## Cost Estimation

* **API calls (LLM, OpenAI, etc.)**: $0.00 — no LLM calls are made by the implementation.
* **Remote compute (Vast.ai, cloud GPU, etc.)**: $0.00 — task runs entirely on local CPU; no GPU
  is required because the audit is a single cell-build + coordinate extraction with no optimisation,
  sweep, or `h.run()` longer than the one ~10 s `simplerun(exptype=1, direction=0)` invocation.
* **Local compute**: ~$0.00 — assumed free per project convention; the task uses approximately 60
  s of one CPU core.
* **Total**: **$0.00 / $1.00 per-task budget** (`project/budget.json` total budget = $1.00 with
  `per_task_default_limit = $1.00`; `available_services = []`). Well within budget; no intervention
  or budget waiver needed.

## Step by Step

The Step by Step is grouped into three milestones. Each milestone is independently verifiable before
the next begins.

### Milestone 1 — Scaffold and constants (Steps 1-2)

Verifiable by: `code/paths.py` and `code/constants.py` exist, are importable
(`uv run python -c "from tasks.t0050_audit_syn_distribution.code import paths, constants"`), ruff
and mypy pass on both files.

1. **Create `tasks/t0050_audit_syn_distribution/code/paths.py`** with absolute path constants
   pointing at the task folder. Use `Path` from `pathlib`. Define at minimum:
   `TASK_DIR: Path = Path(__file__).parent.parent`, `RESULTS_DIR: Path = TASK_DIR / "results"`,
   `IMAGES_DIR: Path = RESULTS_DIR / "images"`, `DATA_DIR: Path = RESULTS_DIR`,
   `SYNAPSE_COORDINATES_CSV: Path = DATA_DIR / "synapse_coordinates.csv"`,
   `PER_CHANNEL_DENSITY_STATS_CSV: Path = DATA_DIR / "per_channel_density_stats.csv"`,
   `SYN_X_HIST_PNG: Path = IMAGES_DIR / "syn_x_hist_per_channel.png"`,
   `SYN_RADIAL_HIST_PNG: Path = IMAGES_DIR / "syn_radial_distance_per_channel.png"`,
   `SYN_COUNT_BAR_PNG: Path = IMAGES_DIR / "syn_count_pd_vs_nd_per_channel.png"`,
   `ASSETS_ANSWER_DIR: Path = TASK_DIR / "assets" / "answer" / "synapse-distribution-audit-deposited-vs-paper"`.
   Inputs read: none. Outputs produced: the file. Pattern source:
   `tasks/t0049_seclamp_cond_remeasure/code/paths.py`. Expected output after the step: the file
   imports cleanly. Satisfies REQ-13.

2. **Create `tasks/t0050_audit_syn_distribution/code/constants.py`** with: an `Enum` `ChannelKind`
   with three members `BIP` ("BIPsyn"), `SAC_EXC` ("SACexcsyn"), `SAC_INHIB` ("SACinhibsyn"); a
   per-channel display-name map `CHANNEL_DISPLAY_NAMES: dict[ChannelKind, str]` with entries
   `"NMDA + AMPA (BIP)"`, `"SAC excitatory (ACh)"`, `"SAC inhibitory (GABA)"`; the symmetry
   threshold constants `SYMMETRY_RATIO_LOW: float = 0.9` and `SYMMETRY_RATIO_HIGH: float = 1.1`; the
   t0049 GABA SEClamp values for cross-reference, `T0049_GABA_PD_NS: float = 47.47`,
   `T0049_GABA_ND_NS: float = 48.04`, `T0049_GABA_DSI: float = -0.006`; a midline classification
   rule comment
   `# midline rule: synapse.bip_locx_um < x_soma -> "side_a" (PD-side); else "side_b" (ND-side)`.
   Add named constants for CSV column names: `COLUMN_INDEX = "index"`,
   `COLUMN_PARENT_SECTION_NAME = "parent_section_name"`,
   `COLUMN_PARENT_SECTION_LENGTH_UM = "parent_section_length_um"`,
   `COLUMN_BIP_LOCX_UM = "bip_locx_um"`, `COLUMN_BIP_LOCY_UM = "bip_locy_um"`,
   `COLUMN_BIP_Z_UM = "bip_z_um"`, `COLUMN_SAC_INHIB_LOCX_UM = "sac_inhib_locx_um"`, etc., plus
   `COLUMN_PARENT_SECTION_CENTROID_X_UM = "parent_section_centroid_x_um"`, `..._Y_UM`, `..._Z_UM`,
   `COLUMN_PATH_DISTANCE_UM = "path_distance_um"`,
   `COLUMN_RADIAL_DISTANCE_UM = "radial_distance_from_soma_um"`, `COLUMN_X_SIDE = "x_side"` (values
   `"side_a"` / `"side_b"`). Inputs read: none. Outputs produced: the file. Pattern source:
   `tasks/t0049_seclamp_cond_remeasure/code/constants.py`. Expected output: file imports cleanly.
   Satisfies REQ-13.

### Milestone 2 — Cell build + coordinate extraction (Steps 3-4)

Verifiable by: `results/synapse_coordinates.csv` exists with exactly 282 data rows; for each row,
the BIP/SACexc/SACinhib `locx` values are identical (single-segment placement); columns include
`parent_section_name`, `parent_section_length_um`, three centroid columns, `path_distance_um`,
`radial_distance_from_soma_um`.

3. **Create `tasks/t0050_audit_syn_distribution/code/extract_coordinates.py`** that: (a) calls
   `ensure_neuron_importable()` (from
   `tasks.t0046_reproduce_poleg_polsky_2016_exact.code.neuron_bootstrap`); (b) builds the cell once
   via `h = build_dsgc()` (from `tasks.t0046_reproduce_poleg_polsky_2016_exact.code.build_cell`);
   (c) calls
   `run_one_trial(exptype=ExperimentType.CONTROL, direction=Direction.PREFERRED, trial_seed=1, b2gnmda_override=0.5)`
   exactly once (from `tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun`) to honour
   the literal "build cell + simplerun" instruction; (d) returns the cached `h` handle. Asserts
   `int(h.RGC.numsyn) == 282` and `int(h.RGC.countON) == 282`. Inputs read: t0046's library code
   only. Outputs produced: an in-memory `h` handle. Pattern source: t0046's
   `code/run_simplerun.py:64-78` `_ensure_cell()` cache. Satisfies REQ-1, REQ-2.

4. **Extend `code/extract_coordinates.py` with the per-synapse extraction loop.** Add a frozen
   dataclass:

   ```python
   @dataclass(frozen=True, slots=True)
   class SynapseAuditRecord:
       index: int
       bip_locx_um: float
       bip_locy_um: float
       bip_z_um: float
       sac_inhib_locx_um: float
       sac_inhib_locy_um: float
       sac_inhib_z_um: float
       sac_exc_locx_um: float
       sac_exc_locy_um: float
       sac_exc_z_um: float
       parent_section_name: str
       parent_section_length_um: float
       parent_section_centroid_x_um: float
       parent_section_centroid_y_um: float
       parent_section_centroid_z_um: float
       path_distance_um: float
       radial_distance_from_soma_um: float
   ```

   Add a helper `def section_centroid_3d(*, sec: Any) -> tuple[float, float, float]` that averages
   `sec.x3d(i)`, `sec.y3d(i)`, `sec.z3d(i)` over `int(sec.n3d())` points (copy and extend
   `_section_midpoint` from
   `tasks/t0022_modify_dsgc_channel_testbed/code/run_tuning_curve.py:181-196`). Add a helper
   `def soma_centroid_3d(*, h: Any) -> tuple[float, float, float]` that locates the soma section by
   iterating `for sec in h.allsec(): if sec.name().endswith(".soma"): break` and returns
   `section_centroid_3d(sec=sec)`. Add the main extractor
   `def extract_synapse_audit(*, h: Any) -> list[SynapseAuditRecord]` that: (1) calls
   `soma_xyz = soma_centroid_3d(h=h)`; (2) sets path-distance origin via
   `h.distance(0, h.RGC.soma(0.5))` and asserts the return is `< 1e-9`; (3) builds
   `on_sections: list[Any] = list(h.RGC.ON)` and asserts
   `len(on_sections) == int(h.RGC.numsyn) == 282`; (4) iterates
   `for idx in range(int(h.RGC.numsyn))`: pulls `bip = h.RGC.BIPsyn[idx]`,
   `sex = h.RGC.SACexcsyn[idx]`, `sin = h.RGC.SACinhibsyn[idx]`, gets the parent section via
   `sec = bip.get_segment().sec` and asserts `sec is sex.get_segment().sec is sin.get_segment().sec`
   (all three channels share the section); computes `centroid = section_centroid_3d(sec=sec)`,
   `path_um = float(h.distance(bip.get_segment()))`, `bip_z = sex_z = sin_z = centroid[2]` (z is
   taken from the section centroid since RANGE variables only store locx/locy),
   `radial = sqrt((centroid[0]-soma_xyz[0])**2 + (centroid[1]-soma_xyz[1])**2 + (centroid[2]-soma_xyz[2])**2)`,
   strips the template prefix from `sec.name()` via `sec.name().rsplit(".", 1)[-1]`, and appends a
   `SynapseAuditRecord`. Add a writer
   `def write_records_csv(*, records: list[SynapseAuditRecord], output_path: Path) -> None` that
   uses `pandas.DataFrame.from_records` with explicit dtypes per the project Python style guide
   (`pd.UInt32Dtype()` for `index`, `pd.StringDtype()` for `parent_section_name`,
   `np.dtype("float64")` for all distance columns) and writes to `paths.SYNAPSE_COORDINATES_CSV`.
   Add a `main()` that wraps Steps 3 + 4 and writes the CSV. Inputs read: t0046's library `h`
   handle. Outputs produced: `results/synapse_coordinates.csv`. Expected output after running:
   `pd.read_csv(paths.SYNAPSE_COORDINATES_CSV)` returns a DataFrame with shape `(282, 17)`.
   Satisfies REQ-3, REQ-4.

   **Run this step locally with the wrapped logger**:

   ```bash
   uv run python -m arf.scripts.utils.run_with_logs \
     --task-id t0050_audit_syn_distribution -- \
     uv run python -u -m tasks.t0050_audit_syn_distribution.code.extract_coordinates
   ```

   Validation gate (this is not an "expensive" operation per the plan-spec rubric — single ~60 s
   cell-build + ~10 s simplerun on local CPU — but a fast sanity check is still warranted):
   immediately after the script writes the CSV, the script must print to stdout the first 5 rows and
   the assertion line
   `"282 synapses extracted; BIP/SACexc/SACinhib parent sections match for all indices"`. Failure
   condition: if any of the asserts fires, halt and print which index/which field disagreed.
   Recovery: re-read `tasks/t0046_.../code/build_cell.py` to confirm the construction order matches
   the assumption.

### Milestone 3 — Statistics, figures, and answer asset (Steps 5-7)

Verifiable by: `results/per_channel_density_stats.csv` exists with rows for all 3 channels
(BIP/NMDA+AMPA, SAC_EXC, SAC_INHIB) and one comparison row each across two alternative midlines; all
three PNGs exist; the answer asset folder exists with `details.json`, `short_answer.md`,
`full_answer.md`.

5. **Create `tasks/t0050_audit_syn_distribution/code/compute_spatial_stats.py`** that: (a) reads
   `paths.SYNAPSE_COORDINATES_CSV` with explicit dtypes (matching the dtype spec from Step 4); (b)
   for each `ChannelKind` and each of three midline conventions
   (`midline_kind in ["soma_x", "zero", "bipsyn_locx_median"]`), classifies each row's `x_side` as
   `"side_a"` (PD-side) if `record.<chan>_locx_um < midline_x` else `"side_b"` (ND-side); (c)
   computes per-channel × per-side aggregates: `count_total`, `count_side_a`, `count_side_b`,
   `count_ratio = count_side_a / count_side_b`, `mean_radial_distance_side_a_um`,
   `sd_radial_distance_side_a_um`, `mean_radial_distance_side_b_um`, `sd_radial_distance_side_b_um`,
   `mean_path_distance_side_a_um`, `sd_path_distance_side_a_um`, `mean_path_distance_side_b_um`,
   `sd_path_distance_side_b_um`, `total_length_side_a_um` (sum of `parent_section_length_um` over
   rows classified side_a; the parent section is shared across channels so the per-side dendritic
   length is identical for all three channels for a given midline), `total_length_side_b_um`,
   `density_side_a_per_um = count_side_a / total_length_side_a_um`,
   `density_side_b_per_um = count_side_b / total_length_side_b_um`; (d) classifies each channel
   under each midline as `verdict_symmetric: bool` using
   `SYMMETRY_RATIO_LOW <= count_ratio <= SYMMETRY_RATIO_HIGH`; (e) uses `frozen=True, slots=True`
   dataclass `PerChannelSpatialStats` to hold the per-row record; (f) writes the result to
   `paths.PER_CHANNEL_DENSITY_STATS_CSV` with explicit dtypes and one row per
   `(channel, midline_kind)` combination (3 × 3 = 9 rows). Print to stdout a markdown-formatted
   table of the headline midline (`"soma_x"`) for the three channels showing
   `count_side_a / count_side_b` and `verdict_symmetric`. Inputs read: `synapse_coordinates.csv`.
   Outputs produced: `per_channel_density_stats.csv`.

   **Run with**:

   ```bash
   uv run python -m arf.scripts.utils.run_with_logs \
     --task-id t0050_audit_syn_distribution -- \
     uv run python -u -m tasks.t0050_audit_syn_distribution.code.compute_spatial_stats
   ```

   Expected output: 9-row CSV; stdout shows the per-channel ratio and verdict for the `"soma_x"`
   midline. No expensive operations and no validation-gate baseline applies (the script reads a
   small CSV and computes pandas aggregates locally; the trivial reference is "every record falls
   into exactly one side", which the script asserts via
   `assert count_side_a + count_side_b == count_total`). Satisfies REQ-4, REQ-6, REQ-7, REQ-8.

6. **Create `tasks/t0050_audit_syn_distribution/code/render_figures.py`** that produces three PNGs
   under `paths.IMAGES_DIR`:

   * `syn_x_hist_per_channel.png` — three subplots in a single column (one per channel); each
     subplot is a histogram of the channel's `<chan>_locx_um` from `synapse_coordinates.csv`, with a
     vertical dashed line at the soma-x midline and tick-marks for the alternative midlines. Title
     each subplot with the channel's display name from `CHANNEL_DISPLAY_NAMES`. X-axis label:
     "Synapse x-coordinate (µm)"; Y-axis label: "Synapse count". Use 30 bins. Embed the per-channel
     `count_side_a / count_side_b` ratio in the subplot title.

   * `syn_radial_distance_per_channel.png` — three subplots; for each channel, two overlaid
     histograms (side_a in one colour, side_b in another) of `radial_distance_from_soma_um`
     classified by the `"soma_x"` midline. Add a legend with side labels (`"side_a (x < x_soma)"`
     and `"side_b (x >= x_soma)"`). X-axis: "Radial distance from soma (µm)". Y-axis: "Synapse
     count". Title per subplot: channel display name plus `mean ± SD` for each side.

   * `syn_count_pd_vs_nd_per_channel.png` — single bar chart with x = 3 channels, two bars per
     channel (side_a in one colour, side_b in another), bar height = count. Add the count value
     above each bar. Title: "Per-channel synapse counts by side (midline = x_soma)".

   All three figures: use `matplotlib.pyplot`, set figure DPI to 150, use `plt.tight_layout()`, save
   with `plt.savefig(path, dpi=150, bbox_inches="tight")`, then `plt.close(fig)`. Inputs read:
   `synapse_coordinates.csv` and `per_channel_density_stats.csv`. Outputs produced: three PNG files.

   **Run with**:

   ```bash
   uv run python -m arf.scripts.utils.run_with_logs \
     --task-id t0050_audit_syn_distribution -- \
     uv run python -u -m tasks.t0050_audit_syn_distribution.code.render_figures
   ```

   Expected output: all three PNG files exist under `results/images/`. No validation gate (small
   in-memory plot). Satisfies REQ-5, REQ-10.

7. **Create the answer asset
   `tasks/t0050_audit_syn_distribution/assets/answer/synapse-distribution-audit-deposited-vs-paper/`**
   per `meta/asset_types/answer/specification.md` v2 with these three files:

   * **`details.json`** with `spec_version="2"`,
     `answer_id="synapse-distribution-audit-deposited-vs-paper"`,
     `question="Does the deposited Poleg-Polsky 2016 DSGC's spatial distribution of NMDA, AMPA, and GABA synapses match the paper's text descriptions, and does it explain the t0049 GABA PD/ND symmetry collapse under somatic SEClamp?"`,
     `short_title="Synapse distribution audit: deposited DSGC vs Poleg-Polsky 2016"`,
     `short_answer_path="short_answer.md"`, `full_answer_path="full_answer.md"`, `categories=[]`
     (only project-defined slugs may go here; if a relevant slug exists in `meta/categories/` use
     it, otherwise leave empty), `answer_methods=["code-experiment", "papers"]`,
     `source_paper_ids=[]` (paper is referenced through the dependency on t0046 which catalogued the
     paper rather than via a local paper asset; if t0046 produced a local paper asset, list its ID
     here — re-check `tasks/t0046_.../assets/paper/` during implementation), `source_urls=[]`,
     `source_task_ids=["t0046_reproduce_poleg_polsky_2016_exact", "t0047_validate_pp16_fig3_cond_noise", "t0049_seclamp_cond_remeasure"]`,
     `confidence="high"`, `created_by_task="t0050_audit_syn_distribution"`,
     `date_created="2026-04-25"`.

   * **`short_answer.md`** with the v2 frontmatter (`spec_version: "2"`, `answer_id`,
     `answered_by_task`, `date_answered`) and three mandatory `##` sections in order: `## Question`
     (verbatim repeat from `details.json`), `## Answer` (2-5 sentences, decisive, no inline
     citations — must state the H1 verdict and the structural reason), `## Sources` (bullet list
     of t0046, t0047, t0049 task IDs).

   * **`full_answer.md`** with the v2 frontmatter (including `confidence: "high"`) and these `##`
     sections in order: `## Question`, `## Short Answer`, `## Research Process`,
     `## Evidence from Papers`, `## Evidence from Internet Sources`,
     `## Evidence from Code or Experiments`, `## Synthesis`, `## Limitations`, `## Sources`. The
     body must contain:

     * In `## Research Process`: an explicit paragraph noting that the audit is a measurement on
       t0046's library, no model modification, no SEClamp re-run.
     * In `## Evidence from Code or Experiments`: a "Per-channel spatial-statistics table"
       reproducing the headline `"soma_x"` rows from `per_channel_density_stats.csv` (count_total,
       count_side_a, count_side_b, count_ratio, mean_radial_distance_side_**um,
       mean_path_distance_side***um, density_side**_per_um, verdict_symmetric for each of the 3
       channels); the structural finding (the deposited `gabaMOD = 0.33 + 0.66 * direction` scalar
       applies uniformly to all SAC inhibitory synapses with no spatial threshold — quote
       `dsgc_model_exact.hoc:316-334` and `dsgc_model_exact.hoc:234`); embed the three PNGs via
       `![Per-channel x-coordinate histograms](../../../results/images/syn_x_hist_per_channel.png)`,
       `![Per-channel radial-distance histograms](../../../results/images/syn_radial_distance_per_channel.png)`,
       `![Per-channel side counts](../../../results/images/syn_count_pd_vs_nd_per_channel.png)`.
     * In `## Evidence from Papers`: cite t0046's audit answer
       (`tasks/t0046_.../assets/answer/poleg-polsky-2016-reproduction-audit/full_answer.md:181-184`)
       for the 282-vs-177 BIP synapse-count discrepancy; cite the paper's qualitative claim that
       GABA is ND-asymmetric and BIP is symmetric (paraphrase from t0046's `research_papers.md`).
     * In `## Synthesis`: explicitly state the H1 verdict (SUPPORTED / REJECTED / PARTIAL) with the
       per-channel `count_side_a / count_side_b` ratios as numerical evidence, and reconcile it with
       t0049's PD ~47.47 / ND ~48.04 nS GABA SEClamp symmetry: if the deposited GABA distribution is
       symmetric (count ratio in [0.9, 1.1]) AND the per-synapse gain is uniform via `gabaMOD`, then
       the somatic SEClamp cannot detect any PD/ND asymmetry — H1 is SUPPORTED on both structural
       and numerical grounds. Identify which of the three t0049-flagged candidate mechanisms is
       supported by the spatial audit (mechanism (1) spatial-distribution discrepancy is the
       supported one) and propose the next test (S-0046-05 supplementary PDF retrieval; or a
       follow-up that re-distributes deposited GABA synapses to match paper text).
     * In `## Limitations`: note that the deposited synapse z-coordinate is not stored — z values
       in the audit are taken from the parent section's centroid, not the synapse's `0.5` segment
       specifically; with `nseg=1` (per `RGCmodel.hoc:11824`) this is the correct approximation but
       should be flagged. Also note that paper text descriptions are qualitative; the audit's
       numerical comparison rests on the deposited count ratios alone.

   Inputs read: all three CSVs and the three PNGs from previous steps. Outputs produced: the three
   answer-asset files. Expected output: the asset folder exists with three files. Satisfies REQ-9,
   REQ-11, REQ-12.

   **Note on metrics.json**: per the task description's Verification Criteria, this task does NOT
   measure any registered metric. The four registered metrics (`direction_selectivity_index`,
   `tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse`) all measure dynamic
   AP-rate behaviour from a tuning-curve simulation sweep, not static synapse coordinates. The audit
   is a structural-coordinate measurement; per `arf/styleguide/python_styleguide.md`'s "use None for
   missing data" rule, no metric is force-fit into `metrics.json`. The orchestrator's results step
   will write `metrics.json = {}` (empty object); the audit's numerical findings (per-channel
   counts, ratios, densities) live in `per_channel_density_stats.csv` and are summarised in
   `full_answer.md`. This omission is deliberate.

   **Style enforcement (covers Step 1-7)**: after Step 7 completes, run
   `uv run flowmark --inplace --nobackup tasks/t0050_audit_syn_distribution/plan/plan.md` on any
   edited markdown, then `uv run ruff check --fix . && uv run ruff format . && uv run mypy .` to
   clear any lint or type-check issues. This is the final implementation-style gate. Satisfies
   REQ-13.

## Remote Machines

**None required**. The task runs entirely on local CPU. Justification: the workload is one NEURON
cell-build (~30-60 s, single-threaded), one `simplerun(exptype=1, direction=0)` invocation (~10 s),
and a sequence of pandas / matplotlib operations on a 282-row table. No GPU or remote machine is
needed; provisioning would add overhead with no benefit.

## Assets Needed

* **Library `modeldb_189347_dsgc_exact`** from
  `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/`. Used
  via direct Python imports of t0046's `code/build_cell.py`, `code/run_simplerun.py`,
  `code/constants.py`, `code/neuron_bootstrap.py`. No download is needed; the library is in the
  project repo.
* **NEURON 8.2.7 + NetPyNE 1.1.1 toolchain** from t0007's environment setup. Imported via
  `ensure_neuron_importable()`.
* **t0049's GABA SEClamp values for cross-reference** (PD ~47.47 / ND ~48.04 nS, DSI ≈ -0.006);
  these are stored as constants in `code/constants.py` (Step 2) and not read live from t0049.
* **Paper Poleg-Polsky 2016 (ModelDB 189347)** — qualitative claims paraphrased from t0046's
  `research/research_papers.md`. The audit does not download or re-read the paper.

## Expected Assets

* **1 answer asset** (matches `task.json` `expected_assets.answer = 1`):
  `tasks/t0050_audit_syn_distribution/assets/answer/synapse-distribution-audit-deposited-vs-paper/`
  with `details.json`, `short_answer.md`, `full_answer.md` per
  `meta/asset_types/answer/specification.md` v2. Question framing, per-channel synapse-count +
  spatial-statistics table, embedded x-coordinate histogram (PNG), H1 verdict with numerical
  evidence, synthesis paragraph reconciling t0049 GABA collapse. Confidence: `"high"` (the
  structural finding alone is sufficient evidence; the numerical per-side ratios confirm and
  quantify it).

In addition (not formal asset deliverables but produced under `results/`):

* `results/synapse_coordinates.csv` — per-synapse 17-column raw extraction.
* `results/per_channel_density_stats.csv` — 9 rows (3 channels × 3 midline conventions) of
  spatial statistics.
* `results/images/syn_x_hist_per_channel.png`, `syn_radial_distance_per_channel.png`,
  `syn_count_pd_vs_nd_per_channel.png` — three diagnostic figures referenced from the answer
  asset's `full_answer.md`.

## Time Estimation

* **Research**: complete (research_code.md done, ~estimated 1 hour previously; not part of this
  plan).
* **Implementation (planning step + Steps 1-2 scaffold)**: ~20 min.
* **Implementation (Steps 3-4 cell build + extraction)**: ~5 min coding + ~2 min wall-clock for the
  script run (~60 s build + ~10 s simplerun + ~5 s extraction + ~2 s CSV write).
* **Implementation (Step 5 stats)**: ~15 min coding + ~1 s wall-clock for the script.
* **Implementation (Step 6 figures)**: ~20 min coding + ~5 s wall-clock for the script.
* **Implementation (Step 7 answer asset)**: ~30 min for prose + ~1 min for asset verification.
* **Style + verificator passes**: ~5 min.
* **Total wall-clock for implementation phase**: ~95 min (~1.5 hours), of which ~3 min is machine
  work and the rest is human-or-agent coding/prose. Comfortably under the task description's "1-2
  hours including coding + analysis + answer asset writing" estimate.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| `h.RGC.ON` enumeration order does not match `BIPsyn[idx]` ordering, breaking the index → section map | Low | Blocking (wrong parent section names + wrong path distances) | Step 4 explicitly asserts `bip.get_segment().sec is sex.get_segment().sec is sin.get_segment().sec` for every index. The research_code.md cites t0022, t0029, t0030 as evidence the pattern works. If the assertion fires, fall back to using `syn.get_segment().sec` directly per index (no enumeration of `h.RGC.ON` needed for parent-section lookup). |
| `h.distance(0, h.RGC.soma(0.5))` does not return ~0 (origin not set as expected) | Low | Blocking (wrong path distances) | Step 4 asserts `abs(h.distance(0, h.RGC.soma(0.5))) < 1e-9` immediately after the call. If it fails, inspect whether the soma section is named differently (`h.RGC.soma` vs `h.soma`) and adjust accordingly. |
| `simplerun(exptype=1, direction=0)` triggers the deposited NEURON simulation to take longer than expected because of TSTOP_MS settings | Low | Slows the script by minutes | Use t0046's `run_one_trial()` helper which controls trial duration. If excessive, fall back to `h("placeBIP()")` directly after `build_dsgc()` (research_code.md confirms this is sufficient because `(locx, locy)` are set at construction time). Document the substitution in the answer asset's `## Limitations`. |
| Soma-section name pattern `endswith(".soma")` does not match the deposited convention | Low | Blocking (no soma centroid → no radial distances) | Step 4's `soma_centroid_3d()` helper falls back to `h.RGC.soma` directly (the template attribute, per t0046's `read_synapse_coords()` pattern at `build_cell.py:124-140`). Test the iteration first by printing all `sec.name()` values for sections whose name contains `"soma"`. |
| Paper qualitative claim about GABA ND-asymmetry is not reproducible from t0046's `research_papers.md` (notes are too thin to ground the comparison) | Medium | Weakens the H1 verdict's paper-side evidence | The audit's structural finding (uniform `gabaMOD` scalar) is independent of the paper's exact claim. State the verdict as SUPPORTED on the structural+numerical evidence; note the paper-side limitation in `## Limitations` and recommend the supplementary-PDF fetch (S-0046-05) as the next test. |
| Code-style or mypy violations block commit | Medium | Adds rework time | Run `uv run ruff check --fix . && uv run ruff format . && uv run mypy .` after each milestone (Steps 2, 4, 5, 6) instead of only at the end. The Python style guide is strict; addressing issues incrementally avoids end-of-task crunch. |
| Answer asset verificator rejects `details.json` because category slugs are not pre-registered | Low | Blocks asset acceptance | Leave `categories=[]` (an empty list is valid per the asset spec); add a category later via `add-category` skill if needed. The verificator only warns (AA-W001) on unknown slugs, it does not error. |

## Verification Criteria

* **VC-1 (REQ-1, REQ-2, REQ-3, REQ-4)**: Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0050_audit_syn_distribution -- uv run python -u -m tasks.t0050_audit_syn_distribution.code.extract_coordinates`
  and confirm the script exits with code 0, prints the assertion line
  `"282 synapses extracted; BIP/SACexc/SACinhib parent sections match for all indices"`, and
  produces `results/synapse_coordinates.csv` with exactly 282 data rows and the 17 expected columns.
  Verify with
  `uv run python -c "import pandas as pd; df = pd.read_csv('tasks/t0050_audit_syn_distribution/results/synapse_coordinates.csv'); assert df.shape == (282, 17), df.shape"`.

* **VC-2 (REQ-4, REQ-6, REQ-7, REQ-8)**: Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0050_audit_syn_distribution -- uv run python -u -m tasks.t0050_audit_syn_distribution.code.compute_spatial_stats`
  and confirm exit code 0, stdout contains a markdown table with three rows (one per channel)
  showing `count_side_a / count_side_b` ratios, and produces `results/per_channel_density_stats.csv`
  with 9 rows. Verify with
  `uv run python -c "import pandas as pd; df = pd.read_csv('tasks/t0050_audit_syn_distribution/results/per_channel_density_stats.csv'); assert df.shape[0] == 9, df.shape"`.

* **VC-3 (REQ-5, REQ-10)**: Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0050_audit_syn_distribution -- uv run python -u -m tasks.t0050_audit_syn_distribution.code.render_figures`
  and confirm exit code 0 plus the existence of three PNGs:
  `ls tasks/t0050_audit_syn_distribution/results/images/syn_x_hist_per_channel.png tasks/t0050_audit_syn_distribution/results/images/syn_radial_distance_per_channel.png tasks/t0050_audit_syn_distribution/results/images/syn_count_pd_vs_nd_per_channel.png`
  must succeed (no `No such file or directory` error).

* **VC-4 (REQ-9, REQ-11, REQ-12)**: Confirm the answer asset folder exists and the three files are
  present:
  `ls tasks/t0050_audit_syn_distribution/assets/answer/synapse-distribution-audit-deposited-vs-paper/details.json tasks/t0050_audit_syn_distribution/assets/answer/synapse-distribution-audit-deposited-vs-paper/short_answer.md tasks/t0050_audit_syn_distribution/assets/answer/synapse-distribution-audit-deposited-vs-paper/full_answer.md`.
  Confirm `full_answer.md` contains the H1 verdict word (SUPPORTED, REJECTED, or PARTIAL) by running
  `grep -E "SUPPORTED|REJECTED|PARTIAL" tasks/t0050_audit_syn_distribution/assets/answer/synapse-distribution-audit-deposited-vs-paper/full_answer.md`
  and getting at least one match. Confirm the embedded image references resolve by running
  `grep -E "syn_x_hist_per_channel\.png|syn_radial_distance_per_channel\.png|syn_count_pd_vs_nd_per_channel\.png" tasks/t0050_audit_syn_distribution/assets/answer/synapse-distribution-audit-deposited-vs-paper/full_answer.md`
  and getting at least three matches.

* **VC-5 (REQ-11, asset-spec verification)**: Run the answer-asset verificator (if present):
  `uv run python -u -m arf.scripts.verificators.verify_answer_asset t0050_audit_syn_distribution synapse-distribution-audit-deposited-vs-paper`
  and confirm zero `AA-E*` errors. If the verificator script does not exist in this checkout, fall
  back to direct inspection per the asset spec's mandatory-section list and confirm all required
  sections are present in `short_answer.md` and `full_answer.md`.

* **VC-6 (REQ-13, style)**: Run
  `uv run ruff check . && uv run ruff format --check . && uv run mypy .` from the task worktree root
  and confirm exit code 0 (no lint, format, or type errors).

* **VC-7 (requirement coverage)**: Each of REQ-1 through REQ-13 must be referenced at least once in
  the Step by Step (auto-check by reading this plan; the verificator confirms via PL-W007 that Step
  by Step references `REQ-*` items). Confirmed by inspection: REQ-1 in Step 3; REQ-2 in Step 3;
  REQ-3 in Step 4; REQ-4 in Step 4 and Step 5; REQ-5 in Step 6; REQ-6, REQ-7, REQ-8 in Step 5; REQ-9
  in Step 7; REQ-10 in Step 6; REQ-11, REQ-12 in Step 7; REQ-13 in Steps 1, 2, 7.
