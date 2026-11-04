import pathlib
d = pathlib.Path(__file__).parent
p = d / 'symphony_version_log.html'
h = p.read_text(encoding='utf8')

def sub1(o, rep):
    global h
    assert h.count(o) == 1, o[:60]
    h = h.replace(o, rep)


sub1('symphony_version_log · rev. 1.23"', 'symphony_version_log · rev. 1.24"')
sub1("<div><b>1.23</b> del 27/10/2026",
     "<div><b>1.24</b> del 27/10/2026 – Revisione indipendente R-01/R-02: codici JLC di U301 (STM32L562RET6P) e IC1/IC5 (TLV9051IDBVR) corretti</div><div>1.23 del 27/10/2026")
sub1('tr.r123 td {', 'tr.r124 td { background: #eef7ea !important; }\ntr.r123 td {')
sub1('<li><a href="#partV">Parte V – Rev. 1.23: protezione ESD dell\'I²C1 (S-11)</a></li>',
     '<li><a href="#partV">Parte V – Rev. 1.23: protezione ESD dell\'I²C1 (S-11)</a></li>\n'
     '<li><a href="#partW">Parte W – Rev. 1.24: revisione indipendente, R-01 e R-02</a></li>')
sub1('righe <span style="background:#eaf1fb;padding:0 2mm">celeste</span> = rev. 1.23,',
     'righe <span style="background:#eaf1fb;padding:0 2mm">celeste</span> = rev. 1.23, righe <span style="background:#eef7ea;padding:0 2mm">verde chiaro</span> = rev. 1.24,')

REV = ('<tr class="r124"><td>1.24</td><td>problemi R-01/R-02 dalla revisione indipendente del 27/10/2026<br>corretti da Brik81 in KiCad il 27/10 (salvataggio 14:14), verificati da Claude Code il 27/10</td>'
       '<td>R-01: il codice JLC di U301 passa da STM32L562RET6 (LQFP64 standard, pinout diverso dal simbolo) a STM32L562RET6P, coerente con il simbolo RETxP. R-02: il codice JLC di IC1/IC5 passa da TLV9001UIDBVR (pinout "U" invertito) a TLV9051IDBVR</td>'
       '<td>Brik81 (modifica) · Claude Code (verifica)</td><td><b>Brik81</b></td>'
       '<td>"R-01 solved; R-02 solved; (controlla e conferma nella rev pdf in cui indichiamo rev per rev ogni modifica fatta)"</td></tr>\n')
i = h.find('<h2>Registro revisioni</h2>'); j = h.find('</table>', i); h = h[:j] + REV + h[j:]
sub1('Rev. 1.23: <code>IF.kicad_sch</code>',
     'Rev. 1.24: nessun file di progetto modificato da Claude Code (le modifiche le ha fatte Brik81 in KiCad); netlist prima e dopo nella cartella temporanea della sessione. Rev. 1.23: <code>IF.kicad_sch</code>')

rows = ('<tr class="r124"><td>1.24-01</td><td>MCU</td><td>U301 (campo JLCPCB Parts)</td>'
        '<td>C1236672 = <b>STM32L562RET6</b> (LQFP64 senza SMPS, Fig.14 DS12736 p.86): pinout diverso dal simbolo dal pin 25 al 30 e dal 54 al 62</td>'
        '<td>C1236664 = <b>STM32L562RET6P</b> (LQFP64 con SMPS esterno, Fig.16 p.87), coerente con simbolo e netlist. Valore, footprint e collegamenti invariati. Stock LCSC al 27/10: 0</td>'
        '<td>R-01, §36</td><td>Brik81 · 27/10</td><td>Brik81 · 27/10 14:14 (verifica Claude Code)</td></tr>\n'
        '<tr class="r124"><td>1.24-02</td><td>SENSORS</td><td>IC1, IC5 (campo JLCPCB Parts)</td>'
        '<td>C544301 = <b>TLV9001UIDBVR</b>: variante "U" con pinout 1 IN+, 2 V−, 3 IN−, 4 OUT, 5 V+ (TLV9001 Fig.6-2 p.7)</td>'
        '<td>C1849429 = <b>TLV9051IDBVR</b> (TI, SOT-23-5, stock 1879): pinout 1 OUT, 2 V−, 3 IN+, 4 IN−, 5 V+, uguale al simbolo (TLV9051 Tab.5-1 p.3)</td>'
        '<td>R-02, §36</td><td>Brik81 · 27/10</td><td>Brik81 · 27/10 14:14 (verifica Claude Code)</td></tr>\n')
i = h.find('<h2>Registro modifiche</h2>'); j = h.find('</table>', i); h = h[:j] + rows + h[j:]

PART = """
<section class="part" id="partW">
<div class="partlabel">Parte W</div>
<h1 class="parttitle">Rev. 1.24 – Revisione indipendente del 27/10: R-01 e R-02</h1>
</section>
<h2 id="s36">36. Correzione dei codici JLC di U301 e IC1/IC5</h2>
<p>La revisione indipendente del 27/10/2026 (file <code>SYMPHONY_V2_revisione_indipendente_2026-10-27.pdf</code> nella cartella DESIGN, fatta senza leggere questo registro) ha trovato due codici JLC che, montati, avrebbero reso inutilizzabile la scheda. Brik81 li ha corretti in KiCad. Claude Code ha riesportato la netlist con kicad-cli e controllato i nuovi codici sul catalogo LCSC.</p>
<ul>
<li><b>R-01 – U301.</b> Il simbolo è STM32L562RETxP (SMPS esterno, VDD12 sui pin 30 e 62), ma il codice era di un STM32L562RET6, che ha un pinout diverso dal pin 25 al 30 e dal 54 al 62 (I2C1, I2C2, SWO e BOOT0 su pin sbagliati, PH3-BOOT0 flottante). Il nuovo codice C1236664 è STM32L562RET6P. <span class="tag warn">Attenzione</span>: al 27/10 LCSC lo dà a stock 0, quindi va verificata la disponibilità prima dell'ordine.</li>
<li><b>R-02 – IC1, IC5.</b> Il codice era di un TLV9001UIDBVR: altro modello, con il pinout "U" in cui OUT è sul pin 4. Il nuovo C1849429 è TLV9051IDBVR, con lo stesso pinout DBV del simbolo.</li>
</ul>
<p><b>Verifica.</b> Netlist esportata dopo il salvataggio delle 14:14 e confrontata con quella della revisione indipendente: cambiano solo i campi JLCPCB Parts di U301, IC1 e IC5. Simboli, footprint, valori e collegamenti sono identici. R-01 e R-02 sono chiusi.</p>
"""
sub1('\n</body></html>', PART + '\n</body></html>')
p.write_text(h, encoding='utf8')
print('ok')
