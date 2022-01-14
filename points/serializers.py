from rest_framework import serializers
from .models import Payer, Transaction, Spend


class PayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payer
        fields = [
            'id',
            'name',
            'total_points',
        ]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'payer', 'points', 'timestamp', 'remaining_points',]


class SpendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spend
        fields = [
            'id',
            'points',
            'receipt',
        ]
