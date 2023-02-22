from django.urls import path

from apps.payment.views import PaymentsListView, PaymentCreateView


urlpatterns = [
    path('payments/', PaymentsListView.as_view(), name='payments_list'),
    path('payments/create/', PaymentCreateView.as_view(), name='payments_create'),
]
