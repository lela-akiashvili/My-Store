from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "მომხმარებლის სახელი"
        self.fields['email'].label = "ელ-ფოსტა"
        
        # ავტომატურად ვადებთ bootstrap კლასებს ლამაზი UI-სთვის
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "მომხმარებლის სახელი"
        self.fields['password'].label = "პაროლი"
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'