from django.urls import path

from apps.payment.views import PaymentsListView


urlpatterns = [
    path('payments/', PaymentsListView.as_view(), name='payments_list'),
]
