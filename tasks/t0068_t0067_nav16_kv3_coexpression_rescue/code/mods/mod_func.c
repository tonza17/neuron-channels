#include <stdio.h>
#include "hocdec.h"
#define IMPORT extern __declspec(dllimport)
IMPORT int nrnmpi_myid, nrn_nobanner_;

extern void _kv3t67_reg();
extern void _kv4t67_reg();
extern void _napt67_reg();
extern void _nart67_reg();
extern void _nav16t67_reg();

void modl_reg(){
	//nrn_mswindll_stdio(stdin, stdout, stderr);
    if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
	fprintf(stderr, "Additional mechanisms from files\n");

fprintf(stderr," kv3t67.mod");
fprintf(stderr," kv4t67.mod");
fprintf(stderr," napt67.mod");
fprintf(stderr," nart67.mod");
fprintf(stderr," nav16t67.mod");
fprintf(stderr, "\n");
    }
_kv3t67_reg();
_kv4t67_reg();
_napt67_reg();
_nart67_reg();
_nav16t67_reg();
}
