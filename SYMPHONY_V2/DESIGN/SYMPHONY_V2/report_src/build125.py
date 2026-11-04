import pathlib
d = pathlib.Path(__file__).parent
p = d / 'symphony_version_log.html'
h = p.read_text(encoding='utf8')

def sub1(o, rep):
    global h
    assert h.count(o) == 1, o[:60]
    h = h.replace(o, rep)


sub1('symphony_version_log · rev. 1.24"', 'symphony_version_log · rev. 1.25"')
sub1("<div><b>1.24</b> del 27/10/2026",
     "<div><b>1.25</b> del 30/10/2026 – R-03/R-11: L242 torna a 1 µH (Taiyo Yuden NRS2012T1R0NGJV) e C260 a 27 pF, come la EVB-02 Qorvo</div><div>1.24 del 27/10/2026")
sub1('tr.r124 td {', 'tr.r125 td { background: #fbf3e4 !important; }\ntr.r124 td {')
sub1('<li><a href="#partW">Parte W – Rev. 1.24: revisione indipendente, R-01 e R-02</a></li>',
     '<li><a href="#partW">Parte W – Rev. 1.24: revisione indipendente, R-01 e R-02</a></li>\n'
     '<li><a href="#partX">Parte X – Rev. 1.25: choke del PA L242 = 1 µH e C260 = 27 pF (R-03, R-11)</a></li>')
sub1('verde chiaro</span> = rev. 1.24,',
     'verde chiaro</span> = rev. 1.24, righe <span style="background:#fbf3e4;padding:0 2mm">sabbia</span> = rev. 1.25,')

REV = ('<tr class="r125"><td>1.25</td><td>problemi R-03/R-11 della revisione indipendente del 27/10/2026<br>modifica eseguita da Claude Code in <code>UHF.kicad_sch</code> il 30/10</td>'
       '<td>L242 da 22 nH (LQW2BAN22NJ00L, rev 1.11) a 1 µH Taiyo Yuden NRS2012T1R0NGJV, footprint L_Taiyo-Yuden_NR-20xx; C260 da 33 pF a 27 pF GQM1875C2E270FB12D. Rete d\'uscita riallineata alla EVB-02 Qorvo. Eccezione approvata alle regole "induttori RF solo Murata LQW" e "footprint esistenti", solo per L242</td>'
       '<td>Claude Code</td><td><b>Brik81</b></td>'
       '<td>"si procedi con questi 3 punti che mi hai proposto" (30/10), dopo "vorrei riamenre coerente con worvo" (= Qorvo) e "non è un problema che non sia su jlc"</td></tr>\n')
i = h.find('<h2>Registro revisioni</h2>'); j = h.find('</table>', i); h = h[:j] + REV + h[j:]
sub1('Rev. 1.24: nessun file di progetto modificato da Claude Code',
     'Rev. 1.25: <code>UHF.kicad_sch</code> (copia precedente in <code>report_src/bak_pre125/</code>). Rev. 1.24: nessun file di progetto modificato da Claude Code')

rows = ('<tr class="r125"><td>1.25-01</td><td>UHF</td><td>L242</td>'
        '<td>22n, L_0805_2012Metric, JLC C2042193 (Murata LQW2BAN22NJ00L, 1,9 A). Equivalente alla EVB solo a 435 MHz, insieme a C260 = 33 pF (rev 1.11, §23)</td>'
        '<td><b>1u</b>, <b>Inductor_SMD:L_Taiyo-Yuden_NR-20xx</b>, Taiyo Yuden <b>NRS2012T1R0NGJV</b> (nuovo nome LCXND2020MKT1R0N0G, AEC-Q200): 1 µH ±30 %, Isat 1,9 A, Itemp 1,7 A (ΔT 40 °C), DCR 84 mΩ max, 2,0×2,0×1,2 mm. Mouser 963-NRS2012T1R0NGJV; campo JLCPCB Parts vuoto (non a catalogo JLC). Collegamenti invariati (3V3 → RF_PA_OUT)</td>'
        '<td>R-03, §37</td><td>Brik81 · 30/10</td><td>Claude Code · 30/10</td></tr>\n'
        '<tr class="r125"><td>1.25-02</td><td>UHF</td><td>C260</td>'
        '<td>33p, GQM1875C2E330FB12D (C2360428): valore di compensazione dei 22 nH</td>'
        '<td><b>27p</b>, Murata <b>GQM1875C2E270FB12D</b> (C2360423, 0603, C0G 1 %, 250 V, stock LCSC 6690 al 30/10) = C10 della EVB-02. Footprint invariato</td>'
        '<td>R-11, §37</td><td>Brik81 · 30/10</td><td>Claude Code · 30/10</td></tr>\n')
