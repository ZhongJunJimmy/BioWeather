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
