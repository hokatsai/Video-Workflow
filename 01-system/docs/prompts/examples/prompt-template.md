---
id: prompt-example-template-v1
title: Example Template
summary: Reference template for authoring new prompts.
model: generic
owner: agent
version: v1
last_updated: 2025-11-17
tags: [template]
variables:
  - name: sample_input
    description: Replace with the actual variable description.
    required: true
safety:
  constraints:
    - Follow project guardrails.
  escalation:
    - Ask for approval before destructive actions.
---

## Usage
- When to use: Use as a starting point for new prompts.
- Invocation notes: Update metadata before publishing.
- Expected outputs: Document the artifact path under `03-outputs/<tool>/`.

## Prompt
<Write the prompt body here.>

## Examples
- Input: <бн> б· Output: <бн>

## Change-log
- v1 (2025-11-17): Initial template stub.
