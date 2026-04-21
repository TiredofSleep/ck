// ═══ CRYSTAL BUG v1.0 — CORRECTED ENGINE + FULL TEST ═══

const σ = 0.991, σs = 0.009, Ts = 0.714, F_ = σ * (1 - σs);
const SS = (V, A) => F_ * Math.max(0, Math.min(1, V)) * Math.max(0, Math.min(1, A));
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
}

const BANDS = ['VOID','QUANTUM','ATOMIC','MOLECULR','CELLULAR','ORGANIC','CRYSTAL'];

function classify(O, x0 = 0.5) {
  const orb = [x0]; const N = 28, esc = 80, eps = 5e-4;
  for (let i = 0; i < N; i++) {
    const xn = O.ev(orb[orb.length - 1]);
    orb.push(xn);
    if (!isFinite(xn) || Math.abs(xn) > esc) {
      if (i < 3) return { band: 0, orb };
      if (i < 9) return { band: 1, orb };
      return { band: 2, orb };
    }
  }
  const t = orb.slice(-8);
  if (Math.abs(t[7] - t[6]) < eps) {
    const ci = orb.findIndex((x, i) => i > 2 && Math.abs(x - orb[i - 1]) < eps * 5);
    return ci > 0 && ci < 10 ? { band: 6, orb } : { band: 5, orb };
  }
  if (Math.abs(t[7] - t[5]) < eps * 3 && Math.abs(t[6] - t[4]) < eps * 3)
    return { band: 4, orb };
  for (let p = 3; p <= 6; p++)
    if (orb.length > p + 2 && Math.abs(t[7] - t[7 - p]) < eps * 8) return { band: 4, orb };
  return { band: 3, orb };
}

function rootDist(O1, O2) {
  const r1 = O1.roots(), r2 = O2.roots();
  if (r1.re && r2.re)
    return Math.min(Math.abs(r1.r1 - r2.r1), Math.abs(r1.r1 - r2.r2), Math.abs(r1.r2 - r2.r1), Math.abs(r1.r2 - r2.r2));
  if (!r1.re && !r2.re)
    return Math.abs(r1.r1 - r2.r1) + Math.abs(r1.im - r2.im);
  return Math.abs(O1.vx() - O2.vx()) + Math.abs(O1.vy() - O2.vy()) * 0.5;
}

// FIXED: Better initial geometry — spread across all bands
function mkCell(col, row) {
  const u = col / (COLS - 1), v = row / (ROWS - 1);
  const cu = u - 0.5, cv = v - 0.5;
  const r = Math.sqrt(cu * cu + cv * cv);
  const th = Math.atan2(cv, cu);
  // Wider coefficient spread to populate all 7 bands
  // Center: high a, low b → bound (Δ<0) with complex dynamics
  // Mid-ring: moderate a, moderate b → click zone (Δ≈0)  
  // Edge: low a, high b → free (Δ>0) with escape dynamics
  const a = 0.8 * Math.cos(r * 3.5) * (1 + 0.5 * Math.sin(v * 7 * Math.PI));
  const b = (cu * 3.5 + cv * 2.0) * (1 + 0.3 * Math.cos(u * 5 * Math.PI));
  const c = 0.5 * Math.exp(-r * 2) + 0.15 * Math.sin(th * 4 + r * 3) + 0.1;
  const O = new Q(a, b, c);
  const cl = classify(O);
  return { col, row, id: row * COLS + col, a0: a, b0: b, c0: c, a, b, c, O,
    D: O.D(), band: cl.band, orb: cl.orb, coh: 0, lit: false, vis: 0, nW: [], fp: O.fp() };
}

function gN(col, row) {
  const ns = [];
  for (let dr = -1; dr <= 1; dr++) for (let dc = -1; dc <= 1; dc++) {
    if (dr === 0 && dc === 0) continue;
    const nr = row + dr, nc = col + dc;
    if (nr >= 0 && nr < ROWS && nc >= 0 && nc < COLS) ns.push({ col: nc, row: nr });
  }
  return ns;
}

function wireNeighbors(cells) {
  for (const cell of cells) {
    const gns = gN(cell.col, cell.row);
    cell.nW = gns.map(n => {
      const nc = cells[n.row * COLS + n.col];
      const rd = rootDist(cell.O, nc.O);
      return { id: nc.id, w: 1 / (1 + rd * 0.5) };
    }).sort((a, b) => b.w - a.w);
  }
}

