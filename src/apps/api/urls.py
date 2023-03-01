from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.api.views import PaymentListView, RequestAntecipationCreateAPIView


router = routers.DefaultRouter()
router.register('payments', PaymentListView)

urlpatterns = [
    # auth
    path('api-auth/', include('rest_framework.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # endpoints
    path('payments/', PaymentListView.as_view(), name='api_payment_list'),
    path('payments/<str:status>/', PaymentListView.as_view(), name='api_payment_list_status'),
    path('antecipation/create/', RequestAntecipationCreateAPIView.as_view(), name='request_antecipation_create'),
]
