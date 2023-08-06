# -*- coding: utf-8 -*-

from .context import Context
import ctypes as ct
from .estimator import Estimator
from .calib import sCMOS_Calib

def create_estimator(psf, ctx:Context, scmos : sCMOS_Calib=None):
#CDLL_EXPORT PSF * GLRT_CreatePSF(PSF* model, Context* ctx, sCMOS_Calibration* calib)
        _GLRT_CreatePSF = ctx.smlm.lib.GLRT_CreatePSF
        _GLRT_CreatePSF.argtypes = [
                ct.c_void_p,
                ct.c_void_p
                ]
        _GLRT_CreatePSF.restype = ct.c_void_p

        if scmos is not None:
            assert(isinstance(scmos,sCMOS_Calib))
            scmos = scmos.inst

        inst = _GLRT_CreatePSF(psf.inst, ctx.inst if ctx else None, 
                               scmos)
        psf = Estimator(ctx, inst)
        return psf
    
