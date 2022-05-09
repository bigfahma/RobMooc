from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x,u):
    x=x.flatten()
    θ = x[2]
    return array([[cos(θ)], [sin(θ)], [u]])


def update_θdes(i,X):
    pi1,pi2  = X[0:2,i]
    pi = array([[pi1],[pi2]])
    k = 0
    for j in range(m):
        if i != j :
            thetaj = X[2,j]
            v= array([[cos(thetaj)],[sin(thetaj)]]) 
            θdes[:,k] = v[:,0] ; k+=1 # alignment
        
            pj1,pj2 = X[0:2,j]
            pj = array([[pj1],[pj2]])
            v = -alpha*(pi-pj) + betha*(pi-pj)/(norm(pi-pj)**3)    # attraction + separation
            v = v/norm(v)
            θdes[:,k] = v[:,0] ; k+=1




def control_i(xi,θdes_mean):
    θi = xi[2,0]
    ui = Kgain*sawtooth(angle(θdes_mean) - θi)
    return ui


ax=init_figure(-60,60,-60,60)
m   = 20
X   = 20*randn(3,m)
dt  = 0.2; Ts = 20




alpha,betha = 0.01,30
Kgain=1
for t in arange(0,Ts,dt):
    clear(ax)
    for i in range(m):
        xi=X[:,i].flatten()
        xi=xi.reshape(3,1)
        
        θdes = zeros((2,2*(m-1))) ; k =0
        update_θdes(i,X)
        θdes_mean = mean(θdes,1)
        ui = control_i(xi,θdes_mean)
        draw_tank(xi,'b')
        xi=xi+f(xi,ui)*dt       
        X[:,i]  = xi.flatten()        



