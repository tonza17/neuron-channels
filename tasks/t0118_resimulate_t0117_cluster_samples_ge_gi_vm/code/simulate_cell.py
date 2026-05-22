"""Per-cell driver for the t0118 three-mode trio (REQ-6, REQ-7, REQ-8, REQ-9, REQ-10).

For each selected cell:
1. Build the cell once via ``generate_fixed_morphology`` + ``insert_baseline_channels`` +
   ``apply_parameter_vector`` (the copied t0106 stack).
2. Build the synapse bundle once via ``setup_synapses_parametric``.
3. For each (mode, direction) pair: apply mode-specific overrides on top of fresh electrophys
   params, attach the per-mode recorders, queue AR(2) events, run NEURON, save the trace parquet.
4. Tear down: ``h.delete_section`` on every section and ``del cell``.

Each per-mode-per-direction trial is wrapped in a try/except so a single failed (mode, direction)
combination does not abort the cell. Cell-level failures (build, bundle) are raised so the caller
can record them.
"""

from __future__ import annotations

import contextlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from numpy.typing import NDArray

# Library imports (allowed cross-task per ARF rules).
from tasks.t0092_diagnose_morphology_generator_silence.code.baseline_channels import (
    insert_baseline_channels,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import (
    generate_fixed_morphology,
)
from tasks.t0117_pooled_pca_cluster_factor_all_cells_4_seeds.code.constants import (
    MAX_MORPH_SEED,
    MORPHOLOGY_PARAM_NAMES,
)

# Bootstrap NEURON first (auto-applies as a side-effect on import).
from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code import (
    bootstrap as _bootstrap,  # noqa: F401  -- import side effect
)
from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.apply_params import (
    apply_parameter_vector,
)
from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.constants import (
    DT_MS,
    G_E_US_COL,
    G_I_US_COL,
    HH_OFF_HHST_PARAMS,
    HH_OFF_SLOW_AHP_SUFFIX,
    HH_OFF_T80_SUFFIXES,
    RECORD_DT_MS,
    SAMPLE_SEED,
    SEED_CELL_STRIDE,
    SEED_DIRECTION_MULT,
    T_MS_COL,
    TSTOP_MS,
    V_M_MV_COL,
    Direction,
    TrialMode,
)
from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.constants_electrophys import (
    CELSIUS_DEG_C,
    N_PARAMS,
    RHO_CORRELATED,
    STEPS_PER_MS,
    V_INIT_MV,
    ParameterVector,
)
from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.generator_wrapper import (
    _LIVE_CELLS,
    morphology_params_from_vector,
)
from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.trial_helpers import (
    BASE_ACH_PROB,
    RATE_DT_MS,
    SynapseBundle,
    _bar_arrival_times,
    _gaba_prob_for_direction,
    _rates_to_events,
    _rates_with_ar2_noise,
    setup_synapses_parametric,
)


@dataclass(frozen=True, slots=True)
class TrialOutcome:
    """Result of a single (mode, direction) simulation."""

    mode: TrialMode
    direction_deg: int
    success: bool
    error_type: str | None
    error_message: str | None
    parquet_path: Path | None


@dataclass(frozen=True, slots=True)
class CellSimResult:
    """Result of running all 6 trials for a single cell."""

    cell_key: str
    cluster_id: int
    n_success: int
    n_failure: int
    trials: list[TrialOutcome]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _morph_params_from_row(*, row: pd.Series) -> Any:
    """Build a MorphologyParams instance from a 14-d slice with seed normalisation."""
    morph_vec_list: list[float] = [float(row[name]) for name in MORPHOLOGY_PARAM_NAMES]
    morph_vec_np: NDArray[np.float64] = np.asarray(morph_vec_list, dtype=np.float64)
    params = morphology_params_from_vector(morph_vector_14d=morph_vec_np)
    # Normalise the morph_seed via modulo (matches t0117 morphology_rendering.to_morph_params).
    from dataclasses import replace as _dataclass_replace

    return _dataclass_replace(params, morph_seed=int(params.morph_seed) % MAX_MORPH_SEED)


def _electrophys_vector_from_row(*, row: pd.Series) -> NDArray[np.float64]:
    """Extract the 54-d electrophys block from a manifest+features DataFrame row."""
    from tasks.t0117_pooled_pca_cluster_factor_all_cells_4_seeds.code.constants import (
        ELECTROPHYS_PARAM_NAMES,
    )

    vec_list: list[float] = [float(row[name]) for name in ELECTROPHYS_PARAM_NAMES]
    return np.asarray(vec_list, dtype=np.float64)


def _zero_all_active_channels(*, cell: Any) -> None:
    """Zero every active channel on every segment to enforce HH-off (EPSP/IPSP PASSIVE mode).

    Touches:
    * Soma + all_dends + AIS sections.
    * For each segment, sets ``gbar_<suffix> = 0`` for every t80 suffix + skahpt80 if present.
    * For each segment, sets ``HHst.gnabar``, ``HHst.gkbar``, ``HHst.gkmbar`` to 0 if HHst present.

    Uses ``hasattr`` because not every section has every mechanism inserted (AIS only carries the
    permitted subset).
    """
    sections: list[Any] = [cell.soma]
    sections.extend(cell.all_dends)
    sections.append(cell.ais_proximal)
    sections.append(cell.ais_distal)
    suffixes_with_gbar: tuple[str, ...] = tuple(HH_OFF_T80_SUFFIXES) + (HH_OFF_SLOW_AHP_SUFFIX,)
    for sec in sections:
        for seg in sec:
            for suffix in suffixes_with_gbar:
                attr = f"gbar_{suffix}"
                if hasattr(seg, attr):
                    setattr(seg, attr, 0.0)
            # HHst is universal: gnabar / gkbar / gkmbar.
            for param in HH_OFF_HHST_PARAMS:
                if hasattr(seg, param):
                    setattr(seg, param, 0.0)


def _silence_synapses(
    *,
    bundle: SynapseBundle,
    silence_ach: bool,
    silence_nmda: bool,
    silence_gaba: bool,
) -> None:
    """Zero NetCon weights for the specified synapse classes."""
    if silence_ach:
        for nc in bundle.ncs_ach:
            nc.weight[0] = 0.0
    if silence_nmda:
        for nc in bundle.ncs_nmda:
            nc.weight[0] = 0.0
    if silence_gaba:
        for nc in bundle.ncs_gaba:
            nc.weight[0] = 0.0


# ---------------------------------------------------------------------------
# Recording helpers
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class _ModeRecorders:
    """NEURON Vector handles for a single mode's recorders (kept alive during h.run)."""

    t_rec: Any  # h.Vector recording h._ref_t
    ach_g: list[Any]  # per-ACh-synapse Vector handles
    nmda_g: list[Any]
    gaba_g: list[Any]
    v_m: Any | None  # soma v_m recorder (FULL mode only)


def _attach_recorders(
    *,
    h: Any,
    cell: Any,
    bundle: SynapseBundle,
    mode: TrialMode,
) -> _ModeRecorders:
    """Attach mode-conditional recorders. Time is always recorded; conductances only in passive."""
    t_rec = h.Vector()
    t_rec.record(h._ref_t, RECORD_DT_MS)
    ach_g: list[Any] = []
    nmda_g: list[Any] = []
    gaba_g: list[Any] = []
    v_m: Any | None = None

    if mode == TrialMode.EPSP_PASSIVE:
        for syn in bundle.syns_ach:
            v = h.Vector()
            v.record(syn._ref_g, RECORD_DT_MS)
            ach_g.append(v)
        for syn in bundle.syns_nmda:
            v = h.Vector()
            v.record(syn._ref_g, RECORD_DT_MS)
            nmda_g.append(v)
    elif mode == TrialMode.IPSP_PASSIVE:
        for syn in bundle.syns_gaba:
            v = h.Vector()
            v.record(syn._ref_g, RECORD_DT_MS)
            gaba_g.append(v)
    elif mode == TrialMode.FULL:
        v_m = h.Vector()
        v_m.record(cell.soma(0.5)._ref_v, RECORD_DT_MS)
    return _ModeRecorders(t_rec=t_rec, ach_g=ach_g, nmda_g=nmda_g, gaba_g=gaba_g, v_m=v_m)


def _vectors_to_total(*, vecs: list[Any], n_samples_expected: int) -> NDArray[np.float64]:
    """Sum a list of NEURON Vector handles into a single 1-D float64 array."""
    if len(vecs) == 0:
        return np.zeros(n_samples_expected, dtype=np.float64)
    arrs: list[NDArray[np.float64]] = []
    for v in vecs:
        arr: NDArray[np.float64] = np.asarray(v.to_python(), dtype=np.float64)
        # Truncate or pad to expected length.
        if arr.shape[0] >= n_samples_expected:
            arrs.append(arr[:n_samples_expected])
        else:
            padded: NDArray[np.float64] = np.zeros(n_samples_expected, dtype=np.float64)
            padded[: arr.shape[0]] = arr
            arrs.append(padded)
    stacked: NDArray[np.float64] = np.stack(arrs, axis=0)
    return stacked.sum(axis=0)


def _vector_to_array(*, vec: Any, n_samples_expected: int) -> NDArray[np.float64]:
    """Convert a single NEURON Vector to a 1-D float64 array of length n_samples_expected."""
    arr: NDArray[np.float64] = np.asarray(vec.to_python(), dtype=np.float64)
    if arr.shape[0] >= n_samples_expected:
        return arr[:n_samples_expected]
    padded: NDArray[np.float64] = np.zeros(n_samples_expected, dtype=np.float64)
    padded[: arr.shape[0]] = arr
    return padded


# ---------------------------------------------------------------------------
# Trial driver
# ---------------------------------------------------------------------------


def _run_one_trial(
    *,
    h: Any,
    cell: Any,
    bundle: SynapseBundle,
    mode: TrialMode,
    direction_deg: int,
    seed: int,
    n_samples: int,
) -> dict[str, NDArray[np.float64]]:
    """Queue events, run h.run(), return the trace columns for the chosen mode."""
    n_ach: int = len(bundle.syns_ach)
    n_gaba: int = len(bundle.syns_gaba)
    n_bins: int = int(np.ceil(TSTOP_MS / RATE_DT_MS))

    arrival_ach: NDArray[np.float64] = _bar_arrival_times(
        syn_xy=bundle.syn_xy_ach,
        origin_xy=cell.origin_xy,
        direction_deg=float(direction_deg),
    )
    arrival_gaba: NDArray[np.float64] = _bar_arrival_times(
        syn_xy=bundle.syn_xy_gaba,
        origin_xy=cell.origin_xy,
        direction_deg=float(direction_deg),
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
    gaba_prob: float = _gaba_prob_for_direction(float(direction_deg))
    ach_probs: NDArray[np.float64] = np.full(n_ach, BASE_ACH_PROB, dtype=np.float64)
    gaba_probs: NDArray[np.float64] = np.full(n_gaba, gaba_prob, dtype=np.float64)
    rng: np.random.Generator = np.random.default_rng(seed + 1_000_003)
    ach_events: list[list[float]] = _rates_to_events(
        rates_hz=ach_rates,
        release_prob=ach_probs,
        rate_dt_ms=RATE_DT_MS,
        rng=rng,
    )
    gaba_events: list[list[float]] = _rates_to_events(
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

    fih = h.FInitializeHandler(_queue)
    recorders: _ModeRecorders = _attach_recorders(h=h, cell=cell, bundle=bundle, mode=mode)
    h.celsius = CELSIUS_DEG_C
    h.dt = DT_MS
    h.steps_per_ms = STEPS_PER_MS
    h.v_init = V_INIT_MV
    h.tstop = TSTOP_MS
    h.finitialize(V_INIT_MV)
    _ = fih  # keep alive
    h.run()

    t_arr: NDArray[np.float64] = _vector_to_array(vec=recorders.t_rec, n_samples_expected=n_samples)

    if mode == TrialMode.EPSP_PASSIVE:
        g_ach_total: NDArray[np.float64] = _vectors_to_total(
            vecs=recorders.ach_g, n_samples_expected=n_samples
        )
        g_nmda_total: NDArray[np.float64] = _vectors_to_total(
            vecs=recorders.nmda_g, n_samples_expected=n_samples
        )
        g_e_total: NDArray[np.float64] = g_ach_total + g_nmda_total
        return {T_MS_COL: t_arr, G_E_US_COL: g_e_total}
    if mode == TrialMode.IPSP_PASSIVE:
        g_i_total: NDArray[np.float64] = _vectors_to_total(
            vecs=recorders.gaba_g, n_samples_expected=n_samples
        )
        return {T_MS_COL: t_arr, G_I_US_COL: g_i_total}
    # FULL mode.
    assert recorders.v_m is not None
    v_arr: NDArray[np.float64] = _vector_to_array(vec=recorders.v_m, n_samples_expected=n_samples)
    if not np.all(np.isfinite(v_arr)):
        # Replace non-finite V_m with -60 mV to keep the trace usable for inspection.
        v_arr = np.where(np.isfinite(v_arr), v_arr, V_INIT_MV).astype(np.float64)
    return {T_MS_COL: t_arr, V_M_MV_COL: v_arr}


# ---------------------------------------------------------------------------
# Cell teardown
# ---------------------------------------------------------------------------


def _teardown_cell(*, cell: Any, h: Any) -> None:
    """Delete every section + remove the cell from _LIVE_CELLS so RAM does not accumulate."""
    sections: list[Any] = list(cell.all_dends) + [
        cell.soma,
        cell.ais_proximal,
        cell.ais_distal,
    ]
    for sec in sections:
        with contextlib.suppress(RuntimeError, AttributeError):
            h.delete_section(sec=sec)
    with contextlib.suppress(ValueError):
        _LIVE_CELLS.remove(cell)
    # Drop the cell id from the apply_params module-level cache so the next cell at the same id
    # (Python may reuse memory addresses after GC) re-runs _insert_channels_once.
    from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.apply_params import (
        _INSERTED_CELLS as _INSERTED_CELLS_SET,
    )

    _INSERTED_CELLS_SET.discard(id(cell))


# ---------------------------------------------------------------------------
# Public entrypoint
# ---------------------------------------------------------------------------


def cell_key(*, source_task: str, seed: int, generation: int, individual_idx: int) -> str:
    """Canonical cell-key string ``<seed>_<generation>_<individual_idx>`` (REQ-9)."""
    _ = source_task  # source_task is not part of the key per task description
    return f"{int(seed)}_{int(generation)}_{int(individual_idx)}"


def trace_parquet_path(
    *,
    traces_root: Path,
    cluster_id: int,
    cell_key_str: str,
    mode: TrialMode,
    direction_deg: int,
) -> Path:
    """Canonical trace parquet path."""
    filename: str = f"{mode.value}_{direction_deg}.parquet"
    return traces_root / str(int(cluster_id)) / cell_key_str / filename


def simulate_cell(
    *,
    cell_row: pd.Series,
    cell_index: int,
    traces_root: Path,
) -> CellSimResult:
    """Run the 3-mode x 2-direction trial trio for one cell.

    Returns a CellSimResult summarising successes and failures across the 6 trials. Raises
    ``RuntimeError`` if the cell could not be built or its synapse bundle could not be created.
    """
    cluster_id: int = int(cell_row["cluster_id"])
    source_task: str = str(cell_row["source_task"])
    seed_val: int = int(cell_row["seed"])
    generation: int = int(cell_row["generation"])
    individual_idx: int = int(cell_row["individual_idx"])
    key: str = cell_key(
        source_task=source_task,
        seed=seed_val,
        generation=generation,
        individual_idx=individual_idx,
    )

    # Build the cell from the 14-d morphology slice.
    morph_params = _morph_params_from_row(row=cell_row)
    cell = generate_fixed_morphology(params=morph_params, morph_seed=morph_params.morph_seed)
    h: Any = cell.h
    insert_baseline_channels(h=h, cell=cell)
    _LIVE_CELLS.append(cell)

    # Apply the 54-d electrophys vector.
    e_vec: NDArray[np.float64] = _electrophys_vector_from_row(row=cell_row)
    assert e_vec.shape == (N_PARAMS,), (
        f"electrophys vector has wrong shape {e_vec.shape}, expected ({N_PARAMS},)"
    )
    electrophys: ParameterVector = ParameterVector(values=e_vec)
    apply_parameter_vector(cell=cell, params=electrophys)

    # Build the synapse bundle once.
    placer_seed: int = SAMPLE_SEED + cell_index * SEED_CELL_STRIDE + 51_077
    bundle: SynapseBundle = setup_synapses_parametric(
        cell=cell,
        n_ach=electrophys.n_ach,
        n_gaba=electrophys.n_gaba,
        rho_0_ach=electrophys.rho0_ach,
        lambda_ach_um=electrophys.lambda_ach_um,
        rho_0_gaba=electrophys.rho0_gaba,
        lambda_gaba_um=electrophys.lambda_gaba_um,
        w_ach_us=electrophys.w_ach_us,
        w_gaba_us=electrophys.w_gaba_us,
        placer_seed=placer_seed,
        gnmda_dend=electrophys.gnmda_dend,
        mg_conc_mm=electrophys.mg_conc_mm,
        voff_nmda=electrophys.voff_nmda,
    )

    # Snapshot canonical NetCon weights (so per-mode silencing is reversible across the 6 trials).
    canonical_ach_w: list[float] = [float(nc.weight[0]) for nc in bundle.ncs_ach]
    canonical_nmda_w: list[float] = [float(nc.weight[0]) for nc in bundle.ncs_nmda]
    canonical_gaba_w: list[float] = [float(nc.weight[0]) for nc in bundle.ncs_gaba]

    def _restore_canonical_weights() -> None:
        for nc, w in zip(bundle.ncs_ach, canonical_ach_w, strict=True):
            nc.weight[0] = w
        for nc, w in zip(bundle.ncs_nmda, canonical_nmda_w, strict=True):
            nc.weight[0] = w
        for nc, w in zip(bundle.ncs_gaba, canonical_gaba_w, strict=True):
            nc.weight[0] = w

    n_samples: int = int(TSTOP_MS / RECORD_DT_MS)
    trials: list[TrialOutcome] = []
    n_success: int = 0
    n_failure: int = 0

    modes: tuple[TrialMode, ...] = (
        TrialMode.EPSP_PASSIVE,
        TrialMode.IPSP_PASSIVE,
        TrialMode.FULL,
    )
    directions: tuple[Direction, ...] = (Direction.PD_DEG, Direction.ND_DEG)

    for mode in modes:
        # Re-apply electrophys params fresh per mode so the next mode starts from canonical state.
        apply_parameter_vector(cell=cell, params=electrophys)
        _restore_canonical_weights()
        if mode == TrialMode.EPSP_PASSIVE:
            _zero_all_active_channels(cell=cell)
            _silence_synapses(
                bundle=bundle, silence_ach=False, silence_nmda=False, silence_gaba=True
            )
        elif mode == TrialMode.IPSP_PASSIVE:
            _zero_all_active_channels(cell=cell)
            _silence_synapses(
                bundle=bundle, silence_ach=True, silence_nmda=True, silence_gaba=False
            )
        # FULL: leave conductances and weights at canonical values.

        for direction in directions:
            dir_deg: int = int(direction.value)
            cell_seed: int = (
                SAMPLE_SEED + cell_index * SEED_CELL_STRIDE + dir_deg * SEED_DIRECTION_MULT
            )
            parquet_path: Path = trace_parquet_path(
                traces_root=traces_root,
                cluster_id=cluster_id,
                cell_key_str=key,
                mode=mode,
                direction_deg=dir_deg,
            )
            try:
                trace_cols: dict[str, NDArray[np.float64]] = _run_one_trial(
                    h=h,
                    cell=cell,
                    bundle=bundle,
                    mode=mode,
                    direction_deg=dir_deg,
                    seed=cell_seed,
                    n_samples=n_samples,
                )
                parquet_path.parent.mkdir(parents=True, exist_ok=True)
                df_trace: pd.DataFrame = pd.DataFrame(trace_cols)
                assert len(df_trace) == n_samples, (
                    f"trace has {len(df_trace)} rows, expected {n_samples}"
                )
                df_trace.to_parquet(path=parquet_path, index=False)
                trials.append(
                    TrialOutcome(
                        mode=mode,
                        direction_deg=dir_deg,
                        success=True,
                        error_type=None,
                        error_message=None,
                        parquet_path=parquet_path,
                    )
                )
                n_success += 1
            except (RuntimeError, ValueError, AssertionError, ArithmeticError, OSError) as exc:
                trials.append(
                    TrialOutcome(
                        mode=mode,
                        direction_deg=dir_deg,
                        success=False,
                        error_type=type(exc).__name__,
                        error_message=str(exc),
                        parquet_path=None,
                    )
                )
                n_failure += 1

    # Tear the cell down so RAM does not accumulate across the 40-cell sweep.
    _teardown_cell(cell=cell, h=h)

    return CellSimResult(
        cell_key=key,
        cluster_id=cluster_id,
        n_success=n_success,
        n_failure=n_failure,
        trials=trials,
    )
