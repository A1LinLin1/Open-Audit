package main

import (
    "fmt"
    "go/parser"
    "go/token"
    "os"
)

func main() {
    if len(os.Args) != 2 {
        fmt.Println("Usage: go_to_ast <go_file>")
        os.Exit(1)
    }

    filePath := os.Args[1]
    fset := token.NewFileSet()
    node, err := parser.ParseFile(fset, filePath, nil, parser.AllErrors)
    if err != nil {
        fmt.Println("Error parsing Go file:", err)
        os.Exit(1)
    }

    fmt.Println("AST:")
    fmt.Println(node)
}
