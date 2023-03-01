from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import RedirectView


class HomePage(RedirectView):
    url = reverse_lazy('payments_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('account_login'))
        return super().dispatch(request, *args, **kwargs)
