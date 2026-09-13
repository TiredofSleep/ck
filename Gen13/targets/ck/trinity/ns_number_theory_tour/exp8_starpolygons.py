# The untouchable center: closed loops wind around a point they never touch.
# {q/p} is ONE loop iff gcd(p,q)=1 (winds p times); else it breaks into gcd(p,q) sub-loops.
# Prime q => every step-size is a single loop (rotationally indivisible). Count = phi(q).
import os, numpy as np
from math import gcd
try: import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt; MPL=True
except Exception as e: MPL=False
OUT=r"C:\Users\brayd\AppData\Local\Temp\claude\C--Users-brayd-OneDrive-Desktop-CK-FINAL-DEPLOYED\4d3410e6-aff7-445d-aa8c-10c94bea4cc0\scratchpad"
def isprime(n): return n>1 and all(n%d for d in range(2,int(n**.5)+1))
print("q  | phi(q) = # single-loop step-sizes (winding numbers) | prime?")
for q in range(3,16):
    cop=[p for p in range(1,q) if gcd(p,q)==1]
    print(f"{q:2d} | phi={len(cop):2d}  coprime windings p={cop}   {'<-- PRIME: every step is one indivisible loop' if isprime(q) else ''}")
def trace(q,p):
    g=gcd(q,p); loops=[]
    for s in range(g):
        seq=[s]; k=s
        while (k:=(k+p)%q)!=s: seq.append(k)
        seq.append(s); loops.append(seq)
    return loops,g
if MPL:
    cases=[(5,2),(7,3),(11,4),(13,5),(6,2),(8,2),(12,4),(12,3)]  # top row: prime/coprime single loops; bottom: composite breaks
    fig,ax=plt.subplots(2,4,figsize=(14,7.2))
    for a,(q,p) in zip(ax.ravel(),cases):
        ang=2*np.pi*np.arange(q)/q; V=np.c_[np.cos(ang),np.sin(ang)]; loops,g=trace(q,p)
        col='C0' if g==1 else 'C3'
        for seq in loops: a.plot(V[seq,0],V[seq,1],'-',color=col,lw=1.4)
        a.scatter(V[:,0],V[:,1],s=14,color='k',zorder=3); a.plot(0,0,'k+',ms=11,mew=2)  # untouchable center
        a.set_title(f"{{{q}/{p}}}  " + (f"ONE loop, winds {p}x" if g==1 else f"breaks into {g} loops"), fontsize=9)
        a.set_aspect('equal'); a.axis('off')
    fig.suptitle("Closed loops wind around an UNTOUCHABLE center (+). gcd(p,q)=1 => single loop (blue); gcd>1 => splits (red).\n"
                 "Prime q: EVERY step-size is one indivisible loop -- primes are the rotationally untouchable.", fontsize=11)
    plt.tight_layout(); fp=os.path.join(OUT,"exp8_starpolygons.png"); plt.savefig(fp,dpi=110); print("figure:",fp)
