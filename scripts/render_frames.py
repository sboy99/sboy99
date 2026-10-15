import math, html

W, H = 128, 50
ASPECT = 0.5           # char width / char height
N = 48                 # frames per loop
RAMP = " .`:-~=+*ox%#@"
R = 0.235

def norm(v):
    l = math.sqrt(sum(c*c for c in v)); return [c/l for c in v]

tilt = math.radians(26)   # axial tilt toward viewer
roll = math.radians(-14)   # rotate whole system on screen
L = norm([-0.45, 0.35, 0.82])  # light direction

def rot_x(p, a):
    x,y,z=p; c,s=math.cos(a),math.sin(a); return [x, c*y-s*z, s*y+c*z]
def rot_z(p, a):
    x,y,z=p; c,s=math.cos(a),math.sin(a); return [c*x-s*y, s*x+c*y, z]
def to_body(p):   # screen -> planet frame
    return rot_x(rot_z(p, -roll), -tilt)
def to_screen(p):
    return rot_z(rot_x(p, tilt), roll)

ring_n = to_screen([0,1,0])   # ring plane normal (planet y = spin axis)

def ring_density(r):
    # r in planet radii; Saturn-ish ring structure
    if r < 1.28 or r > 2.25: return 0
    d = 0.0
    if r < 1.50: d = 0.35                 # C ring (faint)
    elif r < 1.95: d = 1.0                # B ring (bright)
    elif r < 2.02: d = 0.05               # Cassini division
    else: d = 0.70                        # A ring
    if 2.15 < r < 2.17: d = 0.1           # Encke gap
    d *= 0.88 + 0.12*math.sin(r*22)
    return d

def frame(f):
    t = f / N * 2*math.pi
    planet = [[" "]*W for _ in range(H)]
    rings  = [[" "]*W for _ in range(H)]
    for j in range(H):
        for i in range(W):
            x = (i - W/2 + 0.5) * ASPECT / H
            y = -(j - H/2 + 0.5) / H
            # --- planet
            zs = None
            d2 = x*x + y*y
            if d2 < R*R:
                zs = math.sqrt(R*R - d2)
                n = [x/R, y/R, zs/R]
                lam = 0.18 + 0.82*max(0, sum(a*b for a,b in zip(n, L)))
                b = to_body(n)
                lat = math.asin(max(-1,min(1,b[1])))
                lon = math.atan2(b[2], b[0]) + t          # spins one turn per loop
                band = 0.78 + 0.16*math.sin(lat*8) + 0.07*math.sin(lat*19+1)
                swirl = 0.10*math.sin(lon*3 + lat*9) + 0.06*math.sin(lon*5 - lat*14)
                storm = math.exp(-((lat-0.35)**2*90 + (math.sin((lon-1)/2))**2*30))
                v = lam**0.8 * (band + swirl + 0.35*storm)
                v = v*0.88 + 0.10
            # --- rings (ray along -z hits plane n·p = 0)
            zr = None
            if abs(ring_n[2]) > 1e-6:
                zr_ = -(ring_n[0]*x + ring_n[1]*y)/ring_n[2]
                p = to_body([x, y, zr_])
                r = math.hypot(p[0], p[2]) / R
                dens = ring_density(r)
                if dens > 0:
                    # Keplerian-ish: inner bands faster; integer speeds keep loop seamless
                    ang = math.atan2(p[2], p[0])
                    spd = 3 if r < 1.5 else 2 if r < 1.95 else 1
                    clump = 0.86 + 0.14*math.sin(ang*9 - spd*t + r*6) * math.sin(ang*4 - spd*t)
                    # planet shadow on rings (light from L)
                    q = [x, y, zr_]
                    tc = -sum(a*b for a,b in zip(q, L))
                    cl = [q[k] + tc*L[k] for k in range(3)]
                    shadow = 0.25 if (sum(c*c for c in cl) < R*R and tc < 0) else 1
                    rv = dens*clump*shadow*0.78
                    zr = zr_
            # --- composite
            if zs is not None and (zr is None or zr < zs):
                planet[j][i] = RAMP[max(1,min(len(RAMP)-1, int(v*(len(RAMP)-1))))]
            elif zr is not None:
                rings[j][i] = RAMP[max(1, min(len(RAMP)-1, int(rv*(len(RAMP)-1))))]
    return ["".join(r) for r in planet], ["".join(r) for r in rings]

frames = [frame(f) for f in range(N)]

import json
json.dump(frames, open("frames.json","w"))

# merged print
for k in [0]:
    p,r = frames[k]
    print("\n".join("".join(pc if pc!=" " else rc for pc,rc in zip(pl,rl)) for pl,rl in zip(p,r)))
