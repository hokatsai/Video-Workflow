# 工具：影片片段適配器 (clips_adapter)

## 用途

此工具用於調整影片片段的屬性，例如變更其解析度（resolution）或影格率（FPS, frame rate）。

## 使用方式

您可以透過指定輸入檔案、輸出檔案，並選擇性地提供新的解析度和影格率來使用此工具。

### 指令範例

```bash
# 將影片解析度調整為 720p (1280x720)
python 01-system/tools/ops/clips_adapter.py "輸入影片.mp4" "輸出_720p.mp4" --resolution "1280x720"

# 將影片影格率調整為 30 FPS
python 01-system/tools/ops/clips_adapter.py "輸入影片.mp4" "輸出_30fps.mp4" --fps 30

# 同時調整解析度和影格率
python 01-system/tools/ops/clips_adapter.py "輸入影片.mp4" "輸出_720p_30fps.mp4" --resolution "1280x720" --fps 30
```

### 參數說明

*   `input_path` (必須): 來源影片檔案的完整路徑。
*   `output_path` (必須): 您希望保存調整後新影片的完整路徑。
*   `--resolution` (可選): 新的目標解析度，格式為 `"寬度x高度"`，例如 `"1920x1080"`。
*   `--fps` (可選): 新的目標影格率，為一個整數，例如 `24`, `30`, `60`。
