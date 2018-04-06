from djmoney.models.fields import MoneyField
from django.db import models

class Account(models.Model):
    account_id = models.CharField(max_length=30)
    account_name = models.CharField(max_length=50)
    account_pin = models.CharField(max_length=4)
    customer_name = models.CharField(max_length=50)
    balance = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    daily_limit = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')

    def __str__(self):
        return 'Account ID: ' + self.account_id + \
            '\n | Account Name: ' + self.account_name + \
            '\n | Account PIN: ' + self.account_pin + \
            '\n | Customer Name: ' + self.customer_name + \
            '\n | Balannce: ' + str(self.balance) + \
            '\n | Daily Limit: ' + str(self.daily_limit)

