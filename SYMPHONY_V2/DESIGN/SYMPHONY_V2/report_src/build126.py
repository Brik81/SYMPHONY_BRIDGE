import pathlib
d = pathlib.Path(__file__).parent
p = d / 'symphony_version_log.html'
h = p.read_text(encoding='utf8')

def sub1(o, rep):
    global h
    assert h.count(o) == 1, o[:60]
    h = h.replace(o, rep)


sub1('symphony_version_log · rev. 1.25"', 'symphony_version_log · rev. 1.26"')
sub1("<div><b>1.25</b> del 30/10/2026",
     "<div><b>1.26</b> del 30/10/2026 – R-05: codici JLC di R206/R207, R202 e C35 corretti; R-22: datasheet di U701 (74AUP2G14 Diodes)</div><div>1.25 del 30/10/2026")
sub1('tr.r125 td {', 'tr.r126 td { background: #f1ecf8 !important; }\ntr.r125 td {')
sub1('<li><a href="#partX">Parte X – Rev. 1.25: choke del PA L242 = 1 µH e C260 = 27 pF (R-03, R-11)</a></li>',
     '<li><a href="#partX">Parte X – Rev. 1.25: choke del PA L242 = 1 µH e C260 = 27 pF (R-03, R-11)</a></li>\n'
     '<li><a href="#partY">Parte Y – Rev. 1.26: codici JLC (R-05) e datasheet U701 (R-22)</a></li>')
sub1('sabbia</span> = rev. 1.25,',
     'sabbia</span> = rev. 1.25, righe <span style="background:#f1ecf8;padding:0 2mm">lilla</span> = rev. 1.26,')

REV = ('<tr class="r126"><td>1.26</td><td>problemi R-05 e R-22 della revisione indipendente del 27/10/2026<br>R-05 corretto da Brik81 in KiCad (salvataggio 30/10 13:23), R-22 eseguito da Claude Code il 30/10</td>'
       '<td>R-05: i campi JLCPCB Parts di R206/R207, R202 e C35 ora corrispondono al valore. R-22: il campo Datasheet di U701 punta al datasheet Diodes 74AUP2G14, cioè al componente montato</td>'
       '<td>Brik81 (R-05) · Claude Code (R-22 e verifica)</td><td><b>Brik81</b></td>'
       '<td>"allora R-05 dovrebbero essere risolte tutte, fai tu R-22" (30/10)</td></tr>\n')
i = h.find('<h2>Registro revisioni</h2>'); j = h.find('</table>', i); h = h[:j] + REV + h[j:]
sub1('Rev. 1.25: <code>UHF.kicad_sch</code>',
     'Rev. 1.26: <code>UHF.kicad_sch</code> e <code>UHF_LIB/SYMBOL/IC.kicad_sym</code>, solo il campo Datasheet di 74AUP2G14 (copie precedenti in <code>report_src/bak_pre126/</code>). Rev. 1.25: <code>UHF.kicad_sch</code>')

rows = ('<tr class="r126"><td>1.26-01</td><td>IF</td><td>R206, R207 (JLCPCB Parts)</td>'
        '<td>C71617 = 10 kΩ, mentre il valore è 4k7</td><td>C25900 = 4,7 kΩ 0402 (già usato su R30/R32)</td>'
        '<td>R-05, §38</td><td>Brik81 · 30/10</td><td>Brik81 · 30/10 13:23 (verifica Claude Code)</td></tr>\n'
        '<tr class="r126"><td>1.26-02</td><td>UHF</td><td>R202 (JLCPCB Parts)</td>'
        '<td>C25779 = 33 kΩ, mentre il valore è 0R (serie su SHUT_DOWN dell\'LNA)</td><td>C17168 = 0 Ω 0402</td>'
        '<td>R-05, §38</td><td>Brik81 · 30/10</td><td>Brik81 · 30/10 13:23 (verifica Claude Code)</td></tr>\n'
        '<tr class="r126"><td>1.26-03</td><td>POWER</td><td>C35 (JLCPCB Parts)</td>'
        '<td>C1524 = 10 nF 50 V, mentre il valore è 100n</td><td>C1525 = 100 nF 16 V 0402</td>'
        '<td>R-05, §38</td><td>Brik81 · 30/10</td><td>Brik81 · 30/10 13:23 (verifica Claude Code)</td></tr>\n'
        '<tr class="r126"><td>1.26-04</td><td>UHF</td><td>U701 (Datasheet) e simbolo IC:74AUP2G14 in libreria</td>'
        '<td>https://www.ti.com/lit/ds/symlink/sn74lvc2g14.pdf (SN74LVC2G14 TI)</td>'
        '<td>https://www.diodes.com/assets/Datasheets/74AUP2G14.pdf. Il codice JLC C526337 è 74AUP2G14DW-7 Diodes SOT-363 (controllato su LCSC il 30/10). Valore, footprint e collegamenti invariati</td>'
        '<td>R-22, §38</td><td>Brik81 · 30/10</td><td>Claude Code · 30/10</td></tr>\n')
i = h.find('<h2>Registro modifiche</h2>'); j = h.find('</table>', i); h = h[:j] + rows + h[j:]

PART = """
<section class="part" id="partY">
<div class="partlabel">Parte Y</div>
<h1 class="parttitle">Rev. 1.26 – Codici JLC (R-05) e datasheet di U701 (R-22)</h1>
</section>
<h2 id="s38">38. Correzioni di BOM e documentazione</h2>
<ul>
<li><b>R-05.</b> Tre codici JLC non corrispondevano al valore: R206/R207 (4k7 con il codice di un 10 k), R202 (0R con il codice di un 33 k, che in serie a SHUT_DOWN poteva impedire lo spegnimento dell'LNA in TX) e C35 (100n con il codice di un 10 nF). Brik81 li ha corretti in KiCad. Claude Code ha riesportato la netlist e verificato i nuovi codici: C25900, C17168 e C1525.</li>
<li><b>R-22.</b> Il campo Datasheet di U701 (74AUP2G14, montato come Diodes 74AUP2G14DW-7, C526337) puntava al SN74LVC2G14 di TI. È stato aggiornato al datasheet Diodes 74AUP2G14 (URL verificato: risponde con un PDF), sia nelle tre unità dello schema sia nel simbolo di libreria <code>UHF_LIB/SYMBOL/IC.kicad_sym</code>, così KiCad non vede differenze fra i due. Il pinout era già lo stesso, quindi nulla cambia nel circuito.</li>
</ul>
<p><b>Verifica.</b> Netlist esportata prima e dopo la modifica di R-22: le reti sono identiche e U701 riporta il nuovo datasheet. R-05 e R-22 sono chiusi.</p>
"""
sub1('\n</body></html>', PART + '\n</body></html>')
p.write_text(h, encoding='utf8')
print('ok')
