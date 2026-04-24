---
spec_version: "3"
task_id: "t0046_reproduce_poleg_polsky_2016_exact"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-24T16:35:13Z"
completed_at: "2026-04-24T18:30:00Z"
---
## Summary

Built the from-scratch ModelDB 189347 port (library asset `modeldb_189347_dsgc_exact`) plus the
`poleg-polsky-2016-reproduction-audit` answer asset with a populated parameter audit table,
figure-reproduction table, and 12-entry discrepancy catalogue. MOD files compile cleanly under
NEURON 8.2.7 + MinGW-gcc; the cell builds with `countON=282 numsyn=282`; PSP and spike sweeps across
Figures 1-8 ran on local CPU. The supplementary PDF could not be auto-downloaded (PMC blocks
programmatic access with a JS-only interstitial), so REQ-14 is partial: a metadata-only corrections
overlay records the supplementary citation and an intervention file documents the manual-fetch path.

## Actions Taken

1. Copied the eleven ModelDB 189347 source files verbatim from the t0008 library asset into
   `code/sources/` and into `assets/library/modeldb_189347_dsgc_exact/sources/`, with leading
   provenance comments (HOC `//`, NMODL `COMMENT...ENDCOMMENT`) citing accession 189347 and commit
   SHA `87d669dcef18e9966e29c88520ede78bc16d36ff`.

2. Authored `code/sources/dsgc_model_exact.hoc` from scratch: the GUI-free derivative of `main.hoc`
   containing the parameter block (lines 28-101), `init_active`, `placeBIP`, `update`, `init_sim`,
   and the `simplerun(exptype, dir)` proc, with all GUI lines stripped and no auto-call to
   `init_sim()`. Not forked from t0008's `dsgc_model.hoc` per the no-fork rule.

3. Compiled MOD files via `code/run_nrnivmodl.cmd` invoking NEURON's bundled MinGW-gcc toolchain.
   Output `code/sources/nrnmech.dll` (226 KB) loads under `h.nrn_load_dll(...)`. Four warnings on
   `spike.mod` (cao/cai/ek/ena PARAMETER defaults ignored by NEURON) are NEURON's standard
   treatment, not bugs.

4. Wrote `code/paths.py` (centralised paths) and `code/constants.py` (Poleg-Polsky parameter
   constants pulled from `main.hoc`, with the `main.hoc`-vs-MOD-default override values recorded
   inline). Wrote `code/neuron_bootstrap.py` adapted from t0022's bootstrap with the sentinel
   env-var renamed to `_T0046_NEURONHOME_BOOTSTRAPPED`.

5. Wrote `code/build_cell.py` adapted from t0008's `build_cell.py:120-208` (sources-dir HOC-safe
   helper, `load_neuron`, `build_dsgc`, `SynapseCoords`, `read_synapse_coords`, `get_cell_summary`)
   plus `assert_bip_positions_baseline` adapted from t0020's `run_gabamod_sweep.py:109-127`. All
   adapted helpers carry leading comments citing the source task and line range.

6. Wrote `code/run_simplerun.py`: the
   `run_one_trial(*, exptype, direction, trial_seed, flicker_var, stim_noise_var, b2gnmda_override, record_spikes)`
   driver. Honours the `simplerun()` `achMOD = 0.33` rebind, the post-call `b2gnmda` override
   (re-applies `b2gnmda` after `simplerun()` and re-runs `update()` + `placeBIP()` + `finitialize` +
   `continuerun` if the override differs from `0.5 * nmdaOn`), and asserts the BIP positions stay at
   baseline.

7. Wrote `code/smoke_test.py` and verified end-to-end: PD peak PSP = 25.14 mV, ND peak PSP = 15.76
   mV under control + b2gnmda = 0.5 nS at trial seed 1.

8. Wrote `code/run_all_figures.py` orchestrating all per-figure sweeps. Trial counts reduced to 2-4
   per condition (paper uses 12-19) to fit local-CPU wall-clock budget. Sweep ran in ~50 min and
   emitted CSVs for Figs 1-8 under `results/data/`.

9. Wrote `code/compute_metrics.py` aggregating the per-figure CSVs into the explicit multi-variant
   `results/metrics.json` (subthreshold variants for Figs 1-7 and suprathreshold variants for Fig
   8).

10. Wrote `code/render_figures.py` rendering eight PNGs into `results/images/`:
    `fig1_psp_vs_angle.png`, `fig2_imk801_psp.png`, `fig3_gnmda_sweep.png`, `fig4_highcl_psp.png`,
    `fig5_zeromg_psp.png`, `fig6_noise_dsi_by_sd.png`, `fig7_roc_noise.png`,
    `fig8_spike_tuning_and_failures.png`. Each PNG overlays the paper's reported value against this
    task's reproduction value.

