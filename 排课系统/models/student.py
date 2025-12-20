
from tortoise import fields, models

class Student(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    grade = fields.IntField()
    email = fields.CharField(max_length=100, unique=True)
    enrolled_date = fields.DatetimeField(auto_now_add=True)
    is_active = fields.BooleanField(default=True)

    # 密码哈希与验证码字段
    password_hash = fields.CharField(max_length=128, null=True)
    courses = fields.ManyToManyField('models.Course', related_name='students')
    __table__ = "students"  
   
