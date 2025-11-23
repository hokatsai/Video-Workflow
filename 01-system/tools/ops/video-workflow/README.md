# 視訊工作流工具組（整合版）

本資料夾集中原本根目錄下的視訊相關工具與依賴，便於統一維護。

- `cookie/`：下載影片、字幕，以及本機檔案轉錄的腳本（Start-Workflow.ps1 會指向這裡）。
- `video/`：虛擬環境建立與 WhisperX 驅動的 `analyze-video.ps1`。
- `whisperx/`：WhisperX 套件原始碼與資產。

路徑假設：
- 各腳本會從自己的位置往上 5 層取得工作區根目錄（`..\..\..\..\..`），並將產物寫入 `03-outputs/...`。

使用提示：
- 先執行 `video/setup-video-env.ps1` 建立 `.venv` 與依賴。
- 互動式流程可從倉庫根目錄執行 `Start-Workflow.ps1`。
