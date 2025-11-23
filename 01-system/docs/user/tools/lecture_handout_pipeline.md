# 工具：AI 講義生成流程 (lecture_handout_pipeline)

## 用途

此工具利用大型語言模型（Gemini）的智慧，將純文字稿件（如演講逐字稿）自動轉換為一份結構清晰、重點突出、易於閱讀的 Markdown 格式講義。它能自動生成摘要、提煉要點，並對內容進行分段和格式化。

## 使用方式

您需要提供輸入的文字稿、設定輸出的檔案路徑，並可選擇性地提供自訂的指令（Prompt）來指導 AI 生成您想要的格式。

### 指令範例

```bash
# 使用預設的提示詞模板生成講義
python 01-system/tools/ops/lecture_handout_pipeline.py "來源文字稿.txt" "輸出的AI講義.md" --title "AI生成的第一課筆記"

# 使用自訂的提示詞模板
python 01-system/tools/ops/lecture_handout_pipeline.py "來源文字稿.txt" "輸出的AI講義.md" --prompt_file "我的提示詞模板.txt"
```

### 參數說明

*   `input_file` (必須): 來源純文字檔案（逐字稿）的完整路徑。
*   `output_file` (必須): 您希望保存 AI 生成的 Markdown 講義的完整路徑。
*   `--title` (可選): 講義文件的主標題。預設為 "AI-Generated Handout"。
*   `--prompt_file` (可選): 一個包含自訂提示詞（Prompt）的文字檔案路徑。在您的提示詞中，必須包含 `{content}` 這個預留位置，它將被替換為 `input_file` 的完整內容。如果未提供，工具將使用內建的預設提示詞。
