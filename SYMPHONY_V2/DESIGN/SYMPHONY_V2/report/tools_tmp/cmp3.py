import re, sys, os, unicodedata, subprocess
from collections import Counter
sys.stdout.reconfigure(encoding='utf8')
tmp = os.environ['TEMP']
def txt(pdf):
    out = subprocess.run(['pdftotext', '-enc', 'UTF-8', pdf, '-'], capture_output=True).stdout.decode('utf8', 'replace')
    out = unicodedata.normalize('NFKC', out).replace('\f', '\n')
    out = re.sub(r'pag\.\s*\d+(\s*di\s*\d+)?', ' ', out)
    out = re.sub(r'SYMPHONY V2\s*.\s*registro hardware', ' ', out)
    out = re.sub(r'rev\.\s*1\.4\d', ' ', out)
    out = re.sub(r'continua\s+sulla\s+pagina\s+seguente\s*\.{0,3}…?', ' ', out)
    k = [m.start() for m in re.finditer('Riepilogo del documento', out)]
    return out[k[1]:]
def chars(t):
    return Counter(re.sub(r'\s', '', t))
a = txt(os.path.join(tmp, 'before.pdf'))
b = txt(sys.argv[1])
ca, cb = chars(a), chars(b)
d = {k: (ca[k], cb[k]) for k in set(ca) | set(cb) if ca[k] != cb[k]}
print('char-count differences (prima, dopo):')
for k, v in sorted(d.items(), key=lambda kv: -abs(kv[1][0]-kv[1][1]))[:40]:
    print(repr(k), v)
