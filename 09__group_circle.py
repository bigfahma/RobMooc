from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py
from numpy import *


def f(x,u):
    x,u=x.flatten(),u.flatten()
    xdot = array([[x[3]*cos(x[2])],[x[3]*sin(x[2])],[u[0]],[u[1]]])
    return(xdot)

def control(x,w,dw,ddw):
    x1,x2,x3,x4 = x.flatten()
    dp = array([[x4*cos(x3)],[x4*sin(x3)]])
    p = array([[x1],[x2]])
    Ax = array([[-x4*sin(x3), cos(x3)],
                [x4*cos(x3), sin(x3)]])


    v = (w-p) + 2*(dw-dp) +ddw
    u= inv(Ax)@v
    return u    
    

ax=init_figure(-4,4,-4,4)
m   = 20
X   = 10*randn(4,m)
a,dt = 0.1,0.1
Ts = 20

for t in arange(0,Ts,dt):
    clear(ax)
    for i in range(m):        
        w = array([[cos(a*t + 2*i*pi/m)],[sin(a*t+2*i*pi/m)]])
        dw = array([[-a*sin(a*t+2*i*pi/m)],[a*cos(a*t+2*i*pi/m)]])
        ddw =   array([[-a*a*cos(a*t + 2*i*pi/m)],[-a*a*sin(a*t+2*i*pi/m)]])
        x=X[:,i].reshape(4,1)
        u       = control(x,w,dw,ddw)
        x=X[:,i].reshape(4,1)
        draw_tank(x,'b',r=0.1)
        x=x+f(x,u)*dt        
        X[:,i]  = x.flatten()
        plot([w[0][0]],[w[1][0]],'r+')


