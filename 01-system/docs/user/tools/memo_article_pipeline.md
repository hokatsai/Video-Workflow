# 工具：AI 文章生成流程 (memo_article_pipeline)

## 用途

此工具利用大型語言模型（Gemini）的能力，將一份純文字檔案轉換成一篇結構完整、語句通順的 Markdown 格式文章。它適用於將草稿、筆記或任何形式的原始文本快速整理成正式的文章。

## 使用方式

您需要提供輸入的文字檔案、設定輸出的檔案路徑，並可選擇性地提供自訂的指令（Prompt）來指導 AI 的寫作風格。

### 指令範例

```bash
# 使用預設的提示詞模板生成文章
python 01-system/tools/ops/memo_article_pipeline.py "我的草稿.txt" "輸出的文章.md" --title "關於專案的想法"

# 使用自訂的提示詞模板
python 01-system/tools/ops/memo_article_pipeline.py "我的草稿.txt" "輸出的文章.md" --prompt_file "我的文章寫作風格.txt"
```

### 參數說明

*   `input_file` (必須): 來源純文字檔案（草稿）的完整路徑。
*   `output_file` (必須): 您希望保存 AI 生成的 Markdown 文章的完整路徑。
*   `--title` (可選): 文章的主標題。預設為 "AI-Generated Article"。
*   `--prompt_file` (可選): 一個包含自訂提示詞（Prompt）的文字檔案路徑。在您的提示詞中，必須包含 `{content}` 這個預留位置，它將被替換為 `input_file` 的完整內容。如果未提供，工具將使用內建的預設提示詞。
