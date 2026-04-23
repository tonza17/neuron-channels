"""Monkey-patch t0022 ``GABA_CONDUCTANCE_NULL_NS`` to 6.0 nS (halved from 12.0 nS).

Import this module FIRST — before any t0022 ``run_tuning_curve`` import — in every file that
touches the t0022 driver. The patch must run at module-import time so that
``from tasks.t0022_modify_dsgc_channel_testbed.code.run_tuning_curve import ...`` lines
elsewhere see the reduced conductance in their module-load snapshots.

The ``schedule_ei_onsets`` assertion at ``run_tuning_curve.py:327`` compares

    null_weight_us = GABA_CONDUCTANCE_PREFERRED_NS * gaba_null_pref_ratio * 1e-3

against

    GABA_CONDUCTANCE_NULL_NS * 1e-3.

Both ``GABA_CONDUCTANCE_PREFERRED_NS`` and ``GABA_CONDUCTANCE_NULL_NS`` inside that assertion
are module-local names bound at import time from ``t0022.code.constants``. Patching the
*source* module before the driver is imported is therefore sufficient for both the assertion
and every other downstream consumer.

For the caller in ``trial_runner_diameter.py`` the ratio passed into ``schedule_ei_onsets`` is
computed from the runner's own ``GABA_CONDUCTANCE_NULL_NS`` binding. That binding is rebound
locally via ``from ... import GABA_CONDUCTANCE_NULL_NS_OVERRIDE as GABA_CONDUCTANCE_NULL_NS``
so the ratio evaluates to ``6.0 / 3.0 = 2.0``.
"""

from __future__ import annotations

from tasks.t0022_modify_dsgc_channel_testbed.code import constants as _t0022_constants
from tasks.t0036_rerun_t0030_halved_null_gaba.code.constants import (
    GABA_CONDUCTANCE_NULL_NS_OVERRIDE,
)

_PREVIOUS_VALUE_NS: float = float(_t0022_constants.GABA_CONDUCTANCE_NULL_NS)
_t0022_constants.GABA_CONDUCTANCE_NULL_NS = GABA_CONDUCTANCE_NULL_NS_OVERRIDE

print(
    f"[gaba_override] GABA_CONDUCTANCE_NULL_NS = {GABA_CONDUCTANCE_NULL_NS_OVERRIDE} nS",
    flush=True,
)
print(
    "[gaba_override] Patched t0022 GABA_CONDUCTANCE_NULL_NS: "
    f"{_PREVIOUS_VALUE_NS} -> {GABA_CONDUCTANCE_NULL_NS_OVERRIDE}",
    flush=True,
)

# Module-level re-export for callers that need the rebound value in their own namespace.
GABA_CONDUCTANCE_NULL_NS: float = GABA_CONDUCTANCE_NULL_NS_OVERRIDE
