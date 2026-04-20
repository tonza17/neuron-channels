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

#define nrn_init _nrn_init__bipNMDA
#define _nrn_initial _nrn_initial__bipNMDA
#define nrn_cur _nrn_cur__bipNMDA
#define _nrn_current _nrn_current__bipNMDA
#define nrn_jacob _nrn_jacob__bipNMDA
#define nrn_state _nrn_state__bipNMDA
#define _net_receive _net_receive__bipNMDA
#define state state__bipNMDA

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
#define Vdel _p[0]
#define Vdel_columnindex 0
#define Vdur _p[1]
#define Vdur_columnindex 1
#define Vamp _p[2]
#define Vamp_columnindex 2
#define Vbase _p[3]
#define Vbase_columnindex 3
#define locx _p[4]
#define locx_columnindex 4
#define locy _p[5]
#define locy_columnindex 5
#define Vinf _p[6]
#define Vinf_columnindex 6
#define s_inf _p[7]
#define s_inf_columnindex 7
#define t1 _p[8]
#define t1_columnindex 8
#define numves _p[9]
#define numves_columnindex 9
#define release _p[10]
#define release_columnindex 10
#define i _p[11]
#define i_columnindex 11
#define g _p[12]
#define g_columnindex 12
#define iNMDA _p[13]
#define iNMDA_columnindex 13
#define iAMPA _p[14]
#define iAMPA_columnindex 14
#define gNMDA _p[15]
#define gNMDA_columnindex 15
#define local_v _p[16]
#define local_v_columnindex 16
#define A _p[17]
#define A_columnindex 17
#define B _p[18]
#define B_columnindex 18
#define gAMPA _p[19]
#define gAMPA_columnindex 19
#define Vpre _p[20]
#define Vpre_columnindex 20
#define DA _p[21]
#define DA_columnindex 21
#define DB _p[22]
#define DB_columnindex 22
#define DgAMPA _p[23]
#define DgAMPA_columnindex 23
#define DVpre _p[24]
#define DVpre_columnindex 24
#define _g _p[25]
#define _g_columnindex 25
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
#define releasefunc releasefunc_bipNMDA
 extern double releasefunc( double );
 /* declare global and static user variables */
#define VampK VampK_bipNMDA
 double VampK = 2;
#define Vset Vset_bipNMDA
 double Vset = -60;
#define Voff Voff_bipNMDA
 double Voff = 0;
#define Vtau Vtau_bipNMDA
 double Vtau = 30;
#define e e_bipNMDA
 double e = 0;
#define gama gama_bipNMDA
 double gama = 0.08;
#define gNMDAsingle gNMDAsingle_bipNMDA
 double gNMDAsingle = 0.2;
#define gAMPAsingle gAMPAsingle_bipNMDA
 double gAMPAsingle = 0.2;
#define icaconst icaconst_bipNMDA
 double icaconst = 0.1;
#define maxves maxves_bipNMDA
 double maxves = 10;
#define n n_bipNMDA
 double n = 0.25;
#define newves newves_bipNMDA
 double newves = 0.01;
#define tau2NMDA tau2NMDA_bipNMDA
 double tau2NMDA = 2;
#define tau1NMDA tau1NMDA_bipNMDA
 double tau1NMDA = 50;
