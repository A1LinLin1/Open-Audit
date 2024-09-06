package main

import (
	"fmt"
	"io"
	"os"
)

func main() {
	// fileName := "/tmp/sample.txt"
	fileName := "./hack" // 恶意代码尝试写入敏感文件

	file, err := os.Create(fileName)
	if err != nil {
		fmt.Println("Error creating file:", err)
		return
	}
	defer file.Close()

	// 写入数据到文件
	data := "hacked"
	_, err = io.WriteString(file, data)
	if err != nil {
		fmt.Println("Error writing to file:", err)
		return
	}

	fmt.Println("File created and data written successfully")
}
