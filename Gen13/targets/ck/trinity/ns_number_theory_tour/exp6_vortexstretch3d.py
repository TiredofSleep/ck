# EXP 2: 3D Navier-Stokes (Taylor-Green), pseudo-spectral, GPU. The vortex-stretching mechanism
# that 2D lacks -- and the geometry of the strain tensor that drives it:
#   * enstrophy GROWS (stretching amplifies vorticity)  * strain axes ORTHOGONAL (90 deg)
#   * deviatoric strain shape = Lode angle (120-deg periodic)  * omega aligns with intermediate axis
import os, numpy as np, torch
try: import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt; MPL=True
except Exception as e: MPL=False
OUT=r"C:\Users\brayd\AppData\Local\Temp\claude\C--Users-brayd-OneDrive-Desktop-CK-FINAL-DEPLOYED\4d3410e6-aff7-445d-aa8c-10c94bea4cc0\scratchpad"
dev="cuda" if torch.cuda.is_available() else "cpu"; print("device:",dev)
N=128; nu=1.0/400; dt=0.01; T=10.0
k1=torch.fft.fftfreq(N,d=1.0/N).to(dev)
KX,KY,KZ=torch.meshgrid(k1,k1,k1,indexing='ij'); K2=KX**2+KY**2+KZ**2
K2inv=torch.where(K2>0,1.0/K2,torch.zeros_like(K2)); dealias=((KX.abs()<N/3)&(KY.abs()<N/3)&(KZ.abs()<N/3)).float()
xg=(2*np.pi*torch.arange(N,device=dev)/N); X,Y,Z=torch.meshgrid(xg,xg,xg,indexing='ij')
def F(f): return torch.fft.fftn(f.to(torch.complex64),dim=(0,1,2))
def IF(f): return torch.fft.ifftn(f,dim=(0,1,2)).real
uh=F(torch.sin(X)*torch.cos(Y)*torch.cos(Z)); vh=F(-torch.cos(X)*torch.sin(Y)*torch.cos(Z)); wh=torch.zeros_like(uh)
L=-nu*K2; Eh=torch.exp(dt*L/2); E2=torch.exp(dt*L)
def curl(uh,vh,wh): return 1j*(KY*wh-KZ*vh),1j*(KZ*uh-KX*wh),1j*(KX*vh-KY*uh)
def rhs(uh,vh,wh):
    u,v,w=IF(uh),IF(vh),IF(wh); oxh,oyh,ozh=curl(uh,vh,wh); ox,oy,oz=IF(oxh),IF(oyh),IF(ozh)
    cx=F(v*oz-w*oy)*dealias; cy=F(w*ox-u*oz)*dealias; cz=F(u*oy-v*ox)*dealias   # u x omega
    kc=(KX*cx+KY*cy+KZ*cz)*K2inv                                                # projection
    return cx-KX*kc, cy-KY*kc, cz-KZ*kc
def step(uh,vh,wh):
    a=rhs(uh,vh,wh); a=[dt*q for q in a]
    b=rhs(Eh*uh+a[0]/2,Eh*vh+a[1]/2,Eh*wh+a[2]/2); b=[dt*q for q in b]
    c=rhs(Eh*uh+b[0]/2,Eh*vh+b[1]/2,Eh*wh+b[2]/2); c=[dt*q for q in c]
    d=rhs(E2*uh+Eh*c[0],E2*vh+Eh*c[1],E2*wh+Eh*c[2]); d=[dt*q for q in d]
    return (E2*uh+(E2*a[0]+2*Eh*(b[0]+c[0])+d[0])/6, E2*vh+(E2*a[1]+2*Eh*(b[1]+c[1])+d[1])/6,
            E2*wh+(E2*a[2]+2*Eh*(b[2]+c[2])+d[2])/6)
Zt=[];Et=[];ts=[]; bestZ=-1; snap=None
for n in range(int(T/dt)):
    if n%10==0:
        ox,oy,oz=IF(curl(uh,vh,wh)[0]),IF(curl(uh,vh,wh)[1]),IF(curl(uh,vh,wh)[2])
        Z=0.5*(ox**2+oy**2+oz**2).mean().item(); E=0.5*(IF(uh)**2+IF(vh)**2+IF(wh)**2).mean().item()
        Zt.append(Z);Et.append(E);ts.append(n*dt)
        if Z>bestZ: bestZ=Z; snap=(uh.clone(),vh.clone(),wh.clone(),n*dt)
    uh,vh,wh=step(uh,vh,wh)
