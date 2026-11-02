#!/usr/bin/env python3
"""Klipy storytime (bez lektora, bez ceny na ekranie) – 3 formaty storytellingu ze screenów:
historia  = Problem z życia (POV), test = Zaskakujące odkrycie, blad = Błędny sposób (kontrast).
Użycie: python3 storytime.py [historia test blad]
"""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from montaz import text_png, run, dur, W, H, CROP_TOP, ROOT, TMP, OUT

# scena: (wideo, start w źródle, długość, [(od, do|None, tekst)], hook?)
CLIPS = {
    "historia": [  # bohater -> problem -> napięcie -> odkrycie -> rozwiązanie -> efekt
        ("h3", 0.0, 2.8, [(0, None, "POV: wsiadasz do auta\nprosto po siłce")], True),
        ("h1", 0.3, 2.6, [(0, None, "a rano fotel\ndalej mokry")], False),
        ("n1", 1.2, 3.0, [(0, None, "ręcznik z łazienki?\nzjeżdża przy każdym ruchu")], False),
        ("n2", 2.0, 2.8, [(0, None, "a pot i tak\nprzechodzi na fotel")], False),
        ("b1", 0.0, 3.0, [(0, None, "aż w końcu: ręcznik\nz kapturem na zagłówek")], False),
        ("b2", 0.0, 2.4, [(0, None, "góra wciąga pot")], False),
        ("b3", 0.3, 3.2, [(0, 1.4, "a pod spodem?"), (1.4, None, "sucho.")], False),
        ("b5", 0.0, 2.6, [(0, None, "nazywa się Suchy Fotel\nlink w bio")], False),
    ],
    "test": [  # ciekawość -> zaskoczenie -> identyfikacja
        ("h2", 0.0, 2.8, [(0, None, "wylewam wodę\nna fotel w aucie.\nspecjalnie.")], True),
        ("b2", 0.0, 2.4, [(0, None, "frotte wciąga wszystko")], False),
        ("b3", 0.3, 3.2, [(0, 1.4, "podnoszę róg…"), (1.4, None, "fotel suchy.")], False),
        ("h1", 0.3, 2.8, [(0, None, "po co? bo tak wygląda\nfotel po każdym treningu")], False),
        ("b1", 0.0, 2.6, [(0, None, "kaptur na zagłówek,\nnic nie zjeżdża")], False),
        ("b4", 0.0, 2.8, [(0, 1.4, "a potem do torby"), (1.4, None, "Suchy Fotel\nlink w bio")], False),
    ],
    "blad": [  # błędny sposób -> alternatywa (kontrast)
        ("n1", 1.2, 3.0, [(0, None, "tak większość chroni\nfotel po siłce:")], True),
        ("n2", 2.0, 2.8, [(0, None, "efekt?\ni tak mokro")], False),
        ("b1", 0.0, 2.8, [(0, None, "sposób, który\nnie zjeżdża:")], False),
        ("b2", 0.0, 2.4, [(0, None, "góra chłonie\npot i wodę")], False),
        ("b3", 0.3, 3.2, [(0, 1.4, "spód nie przepuszcza"), (1.4, None, "fotel suchy.")], False),
        ("b4", 0.0, 2.4, [(0, None, "200 g, mieści się\nw torbie na siłkę")], False),
        ("b5", 0.0, 2.4, [(0, None, "Suchy Fotel\nlink w bio")], False),
    ],
}
CAP_Y = {"b1": 1250, "b5": 330}


def scene(clip, i, name, ss, d, texts, hook):
    v = os.path.join(ROOT, "wideo", name + ".mp4")
    ct = CROP_TOP.get(name, 0)
    pre = f"crop=iw:ih*{1-ct:.3f}:0:ih*{ct:.3f}," if ct else ""
    inputs = ["-ss", f"{ss}", "-t", f"{d}", "-i", v, "-f", "lavfi", "-t", f"{d}", "-i", "anullsrc=r=44100:cl=stereo"]
    filt = [f"[0:v]{pre}scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,setpts=PTS-STARTPTS[v0]"]
    last, n = "v0", 2
    y = CAP_Y.get(name, 300)
    for j, (a, b, t) in enumerate(texts):
        p = os.path.join(TMP, f"st_{clip}_{i}_{j}.png")
        text_png(t, p, 92 if hook else 74)
        inputs += ["-i", p]
        b = d if b is None else b
        filt.append(f"[{last}][{n}:v]overlay=0:{y}:enable='between(t,{a},{b})'[v{n}]")
        last, n = f"v{n}", n + 1
    out = os.path.join(TMP, f"st_{clip}_{i:02d}.mp4")
    run(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", f"[{last}]", "-map", "1:a",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "44100", out])
    return out


if __name__ == "__main__":
    for clip in sys.argv[1:] or list(CLIPS):
        parts = [scene(clip, i, *s) for i, s in enumerate(CLIPS[clip])]
        lst = os.path.join(TMP, f"st_{clip}.txt")
        open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
        out = os.path.join(OUT, f"storytime_{clip}.mp4")
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out])
        print(out, round(dur(out), 1), "s")
