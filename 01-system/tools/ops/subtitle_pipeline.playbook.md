# Playbook: subtitle_pipeline

**Purpose:** This tool automates the entire subtitle improvement process by chaining together the `subtitle_corrector` and `subtitle_line_refiner` tools. It takes a raw subtitle file and produces a final version that is both grammatically correct and stylistically refined.

**Command:**
```bash
python 01-system/tools/ops/subtitle_pipeline.py [input_file] [output_file] [--corrector_prompt path/to/corr_prompt.txt] [--refiner_prompt path/to/refine_prompt.txt]
```

**Arguments:**
- `input_file`: The full path to the source raw `.srt` subtitle file.
- `output_file`: The full path where the final, fully processed `.srt` file will be saved.
- `--corrector_prompt` (optional): Path to a custom prompt file for the initial correction step.
- `--refiner_prompt` (optional): Path to a custom prompt file for the final refinement step.
