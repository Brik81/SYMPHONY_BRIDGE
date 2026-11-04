import re, glob
pat = re.compile(r'(\\multicolumn\{\d+\}\{)>\{\\raggedright\\arraybackslash\}p\{\\cw\{[\d.]+\}\{[\d.]+pt\}\{[\d.]+pt\}\}(\})')
for f in glob.glob('entries/*.tex'):
    s = open(f, encoding='utf8', newline='').read()
    t = pat.sub(lambda m: m.group(1) + r'>{\raggedright\arraybackslash}X' + m.group(2), s)
    if t != s:
        open(f, 'w', encoding='utf8', newline='').write(t)
        print(f)
