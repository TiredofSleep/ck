# EXP 1 (final): genuine FINITE-TIME singularity from smooth data, no forcing.
# Inviscid Burgers with u0=-sin(x) steepens to a shock at t*=1: max|u_x| ~ 1/(t*-t) -> infinity.
# Viscosity CAPS it (that's exactly what removing viscosity, not adding force, buys you).
import os, numpy as np
try: import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt; MPL=True
except Exception as e: MPL=False
OUT=r"C:\Users\brayd\AppData\Local\Temp\claude\C--Users-brayd-OneDrive-Desktop-CK-FINAL-DEPLOYED\4d3410e6-aff7-445d-aa8c-10c94bea4cc0\scratchpad"
N=4096; dt=1e-4; T=1.12
x=2*np.pi*np.arange(N)/N; k=np.fft.fftfreq(N,d=1.0/N); dealias=(np.abs(k)<N/3.0)
u0=np.fft.fft(-np.sin(x))
def run(nu):
    L=-nu*k**2; Eh=np.exp(dt*L/2); E2=np.exp(dt*L); uh=u0.copy()
    def Nn(uh):
        u=np.real(np.fft.ifft(uh)); return -0.5j*k*np.fft.fft(u*u)*dealias
    def step(uh):
        a=dt*Nn(uh);b=dt*Nn(Eh*uh+a/2);c=dt*Nn(Eh*uh+b/2);d=dt*Nn(E2*uh+Eh*c)
        return E2*uh+(E2*a+2*Eh*(b+c)+d)/6
    ts=[];mg=[]
    for n in range(int(T/dt)):
        if n%40==0:
            ux=np.real(np.fft.ifft(1j*k*uh)); ts.append(n*dt); mg.append(np.abs(ux).max())
        uh=step(uh)
    return np.array(ts),np.array(mg)
res={}
for nu in (2e-3,5e-4,1.5e-4):
    ts,mg=res.setdefault(nu,run(nu))
    i=np.argmin(np.abs(ts-0.95)); print(f"nu={nu:.1e}: max|u_x| at t=0.95 = {mg[i]:7.1f}   peak = {mg.max():7.1f}")
print("inviscid prediction: max|u_x| = 1/(1-t) -> infinity at t*=1  (shock from smooth data)")
if MPL:
    plt.figure(figsize=(7.5,5))
    tt=np.linspace(0.5,0.99,100); plt.plot(tt,1/(1-tt),'k--',lw=2,label='inviscid 1/(1-t) -> ∞ at t*=1')
    for nu in (2e-3,5e-4,1.5e-4):
        ts,mg=res[nu]; plt.plot(ts,mg,label=f'viscous nu={nu:.1e}')
    plt.axvline(1.0,color='.6',ls=':'); plt.yscale('log'); plt.xlabel('t'); plt.ylabel('max |u_x|')
    plt.title('Finite-time gradient blow-up (smooth data, NO forcing)\nviscosity caps it; cap -> infinity as nu -> 0')
    plt.legend(); plt.tight_layout(); fp=os.path.join(OUT,"exp5_burgers_blowup.png"); plt.savefig(fp,dpi=110); print("figure:",fp)
