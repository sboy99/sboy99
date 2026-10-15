import html, sys
THEME = sys.argv[1]
# (symbol, name, group)
E = [
 ("Ts","TypeScript","lang"),("Js","JavaScript","lang"),("Go","GoLang","lang"),("Py","Python","lang"),
 ("Sl","Solidity","lang"),("Mv","Move","lang"),("Sq","SQL","lang"),("Nd","Node.js","back"),
 ("Ns","NestJS","back"),("Ex","Express","back"),("Gn","Gin","back"),("Dz","Drizzle","back"),
 ("Pz","Prisma","back"),("To","TypeORM","back"),("Bq","BullMQ","back"),("Rb","RabbitMQ","back"),
 ("Pg","PostgreSQL","data"),("Rd","Redis","data"),("Mg","MongoDB","data"),("My","MySQL","data"),
 ("Sb","Supabase","data"),("Lt","SQLite","data"),("Dk","Docker","infra"),("K8","Kubernetes","infra"),
 ("Hm","Helm","infra"),("Tf","Terraform","infra"),("Ga","GH Actions","infra"),("Gc","GCP","infra"),
 ("Aw","AWS","infra"),("Ng","Nginx","infra"),("Gf","Grafana","infra"),("Lk","Loki","infra"),
 ("Re","React","front"),("Nx","Next.js","front"),("Tw","Tailwind","front"),("Zu","Zustand","front"),
 ("Cc","Claude Code","ai"),("Cu","Cursor","ai"),("Ai","LLM APIs","ai"),("Ye","Shipping","ai"),
]
COLS = 8
TW = 14  # tile width in chars incl. borders
PAL = dict(
 dark=dict(bg="#0d1117", line="#30363d", dim="#7d8590", txt="#e6edf3",
   lang="#f2cc60", back="#ff7b72", data="#79c0ff", infra="#7ee787", front="#d2a8ff", ai="#ffa657"),
 light=dict(bg="#f6f8fa", line="#d0d7de", dim="#656d76", txt="#1f2328",
   lang="#9a6700", back="#cf222e", data="#0969da", infra="#1a7f37", front="#8250df", ai="#bc4c00"))[THEME]
GROUPS = [("lang","languages"),("back","backend"),("data","data"),("infra","infra"),("front","frontend"),("ai","ai & vibes")]
CW, LH, FS = 7.2, 15, 12
PAD = 22
rows = (len(E)+COLS-1)//COLS
SW = int(COLS*(TW+1)*CW + 2*PAD - CW)
SH = int(rows*6*LH + 2*PAD + 3*LH)
o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{SW}" height="{SH}" viewBox="0 0 {SW} {SH}">',
f'''<style>
text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;font-size:{FS}px;white-space:pre}}
.b{{fill:{PAL["line"]}}}.d{{fill:{PAL["dim"]}}}.t{{fill:{PAL["txt"]}}}
{"".join(f".{g}{{fill:{PAL[g]}}}" for g,_ in GROUPS)}
.sym{{font-size:24px;font-weight:700;animation:glow 4.2s ease-in-out infinite}}
@keyframes glow{{0%,70%,100%{{opacity:.55}}35%{{opacity:1}}}}
@media (prefers-reduced-motion:reduce){{.sym{{animation:none;opacity:1}}}}
</style>''', f'<rect width="{SW}" height="{SH}" rx="12" fill="{PAL["bg"]}"/>']
def T(x,y,s,cls,extra=""):
    if cls=="b": extra+=f' textLength="{len(s)*CW:.1f}" lengthAdjust="spacing"'
    o.append(f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}" xml:space="preserve"{extra}>{html.escape(s)}</text>')
for n,(sym,name,g) in enumerate(E):
    r,c = divmod(n,COLS)
    x0 = PAD + c*(TW+1)*CW; y0 = PAD + r*6*LH + FS
    inner = TW-2
    T(x0,y0,"┌"+"─"*inner+"┐","b")
    for k in range(1,5): T(x0,y0+k*LH,"│"+" "*inner+"│","b")
    T(x0,y0+5*LH,"└"+"─"*inner+"┘","b")
    T(x0+2*CW,y0+LH,f"{n+1:02d}","d")
    T(x0+(TW-3)*CW,y0+LH,"•",g)
    delay = -((r+c)*0.22) % 4.2
    T(x0+2*CW,y0+3*LH-1,sym,f"sym {g}",f' style="animation-delay:{delay:.2f}s"')
    T(x0+2*CW,y0+4*LH,name.lower()[:inner-1],"t")
# legend
ly = PAD + rows*6*LH + FS + LH
x = PAD
for g,label in GROUPS:
    T(x,ly,"■",g); T(x+2*CW,ly,label,"d"); x += (len(label)+5)*CW
open(f"assets/stack-{THEME}.svg","w").write("\n".join(o)+"\n</svg>")
print(SW,SH)
