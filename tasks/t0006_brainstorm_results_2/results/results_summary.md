# Results Summary: Brainstorm Session 2

## Summary

Second brainstorming session for the neuron-channels project. Produced seven second-wave task
folders (t0007-t0013) covering NEURON+NetPyNE installation, ModelDB 189347 port plus sibling-model
port, dendritic-diameter calibration, model hunt, response visualisation, tuning-curve scoring, and
morphology source-paper provenance. Filed two suggestion corrections.

## Session Overview

* **Date**: 2026-04-19
* **Context**: First task wave (t0002-t0005) completed. Quantitative targets established (DSI
  0.7-0.85, peak 40-80 Hz, null < 10 Hz, HWHM 60-90°); simulator choice converged on NEURON 8.2.7 +
  NetPyNE 1.1.1; canonical target-tuning-curve dataset generated; baseline morphology
  141009_Pair1DSGC downloaded with two open issues (placeholder radii; ambiguous source paper).
* **Prompt**: Researcher invoked `/human-brainstorm` and laid out a three-step high-level goal:
  install NEURON+NetPyNE, port ModelDB 189347 and similar compartmental DSGC models, then hunt
  literature for missed models, then add response-visualisation and tuning-curve-scoring support
  libraries.

## Decisions

1. **Create t0007: install NEURON 8.2.7 + NetPyNE 1.1.1** — covers S-0003-01. Infrastructure setup;
   compiles MOD files, runs a single-compartment sanity simulation and a NetPyNE wrapper run, files
   an `answer` asset that records exact versions and reproduction steps.
2. **Create t0008: port ModelDB 189347 + similar DSGC compartmental models** — covers S-0002-03 and
   S-0003-02 (merged). Phase A ports Poleg-Polsky & Diamond 2016 as the `dsgc-polegpolsky-2016`
   library, swaps in the calibrated morphology (t0009 dependency), runs 12 angles × 20 trials,
   scores via t0012. Phase B hunts sibling models on ModelDB/SenseLab/OSF/GitHub and ports portable
   ones.
3. **Create t0009: calibrate dendritic diameters on dsgc-baseline-morphology** — covers S-0005-02.
   Research stage picks the taper source (Vaney/Sivyer/Taylor 2012, Poleg-Polsky 2016, or similar);
   produces `dsgc-baseline-morphology-calibrated` dataset asset.
4. **Create t0010: hunt literature + code for missed DSGC models** — systematic search of ModelDB,
   GitHub, Google Scholar forward citations, bioRxiv 2023-2025. Inclusion bar: compartmental DSGC
   models with biophysical detail.
5. **Create t0011: response-visualisation library** — `tuning_curve_viz` with four plotting
   functions (cartesian, polar, multi-model overlay, raster/PSTH). Smoke-tests against
   `target-tuning-curve` (t0004) and t0008 output.
6. **Create t0012: tuning-curve scoring loss library** — covers S-0002-09 (subsumes S-0004-03).
   `tuning_curve_loss.score()` returns a `ScoreReport` dataclass combining DSI, peak, null, and HWHM
   residuals into a weighted-Euclidean scalar loss plus per-target booleans. Identity test
   `score(target, target) == 0.0`.
7. **Create t0013: resolve morphology source-paper provenance** — covers S-0005-01. Downloads both
   candidate Feller-lab 2018 papers, reads Methods sections, files a correction on
   `dsgc-baseline-morphology` setting `source_paper_id` to the winner.
8. **Reject S-0004-03** — redundant with S-0002-09, which covers the same scoring library with more
   complete envelope semantics; t0012 implements the surviving suggestion.
9. **Reprioritise S-0005-04 from HIGH to MEDIUM** — the SWC -> simulator section-translator is
   premature until at least one port (t0008) demonstrates exactly what cross-simulator behaviours
   matter.

## Researcher Preferences Captured

* t0008 must use the calibrated morphology (→ adds t0009 as a blocking dependency).
* t0011 smoke-tests against both `target-tuning-curve` and t0008 output.
* t0012 is implemented as a proper library, not inline ad-hoc checks.
* `project/budget.json` left untouched at `$0` with no paid services.
* Deferred: diameter source choice (Vaney/Sivyer/Taylor 2012 vs Poleg-Polsky 2016 vs other) will be
  decided by t0009's research stage, not pre-selected.

## Metrics

| Metric | Count |
| --- | --- |
| New tasks created | 7 |
| Suggestions covered | 4 (S-0002-03, S-0002-09, S-0003-01, S-0005-01; plus S-0002-04/05/10 implicit via t0009 dependencies) |
| Suggestions rejected | 1 (S-0004-03) |
| Suggestions reprioritized | 1 (S-0005-04 HIGH → MEDIUM) |
| Corrections written | 2 |
| New suggestions added | 0 |

## Verification

| Verificator | Result |
| --- | --- |
| `verify_task_file.py` (t0006-t0013) | PASSED |
| `verify_corrections.py` (t0006) | PASSED |
| `verify_suggestions.py` (t0006) | PASSED |
| `verify_logs.py` (t0006) | PASSED |
| `verify_pr_premerge.py` | PASSED |

## Next Steps

Execute the second wave. t0007, t0009, t0011, t0012, t0013 can run in parallel (independent
dependencies). t0008 waits on t0005, t0007, t0009, t0012. t0010 waits on t0008.

1. **Wave 2a (parallel)**: t0007, t0009, t0012, t0013 (all have only already-completed deps).
2. **Wave 2b**: t0011 after t0004 + t0008 (but t0004 is done, so starts when t0008 done).
3. **Wave 2c**: t0008 after t0007 + t0009 + t0012.
4. **Wave 2d**: t0010 after t0008.
