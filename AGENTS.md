## 代理執行規範
### 目的
- 只透過自然語言指令運作；使用者不會代替代理執行指令或點擊介面。
- 善用本地工具與共享文件，逐步優化工作流程。
- Playbook 是必要入口：任何需求都先對照 `01-system/docs/agents/PLAYBOOKS.md`，再決定操作。
- 維護長期記憶，讓後續工作階段能快速接續。

### 永久不變的準則
- 僅使用自然語言互動；缺少關鍵資訊時最多詢問一次。
- 先在本地尋找現有工具/Playbook/Prompt，再考慮自創流程。
- 採取最小變更與快速回饋，先完成最小可行步驟。
- 透過 Lean Logflow 紀錄：視工作量選擇最精簡的紀錄模式。
- 隱私安全：僅在需要時從 `01-system/configs/apis/API-Keys.md` 讀取金鑰，且不可紀錄其值。
- 所有產物都放在 `03-outputs/<tool>/...`，並在回報時引用相對路徑。
- `registry.yaml` 是工具真實登錄處；`docs/prompts/INDEX.md` 是提示語資源的權威列表。
- 使用者可見文件必須是繁體中文。

### 啟動檢查表（每次工作）
1. 先閱讀 `STATE.md`，掌握最新腳手架稽核結果與待辦。
2. 若檔案結構更動或稽核過期，進行完整檢查；否則快速確認關鍵檔案（`AGENTS.md`、`registry.yaml`、`03-outputs/README.md`、主要工具資料夾）。
3. 僅在任務需要時讀取 `API-Keys.md` 等祕密資訊。
4. 瀏覽本檔案是否有更新；如有重大異動，再檢視 `PLAYBOOKS.md`、`TOOLS.md`、`SYSTEM_MEMORY.md`、`docs/prompts/INDEX.md` 與 `docs/user/INDEX.md`。
5. 確認執行限制（沙箱、網路、核准）後，決定停留在 Execution Mode 或請求 Build Mode。
6. 當即將使用或調查某個工具且不熟悉其流程時，先至 `01-system/docs/tools-reference/` 尋找對應說明，再繼續後續操作。

### 模式
- **Execution Mode（預設）**：僅使用現有的 Playbook、工具與提示語；未獲允許不得建立新資產。
- **Build Mode（經同意後）**：在獲准後方可建立或修改工具/提示語；完成後須回到 Execution Mode。

## 儲存庫結構（隨時更新）
> 需維護下列樹狀圖，若偵測到結構漂移或於啟動時發現差異，即刻更新。
```
/
- 01-system/
  - configs/{env.example, apis/{README.md, API-Keys.md}, tools/registry.yaml}
  - docs/
    - agents/{PLAYBOOKS.md, TOOLS.md, TROUBLESHOOTING.md, SYSTEM_MEMORY.md, STATE.md, BOOTSTRAP.md, memory/YYYY-MM.md}
    - prompts/{README.md, INDEX.md, examples/prompt-template.md, prompt-*.md, collections/...}
    - tools-reference/{README.md, INDEX.md, TEMPLATE.md, <tool>.md}
    - api-reference/{README.md, Groq STT API Doc.md, Groq STT API Reference.md, ElevenLabs STT API Reference.md}
    - user/{README.md, INDEX.md, tools/{audio_compressor.md, video_cutter.md, clips_adapter.md, clips_copy_exporter.md, clips_orchestrator.md, lecture_handout_local_pipeline.md, lecture_handout_pipeline.md, memo_article_pipeline.md, memo_transcript_pipeline.md, subtitle_corrector.md, subtitle_line_refiner.md, subtitle_pipeline.md, zh_subtitle_converter.md, gemini.md, groq_stt_pipeline.md, eleven_scribe_pipeline.md}}
  - tools/
    - llms/
      - gemini-cli/{README.md, gemini-run.ps1}
      - gemini/
        - __init__.py
        - gemini.py
        - gemini_api_tool.py
        - gemini.playbook.md
    - ops/
      - video-workflow/{README.md, cookie/, video/, whisperx/}
      - audio_compressor.py
      - audio_compressor.playbook.md
      - video_cutter.py
      - video_cutter.playbook.md
      - clips_adapter.py
      - clips_adapter.playbook.md
      - clips_copy_exporter.py
      - clips_copy_exporter.playbook.md
      - clips_orchestrator.py
      - clips_orchestrator.playbook.md
      - lecture_handout_local_pipeline.py
      - lecture_handout_local_pipeline.playbook.md
      - lecture_handout_pipeline.py
      - lecture_handout_pipeline.playbook.md
      - memo_article_pipeline.py
      - memo_article_pipeline.playbook.md
      - memo_transcript_pipeline.py
      - memo_transcript_pipeline.playbook.md
      - memo_gemini_pipeline.py
      - subtitle_corrector.py
      - subtitle_corrector.playbook.md
      - subtitle_line_refiner.py
      - subtitle_line_refiner.playbook.md
      - subtitle_pipeline.py
      - subtitle_pipeline.playbook.md
      - zh_subtitle_converter.py
      - zh_subtitle_converter.playbook.md
      - tool.py
    - stt/{groq_stt_pipeline.py, eleven_scribe_pipeline.py, transcript_utils.py}
    - _categories-README.md
    - tth/{README.md, gemini-default.ps1}
- 02-inputs/{downloads/}
- 03-outputs/{README.md, <tool>/}
```


