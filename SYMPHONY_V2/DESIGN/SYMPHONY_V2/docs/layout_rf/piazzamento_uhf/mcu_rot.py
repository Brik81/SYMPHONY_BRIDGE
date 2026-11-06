"""Rotazione di U301 a passi di 45 gradi, nella posizione attuale del PCB.
Per ogni rotazione: lunghezza totale dei collegamenti in linea d'aria (ratsnest) e numero di incroci
tra collegamenti di gruppi diversi. Scrive fig_mcu_rot.tex e tab_mcu_rot.tex.
Uso: python mcu_rot.py pcb.json cartella_uscita"""
import json, math, os, sys

d = json.load(open(sys.argv[1], encoding="utf-8"))
OUT = sys.argv[2]
F = {f["ref"]: f for f in d["fps"]}
STEP = 45


def rot(x, y, r):
    a = math.radians(r)
    return x * math.cos(a) + y * math.sin(a), -x * math.sin(a) + y * math.cos(a)


def padxy(ref, num):
    f = F[ref]
    for p in f["pads"]:
        if p["n"] == num:
            dx, dy = rot(p["x"], p["y"], f["r"])
            return f["x"] + dx, f["y"] + dy


def centre(ref):
    return F[ref]["x"], F[ref]["y"]


# gruppo: (colore, [(pin MCU, destinazione)])
GROUPS = {
    "Si4464 (SPI1, nIRQ)": ("sbgreen", [("8", padxy("IC204", "11")), ("21", padxy("IC204", "12")),
                                         ("22", padxy("IC204", "13")), ("23", padxy("IC204", "14")),
                                         ("41", padxy("IC204", "15"))]),
    "switch TX/RX": ("sborange", [("10", padxy("IC202", "2"))]),
    "temperatura PA": ("sbred", [("26", centre("IC2"))]),
    "dock (GPIO)": ("violet", [("2", padxy("J708", "13")), ("3", padxy("J708", "17")), ("4", padxy("J708", "14"))]),
    "USB (USART1)": ("sbblue2", [("42", centre("J15")), ("43", centre("J15"))]),
    "CAN (FDCAN1)": ("teal", [("44", centre("J202")), ("45", centre("J202"))]),
    "I2C1": ("brown", [("57", padxy("J203", "3")), ("58", padxy("J203", "2"))]),
}

u = F["U301"]
CX, CY = u["x"], u["y"]
UP = {p["n"]: (p["x"], p["y"]) for p in u["pads"]}


