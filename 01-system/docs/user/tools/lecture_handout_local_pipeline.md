# 工具：本地講義生成流程 (lecture_handout_local_pipeline)

## 用途

此工具會讀取一個純文字檔案（例如，演講或課程的逐字稿），並將其轉換為一個結構化的 Markdown 格式的講義檔案。整個過程完全在本地端執行，不需依賴外部的 AI 服務。

## 使用方式

您可以透過提供輸入文字檔案、指定的輸出檔案路徑，以及講義的標題來使用此工具。

### 指令範例

```bash
# 基本用法，使用預設標題 "Lecture Handout"
python 01-system/tools/ops/lecture_handout_local_pipeline.py "來源文字稿.txt" "輸出的講義.md"

# 自訂標題
python 01-system/tools/ops/lecture_handout_local_pipeline.py "來源文字稿.txt" "輸出的講義.md" --title "我的課程筆記"
```

### 參數說明

*   `input_file` (必須): 來源純文字檔案的完整路徑。
*   `output_file` (必須): 您希望保存 Markdown 格式講義的完整路徑。
*   `--title` (可選): 講義文件的主標題。如果未指定，預設標題為 "Lecture Handout"。
