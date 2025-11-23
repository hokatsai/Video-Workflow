<#
.SYNOPSIS
Wrapper for invoking Gemini CLI with repository-aware defaults.

.DESCRIPTION
Formats @-style targets, runs `gemini` from the repo root, and captures the
prompt plus response under 03-outputs/gemini-cli/<run-id>/.

.PARAMETER Targets
Paths (files or directories) relative to the repo root. `@` is added when omitted.

.PARAMETER Query
Instruction appended after the @ targets.

.PARAMETER Model
Optional Gemini model override (e.g., gemini-1.5-pro).

.PARAMETER OutputName
Optional folder name under 03-outputs/gemini-cli/. Defaults to timestamp.
#>
param(
    [Parameter(Mandatory = $true)]
    [string[]]$Targets,

    [Parameter(Mandatory = $true)]
    [string]$Query,

    [string]$Model,

    [string]$OutputName
)

$repoRoot = (Resolve-Path -Path (Join-Path -Path $PSScriptRoot -ChildPath "..\..\..\..")).Path
Set-Location $repoRoot

$runId = if ($OutputName) { $OutputName } else { Get-Date -Format "yyyyMMdd-HHmmss" }
$logRoot = Join-Path $repoRoot "03-outputs/gemini-cli"
$runDir = Join-Path $logRoot $runId
New-Item -ItemType Directory -Path $runDir -Force | Out-Null

$promptTargets = $Targets | ForEach-Object {
    if ($_ -match "^@") { $_ } else { "@$_" }
}
$promptText = (($promptTargets + $Query).Trim()) -join " "
Set-Content -Path (Join-Path $runDir "prompt.txt") -Value $promptText -Encoding UTF8

$geminiArgs = @()
if ($Model) {
    $geminiArgs += "-m"
    $geminiArgs += $Model
}
$geminiArgs += $promptText

Write-Host "Running: gemini $($geminiArgs -join ' ')" -ForegroundColor Cyan

$result = & gemini @geminiArgs 2>&1
$result | Tee-Object -FilePath (Join-Path $runDir "response.txt") | Out-Host

return @{
    RunDirectory = $runDir
    Prompt = $promptText
    Output = $result
}
