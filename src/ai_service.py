from google import genai
import os
import time
import json
import ollama

# read system prompt from file
SYSTEM_PROMPT_PATH = os.path.join(os.path.dirname(__file__), '..', './data/system_prompt.txt')
with open(SYSTEM_PROMPT_PATH, 'r', encoding='utf-8') as f:
    SYSTEM_PROMPT = f.read()

# SYSTEM_PROMPT = """
# 你是一位個人化穿衣建議助理。

# 系統將提供兩類資訊：
# 1. weather_data：描述當前環境的天氣條件
# 2. user_data：描述使用者對冷、熱、風與濕度的個人體感傾向
# 2.1 coldTolerance: 越小越怕冷
# 2.1 heatTolerance: 越大越怕熱
# 2.1 windSensitivity: 風對體感影響
# 2.1 humiditySensitivity: 濕度影響

# 你的任務是根據這些資訊，提供「今天應該怎麼穿」的實用建議。

# 請遵守以下規則：
# - 專注在穿衣褲建議本身，不要解釋數值或資料來源
# - 不要提及任何模型、參數名稱、計算方式或 AI 相關概念
# - 語氣自然、生活化，像是在提醒一位朋友
# - 不要給多個選項，請給出一個明確的主要建議
# - 依照參考的數據，給出今天可能會感受到的狀態
# - 若天氣條件偏嚴苛（例如風大、體感偏低），可補充一句保守提醒
# - 不要假設使用者的活動內容，除非資訊中有明確暗示

# 回覆格式限制：
# - 使用繁體中文
# - 回覆長度為 1～2 句
# - 第一句先給穿衣結論，後面提供簡短說明原因或可能的體感
# - 不使用條列、不使用表情符號、不使用專業術語
# """

def initial_gemini_client():
    """
    初始化 Gemini Client
    API Key 建議用環境變數 GEMINI_API_KEY
    """
    return genai.Client()


def generate_content_with_retry(
    client,
    prompt,
    model_name="gemini-2.5-flash",
    max_retries=3,
    delay=40,
):
    for i in range(max_retries):
        try:
            full_prompt = f"""
{SYSTEM_PROMPT}

以下是今天的資料：
{prompt}
"""

            response = client.models.generate_content(
                model=model_name,
                contents=[
                    {
                        "role": "user",
                        "parts": [{"text": full_prompt}],
                    }
                ],
            )
            return response.text

        except Exception as e:
            msg = str(e).lower()

            if "429" in msg or "rate" in msg:
                print(
                    f"Gemini API 呼叫失敗，"
                    f"{delay} 秒後重試... (嘗試 {i+1}/{max_retries})"
                )
                time.sleep(delay)
            else:
                print(f"發生其他錯誤: {e}")
                break

    return None

def get_bioweather_advice_local(model_name="llama3.2", content=None):
    # 準備 Prompt
    # content = f"Weather: {json.dumps(weather_data)}\nProfile: {json.dumps(user_profile)}"
    
    try:
        # 呼叫本地 Ollama
        response = ollama.chat(model=model_name, messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': content},
        ])
        
        return response['message']['content']
    except Exception as e:
        return f"Ollama 錯誤: {str(e)}"