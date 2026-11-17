# -*- coding: utf-8 -*-
"""Motor de videos TikTok de Psiclín (1080x1920, 30 fps).
Cada video es una lista de escenas (html, duración). Las animaciones son CSS pausadas
que se posicionan en el tiempo exacto de cada cuadro."""
import os, sys, json, subprocess, shutil
from playwright.sync_api import sync_playwright

W, H, FPS = 1080, 1920, 30
SRC = "/home/claude/pack/src"
F = f"file://{SRC}/fonts"; I = f"file://{SRC}/img"
CREAM = "#F5E6C8"; DEEP = "#3D5A6C"; CORAL = "#FF8C7A"; SKY = "#7EC8E3"; SURF = "#FFFCF6"; INK2 = "#6E8FA6"

CSS = f"""
@font-face{{font-family:P;src:url({F}/poppins-400.woff2);font-weight:400}}
@font-face{{font-family:P;src:url({F}/poppins-500.woff2);font-weight:500}}
@font-face{{font-family:P;src:url({F}/poppins-600.woff2);font-weight:600}}
@font-face{{font-family:P;src:url({F}/poppins-700.woff2);font-weight:700}}
@font-face{{font-family:P;src:url({F}/poppins-800.woff2);font-weight:800}}
@font-face{{font-family:C;src:url({F}/caveat.woff2);font-weight:400 700}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;overflow:hidden;font-family:P,sans-serif;color:{DEEP}}}
.f{{position:relative;width:{W}px;height:{H}px;overflow:hidden}}
.abs{{position:absolute}}
.h{{font-weight:800;text-transform:uppercase;line-height:1.02;letter-spacing:-.015em}}
.c{{font-family:C,cursive;font-weight:700;line-height:1}}
.pill{{display:inline-block;padding:14px 30px;border-radius:999px;font-weight:700;font-size:34px;letter-spacing:.04em;text-transform:uppercase}}
.card{{background:{SURF};border-radius:52px;box-shadow:0 30px 70px rgba(60,40,20,.20)}}
.a{{animation-duration:.5s;animation-fill-mode:both;animation-timing-function:cubic-bezier(.2,.9,.25,1.12);animation-play-state:paused}}
.grain::after{{content:"";position:absolute;inset:0;pointer-events:none;opacity:.05;background-image:radial-gradient(rgba(60,40,20,.9) 1px,transparent 1.2px);background-size:6px 6px}}
@keyframes pop{{from{{opacity:0;transform:scale(.82)}}to{{opacity:1;transform:scale(1)}}}}
@keyframes up{{from{{opacity:0;transform:translateY(70px)}}to{{opacity:1;transform:none}}}}
@keyframes left{{from{{opacity:0;transform:translateX(-90px)}}to{{opacity:1;transform:none}}}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes stamp{{0%{{opacity:0;transform:scale(1.9)}}70%{{opacity:1;transform:scale(.94)}}100%{{opacity:1;transform:scale(1)}}}}
@keyframes strike{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
@keyframes drift{{from{{transform:translate(0,0)}}to{{transform:translate(50px,-70px)}}}}
@keyframes drift2{{from{{transform:translate(0,0)}}to{{transform:translate(-60px,50px)}}}}
@keyframes zoom{{from{{transform:scale(1)}}to{{transform:scale(1.06)}}}}
"""

def A(name, delay=0.0, dur=0.5, extra=""):
    return f"animation-name:{name};animation-delay:{delay}s;animation-duration:{dur}s;{extra}"

def blob(x, y, s, col, op=.35, d=None, k="drift"):
    anim = f'class="abs a" style="{A(k,0,d,"animation-timing-function:linear;")}' if d else 'class="abs" style="'
    return f'<div {anim}left:{x}px;top:{y}px;width:{s}px;height:{s}px;border-radius:50%;background:{col};opacity:{op}"></div>'

def iso_badge(top=232, right=84, size=86):
    # isotipo siempre sobre una pastilla blanca: así se ve en cualquier fondo
    return (f'<div class="abs" style="right:{right}px;top:{top}px;width:{size+44}px;height:{int(size*.69)+30}px;'
            f'border-radius:999px;background:#fff;display:flex;align-items:center;justify-content:center;'
            f'box-shadow:0 10px 26px rgba(0,0,0,.12)"><img src="{I}/isotipo.png" style="width:{size}px"></div>')

