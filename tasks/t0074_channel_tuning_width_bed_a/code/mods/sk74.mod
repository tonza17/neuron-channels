: SK / KCa2 (small-conductance Ca-activated K channel) for t0074 channel sweep.
: Adapted from Hay 2011 ModelDB 139653 SK_E2.mod (DOI 10.1371/journal.pcbi.1002107).
: Upstream citation: Kohler et al. 1996 (DOI 10.1126/science.273.5282.1709).
:
: Voltage-independent, purely Ca-driven activation:
:   m_inf = 1 / (1 + (EC50 / cai)^Hill)
: with EC50 = 0.43 uM, Hill = 4.8, tau = 1 ms (Hay 2011 SK_E2 defaults).
:
: NONSPECIFIC_CURRENT to avoid USEION k WRITE conflict with HHst.
: USEION ca READ cai for read-only Ca-dependence on the cad calcium pool.

NEURON {
    SUFFIX sk74
    USEION ca READ cai
    NONSPECIFIC_CURRENT i
    RANGE gbar, i
    GLOBAL erev, ec50_uM, hill, tau_m
}

UNITS {
    (mA) = (milliamp)
    (mV) = (millivolt)
    (S)  = (siemens)
    (mM) = (milli/liter)
    (uM) = (micro/liter)
}

PARAMETER {
    gbar = 0.0  (S/cm2)
    erev = -85  (mV)
    ec50_uM = 0.43      : Hay 2011 SK_E2 EC50 (uM)
    hill = 4.8          : Hay 2011 SK_E2 Hill exponent
    tau_m = 1.0 (ms)
}

ASSIGNED {
    v     (mV)
    cai   (mM)
    i     (mA/cm2)
    minf
}

STATE { m }

INITIAL {
    rates(cai)
    m = minf
}

BREAKPOINT {
    SOLVE states METHOD cnexp
    i = gbar * m * (v - erev)
}

DERIVATIVE states {
    rates(cai)
    m' = (minf - m) / tau_m
}

PROCEDURE rates(cai (mM)) {
    LOCAL ca_uM, ratio
    ca_uM = cai * 1000   : convert mM to uM
    if (ca_uM <= 1e-6) { ca_uM = 1e-6 }
    ratio = ec50_uM / ca_uM
    minf = 1 / (1 + ratio ^ hill)
}
