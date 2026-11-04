s = open('simphony_v2_log.tex', encoding='utf8').read()
s = s.replace('\\begin{document}', '\\AddToHook{shipout/before}{\\typeout{SHIPOUT \\thepage}}\n\\begin{document}', 1)
open('tmpdbg.tex', 'w', encoding='utf8').write(s)
