from datetime import datetime
from pathlib import Path
import json
import os
from dotenv import load_dotenv
load_dotenv()

from src.weather_api import get_weather_json
from src.utils import get_city_coordinates
from src.ai_service import initial_gemini_client, generate_content_with_retry, get_bioweather_advice_local
from src.user import generate_user_profile

# read from config.json
CONFIG_PATH = os.path.join(os.path.dirname(__file__), './config.json')
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)
print(f"使用 LLM 供應商: {config.get('llm_provider')}")

def main():
    # 設定檔案路徑物件
    file_path = Path("./data/userData.json")

    # 判斷是否存在
    if not file_path.exists():
      user_json = generate_user_profile()

      now = datetime.now()
      date_str = f"{now.year}-{now.month}-{now.day}"

      user_json["lastUpdated"] = date_str
      os.makedirs('./data', exist_ok=True)

      with open('./data/userData.json', 'w', encoding='utf-8') as f:
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

    if config.get('llm_provider') == 'gemini':
        client = initial_gemini_client()
        response = generate_content_with_retry(client, model_name=config.get('gemini_model'), prompt=json.dumps(content_json))
    else:
        response = get_bioweather_advice_local(model_name=config.get('ollama_model'), content=json.dumps(content_json))
    print(f"AI建議: {response}")


if __name__ == '__main__':
    main()

