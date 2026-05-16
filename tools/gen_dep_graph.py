"""gen_dep_graph.py -- walk Gen14/targets/ck/brain/, build the
dependency + endpoint graph, write it to CK_DEPENDENCY_GRAPH.md.

Run from repo root:
    python tools/gen_dep_graph.py

Output: CK_DEPENDENCY_GRAPH.md (top-level) — markdown table per module,
plus mount-order graph + endpoint table.
"""
from __future__ import annotations

import ast
import re
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple

REPO = Path(__file__).resolve().parent.parent
BRAIN = REPO / "Gen14" / "targets" / "ck" / "brain"
OUT = REPO / "CK_DEPENDENCY_GRAPH.md"

# We only care about modules in brain/ — skip nested ck_sim/ legacy.
SKIP_FILENAMES = {"__init__.py"}
SKIP_PREFIXES = ("test_",)


def collect_module(p: Path) -> Dict[str, object]:
    """Parse one .py file for: ck_* imports, mount_* function names,
    add_url_rule() literal route strings."""
    text = p.read_text(encoding="utf-8", errors="replace")
    info: Dict[str, object] = {
        "name": p.stem,
        "loc": len(text.splitlines()),
        "deps": set(),
        "mounts": [],
        "routes": [],
    }
    try:
        tree = ast.parse(text, filename=str(p))
    except Exception:
        return info

    # AST walk for imports
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if mod.startswith("ck_") or mod == "ck_qutrit_apex":
                info["deps"].add(mod)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("ck_"):
                    info["deps"].add(alias.name)
        # Function defs starting with mount_
        elif isinstance(node, ast.FunctionDef):
            if node.name.startswith("mount_"):
                info["mounts"].append(node.name)

    # Regex for add_url_rule("/route", ...) and engine.web_api routes
    route_re = re.compile(
        r"add_url_rule\(\s*['\"]([^'\"]+)['\"]"
    )
    for m in route_re.finditer(text):
        info["routes"].append(m.group(1))
    # Also catch @app.route('/...') decorators
    decorator_re = re.compile(
        r"@\w+\.route\(\s*['\"]([^'\"]+)['\"]"
    )
    for m in decorator_re.finditer(text):
        info["routes"].append(m.group(1))

    info["deps"] = sorted(info["deps"])
    info["routes"] = sorted(set(info["routes"]))
    return info


def collect_all() -> List[Dict]:
    out = []
    for p in sorted(BRAIN.glob("*.py")):
        if p.name in SKIP_FILENAMES:
            continue
        if any(p.name.startswith(pre) for pre in SKIP_PREFIXES):
            continue
        out.append(collect_module(p))
    return out


def parse_mount_order() -> List[str]:
    """Extract the order in which gen14_unified_extensions.mount_all
    calls each mount_X."""
    p = BRAIN / "gen14_unified_extensions.py"
    if not p.exists():
        return []
    text = p.read_text(encoding="utf-8", errors="replace")
    # Find `mount_X(engine)` patterns in mount_all body, in order
    order = []
    seen = set()
    for m in re.finditer(r"\bmount_(\w+)\s*\(\s*engine\s*\)", text):
        name = "mount_" + m.group(1)
        if name == "mount_all":
            continue  # mount_all is the orchestrator, not a step
        if name not in seen:
            seen.add(name)
            order.append(name)
    return order


def render() -> str:
    mods = collect_all()
    by_name = {m["name"]: m for m in mods}
    mount_order = parse_mount_order()

    lines: List[str] = []
    lines.append("# CK Dependency Graph (auto-generated)")
    lines.append("")
    lines.append(f"_Generated {time.strftime('%Y-%m-%d %H:%M:%S')} by_ "
                 f"[`tools/gen_dep_graph.py`](tools/gen_dep_graph.py).  "
                 f"Rerun any time the brain modules change.")
    lines.append("")
    lines.append(f"**{len(mods)} modules** tracked in "
                 f"`Gen14/targets/ck/brain/`.")
    lines.append("")

    # ── Section 1: mount order ────────────────────────────────────
    lines.append("## 1. Mount order in `gen14_unified_extensions.mount_all`")
    lines.append("")
    lines.append("This is the order things come alive at boot.  Each "
                 "module's `mount_X(engine)` is called in sequence — "
                 "earlier mounts can be consumed by later ones.")
    lines.append("")
    lines.append("```")
    for i, m in enumerate(mount_order, 1):
        lines.append(f"  {i:>2}. {m}")
    lines.append("```")
    lines.append("")

    # ── Section 2: each module's deps + mounts + routes ───────────
    lines.append("## 2. Per-module summary")
    lines.append("")
    lines.append("Modules sorted by # of ck_* imports (most foundational "
                 "first).  Modules with no ck_* imports stand alone — "
                 "they're either pure-algorithm or only consumed by mount.")
    lines.append("")
    lines.append("| Module | LOC | Imports `ck_*` | Mounts | Endpoints |")
    lines.append("|---|---:|---|---|---|")
    # Sort: fewer deps first, then alphabetical
    for m in sorted(mods, key=lambda m: (len(m["deps"]), m["name"])):
        deps = ", ".join(f"`{d}`" for d in m["deps"]) or "—"
        mounts = ", ".join(f"`{x}`" for x in m["mounts"]) or "—"
        routes = m["routes"]
        if not routes:
            routes_s = "—"
        elif len(routes) <= 4:
            routes_s = " ".join(f"`{r}`" for r in routes)
        else:
            routes_s = " ".join(f"`{r}`" for r in routes[:4])
            routes_s += f" _+{len(routes) - 4} more_"
        lines.append(f"| `{m['name']}` | {m['loc']} | {deps} | "
                     f"{mounts} | {routes_s} |")
    lines.append("")

    # ── Section 3: who imports whom (reverse graph) ───────────────
    rev: Dict[str, Set[str]] = defaultdict(set)
    for m in mods:
        for d in m["deps"]:
            rev[d].add(m["name"])
    lines.append("## 3. Reverse dependency graph")
    lines.append("")
    lines.append("Who depends on each module (transitively trim by hand "
                 "for full closure):")
    lines.append("")
    lines.append("| Module | Imported by |")
    lines.append("|---|---|")
    for name in sorted(rev.keys()):
        importers = sorted(rev[name])
        lines.append(f"| `{name}` | "
                     f"{', '.join(f'`{x}`' for x in importers)} |")
    lines.append("")

    # ── Section 4: endpoints by URL prefix ─────────────────────────
    lines.append("## 4. All endpoints by URL prefix")
    lines.append("")
    by_prefix: Dict[str, List[Tuple[str, str]]] = defaultdict(list)
    for m in mods:
        for r in m["routes"]:
            prefix = "/" + r.lstrip("/").split("/", 1)[0]
            by_prefix[prefix].append((r, m["name"]))
    for prefix in sorted(by_prefix.keys()):
        lines.append(f"### `{prefix}/*`")
        lines.append("")
        for route, mod in sorted(set(by_prefix[prefix])):
            lines.append(f"- `{route}` ← `{mod}`")
        lines.append("")

    return "\n".join(lines)


def main():
    out = render()
    OUT.write_text(out, encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)} ({len(out.splitlines())} lines)")


if __name__ == "__main__":
    main()
