-- compute_betti.m2
-- Minimal free resolution + Betti table of the binomial ideal I_CL
--   I_CL = ( x_i * x_j  -  x_{CL[i][j]} * x_0  :  0 <= i <= j <= 9 )
-- inside R = k[x_0, ..., x_9], with the 10x10 CL composition table from TIG.
-- Gate-check for MathOverflow post to Dr. Paolo Mantero.

-- Base ring: 10 indeterminates x_0..x_9 over QQ, graded standard (each x_i has degree 1)
R = QQ[x_0, x_1, x_2, x_3, x_4, x_5, x_6, x_7, x_8, x_9];

-- The 10x10 CL composition table (from ck_tig.py / MANTERO_BRIDGE_V3.md)
--   CL[i][j] = index k such that op_i * op_j = op_k in the TIG magma
--   ops: 0=VOID, 1=LATTICE, 2=COUNTER, 3=PROGRESS, 4=COLLAPSE,
--        5=BALANCE, 6=CHAOS, 7=HARMONY, 8=BREATH, 9=RESET
CL = {
  {0,0,0,0,0,0,0,7,0,0},
  {0,7,3,7,7,7,7,7,7,7},
  {0,3,7,7,4,7,7,7,7,9},
  {0,7,7,7,7,7,7,7,7,3},
  {0,7,4,7,7,7,7,7,8,7},
  {0,7,7,7,7,7,7,7,7,7},
  {0,7,7,7,7,7,7,7,7,7},
  {7,7,7,7,7,7,7,7,7,7},
  {0,7,7,7,8,7,7,7,7,7},
  {0,7,9,3,7,7,7,7,7,7}
};

-- Helper: variable at a given index 0..9
xOf = i -> R_i;

-- Build the generating binomials   x_i*x_j - x_{CL[i][j]}*x_0   for  0 <= i <= j <= 9
-- (symmetric case, i=j is included and gives x_i^2 - x_{CL[i][i]}*x_0)
gensL = {};
for i from 0 to 9 do (
  for j from i to 9 do (
    k := (CL#i)#j;
    b := xOf(i) * xOf(j)  -  xOf(k) * xOf(0);
    if b != 0_R then gensL = append(gensL, b);
  );
);

<< "Raw binomial generators produced: " << #gensL << endl;

I = ideal gensL;
I = trim I;

<< "Trimmed ideal I_CL: numgens = " << numgens I << endl;
<< "                    codim   = " << codim I << endl;
<< "                    dim R/I = " << dim(R/I) << endl;
<< "                    deg R/I = " << degree(R/I) << endl;
<< endl;

-- Minimal free resolution
<< "Computing minimal free resolution..." << endl;
C = res I;

<< endl;
<< "=== BETTI TABLE of R/I_CL ===" << endl;
<< betti C << endl;

-- Print length and ranks
<< endl;
<< "Resolution length:            " << length C << endl;
-- pdim takes a module; use the rank-1 free quotient R^1/I.
MI = coker gens I;
pdRI := pdim MI;
<< "pd(R/I_CL)       =            " << pdRI << endl;
<< "pd(I_CL)         =            " << (pdRI - 1) << endl;

-- Projective dimension vs. Auslander-Buchsbaum:   pd + depth = n  (for R polynomial over a field)
-- So depth(R/I) = n - pd(R/I).  Compare to dim R/I to see Cohen-Macaulayness.
nVar := numgens R;
dimRI := dim(R/I);
depthRI := nVar - pdRI;
<< endl;
<< "n (= numgens R)  =            " << nVar << endl;
<< "dim R/I          =            " << dimRI << endl;
<< "depth R/I (A-B)  =            " << depthRI << endl;
<< "Cohen-Macaulay?  =            " << (dimRI == depthRI) << endl;

-- Hilbert series & polynomial
<< endl;
<< "Hilbert series of R/I (numerator, denominator):" << endl;
hs = hilbertSeries(R/I);
<< hs << endl;
<< "reduced form: " << reduceHilbert hs << endl;

<< endl;
<< "Hilbert polynomial of R/I:" << endl;
<< hilbertPolynomial(R/I) << endl;

-- Ranks of free modules in the resolution (convenient for the MathOverflow post)
<< endl;
<< "Ranks of free modules in the minimal free resolution:" << endl;
for i from 0 to length C do (
  << "  F_" << i << "  rank = " << rank C_i << endl;
);

-- Check Koszul-ness via the first quadratic strand of the Betti table
-- (An algebra is Koszul iff beta_{i, i+j} = 0 for j > 1.  We just print the full table above.)

-- Optional: linear strand indicator — compute total Tor dimensions in low homological degree
<< endl;
<< "Tor dim beta_0 = " << numgens target C.dd_1 << endl;
for i from 1 to min(5, length C) do (
  << "Tor dim beta_" << i << " = " << numgens source C.dd_i << endl;
);

<< endl << "=== DONE ===" << endl;
exit 0
