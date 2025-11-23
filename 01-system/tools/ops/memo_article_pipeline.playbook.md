# Playbook: memo_article_pipeline

**Purpose:** This tool uses an AI model (Gemini) to transform a plain text file into a polished, well-structured article in Markdown format.

**Command:**
```bash
python 01-system/tools/ops/memo_article_pipeline.py [input_file] [output_file] --title "[Your Title]" --prompt_file [path_to_prompt.txt]
```

**Arguments:**
- `input_file`: The full path to the source plain text file.
- `output_file`: The full path where the new, AI-generated Markdown article will be saved.
- `--title` (optional): The main title for the article. Defaults to "AI-Generated Article".
- `--prompt_file` (optional): Path to a text file containing a custom prompt. You must use `{content}` as a placeholder within your custom prompt.
