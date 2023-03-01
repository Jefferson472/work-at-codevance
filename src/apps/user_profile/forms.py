from allauth.account.forms import SignupForm
from django import forms

from apps.user_profile.models import Supplier


class CustomSignupForm(SignupForm):
    name = forms.CharField(max_length=55)
    cnpj = forms.CharField(max_length=14)

    class Meta:
        model = Supplier
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Razão Social'
        self.fields['cnpj'].widget.attrs['placeholder'] = 'CNPJ'
