# 工具：AI 字幕校對工具 (subtitle_corrector)

## 用途

此工具利用大型語言模型（Gemini）來自動校對和修正字幕檔案（`.srt` 格式）中的錯誤。它能處理拼寫、文法、標點符號等問題，提升字幕的品質與可讀性。

## 使用方式

您需要提供一個來源字幕檔和一個輸出路徑。工具會讀取來源字幕，將內容整批送交 AI 進行修正，然後將修正後的結果寫入新的字幕檔。

### 指令範例

```bash
# 使用預設的 AI 提示詞校正字幕
python 01-system/tools/ops/subtitle_corrector.py "原始字幕.srt" "校正後的字幕.srt"

# 使用自訂的提示詞模板進行校正
python 01-system/tools/ops/subtitle_corrector.py "原始字幕.srt" "校正後的字幕.srt" --prompt_file "我的校正風格.txt"
```

### 參數說明

*   `input_file` (必須): 來源 `.srt` 字幕檔案的完整路徑。
*   `output_file` (必須): 您希望保存校正後新字幕檔案的完整路徑。
*   `--prompt_file` (可選): 一個包含自訂提示詞（Prompt）的文字檔案路徑。在您的提示詞中，必須包含 `{content}` 這個預留位置，它將被替換為帶有行號的字幕內文。如果未提供，工具將使用內建的、專為校正字幕而設的提示詞。
