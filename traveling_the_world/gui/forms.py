from django import forms
from .models import Destination


class AddDestinationForm(forms.ModelForm):

    class Meta:
        model = Destination
        fields = ('destination_name', 'country', 'list_name')