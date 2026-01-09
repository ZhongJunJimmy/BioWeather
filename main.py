import google.generativeai as genai
import google.api_core.exceptions as exceptions

from datetime import datetime
from pathlib import Path
import requests
import json
import time
import typing_extensions as typing

GEMINI_API_KEY='GEMINI_API_KEY'

def get_weather_json(lat=25.07, lon=121.57):

    # temperature_2m -> temperature
    # apparent_temperature -> feels_like
    # relative_humidity_2m -> humidity
    # wind_speed_10m -> wind_speed
    # precipitation -> precipitation
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,wind_speed_10m"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        current = data['current']

        weather_output = {
            "temperature": current['temperature_2m'],
            "feels_like": current['apparent_temperature'],
            "humidity": current['relative_humidity_2m'],
            "wind_speed": current['wind_speed_10m'],
            "precipitation": current['precipitation']
        }

        return json.dumps(weather_output, indent=4, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"error": str(e)})


def get_city_coordinates():
    # 定義台灣主要縣市的經緯度對照表
    city_map = {
        "1": {"name": "台北", "lat": 25.03, "lon": 121.56},
        "2": {"name": "新北", "lat": 25.01, "lon": 121.46},
        "3": {"name": "桃園", "lat": 24.99, "lon": 121.30},
        "4": {"name": "台中", "lat": 24.14, "lon": 120.67},
        "5": {"name": "台南", "lat": 22.99, "lon": 120.21},
        "6": {"name": "高雄", "lat": 22.62, "lon": 120.31},
        "7": {"name": "花蓮", "lat": 23.97, "lon": 121.60},
        "8": {"name": "宜蘭", "lat": 24.75, "lon": 121.75}
    }

    print("--- 請選擇要查詢的縣市 ---")
    for key, info in city_map.items():
        print(f"{key}. {info['name']}")

    choice = input("\n請輸入編號 (1-8): ")

    if choice in city_map:
        selected = city_map[choice]
        return selected
    else:
        print("輸入錯誤，預設選擇台北。")
        return city_map["1"]

def generate_content_with_retry(model, prompt, max_retries=3, delay=40):
    for i in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response
        except exceptions.TooManyRequests as e:
            print(f"Gemini API (generate_content) 呼叫失敗。將在 {delay} 秒後重試... (嘗試 {i+1}/{max_retries})")
            time.sleep(delay)
        except Exception as e:
            print(f"發生其他錯誤: {e}")
            break
    return None

def generate_user_profile():
    print("--- 體感偏好測驗 (請輸入 1-5 分) ---")

    # 獲取使用者輸入
    q1 = int(input("1. 15度穿薄長袖會發抖嗎？(1-5): "))
    q2 = int(input("2. 28度不開冷氣會心煩嗎？(1-5): "))
    q3 = int(input("3. 冬天強風會讓你覺得冷加倍嗎？(1-5): "))
    q4 = int(input("4. 高濕度會讓你覺得皮膚黏膩不適嗎？(1-5): "))
    q5 = int(input("5. 悶熱環境會讓你提早放棄運動嗎？(1-5): "))

    # 1. coldTolerance: 越小越怕冷 (Score 5 -> 0.0, Score 1 -> 1.0)
    cold_tol = (5 - q1) / 4
    # 2. heatTolerance: 越大越怕熱 (Score 5 -> 1.0, Score 1 -> 0.0)
    heat_tol = (q2 - 1) / 4
    # 3. windSensitivity: 越高越敏感
    wind_sens = (q3 - 1) / 4
    # 4. humiditySensitivity: 越高越敏感 (平均 Q4, Q5)
    hum_sens = (((q4 + q5) / 2) - 1) / 4

    profile = {
        "coldTolerance": round(cold_tol, 2),
        "heatTolerance": round(heat_tol, 2),
        "windSensitivity": round(wind_sens, 2),
        "humiditySensitivity": round(hum_sens, 2)
    }

    return profile


def initial_gemini_model:
    genai.configure(api_key=GEMINI_API_KEY)

    # 設定 API
    genai.configure(api_key=userdata.get('GEMINI_API_KEY'))

    # 設定 System Prompt
    SYSTEM_PROMPT = """
    你是一位個人化穿衣建議助理。

    系統將提供兩類資訊：
    1. weather_data：描述當前環境的天氣條件
    2. user_data：描述使用者對冷、熱、風與濕度的個人體感傾向
    2.1 coldTolerance: 越小越怕冷
    2.1 heatTolerance: 越大越怕熱
    2.1 windSensitivity: 風對體感影響
    2.1 humiditySensitivity: 濕度影響

    你的任務是根據這些資訊，提供「今天應該怎麼穿」的實用建議。

    請遵守以下規則：
    - 專注在穿衣褲建議本身，不要解釋數值或資料來源
    - 不要提及任何模型、參數名稱、計算方式或 AI 相關概念
    - 語氣自然、生活化，像是在提醒一位朋友
    - 不要給多個選項，請給出一個明確的主要建議
    - 依照參考的數據，給出今天可能會感受到的狀態
    - 若天氣條件偏嚴苛（例如風大、體感偏低），可補充一句保守提醒
    - 不要假設使用者的活動內容，除非資訊中有明確暗示

    回覆格式限制：
    - 使用繁體中文
    - 回覆長度為 1～5 句
    - 第一句先給穿衣結論，後面提供簡短說明原因或可能的體感
    - 不使用條列、不使用表情符號、不使用專業術語

    """

    # 初始化模型時傳入 system_instruction
    return genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        system_instruction=SYSTEM_PROMPT
    )


def main():
    model=initial_gemini_model

    # 設定檔案路徑物件
    file_path = Path("./data/userData.json")

    # 判斷是否存在
    if not file_path.exists():
      user_json = generate_user_profile()

      now = datetime.now()
      date_str = f"{now.year}-{now.month}-{now.day}"

      user_json["lastUpdated"] = date_str

      with open('./userData.json', 'w', encoding='utf-8') as f:
          json.dump(user_json, f, indent=4, ensure_ascii=False)

      print(f"Write done!")
    else:
      print("個人化數據已存在")


    with open('./data/userData.json', 'r', encoding='utf-8') as f:
        user_data = json.load(f)
    del user_data['lastUpdated']

    selected_city = get_city_coordinates()

    content_json={
        "weather_data": get_weather_json(lat=selected_city['lat'], lon=selected_city['lon']),
        "user_data": user_data
    }
    # print(content_json)

    response = generate_content_with_retry(model, json.dumps(content_json))
    # response = model.generate_content(json.dumps(content_json))

    print(f"AI建議: {response.text}")


if __name__ == '__main__':
    main()

