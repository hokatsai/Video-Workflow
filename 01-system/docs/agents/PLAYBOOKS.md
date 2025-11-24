# Playbooks

Document common intents here using the Lean playbook format (phrase -> intent -> steps -> outputs under `03-outputs/<tool>/`).

## Playbook: Answer In Traditional Chinese
- **Phrases / Aliases**: "respond in Chinese", "use Traditional Chinese", "all future replies must be Chinese"（含繁中字詞）
- **Intent**: 一旦觸發後，後續回覆改用繁體中文，直到使用者明確要求切換。
- **Steps**:
  1. 偵測使用者要求繁體中文回覆。
  2. 立即改用繁體中文回覆。
  3. 持續使用繁體中文，直到使用者指定其他語言。
- **Outputs**: 無檔案產物。

## Playbook: Gemini Large-Scale Overview
- **Phrases / Aliases**: "give me an overview with Gemini", "summarize the whole repo", "use Gemini CLI for architecture"
- **Intent**: ?????????/?????????
- **Steps**:
  1. ???????????????????????????`gemini-2.5-pro` ? `gemini-2.5-flash`??? fallback??
  2. ? repo root ?? `pwsh 01-system/tools/tth/gemini-default.ps1 -Targets <paths> -Query "<prompt>" [-OutputName "<folder>"]`?
  3. ?? `response.txt`??????????????????????
- **Outputs**: `03-outputs/gemini-cli/<run-id>/response.txt`

## Playbook: Gemini Implementation Audit
- **Phrases / Aliases**: "check if <feature> exists", "verify auth via Gemini", "Gemini security review"
- **Intent**: ? Gemini ??????????/???
- **Steps**:
  1. ?????????????????? `gemini-2.5-pro` ? `gemini-2.5-flash`?
  2. ?? `pwsh 01-system/tools/tth/gemini-default.ps1 -Targets <paths> -Query "Has <feature>? Show files/functions" [-OutputName "<folder>"]`?
  3. ????????????????????????
- **Outputs**: `03-outputs/gemini-cli/<run-id>/response.txt`

## Playbook: Setup Video Workflow Environment
- **Phrases / Aliases**: "setup video workflow", "initialize video environment", "prepare for video analysis"
- **Intent**: 建立穩定的 Python 環境以進行影片處理。
- **Steps**:
  1. 建立 requirements.txt（whisperx、ffmpeg-python 等）。
  2. 建立 setup 腳本（setup-video-env.ps1）創建/啟動 venv 並安裝依賴。
  3. 執行 setup 腳本。
  4. 以短靜音檔跑預熱轉錄，確保環境可用。
  5. 紀錄環境就緒狀態。
- **Outputs**:
  - `01-system/tools/ops/video-workflow/video/requirements.txt`
  - `01-system/tools/ops/video-workflow/video/setup-video-env.ps1`
  - `.venv` 目錄

## Playbook: Optimized Video Analysis
- **Phrases / Aliases**: "analyze this video", "summarize the lecture", "get key points from this course video", "summarize video with timestamps"
- **Intent**: 將長影片分片轉錄並生成含時間戳的摘要。
- **Steps**:
  1. 確認環境已就緒（若否，先跑 Setup Video Workflow Environment）。
  2. 若影片 >10 分鐘，先提示時間成本並提供取樣選項；使用 ffprobe 取得時長。
  3. 以 ffmpeg 切分為 10 分鐘 WAV 段落。
  4. 平行執行 whisperx 取得帶時間戳的轉錄（SRT/JSON），`--compute_type auto`，失敗再退回 float32。
  5. 合併分段 SRT 為完整帶時間戳內容。
  6. 使用 LLM 摘要並保留時間戳，輸出至指定路徑。
- **Outputs**:
  - 摘要檔（含時間戳） e.g. `03-outputs/summaries/.../Lesson_1_Summary_with_timestamps.txt`
  - 處理中的臨時音訊切片

## Playbook: Groq STT Project Memos
- **Phrases / Aliases**: "Groq STT", "專案錄音轉文字", "批次轉錄並合併 Markdown", "生成 SRT + 純文字"
- **Intent**: 將資料夾內多個錄音/影片壓縮後，用 Groq `whisper-large-v3` 轉成純文字與 SRT，並依檔名合併為一份 Markdown（無時間戳）。
- **Steps**:
  1. 確認輸入資料夾、語言提示（可空白）、是否需合併；提醒 Groq free tier 單檔上限 25 MB，模型固定 `whisper-large-v3`。
  2. 在 repo root 執行 `.\.venv\Scripts\python.exe 01-system/tools/stt/groq_stt_pipeline.py --input_dir "<folder>" [--language <iso>] [--prompt "<style>"] [--no_combine]`。預設轉 16k mono FLAC，若超限自動 OGG fallback（48k）；影片會自動擷取音訊。
  3. 取得輸出：`transcripts/*.md`（純文字）、`subtitles/*.srt`（帶時間戳）、`raw/*.json`、`combined/<name>.md`（可關閉）、`run_meta.json`。
