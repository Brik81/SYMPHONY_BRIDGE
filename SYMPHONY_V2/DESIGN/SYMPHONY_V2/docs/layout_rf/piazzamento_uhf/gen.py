"""Genera le figure TikZ in scala per il documento di piazzamento UHF.
Coordinate = coordinate KiCad (mm, y verso il basso)."""
import json, math, os, sys

SCR = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
d = json.load(open(os.path.join(SCR, "pcb.json"), encoding="utf-8"))
F = {f["ref"]: f for f in d["fps"]}

def rot(x, y, r):
    a = math.radians(r)
    return x * math.cos(a) + y * math.sin(a), -x * math.sin(a) + y * math.cos(a)

def tex(s):
    return s.replace("_", r"\_")

# ------------------------------------------------------------- proposta
IC = {  # ref: (x, y, rot)  posizione proposta
    "IC202": (121.45, 82.09, 0),
    "FL201": (130.25, 78.9, 180),
    "IC2":   (139.35, 78.9, 180),
    "Q201":  (130.7, 88.1, 0),
    "IC204": (144.0, 87.3, 180),
    "Y201":  (139.0, 89.7, 0),
}
FIX = {"J201": (F["J201"]["x"], F["J201"]["y"], 0)}

def pad_xy(ref, num, pos=None):
    f = F[ref]
    x0, y0, r = pos or IC.get(ref) or FIX[ref]
    for p in f["pads"]:
        if p["n"] == num:
            dx, dy = rot(p["x"], p["y"], r)
            return x0 + dx, y0 + dy
    raise KeyError(ref + num)

BLOCKS = [  # nome, x0, y0, x1, y1, stile, etichetta, posizione etichetta
    ("ANT", 108.6, 79.4, 118.1, 85.4, "neu", "J201 + C206", "c"),
    ("SW", 118.3, 78.4, 125.0, 84.2, "swb", "", "c"),
    ("C208", 125.2, 77.9, 128.3, 80.0, "txb", "C208", "n"),
    ("FL", 128.4, 77.2, 132.1, 80.6, "txb", "", "c"),
    ("OUT", 132.3, 76.7, 137.0, 83.4, "pab", "rete\\\\uscita\\\\PA", "s"),
    ("PASUP", 130.0, 71.4, 145.6, 76.4, "pas", "alimentazione del PA: L242, L240, L241, R240, R241, condensatori", "c"),
    ("PA", 137.2, 76.7, 141.5, 81.1, "pab", "", "c"),
    ("APC", 137.2, 81.3, 141.5, 83.6, "ctb", "APC", "c"),
    ("ATT", 141.7, 77.0, 147.0, 81.6, "txb", "attenuatore", "s"),
    ("AN648", 147.2, 77.0, 151.3, 86.4, "txb", "rete\\\\AN648", "c"),
    ("SI", 140.6, 84.0, 146.8, 90.4, "sib", "", "c"),
    ("TCXO", 136.4, 88.0, 140.4, 91.6, "ckb", "", "c"),
    ("AN643", 147.2, 87.4, 151.3, 93.6, "rxb", "rete\\\\AN643", "l"),
    ("RXF", 119.6, 84.6, 127.6, 89.8, "rxb", "filtro RX", "s"),
    ("LNA", 127.8, 85.4, 133.6, 90.8, "rxb", "", "c"),
    ("POST", 133.6, 92.0, 147.0, 96.4, "rxb", "filtro dopo l'LNA (C213, C217, L203, C216, L204, C218)", "c"),
]
HOLES = ["H302", "H304", "H305", "H306", "H307"]

