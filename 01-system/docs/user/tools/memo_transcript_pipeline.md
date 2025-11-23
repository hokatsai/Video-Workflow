# 工具：AI 會議紀要生成流程 (memo_transcript_pipeline)

## 用途

此工具利用大型語言模型（Gemini）的能力，將一份會議或對話的純文字逐字稿，自動整理成一份專業的 Markdown 格式會議紀要（Memo）。它能識別並整理出與會者、討論要點、行動項目和最終決議。

## 使用方式

您需要提供輸入的逐字稿檔案、設定輸出的檔案路徑，並可選擇性地提供自訂的指令（Prompt）來指導 AI 生成您偏好的格式。

### 指令範例

```bash
# 使用預設的提示詞模板生成會議紀要
python 01-system/tools/ops/memo_transcript_pipeline.py "會議紀錄.txt" "輸出的會議紀要.md" --title "第一季度專案會議"

# 使用自訂的提示詞模板
python 01-system/tools/ops/memo_transcript_pipeline.py "會議紀錄.txt" "輸出的會議紀要.md" --prompt_file "我的紀要模板.txt"
```

### 參數說明

*   `input_file` (必須): 來源純文字逐字稿檔案的完整路徑。
*   `output_file` (必須): 您希望保存 AI 生成的 Markdown 會議紀要的完整路徑。
*   `--title` (可選): 會議紀要的主標題。預設為 "Meeting Memo"。
*   `--prompt_file` (可選): 一個包含自訂提示詞（Prompt）的文字檔案路徑。在您的提示詞中，必須包含 `{content}` 這個預留位置，它將被替換為 `input_file` 的完整內容。如果未提供，工具將使用內建的、專為生成會議紀要而設的提示詞。
