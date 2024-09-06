import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import stateManager
import fileViewer

def populate_tree(tree, node):
    if tree.set(node, "type") != 'directory':
        return

    path = tree.set(node, "fullpath")
    tree.delete(*tree.get_children(node))

    for p in os.listdir(path):
        ptype = None
        p = os.path.join(path, p).replace('\\', '/')
        if os.path.isdir(p): ptype = "directory"
        elif os.path.isfile(p): ptype = "file"
        fname = os.path.split(p)[1]
        id = tree.insert(node, "end", text=fname, values=[p, ptype])
        if ptype == 'directory':
            if fname not in ('.', '..'):
                tree.insert(id, 0, text="dummy")
                tree.item(id, text=fname)
        # elif ptype == 'file':
            # size = os.path.getsize(p)
            # tree.set(id, "size")

def update_tree(event):
    tree = event.widget
    populate_tree(tree, tree.focus())
    # adjust_column_width(tree, "#0")
    # max_width = 500
    # max_width = get_max_tree_width(tree)
    # print(max_width)
    # tree.column("#0", width=max_width)
    # print("11")

def upload_file(tree):
    # global folder_path
    folder_path = filedialog.askdirectory()  # 打开文件夹选择对话框
    if folder_path:
        load_directory(tree, folder_path)
        stateManager.set_state(folder_path)
    return folder_path

# def get_folder():
#     global folder_path
#     return folder_path

def load_directory(tree, folder_path):
    tree.delete(*tree.get_children())  # 清空文件树
    node = tree.insert('', 'end', text=folder_path, values=[folder_path, "directory"])
    populate_tree(tree, node)
    tree.item(node, open=True)

def get_root_node_path(tree):
    root_id = tree.item(tree.get_children(""))["text"]
    stateManager.get_state()
    return root_id

# def on_item_double_click(tree):
#     print("here")
#     item = tree.selection()[0]  # 获取被选中的项
#     item_type = tree.item(item, "values")[1]  # 获取项的类型
#     if item_type == "file":
#         file_path = tree.item(item, "values")[0]
#         print(f"双击了文件：{file_path}")
# def get_max_tree_width(tree):
    max_width = 0
    # for item_id in tree.get_children():
    #     item_text = tree.item(item_id, "text")
    #     text_length = len(item_text)
    #     # item_width = tree.bbox(item_id, column="#0")[-1]  # 获取节点文本的右边界
    #     left_boundary = tree.bbox(item_id, column="#0")[0]  # 左边界
    #     print(left_boundary)
    #     item_width = left_boundary + text_length
    #     if item_width > max_width:
    #         max_width = item_width
    # global max_width
    # max_width = 0
    # folder_path = get_root_node_path(tree)
    # print("22")
    # print(folder_path)
    # root_node = tree.insert('', 'end', text=folder_path, values=[folder_path, "directory"])
    # for child in tree.get_children(root_node):
    #     item_width = tree.bbox(child)[2] - tree.bbox(child)[0]
    #     if item_width > max_width:
    #         max_width = item_width
    #     max_width = max(max_width, get_max_tree_width(child))
    # return max_width

# def adjust_column_width(tree, column_id):
#     max_width = 0
#     for item in tree.get_children():
#         item_text = tree.item(item, column=column_id)["text"]
#         if item_text:
#             item_width = tree.bbox(item, column=column_id)[2] - tree.bbox(item, column=column_id)[0]
#             if item_width > max_width:
#                 max_width = item_width
#     tree.column(column_id, width=max_width)

