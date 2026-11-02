#!/usr/bin/env python3
"""Montaż klipów Suchy Fotel: 3 wersje różniące się tylko hookiem.
Użycie: python3 montaz.py  (wymaga wideo/<scena>.mp4 i audio/<scena>.mp3)
"""
import json, os, subprocess, sys, textwrap
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
FONT = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
TMP = os.path.join(ROOT, "tmp"); os.makedirs(TMP, exist_ok=True)
OUT = os.path.join(ROOT, "gotowe"); os.makedirs(OUT, exist_ok=True)
TEMPO = 1.2  # lekko szybszy lektor – TikTokowe tempo
# przycięcie kadru: ułamek wysokości odcinany od góry (np. żeby twarz nie weszła w kadr)
CROP_TOP = {"h3": 0.22}
# wysokość napisów (y górnej krawędzi) per scena – tak, żeby nie zasłaniać produktu
CAP_Y = {"b1": 1340}

# scena -> (plik wideo, plik audio, nagłówek na całą scenę lub None, start w klipie źródłowym)
HOOKS = {
    "hook1": ("h1", "NAJGORSZE\nPO SIŁCE"),
    "hook2": ("h2", "WYLEWAM WODĘ\nNA FOTEL"),
    "hook3": ("h3", "PRZEZ LATA\nROBIŁEM TO ŹLE"),
}
BODY = [("b1", None), ("b2", "A FOTEL\nPOD SPODEM?"), ("b3", "FOTEL: SUCHY"), ("b4", None), ("b5", "159 ZŁ\nLINK W OPISIE")]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-2000:]); sys.exit(1)
    return r.stdout


def dur(p):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).strip())


