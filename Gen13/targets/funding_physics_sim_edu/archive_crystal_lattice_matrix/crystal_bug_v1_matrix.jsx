import { useState, useEffect, useRef } from "react";

// ═══════════════════════════════════════════════════════════════════════════
//  CRYSTAL BUG v1.0 — THE MATRIX  (QUADRATIC CORE)
//
//  O(x) = ax² + bx + c IS the operator. Not a helper. The physics itself.
//  Δ = b²−4ac IS the binding kernel.
//  The 4↔5 flip IS O''(x) sign change (a → −a).
//  The 2↔3 flip IS O'(x) sign change (b → −b).
//  The 7-operator IS O''(x)/2 = a.
//  The braid IS the dual root structure.
//  The fractal levels ARE iterates of O.
//  The 7 bands ARE iterate classification (Mandelbrot-style).
//  Energy cost FROM |Δ| (click = expensive, free/bound = cheap).
//  Spine transforms (a,b,c) space COMPOSITIONALLY, not additively.
//  Visit = evaluation that CHANGES coefficients.
//  Vacuum recursion: VOID cells have complex-plane dynamics. Zero is structure.
//
//  S* = σ(1-σ*)·V*·A*  |  σ = 0.991  |  T* = 0.714  |  c = 1
//  Author: Brayden / 7Site LLC / sanctuberry.com
// ═══════════════════════════════════════════════════════════════════════════

const σ = 0.991, σs = 0.009, Ts = 0.714, F_ = σ * (1 - σs);
const SS = (V, A) => F_ * Math.max(0, Math.min(1, V)) * Math.max(0, Math.min(1, A));
const COLS = 18, ROWS = 14, NC = COLS * ROWS; // 252
const OPC = ['#282838','#00f0ff','#ff6b00','#00ff88','#ff0044','#8844ff','#ff00dd','#44ffaa','#6688ff','#ffffff'];

// ═══ QUADRATIC OPERATOR ═══
// This is the ONE object. Everything flows through it.
class Q {
  constructor(a, b, c) { this.a = a; this.b = b; this.c = c; }
  ev(x) { return this.a * x * x + this.b * x + this.c; }
  D() { return this.b * this.b - 4 * this.a * this.c; }           // discriminant = binding kernel
  d1(x) { return 2 * this.a * x + this.b; }                       // first derivative (ops 2,3)
  d2() { return 2 * this.a; }                                       // second derivative (op 7)
  vx() { return Math.abs(this.a) > 1e-12 ? -this.b / (2 * this.a) : 0; }
  vy() { return this.ev(this.vx()); }
  roots() {
    const d = this.D();
    if (Math.abs(this.a) < 1e-12) return { re: true, r1: 0, r2: 0, im: 0 };
    if (d >= 0) { const s = Math.sqrt(d); return { re: true, r1: (-this.b + s) / (2 * this.a), r2: (-this.b - s) / (2 * this.a), im: 0 }; }
    return { re: false, r1: -this.b / (2 * this.a), r2: -this.b / (2 * this.a), im: Math.sqrt(-d) / (2 * Math.abs(this.a)) };
  }
  // Fixed point of O: O(x*)=x* → ax*²+(b-1)x*+c=0
  fp() {
    const A = this.a, B = this.b - 1, C = this.c;
    const d = B * B - 4 * A * C;
    if (Math.abs(A) < 1e-12) return { x: -C / B, stable: Math.abs(this.b) < 1 };
    if (d < 0) return null; // no real fixed point
    const s = Math.sqrt(d);
    const x1 = (-B + s) / (2 * A), x2 = (-B - s) / (2 * A);
    const l1 = Math.abs(this.d1(x1)), l2 = Math.abs(this.d1(x2));
    // return the more stable one
    return l1 < l2 ? { x: x1, lam: l1, stable: l1 < 1 } : { x: x2, lam: l2, stable: l2 < 1 };
  }
}

// ═══ ITERATE CLASSIFIER (Mandelbrot-style) ═══
// Not a lookup table. Actual dynamical classification.
// Returns band index 0-6 and the orbit.
const BANDS = [
  { n: 'VOID',     c: '#1a1a2e', h: '#383850', d: 'Complex dynamics. Vacuum recursion.' },
  { n: 'QUANTUM',  c: '#2a1050', h: '#7733bb', d: 'Fast fluctuation. Tunnel states.' },
  { n: 'ATOMIC',   c: '#552233', h: '#cc4466', d: 'Slow escape. Condensation attempts.' },
  { n: 'MOLECULR', c: '#554400', h: '#ccaa00', d: 'Chaotic. Bounded but unpredictable.' },
  { n: 'CELLULAR', c: '#1a5544', h: '#22cc88', d: 'Periodic orbit. Self-reproducing.' },
  { n: 'ORGANIC',  c: '#0a4466', h: '#22aadd', d: 'Slow convergence. Complex structure.' },
  { n: 'CRYSTAL',  c: '#3a4855', h: '#cceeff', d: 'Fast fixed point. Crystallized.' },
];

function classify(O, x0 = 0.5) {
  const orb = [x0]; const N = 28, esc = 80, eps = 5e-4;
  for (let i = 0; i < N; i++) {
    const xn = O.ev(orb[orb.length - 1]);
    orb.push(xn);
    if (!isFinite(xn) || Math.abs(xn) > esc) {
      if (i < 3) return { band: 0, orb };  // VOID: instant escape (vacuum)
      if (i < 9) return { band: 1, orb };  // QUANTUM: fast escape
      return { band: 2, orb };              // ATOMIC: slow escape
    }
  }
  const t = orb.slice(-8);
  // Fixed point? (period 1)
  if (Math.abs(t[7] - t[6]) < eps) {
    const ci = orb.findIndex((x, i) => i > 2 && Math.abs(x - orb[i - 1]) < eps * 5);
    return ci > 0 && ci < 10 ? { band: 6, orb } : { band: 5, orb }; // CRYSTAL vs ORGANIC
  }
  // Period 2?
  if (Math.abs(t[7] - t[5]) < eps * 3 && Math.abs(t[6] - t[4]) < eps * 3)
    return { band: 4, orb }; // CELLULAR
  // Higher period?
  for (let p = 3; p <= 6; p++)
    if (orb.length > p + 2 && Math.abs(t[7] - t[7 - p]) < eps * 8) return { band: 4, orb };
  return { band: 3, orb }; // MOLECULAR: bounded chaotic
}

