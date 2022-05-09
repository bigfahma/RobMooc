from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x,u):
    x,u  = x.flatten(), u.flatten()
    v,θ = x[2],x[3]    
    return array([[v*cos(θ)],[v*sin(θ)],[u[0]],[u[1]]])
    

def f1(x1,x2):  # Potential field
    Nq1 = (x1 -qhat[0,0]) ; Nq2 = (x2 -qhat[1,0])
    Vx =  x1 + vhat[0,0] - 2*(x1-phat[0,0]) + Nq1/(sqrt(Nq1**2 + Nq2**2))**3
    Vy= x2 + vhat[1,0] - 2*(x2 - phat[1,0]) + Nq2/(sqrt(Nq1**2 + Nq2**2))**3
    return Vx,Vy
    
def control(x,vdes,θdes):
    _,_,v,θ = x.flatten()
    u1 = K1*(vdes - v)
    u2 = K2*sawtooth(θdes - θ)
    u = array([[u1],[u2]])
    return u

def gradV(p):
    return -vhat + 2*(p-phat) - (p-qhat)/(norm(p-qhat)**3)

def potential_block(x):
    x1,x2,_,_ = x.flatten()
    p = array([[x1],[x2]])
    w = - gradV(p)
    vdes = norm(w)
    θdes =arctan2(w[1,0],w[0,0])
    return vdes,θdes
x    = array([[0,-3,0,2]]).T #x,y,v,θ
dt   = 0.05;Ts =30
s=5
ax=init_figure(-s,s,-s,s)

      
vhat = array([[1],[1]])     

K1 = 1
K2 = 5 # Gain for controller

u=array([[0],[0.3]])
for t in arange(0,Ts,dt):
    clear(ax)

    phat = array([[cos(t/10)],[2*sin    (t/10)]])
    qhat = array([[2*cos(t/5)],[2*sin(t/5)]])     

    draw_disk(ax,qhat,0.3,"magenta") # obstacle
    draw_disk(ax,phat,0.2,"green")   # goal

    vdes,θdes = potential_block(x)
    u = control(x,vdes,θdes)
    x=x+dt*f(x,u)    
    draw_tank(x[[0,1,3]],'red',0.2) # x,y,θ
    draw_field(ax,f1,-s,s,-s,s,0.4)

pause(1)    


