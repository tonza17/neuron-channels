/* Created by Language version: 7.7.0 */
/* VECTORIZED */
#define NRN_VECTORIZED 1
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "mech_api.h"
#undef PI
#define nil 0
#include "md1redef.h"
#include "section.h"
#include "nrniv_mf.h"
#include "md2redef.h"

#if METHOD3
extern int _method3;
#endif

#if !NRNGPU
#undef exp
#define exp hoc_Exp
extern double hoc_Exp(double);
#endif

#define nrn_init _nrn_init__gaba_tonic
#define _nrn_initial _nrn_initial__gaba_tonic
#define nrn_cur _nrn_cur__gaba_tonic
#define _nrn_current _nrn_current__gaba_tonic
#define nrn_jacob _nrn_jacob__gaba_tonic
#define nrn_state _nrn_state__gaba_tonic
#define _net_receive _net_receive__gaba_tonic

#define _threadargscomma_ _p, _ppvar, _thread, _nt,
#define _threadargsprotocomma_ double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt,
#define _threadargs_ _p, _ppvar, _thread, _nt
#define _threadargsproto_ double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg(int);
 /* Thread safe. No static _p or _ppvar. */

#define t _nt->_t
#define dt _nt->_dt
#define g _p[0]
#define g_columnindex 0
#define e _p[1]
#define e_columnindex 1
#define t_on _p[2]
#define t_on_columnindex 2
#define t_off _p[3]
#define t_off_columnindex 3
#define ramp_ms _p[4]
#define ramp_ms_columnindex 4
#define i _p[5]
#define i_columnindex 5
#define v _p[6]
#define v_columnindex 6
#define _g _p[7]
#define _g_columnindex 7
#define _nd_area  *_ppvar[0]._pval

#if MAC
#if !defined(v)
#define v _mlhv
#endif
#if !defined(h)
#define h _mlhh
#endif
#endif

#if defined(__cplusplus)
extern "C" {
#endif
 static int hoc_nrnpointerindex =  -1;
 static Datum* _extcall_thread;
 static Prop* _extcall_prop;
 /* external NEURON variables */
 /* declaration of user functions */
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_prop_size(int, int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
extern Memb_func* memb_func;

#define NMODL_TEXT 1
#if NMODL_TEXT
static const char* nmodl_file_text;
static const char* nmodl_filename;
extern void hoc_reg_nmodl_text(int, const char*);
extern void hoc_reg_nmodl_filename(int, const char*);
#endif

 extern Prop* nrn_point_prop_;
 static int _pointtype;
 static void* _hoc_create_pnt(Object* _ho) { void* create_point_process(int, Object*);
 return create_point_process(_pointtype, _ho);
}
 static void _hoc_destroy_pnt(void*);
 static double _hoc_loc_pnt(void* _vptr) {double loc_point_process(int, void*);
 return loc_point_process(_pointtype, _vptr);
}
 static double _hoc_has_loc(void* _vptr) {double has_loc_point(void*);
 return has_loc_point(_vptr);
}
 static double _hoc_get_loc_pnt(void* _vptr) {
 double get_loc_point_process(void*); return (get_loc_point_process(_vptr));
}
 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _extcall_prop = _prop;
 }
 static void _hoc_setdata(void* _vptr) { Prop* _prop;
 _prop = ((Point_process*)_vptr)->_prop;
   _setdata(_prop);
 }
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 0,0
};
 static Member_func _member_func[] = {
 "loc", _hoc_loc_pnt,
 "has_loc", _hoc_has_loc,
 "get_loc", _hoc_get_loc_pnt,
 0, 0
};
 /* declare global and static user variables */
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "g", "uS",
 "e", "mV",
 "t_on", "ms",
 "t_off", "ms",
 "ramp_ms", "ms",
 "i", "nA",
 0,0
};
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 0,0
};
 static DoubVec hoc_vdoub[] = {
 0,0,0
};
 static double _sav_indep;
 static void nrn_alloc(Prop*);
static void  nrn_init(NrnThread*, _Memb_list*, int);
static void nrn_state(NrnThread*, _Memb_list*, int);
 static void nrn_cur(NrnThread*, _Memb_list*, int);
