from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView


class HomePage(TemplateView):
    template_name = 'dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('account_login'))
        return super().dispatch(request, *args, **kwargs)
