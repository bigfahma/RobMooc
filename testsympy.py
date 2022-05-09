from sympy import *
import numpy as np
x1=Symbol('x1') 
x2=Symbol('x2') 
d = Symbol('det')

L1,L2 = Symbol('L1'),Symbol('L2')
A = Matrix([[-L1*sin(x1) -L2*sin(x1+x2), -L2*sin(x1+x2)],
         [L1*cos(x1) + L2*cos(x1+x2), L2*cos(x1+x2)]])


d = det(A)
print(d)