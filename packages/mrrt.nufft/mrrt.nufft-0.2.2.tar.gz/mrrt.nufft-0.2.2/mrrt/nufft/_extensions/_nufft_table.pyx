"""
The underlying C code for these routines are adapted from C code originally
developed by Jeff Fessler and his students at the University of Michigan.

OpenMP support and the Cython wrappers were added by Gregory R. Lee
(Cincinnati Childrens Hospital Medical Center).

Note: The adjoint NUFFT is only threaded across multiple coils and / or
repetitions. This was done for simplicity to avoid any potential thread
conflicts.
"""
from __future__ import division, print_function, absolute_import

cimport cython
import numpy as np
cimport numpy as cnp


def _determine_dtypes(h1):
    kernel_dtype = h1.dtype
    cplx_dtype = np.result_type(kernel_dtype, np.complex64)
    if kernel_dtype in [np.complex64, np.complex128]:
        cplx_kernel = True
    else:
        cplx_kernel = False
    return kernel_dtype, cplx_dtype, cplx_kernel


def _interp1_table_forward(
    ck, int K1, h1, int J1, int L1, tm, int M, int N):
    cdef:
        float_interp1_forward_cplx_t floatfunc_cplx
        float_interp1_forward_real_t floatfunc_real
        double_interp1_forward_cplx_t doublefunc_cplx
        double_interp1_forward_real_t doublefunc_real
        int nn = 0

    kernel_dtype, cplx_dtype, cplx_kernel = _determine_dtypes(h1)
    fm = np.zeros((M, N), dtype=cplx_dtype, order='F')
    ck = np.asarray(ck, dtype=cplx_dtype)
    if tm.dtype != h1.real.dtype:
        tm = tm.astype(h1.real.dtype)
    if ck.ndim == 2:
        ck = ck[..., np.newaxis]

    floatfunc_cplx = float_interp1_table1_complex_forward
    doublefunc_cplx = double_interp1_table1_complex_forward
    doublefunc_real = double_interp1_table1_real_forward
    floatfunc_real = float_interp1_table1_real_forward

    tm = np.asfortranarray(tm)
    r_fm = np.asfortranarray(fm[:, 0].real)
    i_fm = np.asfortranarray(fm[:, 0].imag)

    r_h1 = np.asfortranarray(h1.real)
    if cplx_kernel:
        i_h1 = np.asfortranarray(h1.imag)

    for nn in range(0, N):  # never tested for N>1!
        r_ck = np.asfortranarray(ck[:, nn].real)
        i_ck = np.asfortranarray(ck[:, nn].imag)

        if kernel_dtype == np.complex64:
            floatfunc_cplx(
                <float*>cnp.PyArray_DATA(r_ck),   # [K1,K2] in
                <float*>cnp.PyArray_DATA(i_ck),
                K1,
                <float*>cnp.PyArray_DATA(r_h1), # [J1*L1+1,1] in
                <float*>cnp.PyArray_DATA(i_h1),
                J1,
                L1,
                <float*>cnp.PyArray_DATA(tm), # [M,2] in
                M,
                <float*>cnp.PyArray_DATA(r_fm),     # [M,1] out
                <float*>cnp.PyArray_DATA(i_fm))
        elif kernel_dtype == np.complex128:
            doublefunc_cplx(
                <double*>cnp.PyArray_DATA(r_ck),   # [K1,K2] in
                <double*>cnp.PyArray_DATA(i_ck),
                K1,
                <double*>cnp.PyArray_DATA(r_h1), # [J1*L1+1,1] in
                <double*>cnp.PyArray_DATA(i_h1),
                J1,
                L1,
                <double*>cnp.PyArray_DATA(tm), # [M,2] in
                M,
                <double*>cnp.PyArray_DATA(r_fm),     # [M,1] out
                <double*>cnp.PyArray_DATA(i_fm))
        elif kernel_dtype == np.float32:
            floatfunc_real(
                <float*>cnp.PyArray_DATA(r_ck),   # [K1,K2] in
                <float*>cnp.PyArray_DATA(i_ck),
                K1,
                <float*>cnp.PyArray_DATA(r_h1), # [J1*L1+1,1] in
                J1,
                L1,
                <float*>cnp.PyArray_DATA(tm), # [M,2] in
                M,
                <float*>cnp.PyArray_DATA(r_fm),     # [M,1] out
                <float*>cnp.PyArray_DATA(i_fm))
        elif kernel_dtype == np.float64:
            doublefunc_real(
                <double*>cnp.PyArray_DATA(r_ck),   # [K1,K2] in
                <double*>cnp.PyArray_DATA(i_ck),
                K1,
                <double*>cnp.PyArray_DATA(r_h1), # [J1*L1+1,1] in
                J1,
                L1,
                <double*>cnp.PyArray_DATA(tm), # [M,2] in
                M,
                <double*>cnp.PyArray_DATA(r_fm),     # [M,1] out
                <double*>cnp.PyArray_DATA(i_fm))
        else:
            raise ValueError("invalid algorithm specified")
        fm[:, nn].real = r_fm
        fm[:, nn].imag = i_fm
    return fm


