# The resonant triad: three modes k=1,2,3 (1+2=3), phases 120 deg apart ("internally boxed").
# Sealed (inviscid): energy conserved, sloshes among the three forever.  Leaky: decays.
import os, numpy as np
try: import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt; MPL=True
except Exception as e: MPL=False
OUT=r"C:\Users\brayd\AppData\Local\Temp\claude\C--Users-brayd-OneDrive-Desktop-CK-FINAL-DEPLOYED\4d3410e6-aff7-445d-aa8c-10c94bea4cc0\scratchpad"
c=np.array([1.2,-0.5,-0.7]); ksq=np.array([1.,4.,9.])            # c sums to 0 => energy conserved
a0=np.array([1.0, np.exp(2j*np.pi/3), np.exp(4j*np.pi/3)])       # 120-degree phase spacing
def deriv(a,nu):
    d=np.array([c[0]*np.conj(a[1])*np.conj(a[2]),
                c[1]*np.conj(a[2])*np.conj(a[0]),
                c[2]*np.conj(a[0])*np.conj(a[1])])
    return d - nu*ksq*a
def run(nu,T=60,dt=1e-3):
    a=a0.astype(complex).copy(); ts=[];P=[[],[],[]];Et=[]
    for n in range(int(T/dt)):
        if n%40==0:
            ts.append(n*dt); [P[i].append(abs(a[i])**2) for i in range(3)]; Et.append(np.sum(np.abs(a)**2))
        k1=deriv(a,nu);k2=deriv(a+dt/2*k1,nu);k3=deriv(a+dt/2*k2,nu);k4=deriv(a+dt*k3,nu)
        a=a+dt/6*(k1+2*k2+2*k3+k4)
    return np.array(ts),[np.array(p) for p in P],np.array(Et)
ti,Pi,Ei=run(0.0); tv,Pv,Ev=run(0.01)
print(f"SEALED triad: total energy {Ei[0]:.4f} -> {Ei[-1]:.4f}  ({100*(Ei[-1]/Ei[0]-1):+.3f}%)  "
      f"mode energies swing {Pi[0].min():.2f}-{Pi[0].max():.2f} (sloshing, conserved total)")
print(f"LEAKY  triad: total energy {Ev[0]:.4f} -> {Ev[-1]:.4f}  ({100*(Ev[-1]/Ev[0]-1):+.2f}%)  (decays)")
if MPL:
    fig,ax=plt.subplots(1,2,figsize=(11,4.5))
    for i in range(3): ax[0].plot(ti,Pi[i],label=f"|a{i+1}|^2 (k={i+1})")
    ax[0].plot(ti,Ei,'k--',label='total (conserved)'); ax[0].set_title("Sealed resonant triad: energy sloshes, total rides flat"); ax[0].set_xlabel("t"); ax[0].legend(fontsize=8)
    ax[1].plot(ti,Ei,'C0-',label='sealed (rides)'); ax[1].plot(tv,Ev,'C3-',label='leaky (decays)')
    ax[1].set_title("Total triad energy: sealed vs leaky"); ax[1].set_xlabel("t"); ax[1].legend()
    plt.tight_layout(); fp=os.path.join(OUT,"exp4_triad.png"); plt.savefig(fp,dpi=110); print("figure:",fp)
