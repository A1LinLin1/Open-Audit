# state_manager.py

# 初始状态为空
state = ""

# 设置文件路径状态的函数
def set_state(value):
    global state
    state = value

# 获取文件路径状态的函数
def get_state():
    return state
