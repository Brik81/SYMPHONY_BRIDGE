import pathlib
d = pathlib.Path(__file__).parent
p = d / 'symphony_version_log.html'
h = p.read_text(encoding='utf8')

def sub1(o, rep):
    global h
    assert h.count(o) == 1, o[:60]
    h = h.replace(o, rep)


sub1('symphony_version_log · rev. 1.35"', 'symphony_version_log · rev. 1.36"')
sub1("<div><b>1.35</b> del 02/11/2026",
     "<div><b>1.36</b> del 02/11/2026 – R-14 chiuso senza modifiche: C39 resta 10 µF 0402 10 V</div><div>1.35 del 02/11/2026")
sub1('tr.r135 td {', 'tr.r136 td { background: #f2efe6 !important; }\ntr.r135 td {')
sub1('<li><a href="#partAH">Parte AH – Rev. 1.35: pull-up di I2C1 (R-13)</a></li>',
     '<li><a href="#partAH">Parte AH – Rev. 1.35: pull-up di I2C1 (R-13)</a></li>\n'
     '<li><a href="#partAI">Parte AI – Rev. 1.36: C39 sul 5 V del dock (R-14)</a></li>')
sub1('ardesia</span> = rev. 1.35,',
     'ardesia</span> = rev. 1.35, righe <span style="background:#f2efe6;padding:0 2mm">sabbia</span> = rev. 1.36,')

REV = ('<tr class="r136"><td>1.36</td><td>problema R-14 della revisione indipendente del 27/10/2026<br>decisione di Brik81 del 02/11, registrata da Claude Code</td>'
       '<td>Nessuna modifica. C39 (10 µF 0402 10 V X5R, C315248) resta sull\'ingresso 5 V del dock, accettando la perdita di capacità per polarizzazione DC</td>'
       '<td>Claude Code</td><td><b>Brik81</b></td>'
       '<td>"lascia com\'è, next" (02/11)</td></tr>\n')
i = h.find('<h2>Registro revisioni</h2>'); j = h.find('</table>', i); h = h[:j] + REV + h[j:]
sub1('Rev. 1.35: nessun file di progetto modificato.',
     'Rev. 1.36: nessun file di progetto modificato. Rev. 1.35: nessun file di progetto modificato.')

rows = ('<tr class="r136"><td>1.36-01</td><td>POWER</td><td>C39 (10 µF, rete 5V, IN1 di IC4)</td>'
        '<td>Samsung CL05A106MP5NUNC 0402 10 V X5R (C315248): con 5 V applicati la capacità effettiva è molto sotto il nominale (curva DC-bias non verificata)</td>'
        '<td>Nessuna modifica, per decisione di Brik81. Alternativa scartata: stesso componente di C38 (C15850, 0805 25 V)</td>'
        '<td>R-14, §48</td><td>Brik81 · 02/11</td><td>—</td></tr>\n')
i = h.find('<h2>Registro modifiche</h2>'); j = h.find('</table>', i); h = h[:j] + rows + h[j:]

PART = """
<section class="part" id="partAI">
<div class="partlabel">Parte AI</div>
<h1 class="parttitle">Rev. 1.36 – C39 sul 5 V del dock (R-14)</h1>
</section>
<h2 id="s48">48. C39 sull'ingresso IN1 del TPS2121</h2>
<p>C39 (10 µF 0402 10 V X5R, Samsung CL05A106MP5NUNC, LCSC C315248) e C40 (100 nF) filtrano la rete 5V del dock (J708 pin 1/3) all'ingresso IN1 (pin 7) del TPS2121 IC4. Un X5R 0402 da 10 V polarizzato a 5 V perde gran parte della capacità; la quantità non è stata verificata sulla curva DC-bias Samsung. Sull'ingresso VBUS c'è invece C38 (10 µF 0805 25 V, C15850). Lo schema funziona anche così: Brik81 ha deciso di lasciare C39 com'è. R-14 è chiuso.</p>
"""
sub1('\n</body></html>', PART + '\n</body></html>')
p.write_text(h, encoding='utf8')
print('ok')
