from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def draw_field(ax,f,xmin,xmax,ymin,ymax,a):
    Mx    = arange(xmin,xmax,a)
    My    = arange(ymin,ymax,a)
    X1,X2 = meshgrid(Mx,My)
    VX,VY=fhat(X1,X2) 
    quiver(Mx,My,VX,VY)

def fhat(x1,x2):
    return cos(-arctan(x2)), sin(-arctan(x2)) 
    
def draw(x):
    draw_tank(x,'darkblue',0.3)
    a,b = array([[-30],[0]]), array([[30],[0]])
    draw_segment(a,b,'red',2)
    
def f(x,u):
    θ=x[2,0]
    return array([[cos(θ)], [sin(θ)],[u]])

def control(x):
    x1,x2,x3 = x.flatten()
    u = -x3 - arctan(x2)-sin(x3)/(1+x2**2)
    return u
           

x=array([[-2],[-2],[3]])
dt= 0.05
s=5

def f1(x1,x2):        
        return x2,-x1
 
ax=init_figure(-s,s,-s,s)


for t in arange(0,8,dt):
    clear(ax)
    draw(x)
    draw_field(ax,f1,-s,s,-s,s,1)

    u=control(x)
    x=x+dt*f(x,u)

