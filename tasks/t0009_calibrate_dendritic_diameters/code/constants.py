"""Constants for the t0009 diameter-calibration pipeline."""

# SWC column indices within each data row.
SWC_COLUMN_ID: int = 0
SWC_COLUMN_TYPE: int = 1
SWC_COLUMN_X: int = 2
SWC_COLUMN_Y: int = 3
SWC_COLUMN_Z: int = 4
SWC_COLUMN_RADIUS: int = 5
SWC_COLUMN_PARENT: int = 6

# CNG/SWC type codes.
TYPE_SOMA: int = 1
TYPE_DENDRITE: int = 3
ROOT_PARENT_ID: int = -1

# Physical clamps and constants.
TERMINAL_RADIUS_FLOOR_UM: float = 0.15
SOMA_RADIUS_FLOOR_UM: float = 0.5
AXIAL_RESISTIVITY_OHM_CM: float = 100.0
PLACEHOLDER_RADIUS_UM: float = 0.125

# Topology invariants for the source morphology (141009_Pair1DSGC.CNG.swc).
EXPECTED_COMPARTMENTS: int = 6736
EXPECTED_BRANCH_POINTS: int = 129
EXPECTED_LEAVES: int = 131
EXPECTED_DENDRITIC_LENGTH_UM: float = 1536.25

# Plot configuration.
PNG_DPI: int = 150

# Bin labels used in calibration and analysis outputs.
BIN_SOMA: str = "soma"
BIN_PRIMARY: str = "primary"
BIN_MID: str = "mid"
BIN_TERMINAL: str = "terminal"
