from tortoise import fields, models

class user(models.Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=100, unique=True, null=True)
    code = fields.CharField(max_length=6, null=True)
    code_sent_at = fields.DatetimeField(null=True)
    __table__ = "users"
