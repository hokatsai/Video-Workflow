<#
.SYNOPSIS
    Transcribes a given video/audio file using Whisper.
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$VideoPath,

    [ValidateSet("tiny", "base", "small", "medium", "large")]
    [string]$Model = "base",

    [string]$Language = "Chinese"
)

# Get the directory of the currently running script to build relative paths
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$workspaceRoot = (Resolve-Path -LiteralPath (Join-Path $scriptDir '..\..\..\..\..')).Path

# --- Define Paths ---
$whisperPath = "C:\Users\Hoka.WIN-U73IGPCPECH\AppData\Local\Programs\Python\Python311\Scripts\whisper.exe"
$transcriptDir = (Resolve-Path -LiteralPath (Join-Path $workspaceRoot '03-outputs\transcripts')).Path

# Ensure the file to be transcribed exists
if (-not (Test-Path -LiteralPath $VideoPath)) {
    Write-Error "Input file not found: $VideoPath"
    exit 1
}

# Ensure the output directory exists
if (-not (Test-Path -LiteralPath $transcriptDir)) {
    Write-Host "Creating transcript directory at: $transcriptDir"
    New-Item -ItemType Directory -Path $transcriptDir | Out-Null
}

# --- Execute Whisper ---
Write-Host "Starting transcription for: $VideoPath" -ForegroundColor Cyan
Write-Host "Using Model: $Model, Language: $Language" -ForegroundColor Cyan

$arguments = @(
    $VideoPath,
    "--model", $Model,
    "--language", $Language,
    "--output_dir", $transcriptDir
)

# Execute the command
& $whisperPath @arguments

# Check the exit code and provide feedback
if ($LASTEXITCODE -eq 0) {
    Write-Host "Transcription completed successfully." -ForegroundColor Green
    Write-Host "Output files are located in: $transcriptDir"
} else {
    Write-Error "Transcription failed. Please check the output above for errors."
}
