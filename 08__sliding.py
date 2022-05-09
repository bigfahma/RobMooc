
from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

def f(x,u):
    x=x.flatten()
    u=u.flatten()
    return (array([[x[3]*cos(x[2])],     [x[3]*sin(x[2])],  [u[0]],[u[1]]]))
    
    
    
def control(x,w,dw,ddw):
    x1,x2,x3,x4 = x.flatten()
    dx1,dx2 = x4*cos(x3),x4*sin(x3)
    p = array([[x1],[x2]])
    dp = array([[dx1],[dx2]])
    v = array([(w-p) + 2*(dw-dp) + ddw])
    Ax = array([[-x4*sin(x3), cos(x3)],
                [x4*cos(x3), sin(x3)]])
    
    u = inv(Ax)@v
    return u 

def control_sliding(x,w,dw):
    x1,x2,x3,x4 = x.flatten()
    dx1,dx2 = x4*cos(x3),x4*sin(x3)
    p = array([[x1],[x2]])
    dp = array([[dx1],[dx2]])
    ddy = 100*sign(w-p + dw - dp)
    Ax = array([[-x4*sin(x3), cos(x3)],
                [x4*cos(x3), sin(x3)]])
    
    u = inv(Ax)@ddy
    return u   


ax=init_figure(-30,30,-30,30)
dt = 0.02
xFL = array([[10],[0],[1],[1]])
xSlid = array([[10],[0],[1],[1]])

L=10
s = arange(0,2*pi,0.01)
Ts = 10
abs_errorFL_list = []
error_xFL_list = []
error_yFL_list = []

abs_errorSlid_list = []
error_xSlid_list = []
error_ySlid_list = []
for t in arange(0,Ts,dt) :
  
    w=array([[L*cos(t)],[L*sin(3*t)]]) 
    dw=array([[-L*sin(t)],[3*L*cos(3*t)]])  
    ddw=array([[-L*cos(t)],[-9*L*sin(3*t)]]) 
    ############### Feedback linearization ##############
    u_FL=control(xFL,w,dw,ddw)
    xFL = xFL + dt*f(xFL,u_FL)
    x1FL,x2FL,_,_ = xFL.flatten()
    w1,w2 = w.flatten()
    pFL = array([[x1FL],[x2FL]])

    abs_errorFL = abs(w - pFL)
    error_xFL,error_yFL = abs_errorFL.flatten()
    error_xFL_list.append(error_xFL)
    error_yFL_list.append(error_yFL)
    abs_errorFL_list.append(abs(w1-x1FL)+abs(w2-x2FL))

    ############### SLIDING############
    u_Slid=control_sliding(xSlid,w,dw)
    xSlid = xSlid + dt*f(xSlid,u_Slid)
    x1Slid,x2Slid,_,_ = xSlid.flatten()
    pSlid = array([[x1Slid],[x2Slid]])
    abs_errorSlid = abs(w - pSlid)
    error_xSlid,error_ySlid = abs_errorSlid.flatten()
    error_xSlid_list.append(error_xSlid)
    error_ySlid_list.append(error_ySlid)
    abs_errorSlid_list.append(abs(w1-x1Slid)+abs(w2-x2Slid))

    clear(ax)
    draw_disk(ax,w,0.5,"black")
    plot(L*cos(s), L*sin(3*s),color='magenta')
    draw_tank(xFL,'red')
    draw_tank(xSlid,'blue')


ax1=init_figure(0,Ts,0,10)
T_list = arange(0,Ts,dt)
ax1.plot(T_list,error_xFL_list,label = 'X error FL')
ax1.plot(T_list,error_yFL_list, label = 'Y error FL')
ax1.plot(T_list, abs_errorFL_list, label = 'absolute error FL')
ax1.legend()


ax1.plot(T_list,error_xSlid_list,label = 'X error Slid')
ax1.plot(T_list,error_ySlid_list, label = 'Y error Slid')
ax1.plot(T_list, abs_errorSlid_list, label = 'absolute error Slid')
ax1.legend()
pause(100)




    

    



    
    
    

