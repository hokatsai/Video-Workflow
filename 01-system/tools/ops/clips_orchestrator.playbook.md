# Playbook: 影片片段總调度器 (clips_orchestrator)

**Purpose:** This tool automates the process of extracting, adapting, and exporting multiple video clips from a single source video. It orchestrates the `video_cutter`, `clips_adapter`, and implicitly the `clips_copy_exporter` tools.

**Command:**
```bash
python 01-system/tools/ops/clips_orchestrator.py [input_video] [timestamps_file] [output_base_dir] [--resolution "widthxheight"] [--fps N]
```

**Arguments:**
- `input_video`: 來源影片檔案的完整路徑。
- `timestamps_file`: 包含剪輯時間戳的 JSON 檔案路徑。格式範例：`[{"start": 0.0, "end": 10.0, "name": "intro_clip"}, {"start": 15.0, "end": 30.0, "name": "main_scene"}, ...]`
- `output_base_dir`: 處理後所有影片片段的基礎輸出目錄。
- `--resolution` (可選): 目標解析度，格式為 `"寬度x高度"` (例如 `"1280x720"`)。若指定，所有剪輯出的影片片段將被調整到此解析度。
- `--fps` (可選): 目標影格率，為一個整數 (例如 `25`, `30`)。若指定，所有剪輯出的影片片段將被調整到此影格率。
