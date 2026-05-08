"""Constants for t0092 diagnose-morphology-generator-silence task."""

from __future__ import annotations

# Reproducibility seeds.
MORPH_SEED: int = 1234
PLACER_SEED: int = 42

# Pre-fix expected procedural soma surface area (single 15 um cylinder).
# Source: tasks/t0090_morphology_generator_diversity_test/code/generator.py:380-405
# soma_diameter_um = 15.0; cylinder area = pi * d * L = pi * 15 * 15 = 706.86 um^2.
PRE_FIX_PROCEDURAL_SOMA_AREA_UM2: float = 706.86

# Target soma surface area matching the t0024 hand-coded Bed B cell.
# Source: research/research_code.md "Soma diameter conventions" — the t0024
# hand-coded soma uses 7 pt3d points yielding a frustum-stack area of ~220 um^2.
BEDB_AREA_TARGET_UM2: float = 220.0

# Tolerance band for the post-fix soma area (+/- 5%).
SOMA_AREA_TOLERANCE_FRAC: float = 0.05

# Five STABLE-but-silent cell IDs from t0090 verification used in REQ-9.
STABLE_T0090_CELLS: tuple[str, ...] = (
    "different/morph_00",
    "different/morph_13",
    "different/morph_14",
    "different/morph_15",
    "different/morph_19",
)

# Root cause candidate IDs and verdict labels.
CANDIDATE_SOMA_AREA_MISMATCH: str = "candidate_a_soma_area_mismatch"
CANDIDATE_PT3D_VS_L: str = "candidate_b_pt3d_vs_l_override"
CANDIDATE_SYNAPSE_XY: str = "candidate_c_synapse_xy_mismatch"
CANDIDATE_CHANNEL_SKIP: str = "candidate_d_channel_application_skip"

VERDICT_CONFIRMED: str = "CONFIRMED"
VERDICT_REFUTED: str = "REFUTED"
VERDICT_PARTIAL: str = "PARTIAL"
VERDICT_BLOCKED: str = "BLOCKED"

# Pre-fix Vm peak threshold for spike detection (matches t0080 AP_THRESHOLD_MV).
AP_THRESHOLD_MV: float = -10.0

# 8-direction protocol angles in degrees.
ANGLES_8DIR_DEG: tuple[float, ...] = (0.0, 45.0, 90.0, 135.0, 180.0, 225.0, 270.0, 315.0)

# DSI pass criterion for REQ-8.
DSI_PASS_THRESHOLD: float = 0.1

# Stability check duration before Vm trial (no stim).
NO_STIM_DURATION_MS: float = 50.0
V_INIT_MV: float = -70.0

# Spec versions for output JSONs.
SPEC_VERSION_STRUCTURAL: str = "1"
SPEC_VERSION_SYNAPSE: str = "1"
SPEC_VERSION_ROOT_CAUSE: str = "1"
SPEC_VERSION_POST_FIX: str = "1"

# Variant IDs for results/metrics.json.
VARIANT_PRE_FIX_BEDB: str = "pre_fix_procedural_bedb"
VARIANT_POST_FIX_BEDB: str = "post_fix_procedural_bedb"
