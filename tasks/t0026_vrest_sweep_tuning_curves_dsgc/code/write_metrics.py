"""Emit ``results/metrics.json`` (multi-variant format).

Reads the per-model metrics CSVs and writes a multi-variant ``metrics.json``
with two top-level variants (``t0022`` and ``t0024``). Each variant carries
per-V_rest entries for the registered metric keys
``direction_selectivity_index`` and ``tuning_curve_hwhm_deg``, plus
project-specific entries for peak / null firing rates that are NOT registered
in ``meta/metrics/`` (these are recorded under a ``project_specific`` block
and surfaced as suggestions for future registration).
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from tasks.t0026_vrest_sweep_tuning_curves_dsgc.code.constants import (
    METRICS_JSON,
    VREST_METRICS_T0022,
    VREST_METRICS_T0024,
)


def _read_metrics(*, metrics_csv: Path) -> list[dict[str, float]]:
    records: list[dict[str, float]] = []
    with metrics_csv.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            records.append({k: float(v) for k, v in row.items()})
    records.sort(key=lambda r: r["v_rest_mv"])
    return records


def _vrest_label(v_rest_mv: float) -> str:
    sign = "+" if v_rest_mv >= 0 else "-"
    return f"{sign}{int(abs(v_rest_mv)):02d}mV"


def build_variant(*, records: list[dict[str, float]]) -> dict[str, object]:
    """Build a single variant block keyed by registered metric ids."""
    dsi_per_vrest: dict[str, float] = {}
    hwhm_per_vrest: dict[str, float] = {}
    peak_hz_per_vrest: dict[str, float] = {}
    null_hz_per_vrest: dict[str, float] = {}
    pref_dir_per_vrest: dict[str, float] = {}
    mean_peak_mv_per_vrest: dict[str, float] = {}
    for rec in records:
        label = _vrest_label(rec["v_rest_mv"])
        dsi_per_vrest[label] = round(rec["dsi"], 6)
        hwhm_per_vrest[label] = round(rec["hwhm_deg"], 4)
        peak_hz_per_vrest[label] = round(rec["peak_hz"], 4)
        null_hz_per_vrest[label] = round(rec["null_hz"], 4)
        pref_dir_per_vrest[label] = round(rec["preferred_dir_deg"], 3)
        mean_peak_mv_per_vrest[label] = round(rec["mean_peak_mv"], 3)

    # Headline scalars: best (lowest HWHM and highest DSI across V_rest).
    best_dsi: float = max(dsi_per_vrest.values()) if dsi_per_vrest else float("nan")
    best_hwhm: float = min(hwhm_per_vrest.values()) if hwhm_per_vrest else float("nan")
    return {
        "direction_selectivity_index": {
            "value": best_dsi,
            "per_v_rest_mv": dsi_per_vrest,
        },
        "tuning_curve_hwhm_deg": {
            "value": best_hwhm,
            "per_v_rest_mv": hwhm_per_vrest,
        },
        "project_specific": {
            "peak_hz_per_v_rest_mv": peak_hz_per_vrest,
            "null_hz_per_v_rest_mv": null_hz_per_vrest,
            "preferred_dir_deg_per_v_rest_mv": pref_dir_per_vrest,
            "mean_peak_mv_per_v_rest_mv": mean_peak_mv_per_vrest,
        },
    }


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    _ = _parse_args(argv)
    payload: dict[str, object] = {
        "metric_format": "multi_variant",
        "variants": {},
    }
    variants: dict[str, object] = payload["variants"]  # type: ignore[assignment]

    if VREST_METRICS_T0022.exists():
        records = _read_metrics(metrics_csv=VREST_METRICS_T0022)
        variants["t0022"] = build_variant(records=records)
    else:
        print(
            f"[write_metrics] WARNING: {VREST_METRICS_T0022} missing, t0022 variant skipped",
            flush=True,
        )

    if VREST_METRICS_T0024.exists():
        records = _read_metrics(metrics_csv=VREST_METRICS_T0024)
        variants["t0024"] = build_variant(records=records)
    else:
        print(
            f"[write_metrics] WARNING: {VREST_METRICS_T0024} missing, t0024 variant skipped",
            flush=True,
        )

    METRICS_JSON.parent.mkdir(parents=True, exist_ok=True)
    METRICS_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"[write_metrics] wrote {METRICS_JSON}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
