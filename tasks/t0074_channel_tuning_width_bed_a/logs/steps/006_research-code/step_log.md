---
spec_version: "3"
task_id: "t0074_channel_tuning_width_bed_a"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-01T23:38:06Z"
completed_at: "2026-05-01T23:55:00Z"
---
# Step 6 — Research Code

## Summary

Spawned a `/research-code` subagent to map every code element t0074 depends on (Bed A library
internals, t0067 channel-insertion layer, t0008 12-angle bar-rotation driver, t0024 calcium-pool
MOD, t0011 visualisation library, t0012 tuning-curve loss, t0065 EPSP/IPSP/FULL mode toggle). Three
load-bearing findings emerged: (1) Bed A's `init_active` and CaL/CaT-zeroing live inside the
immutable t0008 library asset (`assets/library/modeldb_189347_dsgc/sources/dsgc_model.hoc:144-145`),
so t0074 must fork the HOC into its own `code/` directory rather than edit in place; (2) t0067's
regression-gate baseline DSI = 0.7974683544303798 came from a 2-direction gabaMOD-swap protocol (NOT
12-angle bar rotation), so the regression gate must also use the 2-direction protocol; (3) the
12-angle bar-rotation driver lives in t0008's `run_tuning_curve.py:56-65` (12 angles, 30 deg step,
20 trials default) and rotates BIP synapse coordinates at `build_cell.py:211-262` — forkable into
t0074's main sweep. The existing `cadecay.mod` from t0024
(`tasks/t0024_*/assets/library/de_rosenroll_2026_dsgc/sources/cadecay.mod`) is a Destexhe-1995
single-shell pool with `taur=5 ms, depth=0.1 um, cainf=2e-4 mM` and composes cleanly with HHst (HHst
writes ica only; cad reads ica, writes cai). Verificator passed with 0 errors and 0 warnings.

## Actions Taken

1. Ran `prestep` for `research-code` to set the step status to `in_progress`.
2. Spawned a `general-purpose` subagent with the `/research-code` skill instruction; passed it the
   worktree path, the task description, the prior `research/research_papers.md` and
   `research/research_internet.md`, and a focused prompt enumerating 6 specific code questions (Bed
   A `init_active` location; t0067 channel-insertion layer + regression-gate protocol; t0024 `cad`
   MOD location; t0011/t0012 entry points; 12-angle bar-rotation driver location).
3. The subagent reviewed `tasks/t0008_*/code/`, `tasks/t0011_*/code/`, `tasks/t0012_*/code/`,
   `tasks/t0024_*/code/`, `tasks/t0046_*/code/`, `tasks/t0047_*/code/`, `tasks/t0065_*/code/`,
   `tasks/t0067_*/code/`, plus the t0008 library asset's bundled HOC and MOD sources, and wrote
   `research/research_code.md` with explicit `tasks/<task_id>/code/<file>:<line>` citations
   throughout.
4. The subagent ran `verify_research_code` via `run_with_logs.py`; PASSED with 0 errors / 0
   warnings.
5. Critical implementation constraints captured:
   * Bed A library assets are immutable; t0074 must fork the HOC into `tasks/t0074/code/` rather
     than edit `tasks/t0008_*/assets/library/.../sources/dsgc_model.hoc` in place.
   * Regression gate must reproduce t0067's 2-direction gabaMOD-swap protocol (FULL mode only, 5
     seeds, GABA_MOD_PD=0.33, GABA_MOD_ND=0.99) with un-zeroed CaL/CaT plus zero-density BK / SK /
     Kv7, targeting baseline DSI = 0.7974683544303798 within 1e-3.
   * Main 12-angle sweep uses t0008's `run_tuning_curve.py` protocol (N_ANGLES=12,
     ANGLE_STEP_DEG=30, synapse-rotation-based bar encoding).
   * EPSP_PASSIVE / IPSP_PASSIVE mode toggling reuses t0065's `_apply_mode_override` pattern.
   * Existing `cadecay.mod` from t0024 is reusable as-is; no new calcium-pool MOD needed.

## Outputs

* `research/research_code.md`

## Issues

No issues encountered. The constraint that Bed A's HOC is inside an immutable library asset is a
non-trivial design implication for the planning step but does not block progress — forking the HOC
into the task's `code/` directory is the standard project pattern (the t0046, t0047, t0067, t0065,
t0066 tasks all do this).