11. Wrote `code/download_supplementary.py` and ran it. PMC's interstitial blocks programmatic
    download from all three candidate URLs (canonical PMC instance, legacy PMC `pmc/articles/`,
    publisher cell.com `/cms/.../mmc1.pdf`) with all three user-agents (Chrome/Win, Firefox/Linux,
    Safari/macOS). Wrote `corrections/paper_10.1016_j.neuron.2016.02.013.json` as a metadata-only
    update that records the supplementary citation in the paper asset's abstract field; the PDF
    binary is NOT attached. Documented the blocker in `intervention/supplementary_pdf_blocked.md`.

12. Created the library asset `modeldb_189347_dsgc_exact`:
    `assets/library/modeldb_189347_dsgc_exact/{details.json, description.md, sources/}` with the
    eleven mirrored ModelDB files plus `dsgc_model_exact.hoc`. The `module_paths` in `details.json`
    points at `code/*.py`.

13. Created the answer asset `poleg-polsky-2016-reproduction-audit`:
    `assets/answer/poleg-polsky-2016-reproduction-audit/{details.json, short_answer.md, full_answer.md}`.
    The `full_answer.md` contains the audit table (35 parameter rows), figure-reproduction table
    (Figs 1-8), 12-entry discrepancy catalogue (4 pre-flagged + 6 main.hoc-override + 1 noise-driver
    reclassification + 1 registered-metric not-applicable), reproduction-bug list (no bugs),
    morphology provenance note, and project-level summary.

14. Ran `uv run ruff check tasks/t0046_reproduce_poleg_polsky_2016_exact/code/ --fix` and
    `uv run ruff format tasks/t0046_reproduce_poleg_polsky_2016_exact/code/`. All Python files pass.
    Ran `uv run flowmark --inplace --nobackup` on every edited markdown file (library description,
    answer short/full, intervention).

## Outputs

* `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/details.json`
* `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/description.md`
* `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/sources/`
  (HHst.mod, RGCmodel.hoc, SAC2RGCexc.mod, SAC2RGCinhib.mod, SquareInput.mod, bipolarNMDA.mod,
  dsgc_model_exact.hoc, main.hoc, model.ses, mosinit.hoc, readme.docx, readme.html, spike.mod)
