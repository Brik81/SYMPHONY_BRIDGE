import pathlib
d = pathlib.Path(__file__).parent
p = d / 'symphony_version_log.html'
h = p.read_text(encoding='utf8')

def sub1(o, rep):
    global h
    assert h.count(o) == 1, o[:60]
    h = h.replace(o, rep)


sub1('symphony_version_log · rev. 1.28"', 'symphony_version_log · rev. 1.29"')
sub1("<div><b>1.28</b> del 30/10/2026",
     "<div><b>1.29</b> del 02/11/2026 – R-04 chiuso senza modifiche allo schema: limite di potenza e sequenza TX affidati al firmware; raccolta delle note per il firmware (§41)</div><div>1.28 del 30/10/2026")
sub1('tr.r128 td {', 'tr.r129 td { background: #edf2e6 !important; }\ntr.r128 td {')
sub1('<li><a href="#partAA">Parte AA – Rev. 1.28: condensatori RF GQM1875 0603 (R-10) e decisione su J15 (R-09)</a></li>',
     '<li><a href="#partAA">Parte AA – Rev. 1.28: condensatori RF GQM1875 0603 (R-10) e decisione su J15 (R-09)</a></li>\n'
     '<li><a href="#partAB">Parte AB – Rev. 1.29: potenza TX (R-04) e note per il firmware</a></li>')
sub1('cipria</span> = rev. 1.28,',
     'cipria</span> = rev. 1.28, righe <span style="background:#edf2e6;padding:0 2mm">salvia</span> = rev. 1.29,')

REV = ('<tr class="r129"><td>1.29</td><td>problema R-04 della revisione indipendente del 27/10/2026<br>decisione di Brik81 del 02/11, registrata da Claude Code</td>'
       '<td>Nessuna modifica allo schema. Il limite della potenza in uscita (≤ 31 dBm all\'antenna) e la sequenza di trasmissione sono requisiti del firmware; misura obbligatoria sul prototipo; R242/R243 restano come regolazione della VAPC. Aggiunta la raccolta delle note per il firmware (§41)</td>'
       '<td>Claude Code</td><td><b>Brik81</b></td>'
       '<td>"si se l\'hw è corretto andiamo di A e lasciamo scritto al firmwarsita" (02/11)</td></tr>\n')
i = h.find('<h2>Registro revisioni</h2>'); j = h.find('</table>', i); h = h[:j] + REV + h[j:]
sub1('Rev. 1.28: <code>UHF.kicad_sch</code>',
     'Rev. 1.29: nessun file di progetto modificato. Rev. 1.28: <code>UHF.kicad_sch</code>')

rows = ('<tr class="r129"><td>1.29-01</td><td>UHF</td><td>Catena TX (IC204 → pad → IC2 → FL201 → IC202)</td>'
        '<td>Con il Si4464 a +20 dBm il PA è in saturazione profonda (≈ +9 dBm in ingresso, ne bastano ≈ −9). Al commutatore arrivano ≈ 32,5 dBm, contro un massimo assoluto dell\'HMC349 di 33,5 dBm (30 dBm in hot switching); l\'LFCG-490+ a 85 °C regge ≈ 1,9 W</td>'
        '<td>Nessuna modifica all\'hardware. Requisiti firmware F-01 e F-02 (§41) e misura M-01 sul prototipo. Se Pout supera i 31 dBm anche con il limite firmware, si ritoccano R242/R243</td>'
        '<td>R-04, §41</td><td>Brik81 · 02/11</td><td>—</td></tr>\n')
i = h.find('<h2>Registro modifiche</h2>'); j = h.find('</table>', i); h = h[:j] + rows + h[j:]

