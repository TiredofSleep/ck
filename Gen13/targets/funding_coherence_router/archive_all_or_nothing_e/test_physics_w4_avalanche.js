// W4 FIX: Spine-mediated avalanche propagation
// Instead of artificial diffusion, perturb one cell then run spine cycles.
// The spine's own transforms are the natural coupling mechanism.

const σ = 0.991, σs = 0.009, Ts = 0.714;
const COLS = 18, ROWS = 14, NC = COLS * ROWS;

class Q {
  constructor(a, b, c) { this.a = a; this.b = b; this.c = c; }
  ev(x) { return this.a * x * x + this.b * x + this.c; }
  D() { return this.b * this.b - 4 * this.a * this.c; }
  d1(x) { return 2 * this.a * x + this.b; }
  vx() { return Math.abs(this.a) > 1e-12 ? -this.b / (2 * this.a) : 0; }
  vy() { return this.ev(this.vx()); }
  roots() { const d = this.D(); if (Math.abs(this.a) < 1e-12) return { re: true, r1: 0, r2: 0, im: 0 }; if (d >= 0) { const s = Math.sqrt(d); return { re: true, r1: (-this.b + s) / (2 * this.a), r2: (-this.b - s) / (2 * this.a), im: 0 }; } return { re: false, r1: -this.b / (2 * this.a), r2: -this.b / (2 * this.a), im: Math.sqrt(-d) / (2 * Math.abs(this.a)) }; }
  fp() { const A = this.a, B = this.b - 1, C = this.c, d = B * B - 4 * A * C; if (Math.abs(A) < 1e-12) return B !== 0 ? { x: -C / B, stable: Math.abs(this.b) < 1 } : null; if (d < 0) return null; const s = Math.sqrt(d), x1 = (-B + s) / (2 * A), x2 = (-B - s) / (2 * A), l1 = Math.abs(this.d1(x1)), l2 = Math.abs(this.d1(x2)); return l1 < l2 ? { x: x1, lam: l1, stable: l1 < 1 } : { x: x2, lam: l2, stable: l2 < 1 }; }
}

function classifySingle(O, x0, maxN = 80) {
  const esc = 80, eps = 5e-4;
  let x = x0; const orb = [x]; let lyapSum = 0, lyapN = 0;
  for (let i = 0; i < maxN; i++) { const xn = O.ev(x); orb.push(xn); const dv = Math.abs(O.d1(x)); if (dv > 1e-15 && isFinite(dv)) { lyapSum += Math.log(dv); lyapN++; } if (!isFinite(xn) || Math.abs(xn) > esc) { if (i < 3) return { band: 0, lyap: lyapN > 0 ? lyapSum / lyapN : 0, conf: 1 }; if (i < 9) return { band: 1, lyap: lyapN > 0 ? lyapSum / lyapN : 0, conf: 1 }; return { band: 2, lyap: lyapN > 0 ? lyapSum / lyapN : 0, conf: .95 }; } x = xn; }
  const lyap = lyapN > 0 ? lyapSum / lyapN : 0;
  if (orb.length > 20) { for (let p = 1; p <= 16; p++) { if (orb.length < p * 3 + 4) continue; let match = true; for (let c = 0; c < 3 && match; c++) for (let k = 0; k < p && match; k++) { const i1 = orb.length-1-k-c*p, i2 = orb.length-1-k-(c+1)*p; if (i2 < 0 || Math.abs(orb[i1]-orb[i2]) > 5e-4*2) match = false; } if (match) { if (p === 1) { let ci = -1; for (let i = 3; i < orb.length-1; i++) if (Math.abs(orb[i]-orb[i-1]) < 2.5e-3) { ci = i; break; } return ci > 0 && ci < 12 ? { band: 6, lyap, conf: 1 } : { band: 5, lyap, conf: .95 }; } return { band: 4, lyap, conf: .95 }; } } }
  if (lyap < -0.01) { const t = orb.slice(-8); if (Math.abs(t[7]-t[6]) < 5e-4) { let ci = -1; for (let i = 3; i < orb.length-1; i++) if (Math.abs(orb[i]-orb[i-1]) < 2.5e-3) { ci = i; break; } return ci > 0 && ci < 12 ? { band: 6, lyap, conf: 1 } : { band: 5, lyap, conf: .95 }; } return { band: 5, lyap, conf: .7 }; }
  if (lyap > 0.1) return { band: 3, lyap, conf: .9 };
  if (lyap > 0) return { band: 3, lyap, conf: .7 };
  return { band: 3, lyap, conf: .5 };
}
function classify(O) {
  const fp = O.fp(), vx = O.vx();
  const seeds = [0.5, vx, fp ? fp.x+0.01 : 0.25, 0.6180339887, Math.PI/4, 1/3, Math.sqrt(2)/2];
  const results = seeds.map(s => classifySingle(O, Math.max(-10, Math.min(10, s))));
  const votes = new Array(7).fill(0); let lyapMax = -Infinity;
  for (const r of results) { votes[r.band] += r.conf; if (r.lyap > lyapMax) lyapMax = r.lyap; }
  let best = 0, bestV = 0;
  for (let i = 0; i < 7; i++) if (votes[i] > bestV) { bestV = votes[i]; best = i; }
  if ((best === 5 || best === 6) && lyapMax > 0.1) best = 4;
  return { band: best };
}

