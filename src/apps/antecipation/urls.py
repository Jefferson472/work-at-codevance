from django.urls import path

from apps.antecipation.views import (
    AntecipationsListView, RequestAntecipationListView, LogTransactionsListView, RequestAntecipationCreateView
)


urlpatterns = [
    path('antecipations/', AntecipationsListView.as_view(), name='antecipations_list'),
    path('antecipations/create/<int:pk>/', RequestAntecipationCreateView.as_view(), name='antecipation_create'),
    path('antecipations-request/', RequestAntecipationListView.as_view(), name='request_antecipations_list'),
    path('logs/', LogTransactionsListView.as_view(), name='log_transactions_list'),
]
