"""Aggregate per-synapse Bed A and Bed B traces to mean/SD per (bed, direction, type).

Loads all 12 raw .npz files from data/, computes the post-hoc current
``I = g_nS * (v_local_mV - E_rev_mV)`` (in pA) per synapse, then collapses across
synapses to mean and SD per time point. Writes a single ``data/aggregated.npz`` with
keys of the form ``<bed>_<dir>_<type>_<g|I>_<mean|sd>`` plus a single shared ``t_ms``.

Bed B's Exp2Syn _ref_g is in microsiemens (uS). To make the I formula consistent across
beds (I_pA = g_nS * (v_mV - E_mV)), we convert Bed B g from uS to nS by multiplying
by 1000 BEFORE computing I.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from tasks.t0072_synaptic_traces_pd_nd.code.constants import (
    G_TRACES_KEY,
    QTY_G,
    QTY_I,
    REVERSAL_MV,
    STAT_MEAN,
    STAT_SD,
    T_MS_KEY,
    V_LOCAL_TRACES_KEY,
    Bed,
    Direction,
    RecordedSynapseType,
)
from tasks.t0072_synaptic_traces_pd_nd.code.paths import (
    AGGREGATED_NPZ,
    BED_A_ND_ACH_NPZ,
    BED_A_ND_AMPA_NPZ,
    BED_A_ND_GABA_NPZ,
    BED_A_ND_NMDA_NPZ,
    BED_A_PD_ACH_NPZ,
    BED_A_PD_AMPA_NPZ,
    BED_A_PD_GABA_NPZ,
    BED_A_PD_NMDA_NPZ,
    BED_B_ND_ACH_NPZ,
    BED_B_ND_GABA_NPZ,
    BED_B_PD_ACH_NPZ,
    BED_B_PD_GABA_NPZ,
    DATA_DIR,
)

# Conversion factor: Bed B Exp2Syn g is in microsiemens (uS); multiply by 1000 to get nS.
US_TO_NS: float = 1000.0


@dataclass(frozen=True, slots=True)
class TraceFile:
    """One (bed, direction, synapse_type) trace file with its on-disk path."""

    bed: Bed
    direction: Direction
    synapse_type: RecordedSynapseType
    path: Path


@dataclass(frozen=True, slots=True)
class AggregatedTraces:
    """Mean and SD across synapses for one (bed, direction, type), plus the time axis."""

    bed: Bed
    direction: Direction
    synapse_type: RecordedSynapseType
    t_ms: np.ndarray
    g_mean_ns: np.ndarray
    g_sd_ns: np.ndarray
    i_mean_pa: np.ndarray
    i_sd_pa: np.ndarray


# All 12 input files in canonical order.
ALL_INPUT_FILES: list[TraceFile] = [
    # Bed A PD
    TraceFile(Bed.BED_A, Direction.PD, RecordedSynapseType.AMPA, BED_A_PD_AMPA_NPZ),
    TraceFile(Bed.BED_A, Direction.PD, RecordedSynapseType.NMDA, BED_A_PD_NMDA_NPZ),
    TraceFile(Bed.BED_A, Direction.PD, RecordedSynapseType.GABA, BED_A_PD_GABA_NPZ),
    TraceFile(Bed.BED_A, Direction.PD, RecordedSynapseType.ACH, BED_A_PD_ACH_NPZ),
    # Bed A ND
    TraceFile(Bed.BED_A, Direction.ND, RecordedSynapseType.AMPA, BED_A_ND_AMPA_NPZ),
    TraceFile(Bed.BED_A, Direction.ND, RecordedSynapseType.NMDA, BED_A_ND_NMDA_NPZ),
    TraceFile(Bed.BED_A, Direction.ND, RecordedSynapseType.GABA, BED_A_ND_GABA_NPZ),
    TraceFile(Bed.BED_A, Direction.ND, RecordedSynapseType.ACH, BED_A_ND_ACH_NPZ),
    # Bed B PD
    TraceFile(Bed.BED_B, Direction.PD, RecordedSynapseType.ACH, BED_B_PD_ACH_NPZ),
    TraceFile(Bed.BED_B, Direction.PD, RecordedSynapseType.GABA, BED_B_PD_GABA_NPZ),
    # Bed B ND
    TraceFile(Bed.BED_B, Direction.ND, RecordedSynapseType.ACH, BED_B_ND_ACH_NPZ),
    TraceFile(Bed.BED_B, Direction.ND, RecordedSynapseType.GABA, BED_B_ND_GABA_NPZ),
]


def _aggregate_one(*, trace_file: TraceFile) -> AggregatedTraces:
    """Load one .npz, convert g to nS if needed, compute I per synapse, reduce to mean/SD."""
    data = np.load(trace_file.path)
    g_traces_raw: np.ndarray = data[G_TRACES_KEY].astype(np.float64)
    v_local_traces: np.ndarray = data[V_LOCAL_TRACES_KEY].astype(np.float64)
    t_ms: np.ndarray = data[T_MS_KEY].astype(np.float64)
    e_rev_mv: float = float(REVERSAL_MV[(trace_file.bed, trace_file.synapse_type)])

    # Convert Bed B uS -> nS so I = g_nS * (v_mV - E_mV) gives pA across both beds.
    if trace_file.bed == Bed.BED_B:
        g_traces_ns: np.ndarray = g_traces_raw * US_TO_NS
    else:
        g_traces_ns = g_traces_raw

    # Per-synapse current in pA: 1 nS * 1 mV = 1 pA.
    i_traces_pa: np.ndarray = g_traces_ns * (v_local_traces - e_rev_mv)

    g_mean: np.ndarray = g_traces_ns.mean(axis=0)
    # ddof=1 for unbiased sample SD; n_synapses >> 1 so the difference is tiny but
    # explicit is better than implicit for the writeup.
    g_sd: np.ndarray = g_traces_ns.std(axis=0, ddof=1)
    i_mean: np.ndarray = i_traces_pa.mean(axis=0)
    i_sd: np.ndarray = i_traces_pa.std(axis=0, ddof=1)

    print(
        f"  {trace_file.path.name}: n_syn={g_traces_ns.shape[0]} "
        f"n_samples={g_traces_ns.shape[1]} "
        f"g_peak_mean={float(g_mean.max()):+.4f} nS "
        f"|I|_peak_mean={float(np.abs(i_mean).max()):.2f} pA"
    )

    return AggregatedTraces(
        bed=trace_file.bed,
        direction=trace_file.direction,
        synapse_type=trace_file.synapse_type,
        t_ms=t_ms,
        g_mean_ns=g_mean,
        g_sd_ns=g_sd,
        i_mean_pa=i_mean,
        i_sd_pa=i_sd,
    )


def _aggregated_key(
    *,
    bed: Bed,
    direction: Direction,
    synapse_type: RecordedSynapseType,
    quantity: str,
    stat: str,
) -> str:
    """Build aggregated.npz key: bed_a_pd_ampa_g_mean, bed_b_nd_gaba_I_sd, etc."""
    return f"{bed.value}_{direction.value}_{synapse_type.value}_{quantity}_{stat}"


def main() -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Aggregating {len(ALL_INPUT_FILES)} input .npz files...")

    aggregated: list[AggregatedTraces] = []
    for trace_file in ALL_INPUT_FILES:
        aggregated.append(_aggregate_one(trace_file=trace_file))

    # All 12 t_ms arrays must be identical (same recording dt and same tstop).
    reference_t_ms: np.ndarray = aggregated[0].t_ms
    for agg in aggregated[1:]:
        assert np.array_equal(agg.t_ms, reference_t_ms), (
            f"t_ms mismatch between {aggregated[0].bed}/{aggregated[0].direction}/"
            f"{aggregated[0].synapse_type} and {agg.bed}/{agg.direction}/"
            f"{agg.synapse_type}: shapes {reference_t_ms.shape} vs {agg.t_ms.shape}"
        )

    # Build the keyed payload: 12 traces x 4 arrays each + shared t_ms = 49 entries.
    payload: dict[str, np.ndarray] = {T_MS_KEY: reference_t_ms}
    for agg in aggregated:
        payload[
            _aggregated_key(
                bed=agg.bed,
                direction=agg.direction,
                synapse_type=agg.synapse_type,
                quantity=QTY_G,
                stat=STAT_MEAN,
            )
        ] = agg.g_mean_ns
        payload[
            _aggregated_key(
                bed=agg.bed,
                direction=agg.direction,
                synapse_type=agg.synapse_type,
                quantity=QTY_G,
                stat=STAT_SD,
            )
        ] = agg.g_sd_ns
        payload[
            _aggregated_key(
                bed=agg.bed,
                direction=agg.direction,
                synapse_type=agg.synapse_type,
                quantity=QTY_I,
                stat=STAT_MEAN,
            )
        ] = agg.i_mean_pa
        payload[
            _aggregated_key(
                bed=agg.bed,
                direction=agg.direction,
                synapse_type=agg.synapse_type,
                quantity=QTY_I,
                stat=STAT_SD,
            )
        ] = agg.i_sd_pa

    AGGREGATED_NPZ.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(AGGREGATED_NPZ, **payload)
    print(
        f"\nWrote {AGGREGATED_NPZ.name}: {len(payload)} arrays, "
        f"size={AGGREGATED_NPZ.stat().st_size} B"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
