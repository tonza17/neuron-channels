"""Constants for the t0078 Bed B v2 MOBO task: 49-d parameter bounds + sim defaults.

Parameter layout (49 dims total):

* 25 tier-stratified channel densities (5 channels x 5 tiers).
  Tiers are: soma, primary-dendrite, mid-dendrite (non-terminal), terminal-
  dendrite, AIS. Channels are: Nav1.6, Kv3, NaP, BK, SK.
* 7 uniform-density channels (single density applied to soma + dendrites; not
  AIS): Kdr, Kv4, NaR, HCN (Ih), CaL, CaT, Kv7 (Im).
* 2 slow-AHP parameters: SK_E2-extended ``gbar`` (soma + AIS), and the
  ``tau_ca_multiplier`` (range [1, 20] per researcher decision).
* 13 synaptic placement parameters identical to t0076 (passive Ra/cm/gleak +
  cad depth/taur + N_ach/N_gaba + spatial-decay rho/lambda + weights).
* 2 free AIS geometry parameters (length, diameter) per researcher decision.

Total: 25 + 7 + 2 + 13 + 2 = 49.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum

import numpy as np
from numpy.typing import NDArray

# ---------------------------------------------------------------------------
# Simulation defaults (mirror t0024 trial-driver settings; TSTOP_MS = 1400 per
# researcher decision overriding t0076's 1000 ms).
# ---------------------------------------------------------------------------

CELSIUS_DEG_C: float = 36.9
DT_MS: float = 0.1
STEPS_PER_MS: float = 10.0
TSTOP_MS: float = 1400.0
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
# Stability detection: a Pareto cell is unstable if peak Vm leaves the
# physiological range [-80, +60] mV during any trial.
# ---------------------------------------------------------------------------
STABILITY_PEAK_VM_MIN_MV: float = -80.0
STABILITY_PEAK_VM_MAX_MV: float = 60.0


# ---------------------------------------------------------------------------
# 12 vendored t78-namespace channel SUFFIXes plus the new skahpt78 slow-AHP.
# ---------------------------------------------------------------------------

CHANNEL_SUFFIXES: tuple[str, ...] = (
    "nav16t78",  # Nav1.6 fast Na
    "napt78",  # NaP persistent Na
    "nart78",  # NaR resurgent Na
    "kdrt78",  # Kdr delayed-rectifier K
    "kv3t78",  # Kv3 fast K
    "kv4t78",  # Kv4 / IA transient K
    "kv7t78",  # Kv7 / KM M-current
    "iht78",  # HCN / Ih hyperpolarisation-activated
    "calt78",  # CaL high-voltage-activated Ca
    "catt78",  # CaT low-voltage-activated Ca
    "bkt78",  # BK / KCa1.1
    "skt78",  # SK / KCa2 (fast)
)
assert len(CHANNEL_SUFFIXES) == 12, "expected 12 channel suffixes"

SLOW_AHP_SUFFIX: str = "skahpt78"

# Tier-stratified channels (each gets 5 per-tier densities).
STRATIFIED_CHANNEL_SUFFIXES: tuple[str, ...] = (
    "nav16t78",
    "kv3t78",
    "napt78",
    "bkt78",
    "skt78",
)

# Channels excluded from AIS per task description (NaP, BK, SK forbidden at AIS).
AIS_PERMITTED_SUFFIXES: tuple[str, ...] = (
    "nav16t78",
    "kv3t78",
    "kv7t78",
)

# Uniform-density channels (single density applied to soma + dendrites only).
UNIFORM_CHANNEL_SUFFIXES: tuple[str, ...] = (
    "kdrt78",
    "kv4t78",
    "nart78",
    "iht78",
    "calt78",
    "catt78",
    "kv7t78",
)
assert len(UNIFORM_CHANNEL_SUFFIXES) == 7, "expected 7 uniform suffixes"


# ---------------------------------------------------------------------------
# 49-d parameter space.
# ---------------------------------------------------------------------------

N_PARAMS: int = 49

N_STRATIFIED_CHANNELS: int = 5
N_TIERS: int = 5
N_TIERED_DENSITIES: int = N_STRATIFIED_CHANNELS * N_TIERS  # 25
N_UNIFORM_CHANNELS: int = 7
N_SLOW_AHP: int = 2  # gbar + tau_ca_multiplier
N_SYNAPTIC: int = 13
N_AIS_GEOMETRY: int = 2

assert (
    N_TIERED_DENSITIES + N_UNIFORM_CHANNELS + N_SLOW_AHP + N_SYNAPTIC + N_AIS_GEOMETRY == N_PARAMS
)


class ParamIndex(IntEnum):
    # 25 tier-stratified densities (channel-major order: all 5 tiers of channel
    # 0, then channel 1, ...).
    NAV16_SOMA_GBAR = 0
    NAV16_PRIMARY_GBAR = 1
    NAV16_MID_GBAR = 2
    NAV16_TERMINAL_GBAR = 3
    NAV16_AIS_GBAR = 4
    KV3_SOMA_GBAR = 5
    KV3_PRIMARY_GBAR = 6
    KV3_MID_GBAR = 7
    KV3_TERMINAL_GBAR = 8
    KV3_AIS_GBAR = 9
    NAP_SOMA_GBAR = 10
    NAP_PRIMARY_GBAR = 11
    NAP_MID_GBAR = 12
    NAP_TERMINAL_GBAR = 13
    NAP_AIS_GBAR = 14  # forbidden at AIS — kept in space; apply_params skips writing
    BK_SOMA_GBAR = 15
    BK_PRIMARY_GBAR = 16
    BK_MID_GBAR = 17
    BK_TERMINAL_GBAR = 18
    BK_AIS_GBAR = 19  # forbidden at AIS
    SK_SOMA_GBAR = 20
    SK_PRIMARY_GBAR = 21
    SK_MID_GBAR = 22
    SK_TERMINAL_GBAR = 23
    SK_AIS_GBAR = 24  # forbidden at AIS
    # 7 uniform-density channels (single per-channel density on soma + dends).
    KDR_GBAR = 25
    KV4_GBAR = 26
    NAR_GBAR = 27
    IH_GBAR = 28
    CAL_GBAR = 29
    CAT_GBAR = 30
    IM_GBAR = 31  # Kv7 / KM
    # 2 slow-AHP params (SK_E2 with extended Ca-binding kinetics).
    SKAHP_GBAR_SOMA_AIS = 32
    SKAHP_TAU_CA_MULTIPLIER = 33
    # 13 synaptic placement / passive parameters identical to t0076.
    RA_OHM_CM = 34  # linear 50..250
    CM_UF_CM2 = 35  # linear 0.5..2.0
    GLEAK_S_CM2 = 36  # log-uniform 1e-5..1e-3
    CAD_DEPTH_UM = 37  # linear 0.05..0.5
    CAD_TAUR_MS = 38  # linear 5..100
    N_ACH = 39  # integer 50..350
    N_GABA = 40
    RHO0_ACH = 41  # linear 0.1..5.0
    LAMBDA_ACH_UM = 42  # linear 30..500
    RHO0_GABA = 43
    LAMBDA_GABA_UM = 44
    W_ACH_US = 45  # log-uniform 1e-4..1e-2 uS
    W_GABA_US = 46
    # 2 free AIS geometry parameters (researcher decision).
    AIS_LENGTH_UM = 47  # linear 25..50
    AIS_DIAMETER_UM = 48  # linear 0.5..1.2


assert int(ParamIndex.AIS_DIAMETER_UM) + 1 == N_PARAMS, "ParamIndex enum count must match N_PARAMS"


# Tier order matches the per-channel five-element block order in ParamIndex.
class Tier(IntEnum):
    SOMA = 0
    PRIMARY = 1
    MID = 2
    TERMINAL = 3
    AIS = 4


N_TIERS_ENUM: int = len(Tier)
assert N_TIERS_ENUM == N_TIERS


def stratified_param_index(*, channel_idx: int, tier: Tier) -> int:
    """Return the ``ParamIndex`` integer for one (channel, tier) pair."""
    assert 0 <= channel_idx < N_STRATIFIED_CHANNELS
    return channel_idx * N_TIERS + int(tier)


# Lower / upper bounds in *natural* units. For log-uniform parameters the
# Bayesian optimiser sees the logarithm and we exponentiate at apply time.
def _build_bounds() -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    lo: list[float] = []
    hi: list[float] = []
    # 25 tier-stratified densities — log-uniform 1e-5..1.0 S/cm^2 (AIS Nav1.6
    # may reach the Kole 2008 prior of 0.25..0.5 S/cm^2).
    for _ in range(N_TIERED_DENSITIES):
        lo.append(1e-5)
        hi.append(1.0)
    # 7 uniform-density channels — log-uniform 1e-5..0.5 S/cm^2.
    for _ in range(N_UNIFORM_CHANNELS):
        lo.append(1e-5)
        hi.append(0.5)
    # SKAHP gbar (soma + AIS), log-uniform 1e-5..0.5 S/cm^2.
    lo.append(1e-5)
    hi.append(0.5)
    # tau_ca_multiplier — log-uniform [1, 20] per researcher decision.
    lo.append(1.0)
    hi.append(20.0)
    # 13 synaptic placement params — copied from t0076 exactly.
    # Ra, cm, gleak.
    lo.extend([50.0, 0.5, 1e-5])
    hi.extend([250.0, 2.0, 1e-3])
    # cad depth, taur.
    lo.extend([0.05, 5.0])
    hi.extend([0.5, 100.0])
    # N_ach, N_gaba (integer, rounded at apply time).
    lo.extend([50.0, 50.0])
    hi.extend([350.0, 350.0])
    # rho0_ach, lambda_ach, rho0_gaba, lambda_gaba.
    lo.extend([0.1, 30.0, 0.1, 30.0])
    hi.extend([5.0, 500.0, 5.0, 500.0])
    # weights (uS), log-uniform.
    lo.extend([1e-4, 1e-4])
    hi.extend([1e-2, 1e-2])
    # AIS geometry.
    lo.extend([25.0, 0.5])
    hi.extend([50.0, 1.2])
    lo_arr: NDArray[np.float64] = np.array(lo, dtype=np.float64)
    hi_arr: NDArray[np.float64] = np.array(hi, dtype=np.float64)
    assert lo_arr.shape == (N_PARAMS,), f"LOWER_BOUNDS shape {lo_arr.shape} != ({N_PARAMS},)"
    assert hi_arr.shape == (N_PARAMS,), f"UPPER_BOUNDS shape {hi_arr.shape} != ({N_PARAMS},)"
    return lo_arr, hi_arr


LOWER_BOUNDS, UPPER_BOUNDS = _build_bounds()


def _build_log_indices() -> tuple[int, ...]:
    """All 25 tier densities + 7 uniform + 2 slow-AHP + 1 gleak + 2 weights."""
    out: list[int] = []
    for i in range(N_TIERED_DENSITIES):
        out.append(i)
    for i in range(N_UNIFORM_CHANNELS):
        out.append(N_TIERED_DENSITIES + i)
    out.append(int(ParamIndex.SKAHP_GBAR_SOMA_AIS))
    out.append(int(ParamIndex.SKAHP_TAU_CA_MULTIPLIER))
    out.append(int(ParamIndex.GLEAK_S_CM2))
    out.append(int(ParamIndex.W_ACH_US))
    out.append(int(ParamIndex.W_GABA_US))
    return tuple(out)


LOG_PARAM_INDICES: tuple[int, ...] = _build_log_indices()

INT_PARAM_INDICES: tuple[int, ...] = (
    int(ParamIndex.N_ACH),
    int(ParamIndex.N_GABA),
)


@dataclass(frozen=True, slots=True)
class ParameterVector:
    """A 49-d candidate point in the natural-units search space."""

    values: NDArray[np.float64]

    @classmethod
    def default(cls) -> ParameterVector:
        """Return a small literature-anchored default for smoke tests.

        Tier densities mirror the t0076 single-density defaults applied
        uniformly across all 5 tiers; uniform-density and synaptic params
        match t0076 verbatim. AIS geometry defaults are the researcher's
        midpoint (length 30 um, diameter 0.8 um).
        """
        v: NDArray[np.float64] = np.zeros(N_PARAMS, dtype=np.float64)
        # Tier-stratified defaults (small literature priors, replicated per tier).
        per_channel_default: tuple[float, ...] = (
            0.03,  # Nav1.6
            0.01,  # Kv3
            0.005,  # NaP
            0.001,  # BK
            0.001,  # SK
        )
        for ch_idx, dens in enumerate(per_channel_default):
            for t in range(N_TIERS):
                v[ch_idx * N_TIERS + t] = dens
        # Uniform-density channels.
        v[ParamIndex.KDR_GBAR] = 0.005
        v[ParamIndex.KV4_GBAR] = 0.005
        v[ParamIndex.NAR_GBAR] = 0.005
        v[ParamIndex.IH_GBAR] = 0.001
        v[ParamIndex.CAL_GBAR] = 0.0001
        v[ParamIndex.CAT_GBAR] = 0.0001
        v[ParamIndex.IM_GBAR] = 0.003
        # Slow-AHP defaults: zero conductance, multiplier=1 (reproduces sk74).
        v[ParamIndex.SKAHP_GBAR_SOMA_AIS] = 1e-5
        v[ParamIndex.SKAHP_TAU_CA_MULTIPLIER] = 1.0
        # Synaptic.
        v[ParamIndex.RA_OHM_CM] = 100.0
        v[ParamIndex.CM_UF_CM2] = 1.0
        v[ParamIndex.GLEAK_S_CM2] = 1.667e-4
        v[ParamIndex.CAD_DEPTH_UM] = 0.1
        v[ParamIndex.CAD_TAUR_MS] = 5.0
        v[ParamIndex.N_ACH] = 177.0
        v[ParamIndex.N_GABA] = 177.0
        v[ParamIndex.RHO0_ACH] = 1.0
        v[ParamIndex.LAMBDA_ACH_UM] = 200.0
        v[ParamIndex.RHO0_GABA] = 1.0
        v[ParamIndex.LAMBDA_GABA_UM] = 200.0
        v[ParamIndex.W_ACH_US] = 0.001
        v[ParamIndex.W_GABA_US] = 0.003
        # AIS geometry midpoints.
        v[ParamIndex.AIS_LENGTH_UM] = 30.0
        v[ParamIndex.AIS_DIAMETER_UM] = 0.8
        return cls(values=v)

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

    @property
    def ais_length_um(self) -> float:
        return float(self.values[ParamIndex.AIS_LENGTH_UM])

    @property
    def ais_diameter_um(self) -> float:
        return float(self.values[ParamIndex.AIS_DIAMETER_UM])

    @property
    def skahp_gbar_soma_ais(self) -> float:
        return float(self.values[ParamIndex.SKAHP_GBAR_SOMA_AIS])

    @property
    def skahp_tau_ca_multiplier(self) -> float:
        return float(self.values[ParamIndex.SKAHP_TAU_CA_MULTIPLIER])

    def stratified_density(self, *, channel_idx: int, tier: Tier) -> float:
        """Return the density for one (stratified channel, tier) pair."""
        idx = stratified_param_index(channel_idx=channel_idx, tier=tier)
        return float(self.values[idx])

    def uniform_density(self, *, suffix: str) -> float:
        """Return the per-channel uniform density for a uniform-channel suffix."""
        try:
            j = UNIFORM_CHANNEL_SUFFIXES.index(suffix)
        except ValueError as exc:
            raise KeyError(f"unknown uniform channel suffix {suffix!r}") from exc
        return float(self.values[N_TIERED_DENSITIES + j])


# ---------------------------------------------------------------------------
# AIS architectural defaults (used when AIS geometry params are absent or as
# initial-state values before BO writes).
# ---------------------------------------------------------------------------

AIS_DEFAULT_LENGTH_UM: float = 30.0
AIS_DEFAULT_DIAMETER_UM: float = 0.8
AIS_PROXIMAL_FRACTION: float = 0.5  # half of total AIS length
AIS_PASSIVE_RA_OHM_CM: float = 100.0
AIS_PASSIVE_CM_UF_CM2: float = 1.0
AIS_PASSIVE_GLEAK_S_CM2: float = 1.667e-4
AIS_PASSIVE_ELEAK_MV: float = -65.0

# d_lambda = 0.1 at 100 Hz segment rule reference (used inside extend_with_ais).
AIS_LAMBDA_F_FREQ_HZ: float = 100.0
AIS_D_LAMBDA: float = 0.1


# ---------------------------------------------------------------------------
# BoTorch / MOBO defaults.
# ---------------------------------------------------------------------------

N_SOBOL_INITIAL: int = 75
N_ACQ_ITERATIONS: int = 700
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
HOURLY_RATE_USD: float = 0.1582  # billed rate of the provisioned Vast.ai instance

# Worst-case fallback when a trial throws (Risk #4 in plan.md).
WORST_CASE_DSI: float = -1.0
WORST_CASE_RATE_HZ: float = 0.0
