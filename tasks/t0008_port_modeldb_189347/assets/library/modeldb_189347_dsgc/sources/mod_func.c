#include <stdio.h>
#include "hocdec.h"
#define IMPORT extern __declspec(dllimport)
IMPORT int nrnmpi_myid, nrn_nobanner_;

extern void _HHst_reg();
extern void _SAC2RGCexc_reg();
extern void _SAC2RGCinhib_reg();
extern void _SquareInput_reg();
extern void _bipolarNMDA_reg();
extern void _spike_reg();

void modl_reg(){
	//nrn_mswindll_stdio(stdin, stdout, stderr);
    if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
	fprintf(stderr, "Additional mechanisms from files\n");

fprintf(stderr," HHst.mod");
fprintf(stderr," SAC2RGCexc.mod");
fprintf(stderr," SAC2RGCinhib.mod");
fprintf(stderr," SquareInput.mod");
fprintf(stderr," bipolarNMDA.mod");
fprintf(stderr," spike.mod");
fprintf(stderr, "\n");
    }
_HHst_reg();
_SAC2RGCexc_reg();
_SAC2RGCinhib_reg();
_SquareInput_reg();
_bipolarNMDA_reg();
_spike_reg();
}
