package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
)

func main() {
	for _, url := range os.Args[1:] {
		// var response string
		if (strings.HasPrefix(url, "http://") || strings.HasPrefix(url, "https://")) == false {
			url = "https://" + url
		}
		resp, err := http.Get(url)
		if err != nil {
			fmt.Printf("err:%v\n", err)
		}
		// response, err := ioutil.ReadAll(resp.Body)
		io.Copy(os.Stdout, resp.Body)
		// if err != nil {
		// 	fmt.Printf("err:%v\n", err)
		// 	os.Exit(1)
		// }
		// fmt.Printf("%s", response)

	}
}
