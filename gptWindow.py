import tkinter as tk
from tkinter import filedialog
import markdown

import subprocess
import datetime


# 在窗口中打开./result.txtz文件

def create_result_gpt_window():
    result_gpt_window = tk.Toplevel()
    result_gpt_window.title("Result of GPT")
    result_gpt_window.geometry("800x600")
    # 以markdown格式显示内容
    
    text_box = tk.Text(result_gpt_window)
    text_box.pack()

    # 文本框自适应大小
    text_box.config(wrap=tk.WORD)
    text_box.config(state=tk.NORMAL)
    text_box.config(font=("Arial", 14))
    text_box.config(bg="white")
    text_box.config(fg="black")
    text_box.config(insertbackground="black")
    text_box.config(selectbackground="lightgray")
    text_box.config(selectforeground="white")
    text_box.config(height=40)
    text_box.config(width=100)
    text_box.config(padx=10)
    text_box.config(pady=10)
    text_box.config(relief=tk.SUNKEN)
    # 在右侧添加滚动条
    scroll = tk.Scrollbar(result_gpt_window, command=text_box.yview)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    text_box.config(yscrollcommand=scroll.set)



    # 读取文件内容
    with open("./result.txtz", 'r', encoding='utf-8') as file:
        content = file.read()
        text_box.insert(tk.END, content)