#define tauAMPA tauAMPA_bipNMDA
 double tauAMPA = 2;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "Vtau_bipNMDA", "/ms",
 "gAMPAsingle_bipNMDA", "nS",
 "gNMDAsingle_bipNMDA", "nS",
 "tau1NMDA_bipNMDA", "ms",
 "tau2NMDA_bipNMDA", "ms",
 "tauAMPA_bipNMDA", "ms",
 "n_bipNMDA", "/mM",
 "gama_bipNMDA", "/mV",
 "e_bipNMDA", "mV",
 "Vdel", "ms",
 "Vdur", "ms",
 "Vamp", "mV",
 "Vbase", "mV",
 "gAMPA", "nS",
 "Vpre", "mV",
 "Vinf", "mV",
 "i", "nA",
 "g", "nS",
 "iNMDA", "nA",
 "iAMPA", "nA",
 "gNMDA", "nS",
 "local_v", "mV",
 0,0
};
 static double A0 = 0;
 static double B0 = 0;
 static double Vpre0 = 0;
 static double delta_t = 0.01;
 static double gAMPA0 = 0;
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "maxves_bipNMDA", &maxves_bipNMDA,
 "newves_bipNMDA", &newves_bipNMDA,
 "VampK_bipNMDA", &VampK_bipNMDA,
 "Vtau_bipNMDA", &Vtau_bipNMDA,
 "gAMPAsingle_bipNMDA", &gAMPAsingle_bipNMDA,
 "gNMDAsingle_bipNMDA", &gNMDAsingle_bipNMDA,
 "tau1NMDA_bipNMDA", &tau1NMDA_bipNMDA,
 "tau2NMDA_bipNMDA", &tau2NMDA_bipNMDA,
 "tauAMPA_bipNMDA", &tauAMPA_bipNMDA,
 "n_bipNMDA", &n_bipNMDA,
 "gama_bipNMDA", &gama_bipNMDA,
 "e_bipNMDA", &e_bipNMDA,
 "icaconst_bipNMDA", &icaconst_bipNMDA,
 "Voff_bipNMDA", &Voff_bipNMDA,
 "Vset_bipNMDA", &Vset_bipNMDA,
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
"bipNMDA",
 "Vdel",
 "Vdur",
 "Vamp",
 "Vbase",
 "locx",
 "locy",
 0,
 "Vinf",
 "s_inf",
 "t1",
 "numves",
 "release",
 "i",
 "g",
 "iNMDA",
 "iAMPA",
 "gNMDA",
 "local_v",
 0,
 "A",
 "B",
 "gAMPA",
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
 	_p = nrn_prop_data_alloc(_mechtype, 26, _prop);
 	/*initialize range parameters*/
 	Vdel = 50;
 	Vdur = 100;
 	Vamp = 10;
 	Vbase = 0;
 	locx = 0;
 	locy = 0;
  }
 	_prop->param = _p;
 	_prop->param_size = 26;
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

 void _bipolarNMDA_reg() {
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
  hoc_register_prop_size(_mechtype, 26, 3);
  hoc_register_dparam_semantics(_mechtype, 0, "area");
  hoc_register_dparam_semantics(_mechtype, 1, "pntproc");
  hoc_register_dparam_semantics(_mechtype, 2, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 bipNMDA bipolarNMDA.mod\n");
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
 static int _slist1[4], _dlist1[4];
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
     state_discontinuity ( _cvode_ieq + 2, & gAMPA , gAMPA + release * gAMPAsingle ) ;
     state_discontinuity ( _cvode_ieq + 0, & A , A + release * gNMDAsingle ) ;
     state_discontinuity ( _cvode_ieq + 1, & B , B + release * gNMDAsingle ) ;
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
   DA = - A / tau1NMDA ;
   DB = - B / tau2NMDA ;
   DgAMPA = - gAMPA / tauAMPA ;
   DVpre = ( - Vpre + Vinf ) / Vtau ;
   }
 return _reset;
}
 static int _ode_matsol1 () {
 DA = DA  / (1. - dt*( ( - 1.0 ) / tau1NMDA )) ;
 DB = DB  / (1. - dt*( ( - 1.0 ) / tau2NMDA )) ;
 DgAMPA = DgAMPA  / (1. - dt*( ( - 1.0 ) / tauAMPA )) ;
 DVpre = DVpre  / (1. - dt*( ( ( - 1.0 ) ) / Vtau )) ;
  return 0;
}
 /*END CVODE*/

static int state () {_reset=0;
 {
   DA = - A / tau1NMDA ;
   DB = - B / tau2NMDA ;
   DgAMPA = - gAMPA / tauAMPA ;
   DVpre = ( - Vpre + Vinf ) / Vtau ;
   }
 return _reset;}

