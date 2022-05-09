from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def phi0(x1,x2):        
    return -(x1**3+x2**2*x1-x1+x2),-(x2**3+x1**2*x2-x1-x2)

def phi(p1,p2):
    D_ = inv(D)
    z1 = D_[0,0]*(p1-c1) + D_[0,1]*(p2-c2)
    z2 = D_[1,0]*(p1-c1) + D_[1,1]*(p2-c2)
    w1,w2 = phi0(z1,z2)
    v1 = D[0,0]*w1 + D[0,1]*w2
    v2 = D[1,0]*w1 + D[1,1]*w2
    return v1,v2

def Jphi0(p):
    p1,p2 = p.flatten()
    return array([[-3*p1**2-p2**2+1,-2*p1*p2-1],[-2*p1*p2+1,-4*p2**2+1]])

def dphi(x):
    p1,p2,theta = x.flatten()
    z = inv(D)@array([[p1-c1],[p2-c2]])
    dv = D@Jphi0(z)@inv(D)@array([[cos(theta)],[sin(theta)]])
    return dv.flatten()

def f(x,u):
    theta = x[2,0]
    return array([[cos(theta)],[sin(theta)],[u]])

def control(x):
    da,db = dphi(x)
    x1,x2,x3 = x.flatten()
    a,b = phi(x1,x2)
    u = -sawtooth(x3 - arctan2(b,a)) -(b*da-a*db)/(a**2+b**2)
    return u 



xmin,xmax,ymin,ymax=-4.5,4.5,-4.5,4.5 
ax=init_figure(xmin,xmax,ymin,ymax)
dt=0.1;Ts =50
x=array([[-2],[-3],[1]])
q = 0
for t in arange(0,Ts,dt):
    clear(ax)
    if (q == 0): 
        c1,c2,r,eps = 2,0,2,1
        draw_tank(x,'blue',0.1,2)
    if (q == 1): 
        c1,c2,r,eps = 2,0,2,1
        draw_tank(x,'red',0.1,2)
    if (q == 2): 
        c1,c2,r,eps = -2,0,2,-1
        draw_tank(x,'green',0.1,2)
    if (q == 3): 
        c1,c2,r,eps = -2,0,2,-1
        draw_tank(x,'magenta',0.1,2)

    D = array([[r,0],[0,r*eps]])
    x1,x2,_ = x.flatten()
    if ((q%2==0) &(x2>0.5)) | ((q%2==1)&(x2<0)) : 
        q = (q+1)%4

    u = control(x)
    x = x + dt*f(x,u)
    draw_field(ax,phi,xmin,xmax,ymin,ymax,0.5)    