# Download the latest database backups from the VPS to this PC (off-site copy).
# Usage: npm run backup:pull
$ErrorActionPreference = 'Stop'

# Windows' own tar: Git Bash ships a GNU tar that reads "C:" as a remote host.
$tar = Join-Path $env:SystemRoot 'System32\tar.exe'

$server = if ($env:DEPLOY_SERVER) { $env:DEPLOY_SERVER } else { 'ubuntu@57.131.145.27' }
$dest   = Join-Path $env:USERPROFILE 'Backups\giuseppecorso.it'
New-Item -ItemType Directory -Force $dest | Out-Null

# Newest dump of each database, packed by root and streamed over ssh.
$archive = Join-Path $dest ("backup-" + (Get-Date -Format 'yyyyMMdd-HHmmss') + ".tar")
# The folder is readable by root only, so the whole command runs under sudo.
$remote  = "sudo sh -c 'cd /var/backups/giuseppecorso && tar -cf - `$(ls -t listmonk-*.sql.gz | head -1) `$(ls -t umami-*.sql.gz | head -1)'"
cmd /c "ssh $server `"$remote`" > `"$archive`""
if ($LASTEXITCODE -ne 0 -or (Get-Item $archive).Length -lt 1024) { throw 'Download failed' }

# Keep the 5 most recent local copies.
Get-ChildItem $dest -Filter 'backup-*.tar' | Sort-Object LastWriteTime -Descending | Select-Object -Skip 5 | Remove-Item
Write-Host "Saved: $archive"
& $tar -tf $archive
