from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect

from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView

from .models import Payer, Transaction, Spend
from .forms import PayerCreateForm, TransactionCreateForm, SpendCreateForm


def index(request):
    return render(request, 'index.html')


class PayerListView(ListView):
    model = Payer
    template_name = 'payer_list.html'


class PayerCreate(CreateView):
    model = Payer
    template_name = 'payer_create_form.html'
    form_class = PayerCreateForm


class PayerDelete(DeleteView):
  model = Payer
  template_name = "payer_delete_form.html"
  success_url = "/payer"
  

class TransactionListView(ListView):
    model = Transaction
    template_name = 'transaction_list.html'
    queryset = Transaction.objects.all().order_by("timestamp")
    

class TransactionCreate(CreateView):
    model = Transaction
    template_name = 'transaction_create_form.html'
    form_class = TransactionCreateForm
    payers = Payer.objects.all()

    # calculates new player points
    def post(self, request, *args, **kwargs):
        new_points = int(request.POST.get("points"))
        payer_id = request.POST.get("payer")
        payer = self.payers.get(id=payer_id)
        new_payer_total = payer.total_points + new_points

        # checks if payer has enough points
        if new_payer_total < 0:
            text = "Not enough points. " + str(payer.name) +" only has " + str(payer.total_points) + " available."
            messages.error(request, text)
            return HttpResponseRedirect('/transaction/create')

        payer.total_points = new_payer_total
        payer.save()
        self.object = None
        return super().post(request, *args, **kwargs)


class SpendListView(ListView):
    model = Spend
    template_name = 'spend_list.html'

    # def get_queryset(self):
    #     return


class SpendCreate(CreateView):
    model = Spend
    template_name = 'spend_create_form.html'
    form_class = SpendCreateForm
    transactions = Transaction.objects.all().order_by("timestamp")

    def post(self, request, *args, **kwargs):
        spending = int(request.POST.get("points"))
        total_transaction_points = sum(self.transactions.values_list("points", flat=True))

        # checks to make sure we have enough spending power
        if spending > total_transaction_points:
            text = "Not enough points. We only have " + str(total_transaction_points) + " available."
            messages.error(request, text)
            return HttpResponseRedirect('/spend/create')

        for transaction in self.transactions:
            payer = transaction.payer

            if transaction.points <= spending:
                spending -= transaction.points
                payer.total_points -= transaction.points
                transaction.delete()
            else:
                payer.total_points -= spending
                transaction.points -= spending
                transaction.save()
                spending = 0

            payer.save()

        self.object = None
        return super().post(request, *args, **kwargs)

    # redirect to payers list