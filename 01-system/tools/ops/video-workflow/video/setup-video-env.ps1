<#
.SYNOPSIS
    Sets up the Python virtual environment for the video processing workflow.
#>
param()

Write-Host "--- Setting up Video Workflow Environment ---" -ForegroundColor Green

# Get the script's directory to resolve paths relative to it
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootDir = (Resolve-Path -Path (Join-Path -Path $scriptDir -ChildPath "..\..\..\..\..")).Path
$venvPath = Join-Path -Path $rootDir -ChildPath ".venv"
$requirementsPath = Join-Path -Path $scriptDir -ChildPath "requirements.txt"

# 1. Check for Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not found in your PATH. Please install Python and try again."
    exit 1
}
Write-Host "[1/4] Python found."

# 2. Create Python virtual environment
if (Test-Path -Path $venvPath) {
    Write-Host "[2/4] Virtual environment '.venv' already exists. Skipping creation."
} else {
    Write-Host "[2/4] Creating Python virtual environment at: $venvPath"
    python -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create virtual environment."
        exit 1
    }
}

# 3. Install dependencies from requirements.txt
Write-Host "[3/4] Installing dependencies from $requirementsPath..."
# Construct the path to the pip executable within the venv
$pipPath = Join-Path -Path $venvPath -ChildPath "Scripts\pip.exe"
& $pipPath install -r $requirementsPath
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to install dependencies. Please check the output above."
    exit 1
}
Write-Host "[3/4] Dependencies installed successfully."

# 4. Add .venv to .gitignore if not already present
$gitignorePath = Join-Path -Path $rootDir -ChildPath ".gitignore"
$ignoreEntry = "/.venv"
if (Test-Path $gitignorePath -And -not (Select-String -Path $gitignorePath -Pattern $ignoreEntry -Quiet)) {
    Write-Host "[4/4] Adding '$ignoreEntry' to .gitignore."
    Add-Content -Path $gitignorePath -Value $ignoreEntry
} else {
    Write-Host "[4/4] .gitignore already contains '$ignoreEntry' or does not exist."
}


Write-Host "--- Environment setup complete! ---" -ForegroundColor Green
Write-Host "You can now use the video analysis tools."
