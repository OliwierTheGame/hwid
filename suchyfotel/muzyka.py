#!/usr/bin/env python3
"""Własny podkład muzyczny (bez praw osób trzecich): lo-fi / chill, generowany syntetycznie.
Tworzy muzyka/<nazwa>.wav (40 s). Użycie: python3 muzyka.py
"""
import os, subprocess, wave
import numpy as np

SR = 44100
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "muzyka")
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(7)


def note(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def keys(freq, dur, vel=0.18):
    """Ciepły „Rhodes”: kilka harmonicznych, wolny atak, wybrzmienie, tremolo."""
    t = np.arange(int(dur * SR)) / SR
    env = (1 - np.exp(-t * 40)) * np.exp(-t * 1.1)
    s = sum(a * np.sin(2 * np.pi * freq * k * t + 0.3 * k) for k, a in [(1, 1), (2, 0.35), (3, 0.12), (4, 0.05)])
    trem = 1 + 0.08 * np.sin(2 * np.pi * 4.2 * t)
    return vel * s * env * trem


def bass(freq, dur, vel=0.30):
    t = np.arange(int(dur * SR)) / SR
    env = (1 - np.exp(-t * 80)) * np.exp(-t * 1.6)
    return vel * (np.sin(2 * np.pi * freq * t) + 0.2 * np.sin(4 * np.pi * freq * t)) * env


def kick(vel=0.55):
    t = np.arange(int(0.35 * SR)) / SR
    f = 45 + 90 * np.exp(-t * 30)
    return vel * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)


def snare(vel=0.08):
    t = np.arange(int(0.25 * SR)) / SR
    n = rng.standard_normal(len(t))
    n = np.convolve(n, np.ones(6) / 6, mode="same")  # zmiękczenie
    return vel * (n * np.exp(-t * 18) + 0.4 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 25))


def hat(vel=0.04):
    t = np.arange(int(0.06 * SR)) / SR
    n = rng.standard_normal(len(t))
    n = n - np.convolve(n, np.ones(3) / 3, mode="same")  # górne pasmo
    return vel * n * np.exp(-t * 70)


def add(buf, sig, at):
    i = int(at * SR)
    j = min(len(buf), i + len(sig))
    if i < len(buf):
        buf[i:j] += sig[: j - i]


def track(name, bpm, chords, length=40.0, swing=0.08):
    beat = 60 / bpm
    bar = 4 * beat
    L = int(length * SR)
    mus = np.zeros(L); drm = np.zeros(L)
    nbars = int(length / bar) + 1
    for b in range(nbars):
        ch = chords[b % len(chords)]
        t0 = b * bar
        # akord rozłożony lekko (strum) + powtórka na „i” trzeciej ćwierćnuty
        for k, m in enumerate(ch[1:]):
            add(mus, keys(note(m), bar * 0.95), t0 + k * 0.018)
            add(mus, keys(note(m), beat * 1.4, 0.08), t0 + 2.5 * beat + k * 0.015)
        add(mus, bass(note(ch[0]), beat * 1.8), t0)
        add(mus, bass(note(ch[0]), beat * 1.2, 0.22), t0 + 2.5 * beat)
        for q in range(4):
            tq = t0 + q * beat
            if q in (0, 2):
                add(drm, kick(), tq)
            if q == 2 and b % 2:
                add(drm, kick(0.35), tq + 0.5 * beat + swing * beat)
            if q in (1, 3):
                add(drm, snare(), tq)
            for e in (0, 1):
                add(drm, hat(0.05 if e == 0 else 0.035), tq + e * (0.5 + swing) * beat)
    # szum winylu + trzaski
    crackle = 0.004 * rng.standard_normal(L)
    clicks = (rng.random(L) > 0.99985) * rng.standard_normal(L) * 0.12
    mix = mus + 0.8 * drm + np.convolve(crackle + clicks, np.ones(8) / 8, mode="same")
    # wejście i wyjście
    fade = int(1.5 * SR)
    mix[:fade] *= np.linspace(0, 1, fade)
    mix[-fade:] *= np.linspace(1, 0, fade)
    mix /= np.max(np.abs(mix)) * 1.1
    raw = os.path.join(OUT, f"_{name}_raw.wav")
    st = np.stack([mix, np.roll(mix, int(0.012 * SR))], axis=1)  # lekka szerokość stereo
    with wave.open(raw, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())
    # filtr „lo-fi” + pogłos + głośność
    out = os.path.join(OUT, f"{name}.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af",
                    "lowpass=f=5200,highpass=f=35,aecho=0.8:0.5:60|110:0.18|0.12,loudnorm=I=-16:TP=-1.5",
                    "-ar", "44100", out], check=True)
    os.remove(raw)
    print(out)


# akordy: [bas, nuty akordu] (MIDI)
track("chill", 84, [[45, 57, 60, 64, 67], [41, 57, 60, 64, 65], [48, 55, 59, 64, 67], [43, 55, 59, 62, 64]])   # Am7 Fmaj7 Cmaj7 G6
track("ciepla", 96, [[48, 60, 64, 67, 71], [45, 57, 60, 64, 67], [41, 57, 60, 65, 69], [43, 55, 59, 62, 67]])  # Cmaj7 Am7 Fmaj7 G
track("spokojna", 74, [[50, 57, 60, 62, 65], [46, 58, 62, 65, 69], [41, 57, 60, 64, 65], [45, 55, 57, 61, 64]])  # Dm7 Bbmaj7 Fmaj7 A7
