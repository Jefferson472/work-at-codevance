from allauth.account.views import SignupView
from django.urls import reverse
from django.http import HttpResponseRedirect

from apps.user_profile.models import Supplier
from apps.user_profile.forms import CustomSignupForm
from apps.core.models import CustomUser


class SupplierSignup(SignupView):
    def post(self, request, *args, **kwargs):
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save(request)
            user = CustomUser.objects.get(email=form.data['email'])
            Supplier.objects.create(user=user, name=form.data['name'], cnpj=form.data['cnpj'])
            return HttpResponseRedirect(reverse('payments_list'))
        return super().post(request, *args, **kwargs)
