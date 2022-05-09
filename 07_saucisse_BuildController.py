from roblib import *
from sympy import *
from sympy.diffgeom import *


def L(F,g,i=1):
    if i==1 : return LieDerivative(F,g)
    return L(F,L(F,g,i-1))

def w(t):
    return array([30*sin(0.1*t),10*cos(0.1*t), 10*(1+cos(0.3*t))])
    
def build_controller():
    C = CoordSystem('C', Patch('P',Manifold('M',10)),[Symbol("x1"),Symbol("x2"),Symbol("x3"),Symbol("psi"),Symbol("vx"),Symbol("vy"),Symbol("vz"),Symbol("w"),Symbol("c1"),Symbol("b1")])
    x1,x2,x3,psi,vx,vy,vz,w,c1,b1 = C.coord_functions()

    E = C.base_vectors()

    F = vx*E[0]+vy*E[1]+vz*E[2]+w*E[3]+(c1*cos(psi))*E[4] + (c1*sin(psi))*E[5]+b1*E[8]
    G1,G2,G3 = E[9],E[7],E[6]

    A = Matrix([[L(G1,L(F,x1,3)), L(G2,L(F,x1,3)), L(G3,L(F,x1,3))],
                [L(G1,L(F,x2,3)), L(G2,L(F,x2,3)), L(G3,L(F,x2,3))],
                [L(G1,L(F,x3,1)), L(G2,L(F,x3,1)), L(G3,L(F,x3,1))]])

    b = Matrix([[L(F,x1,4)],
                [L(F,x2,4)],
                [L(F,x3,2)]])
    print('A= ', simplify(A))
    print('b= ', simplify(b))

    t = symbols('t')
    w1,w2,w3 = 30*sin(0.1*t),10*cos(0.1*t),10*(1+cos(0.3*t))
    v1 = (w1-x1)+4*(diff(w1,t,1)-L(F,x1,1)) + 6*(diff(w1,t,2)- L(F,x1,2)) + 4*(diff(w1,t,3)-L(F,x1,3)) + diff(w1,t,4)
    v2 = (w2-x2)+4*(diff(w2,t,1)-L(F,x2,1)) + 6*(diff(w2,t,2)- L(F,x2,2)) + 4*(diff(w2,t,3)-L(F,x2,3)) + diff(w2,t,4)
    v3 = (w3-x3)+2*(diff(w3,t,1)-L(F,x3,1)) + diff(w3,t,2)
   
    a = A.inv()*(Matrix([[v1],[v2],[v3]])- b)
    print('a= ',simplify(a))

    p = lambdify((x1,x2,x3,psi,vx,vy,vz,w,c1,b1,t),a)
    return p

p = build_controller()
pause(10)