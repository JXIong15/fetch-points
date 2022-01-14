from django.urls import path, include
from .viewsets import PayerViewSet, TransactionViewSet, SpendViewSet, BalanceViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('payer', PayerViewSet, basename='payer')
router.register('transaction', TransactionViewSet, basename='transaction')
router.register('spend', SpendViewSet, basename='spend')
router.register('balance', BalanceViewSet, basename='balance')

urlpatterns = [
    path('', include(router.urls))
]