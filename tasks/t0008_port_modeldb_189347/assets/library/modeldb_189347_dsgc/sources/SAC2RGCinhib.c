/* Created by Language version: 7.7.0 */
/* NOT VECTORIZED */
#define NRN_VECTORIZED 0
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

#define nrn_init _nrn_init__SACinhib
#define _nrn_initial _nrn_initial__SACinhib
#define nrn_cur _nrn_cur__SACinhib
#define _nrn_current _nrn_current__SACinhib
#define nrn_jacob _nrn_jacob__SACinhib
#define nrn_state _nrn_state__SACinhib
#define _net_receive _net_receive__SACinhib
#define state state__SACinhib

#define _threadargscomma_ /**/
#define _threadargsprotocomma_ /**/
#define _threadargs_ /**/
#define _threadargsproto_ /**/
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg(int);
 static double *_p; static Datum *_ppvar;

#define t nrn_threads->_t
#define dt nrn_threads->_dt
#define locx _p[0]
#define locx_columnindex 0
#define locy _p[1]
#define locy_columnindex 1
#define Vinf _p[2]
#define Vinf_columnindex 2
#define s_inf _p[3]
#define s_inf_columnindex 3
#define t1 _p[4]
#define t1_columnindex 4
#define numves _p[5]
#define numves_columnindex 5
#define release _p[6]
#define release_columnindex 6
#define i _p[7]
#define i_columnindex 7
#define local_v _p[8]
#define local_v_columnindex 8
#define g _p[9]
#define g_columnindex 9
#define Vpre _p[10]
#define Vpre_columnindex 10
#define Dg _p[11]
#define Dg_columnindex 11
#define DVpre _p[12]
#define DVpre_columnindex 12
#define _g _p[13]
#define _g_columnindex 13
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
 /* external NEURON variables */
 /* declaration of user functions */
 static double _hoc_releasefunc(void*);
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
 _p = _prop->param; _ppvar = _prop->dparam;
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
 "releasefunc", _hoc_releasefunc,
 0, 0
};
#define releasefunc releasefunc_SACinhib
 extern double releasefunc( double );
 /* declare global and static user variables */
#define Vtau Vtau_SACinhib
 double Vtau = 30;
#define e e_SACinhib
 double e = -65;
#define gsingle gsingle_SACinhib
 double gsingle = 0.2;
#define maxves maxves_SACinhib
 double maxves = 10;
#define newves newves_SACinhib
 double newves = 0.01;
#define tau tau_SACinhib
 double tau = 10;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "Vtau_SACinhib", "/ms",
 "gsingle_SACinhib", "nS",
 "tau_SACinhib", "ms",
 "e_SACinhib", "mV",
 "g", "nS",
 "Vpre", "mV",
 "Vinf", "mV",
 "i", "nA",
 "local_v", "mV",
 0,0
};
 static double Vpre0 = 0;
 static double delta_t = 0.01;
 static double g0 = 0;
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "maxves_SACinhib", &maxves_SACinhib,
 "newves_SACinhib", &newves_SACinhib,
 "Vtau_SACinhib", &Vtau_SACinhib,
 "gsingle_SACinhib", &gsingle_SACinhib,
 "tau_SACinhib", &tau_SACinhib,
 "e_SACinhib", &e_SACinhib,
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

static int _ode_count(int);
static void _ode_map(int, double**, double**, double*, Datum*, double*, int);
static void _ode_spec(NrnThread*, _Memb_list*, int);
static void _ode_matsol(NrnThread*, _Memb_list*, int);

#define _cvode_ieq _ppvar[2]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"SACinhib",
 "locx",
 "locy",
 0,
 "Vinf",
 "s_inf",
 "t1",
 "numves",
 "release",
 "i",
 "local_v",
 0,
 "g",
 "Vpre",
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
 	_p = nrn_prop_data_alloc(_mechtype, 14, _prop);
 	/*initialize range parameters*/
 	locx = 0;
 	locy = 0;
  }
 	_prop->param = _p;
 	_prop->param_size = 14;
  if (!nrn_point_prop_) {
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 3, _prop);
  }
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/

}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 0,0
};
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _SAC2RGCinhib_reg() {
	int _vectorized = 0;
  _initlists();
 	_pointtype = point_register_mech(_mechanism,
	 nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init,
	 hoc_nrnpointerindex, 0,
	 _hoc_create_pnt, _hoc_destroy_pnt, _member_func);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 14, 3);
  hoc_register_dparam_semantics(_mechtype, 0, "area");
  hoc_register_dparam_semantics(_mechtype, 1, "pntproc");
  hoc_register_dparam_semantics(_mechtype, 2, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 SACinhib SAC2RGCinhib.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static char *modelname = "";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}

