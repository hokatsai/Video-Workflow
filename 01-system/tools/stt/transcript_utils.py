"""
Shared helpers for STT pipelines (Groq / ElevenLabs).
"""

from pathlib import Path
from typing import Any, Dict, List, Sequence
import re


def natural_key(path: Path) -> Sequence[Any]:
    parts = re.split(r"(\d+)", path.name)
    return [int(p) if p.isdigit() else p.lower() for p in parts]


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


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
