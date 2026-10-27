"""Build scaled cells and dispose of them (shared by voltage clamp, current clamp, DSI)."""

import gc
import zlib
from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params import (
    apply_parameter_vector,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import ParameterVector
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_helpers import (
    SynapseBundle,
    setup_synapses_parametric,
)
from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyResult,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.constants import SEED_BASE
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.generator_wrapper import (
    build_cell,
    morphology_params_from_vector,
    split_68d_vector,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.mech_loader import load_mechanisms
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.scaling import (
    ChannelScales,
    ScalingReport,
    apply_channel_scales,
)


@dataclass(frozen=True, slots=True)
class BuiltCell:
    cell: MorphologyResult
    bundle: SynapseBundle | None
    report: ScalingReport | None


_H_HOLDER: list[Any] = []


def get_h() -> Any:
    if len(_H_HOLDER) == 0:
        _H_HOLDER.append(load_mechanisms())
    return _H_HOLDER[0]


def placer_seed_for_vector(*, electrophys_54d: NDArray[np.float64]) -> int:
    """Deterministic placer seed (crc32; t0129 used the process-randomised ``hash``)."""
    return SEED_BASE + (zlib.crc32(electrophys_54d.tobytes()) & 0xFFFF)


def dispose_all_cells() -> None:
    """Delete every NEURON section. ``LIVE_CELLS`` is NOT cleared: the t0080 channel-insertion
    cache is keyed on ``id(cell)``, so cell objects must stay referenced to avoid id reuse."""
    h = get_h()
    for sec in list(h.allsec()):
        h.delete_section(sec=sec)
    gc.collect()


def build_scaled(
    *,
    vector_68d: list[float],
    scales: ChannelScales,
    with_synapses: bool,
) -> BuiltCell:
    h = get_h()
    vec = np.asarray(vector_68d, dtype=np.float64)
    split = split_68d_vector(vector_68d=vec)
    morph_params = morphology_params_from_vector(morph_vector_14d=split.morphology_14d)
    params = ParameterVector(values=split.electrophys_54d)
    cell = build_cell(h=h, morph_params=morph_params)
    apply_parameter_vector(cell=cell, params=params)  # type: ignore[arg-type]
    report: ScalingReport | None = None
    if not scales.is_identity():
        report = apply_channel_scales(cell=cell, scales=scales)
    bundle: SynapseBundle | None = None
    if with_synapses:
        bundle = setup_synapses_parametric(
            cell=cell,  # type: ignore[arg-type]
            n_ach=params.n_ach,
            n_gaba=params.n_gaba,
            rho_0_ach=params.rho0_ach,
            lambda_ach_um=params.lambda_ach_um,
            rho_0_gaba=params.rho0_gaba,
            lambda_gaba_um=params.lambda_gaba_um,
            w_ach_us=params.w_ach_us,
            w_gaba_us=params.w_gaba_us,
            placer_seed=placer_seed_for_vector(electrophys_54d=split.electrophys_54d),
            gnmda_dend=params.gnmda_dend,
            mg_conc_mm=params.mg_conc_mm,
            voff_nmda=params.voff_nmda,
        )
    return BuiltCell(cell=cell, bundle=bundle, report=report)
