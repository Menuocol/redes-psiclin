# -*- coding: utf-8 -*-
import os, sys, json, html
sys.path.insert(0, os.path.dirname(__file__))
from content import POSTS
from stories import plan
SRC=os.path.dirname(os.path.abspath(__file__)); F=f"file://{SRC}/fonts"; I=f"file://{SRC}/img"
CREAM="#F5E6C8"; DEEP="#3D5A6C"; CORAL="#FF8C7A"; SKY="#7EC8E3"; SURF="#FFFCF6"
CAMP={"anx":dict(p="#7C3AED",s="#E8FF4D",on="#FFFFFF",ink="#7C3AED"),"burn":dict(p="#E85D04",s=CREAM,on="#FFFFFF",ink="#E85D04")}
SH="0 24px 60px rgba(120,80,30,.22)"
ICON={"luna":'<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',"nube":'<path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/>',
"viento":'<path d="M12.8 19.6A2 2 0 1 0 14 16H2"/><path d="M17.5 8a2.5 2.5 0 1 1 2 4H2"/><path d="M9.8 4.4A2 2 0 1 1 11 8H2"/>',
"corazon":'<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
"libro":'<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/>',
"sol":'<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M6.3 17.7l-1.4 1.4M19.1 4.9l-1.4 1.4"/>',
"escudo":'<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
"juego":'<rect x="2" y="6" width="20" height="12" rx="4"/><path d="M6 12h4M8 10v4M15 11h.01M18 13h.01"/>',
"estrella":'<path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>',
"check":'<path d="M20 6 9 17l-5-5"/>',"alerta":'<path d="M12 9v4M12 17h.01"/><circle cx="12" cy="12" r="10"/>',
"bookmark":'<path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"/>'}
def icon(k,s,c,w=2): return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{ICON[k]}</svg>'
def e(t): return t  # textos ya vienen limpios (pueden incluir <br>)
CSS=f"""
@font-face{{font-family:P;src:url({F}/poppins-400.woff2);font-weight:400}}
@font-face{{font-family:P;src:url({F}/poppins-500.woff2);font-weight:500}}
@font-face{{font-family:P;src:url({F}/poppins-600.woff2);font-weight:600}}
@font-face{{font-family:P;src:url({F}/poppins-700.woff2);font-weight:700}}
@font-face{{font-family:P;src:url({F}/poppins-800.woff2);font-weight:800}}
@font-face{{font-family:C;src:url({F}/caveat.woff2);font-weight:400 700}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:WPX;height:HPX;overflow:hidden;font-family:P,sans-serif;color:{DEEP}}}
.f{{position:relative;width:WPX;height:HPX;overflow:hidden}}
.h{{font-weight:800;text-transform:uppercase;line-height:1.04;letter-spacing:-.01em}}
.c{{font-family:C,cursive;font-weight:700}}
.abs{{position:absolute}}
.iso{{position:absolute;right:64px;bottom:56px;width:112px}}
.grain::after{{content:"";position:absolute;inset:0;pointer-events:none;opacity:.06;background-image:radial-gradient(rgba(60,40,20,.9) 1px,transparent 1.2px);background-size:6px 6px}}
.pattern{{background-color:{CREAM};background-image:radial-gradient(circle at 12% 18%,rgba(255,140,122,.30) 0 90px,transparent 91px),radial-gradient(circle at 92% 26%,rgba(126,200,227,.32) 0 130px,transparent 131px),radial-gradient(circle at 78% 92%,rgba(255,140,122,.22) 0 70px,transparent 71px),radial-gradient(circle at 6% 88%,rgba(126,200,227,.28) 0 54px,transparent 55px)}}
"""
def page(body,w,h):
    body=body.replace(" %","\u00a0%")
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS.replace("WPX",str(w)+"px").replace("HPX",str(h)+"px")}</style></head><body><div class="f grain" style="width:{w}px;height:{h}px">{body}</div></body></html>'
ISO=f'<img class="iso" src="{I}/isotipo.png">'
def isoimg(w=112,r=64,b=56,extra=""): return f'<img src="{I}/isotipo.png" style="position:absolute;right:{r}px;bottom:{b}px;width:{w}px;{extra}">'
def note(t,col,x,y,rot=-4,fs=66,bg=None):
    pad="padding:0 26px;border-radius:999px;" if bg else ""
    return f'<span class="c abs" style="left:{x}px;top:{y}px;font-size:{fs}px;color:{col};transform:rotate({rot}deg);{pad}{"background:"+bg+";" if bg else ""}">{t}</span>'
