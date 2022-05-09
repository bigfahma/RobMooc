from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def draw_pools(x,u):
    x=x.flatten()
    plot([0,0],[10,1],'black',linewidth=2)    
    plot([-7,23],[0,0],'black',linewidth=5)    
    plot([16,16],[1,10],'black',linewidth=2)    
    plot([4,4,6,6],[10,1,1,10],'black',linewidth=2)    
    plot([10,10,12,12],[10,1,1,10],'black',linewidth=2)    
    P=array([[0,x[0]],[0,1],[-6,0],[22,0],[16,1],[16,x[2]],[12,x[2]],[12,1]
            ,[10,1],[10,x[1]],[6,x[1]],[6,1],[4,1],[4,x[0]]])
    draw_polygon(P,ax,'blue')       
    P=array([[1,10],[1,x[0]],[1+0.1*u[0],x[0]],[1+0.1*u[0],10]])            
    draw_polygon(P,ax,'blue')
    P=array([[13,10],[13,x[2]],[13+0.1*u[1],x[2]],[13+0.1*u[1],10]])            
    draw_polygon(P,ax,'blue')

def alpha(h):
    return sign(h)*sqrt(2*g*abs(h))
def f(x,u):
    h1,h2,h3 = x[0,0],x[1,0],x[2,0]
    u1,u2 = u[0,0],u[1,0]
    h1dot = -alpha(h1) - alpha(h1-h2) + u1
    h2dot = alpha(h1-h2)- alpha(h2-h3)
    h3dot = -alpha(h3) + alpha(h2-h3) + u2

    return(array([[h1dot], [h2dot],[h3dot]]))

def b(x):
    h1,h2,h3 = x[0,0],x[1,0],x[2,0]
    return -alpha(h1) -alpha(h1 - h2), -alpha(h3) + alpha(h2-h3)

g = 9.81
dt = 0.05
x = array([[4],[5],[2]])
w = array([[2],[3]])
z1,z2 = 0,0
ax=init_figure(-10,25,-2,12)

for t in arange(0,20,dt) :
    clear(ax)
    y1,y2 = x[0,0],x[2,0] # outputs h1, h3
    z1dot,z2dot = (w[0,0] - y1), (w[1,0]-y2)
    z1,z2 = z1 + z1dot*dt, z2 + z2dot*dt

    v1 = z1 + 2*(w[0,0] - y1)
    v2 = z2 + 2*(w[1,0] - y2)
    b1,b2 = b(x)
    u1, u2 = v1 - b1, v2 -b2
    u = array([[u1],[u2]])
    x = x + dt*f(x,u)
    draw_pools(x,u)
    
  