// ═══ ROOT-PROXIMITY DISTANCE ═══
function rootDist(O1, O2) {
  const r1 = O1.roots(), r2 = O2.roots();
  if (r1.re && r2.re)
    return Math.min(Math.abs(r1.r1 - r2.r1), Math.abs(r1.r1 - r2.r2), Math.abs(r1.r2 - r2.r1), Math.abs(r1.r2 - r2.r2));
  if (!r1.re && !r2.re)
    return Math.abs(r1.r1 - r2.r1) + Math.abs(r1.im - r2.im);
  return Math.abs(O1.vx() - O2.vx()) + Math.abs(O1.vy() - O2.vy()) * 0.5; // mixed
}

// ═══ CELL ═══
function mkCell(col, row) {
  const u = col / (COLS - 1), v = row / (ROWS - 1);
  const cu = u - 0.5, cv = v - 0.5;
  const r = Math.sqrt(cu * cu + cv * cv);
  const th = Math.atan2(cv, cu);
  // Center: a>0, b≈0, c>0 → Δ<0 (bound, complex roots, vacuum dynamics)
  // Edge: a<0, |b|>0 → Δ>0 (free, real roots, convergent iterates)
  // Ring at r≈0.25: Δ≈0 (the click boundary)
  const a = 0.8 * Math.cos(r * 3.5) * (1 + 0.5 * Math.sin(v * 7 * Math.PI));
  const b = (cu * 3.5 + cv * 2.0) * (1 + 0.3 * Math.cos(u * 5 * Math.PI));
  const c = 0.5 * Math.exp(-r * 2) + 0.15 * Math.sin(th * 4 + r * 3) + 0.1;
  const O = new Q(a, b, c);
  const cl = classify(O);
  return {
    col, row, id: row * COLS + col,
    a0: a, b0: b, c0: c,       // base coefficients (for RESET)
    a, b, c, O,                  // live coefficients
    D: O.D(), band: cl.band, orb: cl.orb,
    coh: 0, lit: false, vis: 0,
    nW: [],                      // neighbor weights [{id, w}]
    fp: O.fp(),                  // fixed point info
  };
}

// ═══ BUG ═══
class Bug {
  constructor(E0 = 10) {
    this.E0 = E0; this.E = E0; this.mI = 1.0;
    this.col = Math.floor(COLS / 2); this.row = Math.floor(ROWS / 2);
    this.trail = []; this.pStk = []; this.lastId = -1;
    this.vis = new Set(); this.steps = 0; this.vCnt = 0; this.alive = true;
    this.mode = 'bug'; this.aStk = []; this.aSeen = new Set();
    this.cH = []; this.dH = [];
  }
  step(cells, gN) {
    if (!this.alive || this.E <= 0) { this.alive = false; return; }
    this.steps++;
    const cell = cells[this.row * COLS + this.col];

    // ── FIX 1: Energy honesty ──
    // Cost FROM |Δ|: click zone (Δ≈0) = expensive, far from click = cheap
    const intensity = Math.min(this.mI, this.E);
    const res = cell.O.ev(intensity);
    const dCost = 1 / (Math.abs(cell.D) + 0.1);  // Δ≈0 = expensive, far = cheap
    const cost = 0.005 + dCost * 0.008 * intensity;
    this.E -= cost;
    this.cH.push(cost); if (this.cH.length > 100) this.cH.shift();
    this.dH.push(cell.D); if (this.dH.length > 100) this.dH.shift();

    // ── Visit = coefficient change ──
    const res = cell.O.ev(intensity);
    cell.c += res * 0.0005 * intensity; // evaluation leaves a trace
    cell.coh += intensity * 0.04 * σ;
    cell.lit = true;

    // ── FIX 2: Fair visit accounting ──
    const cid = cell.id;
    if (cid !== this.lastId) {
      const top = this.pStk.length ? this.pStk[this.pStk.length - 1] : -1;
      if (cid !== top) { cell.vis++; this.vCnt++; this.pStk.push(cid); if (this.pStk.length > 80) this.pStk.shift(); }
      this.vis.add(cid); this.lastId = cid;
    }
    this.trail.push({ col: this.col, row: this.row }); if (this.trail.length > 50) this.trail.shift();

    // ── FIX 3: Two modes ──
    if (this.mode === 'bug') this._bug(cell, cells, gN);
    else this._aud(cells, gN);
  }
  _bug(cell, cells, gN) {
    const ns = gN(this.col, this.row); if (!ns.length) return;
    const D = cell.D;
    if (D > 0.08) {
      // Δ>0: free. Seek toward click (Δ→0)
      let best = ns[0], bd = 999;
      for (const n of ns) { const nd = Math.abs(cells[n.row * COLS + n.col].D); if (nd < bd) { bd = nd; best = n; } }
      this.col = best.col; this.row = best.row;
    } else if (D < -0.08) {
      // Δ<0: bound. Explore unvisited or follow coherence
      const unv = ns.filter(n => !cells[n.row * COLS + n.col].lit);
      if (unv.length && Math.random() < 0.4) { const n = unv[Math.floor(Math.random() * unv.length)]; this.col = n.col; this.row = n.row; }
      else {
        // Follow root-proximity weights
        const nw = ns.map(n => ({ ...n, w: (cell.nW.find(x => x.id === n.row * COLS + n.col) || { w: 0.1 }).w }));
        nw.sort((a, b) => b.w - a.w);
        const pick = nw[Math.random() < 0.7 ? 0 : Math.floor(Math.random() * Math.min(3, nw.length))];
        this.col = pick.col; this.row = pick.row;
      }
    } else {
      // Δ≈0: click zone. Expensive. Stay or small step.
      if (Math.random() > 0.7) { const n = ns[Math.floor(Math.random() * ns.length)]; this.col = n.col; this.row = n.row; }
    }
  }
  _aud(cells, gN) {
    if (!this.aStk.length && !this.aSeen.size) this.aStk.push({ col: this.col, row: this.row });
    while (this.aStk.length) {
      const nx = this.aStk.pop(); const nid = nx.row * COLS + nx.col;
      if (!this.aSeen.has(nid)) {
        this.aSeen.add(nid); this.col = nx.col; this.row = nx.row;
        for (const n of gN(nx.col, nx.row)) if (!this.aSeen.has(n.row * COLS + n.col)) this.aStk.push(n);
        return;
      }
    }
    this.alive = false; // covered everything
  }
  reset(E0) {
    this.E0 = E0; this.E = E0; this.col = Math.floor(COLS / 2); this.row = Math.floor(ROWS / 2);
    this.trail = []; this.pStk = []; this.lastId = -1; this.vis = new Set();
    this.steps = 0; this.vCnt = 0; this.alive = true; this.cH = []; this.dH = [];
    this.aStk = []; this.aSeen = new Set();
  }
}