def _interp1_table_adj(
        fm, int K1, h1, int J1, int L1, tm, int M, int N):
    cdef:
        float_interp1_adj_cplx_t floatfunc_cplx
        float_interp1_adj_real_t floatfunc_real
        double_interp1_adj_cplx_t doublefunc_cplx
        double_interp1_adj_real_t doublefunc_real

    fm = np.asarray(fm)  # from Matrix to array
    if fm.ndim == 1:
        fm = fm[..., np.newaxis]

    kernel_dtype, cplx_dtype, cplx_kernel = _determine_dtypes(h1)
    ck = np.zeros((K1, N), dtype=cplx_dtype, order='F')
    if tm.dtype != h1.real.dtype:
        tm = tm.astype(h1.real.dtype)

    floatfunc_cplx = float_interp1_table1_complex_adj
    doublefunc_cplx = double_interp1_table1_complex_adj
    doublefunc_real = double_interp1_table1_real_adj
    floatfunc_real = float_interp1_table1_real_adj

    tm = np.asfortranarray(tm)

    r_fm = np.asfortranarray(fm.real)
    i_fm = np.asfortranarray(fm.imag)

    r_ck = np.zeros(ck.shape, dtype=ck.real.dtype, order='F')
    i_ck = np.zeros(ck.shape, dtype=ck.real.dtype, order='F')

    r_h1 = np.asfortranarray(h1.real)
    if cplx_kernel:
        i_h1 = np.asfortranarray(h1.imag)

    if kernel_dtype == np.complex64:
        floatfunc_cplx(
            <float*>cnp.PyArray_DATA(r_ck),   # [K1,K2] in
            <float*>cnp.PyArray_DATA(i_ck),
            K1,
            <float*>cnp.PyArray_DATA(r_h1), # [J1*L1+1,1] in
            <float*>cnp.PyArray_DATA(i_h1),
            J1,
            L1,
            <float*>cnp.PyArray_DATA(tm), # [M,2] in
            M,
            <float*>cnp.PyArray_DATA(r_fm),     # [M,1] out
            <float*>cnp.PyArray_DATA(i_fm),
            N)
    elif kernel_dtype == np.complex128:
        doublefunc_cplx(
            <double*>cnp.PyArray_DATA(r_ck),   # [K1,K2] in
            <double*>cnp.PyArray_DATA(i_ck),
            K1,
            <double*>cnp.PyArray_DATA(r_h1), # [J1*L1+1,1] in
            <double*>cnp.PyArray_DATA(i_h1),
            J1,
            L1,
            <double*>cnp.PyArray_DATA(tm), # [M,2] in
            M,
            <double*>cnp.PyArray_DATA(r_fm),     # [M,1] out
            <double*>cnp.PyArray_DATA(i_fm),
            N)
    elif kernel_dtype == np.float32:
        floatfunc_real(
            <float*>cnp.PyArray_DATA(r_ck),   # [K1,K2] in
            <float*>cnp.PyArray_DATA(i_ck),
            K1,
            <float*>cnp.PyArray_DATA(r_h1), # [J1*L1+1,1] in
            J1,
            L1,
            <float*>cnp.PyArray_DATA(tm), # [M,2] in
            M,
            <float*>cnp.PyArray_DATA(r_fm),     # [M,1] out
            <float*>cnp.PyArray_DATA(i_fm),
            N)
    elif kernel_dtype == np.float64:
        doublefunc_real(
            <double*>cnp.PyArray_DATA(r_ck),   # [K1,K2] in
            <double*>cnp.PyArray_DATA(i_ck),
            K1,
            <double*>cnp.PyArray_DATA(r_h1), # [J1*L1+1,1] in
            J1,
            L1,
            <double*>cnp.PyArray_DATA(tm), # [M,2] in
            M,
            <double*>cnp.PyArray_DATA(r_fm),     # [M,1] out
            <double*>cnp.PyArray_DATA(i_fm),
            N)
    else:
        raise ValueError("invalid algorithm specified")
    ck.real = np.asfortranarray(r_ck)
    ck.imag = np.asfortranarray(i_ck)
    return ck


