from django import forms
from django.contrib.auth import get_user_model
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError("Passwords don't match.")

        return cleaned_data

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.filter(email=data)
        if self.instance.pk is not None:
            # editing existing user
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Email already in use.')
        return data


# ... rest of your forms (LoginForm, UserEditForm, ProfileEditForm) ...


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo', 'bio']
