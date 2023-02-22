from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


from apps.payment.models import Payment


class PaymentsListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = 'payment_list.html'
