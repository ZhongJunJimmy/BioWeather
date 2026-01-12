# BioWeather

BioWeather 是一個結合即時天氣與個人化體感偏好的「個人化穿衣與生活建議」小工具，主要針對台灣主要縣市，利用 Open-Meteo 取得天氣資料，再透過 LLM（支援 Google Gemini 或本機 Ollama）產生自然、可執行的建議。

**主要功能**
- 取得指定城市即時天氣（使用 Open-Meteo）。
- 根據使用者在 `data/userData.json` 的偏好（耐寒/耐熱/風敏感/濕度敏感）計算體感分類。
- 使用 LLM（Gemini 或 Ollama）將天氣與個人化決策 schema 轉成生活化建議。
- 支援 CLI 互動問卷與簡易的 FastAPI 範例路由。

**重點檔案**
- `main.py`：程式進入點，包含 CLI 問卷流程與可啟動的 FastAPI 範例路由。
- `requirements.txt`：專案相依套件。
- `config.json`：LLM 設定（`llm_provider`、模型名稱等）。
- `data/system_prompt.txt`：系統提示（system prompt），用於引導模型回應格式與內容。
- `data/userData.json`：使用者偏好資料（程式會在不存在時建立）。
- `src/user.py`：互動式問卷與使用者偏好建構。
- `src/utils.py`：城市經緯度、體感分級與 decision schema 建構邏輯。
- `src/weather_api.py`：呼叫 Open-Meteo，回傳整理後的氣象欄位（temperature/feels_like/humidity/wind_speed/precipitation）。
- `src/ai_service.py`：LLM 呼叫封裝（支援 `google-genai` 與 `ollama`），包含重試與本地 fallback。

**環境與相依性**
- Python 3.8+
- 主要相依請見 `requirements.txt`（包含 `google-genai`, `requests`, `python-dotenv`, `ollama`, `fastapi`, `uvicorn`）。

安裝建議：
```bash
python -m venv .venv
.\
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**設定**
- 編輯 `config.json` 以選擇 LLM 供應商與模型：

```json
{
  "llm_provider": "ollama",
  "ollama_model": "gemma3:4b",
  "gemini_model": "gemini-2.5-flash"
}
```

- 若使用 Gemini，請在根目錄建立 `.env` 並設定 `GEMINI_API_KEY`。
- 若使用 Ollama，請確保本機已安裝並啟動 Ollama daemon，且模型已下載。

**使用方式**
1. CLI（互動式）

```bash
python main.py
```

流程：
- 若 `data/userData.json` 不存在，程式會以互動式問卷建立個人化檔案。
- 選擇城市後呼叫 Open-Meteo 獲取天氣，並根據偏好建構 decision schema。
- 根據 `config.json` 決定呼叫 Gemini 或 Ollama，最後在終端輸出建議。

2. FastAPI 範例（啟動 API 伺服器）

```bash
uvicorn main:app --reload --port 8000
```

Endpoint 範例：GET `/getBioWeatherAdvice/{city_id}` 回傳 LLM 產生的建議。

**自訂與延伸**
- 新增或修改城市：編輯 `src/utils.py` 中的 `city_map`。
- 調整系統提示：編輯 `data/system_prompt.txt`（或 `src/ai_service.py` 的載入路徑）。
- 調整重試策略或生成參數：編輯 `src/ai_service.py` 的對應設定。

**除錯建議**
- 若遇到網路或 API 錯誤，先確認電腦能夠存取 `https://api.open-meteo.com`。
- 若使用 Gemini，請檢查 `.env` 中的 `GEMINI_API_KEY` 是否正確。
- 使用 Ollama 時，確認 Ollama daemon 正常執行並且模型名稱與 `config.json` 相符。


**授權**
- 採用專案根目錄的 `LICENSE` 條款。