function advSpine(spine, ph, tick) {
  const i = ph, p = spine[(i + 9) % 10], o = spine[i];
  const ops = [
    () => p * (1 - σ) * 0.1,
    () => o * σ + p * (1 - σ),
    () => Math.abs(o - p) * σ + o * (1 - σ),
    () => o + (1 - o) * (1 - σ),
    () => o * σ,
    () => (o + spine.reduce((a, b) => a + b) / 10) / 2,
    () => o * σ + (Math.random() - .5) * .003,
    () => Math.sqrt(Math.max(.001, o * p)),
    () => o * (1 + .008 * Math.sin(tick * .1)),
    () => o * σ + Ts * (1 - σ),
  ];
  spine[i] = Math.max(.001, Math.min(1, ops[i]()));
  return (i + 1) % 10;
}

// FIXED: Spine transforms — VOID doesn't crush, it contracts gently
function modCells(cells, spine, ph, tick) {
  const sv = spine[ph];
  for (const cell of cells) {
    let { a, b, c } = cell;
    switch (ph) {
      case 0: // VOID: gentle contraction toward origin, NOT destruction
        a = a * (1 - σs * sv); b = b * (1 - σs * sv); c = c * (1 - σs * sv); break;
      case 1: // LATTICE: nudge c upward
        c = c * σ + (c + sv * 0.05) * σs; break;
      case 2: // COUNTER: b → −b 
        b = -b; break;
      case 3: // PROGRESS: b → |b|
        b = Math.abs(b); break;
      case 4: // COLLAPSE: a → −a (THE FLIP)
        a = -a; break;
      case 5: // BALANCE: a → |a|
        a = Math.abs(a); break;
      case 6: // CHAOS: perturb
        a += (Math.random() - .5) * sv * 0.006;
        b += (Math.random() - .5) * sv * 0.006; break;
      case 7: // HARMONY: smooth a
        a = a * σ + sv * 0.2 * σs; break;
      case 8: // BREATH: oscillate b
        b *= 1 + 0.004 * Math.sin(tick * 0.08); break;
      case 9: // RESET: pull toward base at σ rate
        a = a * σ + cell.a0 * σs;
        b = b * σ + cell.b0 * σs;
        c = c * σ + cell.c0 * σs; break;
    }
    cell.a = a; cell.b = b; cell.c = c;
    cell.O = new Q(a, b, c); cell.D = cell.O.D();
  }
}

function reclassify(cells) {
  for (const cell of cells) {
    const cl = classify(cell.O);
    cell.band = cl.band; cell.orb = cl.orb; cell.fp = cell.O.fp();
  }
}

// ═══ OLD BUG ═══
class OldBug {
  constructor(E0) { this.E0 = E0; this.E = E0; this.col = 9; this.row = 7; this.vis = new Set(); this.steps = 0; this.vCnt = 0; this.alive = true; }
  step(cells, gN_) {
    if (!this.alive || this.E <= 0) { this.alive = false; return; }
    this.steps++;
    const cell = cells[this.row * COLS + this.col];
    // OLD: min(1.0) energy cap
    this.E = Math.min(1.0, this.E + 0.01);
    this.E -= 0.03;
    cell.vis++; this.vCnt++; this.vis.add(cell.id); cell.lit = true; cell.coh += 0.05;
    const ns = gN_(this.col, this.row); if (!ns.length) return;
    if (Math.random() < 0.5) {
      let best = ns[0], bd = 999;
      for (const n of ns) { const nd = Math.abs(cells[n.row * COLS + n.col].D); if (nd < bd) { bd = nd; best = n; } }
      this.col = best.col; this.row = best.row;
    } else {
      const n = ns[Math.floor(Math.random() * ns.length)]; this.col = n.col; this.row = n.row;
    }
    // Surface double-count
    cell.vis++; this.vCnt++;
  }
}