static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static double *_temp1;
 static int _slist1[2], _dlist1[2];
 static int state(_threadargsproto_);
 extern int state_discon_flag_;

double releasefunc (  double _lvpre ) {
   double _lreleasefunc;
 double _lrand , _laddves ;
 s_inf = _lvpre / 100.0 ;
   release = 0.0 ;
   {int  _lrand ;for ( _lrand = 0 ; _lrand <= ((int) numves ) - 1 ; _lrand ++ ) {
     if ( scop_random ( ) < s_inf ) {
       release = release + 1.0 ;
       }
     } }
   if ( release > 0.0 ) {
     numves = numves - release ;
     if ( numves < 0.0 ) {
       numves = 0.0 ;
       }
     state_discontinuity ( _cvode_ieq + 0, & g , g + release * gsingle ) ;
     }
   _laddves = 0.0 ;
   {int  _lrand ;for ( _lrand = 0 ; _lrand <= ((int) maxves ) - ((int) numves ) - 1 ; _lrand ++ ) {
     if ( scop_random ( ) < newves ) {
       _laddves = _laddves + 1.0 ;
       }
     } }
   numves = numves + _laddves ;

return _lreleasefunc;
 }

static double _hoc_releasefunc(void* _vptr) {
 double _r;
    _hoc_setdata(_vptr);
 _r =  releasefunc (  *getarg(1) );
 return(_r);
}

/*CVODE*/
 static int _ode_spec1 () {_reset=0;
 {
   Dg = - g / tau ;
   DVpre = ( - Vpre + Vinf ) / Vtau ;
   }
 return _reset;
}
 static int _ode_matsol1 () {
 Dg = Dg  / (1. - dt*( ( - 1.0 ) / tau )) ;
 DVpre = DVpre  / (1. - dt*( ( ( - 1.0 ) ) / Vtau )) ;
  return 0;
}
 /*END CVODE*/

static int state () {_reset=0;
 {
   Dg = - g / tau ;
   DVpre = ( - Vpre + Vinf ) / Vtau ;
   }
 return _reset;}

static int _ode_count(int _type){ return 2;}

static void _ode_spec(NrnThread* _nt, _Memb_list* _ml, int _type) {
   Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
     _ode_spec1 ();
 }}

static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) {
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 2; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 }

static void _ode_matsol_instance1(_threadargsproto_) {
 _ode_matsol1 ();
 }

static void _ode_matsol(NrnThread* _nt, _Memb_list* _ml, int _type) {
   Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
 _ode_matsol_instance1(_threadargs_);
 }}

static void initmodel() {
  int _i; double _save;_ninits++;
 _save = t;
 t = 0.0;
{
  Vpre = Vpre0;
  g = g0;
 {
   s_inf = 0.0 ;
   release = 0.0 ;
   numves = maxves ;
   t1 = 0.0 ;
   Vinf = 0.0 ;
   Vpre = Vinf ;
   g = 0.0 ;
   }
  _sav_indep = t; t = _save;

}
}

static void nrn_init(NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
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
 initmodel();
}}

static double _nrn_current(double _v){double _current=0.;v=_v;{ {
   if ( t > t1 ) {
     releasefunc ( _threadargscomma_ Vpre ) ;
     t1 = t1 + 1.0 ;
     }
   i = ( 1e-3 ) * g * ( v - e ) ;
   local_v = v ;
   }
 _current += i;

} return _current;
}

static void nrn_cur(NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
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
 _g = _nrn_current(_v + .001);
 	{ state_discon_flag_ = 1; _rhs = _nrn_current(_v); state_discon_flag_ = 0;
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

}}

static void nrn_jacob(NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
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

}}

