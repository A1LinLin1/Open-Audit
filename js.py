import subprocess

javascript_code = '''console.log("Hello, World!");

'''
result = subprocess.run(['node', '-e', javascript_code], stdout=subprocess.PIPE)
print(result.stdout.decode())
