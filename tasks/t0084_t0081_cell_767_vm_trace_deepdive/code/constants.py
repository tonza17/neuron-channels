"""Task-local constants for t0084_t0081_cell_767_vm_trace_deepdive."""

from __future__ import annotations

# Target cells from t0081 Pareto front.
CELL_IDS: tuple[int, ...] = (767, 637, 762)

# Integration window for attribution metric (ms).
RESPONSE_WINDOW_START_MS: float = 200.0
RESPONSE_WINDOW_END_MS: float = 1200.0

# Recording timestep — matches RECORD_DT_MS from t0080 constants.
RECORD_DT_MS: float = 1.0

# Exp2NMDA reversal potential (from Exp2NMDA.mod parameter e = 0).
NMDA_EREV_MV: float = 0.0

# Human-readable channel names matching the attribution result fields.
CHANNEL_NAMES: tuple[str, str, str] = ("nmda", "nav16", "nap")

# Generation IDs for display in figures/results.
CELL_GENERATION: dict[int, int] = {767: 7, 637: 6, 762: 7}
