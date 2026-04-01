package models

import (
	"gin-ranking/dao"
	"time"
)

type User struct {
	ID        uint
	Email     string
	Password  string
	Salt      string
	CreatedAt time.Time
}

func (User) TableName() string {
	return "users"
}

func GetUserTest(id int) (User, error) {
	var user User
	err := dao.GetDB().Where("id=?", id).First(&user).Error
	return user, err
}

func AddUser(email string, password string) (uint, error) {
	user := User{
		Email:    email,
		Password: password,
	}
	err := dao.GetDB().Create(&user).Error
	return user.ID, err

}

func UpdateUser(id int, email string) (int, error) {
	dao.GetDB().Model(&User{}).Where("id=?", id).Update("email", email)
	return id, nil

}
