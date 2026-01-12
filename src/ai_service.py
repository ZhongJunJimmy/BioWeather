from google import genai
from google.genai import types

import os
import time
import json
import ollama

# read system prompt from file
SYSTEM_PROMPT_PATH = os.path.join(os.path.dirname(__file__), '..', './data/system_prompt.txt')
with open(SYSTEM_PROMPT_PATH, 'r', encoding='utf-8') as f:
    SYSTEM_PROMPT = f.read()

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
    full_prompt = prompt.strip()

    for i in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=[
                    {
                        "role": "user",
                        "parts": [{"text": full_prompt}],
                    }
                ],
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    max_output_tokens=128,
                    temperature=0.2,
                ),
            )
            return response.text

        except Exception as e:
            msg = str(e).lower()

            if any(k in msg for k in ("429", "rate", "timeout")):
                wait = delay * (2 ** i)
                print(
                    f"Gemini API 失敗，{wait} 秒後重試 "
                    f"(嘗試 {i+1}/{max_retries})"
                )
                time.sleep(wait)
            else:
                print(f"不可重試錯誤: {e}")
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