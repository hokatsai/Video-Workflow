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
  2. From repo root, run `pwsh 01-system/tools/llms/gemini-cli/gemini-run.ps1 -Targets <paths> -Query "<prompt>" [-Model <override>]`.
  3. Inspect `response.txt` for the generated summary; relay key findings referencing the log path.
- **Outputs**: `03-outputs/gemini-cli/<run-id>/response.txt`

## Playbook: Gemini Implementation Audit
- **Phrases / Aliases**: "check if <feature> exists", "verify auth via Gemini", "Gemini security review"
- **Intent**: Use Gemini CLI to verify whether a specific implementation (feature, pattern, safeguard) exists across modules.
- **Steps**:
  1. Gather specific feature criteria plus target directories (e.g., `@src/ @api/`).
  2. Execute `pwsh 01-system/tools/llms/gemini-cli/gemini-run.ps1 -Targets <paths> -Query "Has <feature>? Show files/functions"` and capture the log.
  3. Summarize Gemini's findings, cite file paths, and note any follow-up manual inspections.
- **Outputs**: `03-outputs/gemini-cli/<run-id>/response.txt`

## Playbook: Setup Video Workflow Environment
- **Phrases / Aliases**: "setup video workflow", "initialize video environment", "prepare for video analysis"
- **Intent**: Create a stable and self-contained Python virtual environment for video processing tasks to ensure all dependencies are met and to perform a pre-flight check.
- **Steps**:
  1.  Create a 
equirements.txt file listing all necessary Python packages (whisperx, 
fmpeg-python, etc.).
  2.  Create a setup script (e.g., setup-video-env.ps1) that:
      a. Creates a Python virtual environment (.venv).
      b. Activates it.
      c. Installs the packages from 
equirements.txt.
  3.  Execute the setup script.
  4.  Perform a "pre-flight check" by transcribing a very short, silent audio file to force all models to download and compile, catching any environment/hardware issues upfront.
  5.  Save the fact that the environment is ready for future tasks.
- **Outputs**:
  - 01-system/tools/ops/video-workflow/video/requirements.txt
  - 01-system/tools/ops/video-workflow/video/setup-video-env.ps1
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
  5. **Aggregation & Pre-Summarization**:
      a. Concatenate the *timestamped* transcript data (e.g., from `.srt` files) from all chunks in the correct order.
      b. The `analyze-video.ps1` script will output this aggregated SRT content to standard output and perform its own cleanup of temporary audio chunks.
  6. **LLM Summarization & Final Output**:
      a. Capture the standard output from `analyze-video.ps1` (which is the aggregated SRT content).
      b. Process this aggregated SRT content using LLM capabilities to identify key concepts and associate them with their respective timestamps.
      c. Save the final summary, **including timestamps**, to the user's preferred directory and format (`.txt` by default).
- **Outputs**:
  - A summary file **with timestamps** (e.g., `03-outputs/summaries/声乐教学总结/Lesson_1_Summary_(带时间戳).txt`).
  - Temporary audio chunks during processing.

## Playbook: Groq STT Project Memos
- **Phrases / Aliases**: "Groq STT", "專案錄音轉文字", "批次轉錄並合併 Markdown", "生成 SRT + 純文字"
- **Intent**: 將專案資料夾中的多個錄音檔或影片先壓縮/擷取音訊，再用 Groq `whisper-large-v3` 轉成純文字與 SRT，並可依檔名順序合併成單一 Markdown（無時間戳）。
- **Steps**:
  1. 確認輸入資料夾、語言提示（可空白）、是否需要合併純文字；提醒 Groq free tier 單檔上限 25 MB，模型固定 `whisper-large-v3`。
  2. 在 repo root 執行 `.\.venv\Scripts\python.exe 01-system/tools/stt/groq_stt_pipeline.py --input_dir "<folder>" [--language <iso>] [--prompt "<style>"] [--no_combine]`。預設先轉 16k mono FLAC，若超限會自動 OGG fallback（48k）；影片會自動擷取音訊再送 STT。
  3. 取得輸出：`transcripts/*.md`（純文字）、`subtitles/*.srt`（帶時間戳）、`raw/*.json`（原始回應）、`combined/<name>.md`（合併純文字，可關閉）、`run_meta.json`。
