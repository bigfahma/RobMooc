from tkinter import Y
from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x,u):
    xr,yr,θr,vr=x.flatten()
    u1,u2=u.flatten()
    return (array([[vr*cos(θr)],[vr*sin(θr)],[u1],[u2]]))



ax=init_figure(-30,30,-30,30)

Ts = 100
dt = 0.2
x = array([[0],[1],[pi/3],[1]])
v = array([[1],[1]])
u = array([[1],[1]])

w = 0.1
Lx,Ly = 15,7


def xahat(t):
    return Lx*sin(w*t)
def xahatdot(t):
    return Lx*w*cos(w*t)
def xahat2dot(t):
    return -Lx*w*w*sin(w*t)

def yahat(t):
    return Ly*cos(w*t)  
def yahatdot(t):
    return -Ly*w*sin(w*t)
def yahat2dot(t):
    return -Ly*w*w*cos(w*t) 

xa_list = []
ya_list = []

for t in arange(0,Ts,dt) :
    clear(ax)
    draw_tank(x)  

    xa,ya,θa,va=x.flatten()
    xadot,yadot,_,_ = f(x,u).flatten()
    u1,u2=u.flatten()
    A = array([[-va*sin(θa), cos(θa)],  [va*cos(θa), sin(θa)]])

    v1= (xahat(t) - xa) + 2*(xahatdot(t) - xadot) + xahat2dot(t)
    v2= (yahat(t) - ya) + 2*(yahatdot(t) - yadot) + yahat2dot(t)
    v = array([[v1],[v2]])
    u = inv(A)@v

    x = x+dt*f(x,u)

    xa_list.append(xa)
    ya_list.append(ya)

ax.plot(xa_list,ya_list)
pause(10)