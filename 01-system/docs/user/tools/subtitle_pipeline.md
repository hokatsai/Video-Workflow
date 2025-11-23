# 工具：AI 字幕完整處理流程 (subtitle_pipeline)

## 用途

此工具是一個總调度器，旨在全自動化地改善字幕品質。它會依序執行兩個步驟：
1.  **校對 (Correction)**：首先調用 `subtitle_corrector` 工具，修正字幕中的拼寫、文法和標點錯誤。
2.  **精煉 (Refinement)**：接著，將校對後的字幕傳遞給 `subtitle_line_refiner` 工具，進一步優化其句式、風格和可讀性。

最終，您會得到一個既準確又流暢的高品質字幕檔案。

## 使用方式

您只需提供原始字幕檔和最終輸出路徑即可啟動整個流程。也可以選擇性地為校對和精煉兩個環節提供自訂的 AI 指令。

### 指令範例

```bash
# 使用預設的 AI 提示詞執行完整字幕處理流程
python 01-system/tools/ops/subtitle_pipeline.py "原始字幕.srt" "最終輸出的字幕.srt"

# 為校對和精煉環節分別提供自訂的提示詞
python 01-system/tools/ops/subtitle_pipeline.py "原始字幕.srt" "最終輸出的字幕.srt" --corrector_prompt "校對風格.txt" --refiner_prompt "精煉風格.txt"
```

### 參數說明

*   `input_file` (必須): 來源的原始 `.srt` 字幕檔案的完整路徑。
*   `output_file` (必須): 您希望保存最終成品字幕檔案的完整路徑。
*   `--corrector_prompt` (可選): 為“校對”步驟提供自訂提示詞的檔案路徑。
*   `--refiner_prompt` (可選): 為“精煉”步驟提供自訂提示詞的檔案路徑。
