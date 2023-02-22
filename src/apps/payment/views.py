from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from apps.payment.models import Payment
from apps.payment.forms import PaymentForm


class PaymentsListView(LoginRequiredMixin, ListView):
    model = Payment


class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    success_url = reverse_lazy('payments_list')
