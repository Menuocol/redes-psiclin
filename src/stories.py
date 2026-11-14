# -*- coding: utf-8 -*-
import datetime as dt
from content import REMINDERS
START, END = dt.date(2026,11,16), dt.date(2027,1,3)
def camp(d): return "anx" if d <= dt.date(2026,12,13) else "burn"
ETO = {"2026-11-17":("¿Puente para dormir","o para salir?"),"2026-11-24":("¿Café","o aromática?"),"2026-12-01":("¿Árbol","o pesebre?"),
       "2026-12-08":("¿Buñuelo","o natilla?"),"2026-12-15":("¿Novena con villancicos","o en silencio?"),"2026-12-22":("¿Regalo hecho a mano","o comprado?"),"2026-12-29":("¿Fin de año en casa","o de paseo?")}
FRI = {"2026-11-20":"¿Tus hijos te cuentan cómo les fue de verdad?","2026-11-27":"¿Compras más cuando estás estresado?","2026-12-04":"¿Diciembre te carga o te recarga?",
       "2026-12-11":"¿Ya fuiste a ver los alumbrados?","2026-12-18":"¿Cuántas novenas llevas?","2026-12-25":"¿Cómo te sientes hoy, de verdad?"}
THU = {"2026-11-19":"¿A los hombres de tu vida les cuesta decir cómo están?","2026-11-26":"Pregúntale a la psicóloga: ¿qué te da curiosidad de ir a terapia?",
       "2026-12-03":"¿Qué te gustaría saber de la primera sesión?","2026-12-10":"Pregúntale a la psicóloga lo que quieras sobre ansiedad.",
       "2026-12-17":"¿Cuál es la pregunta más incómoda que te han hecho en una novena?","2026-12-24":None,"2026-12-31":None}
WED = {"2026-11-18":("¿Tienes ansiedad sin saberlo?","test"),"2026-11-25":("7 preguntas. 2 minutos.","test"),"2026-12-02":("¿La ansiedad se coló en tus fiestas?","test"),
       "2026-12-09":("Si te reconociste… hablemos.","whatsapp"),"2026-12-16":("¿Estás cansado de estar cansado?","whatsapp"),"2026-12-23":("¿Te despiertas cansado aunque duermas?","whatsapp"),
       "2026-12-30":("Enero no tiene que empezar con el tanque vacío.","whatsapp")}
NOVENA = ["Hoy empieza la novena. Que te encuentre con un poquito de calma.","Día 2. Cantar desafinado también cuenta como alegría.","Día 3. Está bien llegar cansado y quedarte un rato.",
          "Día 4. Hoy pide un abrazo, no solo un buñuelo.","Día 5. Si hoy no tienes ganas, puedes quedarte en casa.","Día 6. Mira quién está solo en la reunión y acércate.",
          "Día 7. Agradece una cosa pequeña de este año.","Día 8. Respira antes de la última recta.","Día 9. Nochebuena: que sea a tu manera."]
def plan():
    out=[]; d=START; ri=0
    while d<=END:
        k=d.isoformat(); wd=d.weekday(); c=camp(d); day=[]
        if wd==0:
            if k=="2026-12-07": day.append(dict(t="st_photo", img="velitas", head="Prende una velita por lo que sí lograste.", note="noche de velitas", sticker="caja de preguntas: ¿por qué prendes la tuya?"))
            day.append(dict(t="st_slider", head="¿Cómo está tu clima hoy?", note="pronóstico emocional", sticker="deslizador: ☀️ → 🌧️"))
        if wd==1 and k in ETO: day.append(dict(t="st_eto", a=ETO[k][0], b=ETO[k][1], sticker="encuesta: esto o aquello"))
        if wd==2 and k in WED:
            hook,dest=WED[k]
            day.append(dict(t="st_camp", head=hook, note="desliza"))
            day.append(dict(t="st_camp_poll", head="¿Te ha pasado?", sticker="encuesta: sí / a veces / no"))
            day.append(dict(t="st_camp_link", head=("Haz el test de 7 preguntas." if dest=="test" else "Hablemos por WhatsApp."), sticker="enlace: "+("test de ansiedad" if dest=="test" else "WhatsApp +57 319 681 7123")))
            if k=="2026-11-25": day.append(dict(t="st_lines155"))
        if wd==3 and THU.get(k): day.append(dict(t="st_box", head=THU[k], sticker=("encuesta: sí / a veces / no" if k=="2026-11-19" else "caja de preguntas")))
        if wd==4 and k in FRI: day.append(dict(t="st_poll", head=FRI[k], sticker=("deslizador" if k=="2026-12-25" else "encuesta")))
        if k=="2026-11-21": day.append(dict(t="st_share", head="Hola, ¿cómo estás de verdad?", note="envíaselo a alguien hoy"))
        if k=="2026-11-27": day.append(dict(t="st_offer", head="Lo único en oferta hoy: tu descanso.", sticker="enlace: test de ansiedad"))
        if "2026-12-16"<=k<="2026-12-24":
            i=(d-dt.date(2026,12,16)).days; day.append(dict(t="st_novena", n=i+1, head=NOVENA[i]))
        if k=="2026-12-20": day.append(dict(t="st_text", head="La prima no es para pagar la culpa.", note="es para disfrutar un poquito"))
        if k in ("2026-12-24","2026-12-31"): day.append(dict(t="st_lines"))
        if k=="2027-01-01": day.append(dict(t="st_iso", head="Feliz 2027.", note="aquí seguimos"))
        day.append(dict(t="st_reminder", head=REMINDERS[ri%len(REMINDERS)])); ri+=1
        out.append(dict(date=k, camp=c, stories=day)); d+=dt.timedelta(days=1)
    return out
if __name__=="__main__":
    p=plan(); print(len(p), sum(len(x['stories']) for x in p))
