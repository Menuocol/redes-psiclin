import re
src=open('build.py').read()
src=src.split("pages=[")[0]
exec(src)
from playwright.sync_api import sync_playwright
items=[("v_01",s1,CREAM),("v_02",s2,CREAM),("v_03",s3,CORAL)]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome')
    for name,body,bgc in items:
        pg=b.new_page(viewport={'width':1080,'height':1920})
        html=page(f'<div class="abs" style="inset:0;background:{bgc}"></div><div class="abs" style="left:0;top:285px;width:1080px;height:1350px">{body}</div>',1080,1920)
        f=f'/home/claude/diapsi/{name}.html'; open(f,'w').write(html); pg.goto('file://'+f)
        pg.evaluate("Promise.all([document.fonts.load('800 40px P'),document.fonts.load('600 40px P'),document.fonts.load('700 40px C')]).then(()=>document.fonts.ready)"); pg.wait_for_timeout(300)
        pg.screenshot(path=f'/home/claude/diapsi/{name}.jpg',type='jpeg',quality=93); pg.close()
    b.close()
