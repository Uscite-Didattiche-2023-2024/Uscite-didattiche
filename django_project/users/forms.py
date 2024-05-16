from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class PasswordResetForm(forms.Form):
    from_email = forms.EmailField(label="From Email")
    to_email = forms.EmailField(label="To Email")

    
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100, required=False)  # Aggiunto campo per il nome
    last_name = forms.CharField(max_length=100, required=False)   # Aggiunto campo per il cognome

    # Opzioni per il campo 'caratteristiche'
    CARATTERISTICHE_CHOICES = [
        ('nessuna', 'Nessuna'),  
        ('dsa', 'DSA'),
        ('disabile', 'Disabile'),
        ('allergico', 'Allergico'),
        # Aggiungi altre opzioni se necessario
    ]

    # Aggiungi il campo 'caratteristiche' come ChoiceField
    caratteristiche = forms.ChoiceField(choices=CARATTERISTICHE_CHOICES, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','first_name','last_name']

    # Override del metodo save per salvare anche i campi extra del profilo
    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']  # Aggiornamento del nome
        user.last_name = self.cleaned_data['last_name']    # Aggiornamento del cognome
        if commit:
            user.save()

            # Se è stato fornito un first_name e un last_name, crea o aggiorna il profilo
            if self.cleaned_data['first_name'] or self.cleaned_data['last_name']:
                profile, created = Profile.objects.get_or_create(user=user)
                profile.caratteristiche = self.cleaned_data['caratteristiche']
                profile.save()

        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']  # Aggiornamento dei campi


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'caratteristiche']
