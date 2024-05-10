
from django.urls import path
from .views import (
    HomeView,
    LogView,
    Proposta_gitaListView,
    Proposta_gitaCreateView,
    PostListView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)
from . import views


urlpatterns = [

    path('',HomeView.as_view(),name='homepage'),
    path('ProposteList/', Proposta_gitaListView.as_view(), name='proposte'),
    path('proposta/new/', Proposta_gitaCreateView.as_view(), name='proposta-create'),
    path('new/', LogView.as_view(), name='home-logged'),    
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='gite-about'),
]
