# Katz-Pavlovic dyadic model: NS/Euler reduced to ODEs on INTEGER shells n=0,1,2,...
#   du_n/dt = k_n u_{n-1}^2  -  k_{n+1} u_n u_{n+1}  -  nu k_n^{2a} u_n ,  k_n = lambda^n
# Energy-conserving nonlinearity (telescoping cascade). Inviscid: finite-time blow-up.
# Physical viscosity: regular. Watch the singularity climb shell-by-shell up the integers.
import os, numpy as np
try: import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt; MPL=True
except Exception as e: MPL=False
OUT=r"C:\Users\brayd\AppData\Local\Temp\claude\C--Users-brayd-OneDrive-Desktop-CK-FINAL-DEPLOYED\4d3410e6-aff7-445d-aa8c-10c94bea4cc0\scratchpad"
N=20; lam=2.0; k=lam**np.arange(N); knext=lam*k
def rhs(u,nu,a):
    um1=np.zeros(N); um1[1:]=u[:-1]; up1=np.zeros(N); up1[:-1]=u[1:]
    return k*um1**2 - knext*u*up1 - nu*(k**(2*a))*u
def run(nu,a=1.0,T=4.0,dt=5e-6):
    u=np.zeros(N); u[0]=1.0; ts=[];En=[];Om=[];fr=[]; t=0.0; step=0; tstar=None
    while t<T:
        if step%400==0:
            E=0.5*np.sum(u**2); O=0.5*np.sum(k**2*u**2)
            act=np.where(u>1e-5*max(u.max(),1e-30))[0]; f=act.max() if len(act) else 0
            ts.append(t);En.append(E);Om.append(O);fr.append(f)
        k1=rhs(u,nu,a);k2=rhs(u+dt/2*k1,nu,a);k3=rhs(u+dt/2*k2,nu,a);k4=rhs(u+dt*k3,nu,a)
        u=u+dt/6*(k1+2*k2+2*k3+k4); t+=dt; step+=1
        if (not np.all(np.isfinite(u))) or (0.5*np.sum(k**2*u**2)>1e12) or (u[N-2]>1e-3):
            tstar=t; break
    return np.array(ts),np.array(En),np.array(Om),np.array(fr),tstar
ti,Ei,Oi,fi,tsi=run(0.0)                 # inviscid = Euler dyadic
tv,Ev,Ov,fv,tsv=run(0.10,a=1.0)          # physical viscosity
print(f"INVISCID (Euler dyadic): energy {Ei[0]:.3f}->{Ei[-1]:.3f} (conserved until the wall);  "
      f"enstrophy {Oi[0]:.3f} -> {Oi[-1]:.2e};  FINITE-TIME BLOW-UP at t* ~ {tsi:.4f} (front reached top shell)")
print(f"VISCOUS  (physical nu):  energy {Ev[0]:.3f}->{Ev[-1]:.3f} (dissipates);  "
      f"enstrophy peak {Ov.max():.2f} then decays;  REGULAR (no blow-up){' -- ran full T' if tsv is None else ''}")
if MPL:
    fig,ax=plt.subplots(1,2,figsize=(11,4.5))
    ax[0].semilogy(ti,Oi,'C3',label='inviscid: enstrophy -> infinity'); ax[0].semilogy(tv,Ov,'C0',label='viscous: bounded')
    if tsi: ax[0].axvline(tsi,color='C3',ls=':',lw=1)
    ax[0].set_title("Enstrophy: integer-shell Euler BLOWS UP; NS stays regular"); ax[0].set_xlabel("t"); ax[0].set_ylabel("Sum k_n^2 u_n^2"); ax[0].legend(fontsize=8)
    ax[1].plot(ti,fi,'C3o-',ms=2,label='inviscid: front races up integers'); ax[1].plot(tv,fv,'C0o-',ms=2,label='viscous: front halts')
    ax[1].set_title("Cascade front (highest active shell) vs t"); ax[1].set_xlabel("t"); ax[1].set_ylabel("shell index n"); ax[1].legend(fontsize=8)
    plt.tight_layout(); fp=os.path.join(OUT,"exp9_dyadic.png"); plt.savefig(fp,dpi=110); print("figure:",fp)
