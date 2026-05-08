"""Insert baseline HHst + cad channels on a procedurally built cell.

Copied from
``tasks/t0090_morphology_generator_diversity_test/code/verification.py:125-137``
because that helper is task-internal in t0090, not a library entry point. The
copy preserves the exact insertion behaviour:

* HHst + cad on soma + every dendrite section
* HHst on the two AIS subsegments

NEURON treats duplicate ``insert(name)`` calls as silent no-ops, so this helper
is idempotent without its own cache.
"""

from __future__ import annotations

from typing import Any


def insert_baseline_channels(*, h: Any, cell: Any) -> None:
    """Insert HHst + cad on soma + dendrites + AIS of one cell.

    The ``h`` argument is accepted but not used; it is kept in the signature for
    consistency with downstream call sites that pass it explicitly. NEURON's
    section attributes are accessed directly through the section objects.
    """
    _ = h  # explicit unused-arg marker; keeps strict-mypy quiet without a noqa.
    sections: list[Any] = [cell.soma] + list(cell.all_dends)
    for sec in sections:
        sec.insert("HHst")
        sec.insert("cad")
    for ais_sec in (cell.ais_proximal, cell.ais_distal):
        ais_sec.insert("HHst")
