# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0,'/home/claude/redes-psiclin/src'); sys.path.insert(0,'/home/claude/tiktok')
from render import page, note, under, blob, isoimg, icon, CREAM, DEEP, CORAL, SKY, SURF, SH
from chars import char
from playwright.sync_api import sync_playwright
OUT='/home/claude/diapsi'
celeste=lambda x,y,s,expr="feliz",pose="arriba":char(SKY,x,y,s,expr,0,"gafas",pose)
coral=lambda x,y,s,expr="feliz",pose="arriba",flip=False:char(CORAL,x,y,s,expr,0,"",pose,flip)

s1=f'''<div class="abs" style="inset:0;background:{CREAM}"></div>{blob(720,-220,560,SKY,.30)}{blob(-180,980,380,CORAL,.25)}
{note("20 de noviembre",CORAL,90,150,-3,70)}
<div class="h abs" style="left:90px;right:90px;top:250px;font-size:118px">Hoy es el<br>Día del<br>Psicólogo</div>
<div class="abs" style="left:94px;top:648px;font-size:44px;font-weight:600">en Colombia</div>
{celeste(380,1240,1.55)}{coral(720,1240,1.45,"feliz","arriba",True)}
{note("gracias, equipo",DEEP,560,690,-5,72,"#fff")}{isoimg()}'''

def row(ok,t):
    ic=icon("check",48,DEEP,3) if ok else '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>'
    bg="#fff" if ok else DEEP
    return f'<div style="display:flex;align-items:center;gap:28px;margin:20px 0"><div style="width:76px;height:76px;flex:none;border-radius:22px;background:{bg};display:flex;align-items:center;justify-content:center;box-shadow:0 8px 20px rgba(0,0,0,.08)">{ic}</div><span style="font-size:44px;font-weight:600;line-height:1.2">{t}</span></div>'
s2=f'''<div class="abs" style="inset:0;background:{CREAM}"></div>{blob(780,-200,500,CORAL,.22)}
<div class="h abs" style="left:90px;right:90px;top:120px;font-size:82px">Lo que hace un psicólogo<br><span style="color:{CORAL}">(y lo que no)</span></div>
<div class="abs" style="left:90px;right:90px;top:430px">
{row(1,"te escucha sin juzgar")}{row(1,"te ayuda a entender lo que te pasa")}{row(1,"te acompaña mientras decides tú")}
<div style="height:34px"></div>
{row(0,"no te dice qué hacer con tu vida")}{row(0,"no te lee la mente")}{row(0,"no se parece al de las pelis")}</div>
{note("así de simple",CORAL,90,1190,-3,66)}{isoimg()}'''

s3=f'''<div class="abs" style="inset:0;background:{CORAL}"></div>{blob(760,-180,480,"#fff",.18)}
<div class="h abs" style="left:90px;right:90px;top:200px;font-size:96px">No tienes que estar “muy mal” para hablar con alguien.</div>
<div class="abs" style="left:90px;right:330px;top:740px;font-size:44px;font-weight:500;line-height:1.35">Si llevas tiempo pensándolo, hoy es un buen día para escribirnos.</div>
<div class="abs" style="left:90px;top:1060px;background:{DEEP};color:#fff;border-radius:999px;padding:24px 44px;font-size:38px;font-weight:700">WhatsApp 319 681 7123</div>
{char(SKY,880,1060,1.05,"feliz",0,"gafas","habla",True)}{isoimg()}'''

story=f'''<div class="abs" style="inset:0;background:{CREAM}"></div>{blob(700,-200,620,SKY,.30)}{blob(-200,1500,520,CORAL,.25)}
{note("20 de noviembre",CORAL,90,260,-3,76)}
<div class="h abs" style="left:90px;right:90px;top:370px;font-size:112px">Hoy es el Día del Psicólogo en Colombia</div>
<div class="abs" style="left:90px;right:120px;top:830px;font-size:50px;font-weight:600;line-height:1.3">Gracias a nuestro equipo por escuchar sin juzgar, todos los días.</div>
<div class="abs" style="left:90px;right:90px;top:1100px;height:330px;border:5px dashed rgba(61,90,108,.25);border-radius:40px;display:flex;align-items:center;justify-content:center;font-size:34px;color:rgba(61,90,108,.45);font-weight:600" id="slot">aquí va la encuesta</div>
{celeste(330,1760,1.25,"feliz","habla")}{coral(760,1760,1.2,"feliz","arriba",True)}{isoimg(120,64,90)}'''

pages=[("post_01",s1,1080,1350),("post_02",s2,1080,1350),("post_03",s3,1080,1350),("historia",story,1080,1920),("historia_singuia",story.replace('id="slot">aquí va la encuesta','id="slot" style="opacity:0">'),1080,1920)]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome')
    for name,body,w,h in pages:
        pg=b.new_page(viewport={'width':w,'height':h})
        f=f'{OUT}/{name}.html'; open(f,'w').write(page(body,w,h)); pg.goto('file://'+f); pg.evaluate("Promise.all([document.fonts.load('800 40px P'),document.fonts.load('600 40px P'),document.fonts.load('700 40px C')]).then(()=>document.fonts.ready)"); pg.wait_for_timeout(300)
        assert pg.evaluate("document.fonts.check('800 40px P') && document.fonts.check('700 40px C')")
        pg.screenshot(path=f'{OUT}/{name}.png'); pg.close()
    b.close()
from PIL import Image
ims=[Image.open(f'{OUT}/post_0{i}.png').convert('RGB').resize((540,675)) for i in (1,2,3)]+[Image.open(f'{OUT}/historia.png').convert('RGB').resize((380,675))]
c=Image.new('RGB',(540*3+380,675),'white'); x=0
for im in ims: c.paste(im,(x,0)); x+=im.width
c.save(f'{OUT}/sheet.jpg',quality=88)
