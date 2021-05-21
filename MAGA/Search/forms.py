from .models import item
from django import forms


class itemForm(forms.ModelForm):
    class Meta:
        model = item
        fields = ('title', 'detail')

        widgets = {
            'asin' : forms.TextInput(attrs={'class':'form-control'}),
            'reviewText' : forms.TextInput(attrs={'class':'form-control'}),
            'description' : forms.TextInput(attrs={'class':'form-control'}),
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'image': forms.TextInput(attrs={'class':'form-control'}),
        }
