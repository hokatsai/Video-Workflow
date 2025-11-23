# Playbook: subtitle_corrector

**Purpose:** This tool uses an AI model (Gemini) to correct spelling, grammar, and punctuation errors in a subtitle file (e.g., `.srt`).

**Command:**
```bash
python 01-system/tools/ops/subtitle_corrector.py [input_file] [output_file] [--prompt_file path/to/prompt.txt]
```

**Arguments:**
- `input_file`: The full path to the source `.srt` subtitle file.
- `output_file`: The full path where the new, corrected `.srt` file will be saved.
- `--prompt_file` (optional): Path to a text file containing a custom prompt. You must use `{content}` as a placeholder, which will be replaced by the numbered lines of the subtitle text.
