package main

import (
	"gin-ranking/router"
)

func main() {
	r := router.Rrouters()

	r.Run(":9998")

}
