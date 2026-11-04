# SYMPHONY V2 – regole di progetto

## Reportistica delle modifiche hardware
- Il log delle modifiche è in LaTeX: report/simphony_v2_log.tex (preambolo + \input), una entry per modifica in report/entries/NNN_titolo-breve.tex. Il PDF compilato è report/simphony_v2_log.pdf.
- Lo scrive SOLO il subagent `hw-report-writer` (.claude/agents/hw-report-writer.md).
- Dopo ogni modifica hardware completata (e dopo ogni decisione di Brik81 su un problema, anche senza modifica) l'agente principale invoca hw-report-writer passandogli un riepilogo COMPLETO e autosufficiente: cosa è cambiato, dove (file, schede, componenti, net), valori prima/dopo, codici JLCPCB/Mouser, motivazione, citazione testuale dell'approvazione di Brik81, criticità aperte, verifiche da fare. Il subagent non vede la conversazione: deve ricevere tutto dall'agente principale.
- L'agente principale non scrive né legge file LaTeX.
- Il vecchio flusso HTML (report_src/buildNNN.py → symphony_version_log.pdf) non si usa più.
