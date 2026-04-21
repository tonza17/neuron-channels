"""V_rest override helper.

Sets ``h.v_init`` and walks ``h.allsec()`` to set every HHst-bearing section's
``eleak_HHst`` and every pas-bearing section's ``e_pas`` RANGE variable to the
target resting potential. Must be called AFTER the model's own parameter
application (``apply_params`` for t0022 / per-section configuration for t0024)
and BEFORE ``h.finitialize(...)`` so the steady-state solver sees the new leak
reversals when equilibrating membrane voltage.

The per-section loop is required because both backing models set ``eleak_HHst``
(and, for t0022, ``e_pas``) once at cell-build time using module-level
constants. Simply overriding the Python-side constant has no retroactive effect
on sections that already exist in the NEURON runtime.
"""

from __future__ import annotations

from typing import Any


def set_vrest(*, h: Any, v_rest_mv: float) -> None:
    """Set ``h.v_init`` and every section's leak reversal to ``v_rest_mv``.

    Args:
        h: the NEURON ``h`` top-level namespace (``from neuron import h``).
        v_rest_mv: target resting potential in millivolts.
    """
    h.v_init = float(v_rest_mv)

    for sec in h.allsec():
        # HHst sections: the leak reversal RANGE variable is ``eleak_HHst``.
        if h.ismembrane("HHst", sec=sec):
            for seg in sec:
                seg.eleak_HHst = float(v_rest_mv)
        # pas sections (t0022 only): standard pas RANGE variable ``e_pas``.
        if h.ismembrane("pas", sec=sec):
            for seg in sec:
                seg.e_pas = float(v_rest_mv)
