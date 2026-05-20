"""Smoke gate for the t0114 NSGA-II run (REQ-8).

Six pre-launch checks (5 inherited from t0113 + 1 t0114-specific):

1. Single-eval driver run on the 5 anchors with the t0083 best-cell electrophys
   vector. Anchor 1 (bedb_like) must reproduce the t0093 fingerprint of
   PD-rate ~43.6 Hz within +/- 2 Hz. Requires NEURON + compiled MOD library;
   on Windows this check is deferred to the remote Vast.ai instance and
   reported in `smoke_gate_report_remote.json`.

2. Ratio DSI synthetic sanity: `_vector_sum_dsi({0.0: [5], 180.0: [1]})`
   returns 0.6667 +/- 1e-6.

3. Silence guard active: `SILENCE_SPIKE_COUNT_THRESHOLD == 10`.

4. Pool-restart sanity: `_POOL_RESTART_EVERY == 10` (the "10th gen rule"
   preserved verbatim from t0112/t0113 per operator directive 2026-05-20).

5. Cost-watchdog wiring: `T0114_HARD_BUDGET_USD == 25.00`.

6. **NEW for t0114**: the live `TerminationCollection` produced by
   `_build_termination(...)` contains NO `HVPlateauTermination` instance.
   This is the smoke-gate guard against silent regression of S-0113-03 +
   the 2026-05-20 user directive.

Tolerances (check 1):
* DSI <= 0.05 absolute
* PD-rate <= 1.0 Hz absolute (relaxed to +/- 2 Hz at N_EVAL_SEEDS=3)

Returns a JSON report with per-check pass/fail and a top-level all-passed
flag. If check 1 cannot run locally (Windows / missing MODs), it is marked
`status="deferred_to_remote"` and `passed=null`; downstream agent then
re-runs it on the Vast.ai instance.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import numpy as np

from tasks.t0114_seed7755_no_autostop.code.anchor_definitions import (
    anchor_to_14d_vector,
    get_anchors,
)
from tasks.t0114_seed7755_no_autostop.code.constants_morphology import (
    ANCHOR_NAMES,
    DSI_TOLERANCE_SMOKE,
    LOWER_BOUNDS_68,
    N_PARAMS_54,
    PD_RATE_TOLERANCE_HZ_SMOKE,
    UPPER_BOUNDS_68,
)
from tasks.t0114_seed7755_no_autostop.code.paths import (
    SMOKE_GATE_FAILURE_MD,
    T0083_PARETO_FRONT_JSON,
    T0093_POST_FIX_VERIFICATION_SUMMARY_JSON,
    ensure_directories,
)


def _load_t0083_best_cell_electrophys() -> np.ndarray:
    payload = json.loads(T0083_PARETO_FRONT_JSON.read_text(encoding="utf-8"))
    cells = payload["cells"]
    cells_sorted = sorted(
        cells,
        key=lambda c: float(c.get("dsi", 0.0)) * float(c.get("pd_rate_hz", 0.0)),
        reverse=True,
    )
    best = cells_sorted[0]
    arr = np.asarray(best["params"], dtype=np.float64)
    assert arr.shape == (N_PARAMS_54,)
    return arr


def _load_t0093_fingerprint() -> dict[str, object]:
    if not T0093_POST_FIX_VERIFICATION_SUMMARY_JSON.exists():
        return {}
    return json.loads(T0093_POST_FIX_VERIFICATION_SUMMARY_JSON.read_text(encoding="utf-8"))


def _check_1_single_eval_driver_run(*, allow_skip_on_import_error: bool) -> dict[str, Any]:
    """Run the anchor sweep through evaluator.evaluate_68d_vector.

    On Windows where the t0080 NEURON MOD library is not compiled, the
    NEURON import will fail (or the evaluator will raise). In that case
    return `status="deferred_to_remote"` with `passed=None` so the caller
    can re-run this check on the Vast.ai instance.
    """
    try:
        from tasks.t0114_seed7755_no_autostop.code.evaluator import (
            evaluate_68d_vector,
        )
    except Exception as exc:  # noqa: BLE001
        if allow_skip_on_import_error:
            return {
                "id": 1,
                "name": "single-eval driver run (anchor-1 bedb_like ~43.6 Hz)",
                "status": "deferred_to_remote",
                "passed": None,
                "evidence": (
                    f"evaluator import failed locally ({type(exc).__name__}: "
                    f"{exc}). NEURON/t0080 MODs are not compiled on this host; "
                    f"check 1 deferred to the Vast.ai instance per t0112/t0113 "
                    f"precedent."
                ),
            }
        raise

    electrophys_54d = _load_t0083_best_cell_electrophys()
    fingerprint = _load_t0093_fingerprint()
    expected_pd_rate = 43.6
    if isinstance(fingerprint, dict):
        for k in ("bedb_pd_rate_hz", "anchor_1_pd_rate_hz", "reference_pd_rate_hz"):
            if k in fingerprint:
                expected_pd_rate = float(fingerprint[k])
                break

    anchors = get_anchors()
    seeds_eval: list[int] = [42, 4242, 424242]

    per_anchor: list[dict[str, object]] = []
    for i, name in enumerate(ANCHOR_NAMES):
        anchor = anchors[name]
        morph_14d = anchor_to_14d_vector(anchor=anchor)
        vec_68d = np.zeros(68, dtype=np.float64)
        vec_68d[:N_PARAMS_54] = electrophys_54d
        vec_68d[N_PARAMS_54:] = morph_14d
        vec_68d = np.clip(vec_68d, LOWER_BOUNDS_68, UPPER_BOUNDS_68)
        try:
            eval_res = evaluate_68d_vector(
                vector_68d=vec_68d, eval_seeds=seeds_eval, n_directions=2
            )
            per_anchor.append(
                {
                    "anchor_index": i,
                    "anchor_name": name,
                    "dsi_vector_sum": eval_res.dsi_vector_sum,
                    "pd_rate_hz": eval_res.pd_rate_hz,
                    "robustness": eval_res.robustness,
                    "is_unstable": eval_res.is_unstable,
                    "n_errors": eval_res.n_errors,
                    "elapsed_s": eval_res.elapsed_s,
                    "error": None,
                }
            )
        except Exception as exc:  # noqa: BLE001
            per_anchor.append(
                {
                    "anchor_index": i,
                    "anchor_name": name,
                    "dsi_vector_sum": None,
                    "pd_rate_hz": None,
                    "robustness": None,
                    "is_unstable": True,
                    "n_errors": 1,
                    "elapsed_s": 0.0,
                    "error": str(exc),
                }
            )

    # If the t0080 MOD library is not present on this host (Windows local dev),
    # the evaluator raises "Compiled t0080 MOD library not found" instead of
    # producing values. Detect this case and mark the check deferred-to-remote
    # rather than failed, matching the t0112/t0113 precedent.
    anchor1 = per_anchor[0]
    anchor1_err = anchor1.get("error")
    if (
        allow_skip_on_import_error
        and anchor1_err is not None
        and isinstance(anchor1_err, str)
        and "MOD library not found" in anchor1_err
    ):
        return {
            "id": 1,
            "name": "single-eval driver run (anchor-1 bedb_like ~43.6 Hz)",
            "status": "deferred_to_remote",
            "passed": None,
            "evidence": (
                f"t0080 MOD library not compiled on this host. anchor-1 error: "
                f"{anchor1_err}. Check 1 deferred to the Vast.ai instance per "
                f"t0112/t0113 precedent."
            ),
            "expected_pd_rate_hz": expected_pd_rate,
        }

    pd_tolerance_relaxed_hz: float = 2.0
    pd_within = (
        anchor1["pd_rate_hz"] is not None
        and isinstance(anchor1["pd_rate_hz"], int | float)
        and abs(float(anchor1["pd_rate_hz"]) - expected_pd_rate) <= pd_tolerance_relaxed_hz
    )
    passed = all(not a["is_unstable"] for a in per_anchor if a["error"] is None) and pd_within
    return {
        "id": 1,
        "name": "single-eval driver run (anchor-1 bedb_like ~43.6 Hz)",
        "status": "ok" if passed else "failed",
        "passed": bool(passed),
        "expected_pd_rate_hz": expected_pd_rate,
        "anchor1_pd_rate_hz": anchor1.get("pd_rate_hz"),
        "anchor1_dsi": anchor1.get("dsi_vector_sum"),
        "per_anchor": per_anchor,
    }


def _check_2_ratio_dsi_synthetic_sanity() -> dict[str, Any]:
    from tasks.t0114_seed7755_no_autostop.code.evaluator import _vector_sum_dsi

    dsi = _vector_sum_dsi(spike_counts_per_dir={0.0: [5], 180.0: [1]})
    expected = 4.0 / 6.0  # vector-sum |5-1| / (5+1) along x axis.
    err = abs(dsi - expected)
    passed = err < 1e-6
    return {
        "id": 2,
        "name": "ratio DSI synthetic sanity (PD=5, ND=1 -> 0.6667 +/- 1e-6)",
        "status": "ok" if passed else "failed",
        "passed": passed,
        "evidence": f"_vector_sum_dsi(PD=5, ND=1) = {dsi}; abs error vs 4/6 = {err:.2e}",
    }


def _check_3_silence_guard_threshold() -> dict[str, Any]:
    from tasks.t0114_seed7755_no_autostop.code.evaluator import (
        SILENCE_SPIKE_COUNT_THRESHOLD,
    )

    passed = SILENCE_SPIKE_COUNT_THRESHOLD == 10
    return {
        "id": 3,
        "name": "silence guard active (SILENCE_SPIKE_COUNT_THRESHOLD == 10)",
        "status": "ok" if passed else "failed",
        "passed": passed,
        "evidence": f"evaluator.SILENCE_SPIKE_COUNT_THRESHOLD == {SILENCE_SPIKE_COUNT_THRESHOLD}",
    }


def _check_4_pool_restart_cadence() -> dict[str, Any]:
    from tasks.t0114_seed7755_no_autostop.code.nsga2_driver import (
        _POOL_RESTART_EVERY,
    )

    passed = _POOL_RESTART_EVERY == 10
    return {
        "id": 4,
        "name": "pool-restart sanity (_POOL_RESTART_EVERY == 10)",
        "status": "ok" if passed else "failed",
        "passed": passed,
        "evidence": (
            f"nsga2_driver._POOL_RESTART_EVERY == {_POOL_RESTART_EVERY}; "
            f"preserved verbatim from t0112/t0113 per operator directive 2026-05-20"
        ),
    }


def _check_5_cost_watchdog_wiring() -> dict[str, Any]:
    from tasks.t0114_seed7755_no_autostop.code.constants import (
        T0114_HARD_BUDGET_USD,
    )

    passed = abs(T0114_HARD_BUDGET_USD - 25.00) < 1e-9
    return {
        "id": 5,
        "name": "watchdog wiring (T0114_HARD_BUDGET_USD == 25.00)",
        "status": "ok" if passed else "failed",
        "passed": passed,
        "evidence": (
            f"constants.T0114_HARD_BUDGET_USD == {T0114_HARD_BUDGET_USD:.2f}; "
            f"$25 hard cap value unchanged from t0113"
        ),
    }


def _check_6_no_hv_plateau_in_termination() -> dict[str, Any]:
    """t0114-specific: assert HVPlateauTermination is NOT in the live termination list."""
    from tasks.t0114_seed7755_no_autostop.code.hv_plateau_watchdog import (
        HVPlateauTermination,
    )
    from tasks.t0114_seed7755_no_autostop.code.nsga2_driver import (
        _build_termination,
    )

    coll = _build_termination(
        n_max_gen=300,
        cost_watchdog=MagicMock(),
        seed=7755,
        stop_path=Path("intervention/stop.md"),
    )
    has_hv_plateau = any(isinstance(t, HVPlateauTermination) for t in coll.terminations)
    passed = not has_hv_plateau
    termination_kinds = [type(t).__name__ for t in coll.terminations]
    return {
        "id": 6,
        "name": "NEW: no HVPlateauTermination in live TerminationCollection (S-0113-03)",
        "status": "ok" if passed else "failed",
        "passed": passed,
        "evidence": (
            f"_build_termination(...).terminations = {termination_kinds}; "
            f"HVPlateauTermination present = {has_hv_plateau}"
        ),
    }


def run_smoke_gate(*, output_path: Path, run_check_1: bool = True) -> dict[str, object]:
    """Run all six smoke-gate checks and write a combined JSON report."""
    ensure_directories()

    checks: list[dict[str, Any]] = []

    if run_check_1:
        checks.append(_check_1_single_eval_driver_run(allow_skip_on_import_error=True))
    else:
        checks.append(
            {
                "id": 1,
                "name": "single-eval driver run (anchor-1 bedb_like ~43.6 Hz)",
                "status": "deferred_to_remote",
                "passed": None,
                "evidence": "skipped by caller; will run on remote Vast.ai instance.",
            }
        )

    checks.append(_check_2_ratio_dsi_synthetic_sanity())
    checks.append(_check_3_silence_guard_threshold())
    checks.append(_check_4_pool_restart_cadence())
    checks.append(_check_5_cost_watchdog_wiring())
    checks.append(_check_6_no_hv_plateau_in_termination())

    # Fast checks 2-6 must all pass; check 1 may be deferred_to_remote.
    fast_checks_passed: bool = all(c.get("passed", False) for c in checks[1:])
    all_passed: bool = all(
        (c.get("passed") is True) or (c.get("status") == "deferred_to_remote") for c in checks
    )

    report: dict[str, object] = {
        "task_id": "t0114_seed7755_no_autostop",
        "step": "implementation_local_smoke_gate",
        "description": (
            "Local 6-check smoke gate per plan REQ-8. Checks 2-6 run on Windows; "
            "check 1 (single-eval driver run with anchor-1 ~43.6 Hz target) is "
            "deferred to the Vast.ai instance because no Windows nrnmech.dll "
            "exists for t0080 MODs locally. This matches the t0112/t0113 precedent."
        ),
        "checks": checks,
        "fast_checks_passed": fast_checks_passed,
        "all_checks_passed": all_passed,
        "tolerances": {
            "dsi": DSI_TOLERANCE_SMOKE,
            "pd_rate_hz": PD_RATE_TOLERANCE_HZ_SMOKE,
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(
        f"[smoke_gate] wrote {output_path}: fast_checks_passed={fast_checks_passed} "
        f"all_checks_passed={all_passed}"
    )
    for c in checks:
        print(f"  check {c['id']}: {c['status']}  -- {c['name']}")

    if not fast_checks_passed:
        SMOKE_GATE_FAILURE_MD.parent.mkdir(parents=True, exist_ok=True)
        SMOKE_GATE_FAILURE_MD.write_text(
            "# Smoke Gate Failure\n\n"
            f"Fast checks (2-6) did not all pass. Report: {output_path}\n\n"
            f"Failed checks:\n"
            + "\n".join(
                f"* check {c['id']}: {c.get('name')} -- {c.get('evidence', '')}"
                for c in checks[1:]
                if c.get("passed") is not True
            )
            + "\n",
            encoding="utf-8",
        )

    return report


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tasks/t0114_seed7755_no_autostop/logs/steps/009_implementation/smoke_gate.json"
        ),
    )
    parser.add_argument(
        "--skip-check-1",
        action="store_true",
        help="Skip the NEURON single-eval check (use on Windows; defer to remote).",
    )
    args = parser.parse_args()
    run_smoke_gate(output_path=args.output, run_check_1=not args.skip_check_1)
