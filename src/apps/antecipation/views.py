from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from apps.antecipation.forms import RequestAntecipationForm
from apps.antecipation.models import Antecipation, RequestAntecipation, LogTransactions


class AntecipationsListView(LoginRequiredMixin, ListView):
    model = Antecipation


class RequestAntecipationListView(LoginRequiredMixin, ListView):
    model = RequestAntecipation


class RequestAntecipationCreateView(LoginRequiredMixin, CreateView):
    model = RequestAntecipation
    form_class = RequestAntecipationForm
    success_url = reverse_lazy('payments_list')

    def form_valid(self, form):
        form.instance.payment_id = self.kwargs['pk']
        form.instance.requester = self.request.user
        return super().form_valid(form)


class LogTransactionsListView(LoginRequiredMixin, ListView):
    model = LogTransactions
