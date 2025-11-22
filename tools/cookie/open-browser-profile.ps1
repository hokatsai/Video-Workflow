param(
    [ValidateSet("chrome", "edge")]
    [string]$Browser = "chrome",

    [string]$ProfileName = "downloader",

    [string]$ProfilePath
)

function Get-BrowserExecutable {
    param([string]$Name)

    $paths = @()
    if ($Name -eq "chrome") {
        if ($env:ProgramFiles) {
            $paths += Join-Path $env:ProgramFiles "Google\\Chrome\\Application\\chrome.exe"
        }
        if (${env:ProgramFiles(x86)}) {
            $paths += Join-Path ${env:ProgramFiles(x86)} "Google\\Chrome\\Application\\chrome.exe"
        }
        if ($env:LOCALAPPDATA) {
            $paths += Join-Path $env:LOCALAPPDATA "Google\\Chrome\\Application\\chrome.exe"
        }
    } elseif ($Name -eq "edge") {
        if ($env:ProgramFiles) {
            $paths += Join-Path $env:ProgramFiles "Microsoft\\Edge\\Application\\msedge.exe"
        }
        if (${env:ProgramFiles(x86)}) {
            $paths += Join-Path ${env:ProgramFiles(x86)} "Microsoft\\Edge\\Application\\msedge.exe"
        }
    }

    foreach ($p in $paths) {
        if ($p -and (Test-Path -LiteralPath $p)) {
            return $p
        }
    }

    $cmd = Get-Command "$Name.exe" -ErrorAction SilentlyContinue
    if ($cmd) {
        return $cmd.Source
    }

    throw "Browser executable not found: $Name"
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$profileRoot = Join-Path $scriptDir ".browser-profiles"

if (-not $ProfilePath) {
    $ProfilePath = Join-Path $profileRoot ("{0}-{1}" -f $Browser, $ProfileName)
}

if (-not (Test-Path -LiteralPath $profileRoot)) {
    New-Item -ItemType Directory -Path $profileRoot | Out-Null
}
if (-not (Test-Path -LiteralPath $ProfilePath)) {
    New-Item -ItemType Directory -Path $ProfilePath | Out-Null
}

$browserPath = Get-BrowserExecutable -Name $Browser
$arguments = @(
    "--user-data-dir=`"$ProfilePath`"",
    "--no-default-browser-check",
    "--no-first-run"
)

Write-Host ("Launching {0} profile at {1}" -f $Browser, $ProfilePath) -ForegroundColor Cyan
Write-Host "Login to YouTube in this window, then close it before running downloads." -ForegroundColor Yellow

Start-Process -FilePath $browserPath -ArgumentList $arguments | Out-Null
