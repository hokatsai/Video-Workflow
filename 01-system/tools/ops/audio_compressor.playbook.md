# Playbook: audio_compressor

**Purpose:** This tool compresses an audio file to a smaller size by reducing its bitrate. It is useful for reducing storage space or for faster transmission.

**Command:**
```bash
python 01-system/tools/ops/audio_compressor.py [input_path] [output_path] --bitrate [bitrate]
```

**Arguments:**
- `input_path`: The full path to the source audio file (e.g., `.mp3`, `.wav`, `.m4a`).
- `output_path`: The full path where the new, compressed audio file will be saved. The format is determined by the file extension.
- `--bitrate` (optional): The target bitrate for the compression, e.g., "128k", "64k", "32k". Defaults to "64k".
