from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py
from sympy import Symbol, symbols,Matrix,lambdify,cos,sin
from sympy.diffgeom import *


def L(F,g,i=1):
    if size(g)==2: return Matrix([[L(F,g[0],i)],[L(F,g[1],i)]])
    if i==1: return LieDerivative(F,g)
    return L(F,L(F,g,i-1))
    
def ψ(x1,x2): return x2,-(1*(x1**2)-1)*x2-x1    

def build_p_phi():
    C=CoordSystem('C',Patch('P',Manifold('M',5)),[Symbol("x1"),Symbol("x2"),Symbol("x3"),Symbol("x4"),Symbol("x5")])
    x1,x2,x3,x4,x5 = C.coord_functions()
    E = C.base_vectors() 
    v1,a2 = symbols("v1 a2")
    Fx = x5*cos(x3)*E[0] + x5*sin(x3)*E[1] + x5*sin(x3-x4)*E[3]
    Gx1,Gx2 = E[2],E[4]
    Hx1,Hx2 = x1-cos(x4),x2-sin(x4)
    z3 = x5*cos(x3-x4)
    A = Matrix([[L(Gx1,z3),L(Gx2,z3)],[L(Gx1,L(Fx,x4)), L(Gx2,L(Fx,x4))]])
    print('A =',A)
    b = Matrix([L(Fx,z3),L(Fx,x4,2)])
    print('b =',b)
    u = A.inv()*(Matrix([v1,a2])-b)
    p = lambdify((x1,x2,x3,x4,x5,v1,a2),u)
    z = Matrix([Hx1,Hx2,z3,v1,x4,x5*sin(x3-x4)])
    phi = lambdify((x1,x2,x3,x4,x5,v1),z)
    return p,phi

def build_betha():
    C=CoordSystem('C',Patch('P',Manifold('M',6)),[Symbol("z1"),Symbol("z2"),Symbol("z3"),Symbol("z4"),Symbol("z5"),Symbol("z6")])
    z1,z2,z3,z4,z5,z6 = C.coord_functions()
    E = C.base_vectors() 
    Fz = z3*cos(z5)*E[0] + z3*sin(z5)*E[1] + z4*E[2] + z6*E[4]
    Gz1,Gz2 = E[3],E[5]
    Hz = Matrix([z1,z2])
    e = L(Fz,Hz) - Matrix(ψ(z1,z2))
    de = L(Fz,Hz,2)- L(Fz,ψ(z1,z2))
    Lgz = L(Gz1,L(Fz,Hz,2)).row_join(L(Gz2,L(Fz,Hz,2)))

    betha = lambdify((z1,z2,z3,z4,z5,z6),-Lgz.inv()*(L(Fz,Hz,3)-L(Fz,ψ(z1,z2),2)+e+2*de))

    return betha


x = np.array([[0.0],[0.0],[0.0],[0.0],[1.0]])
sc=3
x1,x2,x3,x4,x5 = x.flatten()  
v1,a2 = 1,2
p,phi = build_p_phi() 
betha= build_betha()
dt = 0.02
ax=init_figure(-sc,sc,-sc,sc)

for k in range(0,2000):
    clear(ax)
    x1,x2,x3,x4,x5 = x.flatten() 
    draw_field(ax,ψ,-sc,sc,-sc,sc,0.3)
    draw_tank_trailer(x1,x2,x3,x4,x5);
    z = phi(x1,x2,x3,x4,x5,v1)
    a = betha(*z)
    a1,a2 = a.flatten()
    v1 = v1 + a1*dt
    u = p(x1,x2,x3,x4,x5,v1,a2)
    u1,u2 = u.flatten()
    x =  x + array([[x5*np.cos(x3)],[x5*np.sin(x3)],[u1],[x5*np.sin(x3-x4)],[u2]])*dt



