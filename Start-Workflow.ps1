# =============================================================================
# Video Workflow Master Control Script
# Author: Gemini
# Version: 1.0
#
# This script provides a central, menu-driven interface to run all
# video processing workflows.
# =============================================================================

# Get the directory of the currently running script to build relative paths
$PSScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

# --- Define Paths to our Playbook Scripts ---
$cookieToolsDir = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '01-system\tools\ops\video-workflow\cookie')).Path
$downloadScript = Join-Path $cookieToolsDir "download-video.ps1"
$subtitlesScript = Join-Path $cookieToolsDir "get-subtitles.ps1"
$transcribeScript = Join-Path $cookieToolsDir "run-transcription.ps1"

# --- Main Menu Loop ---
while ($true) {
    Clear-Host
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host "  Video Workflow Automation System" -ForegroundColor White
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host "Please choose a workflow to execute:"
    Write-Host "1. Download Video Only" -ForegroundColor Cyan
    Write-Host "2. Download Subtitles Only" -ForegroundColor Cyan
    Write-Host "3. Transcribe a Local Video File" -ForegroundColor Cyan
    Write-Host "4. Full Workflow: Download & Transcribe" -ForegroundColor Green
    Write-Host "Q. Quit" -ForegroundColor Red
    Write-Host

    $choice = Read-Host -Prompt "Enter your choice"

    switch ($choice) {
        "1" {
            $url = Read-Host -Prompt "Please enter the YouTube URL"
            if ($url) {
                & $downloadScript -Url $url
            }
        }
        "2" {
            $url = Read-Host -Prompt "Please enter the YouTube URL"
            if ($url) {
                & $subtitlesScript -Url $url
            }
        }
        "3" {
            $localPath = Read-Host -Prompt "Please enter the full path to the local video file"
            if ($localPath) {
                & $transcribeScript -VideoPath $localPath
            }
        }
        "4" {
            $url = Read-Host -Prompt "Please enter the YouTube URL for the full workflow"
            if ($url) {
                # Step 1: Download the video and capture the output
                Write-Host "`n--- STEP 1: DOWNLOADING VIDEO ---`n" -ForegroundColor Yellow
                $output = & $downloadScript -Url $url | Out-String
                
                # Check if download was successful before proceeding
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "`nDownload successful. Analyzing output to find video path..." -ForegroundColor Green
                    
                    # Step 2: Extract the video path from the download log
                    $match = $output | Select-String -Pattern '\[Merger\] Merging formats into "([^"]+)"'
                    
                    if ($match) {
                        $videoPath = $match.Matches[0].Groups[1].Value
                        Write-Host "Video path found: $videoPath" -ForegroundColor Cyan
                        
                        # Step 3: Run transcription on the downloaded video
                        Write-Host "`n--- STEP 2: TRANSCRIBING VIDEO ---`n" -ForegroundColor Yellow
                        & $transcribeScript -VideoPath $videoPath
                    } else {
                        Write-Error "Could not determine the downloaded video path from the log. Transcription cannot proceed."
                    }
                } else {
                    Write-Error "Video download failed. The workflow has been stopped."
                }
            }
        }
        "Q" {
            Write-Host "Exiting." -ForegroundColor Yellow
            return # Exit the script
        }
        default {
            Write-Warning "Invalid choice. Please try again."
        }
    }

    Write-Host "`nWorkflow finished. Press Enter to return to the main menu." -ForegroundColor Yellow
    Read-Host
}
