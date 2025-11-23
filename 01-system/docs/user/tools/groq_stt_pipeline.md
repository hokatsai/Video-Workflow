# Groq STT Pipeline（groq_stt_pipeline）

## 用途
- 批次將專案資料夾中的多段錄音或影片轉成文字（影片會自動擷取音訊）。  
- 同步產出兩種格式：純文字（.md，無時間戳）與字幕檔（.srt，含時間戳）。  
- 依檔名順序把所有純文字 transcript 合併成單一 Markdown，方便後續閱讀或整理。

## 準備工作
- 設定 `GROQ_API_KEY`（存放於 `01-system/configs/apis/API-Keys.md`），請勿將金鑰寫入輸出。  
- 需安裝 `ffmpeg`（系統已預裝）；Python 依賴 `requests` 已隨虛擬環境提供。  
- Groq free tier 單檔限制 25 MB，工具預設壓縮上限 24.5 MB，並會在 FLAC 過大時自動 OGG fallback（48k）。

## 使用方式
從 repo root 執行（例：處理 `02-inputs/Project Memos` 內的錄音）：  
```powershell
.\.venv\Scripts\python.exe 01-system/tools/stt/groq_stt_pipeline.py --input_dir "02-inputs/Project Memos" --language zh
```
- 主要參數：  
  - `--language`：ISO-639-1 語言提示（空白則自動偵測）。  
  - `--prompt`：簡短風格/拼字提示（224 tokens 內）。  
  - `--max_size_mb` / `--ogg_bitrate`：調整壓縮強度，避免超過 free tier。  
  - `--no_combine`：若不需要合併純文字。`--combine_filename` 可自訂合併檔名。  
- 若 FLAC 仍超過限制，可降低 `--max_size_mb` 或提高 OGG 壓縮（例：`--ogg_bitrate 48k`），或先手動切段。

## 輸出路徑
- 預設根目錄：`03-outputs/groq_stt_pipeline/<run-id>/`。  
- 內容結構：`compressed/`（壓縮檔）、`transcripts/*.md`、`subtitles/*.srt`、`raw/*.json`、`combined/combined.md`（可關閉）、`run_meta.json`。影片檔會自動擷取音訊後存放壓縮檔。

## 限制與注意事項
- 模型固定 `whisper-large-v3`，不可更換；目前以 Groq free tier 為前提。  
- STT 請求內建 3 次重試（遞增延遲）以降低暫時性 SSL/網路錯誤造成的失敗。  
- 支援音訊格式：flac, mp3, mpeg, mpga, m4a, ogg, wav；支援影片格式：mp4, webm, mov, mkv, avi, m4v, ts。會轉 16 kHz mono 再送出。  
- 若 `segments` 缺失，SRT 檔會標示「No timestamped segments available」。  
- 請在回報或記錄時引用相對路徑（例：`03-outputs/groq_stt_pipeline/<run-id>/combined/combined.md`）。