def emit_band():
    L = []
    w = L.append
    w(r"\begin{tikzpicture}[x=3.25mm,y=-3.25mm,font=\sffamily\scriptsize]")
    # zona RF
    w(r"\fill[sblight!60] (108.05,70.72) rectangle (151.71,97.6);")
    w(r"\draw[sbgray,thick] (108.05,97.6) -- (108.05,84.17) -- (112.55,84.17) -- (112.55,80.67) -- (108.05,80.67) -- (108.06,71.72) -- (109.06,70.72) -- (150.71,70.72) -- (151.71,71.72) -- (151.71,97.6);")
    w(r"\draw[sbgray,densely dotted] (108.05,97.6) -- (151.71,97.6);")
    for h in HOLES:
        f = F[h]
        w(r"\filldraw[fill=white,draw=black!60,thick] (%.2f,%.2f) circle (2.15);" % (f["x"], f["y"]))
        w(r"\fill[black!50] (%.2f,%.2f) circle (1.1);" % (f["x"], f["y"]))
        w(r"\node[font=\sffamily\tiny\bfseries,fill=white,inner sep=0.5pt] at (%.2f,%.2f) {%s};" % (f["x"], f["y"] + (3.0 if f["y"] < 90 else 2.9), h))
    for name, x0, y0, x1, y1, st, lab, pos in BLOCKS:
        w(r"\draw[%s] (%.2f,%.2f) rectangle (%.2f,%.2f);" % (st, x0, y0, x1, y1))
        if lab:
            if pos == "c":
                w(r"\node[align=center,font=\sffamily\tiny,text width=%.1fmm] at (%.2f,%.2f) {%s};" % ((x1 - x0) * 3.25 - 1, (x0 + x1) / 2, (y0 + y1) / 2, lab))
            elif pos == "n":
                w(r"\node[align=center,font=\sffamily\tiny,anchor=south,inner sep=1pt] at (%.2f,%.2f) {%s};" % ((x0 + x1) / 2, y0, lab))
            elif pos == "l":
                w(r"\node[align=center,font=\sffamily\tiny,text width=%.1fmm] at (%.2f,%.2f) {%s};" % ((x1 - x0) * 3.25 - 4, (x0 + x1) / 2 - 0.5, (y0 + y1) / 2, lab))
            else:
                w(r"\node[align=center,font=\sffamily\tiny,anchor=south] at (%.2f,%.2f) {%s};" % ((x0 + x1) / 2, y1 - 0.1, lab))
    # IC in scala: corpo (courtyard) + pad
    for ref, (x, y, r) in list(IC.items()) + list(FIX.items()):
        f = F[ref]
        c = f["cy"] or [-1.3, -1.1, 1.3, 1.1]
        pts = [rot(px, py, r) for px, py in ((c[0], c[1]), (c[2], c[1]), (c[2], c[3]), (c[0], c[3]))]
        w(r"\draw[black!70,fill=white,fill opacity=0.85] " + " -- ".join("(%.2f,%.2f)" % (x + a, y + b) for a, b in pts) + " -- cycle;")
        for p in f["pads"]:
            if p["n"] == "" or (p["n"] in ("17", "21", "9") and ref in ("IC2", "IC204", "IC202", "Q201") and abs(p["x"]) < 0.6 and abs(p["y"]) < 0.6):
                continue
            px, py = rot(p["x"], p["y"], r)
            net = p["net"].split("/")[-1]
            col = "black!35"
            if net.startswith("RF_") and ("TX" in net or "PA" in net or "LPF" in net or "ATT" in net or net == "RF_SW_TX"):
                col = "sbred"
            if net in ("RF_SW_RX", "RF_LNA_IN", "RF_LNA_OUT", "RF_RX_P", "RF_RX_N"):
                col = "sbblue"
            if net in ("RF_ANT", "RF_SW_COM"):
                col = "sborange"
            if net in ("RF_TCXO_OUT", "RF_XIN"):
                col = "olive"
            sz = 0.45 if ref != "J201" else 1.0
            w(r"\fill[%s] (%.2f,%.2f) rectangle (%.2f,%.2f);" % (col, x + px - sz / 2, y + py - sz / 2, x + px + sz / 2, y + py + sz / 2))
        # pin 1
        p1 = next((p for p in f["pads"] if p["n"] == "1"), None)
        if p1 and ref != "J201":
            px, py = rot(p1["x"], p1["y"], r)
            w(r"\draw[black,thick] (%.2f,%.2f) circle (0.42);" % (x + px, y + py))
        name = {"IC202": "IC202\\\\switch", "FL201": "FL201", "IC2": "IC2\\\\PA", "Q201": "Q201\\\\LNA",
                "IC204": "IC204\\\\Si4464", "Y201": "Y201", "J201": "J201"}[ref]
        dy = {"Y201": 0.0, "J201": 0.0}.get(ref, 0.0)
        w(r"\node[align=center,font=\sffamily\tiny\bfseries] at (%.2f,%.2f) {%s};" % (x, y + dy, name))
    # percorsi del segnale
    j = pad_xy("J201", "1"); rfc = pad_xy("IC202", "3"); swtx = pad_xy("IC202", "8"); swrx = pad_xy("IC202", "5")
    flin = pad_xy("FL201", "8"); flout = pad_xy("FL201", "4")
    pain = pad_xy("IC2", "3"); paout = pad_xy("IC2", "10")
    sitx = pad_xy("IC204", "4"); sirxn = pad_xy("IC204", "3"); sirxp = pad_xy("IC204", "2")
    lin = pad_xy("Q201", "2"); lout = pad_xy("Q201", "7")
    yo = pad_xy("Y201", "3"); xin = pad_xy("IC204", "17")
    def path(style, pts):
        w(r"\draw[%s] " % style + " -- ".join("(%.2f,%.2f)" % p for p in pts) + ";")
    path("ant", [j, rfc])
    path("txa", [sitx, (148.4, sitx[1]), (148.4, 79.3), (pain[0] + 0.3, 79.3)])
    path("txa", [(paout[0] - 0.3, 78.9), (flin[0] + 0.3, 78.9)])
    path("txa", [(flout[0] - 0.3, 78.9), (swtx[0] + 0.6, 78.9), (swtx[0] + 0.6, swtx[1]), (swtx[0] + 0.25, swtx[1])])
    path("rxa", [(swrx[0] + 0.25, swrx[1]), (swrx[0] + 0.6, swrx[1]), (swrx[0] + 0.6, lin[1]), (lin[0] - 0.3, lin[1])])
    path("rxa", [(lout[0] + 0.3, lout[1]), (133.0, lout[1]), (133.0, 94.2), (150.7, 94.2), (150.7, sirxp[1] + 0.25), (sirxn[0] + 0.3, sirxp[1] + 0.25)])
    path("cka", [(yo[0] + 0.3, yo[1]), (xin[0], yo[1]), (xin[0], xin[1] + 0.3)])
    # fence di via
    w(r"\draw[fence] (125.2,84.4) -- (140.3,84.4);")
    w(r"\draw[fence] (137.05,76.6) -- (137.05,83.6); \draw[fence] (141.6,76.6) -- (141.6,83.6);")
    w(r"\draw[fence] (148.9,87.05) -- (151.3,87.05);")
    # corridoio digitale
    w(r"\draw[dig] (141.0,87.3) -- (139.2,87.3) -- (139.2,92.0) node[pos=0.0,above left,text=violet,align=right,inner sep=1pt]{};")
    w(r"\draw[dig] (139.2,96.4) -- (139.2,99.0);")
    w(r"\node[text=violet,anchor=north,align=center,font=\sffamily\tiny] at (139.2,99.1) {SPI, nIRQ, SDN: via su In4 verso l'MCU};")
    # quote
    pa = IC["IC2"]; ln = IC["Q201"]; y = IC["Y201"]
    dpa_ln = math.dist(pa[:2], ln[:2]); dpa_y = math.dist(pa[:2], y[:2])
    w(r"\draw[dimq] (%.2f,%.2f) -- (%.2f,%.2f) node[midway,fill=white,inner sep=0.5pt,text=sbred]{%.1f mm};" % (pa[0] - 1.2, pa[1] + 1.4, ln[0] + 1.0, ln[1] - 1.0, dpa_ln))
    w(r"\draw[dimq] (%.2f,%.2f) -- (%.2f,%.2f) node[pos=0.55,fill=white,inner sep=0.5pt,text=sbred]{%.1f mm};" % (pa[0] - 0.4, pa[1] + 2.4, y[0] - 0.2, y[1] - 1.0, dpa_y))
    w(r"\end{tikzpicture}")
    open(os.path.join(OUT, "fig_proposta.tex"), "w", encoding="utf-8").write("\n".join(L))
    return dpa_ln, dpa_y

