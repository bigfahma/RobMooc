from numpy import float64
from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def draw_crank(ax,x): 
    clear(ax)
    θ1=x[0,0]
    θ2=x[1,0]
    z=L1*array([[cos(θ1)],[sin(θ1)]])
    y=z+L2*array([[cos(θ1+θ2)],[sin(θ1+θ2)]])
    plot( [0,z[0,0],y[0,0]],[0,z[1,0],y[1,0]],'magenta', linewidth = 2)   
    draw_disk(ax,c,r,"cyan")


L1,L2 = 4,3
c = array([[1],[2]])
r=4
dt = 0.05

x = array([[-1],[1]])
Ts = 10

def f(x):
    θ1=x[0,0]
    θ2=x[1,0]
    dθ1=1
    dθ2=2
    return(array([[dθ1],[dθ2]]))
    

ax=init_figure(-4,8,-4,8)

for t in arange(0,Ts,dt) :
    draw_crank(ax,x)

    θ1=x[0,0]
    θ2=x[1,0]
    z=L1*array([[cos(θ1)],[sin(θ1)]], dtype=  float64)
    y=z+L2*array([[cos(θ1+θ2)],[sin(θ1+θ2)]], dtype = float64)
    w = c + r*array([[cos(t)], [sin(t)]], dtype = float64)
    dw = r*array([[-sin(t)],[cos(t)]],dtype = float64)

    v = w - y +dw
    A = [[-L1*sin(x[0,0]) -L2*sin(x[0,0] + x[1,0]), -L2*sin(x[0,0]+ x[1,0])],
         [L1*cos(x[0,0]) + L2*cos(x[0,0]+x[1,0]), L2*cos(x[0,0]+x[1,0])]]
    u = inv(A)@v
     
    x = x + dt*u  