// ═══ NEW BUG ═══
class NewBug {
  constructor(E0) { this.E0 = E0; this.E = E0; this.mI = 1.0; this.col = 9; this.row = 7;
    this.pStk = []; this.lastId = -1; this.vis = new Set(); this.steps = 0; this.vCnt = 0; this.alive = true;
    this.mode = 'bug'; this.aStk = []; this.aSeen = new Set(); this.costs = []; this.dHist = []; }
  step(cells, gN_) {
    if (!this.alive || this.E <= 0) { this.alive = false; return; }
    this.steps++;
    const cell = cells[this.row * COLS + this.col];
    // FIX 1: Energy honesty — cost from |Δ|, intensity capped not budget
    const intensity = Math.min(this.mI, this.E);
    const dCost = 1 / (Math.abs(cell.D) + 0.1);  // Softer: +0.1 not +0.05
    const cost = 0.005 + dCost * 0.008 * intensity;  // Lower base + rate
    this.E -= cost;
    this.costs.push(cost); if (this.costs.length > 200) this.costs.shift();
    this.dHist.push(cell.D); if (this.dHist.length > 200) this.dHist.shift();
    // Evaluation deposits trace
    const res = cell.O.ev(intensity);
    cell.c += res * 0.0005 * intensity;
    cell.coh += intensity * 0.04 * σ;
    cell.lit = true;
    // FIX 2: Fair visit accounting — path stack, only count on actual transition
    const cid = cell.id;
    if (cid !== this.lastId) {
      const top = this.pStk.length ? this.pStk[this.pStk.length - 1] : -1;
      if (cid !== top) { cell.vis++; this.vCnt++; this.pStk.push(cid); if (this.pStk.length > 80) this.pStk.shift(); }
      this.vis.add(cid); this.lastId = cid;
    }
    // FIX 3: Two modes
    if (this.mode === 'bug') this._bug(cell, cells, gN_);
    else this._aud(cells, gN_);
  }
  _bug(cell, cells, gN_) {
    const ns = gN_(this.col, this.row); if (!ns.length) return;
    const D = cell.D;
    if (D > 0.08) {
      let best = ns[0], bd = 999;
      for (const n of ns) { const nd = Math.abs(cells[n.row * COLS + n.col].D); if (nd < bd) { bd = nd; best = n; } }
      this.col = best.col; this.row = best.row;
    } else if (D < -0.08) {
      const unv = ns.filter(n => !cells[n.row * COLS + n.col].lit);
      if (unv.length && Math.random() < 0.4) { const n = unv[Math.floor(Math.random() * unv.length)]; this.col = n.col; this.row = n.row; }
      else {
        const nw = ns.map(n => ({ ...n, w: (cell.nW.find(x => x.id === n.row * COLS + n.col) || { w: 0.1 }).w }));
        nw.sort((a, b) => b.w - a.w);
        const pick = nw[Math.random() < 0.7 ? 0 : Math.floor(Math.random() * Math.min(3, nw.length))];
        this.col = pick.col; this.row = pick.row;
      }
    } else {
      if (Math.random() > 0.7) { const n = ns[Math.floor(Math.random() * ns.length)]; this.col = n.col; this.row = n.row; }
    }
  }
  _aud(cells, gN_) {
    if (!this.aStk.length && !this.aSeen.size) this.aStk.push({ col: this.col, row: this.row });
    while (this.aStk.length) {
      const nx = this.aStk.pop(); const nid = nx.row * COLS + nx.col;
      if (!this.aSeen.has(nid)) {
        this.aSeen.add(nid); this.col = nx.col; this.row = nx.row;
        for (const n of gN_(nx.col, nx.row)) if (!this.aSeen.has(n.row * COLS + n.col)) this.aStk.push(n);
        return;
      }
    }
    this.alive = false;
  }
  reset(E0) { this.E0 = E0; this.E = E0; this.col = 9; this.row = 7; this.pStk = []; this.lastId = -1;
    this.vis = new Set(); this.steps = 0; this.vCnt = 0; this.alive = true; this.costs = []; this.dHist = [];
    this.aStk = []; this.aSeen = new Set(); }
}

// ═══════════════════════════════════════════════════
// RUN FULL TEST SUITE
// ═══════════════════════════════════════════════════

function runSim(E0, mode, maxTicks=20000) {
  const cells = []; for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) cells.push(mkCell(c, r));
  wireNeighbors(cells);
  const bug = new NewBug(E0); bug.mode = mode;
  let spine = new Array(10).fill(Ts), ph = 0, tick = 0, epoch = 0;
  const snapshots = [];
  for (let t = 0; t < maxTicks && bug.alive; t++) {
    tick++; ph = advSpine(spine, ph, tick);
    if (ph === 0) epoch++;
    modCells(cells, spine, ph, tick);
    if (tick % 12 === 0) reclassify(cells);
    if (tick % 80 === 0) wireNeighbors(cells);
    bug.step(cells, gN);
    if (tick % 200 === 0) {
      const bc = new Array(7).fill(0); for (const c of cells) bc[c.band]++;
      snapshots.push({ tick, vis: bug.vis.size, E: bug.E, rr: bug.vCnt > 0 ? bug.steps / bug.vCnt : 1, bc: [...bc] });
    }
  }
  const bc = new Array(7).fill(0); for (const c of cells) bc[c.band]++;
  return { bug, cells, tick, epoch, bc, snapshots };
}

