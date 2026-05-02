: Nav1.6 (fast, low-threshold transient sodium) for t0074 channel sweep.
: Forked verbatim from tasks/t0067_t0065_soma_channel_addition_sweep/code/mods/nav16t67.mod
: with SUFFIX renamed to nav16t74 to avoid DLL collision.
: m^3 * h kinetics. Activation V_half ~-43 mV, inactivation V_half ~-65 mV.
: Reference: Carter & Bean 2009 (J Neurophysiol); Khaliq et al. 2003 (JNeurosci).
: NONSPECIFIC_CURRENT to avoid USEION conflicts with the existing HHst mechanism.

NEURON {
    SUFFIX nav16t74
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
    vh_m = -43 (mV)
    vh_h = -65 (mV)
    k_m  = 7   (mV)
    k_h  = -7  (mV)
    tau_m = 0.05 (ms)
}

ASSIGNED {
    v   (mV)
    i   (mA/cm2)
    minf
    hinf
    tau_h (ms)
}

STATE {
    m
    h
}

BREAKPOINT {
    SOLVE states METHOD cnexp
    i = gbar * m * m * m * h * (v - erev)
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
    tau_h = 0.5 + 8.0 / (1.0 + exp((v + 40) / 5))
}
