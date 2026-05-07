"""
Inject the foundations seed crystals into a running CK via /crystals/add.

Idempotent: duplicates (by first_word) are skipped. After running, CK's
runtime crystal store includes the foundations facts and CK will surface
them in chat responses.

Usage:
    # Standalone (CK on localhost:7777)
    python -m foundations.crystal_seed

    # Different CK URL
    python -m foundations.crystal_seed --url http://other-host:7777
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

SEED_FILE = Path(__file__).resolve().parent / "seed_crystals.json"
DEFAULT_CK_URL = "http://localhost:7777"


def inject(ck_url: str = DEFAULT_CK_URL, seed_file: Path = SEED_FILE
           ) -> dict[str, int]:
    """POST each crystal to {ck_url}/crystals/add. Returns counts dict."""
    if not seed_file.exists():
        raise FileNotFoundError(f"seed file not found: {seed_file}")
    data = json.loads(seed_file.read_text(encoding="utf-8"))
    crystals = data.get("crystals", [])

    added = duplicate = errors = 0
    for c in crystals:
        body = {
            "triggers": c["triggers"],
            "fact": c["fact"],
            "op_signature": c.get("op_signature"),
            "related": c.get("related"),
        }
        req = urllib.request.Request(
            f"{ck_url}/crystals/add",
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json"},
        )
        first_word = c["fact"].split(":", 1)[0].strip()
        try:
            res = json.loads(urllib.request.urlopen(req, timeout=10).read())
            if res.get("ok"):
                added += 1
                print(f"  + {first_word}")
            else:
                duplicate += 1
                print(f"  ~ {first_word}: {res.get('error')}")
        except urllib.error.HTTPError as e:
            if e.code == 409:
                duplicate += 1
                print(f"  ~ {first_word}: duplicate (already in store)")
            else:
                errors += 1
                print(f"  ! {first_word}: HTTP {e.code} -- {e.read().decode('utf-8', errors='replace')[:120]}")
        except Exception as e:
            errors += 1
            print(f"  ! {first_word}: {type(e).__name__}: {e}")

    return {"added": added, "duplicate": duplicate, "errors": errors,
            "total": len(crystals)}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--url", default=DEFAULT_CK_URL,
                   help=f"CK base URL (default: {DEFAULT_CK_URL})")
    args = p.parse_args(argv)

    print(f"Seeding foundation crystals into {args.url}...")
    print(f"Source: {SEED_FILE}")
    print()
    summary = inject(args.url)
    print()
    print(f"Result: {summary['added']} added, {summary['duplicate']} duplicate, "
          f"{summary['errors']} errors (of {summary['total']} total)")
    return 0 if summary["errors"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