def _interp2_table_forward(
    ck, Kd, h1, h2, Jd, int L1, tm, int M, int N):
    cdef:
        int J1 = Jd[0]
        int J2 = Jd[1]
        int K1 = Kd[0]
        int K2 = Kd[1]
        int nn = 0
        float_interp2_forward_cplx_t floatfunc_cplx
        float_interp2_forward_real_t floatfunc_real
        double_interp2_forward_cplx_t doublefunc_cplx
        double_interp2_forward_real_t doublefunc_real

    kernel_dtype, cplx_dtype, cplx_kernel = _determine_dtypes(h1)
    fm = np.zeros((M, N), dtype=cplx_dtype, order='F')
    ck = np.asarray(ck, dtype=cplx_dtype)
    if tm.dtype != h1.real.dtype:
        tm = tm.astype(h1.real.dtype)

    if ck.ndim == 2:
        ck = ck[..., np.newaxis]

    floatfunc_cplx = float_interp2_table1_complex_forward
    doublefunc_cplx = double_interp2_table1_complex_forward
    doublefunc_real = double_interp2_table1_real_forward
    floatfunc_real = float_interp2_table1_real_forward

    tm = np.asfortranarray(tm)
    r_fm = np.asfortranarray(fm[:, 0].real)
    i_fm = np.asfortranarray(fm[:, 0].imag)

    r_h1 = np.asfortranarray(h1.real)
    r_h2 = np.asfortranarray(h2.real)
    if cplx_kernel:
        i_h2 = np.asfortranarray(h2.imag)
        i_h1 = np.asfortranarray(h1.imag)

    for nn in range(0, N):  # never tested for N>1!
        r_ck = np.asfortranarray(ck[:, :, nn].real)
        i_ck = np.asfortranarray(ck[:, :, nn].imag)

        if kernel_dtype == np.complex64:
            floatfunc_cplx(
                <float*>cnp.PyArray_DATA(r_ck),   # [K1,K2] in
                <float*>cnp.PyArray_DATA(i_ck),
                K1,
                K2,
                <float*>cnp.PyArray_DATA(r_h1), # [J1*L1+1,1] in
                <float*>cnp.PyArray_DATA(i_h1),
                <float*>cnp.PyArray_DATA(r_h2), # [J2*L1+1,1] in
                <float*>cnp.PyArray_DATA(i_h2),
                J1,
                J2,
                L1,
                <float*>cnp.PyArray_DATA(tm), # [M,2] in
                M,
                <float*>cnp.PyArray_DATA(r_fm),     # [M,1] out
                <float*>cnp.PyArray_DATA(i_fm))
        elif kernel_dtype == np.complex128:
            doublefunc_cplx(
                <double*>cnp.PyArray_DATA(r_ck),   # [K1,K2] in
                <double*>cnp.PyArray_DATA(i_ck),
                K1,
                K2,
                <double*>cnp.PyArray_DATA(r_h1), # [J1*L1+1,1] in
                <double*>cnp.PyArray_DATA(i_h1),
                <double*>cnp.PyArray_DATA(r_h2), # [J2*L1+1,1] in
                <double*>cnp.PyArray_DATA(i_h2),
                J1,
                J2,
                L1,
                <double*>cnp.PyArray_DATA(tm), # [M,2] in
                M,
                <double*>cnp.PyArray_DATA(r_fm),     # [M,1] out
                <double*>cnp.PyArray_DATA(i_fm))
        elif kernel_dtype == np.float32:
            floatfunc_real(
                <float*>cnp.PyArray_DATA(r_ck),   # [K1,K2] in
                <float*>cnp.PyArray_DATA(i_ck),
                K1,
                K2,
                <float*>cnp.PyArray_DATA(r_h1), # [J1*L1+1,1] in
                <float*>cnp.PyArray_DATA(r_h2), # [J2*L1+1,1] in
                J1,
                J2,
                L1,
                <float*>cnp.PyArray_DATA(tm), # [M,2] in
                M,
                <float*>cnp.PyArray_DATA(r_fm),     # [M,1] out
                <float*>cnp.PyArray_DATA(i_fm))
        elif kernel_dtype == np.float64:
            doublefunc_real(
                <double*>cnp.PyArray_DATA(r_ck),   # [K1,K2] in
                <double*>cnp.PyArray_DATA(i_ck),
                K1,
                K2,
                <double*>cnp.PyArray_DATA(r_h1), # [J1*L1+1,1] in
                <double*>cnp.PyArray_DATA(r_h2), # [J2*L1+1,1] in
                J1,
                J2,
                L1,
                <double*>cnp.PyArray_DATA(tm), # [M,2] in
                M,
                <double*>cnp.PyArray_DATA(r_fm),     # [M,1] out
                <double*>cnp.PyArray_DATA(i_fm))
        else:
            raise ValueError("invalid algorithm specified")
        fm[:, nn].real = r_fm
        fm[:, nn].imag = i_fm

    return fm


