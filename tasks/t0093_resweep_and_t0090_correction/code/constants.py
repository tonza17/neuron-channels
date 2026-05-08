"""Typed constants for t0093 patched-generator re-sweep + correction overlay."""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Stability flag string values (mirror StabilityKind enum values from t0090).
# ---------------------------------------------------------------------------

STABILITY_FLAG_STABLE: str = "stable"
STABILITY_FLAG_NAN_VOLTAGE: str = "nan_voltage"
STABILITY_FLAG_DIVERGED: str = "diverged"
STABILITY_FLAG_DISCONNECTED: str = "disconnected"

# Visualisation-only sub-flag: distinguishes silent vs firing STABLE cells.
DISPLAY_FLAG_STABLE_FIRING: str = "stable_firing"
DISPLAY_FLAG_STABLE_SILENT: str = "stable_silent"

# ---------------------------------------------------------------------------
# Population labels (must match t0090's verification_summary.json values).
# ---------------------------------------------------------------------------

POPULATION_DIFFERENT: str = "different"
POPULATION_SIMILAR: str = "similar"

# ---------------------------------------------------------------------------
# Pass / stretch criteria.
# ---------------------------------------------------------------------------

PASS_CRITERION_MIN_FIRING: int = 50
STRETCH_CRITERION_MIN_FIRING: int = 55

# ---------------------------------------------------------------------------
# Transition labels for delta analysis.
# ---------------------------------------------------------------------------

TRANSITION_NAN_TO_STABLE_FIRING: str = "nan_to_stable_firing"
TRANSITION_NAN_TO_STABLE_SILENT: str = "nan_to_stable_silent"
TRANSITION_UNCHANGED_NAN: str = "unchanged_nan"
TRANSITION_UNCHANGED_STABLE_SILENT: str = "unchanged_stable_silent"
TRANSITION_STABLE_SILENT_TO_STABLE_FIRING: str = "stable_silent_to_stable_firing"
TRANSITION_REGRESSION_STABLE_TO_NAN: str = "regression_stable_to_nan"
TRANSITION_REGRESSION_STABLE_TO_DIVERGED: str = "regression_stable_to_diverged"
TRANSITION_UNCHANGED_DIVERGED: str = "unchanged_diverged"
TRANSITION_UNCHANGED_DISCONNECTED: str = "unchanged_disconnected"
TRANSITION_OTHER: str = "other"

TRANSITION_LABELS: list[str] = [
    TRANSITION_NAN_TO_STABLE_FIRING,
    TRANSITION_NAN_TO_STABLE_SILENT,
    TRANSITION_UNCHANGED_NAN,
    TRANSITION_UNCHANGED_STABLE_SILENT,
    TRANSITION_STABLE_SILENT_TO_STABLE_FIRING,
    TRANSITION_REGRESSION_STABLE_TO_NAN,
    TRANSITION_REGRESSION_STABLE_TO_DIVERGED,
    TRANSITION_UNCHANGED_DIVERGED,
    TRANSITION_UNCHANGED_DISCONNECTED,
    TRANSITION_OTHER,
]

# ---------------------------------------------------------------------------
# Okabe-Ito palette (colour-blind safe).
# ---------------------------------------------------------------------------

OKABE_ITO_BLACK: str = "#000000"
OKABE_ITO_ORANGE: str = "#E69F00"
OKABE_ITO_SKY_BLUE: str = "#56B4E9"
OKABE_ITO_GREEN: str = "#009E73"
OKABE_ITO_YELLOW: str = "#F0E442"
OKABE_ITO_BLUE: str = "#0072B2"
OKABE_ITO_VERMILLION: str = "#D55E00"
OKABE_ITO_PURPLE: str = "#CC79A7"

OKABE_ITO_PALETTE: tuple[str, ...] = (
    OKABE_ITO_BLACK,
    OKABE_ITO_ORANGE,
    OKABE_ITO_SKY_BLUE,
    OKABE_ITO_GREEN,
    OKABE_ITO_YELLOW,
    OKABE_ITO_BLUE,
    OKABE_ITO_VERMILLION,
    OKABE_ITO_PURPLE,
)

# Per-flag colour mapping for stability-display in panels.
STABILITY_FLAG_TO_COLOR: dict[str, str] = {
    DISPLAY_FLAG_STABLE_FIRING: OKABE_ITO_GREEN,
    DISPLAY_FLAG_STABLE_SILENT: OKABE_ITO_YELLOW,
    STABILITY_FLAG_NAN_VOLTAGE: OKABE_ITO_VERMILLION,
    STABILITY_FLAG_DIVERGED: OKABE_ITO_ORANGE,
    STABILITY_FLAG_DISCONNECTED: OKABE_ITO_PURPLE,
}

# ---------------------------------------------------------------------------
# Correction overlay constants.
# ---------------------------------------------------------------------------

CORRECTION_ID: str = "C-0093-01"
CORRECTING_TASK: str = "t0093_resweep_and_t0090_correction"
TARGET_TASK: str = "t0090_morphology_generator_diversity_test"
TARGET_KIND_LIBRARY: str = "library"
TARGET_LIBRARY_ID: str = "procedural_dsgc_morphology_generator"
REPLACEMENT_TASK: str = "t0092_diagnose_morphology_generator_silence"
REPLACEMENT_LIBRARY_ID: str = "procedural_dsgc_morphology_generator_fix"

CORRECTION_ACTION_REPLACE: str = "replace"
CORRECTION_SPEC_VERSION: str = "3"

# ---------------------------------------------------------------------------
# Metrics.json variant identifiers (explicit-variant format).
# ---------------------------------------------------------------------------

VARIANT_DIFFERENT_POST_FIX: str = "different_set_post_fix"
VARIANT_SIMILAR_POST_FIX: str = "similar_set_post_fix"

REGISTERED_METRIC_DSI: str = "direction_selectivity_index"

# ---------------------------------------------------------------------------
# Schema field names for JSON output (typed string constants).
# ---------------------------------------------------------------------------

FIELD_MORPH_ID: str = "morph_id"
FIELD_POPULATION: str = "population"
FIELD_MORPH_INDEX: str = "morph_index"
FIELD_STABILITY_FLAG: str = "stability_flag"
FIELD_DSI: str = "dsi"
FIELD_PD_RATE_HZ: str = "pd_rate_hz"
FIELD_ND_RATE_HZ: str = "nd_rate_hz"
FIELD_PEAK_VM_MV: str = "peak_vm_mv"
FIELD_N_DENDRITES: str = "n_dendrites"
FIELD_N_TERMINALS: str = "n_terminals"
FIELD_ELAPSED_S: str = "elapsed_s"
FIELD_ERROR: str = "error"
FIELD_PER_DIRECTION_SPIKES: str = "per_direction_spikes"
FIELD_PRE_FIX_STABILITY_FLAG: str = "pre_fix_stability_flag"
FIELD_PRE_FIX_SPIKE_COUNT_TOTAL: str = "pre_fix_spike_count_total"

# Pass-criterion expected-totals.
TOTAL_CELLS: int = 60
PER_POPULATION_CELLS: int = 30
