"""Recording, simulation, and PD/ND constants for t0072."""

from __future__ import annotations

from enum import StrEnum

# Recording grid: 1 ms gives ~1000 samples per 1 s trial, ~5 MB total.
RECORD_DT_MS: float = 1.0

# Simulation timing (both beds use 1000 ms; t0008 const L18, t0024 const L22).
TSTOP_MS: float = 1000.0
DT_MS: float = 0.1
STEPS_PER_MS: float = 10.0
V_INIT_MV: float = -65.0
CELSIUS_DEG_C: float = 35.0

# Bed A: PD/ND encoded by gabaMOD scalar (t0020 const L37-38).
GABA_MOD_PD: float = 0.33
GABA_MOD_ND: float = 0.99

# Bed B: PD/ND encoded by bar angle (t0066 const L19-20).
DIRECTION_PD_DEG: float = 0.0
DIRECTION_ND_DEG: float = 180.0

# Bed B noise / weight (t0066 correlated default).
RHO_CORRELATED: float = 0.6
GABA_WEIGHT_SCALE: float = 1.0

# Reversal potentials in mV (per channel, sourced from MOD files).
E_AMPA_MV: float = 0.0
E_NMDA_MV: float = 0.0
E_GABA_BED_A_MV: float = -60.0
E_ACH_BED_A_MV: float = 0.0
E_ACH_BED_B_MV: float = 0.0
E_GABA_BED_B_MV: float = -60.0

# Per-trial seed.
SEED: int = 1

# Bed A canonical synapse count (t0008 const L59).
BED_A_N_SYNAPSES: int = 282


class RecordedSynapseType(StrEnum):
    """Synapse channel labels used in .npz file names and aggregated keys."""

    AMPA = "ampa"
    NMDA = "nmda"
    GABA = "gaba"
    ACH = "ach"


class Bed(StrEnum):
    """Model-bed labels."""

    BED_A = "bed_a"
    BED_B = "bed_b"


class Direction(StrEnum):
    """PD / ND labels."""

    PD = "pd"
    ND = "nd"


# Convenience: type-by-bed lookup.
RECORDED_TYPES_BED_A: list[RecordedSynapseType] = [
    RecordedSynapseType.AMPA,
    RecordedSynapseType.NMDA,
    RecordedSynapseType.GABA,
    RecordedSynapseType.ACH,
]
RECORDED_TYPES_BED_B: list[RecordedSynapseType] = [
    RecordedSynapseType.ACH,
    RecordedSynapseType.GABA,
]

# Reversal lookup: (bed, type) -> E_rev (mV).
REVERSAL_MV: dict[tuple[Bed, RecordedSynapseType], float] = {
    (Bed.BED_A, RecordedSynapseType.AMPA): E_AMPA_MV,
    (Bed.BED_A, RecordedSynapseType.NMDA): E_NMDA_MV,
    (Bed.BED_A, RecordedSynapseType.GABA): E_GABA_BED_A_MV,
    (Bed.BED_A, RecordedSynapseType.ACH): E_ACH_BED_A_MV,
    (Bed.BED_B, RecordedSynapseType.ACH): E_ACH_BED_B_MV,
    (Bed.BED_B, RecordedSynapseType.GABA): E_GABA_BED_B_MV,
}

# .npz keys.
G_TRACES_KEY: str = "g_traces"
V_LOCAL_TRACES_KEY: str = "v_local_traces"
T_MS_KEY: str = "t_ms"
E_REV_MV_KEY: str = "e_rev_mv"

# Aggregated .npz quantity / stat suffixes.
QTY_G: str = "g"
QTY_I: str = "I"
STAT_MEAN: str = "mean"
STAT_SD: str = "sd"
