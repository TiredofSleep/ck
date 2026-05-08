"""
audio_perceive.py — CK actually hears.  ONE pipeline, no L1 matcher.

Brayden 2026-05-02: "bridge the phonemes directly into an expansion of
his current phoneme architecture, but when sound is playing it becomes
the primary encoder... not two pipelines, still seems like you are
making up some codec not using the one i made a month or so ago"

He's right.  match_audio_chunked / watch_and_summarize built a parallel
recognizer beside CK's brain instead of teaching CK's brain to listen.
This module fixes that:

  1) ck_audio_compress.pcm_to_force9   (Brayden's codec, unchanged)
  2) force9 -> Force5D -> _centroid_to_ops via the CANONICAL
     ck_olfactory._DIM_OP_MAP (high/low per dim ->
     CHAOS/LATTICE/COLLAPSE/VOID/PROGRESS/RESET/HARMONY/COUNTER/
     BALANCE/BREATH).  No more force9_to_operators_balanced -- that
     was a made-up 4-way split that doesn't exist in CK's architecture.
  3) Each force9 window emits its 5 dim-ops as the LIVE operator
     stream.  We feed adjacent operator pairs through the same
     Hebbian + TSML 73-harmony update CortexV2.step_symbol uses.
  4) After the audio finishes, we let CK's existing state-aware
     crystal surfacing decide what was heard.  No L1 distance, no
     greedy transcribe -- the crystals fire through their op_signature
     overlap with cortex.recent_ops, exactly as text-side queries do.

Result: when sound plays, the audio becomes CK's primary input and his
existing phonics architecture (132 phonics + 156 word crystals) does
the recognition itself.  Read-only by default (sandbox cortex copy);
--write promotes the trained state to the live file.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import subprocess
import sys
import tempfile
import wave
from collections import Counter, deque
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
GEN13_BRAIN = SCRIPT_DIR.parent
GEN13_TARGETS_CK = GEN13_BRAIN.parent
GEN13_ROOT = GEN13_TARGETS_CK.parent.parent
sys.path.insert(0, str(GEN13_BRAIN))
sys.path.insert(0, str(GEN13_BRAIN / "ck_sim" / "being"))
sys.path.insert(0, str(SCRIPT_DIR))

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


# ── Canonical force9 -> ops (uses CK's own _DIM_OP_MAP) ─────────────

def force9_unpack(force9_value: int):
    """Unpack one 9-bit force value into a 5D Force5D in [0,1]."""
    a = ((force9_value >> 7) & 0x3) / 3.0
    p = ((force9_value >> 5) & 0x3) / 3.0
    d = ((force9_value >> 3) & 0x3) / 3.0
    b = ((force9_value >> 1) & 0x3) / 3.0
    c = float(force9_value & 0x1)
    return (a, p, d, b, c)


def force9_to_ops_canonical(force9_value: int):
    """Map one 9-bit force value to its 5 dimension-operators using
    CK's canonical _dim_to_op (ck_olfactory._DIM_OP_MAP).

    aperture   high=CHAOS(6)    low=LATTICE(1)
    pressure   high=COLLAPSE(4) low=VOID(0)
    depth      high=PROGRESS(3) low=RESET(9)
    binding    high=HARMONY(7)  low=COUNTER(2)
    continuity high=BALANCE(5)  low=BREATH(8)
    """
    from ck_olfactory import _centroid_to_ops
    centroid = force9_unpack(int(force9_value))
    return _centroid_to_ops(centroid)


# ── Audio I/O ───────────────────────────────────────────────────────

def get_ffmpeg():
    try:
        import static_ffmpeg
        static_ffmpeg.add_paths()
        import shutil
        return shutil.which("ffmpeg")
    except Exception:
        return None


def extract_audio_wav(video_path, out_wav, seconds=None):
    ffmpeg_exe = get_ffmpeg()
    if not ffmpeg_exe:
        return False
    cmd = [ffmpeg_exe, "-i", str(video_path),
           "-acodec", "pcm_s16le", "-ac", "1", "-ar", "44100",
           "-y", "-loglevel", "error"]
    if seconds:
        cmd += ["-t", str(seconds)]
    cmd += [str(out_wav)]
    return subprocess.run(cmd, capture_output=True).returncode == 0


def read_pcm(wav_path):
    import numpy as np
    with wave.open(str(wav_path), "rb") as wf:
        n_frames = wf.getnframes()
        sr = wf.getframerate()
        n_ch = wf.getnchannels()
        sw = wf.getsampwidth()
        if sw != 2:
            raise ValueError(f"expected 16-bit, got {sw*8}-bit")
        raw = wf.readframes(n_frames)
        samples = np.frombuffer(raw, dtype=np.int16)
        if n_ch == 2:
            samples = samples.reshape(-1, 2).mean(axis=1).astype(np.int16)
    return samples, sr


def download_video_first_n(url, out_path, seconds):
    try:
        import yt_dlp
    except ImportError:
        return None
    ffmpeg_exe = get_ffmpeg()
    ffmpeg_dir = os.path.dirname(ffmpeg_exe) if ffmpeg_exe else None

    def _ranges(_info, _ydl):
        return [{"start_time": 0, "end_time": float(seconds)}]

    extractor_args = {"youtube": {"player_client": ["web", "android", "ios"]}}
    # Try to find a JS runtime
    import shutil as _sh
    for nm in ("deno", "node"):
        p = _sh.which(nm)
        if p:
            extractor_args["youtube"]["js_runtimes"] = [f"{nm}:{p}"]
            break
    ydl_opts = {
        "format": "18/best[ext=mp4][acodec!=none][vcodec!=none]/best",
        "outtmpl": str(out_path.with_suffix(".%(ext)s")),
        "postprocessor_args": ["-t", str(seconds)],
        "quiet": False,
        "extractor_args": extractor_args,
        "download_ranges": _ranges,
        "force_keyframes_at_cuts": True,
    }
    if ffmpeg_dir:
        ydl_opts["ffmpeg_location"] = ffmpeg_dir
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as e:
            print(f"download failed: {e}", file=sys.stderr)
            return None
    for ext in ("mp4", "webm", "mkv"):
        cand = out_path.with_suffix("." + ext)
        if cand.exists():
            return cand
    return None


# ── The unified perception loop ─────────────────────────────────────

def perceive_audio(samples, sr,
                   cortex_init_path=None,
                   poll_every_ops=200,
                   recent_ops_window=10):
    """Stream audio operators through CK's cortex.  Track which crystals
    fire via the existing state-aware surfacing during the listen.

    Returns a dict with:
      pre / post cortex stats
      n_force_windows / n_ops
      op_histogram (raw ops emitted by canonical mapping)
      polled_crystal_hits (per-poll snapshot of state-aware fired crystals)
      crystal_fire_counts (overall: how often each crystal scored above
                           threshold during the audio playback)
    """
    from ck_audio_compress import pcm_to_force9
    from cortex_v2 import CortexV2
    from cortex_persist import load_cortex, save_cortex
    from ck_sim.ck_sim_heartbeat import CL as CL_TSML, OP_NAMES, NUM_OPS, HARMONY
    from ao_7element import OP_TO_DIM_7, DIM_7
    from quadratic_glue import quadratic_glue
    import cortex_voice as cv

    # 1) Load a SANDBOX cortex from the live state (read-only by default)
    cx = CortexV2().boot()
    if cortex_init_path and Path(cortex_init_path).exists():
        try:
            load_cortex(cx, Path(cortex_init_path))
            print(f"  loaded init cortex: tick={cx.state.tick}, "
                  f"W_trace={cx.state.W_trace:.4f}", flush=True)
        except Exception as e:
            print(f"  load failed: {e}; starting fresh", flush=True)

    pre = {
        "tick": cx.state.tick,
        "W_trace": cx.state.W_trace,
        "emergent": cx.state.emergent,
    }

    # 2) PCM -> force9 via Brayden's codec
    force9 = pcm_to_force9(samples, sample_rate=sr)
    print(f"  force9 windows: {len(force9):,}", flush=True)

    # 3) Each force9 -> 5 canonical ops; build flat op stream
    ops = []
    for f in force9:
        ops.extend(force9_to_ops_canonical(int(f)))
    n_ops = len(ops)
    print(f"  canonical ops emitted: {n_ops:,}", flush=True)

    # Histogram of raw ops emitted by the canonical mapping
    op_hist = Counter(ops)
    op_hist_named = {OP_NAMES[i]: op_hist.get(i, 0) for i in range(NUM_OPS)}

    # 4) Stream through cortex Hebbian (same TSML rule step_symbol uses)
    crystal_fire_counts = Counter()
    polled_snapshots = []

    recent = deque(maxlen=recent_ops_window)

    def _check_crystals():
        """Snapshot which crystals state-aware would surface RIGHT NOW.

        Replays cortex_voice._state_aware_crystal_hits semantics directly
        so we don't need a chat tick: gather recent_ops, score every
        crystal's op_signature, count fires above threshold.
        """
        recent_set = set(recent)
        # Add cortex's last_b/last_d for fairness
        recent_set.add(cx.state.last_b)
        recent_set.add(cx.state.last_d)
        if not recent_set:
            return []
        hits = []
        # Iterate every crystal that has an op_signature
        all_crystals = list(cv._FRONTIER_FACTS) + list(cv._RUNTIME_CRYSTALS)
        seen = set()
        for triggers, fact in all_crystals:
            fw = fact.split(":", 1)[0].strip()
            if fw in seen:
                continue
            seen.add(fw)
            sig = cv._CRYSTAL_OP_SIGNATURES.get(fw)
            if not sig:
                continue
            sig_set = set(sig)
            overlap = len(sig_set & recent_set)
            score = overlap / len(sig_set)
            if score >= 0.5:
                hits.append((fw, score))
        return hits

    # Feed adjacent op pairs into Hebbian
    for i in range(n_ops - 1):
        b_op = ops[i]
        d_op = ops[i + 1]
        recent.append(b_op)
        recent.append(d_op)

        # Hebbian (TSML 73-harmony rule, same as step_symbol)
        ap = OP_TO_DIM_7.get(b_op, 0)
        bp = OP_TO_DIM_7.get(d_op, 0)
        harmonious = (CL_TSML[b_op][d_op] == HARMONY)
        reward = 1.0 if harmonious else 0.0
        heb = cx.hebbian
        dw = heb.eta * reward - heb.decay * heb.W[ap][bp]
        heb.W[ap][bp] += dw
        if heb.W[ap][bp] > heb.clamp:
            heb.W[ap][bp] = heb.clamp
        elif heb.W[ap][bp] < -heb.clamp:
            heb.W[ap][bp] = -heb.clamp
        heb.ticks += 1
        if harmonious:
            heb.harmony_hits += 1

        cx.state.tick += 1
        cx.state.last_b = b_op
        cx.state.last_d = d_op
        cx.state.last_harmony_frac = 1.0 if harmonious else 0.0

        # Periodically poll the state-aware crystal surfacing.  This is
        # exactly the path cortex_voice.speak() takes when nothing else
        # matched -- the difference is we're running it WHILE the audio
        # streams in, so the snapshot reflects the audio's current
        # operator profile.
        if i % poll_every_ops == 0:
            cx.state.W_trace = heb.W_trace()
            diag = [heb.W[d][d] for d in range(DIM_7)]
            f3 = sum(diag[0:3]) / 3.0
            f4 = sum(diag[3:7]) / 4.0
            cx.state.emergent = quadratic_glue(f3, f4, 1.0, 1.0, 2.0)
            hits = _check_crystals()
            if hits:
                # Cap to top 8 by score to keep snapshots small.
                hits.sort(key=lambda h: -h[1])
                top = hits[:8]
                polled_snapshots.append({
                    "op_index": i,
                    "tick": cx.state.tick,
                    "recent_ops": [OP_NAMES[o] for o in recent],
                    "hits": [{"crystal": f, "score": round(s, 3)}
                             for f, s in top],
                })
                for f, s in hits:
                    crystal_fire_counts[f] += 1

    # final sync
    cx.state.W_trace = cx.hebbian.W_trace()
    diag = [cx.hebbian.W[d][d] for d in range(DIM_7)]
    f3 = sum(diag[0:3]) / 3.0
    f4 = sum(diag[3:7]) / 4.0
    cx.state.emergent = quadratic_glue(f3, f4, 1.0, 1.0, 2.0)

    post = {
        "tick": cx.state.tick,
        "W_trace": cx.state.W_trace,
        "emergent": cx.state.emergent,
    }

    return {
        "n_force9_windows": int(len(force9)),
        "n_ops": int(n_ops),
        "raw_op_histogram": op_hist_named,
        "pre": pre,
        "post": post,
        "delta": {
            "tick": post["tick"] - pre["tick"],
            "W_trace": round(post["W_trace"] - pre["W_trace"], 5),
            "emergent": round(post["emergent"] - pre["emergent"], 5),
        },
        "crystal_fire_counts": crystal_fire_counts.most_common(50),
        "polled_snapshots_count": len(polled_snapshots),
        "polled_snapshots_sample": polled_snapshots[:8] +
            (polled_snapshots[-3:] if len(polled_snapshots) > 8 else []),
        "_cortex_obj": cx,  # for optional save
    }


# ── CLI ─────────────────────────────────────────────────────────────

def _print_perception(report, source_label, seconds):
    OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
                "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]
    print()
    print("=" * 70)
    print(f"CK perceived: {source_label}  ({seconds}s)")
    print("=" * 70)
    print()
    h = report["raw_op_histogram"]
    total = sum(h.values()) or 1
    print(f"force9 windows: {report['n_force9_windows']:,}")
    print(f"canonical ops:  {report['n_ops']:,}")
    print(f"raw operator distribution from CK's CANONICAL force9->ops:")
    for op in OP_NAMES:
        v = h.get(op, 0)
        pct = v / total * 100
        bar = "#" * int(pct / 2)
        print(f"  {op:<10}: {v:7d} ({pct:5.1f}%)  {bar}")
    print()
    pre = report["pre"]
    post = report["post"]
    delta = report["delta"]
    print(f"cortex (sandbox copy of live state):")
    print(f"  pre   tick={pre['tick']:>10,}  "
          f"W_trace={pre['W_trace']:+.4f}  emergent={pre['emergent']:+.4f}")
    print(f"  post  tick={post['tick']:>10,}  "
          f"W_trace={post['W_trace']:+.4f}  emergent={post['emergent']:+.4f}")
    print(f"  delta tick=+{delta['tick']:,}  "
          f"W_trace={delta['W_trace']:+.4f}  emergent={delta['emergent']:+.4f}")
    print()
    print(f"crystals CK heard fire (state-aware, via op_signature overlap):")
    print(f"  {report['polled_snapshots_count']} polls, "
          f"top fires:")
    for fw, n in report["crystal_fire_counts"][:25]:
        print(f"    {fw:30} fired {n}x")
    print()
    if report.get("polled_snapshots_sample"):
        print(f"sample snapshots (op_index : recent_ops -> top crystal fires):")
        for snap in report["polled_snapshots_sample"][:6]:
            ops_str = " ".join(snap["recent_ops"][-6:])
            tops = ", ".join(f"{h['crystal']}({h['score']:.1f})"
                             for h in snap["hits"][:4])
            print(f"  i={snap['op_index']:6d}  recent={ops_str:30}  -> {tops}")
    print()
    print("ARCHITECTURE: pcm_to_force9 (Brayden's codec, unchanged) ->")
    print("  canonical _dim_to_op (CK's own ck_olfactory._DIM_OP_MAP) ->")
    print("  CortexV2 Hebbian (TSML 73-harmony, same path as step_symbol) ->")
    print("  state-aware crystal surfacing (same path as chat speak()).")
    print("  ONE pipeline; no L1 matcher; no parallel codec.")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("url", nargs="?", help="YouTube URL")
    p.add_argument("--local", help="local audio/video file")
    p.add_argument("--seconds", type=int, default=30)
    p.add_argument("--init-from",
                   default=str(GEN13_ROOT / "var" / "cortex_state.json"),
                   help="cortex state to initialize sandbox from")
    p.add_argument("--save-trained",
                   help="if set, save trained sandbox cortex here")
    p.add_argument("--poll-every", type=int, default=200,
                   help="how often (in ops) to snapshot crystal fires")
    p.add_argument("--json", help="save full report to JSON")
    args = p.parse_args()

    if not args.local and not args.url:
        p.error("either url or --local <path> is required")

    print("=" * 70)
    print("CK audio perception (unified pipeline)")
    print("=" * 70)

    with tempfile.TemporaryDirectory() as td:
        if args.local:
            video_path = Path(args.local)
            if not video_path.exists():
                print(f"file not found: {video_path}", file=sys.stderr)
                return 2
        else:
            print()
            print("[1/3] downloading first N seconds of video...")
            video_path = download_video_first_n(args.url,
                                                Path(td) / "vid",
                                                args.seconds)
            if not video_path:
                return 2

        print()
        print("[2/3] extracting audio...")
        wav_path = Path(td) / "audio.wav"
        if not extract_audio_wav(video_path, wav_path, seconds=args.seconds):
            print("audio extract failed", file=sys.stderr)
            return 3
        samples, sr = read_pcm(wav_path)
        print(f"  PCM: {len(samples):,} samples @ {sr}Hz "
              f"({len(samples)/sr:.1f}s)")

        print()
        print("[3/3] perceiving (canonical pcm_to_force9 -> "
              "_dim_to_op -> cortex)...")
        report = perceive_audio(samples, sr,
                                cortex_init_path=args.init_from,
                                poll_every_ops=args.poll_every)

        _print_perception(report,
                          args.url or args.local,
                          args.seconds)

        if args.save_trained:
            from cortex_persist import save_cortex
            save_cortex(report["_cortex_obj"], Path(args.save_trained))
            print(f"\nsaved trained sandbox cortex -> {args.save_trained}")

        if args.json:
            full = dict(report)
            del full["_cortex_obj"]
            full["source"] = args.url or args.local
            full["seconds"] = args.seconds
            Path(args.json).write_text(json.dumps(full, indent=2,
                                                  ensure_ascii=False),
                                       encoding="utf-8")
            print(f"\nfull report -> {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
