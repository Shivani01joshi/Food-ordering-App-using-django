from django import forms

from .models import Pizza # type: ignore
class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = '__all__'
        
    