function runOldSim(E0, maxTicks=20000) {
  const cells = []; for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) cells.push(mkCell(c, r));
  const bug = new OldBug(E0);
  let spine = new Array(10).fill(Ts), ph = 0, tick = 0;
  for (let t = 0; t < maxTicks && bug.alive; t++) {
    tick++; ph = advSpine(spine, ph, tick); modCells(cells, spine, ph, tick);
    if (tick % 12 === 0) reclassify(cells);
    bug.step(cells, gN);
  }
  return { bug, cells, tick };
}

console.log("═══════════════════════════════════════════════════════════════════");
console.log("  CRYSTAL BUG v1.0 — FULL SIMULATION RESULTS (CORRECTED)");
console.log("═══════════════════════════════════════════════════════════════════");
console.log();

// TEST 1: INITIAL LATTICE
console.log("╔══ TEST 1: INITIAL LATTICE STRUCTURE ═══════════════════════════╗");
const cells0 = []; for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) cells0.push(mkCell(c, r));
const bc0 = new Array(7).fill(0); for (const c of cells0) bc0[c.band]++;
BANDS.forEach((b, i) => console.log(`  ${b.padEnd(10)} ${bc0[i].toString().padStart(4)} cells (${(bc0[i]/NC*100).toFixed(1)}%)`));
const click0 = cells0.filter(c => Math.abs(c.D) < 0.15).length;
const stable0 = cells0.filter(c => c.fp && c.fp.stable).length;
console.log(`  Click zone: ${click0} (${(click0/NC*100).toFixed(1)}%)  Stable FP: ${stable0} (${(stable0/NC*100).toFixed(1)}%)`);
console.log(`  Δ range: [${Math.min(...cells0.map(c=>c.D)).toFixed(3)}, ${Math.max(...cells0.map(c=>c.D)).toFixed(3)}]`);
console.log();

// TEST 2: ENERGY HONESTY
console.log("╔══ TEST 2: FIX 1 — ENERGY HONESTY ═════════════════════════════╗");
console.log("  E0  │ OLD: steps  uniq  rr   │ NEW(bug): steps  uniq   rr    cov%");
console.log("──────┼─────────────────────────┼───────────────────────────────────");
for (const e0 of [3, 10, 25, 50]) {
  const o = runOldSim(e0, 20000);
  const n = runSim(e0, 'bug', 20000);
  const oRR = o.bug.vCnt > 0 ? o.bug.steps / o.bug.vCnt : 1;
  const nRR = n.bug.vCnt > 0 ? n.bug.steps / n.bug.vCnt : 1;
  console.log(`  ${e0.toString().padStart(3)} │ ${o.bug.steps.toString().padStart(5)}  ${o.bug.vis.size.toString().padStart(4)}  ${oRR.toFixed(2).padStart(5)} │         ${n.bug.steps.toString().padStart(5)}  ${n.bug.vis.size.toString().padStart(4)}  ${nRR.toFixed(2).padStart(5)}  ${(n.bug.vis.size/NC*100).toFixed(1).padStart(5)}%`);
}
console.log();

// TEST 3: REVISIT RATIO DEEP DIVE
console.log("╔══ TEST 3: FIX 2 — REVISIT RATIO OVER TIME ════════════════════╗");
{
  const o = runOldSim(25, 5000);
  const n = runSim(25, 'bug', 5000);
  console.log(`  OLD: ${o.bug.steps} steps, ${o.bug.vis.size} unique, ${o.bug.vCnt} visits → rr = ${(o.bug.steps/o.bug.vCnt).toFixed(3)}`);
  console.log(`  NEW: ${n.bug.steps} steps, ${n.bug.vis.size} unique, ${n.bug.vCnt} visits → rr = ${(n.bug.steps/n.bug.vCnt).toFixed(3)}`);
  console.log(`  NEW timeline:`);
  for (const s of n.snapshots) console.log(`    t=${s.tick.toString().padStart(5)} vis=${s.vis.toString().padStart(4)} E=${s.E.toFixed(2).padStart(6)} rr=${s.rr.toFixed(3)}`);
}
console.log();

