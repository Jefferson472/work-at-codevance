from django.urls import path

from apps.antecipation.views import AntecipationsListView


urlpatterns = [
    path('antecipations/', AntecipationsListView.as_view(), name='antecipations_list'),
]
