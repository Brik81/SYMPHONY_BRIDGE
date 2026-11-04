import re, glob, sys
LW = 495.0   # linewidth in pt (A4, margini 1.8 cm)
FS = {'scriptsize': 7.0, 'footnotesize': 8.0, 'small': 9.0, 'normalsize': 10.0}
FAC = float(sys.argv[1]) if len(sys.argv) > 1 else 0.56

hs = re.compile(r'>\{\\hsize=([\d.]+)\\hsize\\raggedright\\arraybackslash\}X')
envre = re.compile(r'\\begin\{(xltabular|tabularx)\}\{\\linewidth\}\{((?:>\{\\hsize=[\d.]+\\hsize\\raggedright\\arraybackslash\}X)+)\}')

def clean(c):
    c = re.sub(r'\\rowcolor\{[^}]*\}', '', c)
    c = re.sub(r'\\tg\{[^}]*\}\{([^}]*)\}', r'[\1]', c)
    c = c.replace('\\allowbreak{}', ' ').replace('\\allowbreak', ' ')
    c = re.sub(r'\\newline(\{\})?', ' ', c)
    c = c.replace('\\_', '_').replace('\\&', '&').replace('\\%', '%').replace('\\#', '#')
    c = re.sub(r'\\(textendash|textquotedblleft|textquotedblright|textperiodcentered|textasciitilde|ldots|textminus)(\{\})?', 'x', c)
    c = re.sub(r'\\(code|textbf|texttt|textit|emph|textsc)\b', '', c)
    c = re.sub(r'\\[A-Za-z]+\*?', 'x', c)
    c = re.sub(r'\\.', 'x', c)
    c = c.replace('{', ' ').replace('}', ' ').replace('$', '').replace('~', ' ')
    return c

def fontsize(s, pos):
    pre = s[max(0, pos - 400):pos]
    best = 'small'
    for m in re.finditer(r'\\(scriptsize|footnotesize|small|normalsize)\b', pre):
        best = m.group(1)
    return FS[best]

def process(s, fn, report):
    out = []
    last = 0
    for m in envre.finditer(s):
        env = m.group(1)
        end = s.index('\\end{%s}' % env, m.end())
        body = s[m.end():end]
        orig = [float(x) for x in hs.findall(m.group(2))]
        n = len(orig)
        fs = fontsize(s, m.start())
        # tabcolsep
        pre = s[max(0, m.start() - 400):m.start()]
        tc = 6.0
        mt = re.findall(r'\\tabcolsep\}\{([\d.]+)pt\}', pre)
        if mt:
            tc = float(mt[-1])
        avail = LW - 2 * tc * n
        need = [0.0] * n
        # drop header/footer controls
        b = re.sub(r'\\(end(?:first)?head|end(?:last)?foot|toprule|bottomrule|midrule(\[[^\]]*\])?)', '', body)
        b = re.sub(r'\\multicolumn\{\d+\}\{[^}]*\}\{.*?\}(?=\s*(\\\\|&|$))', '', b, flags=re.S)
        for row in re.split(r'\\\\(?:\[[^\]]*\])?', b):
            cells = row.split('&')
            if len(cells) != n:
                continue
            for i, c in enumerate(cells):
                raw = c
                c = clean(c)
                fac = FAC + (0.06 if re.search(r'\\code|\\texttt|\\textbf', raw) else 0.0)
                words = c.split()
                if words:
                    need[i] = max(need[i], max(len(w) for w in words) * fs * fac)
        wneed = [x / avail * n for x in need]
        w = [max(a, b2) for a, b2 in zip(orig, wneed)]
        # water-fill: shrink columns having slack so that sum == n
        for _ in range(50):
            tot = sum(w)
            if abs(tot - n) < 1e-4:
                break
            if tot < n:
                w = [x * n / tot for x in w]
                break
            slack = [max(0.0, x - nn) for x, nn in zip(w, wneed)]
            ssum = sum(slack)
            if ssum <= 1e-9:
                report.append((fn, 'INFEASIBLE', round(tot, 3), n))
                w = [x * n / tot for x in w]
                break
            red = min(1.0, (tot - n) / ssum)
            w = [x - sl * red for x, sl in zip(w, slack)]
        spec = ''.join('>{\\hsize=%.4f\\hsize\\raggedright\\arraybackslash}X' % x for x in w)
        out.append(s[last:m.start()])
        out.append('\\begin{%s}{\\linewidth}{%s}' % (env, spec))
        last = m.end()
    out.append(s[last:])
    return ''.join(out)

report = []
for fn in sorted(glob.glob('entries/*.tex')):
    s = open(fn, encoding='utf8', newline='').read()
    t = process(s, fn, report)
    if t != s:
        open(fn, 'w', encoding='utf8', newline='').write(t)
for r in report:
    print(r)
