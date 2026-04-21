# Upstream Source Provenance

This directory contains files vendored from the companion code repository for de Rosenroll et al.
2026 (Cell Reports).

## Source

* **Paper DOI**: `10.1016/j.celrep.2025.116833`
* **GitHub**: <https://github.com/geoffder/ds-circuit-ei-microarchitecture>
* **Zenodo DOI**: `10.5281/zenodo.17666158`
* **License**: MIT (see `LICENSE` in this directory)
* **Imported commit**: `a23f642aa6557a23a51bf76f51e420e8149773fa` (tag: release; "add zenodo badge
  to readme")
* **Import date**: 2026-04-21

## Files imported

### NEURON mechanism / morphology (required for simulation)

* `RGCmodelGD.hoc` — 341-section DSGC morphology template (`DSGC` class).
* `HHst_noiseless.mod` — Hodgkin-Huxley stochastic sodium/potassium channel (noise-free variant).
* `cadecay.mod` — calcium decay mechanism.
* `Exp2NMDA.mod` — dual-exponential NMDA receptor with voltage-dependent Mg block.

### Excluded from the import

The simulation port reimplements the upstream Python model from the paper + code description rather
than importing it; only the MOD mechanisms and HOC morphology are needed at runtime. The following
upstream files therefore are NOT vendored here. Re-fetch them from the upstream commit above if a
future task needs them as reference material.

* Upstream `.git/` history.
* Upstream `README.md` (this file replaces it as a provenance record).
* Jupyter notebooks (`*.ipynb`) and figure/asset directories (`assets/`, `thesis_morphology.h5`).
* GUI scripts (`ei_balance_gui.py`, `interactive.py`) and unrelated plotting helpers.
* Python model sources: `ei_balance.py`, `SacNetwork.py`, `NetQuanta.py`, `Rig.py`, `modelUtils.py`,
  `general_utils.py`, `briggman_counts.py`, `hdf_utils.py`, `sac_mode_configs.py`, `experiments.py`.
* `rec_dist_matrix.csv` — precomputed recorder distance matrix, 12.3 MB, exceeds the repo's 5 MB
  per-file threshold.
* `nrnivmodl` build artifacts (`*.c`, `*.o`) — regenerable locally via the `run_nrnivmodl.cmd`
  wrapper at the library root.

## Build

Compile the `.mod` files to `nrnmech.dll` using the task-local wrapper from the library root:

```
cmd /c run_nrnivmodl.cmd
```

The wrapper calls NEURON's `nrnivmodl.bat` with this directory as both the MOD-source directory and
the build directory; on success a `nrnmech.dll` appears next to the `.mod` files.
