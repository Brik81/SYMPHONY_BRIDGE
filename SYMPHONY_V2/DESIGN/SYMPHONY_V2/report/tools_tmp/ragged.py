import re
RA = r'>{\raggedright\arraybackslash}'
def rd(f): return open(f, encoding='utf8', newline='').read()
def wr(f, s): open(f, 'w', encoding='utf8', newline='').write(s)
for f in ['entries/035_r18-precisione-pt1000.tex', 'entries/036_r17-shdn-tcan3414.tex', 'entries/038_r21-stock-c217-c218.tex']:
    s = rd(f)
    def fix(m):
        spec = m.group(0)
        return re.sub(r'(?<!arraybackslash\})p\{', lambda k: RA + 'p{', spec)
    s2 = re.sub(r'\\begin\{tabular\}\{[^\n]*\}', fix, s)
    if s2 != s:
        wr(f, s2)
f = 'entries/001_parte-b-analisi-e-modifiche.tex'
s = rd(f)
old = '\\subsection[12. Riferimenti]{12. Riferimenti}\n\n\\begin{itemize}\n'
assert old in s
s = s.replace(old, old + '\\raggedright\n', 1)
wr(f, s)
