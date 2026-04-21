// CODEC FIDELITY — final test with reasonable tolerances

const σ = 0.991, σs = 0.009, Ts = 0.714;
const COLS = 18, ROWS = 14, NC = COLS * ROWS;

class Q {
  constructor(a, b, c) { this.a = a; this.b = b; this.c = c; }
  ev(x) { return this.a * x * x + this.b * x + this.c; }
  D() { return this.b * this.b - 4 * this.a * this.c; }
  d1(x) { return 2 * this.a * x + this.b; }
  vx() { return Math.abs(this.a) > 1e-12 ? -this.b / (2 * this.a) : 0; }
  vy() { return this.ev(this.vx()); }
  roots() {
    const d = this.D();
    if (Math.abs(this.a) < 1e-12) return { re: true, r1: 0, r2: 0, im: 0 };
    if (d >= 0) { const s = Math.sqrt(d); return { re: true, r1: (-this.b + s) / (2 * this.a), r2: (-this.b - s) / (2 * this.a), im: 0 }; }
    return { re: false, r1: -this.b / (2 * this.a), r2: -this.b / (2 * this.a), im: Math.sqrt(-d) / (2 * Math.abs(this.a)) };
  }
  fp() {
    const A = this.a, B = this.b - 1, C = this.c;
    const d = B * B - 4 * A * C;
    if (Math.abs(A) < 1e-12) return B !== 0 ? { x: -C / B, stable: Math.abs(this.b) < 1 } : null;
    if (d < 0) return null;
    const s = Math.sqrt(d);
    const x1 = (-B + s) / (2 * A), x2 = (-B - s) / (2 * A);
    const l1 = Math.abs(this.d1(x1)), l2 = Math.abs(this.d1(x2));
    return l1 < l2 ? { x: x1, lam: l1, stable: l1 < 1 } : { x: x2, lam: l2, stable: l2 < 1 };
  }
}

function classify(O, x0 = 0.5) {
  const orb = [x0]; const N = 28, esc = 80, eps = 5e-4;
  for (let i = 0; i < N; i++) { const xn = O.ev(orb[orb.length - 1]); orb.push(xn);
    if (!isFinite(xn) || Math.abs(xn) > esc) { if (i < 3) return { band: 0, orb }; if (i < 9) return { band: 1, orb }; return { band: 2, orb }; } }
  const t = orb.slice(-8);
  if (Math.abs(t[7] - t[6]) < eps) { const ci = orb.findIndex((x, i) => i > 2 && Math.abs(x - orb[i - 1]) < eps * 5);
    return ci > 0 && ci < 10 ? { band: 6, orb } : { band: 5, orb }; }
  if (Math.abs(t[7] - t[5]) < eps * 3 && Math.abs(t[6] - t[4]) < eps * 3) return { band: 4, orb };
  for (let p = 3; p <= 6; p++) if (orb.length > p + 2 && Math.abs(t[7] - t[7 - p]) < eps * 8) return { band: 4, orb };
  return { band: 3, orb };
}
function rootDist(O1, O2) {
  const r1 = O1.roots(), r2 = O2.roots();
  if (r1.re && r2.re) return Math.min(Math.abs(r1.r1 - r2.r1), Math.abs(r1.r1 - r2.r2), Math.abs(r1.r2 - r2.r1), Math.abs(r1.r2 - r2.r2));
  if (!r1.re && !r2.re) return Math.abs(r1.r1 - r2.r1) + Math.abs(r1.im - r2.im);
  return Math.abs(O1.vx() - O2.vx()) + Math.abs(O1.vy() - O2.vy()) * 0.5;
}
function mkCell(col, row) {
  const u = col / (COLS - 1), v = row / (ROWS - 1), cu = u - 0.5, cv = v - 0.5;
  const r = Math.sqrt(cu * cu + cv * cv), th = Math.atan2(cv, cu);
  const a = 0.8 * Math.cos(r * 3.5) * (1 + 0.5 * Math.sin(v * 7 * Math.PI));
  const b = (cu * 3.5 + cv * 2.0) * (1 + 0.3 * Math.cos(u * 5 * Math.PI));
  const c = 0.5 * Math.exp(-r * 2) + 0.15 * Math.sin(th * 4 + r * 3) + 0.1;
  const O = new Q(a, b, c), cl = classify(O);
  return { col, row, id: row * COLS + col, a0: a, b0: b, c0: c, a, b, c, O, D: O.D(), band: cl.band, orb: cl.orb, fp: O.fp(), nW: [] };
}
function gN(col, row) {
  const ns = []; for (let dr = -1; dr <= 1; dr++) for (let dc = -1; dc <= 1; dc++) {
    if (dr === 0 && dc === 0) continue; const nr = row + dr, nc = col + dc;
    if (nr >= 0 && nr < ROWS && nc >= 0 && nc < COLS) ns.push({ col: nc, row: nr }); } return ns;
}
function wireNeighbors(cells) {
  for (const cell of cells) { const gns = gN(cell.col, cell.row);
    cell.nW = gns.map(n => { const nc = cells[n.row * COLS + n.col]; return { id: nc.id, w: 1 / (1 + rootDist(cell.O, nc.O) * 0.5) }; }).sort((a, b) => b.w - a.w); }
}
function advSpine(spine, ph, tick) {
  const i = ph, p = spine[(i + 9) % 10], o = spine[i];
  const ops = [ () => p * (1 - σ) * 0.1, () => o * σ + p * (1 - σ), () => Math.abs(o - p) * σ + o * (1 - σ),
    () => o + (1 - o) * (1 - σ), () => o * σ, () => (o + spine.reduce((a, b) => a + b) / 10) / 2,
    () => o * σ, () => Math.sqrt(Math.max(.001, o * p)),  // removed stochastic for determinism
    () => o * (1 + .008 * Math.sin(tick * .1)), () => o * σ + Ts * (1 - σ) ];
  spine[i] = Math.max(.001, Math.min(1, ops[i]())); return (i + 1) % 10;
}
function modCells(cells, spine, ph, tick) {
  const sv = spine[ph];
  for (const cell of cells) { let { a, b, c } = cell;
    switch (ph) {
      case 0: a *= (1 - σs * sv); b *= (1 - σs * sv); c *= (1 - σs * sv); break;
      case 1: c = c * σ + (c + sv * 0.05) * σs; break;
      case 2: b = -b; break; case 3: b = Math.abs(b); break;
      case 4: a = -a; break; case 5: a = Math.abs(a); break;
      case 6: break;  // skip noise for deterministic test
      case 7: a = a * σ + sv * 0.2 * σs; break;
      case 8: b *= 1 + 0.004 * Math.sin(tick * 0.08); break;
      case 9: a = a * σ + cell.a0 * σs; b = b * σ + cell.b0 * σs; c = c * σ + cell.c0 * σs; break;
    }
    cell.a = a; cell.b = b; cell.c = c; cell.O = new Q(a, b, c); cell.D = cell.O.D();
  }
}

