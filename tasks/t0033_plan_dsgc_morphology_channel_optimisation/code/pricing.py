"""Vast.ai tier pricing snapshot (static; not a live quote).

Writes ``vastai_pricing_snapshot.json`` with one entry per priced tier
(RTX 3090, RTX 4090, A100 40 GB, H100, plus the 96-core CPU node used as
the many-core CPU fallback). Prices are plan-side median observations
dated ``PRICING_SNAPSHOT_DATE``; the plan's answer asset explicitly flags
that these are not live quotes.

The ``filters_applied`` field records the exact ``DEFAULT_FILTERS`` string
from ``arf/scripts/utils/vast_machines.py``.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any

from arf.scripts.utils.vast_machines import DEFAULT_FILTERS, GPU_SPEED_TIERS
from tasks.t0033_plan_dsgc_morphology_channel_optimisation.code import paths
from tasks.t0033_plan_dsgc_morphology_channel_optimisation.code.constants import (
    PRICING_SNAPSHOT_DATE,
    PRICING_SOURCE_NOTE,
    Tier,
)


@dataclass(frozen=True, slots=True)
class PricingRow:
    tier: str
    dollars_per_hour: float
    speed_tier_ratio: float
    snapshot_date: str
    filters_applied: str
    source: str


# Plan-side median prices. Snapshot date committed in constants.
_TIER_PRICE_USD_PER_HOUR: dict[Tier, float] = {
    Tier.RTX_3090: 0.20,
    Tier.RTX_4090: 0.50,
    Tier.A100_40GB: 1.10,
    Tier.H100: 2.50,
    Tier.CPU_96: 0.40,
}


def build_pricing_rows() -> list[PricingRow]:
    rows: list[PricingRow] = []
    for tier, price in _TIER_PRICE_USD_PER_HOUR.items():
        # CPU tier ratio is not meaningful; set to 1.0 as placeholder.
        ratio = 1.0 if tier is Tier.CPU_96 else GPU_SPEED_TIERS[tier.value]
        rows.append(
            PricingRow(
                tier=tier.value,
                dollars_per_hour=price,
                speed_tier_ratio=ratio,
                snapshot_date=PRICING_SNAPSHOT_DATE,
                filters_applied=DEFAULT_FILTERS,
                source=PRICING_SOURCE_NOTE,
            )
        )
    return rows


def main() -> None:
    paths.DATA_DIR.mkdir(parents=True, exist_ok=True)
    rows = build_pricing_rows()
    serialised: list[dict[str, Any]] = [asdict(r) for r in rows]
    paths.PRICING_JSON.write_text(json.dumps(serialised, indent=2), encoding="utf-8")
    print(f"Wrote {len(rows)} rows to {paths.PRICING_JSON}")
    for row in rows:
        print(
            f"  {row.tier:<12}  ${row.dollars_per_hour:.2f}/h  "
            f"speed_ratio={row.speed_tier_ratio:.2f}"
        )
    print(f"  filters_applied={DEFAULT_FILTERS}")


if __name__ == "__main__":
    main()
