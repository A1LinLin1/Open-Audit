import tkinter as tk
from tkinter.ttk import Style

from ttkbootstrap import style

import fileMenu
import gptWindow
import popUpWindow
# from tkinter import ttk
import json
import subprocess
import createReportPdf
import stateManager
import fileViewer
import main_java
import os
# from ttkbootstrap import Style
import ctypes
import ttkbootstrap as ttk
import gpt



isBottom = 1
isState = 0
# 根据父组件的宽度动态调整列宽
def on_parent_resize(event):
    # 获取父组件的宽度
    parent_width = details_frame.winfo_width()
    # 根据父组件的宽度动态调整列宽
    # column_width = parent_width // 4  # 4列均分父组件的宽度
    details_tree.column("#1", width=round(parent_width * 0.1), minwidth=50, anchor="center", stretch=True)
    details_tree.column("#2", width=round(parent_width * 0.3), minwidth=100, stretch=True)
    details_tree.column("#3", width=round(parent_width * 0.3), minwidth=100, stretch=True)
    details_tree.column("#4", width=round(parent_width * 0.3), minwidth=100, stretch=True)

def update_treeview():
    # 从 results.json 文件读取新数据
    # 检查是否存在 results.json 文件，如果不存在，则创建一个空的文件
    # if os.path.exists('results.json'):

    if not os.path.exists('results.json'):
        with open('results.json', 'w', encoding='utf-8') as empty_json_file:
            empty_json_file.write('[]')

    # 然后尝试读取 JSON 数据
    try:
        with open('results.json', 'r', encoding='utf-8') as json_file:
            new_results = json.load(json_file)
    except json.JSONDecodeError:
        # 如果JSON解析错误（JSON为空），将其设置为一个空数组
        new_results = []

    # 清空现有的 Treeview 条目
    details_tree.delete(*details_tree.get_children())

    # 插入新数据
    for item in new_results:
        details_tree.insert('', 'end', values=(item["ID"], item["文件路径"], item["漏洞描述"], item["漏洞详细"]))
        # style.configure("Treeview", rowheight=100)
    # 设置 Treeview 的高度（可选）
    # tree_height = len(new_results)
    # details_tree.configure(height=tree_height)
    # 定期调用此函数，以便动态更新 Treeview
    # root.after(500, update_treeview)  # 在此示例中，每隔 500 毫秒（0.5 秒）调用一次此函数

def slow_scroll():
    global isBottom
    # 获取当前滚动位置
    current_position = float(details_tree.yview()[0])
    # print(current_position)

    # 目标滚动位置为最底部
    target_position = 1.0
    # print( isBottom)
    # 计算每步的滚动增量
    step = (target_position - current_position) / 10
    if isBottom > step:
        isBottom = step
    else:
        isBottom = 0
    # 如果还未达到最底部，则继续滚动
    if isBottom != 0:
        # print(isBottom)
        details_tree.yview_moveto(current_position + step)
        root.after(50, slow_scroll)  # 每隔50毫秒滚动一次
    # else:
        # isBottom = 0
        # print(isBottom)
        # 等待3秒后再滚动至最底部
        # time.sleep(3)
        # details_tree.yview_moveto(target_position)

def scan_button_clicked():
    global isBottom
    global isState
    isBottom = 1
    # isState = 0
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_to_delete = os.path.join(current_directory, 'results.json')
    if os.path.exists(file_to_delete):
        os.remove(file_to_delete)
        print(f"The file '{file_to_delete}' has been deleted.")
    else:
        print(f"The file '{file_to_delete}' does not exist.")
    # 取消之前的滚动任务（如果存在）
    root.after_cancel(slow_scroll)
    # print(1)
    folder_path = stateManager.get_state()
    mode = selected_scan_language
    # print(mode)
    # print(folder_path)
    # 调用 scan.py 脚本
    if folder_path:
        if mode:
            setup_progress_bar(root, progress_frame, footer_label)
            main_java.main(mode, folder_path)
            update_treeview()
            # 开始缓慢滚动
            slow_scroll()
            isState = 1
            print(isState)
            # subprocess.call(["python", "main_java.py"])  # 在这里指定模式

