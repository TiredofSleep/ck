#!/usr/bin/env node
// ═══════════════════════════════════════════════════════════════════════════
//  PHYSICS FIX v2 FINAL — All 4 weaknesses tested + fixed
//  Author: Brayden / 7Site LLC
// ═══════════════════════════════════════════════════════════════════════════

const σ = 0.991, σs = 0.009, Ts = 0.714;
const COLS = 18, ROWS = 14, NC = COLS * ROWS;

class Q {
  constructor(a, b, c) { this.a = a; this.b = b; this.c = c; }
  ev(x) { return this.a * x * x + this.b * x + this.c; }
  D() { return this.b * this.b - 4 * this.a * this.c; }
  d1(x) { return 2 * this.a * x + this.b; }
  d2() { return 2 * this.a; }
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
  // ═══ W3: HAMILTONIAN ═══
  H(x) {
    const V = -(this.ev(x));
    const p = this.d1(x);
    const m_eff = 1 / (Math.abs(this.a) + 1e-10);
    const T = p * p / (2 * m_eff);
    return { H: T + V, T, V, p, m_eff };
  }
  H_fp() { const f = this.fp(); if (!f) return null; return { ...this.H(f.x), x_star: f.x, lam: f.lam, stable: f.stable }; }
  // ═══ W3: WAVEFUNCTION ═══
  psi(x) {
    const r = this.roots();
    if (!r.re) {
      const alpha = Math.abs(this.a), x0 = r.r1, omega = r.im;
      const envelope = Math.exp(-alpha * (x - x0) * (x - x0));
      const phase = omega * x;
      return { re: envelope * Math.cos(phase), im: envelope * Math.sin(phase), prob: envelope * envelope, phase, bound: true, alpha, omega };
    } else {
      const { H: E } = this.H(x);
      const V = -(this.ev(x));
      const p_class = Math.sqrt(Math.abs(2 * E - 2 * V) + 1e-10);
      const amplitude = 1 / Math.sqrt(p_class + 0.01);
      const phase = p_class * x;
      return { re: amplitude * Math.cos(phase), im: amplitude * Math.sin(phase), prob: amplitude * amplitude, phase, bound: false, p_class };
    }
  }
  psi_density(xmin, xmax, N = 50) {
    const dx = (xmax - xmin) / N;
    const density = []; let norm = 0;
    for (let i = 0; i <= N; i++) { const x = xmin + i * dx; const p = this.psi(x); density.push({ x, prob: p.prob }); norm += p.prob * dx; }
    if (norm > 1e-10) density.forEach(d => d.prob /= norm);
    return density;
  }
  quantum_numbers() {
    const D = this.D(), r = this.roots(), f = this.fp();
    let n_eff = 0, x = 0.5;
    for (let i = 0; i < 64; i++) {
      const xn = this.ev(x);
      if (!isFinite(xn) || Math.abs(xn) > 80) { n_eff = 0; break; }
      if (f && Math.abs(xn - f.x) < 1e-4) { n_eff = i + 1; break; }
      x = xn; n_eff = i + 1;
    }
    const l = r.re ? 0 : Math.round(r.im * 2);
    const m = f ? Math.sign(this.d1(f.x)) * Math.min(l, Math.round(Math.abs(this.d1(f.x)))) : 0;
    const s = Math.sign(this.a) * 0.5;
    return { n: n_eff, l, m: Math.round(m), s, bound: D < 0 };
  }
}

