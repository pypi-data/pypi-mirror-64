/*
The underlying C code for these routines are adapted from C code originally
developed by Jeff Fessler and his students at the University of Michigan.

OpenMP support and the Cython wrappers were created by Gregory R. Lee
(Cincinnati Childrens Hospital Medical Center).

Note:  For simplicity the adjoint NUFFT is only parallelized across multiple
coils and/or repetitions.  This was done for simplicity to avoid any potential
thread conflicts.

The C templating used here is based on the implementation by Kai Wohlfahrt as
developed for the BSD-licensed PyWavelets project.
*/
#include "templating.h"


#ifndef TYPE
#error TYPE must be defined here.
#else

//#include "common.h"

#if defined _MSC_VER
#define restrict __restrict
#elif defined __GNUC__
#define restrict __restrict__
#endif

/*
* interp1_table1_complex_forward()
* 1D, 1st order, complex, periodic
*/
void CAT(TYPE, _interp1_table1_complex_forward)(
    const TYPE *r_ck, /* [K1,1] in */
    const TYPE *i_ck,
    const int K1,
    const TYPE *r_h1, /* [J1*L1+1,1] in */
    const TYPE *i_h1, /* imaginary part of complex interpolator */
    const int J1,
    const int L1,
    const TYPE *p_tm, /* [M,1] in */
    const int M,
    TYPE *r_fm,       /* [M,1] out */
    TYPE *i_fm);

/*
* interp1_table1_real_forward()
* 1D, 1st-order, real, periodic
*/
void CAT(TYPE, _interp1_table1_real_forward)(
    const TYPE *r_ck, /* [K,1] in */
    const TYPE *i_ck,
    const int K1,
    const TYPE *r_h1, /* [J1*L1+1,1] in (real) */
    const int J1,
    const int L1,
    const TYPE *p_tm, /* [M,1] in */
    const int M,
    TYPE *r_fm,       /* [M,1] out */
    TYPE *i_fm);


/*
* interp1_table1_complex_adj()
* 1D, 1st order, complex, periodic
*/
void CAT(TYPE, _interp1_table1_complex_adj)(
    TYPE *r_ck,   /* [K1,K2] in */
    TYPE *i_ck,
    const int K1,
    const TYPE *r_h1, /* [J1*L1+1,1] in */
    const TYPE *i_h1,
    const int J1,
    const int L1,
    const TYPE *p_tm, /* [M,2] in */
    const int M,
    const TYPE *r_fm,     /* [M,1] out */
    const TYPE *i_fm,
    const int N);


/*
* interp1_table1_real_adj()
* 1D, 1st order, complex, periodic
*/
void CAT(TYPE, _interp1_table1_real_adj)(
    TYPE *r_ck,   /* [K1,K2] in */
    TYPE *i_ck,
    const int K1,
    const TYPE *r_h1, /* [J1*L1+1,1] in */
    const int J1,
    const int L1,
    const TYPE *p_tm, /* [M,2] in */
    const int M,
    const TYPE *r_fm,     /* [M,1] out */
    const TYPE *i_fm,
    const int N);

/*
* interp2_table1_real_adj()
* 2D, 1st order, complex, periodic
*/
void CAT(TYPE, _interp2_table1_real_adj)(
    TYPE *r_ck,   /* [K1,K2] in */
    TYPE *i_ck,
    const int K1,
    const int K2,
    const TYPE *r_h1, /* [J1*L1+1,1] in */
    const TYPE *r_h2, /* [J2*L1+1,1] in */
    const int J1,
    const int J2,
    const int L1,
    const TYPE *p_tm, /* [M,2] in */
    const int M,
    const TYPE *r_fm,     /* [M,1] out */
    const TYPE *i_fm,
    const int N);


/*
* interp2_table1_complex_adj()
* 2D, 1st order, complex, periodic
*/
void CAT(TYPE, _interp2_table1_complex_adj)(
    TYPE *r_ck,   /* [K1,K2] in */
    TYPE *i_ck,
    const int K1,
    const int K2,
    const TYPE *r_h1, /* [J1*L1+1,1] in */
    const TYPE *i_h1,
    const TYPE *r_h2, /* [J2*L1+1,1] in */
    const TYPE *i_h2,
    const int J1,
    const int J2,
    const int L1,
    const TYPE *p_tm, /* [M,2] in */
    const int M,
    const TYPE *r_fm,     /* [M,1] out */
    const TYPE *i_fm,
    const int N);