def cross(a, b, c, e):
    def o(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return o(a, b, c) * o(a, b, e) < 0 and o(c, e, a) * o(c, e, b) < 0


def evaluate(r):
    lines = []
    for g, (col, pins) in GROUPS.items():
        for n, dest in pins:
            dx, dy = rot(*UP[n], r)
            lines.append((g, col, (CX + dx, CY + dy), dest))
    L = sum(math.dist(a, b) for _, _, a, b in lines)
    X = sum(1 for i in range(len(lines)) for k in range(i + 1, len(lines))
            if lines[i][0] != lines[k][0] and cross(lines[i][2], lines[i][3], lines[k][2], lines[k][3]))
    return L, X, lines


angles = list(range(0, 360, STEP))
res = {r: evaluate(r) for r in angles}
cur = u["r"] % 360
res_cur = evaluate(cur)
best = min(angles, key=lambda r: (res[r][1], res[r][0]))
short = min(angles, key=lambda r: res[r][0])

# ---------------------------------------------------------------- figura
X0, X1, Y0, Y1 = 107, 153, 70, 146
S = 0.6  # mm sul foglio per mm


def panel(r, L, X, lines, title, frame):
    o = []
    o.append(r"\begin{tikzpicture}[x=%.2fmm,y=-%.2fmm]" % (S, S))
    o.append(r"\useasboundingbox (%g,%g) rectangle (%g,%g);" % (X0 - 1.2, Y0 - 11.5, X1 + 1.2, Y1 + 2))
    for e in d["edges"]:
        o.append(r"\draw[black!45,line width=0.4pt] (%.2f,%.2f) -- (%.2f,%.2f);" % (*e["s"], *e["e"]))
    for g, col, a, b in lines:
        o.append(r"\draw[%s,line width=0.5pt] (%.2f,%.2f) -- (%.2f,%.2f);" % (col, *a, *b))
        o.append(r"\fill[%s] (%.2f,%.2f) circle (0.6);" % (col, *b))
    # corpo dell'MCU (LQFP64 10x10) e pin 1
    pts = [rot(x, y, r) for x, y in ((-5, -5), (5, -5), (5, 5), (-5, 5))]
    o.append(r"\draw[black,fill=black!8,line width=0.5pt] " + " -- ".join("(%.2f,%.2f)" % (CX + px, CY + py) for px, py in pts) + " -- cycle;")
    px, py = rot(*UP["1"], r)
    o.append(r"\fill[black] (%.2f,%.2f) circle (0.9);" % (CX + px * 0.8, CY + py * 0.8))
    o.append(r"\node[font=\sffamily\small\bfseries,anchor=base] at (%.1f,%.1f) {%s};" % ((X0 + X1) / 2, Y0 - 6.5, title))
    o.append(r"\node[font=\sffamily\scriptsize,anchor=base] at (%.1f,%.1f) {%.0f\,mm \textbullet{} %d incroci};" % ((X0 + X1) / 2, Y0 - 1.5, L, X))
    if frame:
        o.append(r"\draw[%s,line width=1.4pt,rounded corners=2pt] (%g,%g) rectangle (%g,%g);" % (frame, X0 - 1, Y0 - 11, X1 + 1, Y1 + 1.5))
    o.append(r"\end{tikzpicture}")
    return "\n".join(o)


cells = []
for r in angles:
    L, X, lines = res[r]
    fr = "sbgreen" if r == best else ("sborange" if r == short else ("sbgray" if r == cur else None))
    cells.append(panel(r, L, X, lines, (r"%d\textdegree{} (oggi)" if r == cur else r"%d\textdegree") % r, fr))
if cur not in angles:
    L, X, lines = res_cur
    cells.append(panel(cur, L, X, lines, r"oggi: %d\textdegree" % cur, "sbgray"))
# legenda
leg = [r"\begin{tikzpicture}[font=\sffamily\tiny]"]
for i, (g, (col, _)) in enumerate(GROUPS.items()):
    leg.append(r"\draw[%s,line width=1pt] (0,-%.2f) -- (5mm,-%.2f); \node[anchor=west] at (5.5mm,-%.2f) {%s};" % (col, i * 0.38, i * 0.38, i * 0.38, g))
leg.append(r"\draw[sbgreen,line width=1.4pt] (0,-2.9) rectangle (5mm,-3.15); \node[anchor=west] at (5.5mm,-3.02) {meno incroci};")
leg.append(r"\draw[sborange,line width=1.4pt] (0,-3.4) rectangle (5mm,-3.65); \node[anchor=west] at (5.5mm,-3.52) {collegamenti più corti};")
leg.append(r"\fill[black] (2.5mm,-4.0) circle (0.6mm); \node[anchor=west] at (5.5mm,-4.0) {pin 1 dell'MCU};")
leg.append(r"\end{tikzpicture}")
cells.append("\n".join(leg))

rows = []
for i in range(0, len(cells), 4):
    rows.append("\n\\hfill\n".join(cells[i:i + 4]))
open(os.path.join(OUT, "fig_mcu_rot.tex"), "w", encoding="utf-8").write("\\par\\medskip\n".join(rows))

# ---------------------------------------------------------------- tabella
t = []
for r in angles:
    L, X, _ = res[r]
    mark = ""
    if r == best:
        mark = r"\textcolor{sbgreen}{\textbf{meno incroci}}"
    elif r == short:
        mark = r"\textcolor{sborange}{\textbf{più corta}}"
    if r == cur:
        mark = (mark + "; " if mark else "") + "posizione attuale nel PCB"
        t.append(r"\rowcolor{sbgraybg}\ang{%d} (oggi) & %.0f & %d & %s\\" % (r, L, X, mark))
    else:
        t.append(r"\ang{%d} & %.0f & %d & %s\\" % (r, L, X, mark))
if cur not in angles:
    L, X, _ = res_cur
    t.append(r"\rowcolor{sbgraybg}\ang{%d} (oggi) & %.0f & %d & posizione attuale nel PCB\\" % (cur, L, X))
open(os.path.join(OUT, "tab_mcu_rot.tex"), "w", encoding="utf-8").write("\n".join(t))

# rifinitura a 5 gradi intorno al migliore, per il testo
fine = sorted(((evaluate(a)[1], evaluate(a)[0], a) for a in range(best - 30, best + 31, 5)))
print("migliore", best, res[best][:2], "| più corta", short, res[short][:2], "| attuale", cur, res_cur[:2])
print("fine:", [(a, x, round(l)) for x, l, a in fine[:6]])
print("tutti:", [(a, evaluate(a)[1], round(evaluate(a)[0])) for a in range(0, 360, 45)])
