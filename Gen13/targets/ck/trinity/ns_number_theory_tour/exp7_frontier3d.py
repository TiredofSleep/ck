# FRONTIER (3D): Reynolds sweep of Taylor-Green. As nu->0 does the amplification redline?
# Diagnostics: peak enstrophy Z_max, dissipation eps=2*nu*Z_max (finite limit = dissipation anomaly
# = regular; divergent = blow-up signature), and BKM marker ||omega||_inf growth.
import os, gc, numpy as np, torch
try: import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt; MPL=True
except Exception as e: MPL=False
OUT=r"C:\Users\brayd\AppData\Local\Temp\claude\C--Users-brayd-OneDrive-Desktop-CK-FINAL-DEPLOYED\4d3410e6-aff7-445d-aa8c-10c94bea4cc0\scratchpad"
dev="cuda"; N=128; dt=0.01; T=12.0
k1=torch.fft.fftfreq(N,d=1.0/N).to(dev); KX,KY,KZ=torch.meshgrid(k1,k1,k1,indexing='ij')
K2=KX**2+KY**2+KZ**2; K2inv=torch.where(K2>0,1.0/K2,torch.zeros_like(K2)); dealias=((KX.abs()<N/3)&(KY.abs()<N/3)&(KZ.abs()<N/3)).float()
xg=2*np.pi*torch.arange(N,device=dev)/N; X,Y,Z=torch.meshgrid(xg,xg,xg,indexing='ij')
def Ff(f): return torch.fft.fftn(f.to(torch.complex64),dim=(0,1,2))
def IFf(f): return torch.fft.ifftn(f,dim=(0,1,2)).real
def curl(uh,vh,wh): return 1j*(KY*wh-KZ*vh),1j*(KZ*uh-KX*wh),1j*(KX*vh-KY*uh)
def run(nu):
    uh=Ff(torch.sin(X)*torch.cos(Y)*torch.cos(Z)); vh=Ff(-torch.cos(X)*torch.sin(Y)*torch.cos(Z)); wh=torch.zeros_like(uh)
    Eh=torch.exp(-nu*K2*dt/2); E2=torch.exp(-nu*K2*dt)
    def rhs(uh,vh,wh):
        u,v,w=IFf(uh),IFf(vh),IFf(wh); oxh,oyh,ozh=curl(uh,vh,wh); ox,oy,oz=IFf(oxh),IFf(oyh),IFf(ozh)
        cx=Ff(v*oz-w*oy)*dealias; cy=Ff(w*ox-u*oz)*dealias; cz=Ff(u*oy-v*ox)*dealias
        kc=(KX*cx+KY*cy+KZ*cz)*K2inv; return cx-KX*kc,cy-KY*kc,cz-KZ*kc
    def step(uh,vh,wh):
        a=[dt*q for q in rhs(uh,vh,wh)]
        b=[dt*q for q in rhs(Eh*uh+a[0]/2,Eh*vh+a[1]/2,Eh*wh+a[2]/2)]
        c=[dt*q for q in rhs(Eh*uh+b[0]/2,Eh*vh+b[1]/2,Eh*wh+b[2]/2)]
        d=[dt*q for q in rhs(E2*uh+Eh*c[0],E2*vh+Eh*c[1],E2*wh+Eh*c[2])]
        return (E2*uh+(E2*a[0]+2*Eh*(b[0]+c[0])+d[0])/6, E2*vh+(E2*a[1]+2*Eh*(b[1]+c[1])+d[1])/6,
                E2*wh+(E2*a[2]+2*Eh*(b[2]+c[2])+d[2])/6)
    ts=[];Zt=[];Wt=[]
    for n in range(int(T/dt)):
        if n%10==0:
            ox,oy,oz=IFf(curl(uh,vh,wh)[0]),IFf(curl(uh,vh,wh)[1]),IFf(curl(uh,vh,wh)[2])
            w2=ox**2+oy**2+oz**2; Zt.append(0.5*w2.mean().item()); Wt.append(w2.max().item()**0.5); ts.append(n*dt)
        uh,vh,wh=step(uh,vh,wh)
    return np.array(ts),np.array(Zt),np.array(Wt)
res={}
for nu in (1/200.,1/400.,1/800.):
    ts,Zt,Wt=run(nu); res[nu]=(ts,Zt,Wt); gc.collect(); torch.cuda.empty_cache()
    Zmax=Zt.max(); eps=2*nu*Zmax; Re=int(round(1/nu))
    # BKM growth rate of ||w||_inf
    lg=np.log(Wt); gr=np.gradient(lg,ts); 
    print(f"Re={Re:4d} (nu={nu:.2e}): Z_max={Zmax:6.3f}  eps=2nu*Zmax={eps:.4f}  ||w||inf_peak={Wt.max():5.2f}  max d/dt log||w||inf={gr.max():.2f}")
print("\nDISSIPATION-ANOMALY READ: if eps flattens to a finite limit as Re grows -> controlled cascade, NO blow-up signature.")
if MPL:
    fig,ax=plt.subplots(1,3,figsize=(15,4.3)); C={200:'C0',400:'C1',800:'C2'}
    for nu in (1/200.,1/400.,1/800.):
        ts,Zt,Wt=res[nu]; Re=int(round(1/nu))
        ax[0].plot(ts,Zt,C[Re],label=f'Re={Re}'); ax[1].semilogy(ts,Wt,C[Re],label=f'Re={Re}')
    ax[0].set_title("enstrophy Z(t) (grows with Re)"); ax[0].set_xlabel("t"); ax[0].legend()
    ax[1].set_title("||omega||_inf (BKM marker)"); ax[1].set_xlabel("t"); ax[1].legend()
    Res=[200,400,800]; epss=[2*(1/R)*res[1/R][1].max() for R in Res]
    ax[2].plot(Res,epss,'ko-'); ax[2].set_title("dissipation eps=2*nu*Z_max vs Re\n(flat => anomaly => regular)"); ax[2].set_xlabel("Re"); ax[2].set_ylabel("eps"); ax[2].set_ylim(0,max(epss)*1.3)
    plt.tight_layout(); fp=os.path.join(OUT,"exp7_frontier3d.png"); plt.savefig(fp,dpi=105); print("figure:",fp)
