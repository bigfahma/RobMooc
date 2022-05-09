from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x,u):
    x=x.flatten()
    u=u.flatten()
    return (array([[u[0]*cos(x[2])], [u[0]*sin(x[2])],[u[1]]]))

def control(s,v):
    x,y,theta = s.flatten()
    v1,v2 = v.flatten()
    Ax = array([[-1,y],[0,-x]])
    bx = array([[v1*cos(theta)],[v1*sin(theta)]])
    
    v = array([[w1-x],[w2-y]])
    u = inv(Ax)@(v-bx)
    return u    

ax=init_figure(-30,30,-30,30)
dt = 0.1
Ts = 50
w1,w2 = 10,0 # at 10m, pointing directly

xa = array([[-10], [-10],[0]])
xb = array([[-5],[-5],[0]])


for t in arange(0,Ts,dt) :
    clear(ax)

    x1,y1,theta1 = xa.flatten()
    x2,y2,theta2 = xb.flatten()


                
    x = array([[cos(theta1), sin(theta1), 0],
               [-sin(theta1), cos(theta1), 0],
               [0,0,1]])@array([[x2-x1],
                                [y2-y1],
                                [theta2 - theta1]])

    v = array([[3],[sin(0.2*t)]])
    u=control(x,v)
    draw_tank(xa,'blue')  	
    draw_tank(xb,'red')  	
    xa = xa + dt*f(xa,u)
    xb = xb + dt*f(xb,v)
#show()


    
