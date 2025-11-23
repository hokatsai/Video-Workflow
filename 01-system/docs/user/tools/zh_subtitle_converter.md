# 工具：繁簡字幕轉換 (zh_subtitle_converter)

## 用途

此工具用於將字幕檔案（`.srt` 格式）在**繁體中文**與**簡體中文**之間進行互相轉換。

## 使用方式

您需要提供來源字幕檔、目標輸出路徑，並明確指定轉換的方向。

### 指令範例

```bash
# 將簡體字幕轉換為繁體字幕
python 01-system/tools/ops/zh_subtitle_converter.py "簡體字幕.srt" "繁體字幕.srt" s2t

# 將繁體字幕轉換為簡體字幕
python 01-system/tools/ops/zh_subtitle_converter.py "繁體字幕.srt" "簡體字幕.srt" t2s
```

### 參數說明

*   `input_file` (必須): 來源 `.srt` 字幕檔案的完整路徑。
*   `output_file` (必須): 您希望保存轉換後新字幕檔案的完整路徑。
*   `config` (必須): 轉換方向的設定，必須是以下兩者之一：
    *   `s2t`: 代表 **S**implified to **T**raditional (簡體轉繁體)。
    *   `t2s`: 代表 **T**raditional to **S**implified (繁體轉簡體)。
