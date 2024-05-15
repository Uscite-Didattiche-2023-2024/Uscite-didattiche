
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class PasswordResetForm(forms.Form):
    from_email = forms.EmailField(label="From Email")
    to_email = forms.EmailField(label="To Email")

    
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    # Opzioni per il campo 'caratteristiche'
    CARATTERISTICHE_CHOICES = [
        ('dsa', 'DSA'),
        ('disabile', 'Disabile'),
        ('allergico', 'Allergico'),
        # Aggiungi altre opzioni se necessario
    ]

    # Aggiungi il campo 'caratteristiche' come ChoiceField
    caratteristiche = forms.ChoiceField(choices=CARATTERISTICHE_CHOICES, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # Override del metodo __init__ per aggiungere i campi extra del profilo al form
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['nome'] = forms.CharField(max_length=100, required=False)
        self.fields['cognome'] = forms.CharField(max_length=100, required=False)

     # Override del metodo save per salvare anche i campi extra del profilo
    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.save()
        profile = Profile.objects.create(
            user=user,
            nome=self.cleaned_data.get('nome'),
            cognome=self.cleaned_data.get('cognome'),
            esigenze=self.cleaned_data.get('caratteristiche')  # Utilizza il campo 'caratteristiche'
        )
        if commit:
            profile.save()
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'nome', 'cognome', 'caratteristiche']

