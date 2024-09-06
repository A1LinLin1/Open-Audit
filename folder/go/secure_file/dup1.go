package main

import (
	"bufio"
	"os"
)

func main() {
	counts := make(map[string]int)
	input := bufio.NewScanner(os.Stdin)
	output := bufio.NewWriter(os.Stdout)
	for input.Scan() {
		counts[input.Text()]++
	}
	for line, _ := range counts {
		output.WriteString(line + "\n")
		output.Flush()
		// fmt.Printf("%s\n", line)
	}
}