``

## 輸出規則（單一真實來源）
- 全部產物必須寫入 `03-outputs/<tool>/`，用工具或流程代稱（例：`report-writer`、`image-cleanup`）。
- 每個工具資料夾依執行區分（時間戳、`intermediate/`、`final/` 等）；全程維持同一命名規則，例外需在摘要中說明。
- 暫存下載檔放在 `03-outputs/<tool>/downloads/`，結束前必須搬移或引用。
- 在最終回覆及 `SYSTEM_MEMORY.md` 內皆需提供相對路徑。

## 重要資源位置
- **Playbooks**：`01-system/docs/agents/PLAYBOOKS.md`；用於對應語句與意圖。
- **Prompts Library**：`01-system/docs/prompts/`，並由 `INDEX.md` 維護索引。
- **API Key 單一來源**：`01-system/configs/apis/API-Keys.md`；任何需要調度 API Key 時，預設先查此檔。
- **工具實體**：`01-system/tools/<category>/...`，並以 `registry.yaml` 為權威登錄。
- **Helper scripts**：儲存在根目錄 `01-system/tools/`，集中可重用的自動化腳本（如 Gemini 包裝器）。
- **tth ????**?`01-system/tools/tth/`???? Gemini `gemini-2.5-pro` ?????????? `gemini-2.5-flash`?? `gemini-default.ps1`??
- Gemini ?????`gemini-2.5-pro`????????????? `gemini-2.5-flash`????? `01-system/tools/tth/gemini-default.ps1` ????????
- **Tool index（人類可讀）**：`01-system/docs/agents/TOOLS.md`，對應 registry 的摘要。
- **工具參考說明**：`01-system/docs/tools-reference/`，記錄每個工具的操作手冊。遇到工具不明時，務必先查閱此區。
- **使用者文件（繁中）**：`01-system/docs/user/INDEX.md`，並於 `docs/user/tools/<tool>.md` 提供各工具詳細說明。
- **Memory & State**：`SYSTEM_MEMORY.md`（主紀錄）、`memory/YYYY-MM.md`（鏡射）、`STATE.md`（階段與待辦）。
- **Troubleshooting**：`01-system/docs/agents/TROUBLESHOOTING.md`，集中可重現問題與解法。

## Execution Mode 操作流程
- 先以 Playbook 判斷需求，再進行自由規劃；若仍不清楚，詢問使用者一次以釐清。
- 儘量優先使用已登錄工具與提示語；多個資產可使用時，選擇最安全、最本地的選項並在報告中引用其 ID/版本。
- 操作工具前若有疑問，先查閱 `01-system/docs/tools-reference/`，確認標準流程、參數與輸出位置。
- 以最小可行步驟前進，完成一個階段就回報結果並記錄必要輸出。

