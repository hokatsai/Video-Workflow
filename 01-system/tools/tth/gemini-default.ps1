<#
.SYNOPSIS
Gemini CLI shortcut defaulting to gemini-2.5-pro with automatic fallback to gemini-2.5-flash.

.DESCRIPTION
Invokes the standard gemini-run.ps1 wrapper, logs prompt/response under 03-outputs/gemini-cli/<run-id>/,
and retries with the fallback model when quota/capacity/unavailable signals are detected.

.PARAMETER Targets
Paths (files or directories) relative to the repo root. @ prefix is optional.

.PARAMETER Query
Instruction to send to Gemini.

.PARAMETER OutputName
Optional folder name under 03-outputs/gemini-cli/. If omitted, timestamp is used.

.PARAMETER PreferredModel
Primary model to try first. Defaults to gemini-2.5-pro.

.PARAMETER FallbackModel
Model used when the primary model fails due to capacity/unavailable issues. Defaults to gemini-2.5-flash.
#>
param(
    [Parameter(Mandatory = $true)]
    [string[]]$Targets,

    [Parameter(Mandatory = $true)]
    [string]$Query,

    [string]$OutputName,

    [string]$PreferredModel = "gemini-2.5-pro",

    [string]$FallbackModel = "gemini-2.5-flash"
)

$repoRoot = (Resolve-Path -Path (Join-Path -Path $PSScriptRoot -ChildPath "..\\..\\..")).Path
Set-Location $repoRoot
$geminiRunner = Join-Path $repoRoot "01-system/tools/llms/gemini-cli/gemini-run.ps1"

$commonArgs = @{
    Targets = $Targets
    Query   = $Query
}
if ($OutputName) {
    $commonArgs.OutputName = $OutputName
}

function Invoke-GeminiRun {
    param(
        [string]$Model
    )
    try {
        $result = & $geminiRunner @commonArgs -Model $Model
        $exitCode = $LASTEXITCODE
        $text = ($result.Output | Out-String)
        return @{
            ExitCode = $exitCode
            Text     = $text
            Result   = $result
        }
    }
    catch {
        return @{
            ExitCode = 1
            Text     = $_.Exception.Message
            Result   = $null
        }
    }
}

$primary = Invoke-GeminiRun -Model $PreferredModel
$needFallback = ($primary.ExitCode -ne 0) -or ($primary.Text -match "(?i)(capacity|quota|unavailable|exhausted|rate limit)")

if (-not $needFallback) {
    return $primary.Result + @{
        ModelUsed    = $PreferredModel
        FallbackUsed = $false
    }
}

Write-Warning "Primary model '$PreferredModel' unavailable/limited. Falling back to '$FallbackModel'."
$fallback = Invoke-GeminiRun -Model $FallbackModel

return $fallback.Result + @{
    ModelUsed      = $FallbackModel
    FallbackUsed   = $true
    FallbackReason = $primary.Text
}
