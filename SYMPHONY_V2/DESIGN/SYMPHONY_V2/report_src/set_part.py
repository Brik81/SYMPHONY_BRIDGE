# Set Value / Footprint / "JLCPCB Parts" on a symbol instance (adds the hidden field if missing).
# usage: python set_part.py file.kicad_sch REF VALUE FOOTPRINT JLCCODE   ("-" keeps the current value)
import re, sys
P, ref, val, fp, code = sys.argv[1:6]
t = open(P, encoding='utf-8', newline='').read()
i = t.index('"Reference" "%s"\r\n' % ref)
s = t.rindex('\n\t(symbol\r\n', 0, i) + 1
e = t.index('\n\t)\r\n', i) + 5
b = t[s:e]

def setp(b, name, v):
    return re.sub(r'\(property "%s" "[^"]*"' % re.escape(name), '(property "%s" "%s"' % (name, v), b, count=1)

if val != '-': b = setp(b, 'Value', val)
if fp != '-': b = setp(b, 'Footprint', fp)
if '(property "JLCPCB Parts"' in b:
    b = setp(b, 'JLCPCB Parts', code)
else:  # clone the hidden Footprint property block
    j = b.index('\t\t(property "Footprint"')
    blk = b[j:b.index('\r\n\t\t)\r\n', j) + 7]
    assert '(hide yes)' in blk
    new = re.sub(r'\(property "Footprint" "[^"]*"', '(property "JLCPCB Parts" "%s"' % code, blk, count=1)
    b = b[:j + len(blk)] + new + b[j + len(blk):]
assert b.count('(property "JLCPCB Parts"') == 1
t = t[:s] + b + t[e:]
assert t.replace('\r\n', '').count('\r') == 0  # no stray CR
open(P, 'w', encoding='utf-8', newline='').write(t)
print(ref, re.findall(r'\(property "(Value|Footprint|JLCPCB Parts)" "([^"]*)"', b))
