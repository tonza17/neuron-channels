"""Run 24 per-direction NEURON simulations with extended recording.

For each of the 3 target cells (767, 637, 762) and each of 8 stimulus directions,
records: Vm at soma / mid-dendrite / distal dendrite / AIS; NMDA conductance at
all synapses; Nav1.6 and NaP current density at the representative terminal dendrite.

Saves one .npz per (cell, direction) and one summary JSON per cell to
``results/data/``.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code import (
    bootstrap as _bootstrap,  # noqa: F401
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params import (
    apply_parameter_vector,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.build_cell_ais import (
    DSGCCellWithAIS,
    build_dsgc_cell_with_ais,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import (
    ANGLES_8DIR_DEG,
    AP_THRESHOLD_MV,
    CELSIUS_DEG_C,
    DT_MS,
    ND_DIRECTION_DEG,
    PD_DIRECTION_DEG,
    SEED_BASE,
    STEPS_PER_MS,
    TSTOP_MS,
    V_INIT_MV,
    ParameterVector,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_helpers import (
    BASE_ACH_PROB,
    RATE_DT_MS,
    SynapseBundle,
    _bar_arrival_times,
    _gaba_prob_for_direction,
    _rates_to_events,
    _rates_with_ar2_noise,
    setup_synapses_parametric,
)
from tasks.t0084_t0081_cell_767_vm_trace_deepdive.code.constants import (
    CELL_IDS,
    RECORD_DT_MS,
)
from tasks.t0084_t0081_cell_767_vm_trace_deepdive.code.paths import (
    ALL_EVALUATIONS_JSON,
    RESULTS_DATA_DIR,
    ensure_directories,
)

RHO_CORRELATED: float = 0.6


@dataclass(frozen=True, slots=True)
class CellEntry:
    cell_id: int
    generation: int
    dsi_original: float
    pd_rate_hz_original: float
    params: list[float]


@dataclass(frozen=True, slots=True)
class DirectionResult:
    cell_id: int
    direction_deg: float
    spike_count: int
    peak_vm_mv: float
    is_stable: bool


def _load_cell_entries(cell_ids: tuple[int, ...]) -> dict[int, CellEntry]:
    """Load parameter vectors for target cells from t0081 all_evaluations.json."""
    raw: list[dict[str, Any]] = json.loads(ALL_EVALUATIONS_JSON.read_text(encoding="utf-8"))
    entries: dict[int, CellEntry] = {}
    for record in raw:
        cid: int = int(record["cell_index"])
        if cid in cell_ids:
            entries[cid] = CellEntry(
                cell_id=cid,
                generation=int(record["generation"]),
                dsi_original=float(record["dsi"]),
                pd_rate_hz_original=float(record["pd_rate_hz"]),
                params=list(record["params"]),
            )
    missing: list[int] = [c for c in cell_ids if c not in entries]
    assert len(missing) == 0, f"Cells not found in all_evaluations.json: {missing}"
    return entries


def _count_spikes_arr(v_arr: NDArray[np.float64], threshold_mv: float) -> int:
    """Count threshold crossings (upward) in a Vm trace."""
    crossings: NDArray[np.bool_] = (v_arr[:-1] < threshold_mv) & (v_arr[1:] >= threshold_mv)
    return int(np.sum(crossings))


def _hash_param_vector(values: NDArray[np.float64]) -> int:
    return hash(values.tobytes())


def _run_one_direction_with_recording(
    *,
    cell: DSGCCellWithAIS,
    bundle: SynapseBundle,
    direction_deg: float,
    seed: int,
    sec_mid: Any,
    sec_distal: Any,
) -> dict[str, Any]:
    """Run one simulation with extended recording; return dict of numpy arrays.

    Inlines the h.run() loop from trial_driver.run_one_trial to allow attaching
    Vector.record() handles before h.run() is called — NEURON vectors cannot
    cross process boundaries so this must run in-process.
    """
    h: Any = cell.h
    n_ach: int = len(bundle.syns_ach)
    n_gaba: int = len(bundle.syns_gaba)
    n_bins: int = int(np.ceil(TSTOP_MS / RATE_DT_MS))

    arrival_ach: NDArray[np.float64] = _bar_arrival_times(
        syn_xy=bundle.syn_xy_ach,
        origin_xy=cell.origin_xy,
        direction_deg=direction_deg,
    )
    arrival_gaba: NDArray[np.float64] = _bar_arrival_times(
        syn_xy=bundle.syn_xy_gaba,
        origin_xy=cell.origin_xy,
        direction_deg=direction_deg,
    )

    ach_rates, _ = _rates_with_ar2_noise(
        n_syn=n_ach,
        n_bins=n_bins,
        rate_dt_ms=RATE_DT_MS,
        arrival_times_ms=arrival_ach,
        rho=RHO_CORRELATED,
        seed=seed,
    )
    _, gaba_rates = _rates_with_ar2_noise(
        n_syn=n_gaba,
        n_bins=n_bins,
        rate_dt_ms=RATE_DT_MS,
        arrival_times_ms=arrival_gaba,
        rho=RHO_CORRELATED,
        seed=seed + 7919,
    )

    gaba_prob: float = _gaba_prob_for_direction(direction_deg)
    ach_probs: NDArray[np.float64] = np.full(n_ach, BASE_ACH_PROB, dtype=np.float64)
    gaba_probs: NDArray[np.float64] = np.full(n_gaba, gaba_prob, dtype=np.float64)
    rng: np.random.Generator = np.random.default_rng(seed + 1_000_003)

    ach_events: list[NDArray[np.float64]] = _rates_to_events(
        rates_hz=ach_rates,
        release_prob=ach_probs,
        rate_dt_ms=RATE_DT_MS,
        rng=rng,
    )
    gaba_events: list[NDArray[np.float64]] = _rates_to_events(
        rates_hz=gaba_rates,
        release_prob=gaba_probs,
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

    fih: Any = h.FInitializeHandler(_queue)

    # --- Attach recording vectors ---
    t_vec: Any = h.Vector()
    t_vec.record(h._ref_t, RECORD_DT_MS)

    v_soma_vec: Any = h.Vector()
    v_soma_vec.record(cell.soma(0.5)._ref_v, RECORD_DT_MS)

    v_mid_vec: Any = h.Vector()
    v_mid_vec.record(sec_mid(0.5)._ref_v, RECORD_DT_MS)

    v_distal_vec: Any = h.Vector()
    v_distal_vec.record(sec_distal(0.5)._ref_v, RECORD_DT_MS)

    v_ais_vec: Any = h.Vector()
    v_ais_vec.record(cell.ais_distal(0.5)._ref_v, RECORD_DT_MS)

    # NMDA conductance: one vector per synapse
    g_nmda_vecs: list[Any] = []
    for nmda_syn in bundle.syns_nmda:
        vec: Any = h.Vector()
        vec.record(nmda_syn._ref_g, RECORD_DT_MS)
        g_nmda_vecs.append(vec)

    # Nav1.6 and NaP currents: one vector per segment of the distal section
    segs_distal: list[Any] = list(sec_distal)
    i_nav16_vecs: list[Any] = []
    i_nap_vecs: list[Any] = []
    for seg in segs_distal:
        vec_nav: Any = h.Vector()
        vec_nav.record(seg.nav16t80._ref_i, RECORD_DT_MS)
        i_nav16_vecs.append(vec_nav)
        vec_nap: Any = h.Vector()
        vec_nap.record(seg.napt80._ref_i, RECORD_DT_MS)
        i_nap_vecs.append(vec_nap)

    # --- Run simulation ---
    h.celsius = CELSIUS_DEG_C
    h.dt = DT_MS
    h.steps_per_ms = STEPS_PER_MS
    h.v_init = V_INIT_MV
    h.tstop = TSTOP_MS
    h.finitialize(V_INIT_MV)
    _ = fih  # keep reference so it is not garbage-collected before run
    h.run()

    # --- Harvest vectors ---
    t_arr: NDArray[np.float64] = np.array(t_vec.to_python(), dtype=np.float64)
    v_soma_arr: NDArray[np.float64] = np.array(v_soma_vec.to_python(), dtype=np.float64)
    v_mid_arr: NDArray[np.float64] = np.array(v_mid_vec.to_python(), dtype=np.float64)
    v_distal_arr: NDArray[np.float64] = np.array(v_distal_vec.to_python(), dtype=np.float64)
    v_ais_arr: NDArray[np.float64] = np.array(v_ais_vec.to_python(), dtype=np.float64)

    g_nmda_arr: NDArray[np.float64] = np.stack(
        [np.array(v.to_python(), dtype=np.float64) for v in g_nmda_vecs],
        axis=0,
    )  # shape (n_nmda_syns, n_timepoints)

    i_nav16_arr: NDArray[np.float64] = np.stack(
        [np.array(v.to_python(), dtype=np.float64) for v in i_nav16_vecs],
        axis=0,
    )  # shape (n_segs_distal, n_timepoints)

    i_nap_arr: NDArray[np.float64] = np.stack(
        [np.array(v.to_python(), dtype=np.float64) for v in i_nap_vecs],
        axis=0,
    )  # shape (n_segs_distal, n_timepoints)

    return {
        "t_arr": t_arr,
        "v_soma_arr": v_soma_arr,
        "v_mid_arr": v_mid_arr,
        "v_distal_arr": v_distal_arr,
        "v_ais_arr": v_ais_arr,
        "g_nmda_arr": g_nmda_arr,
        "i_nav16_arr": i_nav16_arr,
        "i_nap_arr": i_nap_arr,
    }


def run_cell(
    *,
    cell: DSGCCellWithAIS,
    entry: CellEntry,
) -> list[DirectionResult]:
    """Run all 8 directions for one cell; save .npz files."""
    pv: ParameterVector = ParameterVector(values=np.array(entry.params, dtype=np.float64))
    apply_parameter_vector(cell=cell, params=pv)

    placer_seed: int = SEED_BASE + (_hash_param_vector(pv.values) & 0xFFFF)
    bundle: SynapseBundle = setup_synapses_parametric(
        cell=cell,
        n_ach=pv.n_ach,
        n_gaba=pv.n_gaba,
        rho_0_ach=pv.rho0_ach,
        lambda_ach_um=pv.lambda_ach_um,
        rho_0_gaba=pv.rho0_gaba,
        lambda_gaba_um=pv.lambda_gaba_um,
        w_ach_us=pv.w_ach_us,
        w_gaba_us=pv.w_gaba_us,
        placer_seed=placer_seed,
        gnmda_dend=pv.gnmda_dend,
        mg_conc_mm=pv.mg_conc_mm,
        voff_nmda=pv.voff_nmda,
    )

    sec_mid: Any = cell.non_terminal_dends[0]
    sec_distal: Any = cell.terminal_dends[0]

    # Compute section area for unit conversion (mA/cm² → nA).
    # area = L * pi * diam * 1e-8 cm² (L and diam in um)
    sec_L_um: float = float(sec_distal.L)
    sec_diam_um: float = float(list(sec_distal)[0].diam)
    sec_area_cm2: float = sec_L_um * math.pi * sec_diam_um * 1e-8

    results: list[DirectionResult] = []
    seed: int = SEED_BASE

    for direction in ANGLES_8DIR_DEG:
        direction_f: float = float(direction)
        rec: dict[str, Any] = _run_one_direction_with_recording(
            cell=cell,
            bundle=bundle,
            direction_deg=direction_f,
            seed=seed,
            sec_mid=sec_mid,
            sec_distal=sec_distal,
        )

        t_arr = rec["t_arr"]
        v_soma_arr = rec["v_soma_arr"]
        v_ais_arr = rec["v_ais_arr"]

        # Stability check
        is_stable: bool = bool(
            np.all(np.isfinite(v_soma_arr)) and np.all(np.isfinite(rec["v_distal_arr"]))
        )

        spike_count: int = _count_spikes_arr(v_soma_arr, AP_THRESHOLD_MV)
        peak_mv: float = float(v_soma_arr.max()) if v_soma_arr.size > 0 else float("nan")

        # Save .npz
        npz_path: Path = RESULTS_DATA_DIR / f"cell{entry.cell_id}_dir{int(direction)}_traces.npz"
        np.savez_compressed(
            npz_path,
            t_ms=t_arr,
            v_soma_mv=v_soma_arr,
            v_mid_mv=rec["v_mid_arr"],
            v_distal_mv=rec["v_distal_arr"],
            v_ais_mv=v_ais_arr,
            g_nmda_us=rec["g_nmda_arr"],
            i_nav16_ma_cm2=rec["i_nav16_arr"],
            i_nap_ma_cm2=rec["i_nap_arr"],
            direction_deg=np.array(direction_f),
            cell_id=np.array(entry.cell_id),
            sec_area_cm2=np.array(sec_area_cm2),
        )

        results.append(
            DirectionResult(
                cell_id=entry.cell_id,
                direction_deg=direction_f,
                spike_count=spike_count,
                peak_vm_mv=peak_mv,
                is_stable=is_stable,
            )
        )
        print(
            f"  [cell {entry.cell_id} dir {int(direction):3d}°] "
            f"spikes={spike_count}  peak={peak_mv:.1f} mV  stable={is_stable}",
            flush=True,
        )

    # Save per-cell summary
    pd_results = [r for r in results if abs(r.direction_deg - PD_DIRECTION_DEG) < 1e-6]
    nd_results = [r for r in results if abs(r.direction_deg - ND_DIRECTION_DEG) < 1e-6]
    pd_spikes: float = float(pd_results[0].spike_count) if pd_results else 0.0
    nd_spikes: float = float(nd_results[0].spike_count) if nd_results else 0.0
    pd_rate_hz: float = pd_spikes / (TSTOP_MS / 1000.0)
    nd_rate_hz: float = nd_spikes / (TSTOP_MS / 1000.0)
    denom: float = pd_spikes + nd_spikes
    dsi_measured: float = 0.0 if denom <= 0.0 else (pd_spikes - nd_spikes) / denom

    summary: dict[str, Any] = {
        "cell_id": entry.cell_id,
        "generation": entry.generation,
        "dsi_original": entry.dsi_original,
        "pd_rate_hz_original": entry.pd_rate_hz_original,
        "dsi_measured": dsi_measured,
        "pd_rate_hz_measured": pd_rate_hz,
        "nd_rate_hz_measured": nd_rate_hz,
        "v3_params": {
            "gnmda_dend": pv.gnmda_dend,
            "mg_conc_mm": pv.mg_conc_mm,
            "voff_nmda": pv.voff_nmda,
            "nav16_dend_distal": pv.nav16_dend_distal,
            "nap_dend_distal": pv.nap_dend_distal,
        },
        "recording_sections": {
            "soma": str(cell.soma),
            "mid": str(sec_mid),
            "distal": str(sec_distal),
        },
        "direction_results": [asdict(r) for r in results],
    }
    summary_path: Path = RESULTS_DATA_DIR / f"cell{entry.cell_id}_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(
        f"[cell {entry.cell_id}] DSI original={entry.dsi_original:.4f}  "
        f"DSI measured={dsi_measured:.4f}  PD rate={pd_rate_hz:.2f} Hz",
        flush=True,
    )
    return results


def main() -> None:
    ensure_directories()
    entries: dict[int, CellEntry] = _load_cell_entries(CELL_IDS)

    print("Building DSGC cell with AIS...", flush=True)
    cell: DSGCCellWithAIS = build_dsgc_cell_with_ais()
    print(
        f"Cell built: {len(cell.terminal_dends)} terminal dends, "
        f"{len(cell.non_terminal_dends)} non-terminal dends",
        flush=True,
    )

    all_results: list[DirectionResult] = []
    for cell_id in CELL_IDS:
        entry: CellEntry = entries[cell_id]
        print(f"\nRunning cell {cell_id} (gen {entry.generation})...", flush=True)
        results: list[DirectionResult] = run_cell(cell=cell, entry=entry)
        all_results.extend(results)

    stable_count: int = sum(1 for r in all_results if r.is_stable)
    total: int = len(all_results)
    print(
        f"\n[DONE] {stable_count}/{total} stable simulations",
        flush=True,
    )
    assert stable_count == 24, (
        f"Expected 24 stable simulations, got {stable_count}. "
        "Check Vm traces for NaN or instability."
    )


if __name__ == "__main__":
    main()
