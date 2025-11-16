# Playbooks

Document common intents here using the Lean playbook format (phrase -> intent -> steps -> outputs under `03-outputs/<tool>/`).

## Playbook: Answer In Traditional Chinese
- **Phrases / Aliases**: "respond in Chinese", "use Traditional Chinese", "all future replies must be Chinese" (and zh-TW equivalents like「之後回覆都用中文」)。
- **Intent**: Once triggered, keep all future responses in Traditional Chinese until the user explicitly changes the preference.
- **Steps**:
  1. Detect when the user asks for replies in Chinese (any phrasing similar to the aliases above).
  2. Switch immediately to Traditional Chinese for all subsequent outputs.
  3. Continue responding in Traditional Chinese until the user specifies another language.
- **Outputs**: No filesystem artifact; conversational commitment only.

## Playbook: YouTube 單片下載 (Single Video)
- **Phrases / Aliases**: 「下載這支 YouTube 影片」, "use yt-dlp for this video", "grab audio for link X".
- **Intent**: Download one video (audio+video or specified format) via `yt-dlp-downloader`.
- **Steps**:
  1. Collect the target URL and confirm desired format/subtitle requirements.
  2. If the video requires login, request cookies info; prefer `-CookiesFromBrowser edge` (or other browser) or `-CookiesFile <path>`.
  3. Run `pwsh 01-system/tools/ops/yt-dlp-downloader/run.ps1 -Url <URL> -Format <format?> -CookiesFromBrowser <browser?> -CookiesFile <file?> -AdditionalArgs <options?>`.
  3. Monitor `run.log` inside the timestamped folder for status/errors.
  4. Share the output folder path `03-outputs/yt-dlp-downloader/<timestamp>/` in the final summary.
- **Outputs**: `03-outputs/yt-dlp-downloader/<timestamp>/` containing downloaded media + `run.log`.

## Playbook: YouTube 播放清單 / 批次下載
- **Phrases / Aliases**: 「備份這個播放清單」, "batch download URLs", "mirror list via yt-dlp".
- **Intent**: Download multiple videos (playlist URL or a URL list) and keep structured artifacts.
- **Steps**:
  1. Gather playlist link or create a newline-separated list in `02-inputs/yt-dlp-urls.txt`.
  2. Confirm if cookies are required; add `-CookiesFromBrowser/-CookiesFile` to the command when necessary.
  3. For playlists: run `run.ps1 -Url <playlistUrl> -AdditionalArgs @('--yes-playlist','--sleep-requests','1')` plus any cookie/format flags.
     For custom list: iterate through the URLs (PowerShell loop) while pointing to the same output root.
  4. Enable metadata/subtitle flags when the user needs text assets (`--write-subs --write-info-json`).
  5. Summarize successes/failures and point to each timestamped directory under `03-outputs/yt-dlp-downloader/`.
- **Outputs**: `03-outputs/yt-dlp-downloader/<timestamp>/` directories per run (include downloaded files, subtitles, `run.log`).
