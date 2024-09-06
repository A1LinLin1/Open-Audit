from cla import  CodeScanner
def main():
    rule_file = 'python_rules.yml'  # 请替换为实际的规则文件路径
    folder_path = 'Z:/p1nk/BUPT/A_scan/YIBAN/new/folder/'

    # 选择要处理的文件类型模式：python 或 java
    mode = "python"  # 可以根据需要修改为 "java"

    code_scanner = CodeScanner(rule_file, mode)
    code_scanner.scan_folder(folder_path)

if __name__ == "__main__":
    main()