def _interp2_table_adj(
        fm, Kd, h1, h2, Jd, int L1, tm, int M, int N):
    cdef:
        int J1 = Jd[0]
        int J2 = Jd[1]
        int K1 = Kd[0]
        int K2 = Kd[1]
        float_interp2_adj_cplx_t floatfunc_cplx
        float_interp2_adj_real_t floatfunc_real
        double_interp2_adj_cplx_t doublefunc_cplx
        double_interp2_adj_real_t doublefunc_real

    fm = np.asarray(fm)  # from Matrix to array
    if fm.ndim == 1:
        fm = fm[..., np.newaxis]

    kernel_dtype, cplx_dtype, cplx_kernel = _determine_dtypes(h1)

    ck = np.zeros((np.prod(Kd), N), dtype=cplx_dtype, order='F')
    if tm.dtype != h1.real.dtype:
        tm = tm.astype(h1.real.dtype)

    floatfunc_cplx = float_interp2_table1_complex_adj
    doublefunc_cplx = double_interp2_table1_complex_adj
    doublefunc_real = double_interp2_table1_real_adj
    floatfunc_real = float_interp2_table1_real_adj

    tm = np.asfortranarray(tm)

    r_fm = np.asfortranarray(fm.real)
    i_fm = np.asfortranarray(fm.imag)

    r_ck = np.zeros(ck.shape, dtype=ck.real.dtype, order='F')
    i_ck = np.zeros(ck.shape, dtype=ck.real.dtype, order='F')

    r_h1 = np.asfortranarray(h1.real)
    r_h2 = np.asfortranarray(h2.real)
    if cplx_kernel:
        i_h1 = np.asfortranarray(h1.imag)
        i_h2 = np.asfortranarray(h2.imag)

    if kernel_dtype == np.complex64:
        floatfunc_cplx(
            <float*>cnp.PyArray_DATA(r_ck),   # [K1,K2] in
            <float*>cnp.PyArray_DATA(i_ck),
            K1,
            K2,
            <float*>cnp.PyArray_DATA(r_h1), # [J1*L1+1,1] in
            <float*>cnp.PyArray_DATA(i_h1),
            <float*>cnp.PyArray_DATA(r_h2), # [J2*L1+1,1] in
            <float*>cnp.PyArray_DATA(i_h2),
            J1,
            J2,
            L1,
            <float*>cnp.PyArray_DATA(tm), # [M,2] in
            M,
            <float*>cnp.PyArray_DATA(r_fm),     # [M,1] out
            <float*>cnp.PyArray_DATA(i_fm),
            N)
    elif kernel_dtype == np.complex128:
        doublefunc_cplx(
            <double*>cnp.PyArray_DATA(r_ck),   # [K1,K2] in
            <double*>cnp.PyArray_DATA(i_ck),
            K1,
            K2,
            <double*>cnp.PyArray_DATA(r_h1), # [J1*L1+1,1] in
            <double*>cnp.PyArray_DATA(i_h1),
            <double*>cnp.PyArray_DATA(r_h2), # [J2*L1+1,1] in
            <double*>cnp.PyArray_DATA(i_h2),
            J1,
            J2,
            L1,
            <double*>cnp.PyArray_DATA(tm), # [M,2] in
            M,
            <double*>cnp.PyArray_DATA(r_fm),     # [M,1] out
            <double*>cnp.PyArray_DATA(i_fm),
            N)
    elif kernel_dtype == np.float32:
        floatfunc_real(
            <float*>cnp.PyArray_DATA(r_ck),   # [K1,K2] in
            <float*>cnp.PyArray_DATA(i_ck),
            K1,
            K2,
            <float*>cnp.PyArray_DATA(r_h1), # [J1*L1+1,1] in
            <float*>cnp.PyArray_DATA(r_h2), # [J2*L1+1,1] in
            J1,
            J2,
            L1,
            <float*>cnp.PyArray_DATA(tm), # [M,2] in
            M,
            <float*>cnp.PyArray_DATA(r_fm),     # [M,1] out
            <float*>cnp.PyArray_DATA(i_fm),
            N)
    elif kernel_dtype == np.float64:
        doublefunc_real(
            <double*>cnp.PyArray_DATA(r_ck),   # [K1,K2] in
            <double*>cnp.PyArray_DATA(i_ck),
            K1,
            K2,
            <double*>cnp.PyArray_DATA(r_h1), # [J1*L1+1,1] in
            <double*>cnp.PyArray_DATA(r_h2), # [J2*L1+1,1] in
            J1,
            J2,
            L1,
            <double*>cnp.PyArray_DATA(tm), # [M,2] in
            M,
            <double*>cnp.PyArray_DATA(r_fm),     # [M,1] out
            <double*>cnp.PyArray_DATA(i_fm),
            N)
    else:
        raise ValueError("invalid algorithm specified")
    ck.real = np.asfortranarray(r_ck)
    ck.imag = np.asfortranarray(i_ck)
    return ck