def bg(kind, d):
    if kind == "crema":
        return (f'<div class="abs" style="inset:0;background:{CREAM}"></div>' + blob(640, -160, 620, CORAL, .25, d)
                + blob(-220, 1380, 560, SKY, .32, d, "drift2"))
    if kind == "coral":
        return (f'<div class="abs" style="inset:0;background:{CORAL}"></div>' + blob(620, 1300, 700, "#fff", .18, d)
                + blob(-260, -200, 560, CREAM, .25, d, "drift2"))
    if kind == "cielo":
        return (f'<div class="abs" style="inset:0;background:linear-gradient(180deg,#8FD3EA 0%,#5BA4CF 100%)"></div>'
                + blob(560, -200, 640, "#fff", .18, d) + blob(-240, 1400, 520, "#fff", .14, d, "drift2"))
    if kind == "deep":
        return (f'<div class="abs" style="inset:0;background:{DEEP}"></div>' + blob(600, -220, 660, CORAL, .22, d)
                + blob(-260, 1380, 560, SKY, .20, d, "drift2"))
    if kind == "sepia":
        return (f'<div class="abs" style="inset:0;background:radial-gradient(ellipse at 50% 40%,#6b5644 0%,#2e231c 85%)"></div>'
                + f'<div class="abs" style="inset:0;box-shadow:inset 0 0 260px rgba(0,0,0,.75)"></div>')
    if kind == "sunset":
        return (f'<div class="abs" style="inset:0;background:linear-gradient(160deg,{CORAL} 0%,#F7B49A 45%,{SKY} 100%)"></div>'
                + blob(560, -180, 600, "#fff", .18, d))
    raise ValueError(kind)

def scene(kind, body, dur, iso=True):
    return (f'<div class="f grain">{bg(kind, dur)}{body}{iso_badge() if iso else ""}</div>', dur)

def page(inner):
    inner = inner.replace(" %", " %")
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{inner}</body></html>'

def endcard(dur=2.6):
    body = f'''
<div class="abs" style="left:0;right:0;top:560px;display:flex;flex-direction:column;align-items:center">
  <div class="a" style="{A('pop',0.05,.55)}"><img src="{I}/isotipo.png" style="width:330px"></div>
  <div class="h a" style="{A('up',0.35)}font-size:84px;text-align:center;margin-top:70px;line-height:1.05">Psicología que<br>te escucha.</div>
  <div class="a" style="{A('pop',0.8)}margin-top:56px"><span class="pill" style="background:{CORAL};color:{DEEP};font-size:40px;padding:22px 44px">Escríbenos · link en la bio</span></div>
  <div class="c a" style="{A('fade',1.2)}font-size:64px;color:{INK2};margin-top:40px">presencial y en línea · Medellín</div>
</div>'''
    return scene("crema", body, dur, iso=False)

# ----------------------------------------------------------------- render
def render(vid, scenes, outdir):
    tmp = f"/tmp/tt_{vid}"; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    parts = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": W, "height": H})
        for i, (html, dur) in enumerate(scenes):
            path = f"{tmp}/s{i}.html"; open(path, "w").write(page(html))
            pg.goto(f"file://{path}"); pg.wait_for_load_state("load")
            ok = pg.evaluate("Promise.all([document.fonts.load('800 40px P'),document.fonts.load('400 40px P'),document.fonts.load('700 40px C')]).then(r=>r.every(x=>x.length>0))")
            assert ok, "fuentes no cargaron"
            pg.evaluate("document.fonts.ready")
            n = round(dur * FPS); part = f"{tmp}/s{i}.part.mp4"; final = f"{tmp}/s{i}.mp4"
            ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg",
                                   "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                                   "-r", str(FPS), part], stdin=subprocess.PIPE)
            for k in range(n):
                t = k / FPS * 1000
                pg.evaluate(f"document.getAnimations().forEach(a=>{{a.pause();a.currentTime={t}}})")
                ff.stdin.write(pg.screenshot(type="jpeg", quality=92))
            ff.stdin.close(); assert ff.wait() == 0
            os.rename(part, final); parts.append(final)
        b.close()
    lst = f"{tmp}/list.txt"; open(lst, "w").write("".join(f"file '{x}'\n" for x in parts))
    out = f"{outdir}/{vid}.mp4"; part = out.replace(".mp4", ".part.mp4")
    # pista de audio silenciosa: TikTok y Metricool aceptan mejor videos con audio; el sonido real se elige en la app
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest", "-c:v", "copy", "-c:a", "aac",
                    "-movflags", "+faststart", part], check=True)
    os.rename(part, out)
    return out

def stills(vid, scenes, outdir, at=None):
    """Cuadros de control: el último cuadro de cada escena (cuando todo está en pantalla)."""
    os.makedirs(outdir, exist_ok=True); res = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": W, "height": H})
        for i, (html, dur) in enumerate(scenes):
            path = f"/tmp/st_{vid}_{i}.html"; open(path, "w").write(page(html))
            pg.goto(f"file://{path}"); pg.evaluate("document.fonts.ready")
            t = (at if at is not None else dur - 0.05) * 1000
            pg.evaluate(f"document.getAnimations().forEach(a=>{{a.pause();a.currentTime={t}}})")
            f = f"{outdir}/{vid}_{i}.jpg"; pg.screenshot(path=f, type="jpeg", quality=80); res.append(f)
        b.close()
    return res
