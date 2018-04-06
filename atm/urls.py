from django.urls import path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('pin/', views.PinView.as_view(), name='pin'),
    path('transaction/', views.TransactionView.as_view(), name='transaction'),
    path('transaction/balance/', views.BalanceView.as_view(), name='balance'),
    path('transaction/withdrawal/', views.WithdrawalView.as_view(), name='withdrawal'),
    path('transaction/deposit/', views.DepositView.as_view(), name='deposit'),
]