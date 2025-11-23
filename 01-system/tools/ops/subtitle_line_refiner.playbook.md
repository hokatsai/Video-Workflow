# Playbook: subtitle_line_refiner

**Purpose:** This tool uses an AI model (Gemini) to refine the style, flow, and readability of a subtitle file. It focuses on improving sentence structure, simplifying language, and ensuring a natural tone, rather than just fixing basic errors.

**Command:**
```bash
python 01-system/tools/ops/subtitle_line_refiner.py [input_file] [output_file] [--prompt_file path/to/prompt.txt]
```

**Arguments:**
- `input_file`: The full path to the source `.srt` subtitle file.
- `output_file`: The full path where the new, refined `.srt` file will be saved.
- `--prompt_file` (optional): Path to a text file containing a custom prompt. You must use `{content}` as a placeholder, which will be replaced by the numbered lines of the subtitle text.
