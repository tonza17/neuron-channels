"""Canonical per-seed visual key and convergence metadata.

Copied verbatim from the t0115 ``build_results.py`` ``SEED_COLORS`` /
``SEED_MARKERS`` / ``SEED_LABELS`` / ``POOL_RESTART_CADENCE`` / ``ALL_SEED_KEYS``
constants to preserve visual consistency with upstream per-seed reports.

The new ``HV_AUTOSTOP_ENABLED`` and ``STOP_TRIGGER`` dicts encode the
protocol drift surfaced by REQ-8.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Per-seed labels and visual key (copied verbatim from t0115)
# ---------------------------------------------------------------------------

ALL_SEED_KEYS: tuple[str, ...] = (
    "t0106_seed44",
    "t0112_seed77",
    "t0113_seed2247",
    "t0114_seed7755",
    "t0115_seed9354",
)

SEED_COLORS: dict[str, str] = {
    "t0106_seed44": "C0",
    "t0112_seed77": "C3",
    "t0113_seed2247": "C2",
    "t0114_seed7755": "C1",
    "t0115_seed9354": "C4",
}

SEED_MARKERS: dict[str, str] = {
    "t0106_seed44": "o",
    "t0112_seed77": "D",
    "t0113_seed2247": "s",
    "t0114_seed7755": "^",
    "t0115_seed9354": "v",
}

SEED_LABELS: dict[str, str] = {
    "t0106_seed44": "t0106 seed 44",
    "t0112_seed77": "t0112 seed 77",
    "t0113_seed2247": "t0113 seed 2247",
    "t0114_seed7755": "t0114 seed 7755",
    "t0115_seed9354": "t0115 seed 9354",
}

POOL_RESTART_CADENCE: dict[str, int] = {
    "t0106_seed44": 25,
    "t0112_seed77": 10,
    "t0113_seed2247": 10,
    "t0114_seed7755": 10,
    "t0115_seed9354": 10,
}

# Auto-stop convention (HV-plateau detector W=2, T=0.01) was enabled for
# t0106 / t0112 / t0113 and DISABLED for t0114 / t0115 per S-0113-03 after
# t0113's premature gen-14 stop. See research_code.md.
HV_AUTOSTOP_ENABLED: dict[str, bool] = {
    "t0106_seed44": True,
    "t0112_seed77": True,
    "t0113_seed2247": True,
    "t0114_seed7755": False,
    "t0115_seed9354": False,
}

# Per-seed source-task IDs (used in CSVs and answer asset).
SEED_TASK_IDS: dict[str, str] = {
    "t0106_seed44": "t0106_long_pdnd_nsga2_300gen",
    "t0112_seed77": "t0112_t0106_seed77_replicate",
    "t0113_seed2247": "t0113_t0106_seed2247_replicate",
    "t0114_seed7755": "t0114_seed7755_no_autostop",
    "t0115_seed9354": "t0115_seed9354_no_autostop",
}

# Per-seed task_seed integer (the NSGA-II RNG seed used by each task).
SEED_TASK_SEED: dict[str, int] = {
    "t0106_seed44": 44,
    "t0112_seed77": 77,
    "t0113_seed2247": 2247,
    "t0114_seed7755": 7755,
    "t0115_seed9354": 9354,
}

# Canonical asset-declared headline numbers (copy from t0115 ASSET_DECLARED).
# These provide the secondary cross-check for HV / generation counts where
# the raw HV-trajectory file does not carry the operator-stop trigger.
ASSET_DECLARED_N_GEN: dict[str, int] = {
    "t0106_seed44": 39,
    "t0112_seed77": 21,
    "t0113_seed2247": 14,
    "t0114_seed7755": 62,
    "t0115_seed9354": 55,
}

ASSET_DECLARED_FINAL_HV: dict[str, float] = {
    "t0106_seed44": 122.0288,
    "t0112_seed77": 107.4602,
    "t0113_seed2247": 45.6221,
    "t0114_seed7755": 111.5353,
    "t0115_seed9354": 50.5646,
}

ASSET_DECLARED_STOP_TRIGGER: dict[str, str] = {
    "t0106_seed44": "hv_plateau",
    "t0112_seed77": "hv_plateau",
    "t0113_seed2247": "hv_plateau",
    "t0114_seed7755": "operator_stop",
    "t0115_seed9354": "operator_stop",
}

# Per-seed protocol-drift narrative for the convergence and convention-drift
# CSVs. Each entry is one self-contained sentence.
PROTOCOL_DRIFT_NOTES: dict[str, str] = {
    "t0106_seed44": (
        "Legacy cadence 25; HV-plateau auto-stop fired at gen 39 above "
        "the Mohacsi 2024 20-60 convergence band."
    ),
    "t0112_seed77": (
        "Cadence 10 (10th-gen rule adopted); HV-plateau auto-stop fired "
        "at gen 21 inside the Mohacsi 2024 convergence band."
    ),
    "t0113_seed2247": (
        "Cadence 10; HV-plateau auto-stop fired prematurely at gen 14 "
        "below the Mohacsi 2024 20-60 convergence band -- zero LEGIT "
        "plausibly a censoring artefact, not a substrate-yield zero."
    ),
    "t0114_seed7755": (
        "Cadence 10; HV-plateau auto-stop DISABLED per S-0113-03; "
        "operator stop at gen 62 after visible plateau at HV ~111."
    ),
    "t0115_seed9354": (
        "Cadence 10; HV-plateau auto-stop DISABLED per S-0113-03; "
        "operator stop at gen 55 after visible plateau at HV ~50."
    ),
}
