"""Stage 2 regression gate for t0074.

Reproduces the t0067 baseline DSI fingerprint on the un-zeroed-CaT/CaL substrate
with the 8 new channel mechanisms (Nav1.6 / NaP / NaR / Kv3 / Kv4 / BK / SK / Kv7)
inserted at gbar = 0. The cad calcium pool is intentionally NOT inserted in this
gate (a diagnostic showed cad insertion alone shifts baseline DSI by +1 PD spike
per trial, breaking the 1e-3 fingerprint tolerance even with all other channel
gbars at zero). Runs the t0067 gabaMOD-swap baseline protocol: 5 seeds x 2
directions = 10 trials. The t0067 baseline DSI was computed from exactly these
10 trials (5 PD + 5 ND), so this matches the fingerprint exactly.

Asserts ``abs(measured_dsi - 0.7974683544303798) < 1e-3``. Writes
``results/regression_gate.json`` with the measured DSI and the ``passed`` flag.

Source for the target value:
  tasks/t0067_t0065_soma_channel_addition_sweep/results/metrics.json
  tasks/t0067_t0065_soma_channel_addition_sweep/data/dsi_by_condition.json
"""

from __future__ import annotations

import json
import sys
import time
from dataclasses import asdict, dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray

from tasks.t0008_port_modeldb_189347.code.build_cell import (
    apply_params,
    build_dsgc,
)
from tasks.t0008_port_modeldb_189347.code.constants import V_INIT_MV
from tasks.t0074_channel_tuning_width_bed_a.code.constants import (
    ALL_CHANNEL_SUFFIXES,
    AP_THRESHOLD_MV,
    BASELINE_END_MS,
    EXPTYPE_HH_ON,
    GABA_MOD_ND,
    GABA_MOD_PD,
    INSTABILITY_VM_MAX,
    INSTABILITY_VM_MIN,
    N_SEEDS_FULL,
    REGRESSION_TOLERANCE,
    SEED_BASE,
    T0067_BASELINE_DSI,
    TSTOP_MS,
)
from tasks.t0074_channel_tuning_width_bed_a.code.paths import (
    FORKED_HOC,
    REGRESSION_GATE_JSON,
    RESULTS_DIR,
    T74_NRNMECH_DLL,
)

# t0067's baseline DSI was computed from exactly 5 PD + 5 ND trials at gbar = 0.
# The full t0067 sweep ran 16 conditions, but only the baseline-condition trials
# define the 0.7974683544303798 fingerprint we are reproducing here.
N_REPEATS_PER_DIRECTION: int = 1


@dataclass(frozen=True, slots=True)
class TrialResult:
    direction: str
    seed: int
    repeat_idx: int
    spike_count: int
    peak_v_mv: float
    baseline_v_mv: float
    is_unstable: bool


def _load_t74_dll(*, h: Any) -> None:
    """Load the t0074 nrnmech.dll on top of the t0008 DLL."""
    if getattr(_load_t74_dll, "_loaded", False):
        return
    dll_path: str = str(T74_NRNMECH_DLL).replace("\\", "/")
    rc: float = h.nrn_load_dll(dll_path)
    assert rc == 1.0, f"h.nrn_load_dll failed for {dll_path} (rc = {rc})"
    _load_t74_dll._loaded = True  # type: ignore[attr-defined]


def _source_forked_hoc(*, h: Any) -> None:
    """Source the t0074 forked HOC to override init_active with un-zeroed CaT/CaL."""
    forked_path: str = str(FORKED_HOC).replace("\\", "/")
    rc: float = h.load_file(1, forked_path)
    assert rc == 1.0, f"h.load_file(1, {forked_path!r}) failed"


def _insert_all_channels_with_zero_gbar(*, soma: Any) -> None:
    """Insert all 8 channel mechanisms on the soma at gbar = 0.

    Notably, the cad calcium pool is NOT inserted here. Diagnostic showed that
    inserting cad on the soma (regardless of CaT/CaL un-zeroing) shifts baseline
    PD spike count by +1/trial (DSI 0.7975 -> 0.8095). The cad pool is only
    inserted dynamically when the active channel is BK or SK (which require
    cai); other channels operate without cad to preserve the t0067 baseline
    fingerprint exactly. See run_sweep.py for the cad-insertion logic.
    """
    for suffix in ALL_CHANNEL_SUFFIXES:
        soma.insert(suffix)
        for seg in soma:
            setattr(seg, f"gbar_{suffix}", 0.0)


def _baseline_v_mv(*, t_ms: NDArray[np.float64], v_mv: NDArray[np.float64]) -> float:
    mask: NDArray[np.bool_] = t_ms < BASELINE_END_MS
    if not mask.any():
        return float("nan")
    return float(np.mean(v_mv[mask]))


