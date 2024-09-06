import ast
import re
import json
import astpretty
import yaml
import os

class CodeScanner:
    def __init__(self, rule_file, mode):
        self.rules = self.load_rules(rule_file)
        self.json_file_name = "results.json"
        self.match_count = 1
        self.mode = mode  # 将 mode 参数传递给类属性

    def load_rules(self, rule_file):
        with open(rule_file, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            rules = data.get('rules')
        return rules

    def apply_rules(self, python_file):
        try:
            with open(python_file, 'r', encoding='utf-8') as file:
                python_code = file.read()
        except FileNotFoundError:
            python_code = "文件未找到"
        except Exception as e:
            python_code = f"发生了一个错误: {e}"

        python_ast = ast.parse(python_code)

        for node in ast.walk(python_ast):
            if isinstance(node, ast.Call):
                node_str = ast.dump(node)
                matched_data = self.match_rules(node_str, python_file)
                self.save_matched_data(matched_data)

    def match_rules(self, node, python_file):
        matched_data = []

        for rule in self.rules:
            if rule['type'] == 'regex':
                for pattern in rule['patterns']:
                    if re.search(pattern, node):
                        matched_item = {
                            "ID": str(self.match_count),
                            "文件路径": python_file,
                            "漏洞描述": rule['name'],
                            "漏洞详细": rule['description']
                        }
                        matched_data.append(matched_item)
                        self.match_count += 1

        return matched_data

    def save_matched_data(self, matched_data):
        try:
            with open(self.json_file_name, "r", encoding='utf-8') as json_file:
                existing_data = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []

        existing_data.extend(matched_data)

        with open(self.json_file_name, "w", encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, ensure_ascii=False, indent=4)

    def scan_folder(self, folder_path):
        # 根据 mode 决定要处理的文件扩展名
        if self.mode == "python":
            file_extension = '.py'
        elif self.mode == "java":
            file_extension = '.java'
        else:
            raise ValueError("不支持的文件类型")

        # 遍历文件夹中的所有指定扩展名的文件
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(file_extension):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            file_code = file.read()
                    except FileNotFoundError:
                        file_code = "文件未找到"
                    except Exception as e:
                        file_code = f"发生了一个错误: {e}"

                    self.apply_rules(file_code, file_path)