# style = Style()
# style = Style.theme_use(, 'sandstone')
#想要切换主题，修改theme值即可，有以下这么多的主题，自己尝试吧：['vista', 'classic', 'cyborg', 'journal', 'darkly', 'flatly', 'clam', 'alt', 'solar', 'minty', 'litera', 'united', 'xpnative', 'pulse', 'cosmo', 'lumen', 'yeti', 'superhero', 'winnative', 'sandstone', 'default']
# root = style.master
#这两行代码在自己原基础的代码上加入即可，放在代码的最开端部分，也就是在窗口创建代码之前


# 创建主窗口
root = tk.Tk()
style = Style()
style.theme_use('clam')

root.title("Open_Audit")
# root.geometry("1000x600")  # 设置窗口大小
# 告诉操作系统使用程序自身的DPI适配
ctypes.windll.shcore.SetProcessDpiAwareness(1)

# 获取屏幕的缩放因子
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)

# 设置程序缩放
root.tk.call('tk', 'scaling', ScaleFactor / 75)

# 设置窗口大小，根据缩放因子调整
window_width = int(10 * ScaleFactor)
window_height = int(6 * ScaleFactor)
root.geometry(f"{window_width}x{window_height}")



# 创建一个StringVar变量来存储选中的语言
selected_scan_language = tk.StringVar()

def update_selected_scan_language(value):
    global selected_scan_language
    selected_scan_language = value
    # print(selected_scan_language)

# 创建head_frame
head_frame = tk.Frame(root)
head_frame.pack(anchor="w")

# 创建button_frame用于按钮
button_frame = tk.Frame(head_frame)
button_frame.pack(pady=3)

# 创建main_frame
main_frame = tk.LabelFrame(root, text="源码列表")
main_frame.pack(fill="both", padx=10, expand=True)

main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)

# 创建left_side
left_side = tk.Frame(main_frame)
left_side.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
file_menu = ttk.Treeview(left_side, columns=("fullpath", "type", "size"), displaycolumns="")
file_menu.heading("#0", text="Project", anchor="w")
# file_menu.column("#0", width=10)
file_menu.bind('<<TreeviewOpen>>', fileMenu.update_tree)
# file_menu.bind(("<Double-1>", fileMenu.on_item_double_click))

ysb = ttk.Scrollbar(file_menu, bootstyle="round", orient='vertical', command=file_menu.yview)
xsb = ttk.Scrollbar(file_menu, bootstyle="round", orient='horizontal', command=file_menu.xview)

file_menu.configure(yscroll=ysb.set, xscroll=xsb.set)
ysb.pack(side='right', fill='y')
xsb.pack(side='bottom', fill='x')
file_menu.pack(expand='yes', fill='both')

# 创建按钮并将它们放入按钮容器中，使用grid布局
button_file = tk.Button(button_frame, text="打开文件", relief="flat", command=lambda: fileMenu.upload_file(file_menu))
button_config = tk.Button(button_frame, text="扫描配置", relief="flat", command=lambda: fileViewer.create_file_viewer(root, "java_rules.yml"))
button_tips = tk.Button(button_frame, text="审计技巧", relief="flat", command=lambda: fileViewer.create_file_viewer(root, "java_rules.yml"))
button_help = tk.Button(button_frame, text="软件帮助", relief="flat", command=lambda: fileViewer.create_file_viewer(root, "关于我们.txt"))

button_file.grid(row=0, column=0, padx=10)
button_config.grid(row=0, column=1, padx=10)
button_tips.grid(row=0, column=2, padx=10)
button_help.grid(row=0, column=3, padx=10)

# # 获取根路径
# rootNodePath = fileMenu.get_root_node_path(file_menu)
# print(rootNodePath)
# 创建right_side
right_side = tk.Frame(main_frame)
right_side.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

footer_frame = tk.Frame(right_side)
footer_frame.pack(anchor="w")

