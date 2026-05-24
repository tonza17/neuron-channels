"""Cost watchdog (REQ-X) using actual instance hourly rate from machine_log.json.

This module fixes t0083's $0.83 budget overrun caused by a hard-coded
$0.2382/hr rate when the actual offer billed at $0.3209/hr (35% under-count).

The watchdog reads the per-instance hourly rate from
`logs/steps/008_setup-machines/machine_log.json`
`selected_offer.price_per_hour` at module init and exposes:

* `load_hourly_rate_from_machine_log(path)` -- helper for testing.
* `CostWatchdog` -- a class that tracks elapsed cost vs a hard cap.
* Module-level patcher `patch_t91_loop_rate(rate)` that re-assigns the
  t0080 module-level `_HOURLY_RATE_USD` so any nested calls into t0080's
  evaluator inherit the resolved rate.

Hard cap for t0086 is $3.50.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

T0104_HARD_BUDGET_USD: float = 4.00  # t0104 per-seed cap (REQ-11)


def load_hourly_rate_from_machine_log(*, path: Path) -> float:
    """Read selected_offer.price_per_hour from a Vast.ai machine_log.json.

    machine_log.json is a list of provisioning records (one per instance).
    The watchdog reads the LAST record (most recent provisioning).
    """
    raw = path.read_text(encoding="utf-8")
    records: list[dict[str, object]] = json.loads(raw)
    assert isinstance(records, list), "machine_log.json must be a list"
    assert len(records) > 0, "machine_log.json contains no records"
    last = records[-1]
    selected = last.get("selected_offer")
    assert isinstance(selected, dict), "last record missing selected_offer"
    rate_obj = selected.get("price_per_hour")
    assert isinstance(rate_obj, (int, float)), (
        f"selected_offer.price_per_hour must be numeric, got {type(rate_obj).__name__}"
    )
    rate: float = float(rate_obj)
    assert rate > 0.0, f"hourly rate must be positive, got {rate}"
    return rate


@dataclass(slots=True)
class CostWatchdog:
    """Real-time cost watchdog using the resolved per-instance hourly rate."""

    instance_started_at: datetime
    hourly_rate_usd: float
    hard_budget_usd: float = T0104_HARD_BUDGET_USD
    tripped: bool = field(default=False, init=False)

    def current_cost_usd(self) -> float:
        """Return real-time elapsed-hours x hourly_rate_usd."""
        now = datetime.now(UTC)
        elapsed_s: float = (now - self.instance_started_at).total_seconds()
        return (elapsed_s / 3600.0) * self.hourly_rate_usd

    def would_exceed_at_next_step(self, *, estimated_step_seconds: float) -> bool:
        """Return True if the hard cap would be breached after one more step."""
        now = datetime.now(UTC)
        elapsed_s: float = (now - self.instance_started_at).total_seconds()
        projected_s: float = elapsed_s + estimated_step_seconds
        projected_cost: float = (projected_s / 3600.0) * self.hourly_rate_usd
        return projected_cost >= self.hard_budget_usd

    def trip_if_over_cap(self, *, intervention_md_path: Path | None = None) -> bool:
        """Trip the watchdog if currently over the hard cap.

        Writes intervention/budget_overrun.md if a path is provided and the
        cap is breached for the first time.
        """
        cost = self.current_cost_usd()
        if cost >= self.hard_budget_usd and not self.tripped:
            self.tripped = True
            if intervention_md_path is not None:
                intervention_md_path.parent.mkdir(parents=True, exist_ok=True)
                intervention_md_path.write_text(
                    "# Budget Overrun\n\n"
                    f"t0104 per-seed cost watchdog tripped the "
                    f"${self.hard_budget_usd:.2f} cap.\n\n"
                    f"- Elapsed cost (USD): {cost:.4f}\n"
                    f"- Hourly rate (USD/hr): {self.hourly_rate_usd:.4f}\n"
                    f"- Hard cap: ${self.hard_budget_usd:.2f}\n"
                    f"- Tripped at: "
                    f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\n"
                    "\nPartial Pareto results for the affected seed are in "
                    "results/data/pareto_front_seed*.json (when generated).\n",
                    encoding="utf-8",
                )
        return self.tripped


def make_watchdog_from_machine_log(
    *,
    machine_log_path: Path,
    instance_started_at: datetime,
    hard_budget_usd: float = T0104_HARD_BUDGET_USD,
) -> CostWatchdog:
    """Factory: build a CostWatchdog using the rate from machine_log.json."""
    rate = load_hourly_rate_from_machine_log(path=machine_log_path)
    print(
        f"[cost_watchdog] resolved hourly rate: ${rate:.4f}/hr from machine_log.json (REQ-X)",
        flush=True,
    )
    return CostWatchdog(
        instance_started_at=instance_started_at,
        hourly_rate_usd=rate,
        hard_budget_usd=hard_budget_usd,
    )


def patch_t99_loop_rate(*, rate: float) -> None:
    """Patch the t0099 nsga2_driver module-level _HOURLY_RATE_USD constant."""
    from tasks.t0122_dsi_cytoplasm_volume_nsga2.code import nsga2_driver as drv

    drv._HOURLY_RATE_USD = rate
    print(
        f"[cost_watchdog] patched t0099.nsga2_driver._HOURLY_RATE_USD = ${rate:.4f}/hr",
        flush=True,
    )
