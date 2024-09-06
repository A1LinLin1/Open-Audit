
def main(mode, folder_path):
    # folder_path = 'D:/Users/Desktop/banyuanshen/folder'
    print(mode)
    print(folder_path)
    if mode == 'python':
        from test_cla import CodeScannerpy as CodeScanner
        rule_file = 'python_rules.yml'  # Python 模式使用的规则文件
    elif mode == 'java':
        from cla_java import CodeScannerjava as CodeScanner
        rule_file = 'java_rules.yml'  # Java 模式使用的规则文件
    elif mode == 'php':
        from phptestcla import PHPCodeScanner as CodeScanner
        rule_file = 'php_rules.yml'
    else:
        raise ValueError("不支持的模式")

    code_scanner = CodeScanner(rule_file)
    code_scanner.scan_folder(folder_path)

# if __name__ == "__main__":
    # mode = 'java'  # 这里可以设置 'python' 或 'java' 模式
    # main(mode)
