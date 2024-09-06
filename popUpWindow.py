import datetime
import tkinter as tk
from tkinter import filedialog
import subprocess


def open_file_and_read(file_path, text_box):
    # file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    if file_path:
        file_content = read_supported_file(file_path)
        if file_content != "不支持的文件类型":
            text_box.delete(1.0, tk.END)  # 清空文本框内容
            text_box.insert(tk.END, file_content)
        else:
            text_box.delete(1.0, tk.END)
            text_box.insert(tk.END, "不支持的文件类型")


# 函数用于根据文件扩展名判断文件类型并返回内容
def read_supported_file(file_path):
    file_extension = file_path.split('.')[-1].lower()
    print(file_extension)

    if file_extension == 'java':
        return read_file(file_path)
    elif file_extension == 'py':
        return read_file(file_path)
    elif file_extension == 'go':
        return read_file(file_path)
    elif file_extension == 'php':
        # print("here")
        return read_file(file_path)
    elif file_extension == 'yml' or file_extension == 'yaml':
        return read_file(file_path)
    elif file_extension == 'txt':
        return read_file(file_path)
    else:
        return "不支持的文件类型"


# 函数用于读取文件内容
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        # print(file.read())
        return file.read()
    



def create_popup_window(root, data):
    popup = tk.Toplevel(root)
    popup.title("details")
    spacer = tk.Label(popup)
    spacer.pack()
    details_frame = tk.Frame(popup)
    details_frame.pack(fill="both", expand=True)
    left_details = tk.Frame(details_frame)
    left_details.grid(row=0, column=0, padx=3, sticky="nsew")
    right_details = tk.Frame(details_frame)
    right_details.grid(row=0, column=1, padx=3, sticky="nswe")
    details_frame.grid_rowconfigure(0, weight=1)
    details_frame.grid_columnconfigure(0, weight=1)
    details_frame.grid_columnconfigure(1, weight=1)

    # 在弹出窗口中显示数据
    label = tk.Label(right_details, text="ID: " + data[0], anchor="w", padx=10, wraplength=600, justify=tk.LEFT)
    label.pack(anchor="w", fill="x")

    label = tk.Label(right_details, text="文件路径: " + data[1], anchor="w", padx=10, wraplength=600, justify=tk.LEFT)
    label.pack(anchor="w", fill="x")

    label = tk.Label(right_details, text="漏洞描述: " + data[2], anchor="w", padx=10, wraplength=600, justify=tk.LEFT)
    label.pack(anchor="w", fill="x")

    label = tk.Label(right_details, text="漏洞详情: " + data[3], anchor="w", padx=10, wraplength=600, justify=tk.LEFT)
    label.pack(anchor="w", fill="x")
    # 创建文本框，用于显示聊天记录
    chat_text = tk.Text(right_details)
    chat_text.pack(fill="both", expand=True, pady=10, padx=5)

    # 创建滚动条并绑定到文本框
    scrollbar = tk.Scrollbar(right_details, command=chat_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    chat_text.config(yscrollcommand=scrollbar.set)

    footer_frame = tk.Frame(right_details)
    footer_frame.pack(side=tk.BOTTOM, fill="x", padx=10)
    # 创建输入框
    input_entry = tk.Entry(footer_frame)
    input_entry.grid(row=0, column=0, sticky="ew")

    # 定义发送消息的函数
    def send_message():
        message = input_entry.get()
        if message:
            # 向另一个Python文件发送消息并获取回复
            process = subprocess.Popen(['python', 'chatWithGPT.py', message],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
            stdout, stderr = process.communicate()

            if stdout:
                # chat_text.insert(tk.END, f"你: {message}\n", "user")
                chat_text.insert(tk.END, f"你: {datetime.datetime.now().strftime('%Y-%m-%d:%H-%M-%S')}\n")
                chat_text.insert(tk.END, f"{message}\n\n", "user")
                chat_text.insert(tk.END, f"对方: {datetime.datetime.now().strftime('%Y-%m-%d:%H-%M-%S')}\n")
                chat_text.insert(tk.END, f"{stdout}\n\n", "other")
            if stderr:
                chat_text.insert(tk.END, f"错误： {datetime.datetime.now().strftime('%Y-%m-%d:%H-%M-%S')}\n")
                chat_text.insert(tk.END, f"错误: {stderr}\n", "error")
            input_entry.delete(0, tk.END)

    # 创建发送按钮
    send_button = tk.Button(footer_frame, text="机器学习判断", command=send_message)
    send_button.grid(row=0, column=1, pady=10)
    footer_frame.grid_rowconfigure(0, weight=1)
    footer_frame.grid_columnconfigure(0, weight=6)
    footer_frame.grid_columnconfigure(1, weight=1)

    # 设置聊天框样式
    chat_text.tag_config("user", foreground="blue")
    chat_text.tag_config("other", foreground="green")
    chat_text.tag_config("error", foreground="red")

    # 创建竖向滚动条
    scrollbar = tk.Scrollbar(left_details)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # 创建文本框，并与滚动条关联
    text_box = tk.Text(left_details, wrap=tk.WORD, yscrollcommand=scrollbar.set)
    text_box.pack(fill="both", expand=True)
    scrollbar.config(command=text_box.yview)
    open_file_and_read(data[1], text_box)
    # 函数用于打开文件对话框并读取文件内容

    # # 按钮
    # button = tk.Button(popup, text="与ChatGPT聊天", command=on_button_click)
    # button.pack(side=tk.BOTTOM, pady=10)

    # root.mainloop()