def emit_board():
    L = []; w = L.append
    w(r"\begin{tikzpicture}[x=2.0mm,y=-2.0mm,font=\sffamily\scriptsize]")
    w(r"\fill[sblight!70] (108.05,70.72) rectangle (151.71,97.6);")
    w(r"\fill[sbgraybg] (109.0,100.8) rectangle (127.6,111.0);")
    w(r"\node[align=center,font=\sffamily\tiny,text=sbgray] at (118.3,105.9) {zona dei comandi\\(IC205, Q701, U701,\\D203, test point)};")
    w(r"\node[align=center,font=\sffamily\small\bfseries,text=sbblue] at (131.5,90.0) {ZONA RF};")
    w(r"\node[align=center,font=\sffamily\tiny,text=sbblue] at (131.5,93.0) {circa 43 $\times$ 26 mm};")
    w(r"\draw[black,thick] (108.05,84.17) -- (112.55,84.17) -- (112.55,80.67) -- (108.05,80.67) -- (108.06,71.72) -- (109.06,70.72) -- (150.71,70.72) -- (151.71,71.72) -- (151.71,144.56) -- (150.71,145.56) -- (122.16,145.56) -- (120.17,143.57) -- (120.17,139.50) -- (118.17,137.50) -- (110.06,137.50) -- (108.06,135.49) -- cycle;")
    for h in ["H301", "H302", "H303", "H304", "H305", "H306", "H307", "H308"]:
        f = F[h]
        w(r"\filldraw[fill=white,draw=black!60] (%.2f,%.2f) circle (2.15); \fill[black!50] (%.2f,%.2f) circle (1.1);" % (f["x"], f["y"], f["x"], f["y"]))
        w(r"\node[font=\sffamily\tiny,anchor=%s] at (%.2f,%.2f) {%s};" % ("west" if f["x"] < 140 else "east", f["x"] + (2.4 if f["x"] < 140 else -2.4), f["y"], h))
    def rect(ref, style, label, wh=None):
        f = F[ref]; c = f["cy"]; r = f["r"]
        pts = [rot(px, py, r) for px, py in ((c[0], c[1]), (c[2], c[1]), (c[2], c[3]), (c[0], c[3]))]
        w(r"\draw[%s] " % style + " -- ".join("(%.2f,%.2f)" % (f["x"] + a, f["y"] + b) for a, b in pts) + " -- cycle;")
        w(r"\node[align=center,font=\sffamily\tiny] at (%.2f,%.2f) {%s};" % (f["x"], f["y"], label))
    rect("J201", "thick,fill=sborangebg,draw=sborange", "J201")
    rect("U301", "thick,fill=white,draw=sbblue", "U301\\\\MCU")
    rect("J708", "thick,dashed,fill=white,fill opacity=0.6,draw=sbgray,text opacity=1", "J708 dock\\\\(lato B)")
    rect("J15", "thick,fill=white,draw=sbgray", "J15\\\\USB-C")
    rect("J202", "thick,fill=white,draw=sbgray", "J202 CAN")
    rect("J203", "thick,fill=white,draw=sbgray", "J203 I2C")
    w(r"\draw[sbblue2,thick,densely dashed] (108.05,97.6) -- (151.71,97.6);")
    w(r"\end{tikzpicture}")
    open(os.path.join(OUT, "fig_scheda.tex"), "w", encoding="utf-8").write("\n".join(L))

