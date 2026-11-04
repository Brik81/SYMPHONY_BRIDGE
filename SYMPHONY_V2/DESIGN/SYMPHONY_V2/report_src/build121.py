import pathlib
d = pathlib.Path(__file__).parent
p = d / 'symphony_version_log.html'
h = p.read_text(encoding='utf8')

def sub1(o, rep):
    global h
    assert h.count(o) == 1, o[:60]
    h = h.replace(o, rep)

sub1('symphony_version_log · rev. 1.20"', 'symphony_version_log · rev. 1.21"')
sub1("<div><b>1.20</b> del 24/10/2026",
     "<div><b>1.21</b> del 24/10/2026 – origine del footprint CPH3225A al centro; testo spurio tolto dal foglio principale; U701 verificato</div><div>1.20 del 24/10/2026")
sub1('tr.r120 td {', 'tr.r121 td { background: #edf6f6 !important; }\ntr.r120 td {')
sub1('<li><a href="#partS">Parte S – Rev. 1.20: S-09, pin non usati dell\'MCU, VBAT del DS3231M</a></li>',
     '<li><a href="#partS">Parte S – Rev. 1.20: S-09, pin non usati dell\'MCU, VBAT del DS3231M</a></li>\n'
     '<li><a href="#partT">Parte T – Rev. 1.21: footprint CPH3225A e pulizia</a></li>')
sub1('righe <span style="background:#fdeef4;padding:0 2mm">rosa tenue</span> = rev. 1.20,',
     'righe <span style="background:#fdeef4;padding:0 2mm">rosa tenue</span> = rev. 1.20, righe <span style="background:#edf6f6;padding:0 2mm">grigio acqua</span> = rev. 1.21,')

REV = ('<tr class="r121"><td>1.21</td><td>richiesta e approvata 24/10/2026<br>eseguita da Claude Code e Brik81 il 24/10</td>'
       '<td>Origine del footprint CPH3225A spostata al centro di pad e corpo (era fuori centro di 0.3 mm in X e Y). Il testo "cd C:\\..." nel foglio principale è stato tolto da Brik81. U701 confermato come simbolo a più unità, non doppione</td>'
       '<td>Claude Code</td><td><b>Brik81</b></td>'
       '<td>"u701 non è un doppione è un simbolo suddiviso in diversi simboli indipendenti, modifica l\'origine, al 3D me la sbrigo io, cava la scritta cd ..."</td></tr>\n')
i = h.find('<h2>Registro revisioni</h2>'); j = h.find('</table>', i); h = h[:j] + REV + h[j:]
sub1('Rev. 1.20: <code>MCU.kicad_sch</code>',
     'Rev. 1.21: <code>CPH3225A.kicad_mod</code> prima della modifica salvato in <code>bak_pre121/</code>. Rev. 1.20: <code>MCU.kicad_sch</code>')

N = [
 ('1.21-01', 'libreria', 'UHF_LIB/FOOTPRINT/passive_v2.pretty/cap.pretty/CPH3225A.kicad_mod',
  'pad 1 a (−0.8, −0.3), pad 2 a (1.4, −0.3): origine spostata di 0.3 mm rispetto al centro; modello 3D con offset (0.3, 0.3, 0.59)',
  'tutto il disegno traslato di (−0.3, +0.3) mm: pad a (∓1.1, 0), corpo, serigrafia, courtyard e testi centrati sull\'origine. Offset del modello 3D portato a (0, 0, 0.59) per restare allineato. Percorso del file 3D (assoluto, cartella Download) invariato: lo sistema Brik81',
  'Brik81 · 24/10', 'Claude Code · 24/10'),
 ('1.21-02', 'radice', 'Testo "cd C:\\Users\\alex2\\…" incollato per sbaglio', 'presente', 'tolto', 'Brik81 · 24/10', 'Brik81 · 24/10 17:50'),
 ('1.21-03', 'UHF', 'U701 74AUP2G14', 'segnalato come possibile doppione', 'nessuna modifica: simbolo a più unità (due inverter + alimentazione), un solo componente in BOM', 'Brik81 · 24/10', '–'),
]
rows = ''.join(f'<tr class="r121"><td>{a}</td><td>{b}</td><td>{c}</td><td>{q}</td><td>{r}</td><td>§33</td><td>{ap}</td><td>{ex}</td></tr>\n'
               for a, b, c, q, r, ap, ex in N)
i = h.find('<h2>Registro modifiche</h2>'); j = h.find('</table>', i); h = h[:j] + rows + h[j:]

PART = '''
<section class="part" id="partT">
<div class="partlabel">Parte T</div>
<h1 class="parttitle">Rev. 1.21 – Footprint CPH3225A e pulizia</h1>
</section>
<h2 id="s33">33. Origine del footprint CPH3225A</h2>
<p>Il footprint dei supercap C415…C424 aveva l'origine non al centro: il pick-and-place di JLCPCB usa l'origine come centro del componente, quindi i 10 supercap sarebbero stati montati spostati di circa 0.4 mm. Ora pad, corpo, serigrafia e courtyard sono centrati sull'origine (pad a ±1.1 mm). Verificato con l'esportazione SVG del footprint. Netlist ed ERC dello schema invariati (114). Il percorso del modello 3D resta da rendere relativo al progetto (lo fa Brik81).</p>
'''
sub1('\n</body></html>', PART + '\n</body></html>')
p.write_text(h, encoding='utf8')
print('ok')
