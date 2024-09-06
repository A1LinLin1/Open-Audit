package main

import (
	"fmt"
	"plugin"
)

func main() {
	pluginPath := "/path/to/malicious/plugin.so" // 恶意代码尝试加载恶意插件

	p, err := plugin.Open(pluginPath)
	if err != nil {
		fmt.Println("Error opening plugin:", err)
		return
	}

	// 恶意代码尝试从插件中调用恶意函数
	maliciousFunc, err := p.Lookup("MaliciousFunction")
	if err != nil {
		fmt.Println("Error looking up function:", err)
		return
	}

	// 调用恶意函数
	maliciousFunc.(func())()
}
