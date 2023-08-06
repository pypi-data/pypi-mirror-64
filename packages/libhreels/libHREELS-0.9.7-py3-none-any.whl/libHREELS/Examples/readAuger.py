import matplotlib.pyplot as plt
# %matplotlib qt
import libHREELS as h
path="./Examples/data"
plt.rcParams['figure.figsize'] = (6,4)
plt.rcParams['figure.dpi'] = 200
plt.rcParams['font.size'] = 12

d1 = h.Auger('181214_A_01', datapath=path)
d1.info()
d1.plot()
d1.show()
