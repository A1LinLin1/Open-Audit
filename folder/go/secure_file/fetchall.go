package main

import (
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"os"
)

func main() {
	channel := make(chan string)
	for _, url := range os.Args[1:] {
		go fetch(url, channel)
	}
	for range os.Args[1:] {
		fmt.Println(<-channel)
	}
}

func fetch(url string, channel chan<- string) {
	res, err := http.Get(url)
	if err != nil {
		channel <- fmt.Sprintf("url %v err %v", url, err)
	}
	nbytes, err := io.Copy(ioutil.Discard, res.Body)
	res.Body.Close()
	if err != nil {
		channel <- fmt.Sprintf("url %v err %v", url, err)
	}
	channel <- fmt.Sprintf("url %v res %6d bytes", url, nbytes)
}
