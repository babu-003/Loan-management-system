from django.urls import path

from . import views

app_name = "investments"

urlpatterns = [
    path("", views.investor_list, name="investor_list"),
    path("add/", views.investor_add, name="investor_add"),
    path("<int:pk>/", views.investor_detail, name="investor_detail"),
    path("deposit/", views.deposit_add, name="deposit_add"),
    path("ledger/", views.ledger_list, name="ledger_list"),
]
