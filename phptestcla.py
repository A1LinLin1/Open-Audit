import os
import re
import json
import subprocess
import yaml

class PHPCodeScanner:
    def __init__(self, rule_file,):
        self.rules = self.load_rules(rule_file)
        self.json_file_name = "results.json"
        self.match_count = 1

    def load_rules(self, rule_file):
        with open(rule_file, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            rules = data.get('rules')
        return rules

    def apply_rules(self, node,file):
        matched_data = []
        for rule in self.rules:
            if rule['type'] == 'regex':
                for pattern in rule['kind']:
                    if re.search(pattern, node):
                        #print(node)
                        i=int(node[-2])
                        try:
                            with open(file, 'r',encoding='utf-8') as f:
                                lines = f.readlines()
                                if i <= len(lines):
                                    print(lines[i - 1])  # 索引从0开始，所以我们使用 i - 1
                                else:
                                    print(f"The file has less than {i} lines")
                        except FileNotFoundError:
                            print("The file was not found")
                        except IndexError:
                            print("Invalid line number")
                        matched_item = {
                            "ID": str(self.match_count),
                            "文件路径": file , # 你需要提供文件路径信息
                            "漏洞描述": rule['description'],
                            "漏洞详细": '第'+node[-2]+'行：'+lines[i - 1]
                        }
                        matched_data.append(matched_item)
                        self.match_count += 1
                        #print(matched_item)
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
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.php'):
                    file_path = os.path.join(root, file)
                    result = subprocess.run(['node', './php.js'], stdout=subprocess.PIPE, text=True, input=file_path,encoding='utf-8')
                    ast_test = result.stdout
                    ast_tree = json.loads(ast_test)

                    for child in ast_tree:
                        # php_code = ''.join(token[1] for token in child)
                        #print(child)
                        matched_data = self.apply_rules(str(child),file_path)
                        self.save_matched_data(matched_data)

# 使用示例
# 使用示例