def under(x,y,w,col=CORAL): return f'<svg class="abs" style="left:{x}px;top:{y}px" width="{w}" height="30" viewBox="0 0 {w} 30"><path d="M4 20 C {w*.3} 6, {w*.6} 28, {w-6} 10" stroke="{col}" stroke-width="7" fill="none" stroke-linecap="round"/></svg>'
def blob(x,y,s,col,op=.35): return f'<div class="abs" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;border-radius:50%;background:{col};opacity:{op}"></div>'
def hs(text,base,avail=900):  # tamaño por longitud y por la palabra más larga
    t=text.replace("<br>"," "); n=len(t)
    f=base if n<26 else int(base*0.86) if n<40 else int(base*0.74) if n<56 else int(base*0.64) if n<72 else int(base*0.56)
    lw=max(len(w) for w in t.split()); return min(f,int(avail/(lw*0.80)))

# ---------- POST TEMPLATES 1080x1350 ----------
def weather_card(s,camp,scale=1):
    rows="".join(f'<div style="display:flex;align-items:center;gap:26px;padding:30px 0;border-top:2px solid rgba(255,255,255,.35)">{icon(k,60,"#fff")}<span style="flex:1;font-size:42px;font-weight:500;color:#fff;line-height:1.2">{t}</span><span style="font-size:42px;font-weight:800;color:#fff;text-align:right;max-width:320px;line-height:1.1">{v}</span></div>' for k,t,v in s["rows"])
    return f'''<div style="background:linear-gradient(180deg,#86CDE6 0%,#5BA4CF 100%);border-radius:56px;padding:52px 56px 40px;box-shadow:{SH}">
<div style="display:flex;justify-content:space-between;align-items:flex-start"><div><div style="font-size:36px;font-weight:500;color:#fff">Medellín · {s["semana"]}</div>
<div class="h" style="font-size:{hs(s["temp"],120,700)}px;color:#fff;margin-top:6px">{s["temp"]}</div></div>{icon("nube",150,"#fff",1.6)}</div>
<div style="font-size:34px;font-weight:700;color:#fff;text-transform:uppercase;letter-spacing:.05em;margin:24px 0 18px">{s["title"]}</div>{rows}</div>'''
def T_weather(s,c):
    return f'{blob(-120,-140,420,CORAL,.25)}<div class="abs" style="left:64px;right:64px;top:0;bottom:150px;display:flex;align-items:center"><div style="width:100%">{weather_card(s,c)}</div></div>{note("desliza →",CORAL,90,1215,-3,64)}{ISO}'
