: CaL (high-voltage-activated L-type calcium channel) for t0076 channel sweep.
: Vendored from Hay et al. 2011 ModelDB 139653 mod/Ca_HVA.mod (DOI 10.1371/journal.pcbi.1002107).
: Upstream kinetic source: Reuveni, Friedman, Amitai, Gutnick 1993 J Neurosci.
: Original SUFFIX Ca_HVA -> renamed calt76 to namespace within the t0076 MOD library.
:
: m^2 * h activation with V_half_m ~-27 mV (slope 5 mV); slow inactivation.
: Hay 2011 uses USEION ca READ eca WRITE ica; here we adopt NONSPECIFIC_CURRENT
: with a fixed Ca reversal of +120 mV to (a) keep the cad mechanism unaffected
: by additional ica writers and (b) match the t0067/t0074 vendoring convention
: where every t76 channel is NONSPECIFIC_CURRENT to dodge USEION conflicts.
: Conductance-equivalent for Ca driving force at typical Bed B Vm.

NEURON {
    SUFFIX calt76
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
    gbar = 0.0  (S/cm2)
    erev = 120  (mV)   : Ca reversal at typical [Ca]_o, [Ca]_i
    vh_m = -27  (mV)
    vh_h = -75  (mV)
    k_m  = 5    (mV)
    k_h  = -5   (mV)   : negative slope -> inactivation gates close on depol
    tau_m = 0.7 (ms)   : Reuveni 1993 fast activation
    tau_h = 60  (ms)   : Reuveni 1993 slow inactivation
}

ASSIGNED {
    v    (mV)
    i    (mA/cm2)
    minf
    hinf
}

STATE { m h }

INITIAL {
    rates(v)
    m = minf
    h = hinf
}

BREAKPOINT {
    SOLVE states METHOD cnexp
    i = gbar * m * m * h * (v - erev)
}

DERIVATIVE states {
    rates(v)
    m' = (minf - m) / tau_m
    h' = (hinf - h) / tau_h
}

PROCEDURE rates(v (mV)) {
    minf = 1.0 / (1.0 + exp(-(v - vh_m) / k_m))
    hinf = 1.0 / (1.0 + exp(-(v - vh_h) / k_h))
}
