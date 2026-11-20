# -*- coding: utf-8 -*-
import sys, json, subprocess, numpy as np
sys.path.insert(0,'/home/claude/tiktok')
from audio import env
from playwright.sync_api import sync_playwright
F="file:///home/claude/pack/src/fonts"; ISO="file:///home/claude/pack/src/img/isotipo.png"
CREAM="#F5E6C8"; DEEP="#3D5A6C"; CORAL="#FF8C7A"; SKY="#7EC8E3"
MS=[(0.13,2.10),(2.66,5.48),(6.08,8.50),(8.96,10.74),(11.30,12.97),(13.43,15.97)]
SS=[(0.16,2.76),(3.29,5.56),(5.85,12.08),(12.51,16.31),(16.72,18.75)]
seq=[]
for i in range(6):
    seq.append(("m",i))
    if i<5: seq.append(("s",i))
TXT={("m",0):["Oye, ¿hoy es el día del psicólogo?"],("s",0):["Sí, hoy, 20 de noviembre. ¿Por?"],
("m",1):["He pensado en ir… pero no estoy tan mal"],("s",1):["No tienes que estar “muy mal” para ir"],
("m",2):["¿Y si me acuesta en un sofá y me pregunta por mi mamá?"],("s",2):["Jajaja, eso es en las películas","La primera sesión es para conocerse, no para contarlo todo"],
("m",3):["¿Y me va a decir qué hacer con mi vida?"],("s",3):["No. Te ayuda a entender lo que te pasa, para que decidas tú"],
("m",4):["Bueno… ¿y a quién le escribo?"],("s",4):["A Psiclín. Escríbeles por WhatsApp","+57 319 681 7123"],
("m",5):["Entonces, feliz día a los psicólogos"]}
SUB={("s",2):[0,2.73],("s",4):[0,1.2]}  # momento de cada burbuja dentro de la frase
GAP=0.38; t=0.6; lines=[]
for who,i in seq:
    a,b=(MS if who=="m" else SS)[i]
    lines.append(dict(who=who,i=i,src_a=a,src_b=b,t0=round(t,3),t1=round(t+b-a,3)))
    t+=b-a+GAP
END=t+0.2; TOTAL=END+3.2
bubbles=[]
for L in lines:
    for k,txt in enumerate(TXT[(L["who"],L["i"])]):
        off=SUB.get((L["who"],L["i"]),[0,0])[k]
        bubbles.append(dict(who=L["who"],txt=txt,t=L["t0"]+off,t0=L["t0"],t1=L["t1"],first=(k==0)))
