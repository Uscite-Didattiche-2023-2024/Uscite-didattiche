
from django.urls import path
from .views import (
    HomeView,
    UserPostListView,
    Proposta_gitaListView,
    Proposta_gitaCreateView,
    Proposta_gitaDetailView,
    Proposta_gitaUpdateView,
    Proposta_gitaDeleteView,
)
from . import views


urlpatterns = [

    path('',HomeView.as_view(),name='homepage'),
    path('ProposteList/', Proposta_gitaListView.as_view(), name='proposte'),
    path('proposta/new/', Proposta_gitaCreateView.as_view(), name='proposta-create'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('proposta/<int:pk>/', Proposta_gitaDetailView.as_view(), name='proposta-detail'),
    path('proposta/<int:pk>/update/', Proposta_gitaUpdateView.as_view(), name='proposta-update'),
    path('proposta/<int:pk>/delete/', Proposta_gitaDeleteView.as_view(), name='proposta-delete'),
    path('about/', views.about, name='gite-about'),
]
