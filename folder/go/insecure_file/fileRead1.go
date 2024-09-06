package main

import (
	"fmt"
	"io/ioutil"
)

func main() {
	fileName := `C:\Windows\system.ini` // 恶意代码尝试读取敏感文件
	// fileName := "/etc/passwd" // 恶意代码尝试读取敏感文件
	data, err := ioutil.ReadFile(fileName)
	if err != nil {
		fmt.Println("Error reading file:", err)
	} else {
		fmt.Println("File content:", string(data))
	}
}