static void  nrn_jacob(NrnThread*, _Memb_list*, int);
 static void _hoc_destroy_pnt(void* _vptr) {
   destroy_point_process(_vptr);
}
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"gaba_tonic",
 "g",
 "e",
 "t_on",
 "t_off",
 "ramp_ms",
 0,
 "i",
 0,
 0,
 0};

extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
  if (nrn_point_prop_) {
	_prop->_alloc_seq = nrn_point_prop_->_alloc_seq;
	_p = nrn_point_prop_->param;
	_ppvar = nrn_point_prop_->dparam;
 }else{
 	_p = nrn_prop_data_alloc(_mechtype, 8, _prop);
 	/*initialize range parameters*/
 	g = 0;
 	e = -75;
 	t_on = 0;
 	t_off = 0;
 	ramp_ms = 1;
  }
 	_prop->param = _p;
 	_prop->param_size = 8;
  if (!nrn_point_prop_) {
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 2, _prop);
  }
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/

}
 static void _initlists();
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _GabaTonic_reg() {
	int _vectorized = 1;
  _initlists();
 	_pointtype = point_register_mech(_mechanism,
	 nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init,
	 hoc_nrnpointerindex, 1,
	 _hoc_create_pnt, _hoc_destroy_pnt, _member_func);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 8, 2);
  hoc_register_dparam_semantics(_mechtype, 0, "area");
  hoc_register_dparam_semantics(_mechtype, 1, "pntproc");
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 gaba_tonic GabaTonic.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static char *modelname = "";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {
  int _i; double _save;{

}
}

static void nrn_init(NrnThread* _nt, _Memb_list* _ml, int _type){
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v = _v;
 initmodel(_p, _ppvar, _thread, _nt);
}
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt, double _v){double _current=0.;v=_v;{ {
   double _ld_on , _ld_off , _lenv ;
 if ( t < t_on ) {
     _lenv = 0.0 ;
     }
   else if ( t > t_off ) {
     _lenv = 0.0 ;
     }
   else if ( ramp_ms <= 0.0 ) {
     _lenv = 1.0 ;
     }
   else {
     _ld_on = t - t_on ;
     _ld_off = t_off - t ;
     if ( _ld_on < ramp_ms ) {
       _lenv = 0.5 * ( 1.0 - cos ( 3.14159265358979 * _ld_on / ramp_ms ) ) ;
       }
     else if ( _ld_off < ramp_ms ) {
       _lenv = 0.5 * ( 1.0 - cos ( 3.14159265358979 * _ld_off / ramp_ms ) ) ;
       }
     else {
       _lenv = 1.0 ;
       }
     }
   i = _lenv * g * ( v - e ) ;
   }
 _current += i;

} return _current;
}

static void nrn_cur(NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 _g = _nrn_current(_p, _ppvar, _thread, _nt, _v + .001);
 	{ _rhs = _nrn_current(_p, _ppvar, _thread, _nt, _v);
 	}
 _g = (_g - _rhs)/.001;
 _g *=  1.e2/(_nd_area);
 _rhs *= 1.e2/(_nd_area);
#if CACHEVEC
  if (use_cachevec) {
	VEC_RHS(_ni[_iml]) -= _rhs;
  }else
#endif
  {
	NODERHS(_nd) -= _rhs;
  }

}

}

static void nrn_jacob(NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml];
#if CACHEVEC
  if (use_cachevec) {
	VEC_D(_ni[_iml]) += _g;
  }else
#endif
  {
     _nd = _ml->_nodelist[_iml];
	NODED(_nd) += _g;
  }

}

}

static void nrn_state(NrnThread* _nt, _Memb_list* _ml, int _type) {

}

static void terminal(){}

