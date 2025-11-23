# Groq STT Pipeline
**分類**：stt  
**主要 CLI/腳本**：`.\.venv\Scripts\python.exe 01-system/tools/stt/groq_stt_pipeline.py`  
**輸出位置**：`03-outputs/groq_stt_pipeline/<run-id>/`

## 何時使用
- 專案資料夾內有多段錄音或影片，需要先壓縮/擷取音訊再以 Groq `whisper-large-v3` 轉成文字。  
- 同時要產出純文字（無時間戳）與帶時間戳的 `.srt`。  
- 需要依檔名順序把所有純文字 transcript 合併成一份 Markdown。  
- 遵守 Groq free tier 單檔 25 MB 限制（工具預設 24.5 MB 門檻並自動 OGG fallback）。

## 操作步驟
1. 確認 `GROQ_API_KEY` 已設定（存於 `01-system/configs/apis/API-Keys.md`）且 `ffmpeg` 可用。  
2. 從 repo root 執行，例如：  
   ```powershell
   .\.venv\Scripts\python.exe 01-system/tools/stt/groq_stt_pipeline.py --input_dir "02-inputs/Project Memos" --language zh
   ```  
   - 會建立 `03-outputs/groq_stt_pipeline/<run-id>/`，內含 `compressed/`、`transcripts/*.md`、`subtitles/*.srt`、`raw/*.json`、`combined/combined.md`、`run_meta.json`。影片會自動擷取音訊再轉檔。  
   3. 若想關閉合併輸出，加上 `--no_combine`；若需要手動設定輸出檔名，用 `--combine_filename my-notes.md`。  
   4. 若壓縮後仍超過 free tier，調高壓縮力道（例如 `--max_size_mb 20 --ogg_bitrate 48k`），或先手動切段後再執行。

## 常用旗標/參數
- `--input_dir`（必填）：包含音訊的資料夾。  
- `--language`：ISO-639-1 語言提示（空值則自動偵測）。  
- `--prompt`：STT 風格/拼字提示（224 tokens 內）。  
- `--max_size_mb`：壓縮後允許的最大檔案大小，預設 24.5（低於 25 MB free tier）。  
- `--ogg_bitrate`：當 FLAC 太大時，OGG fallback 的音訊位元率（預設 48k）。  
- `--no_ogg_fallback`：禁用 OGG fallback，只保留 FLAC。  
- `--no_combine` / `--combine_filename`：控制是否合併純文字並自訂檔名。  
- `--run_id` / `--output_base`：自訂輸出資料夾命名或根目錄。

## 注意事項
- 模型固定為 `whisper-large-v3`，不可更換。  
- 先轉 16 kHz mono 的 FLAC；若超過限制且允許 fallback，會再轉 48k OGG 後送出。  
- STT 請求內建 3 次重試（2s 遞增延遲）以處理暫時性 SSL/網路錯誤。  
- 若 `segments` 缺失，SRT 檔會標示「No timestamped segments available」。  
- 請勿在輸出中寫入 API 金鑰；除錯時查看 `raw/*.json` 即可。
