import pathlib
d = pathlib.Path(__file__).parent
p = d / 'symphony_version_log.html'
h = p.read_text(encoding='utf8')

def sub1(o, rep):
    global h
    assert h.count(o) == 1, o[:60]
    h = h.replace(o, rep)

sub1('symphony_version_log · rev. 1.21"', 'symphony_version_log · rev. 1.22"')
sub1("<div><b>1.21</b> del 24/10/2026",
     "<div><b>1.22</b> del 27/10/2026 – tolta l'etichetta UHF.EN_RX_LNA senza collegamenti nel foglio MCU</div><div>1.21 del 24/10/2026")
sub1('tr.r121 td {', 'tr.r122 td { background: #f7f3e6 !important; }\ntr.r121 td {')
sub1('<li><a href="#partT">Parte T – Rev. 1.21: footprint CPH3225A e pulizia</a></li>',
     '<li><a href="#partT">Parte T – Rev. 1.21: footprint CPH3225A e pulizia</a></li>\n'
     '<li><a href="#partU">Parte U – Rev. 1.22: etichetta EN_RX_LNA nel foglio MCU</a></li>')
sub1('righe <span style="background:#edf6f6;padding:0 2mm">grigio acqua</span> = rev. 1.21,',
     'righe <span style="background:#edf6f6;padding:0 2mm">grigio acqua</span> = rev. 1.21, righe <span style="background:#f7f3e6;padding:0 2mm">sabbia</span> = rev. 1.22,')

REV = ('<tr class="r122"><td>1.22</td><td>proposta da Claude Code e approvata 27/10/2026<br>eseguita da Brik81 il 27/10</td>'
       '<td>Tolti nel foglio MCU l\'ingresso dal bus UHF, il pezzo di filo e l\'etichetta UHF.EN_RX_LNA, che non arrivavano a nessun pin (ERC label_dangling)</td>'
       '<td>Claude Code</td><td><b>Brik81</b></td>'
       '<td>"ok ho risolto facendo A"</td></tr>\n')
i = h.find('<h2>Registro revisioni</h2>'); j = h.find('</table>', i); h = h[:j] + REV + h[j:]

rows = ('<tr class="r122"><td>1.22-01</td><td>MCU</td><td>Bus UHF{UHF_SIG_CTRL}, uscita UHF.EN_RX_LNA (275.59, 30.48)</td>'
        '<td>ingresso dal bus, filo ed etichetta senza nessun pin collegato nel foglio MCU</td>'
        '<td>tolti. EN_RX_LNA resta generato in UHF da U701 (pin 6, inverso di EN_TX_ANT_SW, comandato da PC2): la rete continua a collegare R202, TP703 e U701 pin 6</td>'
        '<td>§34</td><td>Brik81 · 27/10</td><td>Brik81 · 27/10 12:10</td></tr>\n')
i = h.find('<h2>Registro modifiche</h2>'); j = h.find('</table>', i); h = h[:j] + rows + h[j:]

PART = '''
<section class="part" id="partU">
<div class="partlabel">Parte U</div>
<h1 class="parttitle">Rev. 1.22 – Etichetta EN_RX_LNA nel foglio MCU</h1>
</section>
<h2 id="s34">34. UHF.EN_RX_LNA</h2>
<p>L'ERC segnalava come scollegata l'etichetta UHF.EN_RX_LNA nel foglio MCU. Il segnale non è un'uscita dell'MCU: lo genera U701 (74AUP2G14) nel foglio UHF invertendo EN_TX_ANT_SW (PC2), così l'LNA è acceso solo quando il commutatore d'antenna è in ricezione. L'uscita dal bus nel foglio MCU era quindi superflua ed è stata tolta (soluzione A, fatta da Brik81).</p>
<p><b>Verifica.</b> Collegamenti della netlist identici a prima (UHF.EN_RX_LNA = R202, TP703, U701 pin 6). ERC da 114 a <b>112</b>: spariti label_dangling e hier_label_mismatch. Restano 82 lib_symbol_mismatch, 19 pin_to_pin, 6 power_pin_not_driven e 5 isolated_pin_label, che Brik81 lascia così.</p>
'''
sub1('\n</body></html>', PART + '\n</body></html>')
p.write_text(h, encoding='utf8')
print('ok')