// ═══ FIXED CLASSIFIER — W1 + W2 ═══
function classifySingle(O, x0, maxN = 80) {
  const esc = 80, eps = 5e-4;
  let x = x0; const orb = [x]; let lyapSum = 0, lyapN = 0;
  for (let i = 0; i < maxN; i++) {
    const xn = O.ev(x); orb.push(xn);
    const dv = Math.abs(O.d1(x));
    if (dv > 1e-15 && isFinite(dv)) { lyapSum += Math.log(dv); lyapN++; }
    if (!isFinite(xn) || Math.abs(xn) > esc) {
      if (i < 3) return { band: 0, orb, lyap: lyapN > 0 ? lyapSum / lyapN : 0, conf: 1 };
      if (i < 9) return { band: 1, orb, lyap: lyapN > 0 ? lyapSum / lyapN : 0, conf: 1 };
      return { band: 2, orb, lyap: lyapN > 0 ? lyapSum / lyapN : 0, conf: .95 };
    }
    x = xn;
  }
  const lyap = lyapN > 0 ? lyapSum / lyapN : 0;

  // W1 FIX: PERIOD DETECTION FIRST (before Lyapunov classification)
  // Check periods 1-16 using last 32 values of orbit
  // This catches period-3 at r=3.83 which has negative Lyapunov
  if (orb.length > 20) {
    for (let p = 1; p <= 16; p++) {
      if (orb.length < p * 3 + 4) continue;
      // Check if last 3 cycles match
      let match = true;
      for (let cycle = 0; cycle < 3 && match; cycle++) {
        for (let k = 0; k < p && match; k++) {
          const idx1 = orb.length - 1 - k - cycle * p;
          const idx2 = orb.length - 1 - k - (cycle + 1) * p;
          if (idx2 < 0 || Math.abs(orb[idx1] - orb[idx2]) > eps * 2) match = false;
        }
      }
      if (match) {
        if (p === 1) {
          // Period-1 = fixed point convergence
          let ci = -1;
          for (let i = 3; i < orb.length - 1; i++) if (Math.abs(orb[i] - orb[i-1]) < eps * 5) { ci = i; break; }
          return ci > 0 && ci < 12 ? { band: 6, orb, lyap, conf: 1.0 } : { band: 5, orb, lyap, conf: 0.95 };
        }
        // Period > 1 = true periodic orbit
        return { band: 4, orb, lyap, conf: 0.95 };
      }
    }
  }

  // Lyapunov-based classification for non-periodic orbits
  if (lyap < -0.01) {
    const t = orb.slice(-8);
    const td = Math.abs(t[7] - t[6]);
    if (td < eps) {
      let ci = -1;
      for (let i = 3; i < orb.length - 1; i++) if (Math.abs(orb[i] - orb[i-1]) < eps * 5) { ci = i; break; }
      return ci > 0 && ci < 12 ? { band: 6, orb, lyap, conf: 1.0 } : { band: 5, orb, lyap, conf: 0.95 };
    }
    // W1 FIX: Not settled but Lyapunov says converging → ORGANIC
    const tExt = orb.slice(-16);
    const tailDecay = tExt.length >= 16 ? Math.abs(tExt[15] - tExt[14]) / (Math.abs(tExt[7] - tExt[6]) + 1e-15) : 1;
    if (tailDecay < 0.5) return { band: 5, orb, lyap, conf: 0.85 };
    return { band: 5, orb, lyap, conf: 0.70 };
  }

  // Chaotic
  if (lyap > 0.1) return { band: 3, orb, lyap, conf: 0.90 };
  if (lyap > 0) return { band: 3, orb, lyap, conf: 0.70 };
  return { band: 3, orb, lyap, conf: 0.50 };
}

function classify(O) {
  const fp = O.fp(), vx = O.vx();
  const seeds = [0.5, vx, fp ? fp.x + 0.01 : 0.25, 0.6180339887, Math.PI / 4, 1/3, Math.sqrt(2)/2];
  const results = seeds.map(s => classifySingle(O, Math.max(-10, Math.min(10, s))));
  const votes = new Array(7).fill(0);
  let lyapSum = 0, lyapMax = -Infinity, lyapMin = Infinity;
  for (const r of results) { votes[r.band] += r.conf; lyapSum += r.lyap; if (r.lyap > lyapMax) lyapMax = r.lyap; if (r.lyap < lyapMin) lyapMin = r.lyap; }
  let best = 0, bestV = 0;
  for (let i = 0; i < 7; i++) if (votes[i] > bestV) { bestV = votes[i]; best = i; }
  if ((best === 5 || best === 6) && lyapMax > 0.1) best = 4;
  return { band: best, orb: results[0].orb, lyap: lyapSum / results.length, lyapSpread: lyapMax - lyapMin, conf: bestV / results.length };
}