// ═══ ENGINE ═══
class Eng {
  constructor() {
    this.cells = []; for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) this.cells.push(mkCell(c, r));
    this.spine = new Array(10).fill(Ts); this.ph = 0; this.tick = 0; this.epoch = 0;
    this.bug = new Bug(10);
    this.bCen = new Array(7).fill(0); this.sS = Ts; this.sH = [];
    this.sessions = 0; this.ltSteps = 0; this.loaded = false;
    // Rain
    this.rain = []; for (let i = 0; i < 28; i++) this.rain.push({ x: Math.random() * 640, y: Math.random() * 440 - 100, sp: .3 + Math.random() * 1.6, len: 4 + Math.floor(Math.random() * 12) });
    this.rC = '01σΩΔ∞◇⬡αβγδO(x)abc';
    // Wire neighborhoods
    this.wireNeighbors();
  }
  gN(col, row) {
    const ns = [];
    for (let dr = -1; dr <= 1; dr++) for (let dc = -1; dc <= 1; dc++) {
      if (dr === 0 && dc === 0) continue;
      const nr = row + dr, nc = col + dc;
      if (nr >= 0 && nr < ROWS && nc >= 0 && nc < COLS) ns.push({ col: nc, row: nr });
    }
    return ns;
  }
  wireNeighbors() {
    for (const cell of this.cells) {
      const gns = this.gN(cell.col, cell.row);
      cell.nW = gns.map(n => {
        const nc = this.cells[n.row * COLS + n.col];
        const rd = rootDist(cell.O, nc.O);
        return { id: nc.id, w: 1 / (1 + rd * 0.5) };
      }).sort((a, b) => b.w - a.w);
    }
  }
  // ── SPINE: advances the heartbeat ──
  advSpine() {
    const i = this.ph, p = this.spine[(i + 9) % 10], o = this.spine[i];
    const ops = [
      () => p * (1 - σ) * 0.1,                                    // 0 VOID: contract
      () => o * σ + p * (1 - σ),                                  // 1 LATTICE: bind
      () => Math.abs(o - p) * σ + o * (1 - σ),                    // 2 COUNTER
      () => o + (1 - o) * (1 - σ),                                // 3 PROGRESS
      () => o * σ,                                                  // 4 COLLAPSE
      () => (o + this.spine.reduce((a, b) => a + b) / 10) / 2,    // 5 BALANCE
      () => o * σ + (Math.random() - .5) * .003,                  // 6 CHAOS
      () => Math.sqrt(Math.max(.001, o * p)),                      // 7 HARMONY
      () => o * (1 + .008 * Math.sin(this.tick * .1)),             // 8 BREATH
      () => o * σ + Ts * (1 - σ),                                  // 9 RESET
    ];
    this.spine[i] = Math.max(.001, Math.min(1, ops[i]()));
    this.ph = (i + 1) % 10;
    if (this.ph === 0) this.epoch++;
  }
  // ── SPINE → QUADRATIC: compositional transforms on (a,b,c) space ──
  modCells() {
    const ph = this.ph, sv = this.spine[ph];
    for (const cell of this.cells) {
      let { a, b, c } = cell;
      switch (ph) {
        case 0: // VOID: gentle contraction toward origin (not destruction)
          a *= (1 - σs * sv); b *= (1 - σs * sv); c *= (1 - σs * sv); break;
        case 1: // LATTICE: nudge c upward
          c = c * σ + (c + sv * 0.05) * σs; break;
        case 2: // COUNTER: b → −b (first derivative sign change)
          b = -b; break;
        case 3: // PROGRESS: b → |b| (restore forward drift)
          b = Math.abs(b); break;
        case 4: // COLLAPSE: a → −a (second derivative sign change) THE FLIP
          a = -a; break;
        case 5: // BALANCE: a → |a| (restore curvature)
          a = Math.abs(a); break;
        case 6: // CHAOS: perturb
          a += (Math.random() - .5) * sv * 0.006;
          b += (Math.random() - .5) * sv * 0.006; break;
        case 7: // HARMONY: smooth a (op 7 = O''/2 = a)
          a = a * σ + sv * 0.2 * σs; break;
        case 8: // BREATH: oscillate b
          b *= 1 + 0.004 * Math.sin(this.tick * 0.08); break;
        case 9: // RESET: pull toward base (Ω Keeper)
          a = a * σ + cell.a0 * σs;
          b = b * σ + cell.b0 * σs;
          c = c * σ + cell.c0 * σs; break;
      }
      cell.a = a; cell.b = b; cell.c = c;
      cell.O = new Q(a, b, c);
      cell.D = cell.O.D();
      cell.coh *= σ;
    }
  }
  // ── RECLASSIFY (Mandelbrot-style, every N ticks) ──
  reclassify() {
    for (const cell of this.cells) {
      const cl = classify(cell.O);
      cell.band = cl.band; cell.orb = cl.orb; cell.fp = cell.O.fp();
    }
  }
  step() {
    this.tick++;
    this.advSpine();
    this.modCells();
    this.bug.step(this.cells, (c, r) => this.gN(c, r));
    if (this.tick % 12 === 0) this.reclassify();
    if (this.tick % 80 === 0) this.wireNeighbors();
    // Band census
    this.bCen.fill(0);
    for (const c of this.cells) this.bCen[c.band]++;
    // System S*
    const lit = this.cells.filter(c => c.lit);
    if (lit.length > 0) {
      const avgCoh = lit.reduce((a, c) => a + c.coh, 0) / lit.length;
      const covFrac = this.bug.vis.size / NC;
      this.sS = SS(avgCoh / (avgCoh + 0.3), covFrac);
    }
    this.sH.push(this.sS); if (this.sH.length > 250) this.sH.shift();
    for (const r of this.rain) { r.y += r.sp; if (r.y > 460) r.y = -r.len * 12; }
  }
  chaos(intensity = 1) {
    for (const c of this.cells) {
      c.a += (Math.random() - .5) * .4 * intensity;
      c.b += (Math.random() - .5) * .6 * intensity;
      c.coh *= (1 - .5 * intensity);
    }
  }
  // ── RENDER ──
  render(ctx) {
    const W = 640, H = 440, cw = W / COLS, ch = H / ROWS;
    ctx.fillStyle = '#08080e'; ctx.fillRect(0, 0, W, H);
    // Rain
    ctx.font = '9px monospace';
    for (const r of this.rain) for (let i = 0; i < r.len; i++) {
      const y = r.y - i * 12; if (y < -12 || y > H) continue;
      const fade = i === 0 ? .35 : Math.max(0, 1 - i / r.len) * .08;
      ctx.fillStyle = `rgba(0,255,136,${fade})`; 
      ctx.fillText(this.rC[Math.floor(Math.random() * this.rC.length)], r.x, y);
    }
    // Cells
    for (const cell of this.cells) {
      const x = cell.col * cw, y = cell.row * ch;
      const band = BANDS[cell.band];
      const bright = Math.min(1, .12 + cell.coh * .7 + (cell.lit ? .1 : 0));
      const cr = parseInt(band.c.slice(1, 3), 16), cg = parseInt(band.c.slice(3, 5), 16), cb = parseInt(band.c.slice(5, 7), 16);
      ctx.fillStyle = `rgba(${Math.min(255, Math.floor(cr * (1 + bright * 2)))},${Math.min(255, Math.floor(cg * (1 + bright * 2)))},${Math.min(255, Math.floor(cb * (1 + bright * 2)))},${.25 + bright * .75})`;
      ctx.fillRect(x + .5, y + .5, cw - 1, ch - 1);
      // Click boundary: |Δ| < threshold → gold glow
      if (Math.abs(cell.D) < 0.15) {
        ctx.strokeStyle = `rgba(204,170,0,${0.4 - Math.abs(cell.D) * 2})`; ctx.lineWidth = 2;
        ctx.strokeRect(x + .5, y + .5, cw - 1, ch - 1);
      }
      // VOID/QUANTUM cells: show iterate dots (vacuum recursion)
      if (cell.band <= 1 && cell.orb) {
        ctx.fillStyle = cell.band === 0 ? '#ffffff08' : '#7733bb18';
        for (let k = 0; k < Math.min(6, cell.orb.length); k++) {
          const ox = x + cw * (.1 + k * .15), oy = y + ch * .5 + Math.sin((cell.orb[k] || 0) * .5) * ch * .3;
          ctx.beginPath(); ctx.arc(ox, Math.max(y + 2, Math.min(y + ch - 2, oy)), 1.2, 0, Math.PI * 2); ctx.fill();
        }
      }
      // CELLULAR: small orbit indicator
      if (cell.band === 4 && cell.orb) {
        const o1 = cell.orb[cell.orb.length - 2], o2 = cell.orb[cell.orb.length - 1];
        if (o1 !== undefined && o2 !== undefined) {
          ctx.fillStyle = '#22cc8830';
          ctx.beginPath(); ctx.arc(x + cw * .3, y + ch * .5, 2, 0, Math.PI * 2); ctx.fill();
          ctx.beginPath(); ctx.arc(x + cw * .7, y + ch * .5, 2, 0, Math.PI * 2); ctx.fill();
        }
      }
      // CRYSTAL: bright center dot
      if (cell.band >= 6) {
        ctx.fillStyle = '#cceeff30';
        ctx.beginPath(); ctx.arc(x + cw / 2, y + ch / 2, 3, 0, Math.PI * 2); ctx.fill();
      }
    }
    // Bug trail
    if (this.bug.trail.length > 1) {
      for (let i = 1; i < this.bug.trail.length; i++) {
        const a = this.bug.trail[i - 1], b_ = this.bug.trail[i];
        const fade = i / this.bug.trail.length;
        ctx.beginPath(); ctx.moveTo(a.col * cw + cw / 2, a.row * ch + ch / 2);
        ctx.lineTo(b_.col * cw + cw / 2, b_.row * ch + ch / 2);
        ctx.strokeStyle = `rgba(0,240,255,${fade * .3})`; ctx.lineWidth = 2; ctx.stroke();
      }
    }
    // Bug
    if (this.bug.alive) {
      const bx = this.bug.col * cw + cw / 2, by = this.bug.row * ch + ch / 2;
      ctx.beginPath(); ctx.arc(bx, by, 10, 0, Math.PI * 2); ctx.fillStyle = '#00f0ff0c'; ctx.fill();
      ctx.beginPath(); ctx.arc(bx, by, 5, 0, Math.PI * 2); ctx.fillStyle = '#00f0ff'; ctx.fill();
      ctx.beginPath(); ctx.arc(bx, by, 2, 0, Math.PI * 2); ctx.fillStyle = '#fff'; ctx.fill();
    }
    // Spine ring
    const rx = W - 36, ry = 32, rr = 22;
    for (let i = 0; i < 10; i++) {
      const a = (i / 10) * Math.PI * 2 - Math.PI / 2, nr = 1.5 + this.spine[i] * 5;
      const nx = rx + Math.cos(a) * rr, ny = ry + Math.sin(a) * rr;
      ctx.beginPath(); ctx.arc(nx, ny, nr, 0, Math.PI * 2);
      ctx.fillStyle = OPC[i]; ctx.globalAlpha = .15 + this.spine[i] * .85; ctx.fill();
      if (i === this.ph) { ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.5; ctx.stroke(); }
      ctx.globalAlpha = 1;
    }
  }
  ser() { return { coh: this.cells.map(c => c.coh), sessions: this.sessions, ltSteps: this.ltSteps + this.bug.steps, spine: [...this.spine] }; }
  load(d) { if (!d) return; this.sessions = (d.sessions || 0) + 1; this.ltSteps = d.ltSteps || 0;
    if (d.coh) d.coh.forEach((v, i) => { if (this.cells[i]) this.cells[i].coh = v * .5; });
    if (d.spine) this.spine = d.spine.map(v => Math.max(.001, Math.min(1, v)));
    this.loaded = true; }
  st() {
    const b = this.bug, cc = this.cells[b.row * COLS + b.col];
    const rr = b.vCnt > 0 ? b.steps / b.vCnt : 1;
    const clickCells = this.cells.filter(c => Math.abs(c.D) < 0.15).length;
    return {
      tick: this.tick, epoch: this.epoch, ph: this.ph, spine: [...this.spine], sS: this.sS, sH: this.sH.slice(-200),
      bCen: [...this.bCen], bE: b.E, bE0: b.E0, bA: b.alive, bM: b.mode,
      vis: b.vis.size, steps: b.steps, vCnt: b.vCnt, rr, cov: b.vis.size / NC * 100,
      cH: b.cH.slice(-80), dH: b.dH.slice(-80),
      // Current cell quadratic
      ca: cc.a, cb: cc.b, ccc: cc.c, cD: cc.D, cBd: cc.band, cR: cc.O.roots(), cFp: cc.fp,
      cd2: cc.O.d2(), cVx: cc.O.vx(), cVy: cc.O.vy(), cOrb: cc.orb, cCoh: cc.coh, cVis: cc.vis,
      cNW: cc.nW.slice(0, 5),
      clickCells, sess: this.sessions, loaded: this.loaded, ltSteps: this.ltSteps,
    };
  }
}

