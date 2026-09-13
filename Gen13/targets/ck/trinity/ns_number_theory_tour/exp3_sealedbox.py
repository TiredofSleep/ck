# EXP 3: the "pressure-sealed box". 2D vorticity NS from ONE initial field, no forcing.
#   inviscid (nu=0)  = sealed box: does energy RIDE forever (conserved)?  smooth (enstrophy conserved)?
#   viscous (nu>0)   = leaky box:  does it decay?
import os, numpy as np, torch
try: import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt; MPL=True
except Exception as e: MPL=False
OUT=r"C:\Users\brayd\AppData\Local\Temp\claude\C--Users-brayd-OneDrive-Desktop-CK-FINAL-DEPLOYED\4d3410e6-aff7-445d-aa8c-10c94bea4cc0\scratchpad"
dev="cuda" if torch.cuda.is_available() else "cpu"
N=256; dt=2e-3; nsteps=4000
k1=torch.fft.fftfreq(N,d=1.0/N).to(dev); KX=k1.view(N,1).expand(N,N); KY=k1.view(1,N).expand(N,N)
K2=KX**2+KY**2; K2inv=torch.where(K2>0,1.0/K2,torch.zeros_like(K2)); dealias=((KX.abs()<N/3)&(KY.abs()<N/3)).float()
torch.manual_seed(0)
env=torch.exp(-K2/(2*4.0**2)); w0=torch.fft.ifft2(torch.fft.fft2(torch.randn(N,N,device=dev).to(torch.complex64))*env).real
w0=w0/w0.std(); WH0=torch.fft.fft2(w0.to(torch.complex64))
def diag(wh):
    ph=wh*K2inv.to(torch.complex64); u=torch.fft.ifft2(1j*KY*ph).real; v=torch.fft.ifft2(-1j*KX*ph).real
    w=torch.fft.ifft2(wh).real
    return 0.5*(u*u+v*v).mean().item(), 0.5*(w*w).mean().item(), w.abs().max().item()
def run(nu):
    wh=WH0.clone(); L=-nu*K2; Eh=torch.exp(dt*L/2); E2=torch.exp(dt*L)
    def rhs(wh):
        ph=wh*K2inv.to(torch.complex64); u=torch.fft.ifft2(1j*KY*ph).real; v=torch.fft.ifft2(-1j*KX*ph).real
        wx=torch.fft.ifft2(1j*KX*wh).real; wy=torch.fft.ifft2(1j*KY*wh).real
        return -torch.fft.fft2((u*wx+v*wy).to(torch.complex64))*dealias
    E=[];Z=[];M=[];T=[]
    for n in range(nsteps):
        if n%40==0:
            e,z,m=diag(wh); E.append(e);Z.append(z);M.append(m);T.append(n*dt)
        a=dt*rhs(wh);b=dt*rhs(Eh*wh+a/2);c=dt*rhs(Eh*wh+b/2);d=dt*rhs(E2*wh+Eh*c)
        wh=E2*wh+(E2*a+2*Eh*(b+c)+d)/6
    return np.array(T),np.array(E),np.array(Z),np.array(M)
Ti,Ei,Zi,Mi=run(0.0)       # inviscid = sealed box
Tv,Ev,Zv,Mv=run(1e-3)      # viscous  = leaky
print(f"SEALED (nu=0):  energy {Ei[0]:.4f} -> {Ei[-1]:.4f}  ({100*(Ei[-1]/Ei[0]-1):+.2f}%)   "
      f"enstrophy {Zi[0]:.3f} -> {Zi[-1]:.3f}  ({100*(Zi[-1]/Zi[0]-1):+.2f}%)")
print(f"LEAKY  (nu=1e-3):energy {Ev[0]:.4f} -> {Ev[-1]:.4f}  ({100*(Ev[-1]/Ev[0]-1):+.2f}%)   "
      f"enstrophy {Zv[0]:.3f} -> {Zv[-1]:.3f}  ({100*(Zv[-1]/Zv[0]-1):+.2f}%)")
if MPL:
    fig,ax=plt.subplots(1,2,figsize=(11,4.5))
    ax[0].plot(Ti,Ei,'C0-',label='sealed nu=0 (rides)'); ax[0].plot(Tv,Ev,'C3-',label='leaky nu=1e-3 (decays)')
    ax[0].set_title("Energy: sealed box rides forever vs leaky decays"); ax[0].set_xlabel("t"); ax[0].set_ylabel("kinetic energy"); ax[0].legend(); ax[0].set_ylim(0,Ei.max()*1.1)
    ax[1].plot(Ti,Zi,'C0-',label='sealed nu=0'); ax[1].plot(Tv,Zv,'C3-',label='leaky nu=1e-3')
    ax[1].set_title("Enstrophy: 2D sealed box stays SMOOTH\n(conserved => no blow-up in 2D)"); ax[1].set_xlabel("t"); ax[1].set_ylabel("enstrophy"); ax[1].legend()
    plt.tight_layout(); fp=os.path.join(OUT,"exp3_sealedbox.png"); plt.savefig(fp,dpi=110); print("figure:",fp)
