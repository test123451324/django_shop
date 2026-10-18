from django import forms 
from .models import Product
class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=[
            "name","price","category","available","rate","description","stock","image"
        ]
class LoginForm(forms.Form):
    username=forms.CharField(label="login", max_length=150)
    password=forms.CharField(label="password", widget=forms.PasswordInput) 