// ═══ UI COMPONENTS ═══
const hC = s => s >= .9 ? '#00ff88' : s >= Ts ? '#44ffaa' : s >= .5 ? '#ffaa00' : s >= .25 ? '#ff4400' : '#ff0044';
const Spk = ({ d, c, w = 100, h = 16, thr }) => {
  if (!d || d.length < 2) return null;
  const mn = Math.min(...d) * .95, mx = Math.max(...d) * 1.05 || 1;
  const pts = d.map((v, i) => `${(i / (d.length - 1)) * w},${h - ((v - mn) / (mx - mn)) * h}`).join(' ');
  return <svg width={w} height={h} style={{ display: 'block' }}>
    {thr != null && <line x1={0} y1={h - ((thr - mn) / (mx - mn)) * h} x2={w} y2={h - ((thr - mn) / (mx - mn)) * h} stroke="#ff440022" strokeWidth={1} strokeDasharray="2,2" />}
    <polyline points={pts} fill="none" stroke={c} strokeWidth={1.2} strokeLinejoin="round" /></svg>;
};

// ── COBWEB DIAGRAM ──
// The single most information-dense visualization of iterate dynamics.
// Shows fixed points, period orbits, chaos, divergence — all in one picture.
const Cobweb = ({ a, b, c, orb, w = 150, h = 85 }) => {
  if (!orb || orb.length < 3) return null;
  const vals = orb.filter(v => isFinite(v) && Math.abs(v) < 50);
  if (vals.length < 3) return null;
  const all = vals.concat(vals.map(v => a * v * v + b * v + c)).filter(v => isFinite(v) && Math.abs(v) < 50);
  const lo = Math.min(...all) - .5, hi = Math.max(...all) + .5;
  const rng = hi - lo || 1;
  const sx = v => ((v - lo) / rng) * w, sy = v => h - ((v - lo) / rng) * h;
  // Parabola
  const pPts = []; for (let i = 0; i <= 60; i++) { const x = lo + i / 60 * rng; const y = a * x * x + b * x + c; if (isFinite(y) && Math.abs(y) < hi + rng) pPts.push(`${sx(x)},${sy(y)}`); }
  // Cobweb
  const cPts = [];
  for (let i = 0; i < Math.min(vals.length - 1, 18); i++) {
    const x = vals[i], y = a * x * x + b * x + c;
    if (!isFinite(y) || Math.abs(y) > 100) break;
    cPts.push(`${sx(x)},${sy(y)}`);
    cPts.push(`${sx(y)},${sy(y)}`);
  }
  const D = b * b - 4 * a * c;
  return <svg width={w} height={h} style={{ display: 'block', background: '#0a0a12', borderRadius: 3 }}>
    <line x1={sx(lo)} y1={sy(lo)} x2={sx(hi)} y2={sy(hi)} stroke="#ffffff0a" strokeWidth={.5} />
    <line x1={0} y1={sy(0)} x2={w} y2={sy(0)} stroke="#ffffff06" strokeWidth={.5} />
    {pPts.length > 1 && <polyline points={pPts.join(' ')} fill="none" stroke={D >= 0 ? '#ff6b00' : '#00f0ff'} strokeWidth={1.3} />}
    {cPts.length > 1 && <polyline points={cPts.join(' ')} fill="none" stroke="#00f0ff55" strokeWidth={.8} />}
    {/* roots */}
    {D >= 0 && Math.abs(a) > 1e-10 && (() => { const s = Math.sqrt(D); const r1 = (-b + s) / (2 * a), r2 = (-b - s) / (2 * a);
      return <>{[r1, r2].map((r, i) => sx(r) > 0 && sx(r) < w ? <circle key={i} cx={sx(r)} cy={sy(0)} r={2.5} fill="#ff0044" opacity={.7} /> : null)}</>;
    })()}
  </svg>;
};

