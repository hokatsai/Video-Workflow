import argparse
import base64
import datetime
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

import requests

from transcript_utils import build_combined_markdown, ensure_dir, natural_key, write_text

DEFAULT_MODEL = "scribe_v1"
FREE_LIMIT_BYTES = 3 * 1024 * 1024 * 1024  # API allows up to ~3GB
AUDIO_EXTENSIONS = {".flac", ".mp3", ".mpeg", ".mpga", ".m4a", ".ogg", ".wav"}
VIDEO_EXTENSIONS = {".mp4", ".webm", ".mov", ".mkv", ".avi", ".m4v", ".ts"}
SUPPORTED_EXTENSIONS = AUDIO_EXTENSIONS | VIDEO_EXTENSIONS


def run_ffmpeg(input_path: Path, output_path: Path) -> None:
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-ar",
        "16000",
        "-ac",
        "1",
        "-map",
        "0:a",
        "-c:a",
        "flac",
        str(output_path),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def compress_audio(source: Path, flac_path: Path, max_size_bytes: int) -> Tuple[Path, List[str]]:
    logs: List[str] = []
    run_ffmpeg(source, flac_path)
    size = flac_path.stat().st_size
    logs.append(f"Compressed to FLAC: {flac_path} ({size / (1024 * 1024):.2f} MB)")
    if size > max_size_bytes:
        raise ValueError(
            f"Compressed file exceeds limit: {size / (1024 * 1024):.2f} MB > {max_size_bytes / (1024 * 1024):.2f} MB"
        )
    return flac_path, logs


