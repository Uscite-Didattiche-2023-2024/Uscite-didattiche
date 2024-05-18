from django import forms
from .models import Gita, Proposta_Gita

class GitaForm(forms.ModelForm):
    class Meta:
        model = Gita
        fields = ['Stato', 'Data_ritrovo', 'Data_rientro', 'Luogo_ritrovo', 'Luogo_rientro', 'Proposta_Gita', 'Allegato']
        widgets = {
            'Data_ritrovo': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'Data_rientro': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class PropostaGitaForm(forms.ModelForm):
    class Meta:
        model = Proposta_Gita
        fields = ['Titolo', 'Descrizione', 'Data', 'Posto', 'Costo', 'Stato']
        widgets = {
            'Data': forms.DateInput(attrs={'type': 'date'}),
            'Costo': forms.NumberInput(attrs={'max': 30000}),
        }