/*
* interp2_table1_real_forward()
* 2D, 1st-order, real, periodic
*/
void CAT(TYPE, _interp2_table1_real_forward)(
    const TYPE *r_ck, /* [K1,K2] in */
    const TYPE *i_ck,
    const int K1,
    const int K2,
    const TYPE *r_h1, /* [J1*L1+1,1] in */
    const TYPE *r_h2, /* [J2*L1+1,1] in */
    const int J1,
    const int J2,
    const int L1,
    const TYPE *p_tm, /* [M,2] in */
    const int M,
    TYPE *r_fm,       /* [M,1] out */
    TYPE *i_fm);


/*
* interp2_table1_complex_forward()
* 2D, 1st order, complex, periodic
*/
void CAT(TYPE, _interp2_table1_complex_forward)(
    const TYPE *r_ck, /* [K1,K2] in */
    const TYPE *i_ck,
    const int K1,
    const int K2,
    const TYPE *r_h1, /* [J1*L1+1,1] in */
    const TYPE *i_h1,
    const TYPE *r_h2, /* [J2*L1+1,1] in */
    const TYPE *i_h2,
    const int J1,
    const int J2,
    const int L1,
    const TYPE *p_tm, /* [M,2] in */
    const int M,
    TYPE *r_fm,       /* [M,1] out */
    TYPE *i_fm);

/*
* interp3_table1_complex_forward()
* 3D, 1st order, complex, periodic
*/
void CAT(TYPE, _interp3_table1_complex_forward)(
    const TYPE *r_ck, /* [K1,K2,K3] in */
    const TYPE *i_ck,
    const int K1,
    const int K2,
    const int K3,
    const TYPE *r_h1, /* [J1*L1+1,1] in */
    const TYPE *i_h1,
    const TYPE *r_h2, /* [J2*L1+1,1] in */
    const TYPE *i_h2,
    const TYPE *r_h3, /* [J3*L1+1,1] in */
    const TYPE *i_h3,
    const int J1,
    const int J2,
    const int J3,
    const int L1,
    const TYPE *p_tm, /* [M,3] in */
    const int M,
    TYPE *r_fm,       /* [M,1] out */
    TYPE *i_fm);

/*
* interp3_table1_real_forward()
* 3D, 1st-order, real, periodic
*/
void CAT(TYPE, _interp3_table1_real_forward)(
    const TYPE *r_ck, /* [K1,K2,K3] in */
    const TYPE *i_ck,
    const int K1,
    const int K2,
    const int K3,
    const TYPE *r_h1, /* [J1*L1+1,1] in */
    const TYPE *r_h2, /* [J2*L1+1,1] in */
    const TYPE *r_h3, /* [J3*L1+1,1] in */
    const int J1,
    const int J2,
    const int J3,
    const int L1,
    const TYPE *p_tm, /* [M,3] in */
    const int M,
    TYPE *r_fm,       /* [M,1] out */
    TYPE *i_fm);

/*
* interp3_table1_complex_adj()
* 3D, 1st order, complex, periodic
*/
void CAT(TYPE, _interp3_table1_complex_adj)(
    TYPE *r_ck,   /* [K1,K2] in */
    TYPE *i_ck,
    const int K1,
    const int K2,
    const int K3,
    const TYPE *r_h1, /* [J1*L1+1,1] in */
    const TYPE *i_h1,
    const TYPE *r_h2, /* [J2*L1+1,1] in */
    const TYPE *i_h2,
    const TYPE *r_h3, /* [J3*L1+1,1] in */
    const TYPE *i_h3,
    const int J1,
    const int J2,
    const int J3,
    const int L1,
    const TYPE *p_tm, /* [M,2] in */
    const int M,
    const TYPE *r_fm,     /* [M,1] out */
    const TYPE *i_fm,
    const int N);

/*
* interp3_table1_real_adj()
* 3D, 1st order, real, periodic
*/
void CAT(TYPE, _interp3_table1_real_adj)(
    TYPE *r_ck,   /* [K1,K2] in */
    TYPE *i_ck,
    const int K1,
    const int K2,
    const int K3,
    const TYPE *r_h1, /* [J1*L1+1,1] in */
    const TYPE *r_h2, /* [J2*L1+1,1] in */
    const TYPE *r_h3, /* [J3*L1+1,1] in */
    const int J1,
    const int J2,
    const int J3,
    const int L1,
    const TYPE *p_tm, /* [M,2] in */
    const int M,
    const TYPE *r_fm,     /* [M,1] out */
    const TYPE *i_fm,
    const int N);

#undef restrict
#endif /* TYPE */
