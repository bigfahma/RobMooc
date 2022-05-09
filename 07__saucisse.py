from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

from sympy import *
from sympy.diffgeom import *       

def f(x,u):  # x,y,z,ψ,vx,vy,vz,w
    x1,x2,x3,ψ,vx,vy,vz,ω=x[0:8,0]
    u1,u2,u3=u[0:3,0]
    return np.array([[vx],[vy],[vz],[ω],[u1*np.cos(ψ)],[u1*np.sin(ψ)],[u3],[u2]])

def draw(x,w1,w2,w3):
    x1,x2,x3,ψ,vx,vy,vz,ω=x[0:8,0]
    u1,u2,u3=u[0:3,0]
    clean3D(ax,-30,30,-30,30,0,60)
    draw_axis3D(ax,0,0,0,np.eye(3,3),10)
    R=eulermat(0,0,ψ)
    M=tran3H(x1,x2,x3)@eulerH(0,0,ψ) @ auv3H()
    draw3H(ax,M,'blue',True)
    U1=5*R@np.array([[u1],[0],[0]])
    draw_arrow3D(ax,x1,x2,x3,*U1[0:3,0],"red")
    U2=5*R@np.array([[0],[0],[u2]])
    draw_arrow3D(ax,x1,x2,x3,*U2[0:3,0],"green")
    U3=5*R@np.array([[0],[0],[u3]])
    draw_arrow3D(ax,x1,x2,x3,*U3[0:3,0],"red")
    ax.scatter(w1,w2,w3,color='magenta')  #target
    pause(0.001)

def L(F,g,i=1):
    if i==1 : return LieDerivative(F,g)
    return L(F,L(F,g,i-1))

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
def w(t):
    return 30*sin(0.1*t),10*cos(0.1*t),10*(1+cos(0.3*t))

ax = Axes3D(figure())    
x = np.array([[0],[0],[0],[0],[1],[0],[0],[0]])
dt = 0.05
Ts = 100
c1,b1=0.1,0.1   
controller_fct = build_controller() 
for t in arange(0,Ts,dt):
    x1,x2,x3,ψ,vx,vy,vz,ω=x[0:8,0]
    if c1<0.1 : c1=0.1
    a = controller_fct(x1,x2,x3,ψ,vx,vy,vz,ω,c1,b1,t)
    a1,a2,a3 = a[0:3,0]

    u=np.array([[c1],[a2],[a3]])    
    x = x + dt * f(x,u)
    c1 = c1 + b1*dt
    b1 = b1 + a1*dt
    draw(x,*w(t))
        
pause(1)
    
