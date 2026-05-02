: Kv4 / IA (transient A-type potassium) for t0074 channel sweep.
: Forked verbatim from tasks/t0067_t0065_soma_channel_addition_sweep/code/mods/kv4t67.mod
: with SUFFIX renamed to kv4t74 to avoid DLL collision.
: m^4 * h kinetics, V_half_act ~-50 mV, fast inactivation V_half ~-78 mV.
: Reference: Hoffman, Magee, Colbert, Johnston 1997 (Nature).

NEURON {
    SUFFIX kv4t74
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
    vh_m = -50 (mV)
    vh_h = -78 (mV)
    k_m  = 13  (mV)
    k_h  = -6  (mV)
    tau_m = 0.5 (ms)
    tau_h = 15  (ms)
}

ASSIGNED {
    v    (mV)
    i    (mA/cm2)
    minf
    hinf
}

STATE { m h }

BREAKPOINT {
    SOLVE states METHOD cnexp
    i = gbar * m * m * m * m * h * (v - erev)
}

DERIVATIVE states {
    rates(v)
    m' = (minf - m) / tau_m
    h' = (hinf - h) / tau_h
}

INITIAL {
    rates(v)
    m = minf
    h = hinf
}

PROCEDURE rates(v (mV)) {
    minf = 1.0 / (1.0 + exp(-(v - vh_m) / k_m))
    hinf = 1.0 / (1.0 + exp(-(v - vh_h) / k_h))
}