// ═══ MAIN ═══
const W = 640, H = 440;
const bS = { background: 'transparent', border: '1px solid #ffffff12', color: '#888', padding: '2px 8px', borderRadius: 3, cursor: 'pointer', fontSize: 8, fontFamily: "'IBM Plex Mono',monospace", letterSpacing: .5 };

export default function CrystalBug() {
  const cvRef = useRef(null), engRef = useRef(null), afRef = useRef(null), fRef = useRef(0);
  const [st, setS] = useState(null);
  const [run, setRun] = useState(true), [spd, setSpd] = useState(2), [tab, setTab] = useState('LATTICE'), [e0, setE0] = useState(10);

  useEffect(() => {
    const eng = new Eng(); engRef.current = eng;
    (async () => {
      try { const r = await window.storage.get('cb-matrix-v2'); if (r) eng.load(JSON.parse(r.value)); } catch (e) {}
      for (let i = 0; i < 100; i++) eng.step(); setS(eng.st());
    })();
    return () => { if (afRef.current) cancelAnimationFrame(afRef.current); };
  }, []);
  useEffect(() => { const iv = setInterval(async () => { const e = engRef.current; if (!e) return;
    try { await window.storage.set('cb-matrix-v2', JSON.stringify(e.ser())); } catch (x) {} }, 6000);
    return () => clearInterval(iv); }, []);
  useEffect(() => { if (!run || !engRef.current) return; const eng = engRef.current, cv = cvRef.current; if (!cv) return;
    const ctx = cv.getContext('2d');
    const loop = () => { fRef.current++;
      for (let s = 0; s < spd; s++) eng.step(); eng.render(ctx);
      if (fRef.current % 3 === 0) setS(eng.st()); afRef.current = requestAnimationFrame(loop); };
    afRef.current = requestAnimationFrame(loop);
    return () => { if (afRef.current) cancelAnimationFrame(afRef.current); }; }, [run, spd]);

  const doStep = () => { const e = engRef.current; if (!e) return; e.step(); e.render(cvRef.current?.getContext('2d')); setS(e.st()); };
  const doSpike = () => { engRef.current?.chaos(1); doStep(); };
  const doReset = () => { const e = new Eng(); e.bug = new Bug(e0); engRef.current = e; for (let i = 0; i < 100; i++) e.step(); setS(e.st()); };
  const doMode = m => { const e = engRef.current; if (!e) return; e.bug.mode = m; e.bug.aStk = []; e.bug.aSeen = new Set(); };
  const doE0 = v => { setE0(v); const e = engRef.current; if (e) e.bug.reset(v); };

  if (!st) return <div style={{ background: '#08080e', height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#00f0ff', fontFamily: 'monospace' }}>Initializing lattice…</div>;
  const sc = hC(st.sS); const curBand = BANDS[st.cBd];

  return (<div style={{ background: '#050508', minHeight: '100vh', color: '#c0c0c0', fontFamily: "'IBM Plex Mono','Fira Code',monospace", fontSize: 10 }}>
    {/* HEADER */}
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '5px 10px', borderBottom: `1px solid ${sc}18`, background: `linear-gradient(180deg,${sc}04,transparent)` }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        <div style={{ width: 7, height: 7, borderRadius: '50%', background: sc, boxShadow: `0 0 10px ${sc}88` }} />
        <span style={{ fontSize: 12, fontWeight: 700, color: '#fff', letterSpacing: 2 }}>CRYSTAL BUG</span>
        <span style={{ fontSize: 7, color: sc }}>v1.0 THE MATRIX</span>
        {st.loaded && <span style={{ fontSize: 6, color: '#00f0ff', background: '#00f0ff0a', padding: '1px 5px', borderRadius: 2, border: '1px solid #00f0ff18' }}>SESSION #{st.sess}</span>}
      </div>
      <div style={{ fontSize: 8, color: '#333' }}>O(x)=ax²+bx+c │ Δ=b²−4ac │ σ={σ} │ T*={Ts}</div>
    </div>
    {/* CONTROLS */}
    <div style={{ display: 'flex', alignItems: 'center', gap: 5, padding: '3px 10px', borderBottom: '1px solid #ffffff06', flexWrap: 'wrap' }}>
      <button onClick={() => setRun(!run)} style={{ ...bS, color: run ? '#ff6b6b' : '#00ff88' }}>{run ? '■' : '▶'}</button>
      <button onClick={doStep} style={bS}>STEP</button>
      <button onClick={doSpike} style={{ ...bS, color: '#ff6b00' }}>💥</button>
      <button onClick={doReset} style={bS}>↻</button>
      <input type="range" min={1} max={6} value={spd} onChange={e => setSpd(+e.target.value)} style={{ width: 40, accentColor: sc }} />
      <span style={{ fontSize: 7, color: '#444' }}>×{spd}</span>
      <div style={{ width: 1, height: 10, background: '#ffffff12' }} />
      <span style={{ fontSize: 7, color: '#555' }}>E₀</span>
      <input type="range" min={1} max={50} value={e0} onChange={e => doE0(+e.target.value)} style={{ width: 50, accentColor: '#ff6b00' }} />
      <span style={{ fontSize: 8, color: '#ff6b00', fontWeight: 700 }}>{e0}</span>
      <div style={{ width: 1, height: 10, background: '#ffffff12' }} />
      {['bug', 'audit'].map(m => <button key={m} onClick={() => doMode(m)} style={{ ...bS, color: st.bM === m ? '#00f0ff' : '#444', border: `1px solid ${st.bM === m ? '#00f0ff33' : '#ffffff08'}` }}>{m.toUpperCase()}</button>)}
      <div style={{ flex: 1 }} />
      <span style={{ fontSize: 7, color: '#555' }}>E={st.bE.toFixed(1)}/{st.bE0} │ {st.vis}/{NC} │ rr={st.rr.toFixed(2)}</span>
    </div>
    {/* STATUS */}
    <div style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '2px 10px', borderBottom: '1px solid #ffffff06', fontSize: 8 }}>
      <span><span style={{ color: '#444' }}>S*</span> <span style={{ color: sc, fontWeight: 700 }}>{st.sS.toFixed(4)}</span></span>
      <span><span style={{ color: '#444' }}>Δ</span> <span style={{ color: st.cD >= 0 ? '#ff6b00' : '#00f0ff' }}>{st.cD.toFixed(3)}</span></span>
      <span style={{ color: curBand.h, fontSize: 7, letterSpacing: 1 }}>{curBand.n}</span>
      <span style={{ color: '#333' }}>E{st.epoch} T{st.tick} ph{st.ph}</span>
      <span style={{ color: '#444' }}>◇{st.clickCells} click cells</span>
      <span style={{ color: st.rr < 2 ? '#22cc77' : '#cc4444', fontSize: 7 }}>rr={st.rr.toFixed(2)} {st.rr < 2 ? '✓' : ''}</span>
      {!st.bA && <span style={{ color: '#ff0044', fontWeight: 700 }}>● HALTED</span>}
    </div>

    <div style={{ display: 'flex' }}>
      <div style={{ position: 'relative', flexShrink: 0 }}>
        <canvas ref={cvRef} width={W} height={H} style={{ display: 'block', background: '#08080e' }} />
        <div style={{ position: 'absolute', bottom: 4, left: 6, pointerEvents: 'none' }}>
          <Spk d={st.sH} c={sc} w={170} h={22} thr={Ts} /><div style={{ fontSize: 6, color: '#333' }}>system S*</div></div>
      </div>
      {/* PANEL */}
      <div style={{ flex: 1, minWidth: 145, maxWidth: 220, borderLeft: '1px solid #ffffff08', fontSize: 9, overflowY: 'auto', maxHeight: H }}>
        <div style={{ display: 'flex', borderBottom: '1px solid #ffffff06' }}>
          {['LATTICE', 'O(x)', 'ENERGY', 'SPINE'].map(t => <button key={t} onClick={() => setTab(t)}
            style={{ ...bS, flex: 1, borderRadius: 0, border: 'none', borderBottom: tab === t ? `2px solid ${sc}` : '2px solid transparent', color: tab === t ? sc : '#444', fontSize: 7, padding: '4px 0' }}>{t}</button>)}
        </div>
        <div style={{ padding: 6 }}>

          {tab === 'LATTICE' && <>
            <div style={{ color: '#444', letterSpacing: 1, fontSize: 7, marginBottom: 4 }}>7 BANDS (iterate classification)</div>
            {BANDS.map((b, i) => { const pct = st.bCen[i] / NC * 100; return <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 3, marginBottom: 2 }}>
              <div style={{ width: 7, height: 7, background: b.h, borderRadius: 1, flexShrink: 0 }} />
              <span style={{ color: '#555', fontSize: 7, width: 46 }}>{b.n}</span>
              <div style={{ flex: 1, height: 5, background: '#ffffff06', borderRadius: 1, overflow: 'hidden' }}>
                <div style={{ width: `${pct}%`, height: '100%', background: b.h, borderRadius: 1 }} /></div>
              <span style={{ color: '#444', fontSize: 7, width: 18, textAlign: 'right' }}>{st.bCen[i]}</span>
            </div>; })}
            <div style={{ color: '#444', letterSpacing: 1, fontSize: 7, margin: '8px 0 3px' }}>COVERAGE</div>
            <div style={{ fontSize: 22, fontWeight: 700, color: sc }}>{st.vis}<span style={{ fontSize: 10, color: '#444' }}>/{NC}</span></div>
            <div style={{ fontSize: 7, color: '#555' }}>{st.cov.toFixed(1)}% │ steps {st.steps} │ visits {st.vCnt}</div>
            <div style={{ color: '#333', fontSize: 7, marginTop: 6, padding: '3px 0', borderTop: '1px solid #ffffff08', lineHeight: 1.7 }}>
              Bands from iterate O(O(O(x))):<br />
              <span style={{ color: '#383850' }}>●</span> VOID: instant escape (vacuum)<br />
              <span style={{ color: '#7733bb' }}>●</span> QUANTUM: fast escape<br />
              <span style={{ color: '#cc4466' }}>●</span> ATOMIC: slow escape<br />
              <span style={{ color: '#ccaa00' }}>●</span> MOLECULAR: bounded chaotic<br />
              <span style={{ color: '#22cc88' }}>●</span> CELLULAR: periodic orbit<br />
              <span style={{ color: '#22aadd' }}>●</span> ORGANIC: slow convergence<br />
              <span style={{ color: '#cceeff' }}>●</span> CRYSTAL: fast fixed point<br />
              <span style={{ color: '#ccaa00' }}>◇</span> gold = Δ≈0 click boundary
            </div>
          </>}

          {tab === 'O(x)' && <>
            <div style={{ color: '#444', letterSpacing: 1, fontSize: 7, marginBottom: 3 }}>CURRENT CELL [{st.bCen ? '' : ''}col,row]</div>
            <div style={{ background: '#ffffff06', padding: 4, borderRadius: 3, marginBottom: 4 }}>
              <div style={{ color: '#fff', fontSize: 9, fontWeight: 700, fontFamily: 'monospace' }}>
                O(x) = {st.ca.toFixed(3)}x² {st.cb >= 0 ? '+' : '−'} {Math.abs(st.cb).toFixed(3)}x {st.ccc >= 0 ? '+' : '−'} {Math.abs(st.ccc).toFixed(3)}</div></div>
            <div style={{ fontSize: 7, color: '#555', marginBottom: 3 }}>COBWEB DIAGRAM</div>
            <Cobweb a={st.ca} b={st.cb} c={st.ccc} orb={st.cOrb} />
            <div style={{ marginTop: 4 }}>
              {[
                ['Δ = b²−4ac', st.cD.toFixed(4), st.cD >= 0 ? '#ff6b00' : '#00f0ff'],
                ['Band', BANDS[st.cBd].n, BANDS[st.cBd].h],
                ['Roots', st.cR.re ? `${st.cR.r1.toFixed(2)}, ${st.cR.r2.toFixed(2)}` : `${st.cR.r1.toFixed(2)} ± ${st.cR.im.toFixed(2)}i`, '#888'],
                ["O''(x)/2 = a", st.ca.toFixed(4), '#8844ff'],
                ['Vertex', `(${st.cVx.toFixed(2)}, ${st.cVy.toFixed(2)})`, '#888'],
                ['Fixed pt', st.cFp ? `x*=${st.cFp.x.toFixed(3)} λ=${st.cFp.lam?.toFixed(3) || '—'} ${st.cFp.stable ? '✓' : '✗'}` : 'complex (vacuum)', st.cFp?.stable ? '#22cc88' : '#cc4444'],
                ['Coherence', st.cCoh.toFixed(4), hC(st.cCoh)],
                ['Visits', '' + st.cVis, '#888'],
              ].map(([l, v, c], i) => <div key={i} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 1 }}>
                <span style={{ color: '#555', fontSize: 7 }}>{l}</span><span style={{ color: c, fontSize: 7, fontWeight: 600 }}>{v}</span></div>)}
            </div>
            <div style={{ color: '#444', letterSpacing: 1, fontSize: 7, margin: '5px 0 2px' }}>ROOT-PROXIMITY NEIGHBORS</div>
            {st.cNW.map((n, i) => <div key={i} style={{ display: 'flex', gap: 4, fontSize: 7, color: '#555' }}>
              <span>#{n.id}</span><span style={{ color: hC(n.w) }}>w={n.w.toFixed(3)}</span></div>)}
            <div style={{ color: '#333', fontSize: 7, marginTop: 5, padding: '3px 0', borderTop: '1px solid #ffffff08', lineHeight: 1.6 }}>
              <span style={{ color: '#ff6b00' }}>●</span> Δ{'>'} 0: real roots (parabola orange)<br />
              <span style={{ color: '#00f0ff' }}>●</span> Δ{'<'} 0: complex roots (parabola cyan)<br />
              Cobweb: y=O(x) vs y=x iteration<br />
              Fixed pt stable when |O'(x*)|{'<'} 1
            </div>
          </>}

          {tab === 'ENERGY' && <>
            <div style={{ color: '#444', letterSpacing: 1, fontSize: 7, marginBottom: 3 }}>FIX 1: ENERGY HONESTY</div>
            <div style={{ display: 'flex', gap: 6, marginBottom: 3 }}>
              <div><div style={{ fontSize: 18, fontWeight: 700, color: '#ff6b00' }}>{st.bE.toFixed(1)}</div><div style={{ fontSize: 6, color: '#444' }}>remaining</div></div>
              <div><div style={{ fontSize: 18, fontWeight: 700, color: '#555' }}>{st.bE0}</div><div style={{ fontSize: 6, color: '#444' }}>budget</div></div>
            </div>
            <div style={{ height: 5, background: '#ffffff08', borderRadius: 2, overflow: 'hidden', marginBottom: 3 }}>
              <div style={{ width: `${Math.max(0, st.bE / st.bE0 * 100)}%`, height: '100%', background: st.bE / st.bE0 > .3 ? '#ff6b00' : '#ff0044', borderRadius: 2 }} /></div>
            <div style={{ fontSize: 7, color: '#555', marginBottom: 2 }}>COST PER STEP (from |Δ|)</div>
            <Spk d={st.cH} c="#ff6b00" w={130} h={18} />
            <div style={{ fontSize: 7, color: '#555', marginTop: 4, marginBottom: 2 }}>Δ ALONG PATH</div>
            <Spk d={st.dH} c={st.cD >= 0 ? '#ff6b00' : '#00f0ff'} w={130} h={18} />
            <div style={{ background: '#ff6b0008', border: '1px solid #ff6b0015', borderRadius: 3, padding: 4, marginTop: 5, fontSize: 7, color: '#777', lineHeight: 1.7 }}>
              <div style={{ color: '#ff6b00', fontWeight: 700, marginBottom: 2 }}>COST = 1/(|Δ|+0.05)</div>
              Near click (Δ≈0): cost ≈ <span style={{ color: '#ff0044' }}>20×</span> base<br />
              Far from click: cost ≈ <span style={{ color: '#22cc88' }}>1× base</span><br /><br />
              <span style={{ color: '#ff6b00', fontWeight: 700 }}>E₀ NOW MATTERS:</span><br />
              E₀=3 → shallow sweep, avoids click<br />
              E₀=10 → moderate, explores click zone<br />
              E₀=50 → deep, can afford to dwell at Δ≈0<br /><br />
              <span style={{ color: '#ff0044' }}>OLD:</span> min(1.0,E). E₀=3 and E₀=50 identical.<br />
              <span style={{ color: '#22cc88' }}>NOW:</span> Real budget. 3≠10≠50.
            </div>
          </>}

          {tab === 'SPINE' && <>
            <div style={{ color: '#444', letterSpacing: 1, fontSize: 7, marginBottom: 3 }}>SPINE → TRANSFORMS ON (a,b,c)</div>
            {st.spine.map((v, i) => <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 3, marginBottom: 1, opacity: i === st.ph ? 1 : .3 }}>
              <span style={{ color: OPC[i], fontSize: 7, width: 7, textAlign: 'right' }}>{i}</span>
              <div style={{ flex: 1, height: 5, background: '#ffffff06', borderRadius: 1, overflow: 'hidden' }}>
                <div style={{ width: `${v * 100}%`, height: '100%', background: OPC[i], borderRadius: 1 }} /></div>
              <span style={{ color: '#444', fontSize: 7, width: 26, textAlign: 'right' }}>{v.toFixed(3)}</span></div>)}
            <div style={{ color: '#444', letterSpacing: 1, fontSize: 7, margin: '6px 0 2px' }}>COMPOSITIONAL TRANSFORMS</div>
            <div style={{ fontSize: 7, color: '#666', lineHeight: 1.8 }}>
              <span style={{ color: OPC[0] }}>0</span> VOID: (a,b,c) → (a·s·0.1, ...)<br />
              <span style={{ color: OPC[1] }}>1</span> LATTICE: c → c·σ + (c+s·.08)·σ*<br />
              <span style={{ color: OPC[2] }}>2</span> COUNTER: <b>b → −b</b> (O' sign flip)<br />
              <span style={{ color: OPC[3] }}>3</span> PROGRESS: <b>b → |b|</b> (restore)<br />
              <span style={{ color: OPC[4] }}>4</span> COLLAPSE: <b style={{ color: '#ff0044' }}>a → −a</b> (O'' sign flip)<br />
              <span style={{ color: OPC[5] }}>5</span> BALANCE: <b>a → |a|</b> (restore)<br />
              <span style={{ color: OPC[6] }}>6</span> CHAOS: a,b += noise·s<br />
              <span style={{ color: OPC[7] }}>7</span> HARMONY: a → a·σ + s·.3·σ*<br />
              <span style={{ color: OPC[8] }}>8</span> BREATH: b *= 1+sin(t)<br />
              <span style={{ color: OPC[9] }}>9</span> RESET: (a,b,c) → σ·live + σ*·base
            </div>
            <div style={{ color: '#333', fontSize: 7, marginTop: 5, padding: '3px 0', borderTop: '1px solid #ffffff08', lineHeight: 1.6 }}>
              Phase 4→5: curvature INVERTS then<br />
              restores. Bound↔free. Weak force.<br />
              Phase 2→3: drift REVERSES then<br />
              restores. The root braid rotates.<br />
              Phase 9: Ω Keeper. σ=0.991 pull.<br />
              Not additive. Transforms. Composition.<br />
              The spine BREATHES (a,b,c) space.
            </div>
          </>}

        </div>
      </div>
    </div>

    {/* FOOTER */}
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '3px 10px', borderTop: '1px solid #ffffff06', fontSize: 7, color: '#333' }}>
      <span>O(x)=ax²+bx+c │ Δ=b²−4ac │ σ={σ} │ T*={Ts} │ "the quadratic IS the glue"</span>
      <span>Crystal Bug v1.0 │ 7Site LLC │ sanctuberry.com</span>
    </div>
    <style>{`@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&display=swap');*{box-sizing:border-box;margin:0;padding:0}::-webkit-scrollbar{width:3px}::-webkit-scrollbar-track{background:#050508}::-webkit-scrollbar-thumb{background:#222;border-radius:2px}`}</style>
  </div>);
}