def generate_report():
    global isState
    print(isState)
    if isState == 1:
        folder_path = stateManager.get_state()
        dir_path, last_folder = os.path.split(folder_path)
        print(last_folder)
        createReportPdf.generate_pdf_report("results.json", last_folder)


# 创建按钮并将它们放入按钮容器中
button_sacn = tk.Button(footer_frame, text="启动扫描", command=lambda: scan_button_clicked())
button_stop = tk.Button(footer_frame, text="停止扫描")
button_report = tk.Button(footer_frame, text="生成报告", command=lambda: generate_report())
button_gpt = tk.Button(footer_frame, text="gpt扫描", command=lambda: gpt.check(folder_path=stateManager.get_state(),outpath="./result.txtz"))







# 当点击"gpt扫描"按钮，检查文件result.json是否存在，如果存在则调用gptWindow.py中的create_result_gpt_window()函数
def gpt_scan():
    if os.path.exists('result.txtz'):
        gptWindow.create_result_gpt_window()
    else:
        print("The file 'result.txtz' does not exist.")

button_gpt_report = tk.Button(footer_frame, text="gpt扫描报告", command=gpt_scan)



# 放置按钮在左上角
button_sacn.grid(row=0, column=0, padx=10, pady=5)
button_stop.grid(row=0, column=1, padx=10, pady=5)
button_report.grid(row=0, column=2, padx=10, pady=5)
button_gpt.grid(row=0, column=3, padx=10, pady=5)
button_gpt_report.grid(row=0, column=4, padx=10, pady=5)



# 添加单选框标签
label_language = tk.Label(footer_frame, text="       选择语言：")
label_language.grid(row=0, column=5, padx=(10, 1), pady=5)

# 创建单选框变量
selected_language = tk.StringVar()

# 创建单选框变量
selected_language = tk.StringVar(value=" ")  # 初始化为一个不匹配任何选项的值

# 创建选择列表并放置在右侧，从各种语言中选择一个
# 节省空间，将单选框放置在一个菜单中
scan_language_menu = ttk.Combobox(footer_frame, values=("java", "python", "go", "php", "cpp", "c"), textvariable=selected_language)
scan_language_menu.grid(row=0, column=6, padx=5)

# 选择列表的回调函数
def on_scan_language_selected(event):
    selected_language = scan_language_menu.get()
    update_selected_scan_language(selected_language)

# 绑定选择列表的回调函数
scan_language_menu.bind("<<ComboboxSelected>>", on_scan_language_selected)


# # 创建单选框并放置在右侧
# rb_python = ttk.Radiobutton(footer_frame, bootstyle="primary", text="Python", variable=selected_language, value="python", command=lambda: update_selected_scan_language("python"))
# rb_c = ttk.Radiobutton(footer_frame, bootstyle="primary", text="Java", variable=selected_language, value="java", command=lambda:update_selected_scan_language("java"))
# rb_go = ttk.Radiobutton(footer_frame, bootstyle="primary", text="Go", variable=selected_language, value="go", command=lambda:update_selected_scan_language("go"))
# rb_php = ttk.Radiobutton(footer_frame, bootstyle="primary", text="Php", variable=selected_language, value="php", command=lambda:update_selected_scan_language("php"))
# rb_cpp= ttk.Radiobutton(footer_frame, bootstyle="primary", text="C/C++", variable=selected_language, value="cpp", command=lambda:update_selected_scan_language("cpp"))
# rb_golang = ttk.Radiobutton(footer_frame, bootstyle="primary", text="Golang", variable=selected_language, value="golang", command=lambda:update_selected_scan_language("golang"))

# # 放置单选框
# rb_python.grid(row=0, column=4, padx=5)
# rb_c.grid(row=0, column=5, padx=5)
# rb_go.grid(row=0, column=6, padx=5)
# rb_php.grid(row=0, column=7, padx=5)
# rb_cpp.grid(row=0, column=8, padx=5)
# rb_golang.grid(row=0, column=9, padx=5)

