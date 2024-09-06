package main

import (
	"fmt"
	"io/ioutil"
)

func main() {
	fileName := "./hack" // 恶意代码尝试写入敏感文件
	data := []byte("Malicious content")

	err := ioutil.WriteFile(fileName, data, 0644)
	if err != nil {
		fmt.Println("Error writing file:", err)
	} else {
		fmt.Println("File written successfully")
	}
}
