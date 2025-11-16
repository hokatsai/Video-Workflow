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
