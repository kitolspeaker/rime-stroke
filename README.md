# 六鍵筆畫 for Windows Rime（Apple 風格實驗版）

這是 [rime-stroke](https://github.com/rime/rime-stroke) 的個人 fork。**原有 `stroke.schema.yaml` 和 `stroke.dict.yaml` 保持不變**；新增 `stroke_apple.schema.yaml`，使用相同詞庫提供 Apple 風格六鍵輸入。

> 目標是接近 macOS／iPhone 繁體筆畫的操作方式；不是 Apple 官方輸入法、沒有 Apple 私有詞庫，候選順序及所有模式**不會完全一致**。

## Windows 小狼毫安裝（不必寫程式）

1. 開啟 [本倉庫的 `stroke_apple.schema.yaml`](stroke_apple.schema.yaml)，按 **Raw** 下載。
2. 開啟 Windows 的 `%APPDATA%\Rime` 資料夾，放入 `stroke_apple.schema.yaml`。若未有 `stroke.dict.yaml`，亦需從本倉庫下載 [詞庫](stroke.dict.yaml) 放入同一資料夾（**無須修改原詞庫**）。
3. 右鍵小狼毫圖示 →「輸入法設定」→ 勾選 **蘋果式六鍵筆畫（實驗）**。如果未出現，先選「重新部署」再返回輸入法設定。
4. 按 `Win + Space` 揀小狼毫，按 `F4` 切換到新方案。修改檔案後需要重新部署。

> 本方案保留原 `stroke`，可隨時切換返「五筆畫」。拼音反查需要預裝 `luna_pinyin`，與原上游方案相同。繁體轉換使用 Rime/OpenCC 的 `s2t.json`。

## 六個按鍵

| 筆畫 | 實體鍵盤 | 數字小鍵盤 |
|---|---|---|
| 一 橫 | J | 1 |
| 丨 豎 | K | 2 |
| 丿 撇 | L | 3 |
| 丶 點／捺 | U | 4 |
| 乛 折 | I | 5 |
| ＊ 萬用筆畫 | O | 6 |

打完筆畫後用 **Space** 選第一候選；數字鍵可以選其他候選。Backspace 刪除最後一筆。數字 **1–6 是數字小鍵盤**，主鍵盤上方的數字鍵仍用於選字。

## 與原 rime-stroke 不同的地方

- 不再要求記住 `h s p n z`；這個新方案直接接受 `J K L U I`，按 `O` 可以代替未知的一個筆畫。
- 以完整筆順為基礎；**多於五筆**的字額外產生「前四筆＋最後一筆」五碼別名（不會關閉完整筆順，兩種編碼並存）。
- 第 1–5 筆可有多個 `O`；第 6–32 筆只能單獨有一個 `O`，且不可和前面其他 `O` 混用。這是為控制 Rime 拼寫索引體積而設的限制，**並非 Apple 完整萬用鍵行為**。
- 使用 OpenCC 把常見簡體候選轉成繁體，並去掉重複候選。OpenCC 的字形轉換不等同完整香港正字校訂。
- 保留 Rime 詞庫及個人詞頻學習；**不會複製 iPhone / macOS 候選字的先後次序**。

## 實際狀態及後續

目前提供可部署的 Rime schema；未喺 Windows 小狼毫進行端到端測試。測試步驟、限制與 Apple 差異見 [驗收清單](docs/APPLE_STROKE_TESTING.md)。

後續如要更接近 iPhone，可比對 iPhone 的候選字截圖與同碼排序，再獨立調整繁體詞庫。避免直接複製 Apple 私有資源。

原始項目及版權：請參閱 [上游](https://github.com/rime/rime-stroke) 與本倉庫 [LICENSE](LICENSE)。
