"""Identity test for the t0012 score() wiring used by this task.

Passing the canonical target CSV as both target and candidate must yield
loss_scalar == 0.0 (within float epsilon). This proves our score-import
path, CSV schema, and the round-trip from data -> metrics are all set up
correctly before we trust the ported tuning curve's loss value.
"""

from __future__ import annotations

import sys

from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import (
    score,
)
from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.paths import (
    TARGET_MEAN_CSV,
)


def test_identity() -> None:
    if not TARGET_MEAN_CSV.exists():
        raise FileNotFoundError(f"Target CSV missing at {TARGET_MEAN_CSV}")
    report = score(simulated_curve_csv=TARGET_MEAN_CSV, target_curve_csv=TARGET_MEAN_CSV)
    assert report.loss_scalar == 0.0, f"identity score must yield loss 0; got {report.loss_scalar}"
    assert report.rmse_vs_target == 0.0, f"identity RMSE must be 0; got {report.rmse_vs_target}"
    print(f"identity test passed: loss={report.loss_scalar} rmse={report.rmse_vs_target}")


def main() -> int:
    test_identity()
    return 0


if __name__ == "__main__":
    sys.exit(main())
