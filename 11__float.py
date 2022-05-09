from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def draw_buoy(x):
    clear(ax) 
    x=x.flatten()
    plot([-10,10],[0,0],'black',linewidth=1)    
    d=x[0]
    P=array([[-ech,-1.8*ech],[ech,-1.8*ech],[ech,0],[-ech,0]])
    draw_polygon(P,ax,'blue')    
    plot([   0,   L,  L,  L/2,   L/2,   L/2,  0,  0],
         [-L-d,-L-d, -d,   -d,   2-d,    -d, -d,-L-d],'black',linewidth=3)
    b=-x[2]     
    P=array([[0,-L-d+L],[L,-L-d+L],[L,-L/2-L*b/2-d],[0,-L/2-L*b/2-d]])
    draw_polygon(P,ax,'white') 
    #plot([-ech,ech],[-depth_des, -depth_des],'red',linewidth = 1)
    plot([-ech,ech],[-w_sin, -w_sin],'red',linewidth = 1)

def f(x,u):
    d,v,b= x.flatten()      
    p,g,cx = 1000,9.81,1.05
    dv = g - (g*max(0,L+min(d,0)) + v*abs(v)*cx/2)/(1+0.1*b)
    #dv = g no friction
    return array([[v],[dv],[u]])

def control(x,depth_des,depth_desdot,depth_des2dot):
    d,v,b= x.flatten()
    s = depth_des2dot - (g-(g*L+0.5*v*abs(v)*cx)/((1+0.1*b)*L)) + 2 * (depth_desdot-v) +(depth_des - d) 
    u = sign(s)
    return u 
p,g,cx = 1000,9.81,1.05
    
       
ech=5
x = array([[3],[0],[0]])
L=1 #length of the cube
ax=init_figure(-ech,ech,-1.8*ech,0.2*ech)
Ts = 20
dt = 0.1

for t in arange(0,Ts,dt):
    depth_des = 5 # 5meter
    depth_desdot = 0
    depth_des2dot  =0

    w_sin = 3 + sin(t/2) #setpoint sinus
    dw_sin = 0.5*cos(t/2)
    ddw_sin = -0.5**2*sin(t/2)
    #u =control(x,depth_des, depth_desdot, depth_des2dot)
    u = control(x,w_sin,dw_sin,ddw_sin)
    x=  x + dt*f(x,u)
    print(x[2])
    if abs(x[2])>1 : x[2]=sign(x[2]) # clamping
    draw_buoy(x)
pause(3)

