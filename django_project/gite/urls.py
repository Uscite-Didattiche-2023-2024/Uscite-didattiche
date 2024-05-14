
from django.urls import path
from .views import (
    HomeView,
    UserPostListView,
    Proposta_gitaListView,
    Proposta_gitaCreateView,
    Proposta_gitaDetailView,
    Proposta_gitaUpdateView,
    Proposta_gitaDeleteView,
    CalendarioView,
    conferma_proposta,
    rifiuta_proposta,
    GiteListView,
    GiteDetailView
)
from . import views


urlpatterns = [

    path('',HomeView.as_view(),name='homepage'),
    path('ProposteList/', Proposta_gitaListView.as_view(), name='proposte'),
    path('proposta/new/', Proposta_gitaCreateView.as_view(), name='proposta-create'),
    path('proposta/<int:pk>/', Proposta_gitaDetailView.as_view(), name='proposta-detail'),
    path('proposta/<int:pk>/update/', Proposta_gitaUpdateView.as_view(), name='proposta-update'),
    path('proposta/<int:pk>/delete/', Proposta_gitaDeleteView.as_view(), name='proposta-delete'),
    path('proposta/<int:pk>/conferma/', conferma_proposta, name='conferma-proposta'),
    path('proposta/<int:pk>/rifiuta/', rifiuta_proposta, name='rifiuta-proposta'),
    path('calendario/', CalendarioView.as_view(), name='calendario'),
    path('gite/', GiteListView.as_view(), name='gite'),
    path('gite/<int:pk>/', GiteDetailView.as_view(), name='gite-detail'),
    path('about/', views.about, name='gite-about'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
]
