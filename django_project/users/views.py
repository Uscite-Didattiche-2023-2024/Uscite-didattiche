from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

from gite.models import Notifica

class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'users/password_reset.html'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        # Ottieni l'indirizzo email fornito dall'utente
        from_email = form.cleaned_data.get('from_email')
        # Imposta il mittente dell'email
        self.from_email = from_email
        # Invia l'email di reset della password
        self.send_mail(form.cleaned_data["email"], self.get_email_context(form.cleaned_data["email"]))
        return super().form_valid(form)

    def send_mail(self, email, context):
        subject = self.get_email_subject()
        message = self.render_email_template(self.get_email_template_name(), context)
        send_mail(subject, message, self.from_email, [email])

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    # Ottieni il contesto dei dati dalle notifiche
    notifiche = Notifica.objects.all()

    return render(request, 'users/register.html', {'form': form, 'notifiche': notifiche})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    notifiche = Notifica.objects.all()

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'notifiche': notifiche,  # Aggiungi le notifiche al contesto
    }

    return render(request, 'users/profile.html', context)