// TEST 4: AUDIT MODE
console.log("╔══ TEST 4: FIX 3 — AUDIT MODE ═════════════════════════════════╗");
for (const e0 of [25, 50, 100]) {
  const a = runSim(e0, 'audit', 20000);
  const litBands = new Array(7).fill(0); 
  for (const c of a.cells) if (c.lit) litBands[c.band]++;
  console.log(`  E0=${e0}: ${a.bug.vis.size}/${NC} (${(a.bug.vis.size/NC*100).toFixed(1)}%) in ${a.bug.steps} steps, E left=${a.bug.E.toFixed(2)}`);
  console.log(`    Lit by band: ${litBands.map((n,i) => `${BANDS[i].slice(0,4)}=${n}`).join(' ')}`);
}
console.log();

// TEST 5: SPINE DYNAMICS — BAND STABILITY
console.log("╔══ TEST 5: BAND STABILITY THROUGH EPOCHS ═══════════════════════╗");
{
  const cells5 = []; for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) cells5.push(mkCell(c, r));
  let spine5 = new Array(10).fill(Ts), ph5 = 0;
  console.log("  Epoch │ " + BANDS.map(b => b.slice(0,4).padStart(5)).join(' ') + " │ click │ Δ_avg");
  console.log("  ──────┼─" + "──────".repeat(7) + "┼───────┼──────");
  for (let ep = 0; ep < 20; ep++) {
    for (let t = 0; t < 10; t++) { ph5 = advSpine(spine5, ph5, ep * 10 + t); modCells(cells5, spine5, ph5, ep * 10 + t); }
    reclassify(cells5);
    const bc5 = new Array(7).fill(0); for (const c of cells5) bc5[c.band]++;
    const click5 = cells5.filter(c => Math.abs(c.D) < 0.15).length;
    const avgD5 = cells5.reduce((a,c) => a + c.D, 0) / NC;
    console.log(`  ${ep.toString().padStart(5)} │ ${bc5.map(n => n.toString().padStart(5)).join(' ')} │ ${click5.toString().padStart(5)} │ ${avgD5.toFixed(3)}`);
  }
}
console.log();

// TEST 6: ENERGY COST DISTRIBUTION
console.log("╔══ TEST 6: Δ-DEPENDENT ENERGY COST ═════════════════════════════╗");
{
  const cells6 = []; for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) cells6.push(mkCell(c, r));
  const zones = { click: [], free: [], bound: [] };
  for (const cell of cells6) {
    const dCost = 1 / (Math.abs(cell.D) + 0.1);
    const cost = 0.005 + dCost * 0.008;
    if (Math.abs(cell.D) < 0.15) zones.click.push(cost);
    else if (cell.D > 0.5) zones.free.push(cost);
    else if (cell.D < -0.5) zones.bound.push(cost);
  }
  const avg = arr => arr.length ? arr.reduce((a,b)=>a+b)/arr.length : 0;
  console.log(`  Click zone (|Δ|<0.15): avg cost/step = ${avg(zones.click).toFixed(5)} (${zones.click.length} cells)`);
  console.log(`  Free zone  (Δ>0.5):    avg cost/step = ${avg(zones.free).toFixed(5)} (${zones.free.length} cells)`);
  console.log(`  Bound zone (Δ<-0.5):   avg cost/step = ${avg(zones.bound).toFixed(5)} (${zones.bound.length} cells)`);
  if (zones.free.length > 0 && zones.click.length > 0) {
    console.log(`  Click/Free cost ratio: ${(avg(zones.click) / avg(zones.free)).toFixed(1)}×`);
  }
  console.log(`  E0=3:  ~${Math.floor(3 / avg(zones.click))} click-zone steps, ~${Math.floor(3 / avg(zones.free))} free-zone steps`);
  console.log(`  E0=10: ~${Math.floor(10 / avg(zones.click))} click-zone steps, ~${Math.floor(10 / avg(zones.free))} free-zone steps`);
  console.log(`  E0=50: ~${Math.floor(50 / avg(zones.click))} click-zone steps, ~${Math.floor(50 / avg(zones.free))} free-zone steps`);
}
console.log();

