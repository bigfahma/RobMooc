from sympy import Matrix, simplify, cos ,sin,Symbol
from sympy.diffgeom import Manifold,Patch, CoordSystem,LieDerivative

def L(F,g,i=1):
    if i==1 : return LieDerivative(F,g)
    return L(F,L(F,g,i-1))

C = CoordSystem('C', Patch('P',Manifold('M',10)),[Symbol("x1"),Symbol("x2"),Symbol("x3"),Symbol("psi"),Symbol("vx"),Symbol("vy"),Symbol("vz"),Symbol("w"),Symbol("c1"),Symbol("b1")])
x1,x2,x3,psi,vx,vy,vz,w,c1,b1 = C.coord_functions()

E = C.base_vectors()

F = vx*E[0]+vy*E[1]+vz*E[2]+w*E[3]+(c1*cos(psi))*E[4] + (c1*sin(psi))*E[5]+b1*E[8]
G1,G2,G3 = E[9],E[7],E[6]

A = Matrix([[L(G1,L(F,x1,3)), L(G2,L(F,x1,3)), L(G3,L(F,x1,3))],
            [L(G1,L(F,x2,3)), L(G2,L(F,x2,3)), L(G3,L(F,x2,3))],
            [L(G1,L(F,x3,1)), L(G2,L(F,x3,1)), L(G3,L(F,x3,1))]])
print('A = ',simplify(A))

b = Matrix([[L(F,x1,4)],
            [L(F,x2,4)],
            [L(F,x3,2)]])

print('B =',simplify(b))