#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 07:49:52 2020

"""

import camb
import matplotlib as mpl, matplotlib.pyplot as plt, numpy as np 
from pixell import enmap, curvedsky, utils
from matplotlib.colors import ListedColormap

colombi1_cmap = ListedColormap(np.loadtxt("Planck_Parchment_RGB.txt")/255.)
cmap = colombi1_cmap
mpl.rcParams['savefig.pad_inches'] = 0
np.random.seed(0)

 #Set up a new set of parameters for CAMB
pars = camb.CAMBparams()
#This function sets up CosmoMC-like settings, with one massive neutrino and heliu m set using BBN consistency
pars.set_cosmology(H0=67.5, ombh2=0.022, omch2=0.122, mnu=0.06, omk=0, tau=0.06)
pars.InitPower.set_params(As=2e-9, ns=0.965, r=0)
pars.set_for_lmax(2500, lens_potential_accuracy=0);
#calculate results for these parameters
results = camb.get_results(pars)
powers =results.get_cmb_power_spectra(pars, CMB_unit='muK')

#D_ell.shape

D_ell = powers['total'][:,0] 
ells = np.arange(D_ell.shape[0])
# plt.plot(D_ell)
# plt.ylabel('$D_\ell$')
# plt.xlabel('$\ell')

C_ell = D_ell / ((ells * (ells + 1) / (2. * np.pi)))
C_ell[0:2] = 0 # just set these to 0 to avoid division by 0

box = np.array([[-10,10],[10,-10]]) * utils.degree
#shape,wcs = enmap.geometry(pos=box,res=0.5 * utils.arcmin,proj='car')
shape,wcs = enmap.fullsky_geometry(res=1 * utils.arcmin,proj='car')
cmb_map = curvedsky.rand_map(shape, wcs, C_ell)
figsize = 20,10
fig = plt.figure(figsize=figsize)
ax = plt.axes([0,0,1,1], frameon=False)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

plt.autoscale(tight=True)

plt.imshow(cmb_map, cmap = colombi1_cmap)