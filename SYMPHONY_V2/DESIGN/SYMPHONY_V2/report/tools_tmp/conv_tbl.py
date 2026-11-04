import re, glob
BS = chr(92)
pat = re.compile(r'p\{(?:\\cw\{([\d.]+)\}\{[\d.]+pt\}\{0pt\}|([\d.]+)\\linewidth)\}')
RA = r'>{\raggedright\arraybackslash}'

def spec_end(s, i):
    d = 0
    for j in range(i, len(s)):
        if s[j] == '{':
            d += 1
        elif s[j] == '}':
            d -= 1
            if d == 0:
                return j
    raise Exception

def conv(s, fn):
    out = []
    for m in re.finditer(r'\\begin\{(longtable|tabular)\}\{', s):
        env = m.group(1)
        st = m.end() - 1
        en = spec_end(s, st)
        spec = s[st + 1:en]
        if 'cw' not in spec and 'linewidth' not in spec:
            continue
        cols = pat.findall(spec)
        rest = pat.sub('', spec).replace(RA, '')
        if not cols or rest.strip():
            print('SKIP', fn, spec[:80])
            continue
        f = [float(a or b) for a, b in cols]
        n = len(f)
        t = sum(f)
        w = [x / t * n for x in f]
        newspec = ''.join(r'>{\hsize=%.4f\hsize\raggedright\arraybackslash}X' % x for x in w)
        out.append((m.start(), en, env, newspec, n))
    for (a, b, env, ns, n) in reversed(out):
        if env == 'longtable':
            e = s.index(r'\end{longtable}', b)
            body = s[b + 1:e]
            old = r'\bottomrule\endfoot'
            new = (r'\midrule[0.15pt]\multicolumn{%d}{r}{\footnotesize\itshape continua sulla pagina seguente\ldots}' % n
                   + BS + BS + r'\bottomrule\endfoot' + '\n' + r'\bottomrule\endlastfoot')
            if old not in body:
                print('NOFOOT', fn)
            body = body.replace(old, new)
            s = s[:a] + r'\begin{xltabular}{\linewidth}{' + ns + '}' + body + r'\end{xltabular}' + s[e + len(r'\end{longtable}'):]
        else:
            e = s.index(r'\end{tabular}', b)
            body = s[b + 1:e]
            s = s[:a] + r'\begin{tabularx}{\linewidth}{' + ns + '}' + body + r'\end{tabularx}' + s[e + len(r'\end{tabular}'):]
    return s

for fn in sorted(glob.glob('entries/*.tex')):
    s = open(fn, encoding='utf8', newline='').read()
    t = conv(s, fn)
    if t != s:
        open(fn, 'w', encoding='utf8', newline='').write(t)
        print('conv', fn)
