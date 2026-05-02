"""Stage 3 + Stage 4 sweep driver for t0074.

For each of 25 conditions (1 baseline + 8 channels x 3 densities), runs:
  * 12 angles x 5 seeds in FULL mode (HH on, gabaMOD = 0.33).
  * 12 angles x 1 seed in EPSP_PASSIVE mode (HH off, GABA off).
  * 12 angles x 1 seed in IPSP_PASSIVE mode (HH off, AMPA/NMDA/ACh off).

Total: 1500 FULL + 600 passive = 2100 trials. Direction is set by rotating BIP
synapse coordinates around the soma (Bed A's native 12-angle protocol; SAC
inhib/exc coords stay pinned to baseline).

Cad calcium pool is inserted on the soma for every condition so that BK and SK
have a working cai source and so that all 25 conditions share an identical
substrate (deltas are computed against this task's own with-cad baseline rather
than against t0067's no-cad baseline). NEURON does not allow build_dsgc() to be
called twice in the same Python process (template redefinition), so a single
build + single sweep pass is the only viable structure.

Per-condition CSVs are appended to ``results/data/per_trial_full.csv`` and
``results/data/per_trial_passive.csv`` immediately after each condition
completes, so a crash partway through preserves the work already done. On
restart the script skips conditions whose rows already exist in the CSVs.
"""

from __future__ import annotations

import csv
import time
from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray

from tasks.t0008_port_modeldb_189347.code.build_cell import (
    SynapseCoords,
    apply_params,
    build_dsgc,
    read_synapse_coords,
    reset_synapse_coords,
    rotate_synapse_coords_in_place,
)
from tasks.t0008_port_modeldb_189347.code.constants import V_INIT_MV
from tasks.t0074_channel_tuning_width_bed_a.code.constants import (
    ACH_MOD_OFF,
    ALL_CHANNEL_SUFFIXES,
    ANGLE_STEP_DEG,
    AP_THRESHOLD_MV,
    B_AMPA_OFF_NS,
    B_NMDA_OFF_NS,
    BASELINE_CONDITION_ID,
    BASELINE_END_MS,
    CALCIUM_POOL_SUFFIX,
    CHANNEL_DEFS,
    COL_ANGLE_DEG,
    COL_BASELINE_VM_MV,
    COL_CHANNEL_KIND,
    COL_CONDITION_ID,
    COL_DENSITY_LABEL,
    COL_DENSITY_MS_CM2,
    COL_FIRING_RATE_HZ,
    COL_IS_UNSTABLE,
    COL_N_SPIKES,
    COL_PEAK_VM_MV,
    COL_TRIAL_MODE,
    COL_TRIAL_SEED,
    EXPTYPE_HH_OFF,
    EXPTYPE_HH_ON,
    GABA_MOD_OFF,
    INSTABILITY_VM_MAX,
    INSTABILITY_VM_MIN,
    N_ANGLES,
    N_SEEDS_FULL,
    N_SEEDS_PASSIVE,
    S_ACH_OFF_NS,
    S_GABA_OFF_NS,
    SEED_BASE,
    TSTOP_MS,
    ChannelDef,
    ChannelKind,
    DensityLabel,
    TrialMode,
)
from tasks.t0074_channel_tuning_width_bed_a.code.paths import (
    DATA_DIR,
    FORKED_HOC,
    PER_TRIAL_FULL_CSV,
    PER_TRIAL_PASSIVE_CSV,
    T74_NRNMECH_DLL,
)


@dataclass(frozen=True, slots=True)
class TrialKey:
    condition_id: str
    channel_kind: ChannelKind
    density_label: DensityLabel
    density_mS_cm2: float
    angle_deg: float
    trial_seed: int
    trial_mode: TrialMode


@dataclass(frozen=True, slots=True)
class TrialOutput:
    key: TrialKey
    n_spikes: int
    firing_rate_hz: float
    peak_vm_mv: float
    baseline_vm_mv: float
    is_unstable: bool


def _channel_def_for_kind(kind: ChannelKind) -> ChannelDef:
    for ch in CHANNEL_DEFS:
        if ch.kind == kind:
            return ch
    raise ValueError(f"Unknown channel kind: {kind}")


