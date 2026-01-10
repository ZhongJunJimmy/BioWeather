# BioWeather

一個基於天氣資料與個人化體感偏好的「個人化穿衣建議」小工具。

主要功能：取得當前城市天氣（使用 Open-Meteo 公開 API）並結合使用者的體感偏好，透過 Google Gemini（透過 `google-genai` 套件）產生簡短、生活化的穿衣建議。

**目標使用者**：想要每天快速知道「今天該怎麼穿」的使用者，特別適合台灣主要縣市的查詢。

---

**特色**

- 結合即時天氣與使用者偏好，給出單一明確的穿衣建議。
- 使用 Open-Meteo（無需金鑰）取得氣象資料。
- 使用 Google Gemini（需設定 API Key）生成自然、精簡的建議文字。

---

**環境與相依性**

- Python 3.8+
- 主要套件（見 `requirements.txt`）:
	- `google-genai`
	- `requests`
	- `python-dotenv`
	- `ollama` (僅在使用本地 Ollama 時需要)

---

**安裝**

1. 取得程式碼：

```bash
git clone git@github.com:ZhongJunJimmy/BioWeather.git
cd BioWeather
```

2. 建議建立虛擬環境並安裝相依：

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
pip install -r requirements.txt
```

3. 若要使用 Gemini（AI 產生穿衣建議），請在根目錄建立一個 `.env`，並加入 Gemin API 金鑰環境變數（範例）：

```
GEMINI_API_KEY=your_gemini_api_key_here
```

（程式會透過 `python-dotenv` 載入 `.env`）

注意：Open-Meteo API 為公開資料來源，不需 API Key。

---

**設定 LLM 供應商（可選：Gemini 或 本地 Ollama）**

本專案現在支援兩種 LLM 執行方式：

- 使用遠端 Google Gemini（需要在 `.env` 設定 `GEMINI_API_KEY`）。
- 使用本機 Ollama（需在系統安裝並執行 Ollama daemon，並確保指定模型已下載）。

設定方式請編輯 `config.json`（專案根目錄），範例：

```json
{
	"llm_provider": "gemini",        
	"ollama_model": "llama3.2",
	"gemini_model": "gemini-2.5-flash"
}
```

- 將 `llm_provider` 設為 `gemini` 或 `ollama`，程式會依此決定呼叫哪個後端。
- 若使用 `ollama`，請確保本機 Ollama 可用，且 `ollama_model` 填寫正確模型名稱。

程式啟動時會輸出目前使用的 LLM 供應商，例如：`使用 LLM 供應商: gemini`。

---

**注意：system prompt 存放位置**

系統提示（system prompt）已從程式內文移出，改為放在 `data/system_prompt.txt`，可直接編輯該檔以調整模型指令。

---

**快速執行**

執行主程式：

```bash
python main.py
```

流程說明：
- 若 `data/userData.json` 不存在，程式會啟動一個簡短的體感偏好問卷（互動式輸入），並將結果儲存成 `data/userData.json`。
- 接著會要求選擇縣市（互動式輸入），取得對應經緯度並呼叫 Open-Meteo 取得當前天氣。
- 最後把天氣資料與使用者偏好送給 Gemini，輸出簡短的穿衣建議到終端機。

---

**檔案與程式說明（重點）**

- `main.py`：程式進入點，負責流程控制（載入用戶資料、選城市、取得天氣、呼叫 AI）。
- `requirements.txt`：相依套件。
- `data/userData.json`：儲存使用者的偏好分數與上次更新日（自動建立）。
- `src/user.py`：互動式問卷與使用者偏好格式化為 `coldTolerance/heatTolerance/windSensitivity/humiditySensitivity`。
- `src/utils.py`：內建台灣主要縣市經緯度，提供互動式選單給使用者選擇查詢城市。
- `src/weather_api.py`：呼叫 Open-Meteo 取得即時天氣並回傳整理過的 JSON。
- `src/ai_service.py`：封裝 Gemini（`google-genai`）的呼叫與重試邏輯，並包含系統提示（系統提示會指示模型產出穿衣建議的格式與限制）。

---

**使用者自訂與調整**

- 若想修改城市或加入更多城市，可編輯 `src/utils.py` 的 `city_map`。
- 若要調整 AI 提示（語氣、回覆長度、規則等），請修改 `src/ai_service.py` 中的 `SYSTEM_PROMPT`。

---

**除錯與開發**

- 若遇到 Gemini API 呼叫失敗，程式會依錯誤類型進行重試（內建最大重試次數）。可在 `src/ai_service.py` 調整 `max_retries` 與 `delay`。
- 若想快速測試而不用呼叫 Gemini，可在 `main.py` 暫時替換 `generate_content_with_retry` 的呼叫，或在 `ai_service.py` 模擬回傳值。

---

**貢獻**

歡迎 fork、PR 與 issue。可能的改進方向：

- 支援更多地區（國際化）
- GUI 或行動裝置介面
- 更豐富的使用者設定（活動屬性、穿衣風格偏好）

---

**授權**

本專案採用 [LICENSE](LICENSE) 中的授權條款。

