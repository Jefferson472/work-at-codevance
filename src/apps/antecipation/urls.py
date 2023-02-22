from django.urls import path

from apps.antecipation.views import AntecipationsListView, RequestAntecipationListView


urlpatterns = [
    path('antecipations/', AntecipationsListView.as_view(), name='antecipations_list'),
    path('antecipations-request/', RequestAntecipationListView.as_view(), name='request_antecipations_list'),
]
