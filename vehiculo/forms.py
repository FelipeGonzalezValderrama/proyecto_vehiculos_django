from django import forms
from .models import Vehiculo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#form add vehiculo
class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = [
            "marca",
            "modelo",
            "serial_carroceria",
            "serial_motor",
            "categoria",
            "precio",
        ]

#registro usuarios
class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email")

    def save(self, commit=True):
        user = super(RegistroUsuarioForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
