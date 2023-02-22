from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from apps.antecipation.forms import RequestAntecipationForm
from apps.antecipation.models import Antecipation, RequestAntecipation, LogTransactions
from apps.user_profile.models import Operator


class BaseListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.has_perm('user_profile.antecipation_view'):
            return queryset.filter(request_antecipation__payment__supplier__user=self.request.user)
        return queryset


class AntecipationsListView(BaseListView):
    model = Antecipation


class RequestAntecipationListView(LoginRequiredMixin, ListView):
    model = RequestAntecipation

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.has_perm('user_profile.antecipation_view'):
            return queryset.filter(payment__supplier__user=self.request.user)
        return queryset


class RequestAntecipationCreateView(LoginRequiredMixin, CreateView):
    model = RequestAntecipation
    form_class = RequestAntecipationForm
    success_url = reverse_lazy('payments_list')

    def form_valid(self, form):
        form.instance.payment_id = self.kwargs['pk']
        form.instance.requester = self.request.user
        form.instance.fee = form.instance.calculated_fee
        return super().form_valid(form)


class LogTransactionsListView(BaseListView):
    model = LogTransactions
