"""Tests for the ``tuning_curve_loss.cli`` module."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.paths import (
    TARGET_MEAN_CSV,
)

CLI_MODULE: str = "tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.cli"


def _run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args=[sys.executable, "-m", CLI_MODULE, *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_cli_runs_on_t0004_curves() -> None:
    proc = _run_cli(str(TARGET_MEAN_CSV), "--target", str(TARGET_MEAN_CSV))
    assert proc.returncode == 0, f"CLI exit code {proc.returncode!r}; stderr={proc.stderr!r}"
    assert "loss_scalar" in proc.stdout, f"CLI stdout missing loss_scalar: {proc.stdout!r}"


def test_cli_missing_simulated_exits_1(tmp_path: Path) -> None:
    missing: Path = tmp_path / "no_such_file.csv"
    proc = _run_cli(str(missing))
    assert proc.returncode == 1, f"expected exit 1 for missing file, got {proc.returncode}"
    assert "error" in proc.stderr.lower()


def test_cli_json_output_parses() -> None:
    proc = _run_cli(
        str(TARGET_MEAN_CSV),
        "--target",
        str(TARGET_MEAN_CSV),
        "--json",
    )
    assert proc.returncode == 0, proc.stderr
    payload: dict[str, object] = json.loads(s=proc.stdout)
    assert "loss_scalar" in payload
    assert payload["loss_scalar"] == 0.0
    assert payload["passes_envelope"] is True


def test_cli_default_target_uses_t0004() -> None:
    # When --target is omitted, the CLI defaults to the t0004 target.
    proc = _run_cli(str(TARGET_MEAN_CSV))
    assert proc.returncode == 0, proc.stderr
    assert "loss_scalar" in proc.stdout


def test_cli_custom_weights_json(tmp_path: Path) -> None:
    weights_path: Path = tmp_path / "w.json"
    weights_path.write_text(
        data=json.dumps(
            obj={
                "dsi": 1.0,
                "peak": 0.0,
                "null": 0.0,
                "hwhm": 0.0,
            }
        ),
        encoding="utf-8",
    )
    proc = _run_cli(
        str(TARGET_MEAN_CSV),
        "--target",
        str(TARGET_MEAN_CSV),
        "--weights",
        str(weights_path),
        "--json",
    )
    assert proc.returncode == 0, proc.stderr
    payload: dict[str, object] = json.loads(s=proc.stdout)
    assert payload["weights_used"] == {
        "dsi": 1.0,
        "peak": 0.0,
        "null": 0.0,
        "hwhm": 0.0,
    }
