import ast
import re
import astpretty
import glob
import os



# 读取规则文件
def load_rules(rule_file):
    with open(rule_file, 'r', encoding='utf-8') as file:
        import yaml
        rules = yaml.safe_load(file)
    return rules


# 定义规则匹配函数
def apply_rules(node, rules):
    for rule in rules:
        if rule['type'] == 'regex':
            for pattern in rule['patterns']:
                if re.search(pattern, node):
                    print(f"Rule {rule['id']} matched: {rule['name']} - {rule['description']}")


# 定义审核文件夹的路径
folder_path = "/path/to/your/folder"  # 将路径替换为您的文件夹路径

# 获取文件夹中所有的 .py 文件
python_files = glob.glob(os.path.join(folder_path, "*.py"))

# 从规则文件加载规则
rules = load_rules('python_rules.yml')

# 遍历每个 .py 文件并执行审核
for python_file in python_files:
    with open(python_file, 'r', encoding='utf-8') as file:
        python_code = file.read()

    # 解析Python代码为AST
    python_ast = ast.parse(python_code)
    astpretty.pprint(python_ast)  # 注释：如果想看AST结构去掉注释

    # 遍历AST节点并应用规则
    for node in ast.walk(python_ast):
        if isinstance(node, ast.Call):
            # 将AST节点转换为字符串，以便与规则进行匹配
            node_str = ast.dump(node)
            apply_rules(node_str, rules['rules'])
