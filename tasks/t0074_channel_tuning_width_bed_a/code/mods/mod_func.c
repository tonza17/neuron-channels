#include <stdio.h>
#include "hocdec.h"
#define IMPORT extern __declspec(dllimport)
IMPORT int nrnmpi_myid, nrn_nobanner_;

extern void _bk74_reg();
extern void _cadecay_reg();
extern void _kv3t74_reg();
extern void _kv4t74_reg();
extern void _kv7t74_reg();
extern void _napt74_reg();
extern void _nart74_reg();
extern void _nav16t74_reg();
extern void _sk74_reg();

void modl_reg(){
	//nrn_mswindll_stdio(stdin, stdout, stderr);
    if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
	fprintf(stderr, "Additional mechanisms from files\n");

fprintf(stderr," bk74.mod");
fprintf(stderr," cadecay.mod");
fprintf(stderr," kv3t74.mod");
fprintf(stderr," kv4t74.mod");
fprintf(stderr," kv7t74.mod");
fprintf(stderr," napt74.mod");
fprintf(stderr," nart74.mod");
fprintf(stderr," nav16t74.mod");
fprintf(stderr," sk74.mod");
fprintf(stderr, "\n");
    }
_bk74_reg();
_cadecay_reg();
_kv3t74_reg();
_kv4t74_reg();
_kv7t74_reg();
_napt74_reg();
_nart74_reg();
_nav16t74_reg();
_sk74_reg();
}