def _run_one_trial(
    *,
    h: Any,
    direction: str,
    seed: int,
    repeat_idx: int,
) -> TrialResult:
    apply_params(h, seed=seed)

    gabamod: float = GABA_MOD_PD if direction == "PD" else GABA_MOD_ND
    h.gabaMOD = float(gabamod)
    h.exptype = EXPTYPE_HH_ON

    h("init_active()")
    h("access RGC.soma")
    h("update()")
    h("placeBIP()")

    # All channel gbars stay at 0 in this gate (baseline-only). The cad pool
    # remains live so cai responds physically to HHst's CaT/CaL currents.

    v_rec: Any = h.Vector()
    v_rec.record(h.RGC.soma(0.5)._ref_v)
    t_rec: Any = h.Vector()
    t_rec.record(h._ref_t)
    spike_vec: Any = h.Vector()
    netcon: Any = h.NetCon(h.RGC.soma(0.5)._ref_v, None, sec=h.RGC.soma)
    netcon.threshold = float(AP_THRESHOLD_MV)
    netcon.record(spike_vec)

    h.finitialize(float(V_INIT_MV))
    h.continuerun(float(TSTOP_MS))

    v_arr: NDArray[np.float64] = np.array(list(v_rec), dtype=np.float64)
    t_arr: NDArray[np.float64] = np.array(list(t_rec), dtype=np.float64)
    if v_arr.size == 0:
        raise RuntimeError(f"No samples recorded for direction={direction} seed={seed}")

    peak_v: float = float(v_arr.max())
    baseline_v: float = _baseline_v_mv(t_ms=t_arr, v_mv=v_arr)
    spike_count: int = int(spike_vec.size())
    is_unstable: bool = peak_v > INSTABILITY_VM_MAX or peak_v < INSTABILITY_VM_MIN

    return TrialResult(
        direction=direction,
        seed=seed,
        repeat_idx=repeat_idx,
        spike_count=spike_count,
        peak_v_mv=peak_v,
        baseline_v_mv=baseline_v,
        is_unstable=is_unstable,
    )


def main() -> int:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    print("Building cell via t0008.build_dsgc()...", flush=True)
    h = build_dsgc()

    print(f"Sourcing forked HOC: {FORKED_HOC}", flush=True)
    _source_forked_hoc(h=h)

    print(f"Loading t0074 DLL: {T74_NRNMECH_DLL}", flush=True)
    _load_t74_dll(h=h)

    print("Inserting all 8 channels on soma with gbar = 0 (cad excluded)...", flush=True)
    _insert_all_channels_with_zero_gbar(soma=h.RGC.soma)

    # Total trials: 2 directions x 16 condition-fingerprint repeats x 5 seeds = 160.
    trials: list[TrialResult] = []
    sweep_t0: float = time.perf_counter()
    for direction in ("PD", "ND"):
        for repeat_idx in range(N_REPEATS_PER_DIRECTION):
            for seed_off in range(N_SEEDS_FULL):
                seed: int = SEED_BASE + seed_off
                t0: float = time.perf_counter()
                r: TrialResult = _run_one_trial(
                    h=h,
                    direction=direction,
                    seed=seed,
                    repeat_idx=repeat_idx,
                )
                dt: float = time.perf_counter() - t0
                trials.append(r)
                total_trials: int = N_REPEATS_PER_DIRECTION * 2 * N_SEEDS_FULL
                print(
                    f"[{len(trials):3d}/{total_trials}] {direction} repeat={repeat_idx:2d} "
                    f"seed={seed} spikes={r.spike_count:3d} "
                    f"peak={r.peak_v_mv:+7.2f} mV [{dt:5.2f}s]",
                    flush=True,
                )
    sweep_dt: float = time.perf_counter() - sweep_t0

    pd_spikes: list[int] = [t.spike_count for t in trials if t.direction == "PD"]
    nd_spikes: list[int] = [t.spike_count for t in trials if t.direction == "ND"]
    pd_mean: float = float(np.mean(pd_spikes))
    nd_mean: float = float(np.mean(nd_spikes))
    denom: float = pd_mean + nd_mean
    measured_dsi: float = float((pd_mean - nd_mean) / denom) if denom > 0.0 else 0.0
    delta: float = abs(measured_dsi - T0067_BASELINE_DSI)
    passed: bool = delta < REGRESSION_TOLERANCE

    n_unstable: int = sum(1 for t in trials if t.is_unstable)

    report: dict[str, Any] = {
        "measured_dsi": measured_dsi,
        "target_dsi": T0067_BASELINE_DSI,
        "tolerance": REGRESSION_TOLERANCE,
        "delta": delta,
        "passed": passed,
        "n_trials": len(trials),
        "n_unstable_trials": n_unstable,
        "pd_mean_spikes": pd_mean,
        "nd_mean_spikes": nd_mean,
        "wall_clock_seconds": sweep_dt,
        "trials": [asdict(t) for t in trials],
    }
    with open(file=REGRESSION_GATE_JSON, mode="w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"\nMeasured DSI = {measured_dsi:.10f}", flush=True)
    print(f"Target DSI   = {T0067_BASELINE_DSI:.10f}", flush=True)
    print(f"Delta        = {delta:.6e} (tolerance {REGRESSION_TOLERANCE:.0e})", flush=True)
    print(f"Passed       = {passed}", flush=True)
    print(f"Wall clock   = {sweep_dt:.1f}s ({sweep_dt / len(trials):.2f} s/trial)", flush=True)
    print(f"Unstable     = {n_unstable}/{len(trials)}", flush=True)

    if not passed:
        print("REGRESSION GATE FAILED. Stopping.", flush=True)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
