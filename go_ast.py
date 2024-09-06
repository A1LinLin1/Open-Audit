import subprocess

go_script = "go run ../go_to_ast/go_to_ast.go ../hello/hello.go"
result = subprocess.run(go_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)

if result.returncode == 0:
    # 打印Go代码的AST
    print("Go AST:")
    print(result.stdout)
else:
    # 处理错误
    print("Error:", result.stderr)
