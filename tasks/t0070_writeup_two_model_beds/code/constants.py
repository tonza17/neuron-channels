"""Constants for the two-model-bed schematic plotting scripts.

All numeric values used by the plotting scripts are defined here so that the two
schematic figures share a single source of truth (Python style guide rule: no magic
numbers, centralise all reused values). Synaptic kinetics and direction-encoding
scalars are copied verbatim from the upstream code with `file:line` references in
the inline comments; the writeup itself cites the canonical source.
"""

from typing import Final

# --- Plot styling -----------------------------------------------------------

FIG_DPI: Final[int] = 150
FIG_WIDTH_IN: Final[float] = 10.0
FIG_HEIGHT_IN: Final[float] = 6.0

COLOR_EXC: Final[str] = "tab:orange"
COLOR_INH: Final[str] = "tab:blue"
COLOR_NMDA: Final[str] = "tab:red"
COLOR_ACH: Final[str] = "tab:orange"
COLOR_GABA: Final[str] = "tab:blue"

COLOR_SOMA: Final[str] = "tab:gray"
COLOR_DEND_ON: Final[str] = "tab:green"
COLOR_DEND_OFF: Final[str] = "lightgray"
COLOR_DEND_PRIMARY: Final[str] = "darkgreen"
COLOR_DEND_NONTERM: Final[str] = "mediumseagreen"
COLOR_DEND_TERM: Final[str] = "lightgreen"

# --- Trace timing ----------------------------------------------------------

TRACE_DURATION_MS: Final[float] = 200.0
TRACE_DT_MS: Final[float] = 0.1
BAR_ARRIVAL_BASELINE_MS: Final[float] = 50.0
BED_B_BAR_VELOCITY_UM_PER_MS: Final[float] = 1.0  # constants.py L78 (t0024)
BED_B_TERMINAL_SPACING_UM: Final[float] = 25.0  # illustrative spacing for 5 terminals

# --- Bed A synaptic kinetics ----------------------------------------------
# Sources: bipolarNMDA.mod L35-42, SAC2RGCinhib.mod L23-26, project overrides
# in tasks/t0008_port_modeldb_189347/code/build_cell.py L294-316.

BED_A_AMPA_TAU_MS: Final[float] = 2.0  # bipolarNMDA.mod L39
BED_A_NMDA_TAU_RISE_MS: Final[float] = 2.0  # bipolarNMDA.mod L38 (tau2NMDA)
BED_A_NMDA_TAU_DECAY_MS: Final[float] = 60.0  # apply_params L313 override
BED_A_GABA_TAU_MS: Final[float] = 30.0  # main.hoc L90 sets tau_SACinhib=30
BED_A_GABAMOD_PD: Final[float] = 0.33  # t0020 constants.py L37
BED_A_GABAMOD_ND: Final[float] = 0.99  # t0020 constants.py L38
BED_A_AMPA_PEAK_NS: Final[float] = 0.25  # B2GAMPA_NS, build_cell.py L294
BED_A_NMDA_PEAK_NS: Final[float] = 0.5  # B2GNMDA_NS, build_cell.py L295
BED_A_GABA_PEAK_NS: Final[float] = 0.5  # S2GGABA_NS, build_cell.py L296

# --- Bed B synaptic kinetics ----------------------------------------------
# Sources: tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py L45-53
# (Exp2Syn parameters used by run_tuning_curve.py L189-226 _setup_synapses).

BED_B_ACH_TAU_RISE_MS: Final[float] = 0.1  # constants.py L45 (ACH_TAU1_MS)
BED_B_ACH_TAU_DECAY_MS: Final[float] = 4.0  # constants.py L46 (ACH_TAU2_MS)
BED_B_GABA_TAU_RISE_MS: Final[float] = 0.5  # constants.py L50 (GABA_TAU1_MS)
BED_B_GABA_TAU_DECAY_MS: Final[float] = 12.0  # constants.py L51 (GABA_TAU2_MS)
BED_B_GABA_PROB_PD: Final[float] = 0.05  # run_tuning_curve.py L57 pref_prob
BED_B_GABA_PROB_ND: Final[float] = 0.80  # run_tuning_curve.py L57 null_prob
BED_B_ACH_WEIGHT_US: Final[float] = 0.001  # constants.py L48 (ACH_WEIGHT_US)
BED_B_GABA_WEIGHT_US: Final[float] = 0.003  # constants.py L53 (GABA_WEIGHT_US)

# --- Morphology counts ----------------------------------------------------
# Sources: RGCmodel.hoc L14, RGCmodelGD.hoc L12, t0008 constants.py L57-69,
# de Rosenroll _map_tree (build_cell.py L140-168).

BED_A_N_DEND: Final[int] = 350  # RGCmodel.hoc L14
BED_A_N_ON_DEND: Final[int] = 282  # t0008 constants.py L68 N_SYNAPSES_EACH_TYPE
BED_A_N_OFF_DEND: Final[int] = BED_A_N_DEND - BED_A_N_ON_DEND

BED_B_N_DEND: Final[int] = 350  # RGCmodelGD.hoc L12
BED_B_N_TERMINAL_DEND_APPROX: Final[int] = 177  # upstream ei_balance.py reference
BED_B_N_PRIMARY_DEND_APPROX: Final[int] = 10  # _map_tree heuristic count
BED_B_N_NONTERM_DEND_APPROX: Final[int] = (
    BED_B_N_DEND - BED_B_N_TERMINAL_DEND_APPROX - BED_B_N_PRIMARY_DEND_APPROX
)
