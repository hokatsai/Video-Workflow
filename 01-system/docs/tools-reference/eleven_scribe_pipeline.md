# Eleven Scribe Pipeline
**分類**：stt  
**主要 CLI/腳本**：`.\.venv\Scripts\python.exe 01-system/tools/stt/eleven_scribe_pipeline.py`  
**輸出位置**：`03-outputs/eleven_scribe_pipeline/<run-id>/`

## 何時使用
- 需要用 ElevenLabs `scribe_v1` 將多個錄音或影片轉成文字，並同時產出純文字與 SRT。  
- 希望依檔名順序合併純文字為單一 Markdown，方便整併 memo。  
- 需要支援影片自動擷取音訊與基礎壓縮（16k mono FLAC）。

## 操作步驟
1. 確認環境變數 `XI_API_KEY` 已設定（請勿將金鑰寫入 repo）。  
2. 從 repo root 執行，例如：  
   ```powershell
   .\.venv\Scripts\python.exe 01-system/tools/stt/eleven_scribe_pipeline.py --input_dir "02-inputs/Project Memos" --language zh
   ```  
   - 會建立 `03-outputs/eleven_scribe_pipeline/<run-id>/`，包含 `compressed/`、`transcripts/*.md`、`subtitles/*.srt`、`raw/*.json`、`combined/combined.md`、`run_meta.json`。  
3. 若不需合併，加上 `--no_combine`；或用 `--combine_filename my-notes.md` 自訂檔名。  
4. 檔案過大時，可調整 `--max_size_mb`（預設 100MB，API 上限約 3GB）；必要時先手動切段。

## 常用旗標/參數
- `--input_dir`（必填）：音訊/影片資料夾。  
- `--language`：ISO 語言提示（空白自動判斷）。  
- `--timestamps_granularity`：`none` | `word` | `character`（預設 word）。  
- `--max_size_mb`：壓縮後單檔最大值（MB），預設 100。  
- `--no_combine` / `--combine_filename`：控制合併輸出。  
- `--run_id` / `--output_base`：自訂輸出目錄與命名。

## 注意事項
- 模型固定 `scribe_v1`（同步模式；`webhook=false`）。  
- API 限制：檔案須 <3GB；支援音訊/影片多種格式。  
- 產出的 SRT 由回傳的 word-level timestamps 生成；若 API 無 timestamps，SRT 會標示未提供。  
- 請勿提交實際金鑰；若需排查，檢視 `raw/*.json`。***
