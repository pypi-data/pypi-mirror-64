from libHREELS import *
import sys
import matplotlib.pyplot as plt
import numpy as np

# datapath = ".\\data"
datapath = "./data"

d2 = HREELS('c1a02', datapath=datapath)
d1 = HREELS('c1a03', datapath=datapath)


d1.figure()

d1.plot(xmin=40, normalized=True, color='red', factor = 10, label=d1.fname)
d2.plot(xmin=40, normalized=True, color='black', factor = 10, label=d2.fname)
d2.plot(normalized=True, color='gray', factor = 1, label=None)

d1.ax.set_ylim(bottom=0)
d1.ax.set_xlim(left=-200,right=1300)
plt.axvline(x=69,ymax=0.4, linestyle='dashed')
plt.show()