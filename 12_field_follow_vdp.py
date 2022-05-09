from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def draw_field(ax,f,xmin,xmax,ymin,ymax,a):
    Mx    = arange(xmin,xmax,a)
    My    = arange(ymin,ymax,a)
    X1,X2 = meshgrid(Mx,My)
    VX,VY=f(X1,X2) 
    R=sqrt(VX**2+VY**2)
    quiver(Mx,My,VX/R,VY/R)  

def vdp(x1,x2):
    return x2, -(0.01*(x1**2)-1)*x2 -x1    
def draw(x):
    draw_tank(x,'darkblue',0.3)
    a,b = array([[-30],[0]]), array([[30],[0]])
    draw_segment(a,b,'red',2)
    
def f(x,u):
    θ=x[2,0]
    return array([[cos(θ)], [sin(θ)],[u]])

def control(x):
    x1,x2,x3 = x.flatten()
    a,b = vdp(x1,x2)
    da = sin(x3)
    db = -0.02*x1*x2*cos(x3) - (0.01*x1**2-1)*sin(x3) - cos(x3)
    y = sawtooth(x3 - arctan2(b,a))
    bx  = (b*da - a*db)/(a**2+b**2)
    u = -y-bx
    return u
           

x=array([[-2],[-2],[3]])
dt= 0.05
Ts = 20
s=10
p = array([[-2],[-3]])
 
ax=init_figure(-s,s,-s,s)


for t in arange(0,Ts,dt):
    p1,p2 = p.flatten()
    
    dp1,dp2 = vdp(p1,p2)
    dp = array([[dp1],[dp2]])
    p = p + 0.5*dt*dp
    clear(ax)
    draw(x)
    draw_field(ax,vdp,-s,s,-s,s,1)
    ax.scatter(p1,p2)
    u=control(x)
    x=x+dt*f(x,u)