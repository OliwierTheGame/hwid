#!/usr/bin/env python3
"""Klipy na tydzień – storytelling z lektorem (ton opowieści, 2. osoba, bez ceny w obrazie).
Każda scena: (wideo, start w źródle, tekst lektora, nagłówek na ekranie lub None).
Audio sceny: audio/t_<klip>_<nr>.mp3. Użycie: python3 tydzien.py [klip ...]
"""
import json, os, sys, textwrap
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import montaz
from montaz import text_png, run, dur, words, W, H, CROP_TOP, ROOT, TMP, OUT

TEMPO = 1.15
CAP_Y = {"b1": 1250, "p15": 1250, "p11": 1300}
# napisy innym zapisem niż lektor (liczby cyframi); "|" = granice grup
# maks. długość czystego fragmentu źródła (dalej wideo się psuje) – dłuższa scena = zwolnienie
MAXSRC = {"p11": 2.4}
CAP_TEXT = {
    ("basen", 4): "Waży 200 g,|zmieścisz w torbie.|Link w bio.",
    ("odp_pasuje", 1): "Ma 142 × 52 cm|i pasuje na|większość foteli.",
    ("odp_pasuje", 2): "Jeden rozmiar,|200 g.",
    ("lista", 0): "3 sytuacje,|kiedy fotel|robi się mokry.|1: po siłowni.",
    ("lista", 1): "2: mokry pies|po spacerze.",
    ("lista", 2): "3: basen.",
}
CLIPS = {
    "historia_lektor": [
        ("h3", 0.0, "Wsiadasz do auta prosto po siłowni.", "POV: prosto po siłce"),
        ("h1", 0.3, "A rano fotel dalej mokry.", None),
        ("n1", 1.2, "Zwykły ręcznik z łazienki? Zjeżdża przy każdym ruchu.", None),
        ("n2", 2.0, "A pot i tak przechodzi na tapicerkę.", None),
        ("b1", 0.0, "Ten ma kaptur na zagłówek. Nic nie zjeżdża.", None),
        ("b2", 0.0, "Góra wciąga pot.", None),
        ("b3", 0.3, "A pod spodem? Sucho.", None),
        ("b5", 0.0, "Nazywa się Suchy Fotel. Link w bio.", None),
    ],
    "test_lektor": [
        ("h2", 0.0, "Wylewam wodę na fotel w samochodzie. Specjalnie.", "WODA NA FOTEL?"),
        ("b2", 0.0, "Materiał wciąga całą wodę.", None),
        ("b3", 0.3, "Podnoszę róg… i fotel suchy.", None),
        ("h1", 0.3, "Po co? Bo tak wygląda fotel po każdym treningu.", None),
        ("b1", 0.0, "Kaptur na zagłówek i nic nie zjeżdża.", None),
        ("b4", 0.0, "Potem zwijasz do torby. Link w bio.", None),
    ],
    "blad_lektor": [
        ("n1", 1.2, "Tak większość chroni fotel po siłowni.", "BŁĄD, KTÓRY ROBI WIĘKSZOŚĆ"),
        ("n2", 2.0, "Efekt? I tak mokro.", None),
        ("b1", 0.0, "Ten ma kaptur na zagłówek, więc nie zjeżdża.", None),
        ("b2", 0.0, "Góra chłonie pot i wodę.", None),
        ("b3", 0.3, "A spód nie przepuszcza. Fotel suchy.", None),
        ("b5", 0.0, "Nazywa się Suchy Fotel. Link w bio.", None),
    ],
    "pies": [
        ("p11", 0.8, "Mokry pies po spacerze. Wiesz, co będzie z fotelem.", "MOKRY PIES + FOTEL"),
        ("b1", 0.0, "Dlatego przed spacerem zakładasz to. Kaptur na zagłówek i gotowe.", None),
        ("p12", 0.0, "Pies może się otrzepać, ile chce.", None),
        ("b3", 0.3, "A fotel pod spodem zostaje suchy.", None),
        ("b4", 0.0, "Potem zwijasz, pierzesz i od nowa. Link w bio.", None),
    ],
    "basen": [
        ("p13", 0.0, "Mokra torba z basenu prosto na fotel?", "PO BASENIE"),
        ("b2", 0.0, "Frotte zbiera całą wodę.", None),
        ("b3", 0.3, "Spód jest wodoodporny, więc tapicerka zostaje sucha.", None),
        ("b1", 0.0, "Zakładasz w kilka sekund.", None),
        ("b4", 0.0, "Waży dwieście gramów, zmieścisz w torbie. Link w bio.", None),
    ],
    "prezent": [
        ("p14", 0.0, "Szukasz prezentu dla kogoś, kto chodzi na siłownię?", "POMYSŁ NA PREZENT"),
        ("h1", 0.3, "Każdy, kto trenuje, zna ten widok.", None),
        ("b1", 0.0, "Ręcznik na fotel z kapturem na zagłówek.", None),
        ("b3", 0.3, "Spód nie przepuszcza wody, fotel zostaje suchy.", None),
        ("p14", 2.5, "Prezent, który naprawdę się przyda. Link w bio.", None),
    ],
    "zestaw": [
        ("h1", 0.3, "Trenujecie we dwoje? To mokre są dwa fotele, nie jeden.", "TRENUJECIE WE DWOJE?"),
        ("p15", 0.0, "Dlatego najlepiej na oba przednie fotele.", None),
        ("b1", 0.0, "Kaptur na zagłówek, nic nie zjeżdża.", None),
        ("b3", 0.3, "A fotel pod spodem zostaje suchy.", None),
        ("p15", 2.5, "Przy dwóch sztukach dostawa gratis. Link w bio.", None),
    ],
    "odp_zjezdza": [
        ("n1", 1.2, "Pewnie myślisz: a czy on nie zjeżdża, jak zwykły ręcznik?", "„A NIE ZJEŻDŻA?”"),
        ("b1", 0.0, "Nie, bo ma kaptur, który zakładasz na zagłówek.", None),
        ("b5", 0.0, "Siadasz, wiercisz się, a on dalej na miejscu.", None),
        ("b3", 0.3, "A spód nie przepuszcza wody. Link w bio.", None),
    ],
    "odp_pasuje": [
        ("b1", 0.0, "Pewnie się zastanawiasz, czy pasuje do twojego auta.", "„PASUJE DO MOJEGO AUTA?”"),
        ("p15", 0.0, "Ma sto czterdzieści dwa na pięćdziesiąt dwa centymetry i pasuje na większość foteli.", None),
        ("b4", 0.0, "Jeden rozmiar, dwieście gramów.", None),
        ("b5", 0.0, "Kaptur trzyma go na zagłówku. Link w bio.", None),
    ],
    "lista": [
        ("h3", 0.0, "Trzy sytuacje, kiedy fotel w samochodzie robi się mokry. Jeden: po siłowni.", "FOTEL ZNOWU MOKRY?"),
        ("p11", 0.8, "Dwa: mokry pies po spacerze.", None),
        ("p13", 0.0, "Trzy: basen.", None),
        ("b3", 0.3, "Z tym fotel za każdym razem zostaje suchy.", None),
        ("b5", 0.0, "Nazywa się Suchy Fotel. Link w bio.", None),
    ],
    "zapach": [
        ("h1", 0.3, "Wiesz, skąd ten zapach w samochodzie po treningach?", "SKĄD TEN ZAPACH?"),
        ("n2", 2.0, "Pot wsiąka w tapicerkę i piankę fotela.", None),
        ("b1", 0.0, "Zamiast tego może wsiąkać tutaj.", None),
        ("b2", 0.0, "Frotte zbiera wilgoć, a ręcznik po prostu wrzucasz do prania.", None),
        ("b3", 0.3, "Fotel pod spodem zostaje suchy. Link w bio.", None),
    ],
}