function mkCell(col, row) {
  const u = col/(COLS-1), v = row/(ROWS-1), cu = u-0.5, cv = v-0.5, r = Math.sqrt(cu*cu+cv*cv), th = Math.atan2(cv, cu);
  const a = 0.8*Math.cos(r*3.5)*(1+0.5*Math.sin(v*7*Math.PI));
  const b = (cu*3.5+cv*2.0)*(1+0.3*Math.cos(u*5*Math.PI));
  const c = 0.5*Math.exp(-r*2)+0.15*Math.sin(th*4+r*3)+0.1;
  const O = new Q(a,b,c);
  return { col, row, id: row*COLS+col, a0: a, b0: b, c0: c, a, b, c, O, D: O.D(), band: classify(O).band, nW: [] };
}
function gN(c, r) { const ns = []; for (let dr=-1; dr<=1; dr++) for (let dc=-1; dc<=1; dc++) { if (!dr&&!dc) continue; const nr=r+dr, nc=c+dc; if (nr>=0&&nr<ROWS&&nc>=0&&nc<COLS) ns.push({col:nc,row:nr}); } return ns; }
function rootDist(O1, O2) { const r1=O1.roots(), r2=O2.roots(); if (r1.re&&r2.re) return Math.min(Math.abs(r1.r1-r2.r1),Math.abs(r1.r1-r2.r2),Math.abs(r1.r2-r2.r1),Math.abs(r1.r2-r2.r2)); if (!r1.re&&!r2.re) return Math.abs(r1.r1-r2.r1)+Math.abs(r1.im-r2.im); return Math.abs(O1.vx()-O2.vx())+Math.abs(O1.vy()-O2.vy())*0.5; }
function wireNeighbors(cells) { for (const cell of cells) { const gns=gN(cell.col,cell.row); cell.nW=gns.map(n => { const nc=cells[n.row*COLS+n.col]; return {id:nc.id, w:1/(1+rootDist(cell.O,nc.O)*0.5)}; }).sort((a,b)=>b.w-a.w); } }

function modCellsSingle(cells, spine, ph, tick) {
  const sv = spine[ph];
  for (const cell of cells) { let {a,b,c} = cell;
    switch(ph) {
      case 0: a*=(1-σs*sv); b*=(1-σs*sv); c*=(1-σs*sv); break;
      case 1: c=c*σ+(c+sv*0.05)*σs; break;
      case 2: b=-b; break; case 3: b=Math.abs(b); break;
      case 4: a=-a; break; case 5: a=Math.abs(a); break;
      case 6: break; // no noise for deterministic test
      case 7: a=a*σ+sv*0.2*σs; break;
      case 8: b*=1+0.004*Math.sin(tick*0.08); break;
      case 9: a=a*σ+cell.a0*σs; b=b*σ+cell.b0*σs; c=c*σ+cell.c0*σs; break;
    }
    cell.a=a; cell.b=b; cell.c=c; cell.O=new Q(a,b,c); cell.D=cell.O.D();
  }
}

const BN = ['VOID','QUANTUM','ATOMIC','MOLECULR','CELLULAR','ORGANIC','CRYSTAL'];

console.log("╔══════════════════════════════════════════════════════════════════╗");
console.log("║  W4: AVALANCHE CASCADES — SPINE-MEDIATED PROPAGATION           ║");
console.log("╚══════════════════════════════════════════════════════════════════╝\n");

// Build lattice
const cells = []; for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) cells.push(mkCell(c, r));
wireNeighbors(cells);

// Evolve 200 ticks to reach mature state
let spine = new Array(10).fill(Ts), ph = 0;
for (let t = 0; t < 200; t++) { ph = (ph + 1) % 10; modCellsSingle(cells, spine, ph, t); }
for (const cell of cells) cell.band = classify(cell.O).band;

const clickCells = cells.filter(c => Math.abs(c.D) < 0.15);
const freeCells = cells.filter(c => c.D > 0.5);
const boundCells = cells.filter(c => c.D < -0.5);
console.log(`Click (|Δ|<0.15): ${clickCells.length}  Free (Δ>0.5): ${freeCells.length}  Bound (Δ<-0.5): ${boundCells.length}\n`);

