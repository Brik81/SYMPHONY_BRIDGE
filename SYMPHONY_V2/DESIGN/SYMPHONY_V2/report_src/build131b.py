import pathlib
p = pathlib.Path(__file__).parent / 'symphony_version_log.html'
h = p.read_text(encoding='utf8')

def sub1(o, rep):
    global h
    assert h.count(o) == 1, o[:60]
    h = h.replace(o, rep)

sub1("<p><b>Ancora aperto in R-12:</b> GPIO_PPS (pin 17), GPIOSX_0 (pin 14) e GPIOSX_2 (pin 13) non sono collegati all'MCU. Brik81 deve decidere se lasciarli così o collegare il PPS a un ingresso timer/EXTI per la sincronizzazione del tempo.</p>",
     "<p><b>Aggiornamento 02/11 – R-12 chiuso.</b> Anche GPIO_PPS (pin 17), GPIOSX_0 (pin 14) e GPIOSX_2 (pin 13) restano non collegati per decisione di Brik81: \"nono lascia stare se non è connessa fregatenene, sono li per avere nomi standard essendo per noi un connettore standard\". Le etichette servono solo a mantenere i nomi standard del connettore.</p>")
sub1("<td>R-12, §43</td><td>Brik81 · 02/11</td><td>Claude Code · 02/11</td></tr>",
     "<td>R-12, §43</td><td>Brik81 · 02/11</td><td>Claude Code · 02/11</td></tr>\n"
     "<tr class=\"r131\"><td>1.31-02</td><td>IF</td><td>J708 pin 13 GPIOSX_2, 14 GPIOSX_0, 17 GPIO_PPS</td>"
     "<td>Etichette senza collegamento all'MCU</td><td>Nessuna modifica: restano solo per i nomi standard del connettore. R-12 chiuso</td>"
     "<td>R-12, §43</td><td>Brik81 · 02/11</td><td>—</td></tr>")
p.write_text(h, encoding='utf8')
print('ok')