def T_weather_tip(s,c):
    return f'''{blob(760,-160,520,SKY,.35)}<div class="abs" style="left:80px;right:80px;top:300px;background:{SURF};border-radius:56px;padding:76px 70px 90px;box-shadow:{SH}">
<div style="display:flex;align-items:center;gap:22px">{icon("sol",80,CORAL)}<span class="c" style="font-size:70px;color:{CORAL};white-space:nowrap">{s["head"]}</span></div>
<div style="font-size:66px;font-weight:700;line-height:1.2;margin-top:34px">{s["tip"]}</div></div>{note(s["note"],DEEP,110,1150,-4,72,SKY)}{ISO}'''
def T_weather_close(s,c):
    return f'''<div class="abs" style="inset:0;background:{SKY}"></div>
<div class="h abs" style="left:90px;right:90px;top:200px;font-size:112px">{s["q"]}</div>
<div class="abs" style="left:90px;right:90px;top:640px;background:#fff;border-radius:48px;padding:46px 56px;box-shadow:{SH}">
<div style="display:flex;justify-content:space-between">{icon("sol",80,"#E85D04")}{icon("nube",80,DEEP)}{icon("viento",80,DEEP)}</div>
<div style="margin-top:38px;height:22px;border-radius:11px;background:linear-gradient(90deg,{CORAL},{SKY},{DEEP})"></div>
<div style="width:62px;height:62px;border-radius:50%;background:#fff;border:8px solid {DEEP};margin:-42px 0 0 380px"></div></div>
<div class="abs" style="left:90px;right:200px;top:980px;font-size:46px;font-weight:600;line-height:1.35">{s["sub"]}</div>{note(s["note"],"#fff",90,1200,-3,70)}{isoimg()}'''
def T_crema(s,c):
    return f'''{blob(700,-200,560,CORAL,.22)}{blob(-160,1050,360,SKY,.3)}
<div class="h abs" style="left:90px;right:120px;top:300px;font-size:{hs(s["head"],132)}px">{s["head"]}</div>
<div class="abs" style="left:90px;right:180px;top:830px;font-size:46px;font-weight:500;line-height:1.35">{s["sub"]}</div>
{note(s["note"],CORAL,90,1110,-4,82)}{under(96,1210,330)}{ISO}'''
def T_crema_list(s,c):
    items="".join(f'<div style="display:flex;align-items:center;gap:30px;margin:22px 0">'+(f'<div style="width:70px;height:70px;border:6px solid {DEEP};border-radius:16px;display:flex;align-items:center;justify-content:center">{icon("check",52,DEEP,3)}</div>' if i<len(s["items"])-1 else f'<div style="width:70px;height:70px;border:6px solid {CORAL};border-radius:16px"></div>')+f'<span class="c" style="font-size:96px;color:{DEEP if i<len(s["items"])-1 else CORAL}">{t}</span></div>' for i,t in enumerate(s["items"]))
    return f'''{blob(760,-180,520,SKY,.3)}<div class="h abs" style="left:90px;right:90px;top:120px;font-size:{hs(s["head"],118)}px">{s["head"]}</div>
<div class="abs" style="left:110px;top:560px;transform:rotate(-2deg);background:{SURF};border-radius:36px;padding:30px 90px 26px 56px;box-shadow:{SH}">{items}</div>
<span class="c abs" style="left:700px;top:820px;width:300px;font-size:72px;line-height:1;color:{CORAL};transform:rotate(-6deg)">{s["note"]}</span>{ISO}'''
def T_camp_hook(s,c):
    k=CAMP[c]; return f'<div class="abs" style="inset:0;background:{k["p"]}"></div><div class="h abs" style="left:90px;right:90px;top:330px;font-size:{hs(s["hook"],150)}px;color:{k["s"]}">{s["hook"]}</div>{note(s["note"]+" →","#fff",90,1150,-3,70)}{isoimg()}'
def T_camp_list(s,c):
    k=CAMP[c]; it="".join(f'<div style="display:flex;gap:34px;align-items:flex-start;margin-bottom:52px"><div style="flex:none;width:34px;height:34px;border-radius:50%;background:{k["s"]};margin-top:22px"></div><span style="font-size:60px;font-weight:700;line-height:1.18;color:{k["on"]}">{t}</span></div>' for t in s["items"])
    return f'<div class="abs" style="inset:0;background:{k["p"]}"></div><div class="abs" style="left:90px;right:110px;top:230px">{it}</div>{isoimg()}'
def T_camp_close(s,c):
    k=CAMP[c]; return f'''<div class="abs" style="inset:0;background:{k["s"]}"></div>{blob(760,-180,520,"#fff",.35)}
<div class="h abs" style="left:90px;right:90px;top:300px;font-size:{hs(s["line"],124)}px;color:{k["ink"]}">{s["line"]}</div>
{note(s["note"],k["ink"],96,760,-4,72)}<div class="abs" style="left:90px;top:900px;background:{k["p"]};color:{k["s"] if c=="anx" else "#fff"};font-size:40px;font-weight:700;padding:30px 54px;border-radius:999px">{s["cta"]}</div>{isoimg()}'''
def T_camp_number(s,c):
    k=CAMP[c]; return f'<div class="abs" style="inset:0;background:{k["p"]}"></div><div class="h abs" style="left:60px;top:40px;font-size:760px;line-height:1;color:{k["s"]}">{s["num"]}</div><div class="h abs" style="left:90px;right:90px;top:900px;font-size:84px;color:#fff">{s["text"]}</div>{isoimg()}'