def emit_pinout():
    """Zoom degli IC con l'orientamento proposto: pad numerati e net."""
    L = []; w = L.append
    show = [("IC202", "IC202 HMC349A (switch) \\textendash{} rotazione 0\\textdegree", 7.0),
            ("IC204", "IC204 Si4464 \\textendash{} rotazione 180\\textdegree", 6.0),
            ("IC2", "IC2 QPA9510 (PA) \\textendash{} rotazione 180\\textdegree", 7.0),
            ("Q201", "Q201 TQP3M9036 (LNA) \\textendash{} rotazione 0\\textdegree", 9.0),
            ("FL201", "FL201 LFCG-490+ \\textendash{} rotazione 180\\textdegree", 9.0)]
    short = {"RF_SW_COM": "RFC (antenna)", "RF_SW_TX": "RF2 = TX", "RF_SW_RX": "RF1 = RX", "UHF.EN_TX_ANT_SW": "CTRL (PC2)",
             "5V0": "VDD 5V0", "RF_RX_P": "RXP", "RF_RX_N": "RXN", "RF_SI_TX": "TX", "RF_SDN": "SDN", "RF_XIN": "XIN",
             "SPI1.CLK": "SCK", "SPI1.MISO": "MISO", "SPI1.MOSI": "MOSI", "SPI1.CS": "NSEL", "UHF.RF_IRQ": "nIRQ",
             "RF_PA_IN": "RF IN", "RF_PA_OUT": "RF OUT", "PA_VCC1": "VCC1", "PA_VCC2": "VCC2", "Net-(IC2-APC1)": "APC",
             "RF_LNA_IN": "RF IN", "RF_LNA_OUT": "RF OUT", "Net-(Q201-SHUT_DOWN)": "SD", "RF_LPF_IN": "IN (dal PA)",
             "RF_LPF_OUT": "OUT (allo switch)", "3V3": "3V3"}
    for ref, title, sc in show:
        f = F[ref]; r = IC[ref][2]; c = f["cy"]
        w(r"\begin{tikzpicture}[x=%.1fmm,y=-%.1fmm,font=\sffamily\tiny,baseline=(t.base)]" % (sc, sc))
        pts = [rot(px, py, r) for px, py in ((c[0], c[1]), (c[2], c[1]), (c[2], c[3]), (c[0], c[3]))]
        bx = max(abs(p["x"]) for p in f["pads"]) ; by = max(abs(p["y"]) for p in f["pads"])
        b = [rot(px, py, r) for px, py in ((-bx, -by), (bx, -by), (bx, by), (-bx, by))]
        w(r"\draw[black,thick,fill=black!6] " + " -- ".join("(%.3f,%.3f)" % p for p in b) + " -- cycle;")
        done = set()
        for p in f["pads"]:
            if (p["n"], p["x"], p["y"]) in done:
                continue
            done.add((p["n"], p["x"], p["y"]))
            px, py = rot(p["x"], p["y"], r)
            pw, ph = (p["w"], p["h"]) if r % 180 == 0 else (p["h"], p["w"])
            net = p["net"].split("/")[-1]
            col = "black!40"
            if net in ("RF_SW_TX", "RF_SI_TX", "RF_PA_IN", "RF_PA_OUT", "RF_LPF_IN", "RF_LPF_OUT"): col = "sbred"
            if net in ("RF_SW_RX", "RF_RX_P", "RF_RX_N", "RF_LNA_IN", "RF_LNA_OUT"): col = "sbblue"
            if net in ("RF_SW_COM",): col = "sborange"
            if net in ("RF_XIN",): col = "olive"
            if net.startswith("SPI") or net in ("UHF.RF_IRQ", "UHF.EN_TX_ANT_SW", "RF_SDN", "Net-(Q201-SHUT_DOWN)", "Net-(IC2-APC1)"): col = "violet"
            if abs(p["x"]) < 0.6 and abs(p["y"]) < 0.6 and p["n"] in ("9", "17", "21"):
                continue
            w(r"\fill[%s] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (col, px - pw / 2, py - ph / 2, px + pw / 2, py + ph / 2))
            if net in short:
                # etichetta verso l'esterno
                ang = math.atan2(py, px)
                ax, ay = px + 0.55 * math.cos(ang) / max(abs(math.cos(ang)), abs(math.sin(ang))), py + 0.55 * math.sin(ang) / max(abs(math.cos(ang)), abs(math.sin(ang)))
                anc = "west" if abs(px) >= abs(py) and px > 0 else "east" if abs(px) >= abs(py) else ("north" if py > 0 else "south")
                key = (anc, round(px, 1) if anc in ("north", "south") else round(py, 1))
                if key in done:
                    continue
                done.add(key)
                if anc in ("north", "south"):
                    w(r"\node[anchor=%s,rotate=90,anchor=%s,text=%s] at (%.3f,%.3f) {%s %s};" % (anc, "east" if anc == "north" else "west", col if col != "black!40" else "black", px, py + ((ph / 2 + 0.2) if anc == "north" else -(ph / 2 + 0.2)), p["n"], short[net]))
                else:
                    w(r"\node[anchor=%s,text=%s] at (%.3f,%.3f) {%s %s};" % (anc, col if col != "black!40" else "black", px + ((pw / 2 + 0.2) if anc == "west" else -(pw / 2 + 0.2)), py, p["n"], short[net]))
        p1 = next(p for p in f["pads"] if p["n"] == "1")
        px, py = rot(p1["x"], p1["y"], r)
        w(r"\draw[black,thick] (%.3f,%.3f) circle (0.25);" % (px, py))
        w(r"\node[anchor=north,font=\sffamily\scriptsize\bfseries,align=center] (t) at (0,%.2f) {%s};" % (max(abs(q) for q in (c[1], c[3], c[0], c[2])) + 1.9, title))
        w(r"\end{tikzpicture}")
        w("%%SEP")
    open(os.path.join(OUT, "fig_pinout.tex"), "w", encoding="utf-8").write("\n".join(L))

# controllo sovrapposizioni tra blocchi e con i fori
def check():
    bad = []
    B = [(n, x0, y0, x1, y1) for n, x0, y0, x1, y1, *_ in BLOCKS if n != "PASUP"]
    for i in range(len(B)):
        for k in range(i + 1, len(B)):
            a, b = B[i], B[k]
            if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
                bad.append(("blocchi", a[0], b[0]))
    for n, x0, y0, x1, y1, *_ in BLOCKS:
        for h in HOLES:
            hx, hy = F[h]["x"], F[h]["y"]
            cx = min(max(hx, x0), x1); cy = min(max(hy, y0), y1)
            if math.hypot(cx - hx, cy - hy) < 2.15 + 0.2:
                bad.append(("foro", n, h, round(math.hypot(cx - hx, cy - hy), 2)))
        if x0 < 108.05 + 0.3 and n != "ANT" or x1 > 151.71 - 0.3 or y0 < 70.72 + 0.3:
            bad.append(("bordo", n))
    # IC dentro il proprio blocco
    owner = {"IC202": "SW", "FL201": "FL", "IC2": "PA", "Q201": "LNA", "IC204": "SI", "Y201": "TCXO"}
    for ref, bn in owner.items():
        x, y, r = IC[ref]; c = F[ref]["cy"] or [-1.3, -1.1, 1.3, 1.1]
        pts = [rot(px, py, r) for px, py in ((c[0], c[1]), (c[2], c[3]))]
        xs = [x + p[0] for p in pts]; ys = [y + p[1] for p in pts]
        b = next(bb for bb in BLOCKS if bb[0] == bn)
        if min(xs) < b[1] - 0.01 or max(xs) > b[3] + 0.01 or min(ys) < b[2] - 0.01 or max(ys) > b[4] + 0.01:
            bad.append(("IC fuori dal blocco", ref, [round(min(xs), 2), round(min(ys), 2), round(max(xs), 2), round(max(ys), 2)], b[1:5]))
    return bad

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print("problemi:", check())
    print("distanze PA-LNA, PA-TCXO: %.1f %.1f" % emit_band())
    emit_board(); emit_pinout()
    j = pad_xy("J201", "1"); lin = pad_xy("Q201", "2"); rfc = pad_xy("IC202", "3"); swrx = pad_xy("IC202", "5")
    print("J201->LNA (percorso a L): %.1f mm" % (math.dist(j, rfc) + abs(lin[0] - swrx[0]) + abs(lin[1] - swrx[1])))
    for ref in IC:
        print(ref, IC[ref], "attuale:", F[ref]["x"], F[ref]["y"], F[ref]["r"])