def text_png(text, path, size, max_w=W - 160):
    font = ImageFont.truetype(FONT, size)
    lines = []
    for raw in text.split("\n"):
        lines += textwrap.wrap(raw, width=40) or [""]
    # zmniejsz, jeśli za szerokie
    while max(font.getlength(l) for l in lines) > max_w and size > 40:
        size -= 4; font = ImageFont.truetype(FONT, size)
    stroke = max(6, size // 9)
    lh = int(size * 1.15)
    img = Image.new("RGBA", (W, lh * len(lines) + stroke * 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, l in enumerate(lines):
        x = (W - font.getlength(l)) / 2
        d.text((x, stroke * 2 + i * lh), l, font=font, fill="white", stroke_width=stroke, stroke_fill="black")
    img.save(path)
    return img.size[1]


_model = None
def words(audio):
    """Słowa z czasami (whisper) -> grupy po 2–3 słowa."""
    global _model
    cache = audio + ".words.json"
    if os.path.exists(cache):
        return json.load(open(cache))
    import whisper
    if _model is None:
        _model = whisper.load_model("small")
    r = _model.transcribe(audio, language="pl", word_timestamps=True)
    ws = [w for s in r["segments"] for w in s["words"]]
    json.dump(ws, open(cache, "w"), ensure_ascii=False)
    return ws


def scene_clip(name, headline, script_words, idx):
    """Jedna scena: wideo + lektor + napisy, zwraca ścieżkę mp4."""
    v = os.path.join(ROOT, "wideo", name + ".mp4")
    a = os.path.join(ROOT, "audio", name + ".mp3")
    # przytnij ciszę na końcu lektora i przyspiesz
    a2 = os.path.join(TMP, f"{name}_a.wav")
    run(["ffmpeg", "-y", "-i", a, "-af",
         f"silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,atempo={TEMPO}",
         "-ar", "44100", "-ac", "2", a2])
    ad = dur(a2)
    seg = max(ad + 0.2, 2.4)
    vd = dur(v)
    slow = max(1.0, seg / (vd - 0.1))  # zwolnij wideo, jeśli lektor dłuższy niż klip
    # napisy zsynchronizowane: grupy 2–3 słów, poprawny zapis z tekstu skryptu
    # czas mowy z whispera; tekst ze skryptu (whisper źle łączy np. "po siłowni"),
    # grupy 2–3 słów rozłożone w czasie proporcjonalnie do liczby znaków
    ws = words(a2)
    t0, t1 = ws[0]["start"], ws[-1]["end"]
    groups = [g.split() for g in script_words.split("|")]
    lens = [sum(len(w) for w in g) + len(g) for g in groups]
    tot = sum(lens); t = t0; caps = []
    for g, L in zip(groups, lens):
        e = t + (t1 - t0) * L / tot
        caps.append((t, e, " ".join(g))); t = e
    caps[0] = (0.0, caps[0][1], caps[0][2])  # napis od pierwszej klatki
    inputs = ["-i", v, "-i", a2]
    ct = CROP_TOP.get(name, 0)
    pre = f"crop=iw:ih*{1-ct:.3f}:0:ih*{ct:.3f}," if ct else ""
    filt = [f"[0:v]{pre}setpts={slow:.4f}*PTS,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,trim=0:{seg:.3f},setpts=PTS-STARTPTS[v0]"]
    last = "v0"; n_in = 2
    if headline:
        p = os.path.join(TMP, f"{name}_head.png"); text_png(headline, p, 104)
        inputs += ["-i", p]
        filt.append(f"[{last}][{n_in}:v]overlay=0:270[v{n_in}]"); last = f"v{n_in}"; n_in += 1
    cap_y = CAP_Y.get(name, 560 if headline else 330)
    for j, (s, e, t) in enumerate(caps):
        p = os.path.join(TMP, f"{name}_c{j}.png"); text_png(t.upper().strip(" ."), p, 78)
        inputs += ["-i", p]
        end = caps[j + 1][0] if j + 1 < len(caps) else seg
        filt.append(f"[{last}][{n_in}:v]overlay=0:{cap_y}:enable='between(t,{s:.2f},{end:.2f})'[v{n_in}]")
        last = f"v{n_in}"; n_in += 1
    filt.append(f"[1:a]apad,atrim=0:{seg:.3f},volume=1.0[a]")
    out = os.path.join(TMP, f"{idx:02d}_{name}.mp4")
    run(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", f"[{last}]", "-map", "[a]",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-ar", "44100", out])
    return out


SCRIPT = {
    "h1": "Najgorsza rzecz|po siłowni?|Właśnie ta.",
    "h2": "Wylewam wodę|na fotel|w samochodzie.|Specjalnie.",
    "h3": "Przez lata wsiadałem|po treningu|prosto na tapicerkę.|A wystarczyło…",
    "b1": "Ręcznik na fotel.|Kaptur na zagłówek|i gotowe.|Kilka sekund.",
    "b2": "Góra to frotte.|Zbiera pot|i wodę.",
    "b3": "Spód jest|wodoodporny,|więc tapicerka|zostaje sucha.",
    "b4": "Waży 200 gramów.|Zwijasz|i wrzucasz|do bagażnika.",
    "b5": "Suchy Fotel.|Link w opisie.",
}

if __name__ == "__main__":
    only = sys.argv[1:] or list(HOOKS)
    body = [scene_clip(n, h, SCRIPT[n], i + 1) for i, (n, h) in enumerate(BODY)]
    for key in only:
        hn, hh = HOOKS[key]
        first = scene_clip(hn, hh, SCRIPT[hn], 0)
        lst = os.path.join(TMP, f"{key}.txt")
        open(lst, "w").write("".join(f"file '{p}'\n" for p in [first] + body))
        raw = os.path.join(TMP, f"{key}_raw.mp4")
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", raw])
        out = os.path.join(OUT, f"suchyfotel_{key}.mp4")
        # normalizacja głośności lektora (szczyt ok. -1 dB)
        run(["ffmpeg", "-y", "-i", raw, "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1:LRA=11", "-c:a", "aac", "-b:a", "160k", "-ar", "44100", out])
        print(out, round(dur(out), 1), "s")