console.log("╔══════════════════════════════════════════════════════════════════╗");
console.log("║  CODEC FIDELITY — DETERMINISTIC LOSSLESS ROUND-TRIP            ║");
console.log("╚══════════════════════════════════════════════════════════════════╝");

// Run sim for 500 ticks (deterministic — no CHAOS noise)
const cells = []; for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) cells.push(mkCell(c, r));
let spine = new Array(10).fill(Ts), ph = 0;
for (let t = 0; t < 500; t++) { ph = advSpine(spine, ph, t); modCells(cells, spine, ph, t); }
// Classify at final state
for (const cell of cells) { const cl = classify(cell.O); cell.band = cl.band; cell.orb = cl.orb; cell.fp = cell.O.fp(); }
wireNeighbors(cells);

// ── COLLAPSE ──
const abc = [];
for (const c of cells) abc.push(c.a, c.b, c.c);
const spineSnap = [...spine];
const bytesF32 = abc.length * 4 + spineSnap.length * 4 + 3 * 4;  // Float32 binary
const bytesF64 = abc.length * 8 + spineSnap.length * 8 + 3 * 8;  // Float64 binary

console.log();
console.log("  ── COLLAPSE ──");
console.log(`  Cells: ${NC} | Coefficients: ${abc.length} (${abc.length/3} × 3)`);
console.log(`  Float32 binary: ${bytesF32.toLocaleString()} bytes (${(bytesF32/1024).toFixed(1)} KB)`);
console.log(`  Float64 binary: ${bytesF64.toLocaleString()} bytes (${(bytesF64/1024).toFixed(1)} KB)`);
console.log(`  Floppy (1.44 MB):`);
console.log(`    Float32: ${Math.floor(1474560 / bytesF32)} snapshots | max ${Math.floor(1474560 / 12).toLocaleString()} cells`);
console.log(`    Float64: ${Math.floor(1474560 / bytesF64)} snapshots | max ${Math.floor(1474560 / 24).toLocaleString()} cells`);
console.log();

// ── EXPAND ──
const rcells = []; for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) rcells.push(mkCell(c, r));
for (let i = 0; i < NC; i++) {
  const cell = rcells[i]; cell.a = abc[i*3]; cell.b = abc[i*3+1]; cell.c = abc[i*3+2];
  cell.O = new Q(cell.a, cell.b, cell.c); cell.D = cell.O.D();
}
for (const cell of rcells) { const cl = classify(cell.O); cell.band = cl.band; cell.orb = cl.orb; cell.fp = cell.O.fp(); }
wireNeighbors(rcells);

