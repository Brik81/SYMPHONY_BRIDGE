import pathlib
d = pathlib.Path(__file__).parent
p = d / 'symphony_version_log.html'
h = p.read_text(encoding='utf8')

def sub1(o, rep):
    global h
    assert h.count(o) == 1, o[:60]
    h = h.replace(o, rep)


sub1('symphony_version_log · rev. 1.27"', 'symphony_version_log · rev. 1.28"')
sub1("<div><b>1.27</b> del 30/10/2026",
     "<div><b>1.28</b> del 30/10/2026 – R-10 chiuso: 8 condensatori RF da 100/56 pF passano a Murata GQM1875 0603; R-09 chiuso con J15 lasciato com'è</div><div>1.27 del 30/10/2026")
sub1('tr.r127 td {', 'tr.r128 td { background: #f6efe9 !important; }\ntr.r127 td {')
sub1('<li><a href="#partZ">Parte Z – Rev. 1.27: gruppo B, correzioni senza scelte (R-08, R-10 parte, R-09 parte)</a></li>',
     '<li><a href="#partZ">Parte Z – Rev. 1.27: gruppo B, correzioni senza scelte (R-08, R-10 parte, R-09 parte)</a></li>\n'
     '<li><a href="#partAA">Parte AA – Rev. 1.28: condensatori RF GQM1875 0603 (R-10) e decisione su J15 (R-09)</a></li>')
sub1('acqua</span> = rev. 1.27,',
     'acqua</span> = rev. 1.27, righe <span style="background:#f6efe9;padding:0 2mm">cipria</span> = rev. 1.28,')

REV = ('<tr class="r128"><td>1.28</td><td>gruppo B della revisione indipendente del 27/10/2026, punti rimasti<br>eseguito da Claude Code il 30/10</td>'
       '<td>R-10: C206, C207, C208, C701, C212, C213 (100 pF) e C255, C230 (56 pF) passano a Murata GQM1875 0603 con lo stesso valore. Eccezione approvata alla regola "footprint esistenti", perché in 0402 la serie GJM arriva solo a 47 pF e GQM1555/GQM2195 sono a stock 0 su JLC. R-09: J15 resta com\'è (codice C393939, linguette del guscio THT), per decisione di Brik81</td>'
       '<td>Claude Code</td><td><b>Brik81</b></td>'
       '<td>"NO IL CONNETTORE TIPOC va bene cois R-09 lascia cosi come sta" e, sulla lista degli 8 condensatori, "si procedi" (30/10)</td></tr>\n')
i = h.find('<h2>Registro revisioni</h2>'); j = h.find('</table>', i); h = h[:j] + REV + h[j:]
sub1('Rev. 1.27: <code>UHF.kicad_sch</code> e <code>POWER.kicad_sch</code>',
     'Rev. 1.28: <code>UHF.kicad_sch</code> (copia precedente in <code>report_src/bak_pre128/</code>). Rev. 1.27: <code>UHF.kicad_sch</code> e <code>POWER.kicad_sch</code>')

