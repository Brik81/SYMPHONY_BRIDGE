import pathlib
d = pathlib.Path(__file__).parent
p = d / 'symphony_version_log.html'
h = p.read_text(encoding='utf8')

def sub1(o, rep):
    global h
    assert h.count(o) == 1, o[:60]
    h = h.replace(o, rep)


sub1('symphony_version_log · rev. 1.29"', 'symphony_version_log · rev. 1.30"')
sub1("<div><b>1.29</b> del 02/11/2026",
     "<div><b>1.30</b> del 02/11/2026 – R-06/R-24 chiusi senza modifiche: il backup dell'RTC serve solo per pochi secondi</div><div>1.29 del 02/11/2026")
sub1('tr.r129 td {', 'tr.r130 td { background: #f3eef0 !important; }\ntr.r129 td {')
sub1('<li><a href="#partAB">Parte AB – Rev. 1.29: potenza TX (R-04) e note per il firmware</a></li>',
     '<li><a href="#partAB">Parte AB – Rev. 1.29: potenza TX (R-04) e note per il firmware</a></li>\n'
     '<li><a href="#partAC">Parte AC – Rev. 1.30: backup dell\'RTC (R-06, R-24)</a></li>')
sub1('salvia</span> = rev. 1.29,',
     'salvia</span> = rev. 1.29, righe <span style="background:#f3eef0;padding:0 2mm">malva</span> = rev. 1.30,')

REV = ('<tr class="r130"><td>1.30</td><td>problemi R-06 e R-24 della revisione indipendente del 27/10/2026<br>decisione di Brik81 del 02/11, registrata da Claude Code</td>'
       '<td>Nessuna modifica. Requisito fissato da Brik81: il backup dell\'RTC deve coprire solo pochi secondi senza alimentazione. Range −20…+60 °C del CPH3225A, assenza dal catalogo JLC e autonomia di circa 7 h accettati</td>'
       '<td>Claude Code</td><td><b>Brik81</b></td>'
       '<td>"temperatura non ti preoccuapre, mancanza su jlcpcb non ti preoccupare, 7h non ti preoccupare mi serve solo come salvataggio di backup nel caso di alimentazione assente quidni un lavoro di qualche secondo a stare larghi" (02/11)</td></tr>\n')
i = h.find('<h2>Registro revisioni</h2>'); j = h.find('</table>', i); h = h[:j] + REV + h[j:]
sub1('Rev. 1.29: nessun file di progetto modificato.',
     'Rev. 1.30: nessun file di progetto modificato. Rev. 1.29: nessun file di progetto modificato.')

rows = ('<tr class="r130"><td>1.30-01</td><td>MCU</td><td>C415–C424 (10× CPH3225A), D401, R412, U404</td>'
        '<td>R-06: CPH3225A specificato −20…+60 °C, non a catalogo JLC. R-24: autonomia ≈ 7 h (110 mF da 3,0 a 2,3 V con ≈ 3 µA)</td>'
        '<td>Nessuna modifica. Il requisito è di pochi secondi, quindi il margine è di molti ordini di grandezza (ne basterebbero già alcune decine di µF)</td>'
        '<td>R-06, R-24, §42</td><td>Brik81 · 02/11</td><td>—</td></tr>\n')
i = h.find('<h2>Registro modifiche</h2>'); j = h.find('</table>', i); h = h[:j] + rows + h[j:]

PART = """
<section class="part" id="partAC">
<div class="partlabel">Parte AC</div>
<h1 class="parttitle">Rev. 1.30 – Backup dell'RTC (R-06, R-24)</h1>
</section>
<h2 id="s42">42. Requisito del backup dell'RTC</h2>
<p>Brik81 ha fissato il requisito: il backup del DS3231M (U404) deve tenere l'ora solo per <b>pochi secondi</b> in caso di mancanza dell'alimentazione. Con 110 mF (10× CPH3225A) l'autonomia stimata è di circa 7 h, quindi il requisito è soddisfatto con un margine enorme. Il range −20…+60 °C del CPH3225A e la sua assenza dal catalogo JLC sono accettati. R-06 e R-24 sono chiusi senza modifiche.</p>
<p>Per riferimento: con ≈ 3 µA di consumo e una finestra 3,0 → 2,3 V, per 10 s bastano circa 43 µF. Il banco attuale è quindi molto sovradimensionato rispetto al requisito, ed è stato lasciato così per scelta.</p>
"""
sub1('\n</body></html>', PART + '\n</body></html>')
p.write_text(h, encoding='utf8')
print('ok')