- **Outputs**: `03-outputs/groq_stt_pipeline/<run-id>/...`

## Playbook: ElevenLabs Scribe Memo
- **Phrases / Aliases**: "ElevenLabs STT", "scribe_v1", "ElevenLabs 轉錄 memo", "用 elevenlabs 合併錄音"
- **Intent**: 使用 ElevenLabs `scribe_v1` 將專案資料夾中的錄音/影片轉成純文字與 SRT，並依檔名順序合併純文字 Markdown（無時間戳）。
- **Steps**:
  1. 確認 `XI_API_KEY` 已設，輸入資料夾與語言提示（可空白），是否需要合併純文字。
  2. 在 repo root 執行 `.\.venv\Scripts\python.exe 01-system/tools/stt/eleven_scribe_pipeline.py --input_dir "<folder>" [--language <iso>] [--timestamps_granularity word|character|none] [--no_combine]`。工具會自動 16k mono FLAC 壓縮並同步送至 ElevenLabs。
  3. 取得輸出：`transcripts/*.md`、`subtitles/*.srt`、`raw/*.json`、`combined/<name>.md`（可關閉）、`run_meta.json`，路徑位於 `03-outputs/eleven_scribe_pipeline/<run-id>/...`。
- **Outputs**: `03-outputs/eleven_scribe_pipeline/<run-id>/...`

## Playbook: Agent Self-Optimization & Workflow Review
- **Phrases / Aliases**: "复盘流程", "优化agent", "分析优化空间", "系统架构师思考", "提升工作效率", "整体工作流优化", "agent更新", "playbook更新"
- **Intent**: To conduct a comprehensive analysis of a specified (or last major) workflow, identify bottlenecks and root causes, propose and implement optimizations, and update the agent's internal documentation (AGENTS.md, PLAYBOOKS.md) and relevant scripts accordingly.
- **Steps**:
  1.  **Acknowledge & Clarify**: Confirm understanding of the request for self-optimization and clarify the target workflow if ambiguous.
  2.  **Workflow Analysis**: Review the specified previous workflow, analyzing execution logs, outputs, and user feedback to identify inefficiencies, errors, and their root causes (e.g., environment brittleness, network friction, script logic flaws, tool limitations, interactive overhead).
  3.  **Identify Bottlenecks & Root Causes**: Detail specific points of failure or slowness (e.g., Git SSL errors, 
ead_file ignore patterns, manual steps, redundant actions).
  4.  **Propose Optimization Plan**: Develop a structured plan for improvement, categorizing solutions into:
      a.  **Script/Tool Refactoring**: Modifying/creating internal scripts (e.g., nalyze-video.ps1).
      b.  **Documentation Updates**: Updating PLAYBOOKS.md, AGENTS.md.
      c.  **Tool/Memory Enhancements**: Suggesting new tool features or memory facts.
      d.  **User-side Actions**: Identifying persistent issues requiring user intervention (e.g., network configuration).
  5.  **Implement Changes (Build Mode)**:
      a.  Execute script/tool modifications using 
eplace or write_file.
      b.  Update PLAYBOOKS.md and AGENTS.md.
      c.  Create new scripts/tools in appropriate directories (e.g., 	ools/video/).
  6.  **Verify & Test**: Where feasible, run small tests (e.g., pre-flight checks) to verify the implemented optimizations.
  7.  **Document & Commit**: Commit all changes to version control with a comprehensive message detailing the optimizations.
  8.  **Report to User**: Summarize the optimizations implemented, explain how the new/modified playbooks/scripts work, highlight any remaining user-side dependencies, and provide instructions for future use.
- **Outputs**:
  - Updated AGENTS.md, PLAYBOOKS.md.
  - New/modified scripts/tools (e.g., 01-system/tools/ops/video-workflow/video/analyze-video.ps1).
  - Git commit reflecting these changes.