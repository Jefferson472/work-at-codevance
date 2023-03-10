from django.urls import path

from apps.antecipation.views import (
    AntecipationsListView,
    RequestAntecipationListView,
    LogTransactionsListView,
    RequestAntecipationCreateView,
    antecipation_approve,
    antecipation_reprove,
)


urlpatterns = [
    path('antecipations/', AntecipationsListView.as_view(), name='antecipations_list'),
    path('antecipations/create/<int:pk>/', RequestAntecipationCreateView.as_view(), name='antecipation_create'),
    path('antecipations-request/', RequestAntecipationListView.as_view(), name='request_antecipations_list'),
    path('antecipations-request/approve/<int:pk>/', antecipation_approve, name='request_antecipations_approve'),
    path('antecipations-request/reprove/<int:pk>/', antecipation_reprove, name='request_antecipations_repprove'),
    path('logs/', LogTransactionsListView.as_view(), name='log_transactions_list'),
]
