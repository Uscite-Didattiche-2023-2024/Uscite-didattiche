from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Proposta_Gita


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'gite/home.html', context)

class HomeView(TemplateView):
    template_name = 'gite/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'Home'
    
class LogView(TemplateView):
    template_name = 'gite/logged.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'Logged'

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
    
class UserPostListView(ListView):
    model = Post
    template_name = 'gite/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class Proposta_gitaDetailView(DetailView):
    model = Proposta_Gita

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aggiungi tutti gli attributi necessari al contesto
        context['creatore'] = self.object.Creatore
        context['titolo'] = self.object.Titolo
        context['data'] = self.object.Data
        context['descrizione'] = self.object.Descrizione
        context['posto'] = self.object.Posto
        context['costo'] = self.object.Costo
        context['stato'] = self.object.get_Stato_display()
        return context



class Proposta_gitaCreateView(LoginRequiredMixin, CreateView):
    model = Proposta_Gita
    fields = ['Titolo', 'Descrizione', 'Data', 'Posto', 'Costo', 'Stato']  

    def form_valid(self, form):
        form.instance.Creatore = self.request.user  
        messages.success(self.request, 'Gita creata con successo!')  # TOFIX
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('proposte') 
    

class Proposta_gitaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Proposta_Gita
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class Proposta_gitaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Proposta_Gita
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'gite/about.html', {'title': 'About'})

