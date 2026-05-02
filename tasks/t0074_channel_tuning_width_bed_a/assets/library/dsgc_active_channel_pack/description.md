---
spec_version: "2"
library_id: "dsgc_active_channel_pack"
documented_by_task: "t0074_channel_tuning_width_bed_a"
date_documented: "2026-05-02"
---
# DSGC Active Channel Pack

## Metadata

* **Name**: DSGC Active Channel Pack
* **Version**: 0.1.0
* **Task**: `t0074_channel_tuning_width_bed_a`
* **Dependencies**: NEURON >= 8.0 (no Python deps beyond the project default)
* **MOD files**: `nav16t74`, `napt74`, `nart74`, `kv3t74`, `kv4t74`, `bk74`, `sk74`, `kv7t74`,
  `cadecay` (SUFFIX `cad`)
* **HOC fork**: `dsgc_model_t74.hoc` (overrides `proc init_active()` to un-zero CaT / CaL)

## Overview

This library bundles nine NEURON mechanisms and one HOC fork required to run active-conductance
sweeps on the deposited Poleg-Polsky DSGC (Bed A, t0008 `modeldb_189347_dsgc`). Five of the channel
mechanisms (Nav1.6, NaP, NaR, Kv3, Kv4) are forked verbatim from the t0067 channel pack with their
NEURON SUFFIX renamed from `*t67` to `*t74` to avoid DLL collision when both libraries are loaded
together. Three new channels (BK / KCa1.1, SK / KCa2, Kv7 / M-current) are vendored fresh from
published ModelDB sources. A single-shell calcium pool (`cad`, Destexhe 1995) is reused verbatim
from t0024's Bed B library to provide [Ca]_i for BK and SK.

