package main

import (
	"fmt"
	"os/exec"
)

func main() {
	// command := "rm -rf /anImportantFile"
	command := "calc" // 恶意代码尝试弹计算器
	// cmd := exec.Command("bash", "-c", command)
	cmd := exec.Command("cmd", "/c", command)

	err := cmd.Start()
	if err != nil {
		fmt.Println("Error executing command:", err)
	} else {
		fmt.Println("Command started successfully")
	}
}
