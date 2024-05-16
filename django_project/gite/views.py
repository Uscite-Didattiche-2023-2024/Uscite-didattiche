from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib import messages 
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from django.forms.models import model_to_dict
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import View

from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import GitaForm
from .models import Classe, Classe_gita, Gita, Post, Proposta_Gita, Notifica

class HomeView(TemplateView):
    template_name = 'gite/home.html'  # <app>/<model>_<viewtype>.html


class CalendarioView(LoginRequiredMixin, ListView):
    model = Gita
    template_name = 'gite/calendario.html'
    context_object_name = 'Calendario'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('Data_ritrovo')

        # Personalizza la query per includere il nome dell'autore
        return queryset
    
    
class Proposta_gitaListView(LoginRequiredMixin, ListView):
    model = Proposta_Gita
    template_name = 'gite/proposte_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'proposte'
    ordering = ['-Data']  # Ordina per data decrescente
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('Data')
        queryset = queryset.order_by('Stato')

        # Personalizza la query per includere il nome dell'autore
        return queryset
    
class Proposta_gitaCreateView(LoginRequiredMixin, CreateView):
    model = Proposta_Gita
    fields = ['Titolo', 'Descrizione', 'Data', 'Posto', 'Costo', 'Stato']  

    def form_valid(self, form):
        form.instance.Creatore = self.request.user  
        messages.success(self.request, 'Gita creata con successo!')  # TOFIX
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('proposte')
    
class Proposta_gitaDetailView(LoginRequiredMixin, DetailView):
    model = Proposta_Gita

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Passa l'intero oggetto Proposta_Gita al contesto
        context['proposta'] = self.object
        
        return context

class Proposta_gitaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Proposta_Gita
    fields = ['Titolo', 'Descrizione', 'Data', 'Posto', 'Costo', 'Stato'] 
    success_url = reverse_lazy('proposte')
    permission_required = 'gite.change_proposta_gita'

    def form_valid(self, form):
        form.instance.Creatore = self.request.user
        return super().form_valid(form)

    def test_func(self):
        proposta = self.get_object()
        return self.request.user == proposta.Creatore or self.request.user.has_perm('gite.change_proposta_gita')
    
    def handle_no_permission(self):
        raise PermissionDenied
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proposta'] = self.get_object()  # Aggiungi la proposta al contesto
        
        return context

class GitaCreateView(LoginRequiredMixin, CreateView):
    model = Gita
    fields = ['Stato', 'Data_ritrovo', 'Data_rientro', 'Luogo_ritrovo', 'Luogo_rientro', 'Proposta_Gita']
    permission_required = 'gite.add_gita'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm(self.permission_required):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.Creatore = self.request.user
        # Salva la gita
        self.object = form.save()
        # Ottieni le classi selezionate dalla form
        classi_selezionate = self.request.POST.getlist('classi')
        # Crea le entità classe_gita per ciascuna classe selezionata
        for classe_id in classi_selezionate:
            classe_gita = Classe_gita.objects.create(Gita=self.object, Classe_id=classe_id)
            classe_gita.save()
        messages.success(self.request, 'Gita creata con successo!')
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        proposta_gita_id = self.request.GET.get('proposta_gita_id')
        if proposta_gita_id:
            initial['Proposta_Gita'] = proposta_gita_id
        return initial

    def get_success_url(self):
        return reverse_lazy('gite')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classi'] = Classe.objects.all()  # Aggiungi le classi al contesto
        
        return context

class Conferma_proposta(LoginRequiredMixin, View):
    def get(self, request, pk):
        proposta = get_object_or_404(Proposta_Gita, pk=pk)
        proposta.Stato = 'CONFERMATA'
        proposta.save()
        notifiche = Notifica.objects.all()  # Ottieni le notifiche
        return redirect(reverse('gita-create') + f'?proposta_gita_id={proposta.id}')

class Rifiuta_proposta(LoginRequiredMixin, View):
    def get(self, request, pk):
        proposta = get_object_or_404(Proposta_Gita, pk=pk)
        proposta.Stato = 'RIFIUTATA'
        proposta.save()
        notifiche = Notifica.objects.all()  # Ottieni le notifiche
        return render(request, 'gite/proposta_gita_detail.html', {'proposta': proposta, 'notifiche': notifiche})


class Proposta_gitaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Proposta_Gita
    success_url = reverse_lazy('proposte')
    permission_required = 'gite.delete_proposta_gita'

    def handle_no_permission(self):
        raise PermissionDenied
    
    def test_func(self):
        proposta = self.get_object()
        return self.request.user == proposta.Creatore or self.request.user.has_perm('gite.delete_proposta_gita')
       
class GitaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Gita
    form_class = GitaForm  # Usa il form personalizzato se ne hai uno
    template_name = 'gite/gita_form.html'  # Assicurati di specificare il tuo template
    success_url = reverse_lazy('gite')
    permission_required = 'gite.change_gita'

    def form_valid(self, form):
        form.instance.Creatore = self.request.user
        # Salva la gita
        self.object = form.save()
        # Ottieni le classi selezionate dalla form
        classi_selezionate = self.request.POST.getlist('classi')
        # Ottieni le classi gia' associate alla gita
        classi_gita_esistenti = Classe_gita.objects.filter(Gita=self.object)
        # Crea le entità classe_gita per ciascuna classe selezionata nella form
        for classe_id in classi_selezionate:
            Classe_gita.objects.get_or_create(Gita=self.object, Classe_id=classe_id)
        # Elimina le entità classe_gita per le classi deselezionate
        classi_da_elimare = classi_gita_esistenti.exclude(Classe_id__in=classi_selezionate)
        classi_da_elimare.delete()
        return super().form_valid(form)

    def test_func(self):
        proposta = self.get_object()
        return self.request.user.has_perm('gite.change_gita')
    
    def handle_no_permission(self):
        raise PermissionDenied
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classi'] = Classe.objects.all()  # Aggiungi le classi al contesto
        return context

class GitaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Gita
    success_url = reverse_lazy('gite')
    permission_required = 'gite.delete_gita'

    def handle_no_permission(self):
        raise PermissionDenied
    
    def test_func(self):
        proposta = self.get_object()
        return self.request.user.has_perm('gite.delete_gita')
    
def aboutUs(request):
    notifiche = Notifica.objects.all()
    return render(request, 'gite/aboutUs.html', {'title': 'AboutUs','notifiche': notifiche})

class GiteListView(LoginRequiredMixin, ListView):
    model = Gita
    template_name = 'gite/gite_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'gite'
    ordering = ['-Data_ritrovo']  # Ordina per Data_ritrovo decrescente
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        # Personalizza la query per includere il nome dell'autore
        queryset = queryset.select_related('Proposta_Gita__Creatore').order_by('-Data_ritrovo')
        return queryset
    
class GiteDetailView(LoginRequiredMixin, DetailView):
    model = Gita

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Passa l'intero oggetto Gite al contesto
        context['gita'] = self.object
        return context

class UserPostListView(ListView):
    model = Post
    template_name = 'gite/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
    

class ProfiloDetailView(LoginRequiredMixin, DetailView):
    model = User 
    template_name = 'gite/profilo_utente_detail.html'  # <app>/<model>_<viewtype>.html

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object 
        return context