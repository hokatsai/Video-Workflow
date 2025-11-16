# State

- **Phase**: Bootstrap (2025-11)
- **Summary**: yt-dlp-downloader now supports cookies-based auth (see SYSTEM_MEMORY entry “2025-11-17 - yt-dlp cookies support”) with latest logs at `03-outputs/yt-dlp-downloader/20251117-033602/run.log`.
- **Next Steps**:
  1. Obtain valid cookies（`-CookiesFromBrowser edge` 或提供 `cookies.txt`）後重新下載受限影片。
  2. Smoke-test公共影片以確保基礎流程無誤並記錄樣本輸出。
  3. 規劃後續媒體處理工具（轉檔、轉寫等）所需的 prompts / wrappers。
