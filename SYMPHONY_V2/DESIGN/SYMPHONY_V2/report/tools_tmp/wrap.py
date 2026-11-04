import re
AB = r'\begin{adjustbox}{max width=\linewidth}'
AE = r'\end{adjustbox}'
def rd(f): return open(f, encoding='utf8', newline='').read()
def wr(f, s): open(f, 'w', encoding='utf8', newline='').write(s)

# 032: dentro la macro \modoAB
f = 'entries/032_parte-ag-rev-1-34.tex'; s = rd(f)
if 'adjustbox' not in s:
    s = s.replace(r'\begin{circuitikz}[scale=0.8', AB + r'\begin{circuitikz}[scale=0.8', 1)
    s = s.replace(r'\end{circuitikz}}', r'\end{circuitikz}' + AE + '}', 1)
    wr(f, s)
# 039, 036, 027, 010: attorno a ogni picture
for f, envs in [('entries/039_watchdog-stwd100-u403.tex', ['circuitikz']),
                ('entries/036_r17-shdn-tcan3414.tex', ['circuitikz']),
                ('entries/027_parte-ab-rev-1-29.tex', ['tikzpicture']),
                ('entries/010_parte-k-rev-1-12.tex', ['tikzpicture'])]:
    s = rd(f)
    if 'adjustbox' in s: continue
    for e in envs:
        s = s.replace('\\begin{%s}' % e, AB + '\\begin{%s}' % e)
        s = s.replace('\\end{%s}' % e, '\\end{%s}' % e + AE)
    wr(f, s)
