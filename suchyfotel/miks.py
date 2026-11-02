#!/usr/bin/env python3
"""Miks końcowy: lektor (EQ, kompresja, lekki pogłos) + własna muzyka z duckingiem.
Wejście: gotowe/<klip>.mp4, wyjście: gotowe/final/<klip>.mp4. Użycie: python3 miks.py
"""
import os, random, subprocess
ROOT = os.path.dirname(os.path.abspath(__file__))
G = os.path.join(ROOT, "gotowe"); F = os.path.join(G, "final"); os.makedirs(F, exist_ok=True)
MUZ = {
    "chill": ["historia_lektor", "test_lektor", "blad_lektor", "odp_zjezdza", "odp_pasuje", "lista",
              "storytime_historia", "storytime_test", "storytime_blad"],
    "ciepla": ["pies", "basen", "prezent", "zestaw", "suchyfotel_hook1"],
    "spokojna": ["zapach", "suchyfotel_hook2", "suchyfotel_hook3"],
}
random.seed(3)

def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout)

for track, clips in MUZ.items():
    m = os.path.join(ROOT, "muzyka", track + ".wav")
    for c in clips:
        src = os.path.join(G, c + ".mp4"); d = dur(src); off = random.uniform(1.5, 40 - d - 1.5) if d < 37 else 0
        fo = max(d - 1.0, 0)
        if c.startswith("storytime"):  # bez lektora: sama muzyka, głośniej
            af = (f"[1:a]atrim={off:.2f}:{off + d:.2f},asetpts=PTS-STARTPTS,afade=t=in:d=0.3,"
                  f"afade=t=out:st={fo:.2f}:d=1,loudnorm=I=-15:TP=-1.5[a]")
        else:
            af = ("[0:a]highpass=f=85,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.2:g=2.5,"
                  "acompressor=threshold=0.1:ratio=3:attack=8:release=120:makeup=1.5,"
                  "aecho=0.9:0.88:28|47:0.10|0.06,asplit=2[vo][sc];"
                  f"[1:a]atrim={off:.2f}:{off + d:.2f},asetpts=PTS-STARTPTS,volume=0.22,"
                  f"afade=t=in:d=0.3,afade=t=out:st={fo:.2f}:d=1[mu];"
                  "[mu][sc]sidechaincompress=threshold=0.02:ratio=5:attack=15:release=350:makeup=1[duck];"
                  "[vo][duck]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1:LRA=9[a]")
        out = os.path.join(F, c + ".mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-i", m, "-filter_complex", af,
                        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
                        "-shortest", out], check=True)
        print(c, track, round(dur(out), 1))
