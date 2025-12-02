# videomachine_agent_prompt

產生 VideoMachine Agent 用的完整短影片製作包提示詞（/auto），寫入 `03-outputs/videomachine-agent/<run-id>/prompt.txt`，方便貼給 LLM。依賴 `VideoMachine-Agent.toml` 說明。

## 依賴
- Python 3.11+（內建 `tomllib`）
- `VideoMachine-Agent.toml`（放在 repo 根目錄）

## 用法
```pwsh
.\.venv\Scripts\python.exe 01-system/tools/ops/videomachine_agent_prompt.py --topic "走出內耗的 3 個步驟"
# 可用 --run-id 自訂輸出目錄名稱；預設時間戳
```

## 輸出
- `03-outputs/videomachine-agent/<run-id>/prompt.txt`
  - 包含 60 秒腳本節奏、14 鏡頭分鏡框架、BGM/標題/縮圖 Prompt/金句/CTA 任務描述

## 注意
- 僅生成提示詞，不直接呼叫 LLM；將 prompt.txt 貼給你慣用的模型即可。
