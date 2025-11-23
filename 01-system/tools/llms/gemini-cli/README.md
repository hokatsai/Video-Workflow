## Gemini CLI Wrapper

**Category:** llms  
**Binary:** `gemini` (pre-installed per user)  
**Artifacts:** `03-outputs/gemini-cli/<run-id>/`

### Purpose
- Provide a sanctioned interface for Gemini CLI when analyzing large workspaces.
- Capture every invocation's prompt/response for reproducibility.
- Keep helper automations (e.g., `01-system/tools/llms/gemini-cli/gemini-run.ps1`) discoverable and documented.

### Usage Patterns
1. **Ad-hoc CLI:**  
   Run from repo root using @-style paths, e.g.  
   ```powershell
   gemini "@src/ @tests/ Summarize architecture and test focus"
   ```
2. **Logged Runs via Script:**  
   ```powershell
   pwsh 01-system/tools/llms/gemini-cli/gemini-run.ps1 -Targets @('AGENTS.md','01-system/docs/agents/') `
       -Query 'Compare agent runtime rules with supporting docs' `
       -Model 'gemini-1.5-pro'
   ```
   - Stores prompt/response under `03-outputs/gemini-cli/<timestamp>/`.
   - Returns a hashtable with locations for downstream scripts.

### Notes
- Always execute from repo root so @ paths stay correct.
- Keep prompts specific to minimize tokens and ensure actionable answers.
- For multi-run workflows, mirror summaries to `SYSTEM_MEMORY.md` per Lean Logflow triggers.
