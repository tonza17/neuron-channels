---
spec_version: "3"
task_id: "t0024_port_de_rosenroll_2026_dsgc"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-21T03:18:55Z"
completed_at: "2026-04-21T08:10:00Z"
---
## Summary

Ported the de Rosenroll et al. 2026 DSGC circuit into a new library asset `de_rosenroll_2026_dsgc`
(NEURON `HHst_noiseless`/`Exp2NMDA`/`cadecay` MOD mechanisms plus the 341-section `RGCmodelGD.hoc`
morphology, vendored from Zenodo 17666158 at commit `a23f642a`). Built `nrnmech.dll` locally and
wrote seven task modules under `code/` (`paths`, `constants`, `ar2_noise`, `build_cell`,
`run_tuning_curve`, `score_envelope`, `plot_tuning_curves`). Ran the full four-sweep protocol (8-dir
correlated, 8-dir uncorrelated, 12-angle correlated, 12-angle uncorrelated; 20 trials per angle;
wall-time ~4h15m) and scored the output against the REQ-5 port-fidelity envelope.

The port-fidelity gate **failed**: correlated 8-dir DSI 0.818 (required [0.30, 0.50]), uncorrelated
8-dir DSI 0.835 (required [0.18, 0.35]), correlation-drop fraction 0.000 (required >= 0.2). Per plan
step 13, this is a first-class finding — the simplified port (ACh/GABA Exp2Syn pairs per terminal
with AR(2)-modulated Poisson release and a null-biased GABA release probability) captures the
asymmetric-inhibition mechanism but does not reproduce the paper's absolute DSI magnitudes or its
correlated-vs-uncorrelated drop. `score_envelope.py` auto-generated
`intervention/port_fidelity_miss.md` documenting the miss and proposing a SacNetwork follow-up. Task
continues with this result preserved in `results/metrics.json` and `data/score_report.json`.

## Actions Taken

1. Vendored upstream NEURON model (MOD, HOC, Python reference) from
   `geoffder/ds-circuit-ei-microarchitecture` (commit `a23f642a`, MIT, Zenodo
   `10.5281/zenodo.17666158`) into `assets/library/de_rosenroll_2026_dsgc/sources/`; wrote
   `details.json`, `description.md`, `UPSTREAM_NOTES.md`, `run_nrnivmodl.cmd` wrapper.
2. Built `sources/nrnmech.dll` via `run_nrnivmodl.cmd` on the local Windows workstation.
3. Wrote seven code modules: centralized paths in `paths.py`; AR(2) correlated-noise generator in
   `ar2_noise.py` (`phi_1=0.9, phi_2=-0.1, rho_cross=0.6`); SAC-terminal wiring and null-biased GABA
   release in `build_cell.py`; per-trial NEURON driver + CSV emitter in `run_tuning_curve.py`;
   envelope scorer with 8-dir DSI bypass and auto-intervention writer in `score_envelope.py`; polar
   + Cartesian plotter in `plot_tuning_curves.py` (12-angle only, since t0011/t0012 loader hardcodes
     12 angles).
4. Ran `run_tuning_curve.py` for all four conditions (8-dir/12-ang x correlated/uncorrelated, 20
   trials each); sweep finished with exit 0.
5. Ran `score_envelope.py`; produced `data/score_report.json`, wrote `results/metrics.json` with
   four DSI values, two peak-Hz values, `port_fidelity_gate_pass=false`, and (bypassing the 12-ang
   scorer for 8-dir) the REQ-5 envelope verdict; auto-wrote `intervention/port_fidelity_miss.md`.
6. Ran `plot_tuning_curves.py`; produced four PNGs under `results/images/` (polar + Cartesian for
   both 12-angle conditions).
7. Cleaned the library asset: removed `nrnivmodl` build artifacts (`*.c`, `*.o`, regenerable) and
   the 12.3 MB `sources/rec_dist_matrix.csv` (exceeds repo's 5 MB per-file threshold and is not used
   by the port); updated `sources/UPSTREAM_NOTES.md` to document the exclusions.
8. Removed a pre-existing `tuning_curves_8dir_correlated_preflight.csv` smoke-test artifact and the
   `code/__pycache__/` directory.
9. Ran `uv run flowmark --inplace --nobackup` on every modified markdown file and
   `uv run ruff check --fix . && uv run ruff format .` on `tasks/t0024_.../code/`; all clean.

## Outputs

* `tasks/t0024_port_de_rosenroll_2026_dsgc/code/__init__.py`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/code/paths.py`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/code/ar2_noise.py`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/code/score_envelope.py`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/code/plot_tuning_curves.py`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/` (asset root,
  `details.json`, `description.md`, `run_nrnivmodl.cmd`, `sources/` with MOD/HOC/DLL plus vendored
  Python reference)
* `tasks/t0024_port_de_rosenroll_2026_dsgc/data/tuning_curves_{8dir,12ang}_{correlated,uncorrelated}.csv`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/data/score_report.json`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/results/metrics.json`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/results/images/tuning_curve_12ang{,_uncorrelated}{,_cartesian}.png`
* `tasks/t0024_port_de_rosenroll_2026_dsgc/intervention/port_fidelity_miss.md`

## Issues

Port-fidelity gate (REQ-5) failed on all three sub-criteria: correlated DSI (0.818, required
[0.30, 0.50]), uncorrelated DSI (0.835, required [0.18, 0.35]), and correlated-vs-uncorrelated drop
fraction (0.000, required >= 0.2). The miss is expected given the deliberate scope of the port
(per-terminal Exp2Syn pairs with AR(2) Poisson release, no full SAC varicosity network). Recorded as
`intervention/port_fidelity_miss.md` per plan step 13 and preserved in `results/metrics.json` as
`de_rosenroll_port_fidelity_gate_pass=false`. Does not block step closure. Follow-up proposal (port
the full `SacNetwork` with `bp_locs`/`probs`/`deltas`) will be captured in step 14 suggestions.
