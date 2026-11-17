# -*- coding: utf-8 -*-
"""Motor de sketches con las comas de Psiclín: boca sincronizada con la voz, parpadeo,
gestos, escenarios, título fijo arriba y subtítulos."""
import os, math, json, subprocess, shutil
import numpy as np
from playwright.sync_api import sync_playwright
from tt import CSS, W, H, FPS, I, CREAM, DEEP, CORAL, SKY, SURF, INK2, iso_badge
from chars import char
from audio import pcm, SR

AUD = "/home/claude/tiktok/audio"

# ------------------------------------------------------------------ elenco
CAST = {
    "coral":   dict(color=CORAL,     acc="",      name="Tú"),
    "mateo":   dict(color="#7EC8A0", acc="",      name="Mateo"),
    "andres":  dict(color="#F4B266", acc="gorra", name="Andrés"),
    "cerebro": dict(color="#FFC2D1", acc="",      name="Tu cerebro"),
    "celeste": dict(color=SKY,       acc="gafas", name="La psicóloga"),
    "amiga":   dict(color="#F4B266", acc="",      name="Tu amiga"),
    "dr":      dict(color="#8A7A6A", acc="barba", name="El psicólogo de película"),
}

# ------------------------------------------------------------------ escenarios
def floor(col, top=1150): return f'<div class="abs" style="left:0;right:0;top:{top}px;bottom:0;background:{col}"></div>'
def bg_tienda():
    shelves = "".join(f'<div class="abs" style="left:{60+i*130}px;top:{y}px;width:100px;height:120px;border-radius:14px;background:{c}"></div>'
                      for y in (450, 620) for i, c in enumerate([CORAL, SKY, "#F4B266", "#7EC8A0", "#FFC2D1", CORAL, SKY]))
    return (f'<div class="abs" style="inset:0;background:#F3DDB8"></div>'
            f'<div class="abs" style="left:40px;right:40px;top:420px;height:370px;border-radius:24px;background:#E7C99A"></div>{shelves}'
            f'<div class="abs" style="left:330px;top:345px;padding:6px 36px;border-radius:14px;background:{DEEP};color:#fff;font:800 44px P;letter-spacing:.12em">TIENDA</div>'
            + floor("#D9B98C", 1120) +
            f'<div class="abs" style="left:-20px;right:-20px;top:1020px;height:150px;border-radius:30px 30px 0 0;background:#B98B5E"></div>')
def bg_noche():
    return (f'<div class="abs" style="inset:0;background:linear-gradient(180deg,#22384a,#2f4d63)"></div>'
            f'<div class="abs" style="left:560px;top:330px;width:330px;height:380px;border-radius:24px;background:#16283a;border:16px solid #e9d8bb"></div>'
            f'<div class="abs" style="left:700px;top:390px;width:110px;height:110px;border-radius:50%;background:#f7e9c5;box-shadow:0 0 60px rgba(247,233,197,.6)"></div>'
            + floor("#273f52", 1150) +
            f'<div class="abs" style="left:40px;top:1010px;width:820px;height:200px;border-radius:40px 40px 10px 10px;background:{SKY}"></div>'
            f'<div class="abs" style="left:60px;top:960px;width:230px;height:110px;border-radius:40px;background:#fff"></div>')
def bg_sala(night=False):
    wall = "#2f4d63" if night else CREAM
    lamp = (f'<div class="abs" style="left:820px;top:520px;width:20px;height:520px;background:#c9a77e"></div>'
            f'<div class="abs" style="left:760px;top:440px;width:140px;height:110px;border-radius:20px 20px 60px 60px;background:#f7e1a8;box-shadow:0 0 120px 40px rgba(247,225,168,.35)"></div>') if night else \
           (f'<div class="abs" style="left:640px;top:360px;width:260px;height:300px;border-radius:20px;background:#fff;border:14px solid #e2cfa9"></div>'
            f'<div class="abs" style="left:676px;top:396px;width:188px;height:228px;border-radius:12px;background:linear-gradient(160deg,{SKY},{CORAL});opacity:.6"></div>')
    return (f'<div class="abs" style="inset:0;background:{wall}"></div>{lamp}' + floor("#3b5a70" if night else "#e2cfa9", 1150) +
            f'<div class="abs" style="left:40px;top:930px;width:700px;height:250px;border-radius:60px 60px 20px 20px;background:{"#5BA4CF" if night else "#7EC8A0"}"></div>'
            f'<div class="abs" style="left:20px;top:1040px;width:740px;height:150px;border-radius:40px;background:{"#4a8fba" if night else "#69b48c"}"></div>')
