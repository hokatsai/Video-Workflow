<#
.SYNOPSIS
    Downloads subtitle files for a given YouTube URL.
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$Url
)

# Get the directory of the currently running script to build relative paths
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
# Go up to the project root (now nested under 01-system/tools/ops/video-workflow)
$workspaceRoot = (Resolve-Path -LiteralPath (Join-Path $scriptDir '..\..\..\..\..')).Path

# --- Define Paths ---
# This makes the script more readable and easier to maintain.
$ytDlpPath = "C:\Users\Hoka.WIN-U73IGPCPECH\AppData\Local\Microsoft\WinGet\Packages\yt-dlp.yt-dlp_Microsoft.Winget.Source_8wekyb3d8bbwe\yt-dlp.exe"
$browserProfilePath = (Resolve-Path -LiteralPath (Join-Path $scriptDir '.browser-profiles\chrome-downloader')).Path
$browserArgument = "chrome:$browserProfilePath"
$transcriptDir = (Resolve-Path -LiteralPath (Join-Path $workspaceRoot '03-outputs\transcripts')).Path

# Ensure the output directory exists
if (-not (Test-Path -LiteralPath $transcriptDir)) {
    Write-Host "Creating transcript directory at: $transcriptDir"
    New-Item -ItemType Directory -Path $transcriptDir | Out-Null
}

# Define the output template for the subtitle file, using the video ID for a clean name
$outputTemplate = Join-Path $transcriptDir "% (id)s.%(ext)s"

# --- Execute yt-dlp ---
Write-Host "Attempting to download subtitles for URL: $Url" -ForegroundColor Cyan

# Define the arguments for the yt-dlp command
$arguments = @(
    "--cookies-from-browser", $browserArgument,
    "--write-sub",
    "--sub-lang", "en,zh-CN,zh-Hans,zh-Hant", # Attempt to get English or Chinese subtitles
    "--sub-format", "srt",
    "--skip-download", # Crucial: Do not download the video again
    "-o", $outputTemplate,
    $Url
)

# Execute the command
& $ytDlpPath @arguments

# Check the exit code and provide feedback to the user
if ($LASTEXITCODE -eq 0) {
    Write-Host "Subtitle download completed successfully." -ForegroundColor Green
} else {
    Write-Error "Subtitle download failed. Please check the output above for errors."
}
