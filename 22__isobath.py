#https://www.ensta-bretagne.fr/jaulin/robmooc.html
from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

        
def h(x,y):
    return 2*exp(-((x+2)**2+(y+2)**2)/10) + 2*exp(-((x-2)**2+(y-2)**2)/10) - 10


def draw_mesh():
    Mx=arange(-L,L,1.5)
    X,Y = meshgrid(Mx,Mx)
    H = h(X,Y)
    ax.plot_surface(X,Y,H)
    #ax.contour(X,Y,H)
    return()

def f(x,u):
    x,u = x.flatten(),u.flatten()
    psi = x[3]
    return array([[cos(psi)],[sin(psi)],[u[0]],[u[1]] ])

def gradh(x,y):
    delta = 0.1
    return array([(h(x+delta,y)-h(x,y))/delta, (h(x,y+delta)-h(x,y))/delta])

def g(x): #observer
    x,y,z,psi = x.flatten()    
    return array([[z-h(x,y)],[angle(gradh(x,y)) -psi],[-z]])

def control(y):
    y1,y2,y3 = y.flatten()
    u1 = Ky3*tanh((y3 -y3d))
    u2 = tanh(-h0d - y3 - y1) + sawtooth(y2+ pi/2) # the 1st term is to go to the desired isobare, and the 2nd is to follow it
                                                   # by keeping the angle of the gradient of h(x,y) = -PI/2
    return array([[u1],[u2]])


def draw_auv3D(ax,x,y,z,φ,θ,ψ,col='blue',size=1):
    ax.set_xlim3d(-L,L); ax.set_ylim3d(-L,L); ax.set_zlim3d(-L,0)
    draw_robot3D(ax,array([[x],[y],[z]]),eulermat(φ,θ,ψ),col,size)

def draw_uav(x):
    clean3D(ax, -L,L, -L, L, -L, 0)
    x,y,z,ψ = x.flatten()
    draw_mesh()
    draw_auv3D(ax,x,y,z,0,0,ψ,col='blue',size=0.1)
    draw_auv3D(ax,x,y,h(x,y),0,0,ψ,col='black',size=0.1)
    return()

L=10 #size of the world   
ax = axis3D(-L,L, -L, L, -L, 0)
x    = array([[2,-1,-1,0]]).T #x,y,z,ψ

dt= 0.1; Ts = 20
Ky3 = 2


for t in arange(0,Ts,dt):
    h0d = -9
    y3d = 2
    y = g(x)    
    u = control(y)
    x = x + dt*f(x,u)
    draw_uav(x)
    pause(0.01)

pause(2)     
