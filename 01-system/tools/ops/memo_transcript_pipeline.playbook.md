# Playbook: memo_transcript_pipeline

**Purpose:** This tool uses an AI model (Gemini) to transform a raw meeting or dialogue transcript into a structured meeting memo (or minutes) in Markdown format.

**Command:**
```bash
python 01-system/tools/ops/memo_transcript_pipeline.py [input_file] [output_file] --title "[Your Title]" --prompt_file [path_to_prompt.txt]
```

**Arguments:**
- `input_file`: The full path to the source plain text transcript file.
- `output_file`: The full path where the new, AI-generated Markdown memo will be saved.
- `--title` (optional): The main title for the memo. Defaults to "Meeting Memo".
- `--prompt_file` (optional): Path to a text file containing a custom prompt. You must use `{content}` as a placeholder within your custom prompt.
