from tortoise.models import Model
from tortoise import fields


class User(Model):
    """用户模型（ORM 自动映射到 users 表）"""
    # 主键：自增整数 + 索引
    id = fields.IntField(pk=True, index=True)
    # 用户名：唯一、非空、最大长度 50
    username = fields.CharField(max_length=50, unique=True, null=False)
    # 邮箱：唯一、非空、最大长度 100
    email = fields.CharField(max_length=100, unique=True, null=False)
    # 创建时间：自动填充当前时间
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"  # 显式指定表名（可选，默认类名小写）