from django import forms

from apps.payment.models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
        widgets = {
            'date_due': forms.DateInput(attrs={'type': 'date'}),
        }
