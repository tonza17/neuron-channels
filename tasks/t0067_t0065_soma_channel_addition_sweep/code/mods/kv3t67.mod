: Kv3 (fast delayed-rectifier potassium) for t0067 channel sweep.
: m^4 kinetics, V_half ~-15 mV, fast time constant (~1 ms).
: Reference: Erisir, Lau, Rudy, Leonard 1999 (J Neurophysiol).

NEURON {
    SUFFIX kv3t67
    NONSPECIFIC_CURRENT i
    RANGE gbar, i
    GLOBAL erev
}

UNITS {
    (mA) = (milliamp)
    (mV) = (millivolt)
    (S)  = (siemens)
}

PARAMETER {
    gbar = 0.0 (S/cm2)
    erev = -85 (mV)
    vh_m = -15 (mV)
    k_m  = 12  (mV)
    tau_m = 1.0 (ms)
}

ASSIGNED {
    v    (mV)
    i    (mA/cm2)
    minf
}

STATE { m }

BREAKPOINT {
    SOLVE states METHOD cnexp
    i = gbar * m * m * m * m * (v - erev)
}

DERIVATIVE states {
    rates(v)
    m' = (minf - m) / tau_m
}

INITIAL {
    rates(v)
    m = minf
}

PROCEDURE rates(v (mV)) {
    minf = 1.0 / (1.0 + exp(-(v - vh_m) / k_m))
}
