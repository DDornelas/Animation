import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation as animation
import math

class Pendulo:	
	def __init__(self, massa, l, theta, w):
		self.m=massa
		self.l=l
		self.theta=theta
		self.w=w
		self.w0=math.sqrt(g/l)
		self.T=2*np.pi*math.sqrt(l/g)
		self.k=massa*self.w0**2
		self.e=0.5*massa*((w*l)**2)+massa*g*(l-l*math.cos(theta))
		
	def accel(self, v, tt):
		a=(-(self.w0**2))*math.sin(self.theta)-gama*v+A*math.sin(wf*tt)
		return a
		
	def move(self, tt):
		at=self.accel(self.w, tt)
		self.theta=self.theta+self.w*dt+0.5*at*dt**2
		atmp=self.accel(self.w, tt)
		vtmp=self.w+0.5*(at+atmp)*dt
		atmp=self.accel(vtmp, tt)
		self.w=self.w+0.5*(at+atmp)*dt
		self.e=0.5*self.m*((self.w*self.l)**2)+self.m*g*(self.l-self.l*math.cos(self.theta))
		
g=9.8
gama=0.5
A=1.25
wf=2/3.0
dt=0.2
t1=0

p1=Pendulo(1, 10, np.pi/6, 0)
p2=Pendulo(1, 10, 0.4, 0)

tmax=64
t=np.arange(0, tmax, dt)
thet1=np.zeros(t.size)
omega1=np.zeros(t.size)
energy1=np.zeros(t.size)
thet2=np.zeros(t.size)
omega2=np.zeros(t.size)
energy2=np.zeros(t.size)
dift=np.zeros(t.size)
difw=np.zeros(t.size)

for i in range(t.size):
	p1.move(t[i])
	p2.move(t[i])
	p1.theta=(p1.theta+np.pi)%(2*np.pi)-np.pi
	p2.theta=(p2.theta+np.pi)%(2*np.pi)-np.pi
	thet1[i], omega1[i], energy1[i]=p1.theta, p1.w, p1.e
	thet2[i], omega2[i], energy2[i]=p2.theta, p2.w, p2.e
	dift[i]=math.sqrt((thet1[i]-thet2[i])**2)
	difw[i]=math.sqrt((omega1[i]-omega2[i])**2)
	
relax=4000
tr,wr,t1r = thet1[relax:],omega1[relax:],t[relax:]
difwr,diftr = difw[relax:],dift[relax:]

fig = plt.figure()
plt.title('Forced Pendulum A=1.25', fontsize=14)

plt.xticks(np.linspace(0, 6.4, 2,endpoint=True), ['', ''])
plt.yticks(np.linspace(min(thet1)-0.1, max(thet1)+0.4, 0.3, endpoint=True))
XxT=fig.add_subplot(331, xlim=(0, tmax), ylim=(min(thet1)-0.1, max(thet1)+0.4))
XxT.xaxis.grid(True)
XxT.yaxis.grid(False)
plt.setp(XxT.get_xticklabels(), visible=False)
plt.xlabel('Tempo(s)')
plt.ylabel('Position(m)')
plt.grid()
line1, = XxT.plot([], [], 'r.', lw=2, label="$x_{(t)}$")


VxT=fig.add_subplot(334, xlim=(0, tmax), ylim=(min(omega1)-0.1, max(omega1)+0.4))
VxT.xaxis.grid(True)
VxT.yaxis.grid(True)
plt.setp(VxT.get_xticklabels(), visible=False)
plt.xlabel('Tempo(s)')
plt.ylabel(r'Velocidade($\frac{m}{s}$)')
line2, = VxT.plot([], [], 'b-', lw=2, label="$v_{(t)}$")


ExT=fig.add_subplot(337, xlim=(0, tmax), ylim=(min(energy1)-0.005, max(energy1)+0.03))
plt.xlabel('Tempo(s)')
plt.ylabel('Energia(J)')
line3, = ExT.plot([], [], 'g-', lw=2, label="$e_{(t)}$")


EF=fig.add_subplot(122, xlim=(min(thet1)-0.1, max(thet1)+0.2), ylim=(min(omega1)-0.1, max(omega1)+0.2))
EF.xaxis.grid(True)
EF.yaxis.grid(True)
plt.setp(EF.get_xticklabels(), visible=True)
plt.xlabel(r'Position(m)')
plt.ylabel(r'Velocidade($\frac{m}{s}$)')
line4, = EF.plot([], [], 'k.', lw=2, label="XxV")


def init():
	line1.set_data([],[])
	line2.set_data([],[])
	line3.set_data([],[])
	line4.set_data([],[])
	return line1, line2, line3, line4,
	
def animate(i):
	x=t[:i]
	y=thet1[:i]
	z=omega1[:i]
	ene=energy1[:i]
	line1.set_data(x, y)
	line2.set_data(x, z)
	line3.set_data(x, ene)
	line4.set_data(y, z)
	return line1, line2, line3, line4,
		
anim=animation.FuncAnimation(fig, animate, init_func=init, frames=640,
interval=0, blit=True)

anim.save('PF125.mp4', fps=30)

plt.show()
