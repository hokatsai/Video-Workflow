# yt-dlp-downloader Tool

This wrapper standardizes downloading YouTube content via `yt-dlp` and stores every run under `03-outputs/yt-dlp-downloader/<timestamp>/`.

## Usage
```powershell
pwsh 01-system/tools/ops/yt-dlp-downloader/run.ps1 -Url "https://www.youtube.com/watch?v=..." -Format "best" -AdditionalArgs "--write-sub"
```

- `Url` (required): video or playlist URL.
- `Format` (optional): defaults to `bestvideo+bestaudio/best`.
- `OutputDir` (optional): defaults to repo `03-outputs/yt-dlp-downloader`.
- `AdditionalArgs` (optional array): extra switches passed directly to `yt-dlp`.
- `CookiesFromBrowser` (optional): pass a browser profile name (e.g., `edge`, `chrome`) to leverage `--cookies-from-browser`.
- `CookiesFile` (optional): path to an exported cookies text file consumed via `--cookies`.

Ensure [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) is installed and available in PATH.
