from tortoise import fields, models

class Course(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100)
    description = fields.TextField()
    credits = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    __table__ = "courses"  # 保持表名不变
    # 如果需要多对多关系，可在 Student 或 Course 中使用 ManyToManyField
