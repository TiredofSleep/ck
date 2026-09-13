# EXP 2: two coupled NS fields provide their OWN force (no external forcing) -- 2D Boussinesq.
#   omega_t + u.grad omega = nu Lap omega + d_x theta      (buoyancy of theta forces the vorticity)
#   theta_t + u.grad theta = nu Lap theta                  (flow advects theta back)
#   u = grad^perp psi,  Lap psi = -omega
# A warm blob (theta) with zero initial vorticity: the coupling alone makes it roll up into a
# mushroom plume -- the two fields forcing each other.  GPU (torch/cuda), pseudo-spectral.
import os, numpy as np, torch
try: import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt; MPL=True
except Exception as e: MPL=False
OUT=r"C:\Users\brayd\AppData\Local\Temp\claude\C--Users-brayd-OneDrive-Desktop-CK-FINAL-DEPLOYED\4d3410e6-aff7-445d-aa8c-10c94bea4cc0\scratchpad"
dev="cuda" if torch.cuda.is_available() else "cpu"; print("device:",dev, torch.cuda.get_device_name(0) if dev=="cuda" else "")
N=256; nu=1.5e-3; dt=2e-3; nsteps=3000
x=2*np.pi*torch.arange(N,device=dev)/N
k1=torch.fft.fftfreq(N,d=1.0/N).to(dev)
KX=k1.view(N,1).expand(N,N); KY=k1.view(1,N).expand(N,N)
K2=KX**2+KY**2; K2inv=torch.where(K2>0,1.0/K2,torch.zeros_like(K2))
dealias=((KX.abs()<N/3)&(KY.abs()<N/3)).float()
Xg=x.view(N,1).expand(N,N); Yg=x.view(1,N).expand(N,N)
theta=torch.exp(-(((Xg-np.pi)**2+(Yg-np.pi)**2)/(2*0.5**2)))   # warm blob
th=torch.fft.fft2(theta.to(torch.complex64)); wh=torch.zeros_like(th)
L=-nu*K2; Eh=torch.exp(dt*L/2); E2=torch.exp(dt*L)
def rhs(wh,th):
    ph=wh*K2inv.to(torch.complex64)
    u=torch.fft.ifft2(1j*KY*ph).real; v=torch.fft.ifft2(-1j*KX*ph).real
    wx=torch.fft.ifft2(1j*KX*wh).real; wy=torch.fft.ifft2(1j*KY*wh).real
    tx=torch.fft.ifft2(1j*KX*th).real; ty=torch.fft.ifft2(1j*KY*th).real
    Nw=-torch.fft.fft2((u*wx+v*wy).to(torch.complex64))*dealias + 1j*KX*th   # advection + buoyancy force
    Nt=-torch.fft.fft2((u*tx+v*ty).to(torch.complex64))*dealias
    return Nw,Nt
def step(wh,th):
    aw,at=rhs(wh,th); aw*=dt; at*=dt
    bw,bt=rhs(Eh*(wh+aw/2),Eh*(th+at/2)); bw*=dt; bt*=dt
    sw,st=rhs(Eh*wh+bw/2,Eh*th+bt/2); sw*=dt; st*=dt
    dw,dtt=rhs(E2*wh+Eh*sw,E2*th+Eh*st); dw*=dt; dtt*=dt
    return E2*wh+(E2*aw+2*Eh*(bw+sw)+dw)/6, E2*th+(E2*at+2*Eh*(bt+st)+dtt)/6
maxw=[]; ts=[]
for n in range(nsteps):
    wh,th=step(wh,th)
    if n%30==0:
        w=torch.fft.ifft2(wh).real; maxw.append(w.abs().max().item()); ts.append(n*dt)
w=torch.fft.ifft2(wh).real.cpu().numpy(); tf=torch.fft.ifft2(th).real.cpu().numpy()
# shell-averaged kinetic energy spectrum
ph=wh*K2inv.to(torch.complex64); u=torch.fft.ifft2(1j*KY*ph); v=torch.fft.ifft2(-1j*KX*ph)
Ek=0.5*(torch.fft.fft2(u.real.to(torch.complex64)).abs()**2+torch.fft.fft2(v.real.to(torch.complex64)).abs()**2)/N**4
kmag=torch.sqrt(K2).cpu().numpy().ravel(); Ekf=Ek.cpu().numpy().ravel()
kb=np.arange(1,N//3); Es=np.array([Ekf[(kmag>=kk-0.5)&(kmag<kk+0.5)].sum() for kk in kb])
print(f"max|omega|: start~0 -> peak {max(maxw):.2f} (vorticity generated purely by the two-field coupling)")
if MPL:
    fig,ax=plt.subplots(1,4,figsize=(18,4.3))
    ax[0].imshow(tf.T,origin='lower',cmap='inferno'); ax[0].set_title("theta (buoyancy field)"); ax[0].set_xticks([]);ax[0].set_yticks([])
    ax[1].imshow(w.T,origin='lower',cmap='RdBu_r'); ax[1].set_title("omega (vorticity) -- made by the coupling"); ax[1].set_xticks([]);ax[1].set_yticks([])
    ax[2].loglog(kb,Es+1e-30); ax[2].loglog(kb,Es[3]*(kb/kb[3])**(-3.0),'r--',label='k^-3'); ax[2].set_title("kinetic energy spectrum"); ax[2].set_xlabel("k"); ax[2].legend()
    ax[3].plot(ts,maxw); ax[3].set_title("max|omega| vs t\n(0 -> finite: internal force at work)"); ax[3].set_xlabel("t")
    plt.tight_layout(); fp=os.path.join(OUT,"exp2_boussinesq.png"); plt.savefig(fp,dpi=105); print("figure:",fp)
