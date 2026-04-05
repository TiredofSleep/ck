import { useState, useEffect, useRef, useCallback } from "react";

// ─── RING MATH ────────────────────────────────────────────────────────────────
function gcd(a, b) { return b === 0 ? a : gcd(b, a % b); }

function getAlphaBeta(n) {
  const idems = [];
  for (let x = 2; x < n - 1; x++) if ((x * x) % n === x) idems.push(x);
  if (!idems.length) return { alpha: null, beta: null, f: null };
  const alpha = Math.min(...idems);
  const units = [];
  for (let k = 1; k < n; k++) if (gcd(k, n) === 1) units.push(k);
  const ordMod = (u) => {
    let v = u, o = 1;
    while (v !== 1) { v = (v * u) % n; o++; }
    return o;
  };
  const maxOrd = Math.max(...units.map(ordMod));
  const cands = units.filter(u => ordMod(u) === maxOrd && u > alpha);
  const beta = cands.length ? Math.min(...cands) : null;
  const f = beta ? alpha / beta : null;
  return { alpha, beta, f, maxOrd };
}

function getCycles(ruleFn, n) {
  const visitedGlobal = new Set();
  const cycles = [];
  for (let start = 0; start < n; start++) {
    if (visitedGlobal.has(start)) continue;
    const path = [start];
    const visitedIdx = new Map([[start, 0]]);
    let x = ruleFn(start, n);
    while (!visitedIdx.has(x)) {
      visitedIdx.set(x, path.length);
      path.push(x);
      x = ruleFn(x, n);
    }
    const cycleStartIdx = visitedIdx.get(x);
    const tail = path.slice(0, cycleStartIdx);
    const cycle = path.slice(cycleStartIdx);
    path.forEach(n => visitedGlobal.add(n));
    cycles.push({ tail, cycle });
  }
  return cycles;
}

const RULES = {
  "×3":   (x, n) => (3 * x) % n,
  "+1":   (x, n) => (x + 1) % n,
  "3x+1": (x, n) => (3 * x + 1) % n,
  "×7":   (x, n) => (7 * x) % n,
};

// ─── PALETTE ──────────────────────────────────────────────────────────────────
const PALETTE = {
  bg: "#0a0a0f",
  surface: "#12121a",
  border: "#1e1e2e",
  alpha: "#f97316",   // orange — absorbing
  beta:  "#a78bfa",   // violet — max-order
  unit:  "#38bdf8",   // sky    — unit orbit
  even:  "#22d3ee",   // cyan   — even orbit
  fixed: "#4ade80",   // green  — other fixed
  trail: "#e2e8f066", // ghost trail
  arrow: "#f8fafc",
  text:  "#e2e8f0",
  dim:   "#64748b",
  gold:  "#fbbf24",
};

function nodeColor(x, n, alpha, beta) {
  if (x === alpha) return PALETTE.alpha;
  if (x === beta)  return PALETTE.beta;
  if (x === 0)     return PALETTE.fixed;
  if (gcd(x, n) === 1) return PALETTE.unit;
  if (x % 2 === 0) return PALETTE.even;
  return PALETTE.dim;
}

// ─── CANVAS HELPERS ───────────────────────────────────────────────────────────
function circlePos(i, n, cx, cy, r) {
  const angle = (2 * Math.PI * i) / n - Math.PI / 2;
  return [cx + r * Math.cos(angle), cy + r * Math.sin(angle)];
}

function drawArrow(ctx, x1, y1, x2, y2, color, width = 1.5, headLen = 8) {
  const dx = x2 - x1, dy = y2 - y1;
  const dist = Math.sqrt(dx*dx+dy*dy);
  if (dist < 1) return;
  const nx = dx/dist, ny = dy/dist;
  const mx = (x1+x2)/2, my = (y1+y2)/2;
  ctx.strokeStyle = color; ctx.lineWidth = width;
  ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
  const angle = Math.atan2(dy, dx);
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.moveTo(mx + nx*headLen, my + ny*headLen);
  ctx.lineTo(mx + (-ny-nx*0.5)*headLen*0.5, my + (nx-ny*0.5)*headLen*0.5);
  ctx.lineTo(mx + (ny-nx*0.5)*headLen*0.5, my + (-nx-ny*0.5)*headLen*0.5);
  ctx.closePath(); ctx.fill();
}

