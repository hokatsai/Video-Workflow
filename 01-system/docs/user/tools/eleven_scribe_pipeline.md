# Eleven Scribe Pipeline（eleven_scribe_pipeline）

## 用途
- 批次將錄音或影片以 ElevenLabs `scribe_v1` 轉成文字。  
- 同步產出純文字（.md，無時間戳）與字幕檔（.srt，含時間戳）。  
- 依檔名順序合併所有純文字為單一 Markdown，方便整理專案 memo。

## 準備工作
- 設定環境變數 `XI_API_KEY`（請勿將金鑰寫入版本庫）。  
- 需可用 `ffmpeg`；工具會自動將輸入轉為 16 kHz mono FLAC。  
- API 限制：單檔需 <3GB；支援多種音訊/影片格式。

## 使用方式
在 repo root 執行（例：處理 `02-inputs/Project Memos`）：  
```powershell
.\.venv\Scripts\python.exe 01-system/tools/stt/eleven_scribe_pipeline.py --input_dir "02-inputs/Project Memos" --language zh
```
- 重要參數：  
  - `--language`：ISO 語言提示（空白則自動偵測）。  
  - `--timestamps_granularity`：`none|word|character`（預設 word）。  
  - `--max_size_mb`：壓縮後單檔上限（預設 100MB）。  
  - `--no_combine` / `--combine_filename`：控制是否合併純文字及檔名。  
- 輸出路徑：`03-outputs/eleven_scribe_pipeline/<run-id>/`，包含 `compressed/`、`transcripts/*.md`、`subtitles/*.srt`、`raw/*.json`、`combined/combined.md`、`run_meta.json`。

## 限制與注意事項
- 模型固定 `scribe_v1`；採同步模式（`webhook=false`）。  
- 若 API 回傳未含 timestamps，SRT 會標示「No timestamped words available.」。  
- 請在回報或記錄時引用相對路徑（如 `03-outputs/eleven_scribe_pipeline/<run-id>/combined/combined.md`）；勿外洩金鑰。
