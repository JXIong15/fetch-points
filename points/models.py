from django.db import models


class Payer(models.Model):
    name = models.CharField(max_length=255)
    total_points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/'
    

class Transaction(models.Model):
    payer = models.ForeignKey(
        'payer',
        on_delete=models.CASCADE
    )
    points = models.IntegerField()
    timestamp = models.DateTimeField()

    def get_absolute_url(self):
        return '/'