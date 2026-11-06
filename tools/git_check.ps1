# Hook "Stop" di Claude Code: se le modifiche non committate sono grosse,
# blocca la chiusura del turno e chiede a Claude di committare e poi di chiedere a Brik81 se pushare.
# Soglie modificabili qui sotto.
$SOGLIA_RIGHE = 150      # righe cambiate (aggiunte+tolte) nei file tracciati
$SOGLIA_NUOVI = 1        # file nuovi non tracciati

$inp = [Console]::In.ReadToEnd() | ConvertFrom-Json -ErrorAction SilentlyContinue
if ($inp -and $inp.stop_hook_active) { exit 0 }   # evita loop

$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo
if ((Test-Path .git\MERGE_HEAD) -or (Test-Path .git\rebase-merge)) { exit 0 }

$righe = 0
git diff HEAD --numstat 2>$null | ForEach-Object {
  $p = $_ -split "`t"
  if ($p[0] -ne '-') { $righe += [int]$p[0] + [int]$p[1] } else { $righe += 1000 }  # binari = grossi
}
$nuovi = @(git ls-files --others --exclude-standard 2>$null).Count

if ($righe -ge $SOGLIA_RIGHE -or $nuovi -ge $SOGLIA_NUOVI) {
  $reason = "Modifiche non committate grosse: $righe righe cambiate, $nuovi file nuovi. " +
            "Usa l'agente git-guardian (o segui .claude/agents/git-guardian.md): fai il commit con un messaggio descrittivo, " +
            "poi chiedi a Brik81 se vuole fare il push. Non pushare senza un si esplicito."
  @{ decision = 'block'; reason = $reason } | ConvertTo-Json -Compress
}
exit 0
