# -*- coding: utf-8 -*-
"""
run-up with constant rotational acceleration 
of a Jeffcott rotor in journal bearings (analytical short bearing solution)

Created on Jan 04 2022

@author: Gerrit Nowald
"""

import rotordynamic as rd

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

import time

g = 9.81    # gravitational acceleration

# -----------------------------------------------------------------------------
# parameters

m   = 0.1       # mass of rotor / kg
mj  = 1e-5      # journal mass / kg
eps = m*1e-6    # center of mass eccentricity / m (unbalance)
cs  = 1e5       # shaft stiffness / N/m
d   = 1e-2*np.sqrt(cs*m)     # damping coefficient / Ns/m (modal damping)

BB = 3.5e-3     # journal width / m
DB = 7e-3       # journal diameter / m
CB = 15e-6      # bearing gap / m
eta = 1e-2     # dyn. oil viscosity / Ns/m^2

tmax = 1                    # max. time of calculation / s
fmax = 500                  # max rotational frequency / Hz
arot = 2*np.pi*fmax/tmax    # acceleration of rotor speed / rad/s**2 (reach fmax in tmax)

# -----------------------------------------------------------------------------
# functions

def rotor_Jeffcott(t, q):
    FB   = 2*rd.bearing_journal_short(q[[0,2,4,6]],BB,DB,CB,eta,arot*t)    # bearing forces
    FU   = rd.unbalance_const_acc(t,eps,arot)       # unbalance forces
    Fvec = np.array([ FB[0], FU[0], FB[1], FU[1] ]) # external forces physical space
    fvec = np.hstack(( np.zeros(4), Minv @ Fvec ))  # external forces state space
    return A @ q + fvec - gvec

# -----------------------------------------------------------------------------
# system matrices [xj, xm, yj, ym]

M = np.diag([mj,m,mj,m])

O = np.array([[1,-1], [-1,1]])
D = np.vstack(( np.hstack((  d*O, np.zeros((2,2)) )), np.hstack(( np.zeros((2,2)),  d*O )) ))
C = np.vstack(( np.hstack(( cs*O, np.zeros((2,2)) )), np.hstack(( np.zeros((2,2)), cs*O )) ))

A, Minv = rd.state_space(M,D,C)                             # state space matrix
gvec    = g*np.hstack(( np.zeros(6), np.array([1,1]) ))     # gravity state space

# -----------------------------------------------------------------------------
# initial conditions
# q0 = [xj, xm, yj, ym, xdj, xdm, ydj, ydm]

q0  = np.zeros(8) + 1e-10

# -----------------------------------------------------------------------------
# numerical integration

start_time = time.time()
res = solve_ivp(rotor_Jeffcott, [0, tmax], q0,
                t_eval = np.linspace(0, tmax, int(tmax*fmax*30) ),    # points of orbit at highest frequency
                rtol=1e-6, atol=1e-6, method='BDF' )
print(f"elapsed time: {time.time() - start_time} s")

# -----------------------------------------------------------------------------
# plot

plt.figure()

# displacement over time
plt.subplot(221)
plt.plot(res.t, np.sqrt(res.y[0]**2+res.y[2]**2)/CB )
plt.title("journal eccentricity")
plt.xlabel("time / s")
plt.ylabel("epsilon")
plt.grid()

# phase diagram
plt.subplot(222)
plt.plot(res.y[0]/CB, res.y[2]/CB )
plt.title("journal orbit")
plt.xlabel("x/C")
plt.ylabel("y/C")
plt.grid()