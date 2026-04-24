"""Runtime-parameterised monkey-patch of t0022 ``GABA_CONDUCTANCE_NULL_NS``.

Unlike t0036's import-time patch (which hard-coded 6.0 nS via a module-load side-effect), this
module exposes a function ``set_null_gaba_ns(*, value_ns)`` that can be called repeatedly with
different values -- enabling a multi-level ladder sweep in a single process.

Two module-level attributes are rebound on every call so that stale imports anywhere in the
NEURON driver chain see the refreshed value:

1. ``tasks.t0022_modify_dsgc_channel_testbed.code.constants.GABA_CONDUCTANCE_NULL_NS`` -- the
   source attribute.
2. ``tasks.t0022_modify_dsgc_channel_testbed.code.run_tuning_curve.GABA_CONDUCTANCE_NULL_NS`` --
   the caller-local copy that ``schedule_ei_onsets`` (at ``run_tuning_curve.py:327``) compares
   ``null_weight_us`` against. Without this rebind, any module already imported before the first
   ``set_null_gaba_ns`` call would hold the stale 12.0 nS default.

Call this function AT THE START of every trial (not just every GABA level) to harden against
any downstream module caching the value in its own namespace.
"""

from __future__ import annotations

# Default value present in t0022 constants prior to any override (bookkeeping only).
GABA_CONDUCTANCE_NULL_NS_DEFAULT_NS: float = 12.0


def set_null_gaba_ns(*, value_ns: float) -> None:
    """Write ``value_ns`` into t0022 ``GABA_CONDUCTANCE_NULL_NS`` (runtime patch).

    Performs a double-binding write: both the ``constants`` source attribute and the
    ``run_tuning_curve`` caller-local copy are updated, so ``schedule_ei_onsets`` sees the
    refreshed value regardless of import order.
    """
    from tasks.t0022_modify_dsgc_channel_testbed.code import constants as _t0022_constants
    from tasks.t0022_modify_dsgc_channel_testbed.code import run_tuning_curve as _t0022_driver

    _previous_ns: float = float(_t0022_constants.GABA_CONDUCTANCE_NULL_NS)
    _t0022_constants.GABA_CONDUCTANCE_NULL_NS = value_ns
    # ``run_tuning_curve`` imports ``GABA_CONDUCTANCE_NULL_NS`` from ``constants`` at load time
    # into its own module namespace. The assertion at ``run_tuning_curve.py:327`` compares
    # ``null_weight_us`` against that caller-local copy, so we must rebind it here too.
    # mypy's --no-implicit-reexport rule hides this attribute; setattr is the cleanest path.
    setattr(_t0022_driver, "GABA_CONDUCTANCE_NULL_NS", value_ns)  # noqa: B010

    print(
        f"[gaba_override] GABA_CONDUCTANCE_NULL_NS = {value_ns} nS (previous = {_previous_ns} nS)",
        flush=True,
    )
