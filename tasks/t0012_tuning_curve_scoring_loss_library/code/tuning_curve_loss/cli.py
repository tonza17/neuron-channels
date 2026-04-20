"""Command-line entry point for ``tuning_curve_loss``.

Usage (from repo root)::

    uv run python -m tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.cli \
        <simulated.csv> [--target <target.csv>] [--weights <weights.json>] [--json]

Exit codes:
* 0 on success
* 1 on missing input file
* 2 on argument parsing error (argparse default)
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.scoring import (
    ScoreReport,
    TuningCurveMetrics,
    score,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tuning_curve_loss.cli",
        description=(
            "Score a simulated tuning-curve CSV against the canonical target (from t0004) "
            "or a supplied target CSV."
        ),
    )
    parser.add_argument(
        "simulated",
        type=Path,
        help="Path to the simulated tuning-curve CSV.",
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=None,
        help="Path to the target CSV. Defaults to the t0004 curve_mean.csv.",
    )
    parser.add_argument(
        "--weights",
        type=Path,
        default=None,
        help="Path to a JSON file overriding the default weights.",
    )
    parser.add_argument(
        "--envelope",
        type=Path,
        default=None,
        help="(Currently ignored; placeholder for future envelope override.)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit the full ScoreReport as JSON on stdout.",
    )
    return parser


def _report_to_json(*, report: ScoreReport) -> str:
    # asdict() handles frozen dataclasses, nested dataclasses, and dict fields.
    payload: dict[str, object] = asdict(obj=report)
    return json.dumps(obj=payload, indent=2, default=float)


def _format_metrics_line(*, label: str, m: TuningCurveMetrics, include_reliability: bool) -> str:
    dsi: float = m.dsi
    peak: float = m.peak_hz
    null: float = m.null_hz
    hwhm: float = m.hwhm_deg
    body: str = (
        f"{label}  dsi={dsi:.4f}  peak={peak:.3f} Hz  null={null:.3f} Hz  hwhm={hwhm:.3f} deg"
    )
    if include_reliability:
        rel: str = f"{m.reliability:.4f}" if m.reliability is not None else "None"
        body = f"{body}  reliability={rel}"
    return body


def _report_to_text(*, report: ScoreReport) -> str:
    lines: list[str] = []
    lines.append(f"loss_scalar        = {report.loss_scalar:.6f}")
    lines.append(f"passes_envelope    = {report.passes_envelope}")
    lines.append(f"per_target_pass    = {report.per_target_pass}")
    lines.append(
        _format_metrics_line(
            label="candidate_metrics: ",
            m=report.candidate_metrics,
            include_reliability=True,
        )
    )
    lines.append(
        _format_metrics_line(
            label="target_metrics:    ",
            m=report.target_metrics,
            include_reliability=False,
        )
    )
    lines.append(f"residuals          = {report.residuals}")
    lines.append(f"normalized_resids  = {report.normalized_residuals}")
    lines.append(f"weights_used       = {report.weights_used}")
    if report.rmse_vs_target is not None:
        lines.append(f"rmse_vs_target     = {report.rmse_vs_target:.6f}")
    else:
        lines.append("rmse_vs_target     = None")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser: argparse.ArgumentParser = _build_parser()
    args: argparse.Namespace = parser.parse_args(args=argv)

    simulated: Path = args.simulated
    target: Path | None = args.target
    weights_path: Path | None = args.weights

    if not simulated.exists():
        print(f"error: simulated CSV not found: {simulated}", file=sys.stderr)
        return 1
    if target is not None and not target.exists():
        print(f"error: target CSV not found: {target}", file=sys.stderr)
        return 1
    if weights_path is not None and not weights_path.exists():
        print(f"error: weights JSON not found: {weights_path}", file=sys.stderr)
        return 1

    report: ScoreReport = score(
        simulated_curve_csv=simulated,
        target_curve_csv=target,
        weights_path=weights_path,
    )
    if args.json:
        sys.stdout.write(_report_to_json(report=report))
        sys.stdout.write("\n")
    else:
        sys.stdout.write(_report_to_text(report=report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