i = h.find('<h2>Registro modifiche</h2>'); j = h.find('</table>', i); h = h[:j] + rows + h[j:]

PART = """
<section class="part" id="partX">
<div class="partlabel">Parte X</div>
<h1 class="parttitle">Rev. 1.25 – Choke del PA: ritorno alla rete Qorvo (R-03, R-11)</h1>
</section>
<h2 id="s37">37. L242 = 1 µH e C260 = 27 pF</h2>
<p><b>Origine.</b> Nella revisione indipendente del 27/10, L242 = 22 nH era stato segnalato come critico (R-03), e C260 = 33 pF come diverso dalla EVB (R-11). Rileggendo i report si è visto che il 22 nH era voluto: nella rev 1.11 (§23) era stato scelto perché nessun Murata LQW da circa 1 µH su JLC regge la corrente del PA (LQW2UAS 1 µH: 0,37 A), e C260 era stato portato a 33 pF per dare al nodo la stessa suscettanza a 435 MHz. Nessuna application note Qorvo usa però 22 nH. PK090 (400 MHz) e la EVB-02 (450 MHz, datasheet QPA9510 pag. 15–18) montano L3 = 1 µH, e il riepilogo EVB 410–470 MHz del 30/06/2025 dà C10 = 27 pF. Brik81 ha chiesto di restare coerenti con Qorvo, anche se il componente non si trova su JLC.</p>
<p><b>Componente.</b> Sul forum Qorvo, L3 della EVB-02 risulta un Taiyo Yuden NR3012T1R0N (3×3 mm, Isat 1,5 A, SRF ≥ 110 MHz), oggi in <i>phaseout</i> (TY-COMPAS: rinominato LSXBD3030MKT1R0N, Phaseout) e a stock 0 su JLC. Si usa il Taiyo Yuden <b>NRS2012T1R0NGJV</b>, proposto da Brik81 da Mouser: stessa costruzione (filo su ferrite, schermato), stesso valore e più corrente. Dati da TY-COMPAS (LCXND2020MKT1R0N0G, produzione di serie): Isat 1,9 A, Itemp 1,7 A, DCR 84 mΩ max, −40…+125 °C, AEC-Q200. Footprint KiCad <code>L_Taiyo-Yuden_NR-20xx</code>, la libreria standard per la serie NR/NRS 2020.</p>
<ul>
<li><b>Corrente.</b> A piena potenza il PA assorbe circa 1,7 A. L'Isat (1,9 A) è sopra l'originale Qorvo (1,5 A). La corrente termica di 1,7 A va bene per trasmissioni a impulsi; in trasmissione continua alla massima potenza l'induttore si scalda di circa 40 °C.</li>
<li><b>Comportamento a 435 MHz.</b> Come l'NR3012, l'induttore lavora sopra la sua frequenza di risonanza e verso massa vale circa 2 pF (|X| ≈ 190 Ω). È trascurabile rispetto a C260 (13,5 Ω), e il lato 3V3 è messo a massa in RF da C258 = 47 pF. La SRF dell'NRS2012 non è indicata da Taiyo Yuden: è <span class="tag warn">da verificare</span> sul prototipo, misurando l'adattamento d'uscita (S22 o potenza), come già previsto per C260 e C261.</li>
<li><b>Eccezioni alle regole di progetto</b>, approvate da Brik81 solo per L242: non è un Murata LQW, perché in quella posizione serve un induttore di potenza e non un induttore RF; il footprint passa da 0805 a 2020; il componente non è su JLC e va fornito a parte (Mouser), quindi il campo JLCPCB Parts è vuoto.</li>
</ul>
<p><b>Verifica.</b> Netlist riesportata con kicad-cli dopo la modifica: L242 = 1u, L_Taiyo-Yuden_NR-20xx, MPN NRS2012T1R0NGJV; C260 = 27p, C2360423. I nodi (3V3 – L242 – RF_PA_OUT, C260 tra RF_PA_OUT e GND) sono gli stessi di prima. R-03 e R-11 sono chiusi.</p>
"""
sub1('\n</body></html>', PART + '\n</body></html>')
p.write_text(h, encoding='utf8')
print('ok')
