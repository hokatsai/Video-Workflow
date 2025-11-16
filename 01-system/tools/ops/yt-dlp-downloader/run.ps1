param(
    [Parameter(Mandatory=$true)]
    [string]$Url,
    [string]$Format = 'bestvideo+bestaudio/best',
    [string]$OutputDir,
    [string[]]$AdditionalArgs = @(),
    [string]$CookiesFromBrowser,
    [string]$CookiesFile
)

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..\..\..\..')
if (-not $OutputDir) {
    $OutputDir = Join-Path $repoRoot '03-outputs\yt-dlp-downloader'
}
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

if (-not (Get-Command yt-dlp -ErrorAction SilentlyContinue)) {
    Write-Error 'yt-dlp command not found in PATH. Install yt-dlp and try again.'
    exit 1
}

$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$runDir = Join-Path $OutputDir $timestamp
New-Item -ItemType Directory -Path $runDir -Force | Out-Null
$logPath = Join-Path $runDir 'run.log'

$arguments = @('-P', $runDir, '-f', $Format)

if ($CookiesFromBrowser) {
    $arguments += @('--cookies-from-browser', $CookiesFromBrowser)
}
if ($CookiesFile) {
    $arguments += @('--cookies', $CookiesFile)
}

$arguments += $AdditionalArgs + @($Url)

"[info] Starting yt-dlp run for $Url" | Tee-Object -FilePath $logPath
try {
    & yt-dlp @arguments 2>&1 | Tee-Object -FilePath $logPath -Append
    if ($LASTEXITCODE -ne 0) {
        throw "yt-dlp exited with code $LASTEXITCODE"
    }
    "[info] Completed. Files stored in $runDir" | Tee-Object -FilePath $logPath -Append
} catch {
    "[error] $_" | Tee-Object -FilePath $logPath -Append
    exit 1
}
