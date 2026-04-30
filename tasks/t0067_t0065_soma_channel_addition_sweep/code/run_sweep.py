"""Channel-density sweep on the deposited Poleg-Polsky DSGC soma.

For each (channel, density, direction, seed) condition, run a FULL-mode trial on
the t0008 cell with the chosen extra channel inserted on the soma at the chosen
peak conductance density. Captures spike count and peak/baseline Vm; computes
per-condition DSI from FULL trial-mean spike counts.
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
from tasks.t0067_t0065_soma_channel_addition_sweep.code.constants import (
    AP_THRESHOLD_MV,
    BASELINE_WINDOW_MS,
    CHANNEL_DEFS,
    GABA_MOD_ND,
    GABA_MOD_PD,
    INSTABILITY_PEAK_HIGH_MV,
    INSTABILITY_PEAK_LOW_MV,
    METRIC_KEY_DSI,
    N_SEEDS_PER_CONDITION,
    SEED_BASE,
    TSTOP_MS,
    ChannelDef,
    ChannelKind,
    DensityLabel,
    Direction,
)
from tasks.t0067_t0065_soma_channel_addition_sweep.code.paths import (
    DATA_DIR,
    DSI_BY_CONDITION_JSON,
    METRICS_JSON,
    PER_TRIAL_METRICS_JSON,
    RESULTS_DIR,
    T67_NRNMECH_DLL,
)


@dataclass(frozen=True, slots=True)
class TrialKey:
    condition_id: str
    channel: ChannelKind
    density_label: DensityLabel
    density_mS_cm2: float
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


def _enumerate_trials() -> list[TrialKey]:
    """Build the (16 conditions x 2 directions x 5 seeds) = 160 trial schedule."""
    trials: list[TrialKey] = []
    # Baseline (no added channel) condition
    for direction in (Direction.PD, Direction.ND):
        for seed_idx in range(N_SEEDS_PER_CONDITION):
            trials.append(
                TrialKey(
                    condition_id="baseline",
                    channel=ChannelKind.NONE,
                    density_label=DensityLabel.NONE,
                    density_mS_cm2=0.0,
                    direction=direction,
                    seed=SEED_BASE + seed_idx,
                )
            )
    # 5 channels x 3 densities
    for ch in CHANNEL_DEFS:
        for label, density in ch.densities_mS_cm2.items():
            condition_id = f"{ch.suffix.replace('t67', '')}_{label.value}"
            for direction in (Direction.PD, Direction.ND):
                for seed_idx in range(N_SEEDS_PER_CONDITION):
                    trials.append(
                        TrialKey(
                            condition_id=condition_id,
                            channel=ch.kind,
                            density_label=label,
                            density_mS_cm2=density,
                            direction=direction,
                            seed=SEED_BASE + seed_idx,
                        )
                    )
    return trials


def _ensure_t67_dll_loaded(*, h: Any) -> None:
    """Load the t0067-local nrnmech.dll containing the 5 new channel mechanisms.

    NEURON allows multiple ``nrn_load_dll`` calls as long as the loaded DLLs do
    not redefine the same SUFFIX. Our t67 DLL only contains ``nav16t67``,
    ``napt67``, ``nart67``, ``kv3t67``, ``kv4t67`` — none collide with t0008's
    HHst / bipNMDA / SACinhib / SACexc.
    """
    if getattr(_ensure_t67_dll_loaded, "_loaded", False):
        return
    dll_path = str(T67_NRNMECH_DLL).replace("\\", "/")
    rc = h.nrn_load_dll(dll_path)
    assert rc == 1.0, f"h.nrn_load_dll failed for {dll_path} (rc = {rc})"
    _ensure_t67_dll_loaded._loaded = True  # type: ignore[attr-defined]


def _insert_all_channels_with_zero_gbar(*, h: Any, soma: Any) -> None:
    """Insert all 5 mechanisms once on the soma; per-trial we just set gbar."""
    for ch in CHANNEL_DEFS:
        soma.insert(ch.suffix)
        for seg in soma:
            setattr(seg, f"gbar_{ch.suffix}", 0.0)


def _set_active_channel(*, soma: Any, key: TrialKey) -> None:
    """Zero all 5 channel densities, then set the active one (if any)."""
    for ch in CHANNEL_DEFS:
        for seg in soma:
            setattr(seg, f"gbar_{ch.suffix}", 0.0)
    if key.channel == ChannelKind.NONE:
        return
    target_def: ChannelDef | None = None
    for ch in CHANNEL_DEFS:
        if ch.kind == key.channel:
            target_def = ch
            break
    if target_def is None:
        raise ValueError(f"Unknown channel kind: {key.channel}")
    # Density passed in mS/cm^2; NEURON expects S/cm^2 (factor of 1e-3).
    g_s_cm2 = float(key.density_mS_cm2) * 1e-3
    for seg in soma:
        setattr(seg, f"gbar_{target_def.suffix}", g_s_cm2)


def _baseline_v_mv(*, t_ms: NDArray[np.float64], v_mv: NDArray[np.float64]) -> float:
    mask = t_ms < BASELINE_WINDOW_MS
    if not mask.any():
        return float("nan")
    return float(np.mean(v_mv[mask]))


def _run_one_trial(*, h: Any, baseline_coords: list[Any], key: TrialKey) -> TrialOutput:
    """Run one FULL-mode trial with the given channel + density configuration."""
    apply_params(h, seed=key.seed)

    gabamod = GABA_MOD_PD if key.direction == Direction.PD else GABA_MOD_ND
    h.gabaMOD = float(gabamod)
    h.exptype = 1  # HH on (FULL mode)

    h("init_active()")
    h("access RGC.soma")
    h("update()")
    h("placeBIP()")

    # init_active rebinds RGCsomana onto HHst gnabar — we set the new-channel gbars
    # AFTER that step so they survive the rebind.
    _set_active_channel(soma=h.RGC.soma, key=key)

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
        raise RuntimeError(f"No samples recorded for {key}")

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
        "condition_id": output.key.condition_id,
        "channel": output.key.channel.value,
        "density_label": output.key.density_label.value,
        "density_mS_cm2": output.key.density_mS_cm2,
        "direction": output.key.direction.value,
        "seed": output.key.seed,
        "peak_v_mv": output.peak_v_mv,
        "baseline_v_mv": output.baseline_v_mv,
        "spike_count": output.spike_count,
        "n_samples": output.n_samples,
        "is_unstable": output.is_unstable,
    }


def _summarise_by_condition(*, all_trials: list[TrialOutput]) -> list[dict[str, Any]]:
    """Aggregate trials into per-condition mean ± SD records."""
    by_condition: dict[str, list[TrialOutput]] = {}
    for trial in all_trials:
        by_condition.setdefault(trial.key.condition_id, []).append(trial)

    summary: list[dict[str, Any]] = []
    for condition_id, trials in by_condition.items():
        first = trials[0]
        pd_spikes = [t.spike_count for t in trials if t.key.direction == Direction.PD]
        nd_spikes = [t.spike_count for t in trials if t.key.direction == Direction.ND]
        pd_mean = float(np.mean(pd_spikes)) if pd_spikes else 0.0
        pd_sd = float(np.std(pd_spikes, ddof=1)) if len(pd_spikes) > 1 else 0.0
        nd_mean = float(np.mean(nd_spikes)) if nd_spikes else 0.0
        nd_sd = float(np.std(nd_spikes, ddof=1)) if len(nd_spikes) > 1 else 0.0
        denom = pd_mean + nd_mean
        dsi = float((pd_mean - nd_mean) / denom) if denom > 0 else 0.0
        n_unstable = sum(1 for t in trials if t.is_unstable)
        summary.append(
            {
                "condition_id": condition_id,
                "channel": first.key.channel.value,
                "density_label": first.key.density_label.value,
                "density_mS_cm2": first.key.density_mS_cm2,
                "n_trials_pd": len(pd_spikes),
                "n_trials_nd": len(nd_spikes),
                "spike_count_pd_mean": pd_mean,
                "spike_count_pd_sd": pd_sd,
                "spike_count_nd_mean": nd_mean,
                "spike_count_nd_sd": nd_sd,
                "firing_rate_pd_hz": pd_mean,
                "firing_rate_nd_hz": nd_mean,
                "dsi": dsi,
                "n_unstable_trials": n_unstable,
            }
        )
    return summary


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Step 1: build cell once via t0008 (loads t0008's nrnmech.dll).
    print("Building cell via t0008.build_dsgc()...")
    h = build_dsgc()
    baseline_coords = read_synapse_coords(h)

    # Step 2: load t0067-local DLL on top (5 new mechanisms).
    _ensure_t67_dll_loaded(h=h)
    print(f"Loaded t0067 DLL: {T67_NRNMECH_DLL}")

    # Step 3: insert all 5 mechanisms with gbar=0; per-trial we'll set the active one.
    _insert_all_channels_with_zero_gbar(h=h, soma=h.RGC.soma)

    # Step 4: enumerate and run trials.
    trials = _enumerate_trials()
    print(f"Total trials: {len(trials)}")

    sweep_t0 = time.perf_counter()
    outputs: list[TrialOutput] = []
    metrics: list[dict[str, Any]] = []
    for idx, key in enumerate(trials, start=1):
        t0 = time.perf_counter()
        output = _run_one_trial(h=h, baseline_coords=baseline_coords, key=key)
        dt = time.perf_counter() - t0
        outputs.append(output)
        metrics.append(_trial_to_dict(output=output))
        unstable_str = "  UNSTABLE" if output.is_unstable else ""
        print(
            f"[{idx:3d}/{len(trials)}] "
            f"{output.key.condition_id:13s} {output.key.direction.value} "
            f"seed={output.key.seed:2d}  "
            f"peak={output.peak_v_mv:+7.2f} mV  spikes={output.spike_count:3d}  "
            f"[{dt:5.2f}s]{unstable_str}"
        )
        # Incremental save (crash-safe).
        with open(file=PER_TRIAL_METRICS_JSON, mode="w", encoding="utf-8") as f:
            json.dump({"trials": metrics}, f, indent=2)

    sweep_dt = time.perf_counter() - sweep_t0

    # Step 5: per-condition aggregation.
    summary = _summarise_by_condition(all_trials=outputs)
    with open(file=DSI_BY_CONDITION_JSON, mode="w", encoding="utf-8") as f:
        json.dump({"conditions": summary}, f, indent=2)

    # Step 6: registered DSI metric (use baseline DSI for the project metric;
    # per-condition DSIs live in dsi_by_condition.json).
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
