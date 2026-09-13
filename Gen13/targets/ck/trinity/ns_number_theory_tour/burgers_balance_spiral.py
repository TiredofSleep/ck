# Tests the REAL parts of the hypothesis:
#  (A) "squared function of balance": is dE/dt == -2 nu * enstrophy exactly?  (energy law)
#  (B) "walk and spiral": do the complex trig modes spiral inward as they decay?
import os, numpy as np
try: import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt; MPL=True
except Exception as e: MPL=False; print("(no mpl)",e)
OUT=r"C:\Users\brayd\AppData\Local\Temp\claude\C--Users-brayd-OneDrive-Desktop-CK-FINAL-DEPLOYED\4d3410e6-aff7-445d-aa8c-10c94bea4cc0\scratchpad"
N=2048; nu=5e-3; A=1.5; dt=5e-4
x=2*np.pi*np.arange(N)/N; k=np.fft.fftfreq(N,d=1.0/N); dealias=(np.abs(k)<N/3.0)
fhat=np.fft.fft(A*np.sin(x)); L=-nu*k**2; Eh=np.exp(dt*L/2); E2=np.exp(dt*L)
def Nn(uh,F):
    u=np.real(np.fft.ifft(uh)); out=-0.5j*k*np.fft.fft(u*u)*dealias
    return out+fhat if F else out
def step(uh,F):
    a=dt*Nn(uh,F);b=dt*Nn(Eh*(uh+a/2),F);c=dt*Nn(Eh*uh+b/2,F);d=dt*Nn(E2*uh+Eh*c,F)
    return E2*uh+(E2*a+2*Eh*(b+c)+d)/6
def En(uh): u=np.real(np.fft.ifft(uh)); return 0.5*np.mean(u*u)
def Ens(uh): ux=np.real(np.fft.ifft(1j*k*uh)); return 0.5*np.mean(ux*ux)
uh=np.zeros(N,complex)
for n in range(8000): uh=step(uh,True)              # buildup
Ks=[1,2,3,5,8,13]; traj={kk:[] for kk in Ks}; E=[];Om=[];T=[]
nd=1200
for n in range(nd+1):
    T.append(n*dt); E.append(En(uh)); Om.append(Ens(uh))
    for kk in Ks: traj[kk].append(uh[kk])
    uh=step(uh,False)                                # decay, forcing OFF
E=np.array(E);Om=np.array(Om);T=np.array(T); dEdt=np.gradient(E,T); pred=-2*nu*Om
rel=np.max(np.abs(dEdt[2:-2]-pred[2:-2]))/np.max(np.abs(pred[2:-2]))
print(f"(A) squared-balance law  dE/dt = -2*nu*enstrophy :  max relative mismatch = {rel:.2e}  (0 = exact)")
print(f"    check @ mid-decay: dE/dt={dEdt[len(T)//2]:.4f}   -2*nu*Omega={pred[len(T)//2]:.4f}")
for kk in Ks:
    z=np.array(traj[kk]); turns=np.abs(np.angle(z[-1])-np.angle(z[0]))/(2*np.pi)
    print(f"(B) mode k={kk:>2}: |u_k| {np.abs(z[0]):.4f} -> {np.abs(z[-1]):.4f}   phase winding ~ {turns:.2f} turns (spiral)")
if MPL:
    fig,ax=plt.subplots(1,2,figsize=(11,4.6))
    ax[0].plot(T,dEdt,'b-',lw=1.4,label='dE/dt (measured)')
    ax[0].plot(T,pred,'r--',lw=1.4,label='-2 nu * enstrophy (law)')
    ax[0].set_title("(A) squared balance: energy law holds exactly"); ax[0].set_xlabel("t"); ax[0].set_ylabel("dE/dt"); ax[0].legend()
    for kk in Ks:
        z=np.array(traj[kk]); ax[1].plot(z.real,z.imag,lw=1.0,label=f"k={kk}"); ax[1].plot(z.real[0],z.imag[0],'o',ms=3)
    ax[1].set_title("(B) trig modes spiral inward as they decay"); ax[1].set_xlabel("Re u_k"); ax[1].set_ylabel("Im u_k"); ax[1].axhline(0,color='.7',lw=.5); ax[1].axvline(0,color='.7',lw=.5); ax[1].legend(fontsize=8)
    plt.tight_layout(); fp=os.path.join(OUT,"burgers_balance_spiral.png"); plt.savefig(fp,dpi=110); print("figure:",fp)
