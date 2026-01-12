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
    
def get_city_data_by_id(city_id):
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
    return city_map.get(city_id, city_map["1"])