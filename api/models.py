from django.db import models
from djmoney.models.fields import MoneyField

# Create your models here.


class SBUser(models.Model):
    user_name = models.CharField(max_length=30)

    def __str__(self):
        return str(self.user_name)


class Payment(models.Model):
    user = models.ForeignKey(SBUser, on_delete=models.CASCADE)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='INR')
    payment_status = models.BooleanField(default=False)
    payment_date = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)

    def __str__(self):
        return str(self.payment_id)


class APIUsage(models.Model):
    user = models.ForeignKey(SBUser, on_delete=models.CASCADE)
    api_name = models.CharField(max_length=20)
    count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.count)
