#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
from libHREELS import lambin, importMaterials

###### Define Barium titanate film on Silver ####
## (Thickness is given in Angstroem as second parm)#
thinFilm = [[{'eps': 5.1295,
    'wTO': [177.4, 272.84, 506.379],
    'gTO': [1.9262, 93.3091, 42.6],
    'wLO': [184.003, 470.972, 739.651],
    'gLO': [9.718, 14.31, 33.044],
    'reference': 'BTO323',
    'name': 'BaTiO_3'},
    20000.]]

d = lambin(thinFilm)
x = np.linspace(-100,1000,1100)
x,y = d.calcHREELS(x)

###### Plotting ###########################
plt.plot(x,y, label=thinFilm[0][0]['name'])

plt.ylabel('Relative HREELS signal')
plt.xlabel('Energy Loss (cm$^{-1}$)')
plt.ylim(bottom=0.)
plt.legend()
plt.show()