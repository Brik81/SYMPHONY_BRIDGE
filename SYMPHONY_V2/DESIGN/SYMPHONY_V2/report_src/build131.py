import pathlib
d = pathlib.Path(__file__).parent
p = d / 'symphony_version_log.html'
h = p.read_text(encoding='utf8')

def sub1(o, rep):
    global h
    assert h.count(o) == 1, o[:60]
    h = h.replace(o, rep)


sub1('symphony_version_log · rev. 1.30"', 'symphony_version_log · rev. 1.31"')
sub1("<div><b>1.30</b> del 02/11/2026",
     "<div><b>1.31</b> del 02/11/2026 – R-12: +12V, +3V3_CONN e RS485 di J708 non usati per scelta, nota sullo schema IF</div><div>1.30 del 02/11/2026")
sub1('tr.r130 td {', 'tr.r131 td { background: #eaf0f7 !important; }\ntr.r130 td {')
sub1('<li><a href="#partAC">Parte AC – Rev. 1.30: backup dell\'RTC (R-06, R-24)</a></li>',
     '<li><a href="#partAC">Parte AC – Rev. 1.30: backup dell\'RTC (R-06, R-24)</a></li>\n'
     '<li><a href="#partAD">Parte AD – Rev. 1.31: pin non usati del connettore dock J708 (R-12)</a></li>')
sub1('malva</span> = rev. 1.30,',
     'malva</span> = rev. 1.30, righe <span style="background:#eaf0f7;padding:0 2mm">ghiaccio</span> = rev. 1.31,')

REV = ('<tr class="r131"><td>1.31</td><td>problema R-12 della revisione indipendente del 27/10/2026<br>decisione di Brik81 del 02/11, nota eseguita da Claude Code</td>'
       '<td>J708 segue il pinout standard del dock. +12V, +3V3_CONN (3V3 generato a bordo nel foglio POWER) e RS485.A1/B1 non sono usati su questa scheda: restano con le loro etichette e senza collegamenti. Aggiunta una nota di testo accanto a J708 nel foglio IF. Nessun no-connect sui pin: in KiCad un no-connect su un pin che ha anche un\'etichetta è un conflitto</td>'
       '<td>Claude Code</td><td><b>Brik81</b></td>'
       '<td>"R-12 si perche il connettore è standard, ma in quiesto caso noi abbiamo che sulla board i 12V non sono usati, i 3v3_conn non sono usati perche venogono prodottti internametne nel shieet power infatti i 5V sono connessi, idem per rs485 per ora non usati ma no problem, se vuoi lasciarli con la label ma mettere il connettore NC a me sta bene" (02/11)</td></tr>\n')
i = h.find('<h2>Registro revisioni</h2>'); j = h.find('</table>', i); h = h[:j] + REV + h[j:]
sub1('Rev. 1.30: nessun file di progetto modificato.',
     'Rev. 1.31: <code>IF.kicad_sch</code>, solo una nota di testo (copia precedente in <code>report_src/bak_pre131/</code>). Rev. 1.30: nessun file di progetto modificato.')

rows = ('<tr class="r131"><td>1.31-01</td><td>IF</td><td>J708 (FSI-110-03-G-D-AB), pin 2/4 +3V3_CONN, 6/8 +12V, 16 RS485.B1, 18 RS485.A1</td>'
        '<td>Reti con un solo nodo, senza spiegazione sullo schema (la nota di Brik81 spiegava solo +3V3_CONN)</td>'
        '<td>Nessun cambio elettrico. Nuova nota di testo a (185,42; 116,84) mm: "+12V, RS485.A1/B1: non usati su questa scheda". Le etichette restano per documentare il pinout standard</td>'
        '<td>R-12, §43</td><td>Brik81 · 02/11</td><td>Claude Code · 02/11</td></tr>\n')
i = h.find('<h2>Registro modifiche</h2>'); j = h.find('</table>', i); h = h[:j] + rows + h[j:]

PART = """
<section class="part" id="partAD">
<div class="partlabel">Parte AD</div>
<h1 class="parttitle">Rev. 1.31 – Pin non usati del connettore dock J708 (R-12)</h1>
</section>
<h2 id="s43">43. J708: +12V, +3V3_CONN e RS485</h2>
<p>J708 ha il pinout standard del dock. Su questa scheda Brik81 ha deciso: il 3V3 è generato a bordo (foglio POWER), quindi +3V3_CONN non serve, mentre il 5V del dock è collegato; +12V non è usato; RS485.A1/B1 per ora non sono usati, e sulla scheda non c'è un transceiver RS485. Le etichette restano sui pin per documentare il pinout. Accanto a J708 c'è ora una nota che lo spiega, così un revisore non li scambia per errori di collegamento.</p>
<p>I flag no-connect non sono stati messi: in KiCad un pin con un no-connect e insieme un'etichetta dà un conflitto, e la nota di testo ottiene lo stesso scopo. Sul PCB questi pad restano semplicemente non collegati.</p>
<p><b>Ancora aperto in R-12:</b> GPIO_PPS (pin 17), GPIOSX_0 (pin 14) e GPIOSX_2 (pin 13) non sono collegati all'MCU. Brik81 deve decidere se lasciarli così o collegare il PPS a un ingresso timer/EXTI per la sincronizzazione del tempo.</p>
<p><b>Verifica.</b> Netlist prima e dopo: identica. Il PDF dello schema conferma che la nota è leggibile e non si sovrappone ad altro.</p>
"""
sub1('\n</body></html>', PART + '\n</body></html>')
p.write_text(h, encoding='utf8')
print('ok')
