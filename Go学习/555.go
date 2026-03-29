package main

import (
	"fmt"
	"time"
)

// 定时器
func main() {

	//延迟处理
	// timmr := time.NewTimer(2 * time.Second)
	// fmt.Println(time.Now())
	// <-timmr.C
	// fmt.Println(time.Now())
	t1 := time.Tick(time.Second)
	t3 := time.Tick(time.Second * 3)
	t5 := time.Tick(time.Second * 5)
	for {
		select {
		case <-t1:
			fmt.Println("1秒到了")
		case <-t3:
			fmt.Println("3秒到了")
		case <-t5:
			fmt.Println("5秒到了")
		}
	}
}
