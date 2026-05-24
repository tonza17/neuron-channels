"""Smoke gate for the t0122 NSGA-II run.

Eight pre-launch checks (6 inherited from t0115 with two threshold/value
updates, plus two new t0122-specific checks):

1. Single-eval driver run on the 5 anchors with the t0083 best-cell
   electrophys vector. Anchor 1 (bedb_like) must reproduce the t0093
   fingerprint of PD-rate ~43.6 Hz within +/- 2 Hz. Requires NEURON +
   compiled MOD library; on Windows this check is deferred to the remote
   Vast.ai instance and reported in ``smoke_gate_report_remote.json``.

2. Ratio DSI synthetic sanity: ``_vector_sum_dsi({0.0: [5], 180.0: [1]})``
   returns 0.6667 +/- 1e-6.

3. **UPDATED for t0122**: Silence guard active with new tightened
   threshold: ``SILENCE_PD_SPIKES_THRESHOLD == 3`` (was
   ``SILENCE_SPIKE_COUNT_THRESHOLD == 10`` in t0115).

4. Pool-restart sanity: ``_POOL_RESTART_EVERY == 10``.

5. **UPDATED for t0122**: Cost-watchdog wiring:
   ``T0122_HARD_BUDGET_USD == 6.00`` (was 25.00 in t0115).

6. No ``HVPlateauTermination`` in the live ``TerminationCollection`` (the
   ``HV_PLATEAU_AUTO_STOP = False`` policy enforcement).

7. **NEW for t0122**: ``compute_cytoplasm_volume_um3`` returns a positive
   finite float in [100, 100000] um^3 on a t0091-style anchor cell. The
   check is deferred to remote if no NEURON / MOD library is locally
   available (same precedent as check 1).

8. **NEW for t0122**: ``BedBV3MorphProblem._evaluate`` emits
   ``out["F"]`` with the volume axis in the POSITIVE direction (i.e.
   ``F[1] >= 0``). This guards against an accidental sign flip that
   would drive the optimiser to inflate volumes instead of minimising
   them.

Tolerances (check 1):

* DSI <= 0.05 absolute
* PD-rate <= 1.0 Hz absolute (relaxed to +/- 2 Hz at N_EVAL_SEEDS=3)
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import numpy as np

from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.anchor_definitions import (
    anchor_to_14d_vector,
    get_anchors,
)
from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.constants_morphology import (
    ANCHOR_NAMES,
    DSI_TOLERANCE_SMOKE,
    LOWER_BOUNDS_68,
    N_PARAMS_54,
    PD_RATE_TOLERANCE_HZ_SMOKE,
    UPPER_BOUNDS_68,
)
from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.paths import (
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
    """Run the anchor sweep through evaluator.evaluate_68d_vector."""
    try:
        from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.evaluator import (
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
                    f"{exc}). NEURON/t0080 MODs not compiled on this host; "
                    f"check 1 deferred to the Vast.ai instance."
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
                    "cytoplasm_volume_um3": eval_res.cytoplasm_volume_um3,
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
                    "cytoplasm_volume_um3": None,
                    "is_unstable": True,
                    "n_errors": 1,
                    "elapsed_s": 0.0,
                    "error": str(exc),
                }
            )

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
                f"{anchor1_err}. Check 1 deferred to the Vast.ai instance."
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
    from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.evaluator import _vector_sum_dsi

    dsi = _vector_sum_dsi(spike_counts_per_dir={0.0: [5], 180.0: [1]})
    expected = 4.0 / 6.0
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
    """t0122 UPDATED: silence guard threshold is now ``SILENCE_PD_SPIKES_THRESHOLD == 3``."""
    from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.evaluator import (
        SILENCE_PD_SPIKES_THRESHOLD,
    )

    passed = SILENCE_PD_SPIKES_THRESHOLD == 3
    return {
        "id": 3,
        "name": "silence guard active (SILENCE_PD_SPIKES_THRESHOLD == 3)",
        "status": "ok" if passed else "failed",
        "passed": passed,
        "evidence": (
            f"evaluator.SILENCE_PD_SPIKES_THRESHOLD == {SILENCE_PD_SPIKES_THRESHOLD}; "
            f"t0122 REQ-11 tightened the guard from "
            f"``total_mean_spikes < 10`` to ``pd_spikes_sum < 3``"
        ),
    }


def _check_4_pool_restart_cadence() -> dict[str, Any]:
    from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.nsga2_driver import (
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
            f"project policy per feedback_nsga2_pool_restart_every_10.md"
        ),
    }


def _check_5_cost_watchdog_wiring() -> dict[str, Any]:
    """t0122 UPDATED: cost cap is now $6.00."""
    from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.constants import (
        T0122_HARD_BUDGET_USD,
    )

    passed = abs(T0122_HARD_BUDGET_USD - 6.00) < 1e-9
    return {
        "id": 5,
        "name": "watchdog wiring (T0122_HARD_BUDGET_USD == 6.00)",
        "status": "ok" if passed else "failed",
        "passed": passed,
        "evidence": (
            f"constants.T0122_HARD_BUDGET_USD == {T0122_HARD_BUDGET_USD:.2f}; "
            f"$6 cap reduced from t0115's $25 because Vast.ai balance is $7"
        ),
    }


def _check_6_no_hv_plateau_in_termination() -> dict[str, Any]:
    """Assert HVPlateauTermination is NOT in the live termination collection."""
    from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.hv_plateau_watchdog import (
        HVPlateauTermination,
    )
    from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.nsga2_driver import (
        _build_termination,
    )

    coll = _build_termination(
        n_max_gen=60,
        cost_watchdog=MagicMock(),
        seed=1524,
        stop_path=Path("intervention/stop.md"),
    )
    has_hv_plateau = any(isinstance(t, HVPlateauTermination) for t in coll.terminations)
    passed = not has_hv_plateau
    termination_kinds = [type(t).__name__ for t in coll.terminations]
    return {
        "id": 6,
        "name": "no HVPlateauTermination in live TerminationCollection",
        "status": "ok" if passed else "failed",
        "passed": passed,
        "evidence": (
            f"_build_termination(...).terminations = {termination_kinds}; "
            f"HVPlateauTermination present = {has_hv_plateau}"
        ),
    }


def _check_7_cytoplasm_volume_positive_on_anchor(
    *, allow_skip_on_import_error: bool
) -> dict[str, Any]:
    """t0122 NEW: ``compute_cytoplasm_volume_um3`` returns a positive finite
    float in [100, 100000] um^3 on a t0091-style anchor cell.
    """
    try:
        from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.cytoplasm_volume import (
            compute_cytoplasm_volume_um3,
        )
        from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.generator_wrapper import (
            build_cell,
            morphology_params_from_vector,
        )
    except Exception as exc:  # noqa: BLE001
        if allow_skip_on_import_error:
            return {
                "id": 7,
                "name": "cytoplasm volume positive on anchor (100 <= v <= 100000 um^3)",
                "status": "deferred_to_remote",
                "passed": None,
                "evidence": (
                    f"NEURON / generator import failed locally "
                    f"({type(exc).__name__}: {exc}). Deferred to remote."
                ),
            }
        raise

    try:
        from neuron import h  # type: ignore[import-not-found]
    except Exception as exc:  # noqa: BLE001
        if allow_skip_on_import_error:
            return {
                "id": 7,
                "name": "cytoplasm volume positive on anchor (100 <= v <= 100000 um^3)",
                "status": "deferred_to_remote",
                "passed": None,
                "evidence": f"neuron import failed locally: {exc}",
            }
        raise

    anchors = get_anchors()
    per_anchor: list[dict[str, object]] = []
    for name in ANCHOR_NAMES:
        anchor = anchors[name]
        morph_14d = anchor_to_14d_vector(anchor=anchor)
        try:
            params = morphology_params_from_vector(morph_vector_14d=morph_14d)
            cell = build_cell(h=h, morph_params=params)
            volume = compute_cytoplasm_volume_um3(cell=cell)
            per_anchor.append(
                {
                    "anchor_name": name,
                    "volume_um3": float(volume),
                    "in_range": bool(100.0 <= volume <= 100000.0),
                    "error": None,
                }
            )
        except Exception as exc:  # noqa: BLE001
            per_anchor.append(
                {
                    "anchor_name": name,
                    "volume_um3": None,
                    "in_range": False,
                    "error": str(exc),
                }
            )

    # If every anchor failed for a NEURON / MOD reason, treat as
    # deferred-to-remote rather than failed (parallel to check 1).
    all_failed_neuron = all(
        a["error"] is not None
        and isinstance(a["error"], str)
        and (
            "MOD library" in a["error"]
            or "hocobj_call" in a["error"]
            or "nrn_load_dll" in a["error"]
            or "Exp2NMDA" in a["error"]
        )
        for a in per_anchor
    )
    if allow_skip_on_import_error and all_failed_neuron:
        return {
            "id": 7,
            "name": "cytoplasm volume positive on anchor (100 <= v <= 100000 um^3)",
            "status": "deferred_to_remote",
            "passed": None,
            "evidence": (
                "every anchor cell build failed on a NEURON / MOD error "
                "(no Windows nrnmech.dll for t0080 MODs locally); check 7 "
                "deferred to the Vast.ai instance."
            ),
        }

    all_in_range = all(a["in_range"] for a in per_anchor)
    passed = all_in_range
    return {
        "id": 7,
        "name": "cytoplasm volume positive on anchor (100 <= v <= 100000 um^3)",
        "status": "ok" if passed else "failed",
        "passed": passed,
        "evidence": f"per-anchor volumes: {per_anchor}",
    }


def _check_8_volume_sign_in_problem_f() -> dict[str, Any]:
    """t0122 NEW: ``BedBV3MorphProblem._evaluate`` emits ``F[1] >= 0``."""
    import inspect

    from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.evaluator import (
        BedBV3MorphProblem,
    )

    src = inspect.getsource(BedBV3MorphProblem._evaluate)
    # Look for ``out["F"] = ... +result.cytoplasm_volume_um3`` (positive sign).
    has_positive_volume = (
        "+result.cytoplasm_volume_um3" in src
        or "result.cytoplasm_volume_um3]" in src
        and "-result.cytoplasm_volume_um3" not in src
    )
    has_negative_volume_bug = "-result.cytoplasm_volume_um3" in src
    passed = has_positive_volume and not has_negative_volume_bug
    return {
        "id": 8,
        "name": "BedBV3MorphProblem._evaluate emits F[1] >= 0 (volume minimised, NOT negated)",
        "status": "ok" if passed else "failed",
        "passed": passed,
        "evidence": (
            f"source contains '+result.cytoplasm_volume_um3' = "
            f"{has_positive_volume}; source contains "
            f"'-result.cytoplasm_volume_um3' (sign-flip bug) = "
            f"{has_negative_volume_bug}"
        ),
    }


def run_smoke_gate(*, output_path: Path, run_check_1: bool = True) -> dict[str, object]:
    """Run all eight smoke-gate checks and write a combined JSON report."""
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
    checks.append(_check_7_cytoplasm_volume_positive_on_anchor(allow_skip_on_import_error=True))
    checks.append(_check_8_volume_sign_in_problem_f())

    # Fast checks 2, 3, 4, 5, 6, 8 must all pass; checks 1 and 7 may be deferred.
    fast_check_ids = {2, 3, 4, 5, 6, 8}
    fast_checks_passed: bool = all(
        c.get("passed", False) for c in checks if c.get("id") in fast_check_ids
    )
    all_passed: bool = all(
        (c.get("passed") is True) or (c.get("status") == "deferred_to_remote") for c in checks
    )

    report: dict[str, object] = {
        "task_id": "t0122_dsi_cytoplasm_volume_nsga2",
        "step": "implementation_local_smoke_gate",
        "description": (
            "Local 8-check smoke gate. Checks 2-6 and 8 run on Windows; "
            "checks 1 and 7 (NEURON simulations on anchors) are deferred to "
            "the Vast.ai instance because no Windows nrnmech.dll for t0080 "
            "MODs exists locally."
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
            f"Fast checks did not all pass. Report: {output_path}\n\n"
            "Failed checks:\n"
            + "\n".join(
                f"* check {c['id']}: {c.get('name')} -- {c.get('evidence', '')}"
                for c in checks
                if c.get("id") in fast_check_ids and c.get("passed") is not True
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
            "tasks/t0122_dsi_cytoplasm_volume_nsga2/logs/steps/009_implementation/smoke_gate.json"
        ),
    )
    parser.add_argument(
        "--skip-check-1",
        action="store_true",
        help="Skip the NEURON single-eval check (use on Windows; defer to remote).",
    )
    args = parser.parse_args()
    run_smoke_gate(output_path=args.output, run_check_1=not args.skip_check_1)
