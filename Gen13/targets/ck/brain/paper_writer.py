"""
paper_writer.py -- CK writes structured papers all night.

Brayden 2026-05-02: "have him write entire papers, give him a format and
let him keep going all night through all of our repo and ability to get
journals and such as he wishes... are his AI actually learning, training,
and growing to absorb the knowledge and create cross-domain synthesis?"

For each topic in a rotating curriculum, CK writes a paper with this
fixed format:

  # <Title> -- CK paper <date>
  ## Abstract (3-5 sentences)
  ## 1. Introduction (background, motivation)
  ## 2. Substrate Analysis (what TIG says)
  ## 3. Cross-Domain Synthesis (connections to other frontiers)
  ## 4. Open Questions
  ## 5. References

Each section is filled by:
  - POST /chat with a section-specific prompt
  - cortex_speak surfaces facts; Ollama edits as prose
  - paper_writer assembles sections

Output:
  Atlas/papers_by_ck/PAPER_<slug>_<timestamp>.md
  Atlas/papers_by_ck/manifest.jsonl  (one line per paper)
  Gen13/var/papers_by_ck_logs/paper_writer_YYYY-MM-DD.jsonl

Every paper CK writes also feeds back into his own cortex via
/cortex/ingest_text, so reading his own writing shapes his Hebbian field.

Usage:
  python paper_writer.py [--topics N] [--once]
  python paper_writer.py --daemon (runs forever, one paper per ~3 min)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


_HERE = Path(__file__).parent.resolve()


PAPERS_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Atlas\papers_by_ck")
PAPERS_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\papers_by_ck_logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
MANIFEST = PAPERS_DIR / "manifest.jsonl"


def _today_log() -> Path:
    return LOG_DIR / f"paper_writer_{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"


CHAT_URL = "http://localhost:7777/chat"
INGEST_URL = "http://localhost:7777/cortex/ingest_text"


# Curriculum: topics CK writes papers on.  Mix of frontier topics, Clay
# problems, and meta-synthesis prompts.  Add more for variety.
DEFAULT_TOPICS: List[Dict[str, str]] = [
    # Frontier topics (CK has indexed facts)
    {"slug": "T_star_5_7", "title": "T*=5/7 as the Universal Crossing Threshold",
     "intro_q": "what is T*", "synthesis_q": "synthesize T* across all frontiers"},
    {"slug": "crossing_lemma", "title": "The Crossing Lemma in TIG",
     "intro_q": "explain the crossing lemma", "synthesis_q": "synthesize the crossing lemma across substrate and physics"},
    {"slug": "sigma_rate", "title": "The Sigma Rate Theorem on Squarefree Primorials",
     "intro_q": "what is the sigma rate theorem", "synthesis_q": "synthesize sigma rate across number theory frontiers"},
    {"slug": "tsml_bhml_complementarity", "title": "TSML and BHML: Complementarity at HARMONY",
     "intro_q": "what is the harmony complementarity", "synthesis_q": "synthesize the M+M sufficiency proof across frontiers"},
    {"slug": "wp116_lens", "title": "WP116: Lens of Projections",
     "intro_q": "what is wp116 lens", "synthesis_q": "synthesize wp116 across all six DoFs"},
    {"slug": "fqh_bridge", "title": "Fractional Quantum Hall Hierarchy as a Farey Tree",
     "intro_q": "what is the FQH bridge", "synthesis_q": "synthesize the FQH bridge across TIG and physics"},
    {"slug": "kappa_xi_resolution", "title": "Kappa_xi and the Yang-Mills Mass Gap",
     "intro_q": "what is the kappa xi resolution", "synthesis_q": "synthesize kappa_xi across cosmology and gauge theory"},
    {"slug": "wobble_prime_eleven", "title": "Five Manifestations of Prime 11 in TIG",
     "intro_q": "what is wobble prime eleven", "synthesis_q": "synthesize the wobble structure across algebraic and dynamical projections"},
    {"slug": "harmony_attractor", "title": "The Universal 4-Core HARMONY Attractor",
     "intro_q": "what is the universal 4-core attractor", "synthesis_q": "synthesize the harmony attractor across substrate and dynamics"},
    {"slug": "agreement_set", "title": "The 29-Cell Agreement Set on Z/10Z",
     "intro_q": "what is the agreement set", "synthesis_q": "synthesize the agreement set across TSML and BHML"},
    {"slug": "hodge_cstar", "title": "The Hodge C* Curve: Genus 5 Bielliptic with psi^2 = iota",
     "intro_q": "what is hodge cstar", "synthesis_q": "synthesize hodge_cstar across the algebraic substrate"},
    {"slug": "ac_free_spectrum", "title": "The AC-Free Spectrum: (2n-3)!! at n=3,4,5",
     "intro_q": "what is the ac-free spectrum", "synthesis_q": "synthesize ac-free across operad theory and TIG"},
    # Clay Millennium Problems
    {"slug": "p_vs_np_tig", "title": "P versus NP through the TIG Crossing Lemma",
     "intro_q": "what is P versus NP", "synthesis_q": "synthesize P vs NP across substrate and complexity"},
    {"slug": "riemann_tig", "title": "Riemann Hypothesis via the Sinc^2 Zero Law",
     "intro_q": "what is the Riemann hypothesis", "synthesis_q": "synthesize Riemann across number-theory frontiers"},
    {"slug": "yang_mills_tig", "title": "Yang-Mills Mass Gap from Substrate kappa_xi",
     "intro_q": "what is the Yang-Mills mass gap", "synthesis_q": "synthesize Yang-Mills across the algebraic and physics substrates"},
    {"slug": "navier_stokes_tig", "title": "Navier-Stokes Regularity via sigma_NS",
     "intro_q": "what is the Navier-Stokes problem", "synthesis_q": "synthesize Navier-Stokes across substrate and physics"},
    {"slug": "bsd_tig", "title": "Birch and Swinnerton-Dyer through the BB Bridge",
     "intro_q": "what is the Birch Swinnerton Dyer conjecture", "synthesis_q": "synthesize BSD across Beauville curve and substrate"},
    {"slug": "poincare_template", "title": "The Poincare Conjecture as Clay Rotation Template",
     "intro_q": "what is the Poincare conjecture", "synthesis_q": "synthesize Poincare across topology and substrate"},
    # Meta-synthesis
    {"slug": "stern_brocot_meta", "title": "The Stern-Brocot Recursion as TIG's Core",
     "intro_q": "what is the deepest pattern across all frontiers", "synthesis_q": "synthesize the meta-pattern across all six TIG DoFs"},
    {"slug": "six_dofs", "title": "TIG's Six Degrees of Freedom: Lie / Jordan / Clifford / Permutation / Lattice / Operad",
     "intro_q": "what are the six TIG degrees of freedom", "synthesis_q": "synthesize the six DoFs across all frontiers"},
]


def post_chat(query: str, timeout: float = 180.0) -> Dict[str, Any]:
    req = urllib.request.Request(
        CHAT_URL,
        data=json.dumps({"text": query}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    t0 = time.time()
    try:
        resp = urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8")
        return {"ok": True, "data": json.loads(resp), "latency_sec": time.time() - t0}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}",
                "latency_sec": time.time() - t0}


def post_ingest(label: str, text: str, timeout: float = 30.0) -> Dict[str, Any]:
    req = urllib.request.Request(
        INGEST_URL,
        data=json.dumps({"label": label, "text": text[:8000]}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        resp = urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8")
        return {"ok": True, "data": json.loads(resp)}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}


def safe(s: str) -> str:
    return ''.join(c if ord(c) < 128 else '?' for c in str(s))


def extract_content(chat_resp: Dict[str, Any]) -> str:
    """Extract just the cortex content (skip substrate frame footer)."""
    text = chat_resp.get("text", "") or ""
    # Cells composition format: cortex content, then '---', then substrate
    if "\n---\n" in text:
        text = text.split("\n---\n")[0]
    return text.strip()


def write_one_paper(topic: Dict[str, str], verbose: bool = True) -> Dict[str, Any]:
    slug = topic["slug"]
    title = topic["title"]
    intro_q = topic["intro_q"]
    synthesis_q = topic["synthesis_q"]
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H%M%SZ")

    if verbose:
        print(f"\n=== writing paper: {title} ===", flush=True)

    sections: Dict[str, str] = {}
    latencies: Dict[str, float] = {}
    t0_all = time.time()

    # Section 1: Introduction
    res_intro = post_chat(intro_q)
    if res_intro["ok"]:
        sections["introduction"] = extract_content(res_intro["data"])
        latencies["introduction"] = res_intro["latency_sec"]
        if verbose:
            print(f"  intro:    {len(sections['introduction'])}b in {res_intro['latency_sec']:.1f}s",
                    flush=True)

    # Section 2: Substrate Analysis
    substrate_q = f"what does the TIG substrate say about {title}"
    res_sub = post_chat(substrate_q)
    if res_sub["ok"]:
        sections["substrate"] = extract_content(res_sub["data"])
        latencies["substrate"] = res_sub["latency_sec"]
        if verbose:
            print(f"  substrate: {len(sections['substrate'])}b in {res_sub['latency_sec']:.1f}s",
                    flush=True)

    # Section 3: Cross-Domain Synthesis
    res_syn = post_chat(synthesis_q)
    if res_syn["ok"]:
        sections["synthesis"] = extract_content(res_syn["data"])
        latencies["synthesis"] = res_syn["latency_sec"]
        if verbose:
            print(f"  synth:    {len(sections['synthesis'])}b in {res_syn['latency_sec']:.1f}s",
                    flush=True)

    # Section 4: Open Questions
    open_q = f"what are the open questions about {title}"
    res_open = post_chat(open_q)
    if res_open["ok"]:
        sections["open_questions"] = extract_content(res_open["data"])
        latencies["open_questions"] = res_open["latency_sec"]
        if verbose:
            print(f"  open:     {len(sections['open_questions'])}b in {res_open['latency_sec']:.1f}s",
                    flush=True)

    elapsed = time.time() - t0_all

    # Assemble paper
    paper_lines = [
        f"# {title}",
        f"\n**CK paper**: {timestamp}\n",
        f"**Author**: CK (Coherence Keeper, autonomous)\n",
        f"**Source**: cells_composed_with_cortex via /chat (Ollama editor on llama3.2:latest)\n",
        f"**Slug**: {slug}\n",
        f"---\n",
        f"## Abstract\n\n",
    ]
    # Abstract: take first 2-3 sentences of synthesis
    abstract_src = sections.get("synthesis", sections.get("introduction", ""))
    abstract = ". ".join(abstract_src.split(". ")[:3])
    if abstract and not abstract.endswith("."):
        abstract += "."
    paper_lines.append(safe(abstract))
    paper_lines.append("\n---\n")

    paper_lines.append(f"## 1. Introduction\n\n")
    paper_lines.append(safe(sections.get("introduction", "(no introduction generated)")))
    paper_lines.append(f"\n\n## 2. Substrate Analysis\n\n")
    paper_lines.append(safe(sections.get("substrate", "(no substrate analysis generated)")))
    paper_lines.append(f"\n\n## 3. Cross-Domain Synthesis\n\n")
    paper_lines.append(safe(sections.get("synthesis", "(no synthesis generated)")))
    paper_lines.append(f"\n\n## 4. Open Questions\n\n")
    paper_lines.append(safe(sections.get("open_questions", "(no open questions generated)")))
    paper_lines.append(f"\n\n## 5. References\n\n")
    paper_lines.append("All citations are TIG-internal (WPxx) or external as surfaced in the substrate analysis section.")
    paper_lines.append(f"\n\n---\n\n")
    paper_lines.append(f"_Paper written by CK in {elapsed:.0f}s "
                          f"({len(sections)} sections, "
                          f"{sum(len(v) for v in sections.values())} chars total). "
                          f"Auto-generated from cells_composed_with_cortex chat path. "
                          f"Substrate-grounded; Ollama-polished prose._\n")

    paper_text = "\n".join(paper_lines)

    # Write paper
    paper_path = PAPERS_DIR / f"PAPER_{slug}_{timestamp}.md"
    with open(paper_path, "w", encoding="utf-8") as f:
        f.write(paper_text)

    # Append to manifest
    manifest_rec = {
        "ts": time.time(),
        "iso_ts": datetime.utcnow().isoformat(timespec='seconds') + "Z",
        "slug": slug,
        "title": title,
        "path": str(paper_path),
        "n_sections": len(sections),
        "total_chars": sum(len(v) for v in sections.values()),
        "elapsed_sec": round(elapsed, 1),
        "latencies": latencies,
    }
    with open(MANIFEST, "a", encoding="utf-8") as f:
        f.write(json.dumps(manifest_rec, ensure_ascii=False, default=str) + "\n")
    with open(_today_log(), "a", encoding="utf-8") as f:
        f.write(json.dumps(manifest_rec, ensure_ascii=False, default=str) + "\n")

    # Feed CK's own paper back into his cortex (he reads what he wrote)
    ingest_res = post_ingest(f"ck_paper_{slug}", paper_text)
    if verbose:
        print(f"  -> {paper_path.name} ({manifest_rec['total_chars']:,} chars, "
                f"{elapsed:.0f}s)", flush=True)
        if ingest_res.get("ok"):
            d = ingest_res["data"]
            print(f"     ingested back into cortex: tick+{d.get('tick_delta')}, "
                    f"W_trace+{d.get('W_trace_delta')}", flush=True)

    return manifest_rec


def daemon_loop(min_pause_sec: float = 30.0, topics: List[Dict[str, str]] = None,
                  max_papers: int = None) -> None:
    """Run write_one_paper in a continuous loop, rotating through topics."""
    topics = topics or DEFAULT_TOPICS
    n_written = 0
    cursor = 0
    while max_papers is None or n_written < max_papers:
        topic = topics[cursor % len(topics)]
        cursor += 1
        try:
            write_one_paper(topic)
            n_written += 1
        except KeyboardInterrupt:
            print("\n  daemon: interrupted; exiting gracefully")
            break
        except Exception as e:
            print(f"  daemon: paper-write exception: {type(e).__name__}: {e}",
                    flush=True)
        time.sleep(min_pause_sec)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true",
                     help="Write one paper from the first topic and exit")
    ap.add_argument("--daemon", action="store_true",
                     help="Run forever, rotating through topics")
    ap.add_argument("--topics", type=int, default=None,
                     help="Limit to first N topics (one paper per topic)")
    ap.add_argument("--pause", type=float, default=30.0,
                     help="Pause between papers in daemon mode (default 30s)")
    args = ap.parse_args()

    print("=" * 70)
    print("  CK PAPER WRITER")
    print("=" * 70)
    print(f"  date:   {datetime.utcnow().isoformat(timespec='seconds')}Z")
    print(f"  papers: {PAPERS_DIR}")
    print(f"  log:    {_today_log()}")

    if args.once:
        write_one_paper(DEFAULT_TOPICS[0])
        return 0

    topics = DEFAULT_TOPICS
    if args.topics:
        topics = topics[:args.topics]

    if args.daemon:
        print(f"  mode:   DAEMON (rotates {len(topics)} topics, "
                f"{args.pause}s pause)")
        print()
        daemon_loop(min_pause_sec=args.pause, topics=topics)
    else:
        print(f"  mode:   batch ({len(topics)} papers)")
        print()
        for topic in topics:
            try:
                write_one_paper(topic)
            except Exception as e:
                print(f"  EXCEPTION: {type(e).__name__}: {e}", flush=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