- **Outputs**: `03-outputs/groq_stt_pipeline/<run-id>/...`

## Playbook: ElevenLabs Scribe Memo
- **Phrases / Aliases**: "ElevenLabs STT", "scribe_v1", "ElevenLabs 轉錄 memo", "用 elevenlabs 合併錄音"
- **Intent**: 使用 ElevenLabs `scribe_v1` 將錄音/影片轉成純文字與 SRT，並依檔名順序合併純文字 Markdown（無時間戳）。
- **Steps**:
  1. 確認 `XI_API_KEY` 已設定，輸入資料夾、語言提示（可空白）、是否合併純文字。
  2. 在 repo root 執行 `.\.venv\Scripts\python.exe 01-system/tools/stt/eleven_scribe_pipeline.py --input_dir "<folder>" [--language <iso>] [--timestamps_granularity word|character|none] [--no_combine]`。工具會自動 16k mono FLAC 壓縮並同步呼叫 ElevenLabs。
  3. 取得輸出：`transcripts/*.md`、`subtitles/*.srt`、`raw/*.json`、`combined/<name>.md`（可關閉）、`run_meta.json`，位於 `03-outputs/eleven_scribe_pipeline/<run-id>/...`。
- **Outputs**: `03-outputs/eleven_scribe_pipeline/<run-id>/...`

## Playbook: Agent Self-Optimization & Workflow Review
- **Phrases / Aliases**: "自我優化", "優化 agent", "工作流優化", "系統架構師思維", "效率提升"
- **Intent**: 回顧既有工作流，找出瓶頸並實作改進，同步更新文件。
- **Steps**:
  1. 確認目標工作流與優化目標。
  2. 檢視執行紀錄/輸出，定位低效率或錯誤根因（環境、網路、腳本邏輯等）。
  3. 梳理瓶頸並提出解法（腳本/工具重構、文件更新、Memory 事項、使用者側依賴）。
  4. 若進入 Build Mode：實作修改，更新相關文件（AGENTS、PLAYBOOKS 等）。
  5. 驗證（小型測試），並記錄於 `SYSTEM_MEMORY.md` / `STATE.md`。
  6. 回報優化內容、剩餘風險與待辦。
- **Outputs**:
  - 更新後的 AGENTS.md、PLAYBOOKS.md
  - 相關工具或腳本的變更

## Playbook: Gemini Troubleshooting
- **Phrases / Aliases**: "Gemini quota error", "TLS handshake fail", "Gemini not working"
- **Intent**: ???? Gemini CLI ?????????????
- **Steps**:
  1. ?? `pwsh 01-system/tools/tth/gemini-default.ps1 -Targets <paths> -Query "<prompt>"` ?????????? fallback?
  2. ??? TLS/??????? `curl https://cloudcode-pa.googleapis.com` ??? `gemini auth login`???????
  3. ??? quota/capacity???????? `-FallbackModel gemini-2.5-flash` ???????????????? token?
  4. ?? `response.txt` ???????????? `SYSTEM_MEMORY.md`??????
- **Outputs**: `03-outputs/gemini-cli/<run-id>/response.txt`


## Playbook: Memo ????STT + Gemini ???
- **Phrases / Aliases**: "??? memo ???", "????????", "????? Gemini"?"??+??"
- **Intent**: ???/?????? STT?groq/eleven???? combine???? Gemini ????????????
- **Steps**:
  1. ???????? STT ???groq ? eleven???? Gemini ?? `gemini-2.5-pro`???????`01-system/docs/prompts/???????????????.md`?
  2. ? repo root ???`..\.venv\Scripts\python.exe 01-system/tools/ops/memo_gemini_pipeline.py --input_dir "<folder>" --stt_tool groq --run_id "<run>"`???? eleven?? `--stt_tool eleven`??
  3. ??????????? `refined.md` ????????? STT/combined ??????
- **Outputs**: `03-outputs/memo_gemini_pipeline/<run-id>/refined.md`

## Playbook: Memo ?? combine ????Gemini?
- **Phrases / Aliases**: "?? combine", "Gemini ???? combine", "???? prompt ??"
- **Intent**: ??????? combined Markdown????????? Gemini ???????
- **Steps**:
  1. ?? combined ?????? `03-outputs/groq_stt_pipeline/<run-id>/combined/combined.md`??
  2. ? repo root ???`..\.venv\Scripts\python.exe 01-system/tools/ops/memo_gemini_pipeline.py --combined_file "<combined.md>" --run_id "<run>"`???? `--title "<????>"`?
  3. ????? `refined.md`?????? prompt/response ?????
- **Outputs**: `03-outputs/memo_gemini_pipeline/<run-id>/refined.md`
