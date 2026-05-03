"""Plot the Pareto front, hypervolume trajectory, and 3-5 deep-dive cell figures.

Reads ``data/trial_history.parquet`` and ``data/hypervolume_trajectory.csv``,
selects 3-5 representative Pareto cells (highest DSI, highest rate, knee
point), runs deep-dive trials with the per-synapse recorder attached, and
emits PNGs to ``results/images/`` plus per-cell .npz files to
``results/data/``.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import build_dsgc_cell
from tasks.t0076_bedb_dsi_firing_rate_mobo.code import bootstrap as _bootstrap  # noqa: F401
from tasks.t0076_bedb_dsi_firing_rate_mobo.code.apply_params import (
    apply_parameter_vector,
)
from tasks.t0076_bedb_dsi_firing_rate_mobo.code.constants import (
    ANGLES_8DIR_DEG,
    AP_THRESHOLD_MV,
    CELSIUS_DEG_C,
    DT_MS,
    N_PARAMS,
    ND_DIRECTION_DEG,
    PD_DIRECTION_DEG,
    SEED_BASE,
    STEPS_PER_MS,
    TSTOP_MS,
    V_INIT_MV,
    ParameterVector,
)
from tasks.t0076_bedb_dsi_firing_rate_mobo.code.paths import (
    HYPERVOLUME_PNG,
    HYPERVOLUME_TRAJECTORY_CSV,
    IMAGES_DIR,
    PARETO_FRONT_PNG,
    RESULTS_DATA_DIR,
    TRIAL_HISTORY_PARQUET,
    ensure_directories,
)
from tasks.t0076_bedb_dsi_firing_rate_mobo.code.recorder import (
    attach_recorders,
    save_recorders_npz,
)
from tasks.t0076_bedb_dsi_firing_rate_mobo.code.trial_helpers import (
    BASE_ACH_PROB,
    RATE_DT_MS,
    SynapseBundle,
    _bar_arrival_times,
    _count_spikes,
    _gaba_prob_for_direction,
    _rates_to_events,
    _rates_with_ar2_noise,
    setup_synapses_parametric,
)


@dataclass(frozen=True, slots=True)
class DeepDivePick:
    iteration: int
    label: str
    dsi: float
    pd_rate_hz: float
    params_natural: np.ndarray


def _load_history() -> pd.DataFrame:
    return pd.read_parquet(TRIAL_HISTORY_PARQUET)


def _pareto_mask(*, dsi: np.ndarray, rate: np.ndarray) -> np.ndarray:
    """Boolean mask of non-dominated points (maximisation in both)."""
    n = len(dsi)
    mask = np.ones(n, dtype=bool)
    for i in range(n):
        if not mask[i]:
            continue
        dominated_by = (dsi >= dsi[i]) & (rate >= rate[i]) & ((dsi > dsi[i]) | (rate > rate[i]))
        if dominated_by.any():
            mask[i] = False
    return mask


def _select_deep_dives(*, df: pd.DataFrame, k: int) -> list[DeepDivePick]:
    dsi = df["dsi"].to_numpy()
    rate = df["pd_rate_hz"].to_numpy()
    mask = _pareto_mask(dsi=dsi, rate=rate)
    pareto_idx = np.where(mask)[0]
    if len(pareto_idx) == 0:
        return []
    candidates: dict[int, DeepDivePick] = {}
    # Highest DSI.
    i_dsi = pareto_idx[np.argmax(dsi[pareto_idx])]
    candidates[int(i_dsi)] = _row_to_pick(row=df.iloc[i_dsi], label="highest_dsi")
    # Highest rate.
    i_rate = pareto_idx[np.argmax(rate[pareto_idx])]
    candidates[int(i_rate)] = _row_to_pick(row=df.iloc[i_rate], label="highest_rate")
    # Knee: maximise normalised DSI + normalised rate.
    if len(pareto_idx) >= 3:
        ds = dsi[pareto_idx]
        rt = rate[pareto_idx]
        ds_n = (ds - ds.min()) / max(1e-12, ds.max() - ds.min())
        rt_n = (rt - rt.min()) / max(1e-12, rt.max() - rt.min())
        i_knee = pareto_idx[int(np.argmax(ds_n + rt_n))]
        if int(i_knee) not in candidates:
            candidates[int(i_knee)] = _row_to_pick(row=df.iloc[i_knee], label="knee")
    # Pad up to k by walking the front by DSI.
    if len(candidates) < k:
        order = pareto_idx[np.argsort(-dsi[pareto_idx])]
        for idx in order:
            if int(idx) in candidates:
                continue
            candidates[int(idx)] = _row_to_pick(
                row=df.iloc[idx], label=f"pareto_extra_{len(candidates)}"
            )
            if len(candidates) >= k:
                break
    return list(candidates.values())


def _row_to_pick(*, row: pd.Series, label: str) -> DeepDivePick:
    params = np.array(
        [float(row[f"p{i:02d}"]) for i in range(N_PARAMS)],
        dtype=np.float64,
    )
    return DeepDivePick(
        iteration=int(row["iteration"]),
        label=label,
        dsi=float(row["dsi"]),
        pd_rate_hz=float(row["pd_rate_hz"]),
        params_natural=params,
    )


def _plot_pareto_scatter(*, df: pd.DataFrame) -> None:
    ensure_directories()
    dsi = df["dsi"].to_numpy()
    rate = df["pd_rate_hz"].to_numpy()
    mask = _pareto_mask(dsi=dsi, rate=rate)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(dsi[~mask], rate[~mask], s=10, color="lightgrey", label="dominated")
    ax.scatter(dsi[mask], rate[mask], s=40, color="C0", label="Pareto front")
    ax.set_xlabel("DSI")
    ax.set_ylabel("PD firing rate (Hz)")
    ax.set_title("Bed B: DSI vs PD firing rate Pareto front")
    ax.legend(loc="best", frameon=False)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(PARETO_FRONT_PNG, dpi=120)
    plt.close(fig)
    print(f"[plot_pareto] wrote {PARETO_FRONT_PNG}")


def _plot_hypervolume() -> None:
    if not HYPERVOLUME_TRAJECTORY_CSV.exists():
        print(f"[plot_pareto] no HV CSV at {HYPERVOLUME_TRAJECTORY_CSV}; skip")
        return
    hv = pd.read_csv(HYPERVOLUME_TRAJECTORY_CSV)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(hv["iteration"], hv["hypervolume"], color="C2")
    ax.set_xlabel("iteration")
    ax.set_ylabel("hypervolume (DSI x rate Hz, ref=(0,0))")
    ax.set_title("Hypervolume trajectory")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(HYPERVOLUME_PNG, dpi=120)
    plt.close(fig)
    print(f"[plot_pareto] wrote {HYPERVOLUME_PNG}")


def _run_deep_dive_direction(
    *,
    cell: Any,
    bundle: SynapseBundle,
    direction_deg: float,
    seed: int,
) -> tuple[Any, Any, np.ndarray, int]:
    """Run a recorded trial; return (recorders, t_array, v_soma, spike_count)."""
    h = cell.h
    recorders = attach_recorders(h=h, soma=cell.soma, bundle=bundle)

    n_ach = len(bundle.syns_ach)
    n_gaba = len(bundle.syns_gaba)
    n_bins = int(np.ceil(TSTOP_MS / RATE_DT_MS))
    arrival_ach = _bar_arrival_times(
        syn_xy=bundle.syn_xy_ach,
        origin_xy=cell.origin_xy,
        direction_deg=direction_deg,
    )
    arrival_gaba = _bar_arrival_times(
        syn_xy=bundle.syn_xy_gaba,
        origin_xy=cell.origin_xy,
        direction_deg=direction_deg,
    )
    ach_rates, _ = _rates_with_ar2_noise(
        n_syn=n_ach,
        n_bins=n_bins,
        rate_dt_ms=RATE_DT_MS,
        arrival_times_ms=arrival_ach,
        rho=0.6,
        seed=seed,
    )
    _, gaba_rates = _rates_with_ar2_noise(
        n_syn=n_gaba,
        n_bins=n_bins,
        rate_dt_ms=RATE_DT_MS,
        arrival_times_ms=arrival_gaba,
        rho=0.6,
        seed=seed + 7919,
    )
    rng = np.random.default_rng(seed + 1_000_003)
    gaba_prob = _gaba_prob_for_direction(direction_deg)
    ach_events = _rates_to_events(
        rates_hz=ach_rates,
        release_prob=np.full(n_ach, BASE_ACH_PROB),
        rate_dt_ms=RATE_DT_MS,
        rng=rng,
    )
    gaba_events = _rates_to_events(
        rates_hz=gaba_rates,
        release_prob=np.full(n_gaba, gaba_prob),
        rate_dt_ms=RATE_DT_MS,
        rng=rng,
    )

    def _queue() -> None:
        for i, nc in enumerate(bundle.ncs_ach):
            for t in ach_events[i]:
                if t < TSTOP_MS:
                    nc.event(t)
        for i, nc in enumerate(bundle.ncs_gaba):
            for t in gaba_events[i]:
                if t < TSTOP_MS:
                    nc.event(t)

    fih = h.FInitializeHandler(_queue)
    h.celsius = CELSIUS_DEG_C
    h.dt = DT_MS
    h.steps_per_ms = STEPS_PER_MS
    h.v_init = V_INIT_MV
    h.tstop = TSTOP_MS
    h.finitialize(V_INIT_MV)
    _ = fih
    h.run()
    t_arr = np.array(list(recorders.t_rec), dtype=np.float64)
    v_soma_arr = np.array(list(recorders.v_soma), dtype=np.float64)
    spikes = _count_spikes(v_soma_arr, AP_THRESHOLD_MV)
    return recorders, t_arr, v_soma_arr, spikes


def _save_deep_dive(*, pick: DeepDivePick, idx: int) -> None:
    cell = build_dsgc_cell()
    pv = ParameterVector(values=pick.params_natural)
    apply_parameter_vector(cell=cell, params=pv)
    bundle = setup_synapses_parametric(
        cell=cell,
        n_ach=pv.n_ach,
        n_gaba=pv.n_gaba,
        rho_0_ach=pv.rho0_ach,
        lambda_ach_um=pv.lambda_ach_um,
        rho_0_gaba=pv.rho0_gaba,
        lambda_gaba_um=pv.lambda_gaba_um,
        w_ach_us=pv.w_ach_us,
        w_gaba_us=pv.w_gaba_us,
        placer_seed=SEED_BASE + idx,
    )

    # 8-direction tuning curve (10 seeds for cost reasons).
    tuning_means: list[float] = []
    tuning_sems: list[float] = []
    for angle in ANGLES_8DIR_DEG:
        spikes_per_seed: list[int] = []
        for s in range(10):
            seed = SEED_BASE + idx * 1019 + s * 10_007 + int(angle) * 13
            _, _, _, sp = _run_deep_dive_direction(
                cell=cell,
                bundle=bundle,
                direction_deg=float(angle),
                seed=seed,
            )
            spikes_per_seed.append(sp)
        tuning_means.append(float(np.mean(spikes_per_seed)))
        tuning_sems.append(float(np.std(spikes_per_seed) / np.sqrt(10)))

    # PD + ND high-resolution traces (1 seed each, full recorder).
    pd_recorders, t_pd, v_pd, _ = _run_deep_dive_direction(
        cell=cell,
        bundle=bundle,
        direction_deg=PD_DIRECTION_DEG,
        seed=SEED_BASE + idx,
    )
    save_recorders_npz(
        output_path=RESULTS_DATA_DIR / f"deepdive_cell_{idx}_pd.npz",
        recorders=pd_recorders,
        direction_label="pd",
    )
    nd_recorders, t_nd, v_nd, _ = _run_deep_dive_direction(
        cell=cell,
        bundle=bundle,
        direction_deg=ND_DIRECTION_DEG,
        seed=SEED_BASE + idx + 1,
    )
    save_recorders_npz(
        output_path=RESULTS_DATA_DIR / f"deepdive_cell_{idx}_nd.npz",
        recorders=nd_recorders,
        direction_label="nd",
    )

    # Tuning-curve PNG.
    fig, ax = plt.subplots(figsize=(5, 4))
    angles_arr = np.array(ANGLES_8DIR_DEG, dtype=np.float64)
    ax.errorbar(
        angles_arr,
        tuning_means,
        yerr=tuning_sems,
        fmt="o-",
        capsize=3,
        color="C3",
    )
    ax.set_xlabel("direction (deg)")
    ax.set_ylabel("spike count (mean +/- SEM, 10 seeds)")
    ax.set_title(f"Cell #{idx} ({pick.label}) DSI={pick.dsi:.2f} rate={pick.pd_rate_hz:.1f} Hz")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / f"deepdive_cell_{idx}_tuning.png", dpi=120)
    plt.close(fig)

    # Trace PNG: PD vs ND soma Vm.
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(t_pd, v_pd, color="C2", label="PD (0 deg)")
    ax.plot(t_nd, v_nd, color="C1", label="ND (180 deg)", alpha=0.7)
    ax.axhline(AP_THRESHOLD_MV, color="grey", linestyle="--", alpha=0.4)
    ax.set_xlabel("time (ms)")
    ax.set_ylabel("V_soma (mV)")
    ax.set_title(f"Cell #{idx} ({pick.label}) PD vs ND somatic Vm")
    ax.legend(loc="best", frameon=False)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / f"deepdive_cell_{idx}_traces.png", dpi=120)
    plt.close(fig)
    print(f"[plot_pareto] saved deep-dive cell #{idx} ({pick.label})")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-deep-dives", type=int, default=3)
    parser.add_argument("--skip-deep-dives", action="store_true")
    args = parser.parse_args(argv)

    ensure_directories()

    df = _load_history()
    print(f"[plot_pareto] loaded {len(df)} evaluations")

    _plot_pareto_scatter(df=df)
    _plot_hypervolume()

    if args.skip_deep_dives:
        print("[plot_pareto] skip-deep-dives set; done.")
        return 0

    picks = _select_deep_dives(df=df, k=args.n_deep_dives)
    print(f"[plot_pareto] running {len(picks)} deep-dive cells")
    for idx, pick in enumerate(picks):
        _save_deep_dive(pick=pick, idx=idx)

    # Save a JSON index of deep-dive picks.
    index_payload = [
        {
            "idx": idx,
            "label": pick.label,
            "iteration": pick.iteration,
            "dsi": pick.dsi,
            "pd_rate_hz": pick.pd_rate_hz,
        }
        for idx, pick in enumerate(picks)
    ]
    with open(RESULTS_DATA_DIR / "deepdive_index.json", "w", encoding="utf-8") as f:
        json.dump(index_payload, f, indent=2)

    return 0


if __name__ == "__main__":
    sys.exit(main())
