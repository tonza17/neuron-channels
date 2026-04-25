---
spec_version: "3"
task_id: "t0050_audit_syn_distribution"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-25T11:42:13Z"
completed_at: "2026-04-25T11:54:07Z"
---
## Summary

Implemented all 7 steps of `plan/plan.md`: scaffold (`paths.py`, `constants.py`), cell build +
synapse-coordinate extraction (`extract_coordinates.py`), per-channel x per-side spatial statistics
under three midline conventions (`compute_spatial_stats.py`), three diagnostic PNGs
(`render_figures.py`), and one answer asset `synapse-distribution-audit-deposited-vs-paper`. The
audit confirms 282 synapses per channel and verifies that all three channels (BIP, SACexc, SACinhib)
share the same parent section for every index. Under the soma_x midline (104.576 μm) the per-side
count split is 171 / 111 (ratio 1.541) for all three channels; under the BIPsyn-locx-median midline
(88.770 μm) the split is 139 / 143 (ratio 0.972, symmetric). H1 is SUPPORTED on both structural
grounds (the deposited PD/ND swap is a uniform `gabaMOD` scalar with no spatial threshold) and
numerical grounds (the intrinsic spatial distribution is symmetric around its own median).

## Actions Taken

1. Created `code/paths.py` and `code/constants.py` with channel kinds, midline rules, t0049
   cross-reference values, and CSV column constants. Verified module imports cleanly.
2. Created `code/extract_coordinates.py` with the `SynapseAuditRecord` dataclass and three helpers
   (`section_centroid_3d`, `soma_centroid_3d`, `extract_synapse_audit`) that wrap t0046's
   `build_dsgc()` and `run_one_trial()`. Initial run failed an `h.distance(0, soma(0.5))` assertion
   (returned 0.5, not 0); switched to NEURON's two-segment `h.distance(soma_seg, syn_seg)` form
   which works correctly and avoids the stateful-origin gotcha. Re-ran successfully producing
   `results/synapse_coordinates.csv` with shape (282, 17).
3. Created `code/compute_spatial_stats.py` producing `results/per_channel_density_stats.csv` with 9
   rows (3 channels x 3 midlines). Soma-x x-coordinate (104.576 μm) is hardcoded from step 2's
   stdout to avoid a second NEURON cell build.
4. Created `code/render_figures.py` producing all three diagnostic PNGs.
5. Created the answer asset `assets/answer/synapse-distribution-audit-deposited-vs-paper/` with
   `details.json`, `short_answer.md`, and `full_answer.md` per
   `meta/asset_types/answer/specification.md` v2.
6. Ran `uv run ruff check --fix` and `uv run ruff format` — fixed `ChannelKind(str, Enum)` to
   `ChannelKind(StrEnum)` (UP042). Ran `uv run mypy .` on the whole repo: 0 errors across 261 source
   files. Ran `uv run flowmark --inplace --nobackup` on both answer-asset markdown files.
7. Verified all four VCs pass: VC-1 (282-row CSV), VC-2 (9-row stats), VC-3 (3 PNGs), VC-4 (verdict
   word "SUPPORTED" in full_answer.md, all 3 image references present).

## Outputs

* `tasks/t0050_audit_syn_distribution/code/paths.py`
* `tasks/t0050_audit_syn_distribution/code/constants.py`
* `tasks/t0050_audit_syn_distribution/code/extract_coordinates.py`
* `tasks/t0050_audit_syn_distribution/code/compute_spatial_stats.py`
* `tasks/t0050_audit_syn_distribution/code/render_figures.py`
* `tasks/t0050_audit_syn_distribution/results/synapse_coordinates.csv` (282 rows x 17 cols)
* `tasks/t0050_audit_syn_distribution/results/per_channel_density_stats.csv` (9 rows x 20 cols)
* `tasks/t0050_audit_syn_distribution/results/images/syn_x_hist_per_channel.png`
* `tasks/t0050_audit_syn_distribution/results/images/syn_radial_distance_per_channel.png`
* `tasks/t0050_audit_syn_distribution/results/images/syn_count_pd_vs_nd_per_channel.png`
* `tasks/t0050_audit_syn_distribution/assets/answer/synapse-distribution-audit-deposited-vs-paper/details.json`
* `tasks/t0050_audit_syn_distribution/assets/answer/synapse-distribution-audit-deposited-vs-paper/short_answer.md`
* `tasks/t0050_audit_syn_distribution/assets/answer/synapse-distribution-audit-deposited-vs-paper/full_answer.md`

## Issues

* The legacy `h.distance(0, soma(0.5))` form returned 0.5 instead of 0 in NEURON 8.2.7 Python
  bindings. Switched to the two-segment form `h.distance(seg1, seg2)` which is more robust and
  documented in the script docstring.
