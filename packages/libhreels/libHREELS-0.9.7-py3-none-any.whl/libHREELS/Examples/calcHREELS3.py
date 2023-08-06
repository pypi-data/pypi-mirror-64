#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
from libHREELS import lambin, importMaterials

# Experimental setup as dictionary:
setup = {
    "e0": 4.0,          # Primary electron energy
    "theta": 60.,       # Scattering angle wrt surface normal
    "phia": 2.0,
    "phib": 2.0,
    "temperature": 80.,# Sample temperature
    "debug": False
}
# Instrumental function describing elastic peak shape:
instrument = {
    "width": 16.,       # Energy resolution in cm-1
    "intensity": 100000.,   # not used.
    "asym": 0.1,        # Elastic peak asymmetry
    "gauss": 0.8        # Gauss vs Lorentian fraction 
}

###### Define Strontium titanate film on Silver ####
## (Thickness is given in Angstroem as second parm)#
thinFilm = [[{'eps': 5.1295,
    'wTO': [177.4, 272.84, 506.379],
    'gTO': [1.9262, 93.3091, 42.6],
    'wLO': [184.003, 470.972, 739.651],
    'gLO': [9.718, 14.31, 33.044],
    'reference': 'BTO323',
    'name': 'BaTiO_3'},
    20000.]]

d = lambin(thinFilm, setup=setup, instrument=instrument)
x = np.linspace(-100,1000,1100)
x,y = d.calcHREELS(x)

###### Plotting ###########################
plt.plot(x,y, label=thinFilm[0][0]['name'])

plt.ylabel('Relative HREELS signal')
plt.xlabel('Energy Loss (cm$^{-1}$)')
plt.ylim(bottom=0.)
plt.legend()
plt.show()