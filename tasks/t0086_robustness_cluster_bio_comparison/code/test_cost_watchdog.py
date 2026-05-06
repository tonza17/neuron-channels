"""Unit tests for cost_watchdog.py (REQ-X verification).

Asserts the watchdog uses the loaded rate from machine_log.json, NOT a
hard-coded constant. This is the regression test for t0083's $0.83 overrun.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

from tasks.t0086_robustness_cluster_bio_comparison.code.cost_watchdog import (
    T0086_HARD_BUDGET_USD,
    load_hourly_rate_from_machine_log,
    make_watchdog_from_machine_log,
)


def _write_machine_log(*, path: Path, rate_per_hour: float) -> None:
    """Write a minimal machine_log.json with the given rate."""
    payload: list[dict[str, object]] = [
        {
            "provider": "vast.ai",
            "instance_id": "test-instance",
            "selected_offer": {
                "offer_id": 99999,
                "price_per_hour": rate_per_hour,
            },
        }
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def test_load_hourly_rate_from_machine_log(tmp_path: Path) -> None:
    log_path = tmp_path / "machine_log.json"
    _write_machine_log(path=log_path, rate_per_hour=0.3209)
    rate = load_hourly_rate_from_machine_log(path=log_path)
    assert rate == 0.3209


def test_watchdog_uses_loaded_rate_not_hardcoded(tmp_path: Path) -> None:
    """Regression test: rate must come from machine_log, not from a constant.

    If the watchdog hard-coded $0.2382/hr, this test would fail because the
    machine_log specifies $0.3209/hr (t0083's actual rate).
    """
    log_path = tmp_path / "machine_log.json"
    _write_machine_log(path=log_path, rate_per_hour=0.3209)
    started_at = datetime.now(UTC) - timedelta(hours=1)
    watchdog = make_watchdog_from_machine_log(
        machine_log_path=log_path,
        instance_started_at=started_at,
    )
    assert watchdog.hourly_rate_usd == 0.3209
    # After 1 hour at $0.3209/hr, expected cost is $0.3209 (within float tolerance).
    cost = watchdog.current_cost_usd()
    assert 0.32 <= cost <= 0.33, f"expected ~$0.3209, got ${cost:.4f}"


def test_would_exceed_at_next_step(tmp_path: Path) -> None:
    log_path = tmp_path / "machine_log.json"
    _write_machine_log(path=log_path, rate_per_hour=0.3209)
    # Started 10 hours ago at $0.3209/hr -> cost is ~$3.21, under cap of $3.50.
    started_at = datetime.now(UTC) - timedelta(hours=10)
    watchdog = make_watchdog_from_machine_log(
        machine_log_path=log_path,
        instance_started_at=started_at,
    )
    # Currently under cap.
    assert watchdog.current_cost_usd() < T0086_HARD_BUDGET_USD
    # 1 more hour at $0.3209/hr would bring total to ~$3.53 -- over cap.
    assert watchdog.would_exceed_at_next_step(estimated_step_seconds=3600.0)


def test_trip_if_over_cap_writes_intervention(tmp_path: Path) -> None:
    log_path = tmp_path / "machine_log.json"
    _write_machine_log(path=log_path, rate_per_hour=0.3209)
    # Started 12 hours ago at $0.3209/hr -> cost is ~$3.85, OVER cap of $3.50.
    started_at = datetime.now(UTC) - timedelta(hours=12)
    watchdog = make_watchdog_from_machine_log(
        machine_log_path=log_path,
        instance_started_at=started_at,
    )
    intervention_path = tmp_path / "intervention" / "budget_overrun.md"
    tripped = watchdog.trip_if_over_cap(intervention_md_path=intervention_path)
    assert tripped
    assert intervention_path.exists()
    content = intervention_path.read_text(encoding="utf-8")
    assert "0.3209" in content
    assert "$3.50" in content


def test_rate_must_be_positive(tmp_path: Path) -> None:
    log_path = tmp_path / "machine_log.json"
    _write_machine_log(path=log_path, rate_per_hour=0.0)
    try:
        load_hourly_rate_from_machine_log(path=log_path)
    except AssertionError:
        return
    raise AssertionError("expected load_hourly_rate_from_machine_log to reject rate=0.0")