def _condition_id(*, kind: ChannelKind, density_label: DensityLabel) -> str:
    if kind == ChannelKind.BASELINE:
        return BASELINE_CONDITION_ID
    short_kind: str = kind.value.replace(".", "").lower()
    return f"{short_kind}_{density_label.value}"


def _angles_deg() -> list[float]:
    return [float(i) * ANGLE_STEP_DEG for i in range(N_ANGLES)]


def _enumerate_all_conditions() -> list[tuple[ChannelKind, DensityLabel, float]]:
    """All 25 conditions: baseline + 8 channels x 3 densities."""
    out: list[tuple[ChannelKind, DensityLabel, float]] = [
        (ChannelKind.BASELINE, DensityLabel.NONE, 0.0),
    ]
    all_kinds: list[ChannelKind] = [
        ChannelKind.NAV16,
        ChannelKind.NAP,
        ChannelKind.NAR,
        ChannelKind.KV3,
        ChannelKind.KV4,
        ChannelKind.BK,
        ChannelKind.SK,
        ChannelKind.KV7,
    ]
    for kind in all_kinds:
        ch = _channel_def_for_kind(kind=kind)
        for label in (DensityLabel.LOW, DensityLabel.MED, DensityLabel.HIGH):
            out.append((kind, label, ch.density_for(label=label)))
    return out


def _ensure_t74_dll_loaded(*, h: Any) -> None:
    if getattr(_ensure_t74_dll_loaded, "_loaded", False):
        return
    dll_path: str = str(T74_NRNMECH_DLL).replace("\\", "/")
    rc: float = h.nrn_load_dll(dll_path)
    assert rc == 1.0, f"h.nrn_load_dll failed for {dll_path} (rc = {rc})"
    _ensure_t74_dll_loaded._loaded = True  # type: ignore[attr-defined]


def _source_forked_hoc(*, h: Any) -> None:
    forked_path: str = str(FORKED_HOC).replace("\\", "/")
    rc: float = h.load_file(1, forked_path)
    assert rc == 1.0, f"h.load_file(1, {forked_path!r}) failed"


def _insert_channels_on_soma(*, soma: Any, with_cad: bool) -> None:
    if with_cad:
        soma.insert(CALCIUM_POOL_SUFFIX)
    for suffix in ALL_CHANNEL_SUFFIXES:
        soma.insert(suffix)
        for seg in soma:
            setattr(seg, f"gbar_{suffix}", 0.0)


def _set_active_channel(
    *,
    soma: Any,
    channel_kind: ChannelKind,
    density_mS_cm2: float,
) -> None:
    """Zero all 8 channel densities, then set the active one (if any).

    Density passed in mS/cm^2; NEURON expects S/cm^2 (factor of 1e-3).
    """
    for suffix in ALL_CHANNEL_SUFFIXES:
        for seg in soma:
            setattr(seg, f"gbar_{suffix}", 0.0)
    if channel_kind == ChannelKind.BASELINE:
        return
    target_def: ChannelDef = _channel_def_for_kind(kind=channel_kind)
    g_s_cm2: float = float(density_mS_cm2) * 1e-3
    for seg in soma:
        setattr(seg, target_def.gbar_attr, g_s_cm2)


def _apply_mode_override(*, h: Any, mode: TrialMode) -> None:
    """Per-mode synaptic conductance overrides on top of canonical apply_params.

    Copied verbatim from t0065 run_protocol._apply_mode_override.
    """
    if mode == TrialMode.FULL:
        return
    if mode == TrialMode.EPSP_PASSIVE:
        h.gabaMOD = float(GABA_MOD_OFF)
        h.s2ggaba = float(S_GABA_OFF_NS)
        return
    if mode == TrialMode.IPSP_PASSIVE:
        h.b2gampa = float(B_AMPA_OFF_NS)
        h.b2gnmda = float(B_NMDA_OFF_NS)
        h.s2gach = float(S_ACH_OFF_NS)
        h.achMOD = float(ACH_MOD_OFF)
        return
    raise ValueError(f"Unknown TrialMode: {mode}")


