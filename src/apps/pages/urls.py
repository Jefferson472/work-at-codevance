from django.urls import path

from apps.pages.views.HomePage import HomePage
from apps.pages.views.PaymentsViews import PaymentsListView


urlpatterns = [
    path('', HomePage.as_view(), name='home_page'),
    path('payments/', PaymentsListView.as_view(), name='payments_list'),
]