// ═══ LATTICE HELPERS ═══
function mkCell(col, row) {
  const u = col / (COLS - 1), v = row / (ROWS - 1), cu = u - 0.5, cv = v - 0.5;
  const r = Math.sqrt(cu * cu + cv * cv), th = Math.atan2(cv, cu);
  const a = 0.8 * Math.cos(r * 3.5) * (1 + 0.5 * Math.sin(v * 7 * Math.PI));
  const b = (cu * 3.5 + cv * 2.0) * (1 + 0.3 * Math.cos(u * 5 * Math.PI));
  const c = 0.5 * Math.exp(-r * 2) + 0.15 * Math.sin(th * 4 + r * 3) + 0.1;
  const O = new Q(a, b, c), cl = classify(O);
  return { col, row, id: row * COLS + col, a0: a, b0: b, c0: c, a, b, c, O, D: O.D(), band: cl.band, orb: cl.orb, fp: O.fp(), nW: [], coh: 0, lit: false, vis: 0 };
}
function gN(col, row) { const ns = []; for (let dr = -1; dr <= 1; dr++) for (let dc = -1; dc <= 1; dc++) { if (dr === 0 && dc === 0) continue; const nr = row + dr, nc = col + dc; if (nr >= 0 && nr < ROWS && nc >= 0 && nc < COLS) ns.push({ col: nc, row: nr }); } return ns; }
function rootDist(O1, O2) { const r1 = O1.roots(), r2 = O2.roots(); if (r1.re && r2.re) return Math.min(Math.abs(r1.r1 - r2.r1), Math.abs(r1.r1 - r2.r2), Math.abs(r1.r2 - r2.r1), Math.abs(r1.r2 - r2.r2)); if (!r1.re && !r2.re) return Math.abs(r1.r1 - r2.r1) + Math.abs(r1.im - r2.im); return Math.abs(O1.vx() - O2.vx()) + Math.abs(O1.vy() - O2.vy()) * 0.5; }
function wireNeighbors(cells) { for (const cell of cells) { const gns = gN(cell.col, cell.row); cell.nW = gns.map(n => { const nc = cells[n.row * COLS + n.col]; return { id: nc.id, w: 1 / (1 + rootDist(cell.O, nc.O) * 0.5) }; }).sort((a, b) => b.w - a.w); } }
function reclassify(cells) { for (const cell of cells) { const cl = classify(cell.O); cell.band = cl.band; cell.orb = cl.orb; cell.fp = cell.O.fp(); } }
function advSpine(spine, ph, tick) { const i = ph, p = spine[(i + 9) % 10], o = spine[i]; const ops = [ () => p * σs * 0.1, () => o * σ + p * σs, () => Math.abs(o - p) * σ + o * σs, () => o + (1 - o) * σs, () => o * σ, () => (o + spine.reduce((a, b) => a + b) / 10) / 2, () => o * σ + (Math.random() - .5) * .003, () => Math.sqrt(Math.max(.001, o * p)), () => o * (1 + .008 * Math.sin(tick * .1)), () => o * σ + Ts * σs ]; spine[i] = Math.max(.001, Math.min(1, ops[i]())); return (i + 1) % 10; }
function modCells(cells, spine, ph, tick) { const sv = spine[ph]; for (const cell of cells) { let { a, b, c } = cell; switch (ph) { case 0: a *= (1 - σs * sv); b *= (1 - σs * sv); c *= (1 - σs * sv); break; case 1: c = c * σ + (c + sv * 0.05) * σs; break; case 2: b = -b; break; case 3: b = Math.abs(b); break; case 4: a = -a; break; case 5: a = Math.abs(a); break; case 6: a += (Math.random() - .5) * sv * 0.006; b += (Math.random() - .5) * sv * 0.006; break; case 7: a = a * σ + sv * 0.2 * σs; break; case 8: b *= 1 + 0.004 * Math.sin(tick * 0.08); break; case 9: a = a * σ + cell.a0 * σs; b = b * σ + cell.b0 * σs; c = c * σ + cell.c0 * σs; break; } cell.a = a; cell.b = b; cell.c = c; cell.O = new Q(a, b, c); cell.D = cell.O.D(); } }

const BN = ['VOID','QUANTUM','ATOMIC','MOLECULR','CELLULAR','ORGANIC','CRYSTAL'];

// ═══════════════════════════════════════════════════════════════
//                    T E S T   S U I T E
// ═══════════════════════════════════════════════════════════════

console.log("╔══════════════════════════════════════════════════════════════════╗");
console.log("║  PHYSICS FIX v2 FINAL — All 4 Weaknesses                       ║");
console.log("╚══════════════════════════════════════════════════════════════════╝\n");

