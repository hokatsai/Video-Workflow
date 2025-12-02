# System Memory

2025-11-17 - Bootstrap baseline :: scaffolded canonical runtime per INITIAL_SYSTEM_PROMPT | AGENTS spec + DocSync stubs ready | 03-outputs/bootstrap/bootstrap-log.md
2025-11-17 - Playbook update :: added "Answer In Traditional Chinese" entry to enforce zh-TW replies | ensures conversational constraint recorded | no artifact
2025-11-17 - yt-dlp tool onboarding :: registered yt-dlp-downloader tool, scripts, docs, and playbooks | enables standardized YouTube downloads | 03-outputs/yt-dlp-downloader/

2025-11-17 - yt-dlp cookies support :: added cookies-from-browser/file options + doc/playbook updates | enables auth-only downloads | 03-outputs/yt-dlp-downloader/20251117-033602/run.log

2025-11-17 - yt-dlp edge cookie attempt :: tried --cookies-from-browser edge but Windows profile inaccessible; needs exported cookies | failure log | 03-outputs/yt-dlp-downloader/20251117-033948/run.log

2025-11-17 - yt-dlp tool removed :: deleted yt-dlp-downloader tool/docs/outputs per user request | repo reset to baseline scaffold | n/a


2025-11-17 - Gemini CLI tooling :: registered gemini-cli tool + helper scripts + zh-TW docs/playbooks | enables logged Gemini-based large code analysis | 03-outputs/gemini-cli/

2025-11-18 - Tool reference hub + AGENTS zh :: added docs/tools-reference/ + zh-TW rewrite of AGENTS with reference reminders | ensures tool usage documented + user can read core spec | 03-outputs/gemini-cli/
2025-11-23 - Tools relocated to system :: change | impact: moved root tools into 01-system/tools (video-workflow, gemini-run) and updated paths/docs | artifacts: n/a

2025-11-23 â€“ Groq STT pipeline :: built groq_stt_pipeline tool (compression+Groq whisper-large-v3 text/SRT+combined markdown) with docs/playbook | 03-outputs/groq_stt_pipeline/20251123-smoke3/combined/project-memos.md
2025-11-23 â€“ Groq STT video support :: pipeline now accepts video inputs (audio extraction) with doc/playbook/user guide updates + retry tuned | 03-outputs/groq_stt_pipeline/20251123-video-smoke/combined/video.md
2025-11-24 â€“ ElevenLabs scribe pipeline :: added eleven_scribe_pipeline tool (scribe_v1 STT text/SRT/combined), docs, playbook; awaiting XI_API_KEY for smoke test | 03-outputs/eleven_scribe_pipeline/
2025-11-24 â€“ Playbooks cleanup + ElevenLabs ref doc :: rewrote PLAYBOOKS.md (zh), added ElevenLabs STT API reference; Groq youtube run 03-outputs/groq_stt_pipeline/20251124-groq-youtube3/combined/youtube_video_dVY-qqXyv5U.md
2025-11-24 - Gemini CLI smoke test :: attempted gemini-run on gemini docs; TLS handshake to cloudcode-pa.googleapis.com failed | no Gemini response; check network/proxy or CLI cert trust if persists | 03-outputs/gemini-cli/20251124-233042/response.txt
2025-11-24 - Gemini CLI smoke test (network restored) :: gemini-run succeeded after one quota retry; wrapper usage summary captured | 03-outputs/gemini-cli/20251124-233415/response.txt
2025-11-24 - Gemini 2.5-pro smoke :: gemini-run with -Model gemini-2.5-pro confirmed model usage | 03-outputs/gemini-cli/20251124-233806/response.txt
2025-11-24 - Gemini 2.5 îAÔO²ßÂÔ + tth ¿ì½İÄ_±¾ :: ÔO¶¨ 2.5-pro¡ú2.5-flash îAÔOÄ£ĞÍ¡¢ÔöÑa Playbook/AGENTS/TOOLS KĞÂÔö gemini-default.ps1£»ŸŸ‡èœyÔ‡İ”³ö | 03-outputs/gemini-cli/20251124-234600/response.txt
2025-11-24 - STT combineÄ£½M»¯ :: ³é³ö¹²ÓÃ transcript_utils£¨natural sort/ensure_dir/combined markdown£©£¬Groq/Eleven pipelines¸ÄÓÃÄ£½M£»˜ä îˆDÔö transcript_utils | no new tests (py_compile ok)
2025-11-24 - Groq STT run dV_FjwwQfiE-ogg32 :: 32k OGG fallback; text/SRT/combined produced | 03-outputs/groq_stt_pipeline/dV_FjwwQfiE-ogg32/
2025-11-25 - Gemini API tool + doc :: added gemini_api_tool (defaults 2.5-pro), new Gemini API reference; smoke test failed: API key invalid | 03-outputs/gemini-api/gemini-2.5-pro-poem/response.txt
2025-11-25 - Gemini API smoke (valid key) :: gemini-2.5-pro å”è©©æ¸¬è©¦æˆåŠŸ | 03-outputs/gemini-api/gemini-2.5-pro-poem/response.txt
2025-11-25 - Memo Gemini pipeline :: adds memo_gemini_pipeline (STT+Gemini flow) + smoke on existing combined | 03-outputs/memo_gemini_pipeline/dV_FjwwQfiE-gemini/refined.md
2025-11-28 - YouTube download g8VgzgnskI0 :: downloaded mp4 plus zh/zh-Hant subtitles via yt-dlp (Edge cookies) | offline copy ready | 03-outputs/youtube-download/2025-11-28_g8VgzgnskI0/
2025-11-28 - YourStyle/VideoMachine prompt tools :: added prompt generator scripts, registry/docs/playbooks updated | 03-outputs/yourstyle-agent/, 03-outputs/videomachine-agent/
2025-11-29 - YouTube download Elsh6-tcYRA :: fetched mp4 + zh-Hans/zh-Hant/en SRT via yt-dlp (chrome cookies + EJS solver) | 03-outputs/youtube-download/2025-11-29_Elsh6-tcYRA/
2025-12-01 - AGENTS API key source :: change: added default API-Keys.md lookup instruction; impact: centralizes key retrieval guidance; artifacts: AGENTS.md
2025-12-01 - Groq STT BV1UBCWBdE8Y :: ran groq_stt_pipeline on bilibili video (zh); outputs text+SRT+combined | 03-outputs/groq_stt_pipeline/BV1UBCWBdE8Y-groq/
2025-12-01 - Video structure note (BV1UBCWBdE8Y) :: analyzed script structure; archived reusable pattern for future copywriting | 03-outputs/video-structure-notes/BV1UBCWBdE8Y-structure.md

2025-12-02 - å„²å­˜ç›¤é» :: change: ç›¤é»å¯åˆªé™¤åª’é«”ä¸¦åˆ—è·¯å¾‘; impact: å¯é‡‹æ”¾ç´„ 4.4GB ä¸¦æ¨™ç¤ºé‡è¤‡ä¾†æº; artifacts: 03-outputs/storage-audit/2025-12-02_disk-audit.md