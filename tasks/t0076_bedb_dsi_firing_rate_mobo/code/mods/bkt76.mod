: BK / KCa1.1 (large-conductance Ca-activated K channel) for t0076 channel sweep.
: Adapted from tasks/t0074_channel_tuning_width_bed_a/code/mods/bk74.mod;
: SUFFIX renamed bk74 -> bkt76 to namespace within the t0076 MOD library.
: Original derivation: Mainen-Sejnowski 1996 ModelDB 2488 kca.mod (DOI 10.1038/382363a0).
: Upstream citations: Pennefather 1990 (Hill exponent 1 on Ca);
:                    Reuveni et al. 1993 (V-half fitting in cortical neurons).
:
: Voltage- and Ca-dependent activation: m_inf = 1/(1 + exp(-(v-V_half)/k_m)) * cai/(cai + K_d).
: Single-gate kinetics with V_half ~-28 mV, K_d = 0.18 uM (Hill exponent 1), Q10 = 2.3.
:
: NONSPECIFIC_CURRENT to avoid USEION k WRITE conflict with HHst (which writes ik).
: USEION ca READ cai for read-only Ca-dependence on the cad calcium pool.

NEURON {
    SUFFIX bkt76
    USEION ca READ cai
    NONSPECIFIC_CURRENT i
    RANGE gbar, i
    GLOBAL erev, kd_uM, q10, temp
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
    vh_m = -28  (mV)
    k_m  = 12   (mV)
    kd_uM = 0.18      : Pennefather 1990 dissociation constant for [Ca]_i (uM)
    tau_m = 1.0 (ms)  : Mainen-Sejnowski default activation tau
    q10  = 2.3
    temp = 23   (degC)  : reference temperature for the source MOD
}

ASSIGNED {
    v     (mV)
    cai   (mM)
    celsius (degC)
    i     (mA/cm2)
    minf
    qt
}

STATE { m }

INITIAL {
    qt = q10 ^ ((celsius - temp) / 10)
    rates(v, cai)
    m = minf
}

BREAKPOINT {
    SOLVE states METHOD cnexp
    i = gbar * m * (v - erev)
}

DERIVATIVE states {
    rates(v, cai)
    m' = (minf - m) / (tau_m / qt)
}

PROCEDURE rates(v (mV), cai (mM)) {
    LOCAL ca_uM, v_act, ca_act
    ca_uM = cai * 1000           : convert mM to uM
    if (ca_uM < 0) { ca_uM = 0 }
    v_act = 1 / (1 + exp(-(v - vh_m) / k_m))
    ca_act = ca_uM / (ca_uM + kd_uM)
    minf = v_act * ca_act
}