// ── VERIFY ──
let dOK = 0, bandOK = 0, fpOK = 0, topoOK = 0, rootsOK = 0, orbOK = 0;
let maxDerr = 0;
for (let i = 0; i < NC; i++) {
  const o = cells[i], r = rcells[i];
  const derr = Math.abs(o.D - r.D);
  if (derr > maxDerr) maxDerr = derr;
  if (derr < 1e-6) dOK++;
  if (o.band === r.band) bandOK++;
  const of_ = o.fp, rf = r.fp;
  if ((!of_ && !rf) || (of_ && rf && Math.abs(of_.x - rf.x) < 1e-6 && of_.stable === rf.stable)) fpOK++;
  if (o.nW.slice(0,3).map(n=>n.id).join(',') === r.nW.slice(0,3).map(n=>n.id).join(',')) topoOK++;
  const or_ = o.O.roots(), rr = r.O.roots();
  if (or_.re === rr.re && Math.abs(or_.r1 - rr.r1) < 1e-6) rootsOK++;
  // Compare final orbit value
  const oEnd = o.orb[o.orb.length-1], rEnd = r.orb[r.orb.length-1];
  if ((!isFinite(oEnd) && !isFinite(rEnd)) || Math.abs(oEnd - rEnd) < 1e-4) orbOK++;
}

console.log("  ── FIDELITY (lossless Float64) ──");
console.log(`    Δ (discriminant):    ${dOK}/${NC} (${(dOK/NC*100).toFixed(1)}%)  max err: ${maxDerr.toExponential(2)}`);
console.log(`    Roots:               ${rootsOK}/${NC} (${(rootsOK/NC*100).toFixed(1)}%)`);
console.log(`    Band classification: ${bandOK}/${NC} (${(bandOK/NC*100).toFixed(1)}%)`);
console.log(`    Fixed points:        ${fpOK}/${NC} (${(fpOK/NC*100).toFixed(1)}%)`);
console.log(`    Orbit convergence:   ${orbOK}/${NC} (${(orbOK/NC*100).toFixed(1)}%)`);
console.log(`    Topology (top-3):    ${topoOK}/${NC} (${(topoOK/NC*100).toFixed(1)}%)`);
console.log();

// Show what 3 numbers buy you
console.log("  ── COMPRESSION RATIO ──");
console.log("  STORED per cell:       3 values (a, b, c)");
console.log("  RECONSTRUCTED per cell:");
console.log("    1. Δ = b²−4ac (binding state)");
console.log("    2. root type (real/complex)");
console.log("    3. root 1 value");
console.log("    4. root 2 value (or imaginary part)");
console.log("    5. vertex x");
console.log("    6. vertex y (= min/max of O)");
console.log("    7. fixed point x*");
console.log("    8. stability λ = |O'(x*)|");
console.log("    9. stable? (λ < 1)");
console.log("   10. band (7-way classification)");
console.log("   11. orbit trajectory (28 values)");
console.log("   12. curvature = O''(x)/2 = a");
console.log("   13. first derivative O'(x) = 2ax+b");
console.log("   14. neighbor weight 1..8 (topology)");
console.log("   15. cobweb visualization path");
console.log("  ─────────────────────────────────────");
console.log("  3 in → 15+ out = 5× expansion minimum");
console.log("  3 in → 28 orbit + 8 neighbors = 12× with dynamics");
console.log();

// Float32 degradation test
console.log("  ── FLOAT32 DEGRADATION ──");
const abc32 = new Float32Array(abc);
const rcells32 = []; for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) rcells32.push(mkCell(c, r));
for (let i = 0; i < NC; i++) {
  const cell = rcells32[i]; cell.a = abc32[i*3]; cell.b = abc32[i*3+1]; cell.c = abc32[i*3+2];
  cell.O = new Q(cell.a, cell.b, cell.c); cell.D = cell.O.D();
}
for (const cell of rcells32) { const cl = classify(cell.O); cell.band = cl.band; cell.fp = cell.O.fp(); }
wireNeighbors(rcells32);
let band32 = 0, topo32 = 0;
for (let i = 0; i < NC; i++) {
  if (cells[i].band === rcells32[i].band) band32++;
  if (cells[i].nW.slice(0,3).map(n=>n.id).join(',') === rcells32[i].nW.slice(0,3).map(n=>n.id).join(',')) topo32++;
}
console.log(`  Float32 band fidelity:     ${band32}/${NC} (${(band32/NC*100).toFixed(1)}%)`);
console.log(`  Float32 topology fidelity: ${topo32}/${NC} (${(topo32/NC*100).toFixed(1)}%)`);
console.log(`  Trade-off: half the bytes, ${(100 - band32/NC*100).toFixed(1)}% band noise`);
console.log();
console.log("══════════════════════════════════════════════════════════════════");
console.log("  Store coefficients. Reconstruct reality.");
console.log("  The quadratic IS the codec. The quadratic IS the decompressor.");
console.log("══════════════════════════════════════════════════════════════════");
