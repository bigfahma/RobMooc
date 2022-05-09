from numpy import float64
from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def draw(x,col):
    θ = x[0]/r
    a=array([[r*cos(θ)],[r*sin(θ)],[θ+pi/2]])
    draw_tank(a,col)

def circular_dist(xa,xb):
    dx = xb - xa
    return r*(sawtooth(dx[0,0]/r-pi)+pi)

def xi(X,i):
    return (X[:,i%m].flatten()).reshape(2,1)

def gi(xa,xb):
    dx = xb - xa
    return array([[circular_dist(xa,xb)],[dx[1,0]]])

def f(xa,u):
    xa= xa.flatten()  
    return array([[xa[1]],[u]])

def control(xa,y):
    y = y.flatten()
    dtheta = L/m
    v0 =10
    u = Kp*(y[0]-dtheta) + Kd*y[1] + Kv*(v0-xa[1])
    return u[0]

Kp =1;Kd=1;Kv=1
v0 = 10
m=10
X = zeros([2,m])  
L=100
r=L/(2*pi)

for i in range(m): X[0,i] = -8*i

dt = 0.05;Ts= 10

ax=init_figure(-20,20,-20,20)

for t in arange(0,Ts,dt):
    clear(ax)
    draw_disk(ax,array([[0],[0]]),r+3,'lightblue')
    draw_disk(ax,array([[0],[0]]),r-3,'white')
    for i in range(m):
        xa=xi(X,i)
        xb = xi(X,i-1)
        yi = gi(xa,xb)
        print('yi:',yi)
        ua = control(xa,yi)
        print('ua:',ua)
        xa = xa + f(xa,ua)*dt
        print('xa:',xa)
        draw(xa,'black')
        if circular_dist(xa,xb) < 5:
            xa[1,0] = 0 #collision
            draw(xa,'red')
        print('X i%m',X[:,i%m].shape)
        X[:,i%m] = xa.flatten()