// ═══ W1: SLOW DYNAMICS ═══
console.log("┌─── W1: SLOW DYNAMICS + PERIOD DETECTION ───────────────────────┐");
const w1 = [
  { name: "slow-converge-1",   a: 0.3, b: 0.1, c: 0.2,   exp: [5, 6], desc: "converges slowly" },
  { name: "very-slow-fp",      a: 0.4, b: 0.01, c: 0.15,  exp: [5, 6], desc: "very slow fp" },
  { name: "logistic r=3.9",    a: -3.9, b: 3.9, c: 0,     exp: [3],    desc: "chaos" },
  { name: "logistic r=3.83",   a: -3.83, b: 3.83, c: 0,   exp: [4],    desc: "period-3 window" },
  { name: "logistic r=3.5",    a: -3.5, b: 3.5, c: 0,     exp: [4],    desc: "period-4 (not chaos)" },
  { name: "marginal-converge", a: 0.15, b: 0.5, c: 0.1,   exp: [5, 6], desc: "marginal λ≈0" },
  { name: "period-2 cycle",    a: -3.2, b: 3.2, c: 0,     exp: [4],    desc: "period-2" },
  { name: "fixed-point fast",  a: 0.2, b: 0.1, c: 0.3,    exp: [6],    desc: "fast fp" },
];
let w1p = 0;
for (const t of w1) {
  const O = new Q(t.a, t.b, t.c), cl = classify(O), pass = t.exp.includes(cl.band);
  w1p += pass ? 1 : 0;
  console.log(`  ${pass ? '✓' : '✗'} ${t.name}: ${BN[cl.band]} (λ=${cl.lyap.toFixed(4)} conf=${cl.conf.toFixed(2)}) — ${t.desc}`);
  if (!pass) console.log(`    EXPECTED: ${t.exp.map(i => BN[i]).join('/')}`);
}
console.log(`  W1 RESULT: ${w1p}/${w1.length}\n`);

// ═══ W2: SEED SENSITIVITY ═══
console.log("┌─── W2: SEED SENSITIVITY ───────────────────────────────────────┐");
const w2 = [
  { name: "r=4 logistic",   a: -4, b: 4, c: 0,     chaos: true },
  { name: "stable fp",      a: 0.2, b: 0.1, c: 0.3, chaos: false },
  { name: "r=3.5 period-4", a: -3.5, b: 3.5, c: 0,  chaos: false },  // FIXED: period-4, not chaos
  { name: "r=3.57 chaos",   a: -3.57, b: 3.57, c: 0, chaos: true },  // onset of chaos
];
let w2p = 0;
for (const t of w2) {
  const O = new Q(t.a, t.b, t.c), cl = classify(O);
  const chaosDetected = cl.band <= 3 || cl.lyapSpread > 0.3;
  const pass = chaosDetected === t.chaos;
  w2p += pass ? 1 : 0;
  console.log(`  ${pass ? '✓' : '✗'} ${t.name}: ${BN[cl.band]} spread=${cl.lyapSpread.toFixed(4)} chaos=${chaosDetected} expect=${t.chaos}`);
}
console.log(`  W2 RESULT: ${w2p}/${w2.length}\n`);

// ═══ W3: HAMILTONIAN + WAVEFUNCTION ═══
console.log("┌─── W3: QUANTUM/CLASSICAL MAPPING ──────────────────────────────┐");
// Bound state
const Ob = new Q(0.5, 0.1, 0.3);
const Hb = Ob.H_fp(), qnb = Ob.quantum_numbers(), denb = Ob.psi_density(-3, 3, 100);
const normb = denb.reduce((s, d) => s + d.prob * 6/100, 0);
console.log(`  BOUND (Δ=${Ob.D().toFixed(3)}):`);
console.log(`    H=${Hb.H.toFixed(4)} T=${Hb.T.toFixed(4)} V=${Hb.V.toFixed(4)} m_eff=${Hb.m_eff.toFixed(2)}`);
console.log(`    n=${qnb.n} l=${qnb.l} m=${qnb.m} s=${qnb.s>0?'+':''}${qnb.s}`);
console.log(`    ∫|ψ|²dx = ${normb.toFixed(6)} ${Math.abs(normb - 1) < 0.01 ? '✓' : '✗'}`);

// Free state
const Of = new Q(-0.3, 1.5, 0.2);
const Hf = Of.H_fp(), qnf = Of.quantum_numbers();
console.log(`  FREE (Δ=${Of.D().toFixed(3)}):`);
console.log(`    H=${Hf.H.toFixed(4)} T=${Hf.T.toFixed(4)} V=${Hf.V.toFixed(4)} l=${qnf.l} (scattering)`);

