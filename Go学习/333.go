package main

import (
	"fmt"
	"time"
)

//go语言中channeql和select的应用场景
//消息收发333
//超时机制444
//定时器555

func main() {
	//消息收发
	serverch := make(chan string)
	clientch := make(chan string)
	//服务器消息处理
	go func() {
		for {
			select {
			case msg, ok := <-serverch:
				if !ok {
					fmt.Println("serverch 已关闭")
					break
				}
				fmt.Printf("收到消息：%s\n", msg)
				clientch <- "消息已收到"

			}
		}
	}()
	//客户端消息处理
	go func() {
		for {
			select {
			case msg, ok := <-clientch:
				if !ok {
					fmt.Println("clientch 已关闭")
					break
				}
				fmt.Printf("收到服务器回复：%s\n", msg)

			}
		}

	}()
	serverch <- "Hello, Server!"
	time.Sleep(time.Second * 1)
}
