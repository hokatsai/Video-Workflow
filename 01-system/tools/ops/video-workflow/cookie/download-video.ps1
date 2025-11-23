param(
    [Parameter(Mandatory = $true)]
    [string]$Url,

    [string]$Browser = "chrome",

    [string]$BrowserProfilePath,

    [string]$CookieFile = "cookies.txt"
)

function Invoke-YtDlp {
    param([string[]]$Arguments)

    $captured = @()
    & yt-dlp @Arguments 2>&1 | ForEach-Object {
        $captured += $_
        Write-Host $_
    }

    return [pscustomobject]@{
        ExitCode = $LASTEXITCODE
        Output   = $captured
    }
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$workspaceRoot = (Resolve-Path -LiteralPath (Join-Path $scriptDir '..\..\..\..\..')).Path

$outputRoot = Join-Path $workspaceRoot "03-outputs"
if (-not (Test-Path -LiteralPath $outputRoot)) {
    New-Item -ItemType Directory -Path $outputRoot | Out-Null
}

$downloadDir = Join-Path $outputRoot "video"
if (-not (Test-Path -LiteralPath $downloadDir)) {
    New-Item -ItemType Directory -Path $downloadDir | Out-Null
}

$profileRoot = Join-Path $scriptDir ".browser-profiles"
$defaultProfile = Join-Path $profileRoot ("{0}-downloader" -f $Browser)

if (-not $BrowserProfilePath -and (Test-Path -LiteralPath $defaultProfile)) {
    $BrowserProfilePath = $defaultProfile
}

$browserArgument = $Browser
if ($BrowserProfilePath) {
    if (-not (Test-Path -LiteralPath $BrowserProfilePath)) {
        throw "BrowserProfilePath not found: $BrowserProfilePath"
    }

    $resolvedProfile = (Resolve-Path -LiteralPath $BrowserProfilePath).Path
    $browserArgument = "{0}:{1}" -f $Browser, $resolvedProfile
    Write-Host ("Using dedicated profile: {0}" -f $resolvedProfile) -ForegroundColor Cyan
}

$outputTemplate = Join-Path $downloadDir "%(title)s [%(id)s].%(ext)s"

$baseArguments = @(
    "--restrict-filenames",
    "--force-overwrites",
    "-f", 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    "-S", "height:1080,fps:60,height:-,fps:-",
    "-N", "8",
    "-c",
    "--retries", "infinite",
    "--fragment-retries", "infinite",
    "--merge-output-format", "mp4",
    "-o", $outputTemplate,
    $Url
)

Write-Host ("Downloading with {0}" -f $browserArgument) -ForegroundColor Cyan
$result = Invoke-YtDlp -Arguments (@("--cookies-from-browser", $browserArgument) + $baseArguments)

$shouldFallback = $result.ExitCode -ne 0 -and (($result.Output -join "`n") -match 'Could not copy Chrome cookie database')
if ($shouldFallback -and (Test-Path -LiteralPath $CookieFile)) {
    Write-Warning ("Falling back to cookie file: {0}" -f $CookieFile)
    $result = Invoke-YtDlp -Arguments (@("--cookies", $CookieFile) + $baseArguments)
}

exit $result.ExitCode