def bg_consultorio():
    return (f'<div class="abs" style="inset:0;background:{CREAM}"></div>' + floor("#e2cfa9", 1150) +
            f'<div class="abs" style="left:110px;top:380px;width:240px;height:300px;border-radius:20px;background:#fff;border:14px solid #e2cfa9"></div>'
            f'<div class="abs" style="left:150px;top:420px;width:160px;height:220px;border-radius:12px;background:linear-gradient(160deg,{SKY},{CORAL});opacity:.7"></div>'
            f'<div class="abs" style="left:470px;top:860px;width:110px;height:230px;border-radius:55px 55px 10px 10px;background:#7EC8A0;opacity:.85"></div>'
            f'<div class="abs" style="left:460px;top:1060px;width:130px;height:120px;border-radius:20px;background:#c98f6a"></div>')
def bg_consejo():
    return (f'<div class="abs" style="inset:0;background:{CREAM}"></div>' + floor("#e2cfa9", 1150) +
            f'<div class="abs" style="left:680px;top:340px;width:230px;height:270px;border-radius:20px;background:#fff;border:14px solid #e2cfa9"></div>'
            f'<div class="abs" style="left:716px;top:376px;width:158px;height:198px;border-radius:12px;background:linear-gradient(160deg,{SKY},{CORAL});opacity:.7"></div>'
            f'<div class="abs c" style="left:84px;top:380px;font-size:76px;line-height:1.05;color:{CORAL};transform:rotate(-4deg)">consejo de<br>la psicóloga</div>')
def bg_pelicula():
    return (f'<div class="abs" style="inset:0;background:radial-gradient(ellipse at 50% 40%,#6b5644 0%,#2e231c 85%)"></div>'
            + floor("#3a2c22", 1150) +
            f'<div class="abs" style="left:30px;top:1000px;width:620px;height:150px;border-radius:70px 20px 20px 20px;background:#5a3420"></div>'
            f'<div class="abs" style="left:30px;top:900px;width:150px;height:200px;border-radius:70px 70px 20px 20px;background:#5a3420"></div>'
            f'<div class="abs" style="inset:0;box-shadow:inset 0 0 260px rgba(0,0,0,.8)"></div>')
BGS = {"tienda": bg_tienda, "noche": bg_noche, "sala": bg_sala, "sala_noche": lambda: bg_sala(True),
       "consultorio": bg_consultorio, "consejo": bg_consejo, "pelicula": bg_pelicula}

# ------------------------------------------------------------------ piezas del guion
class Line:
    def __init__(self, who, take, seg, text, shot, exprs=None, gap=0.22, overlay=None, poses=None):
        self.who, self.take, self.seg, self.text, self.shot = who, take, seg, text, shot
        self.exprs, self.gap, self.overlay, self.poses = exprs or {}, gap, overlay, poses or {}
        self.dur = (seg[1] - seg[0]) + gap
class Beat:
    def __init__(self, dur, shot, exprs=None, overlay=None, poses=None, text=None):
        self.dur, self.shot, self.exprs, self.overlay, self.poses, self.text = dur, shot, exprs or {}, overlay, poses or {}, text
        self.who = None
class Card:
    def __init__(self, dur, html): self.dur, self.html, self.shot = dur, html, "__card"

def envelope(take, seg):
    x = pcm(f"{AUD}/{take}.mp3"); a, b = int(seg[0] * SR), int(seg[1] * SR); x = x[a:b]
    n = SR // FPS; m = max(1, len(x) // n); r = np.sqrt((x[:m * n].reshape(m, n) ** 2).mean(1))
    p = np.percentile(r, 90) + 1e-6; v = np.clip((r / p - 0.12) * 1.25, 0, 1)
    v = np.convolve(v, [0.25, 0.5, 0.25], mode="same")
    return v

# ------------------------------------------------------------------ cuadro
def subtitle(who, text):
    c = CAST[who]
    return (f'<div class="abs" style="left:70px;right:150px;top:1210px;display:flex;flex-direction:column;align-items:center;gap:14px">'
            f'<span style="background:{c["color"]};color:{DEEP};font:800 30px P;letter-spacing:.06em;text-transform:uppercase;padding:8px 22px;border-radius:999px">{c["name"]}</span>'
            f'<span style="background:#fff;color:{DEEP};font:700 50px/1.28 P;padding:16px 28px;border-radius:24px;text-align:center;'
            f'box-shadow:0 12px 30px rgba(0,0,0,.18)">{text}</span></div>')
def title(t):
    return (f'<div class="abs" style="left:70px;right:250px;top:236px"><span style="background:{DEEP};color:#fff;font:800 50px/1.25 P;'
            f'padding:12px 26px;border-radius:20px;-webkit-box-decoration-break:clone;box-decoration-break:clone">{t}</span></div>')

