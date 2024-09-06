import ast
import re
import json
import astpretty
import yaml
import os

class CodeScannerpy:
    def __init__(self, rule_file):
        self.rules = self.load_rules(rule_file)
        self.json_file_name = "results.json"
        self.match_count = 1

    def load_rules(self, rule_file):
        with open(rule_file, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            rules = data.get('rules')
        return rules

    # def apply_rules(self, python_file):
    #     try:
    #         with open(python_file, 'r', encoding='utf-8') as file:
    #             python_code = file.read()
    #     except FileNotFoundError:
    #         python_code = "文件未找到"
    #     except Exception as e:
    #         python_code = f"发生了一个错误: {e}"
    #
    #     python_ast = ast.parse(python_code)

        # for node in ast.walk(python_ast):
        #     if isinstance(node, ast.Call):
        #         node_str = ast.dump(node)
        #         matched_data = self.match_rules(node_str, python_file)
        #         self.save_matched_data(matched_data)

    def match_rules(self, node, python_file,line_number):
        matched_data = []

        for rule in self.rules:
            if rule['type'] == 'regex':
                for pattern in rule['patterns']:
                    if re.search(pattern, node):
                        # if re.search(name,node)
                        try:
                            with open(python_file, 'r',encoding='utf-8') as f:
                                lines = f.readlines()
                                if line_number <= len(lines):
                                    theline=lines[line_number - 1]
                                else:
                                    print(f"The file has less than {line_number} lines")
                                    theline=f"The file has less than {line_number} lines"
                        except FileNotFoundError:
                            theline="The file was not found"
                            print("The file was not found")
                        except IndexError:
                            theline = "Invalid line number"
                            print("Invalid line number")
                        matched_item = {
                            "ID": str(self.match_count),
                            "文件路径": python_file,
                            "漏洞描述": rule['description'],
                            "漏洞详细": '第'+str(line_number)+'行:'+theline#rule['description']
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
        # 遍历文件夹中的所有 .py 文件
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.py'):
                    python_file = os.path.join(root, file)
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
                            line_number = node.lineno = node.lineno
                            matched_data = self.match_rules(node_str, python_file,line_number)
                            self.save_matched_data(matched_data)



