from django.urls import path

from apps.pages.views.HomePage import HomePage


urlpatterns = [
    path('', HomePage.as_view(), name='home_page'),
]
