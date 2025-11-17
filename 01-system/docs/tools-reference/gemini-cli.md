# Gemini CLI
**分類**：llms  
**主要 CLI/腳本**：`gemini`、`pwsh tools/gemini-run.ps1`  
**輸出位置**：`03-outputs/gemini-cli/<run-id>/`

## 何時使用
- 需要對大量程式碼（單檔 >100KB 或整個目錄）進行總覽、行為比對或安全審核。
- 想驗證特定功能是否實作（認證、快取、錯誤處理等）且跨多個模組。
- 需要保留 prompt 與回答以便後續引用或寫入 Lean Logflow。

## 操作步驟
1. **選定範圍**：以 repo root 為基準決定 `@` 路徑（檔案或目錄）。
2. **執行腳本（建議）**：  
   ```powershell
   pwsh tools/gemini-run.ps1 -Targets @('src/', 'tests/') -Query '請比較架構與測試覆蓋' [-Model 'gemini-1.5-pro']
   ```
   - 腳本會建立 `03-outputs/gemini-cli/<timestamp>/`，內含 `prompt.txt` 與 `response.txt`。
3. **檢閱與回報**：摘要回答並在最終訊息引用輸出路徑；若結果影響執行狀態，記錄在 `SYSTEM_MEMORY.md`。
4. **直接 CLI（備選）**：  
   ```powershell
   gemini "@src/ @api/ 檢查 API 是否實作錯誤處理"
   ```
   - 手動將輸出貼入 `03-outputs/gemini-cli/` 後續紀錄。

## 常用旗標/參數
- `@path`：包含檔案/資料夾內容進 prompt，路徑需相對於執行目錄。
- `--all_files`：將當前工作區所有檔案一併送出，僅在必要時使用以控制代價。
- `-m/--model`：切換 Gemini 版本，預設會使用 CLI 的預設模型。
- `--list-sessions` / `--resume`：查詢或回復先前會話，方便長流程分析。

## 注意事項
- 任何 run 都要明確指出輸出路徑（`03-outputs/gemini-cli/<run-id>/response.txt`）以方便稽核。
- 若命令失敗，檢查 `Loaded cached credentials` 相關提示，必要時重新登入但勿記錄祕密。
- 在 `PLAYBOOKS.md` 目前有兩個 Gemini 相關 playbook，可對應「大型概覽」與「實作稽核」情境。
- 若腳本產生的發現會影響後續工作，依 Lean Logflow 規則更新 `SYSTEM_MEMORY.md` / `STATE.md`。
