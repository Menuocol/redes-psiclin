# -*- coding: utf-8 -*-
"""Lote 1 de TikTok actuados (las comas de Psiclín)."""
import math, sys
from skit import *
from tt import bg as tbg

def fade(lt, t0, d=0.3):
    e = min(1, max(0, (lt - t0) / d)); return f"opacity:{e:.3f};transform:translateY({(1-e)*40:.1f}px);"

def card(kind, big, note=None, small=None, pill=None, big_col="#fff"):
    def f(lt):
        h = tbg(kind, 3)
        h += '<div class="abs" style="left:84px;right:150px;top:330px;bottom:440px;display:flex;flex-direction:column;justify-content:center;gap:44px">'
        if pill: h += f'<div style="{fade(lt,0)}align-self:flex-start"><span class="pill" style="background:#fff;color:{DEEP}">{pill}</span></div>'
        h += f'<div class="h" style="{fade(lt,0.05)}font-size:104px;color:{big_col}">{big}</div>'
        if note: h += f'<div style="{fade(lt,0.7)}transform-origin:left"><div class="c" style="font-size:88px;color:{CORAL if kind!="coral" else "#fff"};transform:rotate(-3deg)">{note}</div></div>'
        if small: h += f'<div style="{fade(lt,1.2)}font:600 48px/1.3 P;color:{SKY if kind=="deep" else INK2}">{small}</div>'
        return h + "</div>"
    return f

def endcard(lt):
    b = 4 * math.sin(lt * 5)
    h = tbg("crema", 3)
    h += char(CORAL, 330, 900 + b, 1.25, "feliz", 0, "", "arriba")
    h += char(SKY, 750, 900 - b, 1.25, "feliz", 0, "gafas", "arriba", flip=True)
    h += (f'<div class="abs" style="left:0;right:0;top:960px;display:flex;flex-direction:column;align-items:center;gap:34px">'
          f'<div style="{fade(lt,0.1)}"><img src="{I}/isotipo.png" style="width:170px"></div>'
          f'<div class="h" style="{fade(lt,0.3)}font-size:80px;text-align:center;line-height:1.05">Psicología que<br>te escucha.</div>'
          f'<div style="{fade(lt,0.7)}"><span class="pill" style="background:{CORAL};color:{DEEP};font-size:40px;padding:20px 40px">Escríbenos · link en la bio</span></div></div>')
    return h

def starts(items):
    t, out = 0.0, []
    for it in items: out.append(t); t += it.dur
    return out

def stamp(label, bgc, col, border=False):
    def f(lt):
        e = min(1, lt / 0.35); s = 1.8 - 0.8 * (1 - (1 - e) ** 3)
        bd = f"border:6px solid {col};" if border else ""
        return (f'<div class="abs" style="left:84px;top:420px;transform:scale({s:.3f}) rotate(-4deg);transform-origin:left;opacity:{e:.2f}">'
                f'<span class="pill" style="background:{bgc};color:{col};font-size:52px;{bd}">{label}</span></div>')
    return f

