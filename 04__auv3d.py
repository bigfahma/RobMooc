from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py
import mpl_toolkits.mplot3d 

import matplotlib.pyplot as plt


                
def draw(ax,x):
    clean3D(ax,-5,20,-5,25,-5,20)
    draw_axis3D(ax,0,0,0,eye(3,3),10)
    draw_robot3D(ax,x[0:3],eulermat(*x[4:7,0]),'blue')
           

def f(x,u):
    x,u=x.flatten(),u.flatten()
    v,φ,θ,ψ=x[3],x[4],x[5],x[6]
    cφ,sφ,cθ,sθ,cψ,sψ= cos(φ),sin(φ),cos(θ),sin(θ),cos(ψ),sin(ψ)
    return array([ [v*cθ*cψ],[v*cθ*sψ],[-v*sθ],[u[0]] ,
                    [-0.1*sφ*cθ + tan(θ)*v*(sφ*u[1]+cφ*u[2])] ,
                     [cφ*v*u[1] - sφ*v*u[2]] ,
                     [(sφ/cθ)*v*u[1] + (cφ/cθ)*v*u[2]]])
              
x = array([[0, 0, 1, 0.1, 0, 0, 0]]).T
u = array([[0,0,0.1]]).T
dt = 0.2
Ts = 20

R = 10
f1 = 0.01
f2 = 6*f1
f3 = 3*f1

ax = mpl_toolkits.mplot3d.Axes3D(figure())  
xd_pt = []
yd_pt = []
zd_pt = []

error_x = []
error_y = []
error_z = []
for t in arange(0,Ts,dt):
    xd,yd,zd = array([R*sin(f1*t) + R*sin(f2*t), 
                      R*cos(f1*t) + R*cos(f2*t),
                      R*sin(f3*t)])
    xd_pt.append(xd)
    yd_pt.append(yd)
    zd_pt.append(zd)

    xd_dot,yd_dot,zd_dot = array([R*f1*cos(f1*t) + R*f2*cos(f2*t),
                                 -R*f1*sin(f1*t) - R*f2*sin(f2*t),
                                  R*f3*cos(f3*t)])

    xd_2dot, yd_2dot, zd_2dot = array([-R*f1*f1*sin(f1*t) - R*f2*f2*sin(f2*t),
                                       -R*f1*f1*cos(f1*t) - R*f2*f2*cos(f2*t),
                                       -R*f3*f3*sin(f3*t)])
                                       
    px,py,pz = x[0,0],x[1,0],x[2,0]
    xdot=f(x,u)
    pxdot,pydot,pzdot = xdot[0,0],xdot[1,0],xdot[2,0] 
    v1,v2,v3 = (0.04*(xd-px)+ 0.4*(xd_dot-pxdot) + xd_2dot,
                0.04*(yd-py)+ 0.4*(yd_dot-pydot) + yd_2dot,
                0.04*(zd-pz)+ 0.4*(zd_dot-pzdot) + zd_2dot)
    v_input = array([[v1],[v2],[v3]])

    ########################################################
    v,phi,theta,psi=x[3,0],x[4,0],x[5,0],x[6,0]
    A1 = array([[cos(theta)*cos(psi), -v*cos(theta)*sin(psi), -v*sin(theta)*cos(psi)],
                [cos(theta)*sin(psi), v*cos(theta)*cos(psi), -v*sin(theta)*sin(psi)],
                [-sin(theta), 0, -v*cos(theta)]])
    A2 = array([[1,0,0],
                [0,v*sin(phi)/cos(theta), v*cos(phi)/cos(theta)],
                [0, v*cos(phi), -v*sin(phi)]])
    A = A1@A2

    u = inv(A)@v_input 
    
    x = x + dt*f(x,u)

    error_x.append(px-xd)
    error_y.append(py-yd)
    error_z.append(pz-zd)

  
    draw(ax,x)

t_list = arange(0,Ts,dt)
ax.plot3D(xd_pt,yd_pt,zd_pt,color ='magenta')
pause(10) 

ax = Axes(figure(),[0,-10,Ts,10])
ax.plot(t_list,error_x,color ='red')
ax.plot(t_list,error_y,color ='green')
ax.plot(t_list,error_z, color = 'blue')
pause(20)
   