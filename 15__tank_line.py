from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(X,u):
    θ=X[2,0]
    return array([[cos(θ)], [sin(θ)],[u]])

X=array([[-20],[-10],[4]])
dt= 0.1
Ts = 20
a,b = array([[-30],[-4]]), array([[30],[6]])
a1,a2 = a.flatten()
b1,b2 = b.flatten()
ax=init_figure(-40,40,-40,40)

for t in arange(0,Ts,dt):
    x,y,theta = X.flatten()
    clear(ax)
    draw_tank(X,'darkblue')
    plot2D(hstack((a,b)),'red')
    plot2D(a,'ro')
    plot2D(b,'ro')    
    phi = arctan2(b2-a2,b1-a1)
    m = array([[x],[y]])
    array_e = np.hstack([b-a,m-a])
    e = det(array_e)/norm(b-a)
    theta_ref = phi - arctan(e)
    u = sawtooth(theta_ref-X[2,0])
    X   = X+dt*f(X,u)

    
    