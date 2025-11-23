# 核心模組：Gemini API 介面 (gemini)

## 用途

此工具不是一個可以直接執行的腳本，而是一個核心的 Python 程式庫模組。它的主要目的是提供一個統一、簡單的介面，讓其他工具（例如 `lecture_handout_pipeline`）可以方便地呼叫 Google 的 Gemini AI 模型來完成需要 AI 協助的任務，例如內容總結、文字潤飾、格式轉換等。

## 使用方式 (供開發者參考)

這個模組中的主要函式是 `generate_text`。

### 導入模組

在另一個工具腳本中，可以這樣導入：

```python
from tools.llms.gemini.gemini import generate_text
```

### 呼叫函式

傳遞一個文字提示（prompt），即可獲得 Gemini 模型的回應。

```python
# 建立一個提示
my_prompt = "請幫我將這段文字總結成三個重點：[此處貼上很長的文字]"

# 呼叫函式並取得結果
summary = generate_text(my_prompt)

# 打印結果
print(summary)
```

## API 金鑰設定

此模組會自動遵循專案規範，從 `01-system/configs/apis/API-Keys.md` 檔案中讀取 `GEMINI_API_KEY`。您只需確保該檔案中有正確的金鑰即可。