def _interp3_table_forward(
    ck, Kd, h1, h2, h3, Jd, int L1, tm, int M, int N):
    cdef:
        int J1 = Jd[0]
        int J2 = Jd[1]
        int J3 = Jd[2]
        int K1 = Kd[0]
        int K2 = Kd[1]
        int K3 = Kd[2]
        int nn = 0
        float_interp3_forward_cplx_t floatfunc_cplx
        float_interp3_forward_real_t floatfunc_real
        double_interp3_forward_cplx_t doublefunc_cplx
        double_interp3_forward_real_t doublefunc_real

    kernel_dtype, cplx_dtype, cplx_kernel = _determine_dtypes(h1)
    fm = np.zeros((M, N), dtype=cplx_dtype, order='F')
    ck = np.asarray(ck, dtype=cplx_dtype)
    if tm.dtype != h1.real.dtype:
        tm = tm.astype(h1.real.dtype)

    if ck.ndim == 2:
        ck = ck[..., np.newaxis]

    floatfunc_cplx = float_interp3_table1_complex_forward
    doublefunc_cplx = double_interp3_table1_complex_forward
    doublefunc_real = double_interp3_table1_real_forward
    floatfunc_real = float_interp3_table1_real_forward

    tm = np.asfortranarray(tm)
    r_fm = np.asfortranarray(fm[:, 0].real)
    i_fm = np.asfortranarray(fm[:, 0].imag)

    r_h1 = np.asfortranarray(h1.real)
    r_h2 = np.asfortranarray(h2.real)
    r_h3 = np.asfortranarray(h3.real)
    if cplx_kernel:
        i_h1 = np.asfortranarray(h1.imag)
        i_h2 = np.asfortranarray(h2.imag)
        i_h3 = np.asfortranarray(h3.imag)

    for nn in range(0, N):  # never tested for N>1!
        r_ck = np.asfortranarray(ck[:, :, :, nn].real)
        i_ck = np.asfortranarray(ck[:, :, :, nn].imag)

        if kernel_dtype == np.complex64:
            floatfunc_cplx(
                <float*>cnp.PyArray_DATA(r_ck),   # [K1,K2] in
                <float*>cnp.PyArray_DATA(i_ck),
                K1,
                K2,
                K3,
                <float*>cnp.PyArray_DATA(r_h1), # [J1*L1+1,1] in
                <float*>cnp.PyArray_DATA(i_h1),
                <float*>cnp.PyArray_DATA(r_h2), # [J2*L1+1,1] in
                <float*>cnp.PyArray_DATA(i_h2),
                <float*>cnp.PyArray_DATA(r_h3),
                <float*>cnp.PyArray_DATA(i_h3),
                J1,
                J2,
                J3,
                L1,
                <float*>cnp.PyArray_DATA(tm), # [M,2] in
                M,
                <float*>cnp.PyArray_DATA(r_fm),     # [M,1] out
                <float*>cnp.PyArray_DATA(i_fm))
        elif kernel_dtype == np.complex128:
            doublefunc_cplx(
                <double*>cnp.PyArray_DATA(r_ck),   # [K1,K2] in
                <double*>cnp.PyArray_DATA(i_ck),
                K1,
                K2,
                K3,
                <double*>cnp.PyArray_DATA(r_h1), # [J1*L1+1,1] in
                <double*>cnp.PyArray_DATA(i_h1),
                <double*>cnp.PyArray_DATA(r_h2), # [J2*L1+1,1] in
                <double*>cnp.PyArray_DATA(i_h2),
                <double*>cnp.PyArray_DATA(r_h3),
                <double*>cnp.PyArray_DATA(i_h3),
                J1,
                J2,
                J3,
                L1,
                <double*>cnp.PyArray_DATA(tm), # [M,2] in
                M,
                <double*>cnp.PyArray_DATA(r_fm),     # [M,1] out
                <double*>cnp.PyArray_DATA(i_fm))
        elif kernel_dtype == np.float32:
            floatfunc_real(
                <float*>cnp.PyArray_DATA(r_ck),   # [K1,K2] in
                <float*>cnp.PyArray_DATA(i_ck),
                K1,
                K2,
                K3,
                <float*>cnp.PyArray_DATA(r_h1), # [J1*L1+1,1] in
                <float*>cnp.PyArray_DATA(r_h2), # [J2*L1+1,1] in
                <float*>cnp.PyArray_DATA(r_h3), # [J3*L1+1,1] in
                J1,
                J2,
                J3,
                L1,
                <float*>cnp.PyArray_DATA(tm), # [M,2] in
                M,
                <float*>cnp.PyArray_DATA(r_fm),     # [M,1] out
                <float*>cnp.PyArray_DATA(i_fm))
        elif kernel_dtype == np.float64:
            doublefunc_real(
                <double*>cnp.PyArray_DATA(r_ck),   # [K1,K2] in
                <double*>cnp.PyArray_DATA(i_ck),
                K1,
                K2,
                K3,
                <double*>cnp.PyArray_DATA(r_h1), # [J1*L1+1,1] in
                <double*>cnp.PyArray_DATA(r_h2), # [J2*L1+1,1] in
                <double*>cnp.PyArray_DATA(r_h3), # [J3*L1+1,1] in
                J1,
                J2,
                J3,
                L1,
                <double*>cnp.PyArray_DATA(tm), # [M,2] in
                M,
                <double*>cnp.PyArray_DATA(r_fm),     # [M,1] out
                <double*>cnp.PyArray_DATA(i_fm))
        else:
            raise ValueError("invalid algorithm specified")
        fm[:, nn].real = r_fm
        fm[:, nn].imag = i_fm
    return fm