def T_camp_steps(s,c):
    k=CAMP[c]; st="".join(f'<div style="display:flex;gap:40px;align-items:center;margin-bottom:56px"><div class="h" style="flex:none;width:130px;height:130px;border-radius:50%;background:{k["s"]};color:{k["p"]};font-size:76px;display:flex;align-items:center;justify-content:center">{i+1}</div><span style="font-size:56px;font-weight:700;color:#fff;line-height:1.2">{t}</span></div>' for i,t in enumerate(s["steps"]))
    return f'<div class="abs" style="inset:0;background:{k["p"]}"></div><div class="h abs" style="left:90px;top:190px;font-size:110px;color:{k["s"]}">{s["title"]}</div><div class="abs" style="left:90px;right:90px;top:430px">{st}</div>{isoimg()}'
def T_photo_hook(s,c):
    return f'''<img class="abs" src="{I}/{s["img"]}.jpg" style="inset:0;width:100%;height:100%;object-fit:cover">
<div class="abs" style="inset:0;background:linear-gradient(180deg,rgba(61,90,108,.15) 0%,rgba(61,90,108,0) 30%,rgba(61,90,108,.55) 100%)"></div>
<span class="abs" style="left:70px;top:70px;background:{SURF};font-size:30px;font-weight:700;padding:14px 30px;border-radius:999px;text-transform:uppercase;letter-spacing:.04em">{s["tag"]}</span>
{note(s["note"],DEEP,74,170,-4,66,SKY)}
<div class="abs" style="left:56px;right:56px;bottom:200px;transform:rotate(-1.5deg);background:{SURF};border-radius:52px;padding:52px 60px;box-shadow:{SH}"><div class="h" style="font-size:{hs(s["head"],96)}px">{s["head"]}</div></div>{isoimg()}'''
def T_strike_list(s,c):
    it="".join(f'<div style="margin-bottom:60px;font-size:60px;font-weight:600;line-height:1.3;color:#7A8C97;text-decoration:line-through;text-decoration-color:{CORAL};text-decoration-thickness:4px">{t}</div>' for t in s["items"])
    return f'<div class="abs" style="inset:0;background:{SURF}"></div>{blob(-160,-160,440,SKY,.28)}<div class="h abs" style="left:90px;right:90px;top:170px;font-size:{hs(s["title"],92)}px">{s["title"]}</div><div class="abs" style="left:96px;right:110px;top:420px;bottom:230px;display:flex;flex-direction:column;justify-content:center">{it}</div>{note(s["note"],CORAL,640,1150,-6,86)}{ISO}'
def T_check_list(s,c):
    ic="alerta" if s.get("warn") else "check"; col="#E85D04" if s.get("warn") else CORAL
    it="".join(f'<div style="display:flex;gap:34px;align-items:flex-start;margin-bottom:48px"><div style="flex:none;width:86px;height:86px;border-radius:26px;background:{SURF};display:flex;align-items:center;justify-content:center;box-shadow:0 8px 20px rgba(120,80,30,.14)">{icon(ic,56,col,3)}</div><span style="font-size:58px;font-weight:600;line-height:1.25;padding-top:4px">{t}</span></div>' for t in s["items"])
    return f'<div class="abs" style="inset:0;background:{CREAM}"></div>{blob(800,-160,460,CORAL,.22)}<div class="h abs" style="left:90px;right:120px;top:160px;font-size:{hs(s["title"],92)}px">{s["title"]}</div><div class="abs" style="left:90px;right:90px;top:420px;bottom:220px;display:flex;flex-direction:column;justify-content:center">{it}</div>{note(s["note"],CORAL,90,1165,-4,74)}{ISO}'
def T_icons(s,c):
    it="".join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:18px"><div style="width:190px;height:190px;border-radius:60px;background:{SURF};display:flex;align-items:center;justify-content:center;box-shadow:{SH}">{icon(k,96,CORAL)}</div><span style="font-size:34px;font-weight:600">{l}</span></div>' for k,l in s["items"])
    return f'<div class="abs" style="inset:0;background:{SKY}"></div>{blob(-140,1000,420,"#fff",.25)}<div class="h abs" style="left:90px;right:90px;top:130px;font-size:{hs(s["head"],112)}px">{s["head"]}</div><div class="abs" style="left:90px;right:120px;top:560px;font-size:42px;font-weight:500;line-height:1.3">{s["sub"]}</div><div class="abs" style="left:90px;right:90px;top:760px;display:flex;justify-content:space-between">{it}</div>{note(s["note"],DEEP,90,1150,-3,64,SURF)}{isoimg()}'