// Avalanche test: perturb ONE cell's coefficients, run N spine cycles, count band changes
function testAvalanche(targetCells, epsilon, spineCycles, label, trials = 300) {
  const cascadeSizes = [];
  const bandChangeDist = {};

  for (let trial = 0; trial < Math.min(trials, targetCells.length * 30); trial++) {
    // Save entire lattice state
    const saved = cells.map(c => ({ a: c.a, b: c.b, c: c.c, band: c.band }));

    // Pick and perturb one cell
    const tgt = targetCells[Math.floor(Math.random() * targetCells.length)];
    tgt.a += (Math.random() - 0.5) * epsilon;
    tgt.b += (Math.random() - 0.5) * epsilon;
    tgt.O = new Q(tgt.a, tgt.b, tgt.c); tgt.D = tgt.O.D();

    // Run spine cycles (natural propagation through phase transforms)
    let lph = ph;
    for (let cyc = 0; cyc < spineCycles; cyc++) {
      lph = (lph + 1) % 10;
      modCellsSingle(cells, spine, lph, 200 + cyc);
    }

    // Reclassify and count
    let changed = 0;
    for (let i = 0; i < NC; i++) {
      const newBand = classify(cells[i].O).band;
      if (newBand !== saved[i].band) {
        changed++;
        const key = `${BN[saved[i].band]}→${BN[newBand]}`;
        bandChangeDist[key] = (bandChangeDist[key] || 0) + 1;
      }
    }
    cascadeSizes.push(changed);

    // Restore
    for (let i = 0; i < NC; i++) {
      cells[i].a = saved[i].a; cells[i].b = saved[i].b; cells[i].c = saved[i].c;
      cells[i].O = new Q(cells[i].a, cells[i].b, cells[i].c); cells[i].D = cells[i].O.D();
      cells[i].band = saved[i].band;
    }
  }

  const n = cascadeSizes.length;
  const mean = cascadeSizes.reduce((a, b) => a + b, 0) / n;
  const sorted = [...cascadeSizes].sort((a, b) => a - b);
  const med = sorted[Math.floor(n/2)], p90 = sorted[Math.floor(n*0.9)], max = Math.max(...sorted);
  const nonZero = cascadeSizes.filter(x => x > 0).length;
  const bins = { '0': 0, '1': 0, '2-5': 0, '6-15': 0, '16-40': 0, '40+': 0 };
  for (const s of cascadeSizes) { if (s === 0) bins['0']++; else if (s === 1) bins['1']++; else if (s <= 5) bins['2-5']++; else if (s <= 15) bins['6-15']++; else if (s <= 40) bins['16-40']++; else bins['40+']++; }

  console.log(`  ${label} (ε=${epsilon}, ${spineCycles} spine cycles, ${n} trials):`);
  console.log(`    mean=${mean.toFixed(2)}  med=${med}  P90=${p90}  max=${max}`);
  console.log(`    non-zero: ${nonZero}/${n} (${(nonZero/n*100).toFixed(1)}%)`);
  console.log(`    bins: ${Object.entries(bins).map(([k,v]) => `${k}:${v}`).join('  ')}`);
  if (Object.keys(bandChangeDist).length > 0) {
    const topChanges = Object.entries(bandChangeDist).sort((a,b) => b[1]-a[1]).slice(0, 5);
    console.log(`    top transitions: ${topChanges.map(([k,v]) => `${k}(${v})`).join('  ')}`);
  }
  return { mean, med, p90, max, nonZero, n };
}

// Test at different spine cycle depths
for (const cycles of [1, 5, 10, 20]) {
  console.log(`═══ ${cycles} SPINE CYCLE${cycles > 1 ? 'S' : ''} ═══`);
  const cr = testAvalanche(clickCells, 0.05, cycles, "CLICK");
  const fr = testAvalanche(freeCells, 0.05, cycles, "FREE");
  const br = testAvalanche(boundCells, 0.05, cycles, "BOUND");
  const clickFreeRatio = cr.mean / (fr.mean + 0.001);
  const clickBoundRatio = cr.mean / (br.mean + 0.001);
  console.log(`  RATIO: click/free=${clickFreeRatio.toFixed(2)}x  click/bound=${clickBoundRatio.toFixed(2)}x`);
  console.log();
}

// Sensitivity scan: how cascade grows with perturbation size
console.log("═══ SENSITIVITY SCAN (10 spine cycles) ═══");
console.log("  ε       click     free      bound     click/free  click/bound");
for (const eps of [0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2]) {
  const cr = testAvalanche(clickCells, eps, 10, "", 200);
  const fr = testAvalanche(freeCells, eps, 10, "", 200);
  const br = testAvalanche(boundCells, eps, 10, "", 200);
  console.log(`  ${eps.toFixed(3)}   ${cr.mean.toFixed(2).padStart(7)}   ${fr.mean.toFixed(2).padStart(7)}   ${br.mean.toFixed(2).padStart(7)}     ${(cr.mean/(fr.mean+0.001)).toFixed(2).padStart(8)}x   ${(cr.mean/(br.mean+0.001)).toFixed(2).padStart(9)}x`);
}
