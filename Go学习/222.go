package main

import (
	"errors"
	"fmt"
)

//向上抛
func div(a, b int) (result int, err error) {
	if b == 0 {
		err = errors.New("除数不能为0")
		return
	}
	result = a / b
	return
}
	

func server() (int, error) {
	res, err := div(10, 0)
	if err != nil {
		return 0, err
	}
	res++
	res += 100
	return res, nil
}
func main() {
	res, err := server()
	if err != nil {
		fmt.Println("调用 server 失败：", err)
		return
	}
	fmt.Println("server 返回 res =", res)
}