# 创建details_frame
details_frame = tk.LabelFrame(right_side, text="扫描详情")
details_frame.pack(fill="both", padx=1, pady=1, expand=True)

details_frame_height = details_frame.winfo_height()
# print(details_frame_height)
details_tree_frame = tk.Frame(details_frame)
details_tree_frame.pack(expand=True, fill="both")

# 显示详情
# 创建Treeview控件
details_tree = ttk.Treeview(details_tree_frame, columns=("ID", "文件路径", "漏洞描述", "漏洞详情"), show="headings")
details_tree.heading("#1", text="ID")
details_tree.heading("#2", text="文件路径")
details_tree.heading("#3", text="木马描述")
details_tree.heading("#4", text="木马详情")

# 监听父组件大小变化事件
details_frame.bind("<Configure>", on_parent_resize)

update_treeview()

# 创建滚动条
scrollbar = ttk.Scrollbar(details_tree_frame, bootstyle="round", orient="vertical", command=details_tree.yview)
scrollbar.pack(side="right", fill="y")

# 连接滚动条到Treeview控件
details_tree.configure(yscrollcommand=scrollbar.set)

# 将Treeview控件放置到窗口中
details_tree.pack(fill='both', expand=True)

# 在窗口初始化后设置初始列宽度
def set_initial_column_width():
    details_tree.column("#1", width=10, anchor="center")
    details_tree.column("#2", width=200)
    details_tree.column("#3", width=200)
    details_tree.column("#4", width=200)

root.after(50, set_initial_column_width)  # 延迟执行以确保窗口初始化完成

progress_frame = tk.Frame(right_side)
progress_frame.pack(side=tk.BOTTOM, fill="x")
# progress_frame.lift()

# 在Treeview下方添加Label组件作为底部行字，并将其对齐到左边下边界并紧挨着
footer_label = tk.Label(progress_frame, text="系统已就绪")
footer_label.grid(row=0, column=0, sticky='w', pady=5)

def setup_progress_bar(root, progress_frame, footer_label):
    # 创建Progressbar对象并设置样式和长度
    progress_bar = ttk.Progressbar(progress_frame, mode="determinate", length=300)
    footer_label.config(text="加载中，请稍等...")

    # 将进度条放置在底部行下方
    progress_bar.grid(row=0, column=1, sticky="w", padx=15, pady=5)

    def stop_progress_bar():
        progress_bar.stop()
        footer_label.config(text="扫描已完成")
        progress_bar.grid_remove()  # 从父容器中移除进度条

    # 启动进度条的动画效果
    progress_bar.start(21)

    # 在3秒后停止进度条的动画并隐藏进度条
    root.after(1000, stop_progress_bar)


# 定义双击事件处理函数
def on_double_click(event):
    selected_item = details_tree.selection()  # 获取选中的行
    if selected_item:
        item = details_tree.item(selected_item, "values")
        popUpWindow.create_popup_window(root, item)

# 绑定双击事件处理函数
details_tree.bind("<Double-1>", on_double_click)

# 将Treeview控件放置到窗口中
# details_tree.pack()

spacer = tk.Label(root)
spacer.pack()

def get_frame_width(event):
    main_frame_width = main_frame.winfo_width()
    main_frame.columnconfigure(0, minsize=round(main_frame_width * 0.18))
    main_frame.columnconfigure(1, minsize=round(main_frame_width * 0.82))

root.bind("<Configure>", get_frame_width)

def on_closing():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_to_delete = os.path.join(current_directory, 'results.json')

    if os.path.exists(file_to_delete):
        os.remove(file_to_delete)
        print(f"The file '{file_to_delete}' has been deleted.")
    else:
        print(f"The file '{file_to_delete}' does not exist.")

    file_to_delete2 = os.path.join(current_directory, 'result.txtz')
    if os.path.exists(file_to_delete2):
        os.remove(file_to_delete2)
        print(f"The file '{file_to_delete2}' has been deleted.")
    else:
        print(f"The file '{file_to_delete2}' does not exist.")
        

    print(current_directory)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# 运行Tkinter主循环
root.mainloop()
