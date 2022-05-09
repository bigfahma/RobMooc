from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py


def f(x,u):
    x=x.flatten()
    u=u.flatten()
    return array([[x[3]*cos(x[2])],[x[3]*sin(x[2])],[u[0]],[u[1]]])
        
def control (x,w,dw):
    x=x.flatten()
    A = array([[-x[3]*sin(x[2]), cos(x[2])],
                  [x[3]*cos(x[2]), sin(x[2])]])
    y = array([[x[0]],[x[1]]])
    dy = array([[x[3]*cos(x[2])],[x[3]*sin(x[2])]])

    print('A :',A)
    print('w',w)
    print('dw',dw)
    print('y',y)
    print('dy',dy)
 
    print('2nd term, ',((w - y) + 2*(dw - dy)))
    print('u', inv(A) @ ((w - y) + 2*(dw - dy)))
    return inv(A) @ ((w - y) + 2*(dw - dy))

def b_in(i,t,n):
    return (factorial(n)/(factorial(i)*factorial(n-i)))*((1-t)**(n-i))*(t**i)
    

def db_in(i,t,n):
    if (n==i) : return n*t**(n-1)
    elif (i==0) : return -n*(1-t)**(n-1)
    else :
        return (factorial(n)/(factorial(i)*factorial(n-i)))*(i*(1-t)**(n-i)*t**(i-1) -(n-i)*(1-t)**(n-i-1)*t**i)
def setpoint(t): 
    w = [0,0]
    for i in range(n+1): w = w + b_in(i,t,n)*P[:,i]
    w1,w2 = w
    return array([[w1],[w2]])

def dsetpoint(t): 
    dw = [0,0]
    for i in range(n+1): dw = dw + db_in(i,t,n)*P[:,i]
    dw1,dw2 =dw
    dw = array([[dw1],[dw2]])
    return dw*(1/tmax)
'''
def axplot2D(ax,M,col='black',w=1):
    ax.plot(M[0, :], M[1, :], col, linewidth = w) 

def ax_draw_tank(ax,x,col='darkblue',r=1,w=2):
    mx,my,θ=list(x[0:3,0])
    M = r*array([[1,-1,0,0,-1,-1,0,0,-1,1,0,0,3,3,0], [-2,-2,-2,-1,-1,1,1,2,2,2,2,1,0.5,-0.5,-1]])
    M=add1(M)
    axplot2D(ax,tran2H(mx,my)@rot2H(θ)@M,col,w)'''
    
P = array([[1,1,1,1,2, 3,4,5,4,8,10,8],
           [1,4,7,9,10,8,6,4,0,0,0,8]])
print('Poo', P[:,0])
n = len(P[0])-1

#plot(P[0], P[1], 'or')
dt = 0.1;tmax = 50
k=0

ax=init_figure(-1,11,-1,11)


A1=array([[2,0],[4,2],[2,7]])
A2=array([[7,2],[8,3],[3,10]])


x = array([[1,0,pi/4,1]]).T

draw_polygon(A1,ax,'green')
draw_polygon(A2,ax,'green')

for t in arange(0,tmax,dt):
    w = setpoint(t/tmax)
    dw = dsetpoint(t/tmax)

    u = control(x,w,dw)
    ax.plot(w[0],w[1], 'm.')
    x= x+f(x,u)*dt
    if k%10 == 0 : 
        draw_tank(x,'red',0.2)
        k = 0
    k+=1
    print(k)
    pause(0.01)

pause(10)
