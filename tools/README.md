## Local Tools

Store reusable helper scripts here so cross-session workflows stay consistent. Each script should:

- Assume it is executed from the repository root (or derive the root from `Split-Path $PSScriptRoot`).
- Write any durable artifacts to `03-outputs/<tool>/...`.
- Remain dependency-light; prefer stock PowerShell + already-approved CLIs (e.g., `gemini`).

Current utilities:

- `gemini-run.ps1`: Wrapper that formats a Gemini CLI prompt, executes it, and captures prompt/response logs per run.

Add new helpers alongside README updates so AGENTS.md and docs can reference them.
