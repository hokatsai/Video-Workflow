# Playbook: clips_adapter

**Purpose:** This tool adapts a video clip by changing its properties, such as resolution and frame rate (FPS).

**Command:**
```bash
python 01-system/tools/ops/clips_adapter.py [input_path] [output_path] --resolution [widthxheight] --fps [fps]
```

**Arguments:**
- `input_path`: The full path to the source video file.
- `output_path`: The full path where the new, adapted video will be saved.
- `--resolution` (optional): The new target resolution, formatted as "widthxheight" (e.g., "1280x720").
- `--fps` (optional): The new target frame rate as an integer (e.g., 24, 30).
