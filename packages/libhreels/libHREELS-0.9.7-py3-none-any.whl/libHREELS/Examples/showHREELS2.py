from libHREELS import HREELS 

d = './data'
d = './Examples/data'

file = "c1a03"
factor = 20
xmin = 35

d1 = HREELS(file,d)
d1.plotInfoAmp(factor=factor, xmin=xmin)
d1.pickPeak()
d1.show()