def srt_timestamp(seconds: float) -> str:
    millis = int(round(seconds * 1000))
    hours, remainder = divmod(millis, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, ms = divmod(remainder, 1_000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def words_to_srt(words: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    for idx, word in enumerate(words, start=1):
        start = float(word.get("start", 0) or 0)
        end = float(word.get("end", start) or start)
        text = str(word.get("text", "")).strip()
        lines.append(str(idx))
        lines.append(f"{srt_timestamp(start)} --> {srt_timestamp(end)}")
        lines.append(text)
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def parse_response(resp: Dict[str, Any]) -> Tuple[str, List[Dict[str, Any]]]:
    if "text" in resp and "words" in resp:
        return str(resp.get("text", "")), resp.get("words") or []
    if "transcripts" in resp and isinstance(resp["transcripts"], list):
        merged_text = []
        merged_words: List[Dict[str, Any]] = []
        for transcript in resp["transcripts"]:
            merged_text.append(str(transcript.get("text", "")))
            merged_words.extend(transcript.get("words") or [])
        return "\n".join(merged_text).strip(), merged_words
    return "", []


def save_additional_formats(additional_formats: List[Dict[str, Any]], subtitles_dir: Path, transcripts_dir: Path, stem: str) -> Tuple[Path | None, Path | None]:
    srt_path = None
    txt_path = None
    for item in additional_formats:
        fmt = item.get("requested_format")
        content = item.get("content")
        is_b64 = item.get("is_base64_encoded", False)
        if not content:
            continue
        data = base64.b64decode(content) if is_b64 else content.encode("utf-8")
        if fmt == "srt":
            srt_path = subtitles_dir / f"{stem}.srt"
            srt_path.write_bytes(data)
        elif fmt == "txt":
            txt_path = transcripts_dir / f"{stem}.md"
            txt_path.write_bytes(data)
    return srt_path, txt_path


def transcribe(
    audio_path: Path,
    api_key: str,
    language: str | None,
    timestamps_granularity: str,
) -> Dict[str, Any]:
    headers = {"xi-api-key": api_key}
    data: Dict[str, Any] = {
        "model_id": DEFAULT_MODEL,
        "timestamps_granularity": timestamps_granularity,
    }
    if language:
        data["language_code"] = language
    files = {"file": (audio_path.name, audio_path.open("rb"), "application/octet-stream")}
    response = requests.post(
        "https://api.elevenlabs.io/v1/speech-to-text",
        headers=headers,
        data=data,
        files=files,
        timeout=600,
    )
    if response.status_code not in (200, 202):
        raise RuntimeError(f"ElevenLabs STT failed ({response.status_code}): {response.text}")
    return response.json()


def collect_input_files(input_dir: Path) -> List[Path]:
    files = [p for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS]
    if not files:
        raise FileNotFoundError(f"No supported audio/video files found in {input_dir}")
    return sorted(files, key=natural_key)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Transcribe audio/video with ElevenLabs scribe_v1, output text + SRT, and optionally combine plain text transcripts."
    )
    parser.add_argument("--input_dir", required=True, help="Directory containing audio/video files.")
    parser.add_argument(
        "--output_base",
        default="03-outputs/eleven_scribe_pipeline",
        help="Base output directory (defaults to 03-outputs/eleven_scribe_pipeline).",
    )
    parser.add_argument("--language", default=None, help="ISO language code hint (optional).")
    parser.add_argument("--run_id", default=None, help="Optional run identifier for output folder naming.")
    parser.add_argument(
        "--max_size_mb",
        type=float,
        default=100.0,
        help="Maximum compressed file size (MB). Default 100MB (below 3GB API limit).",
    )
    parser.add_argument(
        "--timestamps_granularity",
        default="word",
        choices=["none", "word", "character"],
        help="Timestamp granularity returned by API (default word).",
    )
    parser.add_argument(
        "--no_combine",
        action="store_true",
        help="Skip generating the combined plain-text Markdown.",
    )
    parser.add_argument(
        "--combine_filename",
        default="combined.md",
        help="Filename for the combined plain-text transcript (when enabled).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir).resolve()
    output_base = Path(args.output_base)
    run_id = args.run_id or datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    run_dir = (output_base / run_id).resolve()

    api_key = os.getenv("XI_API_KEY")
    if not api_key:
        raise EnvironmentError("XI_API_KEY is not set. Please configure the ElevenLabs API key before running.")

    ensure_dir(run_dir)
    compressed_dir = run_dir / "compressed"
    raw_dir = run_dir / "raw"
    transcripts_dir = run_dir / "transcripts"
    subtitles_dir = run_dir / "subtitles"
    combined_dir = run_dir / "combined"
    for path in [compressed_dir, raw_dir, transcripts_dir, subtitles_dir, combined_dir]:
        ensure_dir(path)

    files = collect_input_files(input_dir)
    audio_count = sum(1 for p in files if p.suffix.lower() in AUDIO_EXTENSIONS)
    video_count = sum(1 for p in files if p.suffix.lower() in VIDEO_EXTENSIONS)
    print(f"Found {len(files)} file(s) in {input_dir} (audio={audio_count}, video={video_count})")

    max_size_bytes = int(args.max_size_mb * 1024 * 1024)
    results: List[Dict[str, Any]] = []
    manifest_files: List[Dict[str, Any]] = []

    for source_path in files:
        kind = "video" if source_path.suffix.lower() in VIDEO_EXTENSIONS else "audio"
        print(f"Processing: {source_path.name} ({kind})")
        stem = source_path.stem
        flac_path = compressed_dir / f"{stem}.flac"

        try:
            selected_path, compress_logs = compress_audio(source_path, flac_path, max_size_bytes)
        except Exception as exc:
            print(f"[ERROR] Compression failed for {source_path.name}: {exc}", file=sys.stderr)
            continue

        for line in compress_logs:
            print(f"  - {line}")

        try:
            stt_resp = transcribe(
                selected_path,
                api_key=api_key,
                language=args.language,
                timestamps_granularity=args.timestamps_granularity,
            )
        except Exception as exc:
            print(f"[ERROR] Transcription failed for {source_path.name}: {exc}", file=sys.stderr)
            continue

        write_text(raw_dir / f"{stem}.json", json.dumps(stt_resp, ensure_ascii=False, indent=2))

        text_content, words = parse_response(stt_resp)
        srt_text = words_to_srt(words) if words else "No timestamped words available.\n"

        text_path = transcripts_dir / f"{stem}.md"
        srt_path = subtitles_dir / f"{stem}.srt"
        write_text(text_path, text_content)
        write_text(srt_path, srt_text)

        results.append(
            {
                "source_name": source_path.name,
                "source_path": str(source_path),
                "input_kind": kind,
                "compressed_path": str(selected_path),
                "text": text_content,
                "text_path": str(text_path),
                "srt_path": str(srt_path),
                "raw_path": str(raw_dir / f"{stem}.json"),
            }
        )
        manifest_files.append(
            {
                "source": str(source_path),
                "input_kind": kind,
                "compressed_used": str(selected_path),
                "text_path": str(text_path),
                "srt_path": str(srt_path),
                "raw_path": str(raw_dir / f"{stem}.json"),
            }
        )
        print(f"  - Saved text -> {text_path}")
        print(f"  - Saved SRT -> {srt_path}")

    if not results:
        raise RuntimeError("No files were successfully transcribed.")

    combined_path = None
    if not args.no_combine:
        combined_content = build_combined_markdown(results, run_id, input_dir, DEFAULT_MODEL, args.language)
        combined_path = combined_dir / args.combine_filename
        write_text(combined_path, combined_content)
        print(f"Combined Markdown saved -> {combined_path}")

    manifest = {
        "run_id": run_id,
        "model": DEFAULT_MODEL,
        "language": args.language,
        "input_dir": str(input_dir),
        "output_dir": str(run_dir),
        "input_counts": {"audio": audio_count, "video": video_count},
        "max_size_mb": args.max_size_mb,
        "timestamps_granularity": args.timestamps_granularity,
        "files": manifest_files,
        "combined_path": str(combined_path) if combined_path else None,
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
    }
    write_text(run_dir / "run_meta.json", json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"Run complete. Outputs stored in {run_dir}")


if __name__ == "__main__":
    main()
