package models

import (
	"errors"

	"gin-ranking/core"
	"gin-ranking/dao"
	"time"

	"gorm.io/gorm"
)

var ErrEmailExists = errors.New("email already registered")

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
	db := dao.GetDB()
	var existing User
	if err := db.Where("email = ?", email).First(&existing).Error; err == nil {
		return 0, ErrEmailExists
	} else if !errors.Is(err, gorm.ErrRecordNotFound) {
		return 0, err
	}

	hashed, err := core.HashPassword(password)
	if err != nil {
		return 0, err
	}

	user := User{
		Email:    email,
		Password: string(hashed),
	}
	createErr := db.Create(&user).Error
	return user.ID, createErr
}

func UpdateUser(id int, email string) (int, error) {
	dao.GetDB().Model(&User{}).Where("id=?", id).Update("email", email)
	return id, nil

}
