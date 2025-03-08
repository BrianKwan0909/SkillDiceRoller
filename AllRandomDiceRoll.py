import psycopg2
import random
from datetime import datetime

# 連接 PostgreSQL 資料庫
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="DiceRoll",  # 資料庫名稱
            user="postgres",   # 用戶名
            password="10kwalap", # 密碼
            host="localhost",        # 或其他host
            port="5433"             # PostgreSQL預設端口
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# 根據骰子 ID 查詢每一面技能和機率
def get_dice_skills(dice_id):
    conn = connect_to_db()
    if not conn:
        return []

    cursor = conn.cursor()
    query = """
    SELECT s.skill_name, ds.probability, ds.face_number
    FROM dice_skills ds
    JOIN skills s ON ds.skill_id = s.skill_id
    WHERE ds.dice_id = %s
    ORDER BY ds.face_number;
    """
    cursor.execute(query, (dice_id,))
    skills = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return skills

# 隨機選擇一個技能並寫入txt檔案
def roll_dice_and_write_to_file(dice_id, filename):
    skills = get_dice_skills(dice_id)
    
    if not skills:
        print("No skills found for this dice.")
        return []
    
    dice_result = []
    # 獲取當前時間
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 開啟檔案進行寫入 (使用 'a' 模式來新增內容)
    with open(filename, 'a', encoding='utf-8') as file:
        # 在檔案開始時寫入時間戳記
        file.write(f"結果生成於: {current_time}\n")
        
        for face in range(1, 7):  # 6面骰子
            # 選擇當前面 (face_number) 的所有技能
            face_skills = [skill for skill in skills if skill[2] == face]
            
            # 計算每個技能的機率範圍並選擇
            random_value = random.random()
            cumulative_probability = 0
            for skill, probability, _ in face_skills:
                cumulative_probability += probability
                if random_value <= cumulative_probability:
                    dice_result.append(f"面{face}: {skill} (機率: {probability*100}%)")
                    file.write(f"面{face}: {skill} \n")
                    break
        
        file.write("\n")  # 新增空行，區分不同次的結果
    
    print(f"結果已寫入 {filename}")
    return dice_result

# 測試隨機生成骰子技能並將結果寫入檔案
dice_id = 1  # 假設你查詢的是骰子 ID = 1
filename = 'Result.txt'  # 輸出的txt檔案名稱
result = roll_dice_and_write_to_file(dice_id, filename)

# 顯示隨機結果
for res in result:
    print(res)