from django import forms
from .models import Payer, Transaction, Spend


class PayerCreateForm(forms.ModelForm):
    class Meta:
        model = Payer
        fields = ('name',)


class PayerUpdateForm(forms.ModelForm):
    class Meta:
        model = Payer
        fields = ('name', 'total_points')
        
        
class TransactionCreateForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('payer', 'points', 'timestamp',)


class SpendCreateForm(forms.ModelForm):
    class Meta:
        model = Spend
        fields = ('points',)