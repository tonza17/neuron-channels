---
spec_version: "1"
task_id: "t0068_t0067_nav16_kv3_coexpression_rescue"
research_stage: "code"
tasks_reviewed: 2
tasks_cited: 2
libraries_found: 1
libraries_relevant: 1
date_completed: "2026-05-01"
status: "complete"
---
# Research: Code Survey for t0068

## Task Objective

Identify the t0067 code surface that t0068 reuses and the minimal modifications needed to support
simultaneous Nav1.6 + Kv3 density configuration per trial (instead of one channel at a time).

## Library Landscape

Same as t0067: the deposited modeldb_189347_dsgc library asset (cell builder + HHst + bipNMDA
+ SAC mechanisms) plus t0067's vendored 5 channel MOD files. t0068 reuses the t0067 MOD files
  verbatim — same kinetics, same NONSPECIFIC_CURRENT pattern, same suffixes — and recompiles
  them into a t0068-local DLL.

## Methodology Review

Read in full:

* `tasks/t0067_t0065_soma_channel_addition_sweep/code/run_sweep.py` — trial driver with
  `_set_active_channel` (single-channel case).
* `tasks/t0067_t0065_soma_channel_addition_sweep/code/constants.py` — CHANNEL_DEFS.
* `tasks/t0067_t0065_soma_channel_addition_sweep/code/mods/{nav16t67,kv3t67}.mod` — the two
  channels we will co-express.

## Key Findings

### 1. t0067 trial driver structure

* `_set_active_channel(soma, key)` zeros all 5 channels' gbar then sets ONE channel's gbar per
  trial. For t0068 we need to set TWO channels (Nav1.6 + Kv3) — straightforward generalisation:
  take a list of (suffix, density) pairs.
* `_run_one_trial(h, baseline_coords, key)` does the apply_params → gabaMOD → exptype=1 →
  init_active → update → placeBIP → set channel gbars → finitialize → continuerun
  pipeline. Reusable verbatim with the multi-channel set helper swap.

### 2. MOD file reuse

Vendor the same 5 MOD files from `tasks/t0067_*/code/mods/` into `tasks/t0068_*/code/mods/` (copy,
not symlink — for git portability). Compile a t0068-local DLL via the same `run_nrnivmodl.cmd`
script.

### 3. Plot adaptation

t0067 had 5 channels × 3 densities. t0068 has 2 fixed Nav1.6 levels × 4 Kv3 levels (0, low, med,
high) = 8 + baseline = 9 conditions. Plot shape differs:

* `dsi_rescue_curve.png`: x = Kv3 density level (none/low/med/high), y = DSI; two lines (one per
  Nav1.6 level), with horizontal dashed reference for baseline DSI = 0.80.
* `firing_rate_rescue.png`: 2-panel (Nav1.6_med, Nav1.6_high), each showing PD and ND firing rate vs
  Kv3 density.

## Reusable Code and Assets

* t0008 cell builder + HOC template (deposited cell).
* t0067 MOD files (5 — but only Nav1.6 + Kv3 will have non-zero gbar in this task).
* t0067 trial driver pattern (apply_params → gabaMOD → exptype → init_active → ...
  pipeline).
* t0067 idempotent NEURON loader pattern (cached DLL load).

## Lessons Learned

* From t0067: 160 trials in ~10 min wall-clock. 90 trials in t0068 ≈ 5 min.
* From t0067 lifecycle: be careful to commit BEFORE poststep to avoid dirty-tree errors.
* From t0067/t0066: `git checkout -- tasks/t0008/` before each commit to revert any compile
  artefacts that the nrnivmodl run leaves in t0008's source dir.

## Recommendations for This Task

1. Copy 5 MOD files from t0067/code/mods into t0068/code/mods.
2. Compile t0068-local DLL via t0008's run_nrnivmodl.cmd.
3. Rewrite paths.py and constants.py for t0068's 9-condition schema.
4. run_sweep.py: copy t0067's driver, generalise `_set_active_channel` to `_set_active_channels`
   taking `[(suffix, density_S_cm2), ...]`. New `_enumerate_trials()` produces the 9 × 2 × 5 = 90
   trial schedule.
5. plot_results.py: 2 PNGs per Recommendations § 3.

## Task Index

* **t0008_port_modeldb_189347** — cell builder.
* **t0067_t0065_soma_channel_addition_sweep** — primary parent task; MOD files, driver pattern,
  baseline DSI = 0.80, anchor DSIs (Nav1.6_med = 0.48, Nav1.6_high = 0.23).

t0019 was used by t0067 for kinetic priors but is not directly referenced here (t0067's MOD files
already encode those priors).
