import pathlib
d = pathlib.Path(__file__).parent
p = d / 'symphony_version_log.html'
h = p.read_text(encoding='utf8')

def sub1(o, rep):
    global h
    assert h.count(o) == 1, o[:60]
    h = h.replace(o, rep)


sub1('symphony_version_log · rev. 1.31"', 'symphony_version_log · rev. 1.32"')
sub1("<div><b>1.31</b> del 02/11/2026",
     "<div><b>1.32</b> del 02/11/2026 – R-07 chiuso senza modifiche: il TCXO Y201 resta ECS-TXO-20CSMV4-320-AY-TR (−30…+85 °C)</div><div>1.31 del 02/11/2026")
sub1('tr.r131 td {', 'tr.r132 td { background: #f5f0e6 !important; }\ntr.r131 td {')
sub1('<li><a href="#partAD">Parte AD – Rev. 1.31: pin non usati del connettore dock J708 (R-12)</a></li>',
     '<li><a href="#partAD">Parte AD – Rev. 1.31: pin non usati del connettore dock J708 (R-12)</a></li>\n'
     '<li><a href="#partAE">Parte AE – Rev. 1.32: TCXO Y201 (R-07)</a></li>')
sub1('ghiaccio</span> = rev. 1.31,',
     'ghiaccio</span> = rev. 1.31, righe <span style="background:#f5f0e6;padding:0 2mm">avorio</span> = rev. 1.32,')

REV = ('<tr class="r132"><td>1.32</td><td>problema R-07 della revisione indipendente del 27/10/2026<br>decisione di Brik81 del 02/11, registrata da Claude Code</td>'
       '<td>Nessuna modifica. Y201 resta ECS-TXO-20CSMV4-320-AY-TR (±0,5 ppm, −30…+85 °C). L\'alternativa Epson TG2016SMN (−40…+85 °C) è stata valutata e non adottata</td>'
       '<td>Claude Code</td><td><b>Brik81</b></td>'
       '<td>"A, lascia cosi perfavore" (02/11)</td></tr>\n')
i = h.find('<h2>Registro revisioni</h2>'); j = h.find('</table>', i); h = h[:j] + REV + h[j:]
sub1('Rev. 1.31: <code>IF.kicad_sch</code>',
     'Rev. 1.32: nessun file di progetto modificato. Rev. 1.31: <code>IF.kicad_sch</code>')

rows = ('<tr class="r132"><td>1.32-01</td><td>UHF</td><td>Y201 TCXO 32 MHz</td>'
        '<td>ECS-TXO-20CSMV4-320-AY-TR (C19858587): A = ±0,5 ppm, Y = −30…+85 °C (datasheet ECS, guida alla numerazione, pag. 1)</td>'
        '<td>Nessuna modifica, per decisione di Brik81</td>'
        '<td>R-07, §44</td><td>Brik81 · 02/11</td><td>—</td></tr>\n')
i = h.find('<h2>Registro modifiche</h2>'); j = h.find('</table>', i); h = h[:j] + rows + h[j:]

PART = """
<section class="part" id="partAE">
<div class="partlabel">Parte AE</div>
<h1 class="parttitle">Rev. 1.32 – TCXO Y201 (R-07)</h1>
</section>
<h2 id="s44">44. Range di temperatura del TCXO</h2>
<p>Il TCXO ECS-TXO-20CSMV4-320-<b>AY</b> è specificato fino a −30 °C. La versione −40 °C (-AN) a 32 MHz non risulta in vendita: ECS la offre solo a 19,2, 26, 50 e 52 MHz. È stata valutata come alternativa l'Epson TG2016SMN 32 MHz (X1G0054410305, C3007493): ±0,5 ppm da −40 a +85 °C, stesso package 2016. Richiederebbe però di lasciare aperto il pin 1, che è N.C. e non va collegato a GND (datasheet Epson ver. 1.3, pag. 14), mentre oggi è a GND, e di verificare il footprint.</p>
<p>Brik81 ha scelto di lasciare l'ECS -AY. Motivazione tecnica a supporto: sotto i −30 °C il TCXO continua a oscillare con una deriva di qualche ppm (≈ 1–2 kHz a 435 MHz), molto più piccola dello scostamento Doppler in orbita bassa (≈ ±10 kHz) che la stazione di terra insegue comunque; inoltre la scheda, dentro il satellite, difficilmente scende sotto −30 °C. Nota d'acquisto: al 02/11 su JLC c'erano solo 36 pezzi a stock.</p>
"""
sub1('\n</body></html>', PART + '\n</body></html>')
p.write_text(h, encoding='utf8')
print('ok')
