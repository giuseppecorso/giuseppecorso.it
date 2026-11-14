# One-command deploy: build locally, upload, atomic switch of the "current" symlink.
# Usage: npm run deploy
# Rollback: ssh in and point "current" to a previous folder in releases/.
$ErrorActionPreference = 'Stop'

# Windows' own tar: Git Bash ships a GNU tar that reads "C:" as a remote host.
$tar = Join-Path $env:SystemRoot 'System32\tar.exe'

$server   = if ($env:DEPLOY_SERVER) { $env:DEPLOY_SERVER } else { 'ubuntu@57.131.145.27' }
$base     = '/var/www/giuseppecorso.it'
$release  = Get-Date -Format 'yyyyMMdd-HHmmss'
$archive  = Join-Path $env:TEMP "site-$release.tgz"

Write-Host "1/3 Build"
npm run build
if ($LASTEXITCODE -ne 0) { throw 'Build failed' }

Write-Host "2/3 Upload"
& $tar -czf $archive -C dist .
if ($LASTEXITCODE -ne 0) { throw 'tar failed' }
scp -q $archive "${server}:/tmp/site-$release.tgz"
if ($LASTEXITCODE -ne 0) { throw 'scp failed' }
Remove-Item $archive

Write-Host "3/3 Activate release $release"
$remote = @"
set -e
mkdir -p $base/releases/$release
tar -xzf /tmp/site-$release.tgz -C $base/releases/$release
rm /tmp/site-$release.tgz
ln -sfn $base/releases/$release $base/current.tmp
mv -Tf $base/current.tmp $base/current
ls -1dt $base/releases/* | tail -n +6 | xargs -r rm -rf
echo "Live: `$(readlink $base/current)"
"@
$remote -replace "`r", '' | ssh $server 'bash -s'
if ($LASTEXITCODE -ne 0) { throw 'Remote activation failed' }
