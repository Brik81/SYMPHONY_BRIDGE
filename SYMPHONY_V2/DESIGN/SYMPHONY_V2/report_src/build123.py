import pathlib
d = pathlib.Path(__file__).parent
p = d / 'symphony_version_log.html'
h = p.read_text(encoding='utf8')

def sub1(o, rep):
    global h
    assert h.count(o) == 1, o[:60]
    h = h.replace(o, rep)


sub1('symphony_version_log · rev. 1.22"', 'symphony_version_log · rev. 1.23"')
sub1("<div><b>1.22</b> del 27/10/2026",
     "<div><b>1.23</b> del 27/10/2026 – S-11: D202 sull'I²C1 sostituito con un TVS a 5 V (PESD5V0L2BT)</div><div>1.22 del 27/10/2026")
sub1('tr.r122 td {', 'tr.r123 td { background: #eaf1fb !important; }\ntr.r122 td {')
sub1('<li><a href="#partU">Parte U – Rev. 1.22: etichetta EN_RX_LNA nel foglio MCU</a></li>',
     '<li><a href="#partU">Parte U – Rev. 1.22: etichetta EN_RX_LNA nel foglio MCU</a></li>\n'
     '<li><a href="#partV">Parte V – Rev. 1.23: protezione ESD dell\'I²C1 (S-11)</a></li>')
sub1('righe <span style="background:#f7f3e6;padding:0 2mm">sabbia</span> = rev. 1.22,',
     'righe <span style="background:#f7f3e6;padding:0 2mm">sabbia</span> = rev. 1.22, righe <span style="background:#eaf1fb;padding:0 2mm">celeste</span> = rev. 1.23,')
sub1('<tr><td>S-11</td><td>lasciato così</td><td>Pull-up I²C1 su JP201 volute (configurazione personalizzata). D202 ESD2CAN24: da verificare il motivo della scelta, per ora invariato.</td></tr>',
     '<tr><td>S-11</td><td><span class="tag done">chiuso v1.23</span></td><td>Pull-up I²C1 su JP201 volute (configurazione personalizzata). D202 sostituito con PESD5V0L2BT (§35).</td></tr>')

REV = ('<tr class="r123"><td>1.23</td><td>proposta da Claude Code e approvata 27/10/2026<br>eseguita da Claude Code il 27/10</td>'
       '<td>S-11: D202 (protezione ESD di SCL/SDA dell\'I2C1) passa da ESD2CAN24DBZRQ1, TVS per CAN a 24 V, a Nexperia PESD5V0L2BT,215 a 5 V. Stesso footprint SOT-23 e stessi pin</td>'
       '<td>Claude Code</td><td><b>Brik81</b></td>'
       '<td>"se va bene per la can va bene anche per la i2c?" → "ok, metti quello che consigli tu"</td></tr>\n')
i = h.find('<h2>Registro revisioni</h2>'); j = h.find('</table>', i); h = h[:j] + REV + h[j:]
sub1('Rev. 1.21: <code>CPH3225A.kicad_mod</code>',
     'Rev. 1.23: <code>IF.kicad_sch</code> prima della modifica salvato in <code>report_src/bak_pre123/</code>. Rev. 1.21: <code>CPH3225A.kicad_mod</code>')

rows = ('<tr class="r123"><td>1.23-01</td><td>IF</td><td>D202 (ESD su I2C1.SCL / I2C1.SDA)</td>'
        '<td>TI ESD2CAN24DBZRQ1, JLCPCB Parts C5736151: lavoro 24 V, tensione lasciata passare circa 35–37 V, 3 pF</td>'
        '<td>Nexperia <b>PESD5V0L2BT,215</b>, JLCPCB Parts <b>C12324</b>: 2 canali bidirezionali, lavoro 5 V, 75 pF. Footprint SOT-23-3 e pin invariati (1 SCL, 2 SDA, 3 GND). Aggiornati Datasheet e Description</td>'
        '<td>S-11, §35</td><td>Brik81 · 27/10</td><td>Claude Code · 27/10</td></tr>\n')
i = h.find('<h2>Registro modifiche</h2>'); j = h.find('</table>', i); h = h[:j] + rows + h[j:]

PART = """
<section class="part" id="partV">
<div class="partlabel">Parte V</div>
<h1 class="parttitle">Rev. 1.23 – Protezione ESD dell'I²C1 (S-11)</h1>
</section>
<h2 id="s35">35. D202: TVS per CAN o per I²C</h2>
<ul>
<li><b>Domanda.</b> "Se va bene per il CAN va bene anche per l'I²C?" No. ESD2CAN24 è fatto per il CAN, dove le linee devono reggere guasti fino a ±24 V senza che il diodo conduca: per questo interviene solo sopra circa 25 V e durante una scarica lascia salire la linea a circa 35–37 V.</li>
<li><b>Sull'I²C1.</b> SCL e SDA lavorano a 3,3 V e vanno ai pin 57 e 58 dell'STM32 (massimo circa 5,5 V) e ai connettori esterni J203 e J708. Con ESD2CAN24 la scarica veniva assorbita quasi tutta dalle protezioni interne dell'STM32: il diodo non faceva danni ma proteggeva poco.</li>
<li><b>Scelta.</b> Nexperia PESD5V0L2BT,215 (JLCPCB C12324): lavoro 5 V, sopra i 3,3 V del bus e sotto il massimo dei pin; 75 pF per linea, compatibile con il limite di 400 pF del bus I²C anche a 400 kHz. Stesso SOT-23 e stessa disposizione dei pin, nessun filo spostato. Scartato il TI TPD2E2U06 (1,5 pF): non disponibile in SOT-23 su JLCPCB.</li>
</ul>
<p><b>Verifica.</b> Netlist identica (D202 pin 1 = I2C1.SCL, pin 2 = I2C1.SDA, pin 3 = GND). ERC invariato (112). Con questa modifica S-11 è chiuso.</p>
"""
sub1('\n</body></html>', PART + '\n</body></html>')
p.write_text(h, encoding='utf8')
print('ok')
