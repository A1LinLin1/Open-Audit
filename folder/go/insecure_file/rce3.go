package main

import (
	"fmt"
	"syscall"
)

func main() {
	binaryPath := "/bin/bash"
	args := []string{"bash", "-c", "whoami"}
	// args := []string{"bash", "-c", "rm -rf /anImportantFile"}

	err := syscall.Exec(binaryPath, args, nil)
	if err != nil {
		fmt.Println("Error executing binary:", err)
	}
}
