from django.db import models


class Payer(models.Model):
    name = models.CharField(max_length=255)
    total_points = models.PositiveIntegerField(default=0)
    

class Transaction(models.Model):
    payer = models.ForeignKey(
        'payer',
        on_delete=models.CASCADE
    )
    points = models.PositiveIntegerField()
    timestamp = models.DateTimeField()