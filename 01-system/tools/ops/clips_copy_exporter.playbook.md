# Playbook: clips_copy_exporter

**Purpose:** This tool copies or moves a file (or all files within a directory) to a specified destination directory. It's useful for organizing and exporting final assets.

**Command:**
```bash
python 01-system/tools/ops/clips_copy_exporter.py [source_path] [destination_path] [--move]
```

**Arguments:**
- `source_path`: The full path to the source file or directory that you want to export.
- `destination_path`: The full path of the folder where the files should be copied or moved to.
- `--move` (optional): If this flag is included, the files will be moved instead of copied.
