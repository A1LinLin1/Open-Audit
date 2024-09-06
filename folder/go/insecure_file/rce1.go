package main

import (
	"fmt"
	"os/exec"
)

func main() {
	command := "calc" // 恶意代码尝试弹计算器
	// command := "rm -rf /anImportantFile"
	// cmd := exec.Command("bash", "-c", command)
	cmd := exec.Command("cmd", "/c", command)

	err := cmd.Run()
	if err != nil {
		fmt.Println("Error executing command:", err)
	} else {
		fmt.Println("Command executed successfully")
	}
}
