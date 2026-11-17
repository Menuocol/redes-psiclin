import subprocess, numpy as np, json, itertools
SR=16000; HOP=0.01
LINES={
 "s1_andres":["¡Quiubo, parce! ¿Cómo vas?","Ajá... ¿Y de verdad, cómo vas?","Gracias por contarme. Aquí estoy. Hablemos."],
 "s1_mateo":["Bien, bien. Normal, ahí vamos.","Mal, hermano. Hace rato no duermo bien."],
 "s2_coral":["Bueno, a dormir, que mañana madrugo.","No.","¿Por qué eres así?"],
 "s2_cerebro":["¡Hola! ¿Repasamos lo que dijiste en esa reunión del 2019?","¿Y si mañana todo sale mal? ¿Y ese mensaje que dejaste en visto?","Bueno... mañana."],
 "s2_celeste":["Un truco: escribe en un papel lo que te está dando vueltas, y dile a tu cabeza: “mañana lo pensamos”."],
 "s3_amiga":["¿Y qué te imaginas que va a pasar en tu primera cita?"],
 "s3_coral":["Pues... lo de las películas.","¿Así, sin saludar?","Ah, pues así sí."],
 "s3_dr":["Hábleme... de su madre."],
 "s3_celeste":["¡Hola! Bienvenida. Cuéntame qué te trae por aquí, a tu ritmo. Lo que no quieras contar, no lo cuentas."],
 "s4_coral":["Qué día tan horrible. Me merezco algo.","Lo necesito. Bueno... no sé.","¿Y si lo dejo en el carrito para siempre?"],
 "s4_cerebro":["¿Eso lo necesitas... o lo estás sintiendo?","¡Inversión del año!"],
 "s4_celeste":["Antes de pagar, respira y espera diez minutos. Si lo que buscas es calma, eso no llega en una caja."]}
EXTRA={"s2_cerebro":[0,0,1.4]}  # el bostezo alarga la última frase
def pcm(path):
    raw=subprocess.run(["ffmpeg","-v","error","-i",path,"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True,check=True).stdout
    return np.frombuffer(raw,dtype=np.float32)
def env(path):
    x=pcm(path); n=int(SR*HOP); m=len(x)//n; return np.sqrt((x[:m*n].reshape(m,n)**2).mean(1))
def split(path, lines, extra=None):
    r=env(path); thr=max(r.max()*0.04,0.004); v=r>thr; idx=np.where(v)[0]; s0,s1=idx[0],idx[-1]+1
    n=len(lines)
    if n==1: return [(s0*HOP,s1*HOP)], None
    gaps=[]; i=s0
    while i<s1:
        if not v[i]:
            j=i
            while j<s1 and not v[j]: j+=1
            if (j-i)*HOP>=0.18: gaps.append((i,j))
            i=j
        else: i+=1
    exp=np.array([len(l.replace("...","").replace("“","").replace("”","")) for l in lines],float)
    exp=exp*0.065+np.array(extra or [0]*n)
    best=None
    for comb in itertools.combinations(gaps,n-1):
        b=[s0]+[g for c in comb for g in c]+[s1]; segs=[(b[2*k],b[2*k+1]) for k in range(n)]
        d=np.array([(e-s)*HOP for s,e in segs]); gl=sum((c[1]-c[0])*HOP for c in comb)
        err=((d/d.sum()-exp/exp.sum())**2).sum() - 0.02*gl
        if best is None or err<best[0]: best=(err,segs,d)
    return [(a*HOP,b*HOP) for a,b in best[1]], best[2].round(2).tolist()
if __name__=="__main__":
    import glob; res={}
    for f in sorted(glob.glob("audio/*.mp3")):
        k=f.split("/")[-1][:-4]; base=k[:-2]
        segs,d=split(f,LINES[base],EXTRA.get(base)); res[k]=segs; print(k,d)
    json.dump(res,open("audio/segments.json","w"),indent=1)
