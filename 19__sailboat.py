from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

         
    
def f(x,u):
    x,u=x.flatten(),u.flatten()
    θ=x[2]; v=x[3]; w=x[4]; δr=u[0]; δsmax=u[1];
    w_ap = array([[awind*cos(ψ-θ) - v],[awind*sin(ψ-θ)]])
    ψ_ap = angle(w_ap)
    a_ap=norm(w_ap)
    sigma = cos(ψ_ap) + cos(δsmax)
    if sigma < 0 :
        δs = pi + ψ_ap
    else :
        δs = -sign(sin(ψ_ap))*δsmax
    fr = p4*v*sin(δr)
    fs = p3*a_ap* sin(δs - ψ_ap)
    dx=v*cos(θ) + p0*awind*cos(ψ)
    dy=v*sin(θ) + p0*awind*sin(ψ)
    dv=(fs*sin(δs)-fr*sin(δr)-p1*v**2)/p8
    dw=(fs*(p5-p6*cos(δs)) - p7*fr*cos(δr) - p2*w*v)/p9
    xdot=array([ [dx],[dy],[w],[dv],[dw]])
    return xdot,δs    

    
def control(x,q):
    px,py,θ,v,w = x.flatten()
    m = array([[px],[py]])

    Matrix = np.hstack([(b-a/norm(b-a)), m-a])
    e = det(Matrix)
    phi = arctan2(b2-a2,b1-a1)
    if (abs(e)>r): q = sign(e)
    θbar = phi - arctan(e/r)
    if (cos(ψ -θbar) + cos(zeta)<0) : θbar = pi + ψ - zeta*q
    δr = (δrmax/pi) * sawtooth(θ - θbar)
    δsmax = (pi/4)*(cos(ψ-θbar) + 1)
    u = array([[δr],[δsmax]])
    return u,q 
    


    
    
p0,p1,p2,p3,p4,p5,p6,p7,p8,p9 = 0.1,1,6000,1000,2000,1,1,2,300,10000
x = array([[10,-20,1,1,0]]).T   #x=(x,y,θ,v,w)
zeta = pi/4
q = 1
dt = 0.1
Ts = 100
r = 10
δrmax = 1

awind,ψ = 2,-3 
a = array([[-50],[-100]])   
a1,a2 = a.flatten()
b = array([[50],[100]])
b1,b2 = b.flatten()
                  
ax=init_figure(-100,100,-60,60)

for t in arange(0,Ts,0.1):
    clear(ax)
    plot([a[0,0],b[0,0]],[a[1,0],b[1,0]],'red')
    u=array([[0],[1]])
    u,q = control(x,q)
    xdot,δs=f(x,u)
    x = x + dt*xdot
    draw_sailboat(x,δs,u[0,0],ψ,awind)


        