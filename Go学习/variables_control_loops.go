package main

import (
	"fmt"
	"strconv"
)

func main() {
	// 变量声明
	var a int = 10
	var b = 20 // 类型推断
	c := 30    // 简短声明

	fmt.Println("变量 a:", a)
	fmt.Println("变量 b:", b)
	fmt.Println("变量 c:", c)

	// 条件语法
	if a < b {
		fmt.Println("a 小于 b")
	} else if a == b {
		fmt.Println("a 等于 b")
	} else {
		fmt.Println("a 大于 b")
	}

	// switch 语法
	switch a {
	case 10:
		fmt.Println("a 是 10")
	case 20:
		fmt.Println("a 是 20")
	default:
		fmt.Println("a 不是 10 或 20")
	}

	// for 循环
	for i := 0; i < 5; i++ {
		fmt.Println("循环 i:", i)
	}

	// for 循环作为 while 使用
	n := 0
	for n < 5 {
		fmt.Println("while 循环 n:", n)
		n++
	}

	// 无限循环
	count := 0
	for {
		fmt.Println("无限循环 count:", count)
		count++
		if count == 3 {
			break // 退出循环
		}
	}
}

// 以下示例演示基本类型以及常用的类型转换：
// - 整型与浮点型之间的转换
// - 数字与字符串之间的转换
// - 布尔与字符串之间的转换
func typeAndConversionExamples() {
	fmt.Println("\n--- 类型 与 类型转换 示例 ---")

	// 整型（带注释帮助从 Python/C++ 转来学习的人）
	// - Go 中的整型有带符号和无符号：int8/uint8, int16/uint16, int32/uint32, int64/uint64。
	// - `int` 和 `uint` 是平台相关大小（至少 32 位），在 64 位系统通常是 64 位。
	// - 与 Python 不同：Python 的 int 是任意精度的；与 C++ 不同：C++ 的 int 大小随平台但通常为 32 位。
	// - 使用不同长度的整型能节省内存或与外部格式（协议/文件）对齐，但会增加类型转换成本。
	// - 不同整型间不能隐式转换，需要显式转换，例如 `int32(x)` 或 `int(x)`。
	var i int = 42         // 默认整型（平台相关大小）
	var i8 int8 = -8       // 8 位带符号
	var u8 uint8 = 250     // 8 位无符号
	var i32 int32 = 32000  // 32 位带符号
	var i64 int64 = 1234567890
	var u64 uint64 = 18446744073709551615
	fmt.Println("i (int):", i, "i8 (int8):", i8, "u8 (uint8):", u8)
	fmt.Println("i32 (int32):", i32, "i64 (int64):", i64, "u64 (uint64):", u64)

	// 示例：不同整型之间需要显式转换
	// 下面将 int 转为 int32（可能截断/溢出，需注意）
	iToI32 := int32(i)
	fmt.Println("int -> int32:", iToI32)

	// 浮点型
	var f64 float64 = 3.1415
	var f32 float32 = 2.718
	fmt.Println("f64 (float64):", f64, "f32 (float32):", f32)

	// 布尔
	b := true
	fmt.Println("b (bool):", b)

	// 字符串
	s := "123"
	fmt.Println("s (string):", s)

	// int -> float64
	fFromInt := float64(i)
	fmt.Println("int -> float64:", fFromInt)

	// float64 -> int（截断小数部分）
	iFromFloat := int(f64)
	fmt.Println("float64 -> int (截断):", iFromFloat)

	// int -> string
	sFromInt := strconv.Itoa(i)
	fmt.Println("int -> string:", sFromInt)

	// string -> int
	iFromString, err := strconv.Atoi(s)
	if err != nil {
		fmt.Println("strconv.Atoi 错误:", err)
	} else {
		fmt.Println("string -> int:", iFromString)
	}

	// float -> string
	sFromFloat := fmt.Sprintf("%f", f64)
	fmt.Println("float64 -> string:", sFromFloat)

	// string -> float64
	fFromString, err := strconv.ParseFloat("3.14", 64)
	if err != nil {
		fmt.Println("strconv.ParseFloat 错误:", err)
	} else {
		fmt.Println("string -> float64:", fFromString)
	}

	// bool -> string
	sFromBool := strconv.FormatBool(b)
	fmt.Println("bool -> string:", sFromBool)

	// string -> bool
	boolFromString, err := strconv.ParseBool("true")
	if err != nil {
		fmt.Println("strconv.ParseBool 错误:", err)
	} else {
		fmt.Println("string -> bool:", boolFromString)
	}

	// 注意：有些转换（如 string->int/float/bool）会返回错误，需检查。
}

func init() {
	// 在程序启动时调用示例函数，保持 main 中已有示例不变
	typeAndConversionExamples()
}