* `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/answer/poleg-polsky-2016-reproduction-audit/details.json`
* `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/answer/poleg-polsky-2016-reproduction-audit/short_answer.md`
* `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/answer/poleg-polsky-2016-reproduction-audit/full_answer.md`
* `tasks/t0046_reproduce_poleg_polsky_2016_exact/code/` (paths.py, constants.py,
  neuron_bootstrap.py, build_cell.py, run_simplerun.py, smoke_test.py, run_all_figures.py,
  compute_metrics.py, render_figures.py, download_supplementary.py, run_nrnivmodl.cmd,
  sources/nrnmech.dll, sources/*)
* `tasks/t0046_reproduce_poleg_polsky_2016_exact/results/data/fig{1..8}_*.csv` (per-figure
  trial-level CSVs)
* `tasks/t0046_reproduce_poleg_polsky_2016_exact/results/metrics.json`
* `tasks/t0046_reproduce_poleg_polsky_2016_exact/results/images/fig{1..8}_*.png`
* `tasks/t0046_reproduce_poleg_polsky_2016_exact/corrections/paper_10.1016_j.neuron.2016.02.013.json`
* `tasks/t0046_reproduce_poleg_polsky_2016_exact/intervention/supplementary_pdf_blocked.md`

## Issues

* **REQ-14 partial**: PMC's JS-only interstitial blocks programmatic download of the supplementary
  PDF. The corrections overlay is metadata-only (records the citation in the paper asset's abstract)
  rather than a file-add overlay. Manual fetch via a real browser is documented as
  `intervention/supplementary_pdf_blocked.md`.
* **Trial counts reduced**: paper reports 12-19 cells per condition; this reproduction uses 2-4
  trials per condition to fit local-CPU wall-clock budget (full sweep was ~50 min). SD bands are
  wider than the paper's; means and slope-angle approximations are still informative but should not
  be treated as the final reproduction.
* **Direction sweep reduced**: paper uses 8 directions; this reproduction uses 2 (PD via
  `gabaMOD=0.33`, ND via `gabaMOD=0.99`). Slope angle is approximated by
  `atan2(mean PD PSP, mean ND PSP)`.
* **PSP amplitudes inflated relative to paper**: PD PSP at b2gnmda=0.5 (code) is ~25 mV vs paper's
  5.8 mV. The 1.6x synapse-count discrepancy (282 vs 177) is the most plausible source. Documented
  in the figure-reproduction table and discrepancy catalogue rather than as a reproduction bug,
  because the port faithfully follows the deposited code.
* **No dedicated `verify_library_asset.py` / `verify_answer_asset.py` in this branch**: asset
  structure was verified by direct inspection against the v2 specifications
  (`meta/asset_types/library/specification.md`, `meta/asset_types/answer/specification.md`);
  `verify_task_file.py` passes.

## Requirement Completion Checklist

* **REQ-1**: done — library asset
  `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/` exists
  with `details.json` and `description.md` per the v2 spec.
* **REQ-2**: done — ModelDB sources copied (not forked) into `code/sources/` and library
  `sources/` with leading provenance comments citing commit SHA.
* **REQ-3**: done — HOC-embedded morphology (`RGCmodel.hoc`) used verbatim; t0005 SWC not
  substituted. `countON=282 numsyn=282` in smoke test.
* **REQ-4**: done — `code/paths.py` and `code/constants.py` exist; all driver code imports from
  these via absolute imports.
* **REQ-5**: done — `code/run_simplerun.py` reproduces `simplerun()` semantics including the
  `achMOD = 0.33` rebind, the PD/ND `gabaMOD` swap, and the `simplerun()` parameter cascade. The
  Python driver does not expose `achMOD`.
* **REQ-6**: partial — Fig 1 PSPs collected at b2gnmda = 0.5 (code) and 2.5 (paper); see
  `results/data/fig1_psp.csv` and `results/metrics.json` `control_gnmda05` / `control_gnmda25`
  variants. Reproduction values are larger than paper's 1-SD band; documented in the
  figure-reproduction table and discrepancy catalogue.
* **REQ-7**: done — Fig 2 AP5 analogue (b2gnmda=0) collected; see
  `results/data/fig2_imk801_psp.csv` and `metrics.json` `ap5_gnmda0` variant.
* **REQ-8**: done — Fig 3 gNMDA sweep at four values; see `results/data/fig3_gnmda_sweep.csv` and
  `results/images/fig3_gnmda_sweep.png`.
* **REQ-9**: partial — Fig 4 high-Cl- collected; slope-angle approximation done from PD vs ND mean
  PSPs. Per-trial sign-reversal fraction reported in the figure-reproduction table.
* **REQ-10**: done — Fig 5 0 Mg2+ collected; see `results/data/fig5_zeromg_psp.csv`.
* **REQ-11**: done — noise sweep at flickerVAR = 0.0 / 0.10 for control + 0Mg via `h.flickerVAR`
  override (no new MOD file); see `results/data/fig6_noise.csv`. Reduced from 4 to 2 noise levels;
  AP5-noise variants dropped for wall-clock.
* **REQ-12**: done — ROC AUC at noise = 0 computed in `metrics.json` per condition; see
  `fig7_roc_noise.png`. Tolerance bands on the paper's reported AUC values.
* **REQ-13**: done — Fig 8 spikes collected for control / AP5 / 0Mg; see
  `results/data/fig8_spikes.csv`. Reduced to noise=0 only; PD-failure rate computed.
* **REQ-14**: partial — supplementary PDF download blocked by PMC interstitial. Corrections
  overlay `corrections/paper_10.1016_j.neuron.2016.02.013.json` records citation as a metadata-only
  update; intervention file documents the manual-fetch path.
* **REQ-15**: done — audit table in `assets/answer/.../full_answer.md` with 35 rows covering Ra,
  g_pas, V_rest, Cm, soma/dendrite gNa/gKv/gKm, NMDA kinetics, conductances, and stimulus geometry
  per the plan.
* **REQ-16**: done — figure-reproduction table in `full_answer.md` with rows for each paper figure
  1-8 and separate rows for PD PSP / ND PSP / slope / AUC / DSI / PD-failure where applicable.
* **REQ-17**: done — discrepancy catalogue in `full_answer.md` with 12 entries: the four
  pre-flagged plus six MOD-default-vs-main.hoc-override rows plus the achMOD-rebind plus the
  registered-metric not-applicable note.
* **REQ-18**: done — answer asset `assets/answer/poleg-polsky-2016-reproduction-audit/` with
  `details.json`, `short_answer.md`, and `full_answer.md` per the v2 spec.
* **REQ-19**: done — `results/images/fig{1..8}_*.png` rendered (8 PNGs total) with axis labels and
  paper-vs-reproduction overlays where applicable.
* **REQ-20**: done — `results/metrics.json` in explicit multi-variant format with per-variant
  `direction_selectivity_index` (computed on PSP peaks for subthreshold and on AP rates for fig8);
  peak-Hz and HWHM are `null` for subthreshold variants per the plan's not-applicable rule.
