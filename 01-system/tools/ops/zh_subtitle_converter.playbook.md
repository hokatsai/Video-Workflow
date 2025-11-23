# Playbook: zh_subtitle_converter

**Purpose:** This tool converts the characters in a subtitle file between Simplified Chinese (简体) and Traditional Chinese (繁體).

**Command:**
```bash
python 01-system/tools/ops/zh_subtitle_converter.py [input_file] [output_file] [config]
```

**Arguments:**
- `input_file`: The full path to the source `.srt` subtitle file.
- `output_file`: The full path where the new, converted `.srt` file will be saved.
- `config`: The direction of conversion. Must be one of the following:
    - `s2t`: To convert from **S**implified to **T**raditional Chinese.
    - `t2s`: To convert from **T**raditional to **S**implified Chinese.
