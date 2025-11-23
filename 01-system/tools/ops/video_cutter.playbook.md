# Playbook: video_cutter

**Purpose:** This tool cuts a segment from a video file based on start and end times and saves it as a new file.

**Command:**
```bash
python 01-system/tools/ops/video_cutter.py [input_path] [output_path] [start_time] [end_time]
```

**Arguments:**
- `input_path`: The full path to the source video file.
- `output_path`: The full path where the new, cut video will be saved.
- `start_time`: The start time of the cut in seconds (can be a decimal).
- `end_time`: The end time of the cut in seconds (can be a decimal).
