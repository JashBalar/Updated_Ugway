from django.urls import path
from .views import start_payment, handle_payment_success

urlpatterns = [
    path('pay/', start_payment, name="payment"),
    path('payment/success/', handle_payment_success, name="payment_success")
]