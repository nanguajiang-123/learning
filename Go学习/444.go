package main

import (
	"fmt"
	"time"
)

//超时机制

func main() {

	done := make(chan bool)
	go func() {
		time.Sleep(2 * time.Second)
		done <- true
	}()
	select {
	case <-done:
		fmt.Println("操作完成")
	case <-time.After(13 * time.Second):
		fmt.Println("操作超时")
	}
}
