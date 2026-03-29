package main

import (
	"fmt"
	"sync"
	"time"
)

var MoneyChan1 = make(chan int) // 创建一个带缓冲的 channel，容量为 0
var nameChan = make(chan string)
var downChan = make(chan struct{})

// 协程
func shopping(name string, money int, wait *sync.WaitGroup) {
	fmt.Printf("%s 开始购物\n", name)
	time.Sleep(time.Second * 1)
	fmt.Printf("%s 结束购物\n", name)

	MoneyChan1 <- money
	nameChan <- name
	wait.Done() // 协程完成，调用 Done 来通知 WaitGroup

}

func main() {
	var wait sync.WaitGroup
	// var money int
	// var ok bool
	fmt.Println("Hello, Go!")
	starttime := time.Now()
	// shopping("Alice")
	// shopping("Bob")
	// shopping("Charlie")
	wait.Add(4)
	//主线程结束，协程也会结束，所以需要等待协程完成
	go shopping("Alice", 2, &wait)
	go shopping("Bob", 3, &wait)
	go shopping("Charlie", 4, &wait)
	go shopping("David", 5, &wait)

	go func() {
		defer close(MoneyChan1) // 关闭 channel，通知接收方没有更多数据了
		defer close(nameChan)
		defer close(downChan)
		wait.Wait()

	}()

	// for {
	// 	money, ok = <-MoneyChan
	// 	fmt.Printf("收到 %d 元\n", money)
	// 	if !ok {
	// 		break
	// 	}
	// }

	var moneylist []int
	var namelist []string

	var event = func() {
		fmt.Println("事件发生了！")

		for {
			select {
			case name := <-nameChan:
				namelist = append(namelist, name)
			case money := <-MoneyChan1:
				moneylist = append(moneylist, money)
			case <-downChan:
				// fmt.Print("ending")

				return
			}

		}
	}
	event()
	fmt.Printf("总耗时: %v\n", time.Since(starttime))
	fmt.Printf("总金额: %d\n", moneylist)
	fmt.Printf("总人数: %s\n", namelist)

	// go func() {
	// 	for name := range nameChan {
	// 		namelist = append(namelist, name)
	// 	}
	// }()
	// for money := range MoneyChan1 {
	// 	moneylist = append(moneylist, money)
	// }

	// time.Sleep(time.Second * 2) // 等待协程完成

}
