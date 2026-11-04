import pathlib
d = pathlib.Path(__file__).parent
p = d / 'symphony_version_log.html'
h = p.read_text(encoding='utf8')

def sub1(o, rep):
    global h
    assert h.count(o) == 1, o[:60]
    h = h.replace(o, rep)


sub1('symphony_version_log · rev. 1.32"', 'symphony_version_log · rev. 1.33"')
sub1("<div><b>1.32</b> del 02/11/2026",
     "<div><b>1.33</b> del 02/11/2026 – R-16: ST del TPS2121 collegato a GND (Brik81); OV2 lasciato a GND per decisione</div><div>1.32 del 02/11/2026")
sub1('tr.r132 td {', 'tr.r133 td { background: #e9f3ee !important; }\ntr.r132 td {')
sub1('<li><a href="#partAE">Parte AE – Rev. 1.32: TCXO Y201 (R-07)</a></li>',
     '<li><a href="#partAE">Parte AE – Rev. 1.32: TCXO Y201 (R-07)</a></li>\n'
     '<li><a href="#partAF">Parte AF – Rev. 1.33: TPS2121, pin ST e OV2 (R-16)</a></li>')
sub1('avorio</span> = rev. 1.32,',
     'avorio</span> = rev. 1.32, righe <span style="background:#e9f3ee;padding:0 2mm">menta</span> = rev. 1.33,')

REV = ('<tr class="r133"><td>1.33</td><td>problema R-16 della revisione indipendente del 27/10/2026<br>ST collegato da Brik81 in KiCad (salvataggio 02/11 12:47), verificato da Claude Code</td>'
       '<td>ST (pin 9) di IC4 TPS2121 collegato a GND, come indica TI quando lo stato non serve. OV2 resta a GND (protezione da sovratensione sulla USB disattivata): a terra si usa solo un alimentatore da banco di qualità. La priorità assoluta al 5 V del dock (IN1) è confermata e invariata</td>'
       '<td>Brik81 (modifica) · Claude Code (verifica)</td><td><b>Brik81</b></td>'
       '<td>"ST connesso a gnd, verifica, OV2 dotn worry il nostro alimentatore è buono (500 euro da banco)" (02/11)</td></tr>\n')
i = h.find('<h2>Registro revisioni</h2>'); j = h.find('</table>', i); h = h[:j] + REV + h[j:]
sub1('Rev. 1.32: nessun file di progetto modificato.',
     'Rev. 1.33: nessun file di progetto modificato da Claude Code (ST collegato da Brik81 in POWER). Rev. 1.32: nessun file di progetto modificato.')

rows = ('<tr class="r133"><td>1.33-01</td><td>POWER</td><td>IC4 TPS2121, pin 9 ST</td>'
        '<td>Non collegato (rete unconnected-(IC4-ST-Pad9))</td>'
        '<td>Collegato alla linea GND con un filo e una giunzione, verso il pin GND 12 di IC4. Datasheet TI SLVSEA3F, Pin Functions: "Status output… Connect to GND if not required"</td>'
        '<td>R-16, §45</td><td>Brik81 · 02/11</td><td>Brik81 · 02/11 12:47 (verifica Claude Code)</td></tr>\n'
        '<tr class="r133"><td>1.33-02</td><td>POWER</td><td>IC4 TPS2121, pin 4 OV2</td>'
        '<td>A GND: supervisore di sovratensione su IN2 (VBUS USB) disattivato</td>'
        '<td>Nessuna modifica, per decisione di Brik81: a terra la USB viene alimentata solo da un alimentatore da banco affidabile. Sul dock (IN1) la protezione resta attiva a 6,02 V (R29/R30)</td>'
        '<td>R-16, §45</td><td>Brik81 · 02/11</td><td>—</td></tr>\n')
i = h.find('<h2>Registro modifiche</h2>'); j = h.find('</table>', i); h = h[:j] + rows + h[j:]

PART = """
<section class="part" id="partAF">
<div class="partlabel">Parte AF</div>
<h1 class="parttitle">Rev. 1.33 – TPS2121: pin ST e OV2 (R-16)</h1>
</section>
<h2 id="s45">45. Pin ST e OV2 del TPS2121</h2>
<p><b>ST.</b> È un'uscita open-drain che indica il canale attivo (alta = IN1, cioè il dock; bassa = IN2, cioè la USB). Era lasciata aperta. Non era un guasto, ma TI chiede di collegarla a GND se non serve. Brik81 l'ha collegata in KiCad alla linea GND che va al pin 12. Verifica: nella netlist esportata dopo il salvataggio delle 12:47 l'unica differenza rispetto alla rev 1.31 è IC4/9, passato dalla rete unconnected-(IC4-ST-Pad9) a GND. Controllato anche che il salvataggio non abbia toccato le modifiche delle rev 1.25–1.31.</p>
<p><b>OV2.</b> Il pin a GND disattiva il supervisore di sovratensione sull'ingresso USB. Brik81 ha deciso di lasciarlo così, perché la USB si usa solo a terra con un alimentatore da banco di qualità. Rischio residuo accettato: se un alimentatore guasto desse più di 5,5–6 V sulla USB, la tensione arriverebbe al 5V0, dove ci sono il buck TPSM863257 (che la regge) e la VDD del commutatore HMC349.</p>
<p>La priorità al 5 V del dock (IN1, tramite PR1 con R31/R32) è confermata da Brik81 come assoluta e resta invariata. R-16 è chiuso.</p>
"""
sub1('\n</body></html>', PART + '\n</body></html>')
p.write_text(h, encoding='utf8')
print('ok')
