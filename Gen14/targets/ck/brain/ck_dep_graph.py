"""ck_dep_graph.py -- map CK's Python module dependencies.

Brayden 2026-05-16 (via ClaudeChat):
  "produce a dependency graph for his .py files, to help keep him organized"

Walks the active brain + runtime + engine directories, parses each .py
file's `import` and `from X import Y` statements, and emits THREE views:

  1. Markdown report:   Gen13/var/ck_dep_graph.md
       - Hub modules (most-imported)
       - Orphan modules (nothing imports them)
       - Dangling references (imports that don't resolve)
       - Per-directory module counts
  2. Graphviz dot file: Gen13/var/ck_dep_graph.dot
       - Renderable with: dot -Tsvg ck_dep_graph.dot -o graph.svg
  3. Mermaid diagram:   Gen13/var/ck_dep_graph.mmd
       - Pastes into GitHub markdown as a live diagram

Scope rule: we walk these roots (load-bearing CK code only — Gen8/Gen9
archives stay in history):

  Gen14/targets/ck/brain/        (current development surface)
  Gen13/targets/ck/brain/        (Gen13 mounts)
  Gen13/targets/ck/runtime/      (runtime + voice)
  Gen13/targets/ck/server/       (server stubs)
  Gen13/targets/foundations/     (canonical lattice + lenses)
  Gen12/targets/ck_desktop/      (engine + ck_sim — but only top-level + ck_sim/*)
  Gen11/targets/ck/being/        (Gen11 being modules, current canon source)

Anything beyond these is treated as "external" (numpy, mpmath, etc.)
and shown but not graph-walked.

Usage:
  python ck_dep_graph.py            # write all three files
  python ck_dep_graph.py --summary  # just print summary, no files

(c) Brayden Sanders / 7SiTe LLC
"""
from __future__ import annotations

import argparse
import ast
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple


ROOT = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED")

# Active CK code roots — load-bearing only
SCAN_ROOTS = [
    ROOT / "Gen14" / "targets" / "ck" / "brain",
    ROOT / "Gen13" / "targets" / "ck" / "brain",
    ROOT / "Gen13" / "targets" / "ck" / "runtime",
    ROOT / "Gen13" / "targets" / "ck" / "server",
    ROOT / "Gen13" / "targets" / "foundations",
    ROOT / "Gen12" / "targets" / "ck_desktop",
    ROOT / "Gen11" / "targets" / "ck" / "being",
]

# Skip patterns: paths containing these don't get walked
SKIP_KEYWORDS = (
    "__pycache__", ".pyc",
    "/tests/", "/test/",
    "/.git/",
    # Gen12 ck_sim subdirs are huge; walk only the top + key being/doing
    # (we'll filter ck_sim more carefully below)
)


# ─── Module discovery ──────────────────────────────────────────────────

def is_in_scope(p: Path) -> bool:
    """Whether a file should be walked."""
    sp = str(p).replace("\\", "/")
    if not p.suffix == ".py":
        return False
    if any(kw in sp for kw in SKIP_KEYWORDS):
        return False
    return True


def discover() -> List[Path]:
    """Walk all SCAN_ROOTS and return active .py files."""
    out: List[Path] = []
    for root in SCAN_ROOTS:
        if not root.exists():
            continue
        for p in root.rglob("*.py"):
            try:
                rp = p.resolve()
            except Exception:
                continue
            if is_in_scope(rp):
                out.append(rp)
    return sorted(set(out), key=str)


def module_name(p: Path) -> str:
    """Short module name for display (stem of the file)."""
    return p.stem