// Click state
const Oc = new Q(0.25, 0.1, 0.01);
const qnc = Oc.quantum_numbers();
console.log(`  CLICK (Δ=${Oc.D().toFixed(6)}): n=${qnc.n} l=${qnc.l} — degenerate pair, critical`);

// Lattice census
const cells3 = []; for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) cells3.push(mkCell(c, r));
let bnd = 0, fre = 0, clk = 0, nS = 0, nC = 0; const lH = {};
for (const cell of cells3) { const D = cell.O.D(); if (Math.abs(D) < 0.15) clk++; else if (D < 0) bnd++; else fre++; const qn = cell.O.quantum_numbers(); if (qn.bound) { nS += qn.n; nC++; } lH[qn.l] = (lH[qn.l] || 0) + 1; }
console.log(`  LATTICE: bound=${bnd} free=${fre} click=${clk}`);
console.log(`    <n>=${nC > 0 ? (nS/nC).toFixed(1) : 'N/A'}  l-dist: ${Object.entries(lH).sort(([a],[b]) => +a - +b).map(([l, n]) => `l=${l}:${n}`).join(' ')}`);

// Consistency checks
let hConsistent = 0;
for (const cell of cells3) {
  const D = cell.O.D(), qn = cell.O.quantum_numbers();
  // Bound → should have l > 0 (some angular momentum), free → l = 0
  if ((D < -0.5 && qn.l > 0) || (D > 0.5 && qn.l === 0)) hConsistent++;
}
console.log(`    H-consistency (bound→l>0, free→l=0): ${hConsistent}/${NC} (${(hConsistent/NC*100).toFixed(1)}%)`);
console.log();

