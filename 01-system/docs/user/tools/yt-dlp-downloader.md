# yt-dlp 影音下載器
**類別**：ops
**版本**：v0.2 （更新日期：2025-11-17）

## 能力總覽
- 透過 `yt-dlp` 下載 YouTube 影片或播放清單。
- 支援自訂格式（audio/video/best）與字幕、資訊檔。
- 自動將檔案儲存到 `03-outputs/yt-dlp-downloader/<timestamp>/`，並產生 `run.log` 記錄。

## 參數說明
- `Url`：必填，YouTube 影片或播放清單連結。
- `Format`：選填，`yt-dlp` 的 `-f` 參數（預設 `bestvideo+bestaudio/best`）。
- `OutputDir`：選填，自訂輸出根目錄（預設 repo `03-outputs/yt-dlp-downloader`）。
- `AdditionalArgs`：選填陣列，原封不動傳給 `yt-dlp` 的額外參數。
- `CookiesFromBrowser`：選填，指定瀏覽器（如 `edge`、`chrome`）讓 `yt-dlp` 自動抓取登入 cookies。
- `CookiesFile`：選填，提供自行匯出的 cookies 檔案路徑（`Netscape` 格式）。

## 常見用法（逐步）
1. 確認 `yt-dlp` 已安裝並可從 PATH 呼叫。
2. 執行 `pwsh 01-system/tools/ops/yt-dlp-downloader/run.ps1 -Url "<影片網址>"`。
3. 需要字幕或其他旗標時，加入 `-AdditionalArgs @("--write-subs","--sub-lang","zh-Hant")`。
4. 若影片需要登入權限，提供 `-CookiesFromBrowser edge` 或 `-CookiesFile "C:\path\cookies.txt"`。
5. 完成後到 `03-outputs/yt-dlp-downloader/<timestamp>/` 取用下載檔及 `run.log`。

## 範例
- **快速範例**：`pwsh .../run.ps1 -Url "https://youtu.be/xyz" -Format best` → 產出於 `03-outputs/yt-dlp-downloader/20251117-120000/`
- **登入範例**：`pwsh .../run.ps1 -Url "https://youtu.be/xyz" -CookiesFromBrowser edge`

## 輸入 / 輸出路徑
- 輸入來源：`02-inputs/`（如需自備 URL 列表可放此）。
- 產出位置：`03-outputs/yt-dlp-downloader/<timestamp>/`

## 風險與權限
- 下載內容須遵守 YouTube 與著作權規範。
- 需安裝 `yt-dlp` 並允許網路連線；如使用 cookies，確保檔案安全。

## 故障排除
- `yt-dlp` 找不到：確認已安裝並在 PATH。
- 下載失敗：檢查 `run.log`，若提示需要登入，使用 cookies 參數。
- 速度慢：可使用 `--concurrent-fragments` 或調整網路環境。

## 版本與更新紀錄
- v0.2（2025-11-17）：新增 cookies-from-browser / cookies 檔案支援。
- v0.1（2025-11-17）：初版。
