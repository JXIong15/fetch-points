from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('payer', views.PayerListView, name='payers'),
    path("payer/create", views.PayerCreate.as_view(), name="payercreate"),
    path("payer/update/<pk>", views.PayerUpdate.as_view(), name="payerupdate"),
    path("payer/delete/<pk>", views.PayerDelete.as_view(), name="payerdelete"),
    
    path('transaction', views.TransactionListView, name='transactions'),
    path("transaction/create", views.TransactionCreate.as_view(), name="transactioncreate"),
    path("transaction/delete/<pk>", views.TransactionDelete.as_view(), name="transactiondelete"),
]