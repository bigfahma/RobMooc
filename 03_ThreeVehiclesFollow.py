from tkinter import Y

from numpy import ubyte
from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x,u):
    xr,yr,θr,vr=x.flatten()
    u1,u2=u.flatten()
    return (array([[vr*cos(θr)],[vr*sin(θr)],[u1],[u2]]))



ax=init_figure(-30,30,-30,30)

Ts = 100
dt = 0.1
x_a = array([[10],[0],[1],[1]])
va = array([[0],[0]])
ua = array([[0],[0]])

x_b = array([[0],[0],[1],[2]])

x_c = array([[-10],[0],[1],[3]])

vb = array([[1],[1]])
ub = array([[1],[1]])

vc = array([[0],[0]])
uc = array([[0],[0]])
l = 6

w = 0.1
Lx,Ly = 15,7


def xahat(t): return Lx*sin(w*t)
def xahatdot(t): return Lx*w*cos(w*t)
def xahat2dot(t): return -Lx*w*w*sin(w*t)

def yahat(t): return Ly*cos(w*t)  
def yahatdot(t): return -Ly*w*sin(w*t)
def yahat2dot(t): return -Ly*w*w*cos(w*t) 

### Xb Hat###
def xbhat(t,θ): return xahat(t) - l*cos(θ)
def xbhatdot(t,θ,θdot) : return xahatdot(t) + l*θdot*sin(θ)
def xbhat2dot(t,θ,θdot): return xahat2dot(t) + l*θdot*θdot*cos(θ)

def ybhat(t,θ) : return yahat(t) - l*sin(θ)
def ybhatdot(t,θ,θdot) : return yahatdot(t) - l*θdot*cos(θ)
def ybhat2dot(t,θ,θdot): return yahat2dot(t) + l*θdot*θdot*sin(θ)

### XC Hat ####
def xchat(t,θ,θ_prev): return xbhat(t,θ_prev) - l*cos(θ)
def xchatdot(t,θ,θdot,θ_prev,θdot_prev) : return xbhatdot(t,θ_prev,θdot_prev) + l*θdot*sin(θ)
def xchat2dot(t,θ,θdot,θ_prev,θdot_prev): return xbhat2dot(t,θ_prev,θdot_prev) + l*θdot*θdot*cos(θ)

def ychat(t,θ,θ_prev) : return ybhat(t,θ_prev) - l*sin(θ)
def ychatdot(t,θ,θdot,θ_prev,θdot_prev) : return ybhatdot(t,θ_prev,θdot_prev) - l*θdot*cos(θ)
def ychat2dot(t,θ,θdot,θ_prev,θdot_prev): return ybhat2dot(t,θ_prev,θdot_prev) + l*θdot*θdot*sin(θ)


xa_list = []
ya_list = []

xb_list = []
yb_list = []

xc_list = []
yc_list = []
k = 0
for t in arange(0,Ts,dt) :
    k+=1
 
    xa,ya,θa,va=x_a.flatten()
    xb,yb,θb,vb=x_b.flatten()
    xc,yc,θc,vc=x_c.flatten()

    xadot,yadot,θadot,_ = f(x_a,ua).flatten()
    xbdot,ybdot,θbdot,_ = f(x_b,ub).flatten()
    xcdot,ycdot,θcdot,_ = f(x_c,uc).flatten()


    u1a,u2a=ua.flatten()
    u1b,u2b=ub.flatten()
    u1c,u2c=uc.flatten()


    A_a = array([[-va*sin(θa), cos(θa)],  [va*cos(θa), sin(θa)]])
    A_b = array([[-vb*sin(θb), cos(θb)],  [vb*cos(θb), sin(θb)]])
    A_c = array([[-vc*sin(θc), cos(θc)],  [vc*cos(θc), sin(θc)]])

    v1a= (xahat(t) - xa) + 2*(xahatdot(t) - xadot) + xahat2dot(t)
    v2a= (yahat(t) - ya) + 2*(yahatdot(t) - yadot) + yahat2dot(t)

    v1b= (xbhat(t,θa) - xb) + 2*(xbhatdot(t,θa,θadot) - xbdot) + xbhat2dot(t,θa,θadot)
    v2b= (ybhat(t,θa) - yb) + 2*(ybhatdot(t,θa,θadot) - ybdot) + ybhat2dot(t,θa,θadot)

    v1c= (xchat(t,θb,θa) - xc) + 2*(xchatdot(t,θb,θbdot,θa,θadot) - xcdot) + xchat2dot(t,θb,θbdot,θa,θadot)
    v2c= (ychat(t,θb,θa) - yc) + 2*(ychatdot(t,θb,θbdot,θa,θadot) - ycdot) + ychat2dot(t,θb,θbdot,θa,θadot)

    va = array([[v1a],[v2a]])
    vb = array([[v1b],[v2b]])
    vc = array([[v1c],[v2c]])

    ua = inv(A_a)@va
    ub = inv(A_b)@vb
    uc = inv(A_c)@vc


    x_a = x_a+dt*f(x_a,ua)
    x_b = x_b+dt*f(x_b,ub)
    x_c = x_c+dt*f(x_c,uc)
   
    if k >150 :         # to remove transient 
        clear(ax)
        draw_tank(x_a)  
        draw_tank(x_b,col = 'blue')  
        draw_tank(x_c, col = 'red') 

        xa_list.append(xa)
        ya_list.append(ya)

        xb_list.append(xb)
        yb_list.append(yb)

        xc_list.append(xc)
        yc_list.append(yc)

ax.plot(xa_list,ya_list)
ax.plot(xb_list,yb_list)
ax.plot(xc_list,yc_list)


pause(10)