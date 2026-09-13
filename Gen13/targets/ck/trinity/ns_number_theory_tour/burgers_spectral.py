# Your experiment on the baby-NS (1D viscous Burgers): u_t + u u_x = nu u_xx + f
# 1) FORCE a single frequency f=A sin(x); nonlinearity cascades it to high k -> shock.
# 2) REMOVE the force; DATA-LOG the "resolve" (decay of every Fourier/trig mode).
# 3) PREDICTIONS:  P1 buildup spectrum slope ~ -2 (Fourier signature of a shock)
#                  P2 after removal, high-k obeys pure-viscous decay exp(-2 nu k^2 t);
#                     a mid-k band stays ABOVE that (nonlinear triad transfer still feeding it)
#                  P3 total energy decays monotonically (dissipation wins -> no self-blow-up)
import os, numpy as np
try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt; MPL=True
except Exception as e:
    MPL=False; print("(no matplotlib:", e, ")")
OUT=r"C:\Users\brayd\AppData\Local\Temp\claude\C--Users-brayd-OneDrive-Desktop-CK-FINAL-DEPLOYED\4d3410e6-aff7-445d-aa8c-10c94bea4cc0\scratchpad"

N=2048; nu=5e-3; A=1.5; dt=5e-4
x=2*np.pi*np.arange(N)/N
k=np.fft.fftfreq(N, d=1.0/N)                 # integer wavenumbers
dealias=(np.abs(k)<N/3.0)                    # 2/3 rule
fhat=np.fft.fft(A*np.sin(x))
L=-nu*k**2; Eh=np.exp(dt*L/2); E2=np.exp(dt*L)   # integrating factor
def Nn(uh,F):                                # nonlinear + forcing:  -0.5 (u^2)_x [+ f]
    u=np.real(np.fft.ifft(uh)); out=-0.5j*k*np.fft.fft(u*u)*dealias
    return out+fhat if F else out
def step(uh,F):                              # integrating-factor RK4 (Trefethen p27)
    a=dt*Nn(uh,F); b=dt*Nn(Eh*(uh+a/2),F); c=dt*Nn(Eh*uh+b/2,F); d=dt*Nn(E2*uh+Eh*c,F)
    return E2*uh+(E2*a+2*Eh*(b+c)+d)/6
def spec(uh): return np.abs(uh)**2
def energy(uh): u=np.real(np.fft.ifft(uh)); return 0.5*np.mean(u*u)

uh=np.zeros(N,complex); ts=[]; Ets=[]
nb=8000                                      # buildup to t=4.0
for n in range(nb):
    uh=step(uh,True)
    if n%40==0: ts.append(n*dt); Ets.append(energy(uh))
P_build=spec(uh); t_off=nb*dt
kk=k[:N//2]; PP=P_build[:N//2]
m=(kk>=4)&(kk<=120)&(PP>0)
slope=np.polyfit(np.log(kk[m]),np.log(PP[m]),1)[0]

snaps={0.0:spec(uh).copy()}; targets={20:0.01,60:0.03,200:0.1,600:0.3}
for n in range(1,601):                       # decay: forcing OFF, run t=0.3 more
    uh=step(uh,False)
    if n%40==0: ts.append(t_off+n*dt); Ets.append(energy(uh))
    if n in targets: snaps[targets[n]]=spec(uh).copy()
D=0.03; Ppred=P_build*np.exp(-2*nu*k**2*D); Pact=snaps[D]
ratio=(Pact+1e-30)/(Ppred+1e-30)
fed=kk[(kk>=2)&(kk<=N/3)&(ratio[:N//2]>2)]
ts=np.array(ts); Ets=np.array(Ets); after=Ets[ts>=t_off]
mono=bool(np.all(np.diff(after)<=1e-12))

print(f"P1  buildup spectral slope, k in [4,120] = {slope:.3f}   (prediction ~ -2.0)")
print(f"P2  after removal, k-band where actual > 2x pure-viscous (nonlinear-fed) = "
      f"[{int(fed.min()) if len(fed) else '-'}, {int(fed.max()) if len(fed) else '-'}];  "
      f"high-k tail should track viscous exp(-2 nu k^2 t)")
# report a few explicit per-mode decay checks (high-k = viscous)
for kc in (80,150,250):
    p0=P_build[kc]; p1=snaps[D][kc]
    r_meas=-np.log((p1+1e-30)/(p0+1e-30))/D; r_pred=2*nu*kc**2
    print(f"      k={kc:>3}:  measured decay rate {r_meas:8.1f}   viscous 2*nu*k^2 = {r_pred:8.1f}"
          f"   ratio {r_meas/r_pred:5.2f}")
print(f"P3  total energy monotonically decays after forcing off: {mono}   "
      f"(peak E={after.max():.4f} -> end E={after[-1]:.4f})")

np.savez(os.path.join(OUT,"burgers_data.npz"), kk=kk, PP=PP, P_build=P_build[:N//2],
         Pact=Pact[:N//2], Ppred=Ppred[:N//2], ts=ts, Ets=Ets, t_off=t_off, slope=slope)
if MPL:
    fig,ax=plt.subplots(1,3,figsize=(15,4.3))
    ax[0].loglog(kk[1:],PP[1:],lw=.7); kr=np.array([3.,200.])
    ax[0].loglog(kr, PP[m][0]*(kr/kk[m][0])**-2,'r--',label='k^-2')
    ax[0].set_title(f"1) Buildup: forced shock\nslope={slope:.2f}  (predict -2)"); ax[0].set_xlabel("k"); ax[0].set_ylabel("|u_k|^2"); ax[0].legend()
    ax[1].loglog(kk[1:],P_build[1:N//2],'k-',lw=.6,label='at force-off')
    ax[1].loglog(kk[1:],Pact[1:N//2],'b-',lw=.9,label=f'actual +{D}')
    ax[1].loglog(kk[1:],Ppred[1:N//2],'r--',lw=.9,label='pure-viscous predict')
    ax[1].set_ylim(1e-6, PP.max()*3); ax[1].set_title("2) Resolve: actual vs viscous-only\n(gap = nonlinear transfer)"); ax[1].set_xlabel("k"); ax[1].legend()
    ax[2].plot(ts,Ets,lw=1.2); ax[2].axvline(t_off,color='g',ls=':')
    ax[2].set_title("3) Total energy\n(force off = dotted; dissipation wins)"); ax[2].set_xlabel("t"); ax[2].set_ylabel("E")
    plt.tight_layout(); fp=os.path.join(OUT,"burgers_spectral.png"); plt.savefig(fp,dpi=110); print("figure:",fp)
