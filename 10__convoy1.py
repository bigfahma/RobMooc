
from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x,u):
    x,u=x.flatten(),u.flatten()
    xdot = array([[x[3]*cos(x[2])],[x[3]*sin(x[2])],
                  [u[0]],[u[1]]])
    return(xdot)

def control(x,w,dw,ddw):
    x,y,theta,v = x.flatten()
    p = array([[x],[y]])
    dp = array([[v*cos(theta)],[v*sin(theta)]])
    Ax = array([[-v*sin(theta), cos(theta)],[v*cos(theta),sin(theta)]])
    v = (w-p) + (dw - dp) + ddw
    u = inv(Ax)@v
    return u    
    
    
ax=init_figure(-30,30,-30,30)
xa  = array([[10],[0],[1],[1]])
m= 6
X=array([4*arange(0,m),zeros(m),ones(m),3*ones(m),zeros(m)])
Lx,Ly = 20,5
e   = np.linspace(0.,2*pi,30)
p   = array([[Lx*cos(e)],[Ly*sin(e)]])
S   = zeros((5,1))
dt  = 0.05
for t in arange(0,5,dt):
    clear(ax)
    wa  = array([[Lx*sin(0.1*t)],[Ly*cos(0.1*t)]])
    dwa = array([[Lx*0.1*cos(0.1*t)],[-Ly*0.1*sin(0.1*t)]]) 
    ddwa = -0.1*0.1*wa
    ua  = control(xa,wa,dwa,ddwa)    
    plot(wa[0][0],wa[1][0],'ro')
    plot(p[0][0],p[1][0])
    draw_tank(xa,'blue')
    xa  = xa + dt*f(xa,ua)
           
pause(1)