# ======================================================================= S1
def s1():
    T = "Pregúntale dos veces."
    shots = {"t": {"bg": "tienda", "chars": {"andres": dict(x=300, y=1165, scale=1.6), "mateo": dict(x=770, y=1165, scale=1.6, flip=True)}}}
    def piensa(lt):
        chips = ["no duermo bien", "la plata", "el trabajo", "todo solo"]
        h = (f'<div class="abs" style="left:430px;top:450px;width:520px;height:360px;border-radius:180px;background:#fff;box-shadow:0 20px 50px rgba(0,0,0,.15)"></div>'
             f'<div class="abs" style="left:700px;top:790px;width:60px;height:60px;border-radius:50%;background:#fff"></div>'
             f'<div class="abs" style="left:745px;top:860px;width:34px;height:34px;border-radius:50%;background:#fff"></div>'
             f'<div class="abs c" style="left:600px;top:372px;font-size:66px;color:{CORAL};transform:rotate(-4deg)">lo que no dijo:</div>')
        for k, c in enumerate(chips):
            h += (f'<div class="abs" style="left:{490 + (k%2)*190}px;top:{470 + k*70}px;{fade(lt, 0.15 + k*0.35, .25)}">'
                  f'<span style="background:{DEEP};color:#fff;font:700 40px P;padding:8px 20px;border-radius:14px;white-space:nowrap">{c}</span></div>')
        return h
    A, M = "s1_andres_a", "s1_mateo_a"
    items = [
        Line("andres", A, (0.0, 1.95), "¡Quiubo, parce! ¿Cómo vas?", "t", {"andres": "feliz", "mateo": "neutral"}),
        Line("mateo", M, (0.0, 2.95), "Bien, bien. Normal, ahí vamos.", "t", {"mateo": "feliz", "andres": "feliz"}, gap=0.1),
        Beat(2.8, "t", {"mateo": "triste", "andres": "neutral"}, overlay=piensa),
        Line("andres", A, (2.60, 5.20), "Ajá… ¿Y de verdad, cómo vas?", "t", {"andres": "lado", "mateo": "pena"}, gap=0.5),
        Line("mateo", M, (3.55, 7.20), "…Mal, hermano. Hace rato no duermo bien.", "t", {"mateo": "triste", "andres": "triste"}),
        Line("andres", A, (5.45, 8.56), "Gracias por contarme. Aquí estoy. Hablemos.", "t", {"andres": "feliz", "mateo": "neutral"}, poses={"andres": "arriba"}, gap=0.5),
        Card(3.4, card("deep", "A veces un “normal” necesita una segunda pregunta.", "pedir ayuda también es de hombres", pill="19 nov · Día Internacional del Hombre")),
        Card(2.6, endcard)]
    return items, shots, T

# ======================================================================= S2
def s2():
    T = "Tu cerebro a las 3 a. m."
    C, B, P = "s2_coral_a", "s2_cerebro_a", "s2_celeste_a"
    def manta(lt=0): return '<div class="abs" style="left:250px;top:1035px;width:640px;height:170px;border-radius:40px;background:#e9d8bb"></div>'
    def reloj(lt=0): return f'<div class="abs" style="left:84px;top:350px;font:800 60px P;color:#fff;opacity:.9">3:07 a. m.</div>'
    base = lambda lt: manta() + reloj()
    def anota(lt):
        n = min(4, int(lt / 0.3) + 1)
        rows = "".join(f'<div style="height:12px;width:{220 - k*30}px;border-radius:6px;background:{DEEP};opacity:.6;margin-top:22px"></div>' for k in range(n))
        return manta() + reloj() + (f'<div class="abs" style="left:300px;top:930px;width:300px;height:210px;background:#fff;border-radius:18px;padding:22px 26px;'
                                     f'transform:rotate(6deg);box-shadow:0 14px 30px rgba(0,0,0,.25)">{rows}</div>')
    def zz(lt):
        return manta() + "".join(f'<div class="abs c" style="left:{330 + k*70}px;top:{700 - k*70 - (lt*30)%40}px;font-size:{70 + k*20}px;color:#fff;opacity:{min(1,max(0,(lt-k*0.3)/0.3)):.2f}">z</div>' for k in range(3))
    items = [
        Line("coral", C, (0.0, 3.35), "Bueno, a dormir, que mañana madrugo.", "cama", {"coral": "neutral"}, overlay=base, gap=0.3),
        Line("cerebro", B, (0.0, 3.9), "¡Hola! ¿Repasamos lo que dijiste en esa reunión del 2019?", "cama", {"cerebro": "loco", "coral": "susto"}, overlay=base),
        Line("coral", C, (3.38, 4.10), "No.", "cama", {"coral": "lado", "cerebro": "loco"}, overlay=base),
        Line("cerebro", B, (4.30, 8.70), "¿Y si mañana todo sale mal? ¿Y ese mensaje que dejaste en visto?", "cama", {"cerebro": "loco", "coral": "susto"}, overlay=base),
        Line("coral", C, (4.30, 5.60), "¿Por qué eres así?", "cama", {"coral": "pena", "cerebro": "feliz"}, overlay=base, gap=0.4),
        Line("celeste", P, (0.0, 6.50), "Un truco: escribe en un papel lo que te está dando vueltas y dile a tu cabeza: “mañana lo pensamos”.", "consejo", {"celeste": "feliz"}, gap=0.3),
        Beat(1.4, "cama", {"coral": "feliz", "cerebro": "neutral"}, overlay=anota),
        Line("cerebro", B, (8.75, 11.60), "Bueno… mañana.", "cama", {"cerebro": "cerrados", "coral": "feliz"}, overlay=base),
        Beat(1.5, "cama", {"coral": "cerrados", "cerebro": "cerrados"}, overlay=zz),
        Card(3.4, card("deep", "Si te pasa casi todas las noches, vale la pena hablarlo.", "no tienes que resolverlo sin ayuda")),
        Card(2.6, endcard)]
    st = starts(items)
    shots = {"cama": {"bg": "noche", "chars": {"coral": dict(x=380, y=1100, scale=1.5),
                                               "cerebro": dict(x=790, y=990, scale=1.1, flip=True, enter=st[1])}},
             "consejo": {"bg": "consejo", "chars": {"celeste": dict(x=640, y=1160, scale=1.7, flip=True)}}}
    return items, shots, T

