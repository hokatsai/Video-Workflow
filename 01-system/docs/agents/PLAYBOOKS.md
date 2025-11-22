# Playbooks

Document common intents here using the Lean playbook format (phrase -> intent -> steps -> outputs under `03-outputs/<tool>/`).

## Playbook: Answer In Traditional Chinese
- **Phrases / Aliases**: "respond in Chinese", "use Traditional Chinese", "all future replies must be Chinese" (and zh-TW equivalents like「之後回覆都用中文」)。
- **Intent**: Once triggered, keep all future responses in Traditional Chinese until the user explicitly changes the preference.
- **Steps**:
  1. Detect when the user asks for replies in Chinese (any phrasing similar to the aliases above).
  2. Switch immediately to Traditional Chinese for all subsequent outputs.
  3. Continue responding in Traditional Chinese until the user specifies another language.
- **Outputs**: No filesystem artifact; conversational commitment only.
## Playbook: Gemini Large-Scale Overview
- **Phrases / Aliases**: "give me an overview with Gemini", "summarize the whole repo", "use Gemini CLI for architecture"
- **Intent**: Capture a macro-level summary of one or more directories/files that exceed in-context limits.
- **Steps**:
  1. Confirm scope (directories/files) and expected focus (architecture, dependencies, etc.).
  2. From repo root, run `pwsh tools/gemini-run.ps1 -Targets <paths> -Query "<prompt>" [-Model <override>]`.
  3. Inspect `response.txt` for the generated summary; relay key findings referencing the log path.
- **Outputs**: `03-outputs/gemini-cli/<run-id>/response.txt`

## Playbook: Gemini Implementation Audit
- **Phrases / Aliases**: "check if <feature> exists", "verify auth via Gemini", "Gemini security review"
- **Intent**: Use Gemini CLI to verify whether a specific implementation (feature, pattern, safeguard) exists across modules.
- **Steps**:
  1. Gather specific feature criteria plus target directories (e.g., `@src/ @api/`).
  2. Execute `pwsh tools/gemini-run.ps1 -Targets <paths> -Query "Has <feature>? Show files/functions"` and capture the log.
  3. Summarize Gemini's findings, cite file paths, and note any follow-up manual inspections.
- **Outputs**: `03-outputs/gemini-cli/<run-id>/response.txt`

## Playbook: Setup Video Workflow Environment
- **Phrases / Aliases**: "setup video workflow", "initialize video environment", "prepare for video analysis"
- **Intent**: Create a stable and self-contained Python virtual environment for video processing tasks to ensure all dependencies are met and to perform a pre-flight check.
- **Steps**:
  1.  Create a equirements.txt file listing all necessary Python packages (whisperx, fmpeg-python, etc.).
  2.  Create a setup script (e.g., setup-video-env.ps1) that:
      a. Creates a Python virtual environment (.venv).
      b. Activates it.
      c. Installs the packages from equirements.txt.
  3.  Execute the setup script.
  4.  Perform a "pre-flight check" by transcribing a very short, silent audio file to force all models to download and compile, catching any environment/hardware issues upfront.
  5.  Save the fact that the environment is ready for future tasks.
- **Outputs**:
  - 	ools/video/requirements.txt
  - 	ools/video/setup-video-env.ps1
  - .venv directory (added to .gitignore).

## Playbook: Optimized Video Analysis
- **Phrases / Aliases**: "analyze this video", "summarize the lecture", "get key points from this course video", "summarize video with timestamps"
- **Intent**: Transcribe and summarize a video lecture efficiently and robustly, handling long videos by chunking and **including relevant timestamps** in the summary.
- **Steps**:
  1. **Pre-flight Check**: Verify that the video workflow environment is set up. If not, run the "Setup Video Workflow Environment" playbook first.
  2. **Pre-computation & User Feedback**:
      a. Use `ffprobe` to get video duration.
      b. If the video is long (>10 minutes), warn the user about the expected processing time and offer to process a shorter segment as a sample.
  3. **Chunking**:
      a. Create a temporary directory (e.g., `03-outputs/temp_audio_chunks`).
      b. Use `ffmpeg` to split the source audio into smaller, 10-minute WAV files within that directory.
  4. **Parallel Transcription**:
      a. For each audio chunk, run `whisperx` in a separate, parallel process. Generate timestamped output (e.g., `.srt` or `.json`).
      b. Use `--compute_type auto` to let `whisperx` choose the best backend, but have a fallback to `--compute_type float32` if a `float16` error occurs.
  5. **Aggregation & Timestamped Summarization**:
      a. Concatenate the *timestamped* transcript data (e.g., from `.srt` files) from all chunks in the correct order.
      b. Process the timestamped transcript to identify key concepts and associate them with their respective timestamps.
  6. **Output & Cleanup**:
      a. Save the final summary, **including timestamps**, to the user's preferred directory and format (`.txt` by default).
      b. Delete the `temp_audio_chunks` directory.
- **Outputs**:
  - A summary file **with timestamps** (e.g., `03-outputs/summaries/声乐教学总结/Lesson_1_Summary_(带时间戳).txt`).
  - Temporary audio chunks during processing.
