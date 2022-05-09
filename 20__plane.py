from pyrsistent import b
from regex import B
from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def draw(x,u,ax):
    x,u        = x.flatten(),u.flatten()
    plane    = array([[0,  0, 6, 0,  0, 0,   0,   1, 6, 0],
                      [0, -1, 0, 1, -1, 0,   0,   0, 0, 0],
                      [0,  0, 0, 0,  0, 0,   1, 0.2, 0, 0],
                      [1,  1, 1, 1,  1, 1,   1,   1, 1, 1]])
    e        = 0.5
    flap  = array([[-e,  0, 0, -e, -e],[-e, -e, e,  e, -e],
                      [ 0,  0, 0,  0,  0],[ 1,  1, 1,  1,  1]])
    
    R        = hstack((     eulermat(-x[3],-x[4],x[5]),
                            array([[x[0],x[1],-x[2]]]).T
                     ))
    R        = vstack((R,array([[0, 0, 0, 1]])))
    
    def draw_flap(ua,s):
        R1  = hstack((eulermat(0,ua,0),array([[0,s,0]]).T))
        R1  = vstack((R1,array([[0,0,0,1]])))
        flap1  = R @ R1 @ flap
        ax.plot(flap1[0,:],flap1[1,:],flap1[2,:],'red')    
        return
    
    plane    = R @ plane
    draw_flap(-u[1]+u[2],1-e)    #left flap
    draw_flap(-u[1]-u[2],e-1)    #right flap
    ax.plot(plane[0,:],plane[1,:],plane[2,:],'blue')          # drone
    ax.plot(plane[0,:],plane[1,:],0*plane[2,:],'black')       # ombre du drone
    ax.plot(Cx0,Cy0,Cz0,'green')                              # cercle consigne


def f(x,u):
    v     = x[6:9]
    w     = x[9:12]
    x,u=x.flatten(),u.flatten()
    V     = norm(v)
    α = arctan(x[8]/x[6])
    β  = arcsin(x[7]/V)
    φ,θ,ψ = x[3],x[4],x[5]
    cf,sf,ct,st,tt,ca,sa,cb,sb = cos(φ),sin(φ),cos(θ),sin(θ),tan(θ),cos(α),sin(α),cos(β),sin(β)
    Fa= 0.002*(V**2)*array([[-ca*cb,ca*sb,sa],[sb,cb,0],[-sa*cb,sa*sb,-ca]])  \
            @  \
            array([[4+(-0.3+10*α+10*w[1,0]/V+2*u[2]+0.3*u[1])**2+abs(u[1])+3*abs(u[2])],
                   [-50*β + 10*(w[2,0]-0.3*w[0,0])/V],
                   [10+500*α+400*w[1,0]/V+50*u[2]+10*u[1]]])
    
    return vstack((
                         eulermat(φ,θ,ψ) @ v,
                         eulerderivative(φ,θ,ψ)@ w,                  
                         9.81*array([[-st],[ct*sf],[ct*cf]])+Fa+array([[u[0]],[0],[0]]) - cross(w.T,v.T).T,
                         array([ -w[2]*w[1]+0.1*(V**2)*(-β -2*u[2]+(-5*w[0]+w[2])/V),
                                w[2]*w[0]+0.1*(V**2)*(-0.1-2*α+0.2*u[2]-3*u[1]-30*w[1]/V),
                                0.1*w[0]*w[1]+0.1*(V**2)*(β+0.5*u[2]+0.5*(w[0]-2*w[2])/V)])
                         ))


def control(x):
    x = x.flatten()
    px,py,z,φ,θ,ψ = x[0:6]
    θbar = -0.2*arctan(1/10*(zbar-z))
    ψbar = arctan2(py,px) + pi/2 + arctan(1/50*(sqrt(px**2 +py**2)-rbar))
    v = norm(x[7:9])
    u1 = 5*(1+2/pi*arctan(vbar - v)) # Domain : 5*[0,2]
    u2 = -0.3*((2/pi)*arctan(5*(θbar - θ))+abs(sin(φ))) # sin(phi) to compensate the rotation phi, 1/5rad = 11° linear zone
    φbar = 1/2*arctan(5*(arctan(tan((ψbar-ψ)/2)))) # [-pi,pi], arctan(tanθ)≡θmodπ.
    u3 = -0.3*((2/pi)*arctan(φbar-φ))

    u = array([[u1],[u2],[u3]])
    return u 
    
x    = array([[0, 0, -5, 0, 0, 0, 20, 0, 0, 0, 0, 0]]).T #[x;y;z;φ;θ;ψ;v;w]
dt   = 0.02
vbar,zbar,rbar = 15,-50,100  
a    = arange(0,2*pi+0.1, 0.1)
Cx0,Cy0,Cz0 = rbar*np.cos(a),rbar*np.sin(a),[-zbar]*len(a) #circle to follow

fig   = figure()
ax    = Axes3D(fig)
clean3D(ax,-100,100,-100,100,-100,100)

Ts = 50


θ_list = []
ψ_list = []

z_list = []
v_list = []
t_list = arange (0,Ts,dt)
k = 0
for t in arange (0,Ts,dt):
    u=control(x)
    x = x +dt*f(x,u)
    _,y,z,φ,θ,ψ = x[0:6]
    θ_list.append(θ)
    ψ_list.append(ψ)
    if (k%20==0):
        draw(x,u,ax)
    k+=1
    pause(0.01)

## plot
ax=init_figure(0,Ts,-5,5)
ax.plot(t_list,θ_list, color ='green',label = 'θ')

ax.plot(t_list,ψ_list, color ='blue',label = 'ψ')
plt.legend()
pause(20)
