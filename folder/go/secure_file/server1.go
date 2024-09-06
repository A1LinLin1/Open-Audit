package main

import (
	"fmt"
	"log"
	"net/http"
)

func main() {
	http.HandleFunc("/", webHandler)
	log.Fatal(http.ListenAndServe("127.0.0.1:8000", nil))
}

func webHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "url: %q\n", r.URL.Path)
}