caps = [
    ('C206', '100 pF', 'RF_SW_COM → RF_ANT, blocco DC verso l\'antenna', 'C21366878 GRM1555C2A101GA01D, 0402', 'C17308632'),
    ('C207', '100 pF', 'RF_RX_F1 → RF_SW_RX, blocco DC ramo RX', 'C77177 GRM1555C1H101JA01D, 0402', 'C17308632'),
    ('C208', '100 pF', 'RF_LPF_OUT → RF_SW_TX, blocco DC ramo TX', 'C21366878 GRM1555C2A101GA01D, 0402', 'C17308632'),
    ('C701', '100 pF', 'RF_ATT_IN → RF_TX_M2, blocco DC verso il pad', 'C77177 GRM1555C1H101JA01D, 0402', 'C17308632'),
    ('C255', '56 pF', 'RF_ATT_OUT → RF_PA_IN, C1 della EVB Qorvo', 'C393672 GCM1555C1H560JA16D, 0402', 'C237591'),
    ('C212', '100 pF', 'RF_LNA_IN → RF_RX_F2, blocco DC ingresso LNA', 'C1864265 GRM21A5C2E101FW01D, 0805', 'C17308632'),
    ('C213', '100 pF', 'RF_RX_F3 → RF_LNA_OUT, blocco DC uscita LNA', 'C1864265 GRM21A5C2E101FW01D, 0805', 'C17308632'),
    ('C230', '56 pF', 'RF_PA_MATCH → RF_LPF_IN, uscita PA', 'C913752 GRM21A5C2E560JW01D, 0805', 'C237591'),
]
mpn = {'C17308632': 'GQM1875C2E101FB12D (C0G ±1 %, 250 V)', 'C237591': 'GQM1875C2E560JB12D (C0G ±5 %, 250 V)'}
rows = ''
for n, (ref, val, role, old, new) in enumerate(caps, 1):
    rows += (f'<tr class="r128"><td>1.28-{n:02d}</td><td>UHF</td><td>{ref} ({val})</td>'
             f'<td>{old}. {role}</td><td>{new} Murata <b>{mpn[new]}</b>, <b>Capacitor_SMD:C_0603_1608Metric</b>. Valore e collegamenti invariati</td>'
             f'<td>R-10, §40</td><td>Brik81 · 30/10</td><td>Claude Code · 30/10</td></tr>\n')
rows += ('<tr class="r128"><td>1.28-09</td><td>POWER</td><td>J15 USB-C</td>'
         '<td>C393939 (SHOU HAN TYPE-C16PIN) con footprint GCT_USB4105; 4 linguette del guscio THT</td>'
         '<td>Nessuna modifica, per decisione di Brik81. Il pin schermo era già stato corretto in SH nella rev 1.27</td>'
         '<td>R-09, §40</td><td>Brik81 · 30/10</td><td>—</td></tr>\n')
i = h.find('<h2>Registro modifiche</h2>'); j = h.find('</table>', i); h = h[:j] + rows + h[j:]

PART = """
<section class="part" id="partAA">
<div class="partlabel">Parte AA</div>
<h1 class="parttitle">Rev. 1.28 – Condensatori RF Murata GQM (R-10) e connettore USB-C (R-09)</h1>
</section>
<h2 id="s40">40. Chiusura di R-10 e R-09</h2>
<p><b>R-10.</b> Otto condensatori del percorso RF erano Murata GRM/GCM, cioè della serie standard e non di quella ad alta Q. Su JLC (ricerca del 30/10) la serie GJM1555 in 0402 arriva al massimo a 47 pF, la GQM1555 (0402) e la GQM2195 (0805) sono a stock 0. Per mantenere i valori, compreso C255 = 56 pF che è il C1 della EVB Qorvo, Brik81 ha approvato il passaggio di tutti e otto a <b>GQM1875 0603</b>: GQM1875C2E101FB12D (C17308632, 2634 a stock, 6 pezzi) e GQM1875C2E560JB12D (C237591, 3805 a stock, 2 pezzi). Il PCB non esiste ancora, quindi il cambio di footprint non costa nulla. La tensione nominale passa a 250 V: è la stessa di prima per C212, C213 e C230, ed è più alta per gli altri. La corrente RF ammessa dal 0603 non è stata verificata sul datasheet; a questi livelli di potenza un 0603 C0G è normalmente adeguato.</p>
<p><b>R-09.</b> Brik81 ha deciso di lasciare J15 com'è: codice C393939 con footprint GCT_USB4105 e 4 linguette THT del guscio. Il pin schermo era già stato allineato al footprint (S1 → SH) nella rev 1.27.</p>
<p><b>Verifica.</b> Netlist prima e dopo: le reti sono identiche, e gli 8 condensatori risultano con il footprint 0603 e i nuovi codici. Il gruppo B (R-08, R-09, R-10) è chiuso.</p>
"""
sub1('\n</body></html>', PART + '\n</body></html>')
p.write_text(h, encoding='utf8')
print('ok')
