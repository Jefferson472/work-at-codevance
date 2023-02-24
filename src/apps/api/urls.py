from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.api.views import PaymentListView


router = routers.DefaultRouter()
router.register('payments', PaymentListView)

urlpatterns = [
    # auth
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # endpoints
    path('payments/', PaymentListView.as_view(), name='api_payment_list'),
]
