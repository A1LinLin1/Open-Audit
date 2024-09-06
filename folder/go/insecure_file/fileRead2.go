package main

import (
	"fmt"
	"io"
	"os"
)

func main() {
	// fileName := "/etc/passwd"
	fileName := `C:\Windows\system.ini` // 恶意代码尝试读取敏感文件

	file, err := os.Open(fileName)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close()

	// 创建一个缓冲区来存储文件内容
	buffer := make([]byte, 1024)

	for {
		n, err := file.Read(buffer)
		if err == io.EOF {
			break // 读取到文件末尾，退出循环
		}
		if err != nil {
			fmt.Println("Error reading file:", err)
			break
		}

		// 输出读取的内容到标准输出
		fmt.Print(string(buffer[:n]))
	}
}
