from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x,u):
    x    = x.flatten()
    return array([[5*cos(x[2])],[5*sin(x[2])],[u]])


def control(x):
    px,py,theta = x.flatten()
    alpha = arctan2(py,px)
    phi = pi + theta - alpha
    if cos(phi)<= 1/sqrt(2) : u = 1
    else : u = -sin(phi)

    return u

x1    = array([[15],[20],[1]])
x2    = array([[-15],[20],[2]])
x3    = array([[15],[-20],[0]])

dt   = 0.1
Ts = 20
ax=init_figure(-30,30,-30,30)
for t in arange(0,Ts,dt):
    clear(ax)
    draw_disk(ax,array([[0],[0]]),10,'cyan')

    draw_tank(x1,'red')
    u1 = control(x1)
    x1 = x1+dt*f(x1,u1)   

    draw_tank(x2,'blue')
    u2 = control(x2)
    x2 = x2+dt*f(x2,u2)

    draw_tank(x3,'black')
    u3 = control(x3)
    x3 = x3+dt*f(x3,u3)      



