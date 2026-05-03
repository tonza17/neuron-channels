"""Constants for the t0076 Bed B MOBO task: 25-d parameter bounds + simulation defaults."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum

import numpy as np
from numpy.typing import NDArray

# ---------------------------------------------------------------------------
# Simulation defaults (mirror t0024 trial-driver settings).
# ---------------------------------------------------------------------------

CELSIUS_DEG_C: float = 36.9
DT_MS: float = 0.1
STEPS_PER_MS: float = 10.0
TSTOP_MS: float = 1000.0
V_INIT_MV: float = -60.0
AP_THRESHOLD_MV: float = -10.0
RECORD_DT_MS: float = 1.0

# Direction sweep: 8 evenly spaced directions, 0 deg = preferred-direction (PD).
ANGLES_8DIR_DEG: tuple[int, ...] = (0, 45, 90, 135, 180, 225, 270, 315)
N_DIRECTIONS: int = 8
N_SEEDS: int = 20
PD_DIRECTION_DEG: float = 0.0
ND_DIRECTION_DEG: float = 180.0

# AR(2) noise / release defaults (mirrors t0024).
RHO_CORRELATED: float = 0.6
SEED_BASE: int = 1000

# Synaptic kinetics (kept fixed, only weights and counts are optimised).
ACH_TAU1_MS: float = 0.1
ACH_TAU2_MS: float = 4.0
ACH_EREV_MV: float = 0.0
GABA_TAU1_MS: float = 0.5
GABA_TAU2_MS: float = 12.0
GABA_EREV_MV: float = -60.0

# ---------------------------------------------------------------------------
# 12 vendored channel SUFFIXes (parameter indices 1-12, in this exact order).
# ---------------------------------------------------------------------------

CHANNEL_SUFFIXES: tuple[str, ...] = (
    "nav16t76",  # 1: Nav1.6 fast Na, t0067-derived
    "napt76",  # 2: NaP persistent Na, t0067-derived
    "nart76",  # 3: NaR resurgent Na, t0067-derived
    "kdrt76",  # 4: Kdr delayed-rectifier K, Mainen 1996 ModelDB 2488
    "kv3t76",  # 5: Kv3 fast K, t0067-derived
    "kv4t76",  # 6: Kv4 / IA transient K, t0067-derived
    "kv7t76",  # 7: Kv7 / KM M-current, t0074-derived (Hay 2011 Im)
    "iht76",  # 8: HCN / Ih hyperpolarisation-activated, Hay 2011 ModelDB 139653
    "calt76",  # 9: CaL high-voltage-activated Ca, Hay 2011 ModelDB 139653
    "catt76",  # 10: CaT low-voltage-activated Ca, Hay 2011 ModelDB 139653
    "bkt76",  # 11: BK / KCa1.1, t0074-derived (Mainen 1996 kca)
    "skt76",  # 12: SK / KCa2, t0074-derived (Hay 2011 SK_E2)
)
assert len(CHANNEL_SUFFIXES) == 12, "expected 12 channel suffixes"

# ---------------------------------------------------------------------------
# 25-d parameter space.
# ---------------------------------------------------------------------------

N_PARAMS: int = 25


class ParamIndex(IntEnum):
    # Channel densities (0..11), log-uniform 1e-5 to 0.5 S/cm^2.
    GBAR_NAV16 = 0
    GBAR_NAP = 1
    GBAR_NAR = 2
    GBAR_KDR = 3
    GBAR_KV3 = 4
    GBAR_KV4 = 5
    GBAR_KV7 = 6
    GBAR_IH = 7
    GBAR_CAL = 8
    GBAR_CAT = 9
    GBAR_BK = 10
    GBAR_SK = 11
    # Passive properties (12..14).
    RA_OHM_CM = 12  # linear 50..250
    CM_UF_CM2 = 13  # linear 0.5..2.0
    GLEAK_S_CM2 = 14  # log-uniform 1e-5..1e-3
    # Calcium dynamics (15..16).
    CAD_DEPTH_UM = 15  # linear 0.05..0.5
    CAD_TAUR_MS = 16  # linear 5..100
    # Synapse counts (17..18).
    N_ACH = 17  # integer 50..350 (continuous; rounded at apply time)
    N_GABA = 18  # integer 50..350
    # Spatial-rule (19..22).
    RHO0_ACH = 19  # linear 0.1..5.0
    LAMBDA_ACH_UM = 20  # linear 30..500
    RHO0_GABA = 21  # linear 0.1..5.0
    LAMBDA_GABA_UM = 22  # linear 30..500
    # Synapse weights (23..24), log-uniform 1e-4..1e-2 uS.
    W_ACH_US = 23
    W_GABA_US = 24


# Lower / upper bounds in *natural* units. For log-uniform parameters the
# Bayesian optimiser sees the logarithm and we exponentiate at apply time.
LOWER_BOUNDS: NDArray[np.float64] = np.array(
    [
        # 12 channel densities (S/cm^2).
        1e-5,
        1e-5,
        1e-5,
        1e-5,
        1e-5,
        1e-5,
        1e-5,
        1e-5,
        1e-5,
        1e-5,
        1e-5,
        1e-5,
        # passive: Ra, cm, gleak.
        50.0,
        0.5,
        1e-5,
        # cad depth, taur.
        0.05,
        5.0,
        # N_ach, N_gaba.
        50.0,
        50.0,
        # rho0_ach, lambda_ach, rho0_gaba, lambda_gaba.
        0.1,
        30.0,
        0.1,
        30.0,
        # weights uS.
        1e-4,
        1e-4,
    ],
    dtype=np.float64,
)

UPPER_BOUNDS: NDArray[np.float64] = np.array(
    [
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        250.0,
        2.0,
        1e-3,
        0.5,
        100.0,
        350.0,
        350.0,
        5.0,
        500.0,
        5.0,
        500.0,
        1e-2,
        1e-2,
    ],
    dtype=np.float64,
)
assert LOWER_BOUNDS.shape == (N_PARAMS,)
assert UPPER_BOUNDS.shape == (N_PARAMS,)

# Indices that should be sampled in log space.
LOG_PARAM_INDICES: tuple[int, ...] = (
    ParamIndex.GBAR_NAV16,
    ParamIndex.GBAR_NAP,
    ParamIndex.GBAR_NAR,
    ParamIndex.GBAR_KDR,
    ParamIndex.GBAR_KV3,
    ParamIndex.GBAR_KV4,
    ParamIndex.GBAR_KV7,
    ParamIndex.GBAR_IH,
    ParamIndex.GBAR_CAL,
    ParamIndex.GBAR_CAT,
    ParamIndex.GBAR_BK,
    ParamIndex.GBAR_SK,
    ParamIndex.GLEAK_S_CM2,
    ParamIndex.W_ACH_US,
    ParamIndex.W_GABA_US,
)

# Integer-valued parameters (rounded at apply time).
INT_PARAM_INDICES: tuple[int, ...] = (ParamIndex.N_ACH, ParamIndex.N_GABA)


@dataclass(frozen=True, slots=True)
class ParameterVector:
    """A 25-d candidate point in the natural-units search space."""

    values: NDArray[np.float64]

    @classmethod
    def default(cls) -> ParameterVector:
        """Return the de Rosenroll defaults projected into this 25-d space.

        Channel densities default to small but non-zero values close to the
        de Rosenroll HHst defaults (~3e-2 S/cm^2 for Nav, etc.). Synapse
        defaults match t0024 (177 of each, weights 0.001/0.003 uS).
        """
        v: NDArray[np.float64] = np.array(
            [
                # 12 channels — small literature defaults.
                0.03,
                0.005,
                0.005,
                0.005,
                0.01,
                0.005,
                0.003,
                0.001,
                0.0001,
                0.0001,
                0.001,
                0.001,
                # passive defaults.
                100.0,
                1.0,
                1.667e-4,
                # cad defaults.
                0.1,
                5.0,
                # 177 of each.
                177.0,
                177.0,
                # spatial rule: roughly uniform.
                1.0,
                200.0,
                1.0,
                200.0,
                # default weights (t0024: 0.001 ACh, 0.003 GABA).
                0.001,
                0.003,
            ],
            dtype=np.float64,
        )
        return cls(values=v)

    def channel_densities(self) -> NDArray[np.float64]:
        return self.values[: len(CHANNEL_SUFFIXES)]

    @property
    def ra_ohm_cm(self) -> float:
        return float(self.values[ParamIndex.RA_OHM_CM])

    @property
    def cm_uf_cm2(self) -> float:
        return float(self.values[ParamIndex.CM_UF_CM2])

    @property
    def gleak_s_cm2(self) -> float:
        return float(self.values[ParamIndex.GLEAK_S_CM2])

    @property
    def cad_depth_um(self) -> float:
        return float(self.values[ParamIndex.CAD_DEPTH_UM])

    @property
    def cad_taur_ms(self) -> float:
        return float(self.values[ParamIndex.CAD_TAUR_MS])

    @property
    def n_ach(self) -> int:
        return int(round(float(self.values[ParamIndex.N_ACH])))

    @property
    def n_gaba(self) -> int:
        return int(round(float(self.values[ParamIndex.N_GABA])))

    @property
    def rho0_ach(self) -> float:
        return float(self.values[ParamIndex.RHO0_ACH])

    @property
    def lambda_ach_um(self) -> float:
        return float(self.values[ParamIndex.LAMBDA_ACH_UM])

    @property
    def rho0_gaba(self) -> float:
        return float(self.values[ParamIndex.RHO0_GABA])

    @property
    def lambda_gaba_um(self) -> float:
        return float(self.values[ParamIndex.LAMBDA_GABA_UM])

    @property
    def w_ach_us(self) -> float:
        return float(self.values[ParamIndex.W_ACH_US])

    @property
    def w_gaba_us(self) -> float:
        return float(self.values[ParamIndex.W_GABA_US])


# ---------------------------------------------------------------------------
# BoTorch / MOBO defaults.
# ---------------------------------------------------------------------------

N_SOBOL_INITIAL: int = 30
N_ACQ_ITERATIONS: int = 400
ACQ_NUM_RESTARTS: int = 10
ACQ_RAW_SAMPLES: int = 256
CHECKPOINT_EVERY: int = 10
HV_PLATEAU_PATIENCE: int = 50
HV_PLATEAU_TOL: float = 1e-3

# Reference point for hypervolume — both objectives (DSI, rate) lower-bounded
# at 0; rate is in Hz. Cells worse than reference do not count toward HV.
REF_POINT_DSI: float = 0.0
REF_POINT_RATE_HZ: float = 0.0

# Cost gates (USD); mirrored from plan.md "Cost Estimation".
SOFT_BUDGET_USD: float = 4.0
HARD_BUDGET_USD: float = 5.0
HOURLY_RATE_USD: float = 0.1636  # billed rate of the provisioned Vast.ai instance

# Worst-case fallback when a trial throws (Risk #4 in plan.md).
WORST_CASE_DSI: float = -1.0
WORST_CASE_RATE_HZ: float = 0.0
