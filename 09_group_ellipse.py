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
    

ax=init_figure(-40,40,-40,40)
m   = 20
X   = 10*randn(4,m)
a,dt = 0.1,0.1
Ts = 20

for t in arange(0,Ts,dt):
    clear(ax)
    for i in range(m):  
        R = array([[cos(a*t), -sin(a*t)],[sin(a*t),cos(a*t)]])
        D = array([[20+15*sin(a*t),0],[0,10]])
        dR = a*array([[-sin(a*t),-cos(a*t)],[cos(a*t),-sin(a*t)]])
        dD = array([[15*a*cos(a*t),0],[0,0]])
        ddR = -a**2*R
        ddD = array([[-15*a*a*sin(a*t),0],[0,0]]) 

        c = array([[cos(a*t + 2*i*pi/m)],[sin(a*t+2*i*pi/m)]])
        dc = array([[-a*sin(a*t+2*i*pi/m)],[a*cos(a*t+2*i*pi/m)]])
        ddc =   array([[-a*a*cos(a*t + 2*i*pi/m)],[-a*a*sin(a*t+2*i*pi/m)]])

        w = R@D@c
        dw = R@D@dc + R@dD@c + dR@D@c
        ddw = R@D@ddc + R@ddD@c + ddR@D@c + 2*dR@D@dc + 2*R@dD@dc + 2*dR@dD@c
        x=X[:,i].reshape(4,1)
        u       = control(x,w,dw,ddw)
        x=X[:,i].reshape(4,1)
        draw_tank(x,'b',r=1)
        x=x+f(x,u)*dt        
        X[:,i]  = x.flatten()
        plot([w[0][0]],[w[1][0]],'r+')


