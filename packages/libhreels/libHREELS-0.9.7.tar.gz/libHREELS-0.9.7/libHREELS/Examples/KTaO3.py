#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
from libHREELS import lambin, importMaterials

###### Define Strontium titanate film on Silver ####
## (Thickness is given in Angstroem as second parm)#
thinFilm = [[importMaterials('KTO'),20000.],
    [importMaterials('Ag'),1000.]]

d = lambin(thinFilm)
x = np.linspace(-100,1000,1100)
x,y = d.calcHREELS(x)

###### Plotting ###########################
plt.plot(x,y, label=thinFilm[0][0]['reference'])

plt.ylabel('Relative Intensity')
plt.xlabel('Energy Loss (cm$^{-1}$)')
plt.title(thinFilm[0][0]['name'])
plt.ylim(bottom=0.)
plt.legend()
plt.show()