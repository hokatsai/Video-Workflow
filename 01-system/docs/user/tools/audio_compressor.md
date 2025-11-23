# 工具：音訊壓縮 (audio_compressor)

## 用途

此工具用於將一個音訊檔案（如 `.mp3`, `.wav`, `.m4a`）壓縮成較小的檔案，主要方式是降低其位元率（bitrate）。這對於節省儲存空間或加速網路傳輸非常有用。

## 使用方式

您可以透過指定輸入檔案、輸出檔案以及目標位元率來使用此工具。

### 指令範例

```bash
# 基本用法，使用預設的 64k 位元率
python 01-system/tools/ops/audio_compressor.py "輸入音訊.mp3" "輸出音訊.mp3"

# 指定 128k 位元率
python 01-system/tools/ops/audio_compressor.py "輸入音訊.wav" "輸出音訊_compressed.mp3" --bitrate "128k"
```

### 參數說明

*   `input_path` (必須): 來源音訊檔案的完整路徑。
*   `output_path` (必須): 您希望保存壓縮後新檔案的完整路徑。檔案格式將根據副檔名自動決定。
*   `--bitrate` (可選): 目標位元率，例如 `"128k"`, `"64k"`, `"32k"`。如果未指定，預設為 `"64k"`。
