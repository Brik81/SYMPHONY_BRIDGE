import re, sys, os, unicodedata, subprocess
from collections import Counter
sys.stdout.reconfigure(encoding='utf8')
tmp = os.environ['TEMP']
def txt(pdf):
    out = subprocess.run(['pdftotext', '-enc', 'UTF-8', pdf, '-'], capture_output=True).stdout.decode('utf8', 'replace')
    out = unicodedata.normalize('NFKC', out).replace('\f', '\n')
    out = re.sub(r'(?m)^pag\. ?\d+( di \d+)?$', '', out)
    out = re.sub(r'(?m)^SYMPHONY V2 . registro hardware$', '', out)
    out = re.sub(r'(?m)^rev\. 1\.4\d$', '', out)
    k = [m.start() for m in re.finditer('Riepilogo del documento', out)]
    return out[k[1]:]
def chars(t):
    # sequenza di soli caratteri alfanumerici, senza spazi/trattini/underscore: l'ordine dei blocchi delle tabelle cambia
    return Counter(re.sub(r'[^0-9A-Za-zÀ-ɏͰ-Ͽ]', '', t))
a = txt(os.path.join(tmp, 'before.pdf'))
b = txt(sys.argv[1])
ca, cb = chars(a), chars(b)
d = {k: (ca[k], cb[k]) for k in set(ca) | set(cb) if ca[k] != cb[k]}
print('char-count differences (prima, dopo):', d)
def words(t):
    return Counter(w for w in re.sub(r'[\-_]', '', t).split())
wa, wb = words(a), words(b)
miss = {k: wa[k] - wb[k] for k in wa if wa[k] > wb[k]}
extra = {k: wb[k] - wa[k] for k in wb if wb[k] > wa[k]}
print('parole solo nel vecchio:', len(miss), list(miss.items())[:40])
print('parole solo nel nuovo:', len(extra), list(extra.items())[:40])
