import tkinter as tk
import treeView
import popUpWindow
from tkinter import ttk
import json
import subprocess

def start_scan():
    # 启动外部Python文件
    subprocess.Popen(['python', 'test.py'])


# 创建主窗口
root = tk.Tk()
root.title("My App")
root.geometry("1000x600")  # 设置窗口大小

# 创建head_frame
head_frame = tk.Frame(root)
head_frame.pack(anchor="w")

# 创建button_frame用于按钮
button_frame = tk.Frame(head_frame)
button_frame.pack(pady=3)

# 创建菜单栏
# menu = tk.Menu(root)
# root.config(menu=menu)

# # 创建菜单
# file_menu = tk.Menu(menu, tearoff=0)
# menu.add_cascade(label="文件系统", menu=file_menu)
# file_menu.add_command(label="打开")
# # file_menu.add_separator()
#
# config_menu = tk.Menu(menu, tearoff=0)
# menu.add_cascade(label="扫描配置", menu=config_menu)
# # config_menu.add_command(label="")
#
# tips_menu = tk.Menu(menu, tearoff=0)
# menu.add_cascade(label="审计技巧", menu=tips_menu)
#
# help_menu = tk.Menu(menu, tearoff=0)
# menu.add_cascade(label="软件帮助", menu=help_menu)
# help_menu.add_command(label="")

# 创建main_frame

main_frame = tk.LabelFrame(root, text="源码列表")
main_frame.pack(fill="both", padx=10, expand=True)

main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=3)

# 创建left_side
left_side = tk.Frame(main_frame)
left_side.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
tree = ttk.Treeview(left_side, columns=("fullpath", "type", "size"), displaycolumns="size")
tree.bind('<<TreeviewOpen>>', treeView.update_tree)

ysb = ttk.Scrollbar(tree, orient='vertical', command=tree.yview)
xsb = ttk.Scrollbar(tree, orient='horizontal', command=tree.xview)

tree.configure(yscroll=ysb.set, xscroll=xsb.set)
ysb.pack(side='right', fill='y')
xsb.pack(side='bottom', fill='x')
tree.pack(expand='yes', fill='both')

# 创建按钮并将它们放入按钮容器中，使用grid布局
button_file = tk.Button(button_frame, text="打开文件", relief="flat", command=lambda: treeView.upload_file(tree))
button_config = tk.Button(button_frame, text="扫描配置", relief="flat")
button_tips = tk.Button(button_frame, text="审计技巧", relief="flat")
button_help = tk.Button(button_frame, text="软件帮助", relief="flat")

button_file.grid(row=0, column=0, padx=10)
button_config.grid(row=0, column=1, padx=10)
button_tips.grid(row=0, column=2, padx=10)
button_help.grid(row=0, column=3, padx=10)

# 创建right_side
right_side = tk.Frame(main_frame)
right_side.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

footer_frame = tk.Frame(right_side)
footer_frame.pack(anchor="w")
# 创建按钮并将它们放入按钮容器中
button_sacn = tk.Button(footer_frame, text="自动扫描",command=start_scan)
button_stop = tk.Button(footer_frame, text="停止扫描")
button_report = tk.Button(footer_frame, text="生成报告")

# 放置按钮在左上角
button_sacn.grid(row=0, column=0, padx=10, pady=5)
button_stop.grid(row=0, column=1, padx=10, pady=5)
button_report.grid(row=0, column=2, padx=10, pady=5)

# 添加单选框标签
label_language = tk.Label(footer_frame, text="       选择语言：")
label_language.grid(row=0, column=3, padx=(10,1), pady=5)

# 创建单选框变量
selected_language = tk.StringVar()

# 创建单选框变量
selected_language = tk.StringVar(value=" ")  # 初始化为一个不匹配任何选项的值

# 创建单选框并放置在右侧
rb_python = tk.Radiobutton(footer_frame, text="Python", variable=selected_language, value="Python")
rb_c = tk.Radiobutton(footer_frame, text="C", variable=selected_language, value="C")
rb_go = tk.Radiobutton(footer_frame, text="Go", variable=selected_language, value="Go")

# 放置单选框
rb_python.grid(row=0, column=4, padx=5)
rb_c.grid(row=0, column=5, padx=5)
rb_go.grid(row=0, column=6, padx=5)

# 创建details_frame
details_frame = tk.LabelFrame(right_side, text="扫描详情")
details_frame.pack(fill="both", padx=10, expand=True)

# 显示详情
# 创建Treeview控件
details_tree = ttk.Treeview(details_frame, columns=("ID", "文件路径", "漏洞描述", "漏洞详情"), show="headings")
details_tree.heading("#1", text="ID")
details_tree.heading("#2", text="文件路径")
details_tree.heading("#3", text="漏洞描述")
details_tree.heading("#4", text="漏洞详情")

import json


def load_json_to_treeview(json_file_name, treeview):
    with open(json_file_name, 'r', encoding='utf-8') as json_file:
        results = json.load(json_file)

    for item in results:
        treeview.insert('', 'end', values=(item["ID"], item["文件路径"], item["漏洞描述"], item["漏洞详细"]))


# 定义双击事件处理函数
def on_double_click(event):
    selected_item = details_tree.selection()  # 获取选中的行
    if selected_item:
        item = details_tree.item(selected_item, "values")
        popUpWindow.create_popup_window(root, item)

# 绑定双击事件处理函数
details_tree.bind("<Double-1>", on_double_click)

# 将Treeview控件放置到窗口中
details_tree.pack()

spacer = tk.Label(root)
spacer.pack()

# 运行Tkinter主循环
root.mainloop()
