# flake8: noqa
from django import forms
from . import models
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

class ContactForm(forms.ModelForm):
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*'
            }
        ),
        required=False
    )

    class Meta:
        model = models.Contact
        fields = (
            'first_name','last_name', 'phone', 'email','category',
            'description', 'picture',
            
        )
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'classe-a classe-b','placeholder': 'Digite o primeiro nome.'
                    }
                ), 
            'last_name': forms.TextInput(
                attrs={
                    'placeholder':'Digite o sobrenome.'
                    }
                ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder':'Digite o e-mail do seu contato.'
                    }
                ),
            'phone': forms.TextInput(
                attrs={
                    'placeholder':'Digite o número do seu contato.'
                    }
                ),
            'description': forms.Textarea(
                attrs={
                    'placeholder':'Faça uma descrição do seu contato.'
                    }
                ),
            }
        
    def clean(self):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name == last_name:
            msg = ValidationError(
                'Primeiro nome não pode ser igual ao segundo',
                code='invalid'
            )
            self.add_error('first_name', msg)
            self.add_error('last_name', msg)

        return super().clean()


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=5
    )
    last_name = forms.CharField(
        required=True,
        min_length=5
    )
    email = forms.EmailField(
        required=True,
        min_length=10
    )
    
    
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'username', 'password1',
            'password2',
        )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('Este e-mail já existe.', code='invalid')
            )

class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.',
        error_messages={
            'min_length': 'Please, add more than 2 letters.'
        }
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.'
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label="Password 2",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Use the same password as before.',
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username',
        )

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        password = cleaned_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('Senhas não coincidem')
                )

        return super().clean()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                'email',
                ValidationError('Este e-mail já existe.', code='invalid')
            )

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                )

        return password1