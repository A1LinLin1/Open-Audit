import tkinter as tk
from tkinter import filedialog
from tkinter import Scrollbar

# 函数用于打开文件对话框并读取文件内容
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
    # print(file_extension)

    if file_extension == 'java':
        return read_file(file_path)
    elif file_extension == 'py':
        return read_file(file_path)
    elif file_extension == 'go':
        return read_file(file_path)
    elif file_extension == 'php':
        return read_file(file_path)
    elif file_extension == 'c'or file_extension == 'cpp':
        return read_file(file_path)
    elif file_extension == 'yml' or file_extension == 'yaml':
        return read_file(file_path)
    elif file_extension == 'txt':
        return read_file(file_path)
    elif file_extension == 'golang':
        return read_file(file_path)
    else:
        return "不支持的文件类型"

# 函数用于读取文件内容
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()

def create_file_viewer(root, file_path):
    popup = tk.Toplevel(root)
    popup.title("FileViewer")

    # 创建竖向滚动条
    scrollbar = Scrollbar(popup)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # 创建文本框，并与滚动条关联
    text_box = tk.Text(popup, wrap=tk.WORD, yscrollcommand=scrollbar.set)
    text_box.pack(fill="both", expand=True)
    scrollbar.config(command=text_box.yview)
    open_file_and_read(file_path, text_box)

# # 创建打开文件按钮
# open_button = tk.Button(root, text="打开文件", command=open_file_and_read)
# open_button.pack()
#
# # 运行主循环
# root.mainloop()
