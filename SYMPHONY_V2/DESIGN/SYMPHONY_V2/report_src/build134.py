import pathlib
d = pathlib.Path(__file__).parent
p = d / 'symphony_version_log.html'
h = p.read_text(encoding='utf8')

def sub1(o, rep):
    global h
    assert h.count(o) == 1, o[:60]
    h = h.replace(o, rep)


sub1('symphony_version_log · rev. 1.33"', 'symphony_version_log · rev. 1.34"')
sub1("<div><b>1.33</b> del 02/11/2026",
     "<div><b>1.34</b> del 02/11/2026 – R-19: supervisore IC205 escludibile (R204 0R montata, R205 0R DNP verso PC4); misura M-03 e note firmware F-05/F-10</div><div>1.33 del 02/11/2026")
sub1('tr.r133 td {', 'tr.r134 td { background: #f7ece4 !important; }\ntr.r133 td {')
sub1('<li><a href="#partAF">Parte AF – Rev. 1.33: TPS2121, pin ST e OV2 (R-16)</a></li>',
     '<li><a href="#partAF">Parte AF – Rev. 1.33: TPS2121, pin ST e OV2 (R-16)</a></li>\n'
     '<li><a href="#partAG">Parte AG – Rev. 1.34: supervisore della radio escludibile (R-19)</a></li>')
sub1('menta</span> = rev. 1.33,',
     'menta</span> = rev. 1.33, righe <span style="background:#f7ece4;padding:0 2mm">pesca</span> = rev. 1.34,')

REV = ('<tr class="r134"><td>1.34</td><td>problema R-19 della revisione indipendente del 27/10/2026<br>R204/R205 aggiunte da Brik81 in KiCad (salvataggio 02/11 13:11), verificate da Claude Code</td>'
       '<td>IC205 resta TPS3825-33. Per poterlo escludere in laboratorio senza fili volanti: R204 0R (montata) in serie tra IC205 RESET e RF_SDN; R205 0R (DNP) tra RF_MR_N (PC4) e RF_SDN. Aggiunte la misura M-03 e le note firmware F-05 (aggiornata) e F-10</td>'
       '<td>Brik81 (modifica) · Claude Code (verifica e log)</td><td><b>Brik81</b></td>'
       '<td>"ok io lascerei cosi e speriamo…", poi "potrei prevedere un solder bridge… lo disissaldo e metto 0 ohm che cosi è conensso diretto al MCU gpio cosi comando via firmware il powerup" e "guarda R205 e R204 le ho aggiunte ora" (02/11)</td></tr>\n')
i = h.find('<h2>Registro revisioni</h2>'); j = h.find('</table>', i); h = h[:j] + REV + h[j:]
sub1('Rev. 1.33: nessun file di progetto modificato da Claude Code',
     'Rev. 1.34: nessun file di progetto modificato da Claude Code (R204/R205 aggiunte da Brik81 in UHF). Rev. 1.33: nessun file di progetto modificato da Claude Code')

rows = ('<tr class="r134"><td>1.34-01</td><td>UHF</td><td>R204 (nuova)</td>'
        '<td>IC205 pin 3 (RESET, push-pull) collegato direttamente a RF_SDN</td>'
        '<td>R204 0R 0402 (C17168), montata, in serie: IC205 pin 3 → nuova rete Net-(IC205-RESET) → R204 → /UHF/RF_SDN (IC204 pin 1)</td>'
        '<td>R-19, §46</td><td>Brik81 · 02/11</td><td>Brik81 · 02/11 13:11 (verifica Claude Code)</td></tr>\n'
        '<tr class="r134"><td>1.34-02</td><td>UHF</td><td>R205 (nuova, DNP)</td>'
        '<td>—</td>'
        '<td>R205 0402 (C17168), DNP, tra RF_MR_N (PC4 / U301 pin 24, pull-up R208, IC205 ~MR) e /UHF/RF_SDN. Il campo Value oggi vale "DNP"; consigliato "0R" con il solo flag DNP</td>'
        '<td>R-19, §46</td><td>Brik81 · 02/11</td><td>Brik81 · 02/11 13:11 (verifica Claude Code)</td></tr>\n')
i = h.find('<h2>Registro modifiche</h2>'); j = h.find('</table>', i); h = h[:j] + rows + h[j:]

