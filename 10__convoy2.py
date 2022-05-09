
from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x,u):
    x,u=x.flatten(),u.flatten()
    xdot = array([[x[3]*cos(x[2])],[x[3]*sin(x[2])],
                  [u[0]],[u[1]],[x[3]]])
    return(xdot)

def control(x,w,dw):
    x,y,theta,v,s = x.flatten()
    p = array([[x],[y]])
    dp = array([[v*cos(theta)],[v*sin(theta)]])
    Ax = array([[-v*sin(theta), cos(theta)],[v*cos(theta),sin(theta)]])
    v = (w-p) + (dw - dp) 
    u = inv(Ax)@v
    return u   
    
ax=init_figure(-30,30,-30,30)
xa  = array([[10],[0],[1],[1],[0]])
m= 6
X=array([4*arange(0,m),zeros(m),ones(m),3*ones(m),zeros(m)])

Lx,Ly = 20,5
e   = np.linspace(0.,2*pi,30)
p   = array([[Lx*cos(e)],[Ly*sin(e)]])
ds = 0.1
dt  = 0.03
d = 5
count = 0
Ts = 20
S = array([[0],[0],[0],[0],[0]])
for t in arange(0,Ts,dt):
    clear(ax)
    wa  = array([[Lx*sin(0.1*t)],[Ly*cos(0.1*t)]])
    dwa = array([[Lx*0.1*cos(0.1*t)],[-Ly*0.1*sin(0.1*t)]]) 
    ua  = control(xa,wa,dwa)    
    plot(wa[0][0],wa[1][0],'ro')
    plot(p[0][0],p[1][0])
    draw_tank(xa,'blue')
    xa  = xa + dt*f(xa,ua)
    xa_x,xa_y,xa_theta,xa_v,s = xa.flatten()
    if xa[4][0] > ds:
            xa[4,0] = 0
            S = np.hstack([S,xa])
    

    for i in range(m):
        j = int(size(S,1) - d*i/ds)
        if j >0 :
            xai = S[:,j-1]
            wi = array([[xai[0]],[xai[1]]])
            dwi = xa[4,0]*array([[cos(xai[3])] , [sin(xai[3])]])
            ui = control(X[:,i],wi,dwi)


        else : ui = array([0.2,0])

        x=X[:,i].reshape(5,1)
        draw_tank(x,'black')
        x=x+f(x,ui)*dt        
        X[:,i]  = x.flatten()            
pause(1)


