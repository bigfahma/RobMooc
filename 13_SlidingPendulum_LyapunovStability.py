from pyibex import Function,SepFwdBwd,IntervalVector,pySIVIA
from vibes import vibes
from roblib import *

f1 = Function("x1","x2","(x2+x1)*(-5*sign(x1+x2)+x2)")
S1 = SepFwdBwd(f1,[0,10000])

vibes.beginDrawing()
vibes.newFigure('sliding')
vibes.setFigureSize(1000,1000)

P = IntervalVector([[-12,12],[-12,12]])
pySIVIA(P,S1,0.1)
vibes.axisEqual()
