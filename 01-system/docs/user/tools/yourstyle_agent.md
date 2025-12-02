# yourstyle_agent_prompt 使用說明

生成 YourStyle 內容 Agent 的提示詞（/video、/long、/title、/matrix、/quote、/ideas、/persona），輸出到 `03-outputs/yourstyle-agent/<run-id>/prompt.txt`，再貼給你慣用的模型即可。

## 前置需求
- Python 3.11+（內建 tomllib）
- `YourStyle-Agent.toml` 應位於 repo 根目錄

## 指令範例
```pwsh
.\.venv\Scripts\python.exe 01-system/tools/ops/yourstyle_agent_prompt.py --mode video --topic "自我懷疑怎麼辦"
# ideas 模式可加 --count 20
# 可用 --run-id 指定輸出子目錄（預設時間戳）
```

## 輸出
- `03-outputs/yourstyle-agent/<run-id>/prompt.txt`

## 注意
- 工具只產生提示詞，不直接呼叫模型。
- 產出內容會強制繁體中文、卡卡語氣，避免雞湯與模板話術。
