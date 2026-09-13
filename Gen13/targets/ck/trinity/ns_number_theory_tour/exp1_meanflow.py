# EXP 1: does the spiral persist if we give the flow conserved net momentum (mean flow U)?
# Build the same traveling-forced state, then free-decay from it with U=0 vs U=2; measure
# whether the paired corners keep winding (persistent spiral) or unwind (collapse).
import os, numpy as np
try: import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt; MPL=True
except Exception as e: MPL=False
OUT=r"C:\Users\brayd\AppData\Local\Temp\claude\C--Users-brayd-OneDrive-Desktop-CK-FINAL-DEPLOYED\4d3410e6-aff7-445d-aa8c-10c94bea4cc0\scratchpad"
N=2048; nu=5e-3; A=1.2; cw=1.5; dt=5e-4
x=2*np.pi*np.arange(N)/N; k=np.fft.fftfreq(N,d=1.0/N); dealias=(np.abs(k)<N/3.0)
L=-nu*k**2; Eh=np.exp(dt*L/2); E2=np.exp(dt*L)
def fhat(t):
    xi=x-cw*t; return np.fft.fft(A*(np.sin(xi)+0.5*np.sin(2*xi+0.4)+(1/3.)*np.sin(3*xi+0.9)))
def Nn(uh,t,F):
    u=np.real(np.fft.ifft(uh)); out=-0.5j*k*np.fft.fft(u*u)*dealias
    return out+fhat(t) if F else out
def step(uh,tn,F):
    a=dt*Nn(uh,tn,F);b=dt*Nn(Eh*(uh+a/2),tn+dt/2,F);s=dt*Nn(Eh*uh+b/2,tn+dt/2,F);d=dt*Nn(E2*uh+Eh*s,tn+dt,F)
    return E2*uh+(E2*a+2*Eh*(b+s)+d)/6
uh=np.zeros(N,complex); tn=0.0
for n in range(6000): uh=step(uh,tn,True); tn+=dt      # buildup
Ks=[1,2,3]
def decay(U):
    v=uh.copy(); v[0]=U*N                              # inject conserved mean flow U
    tr={kk:[v[kk]] for kk in Ks}; means=[np.mean(np.real(np.fft.ifft(v)))]
    for n in range(3000):
        v=step(v,tn+n*dt,False)
        if n%6==0:
            for kk in Ks: tr[kk].append(v[kk])
            means.append(np.mean(np.real(np.fft.ifft(v))))
    return tr, means
def wind(a):
    z=np.array(a); return (np.unwrap(np.angle(z))[-1]-np.angle(z[0]))/(2*np.pi)
res={}
for U in (0.0,2.0):
    tr,means=decay(U); res[U]=tr
    print(f"U={U}: mean flow conserved? start {means[0]:+.3f} -> end {means[-1]:+.3f}")
    for kk in Ks: print(f"     decay winding k={kk}: {wind(tr[kk]):+.2f} turns")
if MPL:
    fig,ax=plt.subplots(1,2,figsize=(11,4.7)); col={1:'C0',2:'C1',3:'C2'}
    for j,U in enumerate((0.0,2.0)):
        for kk in Ks:
            z=np.array(res[U][kk]); ax[j].plot(z.real,z.imag,color=col[kk],lw=1.1,label=f"k={kk}")
            ax[j].plot(z.real[0],z.imag[0],'o',color=col[kk],ms=4)
        ax[j].set_title(("U=0 (zero momentum): spiral UNWINDS" if U==0 else "U=2 (conserved momentum): spiral PERSISTS")); ax[j].set_xlabel("Re u_k"); ax[j].set_ylabel("Im u_k")
        ax[j].axhline(0,color='.85',lw=.5); ax[j].axvline(0,color='.85',lw=.5); ax[j].legend(fontsize=8)
    plt.tight_layout(); fp=os.path.join(OUT,"exp1_meanflow.png"); plt.savefig(fp,dpi=110); print("figure:",fp)