static int _ode_count(int _type){ return 4;}

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
	for (_i=0; _i < 4; ++_i) {
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
  A = A0;
  B = B0;
  Vpre = Vpre0;
  gAMPA = gAMPA0;
 {
   s_inf = 0.0 ;
   release = 0.0 ;
   numves = maxves ;
   t1 = 0.0 ;
   Vinf = 0.0 ;
   Vpre = Vinf ;
   gAMPA = 0.0 ;
   gNMDA = 0.0 ;
   A = 0.0 ;
   B = 0.0 ;
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
   local_v = v * ( 1.0 - Voff ) + Vset * Voff ;
   gNMDA = ( A - B ) / ( 1.0 + n * exp ( - gama * local_v ) ) ;
   iAMPA = ( 1e-3 ) * gAMPA * ( v - e ) ;
   iNMDA = ( 1e-3 ) * gNMDA * ( v - e ) ;
   i = iAMPA + iNMDA ;
   g = gNMDA + gAMPA ;
   }
 _current += iAMPA;
 _current += iNMDA;

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
 { error =  euler(_ninits, 4, _slist1, _dlist1, _p, &t, dt, state, &_temp1);
 if(error){fprintf(stderr,"at line 80 in file bipolarNMDA.mod:\n	SOLVE state METHOD euler\n"); nrn_complain(_p); abort_run(error);}
    if (secondorder) {
    int _i;
    for (_i = 0; _i < 4; ++_i) {
      _p[_slist1[_i]] += dt*_p[_dlist1[_i]];
    }}
 }}}
 dt = _dtsav;
}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = A_columnindex;  _dlist1[0] = DA_columnindex;
 _slist1[1] = B_columnindex;  _dlist1[1] = DB_columnindex;
 _slist1[2] = gAMPA_columnindex;  _dlist1[2] = DgAMPA_columnindex;
 _slist1[3] = Vpre_columnindex;  _dlist1[3] = DVpre_columnindex;
_first = 0;
}

