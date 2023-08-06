#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
from libHREELS import lambin, importMaterials

###### Define Strontium titanate film on Silver ####
## (Thickness is given in Angstroem as second parm)#
thinFilm = [[importMaterials('STO'),200.],
    [importMaterials('Ag'),1000.]]

d = lambin(thinFilm)
x = np.linspace(-100,1000,1100)
x,y = d.calcHREELS(x)

###### Plotting ###########################
plt.plot(x,y, label=importMaterials('STO')['reference'])

plt.ylabel('Relative HREELS signal')
plt.xlabel('Energy Loss (cm$^{-1}$)')
plt.title(r'SrTiO$_3$')
plt.ylim(bottom=0.)
plt.legend()
plt.show()