def T_question(s,c):
    return f'<div class="abs" style="inset:0;background:{CREAM}"></div>{blob(760,-140,460,SKY,.3)}{blob(-120,1080,340,CORAL,.22)}<div class="h abs" style="left:80px;top:90px;font-size:300px;color:{CORAL}">{s["n"]}</div><div class="abs" style="left:80px;right:80px;top:470px;background:{SURF};border-radius:52px;padding:70px 64px;box-shadow:{SH}"><div class="h" style="font-size:{hs(s["q"],104,860)}px">{s["q"]}</div><div style="font-size:48px;font-weight:500;line-height:1.35;margin-top:34px">{s["sub"]}</div></div>{ISO}'
def T_summary(s,c):
    it="".join(f'<div style="display:flex;gap:30px;align-items:center;margin-bottom:34px"><div class="h" style="flex:none;width:84px;height:84px;border-radius:50%;background:{CORAL};font-size:46px;display:flex;align-items:center;justify-content:center">{i+1}</div><span style="font-size:56px;font-weight:600;line-height:1.2">{t}</span></div>' for i,t in enumerate(s["items"]))
    return f'<div class="abs" style="inset:0;background:{CREAM}"></div><div class="abs" style="left:90px;top:140px;display:flex;gap:24px;align-items:center">{icon("bookmark",96,CORAL)}<span class="h" style="font-size:{hs(s["title"],96,780)}px">{s["title"]}</span></div><div class="abs" style="left:90px;right:90px;top:420px;background:{SURF};border-radius:52px;padding:64px 60px 40px;box-shadow:{SH}">{it}</div><div class="abs" style="left:90px;right:220px;top:1060px;font-size:50px;font-weight:700;line-height:1.3">{s["sub"]}</div>{ISO}'
def T_cta_end(s,c):
    return f'<div class="abs" style="inset:0;background:{CORAL}"></div>{blob(760,-200,560,"#fff",.18)}<div class="h abs" style="left:90px;right:90px;top:250px;font-size:{hs(s["head"],120)}px">{s["head"]}</div><div class="abs" style="left:90px;right:140px;top:760px;font-size:46px;font-weight:500;line-height:1.35">{s["sub"]}</div><div class="abs" style="left:90px;top:1000px;background:{DEEP};color:{CREAM};font-size:40px;font-weight:700;padding:30px 54px;border-radius:999px">{s["cta"]}</div>{isoimg()}'
def T_coral_tag(s,c):
    tag=f'<svg class="abs" style="left:640px;top:120px;transform:rotate(14deg)" width="330" height="200" viewBox="0 0 330 200"><path d="M70 10 H310 a10 10 0 0 1 10 10 V180 a10 10 0 0 1 -10 10 H70 L10 100 Z" fill="{SURF}" stroke="{DEEP}" stroke-width="6" stroke-linejoin="round"/><circle cx="62" cy="100" r="14" fill="{CORAL}" stroke="{DEEP}" stroke-width="5"/><text x="195" y="125" text-anchor="middle" font-family="P" font-weight="800" font-size="72" fill="{DEEP}">{s["tag"]}</text></svg>'
    return f'<div class="abs" style="inset:0;background:{CORAL}"></div>{tag}<div class="h abs" style="left:90px;right:90px;top:400px;font-size:{hs(s["head"],140)}px">{s["head"]}</div>{note(s["note"],SURF,90,1150,-4,84)}{isoimg()}'
def T_coral_plain(s,c):
    return f'<div class="abs" style="inset:0;background:{CORAL}"></div>{blob(720,-220,600,"#fff",.18)}{blob(-180,1060,380,SKY,.35)}<div class="h abs" style="left:90px;right:90px;top:300px;font-size:{hs(s["head"],132)}px">{s["head"]}</div>{note(s["note"],SURF,90,1000,-3,76)}{isoimg()}'
