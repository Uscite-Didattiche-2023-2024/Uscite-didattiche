from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from gite.models import Classe, User_classe

class PasswordResetForm(forms.Form):
    from_email = forms.EmailField(label="From Email")
    to_email = forms.EmailField(label="To Email")

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    classe = forms.ModelChoiceField(queryset=Classe.objects.all(), required=False)
    CARATTERISTICHE_CHOICES = [
        ("nessuna", "Nessuna"),
        ("dsa", "DSA"),
        ("invalido", "Invalido"),
        ("allergico", "Allergico"),
    ]
    caratteristiche = forms.ChoiceField(choices=CARATTERISTICHE_CHOICES, required=False)
    dettagli = forms.CharField(max_length=100, required=False, label="Tipi di Allergie")

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "classe",
            "caratteristiche",
            "dettagli",
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("L'email è già in uso.")
        return email

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.caratteristiche = self.cleaned_data["caratteristiche"]
            if self.cleaned_data["caratteristiche"] in ["allergico", "invalido"]:
                profile.dettagli = self.cleaned_data["dettagli"]
            else:
                profile.dettagli = ""
            profile.save()
            if self.cleaned_data["classe"]:
                user_classe = User_classe(user=user, classe=self.cleaned_data["classe"])
                user_classe.save()
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image", "caratteristiche", "dettagli"]