# ======================================================================= S3
def s3():
    T = "Mi primera cita con el psicólogo:"
    F, C, D, P = "s3_amiga_a", "s3_coral_a", "s3_dr_a", "s3_celeste_a"
    exp_ = stamp("Expectativa", "transparent", "#E9D3B4", True)
    real = stamp("Realidad", CORAL, DEEP)
    items = [
        Line("amiga", F, (0.0, 2.95), "¿Y qué te imaginas que va a pasar en tu primera cita?", "sala", {"amiga": "feliz", "coral": "neutral"}),
        Line("coral", C, (0.0, 2.65), "Pues… lo de las películas.", "sala", {"coral": "lado", "amiga": "neutral"}, gap=0.1),
        Beat(0.9, "peli", {"coral": "neutral", "dr": "neutral"}, overlay=exp_),
        Line("dr", D, (0.0, 2.60), "Hábleme… de su madre.", "peli", {"dr": "neutral", "coral": "susto"}, overlay=lambda lt: exp_(9)),
        Line("coral", C, (2.70, 4.55), "¿Así, sin saludar?", "peli", {"coral": "susto", "dr": "neutral"}, overlay=lambda lt: exp_(9), gap=0.4),
        Beat(0.8, "real", {"coral": "neutral", "celeste": "feliz"}, overlay=real),
        Line("celeste", P, (0.0, 7.40), "¡Hola! Bienvenida. Cuéntame qué te trae por aquí, a tu ritmo. Lo que no quieras contar, no lo cuentas.", "real",
             {"celeste": "feliz", "coral": "neutral"}, overlay=lambda lt: real(9)),
        Line("coral", C, (4.70, 6.90), "Ah, pues así sí.", "real", {"coral": "feliz", "celeste": "feliz"}, overlay=lambda lt: real(9), gap=0.5),
        Card(3.0, card("deep", "No somos el psicólogo de las pelis.", "la primera sesión es para conocernos")),
        Card(2.6, endcard)]
    shots = {"sala": {"bg": "sala", "chars": {"coral": dict(x=300, y=1120, scale=1.55), "amiga": dict(x=760, y=1120, scale=1.55, flip=True)}},
             "peli": {"bg": "pelicula", "chars": {"coral": dict(x=330, y=1050, scale=1.3, rot=-72), "dr": dict(x=790, y=1165, scale=1.6, flip=True)}},
             "real": {"bg": "consultorio", "chars": {"coral": dict(x=280, y=1165, scale=1.55), "celeste": dict(x=780, y=1165, scale=1.6, flip=True)}}}
    return items, shots, T

