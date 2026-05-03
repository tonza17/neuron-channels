: CaT (low-voltage-activated T-type calcium channel) for t0076 channel sweep.
: Vendored from Hay et al. 2011 ModelDB 139653 mod/Ca_LVAst.mod (DOI 10.1371/journal.pcbi.1002107).
: Upstream kinetic source: Avery & Johnston 1996 J Neurosci (low-threshold Ca in CA1).
: Original SUFFIX Ca_LVAst -> renamed catt76 to namespace within the t0076 MOD library.
:
: m^2 * h activation with low-threshold V_half_m ~-40 mV (slope 6 mV);
: rapid inactivation V_half ~-90 mV with tau ~ 75 ms.
: Hay 2011 uses USEION ca; here NONSPECIFIC_CURRENT to match the t76 convention
: (see calt76.mod header for full rationale).

NEURON {
    SUFFIX catt76
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
    erev = 120  (mV)   : Ca reversal
    vh_m = -40  (mV)
    vh_h = -90  (mV)
    k_m  = 6    (mV)
    k_h  = -6   (mV)
    tau_m = 1.0 (ms)
    tau_h = 75  (ms)
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
