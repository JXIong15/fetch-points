from django.contrib import admin
from .models import Payer, Transaction, Spend


class PayerAdmin(admin.ModelAdmin):
    search_fields = [
        "name",
    ]
    list_display = [
        "id",
        "name",
        "total_points",
    ]


class TransactionAdmin(admin.ModelAdmin):
    search_fields = [
        "payer",
    ]
    list_display = [
        "id",
        "payer",
        'points',
        'timestamp',
        'remaining_points'
    ]


class SpendAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "points",
        "receipt"
    ]


admin.site.register(Payer, PayerAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Spend, SpendAdmin)
