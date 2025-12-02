# videomachine_agent_prompt 使用說明

生成 VideoMachine Agent 的 /auto 提示詞，涵蓋 60 秒腳本、14 鏡頭分鏡、BGM/標題/縮圖 Prompt、金句、CTA，輸出到 `03-outputs/videomachine-agent/<run-id>/prompt.txt`。

## 前置需求
- Python 3.11+（內建 tomllib）
- `VideoMachine-Agent.toml` 應位於 repo 根目錄

## 指令範例
```pwsh
.\.venv\Scripts\python.exe 01-system/tools/ops/videomachine_agent_prompt.py --topic "走出內耗的 3 個步驟"
# 可用 --run-id 指定輸出子目錄（預設時間戳）
```

## 輸出
- `03-outputs/videomachine-agent/<run-id>/prompt.txt`

## 注意
- 工具只產生提示詞，不直接呼叫模型。
- 產出內容強制繁體中文、卡卡語氣，避免模板與雞湯。
