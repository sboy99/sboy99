import math, html, sys, random, json
THEME = sys.argv[1]
W, H, N = 132, 18, 40
DUR = 5.0
CW, LH, FS, PADX = 6.6, 11, 10, 18
# the water is written in his own stack
words = ("nestjs postgres redis docker terraform gcp aws bullmq drizzle typescript go "
         "solidity kubernetes helm grafana loki nginx github-actions next.js react "
         "ship it  migrate it  scale it  sleep  ").split(" ")
random.seed(3)
P = 80  # texture period (cols); shifts 2 cols/frame -> 80 cols per 40 frames = seamless
tex = []
for j in range(H):
    line = ""
    while len(line) < P:
        line += random.choice(words) + random.choice(["  ", " ", ".", "_", " -", "  ;"])
    tex.append(line[:P])

def surface(x, t):
    # main swell + smaller chop, travelling left->right; integer cycles per loop
    u = 2*math.pi*(2*x - 1*t)
    h = 0.58 + 0.17*(math.sin(u) + 0.35*math.sin(2*u+0.6))/1.2  # skewed swell: steep front
    h += 0.05*math.sin(2*math.pi*(5*x - 2*t) + 1.3)
    h += 0.025*math.sin(2*math.pi*(11*x + 3*t) + 0.4)
    return h

frames = []
for f in range(N):
    t = f / N
    layers = {k: [[" "]*W for _ in range(H)] for k in ("deep","mid","foam")}
    for i in range(W):
        x = i / W
        s = surface(x, t)           # 0..1 from bottom
        top = int((1 - s) * H)      # row index of surface
        # slope -> crest foam where the wave front is steep
        slope = (surface(x + 1/W, t) - surface(x - 1/W, t)) * W
        for j in range(H):
            ch = tex[j][(i - 2*f) % P]
            if j < top:
                # spray above steep crests
                d = top - j
                if slope < -0.5 and d <= 2 and random.random() < 0.35 / d:
                    layers["foam"][j][i] = random.choice(".'`*")
                continue
            depth = j - top
            if ch == " ": continue
            if depth <= 1: layers["foam"][j][i] = ch
            elif depth <= 4 + (2 if slope < -0.6 else 0): layers["mid"][j][i] = ch
            else:
                # thin out deep water into streaks like the reference
                if (j + (i//7)) % 3: layers["deep"][j][i] = ch
    frames.append({k: ["".join(r) for r in v] for k, v in layers.items()})

C = dict(dark=dict(bg="#0d1117", deep="#1f4e79", mid="#4f8fc0", foam="#e6f1ff"),
         light=dict(bg="#f6f8fa", deep="#9cc3e4", mid="#3b7bb5", foam="#0b3a63"))[THEME]
SW = int(W*CW + 2*PADX); SH = H*LH + 30
dt = DUR/N
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{SW}" height="{SH}" viewBox="0 0 {SW} {SH}">',
f'''<style>
text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;font-size:{FS}px;white-space:pre}}
.deep{{fill:{C["deep"]}}}.mid{{fill:{C["mid"]}}}.foam{{fill:{C["foam"]}}}
.f{{opacity:0;animation:k {DUR}s steps(1,end) infinite}}
@keyframes k{{0%{{opacity:1}}{100/N:.3f}%{{opacity:0}}100%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.f{{animation:none}}.f0{{opacity:1}}}}
</style>''',
f'<rect width="{SW}" height="{SH}" rx="12" fill="{C["bg"]}"/>']
for f, fr in enumerate(frames):
    g = []
    for cls in ("deep","mid","foam"):
        for j, ln in enumerate(fr[cls]):
            s = ln.rstrip()
            if not s.strip(): continue
            lead = len(s) - len(s.lstrip()); body = s[lead:]
            g.append(f'<text class="{cls}" x="{PADX+lead*CW:.1f}" y="{12+j*LH+FS}" textLength="{len(body)*CW:.1f}" lengthAdjust="spacing" xml:space="preserve">{html.escape(body)}</text>')
    o.append(f'<g class="f f{f}" style="animation-delay:{f*dt:.3f}s">{"".join(g)}</g>')
o.append("</svg>")
out = f"assets/waves-{THEME}.svg"
open(out,"w").write("\n".join(o))
json.dump(frames, open("frames.json","w"))
import os; print(out, os.path.getsize(out)//1024, "KB")