PART = """
<section class="part" id="partAG">
<div class="partlabel">Parte AG</div>
<h1 class="parttitle">Rev. 1.34 – Supervisore della radio escludibile (R-19)</h1>
</section>
<h2 id="s46">46. IC205: rischio di reset in TX e ripiego hardware</h2>
<p><b>Rischio.</b> La soglia del TPS3825-33 è 2,88 / 2,93 / 3,00 V (min / tip / max, datasheet TI SLVS165O, Electrical Characteristics). In trasmissione il PA assorbe ≈ 1,7 A dal 3V3. Se il rail scende sotto la soglia, IC205 spegne l'Si4464 (SDN alto per ≈ 200 ms), la trasmissione si interrompe e il ciclo si può ripetere. Non c'è danno: l'Si4464 funziona fino a 1,8 V. La stima del minimo in TX è ≈ 3,15–3,2 V, ma non è verificata, perché manca la risposta al gradino del TPSM863257 e il PCB non esiste ancora. La variante TPS3825-30 (soglia 2,63 V, stessa piedinatura) non risulta in vendita; la TPS3823-30 (C55505) ha una piedinatura diversa. Brik81 ha scelto di lasciare IC205 e di prevedere un ripiego.</p>
<p><b>Circuito A/B.</b></p>
<table>
<tr><th>Modo</th><th>Montaggio</th><th>Chi comanda SDN</th><th>PC4 basso</th><th>PC4 alto / alta impedenza</th></tr>
<tr><td><b>A</b> (di serie)</td><td>R204 montata, R205 DNP</td><td>IC205 (supervisore); PC4 agisce tramite ~MR</td><td>radio in reset</td><td>radio attiva</td></tr>
<tr><td><b>B</b> (ripiego)</td><td>R204 rimossa, R205 = 0R montata</td><td>direttamente PC4; IC205 escluso dall'uscita</td><td><b>radio attiva</b></td><td>radio spenta (pull-up R208)</td></tr>
</table>
<p>Nel modo B, durante boot e reset dell'MCU (PC4 in alta impedenza), R208 tiene SDN alto e quindi la radio resta spenta finché il firmware non la accende: è il comportamento giusto per una partenza pulita. Il LED D203 segue ancora IC205 e nel modo B non indica più lo stato della radio.</p>
<div class="box">
<p><b>Aggiunte alle note per il firmware (§41)</b></p>
<table>
<tr><th>ID</th><th>Requisito</th></tr>
<tr><td><b>F-05</b> (aggiornata)</td><td>Il firmware deve sapere in che modo è montata la scheda (costante di compilazione MODO_A / MODO_B). <b>Modo A:</b> PC4 basso = reset della radio; dopo il rilascio aspettare ≥ 200 ms (IC205) più il POR dell'Si4464, poi CTS. <b>Modo B:</b> logica invertita. Accensione: PC4 alto (SDN alto) per il tempo minimo richiesto dal datasheet Si4464 → PC4 basso → attesa del POR → controllo di CTS. I tempi esatti di SDN e POR vanno presi dal datasheet Si4464 (non verificati in questa revisione)</td></tr>
<tr><td><b>F-10</b></td><td>Dopo ogni trasmissione controllare che l'Si4464 risponda ancora (CTS / PART_INFO, oppure lo stato del chip). Se risulta resettato: reinizializzare, contare l'evento e segnalarlo in telemetria. Serve a vedere subito un eventuale reset da calo del 3V3 in TX</td></tr>
</table>
<p><b>Misura obbligatoria sul prototipo M-03:</b> oscilloscopio sul 3V3 al pin 5 (VDD) di IC205 durante una trasmissione a piena potenza, con il limite F-01. Requisito: minimo ≥ 3,05 V (50 mV sopra la soglia massima di 3,00 V). Se non passa, si passa al modo B (togliere R204, montare R205 0R) e si aggiorna il firmware (F-05).</p>
</div>
<p><b>Verifica.</b> Netlist esportata dopo il salvataggio delle 13:11 e confrontata con quella della rev 1.33. Le uniche differenze: IC205 pin 3 passa a Net-(IC205-RESET) insieme a R204 pin 2; R204 pin 1 e R205 pin 2 sono su /UHF/RF_SDN; R205 pin 1 è su RF_MR_N. R205 ha il flag DNP. Il resto è identico. R-19 è chiuso.</p>
"""
sub1('\n</body></html>', PART + '\n</body></html>')
p.write_text(h, encoding='utf8')
print('ok')
