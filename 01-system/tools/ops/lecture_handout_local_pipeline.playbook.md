# Playbook: lecture_handout_local_pipeline

**Purpose:** This tool creates a simple, formatted Markdown handout from a plain text file (like a transcript). This version runs entirely locally without external APIs.

**Command:**
```bash
python 01-system/tools/ops/lecture_handout_local_pipeline.py [input_file] [output_file] --title "[Your Title]"
```

**Arguments:**
- `input_file`: The full path to the source plain text file.
- `output_file`: The full path where the new Markdown handout will be saved.
- `--title` (optional): The main title for the handout document. Defaults to "Lecture Handout".
