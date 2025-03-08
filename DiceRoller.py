import psycopg2
import random
from datetime import datetime
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

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

# 根據骰子 ID 查詢每一面技能和機率，同時拿到 skill_id
def get_dice_skills(dice_id):
    conn = connect_to_db()
    if not conn:
        return []

    cursor = conn.cursor()
    query = """
    SELECT s.skill_id, s.skill_name, ds.probability, ds.face_number
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

# 根據 Class 決定 dice_id
def get_dice_id_by_class(character_class):
    if character_class == "Warrior":
        return 2
    elif character_class == "Mage":
        return 3
    elif character_class == "Assassin":
        return 4
    elif character_class == "Hunter":
        return 5
    elif character_class == "Random":  # 新增 Random 類型，返回 dice_id = 1
        return 1
    else:
        return None  # 如果未識別的 Class，返回 None

# 插入骰子資料到 dics 表格
def insert_dice_to_db(dice_first_face, dice_second_face, dice_third_face, 
                      dice_fourth_face, dice_fifth_face, dice_sixth_face, 
                      owner):
    conn = connect_to_db()
    if not conn:
        print("Failed to connect to database for inserting dice.")
        return

    cursor = conn.cursor()
    insert_query = """
    INSERT INTO dices (dice_first_face, dice_first_face_LV, 
                       dice_second_face, dice_second_face_LV, 
                       dice_third_face, dice_third_face_LV, 
                       dice_fourth_face, dice_fourth_face_LV, 
                       dice_fifth_face, dice_fifth_face_LV, 
                       dice_sixth_face, dice_sixth_face_LV, 
                       owner)
    VALUES (%s, 1, %s, 1, %s, 1, %s, 1, %s, 1, %s, 1, %s);
    """
    cursor.execute(insert_query, (dice_first_face, dice_second_face, dice_third_face, 
                                  dice_fourth_face, dice_fifth_face, dice_sixth_face, owner))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Dice data for {owner} has been inserted into the database.")

# 隨機選擇一個技能並寫入txt檔案
def roll_dice_and_write_to_file(character_class, filename, owner="Unknown"):
    dice_id = get_dice_id_by_class(character_class)
    
    if not dice_id:
        print(f"未識別的Class: {character_class}")
        return []
    
    skills = get_dice_skills(dice_id)
    
    if not skills:
        print("No skills found for this dice.")
        return []
    
    dice_result = []
    dice_faces = [0] * 6  # 用來儲存每個面的 skill_id
    
    # 獲取當前時間
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 開啟檔案進行寫入 (使用 'a' 模式來新增內容)
    with open(filename, 'a', encoding='utf-8') as file:
        # 在檔案開始時寫入時間戳記
        file.write(f"結果生成於: {current_time}\n")
        
        for face in range(1, 7):  # 6面骰子
            # 選擇當前面 (face_number) 的所有技能
            face_skills = [skill for skill in skills if skill[3] == face]
            
            # 計算每個技能的機率範圍並選擇
            random_value = random.random()
            cumulative_probability = 0
            for skill_id, skill_name, probability, _ in face_skills:
                cumulative_probability += probability
                if random_value <= cumulative_probability:
                    dice_faces[face - 1] = skill_id  # 儲存每個面的 skill_id
                    dice_result.append(f"面{face}: {skill_name} (機率: {probability*100}%)")
                    file.write(f"面{face}: {skill_name} \n")
                    break
        
        file.write("\n")  # 新增空行，區分不同次的結果
    
    # 將骰子結果插入資料庫
    insert_dice_to_db(dice_faces[0], dice_faces[1], dice_faces[2], dice_faces[3],
                      dice_faces[4], dice_faces[5], owner)
    
    print(f"結果已寫入 {filename}")
    return dice_result

# GUI部分
root = tk.Tk()
root.title("骰子生成")
root.geometry("500x400")

# 顯示結果的文字框
output_box = ScrolledText(root, width=60, height=15, font=("Arial", 12))
output_box.pack(pady=10)

# 定義範例功能
def function1():
    result = roll_dice_and_write_to_file("Warrior", 'Result.txt', "Warrior")
    output_box.insert(tk.END, "\n".join(result) + "\n\n")

def function2():
    result = roll_dice_and_write_to_file("Assassin", 'Result.txt', "Assassin")
    output_box.insert(tk.END, "\n".join(result) + "\n\n")

def function3():
    result = roll_dice_and_write_to_file("Hunter", 'Result.txt', "Hunter")
    output_box.insert(tk.END, "\n".join(result) + "\n\n")

def function4():
    result = roll_dice_and_write_to_file("Mage", 'Result.txt', "Mage")
    output_box.insert(tk.END, "\n".join(result) + "\n\n")

def function5():
    result = roll_dice_and_write_to_file("Random", 'Result.txt', "Random")
    output_box.insert(tk.END, "\n".join(result) + "\n\n")

# 創建功能按鈕
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

btn1 = tk.Button(button_frame, text="生成戰士骰子", command=function1, width=15)
btn1.grid(row=0, column=0, padx=5, pady=5)

btn2 = tk.Button(button_frame, text="生成刺客骰子", command=function2, width=15)
btn2.grid(row=0, column=1, padx=5, pady=5)

btn3 = tk.Button(button_frame, text="生成獵人骰子", command=function3, width=15)
btn3.grid(row=1, column=0, padx=5, pady=5)

btn4 = tk.Button(button_frame, text="生成法師骰子", command=function4, width=15)
btn4.grid(row=1, column=1, padx=5, pady=5)

btn5 = tk.Button(button_frame, text="生成隨機骰子", command=function5, width=15)  # 新增按鈕
btn5.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# 主迴圈啟動應用程式
root.mainloop()
