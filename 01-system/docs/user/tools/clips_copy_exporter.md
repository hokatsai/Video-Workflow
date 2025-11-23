# 工具：片段複製與導出 (clips_copy_exporter)

## 用途

此工具用於將一個或多個檔案（或整個資料夾的內容）複製或移動到指定的目標資料夾。它特別適合在處理流程的最後，將產出的影片片段或其他資產進行歸檔和導出。

## 使用方式

您可以透過提供來源路徑和目標路徑來使用此工具。

### 指令範例

```bash
# 複製單一檔案
python 01-system/tools/ops/clips_copy_exporter.py "來源/檔案.mp4" "導出目的地資料夾/"

# 複製整個資料夾的內容
python 01-system/tools/ops/clips_copy_exporter.py "來源資料夾/" "導出目的地資料夾/"

# 移動檔案而不是複製（注意 --move 旗標）
python 01-system/tools/ops/clips_copy_exporter.py "來源/檔案.mp4" "導出目的地資料夾/" --move
```

### 參數說明

*   `source_path` (必須): 您想要導出的來源檔案或資料夾的完整路徑。
*   `destination_path` (必須): 您希望將檔案複製或移动到的目標資料夾的完整路徑。
*   `--move` (可選): 若包含此旗標，工具將執行“移動”操作（剪下貼上）而非“複製”操作。
