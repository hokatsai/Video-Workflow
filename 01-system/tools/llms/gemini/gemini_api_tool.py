"""
CLI helper to call Gemini API (gemini-2.5-pro by default) and log prompt/response.
Outputs are written to 03-outputs/gemini-api/<run-id>/.
"""

import argparse
import datetime
import json
import sys
from pathlib import Path

import google.generativeai as genai


def read_api_key(api_keys_path: Path) -> str:
    for line in api_keys_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("GEMINI_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise RuntimeError("GEMINI_API_KEY not found in API-Keys.md")


def save_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Call Gemini API and log prompt/response.")
    parser.add_argument("--prompt", required=True, help="Prompt to send to Gemini.")
    parser.add_argument(
        "--model",
        default="gemini-2.5-pro",
        help="Gemini model name (default gemini-2.5-pro).",
    )
    parser.add_argument(
        "--output_name",
        default=None,
        help="Optional run folder name under 03-outputs/gemini-api/. Defaults to UTC timestamp.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    api_keys_path = repo_root / "01-system" / "configs" / "apis" / "API-Keys.md"
    output_base = repo_root / "03-outputs" / "gemini-api"
    run_id = args.output_name or datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    run_dir = output_base / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    prompt_path = run_dir / "prompt.txt"
    response_path = run_dir / "response.txt"
    meta_path = run_dir / "meta.json"

    save_text(prompt_path, args.prompt)

    try:
        api_key = read_api_key(api_keys_path)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(args.model)
        resp = model.generate_content(args.prompt)
        text = resp.text or ""
        save_text(response_path, text)
        meta = {
            "model": args.model,
            "prompt_path": str(prompt_path),
            "response_path": str(response_path),
            "run_id": run_id,
            "finish_reason": getattr(resp, "finish_reason", None),
        }
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Run saved to {run_dir}")
        return 0
    except Exception as exc:  # pylint: disable=broad-except
        error_msg = f"Gemini call failed: {exc}"
        save_text(response_path, error_msg)
        print(error_msg, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