def chunks(text):
    """Podział na frazy wg interpunkcji; fraza > 4 słów dzielona równo na 2–3 słowa."""
    import math, re
    out = []
    for cl in re.findall(r"[^.,?!:…]+[.,?!:…]*", text):
        w = cl.split()
        if not w:
            continue
        if out and out[-1].endswith("\x00"):
            w = out.pop()[:-1].split() + w
        if len(w) == 1 and not cl.rstrip().endswith((".", "?", "!", "…")):
            out.append(w[0] + "\x00"); continue
        if len(w) <= 4:
            out.append(" ".join(w)); continue
        k = math.ceil(len(w) / 3); n = len(w)
        bounds = [round(n * t / k) for t in range(k + 1)]
        out += [" ".join(w[bounds[t]:bounds[t + 1]]) for t in range(k)]
    return [o.rstrip("\x00") for o in out]


def scene(clip, i, name, ss, vo, head):
    v = os.path.join(ROOT, "wideo", name + ".mp4")
    a = os.path.join(ROOT, "audio", f"t_{clip}_{i}.mp3")
    a2 = os.path.join(TMP, f"t_{clip}_{i}.wav")
    run(["ffmpeg", "-y", "-i", a, "-af",
         f"silenceremove=start_periods=1:start_threshold=-60dB:start_silence=0.08,areverse,silenceremove=start_periods=1:start_threshold=-60dB:start_silence=0.12,areverse,atempo={TEMPO}",
         "-ar", "44100", "-ac", "2", a2])
    ad = dur(a2)
    seg = max(ad + 0.25, 2.2)
    avail = min(dur(v) - ss - 0.05, MAXSRC.get(name, 99))
    slow = max(1.0, seg / avail)
    ws = words(a2)
    t0, t1 = ws[0]["start"], ws[-1]["end"]
    groups = CAP_TEXT[(clip, i)].split("|") if (clip, i) in CAP_TEXT else chunks(vo)
    lens = [len(g) + 1 for g in groups]
    tot = sum(lens); t = t0; caps = []
    for g, L in zip(groups, lens):
        e = t + (t1 - t0) * L / tot
        caps.append((t, e, g)); t = e
    caps[0] = (0.0, caps[0][1], caps[0][2])
    ct = CROP_TOP.get(name, 0)
    pre = f"crop=iw:ih*{1-ct:.3f}:0:ih*{ct:.3f}," if ct else ""
    inputs = ["-ss", f"{ss}", "-i", v, "-i", a2]
    filt = [f"[0:v]{pre}setpts={slow:.4f}*PTS,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,trim=0:{seg:.3f},setpts=PTS-STARTPTS[v0]"]
    last, n = "v0", 2
    if head:
        p = os.path.join(TMP, f"t_{clip}_{i}_h.png"); text_png(head, p, 100)
        inputs += ["-i", p]; filt.append(f"[{last}][{n}:v]overlay=0:270[v{n}]"); last, n = f"v{n}", n + 1
    y = CAP_Y.get(name, 520 if head else 330)
    for j, (s, e, txt) in enumerate(caps):
        p = os.path.join(TMP, f"t_{clip}_{i}_{j}.png"); text_png(textwrap.fill(txt.upper(), 18), p, 76)
        end = caps[j + 1][0] if j + 1 < len(caps) else seg
        inputs += ["-i", p]
        filt.append(f"[{last}][{n}:v]overlay=0:{y}:enable='between(t,{s:.2f},{end:.2f})'[v{n}]"); last, n = f"v{n}", n + 1
    filt.append(f"[1:a]apad,atrim=0:{seg:.3f}[a]")
    out = os.path.join(TMP, f"t_{clip}_{i:02d}.mp4")
    run(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", f"[{last}]", "-map", "[a]",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-ar", "44100", out])
    return out


if __name__ == "__main__":
    if sys.argv[1:] == ["lines"]:
        print(json.dumps([[f"t_{c}_{i}", s[2]] for c, sc in CLIPS.items() for i, s in enumerate(sc)], ensure_ascii=False))
        sys.exit()
    for clip in sys.argv[1:] or list(CLIPS):
        parts = [scene(clip, i, *s) for i, s in enumerate(CLIPS[clip])]
        lst = os.path.join(TMP, f"t_{clip}.txt")
        open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
        raw = os.path.join(TMP, f"t_{clip}_raw.mp4")
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", raw])
        out = os.path.join(OUT, f"{clip}.mp4")
        run(["ffmpeg", "-y", "-i", raw, "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1:LRA=11", "-c:a", "aac", "-b:a", "160k", "-ar", "44100", out])
        print(out, round(dur(out), 1), "s")