The HOC fork makes one targeted edit to Bed A's `init_active` procedure: `RGCcaT` and `RGCcaL` are
changed from zero to 0.0001 S/cm^2 (HHst's reduced-default L- / T-type calcium conductance). Without
this edit the cad calcium pool would see `cai = cainf` indefinitely and the BK / SK biophysics would
be meaningless. The fork is sourced after `build_dsgc()` returns so the existing RGC instance,
synapses, and recorders survive intact.

## API Reference

### NEURON SUFFIXes

All channel SUFFIXes use `NONSPECIFIC_CURRENT i` to avoid USEION conflicts with HHst (which already
declares `USEION na WRITE ina`, `USEION k WRITE ik`, `USEION ca READ eca WRITE ica`). This means
each channel writes a synthetic non-ionic current with its own reversal potential parameter rather
than a true `ina` / `ik`.

* `nav16t74` (Carter-Bean 2009): `RANGE gbar (S/cm2), i`. m^3*h kinetics. V_half_m = -43 mV,
  V_half_h = -65 mV, tau_m = 0.05 ms, tau_h voltage-dependent.
* `napt74` (Magistretti-Alonso 1999): `RANGE gbar, i`. Single-gate m^1, V_half = -50 mV, tau_m = 1
  ms, no inactivation.
* `nart74` (Khaliq 2003 simplified): `RANGE gbar, i`. m^3*h*s, V_half_m = -45 mV, V_half_h = -70 mV,
  V_half_s = -50 mV, tau_s = 12 ms.
* `kv3t74` (Erisir 1999): `RANGE gbar, i`. m^4 fast delayed rectifier, V_half = -15 mV, tau_m = 1
  ms, erev = -85 mV.
* `kv4t74` (Hoffman 1997): `RANGE gbar, i`. m^4*h transient, V_half_m = -50 mV, V_half_h = -78 mV,
  tau_h = 15 ms, erev = -85 mV.
* `bk74` (Mainen-Sejnowski 1996): `USEION ca READ cai; RANGE gbar, i; GLOBAL erev, kd_uM, q10`.
  V_half = -28 mV, K_d = 0.18 uM (Hill exponent 1 on Ca), Q10 = 2.3, tau_m = 1 ms.
* `sk74` (Hay 2011 SK_E2): `USEION ca READ cai; RANGE gbar, i; GLOBAL erev, ec50_uM, hill, tau_m`.
  Voltage-independent, EC50 = 0.43 uM, Hill = 4.8, tau_m = 1 ms.
* `kv7t74` (Hay 2011 Im, Adams 1982 formalism): `RANGE gbar, i; GLOBAL erev, q10, temp`.
  `mAlpha = 3.3e-3 * exp(2.5 * 0.04 * (v + 35))`, `mBeta = 3.3e-3 * exp(-2.5 * 0.04 * (v + 35))`,
  Q10 = 2.3.
* `cad` (Destexhe 1995 formalism): `USEION ca READ ica, cai WRITE cai; RANGE depth, taur, cainf`.
  `depth = 0.1 um, taur = 5 ms, cainf = 2e-4 mM`. Single-shell submembrane Ca pool.

### HOC procedure

* `proc init_active()` (forked): Identical to the deposited Bed A `init_active` except
  `RGCcaT = 0.0001 * active` and `RGCcaL = 0.0001 * active` (vs the original `RGCcaT = 0` and
  `RGCcaL = 0.0`). All other lines verbatim.

### Build script

* `run_nrnivmodl.cmd`: Windows wrapper that calls `C:\Users\md1avn\nrn-8.2.7\bin\nrnivmodl.bat` on
  the `code/mods/` directory and emits `code/build/nrnmech.dll`.

## Usage Examples

```python
from tasks.t0008_port_modeldb_189347.code.build_cell import build_dsgc

# Build Bed A as usual.
h = build_dsgc()

# Source the t0074 forked init_active() (un-zeroes CaT/CaL).
h.load_file(1, "tasks/t0074_channel_tuning_width_bed_a/code/dsgc_model_t74.hoc")

# Load the t0074 nrnmech.dll (registers all 9 mechanisms).
h.nrn_load_dll("tasks/t0074_channel_tuning_width_bed_a/code/build/nrnmech.dll")

# Insert channels on the soma.
soma = h.RGC.soma
soma.insert("cad")          # Calcium pool — only insert when BK or SK active!
soma.insert("bk74")
soma.insert("sk74")
soma.insert("kv7t74")
# ... etc

# Set densities (gbar in S/cm^2).
for seg in soma:
    seg.gbar_bk74 = 1.0e-3   # 1.0 mS/cm^2
    seg.gbar_sk74 = 0.2e-3   # 0.2 mS/cm^2

# Run a trial via t0008 helpers.
h("init_active()")           # Now uses the forked version with un-zeroed CaT/CaL.
h("update()")
h("placeBIP()")
h.finitialize(-65)
h.continuerun(1000)
```

## Dependencies

* NEURON >= 8.0 with `nrnivmodl` available on PATH (compiles MOD files into `nrnmech.dll`).
* No Python dependencies beyond the project default (`numpy`, `pandas`, `matplotlib`).

## Testing

The library is validated by the Stage 2 regression gate in t0074:

```bash
PYTHONIOENCODING=utf-8 \
  uv run python -m arf.scripts.utils.run_with_logs \
    --task-id t0074_channel_tuning_width_bed_a -- \
    uv run python -u -m tasks.t0074_channel_tuning_width_bed_a.code.regression_gate
```

The gate asserts `abs(measured_dsi - 0.7974683544303798) < 1e-3` after inserting all 8 channels on
the soma at gbar = 0 (without `cad`). The gate passed with delta = 0.0 in this task.

End-to-end usage is exercised by `tasks/t0074_channel_tuning_width_bed_a/code/run_sweep.py`, which
runs 2100 trials across 25 conditions and produces `results/metrics_summary.csv` with HWHM,
vector-sum DSI, and RMSE-vs-t0004 for each condition.

## Main Ideas

* **NONSPECIFIC_CURRENT pattern**: All eight channel mechanisms write a synthetic `i` (mA/cm^2)
  rather than a true `ina` / `ik`, so they coexist with HHst's `USEION` declarations without
  conflicts. The trade-off is that membrane current still flows correctly, but no `ek` / `ena`
  consistency is enforced.
* **Conditional cad insertion**: Inserting cad on the soma changes baseline DSI by +1 PD spike per
  trial (DSI 0.7975 -> 0.8095) even with all other channels at gbar = 0. This is because the Ca pool
  subtly modifies HHst's calcium ion flux dynamics. Therefore cad is inserted only for BK / SK
  conditions; baseline and the six non-Ca-dependent channels run without cad.
* **Density grids**: Recommended grids per channel — Nav1.6 (10 / 30 / 90 mS/cm^2), NaP (0.3 / 0.8
  / 2.4), NaR (3 / 8 / 24), Kv3 (7 / 20 / 60), Kv4 (4 / 12 / 36), BK (0.3 / 1.0 / 3.0), SK (0.06 /
  0.2 / 0.6), Kv7 (0.0001 / 0.001 / 0.005). The first five are taken from t0067; BK / SK / Kv7
  follow Mainen-Sejnowski / Hay 2011 ranges.
* **HHst CaT / CaL un-zeroing**: The deposited Bed A HOC sets both calcium currents to zero,
  rendering the cad pool meaningless. The library's HOC fork raises both to 0.0001 S/cm^2 (HHst's
  reduced default), still small enough to keep the t0067 baseline DSI fingerprint intact when cad is
  not inserted, but large enough to provide physical Ca current to the pool.

## Summary

This library packages every NEURON-side artefact required to run active-conductance sweeps on the
deposited Poleg-Polsky DSGC. It bundles eight ion-channel MODs (five forked from t0067 with SUFFIX
renames, three new for BK / SK / Kv7), a calcium-pool MOD reused from t0024, a forked HOC procedure
that un-zeroes the latent CaT and CaL conductances, a Windows compile script, and the registration C
file that wires all nine mechanisms into a single `nrnmech.dll`.

It is consumed by t0074's tuning-width sweep and is intended as the substrate dependency for any
future task that needs to study active conductances on Bed A — including the planned t0075
follow-up that localises Kv7 to the AIS rather than the soma. The library has zero Python
dependencies and is fully reproducible from the published ModelDB sources documented in the
per-mechanism MOD-file header comments.
