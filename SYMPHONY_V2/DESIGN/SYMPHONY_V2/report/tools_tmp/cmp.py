import subprocess, re, sys, unicodedata, difflib, os
tmp = os.environ['TEMP']
def txt(pdf):
    out = subprocess.run(['pdftotext', '-enc', 'UTF-8', pdf, '-'], capture_output=True).stdout.decode('utf8', 'replace')
    out = unicodedata.normalize('NFKC', out)
    out = out.replace('', '')
    out = out.replace('\f', '\n')
    out = re.sub(r'-\n(?=\S)', '', out)   # sillabazione a fine riga
    out = re.sub(r'(?m)^pag\. ?\d+( di \d+)?$', '', out)
    out = re.sub(r'(?m)^SYMPHONY V2 . registro hardware$', '', out)
    out = re.sub(r'(?m)^rev\. 1\.4\d$', '', out)
    return out
def body(t):
    k = [m.start() for m in re.finditer('Riepilogo del documento', t)]
    return t[k[1]:]
a = body(txt(os.path.join(tmp, 'before.pdf')))
b = body(txt(sys.argv[1]))
ta = [w.replace('-', '') for w in a.split()]
tb = [w.replace('-', '') for w in b.split()]
ta = [w for w in ta if w]
tb = [w for w in tb if w]
print(len(ta), len(tb))
sm = difflib.SequenceMatcher(None, ta, tb, autojunk=False)
n = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != 'equal':
        n += 1
        if n < 80:
            print(tag, ' '.join(ta[max(0,i1-3):i2+3])[:160], '=>', ' '.join(tb[max(0,j1-3):j2+3])[:160])
print('diff blocks', n)
