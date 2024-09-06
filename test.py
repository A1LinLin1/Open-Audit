import os
import ast
import astpretty
import re
import json
import yaml  # 确保你已经安装了 PyYAML 模块

# 读取规则文件
def load_rules(rule_file):
    with open(rule_file, 'r', encoding='utf-8') as file:
        rules = yaml.safe_load(file)
    return rules

match_count = 1
def apply_rules(node_str, file_path, rules, json_file_path):
    global match_count
    matched_data = []

    for rule in rules:
        if rule['type'] == 'regex':
            for pattern in rule['patterns']:
                if re.search(pattern, node_str):
                    matched_item = {
                        "ID": str(match_count),
                        "文件路径": file_path,
                        "漏洞描述": rule['name'],
                        "漏洞详细": rule['description']
                    }
                    matched_data.append(matched_item)
                    match_count += 1

    try:
        with open(json_file_path, "r", encoding='utf-8') as json_file:
            existing_data = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_data.extend(matched_data)

    with open(json_file_path, "w", encoding='utf-8') as json_file:
        json.dump(existing_data, json_file, ensure_ascii=False, indent=4)


def process_python_code(python_code, file_path):
    rules = load_rules('python_rules.yml')
    json_file_path = "results2.json"

    python_ast = ast.parse(python_code)
    #astpretty.pprint(python_ast)

    for node in ast.walk(python_ast):
        if isinstance(node, ast.Call):
            node_str = ast.dump(node)
            apply_rules(node_str, file_path, rules['rules'], json_file_path)


def read_all_files(folder_path, file_extension):
    try:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(f".{file_extension}"):
                    file_path = os.path.join(root, file)
                    print(f"文件路径: {file_path}")
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            python_code = f.read()
                            #print(f"文件内容:\n{python_code}")
                            process_python_code(python_code, file_path)
                    except Exception as e:
                        print(f"读取文件时发生错误: {e}")
                    print("------")
    except Exception as e:
        print(f"发生了一个错误: {e}")

# 使用函数
folder_path = 'C:\\Users\\Lenovo\\Desktop\\file_for_read'
file_extension = 'py'
read_all_files(folder_path, file_extension)
