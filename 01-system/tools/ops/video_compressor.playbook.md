# Playbook: video_compressor

**Purpose:** This tool compresses a video file by re-encoding it with a lower video bitrate, which significantly reduces the file size.

**Command:**
```bash
python 01-system/tools/ops/video_compressor.py [input_path] [output_path] --bitrate [bitrate]
```

**Arguments:**
- `input_path`: The full path to the source video file.
- `output_path`: The full path where the new, compressed video file will be saved.
- `--bitrate` (optional): The target video bitrate for the compression, e.g., "500k", "1000k". A lower value results in a smaller file and lower quality. Defaults to "500k".
