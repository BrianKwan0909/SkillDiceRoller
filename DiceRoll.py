import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import AllRandomDiceRoll_U as alldice
import AssassinDiceRoll as assdice 
import HunterDiceRoll as Hundice 
import MageDiceRoll as Magedice 
import WarriorDiceRoll as Wardice 


root = tk.Tk()
root.title("骰子生成")
root.geometry("500x400")

# 顯示結果的文字框
output_box = ScrolledText(root, width=60, height=15, font=("Arial", 12))
output_box.pack(pady=10)

# 定義範例功能
def function1():
    result = alldice.roll_dice_and_write_to_file(1, 'Result.txt')
    output_box.insert(tk.END, "\n".join(result) + "\n\n")

def function2():
    result = assdice.roll_dice_and_write_to_file(1, 'Result.txt')
    output_box.insert(tk.END, "\n".join(result) + "\n\n")

def function3():
    result = Hundice.roll_dice_and_write_to_file(1, 'Result.txt')
    output_box.insert(tk.END, "\n".join(result) + "\n\n")

def function4():
    result = Magedice.roll_dice_and_write_to_file(1, 'Result.txt')
    output_box.insert(tk.END, "\n".join(result) + "\n\n")

def function5():
    result = Wardice.roll_dice_and_write_to_file(1, 'Result.txt')
    output_box.insert(tk.END, "\n".join(result) + "\n\n")

# 創建功能按鈕
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

btn1 = tk.Button(button_frame, text="生成隨機骰子", command=function1, width=15)
btn1.grid(row=0, column=0, padx=5, pady=5)

btn2 = tk.Button(button_frame, text="生成刺客骰子", command=function2, width=15)
btn2.grid(row=0, column=1, padx=5, pady=5)

btn3 = tk.Button(button_frame, text="生成獵人骰子", command=function3, width=15)
btn3.grid(row=1, column=0, padx=5, pady=5)

btn4 = tk.Button(button_frame, text="生成法師骰子", command=function4, width=15)
btn4.grid(row=1, column=1, padx=5, pady=5)

btn5 = tk.Button(button_frame, text="生成戰士骰子", command=function5, width=15)
btn5.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# 主迴圈啟動應用程式
root.mainloop()
