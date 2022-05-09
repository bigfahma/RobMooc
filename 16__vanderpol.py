from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def vdp(x1,x2):  
    return x2,-(0.01*(x1**2)-1)*x2-x1
    
    
def f(x,u):
    mx,my,θ,v,δ =list(x[0:5,0])
    u1,u2=list(u[0:2,0])
    return array([[v*cos(δ)*cos(θ)],[v*cos(δ)*sin(θ)],[v*sin(δ)/L],[u1],[u2]])


x    = array([[0],[5],[pi/2],[30],[0.6]])
s=40
L,dt=3,0.03
Ts = 30
K_gain = 10
V0 = 10
ax=init_figure(-s,s,-s,s)
mx_list=[]
my_list =[]
count = 0
for t in arange(0,Ts,dt):
    mx,my,θ,v,δ =x.flatten()

    clear(ax)
    angle_vdp = angle(array([ my,-(0.01*(mx**2)-1)*my-mx]))
    w1,w2 = V0,angle_vdp
    ubar = array([[w1],[3*sawtooth(w2-θ)]])
    u=(ubar - array([[v*cos(δ)],[v*sin(δ)/L]]))*K_gain
    print(u.shape)
    x=x+dt*f(x,u)
    draw_field(ax,vdp,-s,s,-s,s,4)
    draw_car(x,L,2)
    mx_list.append(mx)
    my_list.append(my)
    if count == 150 :
        count = 0
        ax.scatter(mx_list,my_list,s = 0.5)
        pause(1)
    count +=1

pause(1)    



