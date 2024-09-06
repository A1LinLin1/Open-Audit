package main

import (
	"fmt"
	"log"
	"net/http"
	"sync"
)

var mu sync.Mutex
var count int

func main() {
	http.HandleFunc("/", rootHandler)
	http.HandleFunc("/count", countHandler)
	log.Fatal(http.ListenAndServe("127.0.0.1:8000", nil))
}

func rootHandler(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	count++
	mu.Unlock()
	fmt.Fprintf(w, "url:%q\n", r.URL.Path)
	if err := r.ParseForm(); err != nil {
		fmt.Fprintf(w, "err: %v", err)
	}
	for k, v := range r.Form {
		fmt.Fprintf(w, "form[%q]:%q\n", k, v)
	}
}

func countHandler(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	fmt.Fprintf(w, "total count: %d", count)
	mu.Unlock()
}
