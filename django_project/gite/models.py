from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.models import Group
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.conf import settings

# Validatore per caratteri maiuscoli
character = RegexValidator(r'^[A-Z]*$', 'Only CAPS characters are allowed.')

def get_default_group():
    try:
        # Cerca il gruppo vuoto
        group = Group.objects.get(name='')
        return group.id 
    except Group.DoesNotExist:
        return None
    
    
class Classe(models.Model):
    anno = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    sezione = models.CharField(max_length=3, default='', validators=[character])

    def __str__(self):
        return "{}{}".format(self.anno, self.sezione)
        
    class Meta:
        verbose_name_plural = 'Classi'

class Gita(models.Model):
    STATO_CHOICES = (
        ('IN_PROGRAMMA', 'In programma'),
        ('IN_CORSO', 'In corso'),
        ('TERMINATA', 'Terminata'),
    )
    
    Stato = models.CharField(max_length=20, choices=STATO_CHOICES, default='IN_PROGRAMMA')
    Data_ritrovo = models.DateTimeField(null=True, blank=True)
    Data_rientro = models.DateTimeField(null=True, blank=True)
    Luogo_ritrovo = models.CharField(max_length=20)
    Luogo_rientro = models.CharField(max_length=20)
    Proposta_Gita = models.ForeignKey('Proposta_Gita', on_delete=models.CASCADE)
    Allegato = models.FileField(upload_to='documenti/', blank=True, null=True)

    def __str__(self):
        return self.Proposta_Gita.Titolo
        
    class Meta:
        verbose_name_plural = 'Gita'

class Proposta_Gita(models.Model):
    STATO_CHOICES = (
        ('IN_ELABORAZIONE', 'In elaborazione'),
        ('CONFERMATA', 'Confermata'),
        ('RIFIUTATA', 'Rifiutata'),
    )
    Titolo = models.CharField(max_length=20)
    Descrizione = models.CharField(max_length=300)
    Data = models.DateTimeField(null=True, blank=True)
    Posto = models.CharField(max_length=20)
    Costo = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(30000)])
    Stato = models.CharField(max_length=20, choices=STATO_CHOICES, default='IN_ELABORAZIONE')
    Creatore = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.Titolo

    class Meta:
        verbose_name_plural = 'Proposte_Gita'

    def save(self, *args, **kwargs):
        if self.pk is not None:
            original = Proposta_Gita.objects.get(pk=self.pk)
            self.Creatore = original.Creatore
        super(Proposta_Gita, self).save(*args, **kwargs)

class Attività(models.Model):
    STATO_CHOICES = (
        ('IN_ELABORAZIONE', 'In elaborazione'),
        ('CONFERMATA', 'Confermata'),
        ('RIFIUTATA', 'Rifiutata'),
    )
    Titolo = models.CharField(max_length=20)
    Descrizione = models.CharField(max_length=300)
    Costo = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5000)])
    Stato = models.CharField(max_length=20, choices=STATO_CHOICES, default='IN_ELABORAZIONE')
    
    Proposta_Gita = models.ForeignKey('Proposta_Gita', on_delete=models.CASCADE)

    def __str__(self):
        return self.Titolo
        
    class Meta:
        verbose_name_plural = 'Attività'

class Docenti_gita(models.Model):
    Gita = models.ForeignKey('Gita', on_delete=models.CASCADE, default='')
    utente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='')
    
    def __str__(self):
        return "{} - {}".format(self.Gita, self.utente.username)
        
    class Meta:
        verbose_name_plural = 'Docenti_gita'
         
class Documenti(models.Model):
    Titolo = models.CharField(max_length=20)
    Descrizione = models.CharField(max_length=300, default='')
    Gita = models.ForeignKey('Gita', on_delete=models.CASCADE, default='')
    Allegato = models.FileField(upload_to='documenti/', default='')
    groups = models.ManyToManyField(Group, related_name="documenti")

    def __str__(self):
        return self.Titolo

    class Meta:
        verbose_name_plural = 'Documenti'

class Classe_gita(models.Model):
    Gita = models.ForeignKey('Gita', on_delete=models.CASCADE, default='')
    Classe = models.ForeignKey('Classe', on_delete=models.CASCADE, default='')
    def __str__(self):
        return "{} - {}".format(self.Classe, self.Gita)
        
    class Meta:
         verbose_name_plural = 'Classe_gita'

class Presenti_prenotati(models.Model):
    Gita = models.ForeignKey('Gita', on_delete=models.CASCADE, default='')
    utente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='')
    
    def __str__(self):
        return "{} - {}".format(self.Gita, self.utente.username)
        
    class Meta:
        verbose_name_plural = 'Presenti_prenotati'

class Notifica(models.Model):
    Titolo = models.CharField(max_length=20)
    Descrizione = models.CharField(max_length=300, default='')
    Gita = models.ForeignKey('Gita', on_delete=models.CASCADE, default='')
    Proposta_Gita = models.ForeignKey('Proposta_Gita', on_delete=models.CASCADE, default='')
    Classe = models.ManyToManyField('Classe', related_name="notifica")
    Documenti = models.ForeignKey('Documenti', on_delete=models.CASCADE, default='', blank=True, null=True)
    utenti_letto = models.ManyToManyField(User, related_name='notifiche_lette', blank=True)
    groups = models.ManyToManyField(Group, related_name="notifica")

    def __str__(self):
        return self.Titolo

    class Meta:
        verbose_name_plural = 'Notifica'

class User_classe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    classe = models.ForeignKey('Classe', on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.user.username, self.classe)

    class Meta:
        verbose_name_plural = 'User_classe'