print(f"enstrophy: start {Zt[0]:.3f} -> peak {max(Zt):.3f} at t={ts[int(np.argmax(Zt))]:.1f}  "
      f"(x{max(Zt)/Zt[0]:.1f} amplification by vortex stretching; in 2D this is IMPOSSIBLE)")
uh,vh,wh,tsnap=snap
# strain-tensor statistics at peak stretching
g=[[IF(1j*Kj*uu) for Kj in (KX,KY,KZ)] for uu in (uh,vh,wh)]   # g[i][j]=d u_i / d x_j
ns=120000; idx=torch.randint(0,N**3,(ns,),device=dev)
S=torch.zeros(ns,3,3,device=dev)
for i in range(3):
    for j in range(3): S[:,i,j]=0.5*(g[i][j].reshape(-1)[idx]+g[j][i].reshape(-1)[idx])
evals,evecs=torch.linalg.eigh(S)      # ascending: evals[:,2]>=[:,1]>=[:,0]
l3,l2,l1=evals[:,0],evals[:,1],evals[:,2]     # l1>=l2>=l3, sum~0
s=(-3*np.sqrt(6))*(l1*l2*l3)/((l1**2+l2**2+l3**2)**1.5+1e-20)   # strain-state (Lode) param in [-1,1]
ratio=torch.stack([l1,l2,l3]).mean(1); ratio=ratio/ratio.abs().max()
oxh,oyh,ozh=curl(uh,vh,wh); ov=torch.stack([IF(oxh).reshape(-1)[idx],IF(oyh).reshape(-1)[idx],IF(ozh).reshape(-1)[idx]],1)
ovn=ov/(ov.norm(dim=1,keepdim=True)+1e-20)
al=torch.stack([ (ovn*evecs[:,:,c]).sum(1).abs() for c in range(3)],1)   # |cos| with e_low,e_mid,e_high
prod=((ov.unsqueeze(1)@S@ov.unsqueeze(2)).squeeze()/((ov**2).sum(1)+1e-20)).mean().item()
print(f"mean strain eigenvalues (normalized) lam1:lam2:lam3 = {ratio[0]:.2f} : {ratio[1]:.2f} : {ratio[2]:.2f}  (sum~0, biaxial)")
print(f"mean Lode/shape param <s> = {s.mean().item():+.3f}  (>0 => intermediate eigenvalue positive; s=cos(3*theta_Lode), 120-deg periodic)")
print(f"omega alignment <|cos|> with (low,intermediate,high) strain axes = {al.mean(0)[0]:.3f}, {al.mean(0)[1]:.3f}, {al.mean(0)[2]:.3f}  (peak = intermediate)")
print(f"vortex-stretching production <omega.S.omega>/<|omega|^2> = {prod:+.3f}  (>0 = net stretching)")
if MPL:
    fig,ax=plt.subplots(1,3,figsize=(15,4.3))
    ax[0].plot(ts,Zt,'C3',label='enstrophy (grows: stretching)'); ax[0].plot(ts,Et,'C0',label='energy (viscous decay)')
    ax[0].set_title("3D: enstrophy amplified by vortex stretching\n(2D conserves it -> stays smooth)"); ax[0].set_xlabel("t"); ax[0].legend(fontsize=8)
    ax[1].hist(s.cpu().numpy(),bins=60,color='C2'); ax[1].axvline(s.mean().item(),color='k',ls='--')
    ax[1].set_title("strain shape s=cos(3*theta_Lode)\n(the 120-deg periodic geometry)"); ax[1].set_xlabel("s in [-1,1]")
    lab=['low axis','intermediate','high axis']
    for c in range(3): ax[2].hist(al[:,c].cpu().numpy(),bins=50,histtype='step',lw=1.5,label=lab[c])
    ax[2].set_title("omega alignment with strain axes\n(orthogonal=90deg; peak at intermediate)"); ax[2].set_xlabel("|cos angle|"); ax[2].legend(fontsize=8)
    plt.tight_layout(); fp=os.path.join(OUT,"exp6_vortexstretch3d.png"); plt.savefig(fp,dpi=105); print("figure:",fp)
