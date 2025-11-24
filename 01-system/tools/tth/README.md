## tth 快捷腳本

- 目的：集中常用的自動化/包裝腳本，減少重複輸入並維持輸出路徑一致性。
- 路徑：`01-system/tools/tth/`
- 慣例：維持與既有工具一致的紀錄位置（`03-outputs/<tool>/...`），預設以最安全、最高可用的模型與配置執行。

### 清單
- `gemini-default.ps1`：Gemini CLI 預設使用 `gemini-2.5-pro`，遇到額度/不可用時自動退回 `gemini-2.5-flash`，並沿用 `gemini-run.ps1` 的記錄格式。