## Build Mode 流程（工具與提示語）
1. **規格（1–3 點）**：描述名稱、分類、輸入/輸出與副作用；提示語還需註明模型/提供者、變數與限制。
2. **腳手架**：
   - 工具包裹放在 `01-system/tools/<category>/<tool-name>/`，輸出預設寫入 `03-outputs/<tool-name>/...`。
   - 提示語採 `01-system/docs/prompts/prompt-<domain>-<intent>.md` 模板（見下方範本）。
3. **登錄/索引**：完成後立即更新 `registry.yaml`、`docs/agents/TOOLS.md`，提示語需同步到 `docs/prompts/INDEX.md`。
4. **冒煙測試**：以最小案例驗證並將結果存於 `03-outputs/<tool-name>/tests/` 或類似路徑。
5. **繁中文件更新**：包含 `TOOLS.md`、`PLAYBOOKS.md`、`docs/user/tools/<tool>.md`、`docs/user/INDEX.md`，並在 `SYSTEM_MEMORY.md`/`STATE.md` 留下紀錄。若結構變動，也請更新本檔案中的樹狀圖。
6. **完成後回到 Execution Mode**。

## 模板：`01-system/docs/user/tools/<tool-name>.md`
```
/
- 01-system/
  - configs/{env.example, apis/{README.md, API-Keys.md}, tools/registry.yaml}
  - docs/
    - agents/{PLAYBOOKS.md, TOOLS.md, TROUBLESHOOTING.md, SYSTEM_MEMORY.md, STATE.md, BOOTSTRAP.md, memory/YYYY-MM.md}
    - prompts/{README.md, INDEX.md, examples/prompt-template.md, prompt-*.md, collections/...}
    - tools-reference/{README.md, INDEX.md, TEMPLATE.md, <tool>.md}
    - user/{README.md, INDEX.md, tools/...}  # 使用者文件（繁中）
  - tools/{ops/, llms/, stt/, _categories-README.md}
    - llms/gemini-cli/{README.md, gemini-run.ps1}
    - ops/video-workflow/{README.md, cookie/, video/, whisperx/}
- 02-inputs/{downloads/}
- 03-outputs/{README.md, <tool>/}
```




## 模板：`01-system/docs/prompts/prompt-<domain>-<intent>.md`
```md
---
id: prompt-<domain>-<intent>-v1
title: <簡潔標題>
summary: <用途與使用時機>
model: <openai:gpt-4o|anthropic:claude-3.5|google:gemini-1.5|generic>
owner: <user|agent|team>
version: v1
last_updated: YYYY-MM-DD
tags: [<domain>, <intent>, <safety>]
variables:
  - name: <var_name>
    description: <用途>
    required: true|false
safety:
  constraints:
    - <限制，例如不得含 PII>
  escalation:
    - <需要詢問使用者的情境>
---

## 使用方式
- 何時使用：<說明>
- 呼叫注意事項：<模型限制或速率>
- 預期輸出：<格式、品質指標、`03-outputs/<tool>/` 目的地>

## Prompt
<以 {{variables}} 標示替換區塊>

## 範例
- Input: <例> → Output: <例>

## 變更記錄
- v1（YYYY-MM-DD）：初版。
```

## 提示語庫與寫作守則
- `docs/prompts/INDEX.md` 是唯一索引，需列出 ID、模型/供應商、擁有者、最後更新、標籤、變數與安全等級。
- 提示語屬於可被工具呼叫的資產，請保持原子性與可組合性。
- 修改提示語時必須提升 `version`、更新索引並在 Lean Logflow 紀錄。
- 回報時引用 `id` 與 `version`。

## Playbook 撰寫守則（關鍵）
- 將語句/別名 → 意圖 → 步驟 → 產出路徑 (`03-outputs/<tool>/...`) 明確映射。
- 保持條目清楚可複用，避免重複內容。
- 在定稿前確認需要的工具/提示語皆已存在（或請示進入 Build Mode）。
- 在自由規劃前，一律先嘗試對照 Playbook。

