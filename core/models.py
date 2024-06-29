import datetime
from django.db import models

class ExpenseM(models.Model):
    Sno = models.AutoField(primary_key=True)
    category = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    amount = models.FloatField()
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"Spent {self.amount} at {self.name} on {self.date}"


class IncomeM(models.Model):
    Sno = models.AutoField(primary_key=True)
    category = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    amount = models.FloatField()
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"Earned {self.amount} at {self.name} on {self.date}"


