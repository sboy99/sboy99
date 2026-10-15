import json, html, random, sys
THEME = sys.argv[1]
C = dict(dark=dict(bg="#0d1117",p="#f2d29b",r="#8a93a6",s="#c9d1d9",t="#e6edf3",m="#7d8590"),
         light=dict(bg="#f6f8fa",p="#9a6418",r="#6e7781",s="#57606a",t="#1f2328",m="#656d76"))[THEME]
fr = json.load(open("frames.json"))
N = len(fr); H = len(fr[0][0]); W = len(fr[0][0][0])
# crop empty rows
rows = [j for j in range(H) if any(fr[f][0][j].strip() or fr[f][1][j].strip() for f in range(N))]
top, bot = rows[0]-2, rows[-1]+3
FS, LH, CW = 11, 13, 6.6
PADX, PADY = 24, 20
SW = int(W*CW + 2*PADX); SH = int((bot-top)*LH + 2*PADY) + 44
DUR = 4.8; dt = DUR/N
out = []
out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{SW}" height="{SH}" viewBox="0 0 {SW} {SH}">')
out.append(f'''<style>
text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;font-size:{FS}px;white-space:pre}}
.p{{fill:{C["p"]}}} .r{{fill:{C["r"]}}} .s{{fill:{C["s"]}}} .t{{fill:{C["t"]};font-size:15px}} .m{{fill:{C["m"]};font-size:15px}}
.cur{{animation:bl 1s steps(1) infinite}} @keyframes bl{{50%{{opacity:0}}}}
.ty{{animation:ty 2.4s steps(52,end) .4s both}} @keyframes ty{{from{{width:0}}to{{width:{SW}px}}}}
.f{{opacity:0;animation:k {DUR}s steps(1,end) infinite}}
@keyframes k{{0%{{opacity:1}}{100/N:.4f}%{{opacity:0}}100%{{opacity:0}}}}
.tw{{animation:tw 3.2s ease-in-out infinite}}
@keyframes tw{{0%,100%{{opacity:.15}}50%{{opacity:.9}}}}
@media (prefers-reduced-motion:reduce){{.f{{animation:none}}.f0{{opacity:1}}.tw{{animation:none}}}}
</style>''')
out.append(f'<rect width="{SW}" height="{SH}" rx="12" fill="{C["bg"]}"/>')
random.seed(7)
for _ in range(38):
    x = random.uniform(10, SW-10); y = random.uniform(10, SH-10)
    c = random.choice(".·.+*.")
    out.append(f'<text class="s tw" x="{x:.0f}" y="{y:.0f}" style="animation-delay:-{random.uniform(0,3.2):.2f}s">{html.escape(c)}</text>')
def lines(layer, cls):
    s = []
    for j in range(top, bot):
        ln = layer[j].rstrip()
        if not ln.strip(): continue
        lead = len(ln) - len(ln.lstrip())
        body = ln[lead:]
        x = PADX + lead*CW; y = PADY + (j-top)*LH + FS
        s.append(f'<text class="{cls}" x="{x:.1f}" y="{y}" textLength="{len(body)*CW:.1f}" lengthAdjust="spacing" xml:space="preserve">{html.escape(body)}</text>')
    return "".join(s)
for f in range(N):
    p, r = fr[f]
    out.append(f'<g class="f f{f}" style="animation-delay:{f*dt:.3f}s">{lines(r,"r")}{lines(p,"p")}</g>')
cap = "~/sagar/sboy99 $ backend & devops engineer — bengaluru"
cy = SH - 26
out.append(f'<clipPath id="c"><rect class="ty" x="0" y="{cy-16}" height="24" width="0"/></clipPath>')
out.append(f'<g clip-path="url(#c)"><text class="m" x="{PADX}" y="{cy}" xml:space="preserve">~/sagar/sboy99 $ <tspan class="t">backend &amp; devops engineer — bengaluru</tspan></text></g>')
out.append(f'<text class="t cur" x="{PADX + len(cap)*9.05:.0f}" y="{cy}">▍</text>')
out.append('</svg>')
open(f"assets/saturn-{THEME}.svg","w").write("\n".join(out))
import os; print(SW, SH, os.path.getsize(f"assets/saturn-{THEME}.svg")//1024, "KB")