* Ruff initially flagged `ChannelKind(str, Enum)` (UP042) — replaced with `StrEnum` (Python 3.12+
  syntax).
* The `verify_answer_asset.py` script does not exist in this checkout; per VC-5's documented
  fallback, verified the asset by direct inspection (all mandatory sections present in
  short_answer.md and full_answer.md per `meta/asset_types/answer/specification.md` v2).

## Requirement Completion Checklist

| REQ | Status | Result | Evidence |
| --- | --- | --- | --- |
| REQ-1 | done | Re-used t0046's library; no fork or copy | `code/extract_coordinates.py` imports only from `tasks.t0046_reproduce_poleg_polsky_2016_exact.code.*` and adds the audit-specific extraction helper locally. |
| REQ-2 | done | Built cell once via `build_dsgc()`; ran `simplerun(exptype=1, direction=0)` exactly once via `run_one_trial(exptype=ExperimentType.CONTROL, direction=Direction.PREFERRED, trial_seed=1, b2gnmda_override=0.5)` | `code/extract_coordinates.py:`build_cell_and_run_simplerun(); stdout log shows "[build_cell] countON=282 numsyn=282" + "[extract] simplerun completed: peak_psp_mv=25.143". |
| REQ-3 | done | Per-synapse extraction with parent section name, length, centroid (x,y,z), path distance, radial distance | `results/synapse_coordinates.csv` (shape 282 x 17). Columns include `parent_section_name`, `parent_section_length_um`, three centroid columns, `path_distance_um`, `radial_distance_from_soma_um`. |
| REQ-4 | done | Per-channel synapse counts confirmed at 282; PD-side / ND-side split reported numerically | `results/per_channel_density_stats.csv` rows; assertion `len(records) == EXPECTED_NUMSYN == 282` in `extract_coordinates.py` never fires. |
| REQ-5 | done | Per-channel x-position bimodal histograms (PD vs ND) rendered | `results/images/syn_x_hist_per_channel.png` — three subplots (BIP, SACexc, SACinhib) with soma_x dashed line, x=0 dotted line, BIPsyn-median dot-dashed line. |
| REQ-6 | done | Per-channel mean radial distance from soma, broken down by side, mean ± SD | `results/per_channel_density_stats.csv` columns `mean_radial_distance_side_a_um`, `sd_radial_distance_side_a_um`, `..._side_b_um`. Soma_x rows: side_a 64.2 ± 24.5 μm, side_b 49.5 ± 23.4 μm (identical for all three channels). |
| REQ-7 | done | Per-channel mean dendritic-tree path distance from soma, broken down by side, mean ± SD | Same CSV with `mean_path_distance_side_a_um` / `sd_path_distance_side_a_um` and `..._side_b_um`. Soma_x rows: side_a 131.4 ± 46.4 μm, side_b 106.9 ± 47.1 μm. |
| REQ-8 | done | PD-side vs ND-side density (synapses per unit dendritic length per side, per channel) | Same CSV with `total_length_side_a_um` (2942.4 μm), `total_length_side_b_um` (1665.4 μm), `density_side_a_per_um` (0.0581), `density_side_b_per_um` (0.0667). |
| REQ-9 | done | Compared statistics against paper text claims and identified mechanism explaining t0049 GABA collapse | `full_answer.md` `## Evidence from Papers` and `## Synthesis` sections explicitly state the 282-vs-177 BIP discrepancy, the paper's qualitative GABA ND-bias claim, and tie the structural finding (uniform `gabaMOD`) + numerical symmetry (intrinsic ratio 0.972) to the t0049 PD ~47.5 / ND ~48.0 nS GABA collapse. |
| REQ-10 | done | Three PNGs rendered under `results/images/` | `syn_x_hist_per_channel.png`, `syn_radial_distance_per_channel.png`, `syn_count_pd_vs_nd_per_channel.png` all exist. |
| REQ-11 | done | One answer asset produced per `meta/asset_types/answer/specification.md` v2 | `assets/answer/synapse-distribution-audit-deposited-vs-paper/` contains `details.json` + `short_answer.md` + `full_answer.md`; all three files validated by direct inspection against the spec (frontmatter, mandatory sections, source-task references, confidence value). |
| REQ-12 | done | H1 verdict (SUPPORTED) stated with numerical evidence | `full_answer.md` `## Synthesis` section: "The H1 (spatial-distribution) hypothesis is **SUPPORTED**" with per-channel `count_side_a / count_side_b` ratios cited from `per_channel_density_stats.csv`. |
| REQ-13 | done | Python style guide compliance | `uv run ruff check tasks/t0050_audit_syn_distribution/` → all checks passed. `uv run ruff format` → 7 files left unchanged. `uv run mypy .` → 0 issues across 261 source files. Absolute imports throughout, paths centralised in `code/paths.py`, constants in `code/constants.py`, frozen dataclasses, keyword-only args. |
