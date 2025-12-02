# yourstyle_agent_prompt

產生 YourStyle 內容 Agent 的提示詞（/video、/long、/title、/matrix、/quote、/ideas、/persona），寫入 `03-outputs/yourstyle-agent/<run-id>/prompt.txt`，方便再貼給 LLM 執行創作。依賴 `YourStyle-Agent.toml` 說明。

## 依賴
- Python 3.11+（內建 `tomllib`）
- `YourStyle-Agent.toml`（放在 repo 根目錄）

## 用法
```pwsh
.\.venv\Scripts\python.exe 01-system/tools/ops/yourstyle_agent_prompt.py --mode video --topic "自我懷疑怎麼辦"
# 更多模式：video|long|title|matrix|quote|ideas|persona
# ideas 模式可加 --count 20
# 可用 --run-id 自訂輸出目錄名稱；預設時間戳
```

## 輸出
- `03-outputs/yourstyle-agent/<run-id>/prompt.txt`
  - 包含卡卡語氣要求、60 秒節奏/長稿/標題/矩陣/金句/點子/人設任務描述

## 注意
- 僅生成提示詞，不直接呼叫 LLM；將 prompt.txt 貼給你慣用的模型即可。
