package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	output := bufio.NewWriter(os.Stdout)
	counts := make(map[string]int)
	files := os.Args[1:]
	if len(files) == 0 {
		output.WriteString("file name")
		output.Flush()
	} else {
		for _, arg := range files {
			f, err := os.Open(arg)
			if err != nil {
				output.WriteString("open failed")
				output.Flush()
			} else {
				countLines(f, counts)
				f.Close()
			}
		}

		for line, n := range counts {
			fmt.Printf("%s %d\n", line, n)
		}
	}
}

func countLines(f *os.File, counts map[string]int) {
	input := bufio.NewScanner(f)
	for input.Scan() {
		counts[input.Text()]++
	}
}
