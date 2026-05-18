#include <stdio.h>
#include "hocdec.h"
#define IMPORT extern __declspec(dllimport)
IMPORT int nrnmpi_myid, nrn_nobanner_;

extern void _bkt80_reg();
extern void _calt80_reg();
extern void _catt80_reg();
extern void _iht80_reg();
extern void _kdrt80_reg();
extern void _kv3t80_reg();
extern void _kv4t80_reg();
extern void _kv7t80_reg();
extern void _napt80_reg();
extern void _nart80_reg();
extern void _nav16t80_reg();
extern void _skahpt80_reg();
extern void _skt80_reg();

void modl_reg(){
	//nrn_mswindll_stdio(stdin, stdout, stderr);
    if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
	fprintf(stderr, "Additional mechanisms from files\n");

fprintf(stderr," bkt80.mod");
fprintf(stderr," calt80.mod");
fprintf(stderr," catt80.mod");
fprintf(stderr," iht80.mod");
fprintf(stderr," kdrt80.mod");
fprintf(stderr," kv3t80.mod");
fprintf(stderr," kv4t80.mod");
fprintf(stderr," kv7t80.mod");
fprintf(stderr," napt80.mod");
fprintf(stderr," nart80.mod");
fprintf(stderr," nav16t80.mod");
fprintf(stderr," skahpt80.mod");
fprintf(stderr," skt80.mod");
fprintf(stderr, "\n");
    }
_bkt80_reg();
_calt80_reg();
_catt80_reg();
_iht80_reg();
_kdrt80_reg();
_kv3t80_reg();
_kv4t80_reg();
_kv7t80_reg();
_napt80_reg();
_nart80_reg();
_nav16t80_reg();
_skahpt80_reg();
_skt80_reg();
}
