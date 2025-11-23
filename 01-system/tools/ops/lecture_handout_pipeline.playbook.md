# Playbook: lecture_handout_pipeline

**Purpose:** This tool uses an AI model (Gemini) to transform a plain text transcript into a well-structured Markdown handout, including a summary, key points, and formatted content.

**Command:**
```bash
python 01-system/tools/ops/lecture_handout_pipeline.py [input_file] [output_file] --title "[Your Title]" --prompt_file [path_to_prompt.txt]
```

**Arguments:**
- `input_file`: The full path to the source plain text file (e.g., a transcript).
- `output_file`: The full path where the new, AI-generated Markdown handout will be saved.
- `--title` (optional): The main title for the handout document. Defaults to "AI-Generated Handout".
- `--prompt_file` (optional): Path to a text file containing a custom prompt. You must use `{content}` as a placeholder within your custom prompt, which will be replaced by the content of the `input_file`.