PART = """
<section class="part" id="partAB">
<div class="partlabel">Parte AB</div>
<h1 class="parttitle">Rev. 1.29 – Potenza TX (R-04) e note per il firmware</h1>
</section>
<h2 id="s41">41. R-04 e raccolta delle note per il firmware</h2>
<p><b>R-04.</b> L'hardware della catena TX è corretto. Il PA è protetto in ingresso: anche con il Si4464 al massimo arrivano ≈ +9 dBm, contro un massimo assoluto di +13 dBm. Il margine che manca è a valle, sul commutatore e sul filtro. Un pad più grande non risolverebbe, perché in saturazione la potenza in uscita resta circa la Psat qualunque sia il pilotaggio. Le leve vere sono il pilotaggio, cioè PA_PWR_LVL (sotto la compressione il PA è lineare), e la VAPC (partitore R242/R243). Brik81 ha scelto di non modificare lo schema e di affidare il limite al firmware. Con modulazione FSK/GFSK lavorare vicino alla saturazione va bene, perché l'inviluppo è costante.</p>
<p><b>Come è fatto l'hardware.</b> Un solo pin, PC2 (rete UHF.EN_TX_ANT_SW), comanda insieme tre cose: il CTRL dell'HMC349, l'abilitazione dell'APC del PA (Q701 P-MOS con pull-up R702 verso 3V3, gate tramite R703: PC2 basso = APC alimentata) e, tramite l'invertitore U701, EN_RX_LNA. Con PC2 in alta impedenza (boot, reset dell'MCU) il pull-up tiene il PA spento. Il commutatore e l'APC si muovono quindi insieme. La RF però c'è solo quando il Si4464 trasmette: per non commutare mai con la RF presente basta cambiare PC2 solo quando il Si4464 non è in TX.</p>
<div class="box">
<p><b>Note per il firmware: requisiti hardware da rispettare</b> (raccolta di quelle sparse nelle revisioni precedenti, più le nuove di R-04)</p>
<table>
<tr><th>ID</th><th>Argomento</th><th>Requisito</th><th>Origine</th></tr>
<tr><td><b>F-01</b></td><td>Potenza TX</td><td><b>Limite rigido</b> su PA_PWR_LVL del Si4464, tarato sul prototipo (misura M-01) per avere <b>≤ 31 dBm</b> all'uscita d'antenna. Il valore va scritto come costante non modificabile da telecomando, o al più con una saturazione lato firmware. Il Si4464 non deve mai andare a +20 dBm</td><td>R-04 (rev 1.29), §3, S-07</td></tr>
<tr><td><b>F-02</b></td><td>Sequenza TX/RX</td><td>Entrata in TX: Si4464 non in TX → PC2 su "TX" (commutatore su TX, APC del PA alimentata, LNA spento) → attendere che commutatore e PA si assestino → Si4464 START_TX. Uscita: fine pacchetto, Si4464 fuori da TX (READY/RX) → solo dopo PC2 su "RX". <b>Mai cambiare PC2 mentre il Si4464 trasmette</b> (hot switching dell'HMC349, limite 30 dBm)</td><td>R-04 (rev 1.29), §4, 1.1-04</td></tr>
<tr><td><b>F-03</b></td><td>Durata TX</td><td>Preferire trasmissioni a impulsi o con duty cycle limitato. L242 (NRS2012, 1,7 A ΔT 40 °C) e l'LFCG-490+ (≈ 1,9 W a 85 °C) scaldano in trasmissione continua alla massima potenza. Se serve TX continuo, ridurre F-01</td><td>rev 1.25, R-04</td></tr>
<tr><td><b>F-04</b></td><td>Clock del Si4464</td><td>POWER_UP con l'opzione TCXO (TCXO a 32 MHz su XIN, XOUT flottante) e banco capacità XO (GLOBAL_XO_TUNE) = 0</td><td>§2</td></tr>
<tr><td><b>F-05</b></td><td>Reset del Si4464</td><td>PC4 (RF_MR_N) basso = reset della radio. Dopo il rilascio di ~MR o all'accensione aspettare almeno 200 ms (ritardo del supervisore IC205) più il POR del Si4464 prima di mandare comandi SPI, e controllare CTS</td><td>supervisore IC205</td></tr>
<tr><td><b>F-06</b></td><td>Clock dell'MCU</td><td>HSE_VALUE = 24000000 (quarzo Y1 da 24 MHz). Con un valore diverso UART, USB e timer partono alla frequenza sbagliata</td><td>S-04, rev 1.15</td></tr>
<tr><td><b>F-07</b></td><td>Console</td><td>USART1 su PA9/PA10 (AF7), collegata al CH340 U402, non UART4. Bootloader: BOOT0 (PH3, TP1) alto al reset, poi STM32CubeProgrammer in UART</td><td>rev 1.8</td></tr>
<tr><td><b>F-08</b></td><td>Sensori di temperatura</td><td>ADC1 canale 16 (PB1, V_TEMP_PA) e canale 2 (PC1, V_TEMP_BUCK), misura raziometrica su VDDA = 3V3. Calibrazione a un punto per canale (offset del TLV9051 ≈ ±0,9 °C)</td><td>S-06, rev 1.17–1.18, R-18</td></tr>
<tr><td><b>F-09</b></td><td>RTC DS3231M</td><td>All'avvio EN32KHZ = 0 (registro 0Fh, bit 3): l'uscita 32 kHz non è usata e consuma il backup. Dopo un'interruzione lunga controllare il flag OSF e risincronizzare l'ora</td><td>S-09, rev 1.20</td></tr>
</table>
<p><b>Misure obbligatorie sul prototipo.</b> <b>M-01:</b> Pout all'uscita d'antenna su carico da 50 Ω (attenuatore di potenza), alla temperatura ambiente e se possibile a caldo, con il Si4464 al valore F-01 e al massimo. Se con il valore F-01 si superano i 31 dBm, ridurre la VAPC con R242/R243. <b>M-02:</b> adattamento d'uscita del PA (S22 o potenza in banda 430–440 MHz) con L242 = NRS2012 e C260 = 27 pF (rev 1.25).</p>
</div>
<p>Dati non verificati sul datasheet: guadagno ≈ 42 dB e P3dB ≈ 34 dBm (riepilogo EVB Qorvo del 30/06/2025, alla tensione della EVB); la curva Pout/VAPC del QPA9510. Per questo il valore di F-01 si fissa con la misura M-01 e non con un calcolo.</p>
"""
sub1('\n</body></html>', PART + '\n</body></html>')
p.write_text(h, encoding='utf8')
print('ok')
