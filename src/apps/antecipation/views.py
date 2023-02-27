from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from apps.antecipation.forms import RequestAntecipationForm
from apps.antecipation.models import Antecipation, RequestAntecipation, LogTransactions
from apps.antecipation.tasks import log_create, send_email
from apps.user_profile.models import Operator


class BaseListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.has_perm('user_profile.antecipation_view'):
            return queryset.filter(req_antecipation__payment__supplier__user=self.request.user)
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
        payment_id = self.kwargs['pk']
        form.instance.payment_id = payment_id
        form.instance.requester = self.request.user
        form.instance.fee = form.instance.calculated_fee
        response = super().form_valid(form)

        log_create.delay(self.object.id, self.request.user.id, type='0')
        msg = 'Pedido de antecipação encaminhado com sucesso!'
        send_email.delay(payment_id, msg)
        return response


class LogTransactionsListView(BaseListView):
    model = LogTransactions


def antecipation_approve(request, **kwargs):
    req_antecipation = RequestAntecipation.objects.get(id=kwargs['pk'])
    req_antecipation.status = '1'
    req_antecipation.save()

    new_value = req_antecipation.payment.value - req_antecipation.fee
    operator = Operator.objects.get(user=request.user)
    Antecipation.objects.create(
        operator=operator,
        req_antecipation=req_antecipation,
        new_value=new_value
    )
    log_create.delay(req_antecipation.id, request.user.id, type='1')
    msg = 'Pedido de antecipação aprovado!'
    send_email.delay(req_antecipation.payment.id, msg)
    return HttpResponseRedirect(reverse_lazy('request_antecipations_list'))


def antecipation_reprove(request, **kwargs):
    req_antecipation = RequestAntecipation.objects.get(id=kwargs['pk'])
    req_antecipation.status = '2'
    req_antecipation.save()

    log_create.delay(req_antecipation.id, request.user.id, type='2')
    msg = 'Pedido de antecipação reprovado!'
    send_email.delay(req_antecipation.payment.id, msg)

    return HttpResponseRedirect(reverse_lazy('request_antecipations_list'))