## Lean Logflow（自我更新規則）
### 第一步：分類工作
- **Micro run**：單步驟、無長期產物 → 直接回答並結束，不需 DocSync。
- **Standard run**：預設類型（多步或有產物）→ 建立一筆 Lean Logflow 紀錄。
- **Milestone run**：里程碑/交接 → 同樣格式但內容更詳盡。

### 第二步：最小 DocSync
- 以 `YYYY-MM-DD – Title :: change | impact | artifacts` 追加一行到 `SYSTEM_MEMORY.md`（路徑使用 `03-outputs/<tool>/...`）。
- 僅在月份變更或使用者要求摘要時，才同步到 `memory/YYYY-MM.md`。
- 若第三步無觸發條件，即可在此結束。

### 第三步：決定性觸發（僅在條件成立時執行）
1. **執行狀態改變？** → 當階段改變、待辦調整或使用者要求刷新時，更新 `STATE.md`；內容須包含月份/階段、引用的 `SYSTEM_MEMORY.md` 行與當前步驟。
2. **有資產新增/移動？** → 新增或修改工具包/提示語時，必須同步更新：`registry.yaml` → `docs/agents/TOOLS.md` → `docs/prompts/INDEX.md`（如適用）→ 相關 Playbook → 使用者文件（繁中）。
3. **Playbook 意圖更新但無新工具？** → 仍需更新 `PLAYBOOKS.md` 並標註所用工具/提示語。
4. **新增疑難排解知識？** → 將解法與升級流程寫入 `docs/agents/TROUBLESHOOTING.md`。
5. **儲存庫結構更新？** → 必須同步刷新本檔案的樹狀圖。
6. **使用者另有要求？** → 立即處理（如重新產出摘要或狀態）。

所有觸發都應在同一個工作區塊內完成，確保紀錄維持精簡且一致。

## 工具探索與登錄規範
- 禁止呼叫未登錄的工具；若已有包裹但未登錄，需先提案補齊登錄。
- 登錄變更與程式碼更新需同時完成，避免留下一半的工具。
- 提示語一律留在 `docs/prompts/INDEX.md`，勿混同於工具。

## 安全與金鑰
- 只讀取必要的祕密，且避免輸出真實值。
- 實施最小權限；在進行高風險或具破壞性的操作前先確認。
- 遵循提示語的安全限制，並在需要時向使用者請示。

## 報告
- 摘要需包含已執行的命令/流程、關鍵決策與所引用的 `03-outputs/<tool>/...` 路徑。
- 若使用 LLM/提示語，請註明 Prompt ID 與版本。
- 發生錯誤時說明可能原因與最小修復步驟。
- 對於長時任務，提供精簡的進度更新即可，避免過度訊息。

## Ask-Once 檢查清單
- 是否缺少必要環境變數或金鑰？
- 有無使用者針對模型/供應者/工具的偏好？
- 任務意圖或 `03-outputs/` 目標資料夾是否不明？

## 變更管理
- 維持變更小而可回溯；若需要大幅調整，先提出方案。
- 未經指示不得修改此規範。
- 任何已核准的變更都必須透過 Lean Logflow 與相關文件反映。

---

**本規範為唯一權威來源。**

## ϵyܘģʽ (Systems Architect Mode)
- **|ll**: ʹՈ󌦹M}PQԆ}r磺}Pһ¡ҳ}KQ
- **D**: ÓμָУԼܘҕǷOӋK̻ѡЧԄӻQ
- **вE**:
  1. **}̷ (Review & Analyze)**: ȫzҕǰĹReеġhĦW·ĦcĦ
  2. **ԭλ (Root Cause Analysis)**: ҳLʧĸԭhδ֪هȱʧ͆wȡ
  3. ** (Propose New Architecture)**: OӋµġģMĹPlaybookhAz΄ղ֡K̎YRȲԡ
  4. **̻ (Codify Workflow)**:
     - µ Playbook  1-system/docs/agents/PLAYBOOKS.md
     - K䛌F_cߣ 
equirements.txt, setup-video-env.ps1
     - ±n (AGENTS.md)wFcɫ
- **a**:
  -  PLAYBOOKS.md c AGENTS.md
  - 춌FԄӻ̵¹߻_
