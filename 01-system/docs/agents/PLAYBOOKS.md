# Playbooks

Document common intents here using the Lean playbook format (phrase -> intent -> steps -> outputs under `03-outputs/<tool>/`).

## Playbook: Answer In Traditional Chinese
- **Phrases / Aliases**: "respond in Chinese", "use Traditional Chinese", "all future replies must be Chinese" (and zh-TW equivalents like「之後回覆都用中文」)。
- **Intent**: Once triggered, keep all future responses in Traditional Chinese until the user explicitly changes the preference.
- **Steps**:
  1. Detect when the user asks for replies in Chinese (any phrasing similar to the aliases above).
  2. Switch immediately to Traditional Chinese for all subsequent outputs.
  3. Continue responding in Traditional Chinese until the user specifies another language.
- **Outputs**: No filesystem artifact; conversational commitment only.
## Playbook: Gemini Large-Scale Overview
- **Phrases / Aliases**: "give me an overview with Gemini", "summarize the whole repo", "use Gemini CLI for architecture"
- **Intent**: Capture a macro-level summary of one or more directories/files that exceed in-context limits.
- **Steps**:
  1. Confirm scope (directories/files) and expected focus (architecture, dependencies, etc.).
  2. From repo root, run `pwsh tools/gemini-run.ps1 -Targets <paths> -Query "<prompt>" [-Model <override>]`.
  3. Inspect `response.txt` for the generated summary; relay key findings referencing the log path.
- **Outputs**: `03-outputs/gemini-cli/<run-id>/response.txt`

## Playbook: Gemini Implementation Audit
- **Phrases / Aliases**: "check if <feature> exists", "verify auth via Gemini", "Gemini security review"
- **Intent**: Use Gemini CLI to verify whether a specific implementation (feature, pattern, safeguard) exists across modules.
- **Steps**:
  1. Gather specific feature criteria plus target directories (e.g., `@src/ @api/`).
  2. Execute `pwsh tools/gemini-run.ps1 -Targets <paths> -Query "Has <feature>? Show files/functions"` and capture the log.
  3. Summarize Gemini's findings, cite file paths, and note any follow-up manual inspections.
- **Outputs**: `03-outputs/gemini-cli/<run-id>/response.txt`
