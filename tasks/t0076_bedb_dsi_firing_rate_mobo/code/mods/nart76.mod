: NaR (resurgent sodium) for t0076 channel sweep.
: Adapted from tasks/t0067_t0065_soma_channel_addition_sweep/code/mods/nart67.mod;
: SUFFIX renamed nart67 -> nart76 to namespace within the t0076 MOD library.
: Approximated as a slowly-recovering Nav with a slow inactivation gate that
: re-opens during the spike afterhyperpolarisation (Khaliq, Gouwens, Raman 2003).
: Simplified m^3 * h * s where s reactivates around -50 mV (the resurgent peak).

NEURON {
    SUFFIX nart76
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
    erev = 50  (mV)
    vh_m = -45 (mV)
    vh_h = -70 (mV)
    vh_s = -50 (mV)
    k_m  = 7   (mV)
    k_h  = -7  (mV)
    k_s  = 4   (mV)
    tau_m = 0.05 (ms)
    tau_h = 4.0  (ms)
    tau_s = 12.0 (ms)
}

ASSIGNED {
    v     (mV)
    i     (mA/cm2)
    minf
    hinf
    sinf
}

STATE { m h s }

BREAKPOINT {
    SOLVE states METHOD cnexp
    i = gbar * m * m * m * h * s * (v - erev)
}

DERIVATIVE states {
    rates(v)
    m' = (minf - m) / tau_m
    h' = (hinf - h) / tau_h
    s' = (sinf - s) / tau_s
}

INITIAL {
    rates(v)
    m = minf
    h = hinf
    s = sinf
}

PROCEDURE rates(v (mV)) {
    minf = 1.0 / (1.0 + exp(-(v - vh_m) / k_m))
    hinf = 1.0 / (1.0 + exp(-(v - vh_h) / k_h))
    sinf = 1.0 / (1.0 + exp((v - vh_s) / k_s))
}
