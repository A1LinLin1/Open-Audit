package main

import (
	"fmt"
	"os"
)

func main() {
	maliciousEnv := "PATH=/malicious/bin:$PATH" // 恶意代码尝试修改PATH环境变量
	os.Setenv("EVIL_ENV", maliciousEnv)

	expanded := os.ExpandEnv("$EVIL_ENV")

	fmt.Println("Expanded environment variable:", expanded)
	fmt.Println("PATH:", os.Getenv("EVIL_ENV"))
}
