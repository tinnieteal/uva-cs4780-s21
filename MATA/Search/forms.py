from .models import item
from django import forms


class itemForm(forms.ModelForm):
    class Meta:
        model = item
        fields = ('title', 'detail')

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'detail':forms.TextInput(attrs={'class':'form-control'}),
        }