// TEST 7: ROOT-PROXIMITY
console.log("╔══ TEST 7: ROOT-PROXIMITY NEIGHBORHOODS ════════════════════════╗");
{
  const cells7 = []; for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) cells7.push(mkCell(c, r));
  wireNeighbors(cells7);
  let diffCount = 0;
  for (const cell of cells7) {
    const gridIds = gN(cell.col, cell.row).map(n => n.row * COLS + n.col).sort((a,b)=>a-b);
    const rootIds = cell.nW.map(n => n.id).sort((a,b)=>a-b);
    // Same set but different priority
    const rootTop3 = cell.nW.slice(0, 3).map(n => n.id);
    const gridTop3 = gN(cell.col, cell.row).slice(0, 3).map(n => n.row * COLS + n.col);
    if (rootTop3.join(',') !== gridTop3.join(',')) diffCount++;
  }
  console.log(`  Cells where root-priority ≠ grid-priority: ${diffCount}/${NC} (${(diffCount/NC*100).toFixed(1)}%)`);
  // Show a few examples
  const examples = [0, Math.floor(NC/4), Math.floor(NC/2), Math.floor(3*NC/4), NC-1];
  for (const idx of examples) {
    const c = cells7[idx];
    console.log(`  Cell [${c.col},${c.row}] band=${BANDS[c.band].slice(0,4)} top neighbor: #${c.nW[0]?.id} w=${c.nW[0]?.w.toFixed(3)} (band=${BANDS[cells7[c.nW[0]?.id]?.band]?.slice(0,4) || '?'})`);
  }
}
console.log();

// TEST 8: BUG vs AUDIT COMPARISON
console.log("╔══ TEST 8: BUG MODE vs AUDIT MODE (E0=50) ══════════════════════╗");
{
  const b = runSim(50, 'bug', 20000);
  const a = runSim(50, 'audit', 20000);
  console.log(`  BUG:   ${b.bug.vis.size}/${NC} (${(b.bug.vis.size/NC*100).toFixed(1)}%) in ${b.bug.steps} steps`);
  console.log(`  AUDIT: ${a.bug.vis.size}/${NC} (${(a.bug.vis.size/NC*100).toFixed(1)}%) in ${a.bug.steps} steps`);
  // Which bands does bug prefer vs avoid?
  const bugBandLit = new Array(7).fill(0);
  for (const c of b.cells) if (c.lit) bugBandLit[c.band]++;
  const audBandLit = new Array(7).fill(0);
  for (const c of a.cells) if (c.lit) audBandLit[c.band]++;
  console.log(`  Bug lit by band:   ${bugBandLit.map((n,i)=>`${BANDS[i].slice(0,4)}=${n}`).join(' ')}`);
  console.log(`  Audit lit by band: ${audBandLit.map((n,i)=>`${BANDS[i].slice(0,4)}=${n}`).join(' ')}`);
  // Bug attractor analysis
  const bugOnlyVis = [...b.bug.vis];
  const bandPref = new Array(7).fill(0);
  for (const id of bugOnlyVis) bandPref[b.cells[id].band]++;
  console.log(`  Bug visits by band: ${bandPref.map((n,i)=>`${BANDS[i].slice(0,4)}=${n}`).join(' ')}`);
}
console.log();

// TEST 9: PERFORMANCE
console.log("╔══ TEST 9: PERFORMANCE ═════════════════════════════════════════╗");
{
  const cells9 = []; for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) cells9.push(mkCell(c, r));
  wireNeighbors(cells9);
  const bug9 = new NewBug(9999);
  let s9 = new Array(10).fill(Ts), p9 = 0, t9 = 0;
  const N = 20000, t0 = Date.now();
  for (let t = 0; t < N; t++) {
    t9++; p9 = advSpine(s9, p9, t9); modCells(cells9, s9, p9, t9);
    if (t9 % 12 === 0) reclassify(cells9);
    if (t9 % 80 === 0) wireNeighbors(cells9);
    bug9.step(cells9, gN);
  }
  const ms = Date.now() - t0;
  console.log(`  ${N} ticks in ${ms}ms = ${(N/ms*1000).toFixed(0)} ticks/sec`);
  console.log(`  Target: 120 ticks/sec (60fps × 2) → headroom: ${((N/ms*1000)/120).toFixed(0)}×`);
}
console.log();
console.log("═══════════════════════════════════════════════════════════════════");
