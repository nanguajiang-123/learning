package main

import (
	"errors"
	"fmt"
	"time"
)

// 这是一些中级 Go 语言特性的示例：函数、方法、接口、错误处理、goroutine、channel、泛型等。

// 多返回值示例
func swap(a, b string) (string, string) { return b, a }

// 命名返回值示例
func namedDouble(a int) (double int) { double = a * 2; return }

// 可变参数示例
func sum(nums ...int) int {
	s := 0
	for _, v := range nums {
		s += v
	}
	return s
}

// 接口与方法示例
type Calculator interface {
	Add(a, b int) int
	Divide(a, b int) (int, error)
}

type SimpleCalc struct{}

func (s SimpleCalc) Add(a, b int) int { return a + b }

func (s SimpleCalc) Divide(a, b int) (int, error) {
	if b == 0 {
		return 0, errors.New("divide by zero")
	}
	return a / b, nil
}

// 泛型示例（Go 1.18+）: 对 slice 做映射
func MapSlice[T any, U any](slice []T, fn func(T) U) []U {
	res := make([]U, 0, len(slice))
	for _, v := range slice {
		res = append(res, fn(v))
	}
	return res
}

// goroutine + channel 示例：消费者
func worker(ch <-chan int, done chan<- bool) {
	for v := range ch {
		fmt.Println("worker got", v)
	}
	done <- true
}

func main() {
	fmt.Println("--- 中级 Go 示例开始 ---")

	// 函数用法
	a, b := swap("hello", "world")
	fmt.Println("swap:", a, b)
	fmt.Println("namedDouble:", namedDouble(5))
	fmt.Println("sum:", sum(1, 2, 3, 4))

	// 接口与方法
	var c Calculator = SimpleCalc{}
	fmt.Println("Add:", c.Add(10, 5))
	if q, err := c.Divide(10, 0); err != nil {
		fmt.Println("Divide error:", err)
	} else {
		fmt.Println("Divide result:", q)
	}

	// 泛型
	nums := []int{1, 2, 3}
	squares := MapSlice(nums, func(i int) int { return i * i })
	fmt.Println("squares:", squares)

	// goroutine + channel
	ch := make(chan int) // 无缓冲 channel
	done := make(chan bool)
	go func() {
		for i := 0; i < 3; i++ {
			ch <- i
		}
		close(ch)
	}()
	go worker(ch, done)
	<-done
	fmt.Println("goroutine done")

	// defer / panic / recover 示例
	func() {
		defer func() {
			if r := recover(); r != nil {
				fmt.Println("recovered:", r)
			}
		}()
		panic("示例 panic：recover 可捕获")
	}()

	// 等待少许时间以确保所有输出完成
	time.Sleep(50 * time.Millisecond)
	fmt.Println("--- 示例结束 ---")
}