def T_mito(s,c):
    return f'<div class="abs" style="inset:0;background:{SURF}"></div>{blob(780,-180,480,SKY,.3)}<span class="c abs" style="left:90px;top:220px;font-size:130px;color:{CORAL}">mito</span><div class="abs" style="left:90px;right:90px;top:430px"><div class="h" style="font-size:{hs(s["text"],120)}px;position:relative">{s["text"]}<svg style="position:absolute;left:-20px;top:30%;transform:rotate(-8deg)" width="105%" height="60" viewBox="0 0 100 60" preserveAspectRatio="none"><path d="M0 40 C 25 20, 60 50, 100 18" stroke="{CORAL}" stroke-width="10" fill="none" vector-effect="non-scaling-stroke" stroke-linecap="round"/></svg></div></div>{note(s["note"]+" →",DEEP,90,1150,-3,66)}{ISO}'
def T_realidad(s,c):
    return f'<div class="abs" style="inset:0;background:{CORAL}"></div>{blob(-160,-160,460,"#fff",.2)}<span class="c abs" style="left:90px;top:220px;font-size:130px;color:{SURF}">realidad</span><div class="h abs" style="left:90px;right:90px;top:430px;font-size:{hs(s["text"],120)}px">{s["text"]}</div><div class="abs" style="left:90px;right:140px;top:960px;font-size:46px;font-weight:600;line-height:1.35">{s["sub"]}</div>{isoimg()}'
def T_quote_dark(s,c):
    return f'<div class="abs" style="inset:0;background:{DEEP}"></div>{blob(820,1040,420,SKY,.15)}<span class="h abs" style="left:70px;top:40px;font-size:420px;color:{CORAL};line-height:1">“</span><div class="h abs" style="left:90px;right:90px;top:400px;font-size:{hs(s["quote"],116)}px;color:{CREAM}">{s["quote"]}</div>{note(s["sign"],SKY,90,1100,-2,64)}{isoimg()}'
def T_lines(s,c):
    ln="".join(f'<div style="background:{SURF};border-radius:36px;padding:26px 44px;margin-bottom:22px"><div style="font-size:60px;font-weight:800">{a}</div><div style="font-size:32px;font-weight:500;margin-top:4px">{b}</div></div>' for a,b in s["lines"])
    return f'<div class="abs" style="inset:0;background:{DEEP}"></div><div class="h abs" style="left:90px;right:90px;top:110px;font-size:76px;color:{CREAM}">{s["title"]}</div><div class="abs" style="left:90px;right:90px;top:470px">{ln}</div><div class="abs" style="left:90px;right:220px;top:1120px;font-size:38px;font-weight:500;line-height:1.35;color:{CREAM}">{s["sub"]}</div>{isoimg()}'
def T_iso_big(s,c):
    return f'<div class="abs" style="inset:0;background:{CREAM}"></div>{blob(-200,-200,520,SKY,.25)}{blob(780,1040,460,CORAL,.2)}<img class="abs" src="{I}/isotipo.png" style="left:290px;top:200px;width:500px"><div class="h abs" style="left:90px;right:90px;top:640px;font-size:{hs(s["head"],104)}px;text-align:center">{s["head"]}</div>{note(s["note"],CORAL,330,1070,-4,96)}'
def T_pattern_hook(s,c):
    return f'<div class="abs pattern" style="inset:0"></div><div class="h abs" style="left:90px;right:90px;top:300px;font-size:{hs(s["head"],136)}px">{s["head"]}</div><div class="abs" style="left:90px;right:200px;top:800px;font-size:50px;font-weight:600;line-height:1.3">{s["sub"]}</div>{note(s["note"]+" →",CORAL,90,1130,-3,70)}{ISO}'
POST_T={k[2:]:v for k,v in globals().items() if k.startswith("T_")}

# ---------- STORIES 1080x1920 ----------
def S_bg(c,kind):
    k=CAMP[c]; return {"camp":k["p"],"alt":k["s"]}.get(kind,kind)
