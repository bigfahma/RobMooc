from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def draw_rob(x,col):
    x = x.flatten()
    lx,ly,ψ = x[0],x[1],x[2]
    R = Rlatlong(lx,ly) @ eulermat(0,0,ψ)
    draw_robot3D(ax,latlong2cart(ρ,lx,ly),R,col,1) 
    
def f(x,u):
    x = x.flatten()
    lx,ly,ψ = x[0],x[1],x[2]
    return array([[cos(ψ)/(ρ*cos(ly))], [sin(ψ)/ρ], [u]])

def control(x,xa):
    lx,ly,ψ = xa.flatten()
    dx = x - xa
    print(dx)
    A = array([[cos(ψ), dx[0,0]*cos(ly)],[sin(ψ),dx[1,0]]])
    ua = det(A)
    return ua
ρ = 30 
ax = Axes3D(figure())  
x   = array([[-0.5],[0],[0.3]])
xa   = array([[-1],[0],[0.5]])

dt = 0.1;Ts = 50

for t in arange(0,Ts,dt):
    clean3D(ax,-ρ,ρ,-ρ,ρ,-ρ,ρ)
    draw_earth3D(ax,ρ,eye(3),'gray')    
    u = 0.1 * randn(1) [0]
    x = x + dt*f(x,u) # robot to follow

    ua = control(x,xa)
    xa = xa + dt*f(xa,ua)   
     
    draw_rob(x,"blue")
    draw_rob(xa,'red')

pause(1)
