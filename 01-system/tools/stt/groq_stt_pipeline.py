import argparse
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

DEFAULT_MODEL = "whisper-large-v3"
FREE_TIER_LIMIT_BYTES = 25 * 1024 * 1024
AUDIO_EXTENSIONS = {".flac", ".mp3", ".mpeg", ".mpga", ".m4a", ".ogg", ".wav"}
VIDEO_EXTENSIONS = {".mp4", ".webm", ".mov", ".mkv", ".avi", ".m4v", ".ts"}
SUPPORTED_EXTENSIONS = AUDIO_EXTENSIONS | VIDEO_EXTENSIONS


def natural_key(path: Path) -> Sequence[Any]:
    parts = re.split(r"(\d+)", path.name)
    return [int(p) if p.isdigit() else p.lower() for p in parts]


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def run_ffmpeg(
    input_path: Path,
    output_path: Path,
    codec_args: List[str],
) -> None:
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
        *codec_args,
        str(output_path),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def compress_audio(
    source: Path,
    flac_path: Path,
    ogg_path: Path,
    max_size_bytes: int,
    allow_ogg_fallback: bool,
    ogg_bitrate: str,
) -> Tuple[Path, List[str]]:
    logs: List[str] = []
    run_ffmpeg(source, flac_path, ["-c:a", "flac"])
    logs.append(f"Compressed to FLAC: {flac_path}")

    selected = flac_path
    size = flac_path.stat().st_size

    if size > max_size_bytes and allow_ogg_fallback:
        run_ffmpeg(source, ogg_path, ["-c:a", "libvorbis", "-b:a", ogg_bitrate])
        logs.append(
            f"FLAC size {size / (1024 * 1024):.2f} MB exceeded limit; fallback to OGG at {ogg_bitrate}: {ogg_path}"
        )
        selected = ogg_path
        size = ogg_path.stat().st_size

    if size > max_size_bytes:
        raise ValueError(
            f"Compressed file still exceeds free tier limit: {size / (1024 * 1024):.2f} MB > {max_size_bytes / (1024 * 1024):.2f} MB"
        )

    logs.append(f"Selected for STT: {selected} ({size / (1024 * 1024):.2f} MB)")
    return selected, logs


