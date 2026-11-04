import pathlib
d = pathlib.Path(__file__).parent
p = d / 'symphony_version_log.html'
h = p.read_text(encoding='utf8')

def sub1(o, rep):
    global h
    assert h.count(o) == 1, o[:60]
    h = h.replace(o, rep)


sub1('symphony_version_log · rev. 1.26"', 'symphony_version_log · rev. 1.27"')
sub1("<div><b>1.26</b> del 30/10/2026",
     "<div><b>1.27</b> del 30/10/2026 – Gruppo B: test point SMD (R-08), C261/C702/C704 Murata GJM (R-10, parte), pin schermo USB-C S1→SH (R-09, parte)</div><div>1.26 del 30/10/2026")
sub1('tr.r126 td {', 'tr.r127 td { background: #e8f4f4 !important; }\ntr.r126 td {')
sub1('<li><a href="#partY">Parte Y – Rev. 1.26: codici JLC (R-05) e datasheet U701 (R-22)</a></li>',
     '<li><a href="#partY">Parte Y – Rev. 1.26: codici JLC (R-05) e datasheet U701 (R-22)</a></li>\n'
     '<li><a href="#partZ">Parte Z – Rev. 1.27: gruppo B, correzioni senza scelte (R-08, R-10 parte, R-09 parte)</a></li>')
sub1('lilla</span> = rev. 1.26,',
     'lilla</span> = rev. 1.26, righe <span style="background:#e8f4f4;padding:0 2mm">acqua</span> = rev. 1.27,')

REV = ('<tr class="r127"><td>1.27</td><td>gruppo B della revisione indipendente del 27/10/2026 (violazioni delle regole di progetto)<br>eseguito da Claude Code il 30/10</td>'
       '<td>Solo le correzioni che non richiedono scelte: footprint SMD per TP701–TP703; C261, C702 e C704 a Murata GJM con lo stesso valore e footprint; numero del pin schermo di J15 allineato al footprint (S1→SH). Restano da decidere: R-10 per i 100 pF/56 pF e R-09 per connettore e linguette</td>'
       '<td>Claude Code</td><td><b>Brik81</b></td>'
       '<td>"Partiamo dal gruppo B" (30/10), in risposta all\'elenco con le correzioni proposte</td></tr>\n')
i = h.find('<h2>Registro revisioni</h2>'); j = h.find('</table>', i); h = h[:j] + REV + h[j:]
sub1('Rev. 1.26: <code>UHF.kicad_sch</code>',
     'Rev. 1.27: <code>UHF.kicad_sch</code> e <code>POWER.kicad_sch</code> (copie precedenti in <code>report_src/bak_pre127/</code>). Rev. 1.26: <code>UHF.kicad_sch</code>')