# ======================================================================= S4
def s4():
    T = "Black Friday después de un día pesado:"
    C, B, P = "s4_coral_b", "s4_cerebro_a", "s4_celeste_a"
    phone = (f'<div class="abs" style="left:470px;top:860px;width:120px;height:210px;border-radius:22px;background:#1f2d36;border:6px solid #fff;transform:rotate(12deg)">'
             f'<div style="margin:12px;height:150px;border-radius:12px;background:linear-gradient(160deg,{CORAL},#F4B266)"></div></div>')
    def notis(lt, static=False):
        h = phone
        for k in range(3):
            t0 = 0.1 + k * 0.45
            op = 1 if static else min(1, max(0, (lt - t0) / 0.2))
            sc = 1 if static else 0.8 + 0.2 * op
            h += (f'<div class="abs" style="left:520px;top:{430 + k*110}px;opacity:{op:.2f};transform:scale({sc:.2f})">'
                  f'<span style="background:#fff;color:{DEEP};font:700 40px P;padding:16px 26px;border-radius:20px;box-shadow:0 10px 24px rgba(0,0,0,.25);white-space:nowrap">'
                  f'<span style="color:{CORAL}">●</span> Agregado al carrito</span></div>')
        return h
    items = [
        Line("coral", C, (0.0, 3.55), "Qué día tan horrible. Me merezco algo.", "sofa", {"coral": "triste"}, overlay=lambda lt: phone, gap=0.1),
        Beat(1.7, "sofa", {"coral": "loco"}, overlay=notis),
        Line("cerebro", B, (0.0, 3.40), "¿Eso lo necesitas… o lo estás sintiendo?", "sofa", {"cerebro": "lado", "coral": "susto"}, overlay=lambda lt: notis(0, True)),
        Line("coral", C, (3.75, 6.95), "Lo necesito. Bueno… no sé.", "sofa", {"coral": "pena", "cerebro": "neutral"}, overlay=lambda lt: notis(0, True), gap=0.3),
        Line("celeste", P, (0.0, 7.50), "Antes de pagar, respira y espera diez minutos. Si lo que buscas es calma, eso no llega en una caja.", "consejo", {"celeste": "feliz"}, gap=0.3),
        Line("coral", C, (7.15, 9.60), "¿Y si lo dejo en el carrito para siempre?", "sofa", {"coral": "feliz", "cerebro": "feliz"}, overlay=lambda lt: phone),
        Line("cerebro", B, (3.50, 5.44), "¡Inversión del año!", "sofa", {"cerebro": "feliz", "coral": "feliz"}, poses={"cerebro": "arriba"}, overlay=lambda lt: phone, gap=0.5),
        Card(3.4, card("deep", "Comprar para tapar lo que sientes no tiene devolución.", "si te pasa seguido, hablemos")),
        Card(2.6, endcard)]
    st = starts(items)
    shots = {"sofa": {"bg": "sala_noche", "chars": {"coral": dict(x=330, y=1120, scale=1.55),
                                                    "cerebro": dict(x=800, y=1000, scale=1.1, flip=True, enter=st[2])}},
             "consejo": {"bg": "consejo", "chars": {"celeste": dict(x=640, y=1160, scale=1.7, flip=True)}}}
    return items, shots, T

SKITS = {"TK01_preguntale_dos_veces": s1, "TK02_cerebro_3am": s2, "TK03_primera_cita": s3, "TK04_black_friday": s4}

if __name__ == "__main__":
    mode = sys.argv[1]; ids = sys.argv[2:] or list(SKITS)
    for v in ids:
        items, shots, T = SKITS[v]()
        if mode == "preview":
            st = starts(items); pts = [s + it.dur * 0.6 for s, it in zip(st, items)]
            outs, tot = render_skit(v, items, shots, T, "/home/claude/tiktok/prev", preview=pts)
            print(v, round(tot, 1), "s")
        else:
            print(render_skit(v, items, shots, T, "/home/claude/tiktok/out"), flush=True)
