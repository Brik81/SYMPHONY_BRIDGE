f = 'entries/001_parte-b-analisi-e-modifiche.tex'
s = open(f, encoding='utf8', newline='').read()
a = r'\multirow{2}{\hsize}{'
print(s.count(a))
s = s.replace(a, r'\multirow{2}{=}{', 1)
open(f, 'w', encoding='utf8', newline='').write(s)
