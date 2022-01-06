# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np

def fun_short_bearing(eps,epsS,phiS,B2D):
# journal bearing forces short bearing theory
    E = 2*epsS # radial dimensionless speed
    G = 2*phiS     # tangential dimensionless speed
    if E==0 and G==0:   # case 1: only rotation
        fr   = 2*eps**2/(1-eps**2)**2
        fphi = - 0.5*np.pi*eps/(1-eps**2)**1.5
    else:               # case 2: rotation + squeeze
        if G>1:             # case 2a
            tan_kappa_1 = E/(eps*(1-G))
            cos_kappa_1 = 1/np.sqrt(1+tan_kappa_1**2)
            sin_kappa_1 = tan_kappa_1/np.sqrt(1+tan_kappa_1**2)
        else:               # case 2b: G<=1
            if G==1:            # case 2b1 (singularity)
                if E>0:             # case 2b1a
                    tan_kappa_1 = -1e16
                else:               # case 2b1b: E<0
                    tan_kappa_1 =  1e16
            else:               # case 2b2: G<1
                tan_kappa_1 = E/(eps*(1-G))
            cos_kappa_1 = - 1/np.sqrt(1+tan_kappa_1**2)
            sin_kappa_1 = - tan_kappa_1/np.sqrt(1+tan_kappa_1**2)
        if sin_kappa_1/(1+cos_kappa_1) < 0:
            piS = np.pi
        else:
            piS = 0
        # integrals
        I1 = 2*eps*cos_kappa_1**3/(1-eps**2*cos_kappa_1**2)**2
        I2 = - eps*sin_kappa_1*(1-(2-eps**2)*cos_kappa_1**2)/(1-eps**2)/(1-eps**2*cos_kappa_1**2)**2 + (piS + np.arctan(np.sqrt(1-eps**2)/eps/sin_kappa_1))/(1-eps**2)**1.5
        I3 = - eps*sin_kappa_1*(4-eps**2*(1+(2+eps**2)*cos_kappa_1**2))/(1-eps**2)**2/(1-eps**2*cos_kappa_1**2)**2 + (piS + np.arctan(np.sqrt(1-eps**2)/eps/sin_kappa_1))*(2+eps**2)/(1-eps**2)**2.5
        # dimensionless forces
        fr   = B2D**2*( I2*eps*(1-G) - E*I1 )
        fphi = B2D**2*( I1*eps*(1-G) + E*(I2-I3) )
    return np.array([fr, fphi])

    
print(fun_short_bearing(0.7, 0, 0,  0.5))   # 1
print(fun_short_bearing(0.7, 0, 1,  0.5))   # 2a sin_kappa_1=0
print(fun_short_bearing(0.7, 1, 1,  0.5))   # 2a
print(fun_short_bearing(0.7, 1, 0.5, 0.5))  # 2b1a
print(fun_short_bearing(0.7, 0, 0.5, 0.5))  # 2b1b
print(fun_short_bearing(0.7, 0, - 0.5, 0.5))  # 2b1b sin_kappa_1=0