def ST(st,c):
    k=CAMP[c]; t=st["t"]; iso=isoimg(120,70,120)
    if t=="st_slider":
        return f'<div class="abs" style="inset:0;background:{k["p"]}"></div><span class="c abs" style="left:90px;top:300px;font-size:74px;color:#fff">{st["note"]}</span><div class="h abs" style="left:90px;right:90px;top:420px;font-size:118px;color:{k["s"]}">{st["head"]}</div>{iso}'
    if t=="st_photo":
        return f'<img class="abs" src="{I}/{st["img"]}.jpg" style="inset:0;width:100%;height:100%;object-fit:cover"><div class="abs" style="left:70px;right:70px;top:300px;background:{SURF};border-radius:52px;padding:50px 56px;box-shadow:{SH}"><div class="h" style="font-size:84px">{st["head"]}</div></div>{note(st["note"],DEEP,90,250,-4,64,SKY)}{iso}'
    if t=="st_eto":
        return f'<div class="abs" style="inset:0;background:{CREAM}"></div>{blob(700,-120,520,SKY,.35)}<span class="c abs" style="left:90px;top:300px;font-size:74px;color:{CORAL}">esto o aquello</span><div class="h abs" style="left:90px;right:90px;top:420px;font-size:112px">{st["a"]}<br><span style="color:{CORAL}">{st["b"]}</span></div>{iso}'
    if t=="st_camp":
        return f'<div class="abs" style="inset:0;background:{k["p"]}"></div><div class="h abs" style="left:90px;right:90px;top:520px;font-size:{hs(st["head"],150)}px;color:{k["s"]}">{st["head"]}</div>{note(st["note"]+" →","#fff",90,1480,-3,70)}{iso}'
    if t=="st_camp_poll":
        return f'<div class="abs" style="inset:0;background:{k["p"]}"></div><div class="h abs" style="left:90px;right:90px;top:360px;font-size:150px;color:{k["s"]}">{st["head"]}</div>{iso}'
    if t=="st_camp_link":
        return f'<div class="abs" style="inset:0;background:{k["s"]}"></div>{blob(700,-120,520,"#fff",.35)}<div class="h abs" style="left:90px;right:90px;top:420px;font-size:120px;color:{k["ink"]}">{st["head"]}</div>{note("toca el enlace ↓",k["ink"],90,1000,-3,74)}{iso}'
    if t=="st_lines155":
        return f'<div class="abs" style="inset:0;background:{DEEP}"></div><span class="c abs" style="left:90px;top:300px;font-size:64px;color:{SKY}">25 de noviembre</span><div class="h abs" style="left:90px;right:90px;top:400px;font-size:80px;color:{CREAM}">Si vives violencia, no estás sola.</div><div class="abs" style="left:90px;right:90px;top:820px;background:{SURF};border-radius:40px;padding:44px 50px"><div style="font-size:96px;font-weight:800">Línea 155</div><div style="font-size:38px;font-weight:500;margin-top:8px">orientación a mujeres · gratis, 24 horas</div><div style="font-size:38px;font-weight:500;margin-top:24px"><b>123</b> · emergencias</div></div>{iso}'
    if t=="st_box":
        return f'<div class="abs" style="inset:0;background:{CREAM}"></div>{blob(-160,-160,520,CORAL,.25)}<span class="c abs" style="left:90px;top:300px;font-size:74px;color:{CORAL}">pregúntale a la psicóloga</span><div class="h abs" style="left:90px;right:90px;top:420px;font-size:{max(hs(st["head"],140),84)}px">{st["head"]}</div>{iso}'
    if t=="st_poll":
        return f'<div class="abs" style="inset:0;background:{SKY}"></div><span class="c abs" style="left:90px;top:300px;font-size:74px;color:#fff">pregunta del día</span><div class="h abs" style="left:90px;right:90px;top:420px;font-size:{max(hs(st["head"],140),84)}px">{st["head"]}</div>{iso}'
    if t=="st_share":
        return f'<div class="abs" style="inset:0;background:{CORAL}"></div>{blob(720,-160,560,"#fff",.2)}<span class="c abs" style="left:90px;top:300px;font-size:74px;color:{SURF}">día mundial del saludo</span><div class="h abs" style="left:90px;right:90px;top:430px;font-size:140px">{st["head"]}</div>{note(st["note"],SURF,90,1300,-3,72)}{iso}'
    if t=="st_offer":
        return f'<div class="abs" style="inset:0;background:{CORAL}"></div><div class="h abs" style="left:90px;right:90px;top:420px;font-size:126px">{st["head"]}</div>{note("black friday","#fff",90,300,-3,74)}{iso}'
    if t=="st_novena":
        return f'<div class="abs" style="inset:0;background:{CREAM}"></div>{blob(680,-140,560,CORAL,.22)}<span class="c abs" style="left:90px;top:300px;font-size:84px;color:{k["ink"]}">novena · día {st["n"]}</span><div class="h abs" style="left:90px;right:90px;top:440px;font-size:{max(hs(st["head"],130),84)}px">{st["head"]}</div>{iso}'
    if t=="st_text":
        return f'<div class="abs" style="inset:0;background:{CREAM}"></div><div class="h abs" style="left:90px;right:90px;top:520px;font-size:124px">{st["head"]}</div>{note(st["note"],CORAL,90,1180,-3,74)}{iso}'
    if t=="st_lines":
        return f'<div class="abs" style="inset:0;background:{DEEP}"></div><div class="h abs" style="left:90px;right:90px;top:300px;font-size:96px;color:{CREAM}">Si hoy pesa demasiado, no estás solo.</div><div class="abs" style="left:90px;right:90px;top:820px">'+"".join(f'<div style="background:{SURF};border-radius:40px;padding:36px 46px;margin-bottom:28px"><div style="font-size:78px;font-weight:800">{a}</div><div style="font-size:36px;font-weight:500;margin-top:6px">{b}</div></div>' for a,b in [("Línea 106","Medellín · 24 horas"),("(604) 444 44 48","Línea Amiga Saludable"),("123","emergencias")])+f'</div>{iso}'
    if t=="st_iso":
        return f'<div class="abs" style="inset:0;background:{CORAL}"></div><img class="abs" src="{I}/isotipo.png" style="left:290px;top:440px;width:500px"><div class="h abs" style="left:90px;right:90px;top:900px;font-size:150px;text-align:center">{st["head"]}</div>{note(st["note"],SURF,360,1150,-3,84)}'
    if t=="st_reminder":
        return f'<div class="abs" style="inset:0;background:{CREAM}"></div>{blob(-180,1400,560,SKY,.3)}{blob(760,-160,480,CORAL,.22)}<span class="c abs" style="left:90px;top:700px;font-size:80px;color:{CORAL}">recordatorio de hoy</span><div class="h abs" style="left:90px;right:90px;top:830px;font-size:{hs(st["head"],130)}px">{st["head"]}</div>{iso}'
    raise ValueError(t)

