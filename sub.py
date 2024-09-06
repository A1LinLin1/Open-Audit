import subprocess
import os

# 获取当前脚本的目录
current_directory = os.path.dirname(os.path.realpath(__file__))

# 构建JavaScript文件的绝对路径
js_file_path = os.path.join(current_directory, 'php.js')

# 使用subprocess运行Node.js并执行JavaScript文件
result = subprocess.run(['node', js_file_path], stdout=subprocess.PIPE, text=True)

# 输出JavaScript脚本的标准输出
print(result.stdout)
