# Gemini API Reference (gemini-2.5-pro)

> 官方文件：https://ai.google.dev/gemini-api/docs

## 認證與端點
- 認證：`GEMINI_API_KEY`（query 參數 `?key=` 或 SDK 配置）。本專案在 `01-system/configs/apis/API-Keys.md` 取用。
- REST 端點範例：`POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key=$GEMINI_API_KEY`
- 請求結構（最小範例）：
  ```json
  {
    "contents": [{
      "parts": [{"text": "你的提示語"}]
    }]
  }
  ```
- 回應重點：`candidates[].content.parts[].text` 為主要文字輸出；`promptFeedback` 可能返回安全分數與封鎖原因。
- 常用選項：
  - `generationConfig.temperature`（0–1）控制隨機性。
  - `top_p`、`top_k` 控制採樣。
  - `max_output_tokens` 限制輸出長度。
  - `safetySettings` 可調整安全策略（預設嚴格）。

## Python SDK 範例（google-generativeai）
```python
import google.generativeai as genai

genai.configure(api_key="YOUR_KEY")
model = genai.GenerativeModel("gemini-2.5-pro")
resp = model.generate_content("寫一首讚美 Gemini 的唐詩")
print(resp.text)
```

## 使用須知
- 請在 repo root 下執行相關腳本，避免路徑錯置。
- 本倉庫提供 `01-system/tools/llms/gemini/gemini_api_tool.py` 作為 API 快捷呼叫，並自動讀取 `GEMINI_API_KEY`。
- 如遇 `429 / quota / safety` 錯誤，可調低長度或略降 temperature，必要時等待片刻再試。