def _interp3_table_adj(
        fm, Kd, h1, h2, h3, Jd, int L1, tm, int M, int N):
    cdef:
        int J1 = Jd[0]
        int J2 = Jd[1]
        int J3 = Jd[2]
        int K1 = Kd[0]
        int K2 = Kd[1]
        int K3 = Kd[2]
        float_interp3_adj_cplx_t floatfunc_cplx
        float_interp3_adj_real_t floatfunc_real
        double_interp3_adj_cplx_t doublefunc_cplx
        double_interp3_adj_real_t doublefunc_real

    fm = np.asarray(fm)  # from Matrix to array
    if fm.ndim == 1:
        fm = fm[..., np.newaxis]

    kernel_dtype, cplx_dtype, cplx_kernel = _determine_dtypes(h1)
    ck = np.zeros((np.prod(Kd), N), dtype=cplx_dtype, order='F')
    if tm.dtype != h1.real.dtype:
        tm = tm.astype(h1.real.dtype)

    floatfunc_cplx = float_interp3_table1_complex_adj
    doublefunc_cplx = double_interp3_table1_complex_adj
    doublefunc_real = double_interp3_table1_real_adj
    floatfunc_real = float_interp3_table1_real_adj

    tm = np.asfortranarray(tm)

    r_fm = np.asfortranarray(fm.real)
    i_fm = np.asfortranarray(fm.imag)

    r_ck = np.zeros(ck.shape, dtype=ck.real.dtype, order='F')
    i_ck = np.zeros(ck.shape, dtype=ck.real.dtype, order='F')

    r_h1 = np.asfortranarray(h1.real)
    r_h2 = np.asfortranarray(h2.real)
    r_h3 = np.asfortranarray(h3.real)
    if cplx_kernel:
        i_h1 = np.asfortranarray(h1.imag)
        i_h2 = np.asfortranarray(h2.imag)
        i_h3 = np.asfortranarray(h3.imag)

    if kernel_dtype == np.complex64:
        floatfunc_cplx(
            <float*>cnp.PyArray_DATA(r_ck),   # [K1,K2] in
            <float*>cnp.PyArray_DATA(i_ck),
            K1,
            K2,
            K3,
            <float*>cnp.PyArray_DATA(r_h1), # [J1*L1+1,1] in
            <float*>cnp.PyArray_DATA(i_h1),
            <float*>cnp.PyArray_DATA(r_h2), # [J2*L1+1,1] in
            <float*>cnp.PyArray_DATA(i_h2),
            <float*>cnp.PyArray_DATA(r_h3),
            <float*>cnp.PyArray_DATA(i_h3),
            J1,
            J2,
            J3,
            L1,
            <float*>cnp.PyArray_DATA(tm), # [M,2] in
            M,
            <float*>cnp.PyArray_DATA(r_fm),     # [M,1] out
            <float*>cnp.PyArray_DATA(i_fm),
            N)
    elif kernel_dtype == np.complex128:
        doublefunc_cplx(
            <double*>cnp.PyArray_DATA(r_ck),   # [K1,K2] in
            <double*>cnp.PyArray_DATA(i_ck),
            K1,
            K2,
            K3,
            <double*>cnp.PyArray_DATA(r_h1), # [J1*L1+1,1] in
            <double*>cnp.PyArray_DATA(i_h1),
            <double*>cnp.PyArray_DATA(r_h2), # [J2*L1+1,1] in
            <double*>cnp.PyArray_DATA(i_h2),
            <double*>cnp.PyArray_DATA(r_h3),
            <double*>cnp.PyArray_DATA(i_h3),
            J1,
            J2,
            J3,
            L1,
            <double*>cnp.PyArray_DATA(tm), # [M,2] in
            M,
            <double*>cnp.PyArray_DATA(r_fm),     # [M,1] out
            <double*>cnp.PyArray_DATA(i_fm),
            N)
    elif kernel_dtype == np.float32:
        floatfunc_real(
            <float*>cnp.PyArray_DATA(r_ck),   # [K1,K2] in
            <float*>cnp.PyArray_DATA(i_ck),
            K1,
            K2,
            K3,
            <float*>cnp.PyArray_DATA(r_h1), # [J1*L1+1,1] in
            <float*>cnp.PyArray_DATA(r_h2), # [J2*L1+1,1] in
            <float*>cnp.PyArray_DATA(r_h3), # [J3*L1+1,1] in
            J1,
            J2,
            J3,
            L1,
            <float*>cnp.PyArray_DATA(tm), # [M,2] in
            M,
            <float*>cnp.PyArray_DATA(r_fm),     # [M,1] out
            <float*>cnp.PyArray_DATA(i_fm),
            N)
    elif kernel_dtype == np.float64:
        doublefunc_real(
            <double*>cnp.PyArray_DATA(r_ck),   # [K1,K2] in
            <double*>cnp.PyArray_DATA(i_ck),
            K1,
            K2,
            K3,
            <double*>cnp.PyArray_DATA(r_h1), # [J1*L1+1,1] in
            <double*>cnp.PyArray_DATA(r_h2), # [J2*L1+1,1] in
            <double*>cnp.PyArray_DATA(r_h3), # [J3*L1+1,1] in
            J1,
            J2,
            J3,
            L1,
            <double*>cnp.PyArray_DATA(tm), # [M,2] in
            M,
            <double*>cnp.PyArray_DATA(r_fm),     # [M,1] out
            <double*>cnp.PyArray_DATA(i_fm),
            N)
    else:
        raise ValueError("invalid algorithm specified")
    ck.real = np.asfortranarray(r_ck)
    ck.imag = np.asfortranarray(i_ck)
    return ck
