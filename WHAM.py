import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import constants as c
import math as m
import glob
import seaborn as sns
import pathlib

xvg = glob.glob('path/to/files/*.xvg')
def e(a):
    approx = 1.0000000
    for i in range(1, 5):
        approx += ((a**i) / m.factorial(i))
    return approx

def diff(f, t):
    f = np.array(f)
    dfdt = np.zeros(len(t))
    dfdt = (f[1:] - f[:-1]) / (t[1:] - t[:-1])
    return dfdt

def mgmt(t, nm, bin_edges, ro, ft):
    """ Manages iteration and convergence for WHAM Ft convergence algorithm adapted from 
    The Weighted Histogram Analysis Method for Free-Energy Calculations on Biomolecules. I. The Method
    Shankar Kumar,l Djamal Bouzida,2 Robert H. Swendsen, Peter A. K~ l lmana, ~nd
    John M. Rosenbergl*
    Department of Biological Sciences, University of Pittsburgh, Pittsburgh, Pennsylvania 15260
    Department of Physics, Carnegie Mellon University, Pittsburgh, Pennsylvania 15213
    SDepartment of Pharmaceutical Chemistry, University of California-Sun Francisco, Sun Francisco, California 941 43
    Received 13 February 1992; accepted 28 April 1992"""
    iteration = 0
    while iteration < maxiter:
        ro_list = []
        ft_opt = 0
        xsum = np.sum(bin_edges)
        ysum = np.sum(ro)
        
        """ exp = e(xsum/(c.k*t))
        ef = e(ft)
        ros = np.sum((ro/exp)) / np.sum(nm*(ef/exp)) """
        exp = e(xsum/(c.k*t))
        ef = e(ft)
        ros = ysum*exp / np.sum(nm*1/(ef/exp))

        lnftc = -np.log(ros)
        ft_tol = np.allclose(ft, lnftc, atol=tol, equal_nan=False)
        if np.all(ft_tol):
            print(f'Converged after {iteration} iterations. Ft = {ft}')
            ft_opt = ft
            iteration = 0
            break
        else:
            ft = lnftc
            
        if iteration == maxiter:
            print('WHAM not converging, check input files. There should only be potential energy .xvg files in the folder, and they should all be of equal length. If any are short the simulation may need to be restarted. The program itself need not be rerun, any potentially problematic simulations can be run as in bash as follows: for file file1.xvg file2.xvg file3.xvg ...; do mdrun -f $file -table table.xvg -tablep table.xvg ...; done')
            run = False
            break
        iteration += 1

    return ft_opt, ro_list

ts = []
deg = []
xs = []
ys = []
maxiter = 1000
gk = []
tol = 1e-6
energies = []
for file in xvg:
    beta = 0
    ros = []
    bin_edges = []
    bin_centers = []
    t = int(pathlib.Path(file).stem)
    print(f'Processing {t}')
    ts.append(t)
    potentials = np.loadtxt(file, comments=['@', '#'], usecols=[1])
    potentials = potentials[1:]
    #energies.append(potentials)
    #potentials = potentials/4.184 # convert from kj/mol to kcal/mol
    bins_init = 40
    nm = len(potentials)
    output = sns.histplot(data=potentials, stat='probability', bins=bins_init)
    patches = output.patches
    ros = [patch.get_height() for patch in patches]
    ros = ros[1:]
    bin_edges = np.array([patch.get_x() for patch in patches])
    bin_centers = ((bin_edges[:-1] + bin_edges[1:]) / 2)
    ft = 0
    ft, wros = mgmt(t, nm, bin_centers, ros, ft)
    beta = bin_centers*0.723 # convert from kj/mol to kj and multiply by 1/1.38
    energies.append(bin_centers)
    gk = [r/np.exp(-(b+ft)) for r, b in zip(ros, beta)]
    deg.append(gk)
    gk = []

degs = np.concatenate(deg)
energies = np.concatenate(energies)
indices = np.argsort(degs)
degeneracy =degs[indices]
indices = np.argsort(energies)
energies = energies[indices]
plt.clf()
plt.plot(energies, np.log(degeneracy))