def frame_html(item, lt, gt, shots, top_title, mouthv):
    if isinstance(item, Card):
        return item.html(lt) if callable(item.html) else item.html
    sh = shots[item.shot]; out = BGS[sh["bg"]]()
    for k, (cid, pos) in enumerate(sh["chars"].items()):
        c = CAST[cid]; ph = k * 1.37
        expr = item.exprs.get(cid, pos.get("expr", "neutral"))
        speaking = item.who == cid
        m = mouthv if speaking else 0.0
        blink = ((gt + ph) % 3.4) < 0.12 and expr not in ("cerrados", "susto", "loco")
        if blink: expr_d = "cerrados"
        else: expr_d = expr
        pose = item.poses.get(cid, pos.get("pose", "abajo"))
        if speaking and m > 0.35 and pose == "abajo": pose = "habla"
        bob = -10 * m + 3 * math.sin(gt * 2.2 + ph)
        rot = pos.get("rot", 0) + 1.6 * math.sin(gt * 1.6 + ph)
        sc = pos.get("scale", 1.35)
        if pos.get("enter") is not None:          # aparece con un rebote
            t0 = pos["enter"]; e = min(1, max(0, (gt - t0) / 0.35))
            if e <= 0: continue
            sc *= 0.6 + 0.4 * (1 - (1 - e) ** 3) + 0.08 * math.sin(e * math.pi)
        out += char(c["color"], pos["x"], pos["y"], sc, expr_d, m, c["acc"], pose, pos.get("flip", False), rot, bob)
    if item.overlay: out += item.overlay(lt) if callable(item.overlay) else item.overlay
    if top_title: out += title(top_title)
    if item.who: out += subtitle(item.who, item.text)
    elif item.text: out += f'<div class="abs" style="left:70px;right:150px;top:1250px;text-align:center"><span style="background:{DEEP};color:#fff;font:700 46px/1.3 P;padding:14px 26px;border-radius:20px">{item.text}</span></div>'
    return out

# ------------------------------------------------------------------ render
def render_skit(vid, items, shots, top_title, outdir, preview=None):
    # tiempos
    t = 0.0; plan = []
    for it in items:
        plan.append((t, it)); t += it.dur
    total = t
    envs = {id(it): envelope(it.take, it.seg) for _, it in plan if isinstance(it, Line)}
    tmp = f"/tmp/sk_{vid}"; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    shell = (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
             f'<div class="f grain"><div id="st" class="abs" style="inset:0"></div>{iso_badge()}</div></body></html>')
    open(f"{tmp}/shell.html", "w").write(shell)
    def html_at(gt):
        for st, it in reversed(plan):
            if gt >= st: break
        lt = gt - st; mv = 0.0
        if isinstance(it, Line):
            e = envs[id(it)]; k = int(lt * FPS); mv = float(e[k]) if k < len(e) else 0.0
        tt = None if isinstance(it, Card) else top_title
        return frame_html(it, lt, gt, shots, tt, mv).replace(" %", " %"), it
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": W, "height": H}); pg.goto(f"file://{tmp}/shell.html")
        assert pg.evaluate("Promise.all([document.fonts.load('800 40px P'),document.fonts.load('700 40px P'),document.fonts.load('700 40px C')]).then(r=>r.every(x=>x.length>0))")
        if preview is not None:
            outs = []
            for i, gt in enumerate(preview):
                h, _ = html_at(gt); pg.evaluate("h=>{document.getElementById('st').innerHTML=h}", h)
                f = f"{outdir}/{vid}_p{i}.jpg"; pg.screenshot(path=f, type="jpeg", quality=80); outs.append(f)
            b.close(); return outs, total
        # una pieza de video por plano (cambio de escenario)
        n = round(total * FPS); parts = []; cur = None; ff = None
        def close():
            ff.stdin.close(); assert ff.wait() == 0; os.rename(parts[-1] + ".part.mp4", parts[-1])
        for k in range(n):
            gt = k / FPS; h, it = html_at(gt)
            if it.shot != cur:
                if ff: close()
                cur = it.shot; parts.append(f"{tmp}/p{len(parts):02d}.mp4")
                ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                                       "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS),
                                       parts[-1] + ".part.mp4"], stdin=subprocess.PIPE)
            pg.evaluate("h=>{document.getElementById('st').innerHTML=h}", h)
            ff.stdin.write(pg.screenshot(type="jpeg", quality=92))
        close(); b.close()
    lst = f"{tmp}/list.txt"; open(lst, "w").write("".join(f"file '{x}'\n" for x in parts))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", f"{tmp}/video.mp4"], check=True)
    # pista de voces
    ins, flt = [], []
    lines = [(st, it) for st, it in plan if isinstance(it, Line)]
    for j, (st, it) in enumerate(lines):
        ins += ["-i", f"{AUD}/{it.take}.mp3"]
        d = int(st * 1000)
        flt.append(f"[{j}:a]atrim={it.seg[0]}:{it.seg[1]},asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=stereo,adelay={d}|{d}[a{j}]")
    mix = "".join(f"[a{j}]" for j in range(len(lines)))
    flt.append(f"{mix}amix=inputs={len(lines)}:normalize=0,apad,atrim=0:{total:.3f},loudnorm=I=-15:TP=-1.5:LRA=11[out]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(flt), "-map", "[out]", "-ar", "44100", f"{tmp}/voz.wav"], check=True)
    out = f"{outdir}/{vid}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{tmp}/video.mp4", "-i", f"{tmp}/voz.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out + ".part.mp4"], check=True)
    os.rename(out + ".part.mp4", out)
    return out, total
