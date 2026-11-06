"""Disegni "come si mette" per ogni blocco RF: pad, piste, via, nell'ordine della netlist.
Non sono in scala con la scheda: sono in scala tra loro (1 mm = SC mm sul foglio)."""
import os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
SC = 6.5  # mm sul foglio per mm reale

SIZES = {  # passo tra i centri dei pad, larghezza pad (lungo l'asse), altezza pad, corpo L, corpo W
    "0402": (1.0, 0.55, 0.6, 1.0, 0.5),
    "0603": (1.6, 0.85, 0.95, 1.6, 0.8),
    "0805": (1.9, 1.05, 1.4, 2.0, 1.25),
}
TW = 0.32   # larghezza pista 50 ohm indicativa
GAP = 0.7


class Fig:
    def __init__(self):
        self.L = []
        self.x = 0.0

    def w(self, s):
        self.L.append(s)

    # ---------------------------------------------------------- primitive
    def pad(self, x, y, w, h):
        self.w(r"\fill[cu] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (x - w / 2, y - h / 2, x + w / 2, y + h / 2))

    def track(self, x0, y0, x1, y1, wd=TW):
        self.w(r"\draw[tr,line width=%.3fmm] (%.3f,%.3f) -- (%.3f,%.3f);" % (wd * SC, x0, y0, x1, y1))

    def via(self, x, y):
        self.w(r"\draw[via] (%.3f,%.3f) circle (0.3); \fill[black!70] (%.3f,%.3f) circle (0.13);" % (x, y, x, y))

    def body(self, x0, y0, x1, y1):
        self.w(r"\draw[bod] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (x0, y0, x1, y1))

    def lab(self, x, y, txt, anchor="south", col="black"):
        self.w(r"\node[lbl,anchor=%s,text=%s] at (%.3f,%.3f) {%s};" % (anchor, col, x, y, txt))

    # ---------------------------------------------------------- elementi
    def start(self, label, length=1.6):
        self.lab(self.x - 0.15, 0, label, "east", "sbgray")
        self.track(self.x, 0, self.x + length, 0)
        self.x += length

    def series(self, ref, val, size):
        p, pw, ph, bl, bw = SIZES[size]
        x0 = self.x + pw / 2
        self.pad(x0, 0, pw, ph); self.pad(x0 + p, 0, pw, ph)
        self.body(x0 - bl / 2 + p / 2 - p / 2, -bw / 2, x0 + p / 2 + bl / 2, bw / 2)
        self.lab(x0 + p / 2, ph / 2 + 0.15, r"\textbf{%s}\\%s" % (ref, val))
        self.x = x0 + p + pw / 2
        self.track(self.x, 0, self.x + GAP, 0)
        self.x += GAP

    def node_shunt(self, items):
        """items: lista di (ref, val, size, 'up'|'down') sullo stesso nodo"""
        xs = self.x
        cur = xs
        for ref, val, size, d in items:
            p, pw, ph, bl, bw = SIZES[size]
            sgn = 1 if d == "up" else -1
            x = cur + ph / 2
            self.pad(x, 0, ph, pw)  # pad sulla pista (ruotato)
            yfar = sgn * p
            self.pad(x, yfar, ph, pw)
            self.body(x - bw / 2, min(0, yfar) - (bl - p) / 2, x + bw / 2, max(0, yfar) + (bl - p) / 2)
            yv = yfar + sgn * (pw / 2 + 0.38)
            self.via(x - 0.33, yv); self.via(x + 0.33, yv)
            self.lab(x + ph / 2 + 0.12, yfar / 2 + sgn * 0.2, r"\textbf{%s} %s" % (ref, val), "west")
            cur = x + ph / 2 + 0.25 + 1.9
        self.track(xs - 0.2, 0, cur - 0.5, 0)
        self.x = cur - 0.5
        self.track(self.x, 0, self.x + GAP, 0)
        self.x += GAP

    def feed(self, ref, val, size, caps, to="3V3", d="up"):
        """induttanza di alimentazione dal nodo verso il 3V3, con condensatori di disaccoppiamento"""
        p, pw, ph, bl, bw = SIZES[size] if size in SIZES else (2.0, 0.9, 2.2, 2.6, 2.6)
        sgn = 1 if d == "up" else -1
        half = max(ph, bw) / 2
        x = self.x + half
        self.track(self.x - 0.2, 0, x + half + 0.2, 0)
        self.pad(x, 0, ph, pw); self.pad(x, sgn * p, ph, pw)
        self.body(x - bw / 2, min(0, sgn * p) - (bl - p) / 2, x + bw / 2, max(0, sgn * p) + (bl - p) / 2)
        self.lab(x + half + 0.12, sgn * p / 2, r"\textbf{%s} %s" % (ref, val), "west")
        # binario 3V3: parte dall'induttanza; i condensatori verso massa pendono dal binario,
        # dal più piccolo (vicino all'induttanza) al più grande; in fondo la via verso il piano 3V3
        ytop = sgn * (p + pw / 2 + 0.9)
        self.track(x, sgn * p, x, ytop, 0.3)
        cx = x + 0.6
        for cref, cval, csize in caps:
            cp, cpw, cph, cbl, cbw = SIZES[csize]
            cx += cph / 2
            yfar = ytop + sgn * cp
            self.pad(cx, ytop, cph, cpw); self.pad(cx, yfar, cph, cpw)
            self.body(cx - cbw / 2, min(ytop, yfar) - (cbl - cp) / 2, cx + cbw / 2, max(ytop, yfar) + (cbl - cp) / 2)
            yv = yfar + sgn * (cpw / 2 + 0.38)
            self.via(cx - 0.33, yv); self.via(cx + 0.33, yv)
            self.lab(cx + max(cph, cbw) / 2 + 0.1, ytop + sgn * cp / 2, r"\textbf{%s} %s" % (cref, cval), "west")
            cx += max(cph, cbw) / 2 + 1.9
        self.track(x, ytop, cx, ytop, 0.3)
        self.via(cx + 0.3, ytop)
        self.lab(cx + 0.7, ytop, "via al piano 3V3 (In5)", "west", "sbred")
        self.track(x, 0, x + half + 2.0 + GAP, 0)
        self.x = x + half + 2.0
        self.x += GAP

    def ic(self, ref, txt, w, h, rfin=True, gndpads=0, ep=True, rfout=True):
        x0 = self.x
        self.w(r"\draw[bod,fill=black!5] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (x0, -h / 2, x0 + w, h / 2))
        if rfin:
            self.pad(x0 + 0.25, 0, 0.5, 0.28)
        if rfout:
            self.pad(x0 + w - 0.25, 0, 0.5, 0.28)
        if ep:
            e = min(w, h) * 0.45
            cx = x0 + w / 2
            self.w(r"\fill[sborange!45] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (cx - e / 2, -e / 2, cx + e / 2, e / 2))
            n = 3 if e > 1.4 else 2
            for i in range(n):
                for k in range(n):
                    self.via(cx - e / 2 + e * (i + 0.5) / n, -e / 2 + e * (k + 0.5) / n)
        for i in range(gndpads):
            gx = x0 + w * (i + 1) / (gndpads + 1)
            for s in (1, -1):
                self.pad(gx, s * (h / 2 - 0.2), 0.3, 0.5)
                self.via(gx, s * (h / 2 + 0.5))
        self.lab(x0 + w / 2, h / 2 + (0.9 if gndpads else 0.15), r"\textbf{%s}" % txt)
        self.x = x0 + w
        self.track(self.x, 0, self.x + GAP, 0)
        self.x += GAP

    def end(self, label):
        self.lab(self.x + 0.15, 0, label, "west", "sbgray")

    def emit(self, name, extra=""):
        s = ("\\begin{tikzpicture}[x=%.2fmm,y=%.2fmm,font=\\sffamily\\tiny]\n" % (SC, SC)
             + "\n".join(self.L) + "\n" + extra + "\n\\end{tikzpicture}")
        open(os.path.join(OUT, "blk_%s.tex" % name), "w", encoding="utf-8").write(s)


# ---------------------------------------------------------------- blocchi
def antenna():
    f = Fig()
    f.start("J201 (pin centrale)", 2.0)
    f.series("C206", "100p", "0603")
    f.ic("IC202", "IC202 switch (porta RFC)", 3.0, 3.0, rfout=False)
    f.x -= GAP
    f.emit("antenna")

def filtro_tx():
    f = Fig()
    f.start("dalla rete d'uscita del PA", 1.4)
    f.series("C230", "56p", "0603")
    f.ic("FL201", "FL201 LFCG-490+", 3.2, 2.5, gndpads=3, ep=False)
    f.series("C208", "100p", "0603")
    f.end("RF2 dello switch")
    f.emit("filtro_tx")

def uscita_pa():
    f = Fig()
    f.start("uscita del PA (pin 9--12)", 1.4)
    f.node_shunt([("C260", "27p", "0603", "down")])
    f.feed("L242", "1u", "NR20", [("C258", "47p", "0402"), ("C257", "1n", "0402"), ("C256", "10u", "0805")])
    f.series("L243", "2.7n", "0402")
    f.node_shunt([("C261", "22p", "0402", "down"), ("C262", "2p", "0402", "up")])
    f.series("C230", "56p", "0603")
    f.end("a FL201")
    f.emit("uscita_pa")

def alim_pa():
    f = Fig()
    f.start("3V3", 1.2)
    f.w("% binario di alimentazione")
    f.series("R240", "0", "0402")
    f.node_shunt([("C244", "330p", "0402", "down")])
    f.series("L240", "12n", "0603")
    f.end("VCC1 del PA (pin 1)")
    f.emit("alim_pa1")
    g = Fig()
    g.start("3V3", 1.2)
    g.series("R241", "0", "0603")
    g.node_shunt([("C248", "330p", "0402", "down")])
    g.series("L241", "6.8n", "0402")
    g.end("VCC2 del PA (pin 5--7)")
    g.emit("alim_pa2")

def attenuatore():
    f = Fig()
    f.start("da C701 (rete AN648)", 1.2)
    f.node_shunt([("R245", "100", "0603", "down")])
    f.series("R246", "68", "0603")
    f.node_shunt([("R247", "100", "0402", "down"), ("R248", "180", "0402", "up")])
    f.series("C255", "56p", "0603")
    f.end("RF IN del PA (pin 3)")
    f.emit("attenuatore")

def an648():
    f = Fig()
    f.start("TX del Si4464 (pin 4)", 1.4)
    f.feed("L703", "220n", "0603", [("C201", "100n", "0402")])
    f.series("C702", "9.1p", "0402")
    f.series("L702", "33n", "0805")
    f.node_shunt([("C704", "15p", "0402", "down")])
    f.series("C701", "100p", "0603")
    f.end("all'attenuatore")
    f.emit("an648")

def filtro_rx():
    f = Fig()
    f.start("RF1 dello switch", 1.4)
    f.series("C207", "100p", "0603")
    f.node_shunt([("C210", "6.8p", "0805", "down")])
    f.series("L201", "22n", "0805")
    f.node_shunt([("C209", "6.8p", "0805", "down")])
    f.series("C212", "100p", "0603")
    f.end("RF IN dell'LNA (pin 2)")
    f.emit("filtro_rx")

def lna():
    f = Fig()
    f.start("da C212", 1.2)
    f.ic("Q201", "Q201 LNA", 2.6, 2.6)
    f.feed("L202", "120n", "0402", [("C214", "100p", "0402"), ("C215", "1u", "0402")])
    f.series("C213", "100p", "0603")
    f.end("filtro dopo l'LNA")
    f.emit("lna")

def post_lna():
    f = Fig()
    f.start("da C213", 1.2)
    f.node_shunt([("C217", "5.6p", "0603", "down")])
    f.series("L203", "22n", "0805")
    f.node_shunt([("C216", "8.2p", "0805", "down")])
    f.series("L204", "22n", "0805")
    f.node_shunt([("C218", "5.6p", "0603", "down")])
    f.end("rete AN643")
    f.emit("post_lna")

def an643():
    """rete differenziale: disegnata a mano"""
    f = Fig()
    L = f.L
    f.lab(-0.15, 0, "da C218 (nodo RX\\_MATCH)", "east", "sbgray")
    f.track(0, 0, 1.2, 0)
    # biforcazione
    f.track(1.2, 0, 1.2, 1.6); f.track(1.2, 0, 1.2, -1.6)
    # ramo alto: C219 serie verso RXP
    f.track(1.2, 1.6, 1.8, 1.6)
    p, pw, ph, bl, bw = SIZES["0603"]
    f.pad(1.8 + pw / 2, 1.6, pw, ph); f.pad(1.8 + pw / 2 + p, 1.6, pw, ph)
    f.body(1.8 + pw / 2 + p / 2 - bl / 2, 1.6 - bw / 2, 1.8 + pw / 2 + p / 2 + bl / 2, 1.6 + bw / 2)
    f.lab(1.8 + pw / 2 + p / 2, 1.6 + ph / 2 + 0.1, r"\textbf{C219} 2.2p")
    xr = 1.8 + pw + p
    f.track(xr, 1.6, 8.6, 1.6)
    # ramo basso: L205 serie verso RXN
    f.track(1.2, -1.6, 1.8, -1.6)
    f.pad(1.8 + pw / 2, -1.6, pw, ph); f.pad(1.8 + pw / 2 + p, -1.6, pw, ph)
    f.body(1.8 + pw / 2 + p / 2 - bl / 2, -1.6 - bw / 2, 1.8 + pw / 2 + p / 2 + bl / 2, -1.6 + bw / 2)
    f.lab(1.8 + pw / 2 + p / 2, -1.6 - ph / 2 - 0.1, r"\textbf{L205} 56n", "north")
    f.track(xr, -1.6, 8.6, -1.6)
    # L206 tra RXP e RXN (verticale)
    x6 = 5.0
    f.pad(x6, 1.6, ph, pw); f.pad(x6, -1.6, ph, pw)
    f.body(x6 - bw / 2, -1.6 - 0.1, x6 + bw / 2, 1.6 + 0.1)
    f.lab(x6 + ph / 2 + 0.1, 0.4, r"\textbf{L206} 62n", "west")
    # C220 shunt su RXN
    x7 = 7.0
    p, pw, ph, bl, bw = SIZES["0805"]
    f.pad(x7, -1.6, ph, pw); f.pad(x7, -1.6 - p, ph, pw)
    f.body(x7 - bw / 2, -1.6 - p - (bl - p) / 2, x7 + bw / 2, -1.6 + (bl - p) / 2)
    yv = -1.6 - p - pw / 2 - 0.38
    f.via(x7 - 0.33, yv); f.via(x7 + 0.33, yv)
    f.lab(x7 - ph / 2 - 0.1, -1.6 - p / 2, r"\textbf{C220} 4.7p", "east")
    # Si4464
    f.w(r"\draw[bod,fill=black!5] (8.6,-2.6) rectangle (11.2,2.6);")
    f.pad(8.85, 1.6, 0.5, 0.28); f.pad(8.85, -1.6, 0.5, 0.28)
    f.lab(9.9, 2.65, r"\textbf{IC204 Si4464}")
    f.lab(9.15, 1.6, "RXP (2)", "west"); f.lab(9.15, -1.6, "RXN (3)", "west")
    f.emit("an643")

def si_tcxo():
    f = Fig()
    f.start("Y201 TCXO (uscita, pin 3)", 1.2)
    f.series("C204", "10n", "0402")
    f.series("R201", "33", "0402")
    f.end("XIN del Si4464 (pin 17), TP701 sul percorso")
    f.emit("tcxo")


# ------------------------------------------------ esempi giusto / sbagliato
def esempi():
    def panel(fn, title, ok):
        f = Fig()
        f.w(r"\useasboundingbox (-1.8,-4.3) rectangle (9.5,1.4);")
        fn(f)
        col = "sbgreen" if ok else "sbred"
        sym = r"\ding{51}" if ok else r"\ding{55}"
        f.w(r"\node[font=\sffamily\scriptsize\bfseries,text=%s,anchor=north west] at (-1.8,1.4) {%s %s};" % (col, sym, title))
        return f
    # 1 stub
    def stub_bad(f):
        f.track(0, 0, 6, 0); f.track(3, 0, 3, -1.6, 0.25)
        p, pw, ph, bl, bw = SIZES["0402"]
        f.pad(3, -1.6 - pw / 2, ph, pw); f.pad(3, -1.6 - pw / 2 - p, ph, pw)
        f.body(3 - bw / 2, -1.6 - pw / 2 - p - 0.2, 3 + bw / 2, -1.6 - pw / 2 + 0.2)
        f.via(3, -1.6 - pw / 2 - p - pw / 2 - 0.38)
        f.lab(3.4, -0.8, "stub", "west", "sbred")
    def stub_ok(f):
        f.track(0, 0, 6, 0)
        p, pw, ph, bl, bw = SIZES["0402"]
        f.pad(3, 0, ph, pw); f.pad(3, -p, ph, pw)
        f.body(3 - bw / 2, -p - 0.2, 3 + bw / 2, 0.2)
        f.via(2.67, -p - pw / 2 - 0.38); f.via(3.33, -p - pw / 2 - 0.38)
        f.lab(3.5, -0.5, "pad sulla pista", "west", "sbgreen")
    # 2 via lontana
    def via_bad(f):
        f.track(0, 0, 6, 0)
        p, pw, ph, bl, bw = SIZES["0402"]
        f.pad(3, 0, ph, pw); f.pad(3, -p, ph, pw); f.body(3 - bw / 2, -p - 0.2, 3 + bw / 2, 0.2)
        f.track(3, -p, 3, -3.2, 0.2); f.via(3, -3.5)
        f.lab(3.4, -2.4, "via lontana", "west", "sbred")
    def via_ok(f):
        f.track(0, 0, 6, 0)
        p, pw, ph, bl, bw = SIZES["0402"]
        f.pad(3, 0, ph, pw); f.pad(3, -p, ph, pw); f.body(3 - bw / 2, -p - 0.2, 3 + bw / 2, 0.2)
        f.via(2.67, -p - pw / 2 - 0.38); f.via(3.33, -p - pw / 2 - 0.38)
        f.lab(3.6, -1.3, "2 via attaccate al pad", "west", "sbgreen")
    # 3 ordine dei condensatori
    def dec(f, order, okc):
        f.w(r"\draw[bod,fill=black!5] (-1.4,-0.9) rectangle (0,0.9);")
        f.lab(-0.7, -0.95, "pin 3V3", "north")
        f.pad(-0.2, 0, 0.4, 0.3)
        f.track(0, 0, 7.6, 0, 0.3)
        x = 0.8
        for ref, val in order:
            p, pw, ph, bl, bw = SIZES["0402"]
            f.pad(x, 0, ph, pw); f.pad(x, -p, ph, pw); f.body(x - bw / 2, -p - 0.2, x + bw / 2, 0.2)
            f.via(x, -p - pw / 2 - 0.38)
            f.lab(x, 0.4, val)
            x += 2.2
        f.lab(7.7, 0, "verso il 3V3", "west", "sbred")
    def dec_ok(f): dec(f, [("", "100p"), ("", "10n"), ("", "1u")], True)
    def dec_bad(f): dec(f, [("", "1u"), ("", "10n"), ("", "100p")], False)
    # 4 induttanze
    def ind(f, perp):
        p, pw, ph, bl, bw = SIZES["0603"]
        f.track(0, 0, 1.4, 0)
        f.pad(1.4 + pw / 2, 0, pw, ph); f.pad(1.4 + pw / 2 + p, 0, pw, ph)
        f.body(1.4 + pw / 2 + p / 2 - bl / 2, -bw / 2, 1.4 + pw / 2 + p / 2 + bl / 2, bw / 2)
        f.w(r"\draw[sbgray,->] (1.6,0.9) -- (3.4,0.9);")
        x1 = 1.4 + pw + p
        if not perp:
            x2 = x1 + 0.6
            f.track(x1, 0, x2, 0)
            f.pad(x2 + pw / 2, 0, pw, ph); f.pad(x2 + pw / 2 + p, 0, pw, ph)
            f.body(x2 + pw / 2 + p / 2 - bl / 2, -bw / 2, x2 + pw / 2 + p / 2 + bl / 2, bw / 2)
            f.w(r"\draw[sbgray,->] (%.2f,0.9) -- (%.2f,0.9);" % (x2 + 0.2, x2 + 2.0))
            f.track(x2 + pw + p, 0, 8, 0)
            f.lab(4.0, -0.9, "in fila e vicine: i campi si sommano", "north", "sbred")
        else:
            xc = x1 + 1.2
            f.track(x1, 0, xc, 0); f.track(xc, 0, xc, -0.6)
            f.pad(xc, -0.6 - pw / 2, ph, pw); f.pad(xc, -0.6 - pw / 2 - p, ph, pw)
            f.body(xc - bw / 2, -0.6 - pw / 2 - p / 2 - bl / 2, xc + bw / 2, -0.6 - pw / 2 - p / 2 + bl / 2)
            f.w(r"\draw[sbgray,->] (%.2f,-0.5) -- (%.2f,-2.3);" % (xc + 0.8, xc + 0.8))
            f.track(xc, -0.6 - pw - p, xc, -3.6)
            f.lab(xc + 1.1, -1.4, r"girata di 90 gradi:\\i campi non si sommano", "west", "sbgreen")
    pairs = [("stub", stub_bad, stub_ok, "Condensatore verso massa: niente tratto di pista", ""),
             ("via", via_bad, via_ok, "Via di massa: subito accanto al pad", ""),
             ("dec", dec_bad, dec_ok, "Disaccoppiamento: il più piccolo vicino al pin", ""),
             ("ind", lambda f: ind(f, False), lambda f: ind(f, True), "Induttanze vicine: assi a 90 gradi", "")]
    for name, bad, good, title, _ in pairs:
        panel(bad, "sbagliato", False).emit("es_%s_no" % name)
        panel(good, "giusto", True).emit("es_%s_si" % name)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn in (antenna, filtro_tx, uscita_pa, alim_pa, attenuatore, an648, filtro_rx, lna, post_lna, an643, si_tcxo, esempi):
        fn()
    print("ok")
