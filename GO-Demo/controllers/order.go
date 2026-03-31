package controllers

import (
	"github.com/gin-gonic/gin"
)

type OrderController struct{}

type OrderInfo struct {
	Cid  string `json:"cid"`
	Name string `json:"name"`
}

func (o OrderController) GetOrderInfo(c *gin.Context) {
	// cid := c.PostForm("cid")
	// name := c.DefaultPostForm("name", "wangwu")
	// param := make(map[string]interface{})
	// err := c.BindJSON(&param)

	search := &OrderInfo{}
	err := c.BindJSON(&search)
	if err != nil {
		ReturnError(c, 1, gin.H{
			"error": err.Error(),
		})
		return
	}

	ReturnSuccess(c, 0, 18, search.Cid)
}
