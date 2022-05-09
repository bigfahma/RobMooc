from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def draw(ap,aw): 
    aw=-aw-ap;
    c=2*array([-sin(ap),cos(ap)])
    plot( [0,c[0]],[0,c[1]],'magenta', linewidth = 2)
    for i in arange(0,8):
        plot(c[0]+array([0,cos(aw+i*pi/4)]),c[1]+array([0,sin(aw+i*pi/4)]),'blue')
    pause(0.01)
    

def f(x,u): 
    x=x.flatten()
    return array([[x[1]],[a1*sin(x[0])-b1*u],[-a1*sin(x[0])+c1*u]])

def control(x,yd):
    x1,x2,x3 = x[0:3,0]
    a_x = -b1*betha*cos(x1)
    b_x = betha*sin(x1)*(a1*cos(x1)-x2)
    y = c1*x2 + b1*x3
    ydot = betha*sin(x1)
    y2dot = betha*x2*cos(x1)
    v = (yd - y) + 3*(0-ydot)+ 3*(0-y2dot)
    return (-b_x + v)/a_x

a1,b1,c1=10,1,2
betha = a1*(c1-b1)
dt = 0.05
Ts = 10
x = array([[1],[0],[0]])
aw=0  # wheel angle
ax=init_figure(-3,3,-3,3)
x2_ref,x3_ref = 0,0.5 # angular velocity pendulum & disk setpoint
yd = c1*x2_ref + b1*x3_ref
for t in arange(0,Ts,dt) :
    u=control(x,yd)
    x=x+f(x,u)*dt
    aw=aw+dt*x[2]
    clear(ax)
    draw(x[0],aw)
