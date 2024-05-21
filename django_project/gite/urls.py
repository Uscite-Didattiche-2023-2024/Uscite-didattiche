from django.urls import path
from .views import (
    HomeView,
    Proposta_gitaListView,
    Proposta_gitaCreateView,
    Proposta_gitaDetailView,
    Proposta_gitaUpdateView,
    Proposta_gitaDeleteView,
    GitaCreateView,
    Conferma_proposta,
    Rifiuta_proposta,
    GiteListView,
    GiteDetailView,
    GitaUpdateView,
    GitaDeleteView,
    ProfiloDetailView,
    CalendarioView,
)
from . import views

urlpatterns = [
    # Homepage
    path("", HomeView.as_view(), name="homepage"),
    # Proposta
    path("ProposteList/", Proposta_gitaListView.as_view(), name="proposte"),
    path("proposta/new/", Proposta_gitaCreateView.as_view(), name="proposta-create"),
    path(
        "proposta/<int:pk>/", Proposta_gitaDetailView.as_view(), name="proposta-detail"
    ),
    path(
        "proposta/<int:pk>/update/",
        Proposta_gitaUpdateView.as_view(),
        name="proposta-update",
    ),
    path(
        "proposta/<int:pk>/delete/",
        Proposta_gitaDeleteView.as_view(),
        name="proposta-delete",
    ),
    path(
        "proposta/<int:pk>/conferma/",
        Conferma_proposta.as_view(),
        name="conferma-proposta",
    ),
    path(
        "proposta/<int:pk>/rifiuta/",
        Rifiuta_proposta.as_view(),
        name="rifiuta-proposta",
    ),
    # Profilo utente
    path(
        "profilo-utente/<int:pk>/", ProfiloDetailView.as_view(), name="profilo-utente"
    ),
    # Gita
    path("gita/new/", GitaCreateView.as_view(), name="gita-create"),
    path("gite/", GiteListView.as_view(), name="gite"),
    path("gite/<int:pk>/", GiteDetailView.as_view(), name="gite-detail"),
    path("gita/details/<int:gita_id>/", views.gita_details, name="gita-details"),
    path("gita/<int:pk>/update/", GitaUpdateView.as_view(), name="gita-update"),
    path("gita/<int:pk>/delete/", GitaDeleteView.as_view(), name="gita-delete"),
    path(
        "notifiche/letto/<int:notifica_id>/",
        views.segna_come_letto,
        name="segna_come_letto",
    ),
    # Calendario
    path("calendario/", CalendarioView.as_view(), name="calendario"),
    # About
    path("aboutus/", views.aboutUs, name="gite-aboutUs"),
]
