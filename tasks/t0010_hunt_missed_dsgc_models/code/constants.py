"""Constants for t0010_hunt_missed_dsgc_models."""

from __future__ import annotations

CANDIDATE_CSV_COLUMNS: list[str] = [
    "candidate_id",
    "source_url",
    "authors",
    "year",
    "simulator",
    "has_public_code",
    "runnable_guess",
    "priority",
    "port_attempt_status",
    "port_failure_phase",
    "port_failure_reason",
    "library_asset_slug",
    "tuning_curve_csv_path",
    "notes",
]
