"""Estrae dal .kicad_pcb: contorno, footprint (ref, valore, foglio, courtyard, pad con net)."""
import re, sys, json, math

t = open(sys.argv[1], encoding="utf-8").read()

def sexp_blocks(text, head):
    out, i = [], 0
    while True:
        i = text.find("(" + head, i)
        if i < 0:
            return out
        d, j = 0, i
        while True:
            c = text[j]
            if c == "(":
                d += 1
            elif c == ")":
                d -= 1
                if d == 0:
                    break
            elif c == '"':
                j = text.index('"', j + 1)
                while text[j - 1] == "\\":
                    j = text.index('"', j + 1)
            j += 1
        out.append(text[i:j + 1])
        i = j + 1

# contorno
edges = []
for kind in ("gr_line", "gr_arc"):
    for b in sexp_blocks(t, kind + "\n") + sexp_blocks(t, kind + " "):
        if "Edge.Cuts" not in b:
            continue
        s = re.search(r"\(start ([-\d.]+) ([-\d.]+)\)", b)
        e = re.search(r"\(end ([-\d.]+) ([-\d.]+)\)", b)
        m = re.search(r"\(mid ([-\d.]+) ([-\d.]+)\)", b)
        edges.append({"k": kind, "s": [float(s[1]), float(s[2])], "e": [float(e[1]), float(e[2])],
                      "m": [float(m[1]), float(m[2])] if m else None})

fps = []
for b in sexp_blocks(t, "footprint \""):
    name = re.match(r'\(footprint "([^"]+)"', b)[1]
    ref = re.search(r'\(property "Reference" "([^"]+)"', b)[1]
    val = re.search(r'\(property "Value" "([^"]*)"', b)[1]
    sh = re.search(r'\(sheetname "([^"]*)"', b)
    at = re.search(r'\n\t\t\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)', b)
    layer = re.search(r'\n\t\t\(layer "([^"]+)"', b)[1]
    # courtyard locale
    xs, ys = [], []
    for g in sexp_blocks(b, "fp_line") + sexp_blocks(b, "fp_rect") + sexp_blocks(b, "fp_circle") + sexp_blocks(b, "fp_poly"):
        if "CrtYd" not in g:
            continue
        for x, y in re.findall(r"\((?:start|end|xy|center|mid) ([-\d.]+) ([-\d.]+)\)", g):
            xs.append(float(x)); ys.append(float(y))
    pads = []
    for p in sexp_blocks(b, "pad \""):
        num = re.match(r'\(pad "([^"]*)"', p)[1]
        pa = re.search(r"\(at ([-\d.]+) ([-\d.]+)", p)
        sz = re.search(r"\(size ([-\d.]+) ([-\d.]+)\)", p)
        net = re.search(r'\(net (?:\d+ )?"([^"]*)"\)', p)
        pads.append({"n": num, "x": float(pa[1]), "y": float(pa[2]),
                     "w": float(sz[1]), "h": float(sz[2]), "net": net[1] if net else ""})
    fps.append({"ref": ref, "val": val, "fp": name, "sheet": sh[1] if sh else "",
                "x": float(at[1]), "y": float(at[2]), "r": float(at[3] or 0), "layer": layer,
                "cy": [min(xs), min(ys), max(xs), max(ys)] if xs else None, "pads": pads})

json.dump({"edges": edges, "fps": fps}, open(sys.argv[2], "w", encoding="utf-8"), indent=1)
print(len(edges), "segmenti di bordo,", len(fps), "footprint")
