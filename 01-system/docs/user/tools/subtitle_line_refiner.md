# 工具：AI 字幕精煉工具 (subtitle_line_refiner)

## 用途

此工具不僅僅是修正錯誤，它利用大型語言模型（Gemini）來“精煉”字幕，提升其整體的語言品質和可讀性。主要功能包括：

*   將過於冗長的句子打斷成更短、更易於閱讀的短句。
*   簡化複雜或生硬的詞彙，使其更自然、更口語化。
*   確保字幕的整體風格和語氣保持一致。

## 使用方式

與字幕校對工具類似，您需要提供一個來源字幕檔和一個輸出路徑。

### 指令範例

```bash
# 使用預設的 AI 提示詞精煉字幕
python 01-system/tools/ops/subtitle_line_refiner.py "原始字幕.srt" "精煉後的字幕.srt"

# 使用自訂的提示詞模板進行精煉
python 01-system/tools/ops/subtitle_line_refiner.py "原始字幕.srt" "精煉後的字幕.srt" --prompt_file "我的精煉風格.txt"
```

### 參數說明

*   `input_file` (必須): 來源 `.srt` 字幕檔案的完整路徑。
*   `output_file` (必須): 您希望保存精煉後新字幕檔案的完整路徑。
*   `--prompt_file` (可選): 一個包含自訂提示詞（Prompt）的文字檔案路徑。在您的提示詞中，必須包含 `{content}` 這個預留位置。如果未提供，工具將使用內建的、專為精煉字幕而設的提示詞。