#if NMODL_TEXT
static const char* nmodl_filename = "bipolarNMDA.mod";
static const char* nmodl_file_text =
  "\n"
  ":5403813100\n"
  "\n"
  ":glutamate (AMPA+NMDA) release dependent on presynaptic voltage modeled here\n"
  "NEURON {\n"
  "POINT_PROCESS bipNMDA\n"
  "	RANGE Vpre,Vdel,Vdur,Vamp,Vbase,locx,locy,local_v,i,g,release,numves :Vpre1,Vpre2,\n"
  "	RANGE gAMPA,gNMDA,s_inf,t1,A,B,Vinf	:1,Vinf2\n"
  "	GLOBAL maxves,newves,gAMPAsingle,gNMDAsingle,Vtau,Voff,Vset,VampK	:,Vnoiserate,Vnoiseamp,Vnoise,Vtau2\n"
  "	GLOBAL icaconst ,gama,n,e,tauAMPA,tau1NMDA ,tau2NMDA\n"
  "	NONSPECIFIC_CURRENT iAMPA,iNMDA\n"
  "	:USEION ca WRITE ica\n"
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
  "	:Vnoise=0				:VOLTAGE VARIABILITY-INPUT NOISE\n"
  "	Vdel=50 	(ms)		:START OF ACTIVATION\n"
  "	Vdur=100	(ms)		:DURATION OF ACTIVATION\n"
  "	Vamp=10		(mV)		:PEAK AMPLITUDE -STIMULUS\n"
  "	Vbase=0		(mV)		:BACKGROUND ACTIVATION\n"
  "	VampK=2					:SIZE OF THE INITIAL RESPONSE\n"
  "	:Vnoiseamp=.1			:INTRINSIC NOISE\n"
  "	:Vnoiserate=50			:INTRINSIC NOISE\n"
  "	Vtau=30	(/ms)		:STIMULUS DEPOLARIZATION RATE\n"
  "	:Vtau2=100	(/ms)		:STIMULUS HYPERPOLARIZATION RATE\n"
  "							:postsynaptic\n"
  "	gAMPAsingle=0.2	(nS)	:AMPA CONDUCTANCE\n"
  "	gNMDAsingle=0.2	(nS)	:NMDA CONDUCTANCE\n"
  "	tau1NMDA=50	(ms)		:DEACTIVATION\n"
  "	tau2NMDA=2	(ms)		:ACTIVATION\n"
  "	tauAMPA=2	(ms)		:DEACTIVATION\n"
  "	n=0.25 		(/mM)		:NMDA VOLTAGE DEPENDENCE \n"
  "	gama=0.08 	(/mV)		:NMDA VOLTAGE DEPENDENCE \n"
  "	e = 0 		(mV)		:REVERSAL POTENTIAL\n"
  "	locx=0					:location x\n"
  "	locy=0					:location y\n"
  "	icaconst =0.1			:CALCIUM FRACTION\n"
  "	Voff=0					:0 - voltage dependent 1- voltage independent\n"
  "	Vset=-60				:set voltage when voltage independent\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "	:presynaptic\n"
  "	Vinf 		(mV)\n"
  "	:Vinf2 		(mV)	\n"
  "	s_inf\n"
  "	t1	\n"
  "	numves\n"
  "	release\n"
  "\n"
  "	:postsynaptic\n"
  "	v 			(mV)\n"
  "	i 			(nA)\n"
  "	g           (nS)\n"
  "	iNMDA		(nA)\n"
  "	iAMPA		(nA)\n"
  "	gNMDA		(nS)\n"
  "	local_v		(mV)\n"
  "	:ica			(nA)\n"
  "}\n"
  "\n"
  "STATE {\n"
  "	A\n"
  "	B\n"
  "	gAMPA 		(nS)\n"
  "	:Vpre1 		(mV)\n"
  "	:Vpre2 		(mV)\n"
  "	Vpre		(mV)\n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "	SOLVE state METHOD euler\n"
  "	if (t>t1){										:EVERY 1 MS\n"
  "		:Vpre=Vpre1-Vpre2+Vbase						:+normrand(0,Vnoise)	:PRESYNAPTIC VOLTAGE\n"
  "		:if (Vpre<0){\n"
  "		:	Vpre=0\n"
  "		:}\n"
  ":		if (scop_random()<1/Vnoiserate){			:ADDED INTRINSIC NOISE\n"
  ":			Vinf1=Vinf1*(1+Vnoiseamp*(scop_random()-.5))\n"
  ":		}\n"
  "		releasefunc(Vpre)\n"
  "		t1=t1+1\n"
  "	}\n"
  "	:IF(at_time(Vdel)){								:START STIMULUS \n"
  "	:	Vinf1=Vamp*VampK									:*(1+Vnoiseamp*(scop_random()-.5))\n"
  "	:	Vinf2=Vamp*(VampK-1)\n"
  "	:}\n"
  "	:IF(at_time(Vdel+Vdur)){							:END STIMULUS\n"
  "	:	Vinf1=Vbase									:*(1+Vnoiseamp*(scop_random()-.5))\n"
  "	:	Vinf2=Vbase\n"
  "	:}\n"
  "\n"
  "	local_v=v*(1-Voff)+Vset*Voff					:VOLTAGE DEPENDENCE\n"
  "	gNMDA=(A-B)/(1+n*exp(-gama*local_v) )\n"
  "	iAMPA = (1e-3)*gAMPA * (v - e)\n"
  "	iNMDA = (1e-3)*gNMDA * (v - e)\n"
  "	i= iAMPA+iNMDA									:INDICATOR OF TOTAL CURRENT\n"
  "	g=gNMDA+gAMPA									:INDICATOR OF TOTAL CONDUCTANCE\n"
  "\n"
  "	:ica=iNMDA*icaconst	\n"
  "	:iNMDA=iNMDA-ica\n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "	:presynaptic\n"
  "	s_inf=0\n"
  "	release=0\n"
  "	numves=maxves\n"
  "	t1=0\n"
  "	Vinf=0	:Vbase\n"
  "	Vpre=Vinf\n"
  "	:Vinf2=Vbase\n"
  "	:Vpre1=Vbase\n"
  "	:Vpre2=Vbase\n"
  "\n"
  "	:postsynaptic\n"
  "	gAMPA=0\n"
  "	gNMDA=0\n"
  "	A=0\n"
  "	B=0\n"
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
  "		state_discontinuity( gAMPA, gAMPA+ release*gAMPAsingle)\n"
  "		state_discontinuity( A, A+ release*gNMDAsingle)\n"
  "		state_discontinuity( B, B+ release*gNMDAsingle)\n"
  "	}\n"
  "	addves=0							:REPLINISHMENT\n"
  "	FROM rand=0 TO maxves-numves-1 {\n"
  "		if (scop_random()<newves){addves=addves+1}\n"
  "	}\n"
  "	numves=numves+addves\n"
  "}\n"
  "DERIVATIVE state {\n"
  "	A'=-A/tau1NMDA\n"
  "	B'=-B/tau2NMDA\n"
  "	gAMPA'=-gAMPA/tauAMPA\n"
  "	Vpre'=(-Vpre+Vinf)/Vtau\n"
  "	:Vpre2'=(-Vpre2+Vinf2)/Vtau2\n"
  "\n"
  "}\n"
  ;
#endif
