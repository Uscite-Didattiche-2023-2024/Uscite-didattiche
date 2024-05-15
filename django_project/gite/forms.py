from django import forms
from .models import Gita

class GitaForm(forms.ModelForm):
    class Meta:
        model = Gita
        fields = ['Stato', 'Data_ritrovo', 'Data_rientro', 'Luogo_ritrovo', 'Luogo_rientro', 'Proposta_Gita']