static void nrn_state(NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; double _v = 0.0; int* _ni; int _iml, _cntml;
double _dtsav = dt;
if (secondorder) { dt *= 0.5; }
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _nd = _ml->_nodelist[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v=_v;
{
 { error =  euler(_ninits, 2, _slist1, _dlist1, _p, &t, dt, state, &_temp1);
 if(error){fprintf(stderr,"at line 50 in file SAC2RGCinhib.mod:\n	SOLVE state METHOD euler\n"); nrn_complain(_p); abort_run(error);}
    if (secondorder) {
    int _i;
    for (_i = 0; _i < 2; ++_i) {
      _p[_slist1[_i]] += dt*_p[_dlist1[_i]];
    }}
 }}}
 dt = _dtsav;
}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = g_columnindex;  _dlist1[0] = Dg_columnindex;
 _slist1[1] = Vpre_columnindex;  _dlist1[1] = DVpre_columnindex;
_first = 0;
}

#if NMODL_TEXT
static const char* nmodl_filename = "SAC2RGCinhib.mod";
static const char* nmodl_file_text =
  "\n"
  ":GABA release dependent on presynaptic voltage\n"
  "NEURON {\n"
  "POINT_PROCESS SACinhib\n"
  "	RANGE Vpre ,Vinf\n"
  "	GLOBAL tau ,Vtau ,e,maxves,gsingle ,newves\n"
  "	RANGE release,numves,g,s_inf,t1,i,g\n"
  "	RANGE locx,locy,local_v\n"
  "	NONSPECIFIC_CURRENT i\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "	(nA) 	= (nanoamp)\n"
  "	(mV)	= (millivolt)\n"
  "	(nS) 	= (nanomho)\n"
  "}\n"
  "PARAMETER {\n"
  "							:presynaptic\n"
  "	maxves=10				:TOTAL NUMBER OF VESICLES\n"
  "	newves=0.01				:REPLENISHMENT RATE - VESICLES\n"
  "	Vtau=30	(/ms)		:STIMULUS DEPOLARIZATION RATE	\n"
  "							:postsynaptic\n"
  "	gsingle=0.2	(nS)\n"
  "	tau=10		(ms)\n"
  "	e = -65 	(mV)\n"
  "	locx=0		:location x\n"
  "	locy=0		:location y\n"
  "\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "	:presynaptic\n"
  "	Vinf 		(mV)\n"
  "	s_inf\n"
  "	t1\n"
  "	numves\n"
  "	release\n"
  "	:postsynaptic\n"
  "	v 			(mV)\n"
  "	i 			(nA)\n"
  "	local_v		(mV)\n"
  "}\n"
  "\n"
  "STATE {\n"
  "	g	 		(nS)\n"
  "	Vpre 		(mV)\n"
  "}\n"
  " \n"
  "BREAKPOINT {\n"
  "	SOLVE state METHOD euler\n"
  "	if (t>t1){										:EVERY 1 MS\n"
  "		releasefunc(Vpre)\n"
  "		t1=t1+1\n"
  "	}\n"
  "	i = (1e-3)*g * (v - e)\n"
  "	local_v=v\n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "	:presynaptic\n"
  "	s_inf=0\n"
  "	release=0\n"
  "	numves=maxves\n"
  "	t1=0\n"
  "	Vinf=0\n"
  "	Vpre=Vinf\n"
  "	:postsynaptic\n"
  "	g =0\n"
  "}\n"
  " \n"
  "FUNCTION releasefunc(vpre){\n"
  "	LOCAL rand,addves\n"
  "	s_inf=vpre/100\n"
  "	release=0	\n"
  "	FROM rand=0 TO numves-1 {			:GOES OVER ALL RRP\n"
  "		if (scop_random()<s_inf){\n"
  "			release=release+1\n"
  "		}\n"
  "	}\n"
  "	if (release>0){						:RELEASE\n"
  "		numves=numves-release\n"
  "		if (numves<0){numves=0}\n"
  "		state_discontinuity( g, g+ release*gsingle)\n"
  "	}\n"
  "	addves=0							:REPLINISHMENT\n"
  "	FROM rand=0 TO maxves-numves-1 {\n"
  "		if (scop_random()<newves){addves=addves+1}\n"
  "	}\n"
  "	numves=numves+addves\n"
  "}\n"
  "DERIVATIVE state {\n"
  "	g'=-g/tau\n"
  "	Vpre'=(-Vpre+Vinf)/Vtau\n"
  "}\n"
  ;
#endif
