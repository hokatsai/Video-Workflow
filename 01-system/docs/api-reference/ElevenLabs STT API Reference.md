# ElevenLabs Speech-to-Text (scribe_v1) API 參考

> 來源：`https://api.elevenlabs.io/openapi.json` 解析摘要  
> 模型：`scribe_v1`（同步轉錄，預設 word-level timestamps）

## 主要端點

### POST /v1/speech-to-text
- **用途**：上傳音訊/影片進行轉錄（同步回傳；若 webhook=true 則改為非同步）。  
- **認證**：`xi-api-key` 置於 Header。  
- **Content-Type**：`multipart/form-data`。  
- **必要欄位**：
  - `model_id`：`scribe_v1`（或 `scribe_v1_experimental`）。  
  - 二擇一：`file` (binary) 或 `cloud_storage_url` (HTTPS；<2GB)。`file` 上限約 3GB。  
- **常用可選欄位**：
  - `language_code`：ISO-639-1/3 提示。  
  - `timestamps_granularity`：`none` | `word` | `character`（預設 `word`）。  
  - `diarize` (bool)，`num_speakers` (<=32)，`use_multi_channel` (bool，<=5 ch)。  
  - `additional_formats`：指定輸出如 `srt`、`txt`、`segmented_json`… 可設定 `include_speakers`、`include_timestamps` 等。  
  - `webhook`/`webhook_id`：true 時改以 webhook 回傳並立即 202。  
- **回應**：
  - `200`：同步結果（單聲道為 `SpeechToTextChunkResponseModel`，多聲道為 `MultichannelSpeechToTextResponseModel`）。含 `text`、`words[{text,start,end,speaker_id,logprob,...}]`。  
  - `202`：非同步已受理（搭配 webhook）。  
  - `401/422`：未授權或參數錯誤。

### GET /v1/speech-to-text/transcripts/{transcription_id}
- **用途**：依 ID 取回轉錄結果（供 webhook/非同步流程）。  
- **認證**：`xi-api-key` Header。  
- **回應**：與 POST 同型的 transcript 物件；404 時回傳 not found。

### DELETE /v1/speech-to-text/transcripts/{transcription_id}
- **用途**：刪除指定 transcript。  
- **認證**：`xi-api-key` Header。

## 重要參數說明（節錄）
- `additional_formats` → `SrtExportOptions` / `TxtExportOptions` / `SegmentedJsonExportOptions` 等：  
  - `format`: `srt|txt|segmented_json|docx|pdf|html`  
  - `include_speakers` (bool), `include_timestamps` (bool), 其他 srt/txt 格式化參數。  
- `file_format`: `pcm_s16le_16` 或 `other`（若指定 pcm 需 16kHz mono 16-bit PCM）。  
- `tag_audio_events` (default true)：是否在文本中標示音效。  
- `temperature`、`seed`：控制隨機性或嘗試決定性。  
- `webhook_metadata`：可附加 JSON（字串/物件，深度 <=2，<=16KB）。

## 限制與提示
- 檔案大小：`file` < 3GB；`cloud_storage_url` < 2GB。  
- 支援音訊/影片多種格式；多聲道時可用 `use_multi_channel`。  
- 免費方案可能有限額或防濫用（可能回傳 401 detected_unusual_activity）。  
- 典型同步用法：`model_id=scribe_v1` + `timestamps_granularity=word` + `file=@audio.flac` + `xi-api-key:<key>`。
