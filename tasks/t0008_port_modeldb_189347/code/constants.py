"""Canonical constants for the t0008 ModelDB 189347 port.

Values are read verbatim from the pinned ``main.hoc`` at commit
``87d669dcef18e9966e29c88520ede78bc16d36ff`` of
``https://github.com/ModelDBRepository/189347``. Any change here requires a
matching change in ``assets/library/modeldb_189347_dsgc/sources/main.hoc``.
"""

from __future__ import annotations

import os

# NEURON install location on this workstation (validated by t0007).
NEURONHOME_DEFAULT: str = r"C:\Users\md1avn\nrn-8.2.7"
os.environ.setdefault("NEURONHOME", NEURONHOME_DEFAULT)

# Simulation timing (from main.hoc).
TSTOP_MS: float = 1000.0
DT_MS: float = 0.1
CELSIUS_DEG_C: float = 32.0

# Poleg-Polsky NMDA kinetics (from main.hoc).
TAU1_NMDA_BIP_MS: float = 60.0
E_SAC_INHIB_MV: float = -60.0

# Stimulus geometry (from main.hoc). Note: lightspeed=1 um/ms.
LIGHTSPEED_UM_PER_MS: float = 1.0
LIGHTWIDTH_UM: float = 500.0
LIGHTSTART_MS: float = -100.0
LIGHT_X_START_UM: float = -100.0
LIGHT_X_END_UM: float = 200.0
LIGHT_Y_START_UM: float = -130.0
LIGHT_Y_END_UM: float = 100.0
LIGHT_REVERSE: int = 0

# Synaptic conductances (from main.hoc, with sparse=1 maxvesmul=1).
B2GAMPA_NS: float = 0.25
B2GNMDA_NS: float = 0.5
S2GGABA_NS: float = 0.5
S2GACH_NS: float = 0.5
GABA_MOD: float = 0.33
ACH_MOD: float = 0.25
V_SHIFT_HHST_MV: float = -4.0
N_NMDA_V_DEP: float = 0.3
GAMMA_NMDA_V_DEP: float = 0.07
R_SYN_CHANCE: float = 1.0

# Simulation grid (canonical project grid).
N_ANGLES: int = 12
N_TRIALS: int = 20
ANGLE_STEP_DEG: float = 30.0

# Canonical synapse counts: one BIP, one SACinhib, and one SACexc point
# process per ON dendrite. The bundled morphology in ``RGCmodel.hoc``
# yields 282 ON dendrites at the ON/OFF cut ``z >= -0.16 * y + 46``, which
# is what the first ``init_sim`` call produces. The earlier task
# description figure of 177 referred to a different paper architecture;
# the port is faithful to the released HOC template, not to that number.
N_SYNAPSES_EACH_TYPE: int = 282

# AP detection threshold for firing-rate counting.
AP_THRESHOLD_MV: float = -10.0

# Resting potential for initialization.
V_INIT_MV: float = -65.0

# Bundled-morphology constants from RGCmodel.hoc (for reporting only).
BUNDLED_NUM_SOMA: int = 1
BUNDLED_NUM_DEND: int = 350

# Smoke-test tolerance: any positive firing rate passes (the port is not
# expected to hit the envelope without retuning, per plan).
SMOKE_TEST_MIN_FIRING_HZ: float = 0.0

# Validation gate threshold for the 12-angle mini-curve (step 8).
MINI_CURVE_MIN_PEAK_HZ: float = 5.0

# Metric keys registered under meta/metrics/.
METRIC_KEY_DSI: str = "direction_selectivity_index"
METRIC_KEY_HWHM: str = "tuning_curve_hwhm_deg"
METRIC_KEY_RELIABILITY: str = "tuning_curve_reliability"
METRIC_KEY_RMSE: str = "tuning_curve_rmse"

# ModelDB 189347 pinned commit SHA.
MODELDB_COMMIT_SHA: str = "87d669dcef18e9966e29c88520ede78bc16d36ff"
