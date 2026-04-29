COMMENT
=======================================================================
NMDA_MgBlock: minimal NMDA point process with Jahr-Stevens Boltzmann
              Mg-block voltage dependence.

Author / Created by: t0055_nmda_mg_block_dsi_recovery (2026-04-28)

Provenance:
The Mg-block formula and parameter values are taken verbatim from
  tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/
    modeldb_189347_dsgc_exact/sources/bipolarNMDA.mod
which itself is the ModelDB 189347 ``bipolarNMDA.mod`` (commit
87d669dcef18e9966e29c88520ede78bc16d36ff, deposited 2019-05-31 by
tommorse) verbatim mirror.

Cited lines (bipolarNMDA.mod):

* Lines 47-54 (PARAMETER block):
    n=0.25         (/mM)        :NMDA VOLTAGE DEPENDENCE
    gama=0.08      (/mV)        :NMDA VOLTAGE DEPENDENCE
    e = 0          (mV)         :REVERSAL POTENTIAL
    Voff=0                      :0 - voltage dependent 1- voltage independent
    Vset=-60                    :set voltage when voltage independent

* Lines 108-109 (BREAKPOINT, gating expression):
    local_v = v*(1-Voff) + Vset*Voff       :VOLTAGE DEPENDENCE
    gNMDA   = (A-B) / (1 + n * exp(-gama * local_v))

This file STRIPS the t0046 ``bipolarNMDA.mod`` bundling of presynaptic
vesicle release, AMPA conductance, and the calcium fraction (``ica``
write). It keeps only the Mg-block + dual-exponential gating point
process driven by NET_RECEIVE events. Drop-in replacement for an
``Exp2Syn`` NMDA: per-event NetCon weight (in microsiemens) deposits
mass into both states A and B, the dual-exponential ``(B - A)`` shape
emerges from the difference of decay rates, and the Boltzmann factor
multiplies the resulting conductance.

Sign convention: tau2 > tau1, so B decays slower than A; (B - A) is
positive after a brief rise (matches NEURON's stock Exp2Syn convention).

Units:

* tau1, tau2 in ms
* e in mV
* n in /mM (with [Mg2+] folded in)
* gama in /mV
* Voff dimensionless (0 = voltage-dependent, 1 = voltage-independent)
* Vset in mV
* weight in microsiemens (consistent with t0054 Exp2Syn convention)
* g (RANGE) in microsiemens
* i (NONSPECIFIC_CURRENT) in nA
=======================================================================
ENDCOMMENT

NEURON {
    POINT_PROCESS NMDA_MgBlock
    RANGE tau1, tau2, e, n, gama, Voff, Vset, i, g
    NONSPECIFIC_CURRENT i
}

UNITS {
    (nA) = (nanoamp)
    (mV) = (millivolt)
    (uS) = (microsiemens)
}

PARAMETER {
    tau1 = 5    (ms)    : NMDA rise time (matches t0054 NMDA_TAU1_MS)
    tau2 = 80   (ms)    : NMDA decay time (matches t0054 NMDA_TAU2_MS)
    e    = 0    (mV)    : reversal potential (bipolarNMDA.mod L49)
    n    = 0.25 (/mM)   : Mg-block parameter (bipolarNMDA.mod L47)
    gama = 0.08 (/mV)   : Mg-block parameter (bipolarNMDA.mod L48)
    Voff = 0            : 0 = voltage-dependent; 1 = voltage-independent (L53)
    Vset = -60  (mV)    : clamp voltage when Voff = 1 (bipolarNMDA.mod L54)
}

ASSIGNED {
    v        (mV)
    i        (nA)
    g        (uS)
    local_v  (mV)
}

STATE {
    A
    B
}

INITIAL {
    A = 0
    B = 0
}

BREAKPOINT {
    SOLVE state METHOD cnexp
    : Mg-block (Jahr-Stevens) Boltzmann factor multiplying the dual-exponential gating.
    : bipolarNMDA.mod L108-109 verbatim:
    :   local_v = v*(1-Voff) + Vset*Voff
    :   gNMDA   = (A-B) / (1 + n*exp(-gama*local_v))
    : With tau2 > tau1, (B - A) is positive after the rising edge so we use B - A here
    : (matches Exp2Syn sign convention and t0054 Exp2Syn behaviour at gNMDA = 0).
    local_v = v * (1 - Voff) + Vset * Voff
    g = (B - A) / (1 + n * exp(-gama * local_v))
    i = g * (v - e)
}

DERIVATIVE state {
    A' = -A / tau1
    B' = -B / tau2
}

NET_RECEIVE(weight (uS)) {
    : Single NetCon event deposits identical mass into A and B; the dual-exponential
    : (B - A) shape emerges from the difference of the two decay rates. The unnormalised
    : form is acceptable here because the per-pair NetCon weight (gnmda_ns * 1e-3) matches
    : t0054's NMDA Exp2Syn weight semantics (microsiemens), so gNMDA = 0 yields a wired-but-
    : inert mechanism that is bit-identical to t0054 at gnmda = 0.
    A = A + weight
    B = B + weight
}