function drawSelfLoop(ctx, x, y, color, r = 14) {
  ctx.strokeStyle = color; ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.arc(x, y - r * 1.4, r, 0.3, Math.PI * 1.8);
  ctx.stroke();
}

// ─── MAIN COMPONENT ───────────────────────────────────────────────────────────
export default function ZnZFlow() {
  const [n, setN] = useState(10);
  const [rule, setRule] = useState("×3");
  const [hoveredNode, setHoveredNode] = useState(null);
  const [step, setStep] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [trailNodes, setTrailNodes] = useState([]);
  const canvasRef = useRef(null);
  const animRef = useRef(null);

  const ringData = getAlphaBeta(n);
  const { alpha, beta, f } = ringData;
  const ruleFn = RULES[rule];
  const cycles = getCycles(ruleFn, n);

  const SIZE = 420;
  const CX = SIZE / 2, CY = SIZE / 2;
  const R = SIZE * 0.36;
  const NODE_R = Math.max(10, Math.min(16, 160 / n));

  // Build successor map
  const successors = {};
  for (let x = 0; x < n; x++) successors[x] = ruleFn(x, n);

  // Draw
  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, SIZE, SIZE);

    // Background glow for alpha/beta
    [alpha, beta].forEach((v, i) => {
      if (v == null) return;
      const [px, py] = circlePos(v, n, CX, CY, R);
      const grad = ctx.createRadialGradient(px, py, 0, px, py, 48);
      grad.addColorStop(0, i === 0 ? "#f9731622" : "#a78bfa22");
      grad.addColorStop(1, "transparent");
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, SIZE, SIZE);
    });

    // Draw edges first (arrows)
    for (let x = 0; x < n; x++) {
      const s = successors[x];
      const [x1, y1] = circlePos(x, n, CX, CY, R);
      const [x2, y2] = circlePos(s, n, CX, CY, R);
      const col = nodeColor(x, n, alpha, beta) + "88";
      if (x === s) {
        drawSelfLoop(ctx, x1, y1, col, NODE_R * 1.1);
      } else {
        const shrink = NODE_R + 2;
        const dx = x2-x1, dy = y2-y1, d = Math.sqrt(dx*dx+dy*dy);
        const nx = dx/d, ny = dy/d;
        drawArrow(ctx, x1+nx*shrink, y1+ny*shrink, x2-nx*shrink, y2-ny*shrink, col, 1.4, 7);
      }
    }

    // Trail
    trailNodes.forEach((tx, idx) => {
      const [px, py] = circlePos(tx, n, CX, CY, R);
      const alpha_val = (idx / trailNodes.length) * 0.5;
      ctx.fillStyle = `rgba(249,115,22,${alpha_val})`;
      ctx.beginPath();
      ctx.arc(px, py, NODE_R * 0.5, 0, Math.PI * 2);
      ctx.fill();
    });

    // Draw nodes
    for (let x = 0; x < n; x++) {
      const [px, py] = circlePos(x, n, CX, CY, R);
      const col = nodeColor(x, n, alpha, beta);
      const isHovered = x === hoveredNode;
      const nodeSize = isHovered ? NODE_R * 1.4 : NODE_R;

      // Shadow
      ctx.shadowColor = col;
      ctx.shadowBlur = isHovered ? 20 : (x === alpha || x === beta ? 14 : 6);

      ctx.fillStyle = isHovered ? "#fff" : col;
      ctx.beginPath();
      ctx.arc(px, py, nodeSize, 0, Math.PI * 2);
      ctx.fill();

      ctx.shadowBlur = 0;

      // Label
      ctx.fillStyle = isHovered ? "#000" : "#0a0a0f";
      ctx.font = `bold ${Math.max(9, NODE_R * 0.75)}px 'JetBrains Mono', monospace`;
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(x, px, py);
    }

    // Special badges
    if (alpha != null) {
      const [px, py] = circlePos(alpha, n, CX, CY, R);
      ctx.fillStyle = PALETTE.alpha;
      ctx.font = `bold 9px monospace`;
      ctx.fillText("α", px + NODE_R + 6, py - NODE_R + 2);
    }
    if (beta != null) {
      const [px, py] = circlePos(beta, n, CX, CY, R);
      ctx.fillStyle = PALETTE.beta;
      ctx.font = `bold 9px monospace`;
      ctx.fillText("β", px + NODE_R + 6, py - NODE_R + 2);
    }
  }, [n, rule, hoveredNode, trailNodes, alpha, beta]);

  useEffect(() => { draw(); }, [draw]);

  // Animation: walk forward from alpha
  useEffect(() => {
    if (playing) {
      let current = alpha ?? 0;
      let trail = [current];
      let localStep = 0;
      animRef.current = setInterval(() => {
        current = ruleFn(current, n);
        trail = [...trail.slice(-12), current];
        setTrailNodes([...trail]);
        setStep(s => s + 1);
        localStep++;
        if (localStep > 60) setPlaying(false);
      }, 180);
    } else {
      clearInterval(animRef.current);
    }
    return () => clearInterval(animRef.current);
  }, [playing, n, rule, alpha]);

  // Hover detection
  const handleMouseMove = useCallback((e) => {
    const rect = canvasRef.current?.getBoundingClientRect();
    if (!rect) return;
    const mx = (e.clientX - rect.left) * (SIZE / rect.width);
    const my = (e.clientY - rect.top) * (SIZE / rect.height);
    let found = null;
    for (let x = 0; x < n; x++) {
      const [px, py] = circlePos(x, n, CX, CY, R);
      if (Math.sqrt((mx-px)**2+(my-py)**2) < NODE_R + 4) { found = x; break; }
    }
    setHoveredNode(found);
  }, [n]);

  const handleMouseLeave = () => setHoveredNode(null);

  // Cycle analysis
  const cycleTable = cycles.map(c => ({
    tail: c.tail,
    cycle: c.cycle,
    containsAlpha: alpha != null && c.cycle.includes(alpha),
    containsBeta:  beta  != null && c.cycle.includes(beta),
  }));

  const hoveredSucc = hoveredNode != null ? successors[hoveredNode] : null;

  return (
    <div style={{
      background: PALETTE.bg,
      minHeight: "100vh",
      color: PALETTE.text,
      fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      padding: "24px 16px",
      gap: "20px",
    }}>
      {/* Title */}
      <div style={{ textAlign: "center" }}>
        <div style={{ fontSize: "11px", letterSpacing: "4px", color: PALETTE.dim, marginBottom: "6px" }}>
          FLOW VISUALIZATION
        </div>
        <div style={{ fontSize: "22px", fontWeight: 700, letterSpacing: "-0.5px" }}>
          ℤ/<span style={{ color: PALETTE.gold }}>{n}</span>ℤ — Dynamic Flow
        </div>
      </div>

      {/* Controls row */}
      <div style={{ display: "flex", gap: "10px", flexWrap: "wrap", justifyContent: "center" }}>
        {/* Modulus */}
        <div style={{ display: "flex", flexDirection: "column", gap: "4px", alignItems: "center" }}>
          <div style={{ fontSize: "9px", color: PALETTE.dim, letterSpacing: "2px" }}>MODULUS n</div>
          <div style={{ display: "flex", gap: "4px" }}>
            {[6, 10, 12, 18, 20].map(v => (
              <button key={v} onClick={() => { setN(v); setTrailNodes([]); setStep(0); setPlaying(false); }}
                style={{
                  background: n === v ? PALETTE.gold : PALETTE.surface,
                  color: n === v ? "#000" : PALETTE.text,
                  border: `1px solid ${n === v ? PALETTE.gold : PALETTE.border}`,
                  borderRadius: "4px", padding: "4px 10px", cursor: "pointer",
                  fontSize: "12px", fontFamily: "inherit", fontWeight: n===v?700:400,
                }}>
                {v}
              </button>
            ))}
          </div>
        </div>

        {/* Rule */}
        <div style={{ display: "flex", flexDirection: "column", gap: "4px", alignItems: "center" }}>
          <div style={{ fontSize: "9px", color: PALETTE.dim, letterSpacing: "2px" }}>RULE x →</div>
          <div style={{ display: "flex", gap: "4px" }}>
            {Object.keys(RULES).map(r => (
              <button key={r} onClick={() => { setRule(r); setTrailNodes([]); setStep(0); setPlaying(false); }}
                style={{
                  background: rule === r ? PALETTE.unit : PALETTE.surface,
                  color: rule === r ? "#000" : PALETTE.text,
                  border: `1px solid ${rule === r ? PALETTE.unit : PALETTE.border}`,
                  borderRadius: "4px", padding: "4px 10px", cursor: "pointer",
                  fontSize: "12px", fontFamily: "inherit", fontWeight: rule===r?700:400,
                }}>
                {r}
              </button>
            ))}
          </div>
        </div>

        {/* Play/stop */}
        <div style={{ display: "flex", flexDirection: "column", gap: "4px", alignItems: "center" }}>
          <div style={{ fontSize: "9px", color: PALETTE.dim, letterSpacing: "2px" }}>TRACE FROM α</div>
          <button
            onClick={() => { setTrailNodes([]); setStep(0); setPlaying(p => !p); }}
            style={{
              background: playing ? "#ef444420" : "#4ade8020",
              color: playing ? "#ef4444" : "#4ade80",
              border: `1px solid ${playing ? "#ef4444" : "#4ade80"}`,
              borderRadius: "4px", padding: "4px 16px", cursor: "pointer",
              fontSize: "12px", fontFamily: "inherit", fontWeight: 600,
            }}>
            {playing ? "■ STOP" : "▶ PLAY"}
          </button>
        </div>
      </div>

      {/* Main layout */}
      <div style={{ display: "flex", gap: "20px", flexWrap: "wrap", justifyContent: "center", alignItems: "flex-start" }}>

        {/* Canvas */}
        <div style={{ position: "relative" }}>
          <canvas
            ref={canvasRef}
            width={SIZE} height={SIZE}
            onMouseMove={handleMouseMove}
            onMouseLeave={handleMouseLeave}
            style={{
              border: `1px solid ${PALETTE.border}`,
              borderRadius: "12px",
              cursor: hoveredNode != null ? "crosshair" : "default",
              maxWidth: "100%",
            }}
          />
          {/* Hover tooltip */}
          {hoveredNode != null && (
            <div style={{
              position: "absolute", bottom: "12px", left: "50%",
              transform: "translateX(-50%)",
              background: PALETTE.surface,
              border: `1px solid ${nodeColor(hoveredNode, n, alpha, beta)}`,
              borderRadius: "6px", padding: "6px 12px",
              fontSize: "11px", color: PALETTE.text, whiteSpace: "nowrap",
              pointerEvents: "none",
            }}>
              <span style={{ color: nodeColor(hoveredNode, n, alpha, beta), fontWeight: 700 }}>
                {hoveredNode}
              </span>
              {" → "}
              <span style={{ color: nodeColor(hoveredSucc, n, alpha, beta), fontWeight: 700 }}>
                {hoveredSucc}
              </span>
              {hoveredNode === alpha && <span style={{ color: PALETTE.alpha }}> [α absorber]</span>}
              {hoveredNode === beta  && <span style={{ color: PALETTE.beta  }}> [β max-order]</span>}
              {hoveredNode === 0     && <span style={{ color: PALETTE.fixed }}> [0 void]</span>}
            </div>
          )}
        </div>

        {/* Right panel */}
        <div style={{ display: "flex", flexDirection: "column", gap: "12px", minWidth: "220px" }}>

          {/* Ring constants */}
          <div style={{ background: PALETTE.surface, border: `1px solid ${PALETTE.border}`, borderRadius: "8px", padding: "14px" }}>
            <div style={{ fontSize: "9px", letterSpacing: "3px", color: PALETTE.dim, marginBottom: "10px" }}>RING CONSTANTS</div>
            <div style={{ display: "flex", flexDirection: "column", gap: "7px", fontSize: "13px" }}>
              <div><span style={{ color: PALETTE.dim }}>n = </span><span style={{ color: PALETTE.gold }}>{n}</span></div>
              <div><span style={{ color: PALETTE.dim }}>α = </span><span style={{ color: PALETTE.alpha }}>{alpha ?? "—"}</span><span style={{ color: PALETTE.dim, fontSize: "10px" }}> (absorber)</span></div>
              <div><span style={{ color: PALETTE.dim }}>β = </span><span style={{ color: PALETTE.beta }}>{beta ?? "—"}</span><span style={{ color: PALETTE.dim, fontSize: "10px" }}> (max-order)</span></div>
              <div style={{ borderTop: `1px solid ${PALETTE.border}`, paddingTop: "7px" }}>
                <span style={{ color: PALETTE.dim }}>f = α/β = </span>
                <span style={{ color: PALETTE.gold, fontWeight: 700 }}>
                  {f != null ? `${alpha}/${beta} = ${f.toFixed(4)}` : "—"}
                </span>
              </div>
              {n === 10 && <div style={{ color: "#4ade80", fontSize: "10px" }}>= T* (empirical threshold)</div>}
            </div>
          </div>

          {/* Legend */}
          <div style={{ background: PALETTE.surface, border: `1px solid ${PALETTE.border}`, borderRadius: "8px", padding: "14px" }}>
            <div style={{ fontSize: "9px", letterSpacing: "3px", color: PALETTE.dim, marginBottom: "10px" }}>LEGEND</div>
            {[
              [PALETTE.alpha, "α — absorbing idempotent"],
              [PALETTE.beta,  "β — max-order unit > α"],
              [PALETTE.unit,  "unit orbit (ℤ/nℤ)*"],
              [PALETTE.even,  "non-unit even"],
              [PALETTE.fixed, "0 — void fixed"],
            ].map(([col, label]) => (
              <div key={label} style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "5px", fontSize: "11px" }}>
                <div style={{ width: "10px", height: "10px", borderRadius: "50%", background: col, flexShrink: 0 }} />
                <span style={{ color: PALETTE.dim }}>{label}</span>
              </div>
            ))}
          </div>

          {/* Cycle table */}
          <div style={{ background: PALETTE.surface, border: `1px solid ${PALETTE.border}`, borderRadius: "8px", padding: "14px" }}>
            <div style={{ fontSize: "9px", letterSpacing: "3px", color: PALETTE.dim, marginBottom: "10px" }}>
              CYCLE STRUCTURE — {rule}
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: "5px", maxHeight: "180px", overflowY: "auto" }}>
              {cycleTable.map((c, i) => (
                <div key={i} style={{ fontSize: "10px", lineHeight: 1.5 }}>
                  {c.tail.length > 0 && (
                    <span style={{ color: PALETTE.dim }}>tail {JSON.stringify(c.tail)} → </span>
                  )}
                  <span style={{
                    color: c.containsAlpha ? PALETTE.alpha : c.containsBeta ? PALETTE.beta : PALETTE.unit,
                    fontWeight: (c.containsAlpha || c.containsBeta) ? 700 : 400,
                  }}>
                    cycle{JSON.stringify(c.cycle)}
                    {c.containsAlpha && " [α]"}
                    {c.containsBeta  && " [β]"}
                  </span>
                </div>
              ))}
            </div>
          </div>

        </div>
      </div>

      {/* Bottom observation row */}
      <div style={{
        background: PALETTE.surface,
        border: `1px solid ${PALETTE.border}`,
        borderRadius: "8px", padding: "12px 16px",
        maxWidth: "680px", width: "100%",
        fontSize: "11px", color: PALETTE.dim, lineHeight: 1.7,
      }}>
        <span style={{ color: PALETTE.text, fontWeight: 700 }}>KEY OBSERVATION — {rule} on ℤ/{n}ℤ: </span>
        {rule === "×3" && n === 10 && "α=5 is a fixed point (absorbing). β=7 lives in the unit 4-cycle {1,3,7,9}. These two orbits are structurally isolated — no path from unit orbit reaches α under ×3 alone."}
        {rule === "×7" && n === 10 && "β=7 generates the same 4-cycle as ×3. α=5 remains fixed. The COLLAPSE rule maps unit orbit to itself identically."}
        {rule === "+1" && n === 10 && "Additive drift is a single n-cycle. All structure dissolves — α and β are indistinguishable from any other element. No arithmetic selector survives pure drift."}
        {rule === "3x+1" && n === 10 && "Mixed rule: α=5 enters the cycle {5,6,9,8}. No longer isolated. β=7 appears in cycle {2,7}. The arithmetic selector structure partially dissolves under mixing."}
        {!["×3","×7","+1","3x+1"].includes(rule) && "Select a rule to see observations."}
        {n !== 10 && " — Note: arithmetic selector f=" + (f != null ? `${alpha}/${beta}` : "—") + " for this modulus."}
      </div>

      {/* Footer */}
      <div style={{ fontSize: "9px", color: PALETTE.dim, letterSpacing: "2px", textAlign: "center" }}>
        SPRINT 8 · Z/nZ FLOW DYNAMICS · TIG / CK RESEARCH · 7SITE LLC
      </div>
    </div>
  );
}
