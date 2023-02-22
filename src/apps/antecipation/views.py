from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


from apps.antecipation.models import Antecipation, RequestAntecipation


class AntecipationsListView(LoginRequiredMixin, ListView):
    model = Antecipation


class RequestAntecipationListView(LoginRequiredMixin, ListView):
    model = RequestAntecipation
