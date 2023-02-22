from django import forms

from apps.antecipation.models import RequestAntecipation


class RequestAntecipationForm(forms.ModelForm):
    class Meta:
        model = RequestAntecipation
        fields = ('request_date',)
        widgets = {
            'request_date': forms.DateInput(attrs={'type': 'date'}),
        }