def build(out):
    from playwright.sync_api import sync_playwright
    os.makedirs(out,exist_ok=True); man={"posts":[],"stories":[]}
    with sync_playwright() as p:
        b=p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--allow-file-access-from-files"])
        pg=b.new_page(viewport={"width":1080,"height":1350})
        tmp=os.path.join(out,"_tmp.html")
        def shot(htmlstr,path,w,h):
            pg.set_viewport_size({"width":w,"height":h}); open(tmp,"w").write(htmlstr)
            pg.goto("file://"+tmp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(120)
            ok=pg.evaluate("Promise.all([document.fonts.load('800 40px P'),document.fonts.load('400 40px P'),document.fonts.load('700 40px C')]).then(r=>r.every(x=>x.length>0))")
            assert ok, "fuente no cargada: "+path
            pg.screenshot(path=path,clip={"x":0,"y":0,"width":w,"height":h})
        for po in POSTS:
            d=os.path.join(out,"posts",f'{po["date"]}_{po["id"]}'); os.makedirs(d,exist_ok=True); files=[]
            for i,s in enumerate(po["slides"]):
                fn=f'{i+1:02d}.png'; shot(page(POST_T[s["t"]](s,po["camp"]),1080,1350),os.path.join(d,fn),1080,1350); files.append(fn)
            man["posts"].append(dict({k:v for k,v in po.items() if k!="slides"},folder=f'posts/{po["date"]}_{po["id"]}',media=files))
        for day in plan():
            d=os.path.join(out,"stories",day["date"]); os.makedirs(d,exist_ok=True); items=[]
            for i,st in enumerate(day["stories"]):
                fn=f'{i+1:02d}_{st["t"][3:]}.png'; shot(page(ST(st,day["camp"]),1080,1920),os.path.join(d,fn),1080,1920)
                items.append(dict(file=fn,type=st["t"][3:],sticker=st.get("sticker"),text=st.get("head") or st.get("a")))
            man["stories"].append(dict(date=day["date"],camp=day["camp"],folder=f'stories/{day["date"]}',items=items))
        b.close(); os.remove(tmp)
    json.dump(man,open(os.path.join(out,"manifest.json"),"w"),ensure_ascii=False,indent=1)
if __name__=="__main__": build(sys.argv[1])
