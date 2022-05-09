from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x,u):
    x1,x2,x3,x4 = x.flatten()
    n3 = (x1**2 +x2**2)**1.5
    v3 = (-x1/n3) + u*x3
    v4 = (-x2/n3) + u*x4
    return array([[x3],[x4],[v3],[v4]])

def control(x):
    x1,x2,x3,x4 = x.flatten()
    e1 = x1**2+x2**2-R**2 # error wrt potential energy
    e2 = x1*x3 + x2*x4  # error wrt to derivative of potential energy
    e3 = x3**2 + x4**2 -1/R # error wrt to kinetic energy
    u = ke1*e1 + ke2*e2 + ke3*e3
    return u

R = 1
s=2
ax=init_figure(-s,s,-s,s)
clear(ax)
draw_disk(ax,array([[0],[0]]),R,"black",0.1,4)

draw_disk(ax,array([[0],[0]]),0.2,"blue",1,1)

x=array([[1.22],[0],[0],[1]]) #x,y,vx,vy
draw_disk(ax,array([[x[0]],[x[1]]]),0.1,"red",1)
dt = 0.1;Ts = 50
ke1,ke2,ke3 = -1,-5,-1 # <0 to decrease the energies
for t in arange(0,Ts,dt):
    u = control(x)
    x = x + dt*(0.25*f(x,u) + 0.75*(f(x+dt*(2/3)*f(x,u),u)))
    ax.scatter(x[0],x[1], color = 'red',s=0.5)
    pause(0.01)

pause(1)    





 