def srt_timestamp(seconds: float) -> str:
    millis = int(round(seconds * 1000))
    hours, remainder = divmod(millis, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, ms = divmod(remainder, 1_000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def segments_to_srt(segments: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    for idx, seg in enumerate(segments, start=1):
        start = float(seg.get("start", 0))
        end = float(seg.get("end", start))
        text = str(seg.get("text", "")).strip()
        lines.append(str(idx))
        lines.append(f"{srt_timestamp(start)} --> {srt_timestamp(end)}")
        lines.append(text)
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def transcribe(
    audio_path: Path,
    api_key: str,
    language: str | None,
    prompt: str | None,
) -> Dict[str, Any]:
    headers = {"Authorization": f"Bearer {api_key}"}
    data: List[Tuple[str, str]] = [
        ("model", DEFAULT_MODEL),
        ("response_format", "verbose_json"),
        ("timestamp_granularities[]", "segment"),
    ]
    if language:
        data.append(("language", language))
    if prompt:
        data.append(("prompt", prompt))

    with audio_path.open("rb") as audio_file:
        files = {"file": (audio_path.name, audio_file, "application/octet-stream")}
        response = requests.post(
            "https://api.groq.com/openai/v1/audio/transcriptions",
            headers=headers,
            data=data,
            files=files,
            timeout=600,
        )

    if not response.ok:
        raise RuntimeError(f"Groq STT failed ({response.status_code}): {response.text}")

    return response.json()


def transcribe_with_retry(
    audio_path: Path,
    api_key: str,
    language: str | None,
    prompt: str | None,
    retries: int = 3,
    delay: float = 2.0,
) -> Dict[str, Any]:
    last_exc: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            return transcribe(audio_path, api_key, language, prompt)
        except Exception as exc:
            last_exc = exc
            message = str(exc)
            if "401" in message or "invalid_api_key" in message.lower():
                raise RuntimeError(f"Transcription aborted due to auth error: {exc}")
            if attempt == retries:
                break
            print(f"  - Retry {attempt}/{retries} after error: {exc}")
            time.sleep(delay * attempt)
    raise RuntimeError(f"Transcription failed after {retries} attempts: {last_exc}")


def collect_audio_files(input_dir: Path) -> List[Path]:
    files = [p for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS]
    if not files:
        raise FileNotFoundError(f"No supported audio/video files found in {input_dir}")
    return sorted(files, key=natural_key)


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def build_combined_markdown(
    items: List[Dict[str, Any]],
    run_id: str,
    input_dir: Path,
    model: str,
    language: str | None,
) -> str:
    lines = [
        "# Combined Transcripts (Plain Text)",
        f"- Run: {run_id}",
        f"- Source: {input_dir}",
        f"- Model: {model}",
        f"- Language hint: {language or 'auto-detect'}",
        "",
    ]
    for item in items:
        lines.append(f"## {item['source_name']}")
        lines.append(item["text"].strip())
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compress audio, transcribe with Groq whisper-large-v3, emit text + SRT, and optionally combine text transcripts."
    )
    parser.add_argument("--input_dir", required=True, help="Directory containing audio files.")
    parser.add_argument(
        "--output_base",
        default="03-outputs/groq_stt_pipeline",
        help="Base output directory (defaults to 03-outputs/groq_stt_pipeline).",
    )
    parser.add_argument("--language", default=None, help="ISO-639-1 language code (optional).")
    parser.add_argument("--prompt", default=None, help="Optional style/context prompt for STT.")
    parser.add_argument("--run_id", default=None, help="Optional run identifier for output folder naming.")
    parser.add_argument(
        "--max_size_mb",
        type=float,
        default=24.5,
        help="Maximum compressed file size for free tier (MB). Defaults to 24.5 MB (slightly under Groq 25 MB limit).",
    )
    parser.add_argument(
        "--ogg_bitrate",
        default="48k",
        help="Bitrate used when falling back to OGG compression. Defaults to 48k.",
    )
    parser.add_argument(
        "--no_combine",
        action="store_true",
        help="Skip generating the combined plain-text Markdown.",
    )
    parser.add_argument(
        "--no_ogg_fallback",
        action="store_true",
        help="Do not fallback to OGG even if FLAC exceeds the free tier limit.",
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

    ensure_dir(run_dir)
    compressed_dir = run_dir / "compressed"
    raw_dir = run_dir / "raw"
    transcripts_dir = run_dir / "transcripts"
    subtitles_dir = run_dir / "subtitles"
    combined_dir = run_dir / "combined"
    for path in [compressed_dir, raw_dir, transcripts_dir, subtitles_dir, combined_dir]:
        ensure_dir(path)

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError("GROQ_API_KEY is not set. Please configure the Groq API key before running.")

    audio_files = collect_audio_files(input_dir)
    audio_count = sum(1 for p in audio_files if p.suffix.lower() in AUDIO_EXTENSIONS)
    video_count = sum(1 for p in audio_files if p.suffix.lower() in VIDEO_EXTENSIONS)
    print(f"Found {len(audio_files)} file(s) in {input_dir} (audio={audio_count}, video={video_count})")

    max_size_bytes = int(args.max_size_mb * 1024 * 1024)
    results: List[Dict[str, Any]] = []
    manifest_files: List[Dict[str, Any]] = []

    for audio_path in audio_files:
        source_kind = "video" if audio_path.suffix.lower() in VIDEO_EXTENSIONS else "audio"
        print(f"Processing: {audio_path.name} ({source_kind})")
        stem = audio_path.stem
        flac_path = compressed_dir / f"{stem}.flac"
        ogg_path = compressed_dir / f"{stem}.ogg"

        try:
            selected_path, compress_logs = compress_audio(
                audio_path,
                flac_path,
                ogg_path,
                max_size_bytes=max_size_bytes,
                allow_ogg_fallback=not args.no_ogg_fallback,
                ogg_bitrate=args.ogg_bitrate,
            )
        except Exception as exc:
            print(f"[ERROR] Compression failed for {audio_path.name}: {exc}", file=sys.stderr)
            continue

        for line in compress_logs:
            print(f"  - {line}")

        try:
            stt_result = transcribe_with_retry(
                selected_path,
                api_key=api_key,
                language=args.language,
                prompt=args.prompt,
            )
        except Exception as exc:
            print(f"[ERROR] Transcription failed for {audio_path.name}: {exc}", file=sys.stderr)
            continue

        text_content = stt_result.get("text", "")
        segments = stt_result.get("segments", [])
        text_path = transcripts_dir / f"{stem}.md"
        raw_path = raw_dir / f"{stem}.json"
        srt_path = subtitles_dir / f"{stem}.srt"

        write_text(text_path, text_content)
        write_text(raw_path, json.dumps(stt_result, ensure_ascii=False, indent=2))

        if segments:
            srt_text = segments_to_srt(segments)
            write_text(srt_path, srt_text)
        else:
            write_text(srt_path, "No timestamped segments available.\n")

        results.append(
            {
                "source_name": audio_path.name,
                "source_path": str(audio_path),
                "input_kind": source_kind,
                "compressed_path": str(selected_path),
                "text": text_content,
                "text_path": str(text_path),
                "srt_path": str(srt_path),
                "raw_path": str(raw_path),
            }
        )
        manifest_files.append(
            {
                "source": str(audio_path),
                "input_kind": source_kind,
                "compressed_used": str(selected_path),
                "text_path": str(text_path),
                "srt_path": str(srt_path),
                "raw_path": str(raw_path),
            }
        )
        print(f"  - Saved text -> {text_path}")
        print(f"  - Saved SRT -> {srt_path}")

    if not results:
        raise RuntimeError("No files were successfully transcribed.")

    if not args.no_combine:
        combined_content = build_combined_markdown(results, run_id, input_dir, DEFAULT_MODEL, args.language)
        combined_path = combined_dir / args.combine_filename
        write_text(combined_path, combined_content)
        print(f"Combined Markdown saved -> {combined_path}")
    else:
        combined_path = None

    manifest = {
        "run_id": run_id,
        "model": DEFAULT_MODEL,
        "language": args.language,
        "prompt": bool(args.prompt),
        "input_dir": str(input_dir),
        "output_dir": str(run_dir),
        "input_counts": {"audio": audio_count, "video": video_count},
        "max_size_mb": args.max_size_mb,
        "ogg_bitrate": args.ogg_bitrate,
        "files": manifest_files,
        "combined_path": str(combined_path) if combined_path else None,
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
    }
    write_text(run_dir / "run_meta.json", json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"Run complete. Outputs stored in {run_dir}")


if __name__ == "__main__":
    main()
