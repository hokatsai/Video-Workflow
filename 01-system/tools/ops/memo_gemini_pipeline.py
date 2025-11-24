"""
Pipeline: refine combined memo transcripts with Gemini (gemini-2.5-pro by default).
- Mode A: Provide --combined_file to directly refine existing combined Markdown.
- Mode B: Provide --input_dir and --stt_tool (groq|eleven) to run STT first, then refine the combined output.
Outputs are stored under 03-outputs/memo_gemini_pipeline/<run-id>/.
"""

import argparse
import datetime
import json
import os
import subprocess
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(repo_root / "01-system"))

from tools.llms.gemini.gemini import generate_text  # type: ignore


def load_api_keys() -> dict:
    path = repo_root / "01-system" / "configs" / "apis" / "API-Keys.md"
    keys: dict[str, str] = {}
    if not path.exists():
        return keys
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if "=" not in line:
            continue
        name, value = line.split("=", 1)
        keys[name.strip()] = value.strip()
    return keys


def ensure_env(env_name: str, keys: dict, key_name: str | None = None) -> str:
    if os.environ.get(env_name):
        return os.environ[env_name]
    key_lookup = key_name or env_name
    if key_lookup in keys and keys[key_lookup]:
        os.environ[env_name] = keys[key_lookup]
        return keys[key_lookup]
    raise EnvironmentError(f"{env_name} not set and missing in API-Keys.md")


def run_stt(stt_tool: str, input_dir: Path, stt_run_id: str, keys: dict) -> Path:
    python_bin = repo_root / ".venv" / "Scripts" / "python.exe"
    if stt_tool == "groq":
        ensure_env("GROQ_API_KEY", keys, "GROQ_API_KEY")
        script = repo_root / "01-system" / "tools" / "stt" / "groq_stt_pipeline.py"
        output_base = repo_root / "03-outputs" / "groq_stt_pipeline"
        cmd = [
            str(python_bin),
            str(script),
            "--input_dir",
            str(input_dir),
            "--run_id",
            stt_run_id,
        ]
        subprocess.run(cmd, check=True)
        return output_base / stt_run_id / "combined" / "combined.md"

    if stt_tool == "eleven":
        ensure_env("XI_API_KEY", keys, "Elevenlabs API KEY")
        script = repo_root / "01-system" / "tools" / "stt" / "eleven_scribe_pipeline.py"
        output_base = repo_root / "03-outputs" / "eleven_scribe_pipeline"
        cmd = [
            str(python_bin),
            str(script),
            "--input_dir",
            str(input_dir),
            "--run_id",
            stt_run_id,
        ]
        subprocess.run(cmd, check=True)
        return output_base / stt_run_id / "combined" / "combined.md"

    raise ValueError("Unsupported stt_tool (expected groq or eleven).")


def build_prompt(template_path: Path, combined_text: str) -> str:
    template = template_path.read_text(encoding="utf-8")
    return f"{template.strip()}\n\n---\n原始文本：\n{combined_text.strip()}\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Refine combined memo transcripts with Gemini. Provide --combined_file or (--input_dir + --stt_tool)."
    )
    parser.add_argument("--combined_file", help="Path to existing combined Markdown to refine.")
    parser.add_argument("--input_dir", help="Folder with audio/video files (will run STT to produce combined).")
    parser.add_argument("--stt_tool", choices=["groq", "eleven"], help="STT backend when input_dir is provided.")
    parser.add_argument(
        "--prompt_file",
        default=str(repo_root / "01-system" / "docs" / "prompts" / "風格化文章生成器（口述稿專用）.md"),
        help="Prompt file used to guide Gemini refinement.",
    )
    parser.add_argument(
        "--model",
        default="gemini-2.5-pro",
        help="Gemini model name (default gemini-2.5-pro).",
    )
    parser.add_argument("--title", default="Refined Memo", help="Title for the output Markdown.")
    parser.add_argument(
        "--output_base",
        default=str(repo_root / "03-outputs" / "memo_gemini_pipeline"),
        help="Base output directory.",
    )
    parser.add_argument("--run_id", default=None, help="Optional run identifier for output folder naming.")
    parser.add_argument("--stt_run_id", default=None, help="Optional STT run identifier override.")
    parser.add_argument("--output_filename", default="refined.md", help="Filename for refined Markdown.")

    args = parser.parse_args()

    run_id = args.run_id or datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    run_dir = Path(args.output_base).resolve() / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    keys = load_api_keys()

    # Determine combined source
    combined_path: Path
    stt_info: dict | None = None
    if args.combined_file:
        combined_path = Path(args.combined_file).resolve()
    else:
        if not args.input_dir or not args.stt_tool:
            raise ValueError("Provide --combined_file or (--input_dir and --stt_tool).")
        stt_run_id = args.stt_run_id or f"{run_id}-{args.stt_tool}"
        combined_path = run_stt(args.stt_tool, Path(args.input_dir).resolve(), stt_run_id, keys)
        stt_info = {"tool": args.stt_tool, "run_id": stt_run_id, "combined_path": str(combined_path)}

    if not combined_path.exists():
        raise FileNotFoundError(f"Combined file not found: {combined_path}")

    combined_text = combined_path.read_text(encoding="utf-8")
    prompt_path = Path(args.prompt_file).resolve()
    final_prompt = build_prompt(prompt_path, combined_text)

    # Save prompt and source for traceability
    prompt_out = run_dir / "prompt.txt"
    prompt_out.write_text(final_prompt, encoding="utf-8")
    (run_dir / "input_combined.md").write_text(combined_text, encoding="utf-8")

    ensure_env("GEMINI_API_KEY", keys, "GEMINI_API_KEY")
    response = generate_text(final_prompt, model_name=args.model)
    response_path = run_dir / "response.txt"
    response_path.write_text(response, encoding="utf-8")

    refined_md = f"# {args.title}\n\n{response.strip()}\n"
    output_md_path = run_dir / args.output_filename
    output_md_path.write_text(refined_md, encoding="utf-8")

    meta = {
        "mode": "combined_only" if args.combined_file else "stt_then_refine",
        "run_id": run_id,
        "stt": stt_info,
        "prompt_file": str(prompt_path),
        "combined_file": str(combined_path),
        "gemini_model": args.model,
        "outputs": {
            "prompt": str(prompt_out),
            "response": str(response_path),
            "refined_markdown": str(output_md_path),
        },
    }
    (run_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Refined article saved -> {output_md_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