static void _initlists(){
 double _x; double* _p = &_x;
 int _i; static int _first = 1;
  if (!_first) return;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif

#if NMODL_TEXT
static const char* nmodl_filename = "GabaTonic.mod";
static const char* nmodl_file_text =
  "COMMENT\n"
  "=======================================================================\n"
  "gaba_tonic: minimal tonic GABA POINT_PROCESS with a sustained\n"
  "            conductance window (t_on, t_off) and a 1 ms cosine ramp at\n"
  "            each window edge.\n"
  "\n"
  "Author / Created by: t0057_tonic_gaba_sweep_t0053 (2026-04-28)\n"
  "\n"
  "Provenance:\n"
  "This MOD is task-specific (no upstream provenance). It replaces the\n"
  "per-event Exp2Syn GABA mechanism used by the parent task\n"
  "(t0053_minimal_dsgc_spatial_gaba). The motivation is documented in\n"
  "tasks/t0057_tonic_gaba_sweep_t0053/task_description.md: per-event\n"
  "Exp2Syn GABA with tau2 = 20 ms decays within ~100-200 ms of the bar-\n"
  "arrival time, leaving the cell uninhibited for the remaining ~1100 ms\n"
  "of the 1500 ms trial. Real SAC->DSGC IPSCs envelope over 100-300 ms\n"
  "through multiple GABA release events; the simplest model that matches\n"
  "this is a sustained tonic conductance over the full stimulus window,\n"
  "gated by the same per-synapse spatial centripetal-gating predicate\n"
  "from t0053.\n"
  "\n"
  "Conductance envelope:\n"
  "\n"
  "  g_eff(t) = g * envelope(t)\n"
  "\n"
  "  envelope(t) = 0                                          if t < t_on or t > t_off\n"
  "              = 0.5 * (1 - cos(pi * (t - t_on)  / ramp))   if (t - t_on) < ramp\n"
  "              = 0.5 * (1 - cos(pi * (t_off - t) / ramp))   if (t_off - t) < ramp\n"
  "              = 1                                          otherwise\n"
  "\n"
  "The 1 ms cosine ramp at each edge avoids stiff-step integrator\n"
  "artefacts under CVODE (variable time-stepping). The default ramp width\n"
  "is 1 ms; setting ramp_ms to 0 yields a piecewise-constant envelope\n"
  "(this is acceptable per the task description \"piecewise constant is\n"
  "acceptable\" clause but may produce visible CVODE step events).\n"
  "\n"
  "No NET_RECEIVE block is present: the conductance is set by direct\n"
  "attribute write to .g, .t_on, .t_off, .e per-trial in the Python\n"
  "scheduler (synapses.schedule_ei_onsets). This decouples conductance\n"
  "amplitude from event-decay-tau interactions, which is the headline\n"
  "goal of the t0057 sweep.\n"
  "\n"
  "Units:\n"
  "\n"
  "* g          (uS)   tonic peak conductance, set per trial\n"
  "* e          (mV)   reversal potential (default -75 mV; matches\n"
  "                    t0053 GABA_E_MV)\n"
  "* t_on       (ms)   window opening time, set per trial\n"
  "* t_off      (ms)   window closing time, set per trial\n"
  "* ramp_ms    (ms)   cosine ramp width at each edge (default 1 ms)\n"
  "* i          (nA)   nonspecific current\n"
  "* v          (mV)   local membrane potential (NEURON-managed)\n"
  "=======================================================================\n"
  "ENDCOMMENT\n"
  "\n"
  "NEURON {\n"
  "    POINT_PROCESS gaba_tonic\n"
  "    RANGE g, e, t_on, t_off, ramp_ms, i\n"
  "    NONSPECIFIC_CURRENT i\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "    (nA) = (nanoamp)\n"
  "    (mV) = (millivolt)\n"
  "    (uS) = (microsiemens)\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "    g       = 0       (uS)\n"
  "    e       = -75     (mV)\n"
  "    t_on    = 0       (ms)\n"
  "    t_off   = 0       (ms)\n"
  "    ramp_ms = 1       (ms)\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "    v       (mV)\n"
  "    i       (nA)\n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "    LOCAL d_on, d_off, env\n"
  "    if (t < t_on) {\n"
  "        env = 0\n"
  "    } else if (t > t_off) {\n"
  "        env = 0\n"
  "    } else if (ramp_ms <= 0) {\n"
  "        env = 1\n"
  "    } else {\n"
  "        d_on  = t - t_on\n"
  "        d_off = t_off - t\n"
  "        if (d_on < ramp_ms) {\n"
  "            env = 0.5 * (1 - cos(3.14159265358979 * d_on / ramp_ms))\n"
  "        } else if (d_off < ramp_ms) {\n"
  "            env = 0.5 * (1 - cos(3.14159265358979 * d_off / ramp_ms))\n"
  "        } else {\n"
  "            env = 1\n"
  "        }\n"
  "    }\n"
  "    i = env * g * (v - e)\n"
  "}\n"
  ;
#endif
