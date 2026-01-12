from typing import Dict

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


def clamp(value: float, min_v: float, max_v: float) -> float:
    return max(min_v, min(value, max_v))


def classify_thermal_feel(feels_like: float, cold_tolerance: float, heat_tolerance: float) -> str:
    """
    根據體感溫度 + 個人耐溫能力，判斷整體冷熱感受
    """
    # 基準區間（可微調）
    if feels_like <= 5:
        base = "very_cold"
    elif feels_like <= 12:
        base = "cold"
    elif feels_like <= 18:
        base = "cool"
    elif feels_like <= 24:
        base = "neutral"
    elif feels_like <= 30:
        base = "warm"
    else:
        base = "hot"

    # 個人修正（怕冷 / 怕熱）
    # coldTolerance 越小越怕冷 → 感覺更冷
    if base in ("cool", "neutral") and cold_tolerance < 0.4:
        return "cool"

    # heatTolerance 越大越怕熱 → 感覺更熱
    if base in ("neutral", "warm") and heat_tolerance > 0.7:
        return "warm"

    return base


def classify_wind_effect(wind_speed: float, wind_sensitivity: float) -> str:
    """
    依風速與個人風敏感度判斷風影響
    """
    # 個人化風速（敏感者放大影響）
    adjusted_wind = wind_speed * (1 + (wind_sensitivity - 0.5))

    if adjusted_wind < 2:
        return "none"
    elif adjusted_wind < 4:
        return "light"
    elif adjusted_wind < 7:
        return "noticeable"
    else:
        return "strong"


def classify_humidity_feel(humidity: float, humidity_sensitivity: float) -> str:
    """
    濕度體感判斷
    """
    adjusted_humidity = humidity * (1 + (humidity_sensitivity - 0.5) * 0.5)

    if adjusted_humidity < 35:
        return "dry"
    elif adjusted_humidity <= 70:
        return "normal"
    else:
        return "humid"


def classify_tolerance(value: float, reverse: bool = False) -> str:
    """
    將 0~1 的 tolerance 轉為 enum
    reverse=True 表示「數值越小越怕」
    """
    if reverse:
        value = 1 - value

    if value < 0.33:
        return "low"
    elif value < 0.66:
        return "normal"
    else:
        return "high"


def build_decision_schema(
    weather: Dict,
    personal: Dict,
    activity_level: str = "low",
    time_of_day: str = "daytime",
) -> Dict:
    """
    將原始天氣 + 個人體感轉為 Ollama 友善 decision schema
    """

    thermal_feel = classify_thermal_feel(
        feels_like=weather["feels_like"],
        cold_tolerance=personal["coldTolerance"],
        heat_tolerance=personal["heatTolerance"],
    )

    wind_effect = classify_wind_effect(
        wind_speed=weather["wind_speed"],
        wind_sensitivity=personal["windSensitivity"],
    )

    humidity_feel = classify_humidity_feel(
        humidity=weather["humidity"],
        humidity_sensitivity=personal["humiditySensitivity"],
    )

    cold_tolerance_enum = classify_tolerance(
        personal["coldTolerance"], reverse=True
    )

    return {
        "thermal_feel": thermal_feel,
        "wind_effect": wind_effect,
        "humidity_feel": humidity_feel,
        "activity_level": activity_level,
        "cold_tolerance": cold_tolerance_enum,
        "time_of_day": time_of_day,
    }
