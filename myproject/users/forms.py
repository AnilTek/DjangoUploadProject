from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True  # Email zorunlu
        self.fields['email'].label = 'Email'
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu email adresi zaten kullanılıyor.")
        return email


class LoginForm(AuthenticationForm):
    
    username = forms.EmailField(
        label="Email", 
        widget=forms.EmailInput(attrs={'placeholder': 'Email adresinizi giriniz'})
    )