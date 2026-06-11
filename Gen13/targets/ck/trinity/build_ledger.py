"""build_ledger.py -- regenerate CK's LEARNING_LEDGER.md from the
measured artifacts. Run any time; it reflects his current state.

  python build_ledger.py
"""
import glob
import io
import json
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))


def jload(p):
    try:
        return json.load(io.open(p, encoding="utf-8"))
    except Exception:
        return None


def main():
    lines = ["# CK LEARNING LEDGER (auto-generated)",
             f"_regenerated {time.strftime('%Y-%m-%d %H:%M')}_", ""]

    # study journal stats
    jp = os.path.join(HERE, "study_journal.jsonl")
    if os.path.exists(jp):
        rows = [json.loads(l) for l in io.open(jp, encoding="utf-8")]
        fic = sum(1 for r in rows if r["verdict"] == "FICTION")
        chars = sum(r["chars"] for r in rows)
        lines += [f"## Reading",
                  f"- books read & judged: **{len(rows)}** "
                  f"({chars/1e6:.0f}M chars) -> {fic} fiction / "
                  f"{len(rows)-fic} fact",
                  f"- latest: " + "; ".join(
                      r['title'][:36] for r in rows[-3:]), ""]

    # organ results
    lines += ["## Organ measurements (latest)"]
    for p in sorted(glob.glob(os.path.join(HERE, "*_result.json")) +
                    glob.glob(os.path.join(HERE, "..", "extraction",
                                           "*_result.json"))):
        d = jload(p)
        if d is None:
            continue
        name = os.path.basename(p).replace("_result.json", "")
        flat = []
        def walk(prefix, v):
            if isinstance(v, dict):
                for k, vv in list(v.items())[:6]:
                    walk(f"{prefix}{k}.", vv)
            elif isinstance(v, (int, float)) and not isinstance(v, bool):
                flat.append(f"{prefix[:-1]}={v:.3g}")
        walk("", d)
        lines.append(f"- **{name}**: " + ", ".join(flat[:8]))
    lines += ["",
              "## Provenance",
              "- arc narrative: `../THE_EDUCATION_OF_CK.md`",
              "- architecture + registry: `CK_TRINITY.md`",
              "- every number above regenerates from the script of the "
              "same name in this folder.", ""]
    out = os.path.join(HERE, "LEARNING_LEDGER.md")
    io.open(out, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print(f"ledger written: {out} ({len(lines)} lines)")


if __name__ == "__main__":
    main()
