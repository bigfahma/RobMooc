from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def clock_quadri(p,R,vr,wr,w):
    w2=w*abs(w)
    τ=B@w2.flatten()
    p=p+dt*R@vr      #R = eulermat(phi,theta,psi)
    vr=vr+dt*(-adjoint(wr)@vr+inv(R)@array([[0],[0],[g]])+array([[0],[0],[-τ[0]/m]]))
    # https://robotacademy.net.au/lesson/derivative-of-a-rotation-matrix/
    R=R@expm(adjoint(dt*wr))
    wr=wr+dt*(inv(I)@(-adjoint(wr)@I@wr+τ[1:4].reshape(3,1)))
    return p,R,vr,wr


def vdp(p):
    px,py,pz = p.flatten()
    return array([[py],[-(0.001*(px**2)-1)*py - px]])


def control(p,R,vr,wr):
    #https://en.wikipedia.org/wiki/Feed_forward_(control)
    x,y,z = p.flatten()
    dp = R@vr
    zd = -10
    vd = 10
    fd = vdp(p) #desired heading
    τd0 = Kpτ0*tanh(z-zd) + Kdτ0*vr[2,0]
    
    θd=-Kθ*tanh(vd-vr[0,0])
    ψd = angle(dp)
    error_ψd = angle(fd) - ψd
    φd = Kφ*tanh(Keψ*sawtooth(error_ψd))
    Rd = eulermat(φd,θd,ψd)
    # Block (c)
    S = KR*((Rd - R)@inv(R))
    wrd = adjoint_inv(S)
    ### 2nd method via conversion to euler angles
    #φ,θ,ψ = eulermat2angles(R)
    #wrd = KR*inv(eulerderivative(φ,θ,ψ))@array([[sawtooth(φd - φ)],[sawtooth(θd - θ)],[sawtooth(ψd - ψ)]])


    # Controller for Block (b)
    τd1_3 = I@((Kw*(wrd - wr)) + adjoint(wr)@I@wr)

    # inverse of block (a)
    w2 = inv(B)@vstack((τd0,τd1_3))
    w = sqrt(abs(w2))*sign(w2)
    return w

p = array([[0], [0], [-5]])  #x,y,z (front,right,down)
R = eulermat(0,0,0) # hover init
vr = array([[5], [0], [0]])
wr = array([[0], [0], [0]])
α=array([[0,0,0,0]]).T #angles for the blades

Kw = 100 # Gain for Controller (b)
KR = 5 # Gain for controller(c)
Kpτ0 = 300; Kdτ0 = 60 # Gain for controller (d)
Kθ = 0.3 
Keψ,Kφ = 10,0.5  # Gains for controller(e),Keψ for the precision
fig = figure()
ax = Axes3D(fig)

m,g,b,d,l=10,9.81,2,1,1
I=array([[10,0,0],[0,10,0],[0,0,20]])
dt = 0.01;Ts=20
B=array([[b,b,b,b],[-b*l,0,b*l,0],[0,-b*l,0,b*l],[-d,d,-d,d]])

for t in arange(0,Ts,dt):
    w=control(p, R, vr, wr)
    p, R, vr, wr = clock_quadri(p, R, vr, wr, w)
    clean3D(ax, -25, 25, -25, 25, 0, 25)
    print('z:',p[2,0])
    draw_quadrotor3D(ax, p, R, α, 5 * l)
    α = α + dt * 30 * w
    pause(0.001)
pause(1)







'''
def f(X,W):
    X = X.flatten()
    x,y,z,phi,theta,psi = X[0:6]
    vr = (X[6:9]).reshape(3,1)
    wr = (X[9:12]).reshape(3,1)
    W2 = W*abs(W)
    tau = B@W2.flatten()
    E = eulermat(phi,theta,psi)
    dvr = -adjoint(wr)@vr+inv(R)@array([[0],[0],[g]])+array([[0],[0],[-tau[0]/m]])
    dp =  E@vr
    dangles = eulerderivative(phi,theta,psi)@wr
    dwr = inv(I)@(-adjoint(wr)@I@wr+tau[1:4].reshape(3,1))
    dX = vstack([dp,dangles,dvr,dwr])
    return dX'''