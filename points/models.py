from django.db import models
from datetime import datetime


class Payer(models.Model):
    name = models.CharField(max_length=255)
    total_points = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    

class Transaction(models.Model):
    payer = models.ForeignKey(
        'payer',
        on_delete=models.CASCADE
    )
    points = models.IntegerField()
    timestamp = models.DateTimeField(default=datetime.now)
    remaining_points = models.IntegerField(default=0, blank=True, null=True)


class Spend(models.Model):
    points = models.PositiveIntegerField(default=0)
    receipt = models.JSONField()

