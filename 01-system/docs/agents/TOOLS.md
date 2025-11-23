# Tool Index

| name | category | summary | artifacts |
| --- | --- | --- | --- |
| gemini-cli | llms | Gemini CLI wrapper + logged runs via 01-system/tools/llms/gemini-cli/gemini-run.ps1 | 03-outputs/gemini-cli/ |
| gemini (module) | llms | Core Python module for other tools to call the Gemini API (`generate_text` function). | N/A (library) |
| audio_compressor | ops | Compresses an audio file to a specified bitrate. | 03-outputs/audio_compressor/ |
| groq_stt_pipeline | stt | Groq whisper-large-v3 STT with pre-compression, text/SRT outputs, optional combined markdown. | 03-outputs/groq_stt_pipeline/ |
| clips_adapter | ops | Adapts a video clip to a new resolution and/or frame rate. | 03-outputs/clips_adapter/ |
| clips_copy_exporter | ops | Copies or moves files to an export directory. | 03-outputs/clips_copy_exporter/ |
| clips_orchestrator | ops | Automates the process of extracting, adapting, and exporting multiple video clips from a single source video. | 03-outputs/clips_orchestrator/ |
| lecture_handout_local_pipeline | ops | Creates a formatted Markdown handout from a plain text file locally. | 03-outputs/lecture_handout_local_pipeline/ |
| lecture_handout_pipeline | ops | Creates a formatted Markdown handout from a text file using an AI model. | 03-outputs/lecture_handout_pipeline/ |
| memo_article_pipeline | ops | Creates a formatted Markdown article from a text file using an AI model. | 03-outputs/memo_article_pipeline/ |
| memo_transcript_pipeline | ops | Creates a formatted Markdown memo/minutes from a transcript file using an AI model. | 03-outputs/memo_transcript_pipeline/ |
| subtitle_corrector | ops | Corrects spelling, grammar, and punctuation in a subtitle file using an AI model. | 03-outputs/subtitle_corrector/ |
| subtitle_line_refiner | ops | Refines the style, flow, and readability of a subtitle file using an AI model. | 03-outputs/subtitle_line_refiner/ |
| subtitle_pipeline | ops | Automates the subtitle correction and refinement process. | 03-outputs/subtitle_pipeline/ |
| zh_subtitle_converter | ops | Converts subtitle files between Simplified and Traditional Chinese. | 03-outputs/zh_subtitle_converter/ |
| video_compressor | ops | Compresses a video file by re-encoding it with a lower bitrate. | 03-outputs/video_compressor/ |
