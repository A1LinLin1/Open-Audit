import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os

def populate_tree(tree, node):
    if tree.set(node, "type") != 'directory':
        return

    path = tree.set(node, "fullpath")
    tree.delete(*tree.get_children(node))

    parent = tree.parent(node)
    special_dirs = [] if parent else [os.environ.get('USERPROFILE') or os.path.expanduser('~')]

    for p in special_dirs + os.listdir(path):
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
        elif ptype == 'file':
            size = os.path.getsize(p)
            tree.set(id, "size")

def update_tree(event):
    tree = event.widget
    populate_tree(tree, tree.focus())

def upload_file(tree):
    folder_path = filedialog.askdirectory()  # 打开文件夹选择对话框
    if folder_path:
        load_directory(tree, folder_path)

def load_directory(tree, folder_path):
    tree.delete(*tree.get_children())  # 清空文件树
    node = tree.insert('', 'end', text=folder_path, values=[folder_path, "directory"])
    populate_tree(tree, node)

# root = tk.Tk()
# root.title("文件结构浏览器")
# root.geometry("800x600")

# def tree_view_open(frame):
#     tree = ttk.Treeview(frame, columns=("fullpath", "type", "size"), displaycolumns="size")
#     tree.bind('<<TreeviewOpen>>', update_tree)
#
#     ysb = ttk.Scrollbar(tree, orient='vertical', command=tree.yview)
#     xsb = ttk.Scrollbar(tree, orient='horizontal', command=tree.xview)
#     tree.configure(yscroll=ysb.set, xscroll=xsb.set)
#     ysb.pack(side='right', fill='y')
#     xsb.pack(side='bottom', fill='x')
#     tree.pack(expand='yes', fill='both')

# # 创建上传文件按钮
# upload_button = tk.Button(root, text="上传文件夹", command=upload_file)
# upload_button.pack(pady=10)
#
# root.mainloop()