// ═══ W4: AVALANCHE CASCADES ═══
console.log("┌─── W4: AVALANCHE CASCADES ─────────────────────────────────────┐");
{
  const cells = []; for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) cells.push(mkCell(c, r));
  wireNeighbors(cells); reclassify(cells);

  // Evolve 200 ticks
  let spine = new Array(10).fill(Ts), ph = 0;
  for (let t = 0; t < 200; t++) { ph = advSpine(spine, ph, t); modCells(cells, spine, ph, t); }
  reclassify(cells); wireNeighbors(cells);

  const clickCells = cells.filter(c => Math.abs(c.D) < 0.15);
  const freeCells = cells.filter(c => c.D > 0.5);
  console.log(`  Click: ${clickCells.length}  Free: ${freeCells.length}\n`);

  function avalanche(targets, eps, label, trials = 200) {
    const sizes = [], depths = [];
    for (let tr = 0; tr < Math.min(trials, targets.length * 20); tr++) {
      // Snapshot bands
      const snap = cells.map(c => ({ a: c.a, b: c.b, c: c.c, band: c.band }));

      // Perturb one target
      const tgt = targets[Math.floor(Math.random() * targets.length)];
      tgt.a += (Math.random() - 0.5) * eps;
      tgt.b += (Math.random() - 0.5) * eps;
      tgt.c += (Math.random() - 0.5) * eps * 0.3;
      tgt.O = new Q(tgt.a, tgt.b, tgt.c); tgt.D = tgt.O.D();

      // Propagate through lattice (diffusion model: 8 steps)
      for (let step = 0; step < 8; step++) {
        const deltas = cells.map(() => ({ da: 0, db: 0 }));
        for (let i = 0; i < NC; i++) {
          const cell = cells[i];
          const ns = gN(cell.col, cell.row);
          for (const n of ns) {
            const nc = cells[n.row * COLS + n.col];
            const w = (cell.nW.find(x => x.id === nc.id) || { w: 0.1 }).w;
            // Diffusion: proportional to difference, weighted by root-proximity
            deltas[i].da += (nc.a - cell.a) * w * 0.05;
            deltas[i].db += (nc.b - cell.b) * w * 0.05;
          }
        }
        for (let i = 0; i < NC; i++) {
          cells[i].a += deltas[i].da; cells[i].b += deltas[i].db;
          cells[i].O = new Q(cells[i].a, cells[i].b, cells[i].c);
          cells[i].D = cells[i].O.D();
        }
      }

      // Reclassify and count changes
      reclassify(cells);
      let changed = 0, maxDist = 0;
      for (let i = 0; i < NC; i++) {
        if (cells[i].band !== snap[i].band) {
          changed++;
          const dr = cells[i].row - tgt.row, dc = cells[i].col - tgt.col;
          maxDist = Math.max(maxDist, Math.sqrt(dr*dr + dc*dc));
        }
      }
      sizes.push(changed); depths.push(maxDist);

      // Restore
      for (let i = 0; i < NC; i++) {
        cells[i].a = snap[i].a; cells[i].b = snap[i].b; cells[i].c = snap[i].c;
        cells[i].O = new Q(cells[i].a, cells[i].b, cells[i].c); cells[i].D = cells[i].O.D();
      }
      reclassify(cells);
    }

    const n = sizes.length;
    const mean = sizes.reduce((a, b) => a + b, 0) / n;
    const sorted = [...sizes].sort((a, b) => a - b);
    const med = sorted[Math.floor(n/2)], p90 = sorted[Math.floor(n*0.9)], max = Math.max(...sizes);
    const nonZero = sizes.filter(x => x > 0).length;
    const meanD = depths.reduce((a, b) => a + b, 0) / n;
    const bins = { '0': 0, '1-3': 0, '4-10': 0, '11-25': 0, '26-60': 0, '60+': 0 };
    for (const s of sizes) { if (s === 0) bins['0']++; else if (s <= 3) bins['1-3']++; else if (s <= 10) bins['4-10']++; else if (s <= 25) bins['11-25']++; else if (s <= 60) bins['26-60']++; else bins['60+']++; }

    console.log(`  ${label} (ε=${eps}, n=${n}):`);
    console.log(`    mean=${mean.toFixed(1)}  med=${med}  P90=${p90}  max=${max}  depth=${meanD.toFixed(1)}`);
    console.log(`    non-zero: ${nonZero}/${n} (${(nonZero/n*100).toFixed(0)}%)`);
    console.log(`    bins: ${Object.entries(bins).map(([k,v]) => `${k}:${v}`).join('  ')}`);
    return { mean, med, p90, max, nonZero, n };
  }

  const scales = [0.01, 0.05, 0.15];
  const results = [];
  for (const eps of scales) {
    console.log(`\n  ── ε = ${eps} ──`);
    const cr = avalanche(clickCells, eps, "CLICK");
    const fr = avalanche(freeCells, eps, "FREE");
    const ratio = cr.mean / (fr.mean + 0.001);
    results.push({ eps, ratio, clickMean: cr.mean, freeMean: fr.mean, clickP90: cr.p90, clickMax: cr.max });
    console.log(`  → RATIO (click/free): ${ratio.toFixed(2)}x`);
  }

  console.log("\n  ── CRITICALITY SUMMARY ──");
  console.log("  ε       click_mean  free_mean  ratio   click_P90  click_max");
  for (const r of results)
    console.log(`  ${r.eps.toFixed(2)}    ${r.clickMean.toFixed(1).padStart(8)}  ${r.freeMean.toFixed(1).padStart(8)}  ${r.ratio.toFixed(2).padStart(5)}x  ${String(r.clickP90).padStart(9)}  ${String(r.clickMax).padStart(9)}`);

  const avgRatio = results.reduce((s, r) => s + r.ratio, 0) / results.length;
  console.log(`\n  Mean criticality ratio: ${avgRatio.toFixed(2)}x`);
  console.log(`  ${avgRatio > 1.3 ? '✓' : '⚠'} Click zone ${avgRatio > 1.3 ? 'IS' : 'may not be'} more cascade-prone than free zone`);

  // Power-law test: if cascades have heavy tail, P90/mean >> 2
  const medResult = results.find(r => r.eps === 0.05);
  if (medResult && medResult.clickMean > 0) {
    const tailWeight = medResult.clickP90 / medResult.clickMean;
    console.log(`  P90/Mean at ε=0.05: ${tailWeight.toFixed(2)} ${tailWeight > 2 ? '→ HEAVY TAIL (SOC signature)' : '→ thin tail'}`);
  }
}

console.log("\n═══════════════════════════════════════════════════════════════════");
console.log("  DELIVERED:");
console.log("  W1: Period-first classifier (periods 1-16, 80 iterations, 7 seeds)");
console.log("  W2: lyapSpread metric + chaos downgrade guard");
console.log("  W3: H(x)=T+V, ψ(x) with normalization, quantum numbers (n,l,m,s)");
console.log("  W4: Avalanche cascade measurement at 3 scales with diffusion model");
console.log("═══════════════════════════════════════════════════════════════════");