def _baseline_v_mv(*, t_ms: NDArray[np.float64], v_mv: NDArray[np.float64]) -> float:
    mask: NDArray[np.bool_] = t_ms < BASELINE_END_MS
    if not mask.any():
        return float("nan")
    return float(np.mean(v_mv[mask]))


def _run_one_trial(
    *,
    h: Any,
    soma: Any,
    baseline_coords: list[SynapseCoords],
    key: TrialKey,
) -> TrialOutput:
    apply_params(h, seed=key.trial_seed)

    # Per-mode synaptic overrides (no-op for FULL mode).
    _apply_mode_override(h=h, mode=key.trial_mode)

    # exptype: HH on for FULL; HH off for passive (TTX = exptype == 2 zeroes Na).
    h.exptype = EXPTYPE_HH_ON if key.trial_mode == TrialMode.FULL else EXPTYPE_HH_OFF

    h("init_active()")
    h("access RGC.soma")
    h("update()")

    # Re-apply active channel gbar after init_active rebinds HHst soma channels.
    _set_active_channel(
        soma=soma,
        channel_kind=key.channel_kind,
        density_mS_cm2=key.density_mS_cm2,
    )

    # Reset then rotate BIP coords BEFORE placeBIP (placeBIP reads coords to
    # compute per-synapse arrival times; rotating after placeBIP has no effect).
    reset_synapse_coords(h=h, baseline=baseline_coords)
    rotate_synapse_coords_in_place(
        h=h,
        angle_deg=key.angle_deg,
        baseline=baseline_coords,
    )
    h("placeBIP()")

    v_rec: Any = h.Vector()
    v_rec.record(h.RGC.soma(0.5)._ref_v)
    t_rec: Any = h.Vector()
    t_rec.record(h._ref_t)
    spike_vec: Any = h.Vector()
    netcon: Any | None = None
    if key.trial_mode == TrialMode.FULL:
        netcon = h.NetCon(h.RGC.soma(0.5)._ref_v, None, sec=h.RGC.soma)
        netcon.threshold = float(AP_THRESHOLD_MV)
        netcon.record(spike_vec)

    h.finitialize(float(V_INIT_MV))
    h.continuerun(float(TSTOP_MS))

    v_arr: NDArray[np.float64] = np.array(list(v_rec), dtype=np.float64)
    t_arr: NDArray[np.float64] = np.array(list(t_rec), dtype=np.float64)
    if v_arr.size == 0:
        raise RuntimeError(f"No samples recorded for {key}")

    peak_vm: float = float(v_arr.max())
    baseline_vm: float = _baseline_v_mv(t_ms=t_arr, v_mv=v_arr)
    n_spikes: int = int(spike_vec.size()) if key.trial_mode == TrialMode.FULL else 0
    firing_rate_hz: float = float(n_spikes) / (TSTOP_MS / 1000.0)

    is_unstable: bool = peak_vm > INSTABILITY_VM_MAX or peak_vm < INSTABILITY_VM_MIN

    # Reset coords for the next trial.
    reset_synapse_coords(h=h, baseline=baseline_coords)

    return TrialOutput(
        key=key,
        n_spikes=n_spikes,
        firing_rate_hz=firing_rate_hz,
        peak_vm_mv=peak_vm,
        baseline_vm_mv=baseline_vm,
        is_unstable=is_unstable,
    )


def _trial_to_row(*, output: TrialOutput) -> dict[str, Any]:
    return {
        COL_CONDITION_ID: output.key.condition_id,
        COL_CHANNEL_KIND: output.key.channel_kind.value,
        COL_DENSITY_LABEL: output.key.density_label.value,
        COL_DENSITY_MS_CM2: output.key.density_mS_cm2,
        COL_ANGLE_DEG: output.key.angle_deg,
        COL_TRIAL_SEED: output.key.trial_seed,
        COL_TRIAL_MODE: output.key.trial_mode.value,
        COL_N_SPIKES: output.n_spikes,
        COL_FIRING_RATE_HZ: output.firing_rate_hz,
        COL_PEAK_VM_MV: output.peak_vm_mv,
        COL_BASELINE_VM_MV: output.baseline_vm_mv,
        COL_IS_UNSTABLE: output.is_unstable,
    }


