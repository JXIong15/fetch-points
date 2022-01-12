from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Payer, Transaction
from .forms import PayerCreateForm, PayerUpdateForm, TransactionCreateForm


def index(request):
    return render(request, 'index.html')


class PayerListView(ListView):
    model = Payer
    template_name = 'payer_list.html'


class PayerCreate(CreateView):
    model = Payer
    template_name = 'payer_create_form.html'
    form_class = PayerCreateForm
    
    
class PayerUpdate(UpdateView):
  model = Payer
  template_name = "payer_update_form.html"
  form_class = PayerUpdateForm


class PayerDelete(DeleteView):
  model = Payer
  template_name = "payer_delete_form.html"
  success_url = "/"
  

class TransactionListView(ListView):
    model = Transaction
    template_name = 'transaction_list.html'
    queryset = Transaction.objects.all().order_by("timestamp")
    

class TransactionCreate(CreateView):
    model = Transaction
    template_name = 'transaction_create_form.html'
    form_class = TransactionCreateForm
    
    
class TransactionDelete(DeleteView):
  model = Transaction
  template_name = "transaction_delete_form.html"
  success_url = "/"