envs={w:env(f"/home/claude/chatvid/{n}.mp3").tolist() for w,n in (("m","mateo"),("s","sara"))}
mx={w:max(v) for w,v in envs.items()}
html=f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:P;src:url({F}/poppins-500.woff2);font-weight:500}}
@font-face{{font-family:P;src:url({F}/poppins-600.woff2);font-weight:600}}
@font-face{{font-family:P;src:url({F}/poppins-700.woff2);font-weight:700}}
@font-face{{font-family:P;src:url({F}/poppins-800.woff2);font-weight:800}}
@font-face{{font-family:C;src:url({F}/caveat.woff2);font-weight:400 700}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;overflow:hidden;font-family:P;color:{DEEP};background:{CREAM}}}
.bg{{position:absolute;inset:0;background-color:{CREAM};background-image:radial-gradient(circle at 10% 30%,rgba(255,140,122,.22) 0 120px,transparent 121px),radial-gradient(circle at 95% 62%,rgba(126,200,227,.28) 0 170px,transparent 171px),radial-gradient(circle at 20% 92%,rgba(126,200,227,.22) 0 90px,transparent 91px)}}
.top{{position:absolute;left:0;right:0;top:150px;text-align:center}}
.pill{{display:inline-block;background:{DEEP};color:#fff;font-weight:800;font-size:40px;text-transform:uppercase;padding:14px 34px;border-radius:999px;letter-spacing:.01em}}
.note{{font-family:C;font-weight:700;font-size:58px;color:{CORAL};transform:rotate(-3deg);margin-top:4px}}
.head{{position:absolute;left:60px;right:60px;top:330px;height:140px;background:#fff;border-radius:40px;display:flex;align-items:center;gap:28px;padding:0 34px;box-shadow:0 14px 40px rgba(120,80,30,.14)}}
.av{{width:92px;height:92px;border-radius:50%;background:{SKY};color:#fff;font-weight:800;font-size:46px;display:flex;align-items:center;justify-content:center}}
.nm{{font-weight:700;font-size:44px;line-height:1}} .st{{font-size:30px;font-weight:500;color:#6E8FA6;margin-top:8px}}
.win{{position:absolute;left:0;right:0;top:500px;height:1010px;overflow:hidden;-webkit-mask-image:linear-gradient(180deg,transparent 0,#000 60px,#000 100%)}}
.list{{position:absolute;left:60px;right:150px;top:0;display:flex;flex-direction:column;gap:22px;padding-top:70px}}
.b{{max-width:740px;font-size:44px;font-weight:600;line-height:1.28;padding:26px 34px;border-radius:40px;box-shadow:0 10px 26px rgba(120,80,30,.12);display:none;transform-origin:left bottom;position:relative}}
.b.s{{align-self:flex-start;background:#fff;border-bottom-left-radius:12px}}
.b.m{{align-self:flex-end;background:{CORAL};border-bottom-right-radius:12px;transform-origin:right bottom}}
.w{{display:inline-flex;gap:6px;align-items:center;height:30px;margin-left:16px;vertical-align:middle}}
.w i{{display:block;width:7px;border-radius:4px;background:{DEEP};opacity:.55}}
.typing{{align-self:flex-start;background:#fff;border-radius:40px;padding:26px 34px;display:none;gap:12px}}
.typing i{{display:block;width:16px;height:16px;border-radius:50%;background:#9DB3C2}}
.inp{{position:absolute;left:60px;right:150px;top:1530px;height:110px;background:#fff;border-radius:999px;display:flex;align-items:center;padding:0 40px;font-size:36px;color:#9DB3C2;font-weight:500}}
.end{{position:absolute;inset:0;background:{CORAL};opacity:0;display:flex;flex-direction:column;justify-content:center;padding:0 90px}}
.end h1{{font-weight:800;font-size:112px;line-height:1.03;text-transform:uppercase}}
.end p{{font-size:48px;font-weight:600;line-height:1.3;margin-top:40px;max-width:780px}}
.end .wa{{margin-top:56px;align-self:flex-start;background:{DEEP};color:#fff;font-weight:700;font-size:44px;padding:26px 48px;border-radius:999px}}
.end img{{position:absolute;right:90px;bottom:330px;width:150px}}
</style></head><body><div class="bg"></div>
<div class="top"><div class="pill">Día del Psicólogo</div><div class="note">20 de noviembre</div></div>
<div class="head"><div class="av">S</div><div><div class="nm">Sara</div><div class="st" id="st">en línea</div></div></div>
<div class="win"><div class="list" id="list"></div></div>
<div class="inp">Escribe un mensaje…</div>
<div class="end" id="end"><h1>Feliz Día del Psicólogo</h1><p>No tienes que estar “muy mal” para hablar con alguien.</p><div class="wa">WhatsApp 319 681 7123</div><img src="{ISO}"></div>
<script>
const B={json.dumps(bubbles)}, E={json.dumps(envs)}, MX={json.dumps(mx)}, END={END}, LINES={json.dumps(lines)};
const list=document.getElementById('list'); const els=[];
const ty=document.createElement('div'); ty.className='typing'; ty.innerHTML='<i></i><i></i><i></i>';
B.forEach((b,k)=>{{const d=document.createElement('div'); d.className='b '+b.who; d.innerHTML='<span>'+b.txt+'</span>'+(b.first?'<span class="w"><i></i><i></i><i></i><i></i></span>':''); list.appendChild(d); els.push(d);}});
list.appendChild(ty);
let scroll=0;
function lvl(who,src){{const e=E[who]; const i=Math.max(0,Math.min(e.length-1,Math.round(src*100))); return Math.min(1,e[i]/MX[who]*1.6);}}
window.setT=function(t){{
  let next=null; for(const L of LINES) if(L.t0>t){{next=L;break;}}
  const sTyping = next && next.who=='s' && next.t0-t<0.9 && !(LINES.find(L=>L.t0<=t&&t<L.t1));
  document.getElementById('st').textContent = sTyping?'escribiendo…':'en línea';
  ty.style.display = sTyping?'flex':'none';
  if(sTyping){{[...ty.children].forEach((c,j)=>{{c.style.transform='translateY('+(-8*Math.max(0,Math.sin(t*9-j*0.9)))+'px)';}});}}
  B.forEach((b,k)=>{{const d=els[k]; if(t<b.t){{d.style.display='none';return;}} d.style.display='block';
    const p=Math.min(1,(t-b.t)/0.22); const s=0.7+0.3*(1-Math.pow(1-p,3))+0.06*Math.sin(Math.PI*p);
    d.style.transform='scale('+s+')'; d.style.opacity=Math.min(1,p*2);
    if(b.first){{const w=d.querySelector('.w'); const L=LINES.find(L=>L.t0==b.t0); const on=t>=b.t0&&t<b.t1;
      const src=(L.who=='m'?0:0)+(t-L.t0)+L.src_a;
      [...w.children].forEach((c,j)=>{{const v=on?lvl(b.who,src+j*0.03):0; c.style.height=(8+22*v*(0.7+0.3*Math.sin(t*20+j*2)))+'px'; c.style.opacity=on?.9:.35;}}); }}
  }});
  const H=list.scrollHeight, avail=1010-20; const target=Math.max(0,H-avail);
  scroll+= (target-scroll)*0.22; list.style.transform='translateY('+(-scroll)+'px)';
  const e=document.getElementById('end'); const q=Math.max(0,Math.min(1,(t-END)/0.35)); e.style.opacity=q; e.style.transform='translateY('+(60*(1-q))+'px)';
}};
</script></body></html>'''
open('/home/claude/chatvid/chat.html','w').write(html)
json.dump(dict(lines=lines,END=END,TOTAL=TOTAL),open('/home/claude/chatvid/timeline.json','w'))
mode=sys.argv[1] if len(sys.argv)>1 else "prev"
FPS=30
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=br.new_page(viewport={'width':1080,'height':1920})
    pg.goto('file:///home/claude/chatvid/chat.html')
    pg.evaluate("Promise.all([document.fonts.load('800 40px P'),document.fonts.load('600 40px P'),document.fonts.load('700 40px C')]).then(()=>document.fonts.ready)")
    if mode=="prev":
        for k,ts in enumerate([1.5,9.0,20.5,31.0,TOTAL-1]):
            # avanzar el scroll suavizado
            for tt in np.arange(0,ts,1/FPS): pg.evaluate(f"setT({tt})")
            pg.screenshot(path=f'/home/claude/chatvid/prev{k}.jpg',type='jpeg',quality=85)
    else:
        n=int(TOTAL*FPS)
        ff=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","image2pipe","-framerate",str(FPS),"-c:v","mjpeg","-i","-","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","/home/claude/chatvid/video_tmp.mp4"],stdin=subprocess.PIPE)
        for f in range(n):
            pg.evaluate(f"setT({f/FPS})"); ff.stdin.write(pg.screenshot(type='jpeg',quality=92))
        ff.stdin.close(); assert ff.wait()==0
    br.close()
print("TOTAL",TOTAL)
