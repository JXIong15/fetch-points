from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('payer', views.PayerListView.as_view(), name='payers'),
    path("payer/create", views.PayerCreate.as_view(), name="payercreate"),
    path("payer/delete/<pk>", views.PayerDelete.as_view(), name="payerdelete"),
    
    path('transaction', views.TransactionListView.as_view(), name='transactions'),
    path("transaction/create", views.TransactionCreate.as_view(), name="transactioncreate"),

    path('spend', views.SpendListView.as_view(), name='spend'),
    path("spend/create", views.SpendCreate.as_view(), name="spendcreate"),

]