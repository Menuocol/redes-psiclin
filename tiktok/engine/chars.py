# -*- coding: utf-8 -*-
"""Personajes de Psiclín: las dos comas del isotipo convertidas en muñequitos."""
CREAM = "#F5E6C8"; DEEP = "#3D5A6C"; CORAL = "#FF8C7A"; SKY = "#7EC8E3"

BODY = ("M100,12 C158,12 192,54 192,110 C192,166 152,206 104,220 C122,234 146,244 170,248 "
        "C114,258 56,242 30,200 C14,174 8,142 8,110 C8,54 44,12 100,12 Z")

def face(expr="neutral", mouth=0.0):
    # ojos
    ey = 98
    if expr == "cerrados":
        eyes = (f'<path d="M62,{ey} q14,10 28,0" stroke="{DEEP}" stroke-width="6" fill="none" stroke-linecap="round"/>'
                f'<path d="M112,{ey} q14,10 28,0" stroke="{DEEP}" stroke-width="6" fill="none" stroke-linecap="round"/>')
    else:
        big = 1.25 if expr in ("susto", "loco") else 1
        px = {"neutral": 0, "susto": 0, "triste": 0, "feliz": 0, "loco": 4, "lado": 6, "pena": -5}.get(expr, 0)
        py = {"triste": 4, "pena": 5}.get(expr, 0)
        eyes = ""
        for cx in (76, 126):
            eyes += (f'<ellipse cx="{cx}" cy="{ey}" rx="{17*big}" ry="{21*big}" fill="#fff"/>'
                     f'<circle cx="{cx+px}" cy="{ey+3+py}" r="{9 if expr!="loco" else 6}" fill="{DEEP}"/>'
                     f'<circle cx="{cx+px+3}" cy="{ey-1+py}" r="3" fill="#fff"/>')
    # cejas
    br = {"neutral": ("M60,68 q16,-8 32,0", "M110,68 q16,-8 32,0"),
          "triste": ("M60,70 q16,-2 32,-10", "M110,60 q16,-2 32,10"),
          "pena": ("M60,72 q16,-2 32,-12", "M110,60 q16,-2 32,12"),
          "susto": ("M60,56 q16,-12 32,-4", "M110,52 q16,-8 32,4"),
          "loco": ("M58,58 q16,-14 34,2", "M110,64 q16,6 34,-8"),
          "feliz": ("M60,64 q16,-10 32,0", "M110,64 q16,-10 32,0"),
          "cerrados": ("M60,70 q16,-6 32,0", "M110,70 q16,-6 32,0"),
          "lado": ("M60,66 q16,-6 32,2", "M110,62 q16,-8 32,0")}[expr]
    brows = "".join(f'<path d="{d}" stroke="{DEEP}" stroke-width="7" fill="none" stroke-linecap="round"/>' for d in br)
    # boca: mouth 0..1 abre al hablar
    my = 146
    if expr in ("feliz",) and mouth < .15:
        m = f'<path d="M80,{my} q21,22 42,0" stroke="{DEEP}" stroke-width="6" fill="none" stroke-linecap="round"/>'
    elif expr in ("triste", "pena") and mouth < .15:
        m = f'<path d="M82,{my+10} q19,-14 38,0" stroke="{DEEP}" stroke-width="6" fill="none" stroke-linecap="round"/>'
    elif expr == "susto" and mouth < .15:
        m = f'<ellipse cx="101" cy="{my+4}" rx="12" ry="16" fill="{DEEP}"/>'
    elif mouth < .15:
        m = f'<path d="M86,{my} q15,8 30,0" stroke="{DEEP}" stroke-width="6" fill="none" stroke-linecap="round"/>'
    else:
        h = 8 + 26 * mouth
        m = (f'<path d="M80,{my-4} q21,{h*2} 42,0 z" fill="{DEEP}"/>'
             f'<path d="M90,{my-4+h*0.9} q11,{h*0.45} 22,0" fill="#FF6F6F" opacity=".9"/>')
    # cachetes
    cheeks = (f'<ellipse cx="54" cy="128" rx="13" ry="8" fill="#ff5f5f" opacity=".22"/>'
              f'<ellipse cx="148" cy="128" rx="13" ry="8" fill="#ff5f5f" opacity=".22"/>')
    return eyes + brows + m + cheeks

ACC = {
    "gafas": f'<g stroke="{DEEP}" stroke-width="5" fill="none"><circle cx="76" cy="98" r="27"/><circle cx="126" cy="98" r="27"/><path d="M103,98 h-0"/><path d="M98,96 q3,-4 6,0"/></g>',
    "corbata": f'<path d="M100,176 l-14,10 14,40 14,-40 z" fill="{DEEP}"/>',
    "monho": f'<circle cx="100" cy="2" r="26" fill="#7a5a48"/><path d="M40,40 q60,-50 120,0" stroke="#7a5a48" stroke-width="22" fill="none" stroke-linecap="round"/>',
    "gorra": f'<path d="M30,52 q70,-70 140,0 z" fill="{DEEP}"/><rect x="130" y="44" width="70" height="14" rx="7" fill="{DEEP}"/>',
    "pijama": '<g opacity=".35"><circle cx="70" cy="190" r="6" fill="#fff"/><circle cx="110" cy="205" r="6" fill="#fff"/><circle cx="140" cy="180" r="6" fill="#fff"/></g>',
    "barba": '<path d="M44,128 q56,90 112,0 q-10,30 -56,34 q-46,-4 -56,-34z" fill="#6b4a3a"/>',
    "": "",
}

def arms(pose="abajo", col=DEEP):
    P = {"abajo": ("M22,150 q-26,30 -14,58", "M178,150 q26,30 14,58"),
         "arriba": ("M20,130 q-40,-30 -30,-80", "M180,130 q40,-30 30,-80"),
         "habla": ("M22,150 q-26,30 -14,58", "M178,140 q44,-6 52,-44"),
         "cara": ("M24,150 q-20,-10 20,-30", "M176,150 q20,-10 -20,-30"),
         "cruzados": ("M30,170 q70,30 140,-10", "M170,170 q-70,30 -140,-10")}[pose]
    return "".join(f'<path d="{d}" stroke="{col}" stroke-width="9" fill="none" stroke-linecap="round"/>' for d in P)

def char(color, x, y, scale=1.0, expr="neutral", mouth=0.0, acc="", pose="abajo", flip=False, rot=0, bob=0.0, name=None):
    """Devuelve un <svg> posicionado. (x,y)=centro inferior. bob=desplazamiento vertical."""
    w, h = 260 * scale, 290 * scale
    tr = f"scale(-1,1) translate(-200,0)" if flip else ""
    label = (f'<div style="position:absolute;left:50%;top:{h+6}px;transform:translateX(-50%);white-space:nowrap;'
             f'font:700 {int(30*scale)}px P;color:{DEEP};background:#fff;padding:4px 16px;border-radius:999px">{name}</div>') if name else ""
    return (f'<div style="position:absolute;left:{x - w/2}px;top:{y - h + bob}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);transform-origin:50% 100%">'
            f'<svg viewBox="-30 -30 260 290" width="{w}" height="{h}"><g transform="{tr}">'
            f'<ellipse cx="100" cy="252" rx="80" ry="10" fill="#000" opacity=".12"/>'
            f'{arms(pose)}<path d="{BODY}" fill="{color}"/>'
            f'<path d="M40,60 q30,-36 70,-36" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round" opacity=".35"/>'
            f'{"" if acc=="gafas" else ACC.get(acc,"")}{face(expr, mouth)}{ACC["gafas"] if acc=="gafas" else ""}</g></svg>{label}</div>')
