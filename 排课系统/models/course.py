from tortoise import fields, models

class Course(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100)
    description = fields.TextField()
    credits = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    teacher = fields.CharField(max_length=100, null=True)
    # schedule 字符串示例： "Mon[1-16;odd] 09:00-11:00; Wed 13:30-15:00"
    schedule = fields.CharField(max_length=255, null=True)
    updated_at = fields.DatetimeField(auto_now=True)
    __table__ = "courses"  # 保持表名不变
    # 如果需要多对多关系，可在 Student 或 Course 中使用 ManyToManyField