rows = ('<tr class="r127"><td>1.27-01</td><td>UHF</td><td>TP701, TP702, TP703</td>'
        '<td>Connector_Pin:Pin_D0.7mm_L6.5mm_W1.8mm_FlatFork (through-hole)</td><td><b>TestPoint:TestPoint_Pad_D1.0mm</b> (pad SMD, come TP1). Reti invariate: RF_XIN, EN_TX_ANT_SW, EN_RX_LNA</td>'
        '<td>R-08, §39</td><td>Brik81 · 30/10</td><td>Claude Code · 30/10</td></tr>\n'
        '<tr class="r127"><td>1.27-02</td><td>UHF</td><td>C261 (22p 0402, adattamento PA)</td>'
        '<td>C710855 GRM1555C2A220JA01D (GRM, ±5 %)</td><td>C882567 <b>GJM1555C1H220FB01D</b> (C0G ±1 %, 50 V, stock 47343)</td>'
        '<td>R-10, §39</td><td>Brik81 · 30/10</td><td>Claude Code · 30/10</td></tr>\n'
        '<tr class="r127"><td>1.27-03</td><td>UHF</td><td>C702 (9.1p 0402, C0 AN648)</td>'
        '<td>C415411 GRM1555C1H9R1DA01D (±0,5 pF)</td><td>C497527 <b>GJM1555C1H9R1BB01D</b> (C0G ±0,1 pF, 50 V, stock 5366)</td>'
        '<td>R-10, §39</td><td>Brik81 · 30/10</td><td>Claude Code · 30/10</td></tr>\n'
        '<tr class="r127"><td>1.27-04</td><td>UHF</td><td>C704 (15p 0402, CM AN648)</td>'
        '<td>C76950 GRM1555C1H150JA01D (±5 %)</td><td>C441742 <b>GJM1555C1H150FB01D</b> (C0G ±1 %, 50 V, stock 311272)</td>'
        '<td>R-10, §39</td><td>Brik81 · 30/10</td><td>Claude Code · 30/10</td></tr>\n'
        '<tr class="r127"><td>1.27-05</td><td>POWER</td><td>J15 USB-C, pin schermo</td>'
        '<td>Il pin del simbolo si chiamava "S1", mentre nel footprint GCT_USB4105 i 4 pad del guscio si chiamano "SH": sul PCB lo schermo non sarebbe stato collegato a GND</td>'
        '<td>Pin rinominato in "SH" (nella copia del simbolo dentro lo schema e nell\'istanza), come nel simbolo standard KiCad 10 Connector:USB_C_Receptacle_USB2.0_16P. Rete: J15/SH su GND</td>'
        '<td>R-09 (a), §39</td><td>Brik81 · 30/10</td><td>Claude Code · 30/10</td></tr>\n')
i = h.find('<h2>Registro modifiche</h2>'); j = h.find('</table>', i); h = h[:j] + rows + h[j:]

PART = """
<section class="part" id="partZ">
<div class="partlabel">Parte Z</div>
<h1 class="parttitle">Rev. 1.27 – Gruppo B: correzioni senza scelte</h1>
</section>
<h2 id="s39">39. Test point SMD, condensatori RF GJM, schermo USB-C</h2>
<ul>
<li><b>R-08.</b> I test point TP701–TP703 avevano un footprint a spina through-hole, in contrasto con la regola "solo SMD". Ora usano il pad SMD da 1 mm, come TP1. Il pad su RF_XIN (clock del TCXO) aggiunge qualche decimo di pF, trascurabile per un clipped sine accoppiato in AC.</li>
<li><b>R-10, parte.</b> I tre condensatori RF per cui esiste un Murata GJM a stock su JLC con lo stesso valore e lo stesso footprint 0402 sono stati sostituiti, scegliendo la tolleranza più stretta disponibile: C261 22 pF ±1 %, C702 9,1 pF ±0,1 pF, C704 15 pF ±1 %. La serie GJM15 arriva solo fino a 33 pF, quindi per i 100 pF e 56 pF serve una decisione (vedi sotto).</li>
<li><b>R-09 (a).</b> Il pin schermo del simbolo USB-C si chiamava S1, mentre il footprint ha i pad SH: il guscio non sarebbe stato collegato. Ora il pin si chiama SH, come nel simbolo standard di KiCad 10.</li>
</ul>
<p><b>Ancora da decidere.</b> R-10: C206, C207, C208, C701 (100 pF 0402), C255 (56 pF 0402), C212, C213 (100 pF 0805) e C230 (56 pF 0805) non hanno un Murata GQM/GJM a stock su JLC con lo stesso footprint. R-09 (b, c): linguette THT del guscio e codice JLC del connettore.</p>
<p><b>Verifica.</b> Netlist prima e dopo: l'unica differenza è J15/S1 → J15/SH sulla rete GND. Footprint e codici risultano quelli indicati.</p>
"""
sub1('\n</body></html>', PART + '\n</body></html>')
p.write_text(h, encoding='utf8')
print('ok')
