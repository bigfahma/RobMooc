from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x,u):
    x = x.flatten()
    θ = x[2]
    return array([[cos(θ)],[sin(θ)],[u]])

def control(x):
    theta = x[2,0]
    theta_ = thetabar - theta

    #u= (theta_%(2*pi)) - pi # delta in [0,2*pi]
    u= ((theta_ + pi)%(2*pi)) - pi # delta in [-pi,pi]
    #u= (theta_%(2*pi)) - 2*pi # delta in [-2pi,0]

    return u
    
    
x   = array([[0],[0],[0]])
dt  = 0.05;Ts = 20
ax=init_figure(-20,20,-20,20)
thetabar = pi/2 + 10*pi
for t in arange(0,Ts,dt):
    clear(ax)
    u = control(x)
    x = x + dt*f(x,u)    
    draw_tank(x,'red',0.5) 
    
