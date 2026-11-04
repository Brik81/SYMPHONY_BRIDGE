import pathlib
d = pathlib.Path(__file__).parent
p = d / 'symphony_version_log.html'
h = p.read_text(encoding='utf8')

def sub1(o, rep):
    global h
    assert h.count(o) == 1, o[:60]
    h = h.replace(o, rep)


sub1('symphony_version_log · rev. 1.34"', 'symphony_version_log · rev. 1.35"')
sub1("<div><b>1.34</b> del 02/11/2026",
     "<div><b>1.35</b> del 02/11/2026 – R-13 chiuso senza modifiche: pull-up I2C1 tramite JP201 aperto, standard di progetto</div><div>1.34 del 02/11/2026")
sub1('tr.r134 td {', 'tr.r135 td { background: #e9eef3 !important; }\ntr.r134 td {')
sub1('<li><a href="#partAG">Parte AG – Rev. 1.34: supervisore della radio escludibile (R-19)</a></li>',
     '<li><a href="#partAG">Parte AG – Rev. 1.34: supervisore della radio escludibile (R-19)</a></li>\n'
     '<li><a href="#partAH">Parte AH – Rev. 1.35: pull-up di I2C1 (R-13)</a></li>')
sub1('pesca</span> = rev. 1.34,',
     'pesca</span> = rev. 1.34, righe <span style="background:#e9eef3;padding:0 2mm">ardesia</span> = rev. 1.35,')

REV = ('<tr class="r135"><td>1.35</td><td>problema R-13 della revisione indipendente del 27/10/2026<br>decisione di Brik81 del 02/11, registrata da Claude Code</td>'
       '<td>Nessuna modifica e nessuna nota sullo schema. I pull-up R206/R207 (4k7) di I2C1 restano collegati al 3V3 tramite il solder jumper JP201, aperto di serie: è lo standard di progetto</td>'
       '<td>Claude Code</td><td><b>Brik81</b></td>'
       '<td>"Lascia come è senza nota, è nostro standard fare cosi, next" (02/11)</td></tr>\n')
i = h.find('<h2>Registro revisioni</h2>'); j = h.find('</table>', i); h = h[:j] + REV + h[j:]
sub1('Rev. 1.34: nessun file di progetto modificato da Claude Code',
     'Rev. 1.35: nessun file di progetto modificato. Rev. 1.34: nessun file di progetto modificato da Claude Code')

rows = ('<tr class="r135"><td>1.35-01</td><td>IF</td><td>R206, R207 (4k7), JP201 (SolderJumper_2_Open)</td>'
        '<td>Con JP201 aperto il bus I2C1 (PB6/PB7, J203, J708 pin 9/11) non ha pull-up a bordo</td>'
        '<td>Nessuna modifica. Standard di progetto: JP201 si chiude solo sulla scheda che deve fornire i pull-up al bus</td>'
        '<td>R-13, §47</td><td>Brik81 · 02/11</td><td>—</td></tr>\n')
i = h.find('<h2>Registro modifiche</h2>'); j = h.find('</table>', i); h = h[:j] + rows + h[j:]

PART = """
<section class="part" id="partAH">
<div class="partlabel">Parte AH</div>
<h1 class="parttitle">Rev. 1.35 – Pull-up di I2C1 (R-13)</h1>
</section>
<h2 id="s47">47. Pull-up di I2C1 tramite JP201</h2>
<p>I2C1 (SCL PB6, SDA PB7) arriva a J203 (pin 3/2) e al dock J708 (pin 11/9), con D202 come protezione ESD. I pull-up R206/R207 da 4k7 vanno al 3V3 solo attraverso JP201, un solder jumper aperto di serie e fuori BOM. Con JP201 aperto il bus non ha pull-up a bordo. Brik81 ha confermato che è lo standard di progetto: sul bus del dock i pull-up li fornisce una sola scheda, e su quella si chiude il jumper; così non si sommano in parallelo i pull-up di tutte le schede. Nessuna nota aggiunta sullo schema, su richiesta di Brik81. R-13 è chiuso.</p>
<p><b>Da ricordare al collaudo:</b> se la scheda si usa da sola (al banco con un sensore su J203, senza dock) JP201 va chiuso, altrimenti I2C1 non funziona.</p>
"""
sub1('\n</body></html>', PART + '\n</body></html>')
p.write_text(h, encoding='utf8')
print('ok')