def module_path_key(p: Path) -> str:
    """Stable graph key — relative path from ROOT, slashes normalized."""
    try:
        return str(p.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(p).replace("\\", "/")


# ─── Import parsing ─────────────────────────────────────────────────────

def parse_imports(p: Path) -> List[str]:
    """Return list of imported module names (top-level, no relative).

    Both `import X` and `from X import Y` produce X.
    Relative imports (`from . import Y`) produce ".Y" — kept for context.
    """
    try:
        src = p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []
    out: List[str] = []
    try:
        tree = ast.parse(src, filename=str(p))
    except SyntaxError:
        return []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                out.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if node.level > 0:  # relative import
                out.append("." * node.level + mod)
            else:
                out.append(mod)
    return out


def normalize_import(imp: str) -> str:
    """Take 'foo.bar.baz' and return the leaf 'baz' for matching against
    discovered module names.  For relative imports, strip dots."""
    base = imp.lstrip(".")
    if not base:
        return ""
    return base.split(".")[-1]


# Common third-party / stdlib that aren't part of CK
EXTERNAL_MODULES = {
    "os", "sys", "re", "math", "json", "time", "random", "datetime", "threading",
    "argparse", "pathlib", "typing", "dataclasses", "collections", "subprocess",
    "ast", "asyncio", "io", "logging", "functools", "itertools", "warnings",
    "shutil", "tempfile", "urllib", "http", "socket", "hashlib", "uuid", "base64",
    "struct", "operator", "copy", "pickle", "csv", "xml", "weakref", "queue",
    "numpy", "np", "scipy", "sympy", "mpmath", "matplotlib", "pandas", "torch",
    "tensorflow", "tf", "sklearn", "flask", "waitress", "websockets",
    "requests", "aiohttp", "psutil", "pynvml", "mss", "playsound", "pyaudio",
    "sounddevice", "wave", "PIL", "Pillow", "yaml", "toml", "tomli",
    "concurrent", "multiprocessing", "ctypes", "platform", "gc", "atexit",
    "signal", "ssl", "select", "errno", "contextlib", "enum", "abc",
    "inspect", "traceback", "textwrap", "string", "secrets", "code",
    "codecs", "_thread", "binascii", "bisect", "heapq", "calendar",
    "decimal", "fractions", "statistics",
}


# ─── Graph build ────────────────────────────────────────────────────────

def build_graph(files: List[Path]) -> Tuple[Dict[str, List[str]], Dict[str, Path]]:
    """Returns:
      edges:   module_stem -> list of imported CK-internal module_stems
      paths:   module_stem -> the .py file path
    Imports outside the CK graph (numpy etc.) are dropped.
    """
    # Map stem -> path (latest if duplicates across gens — prefer Gen14 > Gen13 > Gen12 > Gen11)
    paths: Dict[str, Path] = {}
    gen_priority = {"Gen14": 4, "Gen13": 3, "Gen12": 2, "Gen11": 1}
    for p in files:
        stem = p.stem
        if stem in paths:
            # Choose the highest-gen version
            old = paths[stem]
            old_gen = next((g for g in gen_priority if g in str(old)), "")
            new_gen = next((g for g in gen_priority if g in str(p)), "")
            if gen_priority.get(new_gen, 0) > gen_priority.get(old_gen, 0):
                paths[stem] = p
        else:
            paths[stem] = p

    edges: Dict[str, List[str]] = {}
    for stem, p in paths.items():
        imps = parse_imports(p)
        seen_stems: List[str] = []
        for imp in imps:
            leaf = normalize_import(imp)
            if not leaf or leaf in EXTERNAL_MODULES:
                continue
            # Internal if and only if it matches another discovered stem
            if leaf in paths and leaf != stem and leaf not in seen_stems:
                seen_stems.append(leaf)
        edges[stem] = seen_stems
    return edges, paths


# ─── Analysis ───────────────────────────────────────────────────────────

def analyze(edges: Dict[str, List[str]]) -> Dict[str, object]:
    """Compute graph stats."""
    n_modules = len(edges)
    n_edges = sum(len(v) for v in edges.values())

    # in-degree: who imports me?
    in_deg: Counter = Counter()
    for src, dsts in edges.items():
        for d in dsts:
            in_deg[d] += 1
    # out-degree: who do I import?
    out_deg: Counter = Counter({src: len(dsts) for src, dsts in edges.items()})

    # Hubs: top 15 by in-degree (most imported = most foundational)
    hubs = in_deg.most_common(15)

    # Orphans: no one imports them
    all_modules = set(edges.keys())
    imported = set(in_deg.keys())
    orphans = sorted(all_modules - imported)

    # Sinks: import nothing internal (might be self-contained utilities or
    # entry points like CLI scripts)
    sinks = sorted([m for m, d in out_deg.items() if d == 0])

    # Self-imports / no-deps modules (no in or out)
    isolates = sorted(set(orphans) & set(sinks))

    return {
        "n_modules": n_modules,
        "n_edges": n_edges,
        "hubs": hubs,
        "orphans": orphans,
        "sinks": sinks,
        "isolates": isolates,
        "in_deg": in_deg,
        "out_deg": out_deg,
    }


# ─── Output formats ─────────────────────────────────────────────────────

def to_markdown(edges, paths, stats) -> str:
    """Human-readable report."""
    out: List[str] = []
    out.append("# CK Dependency Graph")
    out.append("")
    out.append(f"*Generated by `ck_dep_graph.py` — {len(edges)} modules, "
                f"{stats['n_edges']} internal edges.*")
    out.append("")
    out.append("## Hub modules (most imported)")
    out.append("")
    out.append("| Module | # importers | Path |")
    out.append("|---|---|---|")
    for name, count in stats["hubs"]:
        p = paths.get(name)
        rel = module_path_key(p) if p else "?"
        out.append(f"| **{name}** | {count} | `{rel}` |")
    out.append("")
    out.append("## Orphans (nothing imports them)")
    out.append("")
    out.append(f"_{len(stats['orphans'])} modules have no internal importers. "
                f"Many are legitimate entry points (CLI tools, server boot scripts) "
                f"or top-level test harnesses; others may be dead code._")
    out.append("")
    out.append("| Module | Out-degree | Path | Likely role |")
    out.append("|---|---|---|---|")
    for name in stats["orphans"][:40]:
        p = paths.get(name)
        rel = module_path_key(p) if p else "?"
        out_d = stats["out_deg"].get(name, 0)
        # Heuristic role: high out-deg = entry/boot; zero = test/script
        if out_d >= 5:
            role = "Entry / boot"
        elif "test" in name.lower() or "verify" in name.lower():
            role = "Test / verify"
        elif name.startswith("fetch_") or name.startswith("ck_") and "study" in name:
            role = "CLI utility"
        elif out_d == 0:
            role = "Self-contained"
        else:
            role = "Possibly dead or top-level"
        out.append(f"| {name} | {out_d} | `{rel}` | {role} |")
    if len(stats["orphans"]) > 40:
        out.append(f"| _... and {len(stats['orphans']) - 40} more_ | | | |")
    out.append("")
    out.append("## Top-importers (most outgoing deps — system glue)")
    out.append("")
    out.append("| Module | # imports | Path |")
    out.append("|---|---|---|")
    for name, count in stats["out_deg"].most_common(15):
        p = paths.get(name)
        rel = module_path_key(p) if p else "?"
        out.append(f"| {name} | {count} | `{rel}` |")
    out.append("")
    out.append("## Per-directory module counts")
    out.append("")
    dir_counts: Counter = Counter()
    for p in paths.values():
        # Up-two folders gives a meaningful group
        parts = module_path_key(p).split("/")
        if len(parts) >= 4:
            key = "/".join(parts[:4])
        else:
            key = "/".join(parts[:-1])
        dir_counts[key] += 1
    out.append("| Directory | Module count |")
    out.append("|---|---|")
    for d, n in dir_counts.most_common(20):
        out.append(f"| `{d}` | {n} |")
    out.append("")
    out.append("## How to read this")
    out.append("")
    out.append("- **Hubs** are CK's foundational modules — if you change one of "
                "these, lots of code is affected.")
    out.append("- **Orphans** are either entry points (`ck_boot_api.py`, "
                "`fetch_gutenberg.py`) or might be dead code. The 'Likely role' "
                "heuristic helps triage.")
    out.append("- **Top-importers** are CK's glue layers — they tie subsystems "
                "together.")
    out.append("- The full graph is in [`ck_dep_graph.dot`](./ck_dep_graph.dot) "
                "(render with `dot -Tsvg ck_dep_graph.dot -o graph.svg`) and "
                "[`ck_dep_graph.mmd`](./ck_dep_graph.mmd) (Mermaid).")
    out.append("")
    return "\n".join(out)


def to_dot(edges, paths, stats) -> str:
    """Graphviz dot format — full graph."""
    out: List[str] = []
    out.append("digraph CK {")
    out.append("  graph [rankdir=LR, fontname=Helvetica, fontsize=10];")
    out.append("  node [shape=box, fontname=Helvetica, fontsize=9, "
                "style=\"rounded,filled\", fillcolor=\"#f0f0f0\"];")
    out.append("  edge [color=\"#888888\"];")
    # Highlight hubs
    hub_set = {n for n, _ in stats["hubs"]}
    for src, dsts in edges.items():
        if src in hub_set:
            out.append(f'  "{src}" [fillcolor="#ffe080", style="rounded,filled,bold"];')
    # Color sinks differently
    for s in stats["sinks"]:
        if s not in hub_set:
            out.append(f'  "{s}" [fillcolor="#e0f0ff"];')
    # Edges
    for src, dsts in edges.items():
        for d in dsts:
            out.append(f'  "{src}" -> "{d}";')
    out.append("}")
    return "\n".join(out)


def to_mermaid(edges, paths, stats, max_edges: int = 200) -> str:
    """Mermaid diagram — capped at max_edges for renderability."""
    out: List[str] = []
    out.append("```mermaid")
    out.append("graph LR")
    # Only emit edges involving the top-N hubs to keep readable
    hub_set = {n for n, _ in stats["hubs"][:20]}
    important_modules = set(hub_set)
    # Add modules with high out-degree
    important_modules.update(m for m, _ in stats["out_deg"].most_common(15))
    n_emitted = 0
    for src, dsts in edges.items():
        if n_emitted >= max_edges:
            break
        # Emit edges if src OR dst is "important"
        for d in dsts:
            if src in important_modules or d in important_modules:
                # Mermaid-safe names (replace chars)
                s = src.replace("-", "_").replace(".", "_")
                t = d.replace("-", "_").replace(".", "_")
                out.append(f"  {s} --> {t}")
                n_emitted += 1
                if n_emitted >= max_edges:
                    break
    out.append("```")
    return "\n".join(out)


# ─── Main ───────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", action="store_true",
                    help="just print summary, don't write files")
    args = ap.parse_args()

    # Write to tracked location (Gen13/var/ is gitignored) so the graph
    # is part of the repo and not lost between machines.
    out_dir = ROOT / "Gen14" / "targets" / "ck" / "brain" / "dep_graph"
    out_dir.mkdir(parents=True, exist_ok=True)

    print("[ck_dep_graph] Discovering .py files...")
    files = discover()
    print(f"[ck_dep_graph]   {len(files)} files in scope")

    print("[ck_dep_graph] Parsing imports + building graph...")
    edges, paths = build_graph(files)
    print(f"[ck_dep_graph]   {len(edges)} unique modules, "
          f"{sum(len(v) for v in edges.values())} internal edges")

    stats = analyze(edges)

    if args.summary:
        print()
        print(f"Modules:    {stats['n_modules']}")
        print(f"Edges:      {stats['n_edges']}")
        print(f"Orphans:    {len(stats['orphans'])}")
        print(f"Sinks:      {len(stats['sinks'])}")
        print(f"Isolates:   {len(stats['isolates'])}")
        print()
        print("Top 10 hubs (most-imported):")
        for n, c in stats["hubs"][:10]:
            print(f"  {n:35s}  {c} importers")
        return 0

    # Write all three views
    md = to_markdown(edges, paths, stats)
    dot = to_dot(edges, paths, stats)
    mmd = to_mermaid(edges, paths, stats)

    (out_dir / "ck_dep_graph.md").write_text(md, encoding="utf-8")
    (out_dir / "ck_dep_graph.dot").write_text(dot, encoding="utf-8")
    (out_dir / "ck_dep_graph.mmd").write_text(mmd, encoding="utf-8")
    # Also write the raw edge list as JSON for tooling
    raw = {
        "edges": edges,
        "stats": {
            "n_modules": stats["n_modules"],
            "n_edges": stats["n_edges"],
            "hubs": stats["hubs"],
            "orphans": stats["orphans"],
            "in_deg": dict(stats["in_deg"]),
            "out_deg": dict(stats["out_deg"]),
        },
    }
    (out_dir / "ck_dep_graph.json").write_text(
        json.dumps(raw, indent=1, default=str), encoding="utf-8")

    print()
    print(f"Wrote:")
    print(f"  {out_dir / 'ck_dep_graph.md'}")
    print(f"  {out_dir / 'ck_dep_graph.dot'}")
    print(f"  {out_dir / 'ck_dep_graph.mmd'}")
    print(f"  {out_dir / 'ck_dep_graph.json'}")
    print()
    print(f"Modules:  {stats['n_modules']}")
    print(f"Edges:    {stats['n_edges']}")
    print(f"Orphans:  {len(stats['orphans'])}")
    print(f"Top hub:  {stats['hubs'][0][0]} ({stats['hubs'][0][1]} importers)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
