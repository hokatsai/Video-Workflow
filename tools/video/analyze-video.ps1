<#
.SYNOPSIS
    Analyzes a video file by extracting audio, transcribing with WhisperX,
    and preparing for timestamped summarization.
.DESCRIPTION
    This script orchestrates the video analysis workflow. It takes a video path,
    extracts audio, splits it into chunks, transcribes each chunk using WhisperX,
    and then combines the timestamped transcripts.
    It expects the Python virtual environment (setup by setup-video-env.ps1) to be active.
.PARAMETER VideoPath
    The full path to the video file to be analyzed.
.PARAMETER OutputBaseName
    The base name for the output files (e.g., "Lesson_1_Summary").
.EXAMPLE
    .\analyze-video.ps1 -VideoPath "E:\Video-Workflow\02-inputs\網課\1\screen-20250810-172546.mp4" -OutputBaseName "声乐教学网课 - 第一课 - 知识点总结"
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$VideoPath,

    [Parameter(Mandatory=$true)]
    [string]$OutputBaseName
)

Write-Host "--- Starting Optimized Video Analysis for '$VideoPath' ---" -ForegroundColor Green

# --- Configuration ---
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootDir = (Resolve-Path -Path (Join-Path -Path $scriptDir -ChildPath "..\..")).Path
$venvPath = Join-Path -Path $rootDir -ChildPath ".venv"
$tempAudioChunksDir = Join-Path -Path $rootDir -ChildPath "03-outputs\temp_audio_chunks"
$summariesOutputDir = "E:\Video-Workflow\03-outputs\summaries\声乐教学总结" # Hardcoded as per memory

# --- Pre-flight Check: Ensure Venv is active ---
# **CRITICAL CHANGE: Always use paths relative to the virtual environment**
$pythonPath = Join-Path -Path $venvPath -ChildPath "Scripts\python.exe"
$whisperxPath = Join-Path -Path $venvPath -ChildPath "Scripts\whisperx.exe"
# --- End CRITICAL CHANGE ---

if (-not (Test-Path $venvPath -PathType Container)) {
    Write-Error "Virtual environment '.venv' not found at '$venvPath'. Please run setup-video-env.ps1 first."
    exit 1
}
if (-not (Test-Path $pythonPath)) {
    Write-Error "Python executable not found in virtual environment at '$pythonPath'. Please check your virtual environment setup."
    exit 1
}
if (-not (Test-Path $whisperxPath)) {
    Write-Error "whisperx executable not found in virtual environment at '$whisperxPath'. Please run setup-video-env.ps1 first."
    exit 1
}
Write-Host "Python virtual environment and whisperx executable verified."

# --- Cleanup previous temp chunks (if any) ---
if (Test-Path $tempAudioChunksDir) {
    Remove-Item -Path $tempAudioChunksDir -Recurse -Force
}
New-Item -ItemType Directory -Path $tempAudioChunksDir | Out-Null

# --- Step 1: Extract Audio and Get Duration ---
Write-Host "Step 1: Extracting full audio and getting duration..."
$fullAudioPath = Join-Path -Path $tempAudioChunksDir -ChildPath "full_audio.wav"
ffmpeg -y -i "$VideoPath" -vn -acodec pcm_s16le -ar 16000 -ac 1 "$fullAudioPath"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to extract full audio."
    exit 1
}

$durationOutput = ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$VideoPath"
$videoDurationSeconds = [math]::Round([double]$durationOutput)
Write-Host "Video Duration: $videoDurationSeconds seconds."

# --- Step 2: Chunking (Conceptual for now, will process full audio for simplicity) ---
# For a real implementation, this would involve splitting into 10-min chunks.
# For now, we proceed with the full audio.
Write-Host "Step 2: Skipping explicit chunking for simplicity. Processing full audio."
$audioChunks = @($fullAudioPath) # Array containing just the full audio path

# --- Step 3: Transcribe with WhisperX ---
Write-Host "Step 3: Transcribing audio with WhisperX (model: small, compute_type: float32)..."
$allSrtContent = ""
$transcriptOutputTempDir = Join-Path -Path $tempAudioChunksDir -ChildPath "transcript_output"
New-Item -ItemType Directory -Path $transcriptOutputTempDir | Out-Null

foreach ($chunkPath in $audioChunks) {
    $chunkFileName = Split-Path -Path $chunkPath -Leaf -ErrorAction SilentlyContinue
    $chunkOutputName = [System.IO.Path]::GetFileNameWithoutExtension($chunkFileName) # e.g., "full_audio"

    # WhisperX command with retries
    $maxRetries = 3
    for ($i = 0; $i -lt $maxRetries; $i++) {
        Write-Host "  Transcribing chunk '$chunkFileName' (Attempt $($i+1)/$maxRetries)..."
        # Using the absolute path for output_dir to avoid issues
        & $whisperxPath "$chunkPath" --model small --language Chinese --output_dir "$transcriptOutputTempDir" --compute_type float32 # --output_format srt
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  Transcription of '$chunkFileName' successful."
            # Append SRT content
            $srtFilePath = Join-Path -Path $transcriptOutputTempDir -ChildPath "$chunkOutputName.srt"
            if (Test-Path $srtFilePath) {
                $allSrtContent += (Get-Content -Path $srtFilePath -Raw) + "`n"
            } else {
                Write-Warning "SRT file '$srtFilePath' not found after transcription."
            }
            break
        } else {
            Write-Warning "  Transcription of '$chunkFileName' failed. Retrying..."
            Start-Sleep -Seconds 5 # Wait before retrying
        }
    }
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to transcribe chunk '$chunkFileName' after $maxRetries attempts."
        exit 1
    }
}

# --- Step 4: Aggregate and Prepare for LLM Summarization ---
Write-Host "Step 4: Preparing aggregated timestamped transcript for LLM summarization."
$aggregatedSrtPath = Join-Path -Path $tempAudioChunksDir -ChildPath "aggregated_transcript.srt"
Set-Content -Path $aggregatedSrtPath -Value $allSrtContent -Encoding UTF8

# --- Video Analysis ready for LLM summarization. ---
# Output the aggregated SRT content to standard output for direct LLM processing
[System.IO.File]::ReadAllText($aggregatedSrtPath, [System.Text.Encoding]::UTF8)

# --- Cleanup temporary audio chunks ---
Remove-Item -Path $tempAudioChunksDir -Recurse -Force -ErrorAction SilentlyContinue
