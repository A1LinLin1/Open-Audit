import javalang
import re
import yaml
import astpretty
#读取规则文件
def load_rules(rule_file):
    with open(rule_file, 'r', encoding='utf-8') as file:
        rules = yaml.safe_load(file)
    return rules

# 定义规则匹配函数
def apply_rules(node, rules):
    for rule in rules:
        if rule['type'] == 'ast':
            for pattern in rule['kind']:
                if re.search(pattern, node):
                    print(f"Rule {rule['id']} matched: {rule['name']} - {rule['description']}")

# Java代码示例
java_code = """
public class MaliciousCode {
    public static void main(String[] args) {
        // 触发规则 10001 - 命令执行
        String command = "ls";
        try {
            Runtime.getRuntime().exec(command);
        } catch (Exception e) {
            e.printStackTrace();
        }

        // 触发规则 10002 - 执行命令
        String className = "MaliciousClass";
        byte[] maliciousBytes = { /* 恶意字节码 */ };
        ClassLoader classLoader = new ClassLoader() {
            public Class<?> defineClass(String name, byte[] b) {
                return defineClass(name, b, 0, b.length);
            }
        };
        Class<?> maliciousClass = classLoader.defineClass(className, maliciousBytes);
    }
}

"""

# 解析Java代码为AST
tree = javalang.parse.parse(java_code)

# 从规则文件加载规则
rules = load_rules('java_rules.yml')
#
# # 遍历AST节点并应用规则
for node in tree:
    # 将AST节点转换为字符串，以便与规则进行匹配
    node_str = str(node)
    apply_rules(node_str, rules['rules'])
