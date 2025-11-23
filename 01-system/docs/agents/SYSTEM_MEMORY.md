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

2025-11-23 – Groq STT pipeline :: built groq_stt_pipeline tool (compression+Groq whisper-large-v3 text/SRT+combined markdown) with docs/playbook | 03-outputs/groq_stt_pipeline/20251123-smoke3/combined/project-memos.md
2025-11-23 – Groq STT video support :: pipeline now accepts video inputs (audio extraction) with doc/playbook/user guide updates + retry tuned | 03-outputs/groq_stt_pipeline/20251123-video-smoke/combined/video.md
2025-11-24 – ElevenLabs scribe pipeline :: added eleven_scribe_pipeline tool (scribe_v1 STT text/SRT/combined), docs, playbook; awaiting XI_API_KEY for smoke test | 03-outputs/eleven_scribe_pipeline/
2025-11-24 – Playbooks cleanup + ElevenLabs ref doc :: rewrote PLAYBOOKS.md (zh), added ElevenLabs STT API reference; Groq youtube run 03-outputs/groq_stt_pipeline/20251124-groq-youtube3/combined/youtube_video_dVY-qqXyv5U.md
