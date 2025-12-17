from tortoise.models import Model
from tortoise import fields

class Captcha(Model):
    userid = fields.CharField(max_length=255, pk=True)
    code = fields.CharField(max_length=10)
    timestamp = fields.FloatField()

    class Meta:
        table = "captcha"
