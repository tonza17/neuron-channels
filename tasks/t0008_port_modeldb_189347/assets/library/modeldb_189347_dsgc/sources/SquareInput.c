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

#define nrn_init _nrn_init__square
#define _nrn_initial _nrn_initial__square
#define nrn_cur _nrn_cur__square
#define _nrn_current _nrn_current__square
#define nrn_jacob _nrn_jacob__square
#define nrn_state _nrn_state__square
#define _net_receive _net_receive__square

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
#define del _p[0]
#define del_columnindex 0
#define dur _p[1]
#define dur_columnindex 1
#define gmax _p[2]
#define gmax_columnindex 2
#define e _p[3]
#define e_columnindex 3
#define locx _p[4]
#define locx_columnindex 4
#define locy _p[5]
#define locy_columnindex 5
#define Vdependent _p[6]
#define Vdependent_columnindex 6
#define i _p[7]
#define i_columnindex 7
#define g _p[8]
#define g_columnindex 8
#define m _p[9]
#define m_columnindex 9
#define Dm _p[10]
#define Dm_columnindex 10
#define _g _p[11]
#define _g_columnindex 11
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
 0, 0
};
 /* declare global and static user variables */
#define gama gama_square
 double gama = 0.08;
#define n n_square
 double n = 0.25;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "n_square", "/mM",
 "gama_square", "/mV",
 "del", "ms",
 "dur", "ms",
 "gmax", "nA",
 "e", "millivolts",
 "i", "nA",
 "g", "nS",
 0,0
};
 static double m0 = 0;
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "n_square", &n_square,
 "gama_square", &gama_square,
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
"square",
 "del",
 "dur",
 "gmax",
 "e",
 "locx",
 "locy",
 "Vdependent",
 0,
 "i",
 "g",
 0,
 "m",
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
 	_p = nrn_prop_data_alloc(_mechtype, 12, _prop);
 	/*initialize range parameters*/
 	del = 50;
 	dur = 50;
 	gmax = 1;
 	e = 0;
 	locx = 0;
 	locy = 0;
 	Vdependent = 1;
  }
 	_prop->param = _p;
 	_prop->param_size = 12;
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

 void _SquareInput_reg() {
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
  hoc_register_prop_size(_mechtype, 12, 2);
  hoc_register_dparam_semantics(_mechtype, 0, "area");
  hoc_register_dparam_semantics(_mechtype, 1, "pntproc");
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 square SquareInput.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static char *modelname = "";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
 extern int state_discon_flag_;

static void initmodel() {
  int _i; double _save;_ninits++;
{
  m = m0;
 {
   m = 0.0 ;
   }

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
   if ( at_time ( nrn_threads, del ) ) {
     state_discontinuity ( -1, & m , gmax ) ;
     }
   if ( at_time ( nrn_threads, del + dur ) ) {
     state_discontinuity ( -1, & m , 0.0 ) ;
     }
   if ( Vdependent  == 0.0 ) {
     g = m ;
     }
   else {
     g = m / ( 1.0 + n * exp ( - gama * v ) ) ;
     }
   i = ( 1e-3 ) * g * ( v - e ) ;
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

}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
_first = 0;
}

#if NMODL_TEXT
static const char* nmodl_filename = "SquareInput.mod";
static const char* nmodl_file_text =
  "\n"
  "NEURON {\n"
  "POINT_PROCESS square\n"
  "	RANGE del,dur,locx,locy,i,Vdependent\n"
  "	RANGE g,gmax,m,e\n"
  "	GLOBAL gama,n  \n"
  "	NONSPECIFIC_CURRENT i\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "	(nA) 	= (nanoamp)\n"
  "	(mV)	= (millivolt)\n"
  "	(nS) 	= (nanomho)\n"
  "}\n"
  "PARAMETER {\n"
  "	del=50		(ms)\n"
  "	dur=50		(ms)\n"
  "	gmax=1		(nA)\n"
  "	n=0.25 		(/mM)\n"
  "	gama=0.08 	(/mV)\n"
  "	e = 0 		(millivolts)\n"
  "	locx=0		:location x\n"
  "	locy=0		:location y\n"
  "	Vdependent=1		:1 - voltage dependent 0- voltage independent\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "	v 			(mV)\n"
  "	i 			(nA)\n"
  "	g           (nS)\n"
  "	:m			(nS)\n"
  "}\n"
  "\n"
  "STATE {\n"
  "	m\n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "	IF(at_time(del)){\n"
  "		state_discontinuity( m, gmax)\n"
  "	}\n"
  "	IF(at_time(del+dur)){\n"
  "		state_discontinuity( m, 0)\n"
  "	}\n"
  "	IF (Vdependent==0){\n"
  "		g=m\n"
  "	}ELSE{\n"
  "		g=m/(1+n*exp(-gama*v) )\n"
  "	}\n"
  "	i = (1e-3)*g * (v - e)\n"
  "	\n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "	m=0\n"
  "}\n"
  ;
#endif
