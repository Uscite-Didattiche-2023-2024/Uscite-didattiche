from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages 
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Gita, Post, Proposta_Gita



def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'gite/home.html', context)



class HomeView(TemplateView):
    template_name = 'gite/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'Home'
    

class CalendarioView(TemplateView):
    template_name = 'gite/calendario.html'
    context_object_name = 'Calendario'

class Proposta_gitaListView(ListView):
    model = Proposta_Gita
    template_name = 'gite/proposte_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'proposte'
    ordering = ['-Data']  # Ordina per data decrescente
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        # Personalizza la query per includere il nome dell'autore
        queryset = queryset.select_related('Creatore').order_by('Data')
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




class Proposta_gitaDetailView(DetailView):
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


class Proposta_gitaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Proposta_Gita
    success_url = reverse_lazy('proposte')
    permission_required = 'gite.delete_proposta_gita'

    def handle_no_permission(self):
        raise PermissionDenied
    
    def test_func(self):
        proposta = self.get_object()
        return self.request.user == proposta.Creatore or self.request.user.has_perm('gite.delete_proposta_gita')
       



def about(request):
    return render(request, 'gite/about.html', {'title': 'About'})



class UserPostListView(ListView):
    model = Post
    template_name = 'gite/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
