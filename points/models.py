from django.db import models
from datetime import datetime


class Payer(models.Model):
    name = models.CharField(max_length=255)
    total_points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/payer'
    

class Transaction(models.Model):
    payer = models.ForeignKey(
        'payer',
        on_delete=models.CASCADE
    )
    points = models.IntegerField()
    timestamp = models.DateTimeField(default=datetime.now)
    remaining_points = models.IntegerField(default=0, blank=True, null=True)

    def get_absolute_url(self):
        return '/transaction'


class Spend(models.Model):
    points = models.PositiveIntegerField(default=0)
    receipt = models.JSONField()

    def get_absolute_url(self):
        return '/spend'
