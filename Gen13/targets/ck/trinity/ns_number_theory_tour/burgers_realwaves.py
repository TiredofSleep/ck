# Force input updated to REAL TRAVELING NONLINEAR WAVES:
#   f(x,t) = A[ sin(xi) + .5 sin(2 xi + .4) + (1/3) sin(3 xi + .9) ],  xi = x - cw*t
# a steepened multi-harmonic real wave that TRAVELS at speed cw.
# The pairing = modes {+/-1, +/-2, +/-3} coupled by u u_x.  Question: do they WALK (drift)
# and SPIRAL (phase-wind), and does the squared balance still hold?
import os, numpy as np
try: import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt; MPL=True
except Exception as e: MPL=False; print("(no mpl)",e)
OUT=r"C:\Users\brayd\AppData\Local\Temp\claude\C--Users-brayd-OneDrive-Desktop-CK-FINAL-DEPLOYED\4d3410e6-aff7-445d-aa8c-10c94bea4cc0\scratchpad"
N=2048; nu=5e-3; A=1.2; cw=1.5; dt=5e-4
x=2*np.pi*np.arange(N)/N; k=np.fft.fftfreq(N,d=1.0/N); dealias=(np.abs(k)<N/3.0)
L=-nu*k**2; Eh=np.exp(dt*L/2); E2=np.exp(dt*L)
def fhat(t):
    xi=x-cw*t; f=A*(np.sin(xi)+0.5*np.sin(2*xi+0.4)+(1/3.)*np.sin(3*xi+0.9))
    return np.fft.fft(f)
def Nn(uh,t,F):
    u=np.real(np.fft.ifft(uh)); out=-0.5j*k*np.fft.fft(u*u)*dealias
    return out+fhat(t) if F else out
def step(uh,tn,F):
    a=dt*Nn(uh,tn,F); b=dt*Nn(Eh*(uh+a/2),tn+dt/2,F); s=dt*Nn(Eh*uh+b/2,tn+dt/2,F); d=dt*Nn(E2*uh+Eh*s,tn+dt,F)
    return E2*uh+(E2*a+2*Eh*(b+s)+d)/6
def En(uh): u=np.real(np.fft.ifft(uh)); return 0.5*np.mean(u*u)
def Ens(uh): ux=np.real(np.fft.ifft(1j*k*uh)); return 0.5*np.mean(ux*ux)
def shockpos(uh): ux=np.real(np.fft.ifft(1j*k*uh)); return x[np.argmin(ux)]

uh=np.zeros(N,complex); tn=0.0
Ks=[1,2,3]; trF={kk:[] for kk in Ks}; posF=[]; tF=[]
nb=8000
for n in range(nb):
    if n*dt>=2.0 and n%8==0:                 # log forced window t in [2,4]
        tF.append(n*dt); posF.append(shockpos(uh))
        for kk in Ks: trF[kk].append(uh[kk])
    uh=step(uh,tn,True); tn+=dt
P=np.abs(uh)**2; kk=k[:N//2]; PP=P[:N//2]; m=(kk>=4)&(kk<=120)&(PP>0)
slope=np.polyfit(np.log(kk[m]),np.log(PP[m]),1)[0]
# decay
trD={kk:[] for kk in Ks}; Ed=[];Om=[];tD=[]
for n in range(1201):
    if n%4==0:
        tD.append(n*dt); Ed.append(En(uh)); Om.append(Ens(uh))
        for kk in Ks: trD[kk].append(uh[kk])
    uh=step(uh,tn,False)
Ed=np.array(Ed);Om=np.array(Om);tD=np.array(tD); dEdt=np.gradient(Ed,tD); pred=-2*nu*Om
bal=np.max(np.abs(dEdt[2:-2]-pred[2:-2]))/np.max(np.abs(pred[2:-2]))
# drift speed from forced window
tF=np.array(tF); posu=np.unwrap(np.array(posF)); drift=np.polyfit(tF,posu,1)[0]
def winding(arr):
    z=np.array(arr); return (np.unwrap(np.angle(z))[-1]-np.angle(z[0]))/(2*np.pi)
print(f"buildup spectral slope = {slope:.3f}  (still ~ -2 = traveling shock)")
print(f"WALK: shock drift speed measured = {drift:.3f}   (forcing wave speed cw={cw})")
print("SPIRAL (phase winding, turns):")
for kk in Ks:
    print(f"   k={kk}:  forced-phase {winding(trF[kk]):+.2f} turns   |   decay-phase {winding(trD[kk]):+.2f} turns")
print(f"squared-balance in decay: dE/dt=-2*nu*Omega  max rel mismatch = {bal:.2e}")
if MPL:
    fig,ax=plt.subplots(1,2,figsize=(11,4.7))
    col={1:'C0',2:'C1',3:'C2'}
    for kk in Ks:
        z=np.array(trF[kk]); ax[0].plot(z.real,z.imag,color=col[kk],lw=1.1,label=f"k={kk}")
        ax[0].plot(z.real[0],z.imag[0],'o',color=col[kk],ms=4)
        zc=np.conj(z); ax[0].plot(zc.real,zc.imag,color=col[kk],lw=.6,ls=':')   # the -k partner (pairing)
    ax[0].set_title("real traveling waves -> corners WALK & SPIRAL\n(solid=+k, dotted=-k partner = the pairing)")
    ax[0].set_xlabel("Re u_k"); ax[0].set_ylabel("Im u_k"); ax[0].axhline(0,color='.8',lw=.5); ax[0].axvline(0,color='.8',lw=.5); ax[0].legend(fontsize=8)
    ax[1].plot(tF,posu,'.-',lw=1); ax[1].plot(tF, posu[0]+drift*(tF-tF[0]),'r--',label=f"drift {drift:.2f} (cw={cw})")
    ax[1].set_title("WALK: shock position translates in time"); ax[1].set_xlabel("t"); ax[1].set_ylabel("x_shock (unwrapped)"); ax[1].legend(fontsize=8)
    plt.tight_layout(); fp=os.path.join(OUT,"burgers_realwaves.png"); plt.savefig(fp,dpi=110); print("figure:",fp)