def _csv_columns() -> list[str]:
    return [
        COL_CONDITION_ID,
        COL_CHANNEL_KIND,
        COL_DENSITY_LABEL,
        COL_DENSITY_MS_CM2,
        COL_ANGLE_DEG,
        COL_TRIAL_SEED,
        COL_TRIAL_MODE,
        COL_N_SPIKES,
        COL_FIRING_RATE_HZ,
        COL_PEAK_VM_MV,
        COL_BASELINE_VM_MV,
        COL_IS_UNSTABLE,
    ]


def _ensure_csv_header(*, csv_path: Any) -> None:
    """Create the CSV with header if it does not exist."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    if csv_path.exists():
        return
    with open(file=csv_path, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=_csv_columns())
        writer.writeheader()


def _append_rows(*, rows: list[dict[str, Any]], csv_path: Any) -> None:
    """Append rows to the CSV (header already written)."""
    _ensure_csv_header(csv_path=csv_path)
    with open(file=csv_path, mode="a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=_csv_columns())
        for row in rows:
            writer.writerow(row)


def _completed_condition_ids(*, csv_path: Any) -> set[str]:
    """Return the set of condition_ids already present in the CSV."""
    if not csv_path.exists():
        return set()
    seen: set[str] = set()
    with open(file=csv_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            seen.add(row[COL_CONDITION_ID])
    return seen


def _expected_full_count_per_condition() -> int:
    return N_ANGLES * N_SEEDS_FULL


def _expected_passive_count_per_condition() -> int:
    return N_ANGLES * N_SEEDS_PASSIVE * 2  # EPSP + IPSP modes


def _is_condition_complete(
    *,
    condition_id: str,
    full_csv: Any,
    passive_csv: Any,
) -> bool:
    """A condition is complete iff it has the expected number of FULL and passive rows."""
    if not full_csv.exists() or not passive_csv.exists():
        return False
    full_n: int = 0
    pas_n: int = 0
    with open(file=full_csv, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row[COL_CONDITION_ID] == condition_id:
                full_n += 1
    with open(file=passive_csv, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row[COL_CONDITION_ID] == condition_id:
                pas_n += 1
    return (
        full_n == _expected_full_count_per_condition()
        and pas_n == _expected_passive_count_per_condition()
    )


def _run_condition(
    *,
    h: Any,
    soma: Any,
    baseline_coords: list[SynapseCoords],
    kind: ChannelKind,
    density_label: DensityLabel,
    density_mS_cm2: float,
    cond_idx: int,
    n_total_conditions: int,
) -> tuple[int, int, int]:
    """Run all 84 trials (60 FULL + 24 passive) for one condition.

    Returns (n_trials_run, n_unstable, total_seconds).
    """
    condition_id: str = _condition_id(kind=kind, density_label=density_label)
    print(
        f"\n--- Condition {cond_idx}/{n_total_conditions}: {condition_id} "
        f"(kind={kind.value}, density={density_mS_cm2:g} mS/cm^2) ---",
        flush=True,
    )

    # Build the trial list for this condition only.
    angles: list[float] = _angles_deg()
    trial_keys: list[TrialKey] = []
    for angle_deg in angles:
        for seed_off in range(N_SEEDS_FULL):
            trial_keys.append(
                TrialKey(
                    condition_id=condition_id,
                    channel_kind=kind,
                    density_label=density_label,
                    density_mS_cm2=density_mS_cm2,
                    angle_deg=angle_deg,
                    trial_seed=SEED_BASE + seed_off,
                    trial_mode=TrialMode.FULL,
                )
            )
    for mode in (TrialMode.EPSP_PASSIVE, TrialMode.IPSP_PASSIVE):
        for angle_deg in angles:
            for seed_off in range(N_SEEDS_PASSIVE):
                trial_keys.append(
                    TrialKey(
                        condition_id=condition_id,
                        channel_kind=kind,
                        density_label=density_label,
                        density_mS_cm2=density_mS_cm2,
                        angle_deg=angle_deg,
                        trial_seed=SEED_BASE + seed_off,
                        trial_mode=mode,
                    )
                )

    cond_t0: float = time.perf_counter()
    full_rows: list[dict[str, Any]] = []
    passive_rows: list[dict[str, Any]] = []
    n_unstable: int = 0
    for idx, key in enumerate(trial_keys, start=1):
        t0: float = time.perf_counter()
        out: TrialOutput = _run_one_trial(
            h=h,
            soma=soma,
            baseline_coords=baseline_coords,
            key=key,
        )
        dt: float = time.perf_counter() - t0
        unstable_str: str = "  UNSTABLE" if out.is_unstable else ""
        if out.is_unstable:
            n_unstable += 1
        print(
            f"  [{idx:3d}/{len(trial_keys)}] {out.key.trial_mode.value:13s} "
            f"a={out.key.angle_deg:5.1f} seed={out.key.trial_seed:2d} "
            f"n={out.n_spikes:3d} peak={out.peak_vm_mv:+7.2f} mV [{dt:4.2f}s]{unstable_str}",
            flush=True,
        )
        row: dict[str, Any] = _trial_to_row(output=out)
        if out.key.trial_mode == TrialMode.FULL:
            full_rows.append(row)
        else:
            passive_rows.append(row)

    cond_dt: float = time.perf_counter() - cond_t0
    _append_rows(rows=full_rows, csv_path=PER_TRIAL_FULL_CSV)
    _append_rows(rows=passive_rows, csv_path=PER_TRIAL_PASSIVE_CSV)
    print(
        f"  -> condition {condition_id} done in {cond_dt:.1f}s "
        f"({len(full_rows)} FULL + {len(passive_rows)} passive rows appended; "
        f"{n_unstable} unstable)",
        flush=True,
    )
    return (len(trial_keys), n_unstable, int(cond_dt))


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    conditions: list[tuple[ChannelKind, DensityLabel, float]] = _enumerate_all_conditions()
    print(f"Total conditions: {len(conditions)} (single pass, cad always inserted)")

    # Resume support: skip conditions whose rows are already complete.
    skip_ids: set[str] = set()
    for kind, density_label, _density in conditions:
        cid: str = _condition_id(kind=kind, density_label=density_label)
        if _is_condition_complete(
            condition_id=cid,
            full_csv=PER_TRIAL_FULL_CSV,
            passive_csv=PER_TRIAL_PASSIVE_CSV,
        ):
            skip_ids.add(cid)
    if skip_ids:
        print(f"Resuming: {len(skip_ids)} conditions already complete: {sorted(skip_ids)}")

    sweep_t0: float = time.perf_counter()

    print("Building cell via build_dsgc()...", flush=True)
    h = build_dsgc()
    baseline_coords: list[SynapseCoords] = read_synapse_coords(h=h)

    print(f"Sourcing forked HOC: {FORKED_HOC}", flush=True)
    _source_forked_hoc(h=h)

    print(f"Loading t0074 DLL: {T74_NRNMECH_DLL}", flush=True)
    _ensure_t74_dll_loaded(h=h)

    print("Inserting 8 channels + cad on soma at gbar = 0...", flush=True)
    _insert_channels_on_soma(soma=h.RGC.soma, with_cad=True)

    total_trials_run: int = 0
    total_unstable: int = 0
    n_total: int = len(conditions)
    for cond_idx, (kind, density_label, density_mS_cm2) in enumerate(conditions, start=1):
        cid = _condition_id(kind=kind, density_label=density_label)
        if cid in skip_ids:
            print(f"\n--- Condition {cond_idx}/{n_total}: {cid} -- already complete, skipping ---")
            continue
        n_trials, n_unstable, _dt = _run_condition(
            h=h,
            soma=h.RGC.soma,
            baseline_coords=baseline_coords,
            kind=kind,
            density_label=density_label,
            density_mS_cm2=density_mS_cm2,
            cond_idx=cond_idx,
            n_total_conditions=n_total,
        )
        total_trials_run += n_trials
        total_unstable += n_unstable

    sweep_dt: float = time.perf_counter() - sweep_t0
    print(f"\nSweep complete: {total_trials_run} new trials in {sweep_dt:.1f}s")
    print(f"  per_trial_full.csv -> {PER_TRIAL_FULL_CSV}")
    print(f"  per_trial_passive.csv -> {PER_TRIAL_PASSIVE_CSV}")
    print(f"Unstable trials this run: {total_unstable}")


if __name__ == "__main__":
    main()
