from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.user_profile.view import SupplierSignup


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup/', SupplierSignup.as_view(), name='account_signup'),
    path('accounts/', include('allauth.urls')),
    path('', include('apps.pages.urls')),
    path('', include('apps.payment.urls')),
    path('', include('apps.antecipation.urls')),
    path('api/', include('apps.api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
