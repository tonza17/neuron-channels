"""Nav1.6 + Kv3 co-expression rescue sweep on the deposited Poleg-Polsky soma.

For each (condition, direction, seed), run a FULL-mode trial with the configured Nav1.6 and
Kv3 densities on the soma. Captures per-trial spike count + peak/baseline Vm; aggregates DSI
per condition.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray

from tasks.t0008_port_modeldb_189347.code.build_cell import (
    apply_params,
    build_dsgc,
    read_synapse_coords,
)
from tasks.t0008_port_modeldb_189347.code.constants import V_INIT_MV
from tasks.t0068_t0067_nav16_kv3_coexpression_rescue.code.constants import (
    ALL_MECH_SUFFIXES,
    AP_THRESHOLD_MV,
    BASELINE_WINDOW_MS,
    CONDITIONS,
    GABA_MOD_ND,
    GABA_MOD_PD,
    INSTABILITY_PEAK_HIGH_MV,
    INSTABILITY_PEAK_LOW_MV,
    KV3_SUFFIX,
    METRIC_KEY_DSI,
    N_SEEDS_PER_CONDITION,
    NAV16_SUFFIX,
    SEED_BASE,
    TSTOP_MS,
    Condition,
    Direction,
)
from tasks.t0068_t0067_nav16_kv3_coexpression_rescue.code.paths import (
    DATA_DIR,
    DSI_BY_CONDITION_JSON,
    METRICS_JSON,
    PER_TRIAL_METRICS_JSON,
    RESULTS_DIR,
    T68_NRNMECH_DLL,
)


@dataclass(frozen=True, slots=True)
class TrialKey:
    condition: Condition
    direction: Direction
    seed: int


@dataclass(frozen=True, slots=True)
class TrialOutput:
    key: TrialKey
    peak_v_mv: float
    baseline_v_mv: float
    spike_count: int
    n_samples: int
    is_unstable: bool


_T68_LOADED: bool = False


def _ensure_t68_dll_loaded(*, h: Any) -> None:
    global _T68_LOADED
    if _T68_LOADED:
        return
    dll_path = str(T68_NRNMECH_DLL).replace("\\", "/")
    rc = h.nrn_load_dll(dll_path)
    assert rc == 1.0, f"h.nrn_load_dll failed for {dll_path} (rc = {rc})"
    _T68_LOADED = True


def _insert_all_channels_with_zero_gbar(*, soma: Any) -> None:
    for suffix in ALL_MECH_SUFFIXES:
        soma.insert(suffix)
        for seg in soma:
            setattr(seg, f"gbar_{suffix}", 0.0)


def _set_active_channels(*, soma: Any, condition: Condition) -> None:
    """Zero all 5 channel densities, then set Nav1.6 + Kv3 to their target values."""
    for suffix in ALL_MECH_SUFFIXES:
        for seg in soma:
            setattr(seg, f"gbar_{suffix}", 0.0)
    nav16_g = condition.nav16_mS_cm2 * 1e-3
    kv3_g = condition.kv3_mS_cm2 * 1e-3
    for seg in soma:
        setattr(seg, f"gbar_{NAV16_SUFFIX}", nav16_g)
        setattr(seg, f"gbar_{KV3_SUFFIX}", kv3_g)


def _baseline_v_mv(*, t_ms: NDArray[np.float64], v_mv: NDArray[np.float64]) -> float:
    mask = t_ms < BASELINE_WINDOW_MS
    if not mask.any():
        return float("nan")
    return float(np.mean(v_mv[mask]))


def _enumerate_trials() -> list[TrialKey]:
    trials: list[TrialKey] = []
    for cond in CONDITIONS:
        for direction in (Direction.PD, Direction.ND):
            for seed_idx in range(N_SEEDS_PER_CONDITION):
                trials.append(
                    TrialKey(condition=cond, direction=direction, seed=SEED_BASE + seed_idx)
                )
    return trials


def _run_one_trial(*, h: Any, key: TrialKey) -> TrialOutput:
    apply_params(h, seed=key.seed)
    h.gabaMOD = float(GABA_MOD_PD if key.direction == Direction.PD else GABA_MOD_ND)
    h.exptype = 1

    h("init_active()")
    h("access RGC.soma")
    h("update()")
    h("placeBIP()")
    _set_active_channels(soma=h.RGC.soma, condition=key.condition)

    v_rec: Any = h.Vector()
    v_rec.record(h.RGC.soma(0.5)._ref_v)
    t_rec: Any = h.Vector()
    t_rec.record(h._ref_t)
    spike_vec: Any = h.Vector()
    netcon = h.NetCon(h.RGC.soma(0.5)._ref_v, None, sec=h.RGC.soma)
    netcon.threshold = float(AP_THRESHOLD_MV)
    netcon.record(spike_vec)

    h.finitialize(float(V_INIT_MV))
    h.continuerun(float(TSTOP_MS))

    v_arr = np.array(list(v_rec), dtype=np.float64)
    t_arr = np.array(list(t_rec), dtype=np.float64)
    if v_arr.size == 0:
        raise RuntimeError(f"No samples for {key}")

    peak_v = float(v_arr.max())
    baseline_v = _baseline_v_mv(t_ms=t_arr, v_mv=v_arr)
    spike_count = int(spike_vec.size())
    is_unstable = peak_v > INSTABILITY_PEAK_HIGH_MV or peak_v < INSTABILITY_PEAK_LOW_MV
    return TrialOutput(
        key=key,
        peak_v_mv=peak_v,
        baseline_v_mv=baseline_v,
        spike_count=spike_count,
        n_samples=int(v_arr.size),
        is_unstable=is_unstable,
    )


def _trial_to_dict(*, output: TrialOutput) -> dict[str, Any]:
    return {
        "condition_id": output.key.condition.condition_id,
        "nav16_mS_cm2": output.key.condition.nav16_mS_cm2,
        "kv3_mS_cm2": output.key.condition.kv3_mS_cm2,
        "direction": output.key.direction.value,
        "seed": output.key.seed,
        "peak_v_mv": output.peak_v_mv,
        "baseline_v_mv": output.baseline_v_mv,
        "spike_count": output.spike_count,
        "n_samples": output.n_samples,
        "is_unstable": output.is_unstable,
    }


def _summarise_by_condition(*, all_trials: list[TrialOutput]) -> list[dict[str, Any]]:
    by_cond: dict[str, list[TrialOutput]] = {}
    for t in all_trials:
        by_cond.setdefault(t.key.condition.condition_id, []).append(t)
    summary: list[dict[str, Any]] = []
    for cid, trials in by_cond.items():
        first = trials[0]
        pd_spikes = [t.spike_count for t in trials if t.key.direction == Direction.PD]
        nd_spikes = [t.spike_count for t in trials if t.key.direction == Direction.ND]
        pd_mean = float(np.mean(pd_spikes)) if pd_spikes else 0.0
        pd_sd = float(np.std(pd_spikes, ddof=1)) if len(pd_spikes) > 1 else 0.0
        nd_mean = float(np.mean(nd_spikes)) if nd_spikes else 0.0
        nd_sd = float(np.std(nd_spikes, ddof=1)) if len(nd_spikes) > 1 else 0.0
        denom = pd_mean + nd_mean
        dsi = float((pd_mean - nd_mean) / denom) if denom > 0 else 0.0
        summary.append(
            {
                "condition_id": cid,
                "nav16_mS_cm2": first.key.condition.nav16_mS_cm2,
                "kv3_mS_cm2": first.key.condition.kv3_mS_cm2,
                "spike_count_pd_mean": pd_mean,
                "spike_count_pd_sd": pd_sd,
                "spike_count_nd_mean": nd_mean,
                "spike_count_nd_sd": nd_sd,
                "dsi": dsi,
                "n_unstable_trials": sum(1 for t in trials if t.is_unstable),
            }
        )
    return summary


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    print("Building cell via t0008.build_dsgc()...")
    h = build_dsgc()
    _ = read_synapse_coords(h)
    _ensure_t68_dll_loaded(h=h)
    _insert_all_channels_with_zero_gbar(soma=h.RGC.soma)

    trials = _enumerate_trials()
    print(f"Total trials: {len(trials)}")

    sweep_t0 = time.perf_counter()
    outputs: list[TrialOutput] = []
    metrics: list[dict[str, Any]] = []
    for idx, key in enumerate(trials, start=1):
        t0 = time.perf_counter()
        out = _run_one_trial(h=h, key=key)
        dt = time.perf_counter() - t0
        outputs.append(out)
        metrics.append(_trial_to_dict(output=out))
        print(
            f"[{idx:3d}/{len(trials)}] {out.key.condition.condition_id:22s} "
            f"{out.key.direction.value} seed={out.key.seed:2d}  "
            f"peak={out.peak_v_mv:+7.2f}  spikes={out.spike_count:3d}  [{dt:5.2f}s]"
        )
        with open(file=PER_TRIAL_METRICS_JSON, mode="w", encoding="utf-8") as f:
            json.dump({"trials": metrics}, f, indent=2)

    sweep_dt = time.perf_counter() - sweep_t0
    summary = _summarise_by_condition(all_trials=outputs)
    with open(file=DSI_BY_CONDITION_JSON, mode="w", encoding="utf-8") as f:
        json.dump({"conditions": summary}, f, indent=2)

    baseline_dsi = next((s["dsi"] for s in summary if s["condition_id"] == "baseline"), 0.0)
    with open(file=METRICS_JSON, mode="w", encoding="utf-8") as f:
        json.dump({METRIC_KEY_DSI: baseline_dsi}, f, indent=2)

    print(
        f"\nSweep complete: {len(trials)} trials in {sweep_dt:.1f}s "
        f"(mean {sweep_dt / len(trials):.2f}s/trial)"
    )
    print(f"Baseline DSI = {baseline_dsi:.4f}")
    n_unstable = sum(1 for o in outputs if o.is_unstable)
    print(f"Unstable trials: {n_unstable}/{len(trials)}")


if __name__ == "__main__":
    main()
